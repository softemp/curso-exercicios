#!/usr/bin/env python3
"""
Lint do Cofre de Neurônios — valida o contrato do WIKI_SCHEMA.md.

Checagens:
  1. Frontmatter mínimo (type/status/tags/created) em cada neurônio.
  2. status ∈ vocabulário canônico (seedling, incubating, evergreen, archived).
  3. Todo neurônio é referenciado em ≥1 MOC sob 30_Atlas/ (sem órfãos).
  4. Wikilinks resolvíveis (ignora crase inline e blocos cercados).
  5. Taxonomia de tags (lê 50_System/Tags_Taxonomy.md): toda tag ∈ vocabulário;
     exatamente 1 `status/<x>` == campo status; ≥1 `area/`; ≥1 `tipo/`. `source` ausente → aviso.
  6. Toda fonte em 40_Archive/ linka ≥1 neurônio (não fica solta no grafo).

Advisories (não-fatais, backlog de qualidade): [estrutura], [frescor] e
  [linha] (citação por linha `arquivo.ts:NNN` — viola "citar por símbolo" do CLAUDE.md).

Uso:
  python3 50_System/lint.py          # roda a partir da raiz do Vault
Exit code: 0 se sem erros; 1 se houver violações fatais (1–6, exceto source que é aviso).
"""
import os, re, sys, glob, collections, datetime

# Mapa projeto->repo do symbols.py é a MESMA fonte de verdade que o drift.py usa.
# Serve ao frescor: só é "derivado de código verificável" quem tem repo mapeado.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from symbols import REPO_CANDIDATES
    PROJETOS_COM_REPO = set(REPO_CANDIDATES)
except ImportError:            # symbols.py ausente → não bloqueia o lint
    PROJETOS_COM_REPO = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

STATUS_VALIDOS = {"seedling", "incubating", "evergreen", "archived"}
# tipos derivados de código → devem ter `validated` recente (advisory, não-fatal)
TIPOS_CODIGO = {"tipo/implementacao", "tipo/arquitetura", "tipo/debug"}
FRESCOR_DIAS = 180
FM_MINIMO = {"type", "status", "tags", "created"}

def read(f): return open(f, encoding="utf-8").read()
_fence = re.compile(r"```.*?```", re.S)
_code  = re.compile(r"`[^`]*`")
_wl    = re.compile(r"\[\[([^\]]+)\]\]")
_fm    = re.compile(r"^---\n(.*?)\n---", re.S)
_hier  = re.compile(r"\b(?:status|area|tipo|projeto|linguagem|plataforma)/[a-z0-9-]+")
_cite_linha = re.compile(  # anti-padrão: citar por linha (qualquer fonte de código)
    r"\b[\w./-]+\.(?:ts|tsx|js|jsx|mjs|cjs|vue|svelte|py|php|rb|go|java|kt|"
    r"c|h|cpp|hpp|cs|rs|sql|sh|yml|yaml):\d+")
# proveniência: afirmação FORTE de ausência de comportamento (gap/brecha/proposta não implementada).
# Onde fato e proposta mais se confundem — exige declarar `implemented:` no frontmatter.
_gap_forte = re.compile(
    r"gaps? cr[íi]ticos?|é uma brecha|brecha funcional|n[ãa]o implementad|"
    r"ainda n[ãa]o existe|n[ãa]o existe ainda|n[ãa]o chama|n[ãa]o gera comiss", re.I)
GOV_TAGS = {"meta", "wiki", "governanca"}

def load_taxonomy():
    """Extrai o vocabulário permitido do Tags_Taxonomy.md (fonte única de verdade)."""
    path = "50_System/Tags_Taxonomy.md"
    if not os.path.exists(path):
        return None
    allowed = set(_hier.findall(read(path))) | GOV_TAGS
    return allowed

def wikilinks(text):
    text = _code.sub("", _fence.sub("", text))
    return [m.split("|")[0].split("#")[0].split("/")[-1].strip() for m in _wl.findall(text)]

def parse_tags(body):
    tm = re.search(r"tags:\s*\[(.*?)\]", body, re.S)
    if not tm:
        return []
    return [x.strip().strip("'\"") for x in tm.group(1).split(",") if x.strip()]

def main():
    files   = [f for f in glob.glob("**/*.md", recursive=True) if "/.git/" not in f]
    neurons = [f for f in files if f.startswith("10_Neurons/")]
    notes   = {os.path.splitext(os.path.basename(f))[0] for f in files}
    nn      = {os.path.splitext(os.path.basename(f))[0] for f in neurons}

    errors, warns, advis = [], [], []
    hoje = datetime.date.today()
    allowed = load_taxonomy()
    if allowed is None:
        warns.append("[taxonomia] 50_System/Tags_Taxonomy.md ausente — checagem de tags pulada")

    # Cobertura no Atlas: todo neurônio referenciado em algum mapa
    # (MOCs temáticos OU Index.md, que indexa os neurônios de governança).
    atlas_refs = set()
    for f in glob.glob("30_Atlas/*.md"):
        txt = read(f)
        fmm = _fm.match(txt)
        if fmm and re.search(r"^generated:\s*true", fmm.group(1), re.M):
            continue  # catálogo auto-gerado lista todos os neurônios → não conta p/ órfão
        atlas_refs.update(wikilinks(txt))
    for n in sorted(nn):
        if n not in atlas_refs:
            errors.append(f"[órfão] {n} não está em nenhum mapa do Atlas")

    # frontmatter + status + tags
    for f in sorted(neurons):
        name = os.path.basename(f)
        txt = read(f)
        m = _fm.match(txt)
        if not m:
            errors.append(f"[frontmatter] {name} sem bloco YAML")
            continue
        body = m.group(1)
        fields = set(re.findall(r"^(\w+):", body, re.M))
        faltando = FM_MINIMO - fields
        if faltando:
            errors.append(f"[frontmatter] {name} faltam campos: {sorted(faltando)}")
        sm = re.search(r"status:\s*(\S+)", body)
        status_val = sm.group(1).strip().strip("'\"") if sm else None
        if status_val and status_val not in STATUS_VALIDOS:
            errors.append(f"[status] {name} status inválido: '{status_val}'")
        # source recomendado (aviso)
        if not re.search(r"^source:\s*\S", body, re.M):
            warns.append(f"[source] {name} sem campo 'source'")
        # taxonomia de tags
        if allowed is not None:
            tags = parse_tags(body)
            st = [t for t in tags if t.startswith("status/")]
            areas = [t for t in tags if t.startswith("area/")]
            tipos = [t for t in tags if t.startswith("tipo/")]
            for t in tags:
                if t not in allowed:
                    errors.append(f"[tag] {name} tag fora da taxonomia: '{t}'")
            if len(st) != 1:
                errors.append(f"[tag] {name} precisa de exatamente 1 'status/<x>' (tem {len(st)})")
            elif status_val and st[0] != f"status/{status_val}":
                errors.append(f"[tag] {name} '{st[0]}' não casa com status: '{status_val}'")
            if not areas:
                errors.append(f"[tag] {name} sem nenhuma 'area/<x>'")
            if not tipos:
                errors.append(f"[tag] {name} sem nenhuma 'tipo/<x>'")

        # ── Advisories (informativo, não-fatal) ──
        # estrutura previsível: a convenção do Cofre marca as seções pelo EMOJI
        # (💡 = abertura conceitual, 🛠️ = aplicação prática), permitindo nomes
        # descritivos ("💡 Racional", "🛠️ Receita"). A palavra literal também conta.
        tem_conceito = bool(re.search(r"^##\s+💡", txt, re.M)) or "## Conceito" in txt
        tem_aplicacao = bool(re.search(r"^##\s+🛠", txt, re.M)) or bool(re.search(r"##\s+Aplicação", txt))
        if not tem_conceito:
            advis.append(f"[estrutura] {name} sem seção de abertura (💡 Conceito)")
        elif not tem_aplicacao:
            advis.append(f"[estrutura] {name} sem seção de aplicação (🛠️)")
        # frescor: só cobra `validated` de quem é VERIFICÁVEL contra um repo-fonte.
        # `tipo/arquitetura|debug` sozinho não implica código: um padrão de engenharia
        # ("Idempotencia_App_Mais_Banco") ou uma nota de doc ("Prisma_Json_Defensive")
        # não tem repo contra o que revalidar — cobrar `validated:` deles só gera ruído
        # que dessensibiliza o advisory. O sinal confiável é a tag `projeto/<x>` com
        # repo mapeado em symbols.py — o mesmo critério do drift.py.
        tags_n = set(parse_tags(body))
        projs = {t.split("/", 1)[1] for t in tags_n if t.startswith("projeto/")}
        if PROJETOS_COM_REPO is None:
            verificavel = bool(projs)      # sem o mapa, qualquer projeto conta
        else:
            verificavel = bool(projs & PROJETOS_COM_REPO)
        # projeto real cujo repo ninguém mapeou: o buraco é o MAPA, não o neurônio
        if allowed is not None and (tags_n & TIPOS_CODIGO) and projs and not verificavel:
            falta = ", ".join(sorted(projs))
            advis.append(f"[repo] {name} (projeto/{falta}) sem repo em symbols.py — frescor não verificável")
        if allowed is not None and (tags_n & TIPOS_CODIGO) and verificavel:
            vm = re.search(r"^validated:\s*(\d{4}-\d{2}-\d{2})", body, re.M)
            if not vm:
                advis.append(f"[frescor] {name} (código) sem 'validated:'")
            else:
                try:
                    d = datetime.date.fromisoformat(vm.group(1))
                    idade = (hoje - d).days
                    if idade > FRESCOR_DIAS:
                        advis.append(f"[frescor] {name} validado há {idade}d (> {FRESCOR_DIAS})")
                except ValueError:
                    advis.append(f"[frescor] {name} 'validated' inválido: {vm.group(1)}")
        # citar por símbolo, não por linha: `arquivo.ts:178` apodrece (CLAUDE.md)
        linhas = _cite_linha.findall(txt)
        if linhas:
            amostra = ", ".join(sorted(set(linhas))[:3])
            extra = " …" if len(set(linhas)) > 3 else ""
            advis.append(f"[linha] {name} cita por linha ({len(linhas)}x): {amostra}{extra}")
        # proveniência: neurônio de código que afirma um gap/brecha deve declarar `implemented:`
        # (true|false|partial) — evita que o agente leia proposta como comportamento real.
        if (set(parse_tags(body)) & TIPOS_CODIGO) and _gap_forte.search(txt) \
                and not re.search(r"^implemented:", body, re.M):
            advis.append(f"[proveniencia] {name} afirma gap/brecha sem 'implemented:' no frontmatter")

    # wikilinks quebrados (templates têm placeholders intencionais → ignorados)
    for f in sorted(files):
        if "50_System/Templates/" in f:
            continue
        for t in wikilinks(read(f)):
            if t not in notes:
                errors.append(f"[link] {os.path.basename(f)} → [[{t}]] inexistente")

    # fontes arquivadas soltas: toda fonte em 40_Archive/ deve linkar ≥1 neurônio
    # (senão fica desconectada do grafo Obsidian). Crase NÃO conta (wikilinks() a remove).
    for f in sorted(glob.glob("40_Archive/*.md")):
        if not (set(wikilinks(read(f))) & nn):
            errors.append(f"[fonte-solta] {os.path.basename(f)} não linka nenhum neurônio (40_Archive)")

    print(f"Neurônios: {len(neurons)} | Notas totais: {len(files)}")
    print(f"Erros: {len(errors)} | Avisos: {len(warns)}\n")
    for e in errors: print("  ERRO  ", e)
    for w in warns:  print("  aviso ", w)
    if not errors and not warns:
        print("  ✓ Cofre íntegro: sem órfãos, frontmatter válido, links resolvíveis.")
    # advisories informativos (não afetam o status nem o exit code)
    if advis and "--no-advis" not in sys.argv:
        cats = collections.Counter(a.split("]")[0][1:] for a in advis)
        print(f"\nℹ️  Advisory (não-fatal, qualidade): {len(advis)} — " +
              ", ".join(f"{k} {v}" for k, v in cats.most_common()))
        if "-v" in sys.argv or "--verbose" in sys.argv:
            for a in advis: print("  ·", a)
        else:
            print("  (use -v para detalhar; backlog de melhoria de frescor/estrutura)")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())

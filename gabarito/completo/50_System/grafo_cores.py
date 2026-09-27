#!/usr/bin/env python3
"""
grafo_cores.py — cores do Graph View a partir de UMA fonte (50_System/grafo_cores.json).

Gera dois artefatos, para nunca mais editar os dois à mão:
  1. `colorGroups` em .obsidian/graph.json (só esse array; o resto do arquivo é preservado);
  2. 30_Atlas/Legenda_Cores_Grafo.md (generated: true), com a contagem real de notas por grupo.

Uso:  python3 50_System/grafo_cores.py [--podar] [--dry-run] [--root DIR]
  --podar    omite dos artefatos os grupos que não casam nenhuma nota (vault derivado);
  --dry-run  só imprime o relatório;
  --root     raiz do vault (padrão: pasta-mãe deste script; usado pelos testes).
Relata sempre: notas por grupo, grupos vazios e tags `projeto/*` com notas mas sem grupo.
Ver [[Cofre_Grafo_Cores_Configuracao_Versionada]].
"""
import argparse, datetime, glob, json, os, re, sys

_FM = re.compile(r"^---\n(.*?)\n---", re.S)
_TAGS = re.compile(r"tags:\s*\[(.*?)\]", re.S)
LEGENDA_REL = os.path.join("30_Atlas", "Legenda_Cores_Grafo.md")
GRAPH_REL = os.path.join(".obsidian", "graph.json")
FONTE_REL = os.path.join("50_System", "grafo_cores.json")
GRAPH_MINIMO = {"collapse-filter": True, "search": "", "showTags": False, "showAttachments": False,
                "hideUnresolved": False, "showOrphans": True, "collapse-color-groups": False,
                "colorGroups": [], "collapse-display": True, "showArrow": False,
                "textFadeMultiplier": 0, "nodeSizeMultiplier": 1, "lineSizeMultiplier": 1,
                "collapse-forces": True, "centerStrength": 0.5, "repelStrength": 10,
                "linkStrength": 1, "linkDistance": 250, "scale": 1, "close": True}


def ler(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def notas(root):
    """(caminho relativo, nome sem extensão, tags) de toda nota .md do vault fora de .git."""
    out = []
    for p in glob.glob(os.path.join(root, "**", "*.md"), recursive=True):
        rel = os.path.relpath(p, root)
        if rel.startswith(".git" + os.sep):
            continue
        m = _FM.match(ler(p))
        tags = []
        if m:
            tm = _TAGS.search(m.group(1))
            if tm:
                tags = [t.strip().strip("'\"") for t in tm.group(1).split(",") if t.strip()]
        out.append((rel, os.path.splitext(os.path.basename(p))[0], tags))
    return out


def query(g):
    partes = [f"file:{p}" for p in g.get("prefixos", [])]
    partes += [f"tag:#{t}" for t in g.get("tags", [])]
    partes += [f"path:{p}" for p in g.get("paths", [])]
    return " OR ".join(partes)


def casa(g, rel, nome, tags):
    return (any(nome.startswith(p) for p in g.get("prefixos", []))
            or any(t in tags for t in g.get("tags", []))
            or any(rel == p or rel.startswith(p.rstrip("/") + os.sep) for p in g.get("paths", [])))


def rgb(hex_cor):
    return int(hex_cor.lstrip("#"), 16)


def contar(grupos, todas):
    """Notas por grupo com a regra do Obsidian: cada nota conta só no PRIMEIRO grupo que casa."""
    c = {g["id"]: 0 for g in grupos}
    for rel, nome, tags in todas:
        for g in grupos:
            if casa(g, rel, nome, tags):
                c[g["id"]] += 1
                break
    return c


def tags_sem_grupo(grupos, todas):
    cobertas = {t for g in grupos for t in g.get("tags", [])}
    usadas = {}
    for rel, nome, tags in todas:
        if rel.startswith(os.path.join("50_System", "Templates") + os.sep):
            continue  # placeholders (`projeto/`) dos templates não são notas reais
        for t in tags:
            if t.startswith("projeto/") and t not in cobertas and not any(casa(g, rel, nome, tags) for g in grupos):
                usadas[t] = usadas.get(t, 0) + 1
    return usadas


def legenda_md(grupos, contagem, hoje):
    L = ["---", "type: reference", "generated: true", "status: evergreen",
         "tags: [meta, grafo, obsidian, navegacao]", f"created: {hoje}", "---",
         "# 🎨 Legenda de Cores do Grafo (Obsidian)", "",
         "> ⚠️ **Arquivo gerado** por `50_System/grafo_cores.py` a partir de `50_System/grafo_cores.json` — "
         f"não editar à mão. Última geração: **{hoje}**.", "",
         "Convenção de cores do **Graph View** para localizar projetos e domínios de relance. A fonte é o JSON; "
         "o script reescreve `colorGroups` em `.obsidian/graph.json` (versionado, viaja com o vault) e esta "
         "nota. Decisão e limites em [[Cofre_Grafo_Cores_Configuracao_Versionada]].", "",
         "## 🗂️ Esquema", "",
         "| Cor | Hex | Domínio / Projeto | Query (gerada) | Notas (1º grupo que casa) |",
         "|---|---|---|---|---|"]
    for g in grupos:
        L.append(f"| {g['emoji']} | `{g['cor']}` | **{g['nome']}** | `{query(g)}` | {contagem[g['id']]} |")
    L += ["", "Notas fora desses grupos (padrões transversais como `Idempotencia_*`, `Canvas_*`) ficam na cor "
          "neutra — por desenho, para os projetos saltarem aos olhos.", "",
          "## 🛠️ Como alterar", "",
          "1. Edite `50_System/grafo_cores.json` (novo grupo = `id`, `emoji`, `cor`, `nome`, `prefixos`/`tags`/`paths`).",
          "2. Rode `python3 50_System/grafo_cores.py` com o Obsidian **fechado** (aberto, ele sobrescreve o `graph.json` ao salvar).",
          "3. Confira o relatório: grupo com 0 notas ou tag `projeto/*` sem grupo é sinal de JSON desatualizado.", "",
          "## 🔗 Conexões",
          "- Índice: [[Index]] · catálogo: [[Catalogo_Neuronios]] · clusters de projeto: [[MOC_Projetos]].",
          "- Política de portabilidade: [[Cofre_Grafo_Cores_Configuracao_Versionada]].", ""]
    return "\n".join(L)


def gerar(root, podar=False, dry_run=False, hoje=None):
    hoje = hoje or datetime.date.today().isoformat()
    with open(os.path.join(root, FONTE_REL), encoding="utf-8") as f:
        grupos = json.load(f)["grupos"]
    todas = notas(root)
    contagem = contar(grupos, todas)
    vazios = [g["id"] for g in grupos if contagem[g["id"]] == 0]
    orfas = tags_sem_grupo(grupos, todas)
    ativos = [g for g in grupos if not (podar and contagem[g["id"]] == 0)]

    for g in grupos:
        marca = "  (vazio" + (", podado)" if podar else ")") if contagem[g["id"]] == 0 else ""
        print(f"  {g['emoji']:<14} {g['id']:<16} {contagem[g['id']]:>4} notas{marca}")
    if orfas:
        print("  ⚠️  tags projeto/* com notas e sem grupo: " + ", ".join(f"{t} ({n})" for t, n in sorted(orfas.items())))
    if dry_run:
        return {"contagem": contagem, "vazios": vazios, "orfas": orfas}

    gpath = os.path.join(root, GRAPH_REL)
    graph = dict(GRAPH_MINIMO)
    if os.path.exists(gpath):
        with open(gpath, encoding="utf-8") as f:
            graph = json.load(f)
    graph["colorGroups"] = [{"query": query(g), "color": {"a": 1, "rgb": rgb(g["cor"])}} for g in ativos]
    os.makedirs(os.path.dirname(gpath), exist_ok=True)
    with open(gpath, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with open(os.path.join(root, LEGENDA_REL), "w", encoding="utf-8") as f:
        f.write(legenda_md(ativos, contagem, hoje))
    print(f"✓ {len(ativos)} grupos → {GRAPH_REL} e {LEGENDA_REL}")
    return {"contagem": contagem, "vazios": vazios, "orfas": orfas}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cores do Graph View a partir de grafo_cores.json.")
    ap.add_argument("--podar", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args(argv)
    gerar(a.root, podar=a.podar, dry_run=a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())

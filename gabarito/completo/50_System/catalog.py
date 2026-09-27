#!/usr/bin/env python3
"""
Gerador de catálogo do Cofre de Neurônios.

Lê todos os neurônios em 10_Neurons/ e produz um índice navegável único em
`30_Atlas/Catalogo_Neuronios.md` — pensado para entender o acervo inteiro num
arquivo só: panorama (contagens), visão por projeto/fonte, visão por MOC com a
frase-conceito de cada neurônio, e índice de tags (tópico → neurônios).

O arquivo gerado leva `generated: true` no frontmatter; o `lint.py` ignora
arquivos gerados ao calcular cobertura do Atlas (senão o catálogo — que lista
todos os neurônios — mascararia órfãos reais).

Uso:
  python3 50_System/catalog.py        # gera/atualiza o catálogo (roda da raiz)
"""
import os, re, glob, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OUT = "30_Atlas/Catalogo_Neuronios.md"

STATUS_EMOJI = {"seedling": "🌱", "growing": "🌿", "evergreen": "🌳", "archived": "🗄️"}
MOC_ORDER = [
    "MOC_Projetos", "MOC_ProjetoBC", "MOC_Financeiro",
    "MOC_Desenvolvimento", "MOC_Frontend", "MOC_Infraestrutura", "MOC_WhatsApp",
]

_fm    = re.compile(r"^---\n(.*?)\n---", re.S)
_wl    = re.compile(r"\[\[([^\]]+)\]\]")
_fence = re.compile(r"```.*?```", re.S)
_code  = re.compile(r"`[^`]*`")

def read(f): return open(f, encoding="utf-8").read()

def strip_code(s): return _code.sub("", _fence.sub("", s))

def field(body, name):
    m = re.search(rf"^{name}:\s*(.+)$", body, re.M)
    return m.group(1).strip() if m else None

def tags_of(body):
    m = re.search(r"tags:\s*\[(.*?)\]", body, re.S)
    if not m: return []
    return [t.strip().strip("'\"") for t in m.group(1).split(",") if t.strip()]

def mocs_of(text):
    # linha "- MOC:" ou "- MOC Pai:" no rodapé Conexões (ignora crase/exemplos)
    text = strip_code(text)
    m = re.search(r"^- MOC(?: Pai)?:\s*(.+)$", text, re.M)
    if not m: return []
    return [x.split("|")[0].strip() for x in _wl.findall(m.group(1))
            if x.split("|")[0].strip().startswith("MOC_")]

def clean(s):
    s = _wl.sub(lambda m: m.group(1).split("|")[-1].split("/")[-1], s)  # [[a|b]] -> b
    s = re.sub(r"[`*_]", "", s)                                          # md inline
    s = re.sub(r"\s+", " ", s).strip()
    return s

def concept(text):
    body = _fm.sub("", text, count=1)
    m = re.search(r"##+\s*(?:💡\s*)?Conceito\s*\n(.*?)(?=\n##\s|\Z)", body, re.S)
    chunk = m.group(1) if m else body
    para = []
    for ln in chunk.splitlines():
        s = ln.strip()
        if not s:
            if para: break
            continue
        if s[0] in "#>|" or s.startswith("```") or s.startswith("- ") or s.startswith("!["):
            if para: break
            continue
        para.append(s)
    txt = clean(" ".join(para))
    if not txt: return "—"
    cut = txt.split(". ")[0]
    if len(cut) > 180:
        cut = cut[:180].rsplit(" ", 1)[0] + "…"
    elif len(txt) > len(cut) + 1:
        cut += "."
    return cut

def main():
    neurons = {}
    for f in sorted(glob.glob("10_Neurons/*.md")):
        name = os.path.splitext(os.path.basename(f))[0]
        text = read(f)
        fmm = _fm.match(text)
        body = fmm.group(1) if fmm else ""
        neurons[name] = {
            "status": (field(body, "status") or "seedling"),
            "source": field(body, "source"),
            "tags": tags_of(body),
            "mocs": mocs_of(text) or ["(sem MOC)"],
            "concept": concept(text),
        }

    n = len(neurons)
    archives = [f for f in glob.glob("40_Archive/*.md")]
    by_status = collections.Counter(d["status"] for d in neurons.values())

    # por MOC (um neurônio pode aparecer em mais de um MOC que declara)
    by_moc = collections.defaultdict(list)
    for name, d in neurons.items():
        for moc in d["mocs"]:
            by_moc[moc].append(name)
    moc_sorted = [m for m in MOC_ORDER if m in by_moc] + \
                 sorted(m for m in by_moc if m not in MOC_ORDER)

    # por projeto (tag projeto/<x>; sem tag = conhecimento transversal)
    def proj(d):
        for t in d["tags"]:
            if t.startswith("projeto/"):
                return t.split("/", 1)[1]
        return "Padrões gerais (sem projeto)"
    by_proj = collections.defaultdict(list)
    for name, d in neurons.items():
        by_proj[proj(d)].append(name)

    # índice de tags (>=2 usos indexam; 1 uso vira nota de rodapé)
    by_tag = collections.defaultdict(list)
    for name, d in neurons.items():
        for t in d["tags"]:
            by_tag[t].append(name)
    multi = sorted(((t, ns) for t, ns in by_tag.items() if len(ns) >= 2),
                   key=lambda x: (-len(x[1]), x[0]))
    singles = sorted(t for t, ns in by_tag.items() if len(ns) == 1)

    today = datetime.date.today().isoformat()
    L = []
    L.append("---")
    L.append("type: catalog")
    L.append("generated: true")
    L.append("status: evergreen")
    L.append("tags: [meta, indice, catalogo]")
    L.append(f"created: {today}")
    L.append("---")
    L.append("# 📇 Catálogo de Neurônios")
    L.append("")
    L.append(f"> ⚠️ **Arquivo gerado** por `50_System/catalog.py` — não editar à mão. "
             f"Regenere após cada ingest. Última geração: **{today}**.")
    L.append("")
    L.append("Ponto de entrada único para navegar todo o acervo: panorama, por projeto, "
             "por MOC (com a frase-conceito de cada neurônio) e por tag. Para o mapa curado "
             "e a governança, ver [[Index]].")
    L.append("")

    L.append("## 📊 Panorama")
    L.append(f"- **{n} neurônios** · {len(archives)} fontes arquivadas · {len(by_tag)} tags distintas.")
    st = " · ".join(f"{STATUS_EMOJI.get(s,'')} {s} {by_status[s]}"
                    for s in ["seedling","growing","evergreen","archived"] if by_status.get(s))
    L.append(f"- Maturidade: {st}.")
    L.append(f"- Por MOC: " + " · ".join(f"[[{m}]] {len(by_moc[m])}" for m in moc_sorted if m != "(sem MOC)") + ".")
    L.append("")

    L.append("## 🗂️ Por Projeto / Fonte")
    for p in sorted(by_proj, key=lambda x: (x.startswith("Padrões"), -len(by_proj[x]), x)):
        names = sorted(by_proj[p])
        L.append(f"### {p} ({len(names)})")
        L.append(", ".join(f"[[{x}]]" for x in names))
        L.append("")

    L.append("## 🧭 Por MOC")
    for moc in moc_sorted:
        names = sorted(by_moc[moc])
        title = f"[[{moc}]]" if moc != "(sem MOC)" else "(sem MOC declarado)"
        L.append(f"### {title} ({len(names)})")
        for x in names:
            d = neurons[x]
            L.append(f"- {STATUS_EMOJI.get(d['status'],'')} [[{x}]] — {d['concept']}")
        L.append("")

    L.append("## 🏷️ Índice de Tags")
    L.append("*Tags com ≥2 neurônios (as de uso único não indexam — listadas ao fim).*")
    L.append("")
    for t, ns in multi:
        L.append(f"- **{t}** ({len(ns)}): " + ", ".join(f"[[{x}]]" for x in sorted(ns)))
    if singles:
        L.append("")
        L.append("> Uso único: " + " · ".join(f"`{t}`" for t in singles))
    L.append("")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    print(f"✓ Catálogo gerado: {OUT}  ({n} neurônios, {len(moc_sorted)} MOCs, {len(by_tag)} tags)")

if __name__ == "__main__":
    main()

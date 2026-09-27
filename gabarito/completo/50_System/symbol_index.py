#!/usr/bin/env python3
"""
symbol_index.py — gera o Índice Reverso de Símbolos:  arquivo-fonte → neurônios que o cobrem.

Usa o mesmo parser (symbols.py) do drift.py. Enquanto o drift verifica "o símbolo ainda existe?",
o índice responde a pergunta inversa, de RECALL: "vou mexer em `WithdrawalService.ts` — o que o
cérebro já sabe sobre isso?". Transforma o protocolo de consulta (passo 0) em algo determinístico
e disparado pelo arquivo que se vai tocar, em vez de depender de lembrar de grepar.

Saída: 30_Atlas/Indice_Simbolos.md (gerado; `generated: true` → o lint não o trata como órfão).

Uso:
  python3 50_System/symbol_index.py            # regenera o índice
  python3 50_System/symbol_index.py <arquivo>  # consulta rápida no terminal (ex.: WithdrawalService.ts)
"""
import sys, os, collections
import symbols as S

OUT = os.path.join(S.ROOT, "30_Atlas", "Indice_Simbolos.md")

def build():
    # projeto -> arquivo -> { simbolo -> set(neuronios) }
    tree = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(set)))
    n_refs = 0
    for n in S.all_neurons():
        proj = n["project"] or "—sem-projeto—"
        for sym, _method, fname in n["refs"]:
            tree[proj][fname][sym].add(n["name"])
            n_refs += 1
    return tree, n_refs

def render(tree, n_refs):
    L = []
    L.append("---")
    L.append("type: index")
    L.append("status: evergreen")
    L.append("tags: [meta, wiki]")
    L.append("generated: true")
    L.append('summary: "Índice reverso arquivo-fonte → neurônios (gerado por symbol_index.py). '
             'Pre-flight: antes de tocar um arquivo, veja o que o cérebro já sabe."')
    L.append("---")
    L.append("# 🧭 Índice de Símbolos — arquivo-fonte → neurônios\n")
    L.append("> **Gerado** por `50_System/symbol_index.py`. Não editar à mão.")
    L.append("> **Uso (pre-flight):** antes de editar um arquivo do código, localize-o aqui (Ctrl+F pelo "
             "nome do arquivo) e **leia os neurônios listados antes de mexer**. Cada linha mostra o símbolo "
             "citado e o(s) neurônio(s) que o cobrem.\n")
    total_files = sum(len(files) for files in tree.values())
    L.append(f"*Cobertura: {n_refs} citações por símbolo · {total_files} arquivos-fonte · "
             f"{len(tree)} projetos.*\n")
    for proj in sorted(tree):
        L.append(f"\n## 📂 {proj}\n")
        for fname in sorted(tree[proj]):
            L.append(f"### `{fname}`")
            for sym in sorted(tree[proj][fname]):
                neurons = " · ".join(f"[[{x}]]" for x in sorted(tree[proj][fname][sym]))
                L.append(f"- `{sym}` → {neurons}")
            L.append("")
    return "\n".join(L) + "\n"

def query(term):
    tree, _ = build()
    hits = []
    for proj, files in tree.items():
        for fname, syms in files.items():
            if term.lower() in fname.lower():
                for sym, neurons in syms.items():
                    hits.append((proj, fname, sym, sorted(neurons)))
    if not hits:
        print(f"Nenhum neurônio cobre '{term}'.")
        return
    print(f"🧭 '{term}' — o cérebro já sabe:\n")
    for proj, fname, sym, neurons in sorted(hits):
        print(f"  [{proj}] {fname} :: {sym}")
        for nm in neurons:
            print(f"      → {nm}")

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if args:
        query(args[0]); return 0
    tree, n_refs = build()
    open(OUT, "w", encoding="utf-8").write(render(tree, n_refs))
    total_files = sum(len(f) for f in tree.values())
    print(f"✓ Índice gerado: {os.path.relpath(OUT, S.ROOT)} "
          f"({n_refs} citações · {total_files} arquivos · {len(tree)} projetos)")
    return 0

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main())

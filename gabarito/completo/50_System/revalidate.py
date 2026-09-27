#!/usr/bin/env python3
"""
Relatório de re-validação — lista neurônios derivados de código (tipo/implementacao|
arquitetura|debug) que precisam ser reconferidos contra o repositório-fonte: sem
`validated:` ou validados há mais de FRESCOR_DIAS. Agrupa por projeto.

Não altera nada — só reporta. Alimenta a skill `revalidar` (parte agêntica) e o cron mensal.

Uso:
  python3 50_System/revalidate.py            # todos os projetos
  python3 50_System/revalidate.py wbot       # só um projeto (slug da tag projeto/)
"""
import os, re, glob, sys, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FRESCOR_DIAS = 180
TIPOS_CODIGO = {"tipo/implementacao", "tipo/arquitetura", "tipo/debug"}
_fm = re.compile(r"^---\n(.*?)\n---", re.S)
hoje = datetime.date.today()

def main():
    alvo = sys.argv[1].lower() if len(sys.argv) > 1 else None
    por_proj = collections.defaultdict(list)
    for f in sorted(glob.glob("10_Neurons/*.md")):
        m = _fm.match(open(f, encoding="utf-8").read())
        if not m:
            continue
        head = m.group(1)
        tm = re.search(r"tags:\s*\[(.*?)\]", head, re.S)
        tags = [t.strip() for t in (tm.group(1).split(",") if tm else []) if t.strip()]
        if not (set(tags) & TIPOS_CODIGO):
            continue
        proj = next((t.split("/")[1] for t in tags if t.startswith("projeto/")), "—transversal—")
        if alvo and proj != alvo:
            continue
        vm = re.search(r"^validated:\s*(\d{4}-\d{2}-\d{2})", head, re.M)
        if not vm:
            por_proj[proj].append((9999, os.path.basename(f)[:-3], "sem validated"))
        else:
            idade = (hoje - datetime.date.fromisoformat(vm.group(1))).days
            if idade > FRESCOR_DIAS:
                por_proj[proj].append((idade, os.path.basename(f)[:-3], f"{idade}d"))

    total = sum(len(v) for v in por_proj.values())
    print(f"🔁 Re-validação — {total} neurônio(s) de código a reconferir (> {FRESCOR_DIAS}d ou sem validated)\n")
    if not total:
        print("  ✓ Tudo fresco — nada a re-validar.")
        return 0
    for proj in sorted(por_proj, key=lambda p: -len(por_proj[p])):
        itens = sorted(por_proj[proj], reverse=True)
        print(f"  [{proj}] ({len(itens)})")
        for _, name, why in itens:
            print(f"    · {name}  ({why})")
    print(f"\n→ Para reconferir um projeto: skill `revalidar <projeto>` (ou EXTRACAO_PROJETO passo de validação).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

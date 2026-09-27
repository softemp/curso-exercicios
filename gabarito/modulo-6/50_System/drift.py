#!/usr/bin/env python3
"""
drift.py — detecta drift REAL (não por idade) entre neurônios e o código-fonte.

Para cada neurônio com `projeto/<x>` cujo repo está mapeado em symbols.REPOS, verifica
cada citação por símbolo (`Service.metodo()` em `arquivo.ts`):
  - o arquivo citado ainda existe no repo?              (sumiu → drift forte)
  - o método/função citado ainda existe nesse arquivo?  (sumiu → drift)
Símbolos sem `()` (rotas, campos, eventos) são contados como "não-verificáveis" e não
geram drift (evita falso positivo).

Complementa o revalidate.py (que prioriza por IDADE): aqui priorizamos por MUDANÇA real.
Saída: neurônios com drift primeiro. Exit 0 sempre (relatório, não-fatal).

Uso:
  python3 50_System/drift.py [projeto]      # opcional: filtra por um projeto
  python3 50_System/drift.py -v             # lista também as âncoras OK
"""
import sys, re, os
import symbols as S

def grep_method(file_paths, method):
    """True se o identificador aparece como definição/uso em algum dos arquivos."""
    pat = re.compile(r"\b" + re.escape(method) + r"\b")
    for fp in file_paths:
        try:
            if pat.search(S.read(fp)):
                return True
        except Exception:
            continue
    return False

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    verbose = "-v" in sys.argv
    only = args[0] if args else None

    total_refs = total_ok = total_drift = total_unver = 0
    total_files = total_files_ok = 0
    drift_neurons = []    # (name, project, [drift forte])   — símbolo/arquivo de âncora sumiu
    review_neurons = []   # (name, project, [revisar])       — citação isolada não-resolvida
    skipped_no_repo = {}
    skipped_proposal = 0

    for n in S.all_neurons():
        proj = n["project"]
        if not (n["refs"] or n["files"]):
            continue
        if only and proj != only:
            continue
        # neurônio de proposta (gap não implementado): cita arquivos/símbolos que SERÃO criados → não é drift
        if n.get("implemented") == "false":
            skipped_proposal += 1
            continue
        repo = S.REPOS.get(proj)
        if not repo or not os.path.isdir(repo):
            if proj:
                skipped_no_repo[proj] = skipped_no_repo.get(proj, 0) + 1
            continue
        idx = S.repo_files(repo)
        drift, review, ok, unver, fok = [], [], 0, 0, 0
        # (a) pares símbolo+arquivo: arquivo existe? símbolo ainda lá?  (drift FORTE)
        for sym, method, fname in n["refs"]:
            total_refs += 1
            paths = idx.get(fname, [])
            if not paths:
                drift.append(f"arquivo sumiu: {fname}  (citado: {sym})")
                continue
            if method is None:
                unver += 1
                continue
            if grep_method(paths, method):
                ok += 1
            else:
                drift.append(f"símbolo sumiu: {method}  em {fname}  (citado: {sym})")
        # (b) arquivos citados isoladamente: só EXISTÊNCIA (pula os já cobertos pelos pares) → REVISAR
        ref_files = {fn for _s, _m, fn in n["refs"]}
        for cit, base in n["files"]:
            if base in ref_files:
                continue
            total_files += 1
            if base in idx:
                fok += 1
            else:
                review.append(f"arquivo citado não existe: {cit}")
        total_ok += ok; total_unver += unver; total_files_ok += fok
        total_drift += len(drift)
        if drift:
            drift_neurons.append((n["name"], proj, drift))
        if review:
            review_neurons.append((n["name"], proj, review))
        if verbose and (ok or fok) and not drift:
            print(f"  ✓ {n['name']} [{proj}] — {ok} símbolo(s) OK, {fok} arquivo(s) OK, "
                  f"{unver} não-verificável(is)")

    print(f"\n🔬 Drift contra código:")
    print(f"   símbolos: {total_refs} (✓ {total_ok} OK · ◽ {total_unver} não-verificáveis)")
    print(f"   arquivos: {total_files} (✓ {total_files_ok} existem)")
    print(f"   ⚠️ {total_drift} drift forte · 🔍 {sum(len(r[2]) for r in review_neurons)} a revisar\n")
    if drift_neurons:
        print(f"⚠️  DRIFT FORTE — {len(drift_neurons)} neurônio(s) (símbolo/arquivo de âncora sumiu; revalidar já):\n")
        for name, proj, probs in sorted(drift_neurons, key=lambda x: -len(x[2])):
            print(f"  ● {name} [{proj}]")
            for p in probs:
                print(f"      - {p}")
        print()
    else:
        print("  ✓ Nenhum drift forte (todos os símbolos/arquivos de âncora presentes).\n")
    if review_neurons:
        print(f"🔍 A REVISAR — {len(review_neurons)} neurônio(s) com citação isolada não-resolvida "
              f"(pode ser lib externa, casing ou arquivo movido):\n")
        for name, proj, probs in sorted(review_neurons, key=lambda x: -len(x[2])):
            print(f"  · {name} [{proj}]: " + "; ".join(p.replace("arquivo citado não existe: ", "") for p in probs))
    if skipped_proposal:
        print(f"\nℹ️  {skipped_proposal} neurônio(s) pulado(s) por 'implemented: false' (proposta, não código atual).")
    if skipped_no_repo:
        print("ℹ️  Projetos sem repo mapeado (não verificados): " +
              ", ".join(f"{k} ({v})" for k, v in sorted(skipped_no_repo.items())))
    return 0

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main())

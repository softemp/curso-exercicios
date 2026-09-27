#!/usr/bin/env bash
# Revisão mensal do Cofre — junta os dois sinais de saúde do conhecimento de código:
#   • frescor (revalidate.py): neurônios stale por IDADE (> 180d / sem validated)
#   • drift   (drift.py):      símbolo/arquivo citado que SUMIU do repo-fonte (mudança real)
# Pensado para o cron mensal (dia 1). Uso manual: bash 50_System/monthly_review.sh
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 1

echo "════════════════════════════════════════════════════════════"
echo " Revisão mensal do Cofre — $(date +'%Y-%m-%d %H:%M')"
echo "════════════════════════════════════════════════════════════"

echo
echo "───── Frescor (idade): revalidate.py ─────"
python3 50_System/revalidate.py || echo "aviso: revalidate.py falhou"

echo
echo "───── Drift (mudança real vs código): drift.py ─────"
python3 50_System/drift.py || echo "aviso: drift.py falhou"

echo
echo "Fim da revisão. Priorize os neurônios com DRIFT (símbolo sumiu) — são certeza de"
echo "desatualização; o frescor por idade é só suspeita. Revalide e bumpe 'validated:'."

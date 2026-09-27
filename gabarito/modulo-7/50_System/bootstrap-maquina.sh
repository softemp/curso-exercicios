#!/usr/bin/env bash
# Prepara ESTA máquina para usar o Cofre a partir de qualquer projeto.
#
# Por que existe: as skills e o CLAUDE.md dos projetos são o GATILHO — sem eles o
# conhecimento do Cofre existe e não é lido (ver Base_Gate_Piso_UI_Novo_Projeto).
# O Cofre viaja por git; ~/.claude/ não viaja. Este script recria o elo local.
#
# Uso, em cada máquina, depois de um `git pull` no Cofre:
#   bash 50_System/bootstrap-maquina.sh
set -euo pipefail

COFRE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_USUARIO="$HOME/.claude/skills"
LISTA="$COFRE/50_System/projetos-com-gatilho.txt"
TEMPLATE="$COFRE/50_System/Templates/CLAUDE_projeto.md"

echo "Cofre: $COFRE"

# ── 1. Ecossistema da máquina (plugins, CLAUDE.md global, skills, hooks, Cartographer) ──
# O manifesto 50_System/ecossistema.json diz o que toda máquina deve ter; o verificador aplica o
# que é seguro e aponta o resto (apt, cron). Ver o neurônio Eco_Paridade_Entre_Maquinas.
python3 "$COFRE/50_System/checar_maquina.py" --corrigir || true

# ── 2. CLAUDE.md nos projetos listados ───────────────────────────────────────
[ -f "$LISTA" ] || { echo "  (sem $LISTA — nada a fazer)"; exit 0; }

while IFS='|' read -r caminho stack; do
  case "$caminho" in ''|\#*) continue ;; esac
  destino="$HOME/$caminho"
  [ -d "$destino" ] || { echo "  projeto — $caminho (não existe nesta máquina)"; continue; }

  if [ -f "$destino/CLAUDE.md" ]; then
    echo "  projeto = $caminho (já tem CLAUDE.md — preservado)"
    continue
  fi

  # Versão real da stack, quando dá para ler do próprio projeto.
  detalhe="$stack"
  if [ -f "$destino/composer.json" ]; then
    versao="$(grep -oE '"laravel/framework": *"[^"]+"' "$destino/composer.json" | grep -oE '[0-9][^"]*' || true)"
    [ -n "$versao" ] && detalhe="$stack (laravel/framework $versao)"
  fi

  python3 - "$TEMPLATE" "$destino/CLAUDE.md" "$(basename "$destino")" "$detalhe" "$COFRE" <<'PY'
import sys
tpl, saida, projeto, stack, cofre = sys.argv[1:6]
texto = open(tpl, encoding='utf-8').read()
texto = texto.replace('{{PROJETO}}', projeto).replace('{{STACK}}', stack).replace('{{COFRE}}', cofre)
open(saida, 'w', encoding='utf-8').write(texto)
PY
  echo "  projeto ✓ $caminho"
done < "$LISTA"

echo "Pronto. Confira a qualquer momento: python3 $COFRE/50_System/checar_maquina.py"

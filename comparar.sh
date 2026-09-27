#!/usr/bin/env bash
# Uso: ./comparar.sh N [caminho-do-seu-cerebro]   (N = 2..8; padrão do vault: .cerebro do .curso.json, senão ~/meu-cerebro)
set -euo pipefail
N="${1:?informe o módulo (2..8)}"
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT="${2:-}"
if [ -z "$VAULT" ]; then
  if [ -f "$AQUI/.curso.json" ]; then
    if command -v jq >/dev/null 2>&1; then
      VAULT="$(jq -r '.cerebro // empty' "$AQUI/.curso.json")"
    else
      echo "· aviso: jq ausente, usando ~/meu-cerebro" >&2
    fi
  fi
  VAULT="${VAULT:-$HOME/meu-cerebro}"
fi
VAULT="${VAULT/#\~/$HOME}"
GAB="$AQUI/gabarito/modulo-$N"
[ -d "$GAB" ] || { echo "gabarito/modulo-$N não existe"; exit 2; }
diff -r \
  --exclude=.git --exclude='workspace*' --exclude=__pycache__ --exclude='*.pyc' \
  --exclude=README.md --exclude=Templates_curso --exclude=Minhas_Memorias.md --exclude=Wiki_Log.md \
  --exclude=settings.local.json --exclude=graph.json --exclude=types.json --exclude=core-plugins-migration.json \
  "$VAULT" "$GAB" && echo "✓ igual ao gabarito do módulo $N"

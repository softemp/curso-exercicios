#!/usr/bin/env bash
# instalar-skill.sh [--remover] — instala a skill /curso como skill global do usuário (spec 3, 3.2).
set -euo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_HOME:-$HOME/.claude}/skills/curso"

if [ "${1:-}" = "--remover" ]; then
  if [ -d "$DEST" ] && [ ! -f "$DEST/exercicios.path" ]; then
    echo "✗ a skill 'curso' em $DEST é de outra origem — não removi." >&2; exit 1
  fi
  rm -rf "$DEST"; echo "✓ skill /curso removida de $DEST"; exit 0
fi
if [ -d "$DEST" ] && [ ! -f "$DEST/exercicios.path" ]; then
  echo "✗ já existe uma skill 'curso' de outra origem em $DEST — não toquei." >&2; exit 1
fi
mkdir -p "$DEST"
cp -r "$AQUI/.claude/skills/curso/." "$DEST/"
printf '%s\n' "$AQUI" > "$DEST/exercicios.path"
echo "✓ skill /curso instalada em $DEST (exercícios: $AQUI)"

#!/usr/bin/env bash
# Instala os git hooks do Cofre (versionados → reinstaláveis após clone).
# Uso: bash 50_System/install-hooks.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_DIR="$ROOT/.git/hooks"

if [ ! -d "$ROOT/.git" ]; then
  echo "✗ $ROOT não é um repositório git (sem .git/)." >&2
  exit 1
fi

mkdir -p "$HOOKS_DIR"

cat > "$HOOKS_DIR/pre-commit" <<'HOOK'
#!/usr/bin/env bash
# Gate de qualidade do Cofre — bloqueia commit se o lint não for 0/0.
# Gerado por 50_System/install-hooks.sh (não edite aqui; edite o instalador).
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if ! command -v python3 >/dev/null 2>&1; then
  echo "⚠️  python3 ausente — pulando lint (commit liberado)." >&2
  exit 0
fi

echo "🔎 lint do Cofre (pre-commit)…"
if ! python3 50_System/lint.py; then
  echo "" >&2
  echo "✗ Commit BLOQUEADO: o lint encontrou erros fatais. Corrija e tente de novo." >&2
  echo "  (rode 'python3 50_System/lint.py -v' p/ detalhes; advisories não bloqueiam)" >&2
  exit 1
fi
HOOK

chmod +x "$HOOKS_DIR/pre-commit"
echo "✓ Hook instalado: $HOOKS_DIR/pre-commit"
echo "  Bloqueia commits quando 'python3 50_System/lint.py' retorna erro fatal."

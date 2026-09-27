#!/usr/bin/env bash
# entrar.sh <cerebro> — sobe um container limpo com o seu cérebro montado em /origem (só leitura).
# Dentro: git clone /origem ~/meu-cerebro && cd ~/meu-cerebro && bash 50_System/bootstrap-maquina.sh
set -euo pipefail
CEREBRO="${1:?uso: entrar.sh <caminho do cérebro>}"
CEREBRO="$(cd "$CEREBRO" && pwd)"
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
docker build -q -t curso-modulo-7 "$AQUI"
exec docker run --rm -it -v "$CEREBRO:/origem:ro" curso-modulo-7 bash

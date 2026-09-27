#!/usr/bin/env bash
# Hook global SessionStart: confere esta máquina contra o manifesto do Cofre
# (50_System/ecossistema.json) e avisa SÓ se algo divergir. Tudo certo = silêncio.
# Rápido de propósito (só leitura local; o `git fetch` do Cofre roda em segundo plano e vale
# para a próxima sessão). Ver o neurônio Eco_Paridade_Entre_Maquinas.
COFRE="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/../.." && pwd)"
exec python3 "$COFRE/50_System/checar_maquina.py" --sessao

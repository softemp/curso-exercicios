#!/usr/bin/env bash
# Hook global UserPromptSubmit: lembra, em todo prompt fora do Cofre, que os padrões SoftEmp vivem
# no Cofre. Versionado no Cofre e registrado no ~/.claude/settings.json pelo checar_maquina.py.
# Ver o neurônio Eco_Gatilho_Cofre_Hook_E_CLAUDE_md.
COFRE="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/../.." && pwd)"
cwd="$(jq -r '.cwd // empty')"
case "$cwd" in "$COFRE"*) exit 0 ;; esac

msg="Padroes de engenharia do operador vivem no Cofre de Neuronios em $COFRE (Vault Obsidian). Antes de criar listagens/tabelas/grids de dados, gerar PDF/impressao, ou decidir stack/estrutura/seguranca, consulte o Cofre: grep em 10_Neurons/ e os hubs em 30_Atlas/ (especialmente [[MOC_Stack_Base]]). Cite os neuronios por [[Nome]] e diga quando o assunto NAO estiver coberto."
jq -cn --arg m "$msg" '{hookSpecificOutput:{hookEventName:"UserPromptSubmit",additionalContext:$m}}'

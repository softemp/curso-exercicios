#!/bin/bash

# Script de Sincronização da Wiki - Claude Code
VAULT_PATH="$HOME/projetos/IA/meu-cerebro"
LOG_FILE="$VAULT_PATH/20_Projects/Wiki_Log.md"

cd "$VAULT_PATH" || exit

# Regenera o catálogo navegável a partir dos neurônios (mantém sempre fresco)
python3 50_System/catalog.py || echo "aviso: catalog.py falhou (segue o sync)"

# Regenera o índice reverso de símbolos (arquivo-fonte → neurônios; pre-flight de consulta)
python3 50_System/symbol_index.py || echo "aviso: symbol_index.py falhou (segue o sync)"

# Regenera as cores do grafo (colorGroups + Legenda) a partir de grafo_cores.json
python3 50_System/grafo_cores.py || echo "aviso: grafo_cores.py falhou (segue o sync)"

# Valida o contrato do Cofre antes de commitar (aborta se houver violação fatal)
if ! python3 50_System/lint.py; then
    echo "Lint falhou — corrija as violações antes de sincronizar."
    exit 1
fi

# Verifica se há mudanças
if [[ -z $(git status -s) ]]; then
    echo "Nenhuma mudança para sincronizar."
    exit 0
fi

# Extrai a última entrada do log para usar como mensagem de commit (opcional)
LAST_LOG=$(grep -m 1 "^## \[" "$LOG_FILE" | sed 's/## //')

echo "Sincronizando mudanças na Wiki..."
git add .

# Tenta usar a última entrada do log, senão usa data/hora
COMMIT_MSG="Wiki Maintenance: ${LAST_LOG:-$(date +'%Y-%m-%d %H:%M')}"

git commit -m "$COMMIT_MSG"

echo "Mudanças registradas com sucesso: $COMMIT_MSG"
# git push # Descomente se houver um remote configurado

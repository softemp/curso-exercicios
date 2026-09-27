#!/usr/bin/env bash
# Backup diário do Cofre de Neurônios com rotação.
# Independente do git: gera um tarball completo (inclui .git) em ~/backups/meu-cerebro.
# Agendado via cron (ver crontab). Ajuste KEEP/horário conforme necessidade.
set -euo pipefail

VAULT_PARENT="$HOME/projetos/IA"
VAULT="meu-cerebro"
DEST="$HOME/backups/meu-cerebro"
KEEP=14                                    # nº de backups a manter (rotação)

mkdir -p "$DEST"
TS="$(date +%Y-%m-%d_%H%M%S)"
FILE="$DEST/meu-cerebro_vault_${TS}.tar.gz"

tar czf "$FILE" -C "$VAULT_PARENT" "$VAULT"
gzip -t "$FILE"                            # falha (set -e) se o tarball estiver corrompido

# Rotação: remove os mais antigos além dos KEEP mais recentes
ls -1t "$DEST"/meu-cerebro_vault_*.tar.gz | tail -n +"$((KEEP + 1))" | xargs -r rm -f

KEPT="$(ls -1 "$DEST"/meu-cerebro_vault_*.tar.gz | wc -l)"
echo "$(date '+%F %T') ok $FILE ($(du -h "$FILE" | cut -f1)) | mantidos: $KEPT" >> "$DEST/backup.log"

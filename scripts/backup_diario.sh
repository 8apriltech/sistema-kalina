#!/bin/bash
set -e

BACKUP_DIR="/root/sistema-kalina/backup"
DB_SRC="/root/sistema-kalina/data/controle.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/controle_backup_${TIMESTAMP}.db"
LOG_FILE="${BACKUP_DIR}/backup.log"

if [ -f "$DB_SRC" ]; then
    cp "$DB_SRC" "$BACKUP_FILE"
    find "$BACKUP_DIR" -type f -name "controle_backup_*.db" -mtime +30 -delete
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Backup realizado com sucesso: ${BACKUP_FILE}" >> "$LOG_FILE"
else
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] ERRO: Arquivo ${DB_SRC} nao encontrado!" >> "$LOG_FILE"
fi

#!/bin/bash

# Variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

DISCORD_WEBHOOK_URL="$DISCORD_WEBHOOK_URL"
BACKUP_DIR="./backups"
DATA_DIR="./data"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/minecraft_backup_$TIMESTAMP.tar.gz"

# Function to send a message to Discord
send_discord_notification() {
    local title="$1"
    local description="$2"
    curl -H "Content-Type: application/json" \
         -X POST \
         -d "{
              \"embeds\": [{
                \"title\": \"$title\",
                \"description\": \"$description\",
                \"color\": 3066993
              }]
            }" \
         "$DISCORD_WEBHOOK_URL"
}

# Notify about backup start
send_discord_notification "Backup Starting" "Players may experience minor lag."

# Create backup
mkdir -p "$BACKUP_DIR"
tar -czvf "$BACKUP_FILE" "$DATA_DIR"
if [ $? -eq 0 ]; then
    send_discord_notification "Backup Successful" "File: $BACKUP_FILE"
else
    send_discord_notification "Backup Failed" "Please check the server logs."
    exit 1
fi

# Clean up old backups (optional)
find "$BACKUP_DIR" -type f -mtime +1 -name "*.tar.gz" -exec rm -f {} \;
send_discord_notification "Recycling Old Backups" ":recycle: Old backups cleaned up (if any)."

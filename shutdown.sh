#!/bin/bash

# Variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

DISCORD_WEBHOOK_URL="$DISCORD_WEBHOOK_URL"
CONTAINER_NAME="minecraft-server"
BACKUP_SCRIPT="./backup.sh"

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

# Start shutdown process
send_discord_notification "Server Shutting Down" ":warning: Running backup before stopping..."

# Run the backup script
if [ -f "$BACKUP_SCRIPT" ]; then
    chmod +x "$BACKUP_SCRIPT"
    "$BACKUP_SCRIPT"
else
    send_discord_notification "Backup Script Not Found" ":x: Skipping backup."
fi

# Stop the Minecraft server
docker stop $CONTAINER_NAME

# Send final Discord notification
send_discord_notification "Server Shut Down" ":octagonal_sign: GG."

echo "Server shutdown complete!"

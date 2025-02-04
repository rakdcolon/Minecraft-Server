#!/bin/bash

# Variables
# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

DISCORD_WEBHOOK_URL="$DISCORD_WEBHOOK_URL"
CONTAINER_NAME="minecraftserver"

get_local_ip() {
    ipconfig getifaddr en0 2>/dev/null || echo "Unknown IP"
}

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

# Check if the container is already running
if docker ps | grep -q "$CONTAINER_NAME"; then
    docker restart $CONTAINER_NAME
else
    docker-compose up -d
fi

LOCAL_IP=$(get_local_ip)

# Send the IP to Discord
if [ -n "$LOCAL_IP" ] && [ "$LOCAL_IP" != "Unknown IP" ]; then
    send_discord_notification "Server Started" ":white_check_mark: Minecraft server is now online! Connect using: **$LOCAL_IP:25565**"
else
    send_discord_notification "Failed to get IP" ":x: Check server connectivity!"
fi

echo "Server started/restarted successfully!"

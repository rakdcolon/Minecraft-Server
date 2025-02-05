from dotenv import load_dotenv
import os
import socket
import requests
import json
import subprocess

def load_environment():
    """
    Load environment variables from a .env file if it exists.
    """
    load_dotenv() # This will read a .env file in the current directory

def get_local_ip():
    """
    Get the local IP address of the machine.
    This function opens a temporary UDP socket to Google's DNS server
    to determine the local IP address.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

def send_discord_notification(title, description):
    """
    Send a Discord notification using the webhook URL.
    The payload is constructed as an embed with a title, description, and a color.
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Discord webhook URL is not set!")
        return

    payload = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": 3066993  # Green-ish color
        }]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        # Discord responds with a 204 status code when successful
        if response.status_code not in (200, 204):
            print("Error sending Discord notification:", response.status_code, response.text)
    except Exception as e:
        print("Exception occurred while sending Discord notification:", e)

def is_container_running(container_name):
    """
    Check if a Docker container is running by looking for the container name
    in the output of 'docker ps'.
    """
    try:
        result = subprocess.run(
            ["docker", "ps"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Check if the container name appears in the output
        return container_name in result.stdout
    except Exception as e:
        print("Error checking Docker containers:", e)
        return False
    
def restart_or_start_container(container_name):
    """
    If the container is running, restart it.
    Otherwise, start the container using docker-compose.
    """
    if is_container_running(container_name):
        print(f"Container '{container_name}' is running. Restarting...")
        subprocess.run(["docker", "restart", container_name])
    else:
        print(f"Container '{container_name}' is not running. Starting via docker-compose...")
        subprocess.run(["docker-compose", "up", "-d"])

def main():
    # Load environment variables from .env file.
    load_environment()

    # Retrieve container name from environment (defaulting to "minecraft-server")
    container_name = os.getenv("CONTAINER_NAME", "minecraft-server")

    # Restart or start the container as needed.
    restart_or_start_container(container_name)

    # Get the local IP address.
    local_ip = get_local_ip()

    # Prepare and send the Discord notification.
    if local_ip is not None:
        message = f":white_check_mark: Minecraft server is now online! Connect using: **{local_ip}:25565**"
        send_discord_notification("Server Started", message)
    else:
        send_discord_notification("Failed to get IP", ":x: Check server connectivity!")
        return

    print("Server started/restarted successfully!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import subprocess
import json
import stat
import sys
import requests
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from the .env file."""
    load_dotenv()

def send_discord_notification(title, description):
    """Send a notification to Discord using a webhook."""
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Discord webhook URL is not set!")
        return

    payload = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": 3066993
        }]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        if response.status_code not in (200, 204):
            print("Error sending Discord notification:", response.status_code, response.text)
    except Exception as e:
        print("Exception occurred while sending Discord notification:", e)

def run_backup_script(backup_script):
    """
    Run the backup script.
    Uses the current Python interpreter (sys.executable) to run a Python backup script.
    """
    if os.path.isfile(backup_script):
        # Ensure the backup script is executable (if necessary)
        st = os.stat(backup_script)
        os.chmod(backup_script, st.st_mode | stat.S_IEXEC)
        try:
            # Run the backup script using the current Python interpreter
            subprocess.run([sys.executable, backup_script], check=True)
        except subprocess.CalledProcessError as e:
            print("Backup script failed:", e)
    else:
        send_discord_notification("Backup Script Not Found", ":x: Skipping backup.")

def stop_container(container_name):
    """Stop the Docker container using 'docker stop'."""
    try:
        subprocess.run(["docker", "stop", container_name], check=True)
    except subprocess.CalledProcessError as e:
        print("Error stopping Docker container:", e)

def main():
    load_environment()

    # Retrieve container name and backup script location from environment variables.
    container_name = os.getenv("CONTAINER_NAME", "minecraft-server")
    # Now default to the Python backup script
    backup_script = os.getenv("BACKUP_SCRIPT", "./backup.py")
    
    # Notify Discord that shutdown is starting and a backup is being performed.
    send_discord_notification("Server Shutting Down", ":warning: Running backup before stopping...")

    # Run the backup script.
    run_backup_script(backup_script)

    # Stop the Docker container.
    stop_container(container_name)

    # Send final shutdown notification.
    send_discord_notification("Server Shut Down", ":octagonal_sign: GG.")
    print("Server shutdown complete!")

if __name__ == "__main__":
    main()

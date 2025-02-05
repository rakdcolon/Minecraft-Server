import os
import tarfile
import time
import datetime
import json
import requests
from dotenv import load_dotenv

def load_environment():
    """
    Load environment variables from the .env file.
    """
    load_dotenv()

def send_discord_notification(title, description):
    """
    Send a notification to Discord using a webhook.
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Discord webhook URL is not set!")
        return

    payload = {
        "embeds": [{
            "title": title,
            "description": description,
            "color": 3066993  # A green-ish color
        }]
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        if response.status_code not in (200, 204):
            print("Error sending Discord notification:", response.status_code, response.text)
    except Exception as e:
        print("Exception occurred while sending Discord notification:", e)

def create_backup():
    # Read configuration from environment variables
    backup_dir = os.getenv("BACKUP_DIR", "./backups")
    data_dir = os.getenv("DATA_DIR", "./data")
    # Create a timestamp in the format YYYYMMDD_HHMMSS
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"minecraft_backup_{timestamp}.tar.gz")

    # Notify users that the backup is starting
    send_discord_notification("Backup Starting", "Players may experience minor lag.")

    # Ensure the backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    try:
        # Create a compressed tar.gz archive of the data directory
        with tarfile.open(backup_file, "w:gz") as tar:
            # Use the basename so that the archive doesn't include the full path.
            tar.add(data_dir, arcname=os.path.basename(data_dir))
        send_discord_notification("Backup Successful", f"File: {backup_file}")
    except Exception as e:
        send_discord_notification("Backup Failed", "Please check the server logs.")
        print("Backup failed:", e)
        return False

    # Clean up old backups: remove any .tar.gz files older than 1 day (86400 seconds)
    now = time.time()
    for filename in os.listdir(backup_dir):
        if filename.endswith(".tar.gz"):
            file_path = os.path.join(backup_dir, filename)
            if os.path.isfile(file_path) and now - os.path.getmtime(file_path) > 86400:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print("Error removing old backup file:", file_path, e)

    send_discord_notification("Recycling Old Backups", ":recycle: Old backups cleaned up (if any).")
    return True

def main():
    load_environment()
    create_backup()

if __name__ == "__main__":
    main()

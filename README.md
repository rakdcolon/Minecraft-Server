# Minecraft Server Manager

This repository provides a set of Python scripts and Docker Compose configuration to manage a modded Minecraft server. The project includes:

- **run.py**: Starts or restarts the Minecraft server container and sends Discord notifications with the server's IP.
- **shutdown.py**: Shuts down the Minecraft server gracefully by running a backup (using `backup.py`), stopping the Docker container, and sending Discord notifications.
- **backup.py**: Creates a timestamped backup of the Minecraft server data, cleans up old backups, and notifies via Discord.
- **docker-compose.yml**: Manages the Docker container for your Minecraft server.

All scripts rely on environment variables loaded from a `.env` file. See the [Environment Variables](#environment-variables) section below.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
  - [Starting/Restarting the Server](#startingrestart-the-server)
  - [Shutting Down the Server](#shutting-down-the-server)
  - [Running a Backup](#running-a-backup)
- [Docker Compose](#docker-compose)
- [Environment Variables](#environment-variables)
- [Additional Notes](#additional-notes)
- [License](#license)

## Requirements

- **Docker**  
  Download and install Docker from the [official Docker website](https://www.docker.com/get-started).

- **Docker Compose**  
  Docker Compose is typically included with Docker Desktop for Windows and Mac. Linux users may need to install it separately.

- **Python 3.7+**  
  Download and install Python from [python.org](https://www.python.org/downloads/).

- **pip**  
  The Python package installer (usually included with Python).

## Setup

1. **Clone the Repository**

    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. **Create a Virtual Environment (Optional but Recommended)**

    ```bash
    python3 -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate
    ```

3. **Install Python Dependencies**

    The project uses the `python-dotenv` and `requests` packages. Install them by running:

    ```bash
    pip install -r requirements.txt
    ```

    *Note: Ensure you have a `requirements.txt` file in your repository containing:*

    ```txt
    python-dotenv
    ```

4. **Create a `.env` File**

    In the repository root, create a `.env` file with the following variables (adjust values as needed):

    ```dotenv
    # Discord webhook URL for notifications
    DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url

    # Name of the Docker container (used by the scripts)
    CONTAINER_NAME=minecraft-server

    # Optionally, override the backup script path (defaults to ./backup.py)
    BACKUP_SCRIPT=./backup.py
    ```

## Usage

### Starting/Restarting the Server

Run the `run.py` script to either restart an existing container or start it using Docker Compose. The script also sends a Discord notification.

```bash
python run.py

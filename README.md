# thesonofmc

Self-hosted Minecraft 1.20.1 Forge server for a 6-player private group. Runs as two Docker services: the game server and an automated backup sidecar.

## Layout

```
.
├── .env                 # version, memory, passwords, retention
├── docker-compose.yml   # minecraft + backup services
├── mods/                # server-side mod jars (read-only mount)
├── config/              # per-mod configs
├── data/                # world + server data (persistent)
├── backups/             # rotated .tgz snapshots
└── MODLIST.md           # tracked modpack
```

See [SETUP.md](SETUP.md) for installation, operations, and troubleshooting.

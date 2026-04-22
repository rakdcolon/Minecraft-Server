# Setup

## Prerequisites

- Docker Engine 24+ with the Compose plugin
- Ports `25566` free on the host (change in `docker-compose.yml` if not)

## First-time install

1. Copy the example env file and fill it in:
   ```bash
   cp .env.example .env
   ```
   Set a real `RCON_PASSWORD`. Review `MEMORY`, `MOTD`, and other settings.
2. Drop Forge 1.20.1 server-side mod jars into [mods/](mods/). Track them in [MODLIST.md](MODLIST.md).
3. Start the stack:
   ```bash
   docker compose up -d
   ```
4. First boot takes a few minutes — Forge downloads, the world generates. Watch progress:
   ```bash
   docker compose logs -f minecraft
   ```
5. Connect in-game at `localhost:25566`.

## Operations

```bash
docker compose up -d                    # start
docker compose down                     # stop
docker compose restart minecraft        # restart game server only
docker compose logs -f minecraft        # tail server logs
docker compose exec minecraft rcon-cli  # in-game console
docker compose exec backup backup now   # force an immediate backup
docker compose pull && docker compose up -d  # update images
```

## Adding or removing mods

1. Drop the Forge 1.20.1 server-compatible jar in `mods/` (or delete it to remove).
2. Update [MODLIST.md](MODLIST.md) with name, version, source, side.
3. Restart the server:
   ```bash
   docker compose restart minecraft
   ```

Client-only mods will crash the server — keep them out of `mods/` and distribute them to players separately.

## Backups

- Runs every `BACKUP_INTERVAL` (default 1h) while players are online, paused when idle.
- Archives land in `./backups/` as `.tgz`, pruned after `BACKUP_PRUNE_DAYS` (default 14).
- Force one at any time with `docker compose exec backup backup now`.

### Restore

1. Stop the stack:
   ```bash
   docker compose down
   ```
2. Move the existing world aside (don't delete until verified):
   ```bash
   mv data/world data/world.bad
   ```
3. Extract the chosen archive into `data/`:
   ```bash
   tar -xzf backups/<archive>.tgz -C data/
   ```
4. Start again:
   ```bash
   docker compose up -d
   ```
5. Verify in-game, then remove `data/world.bad`.

## Troubleshooting

- **Server crashes on start.** Check `data/logs/latest.log` or `docker compose logs minecraft`. Usual causes: client-only mod in `mods/`, Forge version mismatch, mod dependency conflict.
- **Backup never runs.** Confirm `ENABLE_RCON=true` and `RCON_PASSWORD` is set. The backup sidecar waits on the minecraft health check, which takes ~2 minutes after first boot.
- **Port already in use.** Change the `25566` side of the port mapping in `docker-compose.yml`.

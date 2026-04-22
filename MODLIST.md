# Modpack

- **Minecraft:** 1.20.1
- **Loader:** Forge (LATEST)
- **Target:** ~100 mods, mostly QoL/performance, light on content

## Categories

| Side | Meaning |
| --- | --- |
| `S` | Server-only — drop jar in `mods/` |
| `C` | Client-only — distributed to friends, **not** on server |
| `B` | Both — drop on server and client |

## Mods

| Name | Side | Version | Source | Notes |
| --- | --- | --- | --- | --- |
| _example: Jade_ | B | 14.x | [Modrinth](https://modrinth.com/mod/jade) | tooltip HUD |

<!-- Add mods below as you pick them. Keep versions pinned. -->

## Performance picks (suggested)

- Embeddium (client fork of Sodium for Forge) — client
- Oculus (shaders) — client
- FerriteCore — both (memory reduction)
- Starlight — both (lighting engine)
- Memory Leak Fix — both

## QoL (suggested)

- Jade (tooltips) — both
- JEI / REI — both
- Xaero's Minimap + World Map — client
- AppleSkin — both
- Clumps (XP orb grouping) — both

## Deployment notes

1. Put **server-side** jars in `./mods/` (bind-mounted read-only into container).
2. Keep **client-only** jars out of `./mods/` — they'll crash the server.
3. Pin exact version numbers here so friends get a matching client pack.

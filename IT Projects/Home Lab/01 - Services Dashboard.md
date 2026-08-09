---
tags: [homelab, services, dashboard]
created: 2026-07-25
published_to_garden: true
last_published: '2026-07-25T21:05:10.185673'
---

# Services Dashboard

everything running on the home lab as of 2026-06-27.

## Unraid (192.168.0.120)

| service | port | notes |
|---------|------|-------|
| **Homepage** | 3000 | central dashboard for everything |
| **FileBrowser** | 8083 | Syncthing files browser, user `admin` |
| **Syncthing** | 8384 | syncs m5Pro/BigRig/m4Air Documents + Downloads to `/mnt/user/syncthing/` |
| **Immich** | 2283 | photo backup, RTX 3060 CUDA ML |
| **Home Assistant** | 8123 | plant pumps + lights automations, TP-Link HS300 |
| **Penthouse** | 9080/9443 | compose stack, also public at penthouse.blog |
| **SearXNG** | 8082 | private metasearch engine |
| **qBittorrent** | 8080 | torrents, incomplete in RAM (64GB tmpfs), completed on downloads pool |
| **DuckDNS** | — | keeps aims-photos.duckdns.org pointed at WAN IP |
| **PostgreSQL18** | 5432 | standalone Postgres for Cloudreve (deprecated) and general use |
| **Tailscale** | — | installed via Docker, needs OAuth at login.tailscale.com/a/1ff883870177b5 |

## Penthouse Compose Stack

| container | notes |
|-----------|-------|
| compose-postgres-1 | Postgres 16 Alpine, penthouse DB, local only |
| compose-api-1 | Node.js API, port 3000, healthy |
| compose-caddy-1 | Caddy reverse proxy, 9080→80, 9443→443 |

Deployed from `audit/backend-trim-performance` branch.
Config at `/mnt/cache/appdata/penthouse/app/infra/compose/.env.unraid`.

## Immich Compose Stack

| container | notes |
|-----------|-------|
| immich_server | main server, port 2283 |
| immich_machine_learning | CUDA ML, RTX 3060 |
| immich_postgres | Immich database |
| immich_redis | caching |

## Raspberry Pi 5 (192.168.0.145)

| service | notes |
|---------|-------|
| **Pi-hole** | DNS ad blocking for whole LAN |
| **Unbound** | recursive DNS, no upstream provider sees queries |

## Storage

| pool | device | size | used | mount |
|------|--------|------|------|-------|
| cache | Samsung 512GB NVMe | 476GB | 20GB | `/mnt/cache` |
| downloads | WD Black SN850X 1TB | 928GB | 636KB | `/mnt/downloads` |
| array | 4 HDDs + parity | 7.3TB | 834GB | `/mnt/user` |

## Backup

- **Daily cron**: 3:17 AM, `/boot/config/scripts/hermes-backup.sh`
- **Destination**: `/mnt/user0/backups/hermes/daily/` (parity-protected array)
- **Keeps**: 14 daily backups + 7 ZFS snapshots on cache
- **Home Assistant quick restore**: `ha_quick_restore/` folder in every backup
- **Database dumps**: Immich, Penthouse, PostgreSQL18 in every backup
- **Off-box**: not configured yet (planned M80q + Mac rsync mirror)

## Time Machine

- **Share**: `TimeMachine` on array, exported with 2TB limit
- **Status**: not tested with actual Mac backup yet

## Removed

- **Cloudreve**: wrong tool, replaced by FileBrowser
- **qBittorrentVPN**: broken WireGuard config, not needed for legal torrenting

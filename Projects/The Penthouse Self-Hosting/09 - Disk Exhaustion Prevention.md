---
tags: [self-hosting, truenas, docker, disk, ops, guide, website-rebuild]
created: 2026-02-18
published_to_garden: true
visibility: public
---

# Disk Exhaustion Prevention (Home Server, Docker)

## Why this matters

On a home TrueNAS box, the most common cause of a "random outage" is disk exhaustion, not a software bug. The three biggest culprits are Docker logs growing without bounds, build cache accumulating from frequent rebuilds, and cron job logs sitting in `/var/log` forever.

## What I implemented

### 1. Docker log rotation

Both services in `docker-compose.yml` use the default `json-file` log driver with:
- `max-size: 10m`
- `max-file: 3`

That caps each container at roughly 30MB of logs.

### 2. Host cron log rotation

Cron jobs redirect output to `/var/log/penthouse-*.log`. A weekly rotation script (`scripts/rotate_penthouse_logs.sh`) handles these — rotates when a file exceeds 10MB, keeps a small history, and gzips rotated files when possible.

### 3. Safe Docker pruning

A weekly script (`scripts/docker_prune_safe.sh`) removes:
- Build cache older than 7 days
- Unused images older than 7 days

It does not touch volumes. Don't let anything auto-prune volumes on a production box.

### 4. SQLite WAL maintenance

SQLite in WAL mode keeps a `-wal` file that can grow if it never gets checkpointed. A weekly maintenance script runs `wal_checkpoint(TRUNCATE)` and `optimize` inside the app container.

## All of this gets installed by `enable_autostart.sh`

Running the autostart script installs weekly cron jobs for all three maintenance tasks. Check the crontab after running it to confirm they're there:

```bash
crontab -l | grep -E "rotate_penthouse_logs|docker_prune_safe"
```

## Verification

```bash
ls -lh /var/log/penthouse-*.log 2>/dev/null || echo "no log files yet"
```

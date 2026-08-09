---
tags: [self-hosting, truenas, docker, deployment, runbook]
created: 2026-02-17
published_to_garden: true
visibility: public
---

# TrueNAS Deploy Runbook (SCALE 25.x + Compose)

This assumes a hardened baseline with Docker Compose, a Caddy edge proxy, and a `.env` file for secrets and config.

## One-time setup

**1. Clone the repo into your dataset**

```bash
cd /mnt/Storage_Pool/penthouse
git clone <your-repo-url> app
cd app
```

**2. Create your `.env` file**

```bash
cp server/.env.example .env
chmod 600 .env
```

Required values:

```env
NODE_ENV=production
PORT=3000
JWT_SECRET=<strong random secret>
CORS_ORIGIN=https://penthouse.blog,https://api.penthouse.blog
DOMAIN=penthouse.blog
ENABLE_DEBUG_ENDPOINTS=false
```

**3. Start the stack**

```bash
./scripts/start_stack.sh
docker compose ps
```

**4. Validate internal health**

```bash
docker compose exec -T app wget -q --spider http://localhost:3000/api/health && echo ok
```

**5. Validate external health**

```bash
curl -fsSL https://penthouse.blog/api/health
curl -fsSL https://api.penthouse.blog/api/health
```

## Auto-start options

**Option A — TrueNAS UI (simplest)**

System Settings → Advanced → Init/Shutdown Scripts → add a Post Init command pointing at `start_stack.sh`.

**Option B — Cron `@reboot` plus watchdog**

```bash
./scripts/enable_autostart.sh
crontab -l
```

This installs:
- `@reboot` start
- A `*/5` watchdog that'll restart the stack if it's down
- Optional nightly backups when `.backup.env` is present
- Optional Cloudflare DDNS when `.cloudflare-ddns.env` is present

## Common checks

```bash
# Container status
docker compose ps

# Logs
docker compose logs --tail=200 app
docker compose logs --tail=200 caddy
```

**If TLS fails:**
- Check Cloudflare A records match the actual current public IP.
- Check the router is forwarding WAN 80/443 correctly.
- Check you're not behind CGNAT (most residential ISPs aren't, but some are).

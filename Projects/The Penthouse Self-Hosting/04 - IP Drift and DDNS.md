---
tags: [self-hosting, ddns, cloudflare, tls, networking]
created: 2026-02-17
published_to_garden: true
visibility: public
---

# IP Drift and DDNS (Cloudflare DNS-Only)

## The problem

Home internet public IPs change. When they do and your DNS A records still point at the old IP:
- `http-01` ACME challenges fail
- TLS issuance and renewal fail
- The app goes dark from the internet

This happened on 2026-02-17 and caused downtime until I updated the Cloudflare A records manually. The fix is automating that update so it can't happen again.

## The fix

A Cloudflare DDNS updater script that:
- Discovers the current public IP
- Checks the current DNS record values
- Only calls the Cloudflare API when drift is actually detected

Runs every 5 minutes via cron.

## Configuration

```bash
cp .cloudflare-ddns.env.example .cloudflare-ddns.env
chmod 600 .cloudflare-ddns.env
```

Set your Cloudflare API token:

```env
CF_API_TOKEN=your_token_here
```

The token needs Zone:Zone Read and Zone:DNS Edit permissions, scoped to only the zone you're managing. Don't give it broader access than it needs.

## Cron entry (installed by `enable_autostart.sh`)

```
*/5 * * * * [ -f /path/to/app/.cloudflare-ddns.env ] && cd /path/to/app && ./scripts/cloudflare_ddns.sh >> /var/log/penthouse-ddns.log 2>&1
```

## Verifying it works

```bash
./scripts/cloudflare_ddns.sh
tail -n 50 /var/log/penthouse-ddns.log
```

Expected log output when IP hasn't changed:
```
penthouse.blog already <current-ip>
api.penthouse.blog already <current-ip>
```

On actual IP drift:
```
updating penthouse.blog <old-ip> -> <new-ip>
```

## Token hygiene

If a Cloudflare token ever ends up in a screenshot, a chat log, or anywhere it shouldn't be:
1. Revoke it immediately in the Cloudflare dashboard.
2. Create a fresh scoped token.
3. Update `.cloudflare-ddns.env`.

Don't wait and see — revoke first, ask questions later.

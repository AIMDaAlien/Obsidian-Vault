---
tags: [self-hosting, truenas, docker, caddy, networking, security]
created: 2026-02-17
published_to_garden: true
visibility: public
---

# Architecture — TrueNAS, Public Internet, No Proxy

## Goal

Public internet access to two domains:
- `penthouse.blog` — landing page and downloads
- `api.penthouse.blog` — canonical API and Socket.IO

Without Cloudflare proxying. Single TrueNAS box on home internet. Docker Compose for everything.

## Topology

```
Internet
  |
  | 80/443
  v
Router (NAT / port forward)
  WAN:80  → TrueNAS:9080
  WAN:443 → TrueNAS:9443
  |
  v
TrueNAS SCALE (host)
  Docker bridge network
  |
  v
Caddy container (9080/9443 exposed)
  reverse proxy to app container (internal only)
  |
  v
App container (port not published externally)
  |
  v
/mnt/Storage_Pool/penthouse/app/data
  (database, uploads, downloads)
```

## Why these port numbers

TrueNAS often occupies host ports 80 and 443 itself. The pattern here is:
- Host listens on `9080` and `9443`
- Router forwards WAN 80 to 9080 and WAN 443 to 9443

Externally it still looks like normal HTTP/HTTPS.

## Domain and TLS

TLS is handled by Caddy using ACME `http-01` challenges. This requires:
- DNS A records pointing at the current public IP
- WAN ports 80 and 443 actually reachable from the internet

If either is wrong, certificate issuance and renewal fail.

## Operational principle

Only Caddy is exposed to the internet. The app container port is not published — it's only reachable on the internal Docker network. This means even if someone found the TrueNAS host, they couldn't hit the app directly.

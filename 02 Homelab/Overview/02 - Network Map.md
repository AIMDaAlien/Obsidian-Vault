---
tags: [homelab, network, map, monitoring]
created: 2026-07-25
publish: true
---

# Network Map

## IP Assignments

| IP | device | hostname | notes |
|----|--------|----------|-------|
| <lan-ip-1> | TP-Link router | — | DHCP + gateway |
| <lan-ip-5> | Unraid server | — | static, main server |
| <lan-ip-6> | RPi 5 | — | pi-hole + unbound, static needed |
| <lan-ip-2> | MacBook Pro (m5Pro) | — | DHCP, syncthing source |
| 192.168.0.??? | M80q Tiny | — | not deployed yet |
| 192.168.0.??? | RPi B+ | — | not deployed yet |

## DNS Flow

```
device -> Pi-hole (<lan-ip-6>:53) -> Unbound (127.0.0.1:5335) -> root DNS servers
```

no google dns, no cloudflare dns. all queries resolved from root.

## DHCP

- handled by TP-Link router
- primary DNS points to Pi-hole (<lan-ip-6>)
- if tp-link refuses custom dns, switch DHCP to Pi-hole

## Port Map (Unraid)

| port | service | external? |
|------|---------|-----------|
| 3000 | Homepage dashboard | no |
| 2283 | Immich | duckdns |
| 8123 | Home Assistant | no |
| 5212 | — | removed (was Cloudreve) |
| 8080 | qBittorrent | no |
| 8082 | SearXNG | no |
| 8083 | FileBrowser | no |
| 8384 | Syncthing | no |
| 9080 | Penthouse (HTTP) | no |
| 9443 | Penthouse (HTTPS) | no |
| 3001 | Uptime Kuma | no (planned) |

public access through DuckDNS for Immich and Penthouse.
everything else is LAN-only or Tailscale.

## Tailscale

- installed on Unraid via Docker
- planned: install on mac, phone, m80q, rpi5
- optional: mullvad exit node integration ($5/mo)

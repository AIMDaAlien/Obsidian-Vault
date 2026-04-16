---
tags: [self-hosting, truenas, docker, ops, penthouse-v1]
created: 2026-02-17
published_to_garden: true
visibility: public
---

# Self-Hosting a Chat App on TrueNAS — Index

These notes document what I learned running the first version of The Penthouse on a home TrueNAS SCALE server with Docker Compose and Caddy. The goal was public internet access, small-scale concurrent users, and minimal ops overhead.

The app's since been through a full backend and frontend rebuild, but the operational lessons here still apply to anyone doing something similar — self-hosted, public-facing, running on a single box at home.

## Notes in this series

- [[01 - Architecture]]
- [[02 - TrueNAS Deploy Runbook]]
- [[03 - Backend Hardening Checklist]]
- [[04 - IP Drift and DDNS]]
- [[05 - Git Push Auto-Deploy]]
- [[06 - Deploy Downtime Minimization]]
- [[07 - Security Gotchas]]
- [[08 - SSH Hardening on TrueNAS]]
- [[09 - Disk Exhaustion Prevention]]
- [[10 - Mobile Update Versioning Protocol]]
- [[11 - What Changed Between Notes]]

## Timeline

- **2026-02-17** — DNS IP drift caused ACME timeouts and downtime until Cloudflare A records were corrected. Added DDNS to prevent it happening again.
- **2026-02-17 to 02-18** — Backend hardening pass covering auth, invites, message and WebSocket authorization, rate limits, upload safety, and token hashing. Production deployment automation and downtime reduction.
- **2026-02-21** — Mobile update system added: automated APK publish with changelog manifest, OTA workflow, and in-app update prompts.
- **2026-03-03** — Phase 1 mobile MVP stabilization documented: invite-only signup, startup and noise controls, smart resume, route scope pruning, and mobile test automation.

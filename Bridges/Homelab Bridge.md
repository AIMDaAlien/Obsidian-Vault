---
tags: [bridge, homelab]
created: 2026-08-21
---

# Homelab Bridge

> **What this is:** the single entry point for the home lab — what's running,
> where it lives, and how to operate it.

## The three layers (and where each note lives)
- **IT Projects/Home Lab/** — the *operational* docs: [[01 - Services Dashboard]],
  [[02 - Network Map]], [[00 - Server Inventory]] ← **start here for "what's running"**
- **Systems/Homelab/** — the *knowledge* notes: [[Home Lab]], [[Home Networking]],
  [[Home Server]], plus guides (tag: `guide`) and lessons learned
- **Projects/Homelab NOC Skills/** — the *learning project*: [[Project Overview - NOC Skills Homelab]],
  troubleshooting log, monitoring stack

## Monitoring & ops
- [[Prometheus Grafana Stack - Implementation Guide]] (tag: `guide`)
- Tag filters that matter day-to-day: `monitoring`, `troubleshooting`, `reliability`

## Open questions
- [ ] Is the Services Dashboard current? (last updated when?)
- [ ] Which services are "set and forget" vs need attention?

## How to use this bridge
When you change the lab (new service, new box, network change), update the
matching IT Projects doc AND tag the note. This bridge stays a map, not a manual —
the manuals live in the three layers above.

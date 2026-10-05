---
tags: [homelab, server-inventory, unraid, hardware, monitoring, reliability, hardware-constraints]
created: 2026-06-27
published_to_garden: true
last_published: '2026-07-29T23:14:32'
last_incident: '2026-06-27'
---

# Server Inventory

last updated: 2026-10-05

> Documentation convention (2026-10-05): changes are APPENDED with dated entries
> (e.g. "2026-10-05: ..."), not overwriting prior entries, so history stays
> reviewable. This vault is the source for the portfolio Knowledge Garden
> (auto-committed and published to GitHub Pages).

## Unraid Server

- **OS**: Unraid 7.2.4
- **CPU**: i5-12600KF (10C/16T, up to 4.9GHz)
- **RAM**: 128GB DDR4-3200 (4×32GB)
- **Mobo**: ASRock B660M RS Pro
- **GPU**: RTX 3060 12GB
- **PSU**: be quiet 550W
- **HBA**: LSI SAS2308 (IT mode, FW 20.00.06.00)
- **Cache**: Samsung 512GB NVMe (ZFS, `cache`)
- **Downloads pool**: WD Black SN850X 1TB NVMe (ZFS, `downloads`)
- **Array drives**:
  - parity: 14.6TB WUH721816AL5204
  - disk1: 3.6TB HGST HUS724040ALA640
  - disk2: 1.8TB ST2000NM0045
  - disk3: 1.8TB ST2000NM0045
- **IP**: 192.168.0.120
- **Root pass**: stored offline (redacted from published copy)
- **Docker image**: 35GB on `/mnt/user/system/docker/docker.img`
- **Quirks**:
  - 2.4GHz wireless keyboard freezes B660M UEFI -- use wired keyboard
  - SAS drives need staggered spin-up in LSI BIOS (not configured yet)
  - Old 128GB cache NVMe unrecoverable (SanDisk USB bridge chip reports 0 bytes)

## Raspberry Pi 5

- **Role**: Pi-hole DNS + Unbound recursive DNS
- **Storage**: 512GB NVMe (overkill, mostly unused)
- **IP**: 192.168.0.145
- **Root pass**: stored offline (redacted from published copy)
- **SSH**: password auth might be disabled, needs HDMI check

## Raspberry Pi B+ (512MB)

- **Role**: not deployed yet -- planned NTP server + ping watchdog
- **Status**: unplugged

## Lenovo ThinkCentre M80q Tiny (Penthouse Hotswap)

- **Role**: read-only failover node for The Penthouse (deployed)
- **CPU**: i5-12500T (6 P-cores, 35W)
- **RAM**: 16GB DDR4
- **Storage**: 512GB NVMe (OS) + 2TB SATA SSD
- **Failover design** (recovery architecture):
  - Unraid remains the only writer; mini never becomes a writer (no split-brain, no DB merging)
  - PostgreSQL synchronous replication: DB commits wait until mini has applied them
  - Uploads/media mirrored and verified on both machines before success is returned
  - HAProxy routes readers to mini if Unraid fails; existing content stays available
  - Messaging, uploads, and account changes pause during failover; writing resumes when Unraid returns and both copies are healthy
  - Cloudflare public access via independently supervised connectors
  - Monitoring is live; full production cutover still pending

  **2026-10-05 details (from `infra/recovery/README.md`):**
  - Gateways/connectors on both hosts are independently supervised; both prefer Unraid and select mini after 3 failed readiness checks, 10 seconds apart. Three successful checks restore preference.
  - PostgreSQL `remote_apply` synchronous replication; runtime/replication/maintenance identities are separate; no automation weakens synchronous replication.
  - Primary write gate verifies streaming readiness plus SHA-256/size of every database-referenced media file on both hosts. Media finalized via fsync + forced-SSH receiver mirroring before metadata insertion; published files immutable.
  - Mini is physically recovered, read-only application connection, read-only uploads; migrations/push/notification writers disabled. Mutations return HTTP 503 / `WRITES_PAUSED`; `/api/v1/health` stays available.
  - Measured disposable failover transitions: approximately 30.1 seconds each direction (local evidence, not a public-Cloudflare-latency promise).
  - Repeatable proof harness exists (`check-read-only-recovery.mts` + api-recovery tests) covering streaming/remote_apply, SSH media finalization, interruption, write rejection, corruption/recovery, revocation, TLS gateways, and gateway restart.
  - Status 2026-10-05: monitor-only watchdog installed on mini (old script preserved at `/var/backups/penthouse-recovery-20261005T211022Z`); DB/media archives restored into fresh isolated storage, all 20 referenced media files verified; sequential row comparison found no mini-only messages. No DNS move or service replacement yet. Live cutover checklist (8 steps) is written; completion requires controlled live drill and public-client proof.

## BigRig (Local LLM Inference Server)

- **Role**: local LLM inference server; OpenAI-compatible serving host for LAN clients; local AI benchmarking (results to be imported into portfolio + MetalBench later)
- **OS**: Windows
- **CPU**: Ryzen 9 7950X (16C/32T)
- **RAM**: 64GB DDR5
- **Mobo**: ASUS TUF X670E
- **GPUs**: RX 9060 XT 16GB + 2x RTX 3060 (12GB each)
- **Planned upgrade**: Tesla V100 32GB to replace the two RTX 3060s
- **Serving stack**: llama.cpp-based multi-runtime mix (per MetalBench plan: flash-next, FreeToken, MTP experiments) -- confirm exact runtimes
- **Target models**: Qwen3 Flash Next, Qwen 27B-class, small models hosted for LAN clients
- **Also planned**: Obsidian on BigRig, vault synced through Unraid

  **2026-10-05: current model serving stack (per Aim; more models exist but unrecorded):**
  - Qwen3.8 Flash Next, IQ3_XXS quant: one RTX 3060 holds dense weights, experts offloaded to CPU/DDR5 ("Strata" setup)
  - Qwen3.8 Swift (low thinking), Q5: split across RX 9060 XT + RTX 3060 at 15/11 layers
  - Ornith 1.5, Q2: runs on RX 9060 XT
  - Serving stack is llama.cpp-based multi-runtime (confirm exact launcher/router later)
  - Benchmarking agents running on BigRig; MetalBench import held until substantiated, standardized results exist (benchmarks not standardized yet)

## MacBook Pro (m5Pro)

- **Role**: daily driver, Syncthing source
- **Syncthing**: Documents + Downloads synced to Unraid
- **IP**: 192.168.0.109 (DHCP)

## Future Devices

- **BigRig**: Windows desktop, Syncthing (Documents + Downloads); Obsidian vault synced through Unraid
- **m4Air**: M4 MacBook Air, Syncthing (Documents + Downloads)
- **Vault sync plan**: Obsidian vault centralized on Unraid; this Mac, BigRig, and any future devices sync to the Unraid vault copy

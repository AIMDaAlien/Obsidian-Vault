---
tags: [unraid, hardware-swap, troubleshooting, homelab]
created: 2026-06-20
---

# Unraid Server Hardware Swap — B660M + 12600KF Transplant

## What happened

replaced the old Unraid server guts (**ASUS PRIME H510M-A CSM + i5-11400 + 2x16GB DDR4**) with the gaming PC's hardware (**ASRock B660M RS Pro + i5-12600KF + 4x32GB DDR4-3200 quad channel + RTX 3060 12GB**). kept the drives, LSI HBA, 500W PSU, fans, and Unraid USB flash. also swapped the 128GB NVMe cache for a **Samsung 970 EVO Plus 512GB** and planning to add a shucked 1TB SanDisk NVMe as a 6th data drive (Unraid Starter max).

## Pre-swap backup (done)

- SCP'd `/mnt/user/appdata/` (~2.1GB) to Mac at `~/Documents/unraid-backup-202606..` — all container configs
- copied `/boot/config/` — disk assignments, network config, go file
- dumped Immich Postgres DB: `docker exec immich_postgres pg_dump -U immich immich > immich-db.sql`
- saved `docker-compose.yml` and `.env` from Immich container
- noted old MAC address: `04:42:1a:0a:81:e5`

## Running containers before swap

- Immich (server + ML + Postgres + Redis)
- DuckDNS
- qBittorrent + qBittorrentVPN (binhex)
- CloudReve
- PostgreSQL 18
- Penthouse

3 data drives: 3.6TB WUH721816AL5204 + 2x 1.8TB ST2000NM0045. array at 795GB used of 7.3TB (11%).

## The troubleshooting nightmare

after physical transplant — black screen, random freezes, BIOS unusable.

### what i tried (all wrong leads)

- one RAM stick in A2 — no change
- cleared CMOS repeatedly
- reseated GPU, tried 12V2 vs 12V1 PCIe power
- removed all but one RAM stick, cycled sticks
- loosened cooler mounting pressure
- checked socket pins — pristine
- pulled NVMe drive with Linux Mint (thought bootloader conflict)
- tested outside case on paper bag (PCIe slot not fully seated — board flexed)
- suspected: RAM training issues, dead board, bad PCIe slot, scratched screw hole (copper sliver visible), standoff short

### the actual problem

**2.4GHz wireless mechanical keyboard dongle freezing the UEFI BIOS.** ASRock B660M RS Pro's UEFI USB stack chokes on 2.4GHz HID dongle reports. every keypress triggers a USB stack hang — the whole BIOS freezes. the board, RAM, GPU, and drives were all fine.

### confirmed fix

- unplugged the 2.4GHz dongle
- plugged in a wired USB keyboard
- BIOS instantly stable — no freezes, everything works
- once Unraid boots (Linux USB stack), the wireless keyboard works fine

## Lessons

- **2.4GHz wireless peripherals can lock up UEFI on ASRock B660 boards.** keep a wired keyboard handy for BIOS work
- the **debug LEDs were accurate the whole time** — DRAM passed, VGA passed, BOOT LED just meant no boot device configured. i ignored the evidence because i couldnt interact with BIOS
- **memory training on 4x32GB quad channel takes 30-90 seconds** of black screen before first POST. this is normal after CMOS clear or first boot
- the **12600KF has no iGPU** — VGA LED stays on if GPU has any issue at all. GPU must be fully seated with PCIe power connected
- **do not power on without a cooler** on LGA1700 — thermal shutdown in seconds. invalidates the test
- **LGA1700 cooler mounting pressure matters** — cross-tighten, dont crank one side down

## Post-swap to-do

- [ ] boot Unraid, find new IP (different MAC on new NIC)
- [ ] stop array, assign **Samsung 970 EVO Plus 512GB** as new cache pool
- [ ] start array, let Unraid format cache
- [ ] add 1TB SanDisk NVMe as 6th data drive (if installed)
- [ ] start Docker containers in order: DuckDNS → PostgreSQL 18 → qBittorrent → Immich stack → CloudReve → Penthouse
- [ ] install NVIDIA Driver plugin for RTX 3060 Immich ML acceleration
- [ ] update router DHCP reservation for new MAC address
- [ ] expand Docker image from 20GB to ~50GB on new cache
- [ ] disable Fast Boot in BIOS (helps USB init)
- [ ] set boot order: Unraid USB first

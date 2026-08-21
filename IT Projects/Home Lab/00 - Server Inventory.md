---
tags: [homelab, server-inventory, unraid, hardware, guide, monitoring, reliability, hardware-constraints]
created: 2026-06-27
published_to_garden: true
last_published: '2026-07-29T23:14:32'
last_incident: '2026-06-27'
---

# Server Inventory

last updated: 2026-06-27

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

## Lenovo ThinkCentre M80q Tiny

- **Role**: planned Uptime Kuma + Penthouse fallback + backup mirror
- **CPU**: i5-12500T (6 P-cores, 35W)
- **RAM**: 16GB
- **Storage**: 120GB NVMe (OS) + slot for 2TB SATA SSD
- **Status**: not deployed yet

## MacBook Pro (m5Pro)

- **Role**: daily driver, Syncthing source
- **Syncthing**: Documents + Downloads synced to Unraid
- **IP**: 192.168.0.109 (DHCP)

## Future Devices

- **BigRig**: Windows desktop, Syncthing (Documents + Downloads)
- **m4Air**: M4 MacBook Air, Syncthing (Documents + Downloads)

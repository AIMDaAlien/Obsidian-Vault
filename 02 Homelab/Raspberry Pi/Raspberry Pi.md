---
tags: [hardware-constraints, homelab, raspberry-pi, pihole, hardware]
created: 2025-09-15
updated: 2026-10-25
publish: true
summary: "The two Raspberry Pis in my homelab, a 512MB B+ and a 4GB Pi 5, and the Pi-hole notes that moved from one to the other."
---
# Raspberry Pi

Two Pis live in the [[Homelab Index|homelab]]. Pi-hole started on the old one and now runs on the new one.

| | Raspberry Pi B+ | Raspberry Pi 5 |
|---|---|---|
| RAM | 512MB | 4GB |
| CPU | ARMv6 700MHz, single core | Cortex-A76 2.4GHz, quad core |
| Storage | SD card | PCIe NVMe |
| Role | retired from Pi-hole, unplugged; planned NTP server and ping watchdog | Pi-hole + Unbound DNS, NOC monitoring stack |

## Pi-hole

1. [[Pi-hole Setup Guide - Complete Journey]] — the first build on the B+.
2. [[Pi-hole TrueNAS Network Conflict Troubleshooting]] — ad blocking stopped when the NAS joined the network.
3. [[Pi-hole Migration - RPi B+ to RPi 5 NVMe]] — moving DNS onto the Pi 5.

## The boards

- **B+:** [[Raspberry Pi B+ Utility Node]] covers what a 2014 Pi can still do.
- **Pi 5:** [[Project Overview - NOC Skills Homelab]] covers the services it runs.
- Both are listed in [[00 - Server Inventory]].

## Other uses for a Pi

A Pi also works as a small [[Home Server]]:

1. **Desktop replacement:** basic web browsing and coding
2. Streaming media
3. Wireshark and intrusion detection (IDS)
4. **Educational tool:** programming, electronics, and computer science
5. **Remote control:** remotely control and monitor robots and smart home devices
6. **AI and machine learning**
7. External or cloud storage

---
tags: [troubleshooting, monitoring, interview-prep, homelab, noc, career, docker, portfolio]
created: 2026-01-07
publish: true
---

# NOC Skills Homelab Project

## Purpose
Build demonstrable NOC/Data Center technician skills through hands-on homelab projects. This project directly supports the IT career transition by creating portfolio-worthy monitoring infrastructure.

## Hardware
- **RPi 5 (4GB)** — Primary lab box for monitoring stack + Pi-hole + Unbound (migrated 2026-03-15)
- **RPi B+** — ~~Running Pi-hole~~ **Retired** (see [[Pi-hole Migration - RPi B+ to RPi 5 NVMe]])
- **TrueNAS Server** — Storage-heavy applications

## Target Skills (Based on Job Market Research)
| Skill | Tool/Project | Status |
|-------|--------------|--------|
| Containerization | Docker + Portainer | Not Started |
| Metrics Collection | Prometheus + Node Exporter | Not Started |
| Visualization | Grafana | Not Started |
| Service Monitoring | Uptime Kuma | Not Started |
| Alerting | Ntfy or Gotify | Not Started |
| Log Aggregation | Loki | Not Started |
| Scripting | Python/Bash automation | Not Started |

## Project Timeline
- **Week 1-2**: Docker fundamentals + Portainer
- **Week 3-4**: Prometheus + Grafana stack
- **Week 5-6**: Alerting integration
- **Week 7+**: Log aggregation, advanced dashboards

## Quick Links
- [[Docker and Portainer Setup]]
- [[Prometheus Grafana Stack]]
- [[Troubleshooting Log]]
- [[Session Notes]]

## Related
- [[Pi-hole Setup Guide - Complete Journey]]
- [[Pi-hole Migration - RPi B+ to RPi 5 NVMe]]
- [[TrueNAS Build Guide]]
- NOC-DC-Job-Research-2025.docx (generated research document)

---
*Project started: 2026-01-07*
*Goal: Build interview-ready monitoring portfolio*



---
## Status Update: 2026-01-10

### Completed
-  Docker 29.1.4 installed on RPi 5
-  Portainer CE (LTS) deployed and accessible
-  Local environment connected

### Network Map
| Device | IP | Role |
|--------|-----|------|
| RPi 5 (pi5) | <lan-ip-6> | Monitoring stack |
| RPi B+ (pihole) | <lan-ip-4> | DNS/Pi-hole |
| TrueNAS | TBD | Storage |

### Next Session
- Deploy Uptime Kuma or Prometheus + Grafana



---
## Status Update: 2026-01-10 (Revised)

### Actually Completed (Discovered existing setup!)
-  Docker 29.1.4 + Portainer CE
-  Prometheus (systemd, ~10 weeks running)
-  Node Exporter (systemd)
-  Blackbox Exporter (systemd)
-  Grafana with 2 dashboards (systemd)

### Updated Skills Matrix
| Skill | Tool/Project | Status |
|-------|--------------|--------|
| Containerization | Docker + Portainer |  Complete |
| Metrics Collection | Prometheus + Node Exporter |  Complete |
| Visualization | Grafana |  Complete |
| HTTP Probing | Blackbox Exporter |  Complete |
| Service Monitoring | Uptime Kuma | Skipped (redundant) |
| Alerting | Alertmanager + Ntfy | Not Started |
| Log Aggregation | Loki | Not Started |

### Next Priority
Alerting configuration - make monitoring actionable



---
## Service Architecture: 2026-01-10

### RPi 5 Services (<lan-ip-6>)
| Service | Port | Type |
|---------|------|------|
| Prometheus | 9090 | systemd |
| Grafana | 3000 | systemd |
| Node Exporter | 9100 | systemd |
| Blackbox Exporter | 9115 | systemd |
| Portainer | 9443 | Docker |
| Alertmanager | 9093 | Docker |
| ntfy | 8080 | Docker |
| Homepage | 3001 | Docker |
| Watchtower | - | Docker |

### TrueNAS Services (<lan-ip-5>)
| Service | Port | Resources |
|---------|------|-----------|
| Immich | 30041 | - |
| Vaultwarden | TBD | 1 core, 512MB |
| Paperless-ngx | TBD | 2 cores, 1-2GB |
| Changedetection | TBD | 1 core, 512MB |
| Filebrowser | TBD | 0.5 core, 256MB |
| Scrutiny | TBD | 1 core, 512MB |



---
## Session Update: 2026-01-11

### New Services Deployed

**TrueNAS (<lan-ip-5>):**
| Service | Port | Status |
|---------|------|--------|
| Vaultwarden | 30032 |  |
| Scrutiny | 31054 |  |
| Immich | 30041 |  |

**RPi 5 (<lan-ip-6>):**
| Service | Port | Status |
|---------|------|--------|
| Nginx Proxy Manager | 81/443 |  |
| Homepage | 3001 |  |
| Watchtower | - |  |
| Alertmanager | 9093 |  |
| ntfy | 8080 |  |

### SSL Setup
- NPM + self-signed cert for vault.local
- Hosts entry: `<lan-ip-6> vault.local`

### Pending
- Paperless-ngx (2 cores, 2GB)
- Changedetection (1 core, 512MB)
- Jellyfin (2 cores, 2-4GB + iGPU passthrough)



---
## Final Session Update: 2026-01-11

### Complete Service Inventory

**RPi 5 (<lan-ip-6>):**
| Service | Port | Type |
|---------|------|------|
| Prometheus | 9090 | systemd |
| Grafana | 3000 | systemd |
| Node Exporter | 9100 | systemd |
| Blackbox Exporter | 9115 | systemd |
| Alertmanager | 9093 | Docker |
| ntfy | 8080 | Docker |
| Portainer | 9443 | Docker |
| Homepage | 3001 | Docker |
| Watchtower | - | Docker |
| Nginx Proxy Manager | 81/443 | Docker |

**TrueNAS (<lan-ip-5>):**
| Service | Port | Resources |
|---------|------|-----------|
| Immich | 30041 | - |
| Vaultwarden | 30032 | 1 core, 512MB |
| Scrutiny | 31054 | 1 core, 512MB |
| Jellyfin | 30013 | 2 cores, 4GB |
| Changedetection | 30159 | 1 core, 512MB |
| qBittorrent | 30024 | 1 core, 1GB |
| Filebrowser | 30051 | 0.5 core, 256MB |
| Nextcloud | 30027 | 2 cores, 2-4GB |

### Skills Demonstrated
- Linux administration (systemd, Docker)
- Monitoring stack (Prometheus, Grafana, Alertmanager)
- Container orchestration (Portainer)
- Reverse proxy + SSL (NPM, self-signed certs)
- Self-hosted services deployment
- Alert configuration and notification routing



---
## Backup Strategy Discussion: 2026-01-15

### Current Storage
- Storage_Pool: 6 SAS drives in RAID-Z2 (~4.86 TiB usable)
- 1 hot spare SAS drive
- Unassigned: 1.09 TiB SAS, 3.64 TiB external

### Recommended Backup Config
- Create single-drive "Backup" pool with 4TB external
- Keep spare SAS as hot spare for Storage_Pool
- Don't mix mismatched drives — wastes capacity

### 3-2-1 Status
| Copy | Location | Status |
|------|----------|--------|
| 1 | Storage_Pool |  |
| 2 | Backup pool (4TB) | Pending |
| 3 | Offsite (cloud) | Pending |

### Next Steps
- IaC with Ansible (prompt ready for Haiku)
- Obsidian→Portfolio pipeline (prompt ready for Haiku)
- Set up replication tasks to Backup pool



---
## Session Update: 2026-03-15

### Pi-hole Migrated to RPi 5

The Pi-hole instance previously running on the Raspberry Pi B+ (`<lan-ip-4>`) has been migrated to this machine (`<lan-ip-6>`). The B+ is now retired.

**What changed:**
- Pi-hole now runs on the RPi 5 alongside the existing NOC monitoring stack
- Unbound recursive DNS running on this machine (port `5335`)
- HaGeZi Pro + TIF blocklists deployed with telemetry regex filters
- DNS loop resolved — `/etc/resolv.conf` forced to `127.0.0.1`, TP-Link DHCP updated
- RPi B+ retired

**Updated network map:**

| Device | IP | Role |
|---|---|---|
| RPi 5 (pi5) | <lan-ip-6> | NOC monitoring stack + Pi-hole + Unbound |
| RPi B+ | <lan-ip-4> | **Retired** |
| TrueNAS | <lan-ip-5> | Storage |

**Full migration write-up:** [[Pi-hole Migration - RPi B+ to RPi 5 NVMe]]

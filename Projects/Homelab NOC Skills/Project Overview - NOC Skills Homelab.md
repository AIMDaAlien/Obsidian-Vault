---
created: '2026-01-07T22:57:12.633493'
modified: '2026-01-10T12:05:25.626203'
privacy_scan: not_scanned
published_to_garden: false
tags:
- homelab
- noc
- career
- docker
- monitoring
- portfolio
title: Project Overview   Noc Skills Homelab
visibility: private
---

# NOC Skills Homelab Project

## Purpose
Build demonstrable NOC/Data Center technician skills through hands-on homelab projects. This project directly supports the IT career transition by creating portfolio-worthy monitoring infrastructure.

## Hardware
- **RPi 5 (4GB)** - Primary lab box for monitoring stack
- **RPi B+ (512MB)** - Running Pi-hole (leave as-is)
- **TrueNAS Server** - Storage-heavy applications

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
- [[Projects/Archive/Pi-hole Setup Guide - Complete Journey]]
- [[Projects/Archive/TrueNAS Build Guide]]
- NOC-DC-Job-Research-2025.docx (generated research document)

---
*Project started: 2026-01-07*
*Goal: Build interview-ready monitoring portfolio*



---
## Status Update: 2026-01-10

### Completed
- ✅ Docker 29.1.4 installed on RPi 5
- ✅ Portainer CE (LTS) deployed and accessible
- ✅ Local environment connected

### Network Map
| Device | IP | Role |
|--------|-----|------|
| RPi 5 (pi5) | 192.168.0.145 | Monitoring stack |
| RPi B+ (pihole) | 192.168.0.117 | DNS/Pi-hole |
| TrueNAS | TBD | Storage |

### Next Session
- Deploy Uptime Kuma or Prometheus + Grafana



---
## Status Update: 2026-01-10 (Revised)

### Actually Completed (Discovered existing setup!)
- ✅ Docker 29.1.4 + Portainer CE
- ✅ Prometheus (systemd, ~10 weeks running)
- ✅ Node Exporter (systemd)
- ✅ Blackbox Exporter (systemd)
- ✅ Grafana with 2 dashboards (systemd)

### Updated Skills Matrix
| Skill | Tool/Project | Status |
|-------|--------------|--------|
| Containerization | Docker + Portainer | ✅ Complete |
| Metrics Collection | Prometheus + Node Exporter | ✅ Complete |
| Visualization | Grafana | ✅ Complete |
| HTTP Probing | Blackbox Exporter | ✅ Complete |
| Service Monitoring | Uptime Kuma | Skipped (redundant) |
| Alerting | Alertmanager + Ntfy | Not Started |
| Log Aggregation | Loki | Not Started |

### Next Priority
Alerting configuration - make monitoring actionable
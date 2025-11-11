---
tags: #homelab #monitoring #prometheus #grafana #raspberry-pi #infrastructure #sre #lessons-learned
created: 2025-10-14
status: complete
---

# Prometheus & Grafana Monitoring Stack - Lessons Learned

## Overview
This document captures lessons learned from planning and researching a comprehensive monitoring stack for a homelab environment. It serves as both a post-mortem and educational resource for others considering similar projects.

## Executive Summary

**Goal**: Deploy Prometheus + Grafana monitoring for homelab infrastructure (Pi-hole, TrueNAS, network devices)

**Key Findings**:
- Hardware verification is critical before planning
- Prometheus 3.x introduced breaking changes removing console libraries
- ARM architecture can be misleading on Raspberry Pi
- Resource requirements scale beyond base monitoring when planning multiple projects

**Outcome**: Hardware upgrade required (Pi 1B+ → Pi 5 4GB)

---

## Career Context: Why This Project Matters

### IT Career Pathways
Traditional helpdesk roles are declining due to automation. Modern IT careers cluster around:

1. **DevOps/SRE** - Automation, CI/CD, infrastructure as code
2. **Cloud Infrastructure** - AWS/Azure/GCP management
3. **Deployment Engineering** - Mass-scale provisioning/imaging
4. **Network Engineering** - Advanced troubleshooting, security
5. **Cybersecurity Operations** - SOC analyst, monitoring

### Why Monitoring Projects Build Career Skills
- **Systems thinking** - Understanding infrastructure holistically
- **Observability** - Industry-standard practice (Prometheus is CNCF graduated)
- **Troubleshooting at scale** - Moving beyond one-off fixes
- **Data-driven decisions** - Metrics inform optimization
- **Remote work friendly** - Most monitoring roles are remote-capable

Monitoring differentiates "fixes computers" from "maintains infrastructure."

---

## Technical Architecture

### What We're Building

```
Homelab Devices (Pi-hole, NAS, etc.)
        ↓
    Exporters (Port 9100, 9617, etc.)
        ↓
    Prometheus (Scrapes every 15s)
        ↓
    Grafana (Visualizes data)
```

### Components Explained

**Prometheus** (Data Collector)
- Time-series database
- Pulls metrics via HTTP scraping
- Stores data locally (15 days default retention)
- Runs on port 9090

**Node Exporter** (System Metrics)
- Exposes CPU, RAM, disk, network stats
- Standard exporter for *nix systems
- Runs on port 9100

**Grafana** (Dashboard/Visualization)
- Queries Prometheus for data
- Creates graphs, alerts, dashboards
- Runs on port 3000

---

## Critical Lesson: Hardware Verification

### The Problem

**Assumed**: Raspberry Pi 3B+ (quad-core, 1GB RAM, ARMv8)
**Reality**: Raspberry Pi 1B+ (single-core, 512MB RAM, ARMv6)

### How This Happened

1. Multiple Raspberry Pis in homelab
2. SSH'd into wrong device
3. Didn't verify hardware before planning
4. Load warnings (1.1 on "4 processors") were misinterpreted

### How to Verify Your Hardware

```bash
# Check architecture
uname -m
# armv6l = Pi Zero, Pi 1
# armv7l = Pi 2, Pi 3 (32-bit OS)
# aarch64 = Pi 3/4/5 (64-bit OS)

# Check RAM
free -h

# Check CPU info
cat /proc/cpuinfo | grep -E "model name|Hardware"

# Check model explicitly
cat /proc/device-tree/model
```

### ARM Architecture Confusion on Raspberry Pi

**Pi 3B+ hardware**: ARMv8 (64-bit Cortex-A53)
**Pi 3B+ OS (standard)**: 32-bit Raspberry Pi OS
**Reported architecture**: armv7l

This happens because:
- Raspberry Pi OS is 32-bit for compatibility across models
- ARMv8 in 32-bit mode acts like ARMv7
- Most software uses armv7 binaries on Pi 3/4

**Key takeaway**: Don't assume architecture from model number alone.

---

## Prometheus 3.x Breaking Changes

### What Changed

**Prometheus 2.x** (used until Nov 2024):
- Included `consoles/` and `console_libraries/` directories
- Bootstrap-based UI
- Many experimental features behind flags

**Prometheus 3.x** (current, Nov 2024+):
- **Removed console directories entirely**
- New React + Mantine UI
- UTF-8 support enabled by default
- Feature flags removed (now default)
- Simplified installation

### Impact on Installation

**Old guides (2.x) say**:
```bash
sudo cp -r consoles /etc/prometheus
sudo cp -r console_libraries /etc/prometheus
```

**This fails in 3.x** because directories don't exist.

**Correct 3.x installation**:
```bash
# Only copy binaries
sudo cp prometheus promtool /usr/local/bin/
# No console directories needed
```

**Systemd service changes**:
```ini
# REMOVE these lines (2.x only):
--web.console.templates=/etc/prometheus/consoles
--web.console.libraries=/etc/prometheus/console_libraries

# Keep only:
--config.file=/etc/prometheus/prometheus.yml
--storage.tsdb.path=/var/lib/prometheus/
--web.listen-address=0.0.0.0:9090
--web.enable-lifecycle
```

### Why This Matters

- GitHub issues confirm console removal (issue #478)
- Official docs updated but many tutorials aren't
- Copying non-existent directories causes silent failures
- Old systemd services reference paths that don't exist

---

## Resource Requirements & Planning

### Base Monitoring Stack

| Component | RAM | CPU | Storage |
|-----------|-----|-----|---------|
| Prometheus | 80-120MB | ~5% | 1-2GB/day |
| Grafana | 120-180MB | ~3% | Minimal |
| Node Exporter | ~20MB | ~1% | None |
| **Total** | **~300MB** | **~9%** | **~2GB/day** |

### Pi-hole + Unbound Baseline
- Pi-hole: ~100MB RAM
- Unbound DNS: ~40MB RAM
- OS overhead: ~250MB RAM
- **Total: ~400MB used**

### Hardware Capacity Analysis

**Pi 1B+ (512MB RAM)**:
- 512MB total
- 400MB used (OS + Pi-hole)
- 112MB available
- Monitoring needs 300MB
- **Result**: Insufficient, will swap thrash

**Pi 3B+ (1GB RAM)**:
- 1024MB total
- 400MB used
- 624MB available
- Monitoring needs 300MB
- **Result**: Tight but workable for monitoring only

**Pi 4B 4GB**:
- 4096MB total
- 400MB used
- 3696MB available
- Monitoring + multiple projects
- **Result**: Comfortable headroom

**Pi 5 4GB**:
- 4096MB total
- Better CPU/thermals than Pi 4
- **Result**: Recommended for multi-project homelab

### Load Average Context

**Load of 1.1 on single-core Pi 1B+**:
- 110% CPU utilization (over capacity)
- DNS queries blocking due to 400k blocklist
- Already stressed before adding monitoring

**What causes high load with Pi-hole**:
- Large blocklists (400k+ domains)
- Each DNS query checks entire list
- Recursive DNS (Unbound) adds overhead
- Single core bottleneck

**Optimization**: Reduce blocklist to 150-200k domains for 30-40% load reduction.

---

## Pi-hole Blocklist Optimization

### The Problem
400,000 domains on blocklist = excessive for Pi 1B+ hardware

### Recommended Configuration

**Keep**:
- EasyList (core ad blocking) ~50k
- Hagezi Normal/Multi ~150k
- Specific telemetry lists:
  - Microsoft ~3k
  - Samsung ~3k
  - Xiaomi ~2k
  - Oppo/Oneplus ~2k

**Remove**:
- Hagezi Pro+ (900k+ domains - overkill)
- NSFW lists (500k+ unless needed)
- Regional lists (German Privacy unless in Germany)
- Redundant lists (Prigent-Ads overlaps with EasyList)

**Target**: 150-200k total domains

**Result**: 
- 95% blocking effectiveness maintained
- 30-40% CPU load reduction
- Faster DNS resolution

---

## Hardware Selection Guide

### Decision Matrix

| Model | RAM | CPU | Price | Use Case |
|-------|-----|-----|-------|----------|
| Pi 1B+ | 512MB | 1-core | $0 (owned) | Single light service |
| Pi 3B+ | 1GB | 4-core | $25-35 used | Monitoring only |
| Pi 4B 2GB | 2GB | 4-core | $35-45 | Light multi-project |
| Pi 4B 4GB | 4GB | 4-core | $55-65 | Recommended baseline |
| Pi 5 4GB | 4GB | 4-core | $60-80 | Best performance |
| Orange Pi 5 4GB | 4GB | 8-core | $60-70 | Best value/performance |

### Orange Pi vs Raspberry Pi

**Orange Pi 5 Advantages**:
- 50% better CPU performance (8-core vs 4-core)
- Better thermals
- Similar price to Pi 4B/5
- PCIe expansion slot

**Orange Pi 5 Trade-offs**:
- Setup 70-80% as easy (vs Raspberry Pi's 95%)
- Smaller community
- No Raspberry Pi OS (Debian/Ubuntu instead)
- Hardware-specific projects need adaptation
- GPIO compatibility varies

**Projects that work identically**:
- Prometheus/Grafana (yes)
- Docker containers (yes)
- Network services (yes)
- Python/Node.js apps (yes)

**Projects needing adjustment**:
- Pi-specific hardware (cameras, GPIO sensors)
- Tutorials assuming Raspberry Pi OS

### Recommendation Logic

**If you value**:
- Plug-and-play experience → Pi 4B/5
- Maximum community support → Pi 4B/5
- Best performance/price → Orange Pi 5
- Hardware tinkering → Orange Pi 5

**For homelab monitoring + projects**: Pi 5 4GB or Orange Pi 5 4GB

---

## Overclocking Considerations

### Question: Should I overclock Pi 1B+ while waiting for Pi 5?

**Answer**: No, keep at medium or reduce to stock.

### Reasoning

**Current state**:
- Load 1.1 (already maxed)
- Running critical DNS service (Pi-hole)
- Single point of failure for network

**Overclocking gains**:
- Maybe 5-10% performance boost
- Increased heat, power draw
- Higher crash risk
- Marginal benefit for 24-48 hours until migration

**Better strategy**:
1. Maintain stability until Pi 5 arrives
2. Set up monitoring on Pi 5 first
3. Migrate Pi-hole to Pi 5
4. Repurpose Pi 1B+ as experimental device
5. Then overclock freely (no production impact)

**Key principle**: Don't risk production services for marginal temporary gains.

---

## Project Selection for Career Development

### Projects Ranked by Career Signal

**High Value (SRE/DevOps)**:
1. Monitoring stack (this project)
2. CI/CD pipeline for portfolio site
3. Lab provisioning system (Ansible/Terraform)
4. Backup & disaster recovery automation

**Medium Value (Infrastructure)**:
5. Home security camera system (Frigate)
6. Personal API + dashboard
7. Network performance lab

**Lower Value (Specialized)**:
8. 3D printing projects
9. Gaming servers

### Career Path Matching

**Want SRE/Infrastructure role**:
- Do: Monitoring, CI/CD, provisioning
- Shows: Observability, automation, scale thinking

**Want Data Center Tech role**:
- Do: Monitoring, security cameras, network lab
- Shows: Hardware + software integration

**Want DevOps role**:
- Do: CI/CD, provisioning, API development
- Shows: Automation, coding, deployment

**Want Deployment Engineering**:
- Do: Lab provisioning, mass imaging simulation
- Shows: Scale operations, efficiency mindset

---

## Key Takeaways

1. **Verify hardware before planning** - Don't assume, confirm with commands
2. **Check software versions** - Prometheus 3.x has breaking changes from 2.x
3. **Understand ARM architecture** - Pi reports OS arch, not hardware arch
4. **Resource planning matters** - Base requirements + future projects + buffers
5. **Stability over optimization** - Don't risk production for marginal gains
6. **Projects signal career intent** - Choose projects aligned with target role
7. **Documentation prevents repeat mistakes** - This note exists for that reason

---

## Next Steps

1. **Tomorrow**: Receive Pi 5 4GB with active cooler
2. **Day 1-2**: Set up Prometheus 3.7.0 + Node Exporter
3. **Day 3-4**: Install Grafana, create dashboards
4. **Week 2**: Migrate Pi-hole from Pi 1B+ to Pi 5
5. **Week 3**: Add TrueNAS monitoring
6. **Week 4**: Explore next project from career development list

---

## Resources

**Official Documentation**:
- Prometheus: https://prometheus.io/docs/
- Grafana: https://grafana.com/docs/
- Prometheus 3.0 Migration Guide: https://prometheus.io/docs/prometheus/latest/migration/

**GitHub**:
- Prometheus Releases: https://github.com/prometheus/prometheus/releases
- Console Libraries Issue: https://github.com/prometheus-community/ansible/issues/478

**Hardware**:
- Raspberry Pi Documentation: https://www.raspberrypi.com/documentation/
- ARM Architecture: https://developer.arm.com/documentation/

---

## Reflection

This project evolved from "install monitoring" to "understand my infrastructure holistically." The hardware misidentification, while initially frustrating, became a valuable lesson in verification and assumption-testing.

Key insight: **Homelab projects aren't just about getting things working - they're about building troubleshooting methodology, documentation habits, and technical intuition that transfers to professional environments.**

The Pi 5 investment ($60-80) enables not just this project, but a foundation for multiple career-relevant projects over the next year. That's strategic thinking over tactical savings.

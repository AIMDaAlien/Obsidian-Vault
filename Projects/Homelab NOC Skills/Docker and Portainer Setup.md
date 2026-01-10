---
created: '2026-01-07T22:57:31.997978'
modified: '2026-01-10T11:25:55.360552'
privacy_scan: not_scanned
published_to_garden: false
tags:
- docker
- portainer
- homelab
- setup-guide
- rpi5
title: Docker And Portainer Setup
visibility: private
---

# Docker and Portainer Setup Guide

## Overview
Setting up Docker with Portainer GUI on Raspberry Pi 5 (4GB) as the foundation for the NOC skills homelab.

## Prerequisites
- Raspberry Pi 5 with Raspberry Pi OS (64-bit recommended)
- SSH access configured
- Static IP or DHCP reservation recommended
- Internet connectivity

## Why Docker + Portainer?
- **Docker**: Container runtime - mentioned in nearly every NOC/DC job posting
- **Portainer**: Web-based GUI for managing containers - reduces CLI friction while learning

---

## Phase 1: System Preparation

### 1.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 Check Architecture
```bash
uname -m
# Should show: aarch64 (ARM64)
```

### 1.3 Verify Memory
```bash
free -h
# RPi 5 4GB should show ~3.7GB available
```

---

## Phase 2: Docker Installation

### 2.1 Install Docker via Convenience Script
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2.2 Add User to Docker Group
```bash
sudo usermod -aG docker $USER
```

> **Important**: Log out and back in for group changes to take effect!

### 2.3 Verify Installation
```bash
docker --version
docker run hello-world
```

**Expected output**: Docker version 24.x or higher, successful hello-world container run

---

## Phase 3: Portainer Installation

### 3.1 Create Portainer Volume
```bash
docker volume create portainer_data
```

### 3.2 Deploy Portainer CE
```bash
docker run -d \
  -p 8000:8000 \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

### 3.3 Access Portainer
- Open browser: `https://<RPI_IP>:9443`
- Create admin user on first access
- Select "Local" environment

---

## Troubleshooting

### Issue: Permission denied on docker.sock
**Symptom**: `Got permission denied while trying to connect to the Docker daemon socket`
**Solution**: 
```bash
sudo usermod -aG docker $USER
# Then log out and back in
```

### Issue: Portainer not accessible
**Check**:
```bash
docker ps  # Verify container is running
docker logs portainer  # Check for errors
```

### Issue: ARM compatibility errors
**Note**: Ensure using ARM64-compatible images (most official images support this)

---

## Verification Checklist
- [ ] Docker installed and running
- [ ] User can run docker without sudo
- [ ] Portainer accessible at https://IP:9443
- [ ] Admin account created in Portainer
- [ ] Local environment connected

---

## Session Log
*Updates added as work progresses*

### 2026-01-07 - Initial Setup
- Guide created
- Awaiting RPi 5 connection details to begin

---

## Next Steps
After Docker + Portainer are running:
1. Deploy Uptime Kuma via Portainer (easy first container)
2. Set up Prometheus + Node Exporter
3. Add Grafana and connect to Prometheus

---
*Last Updated: 2026-01-07*



### 2026-01-10 - Docker Installation Complete
**Device**: RPi 5 at 192.168.0.145 (hostname: pi5)
**Docker Version**: 29.1.4, build 0e6fee6
**Status**: ✅ Docker installed and verified with hello-world

**Update**: Changed Portainer image from `:latest` to `:lts` per current Portainer documentation (Jan 2026). LTS provides more stable, long-term supported releases.

**Corrected Portainer command**:
```bash
docker run -d \
  -p 8000:8000 \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:lts
```

**Access URL**: https://192.168.0.145:9443
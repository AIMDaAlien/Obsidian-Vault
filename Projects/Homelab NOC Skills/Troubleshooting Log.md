---
created: '2026-01-07T22:57:45.339981'
modified: '2026-01-10T23:18:57.729892'
privacy_scan: not_scanned
published_to_garden: false
tags:
- troubleshooting
- homelab
- documentation
- problem-solving
title: Troubleshooting Log
visibility: private
---

# Troubleshooting Log - NOC Skills Homelab

## Purpose
Running log of issues encountered and solutions found during the homelab build. This serves as both personal reference and portfolio documentation of problem-solving skills.

---

## Format Template
```
### [DATE] - Brief Issue Title
**Symptom**: What was observed
**Context**: What we were doing when it happened
**Root Cause**: Why it happened
**Solution**: How we fixed it
**Prevention**: How to avoid in future
**Time to Resolve**: X minutes
```

---

## Docker Issues

*(No issues logged yet)*

---

## Portainer Issues

*(No issues logged yet)*

---

## Prometheus Issues

*(No issues logged yet)*

---

## Grafana Issues

*(No issues logged yet)*

---

## Network Issues

*(No issues logged yet)*

---

## General Linux/RPi Issues

*(No issues logged yet)*

---

## Lessons Learned Summary
*Aggregated insights that would be valuable in interviews*

| Category | Lesson | Interview Angle |
|----------|--------|-----------------|
| | | |

---
*Last Updated: 2026-01-07*



## Network/SSH Issues

### 2026-01-09 - SSH Connection Instability + Wrong Device
**Symptom**: SSH connection reset, refused, timed out. Eventually connected but to wrong Pi.
**Context**: Attempting to SSH to RPi 5 at 192.168.0.117
**Root Cause**: 
1. RPi may have been rebooting/updating
2. IP 192.168.0.117 actually belongs to Pi-hole (RPi B+), not RPi 5
3. Interrupted apt upgrade required `sudo dpkg --configure -a` to fix

**Indicators of wrong device**:
- `armv6l` instead of `aarch64`
- 427MB RAM instead of 4GB
- Hostname shows `pihole`

**Solution**: Need to identify correct IP for RPi 5
**Prevention**: 
- Set static IPs or DHCP reservations for each Pi
- Use distinct hostnames
- Document IP assignments

**Time to Resolve**: ~30 min debugging + next day dpkg fix

---


### Resolution - Correct Device Found
**RPi 5 IP**: 192.168.0.145 (hostname: pi5)
**RPi B+ IP**: 192.168.0.117 (hostname: pihole)

System verified:
- aarch64 architecture
- 4GB RAM (3.4Gi available)
- 49GB disk free
- Kernel 6.12.47

**Lesson**: Maintain IP address documentation for all homelab devices.



---
## Troubleshooting: 2026-01-10

### Alertmanager dpkg Error
**Symptom**: `prometheus user already exists but is not system user`
**Solution**: Skip apt, use Docker instead
```bash
docker run -d --name alertmanager --restart=always -p 9093:9093 \
  -v /etc/prometheus/alertmanager.yml:/etc/alertmanager/alertmanager.yml \
  prom/alertmanager:latest
```

### Prometheus YAML Duplicates
**Symptom**: `field alerting already set in type config.plain`
**Cause**: Added sections without removing existing ones
**Solution**: Replace entire prometheus.yml, ensure no duplicate keys
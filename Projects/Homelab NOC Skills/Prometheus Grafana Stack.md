---
created: '2026-01-10T12:05:16.232280'
modified: '2026-01-10T23:18:48.631817'
privacy_scan: not_scanned
published_to_garden: false
tags: [monitoring]
- prometheus
- grafana
- monitoring
- homelab
- blackbox
title: Prometheus Grafana Stack
visibility: review
---

# Prometheus + Grafana Stack

## Overview
Full observability stack running as native systemd services on RPi 5. Set up ~10 weeks ago, operational and collecting data.

## Components

| Service | Port | Install Type |
|---------|------|--------------|
| Prometheus | :9090 | systemd |
| Node Exporter | :9100 | systemd |
| Blackbox Exporter | :9115 | systemd |
| Grafana | :3000 | systemd |

## Access URLs
- Prometheus: http://192.168.0.145:9090
- Grafana: http://192.168.0.145:3000
- Node Exporter: http://192.168.0.145:9100/metrics
- Blackbox Exporter: http://192.168.0.145:9115

## Configuration

### Prometheus Config
Location: `/etc/prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'blackbox'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets:
          - https://google.com
          - https://github.com
          - https://prometheus.io
          - http://192.168.0.145:9090
          - http://192.168.0.145:3000
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: localhost:9115

  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

### Blackbox Config
Location: `/etc/blackbox_exporter/blackbox.yml`

Modules configured:
- http_2xx (HTTP GET, follows redirects)
- http_post_2xx (HTTP POST)
- tcp_connect (TCP port check)
- icmp_ping (ICMP ping)
- dns_query (DNS resolution)

## Grafana Dashboards

### 1. Blackbox Exporter Dashboard
- HTTP probe status (up/down)
- Response codes
- SSL certificate expiry
- Probe duration metrics

### 2. Node Exporter Full
- CPU, Memory, Disk usage
- Network traffic
- System load
- Filesystem metrics

## Traffic Note
Blackbox probes external targets every 15s, generating ~5,760 DNS queries/day per target. This is normal and expected behavior visible in Pi-hole logs.

## Next Steps
- [ ] Add Pi-hole to monitoring targets
- [ ] Add TrueNAS to monitoring targets
- [ ] Configure Alertmanager
- [ ] Set up push notifications (ntfy/Gotify)

---
*Discovered: 2026-01-10 (running ~10 weeks)*



---
## Session Update: 2026-01-10

### Alerting Configured
- **Alertmanager**: Running via Docker on :9093
- **ntfy**: Self-hosted on :8080, topic `homelab`
- **Alert rule**: ServiceDown (probe_success == 0 for 1m)

### Current Prometheus Targets
**Blackbox (HTTP):**
- google.com, github.com, prometheus.io
- Pi5 Prometheus/Grafana
- Router (192.168.0.1)
- TrueNAS (192.168.0.120)
- Pi-hole (192.168.0.117/admin)
- Immich (192.168.0.120:30041)

**Ping (ICMP):**
- Router, Pi-hole, TrueNAS, 8.8.8.8

### New Services Added
- Homepage (:3001) - Dashboard
- Watchtower - Auto-updates containers
- Vaultwarden - Password manager (on TrueNAS)

### Alertmanager Config
Location: `/etc/prometheus/alertmanager.yml`
```yaml
route:
  receiver: 'ntfy'
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h

receivers:
  - name: 'ntfy'
    webhook_configs:
      - url: 'http://172.17.0.1:8080/homelab'
        send_resolved: true
```
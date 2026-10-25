---
tags: [guide, monitoring, hardware-constraints, troubleshooting, security, prometheus, grafana, homelab, blackbox, raspberry-pi]
created: 2025-10-14
updated: 2026-10-25
publish: true
status: deployed
featured: 20
summary: "A home monitoring stack on a Raspberry Pi 5 in under 300MB of RAM: the build steps, the wrong-Pi lesson that started it, and the deployed config."
---
# Prometheus + Grafana Monitoring Stack - Implementation Guide

> Merged 2026-10-25 from: Prometheus Grafana Monitoring Stack - Lessons Learned, Prometheus Grafana Stack.

## Overview

This document provides a step-by-step implementation guide for deploying Prometheus, Node Exporter, and Grafana on a Raspberry Pi 5. Created as a companion to the [[Prometheus Grafana Stack - Implementation Guide#Lessons learned|Prometheus Grafana Monitoring Stack - Lessons Learned]] document.

**Deployment Date:** October 18, 2025
**Hardware:** Raspberry Pi 5 Model B Rev 1.0, 4GB RAM
**OS:** Raspberry Pi OS Lite 64-bit (Debian 12 Bookworm)
**IP Address:** <lan-ip-6>

---

##  Time-Sensitive Information

**Software versions documented here were current as of October 2025:**
- Prometheus 3.7.0 (released Oct 15, 2025)
- Grafana 12.3.0 (released Oct 16, 2025)
- Node Exporter 1.9.1 (released Apr 1, 2025)

**Before following this guide:**
1. Check for newer stable releases at official sources
2. Verify ARM64 binary availability for your architecture
3. Review release notes for breaking changes
4. Adjust version numbers in commands accordingly

**What will age:**
- Exact version numbers and download URLs
- APT repository configurations (though Grafana's is stable)
- Dashboard IDs may work for years but could be deprecated
- Prometheus 3.x → 4.x might introduce breaking changes (like 2.x → 3.x did)

**What stays relevant:**
- Overall architecture and component relationships
- Systemd service configuration patterns
- Prometheus query language (PromQL) fundamentals
- Grafana data source connection methodology

---

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│         Raspberry Pi 5 (<lan-ip-6>)      │
│                                             │
│  ┌──────────────┐      ┌─────────────────┐ │
│  │  Prometheus  │◄─────┤  Node Exporter  │ │
│  │   :9090      │      │      :9100      │ │
│  └──────┬───────┘      └─────────────────┘ │
│         │                                   │
│         │ Queries                           │
│         ▼                                   │
│  ┌──────────────┐                          │
│  │   Grafana    │                          │
│  │    :3000     │                          │
│  └──────────────┘                          │
└─────────────────────────────────────────────┘
         ▲
         │ HTTP Access
         │
   ┌─────┴─────┐
   │  Browser  │
   └───────────┘
```

**Data Flow:**
1. Node Exporter exposes system metrics on :9100
2. Prometheus scrapes :9100 every 15 seconds
3. Prometheus stores time-series data locally
4. Grafana queries Prometheus and visualizes data
5. User accesses Grafana dashboards via browser

---

## Prerequisites

### Hardware Requirements
- Raspberry Pi 3B+ or newer (4-core ARM recommended)
- Minimum 1GB RAM (4GB recommended for multiple projects)
- 8GB+ storage (monitoring uses ~2GB/day with 7-day retention)
- Stable network connection

### System Requirements
```bash
# Verify your system meets requirements
uname -a
# Expected: Linux pi5 6.12.47+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.47-1+rpt1 (2025-09-16) aarch64 GNU/Linux

free -h
# Expected: At least 1GB total RAM

df -h
# Expected: At least 10GB free storage
```

**Critical Check:**
```bash
# Confirm architecture is aarch64 (64-bit ARM)
uname -m
```
If you see `armv7l` or `armv6l`, you're running 32-bit OS. This guide uses ARM64 binaries. Either:
- Use 32-bit binaries (replace `arm64` with `armv7` or `armv6` in URLs)
- Reinstall OS with 64-bit Raspberry Pi OS

---

## Phase 1: Prometheus Installation

### Step 1: Download Prometheus

```bash
# Navigate to temp directory
cd /tmp

# Download Prometheus ARM64 binary
wget https://github.com/prometheus/prometheus/releases/download/v3.7.0/prometheus-3.7.0.linux-arm64.tar.gz

# Verify download
ls -lh prometheus-3.7.0.linux-arm64.tar.gz
```

**Version Check:** Before running, verify latest stable release at https://github.com/prometheus/prometheus/releases

**Common Issue:** If download fails with SSL errors:
```bash
# Install/update certificates
sudo apt update
sudo apt install ca-certificates -y
```

### Step 2: Extract and Install Binaries

```bash
# Extract archive
tar xvf prometheus-3.7.0.linux-arm64.tar.gz
cd prometheus-3.7.0.linux-arm64

# Copy binaries to system path
sudo cp prometheus promtool /usr/local/bin/

# Verify installation
prometheus --version
promtool --version
```

**Expected Output:**
```
prometheus, version 3.7.0 (branch: HEAD, revision: ...)
  build date:      20251015-...
  go version:      go1.23.2
  platform:        linux/arm64
  tags:            netgo,builtinassets,stringlabels
```

### Step 3: Create System User and Directories

```bash
# Create prometheus user (no login, no home directory)
sudo useradd --no-create-home --shell /bin/false prometheus

# Create configuration directory
sudo mkdir -p /etc/prometheus

# Create data storage directory
sudo mkdir -p /var/lib/prometheus

# Set ownership
sudo chown prometheus:prometheus /var/lib/prometheus
```

**Why these directories:**
- `/etc/prometheus/` - Configuration files (prometheus.yml, rules)
- `/var/lib/prometheus/` - Time-series database storage

### Step 4: Configure Prometheus

```bash
# Copy default config
sudo cp prometheus.yml /etc/prometheus/

# Set ownership
sudo chown -R prometheus:prometheus /etc/prometheus

# Edit configuration
sudo nano /etc/prometheus/prometheus.yml
```

**Replace entire contents with:**
```yaml
global:
  scrape_interval: 15s       # How often to scrape targets
  evaluation_interval: 15s   # How often to evaluate rules

scrape_configs:
  # Monitor Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Monitor system metrics via Node Exporter
  - job_name: 'node'
    static_configs:
      - targets: ['localhost:9100']
```

**Configuration Explained:**
- `scrape_interval: 15s` - Balance between granularity and storage
- `job_name: 'prometheus'` - Self-monitoring (meta!)
- `job_name: 'node'` - System metrics from Node Exporter (we'll install next)

**Save:** `Ctrl+O`, `Enter`, `Ctrl+X`

### Step 5: Create Systemd Service

```bash
sudo nano /etc/systemd/system/prometheus.service
```

**Paste this configuration:**
```ini
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus/ \
  --web.listen-address=0.0.0.0:9090 \
  --storage.tsdb.retention.time=7d \
  --web.enable-lifecycle

[Install]
WantedBy=multi-user.target
```

**Key flags explained:**
- `--config.file` - Where to find prometheus.yml
- `--storage.tsdb.path` - Where to store time-series data
- `--web.listen-address=0.0.0.0:9090` - Listen on all interfaces, port 9090
- `--storage.tsdb.retention.time=7d` - Keep 7 days of data (adjust based on storage)
- `--web.enable-lifecycle` - Allow config reloads via API

** Prometheus 3.x Change:** Old guides include these flags - DON'T add them:
```ini
#  REMOVED IN 3.x - Do NOT include:
--web.console.templates=/etc/prometheus/consoles
--web.console.libraries=/etc/prometheus/console_libraries
```
These directories don't exist in Prometheus 3.x (console UI was rewritten in React).

### Step 6: Start Prometheus

```bash
# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable prometheus

# Start service now
sudo systemctl start prometheus

# Check status
sudo systemctl status prometheus
```

**Expected Status:**
```
● prometheus.service - Prometheus
     Loaded: loaded (/etc/systemd/system/prometheus.service; enabled; preset: enabled)
     Active: active (running) since Sat 2025-10-18 11:33:08 EDT; 26min ago
```

**If service fails:**
```bash
# View detailed logs
sudo journalctl -u prometheus -n 50 --no-pager

# Common issues:
# - Permission errors: Check /var/lib/prometheus ownership
# - Config errors: Validate with 'promtool check config /etc/prometheus/prometheus.yml'
# - Port conflict: Check if 9090 already in use with 'ss -tulnp | grep 9090'
```

### Step 7: Verify Prometheus

```bash
# Check if Prometheus is listening
ss -tulnp | grep 9090

# Test health endpoint
curl http://localhost:9090/-/healthy

# Expected: Prometheus is Healthy.
```

**Access Web UI:**
- From Pi: http://localhost:9090
- From network: http://<lan-ip-6>:9090 (use your Pi's IP)

**Initial UI exploration:**
- Status → Targets (will show prometheus UP, node DOWN until we install Node Exporter)
- Query → Type `up` → Execute (shows which targets are reachable)

---

## Phase 2: Node Exporter Installation

Node Exporter exposes system metrics (CPU, RAM, disk, network) for Prometheus to scrape.

### Step 1: Download Node Exporter

```bash
cd /tmp

# Download Node Exporter ARM64 binary
wget https://github.com/prometheus/node_exporter/releases/download/v1.9.1/node_exporter-1.9.1.linux-arm64.tar.gz

# Extract
tar xvf node_exporter-1.9.1.linux-arm64.tar.gz
cd node_exporter-1.9.1.linux-arm64
```

**Version Check:** Verify latest at https://github.com/prometheus/node_exporter/releases

### Step 2: Install Binary

```bash
# Copy binary
sudo cp node_exporter /usr/local/bin/

# Create user
sudo useradd --no-create-home --shell /bin/false node_exporter

# Verify
node_exporter --version
```

### Step 3: Create Systemd Service

```bash
sudo nano /etc/systemd/system/node_exporter.service
```

**Paste:**
```ini
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```

**Default collectors enabled:**
- CPU, memory, disk, network, filesystem stats
- No custom flags needed for basic monitoring

### Step 4: Start Node Exporter

```bash
sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter
sudo systemctl status node_exporter
```

### Step 5: Verify Node Exporter

```bash
# Check if listening
ss -tulnp | grep 9100

# Test metrics endpoint
curl http://localhost:9100/metrics | head -20
```

**Expected output:** Long list of metrics starting with `# HELP` and `# TYPE` comments.

**In Prometheus UI:**
- Status → Targets
- Both `prometheus` and `node` should show **UP** in green

**Test a query:**
- Query tab → Enter: `node_cpu_seconds_total`
- Execute → Should show CPU metrics with multiple labels (cpu, mode)

---

## Phase 3: Grafana Installation

### Step 1: Add Grafana APT Repository

```bash
# Create keyring directory
sudo mkdir -p /etc/apt/keyrings/

# Download and add Grafana GPG key
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null

# Add Grafana repository
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
```

**Why APT repository:**
- Easier updates with `apt upgrade`
- Automatic dependency management
- Grafana maintains stable repo (unlikely to break)

**Note:** Debian 12 has HTTPS support built-in. Old guides say to install `apt-transport-https` - not needed anymore.

### Step 2: Install Grafana

```bash
# Update package list
sudo apt update

# Install Grafana
sudo apt install grafana -y
```

**Installation size:** ~250MB including dependencies

### Step 3: Start Grafana

```bash
# Enable service
sudo systemctl enable grafana-server

# Start service
sudo systemctl start grafana-server

# Check status
sudo systemctl status grafana-server
```

**Expected:**
```
● grafana-server.service - Grafana instance
     Loaded: loaded (/usr/lib/systemd/system/grafana-server.service; enabled)
     Active: active (running) since Sat 2025-10-18 11:41:26 EDT; 18min ago
```

### Step 4: Access Grafana Web UI

**URL:** http://<lan-ip-6>:3000 (use your Pi's IP)

**Default Credentials:**
- Username: `admin`
- Password: `admin`

**First Login:**
- System will prompt password change
- Choose strong password (you'll need it for future access)

---

## Phase 4: Configure Grafana

### Step 1: Add Prometheus Data Source

1. **Navigate:** Connections → Data sources → Add data source
2. **Select:** Prometheus
3. **Configure:**
   - Name: `Prometheus` (default)
   - URL: `http://localhost:9090`
   - Access: `Server (default)`
   - Leave all other settings default
4. **Save & Test** (scroll to bottom)

**Expected:** Green success message: "Successfully queried the Prometheus API."

**Troubleshooting:**
- Red error → Check Prometheus is running: `sudo systemctl status prometheus`
- Timeout → Verify URL is exactly `http://localhost:9090` (no trailing slash)

### Step 2: Import Node Exporter Dashboard

Pre-built dashboards save hours of work. Dashboard 1860 is the most popular for Node Exporter.

1. **Navigate:** Dashboards → New → Import
2. **Import via grafana.com:** Enter `1860`
3. **Click Load**
4. **Configure:**
   - Name: Node Exporter Full (pre-filled)
   - Folder: General (or create new)
   - Prometheus: Select `Prometheus` from dropdown
5. **Click Import**

**What you'll see:**
- CPU usage (busy, idle, system, user)
- Memory usage (used, cached, buffered, free)
- Disk I/O (read/write rates)
- Network traffic (receive/transmit)
- System uptime, load averages
- Filesystem usage per mount point

**Dashboard sections (expandable):**
- Quick CPU/Memory/Disk overview
- Basic metrics graphs
- Detailed CPU/Memory/Network/Disk panels

** Dashboard Aging:**
Dashboard 1860 is maintained by the community. If it stops working in future:
1. Search grafana.com for "node exporter" dashboards
2. Sort by downloads/stars
3. Check "Updated" date (recent is better)
4. Import alternative dashboard ID

### Step 3: Explore Your Metrics

**Quick wins to check:**
1. CPU usage should be low (0-5%) at idle
2. RAM usage ~800MB (OS + monitoring stack)
3. Disk should show your microSD/NVMe capacity
4. Network should show active interface traffic

**Time range selection (top right):**
- Last 6 hours (default)
- Last 24 hours (good overview)
- Last 7 days (see retention working)

---

## URLs and Access Points

| Service | Port | Local URL | Network URL | Purpose |
|---------|------|-----------|-------------|---------|
| Prometheus | 9090 | http://localhost:9090 | http://<lan-ip-6>:9090 | Time-series database + query UI |
| Node Exporter | 9100 | http://localhost:9100/metrics | http://<lan-ip-6>:9100/metrics | System metrics endpoint |
| Grafana | 3000 | http://localhost:3000 | http://<lan-ip-6>:3000 | Dashboard and visualization |

**Security Note:** All services are HTTP (not HTTPS). Acceptable for local homelab. For internet-facing deployments, add reverse proxy with TLS.

---

## Resource Usage

**Current consumption (October 18, 2025):**
```
Prometheus:     ~80MB RAM, 2.0s CPU
Node Exporter:  ~20MB RAM, 2.5s CPU
Grafana:        ~180MB RAM, 12s CPU
Total:          ~280MB RAM, ~17s CPU (4-core system)
```

**Storage growth:**
- Prometheus TSDB: ~2GB per day (7-day retention = ~14GB max)
- Grafana database: Minimal (<100MB)

**Expected disk usage after 1 week:** ~15GB

---

## Maintenance Commands

### Check Service Status
```bash
# All monitoring services
sudo systemctl status prometheus node_exporter grafana-server --no-pager
```

### Restart Services
```bash
# Restart individual service
sudo systemctl restart prometheus
sudo systemctl restart node_exporter
sudo systemctl restart grafana-server

# Restart all
sudo systemctl restart prometheus node_exporter grafana-server
```

### View Logs
```bash
# Prometheus logs (last 50 lines)
sudo journalctl -u prometheus -n 50 --no-pager

# Node Exporter logs
sudo journalctl -u node_exporter -n 50 --no-pager

# Grafana logs
sudo journalctl -u grafana-server -n 50 --no-pager

# Follow logs in real-time
sudo journalctl -u prometheus -f
```

### Update Prometheus Configuration
```bash
# Edit config
sudo nano /etc/prometheus/prometheus.yml

# Validate config
promtool check config /etc/prometheus/prometheus.yml

# Reload without restart (if web.enable-lifecycle flag set)
curl -X POST http://localhost:9090/-/reload

# Or restart service
sudo systemctl restart prometheus
```

### Storage Management
```bash
# Check Prometheus data size
sudo du -sh /var/lib/prometheus

# Check oldest data
ls -lh /var/lib/prometheus/

# Manually clean old data (dangerous!)
# Prometheus auto-manages retention based on --storage.tsdb.retention.time flag
```

---

## Troubleshooting

### Prometheus Won't Start
```bash
# Check logs
sudo journalctl -u prometheus -n 50

# Common issues:
# 1. Config syntax error
promtool check config /etc/prometheus/prometheus.yml

# 2. Permission issues
sudo chown -R prometheus:prometheus /var/lib/prometheus /etc/prometheus

# 3. Port already in use
ss -tulnp | grep 9090
```

### Node Exporter Metrics Not Showing
```bash
# Verify Node Exporter is running
sudo systemctl status node_exporter

# Test metrics endpoint
curl http://localhost:9100/metrics

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq '.'

# Common issue: Firewall blocking (unlikely on local)
```

### Grafana Dashboard Shows "No Data"
1. **Check data source:**
   - Connections → Data sources → Prometheus → Save & Test
2. **Verify Prometheus has data:**
   - Go to Prometheus UI → Query → Enter `up` → Execute
   - Should show targets
3. **Check time range:**
   - Dashboard time picker (top right) → Set to "Last 6 hours"
4. **Panel-specific issue:**
   - Edit panel → Check query syntax
   - Prometheus → Test query in Prometheus UI directly

### High Memory Usage
```bash
# Check actual usage
free -h

# Identify culprit
ps aux --sort=-%mem | head -10

# If Prometheus using too much:
# - Reduce scrape frequency in prometheus.yml (30s instead of 15s)
# - Reduce retention time (3d instead of 7d)
# - Add --storage.tsdb.min-block-duration=2h flag (larger blocks = less overhead)
```

---

## Adding More Targets

### Monitor Another Linux Server

**On target server:**
```bash
# Install Node Exporter (same steps as above)
wget https://github.com/prometheus/node_exporter/releases/download/v1.9.1/node_exporter-1.9.1.linux-amd64.tar.gz
tar xvf node_exporter-1.9.1.linux-amd64.tar.gz
sudo cp node_exporter-1.9.1.linux-amd64/node_exporter /usr/local/bin/

# Create systemd service (same as above)
# Start and enable
```

**On Prometheus server (Pi5):**
```bash
sudo nano /etc/prometheus/prometheus.yml
```

Add under `scrape_configs`:
```yaml
  - job_name: 'remote-server'
    static_configs:
      - targets: ['192.168.0.xxx:9100']
        labels:
          alias: 'server-name'
```

```bash
# Reload Prometheus
curl -X POST http://localhost:9090/-/reload
```

### Monitor Pi-hole

**After migrating Pi-hole to this Pi:**
```bash
# Install Pi-hole Exporter
wget https://github.com/eko/pihole-exporter/releases/download/v0.4.0/pihole_exporter-linux-arm64
sudo mv pihole_exporter-linux-arm64 /usr/local/bin/pihole_exporter
sudo chmod +x /usr/local/bin/pihole_exporter

# Create systemd service
sudo nano /etc/systemd/system/pihole_exporter.service
```

```ini
[Unit]
Description=Pi-hole Exporter
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/pihole_exporter -pihole_hostname 127.0.0.1 -port 9617

[Install]
WantedBy=multi-user.target
```

```bash
# Start
sudo systemctl enable pihole_exporter
sudo systemctl start pihole_exporter

# Add to Prometheus
sudo nano /etc/prometheus/prometheus.yml
```

Add:
```yaml
  - job_name: 'pihole'
    static_configs:
      - targets: ['localhost:9617']
```

**Import Pi-hole Dashboard:**
- Dashboard ID: 10176 (popular Pi-hole dashboard)

---

## Security Considerations

### Current Setup (Homelab-Safe)
- HTTP only (no TLS/SSL)
- No authentication on Prometheus/Node Exporter
- Grafana has password protection
- Services listen on all interfaces (0.0.0.0)

**This is acceptable because:**
- Services on internal network only
- Not exposed to internet
- Trusted local network

### Production/Internet-Facing Setup
If exposing to internet, add:

1. **Reverse Proxy (Nginx/Caddy):**
   - Terminate TLS
   - Add basic auth to Prometheus
   - Rate limiting

2. **Firewall Rules:**
   ```bash
   # Allow only specific IPs to monitoring ports
   sudo ufw allow from 192.168.0.0/24 to any port 9090
   sudo ufw allow from 192.168.0.0/24 to any port 3000
   ```

3. **Grafana Settings:**
   - Disable user signup
   - Enable HTTPS
   - Use strong passwords

4. **Network Segmentation:**
   - Monitoring on separate VLAN
   - Minimal firewall rules between zones

---

## Future Expansion Ideas

### Monitoring More Services
- **TrueNAS:** SNMP exporter or TrueNAS built-in metrics
- **Network Devices:** SNMP exporter for switches/routers
- **Docker Containers:** cAdvisor for container metrics
- **Home Assistant:** Built-in Prometheus integration
- **Internet Speed:** Speedtest exporter for ISP monitoring
- **SSL Certificates:** Blackbox exporter for cert expiry

### Advanced Features
- **Alerting:** Prometheus Alertmanager for email/Slack/Discord notifications
- **Long-term Storage:** Thanos or Cortex for years of retention
- **Log Aggregation:** Add Loki + Promtail for log collection
- **Distributed Tracing:** Add Tempo for application traces
- **Recording Rules:** Pre-compute expensive queries

### Dashboard Enhancements
- Custom panels for specific metrics
- Variables for multi-server selection
- Annotations for deployment markers
- Alert list panels

---

## Backup Strategy

### What to Backup

**Critical (must backup):**
- `/etc/prometheus/prometheus.yml` - Prometheus config
- `/etc/grafana/grafana.ini` - Grafana config (if customized)
- Grafana dashboards (export as JSON)

**Optional:**
- `/var/lib/prometheus/` - Time-series data (large, regenerates)
- `/var/lib/grafana/grafana.db` - Grafana dashboards/users (if not exported)

### Backup Commands

```bash
# Backup configs
sudo tar czf /tmp/monitoring-backup-$(date +%Y%m%d).tar.gz \
  /etc/prometheus/ \
  /etc/grafana/ \
  /etc/systemd/system/prometheus.service \
  /etc/systemd/system/node_exporter.service

# Copy to safe location
scp /tmp/monitoring-backup-*.tar.gz user@backup-server:/backups/
```

### Export Grafana Dashboards
1. Dashboard → Settings (gear icon) → JSON Model
2. Copy JSON
3. Save to file for version control

**Pro tip:** Store dashboard JSON in Git repository

---

## Performance Tuning

### Reduce Memory Usage
```bash
# Edit Prometheus service
sudo nano /etc/systemd/system/prometheus.service
```

Add flags:
```ini
ExecStart=/usr/local/bin/prometheus \
  ... existing flags ...
  --storage.tsdb.max-block-chunk-segment-size=134217728 \
  --storage.tsdb.min-block-duration=2h
```

### Reduce Storage Growth
```bash
# Less frequent scraping (prometheus.yml)
global:
  scrape_interval: 30s  # Changed from 15s

# Shorter retention (prometheus.service)
--storage.tsdb.retention.time=3d  # Changed from 7d
```

### Optimize Grafana
```bash
sudo nano /etc/grafana/grafana.ini
```

```ini
[analytics]
reporting_enabled = false
check_for_updates = false

[dashboards]
versions_to_keep = 3  # Limit dashboard history
```

```bash
sudo systemctl restart grafana-server
```

---

## Uninstallation (If Needed)

**Complete removal:**
```bash
# Stop services
sudo systemctl stop prometheus node_exporter grafana-server

# Disable services
sudo systemctl disable prometheus node_exporter grafana-server

# Remove binaries
sudo rm /usr/local/bin/prometheus /usr/local/bin/promtool /usr/local/bin/node_exporter

# Remove data
sudo rm -rf /etc/prometheus /var/lib/prometheus

# Remove Grafana
sudo apt remove --purge grafana -y
sudo rm -rf /etc/grafana /var/lib/grafana

# Remove users
sudo userdel prometheus
sudo userdel node_exporter

# Remove systemd services
sudo rm /etc/systemd/system/prometheus.service
sudo rm /etc/systemd/system/node_exporter.service
sudo systemctl daemon-reload
```

---

## Learning Resources

### Official Documentation
- **Prometheus Docs:** https://prometheus.io/docs/introduction/overview/
- **Grafana Docs:** https://grafana.com/docs/grafana/latest/
- **PromQL Tutorial:** https://prometheus.io/docs/prometheus/latest/querying/basics/

### Community Resources
- **Grafana Dashboards:** https://grafana.com/grafana/dashboards/
- **Prometheus Exporters:** https://prometheus.io/docs/instrumenting/exporters/
- **Reddit:** r/prometheus, r/grafana, r/homelab

### Books
- "Prometheus: Up & Running" by Brian Brazil
- "Practical Monitoring" by Mike Julian

---

## What We Built

**Final Stack:**
-  Prometheus 3.7.0 collecting metrics every 15 seconds
-  Node Exporter 1.9.1 exposing system metrics
-  Grafana 12.3.0 visualizing data in real-time dashboard
-  7-day metric retention (~14GB storage)
-  Professional monitoring setup on $60 hardware

**Current Resource Usage:**
- 280MB RAM (of 4GB = 7%)
- Minimal CPU usage (<1% average)
- 15GB disk space (of 57GB = 26%)

**Capabilities:**
- Real-time system health monitoring
- Historical trend analysis
- Foundation for expanding to monitor Pi-hole, TrueNAS, and other services
- Professional-grade observability platform

---

## Next Steps

1. **Run for 1 week** - Verify stability and storage growth
2. **Set up basic alerts** - CPU >80%, RAM >90%, Disk >90%
3. **Migrate Pi-hole** - Move from Pi 1B+ to this Pi 5
4. **Add Pi-hole monitoring** - Install Pi-hole exporter + dashboard
5. **Monitor TrueNAS** - Add SNMP or HTTP exporter
6. **Explore PromQL** - Learn query language for custom panels

---

## Conclusion

You now have a production-ready monitoring stack that provides:
- Complete visibility into system health
- Historical data for troubleshooting
- Foundation for career-relevant skills (SRE, DevOps, Infrastructure)
- Scalable platform for monitoring entire homelab

**Key Achievement:** Built professional monitoring infrastructure that companies pay thousands for, on $60 hardware, using open-source tools.

**Career Value:** This project demonstrates:
- Systems thinking and architecture design
- Service deployment and configuration management
- Observability best practices
- Troubleshooting methodology
- Documentation skills

Perfect for showcasing in interviews or on a portfolio.

---

**Related Documents:**

## Lessons learned

### Overview
This document captures lessons learned from planning and researching a comprehensive monitoring stack for a homelab environment. It serves as both a post-mortem and educational resource for others considering similar projects.

### Executive Summary

**Goal**: Deploy Prometheus + Grafana monitoring for homelab infrastructure (Pi-hole, TrueNAS, network devices)

**Key Findings**:
- Hardware verification is critical before planning
- Prometheus 3.x introduced breaking changes removing console libraries
- ARM architecture can be misleading on Raspberry Pi
- Resource requirements scale beyond base monitoring when planning multiple projects

**Outcome**: Hardware upgrade required (Pi 1B+ → Pi 5 4GB)

---

### Career Context: Why This Project Matters

#### IT Career Pathways
Traditional helpdesk roles are declining due to automation. Modern IT careers cluster around:

1. **DevOps/SRE** - Automation, CI/CD, infrastructure as code
2. **Cloud Infrastructure** - AWS/Azure/GCP management
3. **Deployment Engineering** - Mass-scale provisioning/imaging
4. **Network Engineering** - Advanced troubleshooting, security
5. **Cybersecurity Operations** - SOC analyst, monitoring

#### Why Monitoring Projects Build Career Skills
- **Systems thinking** - Understanding infrastructure holistically
- **Observability** - Industry-standard practice (Prometheus is CNCF graduated)
- **Troubleshooting at scale** - Moving beyond one-off fixes
- **Data-driven decisions** - Metrics inform optimization
- **Remote work friendly** - Most monitoring roles are remote-capable

Monitoring differentiates "fixes computers" from "maintains infrastructure."

---

### Technical Architecture

#### What We're Building

```
Homelab Devices (Pi-hole, NAS, etc.)
        ↓
    Exporters (Port 9100, 9617, etc.)
        ↓
    Prometheus (Scrapes every 15s)
        ↓
    Grafana (Visualizes data)
```

#### Components Explained

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

### Critical Lesson: Hardware Verification

#### The Problem

**Assumed**: Raspberry Pi 3B+ (quad-core, 1GB RAM, ARMv8)
**Reality**: Raspberry Pi 1B+ (single-core, 512MB RAM, ARMv6)

#### How This Happened

1. Multiple Raspberry Pis in homelab
2. SSH'd into wrong device
3. Didn't verify hardware before planning
4. Load warnings (1.1 on "4 processors") were misinterpreted

#### How to Verify Your Hardware

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

#### ARM Architecture Confusion on Raspberry Pi

**Pi 3B+ hardware**: ARMv8 (64-bit Cortex-A53)
**Pi 3B+ OS (standard)**: 32-bit Raspberry Pi OS
**Reported architecture**: armv7l

This happens because:
- Raspberry Pi OS is 32-bit for compatibility across models
- ARMv8 in 32-bit mode acts like ARMv7
- Most software uses armv7 binaries on Pi 3/4

**Key takeaway**: Don't assume architecture from model number alone.

---

### Prometheus 3.x Breaking Changes

#### What Changed

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

#### Impact on Installation

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

#### Why This Matters

- GitHub issues confirm console removal (issue #478)
- Official docs updated but many tutorials aren't
- Copying non-existent directories causes silent failures
- Old systemd services reference paths that don't exist

---

### Resource Requirements & Planning

#### Base Monitoring Stack

| Component | RAM | CPU | Storage |
|-----------|-----|-----|---------|
| Prometheus | 80-120MB | ~5% | 1-2GB/day |
| Grafana | 120-180MB | ~3% | Minimal |
| Node Exporter | ~20MB | ~1% | None |
| **Total** | **~300MB** | **~9%** | **~2GB/day** |

#### Pi-hole + Unbound Baseline
- Pi-hole: ~100MB RAM
- Unbound DNS: ~40MB RAM
- OS overhead: ~250MB RAM
- **Total: ~400MB used**

#### Hardware Capacity Analysis

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

#### Load Average Context

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

### Pi-hole Blocklist Optimization

#### The Problem
400,000 domains on blocklist = excessive for Pi 1B+ hardware

#### Recommended Configuration

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

### Hardware Selection Guide

#### Decision Matrix

| Model | RAM | CPU | Price | Use Case |
|-------|-----|-----|-------|----------|
| Pi 1B+ | 512MB | 1-core | $0 (owned) | Single light service |
| Pi 3B+ | 1GB | 4-core | $25-35 used | Monitoring only |
| Pi 4B 2GB | 2GB | 4-core | $35-45 | Light multi-project |
| Pi 4B 4GB | 4GB | 4-core | $55-65 | Recommended baseline |
| Pi 5 4GB | 4GB | 4-core | $60-80 | Best performance |
| Orange Pi 5 4GB | 4GB | 8-core | $60-70 | Best value/performance |

#### Orange Pi vs Raspberry Pi

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

#### Recommendation Logic

**If you value**:
- Plug-and-play experience → Pi 4B/5
- Maximum community support → Pi 4B/5
- Best performance/price → Orange Pi 5
- Hardware tinkering → Orange Pi 5

**For homelab monitoring + projects**: Pi 5 4GB or Orange Pi 5 4GB

---

### Overclocking Considerations

#### Question: Should I overclock Pi 1B+ while waiting for Pi 5?

**Answer**: No, keep at medium or reduce to stock.

#### Reasoning

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

### Project Selection for Career Development

#### Projects Ranked by Career Signal

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

#### Career Path Matching

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

### Key Takeaways

1. **Verify hardware before planning** - Don't assume, confirm with commands
2. **Check software versions** - Prometheus 3.x has breaking changes from 2.x
3. **Understand ARM architecture** - Pi reports OS arch, not hardware arch
4. **Resource planning matters** - Base requirements + future projects + buffers
5. **Stability over optimization** - Don't risk production for marginal gains
6. **Projects signal career intent** - Choose projects aligned with target role
7. **Documentation prevents repeat mistakes** - This note exists for that reason

---

### Next Steps

1. **Tomorrow**: Receive Pi 5 4GB with active cooler
2. **Day 1-2**: Set up Prometheus 3.7.0 + Node Exporter
3. **Day 3-4**: Install Grafana, create dashboards
4. **Week 2**: Migrate Pi-hole from Pi 1B+ to Pi 5
5. **Week 3**: Add TrueNAS monitoring
6. **Week 4**: Explore next project from career development list

---

### Resources

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

### Reflection

This project evolved from "install monitoring" to "understand my infrastructure holistically." The hardware misidentification, while initially frustrating, became a valuable lesson in verification and assumption-testing.

Key insight: **Homelab projects aren't just about getting things working - they're about building troubleshooting methodology, documentation habits, and technical intuition that transfers to professional environments.**

The Pi 5 investment ($60-80) enables not just this project, but a foundation for multiple career-relevant projects over the next year. That's strategic thinking over tactical savings.

## Appendix, deployed state 2026-01

### Overview
Full observability stack running as native systemd services on RPi 5. Set up ~10 weeks ago, operational and collecting data.

### Components

| Service | Port | Install Type |
|---------|------|--------------|
| Prometheus | :9090 | systemd |
| Node Exporter | :9100 | systemd |
| Blackbox Exporter | :9115 | systemd |
| Grafana | :3000 | systemd |

### Access URLs
- Prometheus: http://<lan-ip-6>:9090
- Grafana: http://<lan-ip-6>:3000
- Node Exporter: http://<lan-ip-6>:9100/metrics
- Blackbox Exporter: http://<lan-ip-6>:9115

### Configuration

#### Prometheus Config
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
          - http://<lan-ip-6>:9090
          - http://<lan-ip-6>:3000
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

#### Blackbox Config
Location: `/etc/blackbox_exporter/blackbox.yml`

Modules configured:
- http_2xx (HTTP GET, follows redirects)
- http_post_2xx (HTTP POST)
- tcp_connect (TCP port check)
- icmp_ping (ICMP ping)
- dns_query (DNS resolution)

### Grafana Dashboards

#### 1. Blackbox Exporter Dashboard
- HTTP probe status (up/down)
- Response codes
- SSL certificate expiry
- Probe duration metrics

#### 2. Node Exporter Full
- CPU, Memory, Disk usage
- Network traffic
- System load
- Filesystem metrics

### Traffic Note
Blackbox probes external targets every 15s, generating ~5,760 DNS queries/day per target. This is normal and expected behavior visible in Pi-hole logs.

### Next Steps
- [ ] Add Pi-hole to monitoring targets
- [ ] Add TrueNAS to monitoring targets
- [ ] Configure Alertmanager
- [ ] Set up push notifications (ntfy/Gotify)

---
*Discovered: 2026-01-10 (running ~10 weeks)*

---
### Session Update: 2026-01-10

#### Alerting Configured
- **Alertmanager**: Running via Docker on :9093
- **ntfy**: Self-hosted on :8080, topic `homelab`
- **Alert rule**: ServiceDown (probe_success == 0 for 1m)

#### Current Prometheus Targets
**Blackbox (HTTP):**
- google.com, github.com, prometheus.io
- Pi5 Prometheus/Grafana
- Router (<lan-ip-1>)
- TrueNAS (<lan-ip-5>)
- Pi-hole (<lan-ip-4>/admin)
- Immich (<lan-ip-5>:30041)

**Ping (ICMP):**
- Router, Pi-hole, TrueNAS, 8.8.8.8

#### New Services Added
- Homepage (:3001) - Dashboard
- Watchtower - Auto-updates containers
- Vaultwarden - Password manager (on TrueNAS)

#### Alertmanager Config
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

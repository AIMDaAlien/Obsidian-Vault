---
tags: #homelab #monitoring #prometheus #grafana #raspberry-pi #tutorial #implementation
created: 2025-10-18
status: deployed
related: [[Prometheus Grafana Monitoring Stack - Lessons Learned]]
---

# Prometheus + Grafana Monitoring Stack - Implementation Guide

## Overview

This document provides a step-by-step implementation guide for deploying Prometheus, Node Exporter, and Grafana on a Raspberry Pi 5. Created as a companion to the [[Prometheus Grafana Monitoring Stack - Lessons Learned]] document.

**Deployment Date:** October 18, 2025  
**Hardware:** Raspberry Pi 5 Model B Rev 1.0, 4GB RAM  
**OS:** Raspberry Pi OS Lite 64-bit (Debian 12 Bookworm)  
**IP Address:** 192.168.0.145

---

## ⚠️ Time-Sensitive Information

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
│         Raspberry Pi 5 (192.168.0.145)      │
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

**⚠️ Prometheus 3.x Change:** Old guides include these flags - DON'T add them:
```ini
# ❌ REMOVED IN 3.x - Do NOT include:
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
- From network: http://192.168.0.145:9090 (use your Pi's IP)

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

**URL:** http://192.168.0.145:3000 (use your Pi's IP)

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

**⚠️ Dashboard Aging:**
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
| Prometheus | 9090 | http://localhost:9090 | http://192.168.0.145:9090 | Time-series database + query UI |
| Node Exporter | 9100 | http://localhost:9100/metrics | http://192.168.0.145:9100/metrics | System metrics endpoint |
| Grafana | 3000 | http://localhost:3000 | http://192.168.0.145:3000 | Dashboard and visualization |

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
- ✅ Prometheus 3.7.0 collecting metrics every 15 seconds
- ✅ Node Exporter 1.9.1 exposing system metrics
- ✅ Grafana 12.3.0 visualizing data in real-time dashboard
- ✅ 7-day metric retention (~14GB storage)
- ✅ Professional monitoring setup on $60 hardware

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
- [[Prometheus Grafana Monitoring Stack - Lessons Learned]] - Planning and research phase

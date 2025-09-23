
*A real-world guide documenting the setup of Pi-hole on Raspberry Pi 3 B+ with solutions to common issues*

## Table of Contents
1. [Hardware & Prerequisites](#hardware--prerequisites)
2. [The OS Installation Challenge](#the-os-installation-challenge)
3. [Initial Configuration](#initial-configuration)
4. [Pi-hole Installation](#pi-hole-installation)
5. [Unbound DNS Setup](#unbound-dns-setup)
6. [Privacy Enhancements](#privacy-enhancements)
7. [Lessons Learned](#lessons-learned)

---

## Hardware & Prerequisites

### What You'll Need
- **Raspberry Pi 3 B+** (1GB RAM) - Sufficient for Pi-hole + additional services
- **32GB MicroSD card** (Class 10/A2 recommended)
- **Ethernet cable** (preferred over WiFi for DNS stability)
- **Power supply** (5V, 2.5A minimum)
- **Heatsink** (recommended for 24/7 operation)

### The Initial Question

"I want to get a raspberry pi but not sure which device would be the best for my use case. I just want to use Pi-hole for ad blocking and maybe more privacy features."

### Models Considered

1. **Raspberry Pi Zero 2 W** (~$15)
    - ✅ Ultra budget-friendly
    - ❌ WiFi only, no Ethernet
    - ❌ Limited expansion
2. **Raspberry Pi 3 B+** (~$35-40) ← **CHOSEN**
    - ✅ Perfect for Pi-hole
    - ✅ Gigabit Ethernet
    - ✅ Low power usage
    - ✅ 1GB RAM sufficient for multiple services
3. **Raspberry Pi 4 B** (~$55-75)
    - ✅ Future-proof
    - ❌ Overkill for just Pi-hole
4. **Raspberry Pi 5** (~$80-100)
    - ❌ Excessive for this use case
    - ❌ Requires active cooling

---

## The OS Installation Challenge

### Personal Problem 1: Ethernet Not Working with Raspberry Pi OS Lite

**Initial Attempt:**
- Flashed Raspberry Pi OS Lite (64-bit) using Raspberry Pi Imager
- Configured SSH and credentials through Imager
- Result: No ethernet connectivity, no lights on ethernet port

**Troubleshooting Steps Tried:**
1. Verified SD card integrity (no corruption)
2. Tested with original 8GB SD card - worked perfectly with full Desktop OS
3. Tried Legacy Lite OS - still no ethernet

**Solution:**
```bash
# Use Raspberry Pi OS with Desktop (32-bit) - NOT "with recommended software"
# After first boot, remove GUI to reclaim RAM:

sudo raspi-config
# System Options > Boot / Auto Login > Console

# Then remove desktop packages:
sudo apt purge xserver* lightdm* raspberrypi-ui-mods vlc* lxde* chromium* -y
sudo apt autoremove -y
sudo reboot
```

This gives you effectively Lite OS but with working ethernet drivers.

---

## Initial Configuration

### Personal Problem 2: Keyboard Layout Issues

**Issue:** Pipe symbol (|) appearing as tilde (~), making command entry difficult. Found out the default setting for locale was set to en_GB (British) so I had to set it to en_US.

**Solution 1 - Via raspi-config:**
```bash
sudo raspi-config
# Localisation Options > Keyboard
# Generic 104-key PC > Other > English (US) > English (US)
```

**Solution 2 - Direct reconfiguration (if above doesn't stick):**
```bash
sudo dpkg-reconfigure keyboard-configuration
sudo reboot
```

### Setting Static IP Address

For network 192.168.0.x:
```bash
sudo nano /etc/dhcpcd.conf

# Add at end:
interface eth0
static ip_address=192.168.0.117/24  # Your desired IP
static routers=192.168.0.1           # Your router IP
static domain_name_servers=192.168.0.1

sudo reboot
```

---

## Pi-hole Installation

### Basic Installation
```bash
# One-command install
curl -sSL https://install.pi-hole.net | bash
```

### Installation Settings
- **Upstream DNS**: Cloudflare (1.1.1.1) - temporary, will replace with Unbound
- **Blocklists**: Select all default lists
- **Web interface**: Enable
- **Privacy mode**: Anonymous mode (if preferred)
- **Logging**: Disabled for privacy (can enable temporarily for troubleshooting)
- **Save the admin password shown at the end!**

### Router Configuration
**For TP-Link routers:**
1. Access router: `192.168.0.1`
2. Navigate: Advanced → Network → DHCP Server
3. Primary DNS: `192.168.0.117` (your Pi's IP)
4. Secondary DNS: Leave blank or `1.1.1.1` as fallback
5. Save and reboot router

---

## Unbound DNS Setup

### Why Unbound?
Instead of forwarding queries to Google/Cloudflare, Unbound queries root DNS servers directly, eliminating third-party logging of your DNS queries.

### Installation
```bash
# Install Unbound
sudo apt install unbound -y

# Download root hints
sudo wget https://www.internic.net/domain/named.root -O /var/lib/unbound/root.hints
```

### Problem 3: Unbound Configuration Errors

**Initial Config Issues:**
- Service failing to start
- Error: "unknown size specifier"

**Root Cause:** Typo in configuration file - `so-rcvbuf: 1ms` instead of `1m`

**Working Configuration:**
```bash
sudo nano /etc/unbound/unbound.conf.d/pi-hole.conf
```

```yaml
server:
    interface: 127.0.0.1
    port: 5335
    do-ip4: yes
    do-udp: yes
    do-tcp: yes
    do-ip6: no
    prefer-ip6: no
    harden-glue: yes
    harden-dnssec-stripped: yes
    use-caps-for-id: no
    edns-buffer-size: 1232
    prefetch: yes
    num-threads: 1
    so-rcvbuf: 1m  # <- This was the issue! Not "1ms"
    private-address: 192.168.0.0/16
    private-address: 10.0.0.0/8
    private-address: 172.16.0.0/12
```

### Testing & Integration
```bash
# Restart and test Unbound
sudo service unbound restart
dig google.com @127.0.0.1 -p 5335

# Should see "NOERROR" in response
```

### Configure Pi-hole to Use Unbound
1. Access Pi-hole admin: `http://192.168.0.117/admin`
2. Settings → DNS
3. Uncheck all upstream DNS servers
4. Custom 1 (IPv4): `127.0.0.1#5335`
5. Save

---

## Privacy Enhancements

### Essential Blocklists for Telemetry & Privacy

Add via Admin Panel → Adlists:

```text
# Smart TV & IoT Device Telemetry
https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt

# Microsoft Telemetry
https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt

# Samsung Specific
https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/native.samsung.txt

# Xiaomi Devices
https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/native.xiaomi.txt

# General Privacy
https://someonewhocares.org/hosts/zero/hosts
https://v.firebog.net/hosts/Prigent-Ads.txt
```

After adding, update gravity:
```bash
pihole -g
```

### SD Card Protection with Log2RAM
Prevents excessive writes from wearing out SD card:

```bash
echo "deb [signed-by=/usr/share/keyrings/azlux-archive-keyring.gpg] http://packages.azlux.fr/debian/ bookworm main" | sudo tee /etc/apt/sources.list.d/azlux.list
sudo wget -O /usr/share/keyrings/azlux-archive-keyring.gpg https://azlux.fr/repo.gpg
sudo apt update
sudo apt install log2ram
```

### Enable DNSSEC
Admin Panel → Settings → DNS → Enable DNSSEC ✓

---

## Lessons Learned

### Key Takeaways

1. **Desktop OS can be stripped down to Lite equivalent** - Sometimes driver compatibility makes this necessary

2. **Always verify configuration syntax** - A single character typo (`1ms` vs `1m`) can prevent services from starting

3. **Keyboard layout matters** - Check this early if commands aren't working as expected

4. **Privacy is layered**:
   - Pi-hole blocks at DNS level
   - Unbound provides DNS independence
   - Blocklists target specific privacy threats
   - Additional services (WireGuard) extend protection outside home

5. **Resource Management on Pi 3 B+**:
   - 1GB RAM is sufficient for Pi-hole + Unbound + light services
   - With current setup: ~400MB RAM used, ~600MB free
   - Can add: VPN, monitoring, or file sharing services

### Performance After Setup
- **Ads blocked**: 40-70% of requests
- **Telemetry reduced**: Samsung TV went from 14,000 to <100 daily requests
- **Page load times**: 15-30% faster due to blocked ad content
- **Annual power cost**: ~$3-5 for 24/7 operation

### Next Possible Steps
1. **WireGuard VPN** - Secure remote access & mobile ad blocking
2. **Netdata** - Real-time performance monitoring
3. **Uptime Kuma** - Service monitoring dashboard
4. **Syncthing** - Private file synchronization

---

## Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| No ethernet on Lite OS | Use Desktop OS and strip GUI |
| Keyboard layout wrong | `sudo dpkg-reconfigure keyboard-configuration` |
| Unbound won't start | Check config syntax, especially units (m not ms) |
| Can't access Pi-hole admin | Ensure static IP is set correctly |
| Blocklists not updating | Run `pihole -g` manually |
| High CPU usage | Check for SD card issues, consider USB boot |

---

## Final Thoughts

This setup transforms a $40 Raspberry Pi into a powerful privacy tool that:
- Blocks ads and tracking network-wide
- Prevents IoT devices from phoning home
- Provides complete DNS independence
- Costs less than $5/year in electricity

The journey included several troubleshooting challenges, but each provided valuable learning about Linux, networking, and privacy. The end result is a robust, private, and efficient home network guardian.

---

*Document created from real setup experience, September 2024*
*Hardware: Raspberry Pi 3 B+, 32GB SanDisk SD Card*
*Final config: Pi-hole + Unbound + Enhanced blocklists*
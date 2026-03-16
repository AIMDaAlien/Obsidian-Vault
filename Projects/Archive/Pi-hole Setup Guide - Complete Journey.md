---
garden_path: Projects/Archive/Pi-hole Setup Guide - Complete Journey.md
last_published: '2025-11-28T19:41:13.152631'
published_to_garden: true
---

# Pi-hole Setup: Raspberry Pi 3 B+

> [!abstract] TL;DR
> First Pi-hole build on a Raspberry Pi 3 B+ with a 32GB SD card. Learned that Lite OS had broken ethernet drivers, keyboard layouts matter more than you'd think, and a one-character Unbound config typo can silently kill your DNS. End result: 40–70% of network requests blocked, Samsung TV telemetry dropped from 14,000 to under 100 daily requests.
>
> **This hardware was later retired →** [[Pi-hole Migration - RPi B+ to RPi 5 NVMe]]

---

## Hardware

| Component | Choice                     | Why                                                              |
| --------- | -------------------------- | ---------------------------------------------------------------- |
| Pi model  | Raspberry Pi 3 B+ (~$35)   | Gigabit Ethernet, 1GB RAM, low power — right-sized for Pi-hole   |
| Storage   | 32GB MicroSD (Class 10/A2) | Sufficient for Pi-hole + light services                          |
| Network   | Ethernet cable             | Always use wired for DNS — WiFi drops = everyone's internet dies |
| Cooling   | Heatsink                   | Running 24/7, keeps temps stable                                 |

**Why not other models:**

| Model            | Reason skipped                                  |
| ---------------- | ----------------------------------------------- |
| Zero 2 W (~$15)  | No Ethernet port — non-starter for a DNS server |
| Pi 4 B (~$55–75) | Overkill for just Pi-hole                       |
| Pi 5 (~$80–100)  | Excessive at the time, requires active cooling  |

---

## Phase 1 — OS Install

> [!danger] Problem — Ethernet doesn't work on Pi OS Lite (64-bit)
> Flashed Pi OS Lite via Raspberry Pi Imager, configured SSH through the imager, booted up — zero ethernet. No port lights. No connection.
>
> Tried: SD card swap, Legacy Lite, different cables. None of it helped.

> [!success] Fix — Use Desktop OS, then strip the GUI
> The Pi 3 B+ has ethernet driver quirks on Lite images. Desktop OS includes the right drivers.
>
> ```bash
> # After first boot, switch to console-only mode:
> sudo raspi-config
> # System Options → Boot / Auto Login → Console
>
> # Then remove all the GUI packages:
> sudo apt purge xserver* lightdm* raspberrypi-ui-mods vlc* lxde* chromium* -y
> sudo apt autoremove -y
> sudo reboot
> ```
> Result: Functionally identical to Lite OS, but with working ethernet drivers.

---

## Phase 2 — Initial Config

### Keyboard layout was wrong

The pipe symbol `|` was showing up as `~`. Default locale was `en_GB` (British) — had to switch to `en_US`.

```bash
sudo raspi-config
# Localisation Options → Keyboard
# Generic 104-key PC → Other → English (US) → English (US)

# If it doesn't stick after reboot:
sudo dpkg-reconfigure keyboard-configuration
sudo reboot
```

### Static IP

```bash
sudo nano /etc/dhcpcd.conf

# Add at the end of the file:
interface eth0
static ip_address=192.168.0.117/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1

sudo reboot
```

---

## Phase 3 — Pi-hole Install

```bash
curl -sSL https://install.pi-hole.net | bash
```

**Key install choices:**

| Setting | Value | Note |
|---|---|---|
| Upstream DNS | Cloudflare `1.1.1.1` | Temporary — Unbound replaces this |
| Web interface | Enable | Needed for management |
| Query logging | Disabled | Privacy |
| Admin password | Save it | Shown once at end of install |

**Router config (TP-Link):**
Advanced → Network → DHCP Server
- Primary DNS: `192.168.0.117`
- Secondary DNS: leave blank — a fallback lets devices bypass Pi-hole silently

---

## Phase 4 — Unbound (Recursive DNS)

Cuts out DNS middlemen entirely. Queries go straight to root servers — no Google, no Cloudflare, no third-party logging.

```bash
sudo apt install unbound -y
sudo wget https://www.internic.net/domain/named.root -O /var/lib/unbound/root.hints
```

> [!danger] Problem — Unbound fails to start, no useful error
> Config file had `so-rcvbuf: 1ms` — one extra character. Service silently refuses to start with no obvious output.

> [!success] Fix — It's `1m` not `1ms`
> Check every unit in the config carefully. This one took a while to spot.

**Working config** at `/etc/unbound/unbound.conf.d/pi-hole.conf`:

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
    so-rcvbuf: 1m
    private-address: 192.168.0.0/16
    private-address: 10.0.0.0/8
    private-address: 172.16.0.0/12
```

**Test before wiring to Pi-hole:**
```bash
sudo service unbound restart
dig google.com @127.0.0.1 -p 5335
# Should return NOERROR
```

**Wire Unbound to Pi-hole:**
Pi-hole GUI → Settings → DNS → uncheck all upstream providers → Custom IPv4: `127.0.0.1#5335`

---

## Phase 5 — Privacy Blocklists

**Add in Pi-hole → Adlists:**

```
# Smart TV / IoT telemetry
https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt

# Microsoft telemetry
https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt

# Samsung
https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/native.samsung.txt

# Xiaomi
https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/native.xiaomi.txt

# General privacy
https://someonewhocares.org/hosts/zero/hosts
```

```bash
pihole -g  # update gravity after adding lists
```

**Enable DNSSEC:** Pi-hole GUI → Settings → DNS → Enable DNSSEC ✓

**SD card longevity with Log2RAM** — reduces constant write wear:

```bash
echo "deb [signed-by=/usr/share/keyrings/azlux-archive-keyring.gpg] http://packages.azlux.fr/debian/ bookworm main" | sudo tee /etc/apt/sources.list.d/azlux.list
sudo wget -O /usr/share/keyrings/azlux-archive-keyring.gpg https://azlux.fr/repo.gpg
sudo apt update && sudo apt install log2ram
```

---

## Results

| Metric | Before | After |
|---|---|---|
| Ads blocked | 0% | 40–70% of all requests |
| Samsung TV daily requests | ~14,000 | <100 |
| Page load time | Baseline | ~15–30% faster |
| Annual power cost | — | ~$3–5 |

---

## Troubleshooting Quick Reference

| Problem | Fix |
|---|---|
| No ethernet on Lite OS | Use Desktop OS and strip GUI afterward |
| Keyboard typing wrong characters | `sudo dpkg-reconfigure keyboard-configuration` |
| Unbound won't start | Check config — units must be `1m` not `1ms` |
| Can't reach Pi-hole admin | Verify static IP is correctly set |
| Blocklists not updating | `pihole -g` |
| High CPU / instability | Check SD card health, install Log2RAM |

---

## Key Lessons

> [!tip] What this build taught
> 1. **Driver quirks exist on older Pi hardware** — Desktop OS + strip is a valid workaround for Lite ethernet issues
> 2. **One character typos silently kill services** — `1ms` vs `1m`, zero helpful error output
> 3. **Always check keyboard locale early** — confusing symbols cause weird command failures before you realize the real issue
> 4. **Privacy is layered** — Pi-hole (DNS blocking) + Unbound (DNS independence) + blocklists (targeted telemetry) are three distinct layers
> 5. **Never set a Secondary DNS fallback** — it silently bypasses your filtering

---

*Original setup: September 2024*
*Hardware: Raspberry Pi 3 B+, 32GB SanDisk SD Card*
*This hardware was later retired — see [[Pi-hole Migration - RPi B+ to RPi 5 NVMe]]*

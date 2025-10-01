# WireGuard VPN Setup

**Purpose:** Access home network and Pi-hole from anywhere

**Date:** September 30, 2025

---

## Prerequisites
- Raspberry Pi with Pi-hole running
- Router admin access
- 30-45 minutes

---

## Installation

### 1. Install WireGuard on Pi
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install wireguard -y

# Enable IP forwarding
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 2. Install PiVPN (automates config)
```bash
curl -L https://install.pivpn.io | bash
```

**Installation choices:**
- Protocol: WireGuard
- Port: 51820 (default)
- DNS: Use Pi-hole
- Dynamic DNS: DuckDNS (optional)

---

## Port Forwarding

**Router settings:**
- External Port: 51820
- Internal IP: 192.168.0.117 (Pi's IP)
- Internal Port: 51820
- Protocol: UDP ⚠️ (not TCP!)

---

## Create Client

```bash
# Generate client profile
pivpn add

# Display QR code
pivpn -qr [client-name]
```

---

## Connect Phone

1. Install WireGuard app
2. Scan QR code from `pivpn -qr` command
3. Enable tunnel
4. Turn off WiFi (test on mobile data)
5. Visit http://pi.hole/admin to verify

---

## Useful Commands

```bash
# List all clients
pivpn -l

# Remove client
pivpn -r [client-name]

# Show QR code again
pivpn -qr [client-name]

# Check WireGuard status
sudo wg show

# View logs
journalctl -u wg-quick@wg0 -f
```

---

## Troubleshooting

**Can't connect:**
- Verify port 51820 is open (UDP)
- Check router firewall
- Confirm Pi has static IP

**Connected but no internet:**
- Verify IP forwarding: `sudo sysctl net.ipv4.ip_forward` (should be 1)

**DNS not working:**
- Check WireGuard config DNS setting
- Should point to Pi's VPN IP (usually 10.6.0.1)

---

## Security Notes

✅ Port 51820 exposed to internet (WireGuard is secure by design)
✅ Revoke old clients: `pivpn -r [name]`
✅ Enable kill switch in WireGuard app
✅ Use dynamic DNS if home IP changes

---

## Result

✨ Pi-hole blocks ads/trackers on all devices, anywhere
✨ Encrypted tunnel back home
✨ Full network access remotely
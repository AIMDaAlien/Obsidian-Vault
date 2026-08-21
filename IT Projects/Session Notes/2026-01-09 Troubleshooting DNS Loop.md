---
tags: [guide, session-log, troubleshooting]
---
# Troubleshooting Report: The "DNS Loop" & Pi-hole Integration
**Tags:** #Networking #Homelab #Troubleshooting #PiHole #TPLink #DNS
**Date:** 2026-01-09

## 1. The Scenario: The "Orange Light" of Death
**Problem:**
After changing the router's **WAN (Internet) DNS** settings to point to a local Pi-hole instance, the router lost internet connectivity (indicated by a solid Orange LED on the Internet status).

**Symptoms:**
* **No Internet:** All devices disconnected.
* **Router Inaccessible:** The Tether app and `tplinkwifi.net` domain failed to resolve.
* **Services Disabled:** The router's firmware panicked, disabling the 2.4 GHz and 5 GHz WiFi radios.
* **Loop Condition:** The router was trying to resolve "where is the internet?" by asking a device *inside* the local network, but it couldn't reach the local device because the routing logic failed.

---

## 2. Emergency Recovery (Regaining Access)
When WiFi fails and the router is stuck in a logic loop, "surgical" entry is required.

### Step 1: Hardwire Connection
* **Action:** Connect a PC/Laptop directly to the router's LAN port via Ethernet.
* **Note:** Windows devices generally handle "dirty" connections (no internet/bad DHCP) better than macOS, which may self-assign a useless `169.254.x.x` address.

### Step 2: Access via IP (Not Domain)
* **Action:** Navigate to the router's Gateway IP (usually `192.168.0.1` or `192.168.1.1`) in a browser.
* **Avoid:** Do not use friendly domains like `tplinkwifi.net` as they rely on the broken DNS system.

### Step 3: The "Green Light" Fix
* **Action:** Navigate to **Network > Internet** (WAN Settings).
* **Fix:** Change specific DNS settings from the local Pi-hole IP back to a public provider (e.g., Quad 9 `9.9.9.9` or Cloudflare `1.1.1.1`).
* **Result:** This restores the router's ability to "see" the outside world, turning the Internet LED green.

---

## 3. The Correct Architecture: Split DNS
To block ads without breaking the router, we must separate the **Control Plane** (Router) from the **Data Plane** (User Devices).

### The Topology
1.  **Router (WAN):** Uses Public DNS (Quad 9/Cloudflare). This ensures the router can always update firmware and check connectivity.
2.  **Clients (DHCP):** Are instructed to use the Pi-hole.
3.  **Pi-hole (Upstream):** Forwards valid requests to Public DNS.

### Configuration Checklist
**A. Router DHCP Settings**
* **Primary DNS:** Set to `<Pi-hole_IP_Address>`.
* **Secondary DNS:** **CRITICAL** - Set this to `<Pi-hole_IP_Address>` as well.
    * *Why?* If left blank, many routers (like TP-Link) will auto-fill their own IP as a backup. This allows devices to bypass the ad blocker whenever they feel "impatient."
* **Address Reservation:** Manually add the Pi-hole's MAC address to ensure it always keeps the same IP.

**B. Pi-hole Settings**
* **Upstream DNS:** Check Cloudflare or Quad 9 (Do not check your ISP).
* **DHCP:** Disabled (since the Router is handling DHCP).

---

## 4. Client-Side Leaks (The "Hidden" Bypasses)
Even with the router configured correctly, clients may ignore the Pi-hole due to privacy features or caching.

### Diagnostics
* **Terminal Command (macOS):** `scutil --dns | grep "nameserver"`
    * *Checks who the OS is configured to ask.*
* **Lookup Command:** `nslookup doubleclick.net`
    * *Checks who actually answers.*
    * *Goal:* Server should be `<Pi-hole_IP>`, Address should be `0.0.0.0` (Blocked).
    * *Fail:* If Address returns a real IP (e.g., `142.250.x.x`), the ad is being allowed.

### Common Culprits & Fixes
1.  **The "Router Betrayal":**
    * *Issue:* Router injecting itself as Secondary DNS.
    * *Fix:* Hardcode Pi-hole IP into *both* Primary and Secondary DNS slots in the router.

2.  **Browser "Secure DNS" (DoH):**
    * *Issue:* Chrome/Brave/Firefox attempting to use "DNS over HTTPS" to bypass local settings.
    * *Fix:* Go to Browser Settings > Privacy & Security > **Turn OFF "Use Secure DNS"**.

3.  **Apple Privacy Features:**
    * *Issue:* macOS/iOS routing traffic through Apple relays.
    * *Fix:*
        * Disable **iCloud Private Relay**.
        * Disable **"Limit IP Address Tracking"** in WiFi Network Details.

4.  **Stale Cache:**
    * *Issue:* Device remembers the ad server's IP from before the fix.
    * *Fix:*
        * **Windows:** `ipconfig /flushdns` then `ipconfig /release` & `renew`.
        * **macOS:** `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`.
        * **Mobile:** Toggle WiFi Off/On.

---

## 5. Verification
To confirm the system is bulletproof:
1.  **DNS Leak Test:** Visit `dnsleaktest.com`.
    * *Success:* Result shows the Upstream Provider (e.g., WoodyNet/Quad 9) ONLY.
    * *Fail:* Result shows your ISP or multiple mixed servers.
2.  **Ad-Block Test:** Attempt to visit `doubleclick.net`.
    * *Success:* "This site can't be reached" (ERR_NAME_NOT_RESOLVED).
    * *Fail:* Redirects to a Google marketing page.
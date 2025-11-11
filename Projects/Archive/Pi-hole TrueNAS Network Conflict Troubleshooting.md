# Pi-hole Stopped Working After TrueNAS Setup

> **Problem**: Pi-hole was working perfectly until TrueNAS server was added to the network. After that, devices stopped getting DNS filtering and ads/trackers were no longer blocked.
> 
> **Root Cause**: Network configuration conflicts between Pi-hole and TrueNAS causing DHCP clients to bypass Pi-hole DNS
> 
> **Status**: RESOLVED
> **Date**: October 2025

---

## The Problem

### Symptoms
- Pi-hole dashboard showed no client queries (only the Pi itself)
- Ads and trackers were not being blocked on network devices
- Windows devices showed router IP (192.168.0.1) as DNS server instead of Pi-hole (192.168.0.117)
- `ipconfig /release` and `ipconfig /renew` didn't fix the issue
- Router DHCP settings appeared correct but weren't being applied to clients

### Network Setup
- **Pi-hole**: Raspberry Pi at 192.168.0.117
- **TrueNAS**: Dedicated server at 192.168.0.120
- **Router**: TP-Link (192.168.0.1)
- **Upstream DNS**: Unbound running on Pi-hole (127.0.0.1:5335)

---

## Root Causes Identified

### 1. TrueNAS Gateway Misconfiguration (PRIMARY ISSUE)
**What was wrong**: TrueNAS had Pi-hole IP (192.168.0.117) set as the Default Gateway instead of the router (192.168.0.1)

**Why this broke things**: 
- Gateway = where network traffic routes
- DNS = where name lookups go
- Having Pi-hole as gateway caused routing confusion
- TrueNAS couldn't properly communicate with the network

**Location**: TrueNAS Web UI → Network → Global Configuration → IPv4 Default Gateway

### 2. Router DHCP Settings Not Saved/Applied
**What was wrong**: Primary DNS field in router DHCP settings was empty or not properly saved

**Why this broke things**:
- Router was handing out itself (192.168.0.1) as DNS to DHCP clients
- Devices were bypassing Pi-hole entirely
- Router then forwarded queries to ISP DNS or other upstream servers

**Location**: TP-Link Router → Advanced → Network → DHCP Server → Primary DNS

### 3. Stale DHCP Leases
**What was wrong**: Even after fixing router settings, devices retained old DHCP leases with wrong DNS

**Why this broke things**:
- DHCP lease time was 120 minutes
- Devices won't get new settings until lease expires
- Simple `ipconfig /renew` sometimes doesn't force new lease from router

---

## Diagnostic Steps

### Step 1: Verify Pi-hole is Actually Running
```bash
# SSH into Pi-hole
sudo systemctl status pihole-FTL

# Check if Pi-hole web interface loads
http://192.168.0.117/admin
```

**Expected**: Service active, web interface accessible

### Step 2: Check What DNS Clients Are Actually Using
```cmd
# Windows Command Prompt
ipconfig /all | findstr DNS

# Mac/Linux Terminal  
cat /etc/resolv.conf
```

**Expected**: Should show 192.168.0.117 (Pi-hole)
**Problem if**: Shows 192.168.0.1 (router) or 1.1.1.1, 8.8.8.8 (public DNS)

### Step 3: Test Pi-hole Blocking Directly
```cmd
# Force query through Pi-hole
nslookup doubleclick.net 192.168.0.117
```

**Expected**: Should return 0.0.0.0 or no answer (blocked)
**Problem if**: Returns real IP address (not blocking)

### Step 4: Check Pi-hole Query Log
- Go to Pi-hole admin panel
- Check if ANY queries are showing up
- If only seeing queries from 192.168.0.117 (the Pi itself) = clients aren't using it

### Step 5: Verify Router DHCP Configuration
```
Router → Advanced → Network → DHCP Server

Check:
- Primary DNS: 192.168.0.117 ✓
- Secondary DNS: BLANK or also 192.168.0.117 ✓
```

**Important**: If Secondary DNS is set to 1.1.1.1, 8.8.8.8, or any other public DNS, devices will use it as a fallback and bypass Pi-hole intermittently!

### Step 6: Check TrueNAS Network Settings
```
TrueNAS Web UI → Network → Global Configuration

Check:
- Nameserver 1: 192.168.0.117 (Pi-hole) ✓
- Nameserver 2: BLANK ✓  
- IPv4 Default Gateway: 192.168.0.1 (ROUTER, not Pi-hole!) ✓
```

### Step 7: Look for Rogue DHCP Servers
Check if TrueNAS or any other device is running DHCP:
```
TrueNAS → System Settings → Services
Look for: DHCP or ISC DHCP service
Status: Should be DISABLED
```

**Why this matters**: Multiple DHCP servers cause chaos - devices randomly get leases from either one with different DNS settings.

---

## Solutions Applied

### Fix #1: Correct TrueNAS Gateway Setting
**Location**: TrueNAS Web UI → Network → Global Configuration

**Change**:
```
BEFORE:
IPv4 Default Gateway: 192.168.0.117 (WRONG - this is Pi-hole!)

AFTER:  
IPv4 Default Gateway: 192.168.0.1 (CORRECT - this is the router)
```

**Verification**: TrueNAS should now be able to route traffic properly and use Pi-hole for DNS without routing confusion.

### Fix #2: Set Router Primary DNS
**Location**: TP-Link Router → Advanced → Network → DHCP Server

**Settings**:
```
Primary DNS: 192.168.0.117 (Pi-hole)
Secondary DNS: BLANK (or also 192.168.0.117)
```

**Critical**: Leave Secondary DNS blank! Having a fallback DNS defeats the purpose of Pi-hole.

**Action**: Save settings, then **REBOOT THE ROUTER**

**Why reboot**: TP-Link routers often don't apply DHCP changes until rebooted.

### Fix #3: Force DHCP Renewal on All Devices
After router reboot and settings confirmed, force all devices to get fresh DHCP leases:

**Windows**:
```cmd
ipconfig /release
ipconfig /renew
ipconfig /all
```

**Mac**:
```
System Preferences → Network → Advanced → Renew DHCP Lease
```

**Android/iOS**:
- Toggle WiFi off/on
- OR "Forget Network" and reconnect
- OR reboot device

**Smart TVs/IoT Devices**:
- Reboot them (unplug/replug power)

### Fix #4: Disable Any Rogue DHCP Services
If TrueNAS had DHCP enabled:
```
System Settings → Services → DHCP → Disable
```

---

## Verification Steps

### Test 1: Check DNS Assignment
```cmd
ipconfig /all
```

Look for:
```
DNS Servers . . . . . . . . . . . : 192.168.0.117
```

✓ **SUCCESS**: Shows Pi-hole
✗ **FAIL**: Shows 192.168.0.1 or anything else - repeat Fix #3

### Test 2: Verify Pi-hole is Being Used
```cmd
nslookup google.com
```

Should show:
```
Server:  pi.hole (or Unknown)
Address:  192.168.0.117
```

### Test 3: Confirm Blocking Works
```cmd
nslookup doubleclick.net
```

Should return:
- `0.0.0.0` 
- OR "server can't find doubleclick.net"
- OR no answer

If it returns a real IP address = not blocking!

### Test 4: Check Pi-hole Dashboard
Go to: `http://192.168.0.117/admin`

Should now see:
- Multiple clients listed (not just localhost)
- Queries coming in from various devices
- Percentage of queries blocked increasing

---

## Prevention Tips

### Network Documentation
Keep a network map with:
- Device name, IP, MAC address
- What services each device runs
- DNS settings for each device
- Gateway configuration

### Static IPs for Infrastructure
Set static IPs for critical infrastructure:
- Pi-hole: 192.168.0.117
- TrueNAS: 192.168.0.120  
- Router: 192.168.0.1

This prevents DHCP conflicts and makes troubleshooting easier.

### DHCP Configuration Template
When configuring router DHCP:
```
Primary DNS: [Pi-hole IP]
Secondary DNS: BLANK (no fallback!)
Gateway: [Router IP]
Lease Time: 120 minutes (or longer for stability)
```

### Gateway vs DNS Checklist
For any server/device configuration:
- **Gateway** = Router IP (where traffic routes)
- **DNS** = Pi-hole IP (where name lookups go)
- **Never** set Pi-hole as the gateway!

### Testing After Changes
Always test after network changes:
1. `ipconfig /all` - verify DNS assignment
2. `nslookup google.com` - verify Pi-hole is being used
3. `nslookup doubleclick.net` - verify blocking works
4. Check Pi-hole dashboard for client activity

### Router Settings Backup
After confirming working configuration:
- Export/backup router settings
- Document exact values used
- Take screenshots of critical settings pages

---

## Common Mistakes to Avoid

### Don't Use Pi-hole as Gateway
**Wrong**:
```
Gateway: 192.168.0.117 (Pi-hole)
```

**Correct**:
```  
Gateway: 192.168.0.1 (Router)
DNS: 192.168.0.117 (Pi-hole)
```

**Why**: Pi-hole is a DNS filter, not a router. It can't route packets between networks.

### Don't Set Fallback DNS
**Wrong**:
```
Primary DNS: 192.168.0.117
Secondary DNS: 1.1.1.1
```

**Correct**:
```
Primary DNS: 192.168.0.117  
Secondary DNS: BLANK
```

**Why**: Devices will use secondary DNS when primary is "slow" (even if it's working fine), bypassing Pi-hole filtering.

### Don't Trust "ipconfig /renew" Alone
Sometimes Windows caches DNS aggressively:
```cmd
# Do all of these:
ipconfig /flushdns
ipconfig /release  
ipconfig /renew
```

Or just reboot the device (most reliable).

### Don't Run Multiple DHCP Servers
Only ONE device should handle DHCP:
- Usually: Your router
- NOT: TrueNAS, Pi-hole, or other servers

Check all servers to ensure DHCP services are disabled.

---

## Troubleshooting Commands Reference

### Windows DNS Diagnostics
```cmd
# Show current DNS settings
ipconfig /all

# Flush DNS cache
ipconfig /flushdns

# Release and renew DHCP lease
ipconfig /release
ipconfig /renew

# Test DNS resolution
nslookup google.com
nslookup doubleclick.net

# Force query through specific DNS
nslookup google.com 192.168.0.117
```

### Pi-hole Commands
```bash
# Check Pi-hole status
pihole status

# Restart Pi-hole
pihole restartdns

# Update blocklists
pihole -g

# Check if blocking is enabled
pihole status

# Tail query log in real-time
pihole -t
```

### TrueNAS CLI (if needed)
```bash
# Access shell from web UI: System → Shell

# Show network configuration
ifconfig

# Test DNS resolution
nslookup google.com

# Ping test
ping 192.168.0.117
ping 192.168.0.1
```

---

## Related Issues

### If Pi-hole Shows "Not Blocking"
1. Check if Pi-hole-FTL service is running
2. Verify blocklists are installed: `pihole -g`
3. Check if blocking is disabled: `pihole status`
4. Review whitelist for overly broad entries

### If Unbound Stops Working
1. Test Unbound directly: `dig google.com @127.0.0.1 -p 5335`
2. Check Unbound status: `sudo service unbound status`
3. Verify configuration: `/etc/unbound/unbound.conf.d/pi-hole.conf`
4. Restart: `sudo service unbound restart`

### If Network Performance Degrades
1. Check Pi-hole is responsive (not overloaded)
2. Verify Unbound isn't causing delays
3. Temporarily set router DNS to 1.1.1.1 to isolate issue
4. Check Pi-hole logs for errors: `pihole -t`

---

## Key Learnings

1. **Gateway and DNS are different things** - Don't confuse them in network configuration
2. **Secondary DNS bypasses filtering** - Leave it blank or set to same as primary
3. **Router settings need reboot** - DHCP changes often require router restart
4. **DHCP leases are sticky** - Devices keep old settings until lease expires
5. **One DHCP server per network** - Multiple DHCP servers = chaos
6. **Test in layers** - Verify each component works before moving to next
7. **Document working configs** - Future you will thank present you

---

## Resources

- **Pi-hole Documentation**: https://docs.pi-hole.net
- **TrueNAS SCALE Docs**: https://www.truenas.com/docs/scale/
- **Network Troubleshooting Tools**: 
  - `nslookup` - DNS query testing
  - `ping` - Network connectivity  
  - `ipconfig` - Network configuration (Windows)
  - `dig` - Advanced DNS queries (Linux)

---

## Related Documentation

- [[TrueNAS Build Guide]] - Complete NAS hardware and software setup
- [[Budget SAS Drive NAS Build Guide]] - Detailed build documentation with troubleshooting
- Raspberry Pi Network Privacy Setup - Original Pi-hole installation guide

---

*Document created: October 2025*  
*Last incident: Successfully resolved*  
*Prevention: Network configuration checklist implemented*

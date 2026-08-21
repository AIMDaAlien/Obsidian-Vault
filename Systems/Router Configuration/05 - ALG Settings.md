---
tags: [guide, hardening]
garden_path: Router Configuration/05 - ALG Settings.md
last_published: '2025-11-30T20:05:32.548512'
published_to_garden: true
---

# ALG Settings (Application Layer Gateway)

Understanding and optimizing ALG settings for better performance and security.

---

## What is ALG?

**Application Layer Gateway (ALG)** acts as a protocol translator helping certain applications work through NAT (Network Address Translation).

**The Analogy:** Your router is like an office building with a security desk. ALGs are specialized translators at that desk who understand specific "languages" (protocols) that some applications speak.

**Modern Reality:** Most ALGs were designed for the early days of NAT when applications couldn't handle address translation well. Today's applications are much smarter about NAT traversal, making most ALGs unnecessary and potentially harmful.

---

## The ALG Problem

**Why ALGs often cause more harm than good:**
- Poorly implemented in most consumer routers
- Break modern applications that handle NAT themselves
- Add security vulnerabilities
- Create performance overhead
- Interfere with encrypted protocols

**Key Principle:** Modern applications handle NAT better than router ALGs. When in doubt, disable it.

---

## Quick Reference Guide

| Protocol | Recommendation | Reason |
|----------|---------------|--------|
| **PPTP Passthrough** | ❌ DISABLE | Fundamentally insecure, obsolete |
| **L2TP Passthrough** | ⚠️ DISABLE (unless corporate VPN) | Outdated, rarely needed |
| **IPSec Passthrough** | ✅ KEEP ENABLED | Modern, secure, widely used |
| **FTP ALG** | ❌ DISABLE | Breaks more than it fixes |
| **TFTP ALG** | ❌ DISABLE | Rarely needed, security risk |
| **RTSP ALG** | ⚠️ ENABLE (if IP cameras) | Essential for security cameras |
| **H323 ALG** | ❌ DISABLE | Obsolete videoconferencing |
| **SIP ALG** | ❌ DISABLE IMMEDIATELY | Notorious for breaking VoIP |

---

## Detailed Analysis

### PPTP Passthrough

**Status:** ❌ DISABLE IMMEDIATELY

**What it does:** Allows ancient PPTP VPN protocol to pass through router.

**The Problem:**
- Fundamentally broken encryption (crackable in hours)
- Security researchers universally condemn it
- No legitimate reason to use it in 2025
- Better alternatives exist (OpenVPN, WireGuard)

**Security Risk:** 🔴 **CRITICAL**
**Performance Impact:** Negligible when disabled

**Use Case:** Legacy corporate systems from early 2000s (extremely rare)

**Configuration:**
```
PPTP Passthrough: DISABLED
Location: Advanced → Security → ALG Settings
```

---

### L2TP Passthrough

**Status:** ⚠️ SITUATIONAL (Disable unless needed)

**What it does:** Allows L2TP/IPSec VPN connections through router.

**Pros:**
- More secure than PPTP (when used with IPSec)
- Some corporate VPNs still use it
- Industry standard (historically)

**Cons:**
- Higher overhead than modern protocols
- Outdated compared to WireGuard/OpenVPN
- Complex configuration

**Keep Enabled If:**
- Work requires L2TP/IPSec VPN
- Corporate policy mandates it

**Otherwise:** Disable for reduced attack surface

**Security Risk:** 🟡 **MODERATE** (when properly configured)

**Configuration:**
```
L2TP Passthrough: DISABLED (unless corporate VPN needed)
Location: Advanced → Security → ALG Settings
```

---

### IPSec Passthrough

**Status:** ✅ KEEP ENABLED

**What it does:** Allows modern IPSec VPN protocol through router.

**Why Keep It:**
- Industry-standard security protocol
- Used by many legitimate VPN services
- Strong encryption
- Enterprise-grade
- Minimal security risk
- Low performance overhead

**Cons:**
- Slight processing overhead (negligible)
- Can interfere with some applications (rare)

**Security Risk:** 🟢 **LOW**
**Performance Impact:** Minimal

**Used By:**
- Modern VPN clients (NordVPN, ExpressVPN, etc.)
- Corporate networks
- Secure site-to-site connections

**Configuration:**
```
IPSec Passthrough: ENABLED
Location: Advanced → Security → ALG Settings
```

---

### FTP ALG

**Status:** ❌ DISABLE

**What it does:** Attempts to help File Transfer Protocol work through NAT.

**The Notorious Problem:**
- **Breaks modern FTP clients** more often than it helps
- Interferes with FTPS (FTP over SSL)
- Interferes with SFTP (SSH File Transfer)
- Causes connection timeouts and failures
- Creates security vulnerabilities

**Modern Reality:**
Every modern FTP client handles NAT perfectly fine without ALG help.

**Security Risk:** 🟡 **MODERATE**
**Reliability Impact:** 🔴 **HIGH** (often breaks connections)

**Keep Enabled Only If:**
Using ancient FTP software from the 1990s (you're not)

**Configuration:**
```
FTP ALG: DISABLED
Location: Advanced → Security → ALG Settings
```

> [!warning] VoIP Expert Consensus
> If you're having FTP connection issues, the FIRST thing to try is disabling FTP ALG.

---

### TFTP ALG

**Status:** ❌ DISABLE

**What it does:** Allows Trivial File Transfer Protocol through router.

**What is TFTP:**
- Extremely basic, unencrypted file transfer
- Used for network equipment firmware updates
- PXE booting diskless workstations
- Almost never used by home users

**Security Risk:** 🟡 **MODERATE** (unencrypted protocol)
**Home User Relevance:** 🟢 **VERY LOW**

**Keep Enabled Only If:**
- You're a network administrator
- Managing network equipment
- Running PXE boot servers

**Otherwise:** Disable to reduce attack surface

**Configuration:**
```
TFTP ALG: DISABLED
Location: Advanced → Security → ALG Settings
```

---

### RTSP ALG

**Status:** ⚠️ SITUATIONAL

**What it does:** Helps Real-Time Streaming Protocol work through NAT.

**Used By:**
- IP security cameras
- DVR/NVR systems
- Some streaming media servers
- Older media players

**Enable If:**
- ✅ You have IP security cameras
- ✅ Using DVR/NVR systems
- ✅ Running RTSP media servers

**Disable If:**
- ❌ No security cameras
- ❌ Using modern streaming services (they don't use RTSP)
- ❌ Experiencing streaming issues (try disabling to test)

**Security Risk:** 🟡 **MODERATE**
**Performance Impact:** Low

**Configuration:**
```
RTSP ALG: ENABLED (if IP cameras) / DISABLED (otherwise)
Location: Advanced → Security → ALG Settings
```

> [!tip] 3D Printer Camera Use Case
> If you're setting up a cheap network camera to monitor your 3D printer, KEEP RTSP ALG ENABLED. These cameras typically use RTSP streaming.

---

### H323 ALG

**Status:** ❌ DISABLE

**What it does:** Supports H.323 video conferencing protocol from the 1990s.

**Why It's Obsolete:**
- Ancient video conferencing standard
- Modern services (Zoom, Teams, Meet) use completely different protocols
- Security vulnerabilities
- Complex and problematic implementation

**Modern Services DON'T Use H.323:**
- Zoom → Proprietary protocol
- Microsoft Teams → WebRTC
- Google Meet → WebRTC
- FaceTime → Proprietary protocol

**Security Risk:** 🔴 **HIGH** (obsolete protocol)
**Relevance:** 🟢 **NONE** (for modern users)

**Keep Enabled Only If:**
Using ancient corporate video conferencing from early 2000s (extremely unlikely)

**Configuration:**
```
H323 ALG: DISABLED
Location: Advanced → Security → ALG Settings
```

---

### SIP ALG

**Status:** ❌ DISABLE IMMEDIATELY (Most Important!)

**What it does:** Attempts to help Session Initiation Protocol (VoIP) work through NAT.

**The Infamous Problem:**

This is the **most notorious** ALG setting. It's so poorly implemented in consumer routers that it breaks more VoIP systems than it fixes.

**Common Issues Caused by SIP ALG:**
- One-way audio (you can't hear caller, or they can't hear you)
- Registration failures with VoIP providers
- Call drops and disconnections
- Audio quality problems
- Phones failing to register

**Expert Consensus:**
**EVERY** VoIP expert and provider recommends disabling SIP ALG. It's universally recognized as problematic.

**Why Modern VoIP Doesn't Need It:**
- Modern VoIP equipment has built-in NAT traversal (STUN, TURN, ICE)
- Equipment handles NAT better than router ALGs
- SIP ALG implementations are poorly tested

**Security Risk:** 🟡 **MODERATE**
**VoIP Reliability Impact:** 🔴 **CRITICAL**

**Configuration:**
```
SIP ALG: DISABLED
Location: Advanced → Security → ALG Settings
```

> [!danger] Critical for VoIP Users
> If you use ANY VoIP service (business phones, softphones, SIP calling), disable SIP ALG IMMEDIATELY. This is the #1 cause of mysterious VoIP issues.

---

## Recommended Configuration

### For Most Home Users:

```
✅ IPSec Passthrough: ENABLED
❌ PPTP Passthrough: DISABLED
❌ L2TP Passthrough: DISABLED
❌ FTP ALG: DISABLED
❌ TFTP ALG: DISABLED
❌ RTSP ALG: DISABLED
❌ H323 ALG: DISABLED
❌ SIP ALG: DISABLED
```

### With IP Security Cameras:

```
✅ IPSec Passthrough: ENABLED
⚠️ RTSP ALG: ENABLED (for cameras)
❌ Everything else: DISABLED
```

### With Corporate VPN:

```
✅ IPSec Passthrough: ENABLED
⚠️ L2TP Passthrough: ENABLED (if required)
❌ Everything else: DISABLED
```

---

## Performance Impact

**Each Enabled ALG:**
- Adds CPU processing overhead
- Creates inspection/modification latency
- Increases memory usage
- Potential packet corruption risk

**When Disabled:**
- Lower CPU usage = better overall performance
- Reduced latency
- More reliable connections
- Fewer mysterious networking problems

**The Less is More Principle:**
Disable everything you don't actively need. Your network will be faster, more secure, and more reliable.

---

## Privacy & Security Implications

**ALG Privacy Concerns:**

Each enabled ALG can:
- Inspect your network traffic
- Potentially log connection data
- Create attack vectors
- Leak information about network usage patterns

**Security Best Practices:**
1. Disable all ALGs you don't actively use
2. Minimal ALGs = minimal attack surface
3. Modern apps handle NAT better than ALGs
4. Trust your applications over router features

---

## Troubleshooting

**Application Not Working:**
1. Try disabling relevant ALG
2. Modern apps often work BETTER with ALGs disabled
3. Test with all ALGs disabled temporarily

**VoIP Issues:**
1. Disable SIP ALG immediately (99% of VoIP problems)
2. Check provider's NAT traversal settings
3. Ensure provider supports STUN/TURN

**FTP Connection Problems:**
1. Disable FTP ALG
2. Use passive mode in FTP client
3. Consider SFTP or FTPS instead

**Streaming Camera Issues:**
1. Enable RTSP ALG for cameras
2. Check camera's streaming settings
3. Verify port forwarding rules

---

## Related Topics
- [[08 - Privacy & Security Hardening]] - Complete security guide
- [[01 - Network Connection Settings]] - NAT configuration
- [[06 - VPN Configuration]] - VPN setup without ALG issues

---

#alg #security #voip #networking #protocols
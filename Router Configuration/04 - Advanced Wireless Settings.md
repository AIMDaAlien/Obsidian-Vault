# Advanced Wireless Settings

Fine-tune your WiFi for optimal performance, compatibility, and device management.

---

## Quick Reference Table

| Setting | Default | Recommended | Impact |
|---------|---------|-------------|--------|
| WMM | Enabled | **Keep Enabled** | High performance boost |
| AP Isolation | Disabled | **Keep Disabled** (main network) | Device communication |
| Airtime Fairness | Disabled | **Enable** | 30-50% performance boost |
| Beacon Interval | 100ms | **Keep 100ms** | Standard optimal |
| RTS Threshold | 2346 | **Keep 2346** | Low overhead |
| DTIM Interval | 1 | **Keep 1** (or 3 for battery) | Responsiveness |
| Group Key Update | 0 (disabled) | **3600** (1 hour) | Security enhancement |

---

## WMM (Wi-Fi Multimedia)

**What it does:** Prioritizes time-sensitive traffic (video calls, gaming, streaming) over less urgent data (downloads, email).

### Status: ✅ KEEP ENABLED

**How it works:**
- Creates VIP lanes for important traffic
- Four priority queues: Voice, Video, Best Effort, Background
- Uses EDCA (Enhanced Distributed Channel Access)

**Pros:**
- Reduces latency for gaming by up to 50% in congested networks
- Smoother video calls and streaming
- Required for modern WiFi standards (802.11n+)
- No downsides

**Cons:**
- None (essential feature)

**Configuration:**
```
WMM: ENABLED
Location: Wireless → Professional → WMM
```

> [!info] Technical Note
> WMM is mandatory for 802.11n and newer. Disabling it forces legacy mode, dramatically reducing speeds.

---

## AP Isolation

**What it does:** Prevents wireless devices from communicating with each other. Only router can talk to devices.

### Main Network: ❌ KEEP DISABLED
### Guest Network: ✅ ENABLE

**How it works:**
Blocks peer-to-peer communication at layer 2, creating walls between connected devices.

**When Disabled (Main Network):**
- Devices can share files
- Printers work properly
- Chromecast/AirPlay function
- Smart home devices communicate

**When Enabled (Guest Network):**
- Prevents guest devices from accessing your main network
- Protects against infected devices spreading malware
- Isolates untrusted visitors

**Configuration:**
```
Main Network: AP Isolation DISABLED
Guest Network: AP Isolation ENABLED
Location: Wireless → Wireless Settings → AP Isolation
```

---

## Airtime Fairness

**What it does:** Prevents slow devices from monopolizing WiFi airtime, ensuring fast devices maintain their speed.

### Status: ⭐ ENABLE (Significant Performance Boost)

**The Problem:**
Without airtime fairness, a single old 802.11g device can slow down your entire network. Slow devices take much longer to transmit the same amount of data, hogging the channel.

**The Solution:**
Allocates time slots fairly, so one slow device can't degrade performance for everyone else.

**Performance Impact:**
- **30-50% throughput increase** when mixing old and new devices
- Fast devices maintain their speed
- Overall network efficiency improves

**Potential Issues:**
- Very old devices (pre-2010) may experience poor performance
- May cause connection drops on ancient hardware

**Configuration:**
```
Airtime Fairness: ENABLED
Location: Wireless → Professional → Airtime Fairness
```

> [!tip] Recommendation
> Enable unless you have devices older than 2010. Modern networks benefit significantly.

---

## Beacon Interval

**What it does:** Router broadcasts "I'm here!" signals at this interval, helping devices find and sync with the network.

### Status: ✅ KEEP 100ms (Perfect Standard)

**Beacon Functions:**
- Network discovery for new devices
- Time synchronization for connected devices
- SSID advertisement

**Value Options:**

| Interval | Discovery Speed | Bandwidth Overhead | Use Case |
|----------|----------------|-------------------|----------|
| 50ms | Fast | Higher | High mobility, many clients |
| **100ms** ⭐ | **Optimal** | **Balanced** | **Standard (recommended)** |
| 300ms+ | Slower | Lower | IoT devices, power saving |

**Configuration:**
```
Beacon Interval: 100ms
Location: Wireless → Professional → Beacon Interval
```

---

## RTS Threshold

**What it does:** For packets larger than this threshold, devices "ask permission" before transmitting to avoid collisions.

### Status: ✅ KEEP 2346 bytes (Effectively Disabled)

**How it works:**
RTS/CTS (Request to Send/Clear to Send) is like raising your hand before speaking in class.

**High Value (2346) - Recommended:**
- Minimal overhead
- Better performance in most home environments
- Less protocol chatter

**Lower Values (512-1024):**
- Reduces collisions in very dense networks (20+ active devices)
- Higher overhead on every transmission
- Only beneficial in crowded apartment buildings

**Configuration:**
```
RTS Threshold: 2346 bytes
Location: Wireless → Professional → RTS Threshold
```

> [!warning] Only Lower If...
> You're in an extremely dense WiFi environment (apartment complex) AND experiencing frequent disconnections. Otherwise, keep high.

---

## DTIM Interval

**What it does:** Tells sleeping devices when to wake up and check for buffered data.

### Status: ✅ KEEP 1 (Performance) or 3 (Battery Balance)

**How it works:**
Delivery Traffic Indication Message acts as a gentle alarm clock for devices' WiFi chips.

**Value Options:**

| DTIM | Wake Frequency | Responsiveness | Battery Impact |
|------|---------------|----------------|----------------|
| **1** | Every beacon (100ms) | Excellent | Higher drain ⭐ |
| **3** | Every 300ms | Very Good | Balanced |
| 10+ | Every 1000ms+ | Delayed | Maximum saving |

**Best For:**
- **DTIM = 1:** Gaming, VoIP, real-time applications
- **DTIM = 3:** Balanced for most users
- **DTIM = 10:** IoT devices, battery-critical scenarios

**Configuration:**
```
DTIM Interval: 1 (performance) or 3 (balanced)
Location: Wireless → Professional → DTIM Period
```

---

## Group Key Update Period

**What it does:** Controls how often encryption keys change for broadcast/multicast traffic (streaming, file sharing).

### Status: ⚠️ ENABLE - Set to 3600 (1 hour)

**Current Issue:**
Value of 0 means keys **never change** automatically. If someone captures your group key, they can decrypt broadcast traffic indefinitely.

**Security Levels:**

| Value | Security | Interruption | Recommended |
|-------|----------|-------------|-------------|
| 0 | Low | None | ❌ Not recommended |
| **3600** (1 hour) | Good | Brief, imperceptible | ✅ Balanced |
| 86400 (24 hours) | Moderate | Rare | Acceptable |

**Configuration:**
```
Group Key Update Period: 3600 seconds (1 hour)
Location: Wireless → Professional → Group Key Update Period
```

> [!tip] Privacy Enhancement
> Enabling key rotation significantly improves security for long-term monitoring protection with minimal user impact.

---

## Advanced Features (WiFi 6/6E)

If your router supports WiFi 6 or 6E, enable these for maximum performance:

### MU-MIMO (Multi-User MIMO)
**Status:** ✅ ENABLE
- Simultaneous communication with multiple devices
- Dramatically improves multi-device performance

### Beamforming
**Status:** ✅ ENABLE
- Focuses WiFi signal toward specific devices
- Improves range and connection stability

### OFDMA
**Status:** ✅ ENABLE (WiFi 6 feature)
- More efficient use of channels
- Better performance in congested networks

### BSS Coloring
**Status:** ✅ ENABLE (WiFi 6 feature)
- Reduces interference from neighboring networks
- Allows more aggressive channel reuse

**Configuration:**
```
Location: Wireless → Professional → WiFi 6 Features
Enable all advanced features
```

---

## 802.11k/v/r (Fast Roaming)

**What it does:** Enables seamless transitions between access points in mesh or multi-AP setups.

**Status:** ✅ ENABLE (if you have multiple APs)

**Features:**
- **802.11k:** Neighbor reporting (helps devices find best AP)
- **802.11v:** BSS transition management (smooth handoffs)
- **802.11r:** Fast roaming (reduces reconnection time)

**Configuration:**
```
Location: Wireless → Professional → Fast Roaming
Enable 802.11k, 802.11v, 802.11r
```

---

## Channel Selection

**Critical for Performance:** Manual channel selection for 2.4GHz, Auto for 5GHz

### 2.4GHz: Manual (Channels 1, 6, or 11)
These are the only non-overlapping channels. Use a WiFi analyzer app to find the least congested.

### 5GHz: Auto
Let the router choose from the many available channels. Include DFS channels for more options.

**Configuration:**
```
2.4GHz Channel: 1, 6, or 11 (based on survey)
5GHz Channel: Auto (with DFS enabled)
Channel Width: 20MHz (2.4GHz), 80MHz (5GHz)
Location: Wireless → Wireless Settings → Channel
```

---

## Configuration Summary

### Immediate Actions:
1. ✅ Confirm WMM is ENABLED
2. ✅ ENABLE Airtime Fairness
3. ✅ Set Group Key Update to 3600
4. ✅ Enable all WiFi 6 features (if available)
5. ✅ Configure proper channel selection

### Keep Default:
- Beacon Interval: 100ms
- RTS Threshold: 2346
- DTIM Interval: 1 or 3

---

## Related Topics
- [[07 - Performance Optimization Checklist]] - Complete optimization guide
- [[01 - Network Connection Settings]] - Base network configuration

---

#wireless #wifi #performance #optimization

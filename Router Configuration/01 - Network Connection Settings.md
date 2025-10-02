# Network Connection Settings

Core network configuration settings that affect how your router communicates with your ISP and manages traffic.

---

## IPv6 Connection Types

### Quick Comparison

| Type | Performance | Complexity | Best For |
|------|------------|------------|----------|
| Dynamic IP (SLAAC/DHCPv6) | 95% | Low | Most users ⭐ |
| Static IP | 90% | Medium | Servers, consistent access |
| PPPoE | 85% | Medium | DSL/Fiber with ISP login |
| Pass-Through (Bridge) | 98% | High | Advanced users only |
| 6to4 Tunnel | 70% | High | IPv4-only ISPs (avoid) |

### Recommended: Dynamic IP (SLAAC/DHCPv6)

**What it does:** Automatically gets IP address from ISP. Router and ISP negotiate optimal settings.

**Pros:**
- Plug & play simplicity
- ISP-optimized performance
- Automatic updates
- Best compatibility

**Cons:**
- IP address changes periodically
- Less control over configuration
- Potential tracking via IP changes

**Configuration:** 
```
Internet Connection Type: Dynamic IP (SLAAC/DHCPv6)
Location: Advanced → Network → Internet
```

> [!tip] Privacy Enhancement
> Enable **IPv6 Privacy Extensions** to generate temporary addresses that rotate, making long-term tracking harder.

---

## NAT (Network Address Translation)

**What it does:** Translates private IP addresses (192.168.x.x) to your public IP when communicating with the internet.

### Recommendation: ENABLED

**Why keep it on:**
- Essential security layer
- Hides internal network structure
- Prevents direct external access to devices
- Minimal performance overhead on modern routers

**Configuration:**
```
NAT: ENABLED
Location: Advanced → NAT Settings
```

> [!warning] Only Disable If...
> You're using IPv6 exclusively or have very specific networking requirements. For most users, NAT should ALWAYS be enabled.

---

## Port Negotiation Speed

**What it does:** Determines how fast the router communicates with ISP equipment.

### Recommendation: Auto Negotiation

| Setting | Reliability | Speed Achievement |
|---------|-------------|-------------------|
| Auto Negotiation | 95% | Optimal |
| Manual Speed | 80% | Risk of mismatch |

**Why auto is better:**
- Automatically finds optimal speed
- Handles ISP equipment upgrades
- Prevents configuration errors
- No downside to using auto

**Configuration:**
```
Port Negotiation: Auto Negotiation
Location: Advanced → Network → Port Settings
```

---

## Flow Controller

**What it does:** Sends "PAUSE" signals when router is overwhelmed to temporarily stop incoming data.

### Recommendation: DISABLED (for most users)

**RX Enable:** Router can tell others to slow down
**TX Enable:** Router responds to others' slow-down requests

**Pros:**
- Prevents packet loss in extreme congestion
- Useful for very high-traffic scenarios

**Cons:**
- Introduces micro-delays
- Modern equipment handles traffic well without it
- Can interfere with gaming and VoIP
- Potential privacy leak (reveals network load patterns)

**When to enable:**
- Running servers with heavy traffic
- Experiencing consistent packet loss during high usage
- Network monitoring shows buffer overruns

**Configuration:**
```
Flow Control RX: DISABLED
Flow Control TX: DISABLED
Location: Advanced → Network → Flow Control
```

---

## Related Topics
- [[02 - DNS Configuration]] - Configure privacy-respecting DNS
- [[08 - Privacy & Security Hardening]] - Additional security measures

---

#networking #ipv6 #nat #configuration

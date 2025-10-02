# VPN Configuration

Understanding router-level VPN options and when to use them.

---

## VPN Passthrough vs VPN Client

**Critical Distinction:**

### VPN Passthrough (ALG Settings)
- Allows VPN traffic to pass *through* your router
- You run VPN software on individual devices
- Router just forwards the VPN traffic
- Covered in [[05 - ALG Settings]]

### VPN Client (This Document)
- Router *itself* becomes a VPN client
- Entire network connects through VPN
- All devices protected automatically
- Significant performance impact

---

## Router VPN Client Overview

**What it does:** Routes ALL network traffic through a VPN service before reaching the internet.

**The Analogy:** Instead of each person in your house using their own disguise, the whole house moves to a secret location, and everyone automatically benefits.

---

## VPN Protocol Comparison

| Protocol | Speed | Security | Compatibility | Recommendation |
|----------|-------|----------|---------------|----------------|
| **WireGuard** ⭐ | Excellent | Excellent | Modern routers | Best choice |
| **OpenVPN** | Good | Excellent | Universal | Most compatible |
| **IPSec/IKEv2** | Very Good | Excellent | Mixed | Enterprise use |
| **PPTP** | Good | 🔴 TERRIBLE | Legacy only | ❌ Never use |
| **L2TP/IPSec** | Moderate | Good | Older systems | Outdated |

---

## Protocol Details

### WireGuard (Recommended) ⭐

**Best for:** Modern VPN services, maximum performance

**What it is:**
- Next-generation VPN protocol
- Designed for speed and simplicity
- Minimal code = fewer security vulnerabilities
- Modern cryptography

**Pros:**
- **Fastest** VPN protocol available
- Lower battery consumption
- Simpler configuration
- Strong security
- Rapidly gaining support

**Cons:**
- Newer protocol (not universally supported yet)
- Some older routers don't support it
- Fewer provider options (growing rapidly)

**Performance:**
- Speed loss: 5-15% (best in class)
- Latency: Minimal increase
- CPU usage: Very low

**Supported By:**
- Mullvad
- IVPN
- NordVPN (NordLynx)
- Surfshark
- ProtonVPN

**Configuration:**
```
Protocol: WireGuard
Location: Advanced → VPN Client → WireGuard
Requires: Provider configuration file or settings
```

---

### OpenVPN

**Best for:** Universal compatibility, well-tested security

**What it is:**
- Industry-standard VPN protocol
- Open-source, heavily audited
- Proven security track record
- Universal router support

**Pros:**
- Works on virtually any device
- Strong encryption
- Highly configurable
- Extensive documentation
- Most VPN providers support it

**Cons:**
- Slower than WireGuard
- Higher CPU usage
- More complex configuration
- Older codebase

**Performance:**
- Speed loss: 15-30%
- Latency: Moderate increase
- CPU usage: Moderate to high

**Supported By:**
- Nearly all VPN providers
- ExpressVPN
- NordVPN
- ProtonVPN
- Private Internet Access

**Configuration:**
```
Protocol: OpenVPN
Location: Advanced → VPN Client → OpenVPN
Requires: .ovpn configuration file from provider
```

---

### L2TP/IPSec

**Best for:** Compatibility with older systems (if needed)

**What it is:**
- Layer 2 Tunneling Protocol with IPSec encryption
- Older but still secure when properly implemented
- Built into most operating systems

**Pros:**
- Easy to set up
- Native OS support
- No additional software needed
- More secure than PPTP

**Cons:**
- Slower than modern protocols
- Can be blocked by firewalls
- Higher overhead
- Somewhat outdated

**Performance:**
- Speed loss: 20-35%
- Latency: Higher increase
- CPU usage: Moderate

**Configuration:**
```
Protocol: L2TP/IPSec
Location: Advanced → VPN Client → L2TP/IPSec
```

---

### PPTP (Never Use)

**Status:** ❌ **AVOID COMPLETELY**

**What it is:**
- Ancient VPN protocol from 1999
- Fundamentally broken encryption
- Can be cracked in hours

**Why It Exists:**
- Legacy compatibility only
- Some old corporate systems
- Not secure for any use case

**Security:**
- 🔴 **CRITICAL VULNERABILITIES**
- NSA can crack it easily
- Academic researchers consider it broken
- No reputable VPN provider recommends it

> [!danger] Security Warning
> Never use PPTP for anything requiring security or privacy. It provides a false sense of security.

---

## Should You Use Router-Level VPN?

### When Router VPN Makes Sense ✅

**Comprehensive Protection:**
- All devices protected automatically (IoT, smart TVs, game consoles)
- No need to install VPN software on each device
- Guest network devices automatically protected

**Specific Use Cases:**
- Smart home devices that can't run VPN software
- Gaming consoles for geo-restricted content
- Legacy devices without VPN support
- Consistent whole-home privacy

**Family/Shared Living:**
- Everyone benefits without individual setup
- Centralized management
- Consistent privacy protection

### When Device-Level VPN is Better ❌

**Performance Needs:**
- Gaming where latency matters
- Streaming 4K content
- Large file downloads
- Video conferencing

**Selective Use:**
- Only need VPN for specific tasks
- Want maximum speeds most of the time
- Different family members have different needs

**Flexibility:**
- Switch VPN servers frequently
- Different VPN providers for different purposes
- Some apps need local IP (banking, work)

---

## Performance Impact

### Expected Speed Reduction

**Router-Level VPN:**
```
Without VPN: 500 Mbps
WireGuard: 425-475 Mbps (85-95%)
OpenVPN: 350-425 Mbps (70-85%)
L2TP/IPSec: 325-375 Mbps (65-75%)
```

**Factors Affecting Speed:**
- Router CPU power (biggest factor)
- VPN protocol choice
- Distance to VPN server
- Encryption overhead
- Network congestion

### Router Hardware Limitations

**Consumer Router Reality:**
Most home routers have weak CPUs that struggle with VPN encryption:

- Budget routers: 50-150 Mbps max VPN throughput
- Mid-range routers: 150-300 Mbps
- High-end routers: 300-500 Mbps
- Enterprise routers: 500+ Mbps

> [!warning] Hardware Bottleneck
> Your router's VPN speed is often limited by CPU, not your internet speed. A 1 Gbps connection may max out at 200 Mbps through router VPN.

---

## Configuration Process

### Prerequisites

1. VPN service subscription
2. Router firmware that supports VPN client
3. Configuration file or credentials from VPN provider
4. Router admin access

### Setup Steps (OpenVPN Example)

1. **Get Configuration Files**
   - Login to VPN provider dashboard
   - Download OpenVPN configuration files
   - Choose server location

2. **Router Configuration**
   ```
   Access: Advanced → VPN Client → OpenVPN
   Upload: .ovpn configuration file
   Enter: Username and password
   Enable: Kill switch (important!)
   ```

3. **Verify Connection**
   - Check VPN status in router dashboard
   - Visit: whatismyip.com
   - Confirm IP shows VPN server location

4. **Test Performance**
   - Run speed test: speedtest.net
   - Compare with/without VPN
   - Adjust server if needed

---

## DNS Configuration with VPN

**Critical for Privacy:**

When using router VPN, ensure DNS queries also go through VPN tunnel:

**Option 1: VPN Provider DNS (Recommended)**
```
Use DNS servers provided by VPN service
Automatic configuration in most cases
```

**Option 2: Custom DNS over VPN**
```
Primary: 1.1.1.1 (Cloudflare)
Secondary: 9.9.9.9 (Quad9)
Ensure these go through VPN tunnel
```

> [!warning] DNS Leak Risk
> If DNS queries bypass VPN, your ISP can still see which websites you visit. Always verify DNS configuration.

**Test for DNS Leaks:**
- Visit: dnsleaktest.com
- Run extended test
- Verify DNS servers match VPN provider

---

## Kill Switch

**What it does:** Blocks all internet traffic if VPN connection drops, preventing accidental exposure.

**Status:** ✅ **ALWAYS ENABLE**

**Why it's Critical:**
- VPN connections can drop unexpectedly
- Without kill switch, traffic reverts to unencrypted ISP connection
- Defeats entire purpose of VPN for privacy

**Configuration:**
```
Kill Switch: ENABLED
Location: Advanced → VPN Client → Settings
Alternative names: "Network Lock", "VPN Firewall"
```

---

## VPN vs DNS Configuration

### The Key Difference

**DNS Change (from [[02 - DNS Configuration]]):**
- **What it protects:** DNS queries only
- **Speed impact:** Minimal (~0-2%)
- **Privacy gain:** Prevents ISP DNS logging
- **Complexity:** Very simple

**Router VPN:**
- **What it protects:** All internet traffic
- **Speed impact:** Significant (15-30%)
- **Privacy gain:** Complete IP masking, encryption
- **Complexity:** Moderate to high

### Recommended Approach

**For Most Users:**
```
1. Custom DNS (1.1.1.1, 9.9.9.9) - Always
2. Router VPN - Only if specific need
3. Device VPN - For selective use when needed
```

**Privacy-Focused Setup:**
```
1. Custom DNS with DoH (DNS over HTTPS)
2. Router VPN (WireGuard if available)
3. Additional device VPN for high-privacy tasks
```

---

## Alternative Solutions

### Tailscale (Personal VPN Alternative)

**What it is:** Private mesh network connecting your devices

**Pros:**
- Zero configuration NAT traversal
- Better performance than traditional VPN
- Free for personal use
- No public IP exposure

**Cons:**
- Not for hiding IP from websites
- Different use case than privacy VPN

**Best for:** 
- Accessing home network remotely
- Private device-to-device connections
- Alternative to DDNS

---

## Troubleshooting

**VPN Won't Connect:**
- Verify credentials are correct
- Check configuration file format
- Ensure router firmware is updated
- Try different VPN server
- Contact VPN provider support

**Slow Speeds:**
- Try closer VPN server location
- Switch to WireGuard if available
- Check router CPU usage (may be maxed out)
- Consider device-level VPN instead

**Some Apps Don't Work:**
- Banking apps may block VPN IPs
- Streaming services may detect VPN
- Consider split tunneling (if supported)
- Use device-level VPN for selective routing

**DNS Leaks:**
- Configure DNS to use VPN provider's servers
- Enable kill switch
- Test at dnsleaktest.com
- May need custom firewall rules

---

## Recommended VPN Providers

### Privacy-Focused
- **Mullvad** - Anonymous payment, no logs, WireGuard support
- **IVPN** - Audited no-logs policy, strong privacy
- **ProtonVPN** - Secure Core, Swiss privacy laws

### Performance-Focused
- **NordVPN** - NordLynx (WireGuard), good speeds
- **ExpressVPN** - Fast servers, easy setup
- **Surfshark** - Good balance, unlimited devices

---

## Related Topics
- [[02 - DNS Configuration]] - Privacy-focused DNS (simpler alternative)
- [[03 - Dynamic DNS Setup]] - Remote access without VPN
- [[05 - ALG Settings]] - VPN Passthrough configuration
- [[08 - Privacy & Security Hardening]] - Complete privacy guide

---

#vpn #privacy #security #wireguard #openvpn

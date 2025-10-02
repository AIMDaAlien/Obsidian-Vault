# DNS Configuration

DNS (Domain Name System) translates website names into IP addresses. Your choice of DNS provider significantly impacts privacy and performance.

---

## Why Custom DNS Matters

**Privacy Impact:** Your ISP can see and log every website you visit through their DNS servers. Custom DNS prevents this tracking.

**Performance Impact:** Faster DNS lookups mean quicker page loads. Quality DNS providers often outperform ISP defaults.

---

## Recommended DNS Providers

### Primary Recommendation: Cloudflare + Quad9

| Provider | Primary | Secondary | Focus | Speed |
|----------|---------|-----------|-------|-------|
| **Cloudflare** ⭐ | 1.1.1.1 | 1.0.0.1 | Speed + Privacy | Excellent |
| **Quad9** | 9.9.9.9 | 149.112.112.112 | Security + Privacy | Very Good |
| OpenDNS | 208.67.222.222 | 208.67.220.220 | Filtering + Control | Good |
| Google | 8.8.8.8 | 8.8.4.4 | Speed (less privacy) | Excellent |

### Recommended Setup
```
Primary DNS: 1.1.1.1 (Cloudflare - fast & private)
Secondary DNS: 9.9.9.9 (Quad9 - security focused)
```

---

## Configuration Methods

### Method 1: Router-Level (Recommended)

Applies DNS to all devices automatically.

**Steps:**
1. Access router web interface (not mobile app)
2. Navigate to: `Advanced → Network → Internet`
3. Find DNS Server settings
4. Enter: Primary: `1.1.1.1` Secondary: `9.9.9.9`
5. Save and reboot router

> [!tip] Mobile App Limitation
> TP-Link's Tether app restricts DNS changes with Dynamic IP. Use the web interface at `192.168.1.1` instead.

### Method 2: Device-Level

Configure DNS on individual devices. More control but requires per-device setup.

**Windows:**
```
Settings → Network & Internet → Change adapter options
Right-click adapter → Properties → IPv4 → Use the following DNS
```

**macOS:**
```
System Preferences → Network → Advanced → DNS
Add DNS servers: 1.1.1.1, 9.9.9.9
```

**Android/iOS:**
```
WiFi Settings → Modify Network → Advanced → DNS
```

---

## DNS Provider Comparison

### Cloudflare (1.1.1.1)
**Best for:** General use, maximum speed

**Pros:**
- Fastest DNS resolver globally
- Strong privacy policy (doesn't log queries)
- No data selling
- DNSSEC validation

**Cons:**
- No built-in content filtering
- Minimal logging means less troubleshooting data

### Quad9 (9.9.9.9)
**Best for:** Security-conscious users

**Pros:**
- Blocks malicious domains automatically
- Privacy-respecting (based in Switzerland)
- DNSSEC validation
- Threat intelligence integration

**Cons:**
- Slightly slower than Cloudflare (still excellent)
- Blocking can rarely cause false positives

### OpenDNS
**Best for:** Families needing content filtering

**Pros:**
- Customizable filtering
- Parental controls
- Phishing protection
- Dashboard for monitoring

**Cons:**
- Owned by Cisco (privacy concerns)
- Requires account for filtering
- Slightly slower than Cloudflare

### Google DNS (8.8.8.8)
**Best for:** Speed over privacy

**Pros:**
- Very fast
- Extremely reliable
- Global infrastructure

**Cons:**
- Google tracks queries
- Data used for advertising profiles
- Privacy concerns

---

## Advanced: DNS Over HTTPS (DoH)

Encrypts DNS queries end-to-end, preventing even your router from seeing which domains you're visiting.

**Setup on devices:**
- **Windows 11:** Settings → Network → Ethernet/WiFi → DNS → Encrypted preferred
- **Firefox:** Settings → Privacy → Enable DNS over HTTPS → Cloudflare
- **Chrome:** Settings → Privacy → Use secure DNS → Cloudflare

> [!info] Enhanced Privacy
> DoH prevents ISP and router from logging DNS queries. Combine with custom DNS for maximum privacy.

---

## Verification

Test your DNS configuration:

1. Visit: https://1.1.1.1/help
2. Check DNS resolver shows your chosen provider
3. Verify DNSSEC is working

Or use command line:
```bash
nslookup google.com
# Should show your custom DNS server IP
```

---

## Troubleshooting

**DNS not changing:**
- Clear browser cache
- Flush DNS cache: `ipconfig /flushdns` (Windows) or `sudo dscacheutil -flushcache` (Mac)
- Reboot router after changes
- Use web interface instead of mobile app

**Slower internet after DNS change:**
- Try different DNS provider
- Check geographic proximity (use provider with servers near you)
- Verify you entered IPs correctly

---

## Related Topics
- [[01 - Network Connection Settings]] - Base network configuration
- [[08 - Privacy & Security Hardening]] - Additional privacy measures

---

#dns #privacy #performance #configuration

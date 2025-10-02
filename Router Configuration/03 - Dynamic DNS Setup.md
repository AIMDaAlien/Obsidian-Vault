# Dynamic DNS Setup

Dynamic DNS (DDNS) gives your home network a permanent domain name even though your ISP changes your IP address regularly.

---

## What is Dynamic DNS?

**The Problem:** Your ISP regularly changes your IP address. Remote access breaks every time your IP changes.

**The Solution:** DDNS creates a domain name (like `myhouse.example.com`) that automatically updates to point to your current IP address.

**Real-World Analogy:** Your house keeps moving to different streets, but the domain name acts as a permanent forwarding address that always knows where to find you.

---

## Do You Actually Need DDNS?

**You need DDNS if:**
- Accessing home network remotely (SSH, RDP, VPN server)
- Running web server, game server, or NAS from home
- Hosting services external people need to reach
- Remote security camera access

**You DON'T need DDNS if:**
- Just browsing the internet
- Using cloud services
- Only accessing services locally
- Using commercial VPN services

> [!warning] Privacy Consideration
> DDNS creates a permanent identifier linked to your IP address, making long-term tracking easier. Only use if you genuinely need remote access.

---

## Provider Comparison

### No-IP (Recommended) ⭐

**Best for:** Most users seeking reliable DDNS with good privacy

| Feature | Details |
|---------|---------|
| **Cost** | Free tier available |
| **Privacy** | Strong privacy policy, US-based |
| **Performance** | Fast DNS updates (<60 seconds) |
| **Features** | Robust free tier, DDoS protection |
| **Reliability** | Excellent uptime |

**Setup:**
```
Service Provider: No-IP
Purpose: Remote Access
Configuration: Router web interface → Dynamic DNS
```

### DynDNS

**Best for:** Business users needing enterprise features

**Pros:**
- Enterprise-grade reliability
- Advanced analytics
- Professional support

**Cons:**
- Paid service only ($5-25/month)
- Overkill for home users
- More complex than necessary

### TP-Link DDNS

**Best for:** Convenience (with caveats)

**Pros:**
- Free with router
- Easy integration
- Simple setup

**Cons:**
- Limited privacy information
- Chinese company (privacy concerns)
- Vendor lock-in
- Basic features only

---

## Privacy & Security Implications

### Tracking Risks

Dynamic DNS creates several tracking opportunities:

**Permanent Identifier:** Your domain name becomes a persistent tracker linked to your IP address history.

**Public Record:** Domain name is publicly searchable via DNS lookups.

**Attack Surface:** Predictable domain makes you a more consistent target for automated scanning.

**Data Collection:** DDNS providers log IP changes, connection patterns, and usage statistics.

### Privacy Best Practices

1. **Use obscure hostnames**
   - ❌ Bad: `johnsmith-home.ddns.net`
   - ✅ Good: `delta-7-echo-42.ddns.net`

2. **Enable strong authentication**
   - Use 2FA on DDNS account
   - Unique, strong password (20+ characters)

3. **Limit service exposure**
   - Only expose specific services needed
   - Use non-standard ports
   - Never leave default configurations

4. **Regular monitoring**
   - Check DNS provider logs for unusual activity
   - Monitor for unexpected DNS queries

5. **Consider alternatives**
   - Tailscale (private mesh network)
   - ZeroTier (software-defined networking)
   - Cloudflare Tunnel (no public DNS records)

---

## Configuration Steps

### Router Setup

1. Access router web interface
2. Navigate to: `Advanced → Dynamic DNS`
3. Select service provider
4. Choose purpose/plan
5. Create account credentials
6. Save and verify

### Account Setup (No-IP)

1. Create account at no-ip.com
2. Choose hostname (make it non-obvious)
3. Configure router with credentials
4. Test by accessing your domain name

---

## Alternatives to DDNS

If privacy is paramount, consider these modern alternatives:

### Tailscale
- **What:** Private mesh VPN network
- **Privacy:** Excellent (end-to-end encrypted)
- **Complexity:** Low (automatic configuration)
- **Cost:** Free for personal use
- **Best for:** Personal remote access without public exposure

### ZeroTier
- **What:** Software-defined networking
- **Privacy:** Excellent (encrypted overlay network)
- **Complexity:** Moderate
- **Cost:** Free tier available
- **Best for:** Advanced users wanting full control

### Cloudflare Tunnel
- **What:** Secure tunnel to Cloudflare's network
- **Privacy:** Good (no public DNS records)
- **Complexity:** Moderate
- **Cost:** Free
- **Best for:** Exposing web services without port forwarding

> [!tip] Modern Recommendation
> For personal use, Tailscale often provides better security and privacy than traditional DDNS with similar ease of use.

---

## Troubleshooting

**Domain not resolving:**
- Verify DNS update occurred (check provider dashboard)
- DNS propagation can take up to 15 minutes
- Clear local DNS cache
- Check router DDNS status page

**Frequent connection drops:**
- IP may be changing more often than DDNS updates
- Check update interval settings
- Consider paid tier for faster updates

**Can't access services:**
- Verify port forwarding rules
- Check firewall settings
- Ensure service is running
- Test from external network (not local)

---

## Security Hardening

If you proceed with DDNS, implement these protections:

1. **Firewall rules:** Only allow specific IPs or countries
2. **Port changes:** Never use default ports (22, 80, 443, 3389)
3. **VPN access:** Require VPN connection before service access
4. **Rate limiting:** Enable connection throttling
5. **Monitoring:** Set up alerts for unusual access patterns

---

## Related Topics
- [[01 - Network Connection Settings]] - Base network configuration
- [[08 - Privacy & Security Hardening]] - Security best practices
- [[06 - VPN Configuration]] - VPN as DDNS alternative

---

#ddns #remote-access #privacy #security

# Privacy Hardening Journey

#privacy #security #android #smart-devices #data-protection

> **Reality Check**: Modern devices are surveillance systems with useful features attached

## Key Learnings

### OnePlus 12 Privacy Overhaul
**Discovery**: Even after removing bloatware, essential apps were sending data to brokers
**Effective Solutions**:
- **Private DNS**: `dns.adguard.com` blocks trackers at network level
- **NetGuard/TrackerControl**: Per-app network control without VPN overhead
- **ADB Commands**: `pm uninstall -k --user 0 net.oneplus.odm` removes telemetry
- **Shelter App**: Isolates apps in work profile, prevents cross-app tracking

**Learning**: Circumventing surveillance requires multiple layers

### Amazon Echo Pop Hardening
**Problem**: Suspected always-listening despite mic button
**Mitigation Strategy**:
- Physical network isolation (separate IoT VLAN)
- DNS blocking of Amazon telemetry domains
- Regular voice history deletion
- Microphone hardware switch when available

**Insight**: Smart devices prioritize convenience over privacy by design

## Privacy Principles Discovered

### Threat Model First
```
1. Who are you protecting against? (Advertisers, state actors, criminals)
2. What data matters most? (Location, communications, browsing)
3. What's your convenience trade-off tolerance?
4. How much technical complexity can you maintain?
```

### Defense in Depth
- **Network Level**: DNS filtering, firewall rules
- **Device Level**: App permissions, tracking controls  
- **App Level**: Privacy-focused alternatives
- **Behavioral**: Data minimization, compartmentalization

### Practical Wins vs. Perfect Security
**High Impact, Low Effort**:
- Private DNS setup (5 minutes, huge benefit)
- Default app permission review
- Advertising ID reset/disable
- Regular privacy settings audit

**Diminishing Returns**:
- Custom ROMs (high maintenance)
- Complete Google avoidance (convenience loss)
- Hardware modification (warranty void)

## Tools That Actually Work

### Android Privacy Stack
- **TrackerControl**: Real-time tracker blocking
- **Shelter**: App isolation without root
- **Aurora Store**: Google Play without Google account
- **F-Droid**: Open source app repository

### Network Privacy
- **Private DNS**: First line of defense
- **Router-level blocking**: Protects all devices
- **VPN selective**: Use only when necessary

### Monitoring/Verification  
- **Netstat apps**: See what's actually connecting where
- **DNS query logs**: Verify blocking is working
- **Permission audits**: Regular app permission review

## Common Mistakes Learned

### Over-engineering
- Don't break functionality for marginal privacy gains
- Perfect is the enemy of good
- Complexity creates new attack vectors

### Vendor Trust
- "Privacy-focused" marketing vs. actual privacy
- Open source doesn't automatically mean secure
- Regular audits of trusted tools

**Core Principle**: Privacy is a process, not a product.

---
*Tags: #privacy #security #android #surveillance #data-protection*  
*Related: [[Learning/Troubleshooting Lessons Learned]] | [[Learning/Tech Research Strategies]]*
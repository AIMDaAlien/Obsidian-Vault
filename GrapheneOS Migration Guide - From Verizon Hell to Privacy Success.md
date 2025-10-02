# GrapheneOS Migration Guide: From Verizon Hell to Privacy Success

## Executive Summary
This document chronicles a complete journey from attempting to install GrapheneOS on a carrier-locked device to successfully migrating to a functional privacy-focused setup. Key lesson: **Carrier-locked devices are a dead end** - always verify bootloader unlock capability before purchase.

## The Problem: Verizon Bootloader Lock
### Initial Situation
- **Device**: Pixel 6 Pro from carrier (Verizon-branded)
- **Goal**: Install GrapheneOS for enhanced privacy
- **Obstacle**: Automatic eSIM detection suggested Verizon variant

### Verizon Lock Investigation
**Critical Finding**: Verizon Pixel devices **cannot** be bootloader unlocked through any reliable method as of 2025.

**Technical Details**:
- Verizon locks bootloaders at factory via carrier ID in persist partition
- "OEM unlocking" toggle permanently grayed out
- No working exploits or workarounds
- Even customer service explicitly refuses unlock requests

**Verification Methods Failed**:
- Claims of "dirty pipe" exploit (patched/unreliable)
- SIM unlocking ≠ bootloader unlocking for Verizon
- No developer has produced reproducible unlock method

## The Pivot: Security Comparison Analysis
When GrapheneOS proved impossible, compared security options:

### Stock Pixel 6 Pro (Android 16) vs OnePlus 12 (OxygenOS 15)
**Security Winner**: Pixel 6 Pro (51/60 score)
- Titan M security chip
- Hardware-based verified boot
- 7 years security updates until 2028
- Superior hardware security foundation

**Privacy Winner**: OnePlus 12 (41/60 score)  
- Less Google integration
- Better privacy controls in OxygenOS 15
- More granular service disabling
- Easier to minimize data collection

**Conclusion**: Since GrapheneOS wasn't possible, OnePlus 12 was better choice for privacy despite weaker hardware security.

## The Solution: Pixel 7 Pro Acquisition Strategy

### Pre-Purchase Verification Protocol
**Critical Step**: Always verify bootloader unlock capability before buying.

#### IMEI Verification Process
1. **Google's Official Check**: store.google.com/repair
   - Enter IMEI number
   - ✅ Good: Shows device info without "VZ" 
   - ❌ Bad: Shows "VZ" (Verizon) = permanently locked
   - ❓ Unclear: "Cannot determine warranty status"

2. **Physical Verification** (if buying in person):
   - Enable Developer Options (tap Build Number 7x)
   - Check Settings → System → Developer Options → "OEM unlocking"
   - ✅ Toggle available = unlockable
   - ❌ Grayed out = carrier locked

#### Model Number Reference
**Pixel 7 Pro Models**:
- ✅ Unlocked: GVU6C, GA03460-US
- ❌ Verizon: GE2AE (avoid completely)

### Damage Assessment for Used Devices
**Installation-Compatible Damage**:
- ✅ Broken back glass (cosmetic only)
- ✅ Missing volume/power buttons (use ADB commands)
- ✅ Minor screen cracks (if touch works)

**Deal Breakers**:
- ❌ Damaged USB-C port (required for installation)
- ❌ Non-responsive touchscreen
- ❌ Won't power on

## Implementation: GrapheneOS Installation

### Successful Installation Process
**Device**: Pixel 7 Pro with broken back glass and missing volume buttons
**Cost**: Significantly reduced due to cosmetic damage
**Installation Time**: ~30 minutes using web installer

#### Pre-Installation Setup
1. Enable Developer Options
2. Enable "OEM unlocking" 
3. Enable "USB debugging"
4. Avoid Google account sign-in (gets wiped anyway)

#### Installation Method
- **Tool**: GrapheneOS web installer (grapheneos.org/install/web)
- **Browser**: Chrome (best WebUSB support on macOS)
- **Alternative**: CLI method if WebUSB fails

#### Missing Button Workaround
Since volume buttons were missing:
```bash
adb reboot bootloader  # Enter fastboot mode via ADB
```
Rest of installation proceeded normally via web interface.

### Post-Installation Configuration Priority
1. Install F-Droid from GrapheneOS Apps
2. Enable sandboxed Google Play for eSIM functionality
3. Set auto-reboot to 18 hours (Security settings)
4. Configure Network permissions for apps

## App Strategy: Dual-Device Approach

### Device Separation Strategy
**Pixel 7 Pro (GrapheneOS)**:
- Calls, SMS, Signal messaging
- Banking apps (most compatible)
- Navigation, camera, essential utilities
- eSIM for carrier services

**OnePlus 12 (Existing Setup)**:
- Social media, games, work applications
- Google services requiring full integration
- Apps requiring Play Integrity

### Privacy-Focused App Migration
**High Priority for GrapheneOS** (high telemetry/data collection):
- Social media platforms
- Google services (YouTube, Maps, Photos)
- Microsoft applications
- Shopping apps
- Ride sharing services

**Key Advantage**: Network permission toggle allows complete internet blocking for apps that don't require connectivity.

## Lessons Learned

### Critical Success Factors
1. **Verification First**: Always check bootloader unlock capability before purchase
2. **Carrier Avoidance**: Never buy carrier-branded devices for custom ROMs
3. **Damage Tolerance**: Cosmetic damage doesn't affect functionality
4. **Tool Selection**: Web installer superior to manual methods

### Cost-Benefit Analysis
- **Verizon Device**: $X spent, 0% success rate, time wasted
- **Damaged Pixel 7 Pro**: ~50% price reduction, 100% success rate
- **GrapheneOS Support**: Until October 2028 (3+ years)

### Technical Insights
- **WebUSB Issues**: Common on macOS, Chrome works best
- **ADB Workarounds**: Physical button damage irrelevant for installation
- **Dual-Device Benefits**: Risk isolation, gradual migration, fallback option

## Recommendations for Others

### Before Purchase
1. **Verify IMEI** using Google's official tool
2. **Confirm OEM unlocking** toggle availability
3. **Test USB-C port** functionality
4. **Negotiate based on cosmetic damage** (30-50% reduction possible)

### Installation Approach
1. **Use web installer** unless technical preference for CLI
2. **Prepare for WebUSB issues** on macOS/Linux
3. **Don't fear cosmetic damage** - focus on core functionality
4. **Plan dual-device strategy** for smoother transition

### Long-term Strategy
- **Start with essential apps** on GrapheneOS
- **Gradually migrate** privacy-sensitive applications
- **Use Network permissions** aggressively
- **Keep fallback device** until comfortable with compatibility

## Conclusion
This migration demonstrates that with proper verification and realistic expectations, transitioning to GrapheneOS is achievable even with damaged devices. The key insight: **carrier restrictions are absolute blockers**, but verified unlocked devices provide excellent privacy foundations regardless of cosmetic condition.

**Final Status**: Successfully running GrapheneOS on Pixel 7 Pro with full functionality, enhanced privacy controls, and security updates through 2028.

---
*Document created: September 2025*  
*Hardware: Pixel 7 Pro (cosmetically damaged, fully functional)*  
*Software: GrapheneOS latest stable release*
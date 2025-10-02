# Performance Optimization Checklist

Quick-reference guide for achieving optimal router performance.

---

## 🚀 Quick Wins (10 Minutes)

These provide immediate, measurable improvements:

### 1. Channel Optimization
- [ ] Set 2.4GHz to channel 1, 6, or 11 (manual)
- [ ] Set 5GHz to Auto with DFS enabled
- [ ] Channel width: 20MHz (2.4GHz), 80MHz (5GHz)

**Impact:** 30-50% speed improvement in congested areas

---

### 2. Enable Airtime Fairness
- [ ] Navigate to Wireless → Professional
- [ ] Enable Airtime Fairness

**Impact:** 30-50% throughput increase with mixed device ages

---

### 3. Disable Problematic ALGs
- [ ] Disable SIP ALG (most important!)
- [ ] Disable FTP ALG
- [ ] Disable H323 ALG
- [ ] Disable PPTP Passthrough

**Impact:** Better connection reliability, reduced CPU overhead

---

### 4. Enable QoS/Gaming Accelerator
- [ ] Navigate to Advanced → QoS
- [ ] Enable QoS or Gaming Accelerator
- [ ] Set bandwidth limits to 90% of actual speeds

**Impact:** Reduced lag, better streaming during heavy usage

---

## 🔧 Advanced Optimizations (30 Minutes)

### 5. Wireless Advanced Features

**Enable all modern WiFi features:**
- [ ] WMM: ENABLED (should already be on)
- [ ] MU-MIMO: ENABLED
- [ ] Beamforming: ENABLED
- [ ] OFDMA: ENABLED (WiFi 6+)
- [ ] BSS Coloring: ENABLED (WiFi 6+)

**Location:** Wireless → Professional → Advanced Features

**Impact:** 20-40% improvement for multiple devices

---

### 6. Transmission Power Optimization

**Don't max it out!**
- [ ] Small apartment: 50-75%
- [ ] Large house: 75-100%
- [ ] Dense area (apartments): 50%

**Why:** Excessive power increases interference without improving range

**Location:** Wireless → Professional → Transmit Power

---

### 7. Fast Roaming (Multi-AP Setups)

If you have mesh or multiple access points:
- [ ] Enable 802.11k (Neighbor Report)
- [ ] Enable 802.11v (BSS Transition)  
- [ ] Enable 802.11r (Fast Transition)

**Location:** Wireless → Professional → Fast Roaming

**Impact:** Seamless device transitions between APs

---

### 8. DNS Optimization

- [ ] Primary DNS: 1.1.1.1 (Cloudflare)
- [ ] Secondary DNS: 9.9.9.9 (Quad9)
- [ ] Enable DNS over HTTPS on devices

**Location:** Advanced → Network → Internet → DNS Settings

**Impact:** Faster page loads, better privacy

See [[02 - DNS Configuration]] for details

---

### 9. NAT Acceleration

If available on your router:
- [ ] Enable Hardware NAT
- [ ] Enable NAT Acceleration
- [ ] Enable TCP Congestion Control

**Location:** Advanced → System Tools → System Parameters

**Impact:** Higher throughput, reduced latency

---

### 10. Security Key Updates

- [ ] Set Group Key Update Period: 3600 seconds

**Location:** Wireless → Professional → Group Key Update

**Impact:** Better security, imperceptible performance impact

---

## 🛠️ Maintenance (Monthly)

### 11. Firmware Updates
- [ ] Check for firmware updates monthly
- [ ] Read changelog before updating
- [ ] Backup configuration first
- [ ] Manual updates preferred over auto

**Impact:** Security patches, bug fixes, performance improvements

---

### 12. Auto Reboot Schedule
- [ ] Enable weekly automatic reboot
- [ ] Schedule for 3 AM Sunday (or low-usage time)

**Location:** Advanced → System Tools → Reboot Schedule

**Impact:** Clears memory leaks, maintains optimal performance

---

### 13. Configuration Backup
- [ ] Export router configuration
- [ ] Store backup securely offline
- [ ] Label with date and changes made

**Location:** Advanced → System Tools → Backup & Restore

---

## 📊 Performance Testing

### Baseline Testing
1. **Without changes:** Run speedtest.net
2. **Apply optimizations:** One category at a time
3. **Retest after each:** Document improvements
4. **Keep what works:** Revert if something causes issues

### Testing Tools
- **Speed:** speedtest.net, fast.com
- **WiFi Analysis:** WiFi Analyzer (Android), NetSpot (Mac/PC)
- **DNS Performance:** DNSPerf.com
- **Latency:** pingtest.net
- **Buffer bloat:** waveform.com/tools/bufferbloat

---

## 🎯 Optimization by Use Case

### Gaming
**Priority settings:**
1. ✅ QoS/Gaming Accelerator enabled
2. ✅ DTIM Interval: 1
3. ✅ WMM enabled
4. ✅ SIP ALG disabled
5. ✅ 5GHz for gaming devices
6. ✅ Manual channel selection (least congested)

---

### Streaming (4K/Multiple Devices)
**Priority settings:**
1. ✅ Airtime Fairness enabled
2. ✅ QoS with streaming priority
3. ✅ MU-MIMO enabled
4. ✅ 80MHz channel width (5GHz)
5. ✅ Beamforming enabled

---

### Smart Home/IoT Heavy
**Priority settings:**
1. ✅ Separate 2.4GHz and 5GHz networks
2. ✅ IoT devices on 2.4GHz
3. ✅ Disable Smart Connect
4. ✅ DTIM Interval: 3 (battery optimization)
5. ✅ Lower transmission power if congested

---

### Work From Home (Video Calls)
**Priority settings:**
1. ✅ QoS with video/voice priority
2. ✅ WMM enabled
3. ✅ 5GHz for computer
4. ✅ Ethernet for critical devices
5. ✅ SIP ALG disabled (if using VoIP)

---

### Maximum Privacy
**Priority settings:**
1. ✅ Custom DNS (Cloudflare + Quad9)
2. ✅ DNS over HTTPS enabled
3. ✅ All unnecessary ALGs disabled
4. ✅ TP-Link Cloud disabled
5. ✅ Group Key Update: 3600
6. ✅ See [[08 - Privacy & Security Hardening]]

---

## 🔍 Troubleshooting Performance Issues

### Slow WiFi Speeds

**Check these in order:**
1. Run WiFi analyzer - check for interference
2. Change to less congested channel
3. Verify device supports current WiFi standard
4. Check distance from router
5. Enable Airtime Fairness
6. Reduce transmission power if in dense area

---

### High Latency/Lag

**Check these in order:**
1. Disable SIP ALG and FTP ALG
2. Enable QoS/Gaming Accelerator
3. Set DTIM to 1
4. Verify WMM enabled
5. Check for buffer bloat
6. Consider disabling all ALGs temporarily

---

### Frequent Disconnections

**Check these in order:**
1. Update router firmware
2. Disable problematic ALGs (FTP, SIP)
3. Change wireless channel
4. Check RTS Threshold (should be 2346)
5. Verify power supply is adequate
6. Check for router overheating

---

### Slow Device-Specific Performance

**Check these in order:**
1. Verify device WiFi capabilities
2. Update device network drivers
3. Check if device is on 2.4GHz (move to 5GHz if supported)
4. Verify not too far from router
5. Test with different channel
6. Check if device needs Airtime Fairness disabled

---

## 📈 Expected Performance Gains

### After All Optimizations

**Speed Improvements:**
- WiFi throughput: +30-50%
- Latency reduction: -20-40%
- Device capacity: +50-100%
- Reliability: Significantly improved

**Real-World Example:**
```
Before optimization:
- 2.4GHz: 40 Mbps
- 5GHz: 250 Mbps
- Ping: 25ms
- Dropped connections: Weekly

After optimization:
- 2.4GHz: 55 Mbps
- 5GHz: 375 Mbps
- Ping: 15ms
- Dropped connections: Rare
```

---

## ⚠️ Common Mistakes to Avoid

### Don't Do These:

1. **Maxing transmission power**
   - More interference, not better range
   - Use 50-75% in most cases

2. **Using Auto channel on 2.4GHz**
   - Often picks congested channels
   - Manual selection (1/6/11) is better

3. **Enabling every ALG**
   - More problems than solutions
   - Disable what you don't need

4. **Ignoring firmware updates**
   - Miss security patches
   - Miss performance improvements

5. **No configuration backup**
   - Settings lost if router resets
   - Have to reconfigure everything

6. **Using WEP or WPA**
   - Ancient, insecure
   - Always use WPA2 or WPA3

7. **Default admin password**
   - Major security vulnerability
   - Change immediately

8. **Enabling WPS**
   - Easily hackable
   - Disable immediately

---

## 🎓 Advanced Tips

### Buffer Size Optimization
If your router supports it:
```
TCP Buffer: 65536 bytes
UDP Buffer: 32768 bytes
Location: Advanced → System Tools → System Parameters
```

---

### CPU Governor (If Available)
```
Performance mode: Maximum speed
Ondemand mode: Balance efficiency
Location: Advanced → System Tools → CPU Settings
```

---

### IPv6 MTU Tuning
```
Gaming: 1280 (lower latency)
General: 1500 (better throughput)
Location: Advanced → IPv6 → Advanced → MTU
```

---

## 📱 Mobile Optimization

### For Better Mobile Performance:
- [ ] Enable 802.11k/v/r if available
- [ ] DTIM: 1 (performance) or 3 (battery balance)
- [ ] Disable MAC randomization compatibility issues
- [ ] Enable Private Address Support

---

## 🔄 Continuous Optimization

**Monthly checklist:**
1. Check for firmware updates
2. Review performance metrics
3. Adjust channels if interference changed
4. Clean up connected devices list
5. Verify backup is current

**Quarterly checklist:**
1. Full performance benchmark
2. Compare against baseline
3. Review and optimize QoS rules
4. Update DNS if better options available
5. Audit security settings

---

## Related Topics
- [[04 - Advanced Wireless Settings]] - Detailed wireless config
- [[05 - ALG Settings]] - Protocol optimization
- [[08 - Privacy & Security Hardening]] - Security while optimizing

---

#performance #optimization #checklist #wifi

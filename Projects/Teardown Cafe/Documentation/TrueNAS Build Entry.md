# TrueNAS Enterprise SAS Build - Teardown Cafe Entry

> **For teardown-cafe project:** `/Users/aim/Documents/teardown-cafe/src/content/teardowns/`  
> **Date built:** September 28, 2025 (3 weeks ago)  
> **Status:** Ready for markdown file creation once photos are processed

---

## Frontmatter Template

```markdown
---
title: "Enterprise SAS NAS Build - Budget TrueNAS Server"
description: "Building a 5.46TB enterprise NAS from scratch using 10 SAS drives, LSI HBA controller, and consumer hardware for under $300"
pubDate: 2025-09-28
heroImage: "/images/truenas-sas-build/01-complete-system.jpg"
device: "nas"
difficulty: "medium"
obsidianNotes:
  - title: "TrueNAS Build Guide"
    path: "Projects/TrueNAS Build Guide"
  - title: "Budget SAS Drive NAS Build Guide"
    path: "Projects/Budget SAS Drive NAS Build Guide"
---
```

---

## Content Structure

### Opening Section

**Why I Did This**

I scored 10 enterprise SAS hard drives for $50 at a local sale - seemed like a steal until I realized they needed specialized controllers to even connect to a PC. What started as "how do I use these drives?" turned into a month-long journey sourcing parts, troubleshooting power adapters, and building a legitimate enterprise-grade NAS for under $300. 

The goal was simple: **maximize storage capacity while staying economical**. No pre-built Synology boxes at $800+. Just smart sourcing, enterprise hardware, and a lot of patience.

---

### Hardware Breakdown

**The Complete Build**

| Component | Specs | Price | Source/Notes |
|-----------|-------|-------|--------------|
| **System** | Intel i5-11400 (6-core) | $190 | Found complete office PC with 64GB DDR4-3600 |
| **Motherboard** | ASRock B660M Pro RS | Included | Came with system |
| **RAM** | 64GB DDR4-3600 | Included | CPU supports DDR4-3200 (89% utilization) |
| **HBA Card** | LSI 9207-8i (IT mode, P20 firmware) | $35 | Pre-flashed, critical for ZFS compatibility |
| **Cables** | 2x SFF-8087 to 4x SATA with integrated power | $30 | Avoided Molex hell |
| **Storage** | 10x Seagate 1.2TB 10K RPM SAS drives | $50 | Enterprise pulls, 1.09TB usable each |
| **Boot Drive** | 128GB NVMe SSD | $15 | TrueNAS SCALE dedicated |
| **PSU** | 500W (existing) | $0 | System draws ~140W with 8 drives |
| **Total** | | **~$320** | Using 7 drives = ~$285 effective cost |

**Storage Configuration:**
- **RAID-Z2** (7 drives): 5 data + 2 parity
- **Usable capacity:** 5.46TB from 7.63TB raw
- **Can survive:** Any 2 drive failures without data loss
- **Spare drives:** 2 remaining (1 DOA, 1 backup)
- **Max capacity:** 8 drives with HBA card

---

### The Month-Long Sourcing Journey

**Week 1: The SAS Reality Check**
- Discovered SAS ≠ SATA (enterprise vs consumer interface)
- Required: HBA (Host Bus Adapter) controller card
- LSI 9207-8i became the target: 2x SFF-8087 ports = 8 drives

**Week 2: The Power Adapter Nightmare**
- Initial plan: Molex to SATA power adapters
- **Problem:** Molex is ancient tech, sketchy connections
- **Solution:** Found SFF-8087 to SATA cables with integrated SATA power
- Each cable: 1 SFF-8087 plug → 4x SATA data + power connectors

**Week 3: The CPU Generation Mistake**
- Originally looked at 6th-8th gen Intel (DDR4-2400 max)
- Had DDR4-3600 RAM sitting around
- Realized: Only using 67% of RAM capability
- **Pivot:** Found i5-11400 system (DDR4-3200 support = 89% utilization)
- Extra cost: Worth it for proper hardware matching

**Week 4: Finding The System**
- Quoted $280-380 for typical office PCs
- Found deal: Complete i5-11400 system for $190
- Included motherboard, RAM, PSU, case

---

### The Build Process

**Physical Assembly**

1. **HBA Installation**
   - LSI 9207-8i into PCIe x8 slot
   - Verified IT mode firmware (P20)
   - Critical: Not RAID mode (conflicts with ZFS)

2. **Cable Management**
   - SFF-8087 cables: HBA → Drives
   - Integrated SATA power: No external PSU connections needed
   - Result: Messy but functional

3. **Drive Installation**
   - 10 drives attempted
   - 1 DOA (showed 0 B capacity)
   - Proceeded with 7 drives + 2 spares

4. **Boot Drive**
   - 128GB NVMe dedicated to TrueNAS
   - No dual-boot, no shared partitions

---

### Software Configuration

**TrueNAS SCALE Installation**
- USB installer → 128GB NVMe
- Network configuration via console (static IP: 192.168.0.120)
- Web interface access: http://192.168.0.120

**ZFS Pool Creation**
- Pool name: `Storage_Pool`
- Layout: RAID-Z2
- Width: 7 drives
- VDEVs: 1
- Result: 5.46TB usable

**SMB Sharing Setup**
- Dataset: `Shared`
- SMB enabled for cross-platform access
- Works on: Windows, Mac, Linux, Android

**Immich Installation** (Self-hosted Google Photos)
- One-click install via TrueNAS apps
- Access: http://192.168.0.120:2283
- Imported 15-20GB Google Takeout archives

---

### Troubleshooting Hell (The Real Story)

**Issue 1: No Display on Boot**
- **Symptom:** Power on, fans spin, blank screen
- **Cause:** RAM not fully seated
- **Fix:** Reseated all RAM sticks, started with one in slot A2
- **Time lost:** 2 hours of panic

**Issue 2: Dead Drive Detection**
- **Symptom:** Drive `sda` showed 0 B capacity
- **Diagnosis:** Matched serial number to physical label
- **Attempted fixes:** Reseated drive, different cable position, different HBA port
- **Resolution:** Drive toast, proceeded with 7 drives

**Issue 3: Console Network Configuration Bug**
- **Symptom:** Static IP fields not appearing in console wizard
- **Workaround:** Used DHCP initially, set static IP in web GUI
- **Lesson:** Don't fight ncurses interfaces

**Issue 4: Molex to SATA Adapter Failures**
- **Initial plan:** Use cheap Molex adapters
- **Reality:** Loose connections, overheating concerns
- **Solution:** Replaced with SFF-8087 cables with integrated SATA power
- **Cost delta:** +$20, worth every penny

---

### Performance & Results

**Power Consumption**
- System + 7 drives: ~140W continuous
- Idle: ~130W
- During scrub: ~160W

**Storage Performance**
- Sequential read: ~600-700 MB/s (limited by 1GbE network)
- 10K RPM enterprise drives: Low latency
- ZFS compression: Effective ~10-15% space savings

**Reliability Features**
- **Monthly scrubs:** Automated data integrity checks
- **Weekly SMART tests:** Drive health monitoring  
- **Hourly snapshots:** 7-day retention for accidental deletion recovery
- **RAID-Z2:** Survives any 2 simultaneous drive failures

---

### What I Learned

**Hardware Lessons**

1. **CPU generation matters for RAM utilization**
   - 6th-8th gen Intel: DDR4-2400 max (67% of DDR4-3600)
   - 11th gen Intel: DDR4-3200 max (89% of DDR4-3600)
   - **Cost difference:** $30-50 for proper matching

2. **IT mode is non-negotiable for ZFS**
   - RAID mode on HBA fights with ZFS software RAID
   - Pre-flashed cards worth extra $5
   - P20 firmware is stable

3. **Cable quality saves headaches**
   - Integrated SATA power cables: Professional solution
   - Molex adapters: Fire hazard waiting to happen
   - **Cost:** $30 vs endless troubleshooting

4. **Expect DOA enterprise pulls**
   - 1 out of 10 drives failed: Not bad luck, expected
   - Still cheaper than buying new
   - **Economics:** $5/drive vs $80/drive new

**Software Lessons**

1. **Console is for network only**
   - Configure static IP
   - Everything else: Use web GUI

2. **RAID-Z2 minimum for data safety**
   - Single parity (RAID-Z1): Playing with fire
   - Dual parity: Survives 2 drive failures
   - **Trade-off:** ~27% capacity overhead vs peace of mind

3. **Dedicated NAS = Happy NAS**
   - No dual-boot
   - No shared gaming PC
   - One purpose: Storage

---

### Would I Do It Again?

**Absolutely yes.**

**The Math:**
- Built for: $320 ($285 with 7 drives)
- Synology equivalent: $800-1000
- **Savings:** $500-700

**The Value:**
- Full control over hardware
- Upgrade path (add 8th drive, 10GbE card)
- Learning experience: Invaluable
- Self-hosted Immich: Priceless

**The Reality:**
- 4 hours build time (including troubleshooting)
- 1 month parts sourcing (patience required)
- Runs 24/7, zero issues post-setup

---

### For Others Considering This

**You Should Build If:**
- Comfortable with CLI and troubleshooting
- Have time for parts sourcing
- Want full control over hardware
- Value learning over convenience
- Budget-conscious but not cheap

**Buy Pre-Built If:**
- Need plug-and-play solution
- Time is more valuable than money
- Want official warranty support
- Zero interest in tinkering

---

## Photo Checklist (To Capture)

When processing photos for teardown-cafe:

- [ ] Complete system exterior (hero image candidate)
- [ ] LSI 9207-8i HBA card close-up
- [ ] SFF-8087 to SATA cable connections
- [ ] Drive bay showing 7-drive configuration
- [ ] Cable management (the honest truth)
- [ ] TrueNAS web interface - pool status
- [ ] SMART data showing drive health
- [ ] Power consumption meter reading
- [ ] Immich interface showing photo library

**Difficulty Rating:** Medium 🟡
- Multiple specialty components (HBA, SAS cables)
- Some troubleshooting required
- Enterprise hardware learning curve
- Moderate risk management (power, cooling)
- Example: Between monitor teardown and laptop repair

---

## Tags for Obsidian Cross-Reference
#truenas #nas-build #enterprise-storage #sas-drives #zfs #raidz2 #lsi-hba #budget-build #self-hosted #immich #teardown-cafe

---

## Related Resources

**Internal Notes:**
- [[TrueNAS Build Guide]] - Full technical documentation
- [[Budget SAS Drive NAS Build Guide]] - Original planning conversation
- [[Teardown Cafe - Documentation Index]] - Project overview

**External Links:**
- TrueNAS SCALE Documentation: https://docs.truenas.com
- Immich Self-Hosted Photos: https://immich.app/docs  
- ServeTheHome Forums: Enterprise hardware community
- r/TrueNAS: Community troubleshooting

---

**Build Date:** September 28, 2025  
**Documentation Date:** October 19, 2025  
**Status:** Running stable, 5.46TB operational, zero downtime  
**Total Cost:** $285-320 depending on drive count  
**Time Investment:** 1 month sourcing + 4 hours build + 2 hours troubleshooting  

*This entry captures the complete journey from "$50 of mysterious SAS drives" to "legitimate enterprise NAS" - including all the mistakes, fixes, and lessons learned along the way.*

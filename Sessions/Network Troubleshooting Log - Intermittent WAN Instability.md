# Network Troubleshooting Log: Intermittent WAN Instability

#troubleshooting #network #homelab #dns #coaxial #physical-layer #diagnostic

> **Related**: [[🗺️ Knowledge Base - Main Index]] | **Timeframe**: January 20-22, 2026 | **Status**: 🔄 Ongoing (Escalated to Logic Layer)

---

## Executive Summary

The homelab experienced intermittent network "blackouts" lasting seconds to minutes where internet connectivity would drop to zero across all devices—phones, computers, everything simultaneously. Root cause of the initial issue was identified as physical damage to the coaxial cable from external compression and twisting, allowing electromagnetic interference to corrupt the signal at the modem. The physical layer was successfully repaired by straightening the cable and relocating furniture. However, 24 hours after the fix, a secondary issue emerged: logical connectivity drops persist despite clean physical layer signals, indicating an OS-level or configuration-layer problem.

---

## Part 1: Initial Investigation (January 20-21)

### Symptoms & Initial Observations

The issue manifested as follows:

**Connectivity Behavior**
- Intermittent stalling events where high-speed internet would randomly drop to zero (not slow—completely unresponsive)
- Duration: Drops lasted anywhere from 5-30 seconds, then connectivity would spontaneously return
- Frequency: Occurred multiple times per hour
- Pattern: Happened regardless of time of day or load on the network

**Scope of Impact**
- Global across the network: All devices experienced the outages simultaneously
- Wireless and wired devices equally affected (ruled out Wi-Fi-specific issue)
- ISP status page showed no node outages or warnings
- Modem was online and registered with the ISP throughout the events

**Initial Troubleshooting Attempts**
- Power-cycling the modem: Provided temporary relief (minutes) or no improvement
- Rebooting the router: No effect
- Checking ISP account status: No service alerts, no line issues reported by ISP
- Restarting individual devices: Did not prevent future outages
- Switching between wired and wireless: Both were equally affected

The fact that all devices dropped simultaneously indicated a problem with the modem's connection to the ISP, not the internal network.

---

### Technical Investigation (Phase 1)

#### Modem Signal Analysis (DOCSIS WAN)

**Power Levels**
- **Measured**: +7 dBmV to +10.8 dBmV (downstream)
- **Normal Range**: -15 dBmV to +15 dBmV is acceptable; 0 dBmV is ideal
- **Assessment**: Slightly "hot" but within acceptable range

**Signal-to-Noise Ratio (SNR)**
- **Measured**: 38–39 dB
- **Healthy Threshold**: >30 dB
- **Assessment**: SNR was healthy, indicating the signal itself wasn't inherently noisy

**Uncorrectable Codewords** (The smoking gun)
- **Measured**: 1,145+ uncorrectable errors on specific DOCSIS channels
- **Normal**: Close to zero over a 24-hour period
- **Assessment**: Extremely high. This indicated data packets were arriving so corrupted that the modem couldn't recover them

#### DNS Sinkhole Diagnostics (Pi-hole)

**DNS Query Failures**
- Logs showed `Network unreachable` errors when attempting to forward queries upstream
- This confirmed the Pi-hole itself detected WAN connectivity loss in real-time
- Errors directly corresponded to the modem's signal drop periods

**Query Queue Buildup**
- When WAN connectivity dropped, DNS queries accumulated in the Pi-hole's queue
- Peak backlog: 150+ concurrent DNS queries waiting for resolution
- CPU load spiked to handle the queueing and retry logic

**Timeline Correlation**
- Query error timestamps matched the ISP's DOCSIS channel errors
- Two-point confirmation from independent systems (modem + Pi-hole) proved the WAN link was dropping

#### Physical Inspection

With diagnostics pointing to a physical layer problem, the coaxial cable was inspected.

**What Was Found**
- The main coaxial line was compressed under heavy furniture
- Both termination points (at the wall and at the modem) showed severe twisting and kinking
- The cable had visible deformation where it bent around the furniture corner

---

### Root Cause Analysis (Physical Layer)

**Primary Cause: Physical Layer Damage (Coaxial Cable)**

Coaxial cables are engineered with a specific geometry: copper core conductor surrounded by dielectric insulation, wrapped in a conductive shield, with an outer jacket. This geometry confines the signal and blocks external electromagnetic noise.

When compressed or twisted, this geometry is distorted. The shield no longer provides consistent coverage, allowing external electromagnetic noise to leak into the cable and corrupt the signal.

**Why This Caused the Specific Symptoms**

- **Signal Ingress**: The compressed/twisted sections allowed external EM interference to enter the cable
- **Noise on Signal**: The modem received corrupted data packets when noise interference was strongest
- **Uncorrectable Errors**: The modem's forward error correction (FEC) exceeded its recovery capability
- **Total Connectivity Loss**: When uncorrectable codewords exceed a threshold, the modem drops the connection entirely

---

### Resolution & Verification (January 21)

#### Corrective Action

1. **Cable Straightening**: The coaxial cable was carefully straightened and repositioned
2. **Furniture Relocation**: The furniture compressing the cable was moved to create clear space
3. **Cable Routing**: The cable was rerouted to avoid any future compression points

#### Verification Results

**Before Fix**
- Uncorrectable Codewords: 1,145+
- Connectivity: Intermittent drops every few minutes
- DNS errors: Continuous `Network unreachable` during outages

**After Fix**
- Uncorrectable Codewords: 0 (new errors post-correction)
- Connectivity: Stable, continuous uptime
- DNS errors: None

---

## Part 2: Follow-Up Investigation (January 22)

### New Observation

**Date**: January 22, 2026

After the physical cable repair, the intermittent outages appeared resolved. However, approximately 24 hours after the fix, a new issue emerged: **logical connectivity drops persisting despite clean physical layer signals**.

The modem signal parameters remain perfect (Uncorrectable Codewords: 0), yet the network experiences intermittent dropouts at the application layer. This indicates the problem has shifted from physical layer to logical layer (routing, configuration, or protocol negotiation).

### Updated Evidence

**Docker0 Interface TX Drops (Infinity%)**
- The virtual networking interface `docker0` is showing 100% TX (transmit) packet loss
- This suggests the Docker network bridge is dropping all outgoing traffic
- Infinity% indicates the metric is undefined or the interface is completely unable to transmit

**Resource Temporarily Unavailable Errors**
- System logs show `ENOBUFS` or "Resource temporarily unavailable" errors
- OS-level indication that a resource (network path, file descriptor, or buffer) is temporarily unable to fulfill a request
- Often indicates a closed or unresponsive network path
- These errors come from the kernel when it cannot allocate memory for packet buffers

**Modem Uncorrectables: 0**
- No new signal errors since the physical fix
- The modem itself is healthy and stable
- This definitively proves the issue is NOT a physical layer problem
- Signal quality: Clean and stable

### Root Cause Hypothesis

The evidence points to two possible causes at the logical layer:

**Possibility 1: Damaged Cable Core (Secondary Effect)**
- Although the cable is no longer crushed, the internal copper core may have been compromised by the kinking
- The outer shielding is fine (no ingress noise), but the core itself may be fractured internally
- This would allow power/connectivity to flow intermittently, appearing as logic-layer failures
- The cable could have internal micro-fractures that conduct at some angles but fail at others
- Physical inspection would require: continuity testing on the cable core with a multimeter

**Possibility 2: Router or Docker Configuration Error**
- The modem fix may have revealed a pre-existing configuration issue in the router or Docker networking setup
- The docker0 bridge may be misconfigured or stuck in a failed state
- The router may have incompatible settings now that the signal is clean
- Software diagnosis: checking router logs and Docker networking configuration

### Diagnostic Next Steps

**Immediate Actions (Priority Order)**

1. **Cable Continuity Test**: Use a multimeter to test the coaxial cable's internal conductor for continuity
   - Set multimeter to continuity/resistance mode
   - Test between the center conductor at each end
   - Expected: 0 ohms (perfect continuity)
   - If resistance is high or infinite: Cable core is fractured

2. **Docker Network Restart**: Restart the Docker daemon and monitor docker0
   ```bash
   systemctl restart docker
   # Then monitor: watch -n 1 'ip -s link show docker0'
   ```

3. **Router Logs**: Check for errors during the drop periods
   ```bash
   # SSH to router and check syslog
   tail -f /var/log/syslog | grep -i "error\|fail\|drop"
   ```

4. **Ping Continuous**: Run a continuous ping to an external IP
   ```bash
   ping -c 60 8.8.8.8 | tee ping-output.txt
   # Check for packet loss patterns during drops
   ```

**Secondary Actions**

1. If cable continuity fails: **Replace the coaxial cable entirely**
2. If Docker restart fixes the issue: Document the configuration that caused it
3. If router logs show errors: Identify the specific error and research fixes
4. If ping shows packet loss at OS level: Problem is confirmed to be logical layer (not physical)

### Key Insight

Physical layer diagnostics proved the modem connection is healthy. The modem's zero uncorrectables confirms the signal path is clean. Any remaining issues are internal to the network—OS, routing, or device configuration.

**This is valuable information.** Many troubleshooters would have blamed the modem or ISP again. Instead, we know the ISP link is fine.

---

## Prevention & Long-Term Management

### Monitoring

- **Weekly Signal Check**: Monitor the modem's "Uncorrectables" column for anomalies
- **Docker Health Check**: Monitor docker0 TX/RX stats and set alerts if TX errors exceed 0
- **System Logs**: Regularly review `dmesg` and syslog for ENOBUFS or network errors
- **Threshold Alert**: If uncorrectables exceed 100 in a 24-hour period, investigate immediately

### Physical Protection

- **Clear Space**: Ensure the coaxial cable has at least 6 inches of clear space in all directions
- **Right-Angle Adapters**: In tight spaces, use right-angle coaxial connectors to prevent sharp bends
- **Cable Management**: Use cable ties or conduit to keep the line organized
- **Furniture Placement**: Avoid routing the cable under heavy furniture or high-traffic areas
- **Cable Inspection**: Periodically visually inspect for signs of kinking or damage

---

## Technical Deep Dive: Key Concepts

### Uncorrectable Codewords

In DOCSIS systems, data is transmitted in organized "codewords"—discrete packets of information. The modem uses forward error correction (FEC) to detect and fix small errors caused by noise. If errors exceed FEC's recovery capability, the codeword is marked as "uncorrectable" and discarded.

**Why This Matters**: Uncorrectable codewords are a leading indicator of cable problems. They appear before a modem loses connection entirely, providing early detection of physical layer issues.

### Signal Ingress

Signal ingress occurs when external electromagnetic noise enters a cable through compromised shielding. Sources include:
- Power lines running parallel to coaxial cables
- Radio transmitters (cell towers, Wi-Fi access points)
- Electrical equipment (motors, power supplies)
- Lightning and electrical storms

A healthy coaxial cable prevents this noise from entering. But if shielding is compromised (crushing, twisting, damaged connectors, moisture intrusion), noise can leak in and corrupt the signal.

**Why This Matters**: Understanding signal ingress explains why increasing power levels won't fix the problem—it's about signal quality being corrupted by noise, not signal strength.

### OFDM (Orthogonal Frequency Division Multiplexing)

OFDM is used for high-speed downstream data transmission (DOCSIS 3.1 and newer systems). It spreads the signal across many sub-carriers at different frequencies, allowing much higher data rates.

The tradeoff is sensitivity to noise on any sub-carrier. If one sub-carrier is corrupted by noise, that portion of the data becomes unrecoverable. This is why the modem logs flagged uncorrectable errors on "OFDM blocks."

**Why This Matters**: OFDM-based systems are more sensitive to physical layer problems. A cable problem that would have caused minor slowdowns on older systems causes complete signal loss on OFDM.

---

## Lessons Learned

1. **Physical Layer Debugging First**: When all devices on the network fail simultaneously, the problem is almost always the modem's connection to the ISP, not the internal network.

2. **Modem Diagnostics Are Critical**: The modem's signal page is one of the most useful troubleshooting tools available. Uncorrectable codewords are early warning signs.

3. **Correlation Confirms Root Cause**: Cross-checking modem logs with Pi-hole logs (two independent systems) provided confidence that the problem was real and widespread.

4. **Coaxial Cable Management**: Coaxial cables must be handled carefully, routed properly, and protected from compression. A $50 replacement cable beats hours of troubleshooting.

5. **Preventive Monitoring**: Checking signal stats weekly would have caught this issue before it became frequent. Uncorrectable codewords tell you something is wrong before you lose connectivity entirely.

6. **Physical Fixes Don't Guarantee Complete Resolution**: Just because the physical layer is clean doesn't mean all problems are solved. Secondary issues at higher layers may be revealed only after the physical layer is repaired.

7. **Layered Troubleshooting**: Problems often exist at multiple layers. When the obvious culprit is fixed, monitor carefully for symptoms at higher layers (logical, application, configuration).

---

## Current Investigation Status

**Physical Layer**: ✅ Resolved (Uncorrectables: 0, cable straightened and protected)  
**Logical Layer**: 🔄 Investigating (docker0 TX drops, ENOBUFS errors)  
**Next Action**: Cable continuity test + Docker restart  
**Updated**: January 22, 2026

---

**Incident Timeline**
- Jan 20-21: Physical layer problem identified and resolved
- Jan 22: Secondary logic-layer issue discovered
- Jan 22+: Ongoing investigation into root cause of persistent drops

**Key Takeaway**: Physical problems require physical solutions, but fixing the physical layer may reveal configuration or hardware issues that were masked by the initial failure. Troubleshooting doesn't always end with one fix.

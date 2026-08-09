---
created: 2026-04-01
modified: 2026-04-01
tags:
  - android
  - hardware
  - troubleshooting
  - flashing
  - EDL
  - qualcomm
  - LG
  - LGUP
  - ADB
  - DAC
  - repair
privacy_scan: not_scanned
published_to_garden: false
visibility: private
---

# Troubleshooting Report: The Great LG G8 ThinQ (G820TM) Resurrection
**Tags:** #android #hardware #troubleshooting #flashing #EDL #qualcomm #LG #LGUP #ADB #DAC #repair
**Date:** 2026-04-01

> 📌 **Image Setup:** All screenshots should be saved to your vault's `images/` folder using the filenames referenced below. You can drag them directly into Obsidian from this conversation or from your Downloads folder.

---

## 0. Device Profile

| Property | Value |
|---|---|
| **Model** | LG G8 ThinQ — `LM-G820TM` (T-Mobile USA) |
| **Chip** | Qualcomm Snapdragon 855 (SM8150) |
| **DAC** | ESS SABRE ES9218P (Quad DAC) |
| **Storage Type** | UFS 2.1 (multi-LUN configuration) |
| **OS Target** | Android 10 — T-Mobile stock (`G820TM40a`) |
| **Wrongly Flashed Firmware** | `G850UM` — Canadian/International Unlocked variant |

---

## 1. The Incident — What Broke and Why

### The Goal
The LG G8 ThinQ has a hardware Quad DAC (ESS SABRE ES9218P) that's partially gimped on T-Mobile's stock firmware. The aim was to cross-flash the International/Canadian `G850UM` firmware to unlock the full audio pipeline — specifically the "Hi-Fi Quad DAC" menu that's hidden behind carrier restrictions in settings.

### The Cross-Flash
A **cross-flash** means installing firmware from a completely different carrier variant onto your phone's hardware. The process technically worked — the phone booted. But "booting" doesn't mean "working."

> **The Root Cause:** The `G850UM` kernel shipped hardware drivers tuned for a *different display panel assembly* than the `G820TM` motherboard actually uses. The kernel started fine, recognized the screen for output (so you could *see* things), but the touch digitizer controller was completely unknown to it.

### The Symptoms
- Screen: ✅ Displays perfectly
- Touchscreen: ❌ 100% unresponsive — completely dead
- Boot error on every startup: `"Current version is not available for user. Can't find matched carrier. Check NT-Code: 0"`

The NT-Code is basically the phone's carrier ID badge. The `G850UM` firmware had the wrong badge for T-Mobile hardware. The phone booted but was perpetually confused about who it was.

### The Smoking Gun — Fastboot Mode

This screenshot from Fastboot Mode shows the identity mismatch in black and white. The hardware is a G820TM (T-Mobile), but every field reports it as a G850UM. Note `DEVICE STATE – locked` in red — this rules out standard fastboot flashing as a recovery path.

![[LG-G8-fastboot-wrong-identity.png]]

> `PRODUCT_NAME – LM-G850UM` on T-Mobile hardware. `SERIAL NUMBER` also reflects the G850UM identity. This is the mismatched carrier structure LGUP's REFURBISH mode would later have to overwrite from scratch.

---

## 2. Act I — The Great Wall of Windows

Standard repair tools on Windows 11 created two major roadblocks before we could even attempt a fix.

### Problem A: Wrong Driver Identity

When the phone was put into **EDL Mode** and plugged into a Windows 11 PC, Windows tried to load a **Quectel modem driver** instead of the correct Qualcomm diagnostic driver, causing massive read/write errors.

> **Plain English:** Windows thought the phone was a cellular modem (like the chip in a laptop's SIM slot) instead of a phone in recovery mode.

**The Fix:** Force-reboot Windows into **Disable Driver Signature Enforcement** mode.

1. `Settings → Recovery → Advanced Startup → Restart Now`
2. Navigate: `Troubleshoot → Advanced Options → Startup Settings → Restart`
3. On the boot screen, press **F7** — "Disable driver signature enforcement"
4. Manually install the Qualcomm 9008 driver via Device Manager → Update Driver → Browse

> ⚠️ This setting resets on every reboot. Complete the driver install in the same boot session.

---

### Problem B: QFIL Failing Despite Correct Driver

Even after the driver was correctly installed (Device Manager showed `Qualcomm HS-USB QDLoader 9008 (COM7)` — confirming the phone was visible), QFIL still couldn't get through the Sahara handshake. The programmer path `C:\Flash\prog_ufs_firehose_sm8150_lge.elf` was correct for the G8's SM8150 chip, but the tool kept erroring out.

![[LG-G8-qfil-sahara-failure.png]]

> **What you're seeing:** Device Manager (left) confirms the phone is on COM7 and correctly identified. QFIL (right) shows the firehose `.elf` is loaded. But the Status window at the bottom shows: `ERROR: Sahara protocol error` → `Uploading Image using Sahara protocol failed` → `Download Fail: Sahara Fail: Process fail`. QFIL couldn't push the firehose loader to the chip even with the right driver. This is partly a USB 3.0 issue (see below) and partly QFIL's poor error recovery on Windows 11.

This is why we abandoned QFIL entirely in favor of the Python `edl` tool.

---

### Problem C: USB 3.0 Timing Out

The Qualcomm **Sahara Protocol** — the low-level handshake that lets a PC talk to a Snapdragon chip in EDL mode — is extremely sensitive to USB timing. USB 3.0 ports (the blue ones) negotiate too aggressively and the connection times out before data can transfer.

![[LG-G8-edl-usb3-timeout-error.png]]

> **What you're seeing:** The `edl` tool repeating `[Errno 10060] Operation timed out` over and over. The Sahara handshake gets partially started (`connect:0x80`, then `TX: <?xml...`) but keeps dropping before the firehose loader can be uploaded. Ends with `main – Unknown mode. Aborting.` The fix was simply switching to a rear-panel **USB 2.0** port.

> **Plain English:** USB 3.0 is like a hyper-fast conveyor belt — the phone's emergency mode can't load stuff onto it fast enough. USB 2.0 is slower and dumber, which is exactly what Sahara needs.

---

## 3. Act II — The Bluetooth MacGyver Maneuver

With the touchscreen dead, **ADB (Android Debug Bridge)** was locked out. ADB requires you to physically tap "Allow USB Debugging" on screen the first time. No tap = no ADB = no software repair path.

### The Workaround Chain

```
USB-C Hub → Phone
              ├── Wired USB Mouse   (navigate Settings → Bluetooth)
              └── Wired USB Keyboard (optional, for typing)
              
Then: Hub out → PC cable in → Bluetooth mouse clicks "Allow"
```

1. **Connected a USB-C hub** to the phone's charging port
2. Used a **wired USB mouse** to navigate `Settings → Connected Devices → Bluetooth`
3. **Paired a Bluetooth mouse** via the wired mouse
4. **Disconnected the hub** entirely, plugged the phone directly into the PC
5. ADB prompted "Allow USB Debugging?" on-screen
6. Used the **Bluetooth mouse** to click "Allow" — no touchscreen required

> ✅ **Result:** ADB access established without touching the display.

> ⚠️ **Why this works:** Android permits Bluetooth peripherals to interact with permission dialogs at the system UI level. If Bluetooth had been off and never paired, this path would be completely closed.

---

## 4. Act III — KDZ Extraction and the Python EDL Pivot

### Step 1: Cracking Open the KDZ

Before anything could be written to the phone, we needed the raw `laf.img` file from inside the T-Mobile firmware. LG's `.kdz` files are proprietary containers — you can't just open them like a zip. KDZTools (a community-built extraction utility from 2020) was used to unpack it.

![[LG-G8-kdztools-extraction.png]]

> **What you're seeing:** KDZTools working through the `G820TM10q_00_TMO_US_OP_0110.kdz` (~3.9 GB). Left panel shows the source files. Right panel shows the extraction log: individual partition images being extracted and cleaned up, ending with `[Script INFO] Finished!`. Inside the resulting folder lives `laf.img` — the rescue partition we needed.

> **The KDZ Format explained:** Think of it as a Russian nesting doll. The outer `.kdz` container holds a `.dz` file, which itself holds all the individual partition `.img` files (system, boot, laf, modem, etc.). KDZTools automates cracking both layers open.

---

### Step 2: Understanding the Phone's Memory Layout

The LG G8 uses **UFS (Universal Flash Storage)**, which organizes storage into multiple **LUNs (Logical Unit Numbers)** — essentially separate logical drives on a single chip. Knowing this matters because `laf` (the recovery we needed to restore) lives in a specific LUN.

The `edl` tool's `printgpt` command dumped the full partition table so we could verify exactly where `laf_a` and `laf_b` live before writing anything:

![[LG-G8-gpt-partition-table-laf.png]]

> **What you're seeing:** The raw GPT (GUID Partition Table) — the "map" of the phone's storage. Each row is a partition with its name, memory address offset, size, and UUID. `laf_a` and `laf_b` are visible near the top. `abl`, `xbl`, `vbmeta`, `boot`, `modem` — every critical low-level partition is listed here. Scrolling this table confirmed LAF's location before writing.

| LUN | Key Contents |
|---|---|
| LUN 0 | Main Android system, userdata, boot |
| LUN 1–3 | Various system partitions |
| **LUN 4** | **`laf_a/laf_b` (Download Mode), `abl`, `xbl` bootloaders** |
| LUN 5 | IMEI / modem identity (`modemst1`, `modemst2`, `fsg`, `fsc`, `ftm`) |

---

### Step 3: The LAF Injection

**LAF (LG Activation Firmware)** is LG's proprietary "Download Mode" — a small rescue environment that LGUP uses to push firmware. Because the `G850UM` cross-flash had overwritten the `G820TM`'s `laf` partition with the wrong version, Download Mode was broken. LGUP couldn't connect. The fix: write the correct `laf.img` directly via `edl`, bypassing the broken OS entirely.

```bash
# Write correct T-Mobile laf.img to LUN 4
python edl.py w laf laf.img --memory=ufs --lun=4

# Verify the write
python edl.py r laf laf_verify.bin --memory=ufs --lun=4
```

![[LG-G8-edl-laf-write-success.png]]

> **What you're seeing:** The top portion is the raw hex data of `laf.img` being streamed to the phone — those are the actual bytes of the partition being transferred. At the bottom: `Progress: 100.0% Complete` and `Wrote C:\Flash\laf.img to sector 108606`. That's confirmation the write landed.
>
> **The `"Operation not supported or unimplemented on this platform"` message** at the very end is a red herring — it's a known Windows/pyusb quirk where the `edl` tool tries to issue a USB device reset command after the write completes, and WinUSB on Windows doesn't support that specific USB control transfer. The write itself was 100% successful. This trips up a lot of people into thinking the operation failed.

> ⚠️ **Critical:** You must use a `laf.img` from a **T-Mobile G820TM** KDZ specifically. Any other variant will put you back in the same broken state.

---

## 5. Act IV — LGUP REFURBISH (The Final Kill)

With `laf` restored, the phone could enter LG's **Download Mode** — the prerequisite for LGUP to function. Download Mode is LG's proprietary recovery interface, completely separate from EDL.

### The Phone Receiving Firmware

![[LG-G8-download-mode-tmous-restore.png]]

> **What you're seeing:** The G8's screen during the LGUP flash. The USB sync icon confirms the cable connection is active. The progress bar is moving. Most importantly — the bottom of the screen shows `533A B20 TMO_US` and `Official / E / L / R0 / id : 3(TMO_US)`. The `TMO_US` identifier is the T-Mobile carrier flag being written. At this moment, the phone was accepting its correct identity for the first time since the bad cross-flash.

---

### Why REFURBISH and Not UPGRADE?

| LGUP Mode | What It Does | Our Case |
|---|---|---|
| **UPGRADE** | Updates OS, preserves user data | ❌ Won't fix carrier identity corruption |
| **REFURBISH** | Full wipe — rewrites ALL carrier partitions from scratch | ✅ Correct choice |
| **PARTITION DL** | Flashes individual partitions | ❌ Not supported for G8 cross-flash correction |
| **CHIP ERASE** | Nukes everything including IMEI/EFS | ⛔ Never use without a full NV backup |

> **Plain English:** UPGRADE is like repainting a house with the wrong floor plan. REFURBISH tears it down and rebuilds from the correct blueprints. We needed new blueprints.

---

### LGUP in Action — The Identity Crisis Visible in the Tool

![[LG-G8-LGUP-G850UM-identity-crisis.png]]

> **What you're seeing:** LGUP 1.16.0.3 (Lab Version) mid-flash at 11%, sending `system_b 59/181 lun 0`. The KDZ loaded in the file path is correctly the T-Mobile file (`G820TM10q_00_TMO_US_OP_0110.kdz`). But look at the **title bar**: `LGUP[LM-G850UM – G8 ThinQ]`. LGUP is detecting the phone's *current* (wrong) identity as G850UM, while simultaneously flashing the correct T-Mobile firmware over it. This is the transition point — the old identity being overwritten in real time. DLL Version is `2.1.0.52`, which is above the minimum `1.9.39.7` required for G8/SM8150 devices.

### The Process
1. Opened **LGUP 1.16** (patched version — the `LGUP_UI-Fixer.bat` patch is required for the G8 on Windows 11)
2. Loaded KDZ: `G820TM10q_00_TMO_US_OP_0110.kdz`
3. Selected **REFURBISH**
4. Confirmed DLL version was ≥ `1.9.39.7`
5. Hit Start — progress bar climbed to 100%
6. Phone rebooted automatically

> ✅ **Result:** Touchscreen functional. NT-Code error gone. T-Mobile identity fully restored.

---

## 6. The Payoff — Quad DAC Properly Unlocked

With the phone restored to stable T-Mobile firmware:

- **Hardware:** KZ ZS10 Pro (5-driver hybrid IEMs — 1DD + 4BA) into the 3.5mm jack
- **DAC Chip:** ESS SABRE ES9218P — fully recognized by the OS
- **Enabled:** `Settings → Sound → Hi-Fi Quad DAC` toggle appeared correctly post-restore

> The G8's Quad DAC achieves a signal-to-noise ratio of ~130dB with a noise floor that Bluetooth codecs (even LDAC at 990kbps) physically cannot match due to the compression overhead inherent in wireless audio transmission. The 3.5mm analog output is a direct path from DAC to headphone driver — no re-encoding, no wireless stack.

---

## 7. Technical Glossary

| Term | Plain English |
|---|---|
| **EDL (Emergency Download Mode)** | The most fundamental state a Snapdragon phone can enter. The CPU is awake but no OS is running — the processor is sitting in a waiting room, ready to accept instructions before the phone's "personality" loads. |
| **Sahara Protocol** | The language Qualcomm chips speak in EDL mode. It's the initial handshake. If Sahara fails, nothing else can happen. |
| **Firehose** | The second protocol layer after Sahara. The actual worker that reads/writes storage. Requires a device-specific signed `.elf` loader file. |
| **LAF (LG Activation Firmware)** | LG's own "Download Mode" — a small rescue environment in its own partition. LGUP talks through this. If LAF is corrupted, LGUP can't connect at all. |
| **KDZ** | LG's proprietary firmware container. Think of it as a zip-of-a-zip holding the entire Android OS. Multi-gigabyte, carrier/region-specific. |
| **GPT (GUID Partition Table)** | The "map" of the phone's storage. Every partition has an entry with its name, start address, and size. Cross-flashing can corrupt or replace this map. |
| **LUN (Logical Unit Number)** | A subdivision of UFS storage. The G8 has multiple LUNs that function as logically separate drives on a single physical chip. |
| **NT-Code** | LG's "Network Token Code" — the carrier identity stored in the `ftm` partition. After a cross-flash, this won't match the running firmware, causing a boot warning on every startup. |
| **Cross-Flash** | Installing firmware from a different carrier variant onto your hardware. Can unlock features, but risks driver/hardware mismatches like the one in this report. |
| **A/B Slot** | Android's dual-partition scheme. The phone keeps two copies of critical partitions (`_a` and `_b`). One is active, one is a fallback. The G8 uses this — hence `laf_a` and `laf_b` in the GPT. |
| **ADB (Android Debug Bridge)** | A command-line tool for PC-to-Android communication. Requires USB Debugging enabled on the device — which required the Bluetooth mouse workaround here. |

---

## 8. What Didn't Work (Dead Ends Log)

- **QFIL on Windows 11** — Even with the correct Qualcomm 9008 driver installed and the right SM8150 firehose `.elf`, QFIL kept failing at the Sahara handshake. The tool has poor error recovery and no meaningful diagnostics on failure.
- **USB 3.0 ports** — Sahara handshake timed out consistently (`[Errno 10060]`). Wasted ~2 hours on this before switching to rear USB 2.0. Visually identical to a driver problem, which made it hard to diagnose.
- **LGUP UPGRADE mode** — Would not accept the KDZ due to the carrier mismatch. Errored at device handshake with `Error 0x5A03 / Unknown Process Type`.
- **Factory Reset via Recovery** — Recovery partition was also overwritten by the `G850UM` flash. It was the wrong recovery for the hardware. Even navigable (touchscreen was dead anyway), it would've put the phone in the same broken state.
- **Attempting ADB without the Bluetooth trick** — Standard USB debugging authorization requires a physical tap. With a dead touchscreen and no prior authorization saved, this was a hard wall until the hub+BT workaround.

---

## 9. Key Takeaways

1. **Cross-flashing is carrier AND hardware-specific.** "Same chip, different model" isn't safe. Display drivers, touch digitizer firmware, and modem partitions are all bundled per-variant.
2. **EDL is your last resort, but it's a real one.** As long as the Snapdragon SoC is alive, you can recover almost anything. The phone is only a "hard brick" if the SoC itself is physically dead.
3. **USB port selection is not trivial.** Sahara Protocol failures on USB 3.0 look identical to wrong drivers. Don't spend hours on driver fixes if you haven't tried USB 2.0 yet.
4. **Bluetooth peripherals can save a dead touchscreen.** Any Android phone with a working USB-C port and a previously-paired BT device can be navigated without touching the glass.
5. **LGUP REFURBISH is the correct tool for carrier identity corruption.** UPGRADE won't fix a mismatched carrier structure. The nuclear option is the right option here.
6. **The `"Operation not supported"` message from `edl` on Windows is a false alarm.** If the write shows 100% complete and reports the sector it wrote to, the operation succeeded. The error is a Windows/pyusb USB reset limitation, not a write failure.

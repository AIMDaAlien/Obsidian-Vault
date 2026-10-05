---
title: BigRig TUF X670E BIOS Configuration
tags: [homelab]
created: 2025-01-01
published: true
---

# TUF GAMING X670E-PLUS WIFI + Ryzen 9 7950X — BIOS configuration for local AI inference

Target: Ryzen 9 7950X (Zen 4, 2×CCD/16C/32T, 170W), 2×32GB DDR5 (currently stuck at
**4800**, should be 6000), RX 9060 XT 16GB (PCIe 5.0 slot), RTX 3060 12GB (PCIe 4.0 slot).
Boot OS: Omarchy (Arch-based, Limine/UKI, `nvidia-open-dkms`).

BIOS target version: **4004** (2026/09/21, AGESA ComboAM5 PI 1.3.0.1d).
Everything below is verified against strings extracted from the actual 4004 BIOS image, not
just the 2023 manual — ASUS's published manual is stale in several places and those are flagged.

---

## 0. Four things that will waste your time if you don't know them first

1. **The overclock tab is `Ai Tweaker`, not "Tweaker".** Top bar: `My Favorites | Main | Ai
   Tweaker | Advanced | Monitor | Boot | Tool | Exit`.
2. **This board has a ReSize BAR button on the top bar**, next to the menu names.
3. **The 2023 BIOS manual is wrong or missing several options** you will actually use:
   `Preference`, `Core Flex`, `Per CCD` Curve Optimizer, `cTDP to 105W`, `FCH Common
   Options`, `NPU Deep Sleep Enable`, `PPC Adjustment`, `USB power delivery in S4 state`,
   `DDR Turnaround Times`, `Refresh Management (RFM)`. All exist in 4004.
4. **There is no `DRAM Refresh` / tREFI option on ASUS AM5.** The only DRAM power control is
   `Power Down Enable`. Don't waste time looking.

---

## Phase 1 — Memory: 4800 → 6000 (do this first, do it alone)

This is the single largest performance miss on the machine. DDR5-6000 vs 4800 is ~25% more
bandwidth; measured LLM gain on a 2-DIMM board is **+17–19% tok/s**. It costs a few watts of
extra idle draw, which Phase 3 claws back.

**Before changing anything:** `Tool > ASUS User Profile > Save to Profile 1`. Keep your known-good
4800 config as the undo. ASUS notes BIOS 3602+ cannot be rolled back, and Clear CMOS needs a
physical reset.

### 1.1 Confirm the kit actually has a 6000 profile

`Tool > ASUS SPD Information` — look for an entry reading **6000 MT/s, CL30, 1.35V**. If you only
see 4800/JEDEC entries, the kit has no EXPO profile — do **not** hand-tune a server; get a
profile-bearing kit or accept 4800.

Also check rank in CPU-Z once you're in Linux: **2×32GB DDR5 is almost always dual-rank (2R)**,
and 2R 2-DIMM at 6000 is the genuinely hard case on Zen 4. Knowing this tells you how much
SoC headroom you'll need.

### 1.2 The settings

| Path                                                         | Item                                       | Value           | Why                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------ | ------------------------------------------ | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ai Tweaker`                                                 | **Ai Overclock Tuner**                     | **EXPO I**      | ASUS's own instruction for AM5 (FAQ 1042256: "If DRAM support EXPO, then set to [EXPO I]"). EXPO I takes primaries from the DIMM and secondaries from ASUS's validated auto-rules. **EXPO II** applies the DIMM's *complete* secondary set, which is tuned for the IC datasheet, not a Zen 4 IMC at 1DPC — less forgiving. Use EXPO II only if EXPO I fails, not as a first move. |
| `Ai Tweaker > EXPO`                                          | profile                                    | the 6000 one    | Each profile carries its own speed/timings/voltage                                                                                                                                                                                                                                                                                                                                |
| `Ai Tweaker`                                                 | DRAM Frequency                             | **Auto**        | This item only *downclocks*. Leave it alone.                                                                                                                                                                                                                                                                                                                                      |
| `Ai Tweaker > CPU SOC Voltage`                               | Mode                                       | **Manual Mode** |                                                                                                                                                                                                                                                                                                                                                                                   |
| `Ai Tweaker > CPU SOC Voltage`                               | **VDDSOC Voltage Override**                | **1.200 V**     | See below.                                                                                                                                                                                                                                                                                                                                                                        |
| `Advanced > AMD Overclocking > DDR and IF Frequency/Timings` | **Infinity Fabric Frequency and Dividers** | **2000 MHz**    | Verify this after loading EXPO. On this page the max is 2000; on `Ai Tweaker > FCLK Frequency` the range goes to 3000, so use the AMD Overclocking page. Manual text: "Auto = FCLK = MCLK" — leave it on Auto and you're *asking for 3000*, which is wrong.                                                                                                                       |
| same page                                                    | **UCLK DIV1 MODE**                         | **UCLK=MEMCLK** | DDR5 runs UCLK:MCLK 1:1 up to 6000 MT/s. `UCLK=MEMCLK/2` halves controller bandwidth and is a large latency hit.                                                                                                                                                                                                                                                                  |
| `Ai Tweaker`                                                 | UCLK DIV1 MODE                             | **UCLK=MEMCLK** | Same setting, alternate location                                                                                                                                                                                                                                                                                                                                                  |
| all DRAM timings (DDR SPD Timing, DDR Non-SPD Timing)        | —                                          | **Auto**        | Do **not** hand-enter `30-40-40-76`. Real 2×32GB 6000 CL30 kits are ~30-38-38-96; the looser set buys nothing and costs DRAM voltage headroom.                                                                                                                                                                                                                                    |
| `Advanced > AMD Overclocking > DDR...`                       | Memory Target Speed                        | **Auto**        | EXPO drives it. Only set manually (6000) if not using EXPO. Stepping is 200 MT/s, so 5800 isn't a legal value.                                                                                                                                                                                                                                                                    |
| `Ai Tweaker`                                                 | BCLK Frequency                             | **Auto**        |                                                                                                                                                                                                                                                                                                                                                                                   |
| `Ai Tweaker`                                                 | High DRAM Voltage Mode                     | **Disabled**    | Raises the DRAM ceiling to 2.07V. Not needed; a 6000 CL30 kit runs 1.35V.                                                                                                                                                                                                                                                                                                         |

**Resulting clocks: MCLK 3000 / UCLK 3000 / FCLK 2000.**

### 1.3 SoC voltage: 1.200V, then hunt downward

The board hard-caps SoC at **1.30V** for Ryzen 7000 (since BIOS 1413/1601) and AMD enforces the
same in AGESA. That cap is a safety rail, not a target.

EXPO **does not** set SoC voltage. It carries memory timings and memory voltages only. SoC
stays on whatever AGESA picks, which on a 7950X with 6000 loaded is typically ~1.20–1.25V.

**Start at 1.200V.** Evidence for why not lower, from 2-DIMM 6000 reports:

| Kit | Result |
|---|---|
| 96GB SK-Hynix 6000 30-36-36-80 (2×48) | needed **1.2–1.25V** SoC |
| 64GB 2×32 **6000 CL40**, 7900X3D | needed manual **1.20V SoC + 1.20V VDDIO/MC** |
| 2×32 6000 30-38-38 (2R) | **unstable** — 2R is the hard case |
| 2×16 6000 40-40-40 (1R) | stable |

Note the CL40 kit needed 1.20V and the CL30 kits needed *more*. **SoC/IMC load is driven by data
rate and rank, not CAS latency** — so if your kit is 6000 CL32 or CL36 rather than CL30, the
target is the same 1.20V. Don't chase CL30.

There are **no verified reports** of 2×32GB 6000 CL30 running at 1.10V SoC. Treat 1.10V as
likely-failing. Your sequence: 1.200 → 1.190 → 1.180 → … → 1.150, testing at each step, and stop
at the lowest value that survives. 1.20V is a perfectly good place to stop.

The BIOS readout shows *higher* than the actual die voltage (VRM-to-die droop). Seeing 1.25V
displayed while set to 1.20V is normal.

**If it won't train** (hangs at Q-Code 15 / yellow DRAM LED, or boot-loops): raise SoC in 25mV
steps to 1.225, then 1.250. Do **not** reach for EXPO II, AEMP, or manual subtimings first.

**If it trains but errors under test:** raise DRAM VDD/VDDQ to the EXPO value, or +0.02V in
5mV steps.

### 1.4 Verification — do not skip, and do it in this order

Training is **stricter than any software memtest** (ASUS's own wording: waveforms that produce
valid data in software can still fail the hardware electrical mask). "It trained once" is not
evidence of stability, and "it passed 24h of memtest" is not evidence it will train again. You
need both.

1. Confirm 6000 MT/s is actually applied (BIOS EZ Mode DRAM Frequency; CPU-Z).
2. `memtest86` — 4–8h, must pass run 1.
3. **TM5 (TestMem5) `anta777 extreme`** — 4h minimum, 24h+ to trust. The single most effective RAM test.
4. `y-cruncher VST (VT3)` + `Linpack Xtreme` — catches SoC/IMC instability pure RAM tests miss.
5. `occt` — Memory, FPU, VRAM, then CPU.
6. `prime95` small FFTs or `y-cruncher` for 24–48h.
7. **10 cold power-off/power-on cycles + 10 warm reboots.** This is the one people skip and it's
   the one that catches the actual failure mode.
8. 24h of your real workload with output checksums.

The nastiest documented AM5 failure is passing every stress test and then BSODing during
ordinary light-load transitions (downloads, unpacking) — idle↔load boundaries. So include a
light-load transition test, not just a sustained burner.

**Production bar: 24h TM5 anta777 extreme + 24–48h Prime95/OCCT + 10 cold boots + a real 24h
inference run with checksum verification.**

### 1.5 Only now, enable the DRAM power + POST features

Both of these are stability variables themselves, so enable them *after* 1.4 is clean, then
re-verify.

| Path | Item | Value | Note |
|---|---|---|---|
| `Advanced > AMD Overclocking > DDR Controller Configuration > DDR Power Options` | **Power Down Enable** | **Enabled** | Lets DRAM enter power-down/self-refresh when idle |
| `Advanced > NB Configuration > DDR Memory Features` (or BIOS `Search`) | **Memory Context Restore** | **Enabled** | Skips 5–15min first-boot training on future boots |

**These two must be enabled together.** With MCR on and Power Down off, users report constant
BSODs. And if you ever change memory settings, disable MCR temporarily to force full retraining.

Then `Tool > ASUS User Profile > Save to Profile 2`.

---

## Phase 2 — Settings that will break Linux if you get them wrong

Do these before first boot. Each one has burned someone.

| Path | Item | Value | Consequence if wrong |
|---|---|---|---|
| `Advanced > CPU Configuration` | **PSS Support** | **Enabled** | **Biggest trap on the page.** Disabling stops ACPI P-state objects → Linux loses cpufreq governors → **idle power goes UP**, sometimes dramatically. Do not touch. |
| `Advanced > CPU Configuration` | **NX Mode** | **Enabled** | Required. |
| `Advanced > CPU Configuration` | **SVM Mode** | **Enabled** | Required for containers/KVM. |
| `Boot > Secure Boot` | **Secure Boot** | **Disabled** | **Omarchy requires it off.** Its manual: "You must turn off Secure Boot and/or TPM in the BIOS." Structurally, it can't be on: the NVIDIA driver is `nvidia-open-dkms` (DKMS) against a custom `linux-omarchy` kernel, and there is **zero** key-enrollment code in the Omarchy repo — no shim, no MOK, no sbctl. |
| `Boot > Secure Boot > OS Type` | OS Type | **Other OS** | Skips the MS Secure Boot check |
| `Boot > CSM` | **Launch CSM** | **Disabled** | Mandatory for UEFI/Limine. Also required for ReSize BAR, and the single biggest POST-time win (skips CSM16 + all legacy option ROM scanning). |
| `Advanced > PCI Subsystem Settings` | **Above 4G Decoding** | **Enabled** | Effectively mandatory with two large-BAR GPUs. |
| `Advanced > PCI Subsystem Settings` | **Resize BAR Support** | **Enabled** | Needs Above 4G + CSM off. Note the name is "Resize", not "Re-Size". |
| `Advanced > AMD CBS` | **IOMMU** | **Enabled**, set to **largest size offered** | NVIDIA's Linux README explicitly recommends enlarging or disabling the AMD IOMMU: the driver "can result in IOMMU space exhaustion when large amounts of physical memory are remapped" for the GPU. A 12GB + 16GB pair is exactly that case. Enlarging gets you DMA protection *and* avoids exhaustion. If your BIOS has no size control, use `iommu=memaper` + `iommu=pt` on the kernel cmdline. **Never set `GGML_CUDA_P2P=1`** — llama.cpp's build docs warn it "may cause crashes or corrupted outputs for some motherboards and BIOS settings (e.g. IOMMU)". |
| `Advanced > AMD CBS > CPU Common Options` | **ACPI _CST C1 Declaration** | **Auto** or **Enabled** | Turning it off means Linux never sees C1 → cores can't halt → higher idle power. |
| `Advanced > SATA Configuration` | **Restore AC Power Loss** | **Power On** | Headless box returns from an outage without a human. |

### fTPM — deviating from Omarchy's docs, on purpose

Omarchy's manual tells you to turn TPM off too. You don't have to: fTPM is ~2 mW, and it's what
`systemd-cryptenroll --tpm2-device` needs for measured boot and unattended LUKS unlock. Turning it
off buys you nothing on a box you're about to own for years.

| Path | Item | Value |
|---|---|---|
| `Advanced > Trusted Computing` | Security Device Support | **Enable** |
| `Advanced > Trusted Computing` | SHA256 PCR Bank | **Enabled** |
| `Advanced > AMD fTPM configuration` | **Firmware TPM switch** | **Enable Firmware TPM** |
| `Advanced > AMD fTPM configuration` | Erase fTPM NV for factory reset | **Disabled** (enabling destroys sealed-volume keys) |
| `Advanced > Trusted Computing` | Physical Presence Spec Version | 1.2 |

---

## Phase 3 — Idle power

Roughly 25–35W of package idle is achievable (stock is commonly 50–60W). Ranked by impact.

### Tier 1 — the big ones

| # | Path | Item | Value | Notes |
|---|---|---|---|---|
| 1 | `Ai Tweaker` | **Preference** | **Power Efficient** | The most direct perf-vs-power switch ASUS ships on AM5, and it only exists in current BIOS — not in the 2023 manual. Highest-value single setting here. |
| 2 | `Ai Tweaker > CPU SOC Voltage` | VDDSOC Override | **1.200V** (see Phase 1) | Auto/EXPO parks SoC around 1.20–1.25V. SoC idle leakage scales steeply with V. |
| 3 | `Advanced > AMD Overclocking` | **SoC/Uncore OC Mode** | **Disabled** | ASUS's own text: "Forces CPU SoC/Uncore components (e.g. Infinity Fabric, memory, and integrated graphics) to run at their maximum specified frequency at all times. **May improve performance at the expense of idle power savings.**" This is the single largest idle-power trap on AM5 — `Enabled` pins FCLK+MCLK+UCLK at max permanently. Disabling it does **not** hurt memory bandwidth under load, and may slightly *help* all-core boost by freeing SoC power budget. Only reason to enable: FCLK overclocking past 2000, which you have no interest in. **Verify it stuck after a cold boot** — some boards silently revert this. |
| 4 | `Advanced > NB Configuration` | **Primary Video Device** | **PCIE Video** | |
| 5 | `Advanced > AMD PBS` (or CBS) | **Integrated Graphics** | **Disabled** | ASUS's docs note "in Raphael, the IOD power figures will increase if the integrated RDNA 2 graphics are in use." SoC/Uncore OC Mode's description explicitly names integrated graphics as one of the components it force-maxes. VDD_SOC also sets the iGPU rail. You lose only rear I/O video and a fallback console. **Caveat:** a 7950X owner on an ASUS X670 board reports BIOS "Integrated Graphics: Disabled" did *not* remove the iGPU from the PCI bus. Verify with `lspci \| grep -iE 'VGA\|3D\|Display'` after boot; fallback is `video=amdgpu.igpu=off`. |
| 6 | `Advanced > AMD CBS` | **Global C-state Control** | **Enabled** | Biggest C-state knob for I/O + DF |
| 7 | `Advanced > AMD CBS > DF Common Options` | **DF Cstates** | **Enabled** (or Auto — Auto syncs to the above) | |
| 8 | `Advanced > AMD CBS > CPU Common Options` | **Power Supply Idle Control** | **Low Current Idle**, then soak-test | Your instinct is usually inverted here. `Typical Current Idle` is what *disables* Package C6 (measured: "with Typical set, Core C6 is enabled and Package C6 is disabled"; with Low, both show enabled, and idle VID drops to ~0.4V). There is no known AM5 issue where Low Current Idle *prevents* C6. The real Low Current Idle risk is **random multi-hour idle hangs** on some PSUs. Try Low, soak 72h idle, keep Typical as fallback. |

### Tier 2 — chipset and board

| Path | Item | Value | Est. saving |
|---|---|---|---|
| `Advanced > AMD PBS` | **Unused GPP Clocks Off** | **Enabled** | Shuts PCIe GPP clocks for unused ports |
| `Advanced > AMD PBS` | **ACP Power Gating** | **Enabled** | Audio co-processor power gating |
| `Advanced > AMD PBS` | **ACP CLock Gating** | **Enabled** | |
| `Advanced > AMD PBS` | **PM L1 SS** | `L1.1_L1.2` or Auto | Lets idle PCIe links reach L1.1/L1.2 |
| `Advanced > AMD PBS` | **Clock Power Management (CLKREQ#)** | **Enabled** | |
| `Advanced > AMD CBS > NBIO Common Options` | **NPU Deep Sleep Enable** | **Enabled** | Unused accelerator deep-sleep. Harmless on a 7950X, which has **no NPU** at all. |
| `Advanced > AMD CBS > NBIO Common Options` | **PSPP Policy** | **Auto** (→ Balanced) | `Performance` prevents Gen5→Gen3 downshift on AC→DC transitions. Balanced is AMD's recommended config. |
| `Advanced > AMD CBS > NBIO Common Options` | **NB Azalia** | **Disabled** | Chipset-side HDA. ~0.5–1W. |
| `Advanced > Onboard Devices Configuration` | **HD Audio Controller** | **Disabled** | Realtek S1220A + amp + jack detect |
| `Advanced > Onboard Devices Configuration` | **Wi-Fi Controller** | **Disabled** | If you use the 2.5GbE port only. MTK Wi-Fi 6E idles ~0.5–1W. |
| `Advanced > Onboard Devices Configuration` | **Bluetooth Controller** | **Disabled** | |
| `Advanced > Onboard Devices Configuration` | **LED lighting** (both states) | **Stealth Mode** | "All LEDs will be disabled" — kills Aura RGB *and* the Q-LEDs. Top-bar `F4` AURA also works. |
| `Advanced > Onboard Devices Configuration` | **USB power delivery in Soft Off state (S5)** | **Disabled** | Real standby rail draw, ~0.5–2W |
| `Advanced > Onboard Devices Configuration` | **USB power delivery in S4 state** | **Disabled** | New in 4004, not in the manual |
| `Advanced > Onboard Devices Configuration` | **Serial Port** | **Disabled** | Removes the Super I/O COM port |
| `Advanced > Onboard Devices Configuration` | **Launch Realtek PXE OPROM** | **Disabled** | |
| `Advanced > Onboard Devices Configuration` | USB Audio Controller / DVI Port Audio | **Disabled** | |
| `Advanced > AMD CBS > FCH Common Options > USB Configuration Options` | `USB2 controller enable`, `USB0/1/2 2.0 port enable`, unused `USB* 3.1 port enable` | **Disabled** (unused only) | `FCH Common Options` is absent from the 2023 manual. Each disabled root port removes a PHY + PLL: ~0.3–1W per USB3 root port, ~0.1–0.3W per USB2. **Do not disable the port your keyboard is on.** |
| `Advanced > SATA Configuration` | Unused `SATA6G_1..4` | **Disabled** | |
| `Advanced > SATA Configuration` | **Max Power Saving** | **Enabled** | |
| `Advanced > SATA Configuration` | **ErP Ready** | **Enabled (S5)** |  **Kills WoL and RTC wake**, and disables all PME options. Only take this if you don't need remote power-on. |
| `Advanced > APM Configuration` | Power On By PCI-E / RTC | **Disabled** | (ErP forces this off anyway) |
| `Advanced > AMD CBS > NBIO Common Options > Audio Configuration` | `Audio IOs` | leave default | |

### The 0.1% items you asked for

These will not move a watt. Listed because you asked, with the honest verdict.

| Path | Item | Value | Verdict |
|---|---|---|---|
| `Ai Tweaker > DRAM Timing Control > DRAM Signal Control` | `Proc CA Drive Strength`, `Proc CK/CS Drive Strength`, `Proc Data Drive Strength`, `DRAM Data Drive Strength`, `Rtt Nom Wr/Rd`, `Rtt Wr`, `Rtt Park`, `Rtt Park Dqs`, `CPU On-Die Termination (ProcODT)` | **Auto, all of them** | Signal-integrity and training knobs. Zero performance effect once stable. ProcODT is the only one with a marginal story (too high → more reflection and I/O power; too low → marginals) — still leave it on Auto. **This entire page stays on Auto.** |
| `Ai Tweaker > Advanced Memory Voltages` | `PMIC Voltages` → Sync All PMICs | **Sync All PMICs** | |
| `Ai Tweaker > Advanced Memory Voltages` | `Memory Voltage Switching Frequency` | **Auto** | Lower (0.750 MHz) is more efficient at light load but slower transient response. Claimed ~1–3W, **unmeasured**. Leave Auto unless you're chasing the last watt and re-test memory after. |
| `Ai Tweaker > Advanced Memory Voltages` | `Memory Current Capability` | **Auto** | Raising it costs idle power and adds nothing. |
| `Ai Tweaker > DRAM Timing Control` | `DRAM VDD Voltage` / `DRAM VDDQ Voltage` | **Auto** (EXPO's 1.35V) | Trimming to the minimum stable value does reduce DIMM power. Only if you're chasing watts. |
| `Ai Tweaker` | `Clock Spread Spectrum` | **Auto** | EMI reduction, no perf effect |
| `Ai Tweaker` | `Performance Bias` | **Auto** | Workload-specific micro-tuning presets (CB R23 / GB3). Meaningless for inference. |
| `Ai Tweaker` | `Tweaker's Paradise` (all sub-options) | all **Disabled**/Auto | Runtime BCLK OC. Destabilises NVMe and PCIe. |
| `Ai Tweaker` | `Extreme Over-voltage` | **Disabled** | Requires a CPU_OV jumper. |
| `Ai Tweaker` | `TURBO GAME MODE` | **Disabled** | "Disabling second CCD and SMT." You have 2 CCDs — enabling would also kill SMT, which you want. |
| `Ai Tweaker` | `Gaming Adaptive CCD Parker` | **Disabled** | Parks the idle CCD. Pointless for a box that runs inference on all 16 cores. |
| `Ai Tweaker` | `LN2 Mode` | **Auto** | |
| `Ai Tweaker` | `Monitoring Software reboot Workaround` | **Auto** | Enable only if a monitoring agent triggers reboot bugs. |
| `Ai Tweaker` | `Core Flex` (Algorithm 1/2/3) | **Disabled** | This is the renamed `Custom Algorithms` from the 2023 manual — the old name no longer exists. It *can* do thermal-triggered power capping (Condition: CPU Temperature, Action: Package Power Limit Slow) that static PPT/TDC can't express. Genuinely useful, but Phase 4's ECO Mode covers your case. Leave off for now. |
| `Ai Tweaker` | `AI Cache Boost` | test both | "Enhance performance and compute power when using AI-based tools." **Despite the name this is a boost/scheduling behaviour change for X3D cache parts — inert on a 7950X.** The marketing "AMD Ryzen AI / AI PC ready" badge on this board is a series-level badge; the 7950X has **no XDNA/NPU at all**. |
| `Ai Tweaker` | `Enhancement` | **Auto** | ASUS's PBO Enhancement. Leave Auto. |
| `Ai Tweaker` | `Preference` at the *other* (CPU Core Ratio) level | — | Only one `Preference` item exists. |
| `Advanced > AMD CBS > DF Common Options > ACPI` | **ACPI SRAT L3 Cache As NUMA Domain** | **Disabled** | `Disabled` = one NUMA node per socket. `Enabled` = each CCX becomes its own domain (2 nodes on a 7950X). **There is no `NPS` option on this board** — zero strings in 4004. Leave it Disabled. The 7950X's 2 CCDs are not a problem for llama.cpp: cross-CCD traffic during a layer-by-layer sweep is sequential and predictable, which is the best case for Infinity Fabric. NUMA penalties in llama.cpp are a dual-socket phenomenon. |
| `Advanced > AMD CBS > CPU Common Options` | **SMT Control** | **Auto** (keep SMT on) | SMT helps inference. Needs a power cycle to change. |
| `Advanced > AMD CBS > CPU Common Options` | **Core Performance Boost** | **Auto** | Setting CBS's copy to `Disabled` hard-caps boost. There is no "Core Performance Boost Override" in 4004. |
| `Advanced > AMD CBS > CPU Common Options` | `Prefetcher settings` (all 6) | **Auto** | |
| `Advanced > AMD CBS > CPU Common Options` | `AVX512` | absent on 7950X | 7950X is 256-bit AVX2, no AVX-512. Option won't appear. |
| `Advanced > AMD CBS > CPU Common Options` | `Latency Under Load (LUL)` | **Auto** | "Enabling may improve latency in heavy BW scenarios. May slightly reduce peak CCD BW." Could try `Enabled` and measure. Low priority — decode is bandwidth-bound, not latency-bound. |
| `Advanced > AMD CBS > UMC Common Options` | `DDR Timing Configuration` | **Decline** (if prompted) | Once EXPO is set, ASUS drives timings. Entering CBS timing is a footgun. |
| `Advanced > AMD CBS > UMC Common Options > DDR...` | **Refresh Management (RFM)** | **Auto** | Thermal-vs-refresh tradeoff. Forcing it on unsupported ranks disables REFpb/REFsb — a data-integrity risk. Not worth it. |
| `Advanced > AMD CBS > UMC Common Options` | `DDR Turnaround Times` (Read/Write Drift Adjustment P0-P3, PMU DQ Vref) | **Auto** | Tuning-only knobs. |
| `Advanced > AMD CBS > UMC Common Options` | `ARdPtrInitVal P0` | **Auto** | Only relevant above 6400 MT/s. |
| `Advanced > AMD CBS > UMC Common Options` | `DDR Memory Features` | leave default | |
| `Advanced > AMD CBS > SMU Common Options` | `STAPM Control` / `SPL Control` / `STT Control` | greyed on 7000-series | BIOS 2413: "Disable STAPM of AM5 Ryzen 8000 processors" |
| `Advanced > AMD CBS > SOC Miscellaneous Control` | `TSME` | **Auto** | AMD transparent memory encryption. Not needed for inference. |
| `Ai Tweaker` | `Turbo Game Mode`, `AEMP`, `ROG Mode`, `ROG Certified`, `EXPO on the fly` | don't select | AEMP is for profile-less DIMMs; `EXPO on the fly` is a Core Flex action that **downclocks memory under load** — directly harmful to inference. |
| `Advanced > AMD Overclocking` | `CPU Core Count Control` / `Down Core Mode` | leave disabled | You want all 16C/32T. |
| `Advanced > AMD Overclocking` | `LCLK Frequency Control` | **Auto** | 4004 now offers min + max, not just max. |
| `Advanced > AMD Overclocking` | `VDDG / VDDP / VPP Ctrl / VDDIO Ctrl / VDD_MEM Control` | **Auto** | |
| `Advanced > AMD Overclocking` | `GFX Curve Optimizer` | **Disable** | iGPU only. No iGPU on a 7950X. |

---

## Phase 4 — Load power (does not help idle at all)

A cTDP value is a **ceiling**. Idle sits far below any of them, so capping power does nothing for
idle draw. It controls *load* power, heat and noise — which matters for a box that will sit at
sustained load for hours.

The confusing part: there are **three different, non-interchangeable** cTDP items.

| # | Path | Label | Values |
|---|---|---|---|
| 1 | `Ai Tweaker` | **AMD ECO Mode** | `Auto`, **`cTDP 65W (88W/75A/150A)`**, **`cTDP 105W (142W/110A/170A)`**, `cTDP 170W (230W/160A/225A)` |
| 2 | `Ai Tweaker` (top-level row, between `Core Performance Boost` and `Precision Boost Overdrive`) | **cTDP to 105W** | Toggle. This is the 2024 "phase in cTDP 105W" feature for 65W parts (9600X/9700X) — on a 170W 7950X it may not appear or may be greyed. |
| 3 | `Advanced > AMD CBS > SMU Common Options > TDP Control` | **ECO Mode** | `Disabled` (stock), `Enabled` (65W), `Enabled -105W` |

Format is PPT (W) / TDC (A) / EDC (A). Full table also includes 35W (60W/66A/130A) and 45W
(96W/80W/45A/65A), but those only appear in the CBS-level forms.

### Recommendation: `AMD ECO Mode = cTDP 105W (142W/110A/170A)`

**Why 105W and not 65W:** token generation is memory-bandwidth-bound and a decode loop
saturates at roughly **4 threads** — measured on a 16-core 7950X: 8B Q4_K_M hit 13.24 tok/s at
4 threads. A 4-thread bandwidth-bound loop will never approach a 105W ceiling, so **the cap
costs you essentially nothing on decode.** Where it does bite is **prefill**, which is
compute-bound and scales to all 16 cores — expect roughly 5–10%.

That maps cleanly onto your two-server architecture: two independent single-stream decode
sessions, not one long-context batch prefill workload. If you ever serve long prompts or batch
users and care about time-to-first-token, use `cTDP 170W` (= stock) or `PBO = Manual` with
PPT 230 / TDC 160 / EDC 225.

**Never use `cTDP 35W` or `45W` on a 7950X** — TDC of 66A/45A is so low that single-core boost
and heavy transients trip hard throttling instead of clean downclocking.

**Never use Ryzen Master's Eco Mode.** AMD confirmed to Overclock3D that doing the same thing
through Ryzen Master slams *all* Ryzen 7000 to 65W. Use the BIOS dropdown. (You don't have
Ryzen Master anyway — there's no Ryzen Master entry in this board's BIOS; `Tool` only controls
whether Armoury Crate / MyASUS app downloads are permitted.)

### Leave these on Auto

| Path | Item | Value | Why |
|---|---|---|---|
| `Ai Tweaker` or `Advanced > AMD Overclocking` | **Precision Boost Overdrive** | **Auto** | |
| same | **PBO Scalar** | **NORM** (1X) | Higher scalar lets the CPU ignore the per-part voltage-durability limiter. It is a pure OC knob: raises all-core sustained power and junction temp for no benefit on bandwidth- or compute-bound inference. |
| same | **CPU Boost Clock Override** | **Disabled** | |
| same | `Platform Thermal Throttle Limit` | **Auto** | |
| same | `Per-Core Boost Clock Limit` (new in 4004) | **Auto** | |
| same | `Disable Current Limiter` | **Disabled** | "Use at your own risk" |
| same | `Thermal Limit` | leave default | |
| `Ai Tweaker` or `Advanced > AMD Overclocking` | **Curve Optimizer** | **Auto** / **Disable** | Real tempting power lever, but per-core stability roulette. For a box that must not crash and whose data must not silently corrupt, this is the wrong risk. A −5 all-core CO user idles at 36W PPT, so there *is* an efficiency win — but you've already got the big wins from SoC voltage and `Preference`. If you want it later, do it as a separate project with a full test cycle. |
| same | `CO Load Guard`, `Curve Shaper` | **Auto** | |
| `Ai Tweaker` | `CPU Core Ratio`, `CPU Core Ratio (Per CCX)`, `Core VID` | **Auto** | Manual Vcore control was **removed** in BIOS 1409. On current BIOS only `Offset Mode` is live. Don't plan around fixed Vcore. |
| `Ai Tweaker` | `Actual VRM Core Voltage` | **Auto** | Manual Mode expected to be greyed on 4004. |
| `Ai Tweaker` | **CPU Load-line Calibration** | **Auto** | Sets Vcore droop vs current. **Higher level = less droop = higher average Vcore = more power and heat.** It helps hold all-core boost at a linear power cost — the wrong direction for you. `Level 5` is "Recommended for OC", not for efficiency. |
| `Ai Tweaker` | `Segment2 Loadline` / `Segment2 Current Threshold` (new in 4004) | **Auto** | Two-segment load line, "lower values result in a higher voltage droop." Same trade, more granularity. Leave alone. |
| `Ai Tweaker` | `CPU Current Capability` (100–140%) / `VDDSOC Current Capability` | **100%** | Raising above 100% risks instability. |
| `Ai Tweaker` | `CPU Current Reporting Scale`, `VDDSOC Current Reporting Scale` | **100%** | 130/140% are red-flagged in the BIOS UI. |
| `Ai Tweaker` | `CPU Power Thermal Control` (new) | **Auto** | "A higher temperature brings a wider CPU power thermal range" |
| `Ai Tweaker` | `CPU VRM Switching Frequency` | **Auto** (250–500KHz range in 4004) | **The 2023 manual's 300–800KHz is stale.** |
| `Ai Tweaker` | `VDDSOC Switching Frequency` | **Auto** (400–600KHz) | |
| `Ai Tweaker` | `CPU Power Duty Control` | **T. Probe** | Thermal balance, not current balance. |
| `Ai Tweaker` | `CPU Power Phase Control` / `Power Phase Response` | **Auto** | Don't chase transient response on a power-capped server. |
| `Ai Tweaker` | `Prochot VRM Throttling`, `Peak Current Control`, `VRM Initialization Check` | **Enabled** | Safety features. `VRM Initialization Check` **hangs POST at 76/77** if disabled and VRM init fails — leave it on. |
| `Ai Tweaker` | `VRM Spread Spectrum` (new) | **Auto** | "Disable this setting when overclocking" |
| `Ai Tweaker` | `Core Voltage Suspension` / `Voltage Floor Mode` / `Voltage ceiling Mode` (new in 4004) | **Auto** | Sellsweetspot defaults: Floor Low VMin 1.05V, Ceiling Low VMax 1.20V. Leave auto. |
| `Ai Tweaker` | `Overclocking Load Guard` (new) | **Auto** | Switches OC Mode → PBO Mode under heavy load. |
| `Ai Tweaker` | `eCLK Mode` | leave default | |
| `Ai Tweaker` | `CPU Fused Boost Clock Limit` | read-only | Informational. |

**Use the `Advanced > AMD Overclocking` copy of PBO, not the `Ai Tweaker` copy.** They have
different sub-options and can override each other. `PBO Limits` (Auto/Disable/Motherboard/
Manual) exists **only** under `Advanced > AMD Overclocking > Precision Boost Overdrive` in 4004
— the 2023 manual lists it in both places, which is now wrong. Pick one menu and leave the other
on Auto.

---

## Phase 5 — Headless / POST-time

You're booting headless over SSH. This section is about boot time and about not having a problem
at 2am. Cumulative POST saving is roughly 15–50s, potentially more if something was waiting on
PXE.

| # | Path | Item | Value | Saving |
|---|---|---|---|---|
| 1 | `Boot > CSM` | **Launch CSM** | **Disabled** | Multiple seconds — skips CSM16 module + all legacy option ROM scanning. |
| 2 | `Advanced > Network Stack Configuration` | **Network Stack** | **Disabled** | **3–30s.** The biggest POST win after CSM. Disable the whole stack, not just IPv4/IPv6 PXE Support, and set `PXE boot wait time` to minimum. |
| 3 | `Boot` | **Setup Prompt Timeout** | 1–2 (not 65535) | Real, and often bigger than Fast Boot. |
| 4 | `Boot` | **Launch Video OPROM policy** | **Ignore** | 1–3s **per GPU** — two cards doubles this. |
| 5 | `Boot > Boot Configuration` | **Fast Boot** | **Enabled** | 2–5s. Safe with NVMe + Linux. Does not bypass CSM on ASUS, so composes fine. |
| 6 | `Advanced > SATA Configuration` | **SMART Self Test** | **Disabled** | 0.5–2s. Do monitoring in Linux with `smartd`/`nvme-cli`. |
| 7 | `Advanced > USB Configuration` | **USB Mass Storage Driver Support** | **Disabled** | Removes USB mass-storage enumeration from POST. |
| 8 | `Advanced > USB Configuration` | **XHCI Hand-off** | **Disabled** | On a 6.x kernel handoff is native, so this is the modern-correct path. Switch to `Enabled` only if you hit 30s boot delays. Not a power item. |
| 9 | `Advanced > USB Configuration` | `Legacy USB Support` | **Disabled** (unless USB-booting) | |
| 10 | `Advanced > USB Configuration` | `USB Single Port Control` | disable unused | |
| 11 | `Advanced > Onboard Devices Configuration` | unused `SATA6G_1..4`, `PCIEX16_2`, fan headers | **Disabled** | 1–3s |
| 12 | `Advanced > Monitor` | `Chassis Intrusion Detection Support` | **Disabled** | No case switch wired |
| 13 | `Tool` | **Setup Animator** | **Disabled** | 1–2s of logo animation skipped. Also `EZ Mode Fan Animator`. |
| 14 | `Boot > CSM` | `Option ROM Messages` | **Keep Current** | Quieter, slightly faster |
| 15 | `Boot > CSM` | `Interrupt 19 Capture` | **Disabled** | |
| 16 | `Boot` | `Bootup NumLock State` | your preference | Irrelevant headless |
| 17 | `Boot` | `Boot from PCI-E/PCI Expansion Devices` | **Disabled** | Stops probing the GPUs for boot devices |
| 18 | `Boot` | `AMI Native NVMe Driver Support` | **Enabled** | |
| 19 | `Advanced > AMD CBS > UMC` | `DDR Training Runtime Reduction` | **Enabled** | Shortens training. Note: auto-disabled by BIOS when an OC profile is active. |
| 20 | `Advanced > AMD Overclocking > DDR...` | `Memory OC Mode` | `Enable` | Fine with EXPO — it's a training helper. |

**Don't** set `PCIEX16_1 Bandwidth Bifurcation Configuration` to anything but `Auto Mode`. On a
7950X the slot is x16 straight from the CPU; x8 bifurcation only applies to 8000-series. The
manual's "if a PCIe device is inserted to PCIEX16_2, switch PCIEX16_1 to x8" is AM5 boilerplate
that does not describe this board.

Leave every `PCIE Link Speed` / `M.2 Link Mode` / `Chipset_x Link Mode` on **Auto**. Don't
downclock the GPU slots.

**After saving a large config, use `Save Changes & Reset`, not `Save Changes & Exit`** — the
extra reboot re-runs memory training and proves the config actually holds.

---

## Phase 6 — Fans (worth up to ~15W, often the largest non-CPU lever)

A 120mm PWM fan at true 0% draws ~0.1–0.3W. At `Silent` (20–35% duty) it draws ~1.5–3W each.
Six fans is the difference between ~1W and ~15W.

1. **Physically unplug unused fan headers.** Strictly better than any BIOS setting — a disabled
   header still powers a controller channel. This board has CPU_FAN, CPU_OPT, AIO_PUMP,
   Chassis 1–4, W_PUMP+. A dual-tower air cooler uses 2.
2. Run **`Q-Fan Tuning`** (2–5 min) on the fans you keep. It measures a real minimum duty rather
   than guessing from a preset. This is the correct way to get quiet-and-minimal.
3. `CPU Fan Profile` / `Chassis Fan N Profile` = **Silent** on fans you keep. Use `Manual`, not
   `Full Speed`.
4. `CPU Fan Speed Low Limit` = **Ignore**, and same for chassis, to silence the RPM warning.
5. `Allow Fan Stop` = **Enabled on chassis fans only**, with a low Point1 temperature (~40–45°C)
   and low Point1 duty.  **Never on CPU_Fan or AIO_PUMP** — a 7950X at 95°C with a stopped CPU
   cooler is a shutdown.
6. `CPU Fan Q-Fan Source` = `CPU`; `Chassis Fan Q-Fan Source` = `Multiple Sources` or
   `MotherBoard` so they don't all key off CPU temp and short-cycle.
7. `CPU Fan Step Down` = Level 4/5, `Step Up` = Level 2/3 for smoother curves.
8. Leave `AI Cooling` at default for the first week, then evaluate — it self-tunes and may raise
   fans after deciding they're "inefficient."
9. **Do not quiet the CPU cooler below what sustained 170W needs.** A throttled inference node is
   worse than a noisy one. This is the one place where Phase 4's 105W cap helps you keep noise
   down.

---

## Phase 7 — Tool and Exit

| Path | Item | Value | Notes |
|---|---|---|---|
| `Tool` | **BIOS Image Rollback Support** | **Disabled** | BIOS 3602/3854 state rollback is already impossible; this removes the temptation. |
| `Tool` | **Setup Animator** / `EZ Mode Fan Animator` | **Disabled** | |
| `Tool` | **Download & Install ARMOURY CRATE app** | **Disabled** | Windows-only; prevents the OEM provisioning path. Real board-level RGB power is killed by `LED lighting = Stealth Mode`, not this. |
| `Tool` | **Download & Install MyASUS service & app** | **Disabled** | Same. |
| `Tool` | `Publish HII Resources` | leave default | |
| `Tool` | `Flexkey` | **`Aura On/Off`** | Disables Aura LEDs without software (or rely on Stealth Mode). |
| `Tool` | `ASUS User Profile` | **Save 2 profiles** | Profile 1 = known-good 4800, Profile 2 = final 6000 config. This is your only undo besides Clear CMOS. |
| `Tool` | `ASUS SPD Information` | read-only | Verify your EXPO profile here. |
| `Tool` | `ASUS Secure Erase` | don't visit | **Intel SATA only** — not usable on this AMD board, and it's a POST-time cost. |
| `Tool` | `ASUS EZ Flash 3 Utility` | use for updates | Rename the CAP to `TX670ELW.CAP` via BIOSRenamer first if flashing from USB. |
| `Exit` | **Save Changes & Reset** | use this | Not `Save Changes and Exit`, after big changes. |

**BIOS version: 4004 is current and worth flashing before you configure.** Not for idle power —
you'll see no idle benefit from AGESA updates and one user actually reported idle wall power
*rising* ~15W after an AGESA bump. Flash for AGESA 1.3.0.1d's DDR5 training and CXMT memory
compatibility, which is directly relevant to getting 6000 stable on 2×32GB.

---

## Do NOT touch

| Item | Why |
|---|---|
| `Advanced > CPU Configuration > PSS Support` → Disabled | Kills Linux P-states → idle power goes **up** |
| `Advanced > CPU Configuration > NX Mode` → Disabled | Required |
| `Boot > CSM > Launch CSM` → Enabled | Breaks ReSize BAR, Above 4G, and the Limine/UEFI path |
| `Boot > Secure Boot` → Enabled | Omarchy can't enroll keys; DKMS modules are unsigned |
| `Ai Tweaker > DRAM Signal Control` (anything) | SI/training knobs, zero perf effect, real instability risk |
| `Advanced > AMD CBS > UMC > DDR Timing Configuration` | Footgun once EXPO is driving |
| `Advanced > AMD Overclocking > CPU Core Count Control` | You'd lose cores |
| `Ai Tweaker > CPU Load-line Calibration` → high level | More Vcore, more power, wrong direction |
| `Ai Tweaker > Precision Boost Overdrive Scalar` → above 1X | All-core power for no inference gain |
| `Ai Tweaker > SoC Voltage` (`Advanced > AMD Overclocking`) → above ~1.25V | The board caps at 1.30V. That cap exists because ASUS was overvolting SoC. |
| `Ai Tweaker > High DRAM Voltage Mode` → Enabled | Raises DRAM ceiling to 2.07V for no benefit at 6000 CL30 |
| `GGML_CUDA_P2P=1` (Linux, not BIOS) | Documented to cause crashes/corruption with IOMMU |
| `--split-mode tensor` (Linux) | Experimental, and broken on mixed CUDA+Vulkan builds |
| Ryzen Master Eco Mode | Forces all Ryzen 7000 to 65W per AMD |

---

## Expected results

| | Stock | Tuned |
|---|---|---|
| CPU package idle | 50–60W | **25–35W** |
| Memory | 4800 MT/s | 6000 MT/s (+17–19% tok/s on CPU-bound inference) |
| Wall, 2 GPUs at low P-state, well-sized PSU | 180–220W | **~90–130W** |

Wall power is the number that matters. Budget for ~10–25W per discrete GPU at idle — a headless
server never triggers a display-driven downclock, so a card left in P0 will sit at 38W instead of
20W. Both GPUs combined are likely your largest single idle cost after the CPU.

**Also: size your PSU down.** An oversized 1300W unit at a 100W load wastes so much to conversion
inefficiency that it can add 10–15W of pure waste. For ~300W peak, a 650–750W unit is
substantially more efficient at your actual load point.

---

## Post-boot Linux checklist (Omarchy)

Not BIOS, but it's half the battle and each item has a specific reason.

```bash
# 1. Verify both GPUs are present and idle in low P-states
lspci | grep -iE 'VGA|3D|Display'          # expect 2, not 3 (iGPU disabled) — see caveat in Phase 3
nvidia-smi -q -d PERFORMANCE | grep -i pstate
vulkaninfo --summary | grep -iE 'deviceName|apiVersion'
rocminfo 2>/dev/null | grep -i gfx         # gfx1200 if ROCm is installed

# 2. DO NOT enable nvidia persistence mode.
#    Omarchy doesn't, which keeps PCIe RTD3 available so the 3060 can downclock.
#    Enabling persistence *costs* you idle power on this setup.

# 3. Set the power profile. Omarchy defaults desktops to `performance` on AC, which is wrong here.
omarchy powerprofiles set autodetect power-saver

# 4. btop resumes your NVIDIA dGPU every time you open it. Omarchy issue #11184.
#    Edit ~/.config/btop/btop.conf :  shown_gpus = "amd"

# 5. Pin the compositor to the AMD card (issue #12791). Omarchy never sets AQ_DRM_DEVICES
#    and starts a DRM backend on every card, which forces a software cursor on the NVIDIA
#    card and blocks direct scanout.
#    ~/.config/hypr/hyprland.lua — resolve the path fresh at every login:
#      local p = io.popen("readlink -f /dev/dri/by-path/pci-0000:01:00.0-card 2>/dev/null")
#      local c = p and p:read("*l") or ""
#      if p then p:close() end
#      if c:match("^/dev/dri/card%d+$") then hl.env("AQ_DRM_DEVICES", c) end
#    You cannot pass the by-path name directly — its colons are AQ_DRM_DEVICES' list separator (#8776).
#    cardN numbering is not stable across boots, hence readlink at each login.
```

**Plug your monitor into the RX 9060 XT, not the RTX 3060.** This one hardware choice defuses
most of Omarchy's dual-GPU bugs: it puts `boot_vga=1` on AMD, which makes
`omarchy-hw-nvidia-display` return false, which makes Omarchy stop forcing
`LIBVA_DRIVER_NAME=nvidia`. You get a clean AMD compositor and a pure-compute NVIDIA card with no
patches.

**Don't click the "Hybrid GPU" menu item.** `omarchy-hw-hybrid-gpu` just counts display-class
devices (you have 3, or 2 with the iGPU off) with no desktop awareness, so it returns true. The
toggle would install `supergfxctl` and enable hybrid mode, which is meaningless on a desktop
with no MUX.

**Don't use Omarchy's `Install > AI > Ollama` menu entry.** It tests `nvidia-smi` first, so it
will install `ollama-cuda` (~3GB) and never offer you the AMD card. Install Ollama yourself, or
skip it for llama.cpp.

**Size `/boot` (ESP) at 2GB or more.** With two dGPUs, Omarchy's initramfs keeps the `kms` hook
and grows to ~273MB, plus a ~280MB UKI, plus kernel + fallback + Snapper entries on the same ESP.
Omarchy issue #13357 reports a 2GB ESP being exhausted on exactly this kind of box.

### Your GPU strategy (this part matters as much as the BIOS)

**Do not split one model across both GPUs. Run two independent llama-servers, one per GPU.**

The reason is bandwidth, and the numbers are not what you'd assume:

| | RTX 3060 12GB | RX 9060 XT 16GB |
|---|---|---|
| Memory bandwidth | **360 GB/s** | **320 GB/s** |
| VRAM | 12 GB | 16 GB |
| Architecture | Ampere, GA106 | **RDNA 4**, `gfx1200` (not RDNA 5) |
| Backend maturity | CUDA — the reference path | Vulkan solid; ROCm officially lists gfx1200 as of ROCm 10.0.0 |

The 9060 XT has *less* memory bandwidth than the 3060 (320 vs 360 GB/s), and the commonly-quoted
448 GB/s is the 3060 Ti / 3080 figure, not this card. Its real advantages are the 16GB and the
2× matrix throughput — and that 2× doesn't help, because a Q4 decode is bandwidth-bound, not
compute-bound, and llama.cpp's WMMA/MMF path on RDNA4 isn't delivering a FLOPS win anyway
(upstream: "on RDNA the WMMA instructions do to my knowledge not increase peak FLOPS").

**Why splitting loses:** every generated token requires streaming every weight through the
memory system exactly once. Splitting the model across two GPUs does not reduce total bytes
moved per token — it adds a serialization point at the layer boundary, over PCIe, through host
RAM, with no P2P path between vendors. llama.cpp's own docs: "pipeline-parallel maximizes batch
throughput; tensor-parallel minimizes latency… bottlenecked by GPU interconnect speed." And
`--split-mode tensor`, which *would* pool properly, is documented as "no guarantees" outside
CUDA and has confirmed crashes on mixed builds (issue #25594, `GGML_ASSERT` with `-sm tensor`).

Worse, your 3060 is in a chipset-attached slot. On this board only PCIEX16_1 is CPU-attached
(PCIe 5.0 x16); PCIEX16_2 is a chipset slot that is **electrically only x4**, and PCIEX4 is
chipset x4. A non-P2P topology is exactly what produced garbage output above 2048 context in
llama.cpp issue #20052. Unrelated to a two-server setup, but a real reason to never split.

**Setup:**

```bash
# Two separate build dirs — one backend each, so there's no cross-vendor scheduler
# weirdness and no chance of hitting the mixed-build bugs.
cmake -B build-cuda   -DGGML_CUDA=ON   -DCMAKE_BUILD_TYPE=Release
cmake -B build-vulkan -DGGML_VULKAN=ON -DCMAKE_BUILD_TYPE=Release

# Server 1 — RTX 3060, CUDA, 12GB. Faster per-card. 8B Q6_K, or 14B Q4_K_M.
CUDA_VISIBLE_DEVICES=0 ./build-cuda/bin/llama-server \
  -m /models/8b-Q6_K.gguf --host 127.0.0.1 --port 8081 \
  -ngl all -fa on -c 16384 --cache-type-k q8_0 --cache-type-v q8_0 -t 16

# Server 2 — RX 9060 XT, Vulkan, 16GB. Bigger models. 14B Q5_K_M, 20B Q4_K_M.
# Run `vulkaninfo` to find the AMD card's Vulkan index first — order isn't guaranteed.
GGML_VK_VISIBLE_DEVICES=<amd_idx> ./build-vulkan/bin/llama-server \
  -m /models/14b-q5_k_m.gguf --host 127.0.0.1 --port 8082 \
  -ngl all -fa on -c 16384 --cache-type-k q8_0 --cache-type-v q8_0 -t 16
```

Load-balance with nginx in front of both ports. Two servers give you roughly 2× aggregate
throughput and full native-backend performance on each card, with none of the multi-GPU failure
modes.

`-ngl all` and `-t 16` — **physical** core count, not 32. Fully offloaded, llama.cpp's own
troubleshooting data shows `-t 1` → `-t 7` nearly doubles throughput; oversubscribing threads makes
them contend with the GPU's command queue. If you ever do run layers on the CPU, the 7950X's
2 CCDs are a known llama.cpp trap (issue #4716: a 7950X at 3.37 tok/s lost to a 12-core 5900X) —
confine to one CCD with `taskset` and keep DDR5 at full speed.

**If you need one model bigger than 16GB:** a third Vulkan-only build with both cards visible is
the only thing that pools your 28GB. Treat it as a capacity tool, not a speed tool. Pin the
llama.cpp version after testing (issue #28353 has a regression that tears down the secondary
GPU's allocation mid-load and hangs the process unkillably), use the default `--split-mode layer`,
let it auto-split by free VRAM, and **verify output coherence at your target context length**
before trusting it.

**Quant choice: Q4_K_M.** It's the best-tested quant on every backend. IQ-quants (IQ4_XS,
IQ3_XXS) win on quality-per-GB and are now much faster on RDNA4 Vulkan than they were, but
upstream still carries the comment "some quants are not performant on RDNA4, those fall back to
FP16 matmul." Benchmark before choosing one.

**Best use of the asymmetry — speculative decoding.** llama.cpp lets the draft model have its own
device list, which is exactly your two-server situation:

```bash
./build-both/bin/llama-server -m /models/main-14B-Q4_K_M.gguf \
  -md /models/draft-1B-Q4_K_M.gguf --spec-type draft-simple --spec-draft-n-max 5 \
  --device <amd> --spec-draft-device CUDA0 --spec-draft-ngl all \
  -ngl all -fa on -c 16384
```

Realistic gain is 1.5–2.5× on generation with a well-matched draft. Two caveats: `draft-mtp`
roughly halves prompt processing on multi-GPU layer split (#27428), and speculative output has
been reported to diverge from vanilla on quantized targets (#25618) — validate output quality,
especially with i-quants.

**Skip vLLM entirely.** Its guidance is CUDA/NCCL-centric and it has no path for a CUDA+AMD pair.

---

## Explicitly unconfirmed

- Whether **1.10V SoC** works for 2×32GB 6000 CL30 on *your* 7950X sample. No supporting reports
  exist; assume 1.20V and hunt downward with tests.
- Exact watt deltas for: `SoC/Uncore OC Mode = Disabled`, `Integrated Graphics = Disabled`,
  `Memory Voltage Switching Frequency`, FCH USB port disables, chipset ACP gating. Directionally
  certain from ASUS's own documentation, but nobody has published controlled measurements. The
  `Preference = Power Efficient` and SoC-voltage levers dwarf all of these anyway.
- Whether **BIOS "Integrated Graphics: Disabled" actually removes the iGPU from the PCI bus** on
  this board. A 7950X owner on an ASUS X670 board reports it did not. Verify with `lspci`.
- Whether the **9.4W→?** effect of DDR5-6000 vs 4800 on idle is real. The mechanism is
  defensible (higher SoC voltage, worse C-state entry efficiency) but the magnitude is
  unmeasured. Expect single-digit watts.
- Whether **X670-series PCIe bifurcation** exists as a documented table. ASUS published the
  image header-only. Irrelevant for a 7950X (slot is x16, no bifurcation needed).
- Whether the **7950X shows "Core 0-15" or per-CCD entries** in Curve Optimizer. The 2023 manual
  says "Core 0-5" as generic AM5 boilerplate. Irrelevant unless you enable CO.
- Whether **Omarchy's `--filter` / "Hybrid GPU"** menu items misbehave on a desktop with 2–3
  dGPUs. Almost certainly, per the code, but nobody has reported a desktop with two discrete
  cards from different vendors.

---
type: note
category: Rig & Hardware
tags: [omarchy, rig-hardware]
updated: 2026-09-26
publish: true
created: 2026-09-26
machine: bigrig
title: "Hardware Specs & Roles — Rig Fleet (Sep 2026)"
featured: 13
summary: "Which of my three machines does what, with their parts: the AI desktop, the Unraid server and the laptop, as of September 2026."
---

# Hardware Specs & Roles — Rig Fleet (Sep 2026)

> **Interactive 3D board visual:** [Open in browser](file://~/Documents/Obsidian/attachments/motherboard-3d.html) — hover parts for specs, exploded view + camera presets.
> (Obsidian blocks html links in some versions — if the link doesn't click, open `attachments/motherboard-3d.html` from your vault folder, or Ctrl+click it.)


> Spec snapshot + role-fit analysis for LLM serving and Unraid hosting, with comparison visuals.
> Verified live: Sep 25, 2026 (nvidia-smi, lspci, amdgpu sysfs, inxi).

---

## 1. Spec sheet

### Machine A — "MASSIVE-RIG" (AI workstation, Omarchy)
| Component | Spec | Notes |
|---|---|---|
| CPU | Intel i5-13600K (14C/20T, P+E) | 5.1 GHz max, no ECC |
| Board | MSI PRO Z690-A WIFI **DDR4** (MS-7D25) | BIOS A.N0 03/2026, no IPMI |
| RAM | 64 GB DDR4-3200 (4x16, 2DPC) | Silicon Power + mixed, 2 DIMMs/channel |
| GPU 1 | **RX 9060 XT 16 GB** (Navi 44, RDNA4) | PCIe 5.0 x16 @ CPU PEG — 32 GT/s x16, full |
| GPU 2 | **RTX 3060 12 GB** (Zotac, GA106) | PCIe 4.0 x16 slot; link idles at Gen1 x4, ramps on load |
| NVMe | ORICO J20 Pro 1 TB | PCIe 4.0 x4 (CPU lanes) |
| SATA | Team T2532TB 2 TB + Crucial MX500 1 TB | 6 Gb/s |
| Disks | 3.82 TiB total local | |
| Role | LLM inference: 9060 XT + 3060 via Vulkan layer split | Swift-Qwen3.8-27B Q5_K_M, 128K ctx, MTP n=2 |

### Machine B — "Unraid" (server, Unraid OS)
| Component | Spec | Notes |
|---|---|---|
| CPU | Intel i5-12600KF (12C/16T) | no iGPU (KF) |
| RAM | 128 GB DDR4-3200 (4x32) | big cache/vm headroom |
| GPU | RTX 3060 12 GB (LHR) | on bus 01:00, link state check needed |
| HBA | Broadcom/LSI SAS2308 (PCIe 3.0) | Serial Attached SCSI controller |
| Disks | HGST 4 TB (SATA) + 2x Seagate Exos 2 TB + WD 14.6 TB (SAS) | USB 2.0 FD boot |
| NVMe | WD Black SN850X 1 TB + Samsung SM961 512 GB | parity/appdata/cache candidates |
| NIC | Intel I219-V 1 GbE | onboard |
| Role | NAS + Docker self-hosting, uptime-sensitive (websites/apps) |

### Machine C — "New build" (planned AMD board, parts arriving)
| Component | Spec | Notes |
|---|---|---|
| CPU | Ryzen 9 7950X (16C/32T) | AM5, no ECC |
| Board | ASUS TUF X670E-Plus WiFi | X670E dual chipset |
| RAM | 64 GB DDR5-6000 (EXPO) | ~90 GB/s effective dual-channel |
| NVMe | Samsung 980 Pro 1 TB | goes in M.2_1 (Gen5 x4 CPU lanes) |

### Retired/available parts
| Part | Spec | Where |
|---|---|---|
| 2nd RTX 3060 12 GB | same as above | spare (candidate for dual-3060 CUDA rig) |

---

## 2. PCIe lane map — Machine A (verified)

```
CPU (i5-13600K)
 ├─ PEG5 x16  → RX 9060 XT        32 GT/s x16  ✔ full speed
 ├─ PEG4 x4   → ORICO NVMe        16 GT/s x4   ✔ full speed
 ├─ PEG4 x16* → RTX 3060          idles Gen1 x4, ramps to Gen4 x16
 └─ PCH (DMI)
     ├─ 6x SATA   (Team 2TB, MX500 1TB)
     ├─ 2.5G I225-V LAN
     └─ empty chipset slots (future HBA)
```
*3060 sits in a CPU-attached Gen4 x16-capable slot; idle link downtrains by design (ASPM power saving). Under load it trains Gen4 x16.

## 3. PCIe lane map — Machine C (planned, from ASUS spec)

```
CPU (7950X)
 ├─ PCIEX16_1  Gen5 x16 (CPU)   → GPU #1 (9060 XT or 3060)
 ├─ M.2_1      Gen5 x4  (CPU)   → 980 Pro (does NOT steal GPU lanes)
 └─ X670 chipset (dual Prom21)
     ├─ PCIEX16_2  Gen4 x4 (chipset) → GPU #2
     ├─ M.2_2      Gen3 x4 (shares bandwidth with SATA6G_1&2!)
     ├─ M.2_3/4    Gen4 x4
     └─ 4x SATA
```
Key trap: M.2_2 disables SATA ports 1&2 if used at x4. Put boot NVMe in M.2_1 or M.2_3.

---

## 4. How they fit — LLM serving

### Physics that decide speed
| Workload | Bottleneck | Lever |
|---|---|---|
| Decode, model fully in VRAM | VRAM bandwidth | VRAM clock offset (OC), not CPU/RAM |
| Decode, experts offloaded to RAM | System RAM bandwidth | RAM speed (XMP/EXPO), fewer resident experts |
| Prefill | GPU compute + ubatch size | `-ub 1024-2048`, more GPU layers on fastest card |
| Multi-GPU layer split (cross-vendor) | Slowest inter-GPU hop (no P2P over Vulkan) | Order/split tuning; PCIe helps decode slightly |
| Multi-GPU same-vendor split | PCIe P2P available | Works well, cheaper than RAM bounce |

### Machine A serving notes (current, verified)
- 27B Q5_K_M ≈ 20 GB → fits split 16+12 GB with 128K q8_0 KV + MTP n=2.
- Layer split `-ts 16,11` is correct for AMD+NVIDIA (no NVLink → row split loses).
- Cross-vendor handoff = GPU→PCIe→RAM→PCIe→GPU per boundary; capacity lane, not speed lane.
- 62 GB RAM = ~28 GB used by server; tight with agents running. 96 GB (Machine C DDR5) fixes the ceiling.

### Machine C expectations
- DDR5-6000 dual-channel ≈ 90 GB/s vs DDR4-3200 ≈ 51 GB/s → **+60-75% decode on any RAM-offloaded run**.
- 7950X (16C) helps prefill dispatch and `-t 16` CPU-side MoE; irrelevant for GPU-resident decode.
- Same x16/x4 GPU topology as Z690 → no GPU-lane upgrade, but better VRAM-fit headroom via faster RAM pool for offload.

### Machine B serving notes
- RTX 3060 12 GB alone: fine for ≤13B Q4/Q5 single-GPU, or as an endpoint for small models.
- 128 GB RAM is the real LLM asset: CPU-only or expert-offload serving of big MoE is viable here, but 1 GbE caps network serving speed (token streams are tiny; model load time is the real cost).

---

## 5. How they fit — Unraid hosting

- **Machine B (keep as Unraid)**: LSI SAS2308 HBA handles 3 SAS drives (~750 MB/s combined) — nowhere near Gen3 x4 (3.9 GB/s) ceiling. x16 vs x4 irrelevant for spinning rust. Idle PCIe downtrains are power saving; they ramp.
- **Z690 → Unraid candidate**: 6 SATA + iGPU transcoding + fresh board. Loses nothing the server needs; gains uptime-vs-old-board if the current one is aged.
- **Machine C must NOT be Unraid**: its value is bandwidth (DDR5 + Gen5 lanes) which servers can't use, and its x16/x4 GPU layout is wasted on NAS duty.

```
                  ┌───────────────────────────────────────┐
                  │              LAN 1 GbE                │
                  └──────┬──────────────┬─────────────────┘
                         │              │
        ┌────────────────▼───┐   ┌──────▼─────────────────┐
        │  UNRAID (Machine B)│   │  AI RIG (A→C upgraded) │
        │  128GB RAM         │   │  9060 XT + 3060 (+2nd) │
        │  SAS array via HBA │   │  Vulkan layer split    │
        │  Docker/websites   │   │  llama-server :8080    │
        │  NFS/iSCSI exports │   │  24/7, GPU-bound       │
        └──────────▲─────────┘   └────────────────────────┘
                   │  model files over LAN (one-time load)
```

---

## 6. Comparison — the three machines

### Bandwidth hierarchy (the only ladder that matters for LLM)
```
Machine            RAM BW        VRAM BW (GPU)        Decode ceiling (offloaded)
─────────────────────────────────────────────────────────────────────────────
A  Z690/DDR4-3200  ~51 GB/s      9060XT ~322 GB/s*    ~10-17 t/s (Q5-class)
C  X670E/DDR5-6000 ~90 GB/s      same GPUs            ~16-28 t/s (same models)
B  Unraid DDR4-3200 ~51 GB/s      3060  ~360 GB/s      ~10-15 t/s (single 3060)
*RDNA4 GDDR6 ~20 Gbps × 256-bit
```

### Role matrix
| | Machine A (now) | Machine B (Unraid) | Machine C (new) |
|---|---|---|---|
| GPU-resident decode | ★★★ | ★★ (single 3060) | ★★★ (same GPUs) |
| RAM-offload decode | ★★ | ★★★ (128 GB!) | ★★★★★ (DDR5) |
| Prefill | ★★★ | ★★ | ★★★★ (7950X) |
| NAS/parity | ★ | ★★★★★ | ★ |
| Docker/services | ★★ | ★★★★★ | ★★ |
| Uptime hosting | ★★ | ★★★★★ (target) | ★★ |
| Power draw | ★★ | ★★★★ (no big GPU) | ★★ |

### Upgrade logic (one sentence each)
- **GPU-resident only?** Machine C gains ~nothing; keep A.
- **Ever offload (Flash-Next, 176B class)?** Machine C's DDR5-6000 is the single biggest decode lever money can buy (~+60%).
- **Unraid uptime?** Keep B as server; add UPS + spare boot stick instead of hardware.

---

## 7. Action items (carried from research session)

1. Machine A: `nvidia-smi -pl 187 --lock-gpu-clocks=2130 -pm 1` (root script).
2. Machine A: AMD `pp_power_profile_mode=compute` (or LACT) + Overdrive unlock for undervolt-OC.
3. Machine C build: 980 Pro → **M.2_1**, GPU1 → **PCIEX16_1**, GPU2 → **PCIEX16_2**; avoid M.2_2 (kills SATA 1&2).
4. Unraid: SAS HBA fine as-is; consider moving it to Z690's chipset x16 slot only if you exceed ~6 drives.
5. Uptime kit: UPS + cloned Unraid boot USB + parity-check schedule.

*Sources: live `nvidia-smi`/`lspci`/amdgpu sysfs reads; ASUS TUF X670E-Plus WiFi techspec/manual; llama.cpp multi-gpu docs (layer vs row, cross-vendor no-P2P); r/LocalLLaMA power-limit benchmarks; CraftRigs XMP/EXPO-for-LLM guide.*

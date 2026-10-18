---
type: hardware
topic: MASSIVE-RIG
updated: 2026-10-17
category: Rig & Hardware
tags: [rig, hardware, display, hyprland]
publish: true
created: 2026-09-23
machine: bigrig
title: "Rig Hardware & Display"
---
# Rig Hardware & Display
> [!warning] Current configuration (verified 2026-10-17)
> Observed on this machine today: AMD Ryzen 9 7950X (16 cores, 32 threads) on an ASUS TUF Gaming X670E-Plus WiFi board; 63,426 MiB (about 62 GiB) of RAM visible to the OS; one NVIDIA Tesla V100 PCIe 32 GB plus the AMD Raphael integrated GPU. lspci shows no RTX 3060 or RX 9060 XT.
> - i5-13600K on the MSI Z690-A with RX 9060 XT + RTX 3060: the first setup run (2026-09-15) through this note's 2026-09-23 update.
> - Ryzen 9 7950X: in use by 2026-09-28 ([[Flash-Next llama.cpp Audit 2026-09-28]]).
> - 2x RTX 3060 with the 9060 XT removed: 2026-09-29 ([[MASSIVE-RIG]]).
> - RX 9060 XT back beside one RTX 3060, V100 pending: 2026-10-08 ([[Philosopher dsh Backend]]).
> - Tesla V100 32 GB with the Raphael iGPU: 2026-10-13 ([[Strata V100 setup and benchmarks — 2026-10-13]]).


**Category:** [[Rig & Hardware]] · **Vault:** [[Vault Map]]

The MASSIVE-RIG box ([[Qwen3.8 Rig]] is the index; [[Model Benchmarks]] is the scoreboard).
Everything here came out of the first setup run (2026-09-15) and later diagnostics.

## Hardware

- **MSI PRO Z690-A WIFI DDR4**, i5-13600K (14C/20T), 62 GB DDR4 (was 32 GB until 2026-09-20), kernel 7.2.3-arch1-3. (superseded, see Correction above)
- GPUs, in Vulkan index order: **Vulkan0 = AMD RX 9060 XT 16 GB** (Navi 44, x16 Gen5, Resizable BAR on), **Vulkan1 = RTX 3060 12 GB** (driver 610.57.04, CUDA 13.3, lives in the **x4 Gen3** slot). The **Intel UHD 770 iGPU drives the display only** — it must stay out of inference ([[GPU Crash & Vulkan Device Pinning]]). (superseded, see Correction above)
- Disks: 1 TB NVMe (LUKS + btrfs, Omarchy), 1 TB `crucialmx` NTFS (old Windows, mounted **read-only**), 2 TB exFAT `MainBackup` (rw). `crucialmx` mount used: `mount -t ntfs3 -o ro,uid=$(id -u),gid=$(id -g) /dev/sdb3 /mnt/crucialmx`.
- Bootloader **Limine** under Omarchy; `/etc/kernel/cmdline` is the durable kernel-flag edit point (limine-entry-tool regenerates `limine.conf` from it).

## Display: 1440p 120 Hz VRR, and why not 240

- iGPU → monitor over **HDMI** (motherboard port), AMD display output disabled. Locked at **2560x1440 @ 120 Hz VRR**.
- 144 / 180 / 240 Hz all produced **pink horizontal flashes** = HDMI FRL link instability at the bandwidth edge (panel EDID: 48–240 Hz, max pixel clock 1200 MHz, HDMI Forum VSDB). A **DisplayPort cable is the clean 240 Hz path** (~$10, iGPU only) — still unbought.
- Live monitor changes need `hyprctl eval 'hl.monitor({...})'`; plain `hyprctl keyword monitor` is rejected by current Hyprland. Persistent config in `~/.config/hypr/monitors.lua`.

## GPU speed physics (measured, IQ2_XS instrument, no-spec, pp4096/tg128)

| lane | prefill t/s | decode t/s |
|---|---|---|
| AMD 9060 XT solo | 602 | 27.4 |
| NVIDIA 3060 solo | 428 | 16.4 |
| split 15,11 (both) | 599 | 27.5 |

- The **x4 slot is NOT the bottleneck** — 3060 VRAM bandwidth (~360 GB/s vs AMD ~645 GB/s) is.
- **Slowest device gates decode**: a layer split never beats the fast card alone for dense decode. A 2nd 9060 XT would ~2x decode; a 2nd 3060 buys prefill/KV headroom only. (See [[Dual Tesla P100 vs 2nd 9060 XT]].)
- Splitting a small-active MoE across both cards *hurts* decode (Ornith IQ2_M 99 → 61 t/s) but helps prefill slightly.

## Permanent crash rules

- **One GPU workload at a time**; verify VRAM fully drained between runs (idle baseline ~355–363 MiB).
- Model swaps = unload → verify → load. Wrapper `~/.local/bin/gpu-safe` enforces this (refuses with exit 42 while any llama process is alive).
- Never delete model files without per-file consent.
- Machines must never crash: a hard crash was caused by an un-exited `llama-bench` still holding ~14 GB colliding with a second run → `amdgpu: Not enough memory for command submission!` → compositor down.

## Related

[[Qwen3.8 Rig]] · [[Model Benchmarks]] · [[GPU Crash & Vulkan Device Pinning]] · [[Fan Control (MSI Z690-A)]] · [[Omarchy Trim Debloat & Idle Policy]]

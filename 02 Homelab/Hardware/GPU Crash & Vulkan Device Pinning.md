---
type: troubleshooting
topic: llama-server SIGABRT
updated: 2026-09-23
category: Rig & Hardware
tags: [rig, vulkan, gpu, troubleshooting]
publish: true
created: 2026-09-23
machine: bigrig
title: "GPU Crash & Vulkan Device Pinning"
featured: 16
summary: "Our AI server kept crashing; the trace showed it was secretly using the weak display chip, and one setting fixed it."
---
# GPU Crash & Vulkan Device Pinning

**Category:** [[Rig & Hardware]] · **Vault:** [[Vault Map]]

Root cause of the recurring `llama-server` SIGABRT (2026-09-16), proven from coredump + dmesg.

## The chain

1. 11:38:44 kernel `Fence expiration time out i915 ...:llama-server[23594]`
2. 11:38:53 `llama-server context reset due to GPU hang` on `0000:00:02.0` — **the UHD 770 iGPU**
3. ggml-vulkan `ErrorDeviceLost` on every `waitForFences` (ggml-vulkan.cpp:2671)
4. uncaught `vk::DeviceLostError` in `vk_queue_handle_unsynchronized::submit` → `std::terminate` → `abort()` = SIGABRT

A separate OOM killer killed llama-server restarts at 11:35 and 11:37 (30/30 GiB) — two failure modes, one session.

## The actual config bug

`Vulkan0` was the **Intel iGPU**, so every "both dGPUs" run was really iGPU + 9060 XT, with the *bigger* share going to the iGPU (`-ts 15,11`); `llama-amd.service` ("RX 9060 XT only") was in fact running on the iGPU.

- iGPU VRAM reality: 160 MiB BIOS DVMT + ~519 MiB usable. Vulkan advertises a 23.23 GiB "device-local" heap but it is GTT-backed system RAM — anything past ~500 MiB is just eating system RAM and display bandwidth.
- Load source: Hyprland compositing 1440p120 VRR (a real workload) plus 15/26 model layers.

## Fix (verified)

llama.cpp accepts only `VulkanN` indices, not device names, so each systemd unit **pins device order with `GGML_VK_VISIBLE_DEVICES`**:

- `GGML_VK_VISIBLE_DEVICES=1,2` → Vulkan0 = RX 9060 XT, Vulkan1 = RTX 3060, **iGPU invisible**.
- Units renumbered: `llama-server` (AMD+3060 `-ts 16,11`), `llama-server-deep`, `llama-amd`, `llama-nv`.
- `-ts 12,12` / `16,12` **fail** (MTP context doesn't fit on the 3060) — `-ts 16,11` is the working split.
- Verified live: `llama-switch mtp` → health `{"status":"ok"}`, 30-token completion served, NVIDIA at 11.8 GiB, iGPU untouched.

## Notes

- i915 GPU hangs on Alder/Raptor Lake are a known kernel/Mesa issue, **not an Omarchy bug**. Diagnose with `dmesg | grep -A20 "GPU HANG"`; fix by keeping linux + mesa current.
- Left open at the time: the AMD card held ~16.4 GiB in **GTT** (system-memory fallback) with only 57 MiB in VRAM — worth a decode-speed re-check to confirm no spill.

## Related

[[Rig Hardware & Display]] · [[Qwen3.8 Rig]] · [[Hermes Install & Config Port]]

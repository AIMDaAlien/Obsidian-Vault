---
type: benchmark-log
topic: MASSIVE-RIG
publish: true
created: 2026-09-29
tags: [omarchy]
updated: 2026-10-17
machine: bigrig
title: "MASSIVE-RIG"
featured: 39
summary: "We tried every common speed-up on a home AI server; most did nothing, and measuring that saved real money."
---
# MASSIVE-RIG
MASSIVE-RIG is the Omarchy desktop that serves the local models (see [[Rig Hardware & Display]] for its hardware, which changed several times). This log records dated work entries from 2026-09-26 to 2026-09-29: the interactive motherboard render, the switch to two RTX 3060s, re-fitting the daily Qwen lane, power-cap and BIOS/EXPO measurements, and Flash-Next expert traffic to NVMe.



## 2026-09-26 11:22
**Done:** Rebuilt the render layer of the interactive motherboard-3d.html (Obsidian attachment) from flat untextured primitives into a lit PBR scene: procedural studio IBL, ACES + sRGB pipeline, generated PCB texture (solder mask, traces, vias, gold fingers, silkscreen), real axial fans, beveled heatsinks, correct ATX scale/layout, soft shadows. 448 draw calls / 36k tris.
**Findings:** three r128 has NO colour management, so turning on `outputEncoding = sRGBEncoding` re-encodes hex-authored colours and makes every dark material render ~8x too bright (pastel plastic look) — fix is `new THREE.Color(hex).convertSRGBToLinear()` at the material factory. Metals need something to reflect: a PMREM `fromScene()` studio (softboxes as >1.0 radiance MeshBasicMaterial planes) transforms the look more than any texture. A large lit floor plane throws a broad grazing Fresnel lobe that ends up brighter than the subject and inverts the hierarchy — use a dark diffuse-only floor. Straight-down `lookAt` gives the camera arbitrary roll; keep a small z offset in top-down presets.
**Recommendations:** Verify 3D work headlessly with `chromium --headless --enable-unsafe-swiftshader --use-angle=swiftshader --screenshot`, and probe pixels by patching `HTMLCanvasElement.prototype.getContext` to force `preserveDrawingBuffer:true` — guessing at material values from screenshots alone wasted several iterations.

## 2026-09-26 11:30
**Done:** Fixed unusable framerate on the interactive motherboard render running in Zen on the Intel iGPU. Three root causes: continuous rAF re-rendering a 2048² shadow map over 448 meshes every frame for a static scene, MSAA at DPR 2 with a heavy PBR fragment shader, and no quality tiering. Now: on-demand rendering (verified 0 frames rendered while idle), shadow map rebuilt only when the explode state changes, plus a GPU-tier probe before renderer creation that drops MSAA, DPR, soft shadows and bump maps on weak backends.
**Findings:** `antialias` is fixed at context creation, so the GPU must be probed on a throwaway canvas *before* building the WebGLRenderer. Big one: `renderer.setSize(w,h,false)` (updateStyle off) is a trap — a `<canvas>` is a *replaced* element, so `position:fixed; inset:0` with `width:auto` resolves to the intrinsic drawing-buffer size, not the viewport. The box then tracks the buffer and setSize() shrinks the canvas ~20% per frame at any pixel ratio ≠ 1. Invisible at DPR 1.0, catastrophic at 0.8. Also: `WEBGL_debug_renderer_info` strings vary wildly (ANGLE/Vulkan radv vs native Mesa), so classify fail-safe — anything not a recognisable dGPU is treated as weak.
**Recommendations:** Render on demand for any static 3D scene — it is free and removes idle GPU load entirely. Verify both quality tiers render, not just the fast path; a fractional pixel ratio is what exposed the setSize bug.

## 2026-09-29 08:42
**Done:** GPU layout changed to 2x RTX 3060 12GB (RX 9060 XT 16GB removed; may return on an x4 slot). Both cards capped at 100W and made persistent via /etc/systemd/system/gpu-nv-power.service (now enabled, RemainAfterExit, per-card -i N -pl). Enabled persistence mode; PCIe ASPM set to performance. RGB fully off - the boot service had been loading a non-existent profile path (openrgb saves "off.orp" as "off.orp.orp"); fixed and the board/DIMMs are dark.

**Findings:** The 100W cap binds nothing: 70-73W drawn under inference load, SM 1807-1965MHz of an 2130MHz max, 47-54C. Memory clock (7501MHz) is both current and max, so it is NOT overclockable via nvidia-smi, and nvidia-settings is not installed for an X-side offset. SM clock lock needs root - script staged at ~/gpu-oc.sh (revert: ~/gpu-oc.sh revert).

**Gotchas:** The daily Swift-27B lane crash-looped on the new layout - its -ts 16,11 assumed the 16GB AMD card; now -ts 12,11. Any lane with hardcoded -ts/-dev needs re-checking after a GPU swap.

**Recommendations:** Run `sudo bash ~/gpu-oc.sh 2100` to unlock the SM headroom, then re-measure. Full detail: ~/Work/ops/flashnext-2x3060-retune.md

## 2026-09-29 10:24
**Done:** Re-fitted the daily Swift-Qwen3.8-27B Q5_K_M lane after the GPU swap. Losing the 16GB AMD card cut the pool from 28GB to 24GB, and the 19.2GB weights no longer left room for q8_0 KV - it crash-looped with "failed to allocate buffer for rs cache".

**Findings:** On 2x12GB the 27B Q5 has only ~5.3GB for KV+compute+draft. Measured headroom: ctx131072/q8_0 = OOM; ctx98304/q8_0 = 447MiB; ctx65536/q8_0 = ~1000MiB; ctx131072/q4_0 KV = 799/828MiB. Shipped 131072 with q4_0 KV and -np 1 (single slot; the server otherwise sizes graphs for 4 slots), keeping the full 128K context at the cost of KV precision. Weights stay Q5_K_M.

**Gotchas:** Validated at depth, not on a short prompt - an 84,287-token prompt ran clean (251.1 t/s prefill) and a live request returned "DAILY OK" at 26.33 t/s decode with 0 restarts. llama-switch's health wait was 120s; a 19GB model load can exceed that and report a false failure, raised to 240s. Same trap bit the flash lane: configs that load and bench fine can OOM mid-request at depth.

**Recommendations:** If long-context recall degrades, fall back to -c 65536 with q8_0 KV. Revisit the Q5-vs-Q4 weight quant if 24GB keeps forcing quality trades.

## 2026-09-29 12:13
**Done:** Power-cap A/B on 2x RTX 3060. `sudo nvidia-smi -pl 170` (was 100W), 3 reps/lane, cache_prompt=false, GPU sampled throughout.
**Findings:** The 100W cap WAS binding - `SW Power Cap: Active`, 74-89W/card, clocks 1410-1965 MHz (max 2130), cumulative capped time ~78 min. At 170W: flash lane (single 3060, 176B MoE, all experts CPU) prefill 287.92 -> **300.15 t/s** (+4.2%), decode 15.72 -> 16.12 (+1.2%), GPU0 now drawing 125-128W. Daily 27B lane: prefill **349.58 t/s**, decode **15.79 t/s** at 41,309-token depth, GPU0 up to 146.9W / GPU1 128.2W (was clamped at ~89W). Temps 63-74C.
**Also:** the SM clock lock is fiction on driver 610.57.04 - no "Locked Clocks" section, `-ac` deprecated, and a same-prompt A/B gave 288.06 t/s "locked" vs 287.92 unlocked. Memory clock already at max (7501 MHz).
**Recommendations:** Keep 170W (persist via `sed -i 's/-pl 100/-pl 170/g' /etc/systemd/system/gpu-nv-power.service`). Next: EXPO 4800->6000 (biggest remaining flash lever), then a matched 100W re-baseline for the 27B lane.

## 2026-09-29 12:45
**Done:** EXPO + mobo AI-OC enabled; post-BIOS flash re-measurement. Also sized the RAM-fit and weight-mapping questions.
**Findings:** EXPO and AI OC gave NO measurable win. EXPO is live (dmidecode "Configured Memory Speed: 6000", the "4800" was the JEDEC fallback line) but triad BW only 55.8 -> 59.6 GB/s, within its own repeat spread. AI OC did raise CPU max to 5,883 MHz, no WHEA/MCE. Flash @100W: warm reps 290.79/291.82 (mean 291.31) vs 287.92 baseline = +1.2% noise. **The real signal: first request after a boot costs -10.5% (261 vs 291 t/s) while page cache refills across 79 GiB of experts - warm up after reboots.**
**RAM wall:** 79.1 GiB model into 61 GiB RAM; break-even to fit = 2.62 bpw. Any 3-bit quant still spills (Q3_K_S 72.1, IQ3_XXS 63.0 GiB); only ~2.5 bpw fits (IQ2_S 51.5 GiB) = 2-bit territory, real quality cost. 27B: Q6_K 20.6 GiB needs THREE GPUs (on 2x3060 only 3.4 GiB left for KV); on 40 GiB, Q8_0 fits too. 27B Q6 on 3 GPUs beats Flash-Next on speed + precision, loses on knowledge breadth.
**Recommendations:** Ruled-out list is now long (EXPO, AI OC, CUDA, build updates, AVX-512, op-offload, governor, EPP, THP, swappiness, SM lock-is-fiction). Weight mapping is capped at ~2% (per-layer granularity, no expert cache). Real remaining levers: draft-model spec decoding, ik_llama.cpp, OpenBLAS build, vmtouch -l. Handoff written: ~/Work/ops/flashnext-continuation-prompt.md

## 2026-09-29 12:58
**Done:** Sized the NVMe share of Flash-Next expert traffic with block-device read deltas.
**Findings:** Storage is a COLD-START cost, not a steady-state bottleneck. Cold 5,068-tok prompt: 1,807.9 MB off disk = 357 KB/token = ~23% of the ~1.54 GB/token expert traffic (that IS the -10.5% first-request penalty). Warm 2,416-tok prompt: 55.9 MB = 23 KB/token = ~1.5%. So once warm the hot expert set is RAM-resident (MoE routing is skewed) and the 25 GiB that cannot fit costs almost nothing. At 16 t/s decode the lane streams ~1.52 GB/token from RAM = 24 GB/s vs ~58-60 GB/s triad peak (~40%), so the ceiling is CPU memory bandwidth/latency, NOT the SSD.
**Recommendations:** Faster storage buys nothing here; do not chase it. Levers that match the real bottleneck are kernel work (ik_llama.cpp, OpenBLAS build) and smaller bytes-per-token. vmtouch -l is bounded by the 1.5% warm figure, not the 23% cold one. Warm up after every reboot.

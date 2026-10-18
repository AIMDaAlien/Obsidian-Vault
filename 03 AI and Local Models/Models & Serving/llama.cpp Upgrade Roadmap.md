---
type: ops
topic: llama.cpp versions
updated: 2026-09-23
category: Models & Serving
tags: [llama.cpp, versions, ops]
publish: true
created: 2026-09-23
machine: bigrig
title: "llama.cpp Upgrade Roadmap (rig + Unraid)"
---
# llama.cpp Upgrade Roadmap (rig + Unraid)

**Category:** [[Models & Serving]] · **Vault:** [[Vault Map]]

Quality-neutral throughput/stability upgrades found on 2026-09-21 (rig still un-upgraded at that point).

## Rig (Arch packages, tier-1)

- Rig was on build **b10809 (0.4.0-dev)**, **296 commits behind master**; nightlies are now published as releases with a prebuilt `ubuntu-vulkan-x64` tarball (b11102 at the time).
- `pacman -Syu` → llama-cpp **0.4.0 → 0.4.1-1**, ggml-vulkan **0.23 → 0.24.0-2**, mesa **26.2.2 → 26.2.3-1**. All 4 serving regimes use `/usr/bin/llama-server`, so one update covers daily/deep/AMD/NV lanes. (No sudo in the agent shell — run via the user's update script.)
- 0.4.1 content that matters: Vulkan small-M-matrix qwen optimizations (#28457), Vulkan MoE topk fusion for prefill (#28422), NV queuesubmit driver workaround (#28830, 3060 stability), GDN normalization fix max→rsqrt (#28068), ggml v0.24 fixes.
- Dense 27B decode is **VRAM-bandwidth-bound (~29 t/s)** → expect prefill/TTFT + stability gains, not decode gains.

## Master-only wins (not in Arch 0.4.1)

Vulkan sparse Flash Attention #28105 (helps Ornith 35B-A3B on the 9060 XT) · Vulkan qwen4exp HC ops #28988 (Flash-Next class) · **Vulkan IQ3_S MMQ matmul kernels #28822 — direct hit, the AMD split lane is IQ3_S-mtp** · Vulkan IQ4_XS MMQ #28440 · **CUDA sparse flash-attention for qwen4 #28770 (merged Sep 20) — the marquee Unraid item**.

Rebuild qwen38-flash on master ≥ `bfd73a8` (b11102) for #28770 + CUDA 13.4.1.

## Unraid levers (measured)

- `-t` = **ALL logical CPUs (+17%: 14.5 → 16.9 t/s on IQ3_XXS)**.
- **CPU governor = performance** (a 2.3x move — confirm it isn't powersave).
- Keep `--load-mode none`, `q8_0` KV, `-ncmoe 48`.

## Do not chase

Speculative decoding on Unraid Flash-Next (measured dead on RAM-offloaded MoE) · any quant/KV downgrade (violates the no-quality-loss rule) · CPU governor on the rig (GPU-resident — no-op there).

## Forks evaluated — none beat upstream here

poolsideai `laguna` fork dead since Aug 4 · `ik_llama.cpp` active but CUDA-only (useless on the mixed rig) · BeeLlama is KV-tail/spec-decode = dead on RAM-bound MoE. Worth watching (unmerged WIP): 0cc4m's **vulkan-async / vulkan-coopmat** branches — the likely next real AMD win.

## Related

[[Flash-Next llama.cpp Audit 2026-09-28]] — what the Flash-Next lane's wall actually is (CPU MoE GEMM), every lever tested and closed
[[Rig Hardware & Display]] · [[Unraid LLM Control Center]] · [[Unraid Flash-Next]] · [[Qwen3.8 Rig]]

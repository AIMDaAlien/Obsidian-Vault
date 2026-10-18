---
type: note
topic: llama.cpp engine audit — Qwen3.8-Flash-Next 176B on the rig
updated: 2026-09-28
tags: [llama.cpp, serving, flash-next, audit, performance]
publish: true
created: 2026-09-28
machine: bigrig
title: "Flash-Next llama.cpp Audit (2026-09-28)"
featured: 43
summary: "Hunting a 20% speedup on a giant AI model: the real bottleneck turned out to be CPU math, not disk or memory."
---

# Flash-Next llama.cpp Audit (2026-09-28)

Engine-level hunt for ≥20% on the Flash-Next lane (176B A3B, AD384 IQ4_XS, 512 experts x 48
blocks, experts on CPU, Vulkan on the RX 9060 XT). Software-only, no hardware spend.
Artifacts: `~/.hermes/cache/scratch/audit/` (`tiled_srv_summary.txt`, `vramexp.txt`,
`ik_all.txt`, `dd2.txt`, `ngram_ab.txt`).

## Measured state of the deployed lane

- Test prompt 14.7K tokens (real agent shape), flags as deployed (`-b 2048 -ub 2048`, `-fa on`,
  q8_0 KV, `-ngram-map-k`): **prefill 230-315 t/s, decode 15.5-22.4 t/s**.
- **Run-to-run spread is ±10%.** Any claimed win below ~15% on this lane cannot be
  distinguished from noise. Single-shot A/Bs on this lane are worthless; only effect sizes
  like ub 512 -> 2048 (1.7x) or 3060 CUDA -> 9060 XT Vulkan (+45%) are readable.

## What the wall actually is (measured, not assumed)

- **Not disk.** One 14.7K prefill reads **0.20 GB** from the NVMe. Model is page-cache resident.
- **Not DRAM bandwidth.** Streaming ~75 GB of expert weights per ub-2048 chunk at ~13 GB/s is
  well under DDR5 dual-channel capability.
- **Not ubatch/threads.** 2048/16 is the optimum (`ub 512` = 137 t/s, `ub 1024` = 218,
  `ub 2048` = 235, `ub 4096` = 228 at the 922-token reference; t24/t32 are much worse).
- **It is CPU MoE GEMM compute,** ~2.1 TFLOPS effective on the 7950X (AVX-512 VNNI, 16 threads),
  with all 512x48 experts on the CPU. Per ub-2048 chunk: ~5.9 s at 14.7K, ~3.9 s at 922 tokens.

## Levers tested and closed

| Lever | Result | Verdict |
|---|---|---|
| `GGML_CPU_TILED_MM=0` (new tiled CPU MoE kernel, **on by default** in b11223) | default 320.8 vs off 319.7 t/s prefill at ub 2048, order-balanced | no-op at the deployed ubatch. At ub **512** it was 155 vs 201 - the tiled path hurts small ubatch only, and we don't run small ubatch. |
| ik_llama.cpp, Vulkan on the 9060 XT | **cannot load**: `Failed to allocate buffer type Vulkan_Host` (it wants host-mapped buffers for ~75 GB of CPU-resident experts), with both `-cmoe` and `-ot ".ffn_.*_exps.=CPU"`, ub 2048 and 512 | dead end for a 79 GB MoE on 62 GB RAM. |
| Expert tensors on the idle RTX 3060 (`-sm none -mg 0` + `-ot ...=Vulkan1`) | **abort** in `ggml_backend_sched_backend_id_from_cur` | you cannot host tensors on a non-main Vulkan device with split-mode none. The supported expression (`-sm layer` + `-ts`, both devices) was already measured **slower** (-25% prefill). |
| Experts on GPU via `-ncmoe 44/46`, single AMD card | 237.9 / 232.2 t/s vs 235.3 baseline (922-token ref) | wash. The GPU MoE kernel earns nothing per layer moved. |
| `--spec-type ngram-map-k` | decode 15.5 -> 22.4 t/s when output is matchable from the prompt, else neutral; prefill 246.5 (off) vs 256.9 (on), inside noise | keep it - it is free and sometimes a large decode win. |
| Dual-GPU layer split (`-ts`, both cards) | -25% prefill, -8% decode | the 3060 as a Vulkan compute stage is a net loss. |

## Verdict

The deployed Flash-Next lane is at the ceiling of this engine/hardware combination. Prefill is
CPU-MoE-compute-bound and every engine-side dial (`-b/-ub`, `-t`, tiling, expert placement,
ngram, fork swaps) is either already set to its optimum or a wash. The audit's real wins were
found earlier and are already deployed: **ub 2048 (+71% prefill)**, **9060 XT Vulkan instead of
3060 CUDA (+45% prefill/+44% decode)**, **t16**. Getting past ~300 t/s prefill needs fewer
expert bytes or an engine with a faster CPU MoE kernel that can also drive the AMD card - and
ik_llama, the one fork that has that kernel, cannot load this model here.

Separately measured on the daily lane shape (Swift-Qwen3.8-27B Q5, 3010-token prompt):
b11223 Vulkan with the deployed `-ts 16,11` = 293.6 t/s prefill, with `-ts 12,15` = 564.1,
system b10809 at `-ts 16,11` = 590-601. So the daily lane must stay on the system build (as it
is), or if it ever moves to b11223 it needs `-ts 12,15`.

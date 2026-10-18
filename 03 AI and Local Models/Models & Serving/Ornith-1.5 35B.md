---
type: model
model: Ornith-1.5-35B-A3B
host: MASSIVE-RIG (AMD 9060 XT lane)
quant: IQ2_M / MTPv2-23G-ICE
updated: 2026-10-17
category: Models & Serving
tags: [model, benchmark, amd-lane]
publish: true
created: 2026-09-21
machine: bigrig
title: "Ornith-1.5 35B"
---
# Ornith-1.5 35B
> [!warning] Correction (2026-10-17)
> This note's Verdict says its swe40 quality ties the daily Qwen. Its own 2026-09-22 Rebench section below shows that on the uniform 98-task suite the 23G-ICE build is #2 overall, 3 checks behind qwen-low (190 vs 193 of 213) at 2.1x its decode, and IQ2_M scores 184/213 at 97.1 t/s: the best speed/quality balance on the rig, not a quality tie. See [[2026-09-22 Rebench — Coherent Multi-Domain Scoreboard]].


**Category:** [[Models & Serving]] · **Vault:** [[Vault Map]]

Uncensored 35B-A3B MoE on the AMD lane, GPU-only. **swe40 tie at ~4-5x the speed.** See [[Model Benchmarks]].

## swe40 (not LCB-60)

| config | swe40 | t/s | note |
|---|---|---|---|
| IQ2_M (AMD-only) | 107/112, 38/40 | **99** | exact tie with Qwen-Q5, 3.7x faster |
| MTPv2-23G-ICE (dual-GPU) | 110/112, 39/40 | ~61 | best swe40 score, but 2.5x decrypt slower than IQ2_M |

## Verdict

**Speed king on AMD** — swe40 quality ties the daily Qwen at ~4x the throughput on the single 9060. Fast agent lane when you don't need the 27B's LCB hard-tier edge. Quality on LCB-60 not yet measured. (superseded, see Correction above)

Reference: `references/qwen38-mtplx-*` and Ornith swe40 files in the skill.
## Related

- Rig lanes: [[Rig Hardware & Display]] (why a MoE split hurts decode) · [[Qwen-Q5 27B]] · [[Flash-Next AD384]]
- Hub + rules: [[Model Benchmarks]] · [[Benchmark Methodology]] (token-budget artifact lesson came from this model)

## 2026-09-22 Rebench (uniform ~/bench suite, 98 tasks)

| config | checks | full/98 | decode t/s | wall min |
|---|---|---|---|---|
| MTPv2-23G-ICE dual-GPU | 190/213 (89%) | 80/98 | 60.8 | 61 |
| IQ2_M AMD lane | **184/213 (86%)** | **77/98** | **97.1** | **58** |

**Best speed/quality balance on the rig**: 23G is #2 overall (only 3 checks behind qwen-low) at 2.1x its decode. The swe40 110/112 "anomaly" survives in shape — it is a genuinely strong general coder — but narrows here (does not beat qwen-low outright). **IQ2_M's 4-6x speed is USABLE, not a non-starter**: only −9 checks vs 23G (184/190) at 1.6x speed, holds top-2 research. Sub-Q4 floor shows only on backend 78% and hard code; terminal weak (3/11). Deepswe universal wall (0/6). Units validated end-to-end (first-launch gate + throughput spot-check ~60/97 t/s).

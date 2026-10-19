---
type: benchmark-log
topic: Strata Bench
publish: true
created: 2026-10-12
tags: [omarchy]
machine: bigrig
title: "Strata Bench"
---
# Strata Bench

> **Featured project:** [[Strata RTX 3060 Optimization Showcase]] — accepted **16.58% less response time** across six long-context workloads, with the confidence interval, evidence figures and rejected expert-kernel follow-up.


## 2026-10-18 — V100 tuning: +21% decode, +35% prefill, lower energy per token

[[Strata V100 tuning — 2026-10-18]] — paired A/B of GPU power limit and clocks (125 W adopted after a 15.6-min soak), engine 0.1.39 → 0.1.43.1 with the opt-in Volta decode table, chunk ceiling 16384, kernel audit (idle 85 → 59 W; nothing kernel-side on the engine's critical path, measured), and vision added through the model's own encoder. Rounds 4–6: Volta prompt kernels (+1.3% prefill, in production), CPU boost cap 4.5 GHz (engine unchanged, CPU energy −31%, Tctl 86 → 64 °C), 135 W soaked and adopted (+15% 180K prefill), resident routing rejected by the task suite. Interactive dashboard: https://claude.ai/artifact/SVHuTwEfnSbhAVHd55oTzp


## 2026-10-12 — Corrected matched DeepSWE2 comparison

[[2026-10-12 Matched Qwen 27B vs Flash DeepSWE2]] — six complete campaigns, 144 audited results over 24 distinct synthetic repository tasks. Flash averaged **22.67/24** versus Qwen **21.00/24**; the task-bootstrap interval for the +1.67 Flash delta is **[-2.33, +5.67]**, including zero. The historical 27B advantage was not observed on this corrected suite. The note embeds delta and capability/latency charts, with [[2026-10-12 Matched Qwen vs Flash — Methods and artifacts|full methods, provenance and all archived supporting files]].


## 2026-10-05 17:37
**Done:** Compiled the Strata vs llama.cpp wallclock comparison for Qwen3.8-Flash-Next IQ3_XXS from the 2026-09-29 swe40 runs.
**Findings:** Same 40-task suite @3072 budget: Strata (rig, dual 3060) 732.2s / 97/112 / ~48 t/s vs llama.cpp (Unraid) 2055.0s / 99/112 / ~17 t/s — Strata ~2.8x faster wall, quality a wash. Not a pure engine A/B (different hosts); part of the win is Strata's expert cache (40-83% hit). Strata TTFT: 29s warm at 40K prompt, ~19s at 8K.
**Recommendations:** For a clean engine delta, rerun llama.cpp swe40 on the rig with the same IQ3_XXS pack.


## 2026-10-10 — RTX 3060 long-context tuning

[[Strata RTX 3060 Optimization Showcase]] is the project hub for the accepted result, evidence figures and later expert-kernel campaign. [[Strata RTX 3060 long-context tuning]] retains the detailed applied profile, verification and rollback. Five alternating pairs found **16.58% less time overall** at 100 W: fresh requests improved 20–23%, growing conversations 11–12%. All quality checks passed. AMD decode-only missed the 10% improvement gate and remains disabled.


## Public snapshot — 2026-10-12

[Full-source RTX 3060 fork](https://github.com/AIMDaAlien/UnbiasedStrata-RTX3060) · [Dated release and patch](https://github.com/AIMDaAlien/UnbiasedStrata-RTX3060/releases/tag/rtx3060-2026-10-12). Exported documentation version: `rtx3060-2026-10-12`. On-demand, one-way export of the five selected project notes; originals and local evidence remain preserved. No automatic publishing or upstream tracking.

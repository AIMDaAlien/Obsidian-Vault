---
type: model
model: Swift-Qwen3.8-27B-Q5_K_M
host: MASSIVE-RIG (port 8080, daily autostart)
quant: Q5_K_M
updated: 2026-10-17
category: Models & Serving
tags: [model, benchmark, daily-driver, local-ai]
publish: true
created: 2026-09-21
machine: bigrig
title: "Qwen-Q5 27B"
---
# Qwen-Q5 27B
> [!warning] Correction (2026-10-17)
> This note's LCB-60 section calls thinking OFF catastrophic (33/60). Its own 2026-09-22 Rebench section below shows OFF costs only 6 checks on the uniform 98-task suite (193 to 187 of 213) at 4x less wall time, and that thinking LOW is the best config in the whole fleet (193/213, 83/98 full passes). See [[2026-09-22 Rebench — Coherent Multi-Domain Scoreboard]].


**Category:** [[Models & Serving]] · **Vault:** [[Vault Map]]

The daily driver on the MASSIVE-RIG. Both dGPUs over Vulkan, MTP spec-decode. See [[Model Benchmarks]] for the full picture.

## LCB-60

| run | easy | med | hard | total | t/s |
|---|---|---|---|---|---|
| **low-effort** (12K) | 20 | 17 | 11 | **48/60** | **27.7** |
| default xhigh (24K corr) | 20 | 17 | 8 | 45/60 | 24.7 |
| thinking OFF (12K) | 12 | 12 | 9 | 33/60 | 27.1 |

**Low effort wins on both axes** — 48 > 45 quality, 27.7 > 24.7 speed. Less thinking = fewer truncations AND faster. Use `LCB_EFFORT=low`. **Thinking OFF is catastrophic** (33/60) — without a thinking pass Qwen-Q5 can't even close code fences on easy problems. Sweet spot is `low`, not off. (superseded, see Correction above)

Fails at low-effort (12): `3743, 3763, 3722, abc388_f, abc392_g, abc389_g, abc397_f, arc192_e, arc192_d, abc389_e, abc397_d, 3562` — mostly hard, reasoning burns the budget.

## swe40 (older)

107/112 checks, 38/40 tasks — ties Ornith on this suite.

## Verdict

**Value king.** Best quality-to-speed of the fleet. Default fast agentic choice. Template accepts `xhigh/medium/low` (NOT `high`).

Run notes: `~/bench-results/lcb60-qwen5m-8080.json` (default), `lcb60-qwen5m-low.json` (low).
## Related

- Siblings: [[Flash-Next AD384]] (quality lane) · [[Ornith-1.5 35B]] (speed lane) · [[Unraid Flash-Next]] (262K) · [[Laguna XS-2.1]]
- Hub + rules: [[Model Benchmarks]] · [[Benchmark Methodology]] · [[Bench Suite (~bench)]]
- Serving: [[Qwen3.8 Rig]] (flags, MTP, hashes) · [[Omarchy Plugins & Shell Widgets]] (bar switcher)

## 2026-09-22 Rebench (uniform ~/bench suite, 98 tasks)

| config | checks | full/98 | decode t/s | wall min |
|---|---|---|---|---|
| thinking LOW | **193/213 (91%)** | **83/98** | 28.9 | 57 |
| thinking OFF | 187/213 (88%) | 76/98 | 30.2 | 15 |

LOW is the best config in the whole fleet on the same-suite instrument (leads total checks AND full-pass rate). The old "thinking OFF costs ~15 points" (LCB-60: 48→33) does NOT reproduce here — it costs only 6 checks (193→187) at 4x less wall time. OFF is still not recommended over LOW, but it's no catastrophe. 100% on backend+code, best-in-fleet terminal 5/11; deepswe universal wall (0/6). NOTE: prior LCB-60/swe40 numbers were from different harnesses and are not directly comparable — this row is the comparable one.

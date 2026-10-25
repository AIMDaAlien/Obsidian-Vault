---
type: model
model: Qwen3.8-Flash-Next UD-IQ3_XXS
host: Unraid (port 18006, container llm-qwen38-flash)
quant: IQ3_XXS (ncmoe 48 experts on DDR4)
updated: 2026-09-21
category: Models & Serving
tags: [model, unraid, benchmark, local-ai, llama-cpp]
publish: true
created: 2026-09-21
machine: bigrig
title: "Unraid Flash-Next"
---
# Unraid Flash-Next

**Category:** [[Models & Serving]] · **Vault:** [[Vault Map]]

Flash-Next 176B on the Unraid box, lowest quant. **Only real edge: 262K context.** See [[Model Benchmarks]].

## LCB-60

| run | easy | med | hard | total | t/s |
|---|---|---|---|---|---|
| default (16K corr) | 20 | 15 | 4 | 39/60 | 14.2 |
| thinking OFF (12K) | 20 | 16 | 11 | 47/60 | 15.6 |

## swe40

106/112 budget-corrected. Fails on hard-tier lru-ttl even at 16K.

## Verdict

**Lowest quality of the Flash family if thinking uncapped** (IQ3 vs the rig's IQ4 AD384) — 39 vs 54. **With thinking OFF it's competitive** (47/60, hard 11/20 — edge over Laguna's 14/20 hard is on the easy-heavy aggregate) but at ~15 t/s it burns 3.8x longer per task in verbose output. The 262K ctx is its real edge; use [[Flash-Next AD384]] on the rig for Flash quality.

Run notes: `~/bench-results/lcb60-q38flash-v2.json`. Needs `socat` forward 127.0.0.1:18006 → Unraid for local benching.

## Related

- Host mechanics: [[Unraid LLM Control Center]] · sibling: [[Laguna XS-2.1]] (same box, successor candidate)
- Rig-side family: [[Flash-Next AD384]] · hub: [[Model Benchmarks]] · rules: [[Benchmark Methodology]]
- Upgrades: [[llama.cpp Upgrade Roadmap]]

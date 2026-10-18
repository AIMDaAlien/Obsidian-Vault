---
type: model
model: Laguna XS-2.1 (Q4_K_M)
host: Unraid (port 18007, container llm-laguna-xs21, image local/qwen38-flash-cuda)
quant: Q4_K_M, 33B total / 3B active MoE (260K ctx)
updated: 2026-10-17
category: Models & Serving
tags: [model, unraid, benchmark]
publish: true
created: 2026-09-21
machine: bigrig
title: "Laguna XS-2.1 33B (3B active)"
---
# Laguna XS-2.1 33B (3B active)
> [!warning] Correction (2026-10-17)
> This note calls its LCB-60 hard tier (14/20) the best of the fleet. Its own 2026-09-22 Rebench section below places it last of the six strong configs at 175/213 (82%), with the fleet's worst terminal score (0/11), so the hard-tier result did not carry over to multi-domain agent work. See [[2026-09-22 Rebench — Coherent Multi-Domain Scoreboard]].


**Category:** [[Models & Serving]] · **Vault:** [[Vault Map]]

Poolside MoE candidate for the Unraid box. Same engine/arch-support as Flash-Next (deployed image already has `LLM_ARCH_LAGUNA`). 3B active vs Flash-Next's 6B → decode scales ~2x on DDR4-bound Unraid. See [[Model Benchmarks]].

## LCB-60 (thinking OFF, MAXTOK 12K)

| run | easy | med | hard | total | t/s |
|---|---|---|---|---|---|
| thinking OFF | 19 | 13 | **14** | 46/60 | **34.0** |

Hard tier 14/20 is the **best of the fleet**. Decode 34 t/s = ~2.2x Flash-Next IQ3 (15.6). (superseded, see Correction above)

## swe40

**112/112 checks, 40/40 tasks** (per-server budget 1024) — first-ever perfect on the harness, including t4-skyline / t4-lru-ttl / word-ladder-len that trip every other model.

## Verdict — NOT yet conclusive ⚠

The swe40 perfect score **does NOT prove it's best** — that harness saturates and the thinking-caps differed across the field. On LCB-60 hard it holds the top hard tier (14/20), but on easy/medium aggregate it lands mid-fleet. Needs the same budget-corrected escalation ladder as the Qwen/Flash runs before a real verdict. Risk flag (user): prior Laguna XS/S-class "thinks too much, hangs up" — mitigated by `--reasoning-budget 1024` in the entrypoint; thinking OFF in the LCB run answers instantly. Decode is the real win here (2x Flash on the same DDR4 box). (superseded, see Correction above)

Run notes: `~/bench-results/lcb60-laguna-off.json` (thinking off), `swe40-laguna-xs21-3k-budget1024.json` (budget-capped swe40). Config staged: compose profile `laguna-xs21`, roster entry, model at `/mnt/cache/llm-workspace/models/laguna-xs21/` — survives container recreate but is NOT the live default (Unraid currently serving [[Unraid Flash-Next]]).
## Related

- Host mechanics: [[Unraid LLM Control Center]] (roster/compose swap, `--reasoning-budget`) · predecessor on the box: [[Unraid Flash-Next]]
- Hub + rules: [[Model Benchmarks]] · [[Benchmark Methodology]] · [[Bench Suite (~bench)]]
- Agentic caveat context: [[Unraid LLM Control Center#Agentic reality check (2026-09-21)]]

## 2026-09-22 Rebench (uniform ~/bench suite, 98 tasks)

| config | checks | full/98 | decode t/s | wall min |
|---|---|---|---|---|
| Q4_K_M Unraid (thinking OFF) | **175/213 (82%)** | **67/98** | 36.1 | 32 |

**Now clearly LAST of the six strong configs — the swe40 110/112 was a single-domain artifact.** On the broader executed suite it lands at 82%, with the fleet's worst terminal (0/11 — no-code failures across the board) and research 68% (worst of the Q4 crowd). Strong points: code 100% ties everyone, decode 36 t/s beats all Q4+ rig configs except the fast Ornith. The earlier "best hard-tier on LCB-60" does not translate to multi-domain agent work. Run notes: `~/bench/results/rebench-laguna.json`.

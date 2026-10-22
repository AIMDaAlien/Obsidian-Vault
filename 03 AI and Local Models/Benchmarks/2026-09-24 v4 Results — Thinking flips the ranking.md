---
type: note
category: Benchmarks
tags: [omarchy, benchmarks]
updated: 2026-09-24
publish: true
created: 2026-09-24
machine: bigrig
title: "2026-09-24 v4 Results — Thinking flips the ranking: LiteResearcher wins"
featured: 10
summary: "Letting small AI models think before answering reshuffled the leaderboard: the former last-place model rose to first."
blurb: "I run small AI models on my own hardware and score them on the same 45 research tasks. For this round I let each model think before answering. The order changed completely: the model that came last without thinking came first with it. Useful if you're picking a small model and wondering whether thinking mode is worth the wait."
---

# 2026-09-24 v4 Results — Thinking flips the ranking: LiteResearcher wins

v4 = same 45-task REAL research suite, but **thinking ON** for every model (×6 token
budget, min 4096), **64K context** (was 32K), engine b11158 Vulkan, one-by-one load.

| config | v4 | v3 | Δ | med decode |
|---|---|---|---|---|
| LiteResearcher-4B Q8 | **43/45** | 36 | +7 | ~52 t/s |
| K2-Horizon-3.7B Q6 | 41/45 | 40 | +1 | ~56 t/s |
| Spark-X2.5-4B Q8 | 41/45 | 33 | +8 | ~53 t/s |
| Nanbeige4.2-3B Q8 | 41/45 | 33 | +8 | ~39 t/s |
| Ornith-35B IQ2_M | 40/45 | 38 | +2 | ~93 t/s |
| MiniCPM5-2B Q8 | 40/45 | 38 | +2 | ~98 t/s |
| Mellum2-12B-A2.5B Q4 | 39/45 | 28 | +11 | ~132 t/s |

**Headline: thinking mode collapses the fleet spread (9 pts → 4 pts) and flips the
crown.** The v3 direct-mode ranking measured who's good without reasoning; given a
thinking budget, LiteResearcher-4B — purpose-built deep-research agent — dominates
(43/45, perfect hard tier, 16/17 research core). Mellum2 climbs most (+11).

Updated best-fit lanes:
- **LiteResearcher-4B** — default research subagent (if you accept ~52 t/s and thinking-mode latency).
- **K2** — still excellent, and the ONLY near-top model that works great WITHOUT thinking (direct mode 40/45 = best v3 score) — pick for latency-sensitive direct calls.
- **Spark / Nanbeige** — 41/45 with thinking; Nanbeige slow (39 t/s), Spark fine (53). Both now credible.
- **MiniCPM** — fast direct-mode worker (98 t/s, least to gain from thinking).
- **Mellum2** — Q8_0 retest: **41/45 at ~100 t/s** (was 39 at Q4/132 t/s) — now tied with K2/Spark/Nanbeige. If Mellum2 stays in the fleet, use Q8_0.
- **Ornith IQ2_M** — dominated everywhere at this quant. Retire candidate.

Details: ~/bench/results/v4-summary.md; per-task answers in v4-*.json.
Caveat: v4 is single-run per config (v3 did doubles); ±1-2 noise, Ornith proven flaky.

Fleet Pareto (both modes side by side): ![[_attachments/model-benchmarks/fleet-pareto.png]]

Frontier v3 (direct): K2 → MiniCPM → Mellum2. Frontier v4 (thinking): MiniCPM → Ornith → LiteResearcher — the fleet spread collapses and LiteResearcher takes the quality crown.

Links: [[2026-09-24 v3 Results — K2 wins on capability, Ornith loses the research core]] · [[2026-09-23 v3 — Small Models vs Ornith Real Research Bench]] · [[Model Benchmarks]]

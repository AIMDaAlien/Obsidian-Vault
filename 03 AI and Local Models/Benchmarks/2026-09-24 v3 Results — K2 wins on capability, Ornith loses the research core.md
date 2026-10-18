---
type: note
category: Benchmarks
tags: [omarchy, benchmarks]
updated: 2026-10-17
publish: true
created: 2026-09-24
machine: bigrig
title: "2026-09-24 v3 Results — K2 wins on capability, Ornith loses the research core"
featured: 47
summary: "A tiny 3.7B-parameter AI beat a model ten times its size on real document research, once the test itself was fixed."
---

# 2026-09-24 v3 Results — K2 wins on capability, Ornith loses the research core
> [!warning] Correction (2026-10-17)
> This note ranks K2-Horizon-3.7B first (40/45) with thinking off. The v4 rerun with thinking on for every model and 64K context changed the ranking: LiteResearcher-4B led at 43/45, K2 scored 41/45 (tied with Spark and Nanbeige), and Ornith and MiniCPM scored 40/45. See [[2026-09-24 v4 Results — Thinking flips the ranking]].



Suite: bench3.py, 45 executed-verdict tasks (17-task REAL 18K research pack + fab/tool/compliance + 10 harder reasoning). Identical engine (b11149 Vulkan), 32K ctx, q8_0 KV, AMD-only, temp 0, think=off (all four are server-side reasoning models; enable_thinking:false required). Sequential loads only. Full write-up: `~/bench/results/v3-summary.md`.

## Scores (final grader; every config fully re-run)

| config | total | research /17 | hard /10 | compliance | med decode |
|---|---|---|---|---|---|
| K2-Horizon-3.7B Q6_K | **40/45** | 12 | **10** | 6/6 | ~69 t/s |
| Ornith-35B-A3B IQ2_M | 38/45 | 11 | **10** | 5/6 | ~90 t/s |
| MiniCPM5-2B Q8_0 | 38/45 | **14** | 8 | 5/6 | ~100 t/s |
| Spark-X2.5-4B Q8_0 | 33/45 | 10 | 6 | 5/6 | ~58 t/s |

## Verdict
- **v2's conclusion does not survive v3.** Ornith's 46/47 v2 lead was ceiling + grader artifact.
- **K2-Horizon-3.7B is the best free-card research subagent on capability** (perfect compliance, perfect hard tier, bit-for-bit stable across two full runs). (superseded, see Correction above)
- **Ornith lost the real 18K research core**: 11/17 — missed one region in the Q3 table sum, overcounted the team rollup ("Edge 10"), misread the retention-conflict sections. Its ~90 t/s doesn't buy back the 2-point gap vs K2.
- **MiniCPM is the sleeper**: best retriever (14/17) AND fastest (~100 t/s); loses only on hard reasoning + one compliance task.
- Spark strictly last; failed "7*8" health probes twice (instruction-following unreliable).

## Grader bugs found BY the bench (then all four re-run)
1. Angle-bracket literal: models mirror `<values>` → `<47> @ §4`; checker now strips `< > ` *.
2. r4-team-rollup gold was ambiguous: Platform and Edge TIE at 7 services. Required is now `platform|edge`, selftest updated (gold = first alt).
3. bench3 now stores 400-char answers per task in the results JSON.

Verified the remaining shared fails are EARNED: r3-table-q3sum — every model answered Northland's 8316 alone, missing Eastgate (gold 12788 = 4472+8316); grand total 104129 re-summed from the table. These two tasks are genuine long-context retrieval+arithmetic walls and stay.

## Stability
Ornith flipped 3 tasks between two identical full runs (±2-3 noise on verbose models is real). K2 and Spark reproduced bit-for-bit; MiniCPM flipped its two team-lookups.

## Caveat
r1-retention-3 / r4-contradiction: corpus states RegistrySession retention twice (§3: 90 days, §20: 45). Gold is 45 @ §20; a model answering 90 @ §3 reads the same ambiguity the task tests.

Links: [[2026-09-23 v3 — Small Models vs Ornith Real Research Bench]] · [[2026-09-23 Small Models vs Ornith (v2)]] · [[Model Benchmarks]]

Pareto charts: v3 direct mode ![[_attachments/model-benchmarks/v3-pareto.png]] · v4 thinking ON ![[_attachments/model-benchmarks/v4-pareto.png]]

## Updated verdict — who wins where (7 configs)

Pareto frontier after all challengers: **K2 (capability) → MiniCPM (fast quality) → Mellum2 (raw speed)**. Ornith, Spark, LiteResearcher, Nanbeige are all dominated (someone beats them on BOTH axes).

| model | best suited for |
|---|---|
| **K2-Horizon-3.7B Q6** | **Default research subagent.** Best total, only perfect hard tier + compliance, bit-stable across runs. Cost: slowest-ish (69 t/s) + needs the MBZUAI-IFM fork build. |
| **MiniCPM5-2B Q8** | **Fast lane / volume batch research.** 99% of K2's retrieval sharpness (best research core, 14/17) at ~100 t/s; accept it where hard multi-hop reasoning isn't the bottleneck. Also the pick if you want the standard-arch model (stock llama.cpp, no fork). |
| **Mellum2-12B-A2.5B Q4** | **Speed-critical non-grounded work only** — triage, summarization, tool-calling (7/7, compliance 5/6, 8/10 hard) at 142 t/s. NOT a grounded-citation researcher: 4/17 research core, fails the `value @ §sec` contract wholesale. |
| **Ornith-35B IQ2_M** | **Dominated at IQ2_M.** Its only edge was the 35B capability story; at this quant the 3.7B/2B models match or beat it. Only reason to keep the lane: if a higher quant of the 35B were feasible — it isn't on 16GB. |
| **LiteResearcher-4B Q8** | Fine generalist (36/45, best-in-class compliance) but strictly under K2 on the same tasks — the GAIA claims don't transfer to grounded-corpus citation work. No lane it wins. |
| **Spark-X2.5-4B Q8** | Nothing. Weakest reasoning, failed 7×8 twice. Drop from the fleet. |
| **Nanbeige4.2-3B Q8** | Nothing on this workload — fleet-slowest (39 t/s, looped-arch 2× compute) and mid capability. Its claimed agentic wins live in OpenClaw-style scaffolds, not exact-grounding retrieval. |

**Bottom line unchanged and now reinforced: K2 is THE research subagent; MiniCPM is the fast lane; everything post-Gemma-4 lost to it.**

## Post-Gemma-4 challengers (2026-09-24, b11158, same protocol think=off)
| config | total | research /17 | hard /10 | ~t/s |
|---|---|---|---|---|
| LiteResearcher-4B Q8 | 36/45 | 12 | 8 | 63 |
| Nanbeige4.2-3B Q8 | 33/45 | 11 | 6 | 39 |
| Mellum2-12B-A2.5B Q4 | 28/45 | 4 | 8 | 142 |

None beat K2's 40/45. LiteResearcher's GAIA pedigree didn't transfer to the grounded corpus. Nanbeige's looped arch works on Vulkan but the 2× compute makes it the slowest of the fleet and it drops hard-reasoning checks. Mellum2 is blazingly fast (142 t/s) but fails the `value @ §sec` citation contract wholesale (4/17 research) — its 66/66 on other suites doesn't cover exact-grounding retrieval. Verdict unchanged: K2 is the research-subagent pick; MiniCPM is the fast lane. Engine updated to b11158 (~/opt/llama-vulkan-b11158); b11149 kept.

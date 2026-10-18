---
type: note
category: Benchmarks
tags: [omarchy, benchmarks]
updated: 2026-10-17
publish: true
created: 2026-09-24
machine: bigrig
title: "2026-09-23 v3 — Small Models vs Ornith Single-GPU (Real Research-Subagent Bench)"
---

# 2026-09-23 v3 — Small Models vs Ornith Single-GPU (Real Research-Subagent Bench)
> [!warning] Correction (2026-10-17)
> This is the v3 design note and holds no final scores. Scores are in [[2026-09-24 v3 Results — K2 wins on capability, Ornith loses the research core]]; the thinking-on rerun, which changed the ranking, is in [[2026-09-24 v4 Results — Thinking flips the ranking]].


Status: **RUN COMPLETE 2026-09-24. Full four-way results in [[2026-09-24 v3 Results — K2 wins on capability, Ornith loses the research core]].**

## Why v3 exists
The v2 config shootout (46/47 Ornith > 45/47 K2 > 42/47 MiniCPM = Spark, reported in "2026-09-23 Small Models vs Ornith (v2)") was criticized as NOT a fair test: it used a ~600-token corpus, had a scoring ceiling (Ornith scored near-perfect = suite couldn't discriminate), forced thinking OFF for all models (uneven for reasoning models), and a single corpus seed. v3 fixes all four.

## What v3 adds (built + self-tested, 45/45 PASS)
- REAL 18K-token grounded research pack (`~/bench/packs/research/`) — the actual batch-research workload: exact `value @ §section` citation grading over a digit-free-filler corpus where ANY digit is a planted fact (unguessable answers).
- HARDER reasoning + multi-hop tiers (3-hop algebra, compound proportion, contrapositive, nested arithmetic, word-length ordering, negative syllogism, percent, char-count, exception-to-universal) — kills the ceiling.
- Per-model reasoning policy (`--think on|off`) — fairness fix. No single forced regime.
- Reuses v2 fabrication / strict-tool / compliance graders.

## Grader bug fixed from v2 (important)
`last_num()` mis-graded verbose-but-correct answers — a model writing "...so 8 cups, verify 12/8=1.5" read as 1.5, not 8. All numeric graders switched to `has_value()`. This biased against big/verbose models. (Also rewrote the ambiguous "title of Dr. Alma Reyes" → "what position does she hold".)
- A shared failure across 3+ models = suspect the GRADER, not the models.
- A big verbose model can pass one run and grade False the next — re-run a config once before trusting a stored False.

## How to run (sequential VRAM only)
1. `cd ~/bench && python3 selftest3.py` (must PASS).
2. Load ONE config: Ornith→port 8096, MiniCPM→8099, Spark→8097, K2→8098 (b11149 Vulkan; K2 uses the MBZUAI-IFM fork build; all `GGML_VK_VISIBLE_DEVICES=1`, 32768 ctx, q8_0 KV, AMD only).
3. `python3 bench3.py --port <P> --tag <t> --think <on|off>` → `results/v3-<tag>.json`.

HARD RULES: never load >1 bench config at a time (MiniCPM+Spark+K2 alone = 12/16GB; adding Ornith OOMs + spills K2 to GTT). NVIDIA card + :8080 large bench = untouched. Machine must never crash.

## Deliverable for the next session
Four-way v3 head-to-head → `~/bench/results/v3-summary.md` + verdict: does Ornith single-GPU (35B MoE at IQ2_M) genuinely beat a 2-4B model at high quant on the REAL research workload, now that ceiling + fairness are fixed? Update this note with the scores.

Links: [[2026-09-23 Rebench2 — Role-Tagged Scoreboard]] · bench-suite-authoring skill · bench_lib2 / bench3.py
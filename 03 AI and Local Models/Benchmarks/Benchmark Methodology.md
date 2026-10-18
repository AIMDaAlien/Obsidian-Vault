---
type: methodology
topic: Benchmark Methodology
updated: 2026-10-12
category: Benchmarks
tags: [benchmark, methodology]
publish: true
created: 2026-10-12
machine: bigrig
title: "Benchmark Methodology"
---
# Benchmark Methodology

**Category:** [[Benchmarks]] · **Vault:** [[Vault Map]]

How to read the numbers in [[Model Benchmarks]] and the per-model notes.

## 2026-10-12 — Corrected matched DeepSWE2 comparison

[[2026-10-12 Matched Qwen 27B vs Flash DeepSWE2]] — six complete campaigns, 144 audited results over 24 distinct synthetic repository tasks. Flash averaged **22.67/24** versus Qwen **21.00/24**; the task-bootstrap interval for the +1.67 Flash delta is **[-2.33, +5.67]**, including zero. The historical 27B advantage was not observed on this corrected suite. The note embeds delta and capability/latency charts, with [[2026-10-12 Matched Qwen vs Flash — Methods and artifacts|full methods, provenance and all archived supporting files]].


## LCB-60 (primary differentiator)

- **LiveCodeBench** release_v6, 60 problems = 20 easy / 20 medium / 20 hard, contest window ≥ 2025-01-01 (contamination-safe).
- LCB's own prompts + executable hidden tests, graded pass@1.
- Easy tier saturates (all 20) — **only medium + hard differentiate models**. Judge a model on those.

## Budget correction (critical for thinking models)

Thinking models burn their token budget reasoning, then return no code → "no-code-block". That's a *budget artifact*, not a capability miss.

- Run at 4K cap → fails on many hards.
- **Re-run ONLY the no-code-block fails** at escalating `LCB_MAXTOK` (8K/16K/24K) with `LCB_RETRY=1`.
- Ladder caps at one 4x attempt before calling a failure real.
- **Always compare budget-corrected scores** for reasoning models, never the raw 4K pass.

## Reasoning effort

- Low/medium effort changes both quality AND speed. Sweep it before blaming the quant (see [[Qwen-Q5 27B]]: low > default on both axes).
- Pass via `LCB_EFFORT=low` (maps to `chat_template_kwargs.reasoning_effort`).
- Qwen-Q5 GGUF template accepts `xhigh/medium/low` — **not `high`**.

## Value metric

value = (LCB score × t/s) / 100 — output per wall-minute. Combines both Pareto axes into one number. See the value-index chart in [[Model Benchmarks]].

## Running the harness

```bash
cd ~/Work
LCB_API=<url>/v1 LCB_TAG=<tag> LCB_MAXTOK=12288 LCB_EFFORT=low \
  .venv-lcb/bin/python lcb-bench.py
```

Env: `LCB_API`, `LCB_TAG`, `LCB_MAXTOK`, `LCB_EFFORT`, `LCB_RETRY`, `LCB_N_PER_TIER`, `LCB_START_DATE`, `LCB_SEED`. Pin `datasets==3.6.0`. Grade via `check_correctness` (subprocess isolation).

Run it with `~/.venv-lcb/bin/python` (system python3 has no numpy). Dataset = `livecodebench/code_generation_lite` `release_v6` (1055 problems), 60-problem stratified sample, fixed seed 40, contest window ≥ 2025-01-01.

## The multi-domain suite

LCB-60 saturates on one domain, so the current instrument is **[[Bench Suite (~bench)]]** — 76 executed-verdict tasks across code / research / terminal / backend / deepswe, no LLM judge. Cross-harness numbers are **not** comparable; compare only rows from the same suite.
- **Reasoning models need budget headroom or you measure the harness.** At a 1K cap Ornith scored 91/112 and 6 of 7 fails were `[no-code-block]` at exactly max_tokens; at an honest 3K it ties Qwen 107/112.
- **Terminal is the pack that separates configs** (qwen-low 5/11 vs laguna 0/11); code/backend are saturated at Q4+; **deepswe is a universal 0/6 wall** and currently uninformative.
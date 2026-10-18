---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench]
publish: true
created: 2026-09-23
machine: bigrig
title: "ReBench rebench-qwenq5-low"
---
# ReBench rebench-qwenq5-low

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

Generated 2026-09-23 00:37 from `results/rebench-qwenq5-low.json`.

| target | checks | tasks | decode t/s (med) | TTFT s (med) | wall s | caps hit | errors |
|---|---|---|---|---|---|---|---|
| qwen38-27b-q5-mtp-low | 193/213 (91%) | 83/98 | 28.9 | 0.65 | 3396.8 | 0 | 12 |

## qwen38-27b-q5-mtp-low
_Daily Qwen3.8-27B Q5_K_M, MTP n=2, 128K ctx, q8_0 KV. Prior: LCB-60 48/60 (best local), swe40 107/112 @27.5 t/s. Thinking LOW is its measured sweet spot._

### by domain

| domain | checks | tasks | decode t/s (med) |
|---|---|---|---|
| backend | 9/9 (100%) | 9/9 | 29.3 |
| code | 131/131 (100%) | 46/46 | 29.2 |
| deepswe | 0/6 (0%) | 0/6 | 28.6 |
| research | 48/56 (86%) | 23/26 | 27.4 |
| terminal | 5/11 (45%) | 5/11 | 29.4 |

### by tier

| tier | checks | tasks | decode t/s (med) |
|---|---|---|---|
| t1 | 57/60 (95%) | 23/25 | 28.2 |
| t2 | 31/40 (78%) | 15/20 | 28.7 |
| t3 | 47/53 (89%) | 20/26 | 29.0 |
| t4 | 58/60 (97%) | 25/27 | 29.2 |

### failures (executed verdicts, no judge)

| task | tier | score | detail |
|---|---|---|---|
| `research/r1-retention-3` | t1 | 0/2 | 0/2 |
| `terminal/t1-log-counts` | t1 | 0/1 | model-exit127: ~/.hermes/cache/scratch/bench-l967anzf/_model.sh: line 20: [ERROR]: |
| `deepswe/d1-worker-drain` | t2 | 0/1 | patch-failed: patch: **** malformed patch at line 11: +__all__ = ["BoundedQueue", "QueueCl |
| `research/r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `terminal/t2-stale-cleanup` | t2 | 0/1 | no-code |
| `triage/deepswe:d1-worker-drain` | t2 | 0/1 | patch-failed: patch: **** malformed patch at line 11: +__all__ = ["BoundedQueue", "QueueCl |
| `triage/research:r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `deepswe/d2-guards-history` | t3 | 0/1 | patch-failed: error: sm.py: No such file or directory |
| `deepswe/d3-config-precedence` | t3 | 0/1 | patch-failed: patch: **** malformed patch at line 45: +    if effective["verbose"]: |
| `terminal/t3-csv-normalize` | t3 | 0/1 | model-exit2: python3: can't open file '~/.hermes/cache/scratch/bench-xnlle_to/norm |
| `triage/deepswe:d2-guards-history` | t3 | 0/1 | patch-failed: error: sm.py: No such file or directory |
| `triage/deepswe:d3-config-precedence` | t3 | 0/1 | patch-failed: patch: **** malformed patch at line 45: +    if effective["verbose"]: |
| `triage/terminal:t3-csv-normalize` | t3 | 0/1 | model-exit2: python3: can't open file '~/.hermes/cache/scratch/bench-5a3ek2jj/norm |
| `terminal/t4-git-rescue` | t4 | 0/1 | no-code |
| `triage/terminal:t4-git-rescue` | t4 | 0/1 | no-code |

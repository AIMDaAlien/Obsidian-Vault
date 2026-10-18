---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench]
publish: true
created: 2026-09-23
machine: bigrig
title: "ReBench rebench-ornith-iq2m"
---
# ReBench rebench-ornith-iq2m

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

Generated 2026-09-23 00:37 from `results/rebench-ornith-iq2m.json`.

| target | checks | tasks | decode t/s (med) | TTFT s (med) | wall s | caps hit | errors |
|---|---|---|---|---|---|---|---|
| ornith-iq2m-131k | 184/213 (86%) | 77/98 | 97.1 | 0.16 | 3452.9 | 0 | 14 |

## ornith-iq2m-131k
_Ornith-1.5-35B-A3B IQ2_M on the AMD card alone, 128K ctx. Prior: swe40 107/112 38/40 @~99 t/s (speed king). Below the Q4 quality floor by design; competing on throughput, not quality._

### by domain

| domain | checks | tasks | decode t/s (med) |
|---|---|---|---|
| backend | 7/9 (78%) | 7/9 | 96.0 |
| code | 125/131 (95%) | 44/46 | 99.0 |
| deepswe | 0/6 (0%) | 0/6 | 95.9 |
| research | 49/56 (88%) | 23/26 | 93.0 |
| terminal | 3/11 (27%) | 3/11 | 96.1 |

### by tier

| tier | checks | tasks | decode t/s (med) |
|---|---|---|---|
| t1 | 59/60 (98%) | 24/25 | 96.0 |
| t2 | 30/40 (75%) | 14/20 | 98.5 |
| t3 | 45/53 (85%) | 18/26 | 96.0 |
| t4 | 50/60 (83%) | 21/27 | 96.1 |

### failures (executed verdicts, no judge)

| task | tier | score | detail |
|---|---|---|---|
| `terminal/t1-log-counts` | t1 | 0/1 | no-code |
| `backend/b2-token-bucket` | t2 | 0/1 | check-fail: TypeError: 'float' object is not callable |
| `deepswe/d1-worker-drain` | t2 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `research/r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `terminal/t2-stale-cleanup` | t2 | 0/1 | model-exit1: sed: -e expression #1, char 30: unterminated 's' command |
| `triage/deepswe:d1-worker-drain` | t2 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `triage/research:r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `backend/b3-cursor-pagination` | t3 | 0/1 | check-fail: ImportError: cannot import name 'paginate' from 'benchmod' (~/.hermes/ |
| `deepswe/d2-guards-history` | t3 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `deepswe/d3-config-precedence` | t3 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `research/r3-table-argmax` | t3 | 2/3 | 2/3 |
| `terminal/t3-csv-normalize` | t3 | 0/1 | no-code |
| `triage/deepswe:d2-guards-history` | t3 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `triage/deepswe:d3-config-precedence` | t3 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `triage/terminal:t3-csv-normalize` | t3 | 0/1 | no-code |
| `code/t4-lru-ttl` | t4 | 0/3 | NameError: name 'cap' is not defined. Did you mean: 'map'? |
| `terminal/t4-git-rescue` | t4 | 0/1 | model-exit1: ~/.hermes/cache/scratch/bench-9aim55s6/_model.sh: line 18: commit: No |
| `terminal/t4-manifest-repair` | t4 | 0/1 | no-code |
| `triage/code:t4-lru-ttl` | t4 | 0/3 | NameError: name 'cap' is not defined. Did you mean: 'map'? |
| `triage/terminal:t4-git-rescue` | t4 | 0/1 | model-exit1: ~/.hermes/cache/scratch/bench-pycm0rso/_model.sh: line 18: commit: No |
| `triage/terminal:t4-manifest-repair` | t4 | 0/1 | no-code |

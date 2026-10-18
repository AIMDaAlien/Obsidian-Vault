---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench]
publish: true
created: 2026-09-23
machine: bigrig
title: "ReBench rebench-ornith-23g"
---
# ReBench rebench-ornith-23g

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

Generated 2026-09-23 00:37 from `results/rebench-ornith-23g.json`.

| target | checks | tasks | decode t/s (med) | TTFT s (med) | wall s | caps hit | errors |
|---|---|---|---|---|---|---|---|
| ornith-23g-131k | 190/213 (89%) | 80/98 | 60.8 | 0.23 | 3639.2 | 0 | 15 |

## ornith-23g-131k
_Ornith-1.5-35B-A3B MTPv2-23G-ICE, dual-GPU layer split, 128K ctx. Prior: swe40 110/112 39/40 @~61 t/s (best swe40 of any config). LCB-60 never measured — this campaign fills that gap._

### by domain

| domain | checks | tasks | decode t/s (med) |
|---|---|---|---|
| backend | 9/9 (100%) | 9/9 | 59.9 |
| code | 131/131 (100%) | 46/46 | 62.2 |
| deepswe | 0/6 (0%) | 0/6 | 59.1 |
| research | 48/56 (86%) | 23/26 | 58.0 |
| terminal | 2/11 (18%) | 2/11 | 60.6 |

### by tier

| tier | checks | tasks | decode t/s (med) |
|---|---|---|---|
| t1 | 57/60 (95%) | 23/25 | 61.4 |
| t2 | 31/40 (78%) | 15/20 | 61.2 |
| t3 | 46/53 (87%) | 19/26 | 60.2 |
| t4 | 56/60 (93%) | 23/27 | 60.9 |

### failures (executed verdicts, no judge)

| task | tier | score | detail |
|---|---|---|---|
| `research/r1-retention-3` | t1 | 0/2 | 0/2 |
| `terminal/t1-log-counts` | t1 | 0/1 | no-code |
| `deepswe/d1-worker-drain` | t2 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `research/r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `terminal/t2-stale-cleanup` | t2 | 0/1 | no-code |
| `triage/deepswe:d1-worker-drain` | t2 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `triage/research:r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `deepswe/d2-guards-history` | t3 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `deepswe/d3-config-precedence` | t3 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `terminal/t3-csv-normalize` | t3 | 0/1 | no-code |
| `terminal/t3-perm-audit` | t3 | 0/1 | no-code |
| `triage/deepswe:d2-guards-history` | t3 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `triage/deepswe:d3-config-precedence` | t3 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `triage/terminal:t3-csv-normalize` | t3 | 0/1 | no-code |
| `terminal/t4-git-rescue` | t4 | 0/1 | no-code |
| `terminal/t4-manifest-repair` | t4 | 0/1 | no-code |
| `triage/terminal:t4-git-rescue` | t4 | 0/1 | no-code |
| `triage/terminal:t4-manifest-repair` | t4 | 0/1 | no-code |

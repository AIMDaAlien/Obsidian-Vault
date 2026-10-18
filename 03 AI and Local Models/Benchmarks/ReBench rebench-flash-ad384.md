---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench]
publish: true
created: 2026-09-23
machine: bigrig
title: "ReBench rebench-flash-ad384"
---
# ReBench rebench-flash-ad384

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

Generated 2026-09-23 00:37 from `results/rebench-flash-ad384.json`.

| target | checks | tasks | decode t/s (med) | TTFT s (med) | wall s | caps hit | errors |
|---|---|---|---|---|---|---|---|
| flashnext-ad384-131k | 187/213 (88%) | 77/98 | 16.4 | 4.66 | 7441.1 | 0 | 11 |

## flashnext-ad384-131k
_Qwen3.8-Flash-Next 176B AD384 IQ4_XS, -ngl 99 with expert FFN on CPU, 131072 ctx. Thinking is pinned server-side to reasoning_effort=low, so thinking=null inherits it. Prior: LCB-60 54/60 (quality king) @16.9 t/s, swe40 105/112._

### by domain

| domain | checks | tasks | decode t/s (med) |
|---|---|---|---|
| backend | 9/9 (100%) | 9/9 | 17.1 |
| code | 131/131 (100%) | 46/46 | 17.4 |
| deepswe | 0/6 (0%) | 0/6 | 15.9 |
| research | 46/56 (82%) | 21/26 | 14.6 |
| terminal | 1/11 (9%) | 1/11 | 16.3 |

### by tier

| tier | checks | tasks | decode t/s (med) |
|---|---|---|---|
| t1 | 57/60 (95%) | 23/25 | 15.8 |
| t2 | 29/40 (72%) | 13/20 | 17.1 |
| t3 | 45/53 (85%) | 18/26 | 16.4 |
| t4 | 56/60 (93%) | 23/27 | 16.3 |

### failures (executed verdicts, no judge)

| task | tier | score | detail |
|---|---|---|---|
| `research/r1-retention-3` | t1 | 0/2 | 0/2 |
| `terminal/t1-log-counts` | t1 | 0/1 | no-code |
| `deepswe/d1-worker-drain` | t2 | 0/1 | patch-failed: error: dq/worker.py: patch does not apply |
| `research/r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `terminal/t2-fix-runner` | t2 | 0/1 | no-code |
| `terminal/t2-stale-cleanup` | t2 | 0/1 | no-code |
| `triage/deepswe:d1-worker-drain` | t2 | 0/1 | patch-failed: patch: **** malformed patch at line 25: -            self.handler(item) |
| `triage/research:r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `triage/terminal:t2-fix-runner` | t2 | 0/1 | no-code |
| `deepswe/d2-guards-history` | t3 | 0/1 | patch-failed: patch: **** malformed patch at line 81: diff --git a/sm/validate.py b/sm/val |
| `deepswe/d3-config-precedence` | t3 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `research/r3-table-total` | t3 | 1/2 | 1/2 |
| `terminal/t3-csv-normalize` | t3 | 0/1 | no-code |
| `triage/deepswe:d2-guards-history` | t3 | 0/1 | patch-failed: patch: **** malformed patch at line 12: diff --git a/sm/machine.py b/sm/mach |
| `triage/deepswe:d3-config-precedence` | t3 | 0/1 | check-fail: AssertionError: {"host": "localhost", "port": 8080, "retries": 3, "verbose": f |
| `triage/research:r3-table-total` | t3 | 1/2 | 1/2 |
| `triage/terminal:t3-csv-normalize` | t3 | 0/1 | no-code |
| `terminal/t4-git-rescue` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'recovered.txt' |
| `terminal/t4-manifest-repair` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'repair.json' |
| `triage/terminal:t4-git-rescue` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'recovered.txt' |
| `triage/terminal:t4-manifest-repair` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'repair.json' |

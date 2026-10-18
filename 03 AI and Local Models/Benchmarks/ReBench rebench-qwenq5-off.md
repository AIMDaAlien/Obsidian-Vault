---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench]
publish: true
created: 2026-09-23
machine: bigrig
title: "ReBench rebench-qwenq5-off"
---
# ReBench rebench-qwenq5-off

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

Generated 2026-09-23 00:37 from `results/rebench-qwenq5-off.json`.

| target | checks | tasks | decode t/s (med) | TTFT s (med) | wall s | caps hit | errors |
|---|---|---|---|---|---|---|---|
| qwen38-27b-q5-mtp-off | 187/213 (88%) | 76/98 | 30.2 | 0.53 | 894.1 | 0 | 13 |

## qwen38-27b-q5-mtp-off
_Same weights/regime as -low, thinking disabled per request. Prior LCB-60 33/59: the policy costs this model ~15 points. Kept in the roster to measure that gap on the new suite, not to recommend it._

### by domain

| domain | checks | tasks | decode t/s (med) |
|---|---|---|---|
| backend | 9/9 (100%) | 9/9 | 30.2 |
| code | 131/131 (100%) | 46/46 | 30.8 |
| deepswe | 0/6 (0%) | 0/6 | 30.0 |
| research | 44/56 (79%) | 18/26 | 27.1 |
| terminal | 3/11 (27%) | 3/11 | 30.1 |

### by tier

| tier | checks | tasks | decode t/s (med) |
|---|---|---|---|
| t1 | 59/60 (98%) | 24/25 | 31.5 |
| t2 | 31/40 (78%) | 15/20 | 30.3 |
| t3 | 43/53 (81%) | 16/26 | 30.1 |
| t4 | 54/60 (90%) | 21/27 | 30.1 |

### failures (executed verdicts, no judge)

| task | tier | score | detail |
|---|---|---|---|
| `terminal/t1-log-counts` | t1 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-lz51zo38/_model.sh: line 1: `def main() |
| `deepswe/d1-worker-drain` | t2 | 0/1 | patch-failed: patch: **** malformed patch at line 11: diff --git a/dq/worker.py b/dq/worke |
| `research/r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `terminal/t2-stale-cleanup` | t2 | 0/1 | check-fail: AssertionError: ['pid_101.txt', 'pid_102.txt', 'pid_103.txt', 'pid_104.txt', ' |
| `triage/deepswe:d1-worker-drain` | t2 | 0/1 | patch-failed: patch: **** malformed patch at line 11: diff --git a/dq/worker.py b/dq/worke |
| `triage/research:r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `deepswe/d2-guards-history` | t3 | 0/1 | patch-failed: patch: **** malformed patch at line 20: +        return trans, None, None |
| `deepswe/d3-config-precedence` | t3 | 0/1 | patch-failed: patch: **** malformed patch at line 28: |
| `research/r3-table-q3sum` | t3 | 1/2 | 1/2 |
| `research/r3-table-total` | t3 | 1/2 | 1/2 |
| `terminal/t3-csv-normalize` | t3 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-6cgq0mfl/_model.sh: line 5: `def normal |
| `triage/deepswe:d2-guards-history` | t3 | 0/1 | patch-failed: patch: **** malformed patch at line 20: +            return trans[target] |
| `triage/deepswe:d3-config-precedence` | t3 | 0/1 | patch-failed: patch: **** malformed patch at line 28: |
| `triage/research:r3-table-q3sum` | t3 | 1/2 | 1/2 |
| `triage/research:r3-table-total` | t3 | 1/2 | 1/2 |
| `triage/terminal:t3-csv-normalize` | t3 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-wp1nykal/_model.sh: line 5: `def normal |
| `research/r4-team-rollup` | t4 | 1/2 | 1/2 |
| `terminal/t4-git-rescue` | t4 | 0/1 | no-code |
| `terminal/t4-manifest-repair` | t4 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-dx8vrtpx/_model.sh: line 7: `def sha256 |
| `triage/research:r4-team-rollup` | t4 | 1/2 | 1/2 |
| `triage/terminal:t4-git-rescue` | t4 | 0/1 | no-code |
| `triage/terminal:t4-manifest-repair` | t4 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-c4jvw2ae/_model.sh: line 7: `def sha256 |

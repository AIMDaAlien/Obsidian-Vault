---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench]
publish: true
created: 2026-09-23
machine: bigrig
title: "ReBench rebench-laguna"
---
# ReBench rebench-laguna

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

Generated 2026-09-23 00:37 from `results/rebench-laguna.json`.

| target | checks | tasks | decode t/s (med) | TTFT s (med) | wall s | caps hit | errors |
|---|---|---|---|---|---|---|---|
| unraid-laguna-xs21-q4 | 175/213 (82%) | 67/98 | 36.1 | 0.51 | 1917.4 | 0 | 14 |

## unraid-laguna-xs21-q4
_Laguna XS-2.1 33B Q4_K_M (3B active) on Unraid, container llm-laguna-xs21, host port 18007. Prior: LCB-60 46/60 @34 t/s with thinking OFF. No expect_model set (alias unverified — the endpoint was down when this roster was written); confirm the served model name on first run._

### by domain

| domain | checks | tasks | decode t/s (med) |
|---|---|---|---|
| backend | 6/9 (67%) | 6/9 | 33.7 |
| code | 131/131 (100%) | 46/46 | 36.8 |
| deepswe | 0/6 (0%) | 0/6 | 34.0 |
| research | 38/56 (68%) | 15/26 | 33.8 |
| terminal | 0/11 (0%) | 0/11 | 31.3 |

### by tier

| tier | checks | tasks | decode t/s (med) |
|---|---|---|---|
| t1 | 57/60 (95%) | 23/25 | 37.0 |
| t2 | 28/40 (70%) | 12/20 | 36.0 |
| t3 | 40/53 (75%) | 13/26 | 34.8 |
| t4 | 50/60 (83%) | 19/27 | 36.1 |

### failures (executed verdicts, no judge)

| task | tier | score | detail |
|---|---|---|---|
| `research/r1-retention-3` | t1 | 0/2 | 0/2 |
| `terminal/t1-log-counts` | t1 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-y_gnu_46/_model.sh: line 1: `def main() |
| `deepswe/d1-worker-drain` | t2 | 0/1 | patch-failed: patch: **** malformed patch at line 7: -from .dqueue import Worker, BoundedQ |
| `research/r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `research/r2-port-to-team` | t2 | 2/3 | 2/3 |
| `terminal/t2-fix-runner` | t2 | 0/1 | no-code |
| `terminal/t2-stale-cleanup` | t2 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-_ywrat97/_model.sh: line 3: `def main() |
| `triage/deepswe:d1-worker-drain` | t2 | 0/1 | patch-failed: patch: **** malformed patch at line 7: -from .dqueue import Worker, BoundedQ |
| `triage/research:r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `triage/terminal:t2-fix-runner` | t2 | 0/1 | no-code |
| `backend/b3-cursor-pagination` | t3 | 0/1 | check-fail: benchmod.CursorError: bad cursor |
| `deepswe/d2-guards-history` | t3 | 0/1 | patch-failed: patch: **** malformed patch at line 69: |
| `deepswe/d3-config-precedence` | t3 | 0/1 | patch-failed: patch: **** Only garbage was found in the patch input. |
| `research/r3-table-argmax` | t3 | 2/3 | 2/3 |
| `research/r3-table-q3sum` | t3 | 1/2 | 1/2 |
| `research/r3-table-total` | t3 | 1/2 | 1/2 |
| `terminal/t3-csv-normalize` | t3 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-7nu4upj8/_model.sh: line 4: `def proces |
| `terminal/t3-perm-audit` | t3 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'tree/a/secret.txt' |
| `triage/deepswe:d2-guards-history` | t3 | 0/1 | patch-failed: patch: **** malformed patch at line 69: |
| `triage/deepswe:d3-config-precedence` | t3 | 0/1 | patch-failed: patch: **** malformed patch at line 28: -        config['retries'] = args.re |
| `triage/research:r3-table-q3sum` | t3 | 1/2 | 1/2 |
| `triage/research:r3-table-total` | t3 | 1/2 | 1/2 |
| `triage/terminal:t3-csv-normalize` | t3 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-n2s5y9si/_model.sh: line 4: `def proces |
| `backend/b4-http-service` | t4 | 0/1 | check-fail: AssertionError: (404, {'error': 'not found'}) |
| `research/r4-port-hunt` | t4 | 0/2 | 0/2 |
| `terminal/t4-git-rescue` | t4 | 0/1 | no-code |
| `terminal/t4-manifest-repair` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'repair.json' |
| `triage/backend:b4-http-service` | t4 | 0/1 | check-fail: AssertionError: (404, {'error': 'not found'}) |
| `triage/research:r4-port-hunt` | t4 | 0/2 | 0/2 |
| `triage/terminal:t4-git-rescue` | t4 | 0/1 | no-code |
| `triage/terminal:t4-manifest-repair` | t4 | 0/1 | check-fail: AssertionError: {'corrupt': ['gamma.bin'], 'missing': ['delta.bin', 'gamma.bin |

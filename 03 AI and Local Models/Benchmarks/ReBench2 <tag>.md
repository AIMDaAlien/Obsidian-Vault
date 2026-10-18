---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench]
publish: true
created: 2026-09-23
machine: bigrig
title: "ReBench2 <tag>"
---

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

# ReBench2 <tag>

Generated 2026-09-23 19:52 from `results/rebench2-ornith.json`.

| target | checks | tasks | decode t/s (med) | TTFT s (med) | wall s | caps hit | errors |
|---|---|---|---|---|---|---|---|
| ornith-23g-131k | 194/229 (85%) | 84/114 | 59.0 | 0.24 | 5072.4 | 0 | 13 |

## ornith-23g-131k
_Ornith-1.5-35B-A3B MTPv2-23G-ICE, dual-GPU layer split, 128K ctx. Prior: swe40 110/112 39/40 @~61 t/s (best swe40 of any config). LCB-60 never measured — this campaign fills that gap._

### by domain

| domain | checks | tasks | decode t/s (med) |
|---|---|---|---|
| backend | 9/9 (100%) | 9/9 | 58.5 |
| code | 131/131 (100%) | 46/46 | 59.3 |
| deepswe | 2/14 (14%) | 2/14 | 58.1 |
| research | 48/56 (86%) | 23/26 | 57.1 |
| terminal | 4/19 (21%) | 4/19 | 59.4 |

### by tier

| tier | checks | tasks | decode t/s (med) |
|---|---|---|---|
| t1 | 57/60 (95%) | 23/25 | 59.5 |
| t2 | 34/45 (76%) | 18/25 | 58.9 |
| t3 | 47/60 (78%) | 20/33 | 59.0 |
| t4 | 56/64 (88%) | 23/31 | 59.0 |

### by role

| role | checks | tasks | decode t/s (med) |
|---|---|---|---|
| agentic | 144/159 (91%) | 59/74 | 59.2 |
| batch-research | 25/33 (76%) | 12/15 | 57.2 |
| deepswe | 2/14 (14%) | 2/14 | 58.1 |
| obscure-research | 23/23 (100%) | 11/11 | 56.9 |

### failures (executed verdicts, no judge)

| task | tier | score | detail |
|---|---|---|---|
| `research/r1-retention-3` | t1 | 0/2 | 0/2 |
| `terminal/t1-log-counts` | t1 | 0/1 | no-code |
| `deepswe/d1-worker-drain` | t2 | 0/1 | no-file-blocks |
| `deepswe/d4-retry-backoff` | t2 | 0/1 | no-file-blocks |
| `deepswe/d9-secret-redact` | t2 | 0/1 | check-fail: AssertionError |
| `research/r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `terminal/t2-stale-cleanup` | t2 | 0/1 | no-code |
| `triage/deepswe:d1-worker-drain` | t2 | 0/1 | no-file-blocks |
| `triage/research:r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `deepswe/d2-guards-history` | t3 | 0/1 | no-file-blocks |
| `deepswe/d3-config-precedence` | t3 | 0/1 | no-file-blocks |
| `deepswe/d6-dead-letter` | t3 | 0/1 | check-fail: ImportError: cannot import name 'DeadLetterError' from 'courier.engine' (/home |
| `deepswe/d8-config-overlay` | t3 | 0/1 | no-file-blocks |
| `terminal/t3-backup-prune` | t3 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'pruned.txt' |
| `terminal/t3-csv-normalize` | t3 | 0/1 | no-code |
| `terminal/t3-disk-pressure` | t3 | 0/1 | no-code |
| `terminal/t3-patch-apply` | t3 | 0/1 | no-code |
| `terminal/t3-perm-audit` | t3 | 0/1 | no-code |
| `terminal/t3-symlink-repair` | t3 | 0/1 | no-code |
| `triage/deepswe:d2-guards-history` | t3 | 0/1 | no-file-blocks |
| `triage/deepswe:d3-config-precedence` | t3 | 0/1 | no-file-blocks |
| `triage/terminal:t3-csv-normalize` | t3 | 0/1 | no-code |
| `deepswe/d10-checkpoint-resume` | t4 | 0/1 | no-file-blocks |
| `deepswe/d11-migration-runner` | t4 | 0/1 | check-fail: AttributeError: 'tuple' object has no attribute '__name__'. Did you mean: '__n |
| `terminal/t4-config-diff` | t4 | 0/1 | no-code |
| `terminal/t4-git-rescue` | t4 | 0/1 | no-code |
| `terminal/t4-manifest-repair` | t4 | 0/1 | no-code |
| `terminal/t4-restart-wait` | t4 | 0/1 | check-fail: AssertionError: [] |
| `triage/terminal:t4-git-rescue` | t4 | 0/1 | no-code |
| `triage/terminal:t4-manifest-repair` | t4 | 0/1 | no-code |

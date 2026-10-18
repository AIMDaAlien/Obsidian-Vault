---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench]
publish: true
created: 2026-09-24
machine: bigrig
title: "Flash-Next effort sweep: eff-flash-lowlen"
---

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

# Flash-Next effort sweep: eff-flash-lowlen

Generated 2026-09-24 11:54 from `results/eff-flash-lowlen.json`.

| target | checks | tasks | decode t/s (med) | TTFT s (med) | wall s | caps hit | errors |
|---|---|---|---|---|---|---|---|
| flashnext-ad384-131k | 190/229 (83%) | 80/114 | 15.1 | 5.54 | 8930.4 | 0 | 7 |

## flashnext-ad384-131k
_Qwen3.8-Flash-Next 176B AD384 IQ4_XS, -ngl 99 with expert FFN on CPU, 131072 ctx. Thinking is pinned server-side to reasoning_effort=low, so thinking=null inherits it. Prior: LCB-60 54/60 (quality king) @16.9 t/s, swe40 105/112._

### by domain

| domain | checks | tasks | decode t/s (med) |
|---|---|---|---|
| backend | 9/9 (100%) | 9/9 | 16.1 |
| code | 131/131 (100%) | 46/46 | 15.4 |
| deepswe | 2/14 (14%) | 2/14 | 16.4 |
| research | 47/56 (84%) | 22/26 | 12.4 |
| terminal | 1/19 (5%) | 1/19 | 15.5 |

### by tier

| tier | checks | tasks | decode t/s (med) |
|---|---|---|---|
| t1 | 57/60 (95%) | 23/25 | 13.9 |
| t2 | 30/45 (67%) | 14/25 | 14.8 |
| t3 | 47/60 (78%) | 20/33 | 15.5 |
| t4 | 56/64 (88%) | 23/31 | 15.4 |

### by role

| role | checks | tasks | decode t/s (med) |
|---|---|---|---|
| agentic | 141/159 (89%) | 56/74 | 15.5 |
| batch-research | 25/33 (76%) | 12/15 | 13.5 |
| deepswe | 2/14 (14%) | 2/14 | 16.4 |
| obscure-research | 22/23 (96%) | 10/11 | 9.6 |

### failures (executed verdicts, no judge)

| task | tier | score | detail |
|---|---|---|---|
| `research/r1-retention-3` | t1 | 0/2 | 0/2 |
| `terminal/t1-log-counts` | t1 | 0/1 | no-code |
| `deepswe/d1-worker-drain` | t2 | 0/1 | check-fail: AttributeError: 'Worker' object has no attribute 'metrics' |
| `deepswe/d4-retry-backoff` | t2 | 0/1 | check-fail: TypeError: Object of type function is not JSON serializable |
| `deepswe/d9-secret-redact` | t2 | 0/1 | check-fail: AttributeError: 'int' object has no attribute 'lower' |
| `research/r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `terminal/t2-fix-runner` | t2 | 0/1 | check-fail: AssertionError: exit 1: run.sh: line 3: lib/util: No such file or directory |
| `terminal/t2-log-rotate` | t2 | 0/1 | model-exit127: ~/.hermes/cache/scratch/bench-aw48s_om/_model.sh: line 3: -rw-r--r- |
| `terminal/t2-stale-cleanup` | t2 | 0/1 | check-fail: AssertionError: ['pid_101.txt', 'pid_102.txt', 'pid_103.txt', 'pid_104.txt', ' |
| `terminal/t2-vram-report` | t2 | 0/1 | model-exit127: ~/.hermes/cache/scratch/bench-sqg90tcv/_model.sh: line 5: MAX: comm |
| `triage/deepswe:d1-worker-drain` | t2 | 0/1 | check-fail: AttributeError: 'Worker' object has no attribute 'metrics' |
| `triage/research:r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `triage/terminal:t2-fix-runner` | t2 | 0/1 | check-fail: AssertionError: exit 1: run.sh: line 3: lib/util: No such file or directory |
| `deepswe/d2-guards-history` | t3 | 0/1 | check-fail: ImportError: cannot import name 'UnknownState' from 'sm' (~/.hermes/ca |
| `deepswe/d3-config-precedence` | t3 | 0/1 | check-fail: AssertionError: (0, '') |
| `deepswe/d5-rate-limiter` | t3 | 0/1 | check-fail: AssertionError |
| `deepswe/d8-config-overlay` | t3 | 0/1 | check-fail: AssertionError: {'a': 1, 'nested': {'y': 2}, 'keep': {'z': 9}, 'missing': {'de |
| `terminal/t3-backup-prune` | t3 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-mb1iicot/_model.sh: line 1: `<parameter |
| `terminal/t3-csv-normalize` | t3 | 0/1 | no-code |
| `terminal/t3-disk-pressure` | t3 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'disk-top.txt' |
| `terminal/t3-patch-apply` | t3 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-9voqrrd4/_model.sh: line 6: `}' |
| `terminal/t3-symlink-repair` | t3 | 0/1 | check-fail: AssertionError: ('a', 'still dangling') |
| `triage/deepswe:d2-guards-history` | t3 | 0/1 | check-fail: ImportError: cannot import name 'UnknownState' from 'sm' (~/.hermes/ca |
| `triage/deepswe:d3-config-precedence` | t3 | 0/1 | check-fail: AssertionError: (0, '') |
| `triage/research:r3-table-total` | t3 | 1/2 | 1/2 |
| `triage/terminal:t3-csv-normalize` | t3 | 0/1 | no-code |
| `deepswe/d10-checkpoint-resume` | t4 | 0/1 | no-file-blocks |
| `deepswe/d11-migration-runner` | t4 | 0/1 | check-fail: AttributeError: 'MemDB' object has no attribute 'conn' |
| `terminal/t4-config-diff` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'config.diff' |
| `terminal/t4-git-rescue` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'recovered.txt' |
| `terminal/t4-manifest-repair` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'repair.json' |
| `terminal/t4-restart-wait` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'restarted.txt' |
| `triage/terminal:t4-git-rescue` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'recovered.txt' |
| `triage/terminal:t4-manifest-repair` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'repair.json' |

---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench]
publish: true
created: 2026-09-24
machine: bigrig
title: "Flash-Next effort sweep: eff-flash-med"
---

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

# Flash-Next effort sweep: eff-flash-med

Generated 2026-09-24 11:54 from `results/eff-flash-med.json`.

| target | checks | tasks | decode t/s (med) | TTFT s (med) | wall s | caps hit | errors |
|---|---|---|---|---|---|---|---|
| flashnext-ad384-131k-med | 191/229 (83%) | 80/114 | 17.1 | 5.16 | 8275.1 | 0 | 9 |

## flashnext-ad384-131k-med
_Qwen3.8-Flash-Next AD384, reasoning_effort=medium sent PER-REQUEST via chat_template_kwargs (verified 2026-09-23: request overrides the unit's low pin; template supports low/medium/xhigh only, no off). Effort sweep variant of flashnext-ad384-131k._

### by domain

| domain | checks | tasks | decode t/s (med) |
|---|---|---|---|
| backend | 9/9 (100%) | 9/9 | 17.1 |
| code | 131/131 (100%) | 46/46 | 17.2 |
| deepswe | 1/14 (7%) | 1/14 | 16.9 |
| research | 49/56 (88%) | 23/26 | 15.3 |
| terminal | 1/19 (5%) | 1/19 | 17.3 |

### by tier

| tier | checks | tasks | decode t/s (med) |
|---|---|---|---|
| t1 | 59/60 (98%) | 24/25 | 17.0 |
| t2 | 31/45 (69%) | 15/25 | 17.1 |
| t3 | 45/60 (75%) | 18/33 | 17.1 |
| t4 | 56/64 (88%) | 23/31 | 17.1 |

### by role

| role | checks | tasks | decode t/s (med) |
|---|---|---|---|
| agentic | 141/159 (89%) | 56/74 | 17.2 |
| batch-research | 27/33 (82%) | 13/15 | 15.3 |
| deepswe | 1/14 (7%) | 1/14 | 16.9 |
| obscure-research | 22/23 (96%) | 10/11 | 15.4 |

### failures (executed verdicts, no judge)

| task | tier | score | detail |
|---|---|---|---|
| `terminal/t1-log-counts` | t1 | 0/1 | no-code |
| `deepswe/d1-worker-drain` | t2 | 0/1 | check-timeout |
| `deepswe/d4-retry-backoff` | t2 | 0/1 | check-fail: requests.exceptions.MissingSchema: Invalid URL '<function flaky_maker.<locals> |
| `deepswe/d9-secret-redact` | t2 | 0/1 | check-fail: AttributeError: 'int' object has no attribute 'lower' |
| `research/r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `terminal/t2-fix-runner` | t2 | 0/1 | check-fail: AssertionError: exit 1: run.sh: line 3: lib/util: No such file or directory |
| `terminal/t2-stale-cleanup` | t2 | 0/1 | no-code |
| `terminal/t2-vram-report` | t2 | 0/1 | no-code |
| `triage/deepswe:d1-worker-drain` | t2 | 0/1 | check-timeout |
| `triage/research:r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `triage/terminal:t2-fix-runner` | t2 | 0/1 | check-fail: AssertionError: exit 1: run.sh: line 3: lib/util: No such file or directory |
| `deepswe/d2-guards-history` | t3 | 0/1 | check-fail: ImportError: cannot import name 'UnknownState' from 'sm' (~/.hermes/ca |
| `deepswe/d3-config-precedence` | t3 | 0/1 | check-fail: AssertionError: (0, '') |
| `deepswe/d5-rate-limiter` | t3 | 0/1 | check-fail: StopIteration |
| `deepswe/d6-dead-letter` | t3 | 0/1 | check-fail: ImportError: cannot import name 'DeadLetterError' from 'courier.engine' (/home |
| `deepswe/d8-config-overlay` | t3 | 0/1 | check-fail: AssertionError: {'a': 1, 'nested': {'y': 2}, 'keep': {'z': 9}, 'missing': {'de |
| `research/r3-table-argmax` | t3 | 2/3 | 2/3 |
| `terminal/t3-backup-prune` | t3 | 0/1 | check-fail: AssertionError: ['snap-20260910-000000.tar', 'snap-20260911-000000.tar', 'snap |
| `terminal/t3-csv-normalize` | t3 | 0/1 | model-timeout |
| `terminal/t3-disk-pressure` | t3 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'disk-top.txt' |
| `terminal/t3-patch-apply` | t3 | 0/1 | no-code |
| `terminal/t3-perm-audit` | t3 | 0/1 | check-fail: AssertionError: ['tree/a/public.txt 0644', 'tree/a/secret.txt 0600', 'tree/b/s |
| `terminal/t3-symlink-repair` | t3 | 0/1 | check-fail: AssertionError: ('a', 'still dangling') |
| `triage/deepswe:d2-guards-history` | t3 | 0/1 | check-fail: ImportError: cannot import name 'UnknownState' from 'sm' (~/.hermes/ca |
| `triage/deepswe:d3-config-precedence` | t3 | 0/1 | check-fail: AssertionError: (0, '') |
| `triage/terminal:t3-csv-normalize` | t3 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-q0k5gqgt/_model.sh: line 9: `with open( |
| `deepswe/d10-checkpoint-resume` | t4 | 0/1 | check-fail: ValueError: broken part |
| `deepswe/d11-migration-runner` | t4 | 0/1 | check-fail: AttributeError: 'tuple' object has no attribute '__name__'. Did you mean: '__n |
| `terminal/t4-config-diff` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'config.diff' |
| `terminal/t4-git-rescue` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'recovered.txt' |
| `terminal/t4-manifest-repair` | t4 | 0/1 | no-code |
| `terminal/t4-restart-wait` | t4 | 0/1 | check-fail: AssertionError: [] |
| `triage/terminal:t4-git-rescue` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'recovered.txt' |
| `triage/terminal:t4-manifest-repair` | t4 | 0/1 | no-code |

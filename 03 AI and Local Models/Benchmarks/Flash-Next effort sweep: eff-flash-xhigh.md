---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench]
publish: true
created: 2026-09-24
machine: bigrig
title: "Flash-Next effort sweep: eff-flash-xhigh"
---

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

# Flash-Next effort sweep: eff-flash-xhigh

Generated 2026-09-24 11:54 from `results/eff-flash-xhigh.json`.

| target | checks | tasks | decode t/s (med) | TTFT s (med) | wall s | caps hit | errors |
|---|---|---|---|---|---|---|---|
| flashnext-ad384-131k-xhigh | 181/229 (79%) | 76/114 | 16.2 | 5.63 | 36645.2 | 0 | 11 |

## flashnext-ad384-131k-xhigh
_Qwen3.8-Flash-Next AD384, reasoning_effort=xhigh sent PER-REQUEST via chat_template_kwargs (verified 2026-09-23: request overrides the unit's low pin; template supports low/medium/xhigh only, no off). Effort sweep variant of flashnext-ad384-131k._

### by domain

| domain | checks | tasks | decode t/s (med) |
|---|---|---|---|
| backend | 4/9 (44%) | 4/9 | 16.1 |
| code | 121/131 (92%) | 42/46 | 17.2 |
| deepswe | 1/14 (7%) | 1/14 | 16.1 |
| research | 48/56 (86%) | 22/26 | 15.2 |
| terminal | 7/19 (37%) | 7/19 | 16.1 |

### by tier

| tier | checks | tasks | decode t/s (med) |
|---|---|---|---|
| t1 | 60/60 (100%) | 25/25 | 16.2 |
| t2 | 32/45 (71%) | 16/25 | 16.9 |
| t3 | 45/60 (75%) | 18/33 | 16.2 |
| t4 | 44/64 (69%) | 17/31 | 15.9 |

### by role

| role | checks | tasks | decode t/s (med) |
|---|---|---|---|
| agentic | 132/159 (83%) | 53/74 | 16.9 |
| batch-research | 27/33 (82%) | 13/15 | 15.3 |
| deepswe | 1/14 (7%) | 1/14 | 16.1 |
| obscure-research | 21/23 (91%) | 9/11 | 15.0 |

### failures (executed verdicts, no judge)

| task | tier | score | detail |
|---|---|---|---|
| `backend/b2-config-merge` | t2 | 0/1 | check-fail: ImportError: cannot import name 'load_config' from 'benchmod' (~/.herm |
| `deepswe/d1-worker-drain` | t2 | 0/1 | check-fail: SyntaxError: invalid syntax |
| `deepswe/d4-retry-backoff` | t2 | 0/1 | no-file-blocks |
| `deepswe/d9-secret-redact` | t2 | 0/1 | check-fail: ImportError: cannot import name 'redact' from 'guarddog.redact' (~/.he |
| `research/r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `terminal/t2-stale-cleanup` | t2 | 0/1 | no-code |
| `terminal/t2-vram-report` | t2 | 0/1 | no-code |
| `triage/deepswe:d1-worker-drain` | t2 | 0/1 | no-file-blocks |
| `triage/research:r2-legacy-owner` | t2 | 0/3 | 0/3 |
| `backend/b3-cursor-pagination` | t3 | 0/1 | check-fail: ImportError: cannot import name 'paginate' from 'benchmod' (~/.hermes/ |
| `deepswe/d2-guards-history` | t3 | 0/1 | no-file-blocks |
| `deepswe/d3-config-precedence` | t3 | 0/1 | check-fail: json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| `deepswe/d5-rate-limiter` | t3 | 0/1 | check-fail: SyntaxError: invalid syntax |
| `deepswe/d6-dead-letter` | t3 | 0/1 | check-fail: ImportError: cannot import name 'Delivery' from 'courier.engine' (~/.h |
| `deepswe/d8-config-overlay` | t3 | 0/1 | no-file-blocks |
| `research/r3-table-total` | t3 | 1/2 | 1/2 |
| `terminal/t3-csv-normalize` | t3 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'out/normalized.csv' |
| `terminal/t3-disk-pressure` | t3 | 0/1 | check-fail: AssertionError: ([(354692554, 'lib/systemd/coredump/core.llama-server.1000.923 |
| `terminal/t3-patch-apply` | t3 | 0/1 | model-exit2: ls: cannot access '/workspace/': No such file or directory |
| `terminal/t3-perm-audit` | t3 | 0/1 | check-fail: AssertionError: [] |
| `terminal/t3-symlink-repair` | t3 | 0/1 | no-code |
| `triage/deepswe:d2-guards-history` | t3 | 0/1 | no-file-blocks |
| `triage/deepswe:d3-config-precedence` | t3 | 0/1 | check-fail: json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
| `triage/research:r3-table-total` | t3 | 1/2 | 1/2 |
| `backend/b4-http-service` | t4 | 0/1 | check-fail: AssertionError: server never became healthy |
| `backend/b4-migrations` | t4 | 0/1 | no-code |
| `code/t4-lru-ttl` | t4 | 0/3 | no-code |
| `code/t4-skyline` | t4 | 0/2 | no-code |
| `deepswe/d10-checkpoint-resume` | t4 | 0/1 | no-file-blocks |
| `deepswe/d11-migration-runner` | t4 | 0/1 | no-file-blocks |
| `terminal/t4-config-diff` | t4 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-usr4i1ju/_model.sh: line 4: `KEY_RE = r |
| `terminal/t4-git-rescue` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'recovered.txt' |
| `terminal/t4-manifest-repair` | t4 | 0/1 | model-exit2: ~/.hermes/cache/scratch/bench-5y92ghn1/_model.sh: line 4: `DATA = Pat |
| `triage/backend:b4-http-service` | t4 | 0/1 | check-fail: AssertionError: server never became healthy |
| `triage/code:t4-lru-ttl` | t4 | 0/3 | no-code |
| `triage/code:t4-skyline` | t4 | 0/2 | no-code |
| `triage/terminal:t4-git-rescue` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'recovered.txt' |
| `triage/terminal:t4-manifest-repair` | t4 | 0/1 | check-fail: FileNotFoundError: [Errno 2] No such file or directory: 'repair.json' |

---
type: note
category: Benchmarks
tags: [omarchy, benchmarks]
updated: 2026-09-24
publish: true
created: 2026-09-24
machine: bigrig
title: "2026-09-24 Flash-Next Effort Sweep — Lenified Grader (low / medium / xhigh)"
featured: 46
summary: "Telling an AI to think harder made it slower and less accurate: maximum effort took 4x longer and scored worse."
---

# 2026-09-24 Flash-Next Effort Sweep — Lenified Grader (low / medium / xhigh)

Question: does flash-next at higher reasoning_effort beat qwen-low 196/229 (85.6%) on its own test set, and is the effort pin what costs it points?

## Setup
- Grader lenified BEFORE the sweep (2026-09-23): bench_lib.agent_code() tolerates flash's tool-call dialect in terminal tasks (antml parameter blocks + JSON tool_use), extract_files accepts the relpath on the line AFTER ```file. selftest 0 failures. Old rebench2-flash2 answers were truncated at 400 chars so they could not be re-graded post-hoc; eff-flash-lowlen is the fresh low anchor on the new grader, with full answers now saved to results/<tag>.answers.jsonl.
- Effort sent per-request via chat_template_kwargs (verified to override the unit's low pin). Template supports low / medium / xhigh ONLY — off/high rejected. Targets flashnext-ad384-131k-med / -xhigh added.

## Results (229 checks, 114 rows)

| config | checks | full | decode | wall | verdict |
|---|---|---|---|---|---|
| qwen38-27b-q5-mtp-low | **196/229 (85.6%)** | 86/114 | 28.9 t/s | 52 min | still the quality king |
| flash @ low (lenified, eff-flash-lowlen) | 190/229 (83.0%) | 80/114 | 15.2 t/s | 149 min | = flash2's 191 within noise |
| flash @ medium (eff-flash-med) | 191/229 (83.4%) | 80/114 | 17.1 t/s | 149 min | +1 check over low |
| flash @ xhigh (eff-flash-xhigh) | 181/229 (79.0%) | 76/114 | 16.2 t/s | 611 min | WORSE and 4x slower |

Per-pack: backend 6/6 6/6 2/6 | code 112 112 107 | deepswe 2/11 1/11 1/11 | research 38/43 39/43 39/43 | terminal 1/15 1/15 5/15 (low/med/xhigh).

## Verdict

1. **No. Flash does not beat qwen-low 196/229 at ANY effort level.** Peak is 191/229 at medium (83.4%), -5 checks behind qwen-low, at half the speed (17 vs 29 t/s) and 3x the wall time.
2. **The effort pin is NOT what costs it points.** low→medium moves 190→191 (noise). xhigh is a clear REGRESSION: thinking eats the 12,288-token budget before any artifact (8 no-code + 7 no-file-blocks at xhigh vs 3+1 at low), backend collapses 6/6→2/6, and wall time quadruples. Flash's effort pin at low is already optimal.
3. Terminal at xhigh (5/15 vs 1/15) is the one place more effort helped — thinking long enough to produce proper shell. Everywhere else it lost points.

## Grading decisions
- Tool-call dialect tolerance (agent_code): ADOPTED and kept — honest end-state grading, selftested, never fires on fenced answers. But it did NOT rescue the terminal pack at low/med (1/15 unchanged): flash's tool-call answers at low/med include Read-tool calls (not runnable commands) and its commands fail real checks. Terminal stays a genuine flash weakness, not a harness artifact.
- extract_files relpath-next-line: ADOPTED — removes the fake no-file-blocks contract tax (flash2 had 3 of them; deepswe failures are now all earned check-fails).
- Conformance tax verdict: flash2's "20 format losses vs qwen 11" was PARTLY harness (file-block fence format), partly intrinsic (tool-call dialect at low effort). After lenification the gap to qwen-low is real reasoning/perf, not format.

Charts: results/charts/pareto_checks.png (regenerated with eff-flash-* series). Reports: results/eff-flash-{lowlen,med,xhigh}.md.

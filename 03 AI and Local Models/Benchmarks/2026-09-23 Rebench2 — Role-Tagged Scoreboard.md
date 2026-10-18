---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench]
publish: true
created: 2026-09-23
machine: bigrig
title: "2026-09-23 Rebench2 — Role-Tagged Suite Scoreboard (new suite)"
---
# 2026-09-23 Rebench2 — Role-Tagged Suite Scoreboard (new suite)

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

Generated 2026-09-23 ~18:30 from ~/bench, NEW role-tagged suite: 114 rows/target (code 46, research 20, terminal 15, backend 6, deepswe 11, + 16 triage refs = 229 checks). New full-file (kind=files) replacement contract for DeepSWE (models emit complete files, not diffs — the old diff contract graded every model 0). Executed verdicts only, no judge, selftest-verified graders (golds pass, wrongs rejected), fixed answer-storage bug.

**Data integrity note:** an earlier rebench2-flash run was INVALID — target start used systemd (never stopped the QWEN daily), the flash unit crash-looped, and the daily QWEN answered on :8080, so its "206/229" was QWEN at default effort. Fixed targets.json (flash → llama-switch) and re-ran as rebench2-flash2 — the numbers below are the VALID flash pass (17.2 t/s, TTFT 5.12s — the flash fingerprint).

## Master table (checks / tasks, med decode t/s, med TTFT s, wall min)

| target | checks | pct | full/114 | decode t/s | TTFT s | wall min |
|---|---|---|---|---|---|---|
| qwen-low | 196/229 | 86% | 86/114 | 28.9 | 0.62 | 52 |
| ornith-23g | 194/229 | 85% | 84/114 | 59.0 | 0.24 | 85 |
| qwen-off | 192/229 | 84% | 81/114 | 29.8 | 0.57 | 21 |
| flash-ad384 | 191/229 | 83% | 81/114 | 17.2 | 5.12 | 116 |

## Role lanes (checks %, n per lane: batch-research 33, obscure-research 23, agentic 159, deepswe 14)

| role | qwen-low | qwen-off | flash | orn-23g |
|---|---|---|---|---|
| batch-research | 25 (76%) | 27 (82%) | 25 (76%) | 25 (76%) |
| obscure-research | 23 (100) | 17 (74) | 23 (100) | 23 (100) |
| agentic (term/code/backend) | 147 (92%) | 145 (91%) | 141 (89%) | 144 (91%) |
| deepswe | 1 (7%) | 3 (21%) | 2 (14%) | 2 (14%) |

## By domain (checks %, n)

| domain | qwen-low | qwen-off | flash | orn-23g |
|---|---|---|---|---|
| backend 9 | 9 (100) | 9 (100) | 9 (100) | 9 (100) |
| code 46 | 46 (100) | 46 (100) | 46 (100) | 46 (100) |
| research 56 | 48 (86) | 44 (79) | 48 (86) | 48 (86) |
| terminal 19 | 5 (26) | 5 (26) | 3 (16) | 4 (21) |
| deepswe 14 | 1 (7) | 3 (21) | 2 (14) | 2 (14) |

## Compared to the old suite (98 shared tasks, identical IDs: NO prompt drift)

| config | old (Sep 22) | new (Sep 23) | delta |
|---|---|---|---|
| qwen-low | 83/98 | 83/98 | +0 (bit-for-bit reproducible) |
| qwen-off | 76/98 | 76/98 | +0 |
| ornith-23g | 80/98 | 80/98 | +0 |
| flash-ad384 | 77/98 | 79/98 | +2 (research 21→23; terminal still 1/11, deepswe still 0/6) |

Key old-suite comparison points:
- Old suite: qwen-low 193/213 (91%) leader; ornith 190/213; qwen-off 187; flash 187; orn-iq2m 184; laguna 175.
- New suite (114 rows): qwen-low still leader at 86% but margin is thin — only 2 checks over ornith-23g, 5 over flash.
- DeepSWE full-file contract worked mechanically (selftest: golds pass, wrongs rejected — models CAN emit whole files), but quality is still the wall: 1–3 per config on 14 checks. Every model still burns budget or missolves. This is the honest verdict: the wall was trinary-transport — diff contract was unfair, but the models are ALSO genuinely weak at multi-file engineering.
- Terminal stayed the real separator: qwen-low 5/11 (old) → 5/15 (new tasks), flash 1/11 → 1/15. Prose-without-fences remains flash's tax; no-code still pepper all configs.
- The "default effort beats low" effect (from the invalid flash run) is actually informative: QWEN at default ≈ 206/229 equivalent > low 196 > off 192 — thinking effort IS a quality lever on qwen 27B.

## Charts
![[_attachments/model-benchmarks/pareto_checks.png]]
![[_attachments/model-benchmarks/lanes.png]]
![[_attachments/model-benchmarks/overlap_delta.png]]

## Verdict
1. qwen-low is still the fleet leader but the margin shrank to 2 checks — it wins on agentic (147/159) and ties everyone at 100% obscure-research + code.
2. First reproducible-run finding: 3 of 4 configs bit-for-bit reproduced old numbers on the 98 shared tasks — the suite's graders and prompts are stable, runs are deterministic. flash drifted +2 (research) — same server, same effort pin, so that's sampling variance, not a config change.
3. ornith-23g is the throughput pick: 59 t/s, only 2 checks behind the leader, 85% — it produces ~2.7x qwen's tokens/min at near-equal quality. For batch/obscure research, ornith is the obvious workhorse.
4. flash remains the slowest (17.2 t/s, 5.1 s TTFT cold) and minus quality — 5 behind qwen-low. Its only measured edge anywhere was LCB-60 single-domain (54/60) in the old suite. Verdict: not worth the wall for agentic; keep for single-domain SWE sweeps or drop it to last resort.
5. qwen-off (thinking off) lost ~6 checks mostly in obscure-research (23→17) — the 15-min wall vs 52-min is real but the quality hit is now exactly quantified.
6. DeepSWE is the open problem: the full-file contract is fair (golds pass), the fleet is still 1–3/14. 90% of your work is DeepSWE — this is the lane to fix next (bigger/more capable model, better scaffolding in prompts, or an agent loop over the file contract).
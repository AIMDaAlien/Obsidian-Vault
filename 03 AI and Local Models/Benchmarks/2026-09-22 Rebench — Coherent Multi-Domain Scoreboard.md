---
type: benchmark-run
category: Benchmarks
tags: [benchmark, metalbench, local-ai]
publish: true
created: 2026-09-23
machine: bigrig
title: "2026-09-22 Rebench — Coherent Multi-Domain Scoreboard"
featured: 45
summary: "Re-running six AI setups on the same fair test flipped the old ranking: the supposed quality champion was just slow."
---
# 2026-09-22 Rebench — Coherent Multi-Domain Scoreboard

**Category:** [[Benchmarks]] · **Hub:** [[Model Benchmarks]] · **Method:** [[Benchmark Methodology]] · **Vault:** [[Vault Map]]

Generated 2026-09-22 ~22:45 from ~/bench, uniform 98-task suite (code 46 = 40 + 6 triage-refs, research 26, terminal 11, backend 9, deepswe 6 — every config ran the identical set via `--packs all`), executed verdicts only, no judge, selftest-verified graders.

## Master table (checks / tasks, med decode t/s, med TTFT s, wall min)

| target | checks | pct | full/98 | decode t/s | TTFT s | wall min |
|---|---|---|---|---|---|---|
| qwen-q5-low | 193/213 | 91% | 83/98 | 28.9 | 0.65 | 57 |
| ornith-23g | 190/213 | 89% | 80/98 | 60.8 | 0.23 | 61 |
| qwen-q5-off | 187/213 | 88% | 76/98 | 30.2 | 0.53 | 15 |
| flash-ad384 | 187/213 | 88% | 77/98 | 16.4 | 4.66 | 124 |
| ornith-iq2m | 184/213 | 86% | 77/98 | 97.1 | 0.16 | 58 |
| laguna-q4 | 175/213 | 82% | 67/98 | 36.1 | 0.51 | 32 |

## By domain (checks %, full/n)

| domain | qwen-low | qwen-off | flash | orn-23g | orn-iq2m | laguna |
|---|---|---|---|---|---|---|
| backend 9 | 9 (100) | 9 (100) | 9 (100) | 9 (100) | 7 (78) | 6 (67) |
| code 46 | 46 (100) | 46 (100) | 46 (100) | 46 (100) | 44 (95) | 46 (100) |
| research 26 | 23 (86) | 18 (79) | 21 (82) | 23 (86) | 23 (88) | 15 (68) |
| terminal 11 | 5 (45) | 3 (27) | 1 (9) | 2 (18) | 3 (27) | 0 (0) |
| deepswe 6 | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) |

## What this run established

1. **Scoring order on the SAME suite**: qwen-q5-low > ornith-23g > qwen-q5-off ≈ flash-ad384 > ornith-iq2m > laguna-q4. The old "Qwen=speed, Flash=quality" story does NOT survive a uniform multi-domain suite. On executed multi-domain checks qwen-low (91%) and ornith-23g (89%) lead; flash (88%) ties qwen-off exactly, but at 16.4 t/s versus 30 t/s — it is the SLOWEST config, not the quality king, on this instrument.
2. **Ornith-23G swe40 advantage SURVIVES in shape but narrows**: best dual-GPU config on the suite (89%, only 3 checks behind qwen-low at 2.1x speed), but it does not beat qwen-low outright the way swe40 110/112 suggested. The swe40 "anomaly" is a real strength (incl. top-3 terminal), not an artifact.
3. **Where each fails**: UNIVERSAL deepswe 0/6 (every model emits malformed multi-file diffs — grader proven honest by selftest); universal terminal weakness monsters — flash 1/11 and laguna 0/11 worst (prose without fenced blocks), qwen-low 5/11 best. laguna also fails research 68% and backend 67%.
4. **IQ2_M speed is USABLE**: 4-6x faster than the Q4+ crowd at only −7% checks behind the leader (184 vs 193). NOT a non-starter — it trades ~7 points for ~4-6x decode. Below-Q4 hurts backend (78%) and code (95%) but it holds top-2 research.

## Per-config notes (vault)

- qwen-low: best overall; 100% backend+code; only config >50% terminal; deepswe wall shared.
- qwen-off: −6 checks vs low (the much-rumoured “15-point thinking tax” does not reproduce at this difficulty; off is also ~4x faster in wall time). Not recommended over low, but not the disaster swe40-era numbers implied.
- flash-ad384: ties qwen-off on checks at HALF the speed; best cold TTFT 4.66s is an outlier cost (176B prefill), not a win. Its famous LCB-60 54/60 edge came from hard single-domain coding; here code is tied by all Q4+ configs.
- ornith-23g: best speed/quality balance on the rig (89% at 60.8 t/s); units validated, no-spec.
- ornith-iq2m: usable fast lane (86% at 97 t/s) for throughput-bound work; floor shows only on backend/code t4.
- laguna-q4: now clearly LAST. Its swe40 110/112 was a single-domain artifact; the broader suite exposes 82% and the worst terminal (0/11).

## Suite-level verdict

- The rebench corrects three earlier conclusions: (a) flash is not the quality king on multi-domain executed work — it's mid + slow; (b) the qwen thinking tax is ~6 checks, not 15; (c) laguna's swe40 anomaly is an artifact.
- DeepSwe domain (unified-diff grading) is a universal wall and discriminates nothing — the only pack with zero signal across all six configs; treat per-config deepswe scores as uninformative until the diff prompt/gold is reworked (or treat 0/6 as "all models fail repo-grade patch emissions at this difficulty").
- Terminal is the pack that now separates configs (qwen-low 45% vs laguna 0%); code/backend are saturated (all Q4+ at 100%).
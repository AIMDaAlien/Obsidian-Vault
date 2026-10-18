---
type: index
topic: Qwen3.8 Rig
updated: 2026-10-17
category: Models & Serving
tags: [model, rig, serving, index]
publish: true
created: 2026-09-21
machine: bigrig
title: "Qwen3.8 Rig"
---
# Qwen3.8 Rig
> [!warning] Correction (2026-10-17)
> This page lists port 8080 as the Qwen daily model. Later notes put Flash on :8080 ([[Desktop Session Persistence]]) and Strata on :8083 ([[Strata V100 setup and benchmarks — 2026-10-13]]). Port map verified on this machine 2026-10-17 with `ss -ltnp`: :8081 is the Philosopher harness and :8082 the Philosopher bridge; nothing is listening on :8080 or :8083 (the llama-server, llama-server-flash and unbiasedstrata user units are installed but disabled and inactive).


**Category:** [[Models & Serving]] · **Vault:** [[Vault Map]]

**Hub → [[Model Benchmarks]]** (charts, scoreboard, visualization). Full per-model detail moved to separate notes.

## At a glance

- **Best value / speed king:** [[Qwen-Q5 27B]] at low effort — 48/60 @ 27.7 t/s
- **Best quality:** [[Flash-Next AD384]] medium — 54/60, hard 19/20
- **262K ctx only:** [[Unraid Flash-Next]] — 39/60
- **AMD speed lane:** [[Ornith-1.5 35B]] — swe40 tie, ~4x faster

## Rig facts

- i5-13600K / 62 GB DDR4 · RX 9060 XT 16 GB + RTX 3060 12 GB (AI-only) + UHD 770 (display)
- Daily: `llama-switch mtp` → Qwen-Q5 MTP on 8080 · `deep` = 256K q5_1 KV · `split` = one card per agent lane (superseded, see Correction above)
- Harness: `~/Work/lcb-bench.py` + `~/bench-results/` · suite: [[Bench Suite (~bench)]] · [[Benchmark Methodology]]
- Hardware detail, display limits, GPU speed physics, permanent crash rules → [[Rig Hardware & Display]]

## Model file & serving config

- `~/Models/Swift-Qwen3.8-27B-Q5_K_M.gguf` (20.2 GB) from `ukisai/Swift-Qwen3.8-27B-GGUF`; SHA256 `8803944e…93cc01` matches the repo SHA256SUMS (a second stale `.quants` checksum file exists — ignore it). Q4 not worth it (Q4_K_XL 15.9 t/s vs Q5_K_S 15.5).
- Daily: 128K ctx, `-fa on`, `-ctk/-ctv q8_0`, `-dev Vulkan0,Vulkan1 -sm layer -ts 15,11`, `--spec-type draft-mtp --spec-draft-n-max 2 -ctkd/-ctvd q8_0`, port 8080, systemd user unit `~/.config/systemd/user/llama-server.service` (autostart). Units pin devices with `GGML_VK_VISIBLE_DEVICES` — see [[GPU Crash & Vulkan Device Pinning]]. (superseded, see Correction above)
- MTP numbers: **+98% decode** (14.4 → 27.7–30.2 t/s) but ~2x slower prefill; MTP draft KV defaults to f16 → OOM at 128K, must be `q8_0`. MTP **cannot fit at 256K** → 180K+ is the no-spec q5_1-KV path.
- `--cache-reuse` is **architecturally impossible** on Qwen3.8 (hybrid linear attention can't shift KV — `llama_memory_can_shift()` false). Prefix caching on by default is the biggest UX lever: 30K-session follow-up 70 s cold → 3.9 s.

## Full history

The chronological log (2026-09-14 → 2026-09-21) was split out to keep this note short. See:

- [[Model Benchmarks]] — current scoreboard + charts
- Each model's note (links above) — per-model results and verdicts
- **Archived raw log → [[Model Benchmarks Archive]]** — every historical entry verbatim

## Change log

- **2026-09-21:** split single log into per-model notes + visual hub. Overturned Flash verdict: [[Flash-Next AD384]] medium = 54/60 is the quality ceiling; [[Qwen-Q5 27B]] low-effort = 48/60 is the value king.
## 2026-09-21 19:41 [#metalbench]
**Done:** Same-policy (thinking-controlled) LCB-60 runs across the fleet + new Unraid candidate [[Laguna XS-2.1]] (33B/3B-active MoE Q4_K_M) staged and benched.
**Findings:**
- Uncapped thinking was handicapping the field: Flash-Next IQ3 default 39 -> OFF 47 (+8, hard 4->11); Qwen-Q5 LOW (48) is best, OFF catastrophic (33).
- Laguna thinking-OFF: 46/60 (hard 14/20 = fleet BEST), 34 t/s = ~2.2x Flash on same DDR4 box. Perfect swe40 112/112 @ budget-cap.
- Hard-tier LCB is the real differentiator; swe40 saturates. NOT conclusive yet — Laguna/Flash still need budget-corrected escalation ladder.
**Recommendations:** verdict pending; Unraid still serving Flash-Next; Laguna staged, not default.

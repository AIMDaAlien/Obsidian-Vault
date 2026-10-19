---
type: note
category: Strata
tags: [omarchy, strata, v100]
updated: 2026-10-19
publish: true
created: 2026-10-18
machine: bigrig
title: "Strata V100 tuning — 2026-10-18"
---
# Strata V100 tuning — 2026-10-18

**Interactive dashboard (every number traces to a recorded run):** https://claude.ai/artifact/SVHuTwEfnSbhAVHd55oTzp
Record in the fork: `~/opt/UnbiasedStrata/docs/V100_TUNING.md` (branch `v100-tuning`). Data and charts: `_attachments/strata-v100-tuning-20261018/`.

Goal: the most useful tokens per second and per joule out of one Tesla V100-PCIe-32GB + Ryzen 7950X + 64 GB, on the PC that loses power under sustained load, without changing the model (Qwen3.8-Flash-Next GSQ-RCO IQ3_S, 196,608 context). Every change was paired-measured before adoption, one GPU job at a time under the thermal watchdog.

## Result

![[strata-v100-tuning-20261018/headline.png]]

| | morning (0.1.39, 100 W, chunk 8192) | production now (0.1.43.1 + Volta prompt/decode kernels + async cache, 135 W, CPU capped 4.5 GHz, chunk 32768, vision loaded) |
|---|---:|---:|
| decode, short prompts | 67 tok/s | 90 tok/s |
| decode after an 80K prompt | 61 tok/s | 91 tok/s |
| 80K prefill | 873 tok/s | 1284 tok/s |
| 80K request wall / TTFT | 94.9 s / 91.4 s | 64.7 s / ~60 s |
| short coding request wall (400 tokens, medium reasoning) | 8.25 s | 6.78 s |
| GPU J per generated token | 1.9–2.1 | 2.06 (short) / 36 per token after 80K incl. prefill |
| idle CPU package | 85 W | 59 W |
| CPU Tctl under sustained load | 85 °C (BIOS cap) | 64–66 °C |

No prefill-for-decode trade: both improved, because the power limit and the chunk ceiling are prefill-side levers.

## GPU power limit and clocks

![[strata-v100-tuning-20261018/power-sweep.png]]

Locking the SM clock under a cap never helped; the capper already picks the best clock and a lock only trims transient peaks (~30 W). 125 W is the efficiency point (equal or lower system joules per token than 100 W). 150 W buys 10% more for 5% more energy per token and 200 W+ peaks. The card already draws 150–174 W transients at the 100 W cap; the 2026-10-15 power loss followed a sustained 160–182 W average.

### 125 W soak (passed)

![[strata-v100-tuning-20261018/soak-125w.png]]

Five back-to-back 180K prefills, 15.6 min continuous: mean 123 W, p95 157 W, peak 192 W, GPU ≤ 56 °C, no reset. Adopted as the boot cap (`gpu-nv-power.service` override).

## Engine 0.1.39 → 0.1.43.1

![[strata-v100-tuning-20261018/engine-ab.png]]

Upstream 0.1.43.1 imported (same llama.cpp pin; 0.1.44+ avoided for upstream issue 2936's decode regression). The opt-in Volta decode table (`STRATA_SM70_TABLE=1`, PR 1401's kernels, bitwise-identical output) is the whole gain: +15% decode, −12% GPU J/token. Route tail skip, KV prefetch and the short-prompt CPU share bought nothing; the two that alter answers are off. Production: `local/bin/unbiased-strata-0.1.43.1-sm70`, 12 workers, `STRATA_PREFILL_AUTO_MAX=16384 STRATA_SM70_TABLE=1 STRATA_ROUTE_TAIL_SKIP=0 STRATA_PREFILL_CPU_SHARE=0`. Correctness gate (three planted values in the 80K answer) passed for every candidate.

## Kernel

![[strata-v100-tuning-20261018/kernel-ab.png]]

Changed: `iommu=pt` (all 27 groups identity), NMI watchdog off, governor from a 3.0 GHz performance floor to balance_performance (via `powerprofilesctl set balanced`; power-profiles-daemon overrides a plain unit). Same engine configuration before and after the reboot moved within noise, and the reason is measured: during an 80K prefill the engine spends 74.7 s in user space and 0.1 s in the kernel, system-wide kernel share 1%, interrupts 0%, 94% idle. Nothing kernel-side is on the critical path. The substantiated kernel win is idle: 85 → 59 W, 76 → 63 °C with the model loaded. Mitigations stay on. NVIDIA PAT option is inert on driver 580 (no module parameters exposed).

## What did not move the needle

- Worker count (4/8/12/16): same decode at 97–98% cache hits; only CPU energy moves (4 workers −11% J/token). 12 kept for long contexts (+8% decode after 80K, where the hit rate drops to 87%).
- Draft length 3 or 6, KV window 64K, pool spin 2 ms, sleeping stager, ring size 192/384/512 (the chunk ceiling 16384 is the +5% prefill, not the ring).
- `--vram-reserve-mib 300`: 46 MiB free → OOM on the first prompt. Dead end.

## Vision (added)

The model's own encoder (Q8_0 requantization of the BF16 mmproj, 615 MB, llama.cpp rules) runs on the GPU as upstream's `strata-vision` helper; the C++ front end now takes OpenAI `image_url` parts (data: URLs, local files; JPEG/PNG/GIF/BMP; no network fetch). Eight end-to-end checks pass. Cost with `--vram-reserve-mib 2200`: −3% decode short, −6% after 80K (775 fewer cached experts), prefill unchanged. Real screenshot read-back: title, selected entry and all four file names correct; one of two IP ports missed. 2048 image tokens only matter above ~1024-token images.

## Task-suite wall clock (frozen 24-task DeepSWE2, seed 40, medium reasoning)

| | Oct 13: 0.1.39, 250 W | now: 0.1.43.1 + Volta table, 125 W, vision reserve on |
|---|---:|---:|
| median task wall | 37.2 s | 32.6 s |
| total, 24 tasks | 1017 s | 954 s |
| median TTFT (≈650-token prompts) | 1.5 s | 1.6 s |
| median decode | 77.3 tok/s | 84.5 tok/s |
| passes | 22/24 | 23/24 |

17 of 24 tasks faster, paired geometric-mean wall ratio 0.909; on the 14 tasks whose answers were within 15% of the same length, median wall 37.3 → 32.3 s. The 125 W configuration beats the card's 250 W run from five days ago on wall clock, with one more task passing (e21-index-invalidation). Short-prompt TTFT is unchanged: a 650-token prompt prefills in ~1.5 s either way.

## Round 2 at 125 W (final text config, 12 workers; 2 rounds, 80K + 2 short)

| candidate | decode short | decode after 80K | prefill 80K | GPU J/tok | gate |
| --- | ---: | ---: | ---: | ---: | --- |
| final (reference) | 80.9 | 82.0 | 1185 | 1.96 | 2/2 |
| `--adapt-async 1` | **85.5** | **89.5** | 1184 | **1.84** | 2/2 |
| `STRATA_PREFILL_AUTO_MAX=32768` | 82.5 | 83.6 | **1204** | 1.96 | 2/2 |
| `--adapt-every 2` | 84.8 | 78.1 | 1183 | 1.90 | 2/2 |
| `--adapt-swaps 192` | 81.1 | 77.2 | 1183 | 1.88 | 2/2 |
| `--ple-row-cache 4194304` | 80.6 | 81.3 | 1182 | 1.98 | 2/2 |

The async adaptive tier (opt-in in 0.1.43.1; upstream: answers can differ slightly from the blocking tier) is +6-9%
decode at lower energy; the 32K chunk ceiling +1.6% prefill. Both go to a round-3 acceptance on the production
vision configuration plus the 24-task suite before adoption. Swap/adaptation rates and the n-gram row cache: flat.

## Round 3 acceptance on the production vision configuration, and the switch (2026-10-18 evening)

| | production vision config | + `--adapt-async 1` + chunk ceiling 32768 |
| --- | ---: | ---: |
| decode short / after 80K | 78.5 / 82.7 tok/s | **86.4 / 89.6** tok/s |
| 80K prefill | 1182 tok/s | 1200 tok/s |
| GPU J/token (short) | 1.90 | 1.85 |
| correctness gate | 2/2 | 2/2 |
| 24-task suite: median wall / total / passes | 32.6 s / 954 s / 23 | **29.6 s / 874 s / 23** |

The task suite on the candidate: median task wall 29.6 s (Oct 13 at 250 W: 37.2 s), median decode 92.5 tok/s, 23/24
passes with one task flipping each way (e11 now passes, e13 now fails; both were "varies between repeats" tasks in
the Oct 13 three-seed campaign). Adopted. **Production since 18:3x:** the vision binary, Q8_0 encoder at 2048 image
tokens, `--vram-reserve-mib 2400 --adapt-async 1`, `STRATA_PREFILL_AUTO_MAX=32768`, plus the earlier variables;
backup `config.json.before-vision-async-*`. Live checks: health, eight image tests, variables and flags in the engine
process, 125 W cap.

**Against the morning (100 W, 0.1.39, chunk 8192):** short decode 67 -> 86 tok/s (+29%), decode after 80K 61 -> 90
(+47%), 80K prefill 873 -> 1200 (+37%), 80K request 95 -> 69 s, task-suite median 37.2 s (at 250 W!) -> 29.6 s,
with the vision encoder loaded and lower energy per token.

![[strata-v100-tuning-20261018/tasks-ab.png]]

## Rounds 4–5: Volta prompt kernels, opt-in PRs, Samsung SSD (branch `v100-pr1401`)

Upstream PR 1401's FP16 tensor-core prompt kernels for sm_70 merged against their true base (parity test 0 failures on this card): 80K prefill 1200 → 1212 tok/s (+1.3%, repeats across rounds), 80K wall 69.4 → 68.3 s, decode within noise. Far from the author's +10%: at 125 W the prompt path is power-bound (~960 MHz SM), so faster math buys little. PRs 2357/2358 (sm_70 decode opt-ins) and serving the shards from the Samsung 980 PRO were flat (decode after 80K swings ±4 tok/s between identical runs). **Production now runs the combined `pr-all` binary** (`local/bin/unbiased-strata-0.1.43.1-sm70-pr1401`, since 21:31; health and the eight image tests pass); the opt-ins stay off, the model stays on the ORICO drive with the Samsung copy as fallback. CPU Tctl sat at 85–86 °C in every candidate.

## Round 6: the CPU was boosting for nothing (CPU cap, 135 W probe, resident routing)

![[strata-v100-tuning-20261018/cpu-cap.png]]

| boost cap | decode short / after 80K | 80K prefill | 80K wall | CPU J/token (80K) | Tctl max |
| --- | ---: | ---: | ---: | ---: | ---: |
| uncapped (5883 MHz) | 87.4 / 88.1 | 1202 | 68.9 s | 28.5 | 85.9 °C |
| **4500 MHz** | 87.2 / 88.4 | 1195 | 69.2 s | **19.7** | **64.4 °C** |
| 4000 MHz | 87.1 / 86.2 | 1194 | 69.4 s | 17.6 | 57.6 °C |
| 3500 MHz | 86.8 / 83.3 | 1195 | 69.4 s | 16.4 | 56.8 °C |

The engine never cashes in the boost: at 4.5 GHz every engine number is unchanged while the CPU spends 31% less energy per generated token and stops at 64 °C instead of pinning the 85 °C BIOS limit. Prefill is one user-space core on the host side of the GPU pipeline, and above 4.5 GHz its clock is off the critical path. **Adopted:** `v100-tune maxfreq 4500` is live; boot persistence is the tmpfiles drop-in `~/Work/v100-20261013/adopt/cpu-maxfreq-4500.conf` (`sudo adopt/install-cpu-maxfreq.sh`). Side effect for other work on this PC: single-thread peaks lose up to 20% (5.7 → 4.5 GHz); undo with `v100-tune maxfreq reset`. This closes the cooling item and makes the BIOS boost-override / Curve Optimizer questions low-stakes.

**135 W probe** (one round): prefill 1203 → 1284 tok/s (+6.7%), 80K wall 68.9 → 64.7 s, decode +2%, GPU 120 → 131 W, GPU J/token +2%. Energy-neutral per unit of work. **Soaked and adopted (22:09–22:24):** five 180K prefills back to back, 13.3 min under load, secrets 5/5, no watchdog stop, GPU 59 °C, CPU 66 °C (the 4.5 GHz cap); power mean 133 W, p95 177 W, peak sample 219 W (125 W soak: 123 / 157 / 192). 180K prefill 939 → 1090 tok/s (+15%; longer prompts are more power-bound), 180K request 194 → 168 s. Boot override: `sudo ~/Work/v100-20261013/adopt/install-gpu-135w.sh`. 150 W not tried: the 219 W transients on a PC that has lost power under GPU load are the reason to stop here.

**`STRATA_ROUTE_RESIDENT=0.5`** (two rounds): GPU expert-cache hit rate after 80K 80.5% → 92.3%, decode after 80K 87.9 → **94.4** tok/s (+7%), short +1.4%, GPU J/token −5%, 80K secret gate 2/2. It biases the router toward experts already on the GPU, so it changes which experts answer; the 24-task suite decides: **22/24 passes vs 23/24, median task wall 32.7 s vs 29.6 s** (answers ran longer, median 2886 vs 2570 generated tokens; task-level decode +0.7%). Per-token gain real, per-task result worse. **Rejected.**

Housekeeping lesson: two queued windows deadlocked for two hours because each waited on `pgrep -f` for a label that sat in its own command line. One script per window from now on.

## Still open

- Prefill is the long-prompt bottleneck (180K ≈ 3 min) and is power-bound at 125 W: the Volta prompt kernels gave +1.3%, the chunk ceiling +2%; only watts (135 W: +6.7%) move it further.
- `--adapt-async 1` (opt-in in 0.1.43.1), adaptive-cache tuning for long contexts (hit rate 87% at 80K+), `--spec-min-p`, `--ple-row-cache`, PLE table on the unencrypted Samsung SSD (measure the per-token read share first).
- Hardware: CPU heat resolved by the 4.5 GHz cap (round 6); install the boot drop-in. BIOS: Restore AC Power Loss = Power On is the one setting that matters for a PC that drops power; AI Overclocking off and Curve Optimizer −20 → −10/0 are stability hygiene.

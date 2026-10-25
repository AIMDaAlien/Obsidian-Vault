---
type: model
model: Qwen3.8-Flash-Next-AD-3.84bpw-IQ4_XS
host: MASSIVE-RIG (CUDA build, -ot .ffn_.*_exps.=CPU)
quant: IQ4_XS-M64
updated: 2026-10-17
category: Models & Serving
tags: [model, benchmark, llama.cpp, serving, local-ai]
publish: true
created: 2026-09-21
machine: bigrig
---
	# Flash-Next AD384
> [!warning] Correction (2026-10-17)
> This note's opening and Verdict call AD384 the quality ceiling and quality king of the fleet, based on LCB-60 (54/60). Its own 2026-09-22 Rebench section below shows that verdict does not survive the uniform 98-task suite: 187/213 (88%), tied with qwen-off, at half the speed and about 4x the wall time, the slowest config on the roster. See [[2026-09-22 Rebench — Coherent Multi-Domain Scoreboard]].


**Category:** [[Models & Serving]] · **Vault:** [[Vault Map]]

Attention-distilled Flash-Next, IQ4_XS, running on the rig's 3060 with experts on CPU. **Quality ceiling** of the fleet. See [[Model Benchmarks]]. (superseded, see Correction above)

## LCB-60

| run | easy | med | hard | total | t/s |
|---|---|---|---|---|---|
| **medium-effort** (16K corr) | 20 | 15 | **19** | **54/60** | 16.9 |
| low-effort (8K) | 20 | 14 | 7 | 41/60 | 17.4 |

**Shown for the first time: hard-tier 19/20 — the best local score.** Earlier "Flash loses" verdict was on the much lower IQ3_XXS quant (Unraid). Medium effort + 16K budget lets it actually finish hard problems.

## Caveats

- Slow-ish (16.9 t/s) vs Qwen (27.7) — quality lane, not speed lane.
- Needs the CUDA custom build + expert-CPU override to run on this box.
- Heavy thinking — budget-correct (16K) or it truncates on hards.

## Verdict

**Quality king.** Reach for it when accuracy on hard problems beats latency. On the Pareto frontier opposite Qwen-low. (superseded, see Correction above)

## Serving recipe (never guess 176B flags — crash risk)

Recovered verbatim from the process log:

- Prebuilt CUDA nightly `llama-b11063` at `~/opt/llama-b11063/` (commit `3d82ef62d`) — `docker pull` is impossible here (no root).
- `LD_LIBRARY_PATH` must point at the **cudart dir root**, not `/lib` — the wrong path silently falls back to CPU (5 t/s).
- `-ngl 99 -ot "\.ffn_.*_exps.=CPU" --jinja -fit off -fa on -ctk/v q8_0 -c 32768`, alias `qwen38flash-ad384`, port 8080. `-ngl 99 -fit off` alone tries to put all 44 GB on the 12 GB card.
- 176B = 80 GB / **28 shards**, nested under `~/Models/qwen38flash-atomic/` (a top-level `*.gguf` scan misses it). Only **45.8 GB fast memory** needed because the 102 GB BF16 engram n-gram table is a pure lookup (mmap from SSD kept ON). `AD-4.27bpw-Q4_K_M-M64` = 54.5 GB.
- Launcher unit `llama-server-flash.service` is **disabled at boot** (only `mtp` autostarts; `llama-switch` toggles the rest) and is in the exclusivity/VRAM-drain stop loop.
- 128K is allocatable: proven live at `-c 131072` (`--jinja -fit off -fa on -ctk/v q8_0`, `--chat-template-kwargs '{"reasoning_effort": "low"}'`), RSS 42.6 GB, VRAM 8.2/12 GB. `-c` is **per slot** and the server uses 4 slots with a unified KV pool → for a full 128K per conversation use `-np 1`.
- Template accepts only `xhigh|medium|low` — `minimal` returns HTTP 500.

Run notes: `~/bench-results/lcb60-flashnext-ad384-rig.json` (medium corr), `lcb60-flashnext-ad384-rig-low.json` (low).
## Related

- Siblings: [[Qwen-Q5 27B]] (daily/speed) · [[Unraid Flash-Next]] (same family, IQ3) · [[Ornith-1.5 35B]] · [[Laguna XS-2.1]]
- Hub + rules: [[Model Benchmarks]] · [[Benchmark Methodology]]
- Serving safety: [[GPU Crash & Vulkan Device Pinning]] · [[llama.cpp Upgrade Roadmap]] (rebuild for #28770/#28988)

## 2026-09-22 Rebench (uniform ~/bench suite, 98 tasks)

| config | checks | full/98 | decode t/s | TTFT s (med) | wall min |
|---|---|---|---|---|
| AD384 rig 131K | 187/213 (88%) | 77/98 | 16.4 | 4.66 | 124 |

**The "quality king" verdict does not survive the multi-domain suite.** On executed multi-domain work flash ties qwen-off exactly (187/213) while being HALF the speed and ~4x the wall time (124 min vs 15-61). Its LCB-60 54/60 edge came from hard single-domain coding where it ties all Q4+ configs on this instrument (code 46/46, backend 9/9). Weakest terminal of the Q4+ set (1/11 — emits prose without fenced blocks); deepswe universal wall (0/6). Slowest config on the roster at this difficulty.

## 2026-09-29 08:42 [#metalbench]
**Done:** Retuned the Flash-Next 176B lane for the new 2x RTX 3060 12GB layout (9060 XT removed). Swept ncmoe, ub, threads, ctx, KV quant, ngram, single vs dual card; all configs validated with a real completion and drained between arms.

**Findings:** Single 3060 beats the dual-card layer split everywhere: 269.6 t/s prefill / 19.14 decode vs 246.1 / 13.42 at 131K ctx (+9% prefill, +43% decode). A single 3060 also MATCHES the 9060 XT solo on this model (old audit: 230-315 prefill, 15.5-22.4 decode at 14.7K) because only 4.5GB of the model is GPU-resident. VRAM truth: dense 4.5GB, KV 2.2GB, but COMPUTE BUFFERS 9.3GB dual / 5.0GB single at 131K - the compute buffer, not the weights, caps context on a 12GB card. Best config: single card, ncmoe 48, ub 2048, t16, q8_0 KV, ctx 98304.

**Gotchas:** 114K/ub2048 and 131K/ub2048+q5_1 both load and bench clean, then OOM mid-request at depth - never sign off a context from a short prompt. t32 (SMT) collapses decode to 1.42 t/s. ub 512 costs -52% prefill. ngram-map-k was neutral-to-negative at long ctx here.

**Recommendations:** Ship the 98K single-card config (service updated); free the second 3060 for a second lane. Full write-up: ~/Work/ops/flashnext-2x3060-retune.md

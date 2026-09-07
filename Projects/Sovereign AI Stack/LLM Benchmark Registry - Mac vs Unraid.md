---
tags: [local-ai]
---
# LLM Benchmark Registry — Mac vs Unraid

> Last updated: 2026-09-06
> All scores from deterministic graders only. No LLM judge anywhere.
> Exact-match / substring / ROUGE-L / JSON tool-call parse. Nothing hallucinated.

## Hardware and host separation

| Box | Spec | Role | Runs what |
|---|---|---|---|
| **Mac M5 Pro (this)** | 48 GB unified memory, ~400+ GB/s bandwidth | **Interactive daily driver** — everything you touch directly: chat, coding agents, vision/OCR, companion | Models that fit fully in unified memory; bandwidth makes it 2-3× faster per watt than the Unraid box |
| **Unraid** (192.168.0.120) | 128 GB DDR4, i5-12600KF 16T, RTX 3060 12 GB | **Always-on headless server** — serves APIs (OpenCode, gateways) whether the Mac is awake or not | Large MoE models with experts in system RAM, attention on GPU; capacity play, not speed play |

Rule of thumb: **a model you interact with lives on the Mac; a model that must be always reachable for tools/agents lives on Unraid — and if it exists on both, the Mac version is the interactive one.**

## Test batteries

- **Full (76 items)**: vision 10, OCR 8, summary 4, knowledge 40, research 6, planning 8
- **Text (58 items)**: knowledge 40, research 6, planning 8, summary 4
- **Throughput sweep v1** (added 2026-09-06): 3 prompt classes × 3 runs, 512-tok output; mean decode t/s
- Grading: normalized exact-substring (number words → digits), multi-token hits for vision, ROUGE-L F1 ≥ 0.30 for summaries, JSON tool-call parse for research

## Scores — Mac M5 Pro (48 GB unified) — interactive hosts

| Model | Quant | Size | RAM RSS | tps | Full 76 | Text 58 | Knowledge | Research | Planning | Summary |
|---|---|---|---|---|---|---|---|---|---|---|
| [[Qwen3.8-27B]] | MLX 4-bit | 16.1 GB | ~2 GB idle | 14-15 | — | — | — | — | — | — |
| [[Gemma 4 12B QAT Q8]] | 8-bit | 11.9 GB | 4.7–13 GB | ~7 | 68/76 (89.5%) | 55/58 (94.8%) | 40/40 | 6/6 | 8/8 | 1/4 |
| [[Gemma 4 12B QAT Q4]] | 4-bit | 10.3 GB | 9.7 GB | ~7.4 | 66/76 (86.8%) | 55/58 (94.8%) | 40/40 | 6/6 | 8/8 | 1–2/4 |
| [[LFM2.5-8B-A1B]] | MLX 8-bit | 8.4 GB | 9.1 GB | 107 | — | 53/58 (91.4%) | 39/40 | 6/6 | 8/8 | 1–2/4 |
| [[LFM2.5-2.6B]] | MLX 8-bit | 2.9 GB | 3.4 GB | 76.8 | — | 53/58 (91.4%) | 38/40 | 6/6 | 8/8 | 0/4 |
| [[Ternary Bonsai 27B]] | MLX 2-bit | 7.9 GB | 7.1 GB | 6.4 | — | 53/58 (91.4%) | 38/40 | 6/6 | 8/8 | 1/4 |
| [[Maple-Preview 20B]] | 2-bit ternary | 5.3 GB | 2.2 GB | 172.5 | — | 46/58 (79.3%) | 38/40 | 0/6* | 7/8 | 1/4 |
| **K2-Horizon MoVA 36B-A4B** | IQ4_XS (llama.cpp Metal fork) | 20.1 GB | ~22 GB | **~54** (32K and 128K ctx) | — | — | — | — | — | — |

\* Maple research 0/6 = runtime limitation (mlx-lm server has no native tools). It refused to fabricate the FIFA answer — honest non-fabrication, counted as miss by the harness.

Note: Qwen3.8 scored 308/317 on the 317-question fingerprint battery + 17/17 hard-agentic — see [[Qwen3.8-27B]] for the full suite. It sits outside the 76/58 legacy batteries (superseded by the 317-question bank).

### K2-Horizon MoVA on the Mac (added 2026-09-06)

- IQ4_XS via MBZUAI-IFM llama.cpp fork (`model/K2Horizon`), fully unified-memory resident.
- Throughput sweep: **54.7 / 54.4 / 53.2 t/s at 32K**; 54.5 / 54.1 / 51.1 at 128K — decode flat across context, prefill is the only long-context cost (23K-token prompt ≈ 2 min).
- **This is the interactive K2 home.** At ~54 t/s and a higher quant, the Mac is 2.5× faster than the Unraid K2 build was. See [[K2-Horizon MoVA Serving and Benchmarks]].

## Scores — Unraid (128 GB + RTX 3060) — always-on servers

| Model | Quant | Size | RAM | tps | Status |
|---|---|---|---|---|---|
| [[Qwen3.6 35B A3B Abliterated]] | Q6_K + MTP | 27.2 GB | ~27 GB | ~13 | superseded, files kept |
| **[[Qwen3.8-Flash-Next]]** | UD-IQ3_XXS | 76.3 GB | ~100 GB | **14.7 @ 262K ctx** | **current resident** |
| ~~K2-Horizon MoVA 36B~~ | IQ3_XXS | 14.6 GB | ~26 GB | 22.1 (tuned) | **removed 2026-09-06** (container, image, GGUF deleted; Mac takes the interactive role) |

### [[Qwen3.8-Flash-Next]] (176B MoE, qwen4_exp arch — the current Unraid resident)

- 9-task deterministic agentic: **9/9** vs Qwen3.6 NVFP4 7/9.
- **Full native 262,144-token context since 2026-09-06** — the GDN+QSA hybrid makes it nearly free: only 12 of 48 layers carry KV (2 KV heads × 256), so 262K KV at q8_0 is ~3.4 GB. A Qwen3.5-class dense 125B would need tens of GB.
- ~14.7 t/s decode at 262K on llama.cpp master 2026-09-06 (7 qwen4exp fixes incl. GDN normalization correction) — *faster* than the 13.3 the older build did at 128K.
- ncmoe frontier: 18.9 t/s possible with 42 expert layers on CPU, but those configs OOM at 262K. Full context and peak speed are mutually exclusive on 12 GB; serving config = ncmoe 48.
- Wired into OpenCode as `qwen38-unraid/qwen38-flash` (262144 ctx limit). See [[Qwen3.8-Flash-Next 262K Context on Unraid]].

### K2-Horizon MoVA on Unraid (retired)

- IQ3_XXS, 22.1 t/s after the governor/q8_0/mlock tuning (was 9.5). Full story in [[K2-Horizon MoVA Serving and Benchmarks]] and the metalbench finding *Governor and KV tuning more than doubled MoE decode*.
- Removed because the Mac wins the interactive role (54 vs 22 t/s, better quant) and Flash-Next holds the always-on role. The tuning lessons (governor catch, q8_0 KV, mlock) carry over to every model on this box.

## Throughput sweep v1 results (2026-09-06, artifact-backed in metalbench)

| Model | Host | Context | Decode t/s |
|---|---|---|---|
| K2-Horizon IQ4_XS | Mac | 32K | 54.1 |
| K2-Horizon IQ4_XS | Mac | 128K | 53.2 |
| K2-Horizon IQ3_XXS | Unraid | 32K | 22.1 (removed) |
| Flash-Next IQ3_XXS | Unraid | 262K | 14.7 |

## Cluster outlook (gaming rig, hypothetical)

Rig: MSI Z690 Pro WiFi DDR4, i5-13600K, RX 9060 XT 16 GB, +32 GB DDR4-3600 (mixed brands → run 3200-3400 loose). Clustered with Unraid via llama.cpp `--rpc` = ~28 GB VRAM + 192 GB pooled RAM.

- **Feasible payoff:** Qwen3.7-235B-class MoEs (~100-130 GB at Q3/Q4) or GLM-5.3-Flash at IQ3_XXS (120 GB) — intelligence tiers neither machine can hold alone.
- **GLM-5.3-Flash specifics:** 320B/18B active, MIT, GGUFs exist (93-200 GB). Fits at IQ3_XXS/Q3_K_XL; fork-only runtime (`glm5_next`, Unsloth branch, not mainline); expect 5-9 t/s over RPC; both machines loaded → ~500-600 W. Demand-start (wake-on-LAN) only.
- **Recommended first big-model target: Qwen3.7-235B** over GLM-5.3-Flash — similar fit, likely better agentic scores, and mainline llama.cpp support (no fork).
- 2.5 GbE NICs on both ends (~$40) practically required; 1 GbE throttles RPC.
- Not worth it for Flash-Next IQ3_XXS — already optimal single-node and clustering would slow it.

## Key takeaways

- **Host separation is deliberate:** Mac = interactive quality/speed (K2 IQ4_XS, Qwen3.8-27B, Gemma, LFM); Unraid = always-on capacity (Flash-Next 262K) for tools that need a server that never sleeps.
- **Speed vs competence tradeoff is stark.** Maple 172 tps / 2.2 GB vs Gemma Q4 7.4 tps / 9.7 GB — 23× faster at ¼ the RAM, but 79% vs 96% text score.
- **Knowledge + research + planning are saturated.** Differentiation lives in summary, OCR, speed, and now long context.
- **Gemma 4 Q4 = best all-rounder** for careful answers; Q8 only wins glyph-level OCR.
- **LFM2.5 8B = the interactive companion winner.**
- **The governor lesson generalizes:** check `scaling_governor` before blaming hardware. It doubled K2 decode and was inherited by Flash-Next.

## Related

- [[Qwen3.8-27B]]
- [[Qwen3.8-Flash-Next]]
- [[Qwen3.8-Flash-Next 262K Context on Unraid]]
- [[K2-Horizon MoVA Serving and Benchmarks]]
- [[Gemma 4 12B QAT Q8]]
- [[Gemma 4 12B QAT Q4]]
- [[LFM2.5-8B-A1B]]
- [[LFM2.5-2.6B]]
- [[Ternary Bonsai 27B]]
- [[Maple-Preview 20B]]
- [[Deepwen-3.6]]
- [[Unraid Qwen3.6 Terminal Agent - July 2026]]

---
tags: [local-ai, cost]
---
# Deepwen-3.6

> Status: deployed on Unraid, benchmark pending. quimmedes/Deepwen-3.6.

## Model
- Qwen3.6-35B-A3B fine-tune + DeepSeek-V4-Flash-0731 reasoning DNA (effort levels: low/xhigh/max, "verify before you answer")
- Specialized: AAA GameDev 2D/3D, procedural geometry, Blender pipelines, WebGPU/Three.js, UI/design
- Apache-2.0. MoQ quants (mixture of quantizations, per-tensor type selection)

## Quants
| File | Size |
|---|---|
| Q2.5-IQ2XXS | 10.1 GB |
| Q2.5-MoQ / Q3-MoQ | 13.4 GB |
| Q4.5-MoQ (deployed) | 19.7 GB |
| Q5-MoQ | 24.7 GB |
| Q6-MoQ | 28.8 GB |
| Q8-MoQ | 36.9 GB |

## Deployment (Unraid)
- Hardware: 128 GB RAM, RTX 3060 12 GB
- Runtime: laguna llama.cpp image (same arch as Qwen3.6 35B)
- Port 18007, CTX 131072, GPU layers 10
- Container: llm-deepwen-3.6

## Quant compatibility warning (RESOLVED — it was reasoning mode, not quants)
- All three MoQ quants (Q4.5, Q3, Q2.5) initially produced endless "/" spam +
  empty content. Root cause: `--reasoning off` in the entrypoint. Deepwen is a
  heavy reasoning model (DeepSeek-style CoT) — with reasoning disabled it emits
  its thinking delimiter token ("/") as raw content and never produces the real
  answer.
- FIX: `--reasoning auto --reasoning-budget 2048 --reasoning-preserve`. With
  reasoning parsing ON, thinking lands in `reasoning_content` and the real
  answer in `content`.
- Deployed quant: Q2.5-IQ2XXS (10.1 GB, IQ2_XXS — the only type the laguna
  build fully decodes). Q4.5-MoQ/Q3-MoQ use unsupported types (Q4_5_K/Q3_K)
  and are genuinely broken on this runtime.
- The abliterated Qwen3.6 Q6_K works fine on the same runtime (same qwen35moe
  arch — the arch is NOT the problem).

## Benchmark (text 58 items) — DONE 2026-08-10
- Deepwen 38/58 (65.5%) on Q2.5-IQ2XXS, Unraid laguna runtime
- knowledge 34/40 — several empties where the 1200-token budget was eaten by
  reasoning (heavy CoT); occasional `` artifacts leak into content
- research 0/6 — CRITICAL LIMITATION: verbalizes "I will use search_web" but
  emits NO structured tool call. The laguna build doesn't render this
  template's tool-call tokens, so real tool use is impossible on this stack.
- planning 7/8 (strong), summary 1/4 (ROUGE 0.0-0.28, same weak spot as others)
- ~23 t/s decode, 4.3 GB GPU. Reasoning budget 2048 with preserve.
- Honest assessment: the Q2.5 quant + tool-call gap makes Deepwen the weakest
  of the tested models for the user's domains (research is mandatory and it
  can't do it). The base Qwen3.6 abliterated Q6_K remains the Unraid pick.

## Notes
- Same architecture as the abliterated Qwen3.6 already on Unraid → drop-in swap, spec-decode drafts should transfer
- Reasoning template from DeepSeek V4 Flash — three effort levels

## Verdict
pending. Related: [[Qwen3.6 35B A3B Abliterated]] [[LLM Benchmark Registry - Mac vs Unraid]]

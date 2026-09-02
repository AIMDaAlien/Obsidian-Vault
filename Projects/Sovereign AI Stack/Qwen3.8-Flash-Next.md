---
tags: [local-ai, hardware-constraints, unraid]
---
# Qwen3.8-Flash-Next (176B MoE)

> 2026-08-29. Canonical note. Unraid-hosted (RTX 3060 12 GB + 128 GB DDR4).
> Not to be confused with [[Qwen3.8-27B]] (dense, Mac-local). This is the big MoE.

## What it is

- **176B MoE** = ~125B main + **51.2B PLE n-gram table**, **6B active/token**.
- 48 text layers (36 Gated DeltaNet + 12 Qwen Sparse Attention), 512 routed experts
  top-10+1, shared experts, four gated-residual branches, 1-layer MTP head,
  27-layer vision tower, 262K ctx, multimodal (text + image).
- Agentic gap vs 27B dense is huge: DeepSWE 58.7 vs 42.2, NL2Repo 48.1 vs 42.3.
- The PLE n-gram table (~51B) dominates residency. It is not in the 6B active path.

## Deployment (the RAM-fit rule — confirmed)

| Checkpoint | Size | Fits ~101 GB avail RAM? |
|---|---|---|
| NVFP4 | 127 GB | ❌ no — streams SSD, reject |
| Q3_K_XL GGUF | 84 GB | ✅ yes — the pick |
| Q3.6 NVFP4 (baseline) | 22 GB | ✅ yes |

- Serve: `llama-server -m qfn-q3kxl/... --cpu-moe -ngl 99 -ot ple_ngram_embd=CPU`
- Decode ~14.5 tok/s, prefill 89-115 tok/s, 6.3 GiB VRAM. **Memory-bandwidth bound**
  (DDR4 ~45 GB/s streaming experts), not compute bound.

## Benchmark (9-task agentic, deterministic grading)

Flash-Next Q3_K_XL **9/9** vs Qwen3.6 NVFP4 **7/9**. The gap is strict
instruction/format adherence only — Qwen3.6 returns filename arrays + markdown
fences instead of `{files: int}` and echoes a banned word ("deprecated").
Both pass every terminal trap. `reasoning_effort=low` = same 9/9, ~43% faster.

## Speculative decoding — all four investigated, NONE help (2026-08-29)

| Method | What | Status on this box |
|---|---|---|
| MTP | built-in multi-token head (autoregressive drafter) | tested — acceptance 0.8, **no wall-clock gain** (13.6-14 vs 14.67 t/s) |
| DFlash | trained block-diffusion draft (z-lab, ICML'26) | needs trained draft (none exists) + SGLang/vLLM (full VRAM) — dead on 12 GB |
| DSpark | DeepSeek confidence-scheduled semi-AR (arXiv 2607.05147) | merged llama.cpp Jul 28; needs trained drafter GGUF + GPU-dense target |
| MTPLX | packaged Qwen+MTP head, MLX/Apple-only | same MTP mechanism; no decode gain (benchmarked on M5 Pro) |

**Why:** decode is memory-bandwidth bound. Spec decode trades idle compute for
memory traffic; here compute is the free resource and bandwidth is scarce, so
every drafter adds traffic it can't hide. MoE doubles the problem — block-parallel
drafting can't amortize weight reads because k parallel tokens route to ~k
different active experts. llama.cpp `--spec-type` has all of them
(`draft-mtp/dflash/dspark/eagle3/simple` + ngram-*), but every `draft-*` needs a
separate `--model-draft` GGUF, and none exists for this arch.

## Compression options (2026-08-29)

Unsloth UD ladder below Q3_K_XL (all llama.cpp-ready):

| Quant | Size | ~Decode | Quality |
|---|---|---|---|
| Q3_K_XL (current) | 83.8 GiB | 14.5 t/s | baseline |
| **IQ3_XXS** | ~76 GiB | ~15.5 t/s | **≈ Q3_K_XL — VERIFIED 41/42 (identical)** |
| Q2_K_XL | ~73 GiB | ~16.5 t/s | minor loss |
| IQ1_M/S | 67-69 GiB | ~17 t/s | real loss — avoid for agentic |

- **Mixed-quant / expert-tiered** (Baekpica `MQ-*`): the right technique
  (crush cold experts to Q2, keep hot/always-active/MTP at Q8, PLE at Q5) but
  published artifacts are a custom `qwen4exp` schema for the **ds4** engine
  (DGX Spark / Blackwell sm_120+), NOT llama.cpp, and are *larger* than Q3_K_XL.
  No llama.cpp-compatible smaller mixed-quant exists yet.
- Each quant step is a linear ~10-15% speedup (bandwidth-bound) at proportional
  quality risk. The big levers stay: concurrency/batching (amortize expert reads
  across requests), GPU-resident hot experts (FreeToken LRU — blocked: NVFP4
  127 GB > 101 GB RAM), or faster RAM / bigger GPU.

## Optimization pass (2026-08-29) — measured

- **`-t 16` beats `-t 6` by ~+17%** (14.5 → 16.92 t/s). Default 6 threads
  (P-cores) under-saturates DDR4 bandwidth; 16 threads (P+E) issue more concurrent
  memory requests for the CPU-offloaded experts. Biggest single free win.
- **IQ3_XXS = Q3_K_XL quality** (both 41/42 on the quant-sensitivity battery,
  identical single miss) + ~9% decode + 8 GiB RAM. Safe swap.
- **n-gram spec decode HURTS (-50%):** acceptance 0.097, 16.92 → 8.20 t/s. With
  MTP already measured as no-gain, spec decode is confirmed dead for this MoE.
- RAM already 3200 MT/s (XMP on), build already AVX2 (-march=native). No further
  free wins there.

Optimal serve: `llama-server -m .../UD-IQ3_XXS-...gguf --cpu-moe -ngl 99
-ot ple_ngram_embd=CPU -t 16 -c 16384 [-np 4 for concurrency]`.

## Files

- `~/.hermes/skills/devops/local-llm-serving/references/freetoken-qwen38-flash.md`
- Harness: `/workspace/unraid_agent_bench.py` (9-task agentic, deterministic)
- Quant-sensitivity battery: TBD (this session)

## Related

- [[LLM Benchmark Registry - Mac vs Unraid]]
- [[Qwen3.8-27B]]
- [[Unraid Qwen3.6 Terminal Agent - July 2026]]

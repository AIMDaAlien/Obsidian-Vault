# Qwen3.8-27B — Engine & Quant Benchmark (M5 Pro)

> 2026-08-15. Dense 27B, 48GB Mac. Goal: long-context + full-potential MLX.

## Verdict (short)

- **Decode speed is bandwidth-capped ~13-15 t/s** on this Mac. MTP/spec-decode
  gives ZERO wall-clock gain even when fully working.
- **Prefill is where engines differ**: LM Studio NAX 254 t/s vs rapid-mlx 97-114
  t/s. Long context = prefill-dominated, so this matters more than decode.
- **4-bit stays the best all-rounder** (fast decode, good prefill, fits 256K).
- AXQ-6bit = higher-quality quant (6/8-bit overrides on critical tensors) at
  same decode speed, but worse prefill (68 t/s).

## Measured results

| Config | Decode | Prefill 32K | Quality (27q) | Notes |
|---|---|---|---|---|
| 4-bit (rapid-mlx :8110) | 14-15 t/s | 97-114 t/s | 27/27 | current default |
| AXQ-6bit-MTP (rapid-mlx) | 13.3 t/s | 68 t/s | ✓ tricky pass | higher quant + MTP |
| MTPLX-Speed (LM Studio NAX) | 12.4 t/s | **254 t/s** | 27/27 | best prefill by far |

Context (32K+): 4-bit ✓ all sizes. MTPLX ✓ when given token headroom (it
THINKS first — burns ~50 tokens on reasoning, needs max_tokens ≥200).

## Key findings

1. **MTP works but doesn't help.** Got it fully engaged on rapid-mlx:
   `--speculative-config '{"method":"mtp","model":"<path>/mtp.safetensors","num_speculative_tokens":3}'`
   — sidecar must be an explicit file path or standard-named
   `model-mtp.safetensors`; the MTPLX/AXQ custom `mtp.safetensors` name alone
   isn't auto-discovered. Even drafting, decode stays ~13 t/s: the dense 27B is
   memory-bandwidth-bound (~14 GB weights read per token), not step-bound.
2. **NPU/ANE: not reachable.** MLX runs on GPU (Metal). The NPU path is Apple's
   Foundation Models framework — not available for Qwen3.8. LM Studio's "NAX"
   engine is Metal-optimized MLX, not NPU.
3. **LM Studio's prefill advantage (254 vs ~100 t/s) is an engine win.**
   rapid-mlx tops out ~114 t/s with `--prefill-step-size 32768` +
   `--hybrid-cache-entries 4096`. Still 2.2x slower than NAX.
4. **MTPLX model THINKS by default** — short-budget requests return empty
   content (all tokens eaten by reasoning). Harness must use max_tokens ≥200
   or disable thinking.
5. **Rapid-mlx auto-disables spec-decode on hybrid models** (Qwen3.8 has
   GatedDeltaNet 3-of-4 layers) unless force-overridden.

## Engine flags that matter

- 4-bit launcher (current): `--prefill-step-size 16384 --kv-cache-dtype int4
  --kv-cache-turboquant v4 --no-thinking --reasoning-parser qwen3`
- Prefill-tuned: `--prefill-step-size 32768 --hybrid-cache-entries 4096`
  (+17% prefill, tested)
- MTP: `--speculative-config '{"method":"mtp","model":"./mtp.safetensors",
  "num_speculative_tokens":3}'` (no speedup, keep for reference)
- LM Studio: `lms load "qwen3.8-27b-mtplx-optimized-speed" --context-length
  131072 --speculative-draft-mtp`

## Recommendation

- Agentic/tool work: 4-bit on rapid-mlx (fast decode, clean tool calls).
- Long-context ingestion: MTPLX via LM Studio (2.5x prefill — the real win).
- Quality-sensitive short work: AXQ-6bit (higher precision, same speed).
- Don't chase MTP/spec-decode on this hardware — measured dead end.

## Files

- `results/mtplx-q4.json`, `results/mtplx-mtplx.json` (full benchmark data)
- Models: `mlx-community/Qwen3.8-27B-4bit` (16GB),
  `Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed` (20GB),
  `AutomatosX/AX-Qwen3.8-27B-MLX-AXQ-6bit-MTP` (20.9GB)

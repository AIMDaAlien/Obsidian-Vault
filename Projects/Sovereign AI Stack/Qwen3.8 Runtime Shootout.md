# Qwen3.8-27B — Runtime & Quant Shootout (M5 Pro)

> 2026-08-18. Tested engines: rapid-mlx 0.12.12, LM Studio NAX (mlx-llm 1.11.0),
> plus the AXQ-6bit-MTP and MTPLX variants. Goal: long-context usage.

## Headline

- **MTP / speculative decoding: dead end on this Mac.** Got it FULLY working
  (sidecar loaded, drafting active, 13.3 t/s) — no wall-clock gain. The M5 Pro's
  memory bandwidth is the ceiling for a dense 27B, not serial decode steps.
- **NPU/ANE: not reachable from MLX.** MLX runs on GPU (Metal). The NPU path
  needs Apple's Foundation Models framework, which doesn't exist for Qwen3.8.
- **Long context = prefill-bound, and LM Studio's engine is 2.5x faster at it.**

## Measured results

| Config | Decode | Prefill 32K | Quality (27q) | Notes |
|---|---|---|---|---|
| 4-bit (rapid-mlx) | 14-15 t/s | 97-114 t/s | 27/27 | tool-calling via hermes parser |
| AXQ-6bit + MTP (rapid-mlx) | 13.3 t/s | 68 t/s | ✓ | 6/8-bit overrides, MTP sidecar works but no gain |
| MTPLX-Speed (LM Studio NAX) | 12.4-12.8 t/s | **254 t/s** | 27/27 | prefill king; MTP flag accepted but idle |
| MTPLX (LM Studio) e2e 20K+gen | 5.25 t/s incl | — | 27/27 | 2.3x faster end-to-end than rapid-mlx at 32K |

## Findings

- Qwen3.8 KV cache is tiny (64 layers, 4 KV heads, 3-of-4 layers recurrent
  DeltaNet = no KV growth). 256K ctx ≈ 2-3GB at int4. Weights+KV fits 48GB.
- 4-bit stays the long-context pick: 16GB + ~3GB KV = 19GB, huge headroom.
- AXQ-6bit (AutomatosX, 20.9GB) = 4-bit base + 6/8-bit on critical tensors:
  higher effective quality at same decode speed, but worse prefill (68 t/s).
- MTPLX-Quality (30.4GB) doesn't fit 256K comfortably. Skip.
- GGUF/Q6_K path dropped: llama.cpp is slower on Metal than MLX; user correctly
  steered to MLX as the native Apple Silicon option.

## How to use

- **Agentic/tool-calling:** rapid-mlx 4-bit (8110, qwen38 launcher) — fastest decode.
- **Long-context ingestion:** MTPLX via LM Studio — 2.5x prefill.
  `lms load qwen3.8-27b-mtplx-optimized-speed --context-length 131072`
- **MTP sidecar trick (for reference):** rapid-mlx needs the sidecar path in
  `--speculative-config '{"method":"mtp","model":"/path/mtp.safetensors",...}'`.
  The MTPLX/AXQ mtp.safetensors works — it just doesn't speed anything up here.

## Gotchas

- LM Studio MTPLX THINKS by default: burns ~50 tokens on reasoning before content.
  Give max_tokens headroom or you get empty content at short budgets.
- LM Studio defaults to 8192 ctx on load; pass --context-length explicitly.
- rapid-mlx auto-disables spec decode on hybrid (DeltaNet) models unless forced;
  the MTPLX custom head is rejected, the standard-path sidecar is accepted.
- 8114/8115 test servers killed; 4-bit restored on 8110. AXQ model kept on disk
  (20.9GB) for quality-sensitive work.

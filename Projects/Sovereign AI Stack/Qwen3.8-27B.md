# Qwen3.8-27B — Deployment & Benchmark vs Qwen3.6

> 2026-08-14. Qwen3.8-27B dropped (Aug 11). Tested Mac-local (M5 Pro 48GB).

## Verdict: 3.8 beats 3.6. REPLACE.

## Results (317-question fingerprint + agentic suites)

| Suite | Qwen3.6 | Qwen3.8-27B |
|---|---|---|
| fingerprint (317q, 28 domains) | 305/317 (96.2%) | 308/317 (97.2%) |
| hard-agentic (17q) | 16/17 (94.1%)* | 17/17 (100%) |
| agentic (16q) | 16/16 | 16/16 (100%) |

*3.6's hard-agentic was inflated by benchmark bugs (wrong chmod key + meta-phrased
tool prompts) — fixed and re-ran only 3.8, which got 17/17 with real tool calls.

## Quality differentiators (3.8 > 3.6)

- Tool calling: 3.8 emits clean structured tool_calls (13 iterations on search).
- Nile source: 3.8 said "Kagera River" (true headwater) vs "White Nile" — more precise.
- Halal: 3.8 answered "Interest (Riba)" (also haram) — deeper domain knowledge.
- Recent knowledge: 3.8 knows Python 3.14 + Unraid 7 (both fresh); 3.6 stale on both.

## Deployment facts

- Model: mlx-community/Qwen3.8-27B-4bit (16.1GB), qwen3_5 arch (Gated DeltaNet hybrid).
- 8-bit (29.5GB) CRASHED the Mac — dense 27B KV cache at 256K blew 48GB. 4-bit is correct.
- Launcher: ~/.hermes/scripts/qwen38, port 8111.
- CRITICAL flags: --prefill-step-size 16384 (NOT 262144 — a 40k-token prefill tried to
  allocate 76GB and hit Metal's 30GB buffer cap). --kv-cache-dtype int4 --kv-cache-turboquant v4.
- MUST run with `env -i` (unset Hermes PYTHONPATH) — Hermes venv has broken numpy/pydantic.
- 256K context VERIFIED: 40,032-token prompt answered correctly (389s prefill).
- Throughput: ~2-7 tok/s (dense 27B, slow vs Gemma MoE ~60 tps). This is the real cost.

## To replace 3.6 (do these)

1. Unraid: swap qwen36-terminal GGUF (Huihui Q6_K) for Qwen3.8 GGUF — bartowski has Q6_K.
2. Mac: AEON Qwen3.6 27B MLX → delete, Qwen3.8-4bit is the replacement.
3. Update aliases/roster/OpenCode provider to point at qwen3.8.
4. Delete stale: Qwen UD-Q6_K 29GB + DFlash 421MB on Unraid (already flagged).

## Caveat

4-bit is the ONLY viable quant on this Mac (8-bit OOMs). Throughput ~2-7 tok/s means
3.8 is for correctness-heavy agentic work, not interactive loops — Gemma 4 26B MoE
stays the fast all-rounder. 3.8's speed is its only weakness vs 3.6 (similar).

# Qwen3.8-27B — Deploy, Benchmarks, Verdict

> 2026-08-18. Canonical note. Mac-local (M5 Pro 48GB), qwen3_5 arch
> (Gated DeltaNet hybrid, 3-of-4 layers recurrent = tiny KV cache).

## Bottom line

- **3.8 beats 3.6.** Replaced everywhere on Mac. Better knowledge, cleaner tool calls, fresher data.
- **4-bit is the only quant worth running.** 8-bit costs 40% decode speed + 13GB RAM, gets ZERO quality gain. Higher quant does NOT fix the model's weak spots (multi-step arithmetic).
- **MTP/spec-decode = measured dead end** on this Mac. Memory-bandwidth bound, not step bound.
- **Long context = prefill-bound.** LM Studio's NAX engine is 2.5x faster at prefill than rapid-mlx. Use it for big-context ingestion.

## vs Qwen3.6 (317-question fingerprint + agentic)

| Suite | Qwen3.6 | Qwen3.8-27B |
|---|---|---|
| fingerprint (317q, 28 domains) | 305/317 (96.2%) | 308/317 (97.2%) |
| hard-agentic (17q) | 16/17* | 17/17 (100%) |
| agentic (16q) | 16/16 | 16/16 (100%) |

*3.6's hard-agentic inflated by benchmark bugs (wrong chmod key + meta-phrased tool prompts) — fixed, only 3.8 re-ran, got 17/17 with real tool calls.

Quality differentiators: clean structured tool calls (13 iterations on search), "Kagera River" for Nile source (true headwater), "Interest (Riba)" for halal question (also haram, deeper domain grasp), knows Python 3.14 + Unraid 7 (both fresh; 3.6 stale).

## Quant shootout — the key finding (2026-08-18)

33 precision tasks (exact arithmetic, format-exact output, multi-condition logic). Terse-prompt harness, temperature 0, deterministic grading.

| Quant | Score | Decode | Notes |
|---|---|---|---|
| **4-bit (baseline)** | **31/33** | 14-15 t/s | current default |
| AXQ-6bit (6/8-bit overrides) | 30/33 | 13.3 t/s | prefill worse (68 t/s) |
| 8-bit | 30/33 | 9.05 t/s | 29.5GB, tight on RAM |

**All three quants fail the SAME questions with nearly the SAME wrong answers** — sum of first 50 primes, 2^10+2^11+2^12, the a_12 sequence. Those failures are the model's own multi-step arithmetic limit, not quantization error. Higher quant buys nothing.

Easy bank (20 riddle/trap questions): all quants 18/20, misses were grader artifacts (rooster, months).

## Engine shootout (2026-08-15/18)

| Engine | Decode | Prefill 32K | Notes |
|---|---|---|---|
| rapid-mlx 0.12.12 (4-bit) | 14-15 t/s | 97-114 t/s | agentic workhorse |
| rapid-mlx + MTP sidecar | 13.3 t/s | 68 t/s | MTP fully working, no gain |
| LM Studio NAX (MTPLX-Speed) | 12.4-12.8 t/s | **254 t/s** | prefill king |
| LM Studio e2e at 32K | 5.25 t/s incl | — | 2.3x faster than rapid-mlx end-to-end |

Findings:
- **MTP works but doesn't help.** Sidecar loaded + drafting, still 13.3 t/s. Dense 27B reads ~14GB weights/token — bandwidth is the wall, not serial steps. Rapid-mlx auto-disables spec decode on hybrid models unless forced; MTPLX custom head rejected, standard-path sidecar accepted.
- **NPU/ANE not reachable.** MLX runs on GPU (Metal). NPU path = Apple's Foundation Models framework, doesn't exist for Qwen3.8. LM Studio "NAX" = Metal-optimized MLX, not NPU.
- **GGUF/llama.cpp dropped.** Slower on Metal than MLX; MLX is the native Apple Silicon option.
- **KV cache is tiny** (64 layers, 4 KV heads, 3-of-4 layers DeltaNet = no KV growth). 256K ctx ≈ 2-3GB at int4. 4-bit (16GB) + KV = ~19GB, fits 48GB with headroom.
- 8-bit (29.5GB) at 256K CRASHED the Mac earlier. Keep it at 128K max if ever used.

## How to use

- **Agentic/tool work:** 4-bit on rapid-mlx (8110, `~/.hermes/scripts/qwen38`).
- **Long-context ingestion:** MTPLX via LM Studio — 2.5x prefill. `lms load qwen3.8-27b-mtplx-optimized-speed --context-length 131072`
- **Wired into:** hrapid profile `qwen38` (+ all aliases), OpenCode `mac-qwen38` provider, Codex provider `qwen38-local` via chat2responses shim (port 8112).

## Flags that matter

- 4-bit launcher: `--prefill-step-size 16384 --kv-cache-dtype int4 --kv-cache-turboquant v4 --no-thinking --reasoning-parser qwen3`
- MUST run with `env -i` (Hermes venv has broken numpy/pydantic) + `KMP_DUPLICATE_LIB_OK=TRUE`.
- Prefill-tuned rapid-mlx: `--prefill-step-size 32768 --hybrid-cache-entries 4096` (+17% prefill).
- MTP reference: `--speculative-config '{"method":"mtp","model":"<path>/mtp.safetensors","num_speculative_tokens":3}'`

## Gotchas

- MTPLX model THINKS by default — burns ~50 tokens on reasoning before content. Give max_tokens ≥200 or you get empty content.
- LM Studio defaults to 8192 ctx on load; pass `--context-length` explicitly.
- Model arithmetic is weak at ALL quants — pair with a calculator/tool call when precision matters.

## Models on disk

- `mlx-community/Qwen3.8-27B-4bit` (16GB) — default
- `Youssofal/Qwen3.8-27B-MTPLX-Optimized-Speed` (20GB) — LM Studio long-context
- `AutomatosX/AX-Qwen3.8-27B-MLX-AXQ-6bit-MTP` (20.9GB) — quality-sensitive short work
- `mlx-community/Qwen3.8-27B-8bit` (29.5GB) — kept for 128K max, no quality edge

## Files

- `results/fingerprint-qwen38.json`, `results/hard2-{q4,axq6,8bit}.json`, `results/mtplx-{q4,mtplx}.json`
- Harnesses: `fingerprint-bench.py`, `hard-quality-bench.py`, `hard2-bench.py`, `mtplx-bench.py`

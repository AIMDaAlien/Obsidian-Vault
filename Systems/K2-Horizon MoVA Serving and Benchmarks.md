# K2-Horizon MoVA 36B-A4B — Serving & Benchmarks

Date: 2026-09-06
Model: IFM/K2-Horizon-MoVA-36B-A4B — MoE (36B stored / 4B active) with MoVA attention, 524K native context
Related: [[Local AI Benchmark Content Site]], [[Local AI Stack Research - Gemma 4 on M5 Pro]], [[unraid-qwen38-notes]]

## TL;DR

- K2 needs a llama.cpp fork: MBZUAI-IFM/llama.cpp branch model/K2Horizon (commit 35999d10). Official llama.cpp rejects the arch.
- Mac M5 Pro (Metal, IQ4_XS): ~54 tok/s, flat from 32K to 128K context. Winner for interactive use.
- Unraid (CUDA, IQ3_XXS, CPU-offloaded experts): 22 tok/s after tuning — was 9.5 before. The powersave CPU governor was the main culprit.
- Speculative decoding: not available. No MTP draft model exists for this arch; n-gram is a bad fit for bandwidth-bound CPU-offloaded MoE.
- Verdict: keep K2 on the Mac for interactive work; Unraid box is the always-on headless fallback.

## Engine options evaluated

| Engine | Status on this hardware |
|---|---|
| llama.cpp fork | Working — both machines |
| vLLM / SGLang | Officially supported but needs full GPU residency (~38-75 GB). Not viable on 12 GB. |
| MLX | Supported via oMLX ≥0.6.4 (hermitdave oQ4e/8bit/6bit conversions). Not benchmarked here; llama.cpp Metal was already fast. |

Quality is quant-driven, not engine-driven; engine choice moves latency/throughput.

## Unraid (RTX 3060 12 GB, i5-12600KF, 128 GB DDR4)

- Quant: IQ3_XXS (14.6 GB), experts on CPU, attention/KV on GPU (~10.4 GB VRAM)
- Container: llm-k2horizon, port 18007
- Files: /mnt/cache/appdata/unraid-llm/{Dockerfile.k2horizon, k2horizon-entrypoint.sh, k2bench.py}

### The tuning lesson (9.5 → 22 tok/s, no quality loss)

1. CPU governor was powersave — forced performance. This alone was the biggest win.
2. KV cache f16 → q8_0 (halves KV bandwidth, negligible quality cost).
3. --load-mode mlock+mmap (fixes tensor-override/mmap warning, keeps weights resident).

Final flags: --cpu-moe --gpu-layers 99 --threads 16 --flash-attn on --jinja --cache-type-k q8_0 --cache-type-v q8_0 --load-mode mlock+mmap

Results (3 prompts × 3 runs, 512 tok): short 22.2, reasoning 22.1, code 22.1 tok/s.

⚠️ Governor can revert on reboot — re-check /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor after Unraid restarts.

## Mac M5 Pro 48 GB (Metal)

- Quant: IQ4_XS (20.1 GB, NANI-Nithin GGUF) — higher quality than the Unraid IQ3_XXS
- Fork built with -DGGML_METAL=ON -DGGML_ACCELERATE=ON → /tmp/k2llama/build/bin/llama-server (move it somewhere durable before /tmp clears)
- Model at ~/models/k2-horizon/K2-IQ4_XS.gguf
- Results: 54.7 / 54.4 / 53.2 tok/s at 32K ctx; 54.5 / 54.1 / 51.1 at 128K ctx
- Decode is flat across context; 128K KV (q8_0) fits fine in 48 GB
- Prefill is the long-context cost: 23K-token prompt ≈ 2 min end-to-end (~250 tok/s incl. decode)
- Note: 128K context is for big-document work, not chat snappiness

## Model landscape (agentic/SWE, 30-40B class, Sept 2026)

| Benchmark | K2-MoVA-36B | Ornith-1.5-35B | Qwen3.6-35B |
|---|---|---|---|
| DeepSWE | not published | 22 | 0 |
| Terminal-Bench 2.1 | 58.6 | 67.8 | 52.5 |
| SWE-bench Verified | n/a | 79 | 73.4 |
| GPQA-Diamond | 80.8 | 89.2 | 86.0 |
| tau3-Banking (tool use) | 26.8 | n/a | 9.3 |

- DeepSWE "0" for Qwen and "not published" for K2 are what the published tables show — treat with skepticism; likely means "not run/harness mismatch" rather than a true zero.
- Ornith-1.5-35B is the DeepSWE/SWE contender at this size class; K2 wins tool-call reliability and native 512K context.
- "Supersedes GPT-5.6 Luna" claim: card-level BF16 numbers at high reasoning effort; quantized local runs land below those.
- Ornith is Qwen-arch → mainstream llama.cpp support, no fork needed. Good candidate for the Unraid box.

## Where this is recorded publicly

MetalBench (Projects/metalbench) now carries: two K2 model entries, three artifact-backed throughput runs (Unraid 32K, Mac 32K, Mac 128K) with SHA-256-verified JSON artifacts, a "governor and KV tuning" finding, and the updated Unraid hardware notes. Catalog validates; 40/40 tests pass.

## Open items

- [ ] Move /tmp/k2llama build to a durable location
- [ ] Decide whether to restart llm-qwen38-flash or leave K2 as the sole Unraid resident
- [ ] Optional: Ornith-1.5-35B GGUF on Unraid for DeepSWE-type agent work
- [ ] Optional: bump Unraid K2 context to 64K (RAM allows; untested)

---
tags: [local-ai, hardware-constraints]
---
# Local AI Stack Research - Gemma 4 on M5 Pro

> Research distilled from web sources, 2026-08-10. Separate from the benchmark registry.
> Hardware baseline: M5 Pro, 48 GB RAM.

## The short version

Stack is realistic on 48 GB. Use MLX + aggressive 4-bit + KV compression (TurboQuant/RotorQuant) and the Sage tier stays comfortable. Reflex and Awareness hit snappy sub-second latencies. Sage is more like 0.5-1 s TTFT with solid throughput.

## Why MLX

- MLX is the fastest local runtime for Gemma-class models on Apple Silicon.
- Beats llama.cpp/Ollama by ~30-50% on decode throughput.
- 4-bit quants run fully in unified memory.
- Rule of thumb: ~0.5-0.7 GB per billion params (4-bit) + 1-2 GB KV at 8k ctx, scales linearly.

## Gemma 4 footprint table (weights only)

- **Gemma 4 E2B** - ~11.4 GB BF16, 5.7 GB SFP8, 2.9 GB Q4_0
- **Gemma 4 E4B** - ~17.9 GB BF16, 8.9 GB SFP8, 4.5 GB Q4_0
- **Gemma 4 26B A4B** - ~57.7 GB BF16, 28.8 GB SFP8, 14.4 GB Q4_0

## Tier 1 - Reflex: Gemma 4 E2B

- MoE, ~2B active params, text + image + audio variants.
- MLX 4-bit: ~3-3.5 GB weights, ~5-7 GB total. Leaves 40+ GB free on this Mac.
- Throughput: ~97-124 tok/s MLX 4-bit, up to ~158 on M5 Max (Q4_K_M).
- TTFT ~150-400 ms for 1-2k prompts. Sub-100 ms isn't literal physics, ~200-300 ms is real.
- ~120-150 ms to first token + 80-120 tok/s feels instant in normal UX.
- MTP: use it for structured tasks (rewrite/summarize/code). On GPU it trends positive.
- With drafter: ~130-170 tok/s (1.3-1.5x).
- Config: MLX 4-bit + MTP drafter with modest N (2-4).

## Tier 2 - Awareness: Gemma 4 E4B multimodal

- ~9.6B total / ~4.5B active, text + vision (+ audio/video in community builds).
- MLX 4-bit VLM: ~4.9-5 GB weights, ~6-7 GB total.
- Decode ~45-70 tok/s on MLX, TTFT ~300-500 ms for 1-2k prompts.
- Image encode ~180-250 ms per screenshot.
- End-to-end per Awareness tick: ~250-400 ms. Fine for real-time sprite expression updates.
- vs 7-9B VLMs: E4B beats Qwen2.5-VL 7B (~38 tok/s) and crushes LLaVA-1.6 (~10-20 tok/s) on throughput per watt.
- Latency cuts: separate MLX process from Sage, pre-resize screenshots.

## Tier 3 - Sage: Gemma 4 26B A4B

- MoE ~26B total / ~3.8-4B active per token. Behaves like a 4B computationally with 25B reasoning.
- MLX OptiQ 4-bit: ~14.9-17 GB weights. Leaves ~30 GB for KV on 48 GB.
- Real numbers: 113 tok/s at 4k ctx (high-end chip), ~85 on M3 Ultra, ~45.7 on MacBook Air (aggressive quant), ~81 on M5 Max.
- M5 Pro realistic: ~45-70 tok/s decode at 4-8k ctx, TTFT ~0.6-1.0 s.
- With MTP drafter: ~65-80 tok/s (1.3-1.5x). Unsloth reports up to 2x on long agentic prompts.
- Heavy research: TTFT ~0.7-1.2 s, decode ~65-80 tok/s, 512-token answer in ~6-8 s.
- BF16 is a no-go (~50 GB, 8-15 tok/s, saturates the machine). 4-bit is the right call.

## MTP vs speculative decoding

- Classic spec decode: small draft model generates ahead, big target verifies in parallel.
- Gemma 4 MTP: integrated drafter head with shared embeddings/activations.
- Google reports 1.5-2.2x decode speedup on GPU, no quality loss.
- E4B: MTP recommended for all tasks. E2B: structured tasks yes, free-form chat sometimes slower on pure CPU, positive on GPU.
- Use the official drafter pairs, not hand-rolled spec decode.

## TurboQuant vs RotorQuant

- **TurboQuant (KV cache)** - rotates KV vectors (FWHT/FFT style), quantizes to ~2-3 bits, sparse sign residuals. ~3.1 bits/element, 60-78% memory reduction vs fp16.
  - Up to 5.5x compression on long contexts, often neutral or positive throughput.
  - Gemma 4 31B: KV 13.3 GB -> 4.9 GB at 128k ctx.
- **RotorQuant (KV cache)** - rotation-based isotropic quantization, tuned for 2-bit KV.
  - Qwen3.5-27B 2-bit: ~9.3 GB total vs 66.8 GB baseline. ~10x KV compression.
  - Better perplexity than simple 2-bit, often faster than TurboQuant at equivalent bits. More battle-tested on Qwen than Gemma.
- Recommended configs:
  - Reflex: MLX 4-bit, vanilla KV or light TurboQuant (4-bit LEAN) only if context >32k.
  - Awareness: MLX 4-bit + TurboQuant 3-3.5-bit KV. 3.6-5.5x compression, <1% perplexity change, crosses fp16 in throughput at ~4k+ ctx.
  - Sage: MLX 4-bit + TurboQuant 3-bit (K4V4/K3V3) or RotorQuant 2-bit if hard memory-bound at 128k+ ctx.

## Tier cheat sheet (M5 Pro 48 GB)

- **Reflex** - Gemma 4 E2B 4-bit MLX, MLX KV, ~6-7 GB, ~100-140 tok/s (with MTP), TTFT ~150-300 ms.
- **Awareness** - Gemma 4 E4B 4-bit MLX-VLM, TurboQuant 3-3.5-bit KV, ~8-10 GB, ~45-70 tok/s, TTFT ~250-400 ms incl image.
- **Sage** - Gemma 4 26B A4B 4-bit MLX, TurboQuant 3-3.5-bit or RotorQuant 2-bit KV, ~22-28 GB at 64-128k ctx, ~65-80 tok/s (with MTP), TTFT ~0.7-1.2 s.
- All three can coexist on 48 GB with careful context budgeting. Unload Awareness when Sage needs KV for research.

## TTS: Chatterbox

- Open-source, pip-installable, fully offline. ~3.2 GB peak RAM in ONNX app deployments.
- Emotion: punctuation affects prosody but does NOT auto-classify emotion. Emotion tags are explicit inputs (style tokens).
- For automatic emotion: build a text-side classifier (punctuation + lexical cues -> emotion labels), feed into Chatterbox's emotion controls. That glue logic is yours, not native.

## STT: whisper.cpp (Metal)

- De-facto local STT on Apple Silicon.
- M5 Pro Metal: Tiny/Base/Small/Medium ~30-40x real-time, Large-v3 ~14x real-time (1 s audio in ~70 ms).
- Streaming: `./stream -m ggml-small.bin --step 500 --length 5000`, ~200-400 ms latency.
- Use large-v3-turbo or small, stream microphone to feed text to Reflex/Sage.
- Multilingual built-in via `-l` flag.

## Notes

- KV cache is the bottleneck on long contexts, not weights. That's why TurboQuant/RotorQuant matter.
- 速度 (そくど) = speed. 加速 (かそく) = acceleration. "MTP gives かそく to decoding."

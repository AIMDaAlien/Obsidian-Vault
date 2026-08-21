---
tags: []
---
# Speed Myth - Ollama vs Text-Gen-WebUI

> **TL;DR:** Gemini's claim that text-gen-webui is ~30% faster than Ollama is true for EXL2/GPTQ models, but completely irrelevant for vision models which only exist as GGUF.

## The Claim

"Text-generation-webui is about 30% faster than Ollama"

## The Reality

This depends entirely on which **model format** and **backend** you're using.

### Speed by Format and Backend

| Format | Backend | Prompt Speed | Token Speed | Vision Support |
|--------|---------|-------------|-------------|----------------|
| EXL2/GPTQ | ExLlamaV2 (text-gen-webui) | ~56 t/s | Fastest | No |
| GGUF | llama.cpp (text-gen-webui) | ~25 t/s | Baseline | Yes |
| GGUF | llama.cpp fork (Ollama) | ~25 t/s | Baseline | Yes |

ExLlamaV2 processes prompts **2.2x faster** than llama.cpp. That's where the "30%" claim originates — it's actually even bigger than 30% for prompt processing.

**But here's the catch:** ExLlamaV2 only works with EXL2 and GPTQ formats. Vision models like Qwen3-VL require GGUF format because the vision encoder (mmproj) only works with llama.cpp. When text-gen-webui loads a GGUF model, it uses the exact same llama.cpp engine that Ollama uses. Zero speed difference.

## Why Ollama Wins for Our Use Case

- Same inference speed for GGUF models
- One-command model management (`ollama pull`, `ollama list`)
- Native OpenAI-compatible API (http://localhost:11434/v1/)
- Auto GPU detection and layer offloading
- Seamless OpenClaw integration
- `OLLAMA_KEEP_ALIVE` for persistent model loading
- Simpler LAN exposure for cross-machine inference

## When Text-Gen-WebUI Would Win

- You're using EXL2/GPTQ format models (text-only, no vision)
- You need LoRA adapter loading
- You want fine-grained parameter control (rope scaling, speculative decoding)
- You're doing model experimentation and need the Swiss Army knife

## Sources

- oobabooga's official GPTQ/AWQ/EXL2/llama.cpp benchmark blog
- ExLlamaV2 benchmarks (Towards Data Science, Jan 2025)
- llama.cpp GitHub discussions #4167 and #6730

## Navigation

- Back to [[Project Overview - Sovereign AI Stack]]

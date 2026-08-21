---
tags: [local-ai]
---
# LFM2.5-8B-A1B

> Status: deployed + benchmarked. Mac-local, rapid-mlx.

## Model
- LiquidAI/LFM2.5-8B-A1B-MLX-8bit — 8.4 GB, MLX 8-bit
- 8.3B total / 1.5B active hybrid MoE, 128K ctx, ChatML
- Reasoning model (CoT before answer). 38T training tokens.
- Vendor: "on-device personal assistant... not best fit for heavy programming or knowledge-intensive QA without retrieval"

## Runtime
- rapid-mlx, port 8110, `--tool-call-parser lfm`
- 4-bit alias exists: `lfm2.5-8b-a1b-4bit`

## Benchmark (text 58 items)
- **53/58 (91.4%)** — knowledge 39/40, research 6/6, planning 8/8, summary 1–2/4
- **107 tps, 9.1 GB RSS — 14× faster than Gemma Q4 at same RAM**
- Knowledge miss: light speed "300,000 km/s" (correct, wrong unit for grader)

## Notes
- First tool-call attempt sometimes emits `<think>` instead — retry succeeds
- Native tool format is Pythonic `<|tool_call_start|>`

## Verdict
The interactive winner. Desktop-companion / agent-loop material. Related: [[LFM2.5-2.6B]]

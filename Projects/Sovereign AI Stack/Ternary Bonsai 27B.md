---
tags: [local-ai]
---
# Ternary Bonsai 27B

> Status: deployed + benchmarked. Mac-local (was already in LM Studio), rapid-mlx.

## Model
- prism-ml/Ternary-Bonsai-27B-mlx-2bit — 7.9 GB, MLX 2-bit ternary
- 809k downloads. Qwen-based ternary MoE.

## Runtime
- rapid-mlx, port 8110, `--tool-call-parser hermes`
- rapid-mlx registry alias: `bonsai-27b-2bit`

## Benchmark (text 58 items)
- **53/58 (91.4%)** — knowledge 38/40, research 6/6, planning 8/8, summary 1/4
- **6.4 tps, 7.1 GB RSS**
- Two knowledge misses are grader artifacts: H₂O (unicode) and light speed (unit)
- Effective ~55/58 (~94.8%)

## Verdict
Solid dense alternative. Same competence tier as Gemma Q4, slower. Good fallback for the Mac when Gemma is busy. Related: [[Gemma 4 12B QAT Q4]]

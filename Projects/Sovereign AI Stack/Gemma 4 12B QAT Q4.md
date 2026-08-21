---
tags: [local-ai]
---
# Gemma 4 12B QAT Q4

> Status: deployed + benchmarked. Mac-local, rapid-mlx. The desktop-companion candidate.

## Model
- mlx-community/gemma-4-12B-it-qat-4bit — 10.3 GB, MLX 4-bit QAT
- Multimodal, 128K ctx

## Runtime
- rapid-mlx, port 8110, `--tool-call-parser gemma4`
- hrapid profile: `hgemma-q4`

## Benchmark (full 76 items)
- **66/76 (86.8%)** — vision 7/10, OCR 4/8, summary 1/4, knowledge 40/40, research 6/6, planning 8/8
- Text-only: 55/58 (94.8%)
- tps ~7.4, RAM 9.7 GB warm
- Knowledge/research/planning flawless. The only gap vs Q8: OCR (4/8 vs 6/8)

## OCR weaknesses (vs Q8)
- date: 2026 → 2023
- hex: 0x3F8C2A → 0x3E8C2A
- QC-8471 → CQ-8471 (same as Q8)

## Verdict
Same text competence as Q8 at smaller size. Perfect for the desktop companion project. Keep both: Q8 for OCR-critical work, Q4 as the fast default. Related: [[Gemma 4 12B QAT Q8]]

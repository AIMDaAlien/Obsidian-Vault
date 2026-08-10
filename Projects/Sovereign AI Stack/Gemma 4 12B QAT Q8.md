# Gemma 4 12B QAT Q8

> Status: deployed + benchmarked. Mac-local, rapid-mlx.

## Model
- mlx-community/gemma-4-12B-it-qat-8bit — 11.9 GB, MLX 8-bit QAT
- Multimodal (vision + audio + video), 128K ctx
- Gemma 4 family: 4/8/26/31B, QAT quants

## Runtime
- rapid-mlx, port 8110, `--tool-call-parser gemma4`
- Serve: `KMP_DUPLICATE_LIB_OK=TRUE rapid-mlx serve gemma-4-12b-qat-8bit --served-model-name hgemma-local ...`
- hrapid profile: `hgemma`

## Benchmark (full 76 items)
- **68/76 (89.5%)** — vision 7/10, OCR 6/8, summary 1/4, knowledge 40/40, research 6/6, planning 8/8
- Text-only: 55/58 (94.8%)
- tps ~7, RAM 4.7 GB cold / ~13 GB warm
- Vision misses are grader strictness (blue square read as "blue rectangle")
- OCR: only glyph-level slip is QC-8471 → CQ-8471 (font ambiguity)

## Edge vs Q4
- Q8 is measurably more careful on glyph-level OCR: Q4 also botched date (2026→2023) and hex (0x3F→0x3E)
- Same competence everywhere else

## Verdict
Default all-rounder. Best when answer quality trumps speed. Related: [[Gemma 4 12B QAT Q4]]

# LLM Benchmark Registry — Mac vs Unraid

> Last updated: 2026-08-09
> All scores from deterministic graders only. No LLM judge anywhere.
> Exact-match / substring / ROUGE-L / JSON tool-call parse. Nothing hallucinated.

## Hardware

| Box | Spec | Role |
|---|---|---|
| **Mac (this)** | 48 GB unified RAM, Apple Silicon | local daily driver, vision/OCR, companion |
| **Unraid** (192.168.0.120) | 128 GB RAM, i5-12600KF 16T, RTX 3060 12 GB | heavyweight GPU models, always-on |

## Test batteries

- **Full (76 items)**: vision 10, OCR 8, summary 4, knowledge 40, research 6, planning 8
- **Text (58 items)**: knowledge 40, research 6, planning 8, summary 4
- Grading: normalized exact-substring (number words → digits), multi-token hits for vision, ROUGE-L F1 ≥ 0.30 for summaries, JSON tool-call parse for research

## Scores — Mac (48 GB)

| Model | Quant | Size | RAM RSS | tps | Full 76 | Text 58 | Knowledge | Research | Planning | Summary |
|---|---|---|---|---|---|---|---|---|---|---|
| [[Gemma 4 12B QAT Q8]] | 8-bit | 11.9 GB | 4.7–13 GB | ~7 | 68/76 (89.5%) | 55/58 (94.8%) | 40/40 | 6/6 | 8/8 | 1/4 |
| [[Gemma 4 12B QAT Q4]] | 4-bit | 10.3 GB | 9.7 GB | ~7.4 | 66/76 (86.8%) | 55/58 (94.8%) | 40/40 | 6/6 | 8/8 | 1–2/4 |
| [[LFM2.5-8B-A1B]] | MLX 8-bit | 8.4 GB | 9.1 GB | 107 | — | 53/58 (91.4%) | 39/40 | 6/6 | 8/8 | 1–2/4 |
| [[LFM2.5-2.6B]] | MLX 8-bit | 2.9 GB | 3.4 GB | 76.8 | — | 53/58 (91.4%) | 38/40 | 6/6 | 8/8 | 0/4 |
| [[Ternary Bonsai 27B]] | MLX 2-bit | 7.9 GB | 7.1 GB | 6.4 | — | 53/58 (91.4%) | 38/40 | 6/6 | 8/8 | 1/4 |
| [[Maple-Preview 20B]] | 2-bit ternary | 5.3 GB | 2.2 GB | 172.5 | — | 46/58 (79.3%) | 38/40 | 0/6* | 7/8 | 1/4 |

\* Maple research 0/6 = runtime limitation (mlx-lm server has no native tools). It refused to fabricate the FIFA answer — honest non-fabrication, counted as miss by the harness.

## Scores — Unraid (128 GB + RTX 3060)

| Model | Quant | Size | RAM | tps | Text 58 | Knowledge | Research | Planning | Summary |
|---|---|---|---|---|---|---|---|---|---|
| [[Qwen3.6 35B A3B Abliterated]] | Q6_K + MTP | 27.2 GB | ~27 GB | ~13 | — | — | — | — | — |
| [[Deepwen-3.6]] | Q4.5-MoQ | 19.7 GB | — | — | pending | pending | pending | pending | pending |

## Key takeaways

- **Speed vs competence tradeoff is stark.** Maple 172 tps / 2.2 GB vs Gemma Q4 7.4 tps / 9.7 GB — 23× faster at ¼ the RAM, but 79% vs 96% text score.
- **Knowledge + research + planning are the saturated domains.** Every model gets 38–40/40 knowledge and 6/6 tool-calling. Differentiation lives in summary, OCR, and speed.
- **Gemma 4 Q4 = best all-rounder** for careful answers. Q8 only wins on glyph-level OCR (date 2026→2023 and hex 0x3F→0x3E misses on Q4).
- **LFM2.5 8B = the interactive winner.** 14× faster than Gemma at same RAM, same text competence. Desktop-companion material.
- **LFM2.5 2.6B = tiny and fast** but verbose CoT wrecks ROUGE-L summaries.
- **Maple = efficiency king** but preview-grade reasoning focus, no agentic tools.
- **Bonsai 27B = solid dense alternative**, similar competence to Gemma, slower.

## Related

- [[Gemma 4 12B QAT Q8]]
- [[Gemma 4 12B QAT Q4]]
- [[LFM2.5-8B-A1B]]
- [[LFM2.5-2.6B]]
- [[Ternary Bonsai 27B]]
- [[Maple-Preview 20B]]
- [[Deepwen-3.6]]
- [[Unraid Qwen3.6 Terminal Agent - July 2026]]

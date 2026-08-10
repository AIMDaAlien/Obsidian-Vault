# LFM2.5-2.6B

> Status: deployed + benchmarked. Mac-local, rapid-mlx.

## Model
- LiquidAI/LFM2.5-2.6B — 2.6B dense, 128K ctx, 15 languages
- MLX repo ships ALL quants (4/5/6/8-bit + bf16 + mxfp/nvfp) — pulling the whole repo is 18.7 GB; point rapid-mlx at the `8bit/` subfolder (2.9 GB) to save space

## Runtime
- rapid-mlx, port 8110, `--tool-call-parser lfm`
- Serve from: `.../LFM2.5-2.6B-MLX/snapshots/<hash>/8bit`

## Benchmark (text 58 items)
- **53/58 (91.4%)** — knowledge 38/40, research 6/6, planning 8/8, summary 0/4
- **76.8 tps, 3.4 GB RSS** — tiny footprint, fast for a dense model

## Notes
- Verbose CoT hurts ROUGE-L summaries (0/4) — the content is right, the terseness isn't
- H₂O unicode subscript vs "H2O" grader artifact

## Verdict
Tiny + fast. Great for quick interactive loops where 2.6B is enough. The 8B sibling trades RAM for noticeably better summaries. Related: [[LFM2.5-8B-A1B]]

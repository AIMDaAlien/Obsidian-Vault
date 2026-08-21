---
tags: [local-ai]
---
# Maple-Preview 20B

> Status: deployed + benchmarked. Mac-local, dedicated mlx-lm fork.

## Model
- deepgrove/maple-preview-2bit-mlx — 5.3 GB checkpoint, 2-bit ternary
- 20B-A1B ternary MoE: 24 layers, 256 experts top-8, 3:1 SWA-512:GA, 128K ctx
- MIT. DeepGrove = the Bonsai makers.
- "preview focused on raw reasoning... may underperform on agentic"

## Runtime (IMPORTANT)
- Does NOT run under stock rapid-mlx (custom `maple.py` class + flash-head)
- Needs the fork: `deepgrove-ai/mlx-lm-deepgrove` (clone + ./setup.sh)
- Serve: `mlx_lm server --model <dir> --trust-remote-code --flash-head`
- mlx-lm server has NO native OpenAI tool-calling

## Benchmark (text 58 items)
- **46/58 (79.3%)** — knowledge 38/40, planning 7/8, summary 1/4, research 0/6*
- **172.5 tps, 2.2 GB RSS — the efficiency king** (23× faster than Gemma Q4 at ¼ RAM)
- *research 0/6 = no native tools on the fork's server; model honestly refused the FIFA question instead of fabricating

## Notes
- Knowledge misses are unit/typo artifacts (3.00×10^8 m/s correct, "Sahaara" typo)
- Vendor claims 218 tok/s on M4 Mac mini (we measured 172 tps)

## Verdict
Raw-reasoning specialist with insane speed. Not for agentic/tool loops yet. Watch for the "faster custom library" DeepGrove teased. Related: [[Ternary Bonsai 27B]]

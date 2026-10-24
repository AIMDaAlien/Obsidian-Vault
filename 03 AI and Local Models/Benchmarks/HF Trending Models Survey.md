---
type: benchmark-log
topic: HF Trending Models Survey
publish: true
created: 2026-10-01
tags: [omarchy, benchmark]
machine: bigrig
title: "HF Trending Models Survey"
---
# HF Trending Models Survey


## 2026-10-01 23:43
**Done:** Parsed a 222KB Hugging Face trending-models API response (60 text-gen models) and classified entries by size, MoE/A3B-A4B, and uncensored/abliterated/roleplay traits.
**Findings:** Qwen3.8-27B is the dominant base — the top trending model (prism-ml/Ternary-Bonsai-2-27B-gguf, 3.7M downloads) is a 2-bit ternary quant of it, and ~8 further 27B derivatives cluster in the top 20. Secondary families: GLM-5.3 (MoE/DSA, mostly cybersecurity/abliterated forks), MiMo-V2.6 (multimodal RL), Ornith-1.5 (9B/35B-A3B), Spark-X2.5-4B. A large uncensored/abliterated sub-trend (OrcaSAQ, Heretic, OBLITERATED, penclaw) rides on Qwen3.8 and GLM-5.3 base weights. No Hermes/Luma/Magnum/Celeste/Rocinante/Bunny/Suzume/MN-12 or explicit persona/companion naming present in this snapshot.
**Recommendations:** Treat Qwen3.8-27B derivatives as the reference lineage when benchmarking local quants; watch whether MoE A3B/A4B variants (Xing4.0-29B-A4B, yandex AliceAI-80B-A3B) keep climbing.

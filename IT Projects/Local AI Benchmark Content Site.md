---
tags: [local-ai, side-project, monetization]
---
# Local AI Benchmark Content Site — Plan

> 2026-08-29. Goal: turn the local-AI benchmark findings into a traffic site →
> monetize → fund a Mac Studio M5 Ultra 512 GB (Oct 2026).
> Raw material lives in [[Project Overview - Sovereign AI Stack]] + this vault.

## Positioning (the one-liner)

"Frontier models on hardware you actually own." The honest, measured reality of
running 176B MoE / 320B models on a MacBook and a 128 GB + RTX 3060 Unraid box —
with deterministic benchmarks that name *which questions* fail. Almost all local-LLM
content is either "just run Ollama" or "buy 8× H100s"; the CPU-offloaded-MoE middle
ground is under-served and has high search intent.

## Why it's differentiated (defensible moat)

- **No-LLM-judge grading.** Exact/substring/ROUGE-L/JSON-parse only. Nobody else
  publishes this rigorously.
- **"What fails" framing.** Perfection proves nothing; the value is the failure
  diff (Q3_K_XL vs IQ3_XXS vs Q2_K_XL, which questions break).
- **Measured, not vendor-quoted.** RAM-fit rule (total weights ≤ available RAM),
  bandwidth-bound decode math, spec-decode myth-busting with real numbers.
- **Two hardware personas** (Mac 48 GB + Unraid 128 GB) — both recurring, so
  readers self-identify with one.

## Content pillars (each = a repeating series)

1. **"Can it run?"** — frontier-model feasibility teardowns on real hardware.
   GLM-5.3-Flash (320B → IQ1-only no-go), DeepSeek V4 Flash (284B → Q2 marginal),
   Qwen3.8-Flash-Next (176B/6B → the sweet spot). Strong search + share bait.
2. **Quant shootouts** — same model, 2-3 quants, deterministic battery, name the
   failing questions. (IQ3_XXS = Q3_K_XL quality, -9% size.)
3. **Spec-decode myth-busting** — MTP / DFlash / DSpark / MTPLX on memory-bound
   hardware: measured dead-ends. Counter-intuitive = high-share.
4. **Optimization wins** — thread count (+17%), --cpu-moe, quant choice, RAM tuning.
   Actionable "do this" content.
5. **The methodology** — active-vs-total params, bandwidth-bound decode, the
   RAM-fit rule. Positions the author as the rigorous one.
6. **Hardware buyer's guide** — what actually matters (RAM > GPU for MoE offload,
   active params for speed). Monetizable + evergreen.

## Tech stack (low-effort, free)

- **Static site**: Astro (or Hugo) → Cloudflare Pages or GitHub Pages (already used
  for the portfolio project). Markdown content = the vault notes port almost
  directly (tables, links already exist).
- Optional interactive bits: a "which quant fits my RAM" calculator (tiny JS) — the
  single highest-leverage SEO/lead-magnet widget.

## Traffic strategy

- **Search**: long-tail "run Qwen3.8 locally / 176B on 128GB / IQ3_XXS vs Q3_K_XL /
  MoE quantization / speculative decoding CPU offload" — high intent, low competition.
- **Reddit r/LocalLLaMA + HN**: the "I benchmarked every quant that fits" and
  "spec decode doesn't help memory-bound MoE — here's the data" posts are exactly
  what gets upvoted there. The benchmark result files are the receipts.
- **X / newsletter**: short "finding of the day" cadence to feed the site.

## Monetization (in order)

1. Traffic → display ads (Mediavine/AdSense once ~50k+ sessions/mo).
2. Affiliate: cloud-GPU, hardware, HF-adjacent links in buyer's-guide posts.
3. Paid artifact: a "Local LLM Buyer's Guide 2027" PDF / a per-model quant-fit
   spreadsheet. Only after the audience exists.

## Launch sequence

1. Port the finished benchmark write-ups (Flash-Next spec-decode + quant shootout,
   GLM-5.3 no-go, frontier landscape) → 3-4 launch posts.
2. Ship the "which quant fits my RAM" calculator widget.
3. Reddit/HN launch post with the real result JSONs as receipts.
4. Cadence: one "Can it run?" or shootout per new frontier release (there's a new
   one every ~2 weeks — the feed is self-renewing).

## Assets already on hand

- [[Qwen3.8-Flash-Next]], [[Qwen3.8-27B]], [[GLM-5.3-Flash]],
  [[Frontier Landscape - What Fits 128GB]], [[LLM Benchmark Registry - Mac vs Unraid]]
- Harnesses: `quantsens_bench.py` (42-question quant battery), `fingerprint-bench.py`
  (317q), `reason-bench.py` (21-item), `agent_bench.py` (deterministic agentic).
- Real measured numbers everywhere — nothing fabricated.

## MetalBench visual / product decision (2026-08-29)

Site is live at `https://metalbench.penthouse.blog/`.

**Approved frontend direction: Forge × Scout hybrid.**

- **Forge / homepage and hardware pages:** an honest Lab Pulse, current model,
  DDR4 residency, System Stress, VRAM, decode, and data-driven lab mood.
  No fake live movement: metrics are live only from a telemetry source; otherwise
  clearly `RECORDED` with timestamp.
- **Scout / compare page:** accessibility-first quality-vs-speed evidence plot.
  X = tok/s; Y = deterministic quality only within compatible benchmark cohorts;
  bubble size = resident model footprint; color = machine. Every point opens its
  runtime/quant/context/battery/failure/receipt panel.
- **Run Index:** large newest evidence card + metric rail, then chronological,
  machine-grouped evidence stream. Preserve provenance states: verified, tradeoff,
  no gain, no-go, documented/missing raw artifact.
- **Atlas editorial cards:** deferred to run/finding articles. Use for shareable
  verdicts such as `IQ3_XXS 41/42 and 16.92 tok/s vs Q3_K_XL 41/42 and 14.5`.

Motion: restrained counters and real trace interpolation only; respect reduced
motion; no fake terminals/particles/neon-gauge clutter.

OpenCode is wired to the live Unraid Qwen3.8-Flash-Next at `:18006` as
`qwen38-unraid/qwen38-flash`; wrapper: `ocmetal`. It passed a real tool-use
smoke test (read package.json). Implementation brief:
`/Users/aim/Documents/Projects/metalbench/FRONTEND-HYBRID-PLAN.md`.

## Open decisions

- Name/domain (suggest: "frontierlocal.ai" / "canitrun.it" / something persona-first).
- Platform: pure blog vs benchmark leaderboard vs both.
- Mac-first vs Unraid-first launch (suggest Unraid first — 176B-on-128GB is rarer).

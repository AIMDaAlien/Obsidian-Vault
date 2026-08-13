# Nemotron 3.5 Lightning vs Qwen 3.6 — Domain Fingerprint

> 2026-08-12. 130-question battery across 15 domains, deterministic grading.
> Unraid: Nemotron Q4_K_M (25.5G) vs Qwen3.6 Abliterated Q6_K (27.2G), RTX 3060.

## Raw scores (130 questions)

- Nemotron 3.5 Lightning 30B A3B: 126/130 (96.9%)
- Qwen 3.6 35B A3B Abliterated: 128/130 (98.5%)
- Both perfect on: history, science, math, linguistics, pop culture, sports,
  food, medicine, tech history, business, reasoning traps (11 domains, 10/10 each)

## Where they differ (the actual fingerprint)

- python_314: Qwen knows Python 3.14 released 2025. Nemotron says "not yet released" — its knowledge cutoff predates it.
- unraid_version: Nemotron knows Unraid 7. Qwen says 6 — Qwen's infra-specific knowledge is stale.
- Both correct on everything else; the other "misses" are grader artifacts
  (Brasília accent, native kana おはよう, caesium UK spelling — Nemotron's answers were BETTER).

## Agentic suites

- Easy (16): Qwen 16/16, Nemotron 14/16 (2 were reasoning-budget empties, both correct with headroom)
- Hard (17): Qwen 16/17, Nemotron 16/17 after budget fix — tied.
- Shared weaknesses: both used run_command instead of read_file (tool selection),
  both chose chmod 100 over chmod 700 (same trap).

## The real differences

1. Knowledge freshness: Nemotron fresher on server/infra (Unraid 7), Qwen fresher on dev/Python (3.14).
2. Reasoning budget: Nemotron burns 1000-2400 tokens thinking before answering
   (budget 2048) vs Qwen's 1024. Same competence, 2x the token cost per turn —
   matters for agentic loops.
3. Languages: Qwen 12/12 incl native script output; Nemotron 11/12 (native kana correct, grader artifact).
4. Throughput: Nemotron ~16 t/s, Qwen ~18 t/s (Q6_K vs Q4_K_M on the 3060).
5. Nemotron runtime quirk: intermittent HTTP 500 "peg-native format" — needs retry in harnesses.

## Bottom line

At these quants, indistinguishable on general knowledge. Pick by:
- Qwen for dev/Python-flavored agentic work + snappier per-turn cost
- Nemotron for infra/server agent work + fresher ops knowledge (and it's the
  model explicitly designed as a "sub-agent workhorse")

## Files

- results/fingerprint-{qwen,nemotron}.json
- results/agentic-{qwen,nemotron}.json
- results/hardagentic-{qwen,nemotron}.json
- fingerprint-bench.py + bank_{1-8}.py (317 questions, retry-capable)

## Expanded niche battery (banks 5-8, +187 questions)

Nemotron removed (26GB freed, container + roster + compose clean; the rebuilt
laguna image stays for Qwen). Added deep-niche banks:
- bank_5: obscure science (14), esoteric history (15), rare trivia (20)
- bank_6: 18 more languages, regional/cultural (10), food science (13), geo depth (14)
- bank_7: tech deep cuts (18), homelab/self-hosted (15), security (10)
- bank_8: Islamic knowledge (15), deeper math (15), multi-hop reasoning (10)
Full battery now 317 questions across 28 domains.

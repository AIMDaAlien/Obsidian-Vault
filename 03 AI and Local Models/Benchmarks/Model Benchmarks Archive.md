---
type: archive
topic: Qwen3.8 Rig — historical benchmark log
updated: 2026-09-21
category: Benchmarks
tags: [benchmark, archive]
publish: true
created: 2026-09-21
machine: bigrig
title: "Model Benchmarks Archive"
---
# Model Benchmarks Archive

**Category:** [[Benchmarks]] · **Vault:** [[Vault Map]]

Superseded raw log from [[Qwen3.8 Rig]] (pre-2026-09-21). All current data lives in [[Model Benchmarks]] + per-model notes. Kept verbatim for provenance.

## Related

- Current hub: [[Model Benchmarks]] · rules: [[Benchmark Methodology]] · suite: [[Bench Suite (~bench)]]
- Per-run pages: [[2026-09-22 Rebench — Coherent Multi-Domain Scoreboard]]

## 2026-09-19 13:39
**Done:** smoke test of bench-note logger.
**Findings:** entry appended with timestamp; file auto-created.
**Recommendations:** agents call this after every benchmark session.

## 2026-09-19 13:47
**Done:** IQ3_S vs Q5_K_M graded coding eval (eval-swe40.py, 40 tasks / 112 asserts) + decode bench, 2026-09-15 session.
**Findings:** IQ3_S 88/112 (79%) vs Q5 93/112 (83%); T4 hard tier 10/25 vs 12/25; IQ3 1.8x slower (MTP broken on GSQ quants). All IQ3 files deleted. Raw data in ~/bench-results/.
**Recommendations:** keep Q5_K_M daily driver; reuse eval-swe40.py for any future quant test.

## 2026-09-19 13:47
**Done:** llama-server Vulkan split tuning + crash root-cause, 2026-09-16 sessions.
**Findings:** Vulkan0 was the iGPU — iGPU got the big layer share and SIGABRT'd/Hung Hyprland. Fixed: GGML_VK_VISIBLE_DEVICES pinned per launcher, iGPU invisible to llama.cpp. Rig RAM cliff: server ~28.6G RSS of 32G — opencode against local server OOM-kills it.
**Recommendations:** opencode default stays Unraid 176B; local-rig is opt-in; 2nd RX 9060 XT is the standing upgrade path (~2x decode, MTP@256K).

## 2026-09-19 17:48 [#llamafleet]
**Done:** llama.cpp rebuild to master e613ef2 (hc-ops #28901 + Vulkan/Metal, rms_norm fusion #28896, seq_cp fixes #27941) on Unraid container `llm-qwen38-flash`; rollback image tagged `rollback-930e2fa`; container recreated via compose. Swe40 re-run on new build.

**Findings:**
- New build raw swe40@3K: 99/112, 35/40, ~13.6 t/s, 2055s (old build raw: 101/112). All 5 fails = finish=length no-code-block (thinking burns budget); 16K retry in progress for corrected score. Speed unchanged at short ctx — hc-ops gains are long-context territory (#28734 decode-decay still open upstream).
- MTP speculative decode NOT available upstream yet (PRs #28243/#27836 open as of Sep 19); drafter file already downloaded at qfn-mtp/, entrypoint keeps it disabled.
- SSH access restored: `ssh unraid` alias + hermes_unraid key regenerated on MASSIVE-RIG, authorized on Unraid root.
- Key-chain: socat forward 127.0.0.1:18006 -> Unraid 18006 needed for local benching (auto-recreate per session).

**Recommendations:** judge quality only on budget-corrected scores for thinking models; keep rollback images tagged; re-check MTP PR status before next rebuild (drafter file ready).

## 2026-09-19 [#llamafleet]
**Done:** LiveCodeBench harness built (~/Work/lcb-bench.py + ~/Work/.venv-lcb, dataset release_v6 saved to ~/Work/lcb-v6). 60 problems: 20x easy/medium/hard, window >= 2025-01-01 (contamination-safe), LCB's own prompts + subprocess-isolated grader (check_correctness).

**Findings:**
- Gotchas hit: datasets 5.x refuses script datasets (pin datasets==3.6.0); testing_util.run_test nulls os.environ in-process — must run each test in a fresh subprocess (LCB's check_correctness does this); dataset has no input_output column (use CodeGenerationProblem.get_evaluation_sample()).
- Qwen-Q5_K_M on 8080 first LCB-60 run: lots of real differentiation — mediums/hards show genuine fail + no-code-block (4096 cap) results, unlike saturated swe40.

**Recommendations:** LCB-60 replaces eval-swe40 as the primary differentiator for local coders (swe40 saturates ~95%).

## 2026-09-20 00:00
**Done:** idle behavior changed: screensaver disabled (999999s), 5-min lock kept, suspend never used.
**Findings:** user wants local AI always-on, so no S3 suspend despite deep being available. Input wakes the lock screen. Fans already idle-silent (CPU 0 RPM, NVIDIA 0%, 45C) — no fancontrol needed.
**Recommendations:** beware accidental `systemctl suspend` — it would pause llama-server.

## 2026-09-20 08:47 [#llamafleet #lcb]
**Done:** LiveCodeBench-60 (release_v6, 20x easy/medium/hard, contest window >= 2025-01-01, budget-corrected via escalating retries) run on both local coders. Verdict runs: Qwen retry @12K then 24K; Flash @8K then 16K.

**Scoreboard (pass@1, budget-corrected):**
- Qwen3.8-27B Q5_K_M (8080, 27.5 t/s): 45/60 — easy 20/20, medium 17/20, hard 8/20. 14 hard-tier problems truncate even at 24K thinking tokens; 1 true fail.
- Flash-Next UD-IQ3_XXS e613ef2 (Unraid, ~14 t/s): 39/60 — easy 20/20, medium 15/20, hard 4/20. 21 hard-tier truncate even at 16K.
- Ladder was raw 40 vs 29 at 4K/8K caps; retries narrowed to 45 vs 39. Remaining no-code-block sets overlap heavily (arc192_a, abc400_d, abc388_f, abc392_g, 3733, 3562, ...).
- swe40 corrected after llama.cpp e613ef2 rebuild: Flash 106/112, 39/40 (rebuild at worst neutral).

**Findings:**
- Verdict for agentic SWE: Qwen-Q5 wins locally on BOTH quality (45 vs 39 LCB; 107 vs 106 swe40) and speed (27.5 vs 14 t/s, 2x). Flash-Next's only real local edge is 262K context. [SUPERSEDED 2026-09-21 — the [[Flash-Next AD384]] IQ4 at medium effort scores 54/60, beating Qwen.]
- "no-code-block" truncation is the dominant failure mode for both on hard tier — budget-corrected scoring is mandatory for thinking models.
- Caution on flip-flopping defaults: 8080 llama-server (Qwen) OOM-kills when a big opencode node runs on the rig (RAM cliff, 28.6G RSS server).

**Recommendations:** use LCB-60 as primary differentiator; escalation ladder 4K→8K/12K→16K/24K suffices.

## 2026-09-20 10:30
**Done:** Finished local-model metrics wiring: Hermes (plugin at ~/.hermes/plugins/local-model-metrics, sqlite llm-metrics.db, status-bar label) + opencode TUI footer (~/.config/opencode/tui/local-metrics) incl. stress gauge and compaction counter; Unraid llama-server now runs with --metrics.

**Findings:** Unraid /metrics flipped both apps to ·srv (↑182 prefill / ↓16 decode tok/s). Bun's os.loadavg() throws "Not implemented" — use /proc/loadavg. opentui TextRenderable content lives in children (clear/add). Hermes auto-updates wipe core-tree patches — metrics logic moved into the plugin dir; status-bar re-patch lives in ~/Work/ops/hermes-metrics-repatch.sh. Swift-Qwen3.8 GGUF template rejects reasoning_effort=high (xhigh/medium/low only) → use --reasoning low for local runs. Cloud sessions keep the sys gauge; interrupted turns freeze at last activity after 30s.

## 2026-09-21 12:30 [#llamafleet #lcb #pareto]
**Done:** effort-vs-quality LCB-60 sweep + Pareto chart. Qwen-Q5 rerun at `low` (12K), Flash-Next AD384 at medium(16K corr) and low(8K).

**Scoreboard (budget-corrected):**
- Qwen-Q5 low (12K): **48/60** — easy 20/20, med 17/20, hard 11/20, 27.7 t/s. Beats its own xhigh default 45/60 on both axes.
- Qwen-Q5 default xhigh (24K corr): 45/60 @ 24.7 t/s.
- Flash-Next AD384 medium (16K corr): **54/60** — hard 19/20, 16.9 t/s. Overturns the earlier "Flash loses" verdict (that was on IQ3_XXS Quant).
- Flash-Next AD384 low (8K): 41/60 @ 17.4 t/s.
- Unraid Flash-IQ3 (16K corr): 39/60 @ 14.2 t/s.

**Findings:**
- Low reasoning effort HELPS Qwen-Q5 on both axes (48>45, 27.7>24.7). Same for Flash AD384 medium>low (54 vs 41) when budget permits.
- Pareto frontier: Qwen-Q5-low (speed king) + Flash-AD384-medium (quality king). Pick by workload.
- Qwen-Q5 low fails: 3743,3763,3722,abc388_f,abc392_g,abc389_g,abc397_f,arc192_e,arc192_d,abc389_e,abc397_d,3562.

**Recommendations:** for fast agentic default keep Qwen-Q5 at low effort; reach for Flash-AD384-medium when quality > speed.
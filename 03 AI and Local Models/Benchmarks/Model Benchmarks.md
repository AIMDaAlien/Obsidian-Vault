---
type: benchmark-hub
topic: Model Benchmarks
updated: 2026-10-17
category: Benchmarks
tags: [benchmark, hub, index]
publish: true
created: 2026-10-12
machine: bigrig
title: "Model Benchmarks"
featured: 38
summary: "Which home-run AI models code best and fastest? One chart shows the trade-off, and the surprise that thinking less made the daily model better."
---
# Model Benchmarks
> [!warning] Correction (2026-10-17)
> This page's LCB-60 summary calls the best model "NOT yet conclusive" and puts Flash-Next AD384 medium (54/60 on LCB-60, 2026-09-21) on the Pareto frontier as the accurate, quality-king pick. A uniform 98-task multi-domain suite later settled it: qwen-low led with 193/213 checks, while Flash scored 88% (187/213) and was the slowest config ([[2026-09-22 Rebench — Coherent Multi-Domain Scoreboard]]). The role-tagged rerun kept the order, qwen-low 196/229 vs Flash 191/229 ([[2026-09-23 Rebench2 — Role-Tagged Scoreboard]]). Current standing: Qwen-Q5 27B at low effort is the best overall config; Flash-Next AD384 is not the quality king.


**Category:** [[Benchmarks]] · **Vault:** [[Vault Map]]

Local LLM LCB-60 + swe40 results on the MASSIVE-RIG and Unraid. Budget-corrected; higher + rightward / taller = better.

## 2026-10-12 — Corrected matched DeepSWE2 comparison

[[2026-10-12 Matched Qwen 27B vs Flash DeepSWE2]] — six complete campaigns, 144 audited results over 24 distinct synthetic repository tasks. Flash averaged **22.67/24** versus Qwen **21.00/24**; the task-bootstrap interval for the +1.67 Flash delta is **[-2.33, +5.67]**, including zero. The historical 27B advantage was not observed on this corrected suite. The note embeds delta and capability/latency charts, with [[2026-10-12 Matched Qwen vs Flash — Methods and artifacts|full methods, provenance and all archived supporting files]].


## Featured systems project

[[Strata RTX 3060 Optimization Showcase]] — **16.58% less response time** from accepted RTX 3060 long-context prefill tuning. Includes the six-bucket chart and confidence interval, engineering evidence, bottleneck profile, and the separately rejected expert-kernel campaign.

## The money chart — Pareto (quality × speed)

![[_attachments/lcb60-pareto.png]]

- Pareto frontier = **Qwen-Q5 27B low-effort** (fast) and **Flash-Next AD384 medium** (accurate). No point beats either on both axes. (superseded, see Correction above)
- Qwen-Q5 low-effort dominated its own default on *both* axes — use `low` thinking.

## Scoreboard (LCB-60 pass@1)

| Model | Run | easy | med | hard | total | t/s | value |
|---|---|---|---|---|---|---|---|
| [[Flash-Next AD384\|Flash-Next AD384 · medium]] | 16K corr | 20 | 15 | **19** | **54/60** | 16.9 | 9.1 |
| [[Qwen-Q5 27B\|Qwen-Q5 27B · low-eff]] | 12K | 20 | 17 | 11 | 48/60 | **27.7** | **13.3** |
| [[Unraid Flash-Next\|Unraid Flash-Next · OFF]] | 12K | 20 | 16 | 11 | 47/60 | 15.6 | 7.3 |
| [[Laguna XS-2.1\|Laguna XS-2.1 · OFF]] | 12K | 19 | 13 | **14** | 46/60 | **34.0** | 15.6 |
| [[Qwen-Q5 27B\|Qwen-Q5 27B · default]] | 24K corr | 20 | 17 | 8 | 45/60 | 24.7 | 11.1 |
| [[Flash-Next AD384\|Flash-Next AD384 · low]] | 8K | 20 | 14 | 7 | 41/60 | 17.4 | 7.1 |
| [[Unraid Flash-Next\|Unraid Flash-Next · IQ3]] | 16K corr | 20 | 15 | 4 | 39/60 | 14.2 | 5.5 |

**value** = (score × t/s)/100 — most output per wall-minute.

⚠ **Read across, not down-summed:** thinking policy varies row-to-row (corr = budget-corrected escalation; OFF = per-request thinking disabled). Uncorrected/OFF runs underreport on hard tier the way early-4K runs did. **Best is NOT yet conclusive** — see [[Laguna XS-2.1]] and [[Qwen-Q5 27B]]. (superseded, see Correction above)

## Where the passes come from

![[_attachments/lcb60-tier-breakdown.png]]

Easy tier is saturated (everything 20/20) — all differentiation is **medium + hard**.
Flash-AD384-medium tops hard (19/20); Qwen-27B-low tops medium (17/20) and is the speed king.

## Value index (quality × speed)

![[_attachments/lcb60-value-index.png]]

**Qwen-Q5 27B at low effort is the value king** — nearly double the value index of anything else, because it's both near the top in quality AND ~1.6-2x the speed.

## Model notes

- [[Qwen-Q5 27B]] — daily driver, low-effort value king
- [[Flash-Next AD384]] — quality ceiling on the rig (hard tier master)
- [[Unraid Flash-Next]] — 262K ctx edge, lowest quant
- [[Laguna XS-2.1]] — Unraid MoE candidate, fleet-best hard tier + 2.2x decode (not yet conclusive)
- [[Ornith-1.5 35B]] — swe40 tie at 4-5x speed (AMD lane)
- [[Benchmark Methodology]] — harness, budget-correction, how to read these
- [[Bench Suite (~bench)]] — the unattended five-domain suite behind the 2026-09-22 rebench
- [[Hermes Runs — Session Index]] — every run that produced these numbers

## Raw data

- JSON: `~/bench-results/lcb60-*.json` · charts: `~/Documents/Obsidian/assets/`
- Generated via `~/Work/lcb-bench.py` (env-driven: `LCB_API`/`LCB_TAG`/`LCB_MAXTOK`/`LCB_EFFORT`/`LCB_RETRY`)
## Related

- [[Benchmarks]] (category map) · [[Benchmark Methodology]] · [[Bench Suite (~bench)]]
- Per-run pages: [[2026-09-22 Rebench — Coherent Multi-Domain Scoreboard]] (uniform 98-task run)
- Model notes: [[Qwen-Q5 27B]] · [[Flash-Next AD384]] · [[Unraid Flash-Next]] · [[Laguna XS-2.1]] · [[Ornith-1.5 35B]]

## 2026-09-22 13:53 [#metalbench]
**Done:** Built ~/bench — an unattended, five-domain local-LLM bench suite (code, research, terminal, backend, deepswe) with a `triage` gate pack; every verdict is executed, no LLM judge. Plus bench-run.py (crash-resumable runner), campaign.sh + systemd timer (queue-driven, no babysitting), report.py (markdown scoreboard + Obsidian), selftest.py (proves each grader accepts a good answer and rejects a bad one).
**Findings:** 76 tasks total (40 code / 20 research / 7 terminal / 6 backend / 3 deepswe). Params: `bench-run.py --targets <id|all> --packs ... --tag T [--retry]`. Live proof on Flash-Next AD384: first research task 221s (cold 18K-token ingest), every later task ~15s off the prefix cache at 15 t/s decode — the suite reproduces real agent cadence. It solved the backend token-bucket contract task first try. Docker is unusable for grading here (no sudo / not in the docker group) so isolation is scratch-dir + venv, not containers; real SWE-bench/DeepSWE instance harnesses would need a user-run `usermod -aG docker aim`.
**Recommendations:** Run `./campaign.sh --enqueue tag=... targets=... packs=all` for a nightly across the rig, and mirror ~/bench to Unraid for parallel runs once ssh (<lan-ip>:22 and :18006) answers again — it was refusing connections today.

## 2026-09-22 16:37 [#metalbench]
**Done:** Prepared a coherent rebench of every "strong" config on one uniform suite (~/bench, 76 tasks across code/research/terminal/backend/deepswe). Added a 7-target roster, two new systemd units for the Ornith lanes (llama-ornith-23g @8097, llama-ornith-iq2m @8096) wired into llama-switch (`ornith23g`/`ornithiq2`) and its fleet-wide stop list, `expect_model` staleness guard, and a 256-token launch gate. Continuation prompt: ~/bench/CONTINUATION.md.
**Findings:** Both Ornith GGUFs verified loading and answering via CPU-only probes. Their serve flags had to be reconstructed from server logs (n_ctx_slot 131072) because the original launch commands were never saved — the 23G log shows blk.40 nextn/MTP tensors ignored by the Vulkan build, so it effectively ran no-spec at ~61 t/s. Prior scores are cross-harness and not comparable: Qwen-Q5-low LCB 48/60, Flash-Next AD384 LCB 54/60 @16.9 t/s, Ornith-23G swe40 110/112 @61 t/s (LCB never measured), Ornith-IQ2M swe40 107/112 @99 t/s.
**Recommendations:** Run `~/bench/campaign.sh --enqueue ...` for the triage gate first (~1 h for all four local configs), then the full pass overnight. Unraid is still down (ssh refused, :18006 silent) — rebench those two endpoints once it answers.

## 2026-09-23 00:37 [#metalbench]
**Done:** Coherent rebench of all 6 strong configs on the uniform ~/bench suite (98 tasks, 5 domains, executed verdicts). Page: [[2026-09-22 Rebench — Coherent Multi-Domain Scoreboard]].
**Findings:** qwen-low 91% > ornith-23g 89% (60.8 t/s) > qwen-off=flash 88% (flash 2x slower) > ornith-iq2m 86% (97.1 t/s) > laguna 82%. Flash is NOT the quality king on multi-domain work; qwen thinking tax is ~6 checks not 15; laguna swe40 anomaly was an artifact. Deepswe 0/6 universal wall; terminal separates configs (qwen 45% vs laguna 0%).
**Files:** ~/bench/results/rebench-*.json + .md; selftest 0 failures; bench_lib kit_tree ref bug fixed (triage pack crashed without it).
**Next:** treat deepswe as uninformative until diff grader reworked; consider ornith-23g as default daily (quality parity at 2x speed).

## 2026-10-05 17:47
**Done:** Researched Flash-Next ecosystem as of 2026-10-05: new variants, quants, and runtimes.
**Findings:** (1) ISTA-DASLab GSQ-RCO Coder (Sep 28): 50% of experts pruned, code-calibrated; 58.4 GB total / 29.6 GB resident; SWE-bench 75.6 (91.3% of BF16 base 82.8), LCB v6 98.7% retained. Best shot at beating the 27B Q5 on SWE — roughly half the expert bytes/token vs IQ3_XXS, so ~2x decode expected. Weak spot: multi-step agentic (pruning hurts sustained trajectories most). (2) Strata v0.1.34-0.1.39 (Oct 2-4): decode +6%, 32K prompts +18.5%, 243K attention +26% on RTX 3060, --remote-expert-opt for multi-GPU (dual-4090 +63-132%), Responses API for Codex. Rig install (Sep 29) predates all of these. (3) flashrt engine: 2.6-3.4x over llama.cpp but requires sm_90+ — dead on sm_86 3060s. (4) IQ3_S 3.50bpw unpruned added; worse RAM fit on 61 GB. Swift-1.5 finetune exists but gated.
**Recommendations:** Update Strata to 0.1.39, download the Coder, run swe40 A/B vs 27B at 3k budget.

## 2026-10-05 17:48
**Done:** Deep-dive on GSQ-RCO Coder substantiation (HF discussions #6/#14/#16/#19) — corrects the previous note's recommendation.
**Findings:** Coder's card numbers are self-reported and not reproduced. Rigorous independent check (apollo-mg, paired vs unpruned IQ3_XXS): HumanEval+ holds (93.3 vs 93.9) but factual probes collapse 63.3%->32.9% correct with wrong-share 14%->52% and 0% refusals — confidently wrong, a general property of expert pruning. Community: shallower CoT than full IQ3_S, only ~1.5x Strata speed (not 2x), one user got zero SWE-bench tasks done (loops), CJK broken. Verdict: not fit for thorough/logical work; prior disappointment justified.
**Recommendations:** Stay on 27B Q5 for SWE. Free win remains Strata 0.1.39 update (speed only, won't flip quality verdict). Flash beats 27B only with more fast RAM or an sm_90+ card (flashrt class).

## 2026-10-05 17:49
**Done:** Re-framed the Flash-vs-27B question for the user's actual working regime: 80-180K context SWE tasks.
**Findings:** User's own longctx data: 27B Q5 at 180K runs the no-spec q5_1-KV fallback (MTP cannot fit at 256K) — TTFT 654s cold, decode 8.5 t/s; 120K no-spec 215s/10.5. Flash IQ3_XXS on Strata: 262K native, 40K TTFT 29s warm (~1400 t/s), ~48 t/s decode shallow; Strata 0.1.39 adds +18.5% at 32K prompts and +26% attention at 243K on a 3060. Flash's cost (expert streaming) is context-independent; the 27B's cost (attention/KV at depth) scales with context — long tasks tilt toward Flash. But quality at depth is unmeasured on all local instruments; every existing verdict is shallow-context.
**Recommendations:** Long-context A/B: 8-10 swe40-style tasks embedded in 80K/150K realistic filler, 27B no-spec vs Flash on Strata 0.1.39, same checks. Outcome decides a depth-split daily driver vs context-hygiene approach.

## 2026-10-05 17:55
**Done:** Hypothetical analysis: swapping one 3060 12GB for Tesla V100 32GB on the Flash-Next lane.
**Findings:** Prefill is CPU-MoE-GEMM-bound (~2.1 TFLOPS on 7950X) — V100 tensor compute nearly irrelevant. Decode is expert-cache-miss-bound; 32GB buys ~20GB expert-cache slots (~+0.3% decode per +1% slots per flashrt data) = est. 1.2-1.4x decode, plus long-context headroom (f16 KV at 180K+, MTP at 262K on rig — removes the q5_1 no-spec fallback). Caveats: Volta is experimental-tier in Strata (CUDA 12.9 engine only), llama.cpp sm_70 EOL; card must sit in the x16 slot (x4 slot throttles miss streaming); passive cooling needs shrouding. Used 3090/4090 24GB gives same cache/KV wins on first-class sm_86/89 + faster attention.
**Recommendations:** Try Strata 0.1.39 multi-GPU opts on the existing dual 3060 first; only buy if V100 is far cheaper than a used 3090.

## 2026-10-05 18:01
**Done:** Power-neutral speedup options for the Flash-Next CPU-MoE lane, plus model-worthiness triage.
**Findings:** Wall is CPU GEMM, not RAM bandwidth. Power-neutral levers: Curve Optimizer undervolt (best single lever, ~high-single-digit %), single-CCD pinning test (dual-CCD 7950X, could go either way), THP (auto in Strata 0.1.39), STRATA_IQ256_GATHER=1, RAM subtiming/tRFC tuning at stock volts. ub/t16/ngram already optimal per Sep 28 audit. Model triage: only GSQ-RCO IQ3_S (3.5bpw, ~95GB, quality-up at speed cost — test at 80-180K depth) and gated Swift-1.5 finetune worth testing; skip Coder (debunked), IQ2 sizes, UD-IQ4_XS (RAM-walled), abliterated forks.
**Recommendations:** Strata 0.1.39 + undervolt + CCD test first; IQ3_S long-context A/B second.

## 2026-10-05 18:18
**Done:** Comparative estimate: V100 32GB impact on the dense 27B lane vs the Flash MoE lane.
**Findings:** 27B gains far more: decode is HBM-bandwidth-bound (19.3GB/token; 900 vs 360 GB/s = est. 55-75 t/s vs 27.7), prefill is tensor-compute-bound (125 vs ~51 TFLOPS = est. 1000-1200 t/s vs 590; 180K TTFT 654s -> ~260-300s), and the -ts 15,11 PCIe layer split disappears (19.3GB + f16 KV fits one card; audit showed split rebalancing alone was worth 2x prefill). Est. 98-suite wall 57 -> ~25-30 min. Flash lane only gains cache-hit rate (1.2-1.4x). Caveats: Vulkan path likely fine (daily lane is Vulkan), CUDA sm_70 aging; passive cooling needs shroud; 250W vs 170W cap.
**Recommendations:** If buying, the card helps the 27B daily lane decisively; keep 3060s installed until V100 proves out on Vulkan.

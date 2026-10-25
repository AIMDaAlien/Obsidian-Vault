---
type: project-showcase
topic: Strata V100 optimization
category: Benchmarks
created: 2026-10-19
updated: 2026-10-19
tags: [strata, benchmarks, optimization, v100, volta, showcase, gpu, local-ai]
publish: true
machine: bigrig
title: "Strata on the Tesla V100: optimization showcase"
---
# Strata on the Tesla V100: optimization showcase

**Category:** [[Benchmarks]] · **Vault:** [[Vault Map]]

**One day of paired A/B tuning on one card, same model, same context.** Qwen3.8-Flash-Next (GSQ-RCO IQ3_S, 196,608 context) served by UnbiasedStrata on a Tesla V100-PCIe-32GB with a Ryzen 7950X and 64 GB: short-prompt decode **67 → 90 tok/s**, decode after an 80K prompt **61 → 91 tok/s**, 80K prefill **873 → 1,284 tok/s**, an 80K request **95 → 65 s**, the frozen 24-task coding suite's median **37.2 → 29.6 s**, with the vision encoder loaded, idle CPU power down 85 → 59 W and the CPU under load at 66 °C instead of its 85 °C limit.

![[strata-v100-tuning-20261018/headline.png]]

**Visual report:** https://claude.ai/artifact/Ty3FTvucy1Pppx4VRPP6Qg · **Working dashboard (every dataset):** https://claude.ai/artifact/SVHuTwEfnSbhAVHd55oTzp · **Code and record:** https://github.com/AIMDaAlien/UnbiasedStrata-V100 (`docs/V100_TUNING.md`) · **Full lab note:** [[Strata V100 tuning — 2026-10-18]]

## Result at a glance

| Evidence | Result | Status |
|---|---|---|
| Paired A/B, 80K fixture with planted secrets, two rounds per candidate | every adopted change repeats across rounds; secrets 2/2 on every adopted configuration | Adopted |
| Frozen 24-task DeepSWE2 suite (seed 40, medium reasoning) | median task wall **37.2 → 29.6 s**, passes 22/24 → 23/24, decode inside tasks 77 → 92 tok/s | Accepted |
| 180K soak at the final 135 W cap, five back-to-back prefills with the cache defeated | 13 min under load, secrets 5/5, no watchdog stop, GPU 59 °C, CPU 66 °C, peak transient 229 W | Passed |
| CPU boost cap 4.5 GHz | engine unchanged (88 vs 88 tok/s after 80K), CPU energy per token −31%, Tctl 86 → 64 °C | Adopted |
| Kernel changes (identity IOMMU, NMI watchdog off) | every engine number within 1% before and after the reboot | No effect, kept for cleanliness |

## What changed

Seven rounds, each a window with production stopped and every candidate measured against the current production configuration. In order of effect:

1. **GPU power cap 100 → 125 → 135 W.** The prompt path is power-bound: prefill is +28% at 125 W and +15% more at 135 W on a 180K prompt. Locked clocks and clock ceilings never helped at any cap. 135 W was soaked before adoption; 150 W was left alone because the load-burst transients (not the clock) already reach 229 W on a PC that has lost power under GPU load.
2. **Engine 0.1.39 → 0.1.43.1 with the Volta decode table and the async adaptive expert cache.** Decode 74 → 81 tok/s on the table alone; the async tier adds 6 to 9% more and passed the task suite. 0.1.44+ was avoided for an upstream-reported decode regression.
3. **Upstream PR 1401's Volta prompt kernels** (FP16 tensor cores), merged against their true base and parity-tested: +1.3% prefill, repeatable; far below the author's +10% because the card is power-bound at this cap.
4. **CPU boost cap at 4.5 GHz.** Prefill is one user-space core on the host side of the GPU pipeline; above 4.5 GHz the clock is off the critical path. The cap closed the cooling problem without new hardware.
5. **Vision** through the model's own encoder (Q8_0 requantization, 2048 image tokens, GPU helper) for 3 to 6% decode.
6. **Governor:** power-profiles-daemon had pinned a performance profile; balanced takes idle CPU from 85 to 59 W.

![[strata-v100-tuning-20261018/cpu-cap.png]]

## Whole-task evidence

![[strata-v100-tuning-20261018/tasks-ab.png]]

The suite measures the whole request (first token, generation, correctness), not decode alone. One task flips each way between the runs; both are known to vary between repeats.

## What was rejected, and why it matters

- Locked SM clocks and clock ceilings: cost decode, do not clip transients.
- Resident-biased routing: +7% decode per token but 22/24 passes and longer answers, so slower tasks.
- Pinning the engine to one chiplet: −7% after long prompts; the expert streaming path wants both L3 caches.
- Worker count beyond 12, draft lengths other than 4, a 64K KV window, two Volta decode opt-ins, serving the shards from a second SSD: all inside run-to-run noise.
- Huge pages were already on, suffix drafting already default, and the hybrid 4-bit KV cache cannot stream.

The rejected list is what makes the adopted list credible: the same harness, the same gates, and a verdict either way.

## Method

One GPU job at a time under a thermal and power watchdog; the fork's harness samples GPU power, clocks and temperature per second and CPU energy from RAPL, parses the engine log, and gates every long request on planted secrets returning verbatim. Candidates that change answers go through the task suite before adoption. Each window is one script, launched once (a lesson from two queued jobs that waited on their own command line for two hours).

## Source, licence

The code and the full record live in the fork https://github.com/AIMDaAlien/UnbiasedStrata-V100 (default branch `v100-pr1401`), MIT as upstream: the engine is Niko1221 and the Strata contributors' work, the base is Robert Karl's UnbiasedStrata, the Volta kernels are their PR authors'; the V100 additions are released under the same licence. The lab note with every round's table is [[Strata V100 tuning — 2026-10-18]]; the bench index is [[Strata Bench]].

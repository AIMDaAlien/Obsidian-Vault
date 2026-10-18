---
type: note
category: Rig & Hardware
tags: [omarchy, rig-hardware]
updated: 2026-10-17
publish: true
created: 2026-10-13
machine: bigrig
title: "Maya V100 preflight and Qwen fallback — 2026-10-13"
---

# Maya V100 preflight and Qwen fallback — 2026-10-13
> [!warning] Correction (2026-10-17)
> This note says the main Maya optimization objective remains blocked at V100 build compatibility. The next day's matched six-task comparison ended the project instead: Maya S solved 2 of 6 tasks in 20 min 5 s versus 6 of 6 in 3 min 53 s for Qwen3.8-Flash-Next, so Maya was discontinued for coding work and its model files and project software were deleted. See [[V100 coding-model comparison — 2026-10-14]].


Maya's requested pristine `sm_70` baseline cannot be built from the pinned source. CMake rejects compute capability 7.0 and requires 7.5 or newer. **Optimization and the 144-answer Maya coding campaign did not run.** This is a build compatibility rejection, not evidence of incorrect answers, excessive memory use, or poor inference speed.

The local Qwen fallback contains four configurations from the frozen contract-v2 suite, 24 tasks and seeds 40–42 per configuration: 12 repeats and 288 task records. Production Strata remains the default and passed its health check at 2026-10-13T21:17:25.176721-04:00.

## Build evidence and pins

- Maya source: `1e225b983262c1dc3efc3640874261391436d470` from [project-maya](https://github.com/mw00/project-maya/tree/1e225b983262c1dc3efc3640874261391436d470). Clean detached checkout; `git fsck --full` passed. Per-file source SHA256 hashes are exported.
- Requested build: isolated CUDA 12.9 and GCC 14, Release, CUDA architecture 70, tests enabled. `build-pristine.sh` reproduces the nonzero configuration exit. `CMakeLists.txt:76–81` is the architecture gate. `evidence/maya/configure-sm70.log` contains the failure.
- S means the current upstream `Maya-S-v2-IQ2_XXS` offering. S and S24 model metadata are pinned to `f16ee4ba50d8fd2bb726ea1862ca6ca14ba188da` in `peasantsmith/GLM-5.3-Flash-Maya-GGUF`; all three GGUF shard names and remote LFS SHA256 values per quant are recorded in `maya-pins.json`. **Weights were not downloaded, so local model checksums were not verified.** No executable could consume them.
- No compatibility or performance patch was applied. `maya.patch` is empty. No pristine executable exists; the pristine checkout and failed build directory are retained in `~/Work/maya-v100-20261013`.

The plan permits source changes only after a runnable baseline identifies a stage consuming at least 20% of inference time. Removing the architecture guard alone would not establish kernel correctness on Volta. A separate V100 compatibility port and parity validation are required before the planned measured optimization can proceed.

## Matched Qwen observations

| Configuration | Mean complete tasks | Median complete response | Median generation tokens/s |
|---|---:|---:|---:|
| RTX 3060 Swift Qwen3.8 27B Q5_K_M | 21.00/24 | 80.95 s | 28.95 |
| RTX 3060 Qwen3.8 Flash Next GSQ-RCO IQ3_XXS | 22.67/24 | 66.55 s | 42.50 |
| V100 Swift Qwen3.8 27B Q8_0 | 21.00/24 | 44.20 s | 51.95 |
| V100 Qwen3.8 Flash Next GSQ-RCO IQ3_S | 23.00/24 | 34.90 s | 77.60 |

All plotted runs used **Medium reasoning**, temperature zero, the same contract-v2 task/checker hashes, prompt hashes and token/escalation budgets. Maya was planned for High reasoning; there are no Maya points to compare across policies. The RTX 3060 Swift configuration uses llama.cpp Vulkan devices 1+2 with layer split 16:11; its result represents that existing rig configuration. V100 Swift uses llama.cpp CUDA; Flash uses Strata CUDA. All commands, context lengths, model quantization and original engine/model provenance are preserved in copied manifests.

Complete response time sums API wall time over all attempts for each task; it excludes startup and checker execution. The chart's generation speed is the recorded final-attempt decode rate and does not include escalation cost. Aggregate latency and speed are medians over 72 task/repeat observations per configuration; quality is the mean complete-task pass fraction. Small crosses show the three repeats. Error bars use 10,000 deterministic task-cluster bootstrap resamples, preserving all three repeats of each task. Empirical Pareto membership uses aggregate values and does not establish statistical dominance. V100 Flash is the sole empirical frontier point in both charts.

Existing grades were reused. The V100 full regrade evidence covers 144 answers and all agree. The copied RTX subset audits cover 20 answers and all agree; this export does not claim a new full RTX regrade. Historical incompatible suites and upstream speed claims are excluded.

![[_attachments/maya-v100-20261013/quality-vs-response_s.png]]

![[_attachments/maya-v100-20261013/quality-vs-generation_tokens_s.png]]

## Memory and paging

| Variant | Requested process cap | Requested expert RAM | Workload swap policy | Measured peak / paging |
|---|---:|---:|---|---|
| Maya S | 56 GiB | 40 GiB | `MemorySwapMax=0` | Unmeasured; no workload launched |
| Maya S24 | 56 GiB | 40 GiB | `MemorySwapMax=0` | Unmeasured; no workload launched |
| Maya approximate | 56 GiB | 40 GiB | `MemorySwapMax=0` | Unmeasured; no primary selected |
| Historical V100 Flash | See original manifest | Existing configuration | Final snapshots show zero swap | Max recorded cgroup peak 56.00 GiB; no new paging measurement |
| Historical V100 Swift | See original manifest | Dense model | Final snapshots show zero swap | Max recorded cgroup peak 36.27 GiB; no new paging measurement |
| Historical RTX configurations | See original manifest | Existing configuration | No new verification | No final cgroup snapshots in campaign manifest |

The Maya caps were **planned, not applied**, since no Maya workload started. Expert paging remains authorized, but workload swap is prohibited for a future run. Historical cgroup memory peaks can include file cache; final zero swap snapshots alone do not demonstrate zero swap throughout a run. The original V100 validation evidence remains authoritative for those historical checks.

## Unexecuted gates

There are no 8K/32K diagnostic baselines, startup/prefill/decode measurements, expert-tier hits, NVMe/PCIe/kernel profiles, calibrations or alternating tuning pairs. No gain met the 5% acceptance threshold because no gain was measured. A baseline-versus-optimized timing chart cannot be produced without inventing data.

No S/S24 selection was made. The approximate settings `STRATA_GLM_DISK_SKIP_W=0.12` and `STRATA_GLM_DISK_SKIP_FROM=8` would alter model computation and require independent validation; neither was run. Primary settings would retain all main routed experts, disable disk skipping and retain `TRUNK_KEEP=8`. Skipped-expert counts, paging savings and approximate quality deltas remain unknown.

The 126,976-input plus 4,096-reserved-output 131,072-token context gate was not tested. No labeled 32K coding trial was started. Zero Maya answers were generated or graded, so task wins/losses and bootstrap quality differences against Flash are unavailable. No adoption decision is made.

## Reproduction and final state

`chart-data.json`, `task-data.csv`, `aggregates.csv`, `input-sha256.json`, original manifests/answers/available regrades, source and model pins, memory evidence and failed-build logs are in `assets/maya-v100-20261013/`. `export.py` reproduces the charts from preserved original local result paths; its copied inputs permit relocation by adjusting `SOURCES`. The Python dependency versions are in `python-dependencies.txt`. `artifact-sha256.json` verifies the final package.

Run `~/Work/maya-v100-20261013/.venv/bin/python ~/Work/maya-v100-20261013/export.py` to regenerate. `build-pristine.sh` re-runs only the isolated build. Neither script changes production services.

No trial servers started; none remain. The existing `unbiasedstrata.service` stayed active and healthy throughout this session; no restoration was needed. No Qwen weights, launcher defaults, drivers or historical evidence were changed. Artifacts were copied only into the local Obsidian vault; nothing was externally published. The main Maya optimization objective remains blocked at V100 build compatibility. (superseded, see Correction above)

---
type: benchmark-results
category: Benchmarks
tags: [omarchy, benchmarks, v100, gpu, local-ai]
updated: 2026-10-14
publish: true
created: 2026-10-14
machine: bigrig
title: "V100 coding-model comparison — 2026-10-14"
featured: 44
summary: "We tested a rival AI on the same coding tasks: it took 5x longer and solved a third as many, so we stopped the project."
---

# V100 coding-model comparison — 2026-10-14

## Decision

Stop the Maya S (GLM-5.3 Flash) project for coding work. In the matched tasks below, Qwen3.8-Flash-Next solved more tasks and finished much sooner. Maya's model files and project software were removed from this computer after the comparison; Qwen remains available.

## What we tested

We gave both models the same first six tasks from a standard set of 24 coding tasks. A task counted as solved only when the submitted code passed that task's checks.

| Model | Tasks solved | Time for these six tasks |
|---|---:|---:|
| Qwen3.8-Flash-Next | 6 of 6 | 3 min 53 sec |
| Maya S (GLM-5.3 Flash) | 2 of 6 | 20 min 5 sec |

Maya took about **5.2 times longer**, yet solved **four fewer tasks**. It showed no quality improvement that could justify the extra time.

## How to read this result

We stopped before all 24 tasks because Maya was already behind on both success and time. This is an early-stop comparison, not a full 24-task score. It was enough to make the project decision: keep Qwen for this coding workload and discontinue Maya.

A separate Maya correctness check had already found a mismatch and was marked **STOP**. This coding comparison does not resolve that issue or change the earlier result.

## Cleanup

The Maya model weights, packed model copies, source/build workspace, and temporary benchmark helper were removed. Qwen3.8-Flash-Next was checked after cleanup and is healthy at the existing 100 W GPU limit.

Detailed six-task measurements are preserved in [the result record](../../_attachments/v100-coding-model-comparison-20261014/deepswe2-six-task-result.json). Existing Qwen reference charts and data are in the same [evidence folder](../../_attachments/v100-coding-model-comparison-20261014/).

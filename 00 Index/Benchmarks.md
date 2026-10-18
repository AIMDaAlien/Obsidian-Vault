---
type: moc
category: Meta
tags: [meta, moc, benchmark]
updated: 2026-10-12
publish: true
created: 2026-10-12
machine: bigrig
title: "Benchmarks"
---
# Benchmarks

The measurement layer: how it is done, what it scored, and every raw result page.

**Vault:** [[Vault Map]]

## 2026-10-12 — Corrected matched DeepSWE2 comparison

[[2026-10-12 Matched Qwen 27B vs Flash DeepSWE2]] — six complete campaigns, 144 audited results over 24 distinct synthetic repository tasks. Flash averaged **22.67/24** versus Qwen **21.00/24**; the task-bootstrap interval for the +1.67 Flash delta is **[-2.33, +5.67]**, including zero. The historical 27B advantage was not observed on this corrected suite. The note embeds delta and capability/latency charts, with [[2026-10-12 Matched Qwen vs Flash — Methods and artifacts|full methods, provenance and all archived supporting files]].


## Core

- [[Model Benchmarks]] — **the hub**: Pareto chart, LCB-60 scoreboard, value index, current verdicts.
- [[Benchmark Methodology]] — LCB-60, budget correction, reasoning-effort rules, the multi-domain suite, how to read the numbers. Read this before quoting a score.
- [[Bench Suite (~bench)]] — the unattended 76-task five-domain suite: pack shape, commands, known walls (deepswe is a universal 0/6).
- [[Model Benchmarks Archive]] — legacy flat log, verbatim.

## Per-run pages (`Model Benchmarks/`)

- [[2026-09-22 Rebench — Coherent Multi-Domain Scoreboard]] — the uniform 98-task run across all 6 strong configs (the comparison that overturned "Flash = quality king").
- [[ReBench rebench-qwenq5-low]] · [[ReBench rebench-qwenq5-off]] · [[ReBench rebench-flash-ad384]] · [[ReBench rebench-ornith-23g]] · [[ReBench rebench-ornith-iq2m]] · [[ReBench rebench-laguna]]

## Relevance

Benchmarks are the **evidence layer** for claims made in [[Models & Serving]] and [[Rig & Hardware]] — hard-tier confusion, the thinking tax, unsupported quant-fit answers. Route decisions in [[RAFT Laya Router]] use the same tier vocabulary. Native raw data stays in `~/bench-results/` and `~/bench/results/`. The 2026-10-12 matched DeepSWE2 comparison also has a complete supporting-artifact snapshot in this vault, linked from its findings and methods notes.

---
type: index
topic: Hermes session history
updated: 2026-09-23
category: Meta
tags: [meta, sessions, index]
publish: true
created: 2026-09-23
machine: bigrig
title: "Hermes Runs — Session Index"
---
# Hermes Runs — Session Index

**Category:** [[Vault Map]] · **Vault:** [[Vault Map]]

Every substantive Hermes run on this rig (2026-09-15 → 09-23) and where its high-value output now lives.
Trivial sessions (the "Say OK" / greeting probes, ~25 of them, all `.hermes` workspace) are omitted — no content.

| Date | Session | What it was | Documented in |
|---|---|---|---|
| 09-15 | `20260915_131957_48b075` | Omarchy rig build-out + Swift-Qwen3.8-27B dual-GPU serving + benchmark matrix | [[Rig Hardware & Display]], [[Qwen3.8 Rig]] |
| 09-16 | `bg_231939_21a1f2` | Dual Tesla P100 vs 2nd 9060 XT advisory | [[Dual Tesla P100 vs 2nd 9060 XT]] |
| 09-16 | `20260916_103113_4d80d1` | Hermes install: git 0.21.3 shadowed by mise/pipx 0.19 | [[Hermes Install & Config Port]] |
| 09-16 | `20260916_105126_532ed0` | Mac config/skill port, full-yolo approvals, 32 GB OOM ceiling | [[Hermes Install & Config Port]] |
| 09-16 | `20260916_113452_8d045a` | Omarchy debloat → minimal local-LLM dev box, trims, auto-update | [[Omarchy Trim Debloat & Idle Policy]] |
| 09-16 | `20260916_115203_f3c47a` | llama-server SIGABRT → i915 hang, iGPU in the Vulkan path | [[GPU Crash & Vulkan Device Pinning]] |
| 09-16 | `20260916_130812_861789` | Menubar metrics widget for llama-server + system | [[Omarchy Plugins & Shell Widgets]] |
| 09-18 | `20260918_100718_5c524c` | Ornith-1.5 35B quant fit, 3-way bench, token-budget artifact lesson | [[Ornith-1.5 35B]], [[Benchmark Methodology]] |
| 09-18 | `20260918_201600_79ed39` | Knowledge-garden pipeline + Omarchy idle/screensaver policy | [[Knowledge Garden]], [[Omarchy Trim Debloat & Idle Policy]] |
| 09-19 | `20260919_110953_2e37ea` | Swarm Dashboard plan (one window for all agents) | [[Swarm Dashboard]] |
| 09-19 | `20260919_131616_6be4c3` | Unraid Flash-Next: llama.cpp rebuild, LiveCodeBench harness, AD384 on the rig | [[Unraid LLM Control Center]], [[Unraid Flash-Next]], [[Flash-Next AD384]] |
| 09-19 | `20260919_214302_a59ad9` | Browser debloat + Chromium/Helium/Zen RSS benchmark | [[Browser Debloat & Benchmark 2026-09-19]] |
| 09-19 | `20260919_225210_7f89a2` | DeepSeek Harness install, OpenRouter wiring, sandbox EROFS fix | [[DeepSeek Harness Setup]] |
| 09-19 | `20260919_235747_919ecc` | Local Swift-Qwen added as a dsh endpoint | [[DeepSeek Harness Setup]] |
| 09-20 | `20260920_205428_5989aa` | Obsidian as a system, not just notes | [[Knowledge Garden]] |
| 09-20 | `20260920_200914_24da34` | Post-crash resume, reasoning-effort sweep, Pareto chart, vault restructure | [[Model Benchmarks]], [[Benchmark Methodology]] |
| 09-21 | `20260921_100718_4f0ed7` | Laguna XS-2.1 swap on Unraid + thinking-policy bench war | [[Laguna XS-2.1]], [[Unraid LLM Control Center]] |
| 09-21 | `20260921_172710_6e3c0f` | 17 Omarchy community plugins installed | [[Omarchy Plugins & Shell Widgets]] |
| 09-21 | `20260921_224455_6effb4` | llama.cpp throughput upgrade path (rig + Unraid) | [[llama.cpp Upgrade Roadmap]] |
| 09-21 | `20260921_230536_8e4d5d` | Chassis fan curve control — blocked on `acpi_enforce_resources=lax` | [[Fan Control (MSI Z690-A)]] |
| 09-22 | `20260922_094114_4d6369` | llama-switch center-bar plugin → data-driven fleet catalog | [[Omarchy Plugins & Shell Widgets]] |
| 09-22 | `20260922_105413_dbfdb0` | Laya (System-1) RAFT router POC + Flash-Next 128K proof | [[RAFT Laya Router]] |
| 09-22 | `20260922_130727_0449f4` | RAFT calibration (T=0.5, ECE 0.111), threshold policy, cost measure | [[RAFT Laya Router]] |
| 09-22 | `20260922_131012_123c12` | `~/bench` unattended five-domain suite + strong-config roster | [[Bench Suite (~bench)]] |
| 09-22 | `20260922_142127_38bc2c` | Raspberry Pi B+ verdict + Cactus Needle 3 | [[Raspberry Pi B+ Utility Node]] |
| 09-22 | `20260922_164328_688903` | Overnight rebench of 6 configs, uniform 98-task suite | [[Model Benchmarks]] |
| 09-22 | `20260922_202801_615c2b` | Desktop session persistence (Hyprland/tmux) after abrupt crashes | [[Desktop Session Persistence]] |
| 09-23 | `20260923_101809_7cef75` | This documentation pass | this note |

## Non-benchmark work threads

- **Rig / OS**: [[Rig Hardware & Display]], [[Omarchy Trim Debloat & Idle Policy]], [[Omarchy Plugins & Shell Widgets]], [[Desktop Session Persistence]], [[Fan Control (MSI Z690-A)]], [[GPU Crash & Vulkan Device Pinning]]
- **Agents / tooling**: [[Hermes Install & Config Port]], [[DeepSeek Harness Setup]], [[Swarm Dashboard]], [[RAFT Laya Router]]
- **Serving**: [[Qwen3.8 Rig]], [[Unraid LLM Control Center]], [[llama.cpp Upgrade Roadmap]]
- **Benchmarks**: [[Model Benchmarks]] (hub), [[Benchmark Methodology]], [[Bench Suite (~bench)]], and the per-model notes

## Older / other artifacts

- Navigation & theme work on the user's web app: [[Navigation & Theme System Enhancement]], [[Navigation & Theme System Enhancement - Final]]
- Legacy flat log preserved verbatim: [[Model Benchmarks Archive]]

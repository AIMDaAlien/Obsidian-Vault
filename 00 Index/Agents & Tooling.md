---
type: moc
category: Meta
tags: [meta, moc, agents, tooling]
updated: 2026-10-26
publish: true
created: 2026-09-23
machine: bigrig
title: "Agents & Tooling"
---
# Agents & Tooling

The agent layer: Hermes, opencode, dsh, the swarm view, and routing.

**Vault:** [[Vault Map]]

## Notes

- [[Hermes Install & Config Port]] — git install vs mise/pipx shim, mac→Linux config/skill port, **full-yolo approvals** + the guardrails never to disable, the 32 GB OOM ceiling.
- [[DeepSeek Harness Setup]] — dsh on `:3080`, OpenRouter + local routes, the required dummy credential, and the **EROFS sandbox misdiagnosis** (`DSH_PERMISSION_MODE=danger-full-access`).
- [[Swarm Dashboard]] — one stdlib TUI for all live Hermes/opencode instances (aggregator + Catppuccin TUI, <40 MB RSS).
- [[Clickable File Paths in the Terminal]]: agents are told to print full paths, and Ctrl+click on any path in their output shows the file in the file manager or opens the note in Obsidian.
- [[Clop for Linux]]: `clop drag FILE` hands a file an agent produced to the user as a card they can drag into a browser or chat (terminals can't drag files); the global agent instructions tell agents to use it.
- [[RAFT Laya Router]] — Laya 421M System-1 decider in front of the model tiers: 40-task labels, T=0.5 calibration (ECE 0.216 → 0.111), act@conf≥0.6 policy, cost measurement.

## Relevance

These tools all point at the same endpoints defined in [[Models & Serving]]; the router in [[RAFT Laya Router]] picks between them. The dashboard reads live state from the desktop/session layer ([[Desktop Session Persistence]]) and is displayed through the bar ([[Omarchy Plugins & Shell Widgets]]). Routing quality is bounded by how well models actually perform — see [[Benchmarks]]. RAFT's act/show/refuse confidence gate is the same philosophy as Cactus Needle 3 in [[Raspberry Pi B+ Utility Node]].

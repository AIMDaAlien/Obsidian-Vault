---
type: benchmark-log
topic: Knowledge Garden
category: Meta
tags: [meta, vault, logging, obsidian]
publish: true
created: 2026-09-23
machine: bigrig
title: "Knowledge Garden"
---
# Knowledge Garden

**Vault:** [[Vault Map]]


## Related

- [[Vault Map]] — category maps over this vault · [[Hermes Runs — Session Index]] — run history
- Producing runs: [[Omarchy & Desktop]] · [[Benchmarks]]

## 2026-09-19 14:26
**Done:** built auto-logging pipeline: ~/Documents/Obsidian vault, bench-note logger, Hermes skill "knowledge-garden", opencode global instruction file.
**Findings:** logger tested end-to-end; opencode config validated; rule wired via instructions key (AGENTS.md write blocked without approval).
**Recommendations:** vault merges to Unraid with Mac vault later; publish to portfolio.penthouse.blog/knowledge-garden.

## 2026-09-19 14:26
**Done:** moved all notes to vault root; logger now writes topics directly to ~/Documents/Obsidian/.
**Findings:** Benchmarking/ subdir dropped since scope widened to all work, not just benchmarks.

## 2026-09-23 10:30
**Done:** Documented 28 past Hermes runs into the vault: 13 new notes (Rig Hardware and Display, Dual Tesla P100 vs 2nd 9060 XT, Hermes Install and Config Port, GPU Crash and Vulkan Device Pinning, Omarchy Trim Debloat and Idle Policy, Omarchy Plugins and Shell Widgets, DeepSeek Harness Setup, Fan Control, Desktop Session Persistence, Raspberry Pi B+ Utility Node, llama.cpp Upgrade Roadmap, Unraid LLM Control Center, Bench Suite) plus a new index note "Hermes Runs — Session Index"; patched Qwen3.8 Rig, Flash-Next AD384, Model Benchmarks, Benchmark Methodology.
**Findings:** 65 sessions in state.db, ~25 were "Say OK" probes with no content; 26 substantive ones mined. Most bench work was already logged — the undocumented high-value material was rig hardware/display limits, the iGPU-caused SIGABRT, Omarchy trim/plugin/shell details, dsh sandbox EROFS, Unraid control-center mechanics, and the blocked fan-control path.
**Recommendations:** Fan control is blocked on one reboot with acpi_enforce_resources=lax; see the session index for the full map.

## 2026-09-23 10:47
**Done:** Wired the vault into six categories plus a top-level map. New MOC notes: Vault Map, Rig and Hardware, Omarchy and Desktop, Models and Serving, Benchmarks, Agents and Tooling, Web App. Every one of the 43 notes now carries category + tags frontmatter and a Category/Vault line under the H1; 13 notes gained a curated Related section (model siblings, host mechanics, method notes). Added the categorization convention to the knowledge-garden skill and taught bench/report.py to emit the frontmatter so regenerated rebench pages keep it.
**Findings:** Link check across all 43 notes: 0 broken wikilinks (incl. heading anchors). Notes stay at vault root on purpose — bench-note writes new topics there, so moving them into folders would create duplicates on the next log.
**Recommendations:** Use Vault Map as the entry point; when adding a note, add it to its category map's member list.

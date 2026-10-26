---
type: moc
category: Meta
tags: [meta, moc, index, obsidian]
updated: 2026-10-26
publish: true
created: 2026-09-23
machine: bigrig
title: "Vault Map"
---
# Vault Map

Top-level map of this vault. Two audiences: the local MASSIVE-RIG setup itself, and the published knowledge garden (portfolio.penthouse.blog/knowledge-garden) / MetalBench.

## Categories

| Map | Covers |
|---|---|
| [[Rig & Hardware]] | the box itself, display, GPU lanes, fans, hardware advisories |
| [[Omarchy & Desktop]] | OS trimming, shell plugins/bar, session persistence, browsers, Clop, clickable file paths |
| [[Models & Serving]] | models on the rig + Unraid, serve flags, deployment changes |
| [[Benchmarks]] | hub, methodology, suite, per-model and per-run results |
| [[Agents & Tooling]] | Hermes, opencode, dsh, swarm dashboard, the RAFT router |
| [[Web App]] | navigation/theme work on the user's own app |

## Start here

- **What the rig is and what it can do** → [[Rig Hardware & Display]] → [[Qwen3.8 Rig]]
- **Which model to reach for** → [[Model Benchmarks]] (hub) → [[Benchmark Methodology]]
- **How it is served / switched** → [[Unraid LLM Control Center]] · [[Omarchy Plugins & Shell Widgets]] (bar switcher)
- **Every past agent run and where its output lives** → [[Hermes Runs — Session Index]]

## Meta

- [[Knowledge Garden]] — the auto-logging pipeline (`bench-note`) that writes most of this vault
- [[Hermes Runs — Session Index]] — run-by-run history 2026-09-15 → today
- [[Model Benchmarks Archive]] — legacy flat log, kept verbatim

## Conventions

- Notes are auto-appended by `~/.local/bin/bench-note` — entries land at the end of a note, timestamped.
- `--tag metalbench` marks rig/benchmark teardown data (`[#metalbench]`) destined for the MetalBench site.
- Every note carries `category:` + `tags:` frontmatter; each links back to its category map and to this map.

## 2026-09-23 10:47
**Done:** Wired the vault into six categories plus a top-level map. New MOC notes: Vault Map, Rig and Hardware, Omarchy and Desktop, Models and Serving, Benchmarks, Agents and Tooling, Web App. Every one of the 43 notes now carries category + tags frontmatter and a Category/Vault line under the H1; 13 notes gained a curated Related section (model siblings, host mechanics, method notes). Added the categorization convention to the knowledge-garden skill and taught bench/report.py to emit the frontmatter so regenerated rebench pages keep it.
**Findings:** Link check across all 43 notes: 0 broken wikilinks (incl. heading anchors). Notes stay at vault root on purpose — bench-note writes new topics there, so moving them into folders would create duplicates on the next log.
**Recommendations:** Use Vault Map as the entry point; when adding a note, add it to its category map's member list.

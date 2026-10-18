---
type: moc
category: Meta
tags: [meta, moc, models, serving]
updated: 2026-10-17
publish: true
created: 2026-09-23
machine: bigrig
title: "Models & Serving"
---
# Models & Serving
> [!warning] Correction (2026-10-17)
> This page lists port 8080 as the Qwen daily model. Later notes put Flash on :8080 ([[Desktop Session Persistence]]) and Strata on :8083 ([[Strata V100 setup and benchmarks — 2026-10-13]]). Port map verified on this machine 2026-10-17 with `ss -ltnp`: :8081 is the Philosopher harness and :8082 the Philosopher bridge; nothing is listening on :8080 or :8083 (the llama-server, llama-server-flash and unbiasedstrata user units are installed but disabled and inactive).


Which models exist, where they run, the exact flags, and how the fleet is switched.

**Vault:** [[Vault Map]]

## Index and hosts

- [[Qwen3.8 Rig]] — the rig's index note: daily driver, file hashes, serving regimes (`llama-switch mtp/deep/split`).
- [[Unraid LLM Control Center]] — the Unraid box (<lan-ip>): roster/compose swap mechanics, `-ncmoe`, `REASONING_BUDGET` override, SSH-is-flaky/API-on-:18080.

## Per-model notes

| Model | Host | Grab it for |
|---|---|---|
| [[Qwen-Q5 27B]] | rig :8080 (daily) | default agent work — best overall on the uniform suite | (superseded, see Correction above)
| [[Flash-Next AD384]] | rig :8080 (on demand) | hard single-domain coding, heavy thinking — slow |
| [[Unraid Flash-Next]] | Unraid :18006 | **262K context only** — lowest quant |
| [[Laguna XS-2.1]] | Unraid :18007 | high-throughput beam, single-shot tasks (weakest multi-domain) |
| [[Ornith-1.5 35B]] | rig AMD lane :8096/:8097 | speed lane (IQ2_M) or best balance (23G-ICE) |

## Change control

- [[llama.cpp Upgrade Roadmap]] — version/PR-level upgrade path for both hosts; do not chase speculative decoding or quant downgrades.
- [[Rig & Hardware]] — serve flags are only safe after reading [[GPU Crash & Vulkan Device Pinning]].

## Relevance

Every number in these notes is produced via [[Benchmarks]]; read [[Benchmark Methodology]] before comparing anything. Client wiring (Hermes/opencode/dsh) lives in [[Agents & Tooling]]. Switching is driven from the desktop by [[Omarchy Plugins & Shell Widgets]].

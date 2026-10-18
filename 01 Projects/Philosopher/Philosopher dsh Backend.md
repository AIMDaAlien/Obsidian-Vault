---
type: benchmark-log
topic: Philosopher dsh Backend
publish: true
created: 2026-10-11
tags: [omarchy]
machine: bigrig
title: "Philosopher dsh Backend"
---
# Philosopher dsh Backend


## 2026-10-08 12:47
**Done:** Proved dsh (DeepSeek Harness) as agent backend for the philosopher stack: Python SDK (deepseek-harness-sdk 0.1.5rc1, bundles full dsh runtime, no system Node) -> dsh sdk profile -> llm-pi-ai provider -> philosopher harness (:8081) -> llama.cpp engine. End-to-end grounded answer, finish_reason=completed.
**Findings:** SDK is stdio JSON-RPC; sessions durable per session_id; provider routes mount via llm-pi-ai in $DSH_HOME/settings.yaml (schema: providers.<name>.{apiKeyEnv, api: openai-completions, baseURL, models}); SDK never touches ~/.dsh. Hardware changed mid-build: RX 9060 XT 16GB already installed beside one RTX 3060 (V100 pending); old 2x3060 engine unit was down since Oct 7 evening — built llama-ornith-interim.service (-dev Vulkan1,Vulkan2 -ts 4,3, ctx 131072, KV q8_0) and restored service. dsh TRANSPORT errors were the harness's httpx upstream error propagating, not dsh networking.
**Recommendations:** Package to Samsung 980 PRO (reformat pending user sudo); bridge = OpenAI-compat FastAPI fronting DeepSeekHarness with per-conversation session_ids; LibreChat points at bridge.

## 2026-10-08 15:03
**Done:** Friend-facing UX fixes on the LibreChat->bridge->dsh->harness chain: (1) modelSpecs with softDefault+showOnLanding+conversation_starters so new users get Philosopher auto-selected with a branded landing screen (modelSpecs also hides modelSelect/parameters/presets = cleaner UI for non-tinkery users); (2) bridge emits placeholder reasoning delta first so LibreChat's thinking panel opens immediately while waiting; (3) raised output cap 4096->16384 in harness MAX_TOKENS_CAP and bridge DEFAULT_MAX_TOKENS — a reasoning channel could eat the whole 4096 budget and starve the answer empty (root cause of dad's "[couldn't give answer]"); (4) explicit max-tokens starvation message instead of bare "[no response produced]".
**Findings:** dsh SDK wire carries only 4 notification types (session.event/status, subagent.*) — no incremental assistant deltas; live token stream is process-local in dsh by design, so through-SDK reasoning arrives committed at turn end. True live reasoning needs the direct harness endpoint or a future dsh plugin. Verified delta order: placeholder(2ch) -> reasoning(452) -> content(179). Samsung 980 PRO now writable (chown done) — migration unblocked.
**Recommendations:** Migrate package to /mnt/samsung/philosopher next; consider a dsh plugin for live reasoning later.

## 2026-10-11 10:34
**Done:** Migrated the full philosopher package to the Samsung 980 PRO (/mnt/samsung/philosopher, 34G): harness, bridge, dsh-home, KB, eval, engine profiles, unit templates, frontends (LibreChat compose moved in, named mongo volume survived the move). Recreated venv on drive (uv, python 3.13); ~/Work/philosopher is now a symlink to the drive. All services run from drive paths with RequiresMountsFor=/mnt/samsung: llama-ornith, philosopher-harness (:8081), philosopher-bridge (:8082), philosopher-mdns, librechat (:8090). Full chain verified post-migration (grounded streamed answer + container->bridge 200).
**Findings:** Gotchas: systemd-run needs explicit --working-directory; FastAPI header params need Header() not bare args; PyPI name is zeroconf not python-zeroconf; dsh TRANSPORT errors were the harness's httpx upstream error propagating (llama-server was down after the GPU swap — RX 9060 XT already installed beside one 3060, V100 pending). Old engine unit replaced by llama-ornith.service (-dev Vulkan1,Vulkan2 -ts 4,3).
**Recommendations:** Free ~71G on NVMe later (~/Work/philosopher.nvme-backup 577M, ~/Models/ornith 33G, ~/Models/philosopher 38G retired Gemma) once confident. V100 profile staged in engine/profiles/cuda-v100-vulkan-9060xt.yml.

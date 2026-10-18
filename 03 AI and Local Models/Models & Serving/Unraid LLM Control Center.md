---
type: ops
topic: Unraid LLM serving
updated: 2026-09-23
category: Models & Serving
tags: [unraid, serving, docker, ops]
publish: true
created: 2026-09-23
machine: bigrig
title: "Unraid LLM Control Center"
---
# Unraid LLM Control Center

**Category:** [[Models & Serving]] · **Vault:** [[Vault Map]]

How models are served and swapped on the Unraid box (<lan-ip>), learned during the Flash-Next → Laguna swap (2026-09-19 → 09-21).

## Access

- `ssh unraid` → root@<lan-ip>, **key auth only**. SSH :22 **resets repeatedly under load** — the reliable control path is the **control-center HTTP API on :18080**.
- No `socat`-style forward needed all the time, but benching from the rig used `socat` forwards (`TCP-LISTEN:18006` → Flash-Next, :18007 → Laguna, :18008 while swapping).

## Box facts

RTX 3060 12 GB + 125 GB RAM (~52 G available after buff/cache). Model dir `/mnt/cache/llm-workspace/models` (→ `/models-extra`), 93 GB free. Flash-Next served as **UD-IQ3_XXS, 177B / 82 GB, 262K ctx on :18006** at ~14.3 t/s, image `local/qwen38-flash-cuda:latest`, llama.cpp 0.4.1-dev `e613ef2`.

## Swapping in a model (the mechanics)

1. Download the GGUF.
2. `docker compose create` a container (e.g. `llm-laguna-xs21`) **from the existing image** — the control center does **not** create containers.
3. Register it in **`roster.yaml`** at `/mnt/cache/appdata/unraid-llm/control-center/roster.yaml`.
4. POST `/api/models/<name>/load` (the API only start/stops pre-existing containers, and `load()` stops all other model containers first).
- **Roster is read at container startup — restart the control-center container after editing it**, or you get "Unknown model".
- Durability: containers are `restart: "no"` and the control center has **no boot autostart** (starts idle, loads on demand) → **nothing auto-starts after an Unraid reboot**.

## Gotchas

- A bind-mounted entrypoint needs `chmod 755` on the host.
- `--gpu-layers 99` on a 20 GB model **OOMs the 12 GB 3060** → use `--gpu-layers 99 -ncmoe 40` (flags `-cmoe/--cpu-moe`, `-ncmoe/--n-cpu-moe N`; qwen38-flash uses `-ncmoe 48`).
- **Compose env `REASONING_BUDGET: "8192"` overrides the entrypoint default `${REASONING_BUDGET:-1024}`** — the env is what actually lands in the process cmdline.
- **"Thinks too much / hangs up" failure mode**: with thinking uncapped the model dumps the whole budget into `reasoning_content`, returns **empty `content`** and never closes its code fence. Cap thinking (`--reasoning-budget 1024`) and it's a different model.
- Rebuild path when needed: `~/opt/llama-b11063`-style prebuilt CUDA binaries; on the rig `docker pull` fails without root.

## Agentic reality check (2026-09-21)

Tool-calling works on Laguna (`run("ls -la")`, `finish_reason=tool_calls`, clean arg JSON) and a clone-and-verify loop succeeded in 3 turns on a trivial repo — but **swe40/LCB measure single-shot codegen, not the multi-turn agentic loop**. Laguna is a good single-shot coder / high-throughput beam for small bounded tasks, **not an app-remake agent** (it "couldn't even clone the repo" in the user's opencode try — unresolved).

## Client wiring

- Hermes: `hermes --provider unraid-laguna -m /models-extra/laguna-xs21/Laguna-XS-2.1-Q4_K_M.gguf` (config.yaml is edit-protected — add via CLI).
- opencode: provider `laguna-unraid` (:18007, tool_call on, 262K/16K limits) as default model + `small_model` + build agent; `qwen38-unraid` kept switchable. Already-running sessions cache the old provider — restart them.

## Related

[[Laguna XS-2.1]] · [[Unraid Flash-Next]] · [[llama.cpp Upgrade Roadmap]] · [[Hermes Install & Config Port]]

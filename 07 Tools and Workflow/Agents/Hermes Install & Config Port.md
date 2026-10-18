---
type: ops
topic: Hermes / opencode configuration
updated: 2026-09-23
category: Agents & Tooling
tags: [hermes, opencode, config, ops]
publish: true
created: 2026-09-23
machine: bigrig
title: "Hermes Install & Config Port"
---
# Hermes Install & Config Port

**Category:** [[Agents & Tooling]] · **Vault:** [[Vault Map]]

How Hermes and opencode got set up on this rig (2026-09-16), and the two traps that cost time.

## Install: git checkout, not pipx

- Correct install = **`~/.hermes/hermes-agent` git checkout** (was 0.21.3), launched by `~/.local/bin/hermes`, updated via git. Recommended Linux method is the git-based shell installer (uv + venv), **not `pip install`**.
- Trap: a **mise-managed pipx shim** for hermes-agent 0.19.0 sat earlier in PATH and silently won resolution, so the stale copy kept running. Fix = remove the pipx hermes-agent from mise, then **prune shims by hand (mise `auto_prune` is off)**.

## Mac → Linux config port

- **51 of 105 skills** copied into `~/.hermes/skills` (116 SKILL.md total). Skipped: apple/* + MLX (mac-only), healthcare/textbook/coursework/resume/job-search/marketing, red-teaming, webwright (redundant), touchdesigner, empty index dirs. Homelab/Unraid set kept.
- `SOUL.md` (caveman mode) installed; old default backed up to `~/.hermes/backups/SOUL.md.pre-caveman`.
- The **mac `config.yaml` was deliberately NOT merged** — it targets mac-local ports (8787/1234/8110) and contained a plaintext secret.
- `~/.config/opencode.json`: providers = local rig llama-server, Unraid Qwen3.8-Flash-Next 176B (262K), OpenRouter DeepSeek; default model changed to the **Unraid 176B**.
- **`~/.hermes/config.yaml` is agent-edit-protected** — add providers via the CLI (`hermes --provider <name> -m <model>`), not by editing the file.

## Approvals / yolo

- Hermes `approvals.mode = off`, destructive-slash confirm off. opencode `"permission": "allow"` plus per-agent allow; equivalent per-run flag is `--auto`.
- Hermes `unattended_mode` deliberately left at `deny` for cron/kanban safety.
- **Never disable** the tirith scanner + terminal security scan when approvals are off — they are the only remaining guardrail against prompt-injected destructive commands.

## The 32 GB OOM ceiling (and why opencode defaults to Unraid)

- With 32 GB, llama-server alone sat at **28.6 GB RSS**; adding opencode's node runtime tripped the OOM killer (peak 27.9 G RAM + 4.6 G swap, prompt processing collapsed to **1.9 tok/s** from swap thrash, llama-server restart counter hit 6). The Vulkan "DeviceLost" errors were OOM fallout, not a config bug.
- Rig now has 62 GB (2026-09-20), so this is history — but the lesson stands: **the local-rig provider in opencode stays opt-in**, cloud/Unraid is the default.

## Related

[[DeepSeek Harness Setup]] · [[Swarm Dashboard]] · [[Qwen3.8 Rig]] · [[Bench Suite (~bench)]]

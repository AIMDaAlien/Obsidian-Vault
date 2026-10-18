---
type: ops
topic: DeepSeek Harness (dsh)
updated: 2026-09-23
category: Agents & Tooling
tags: [dsh, opencode, config, sandbox]
publish: true
created: 2026-09-23
machine: bigrig
title: "DeepSeek Harness Setup"
---
# DeepSeek Harness Setup

**Category:** [[Agents & Tooling]] · **Vault:** [[Vault Map]]

`dsh` installed and wired to OpenRouter + the local llama-server (2026-09-19). Skill: `deepseek-harness`.

## Install

- **dsh 0.1.5-rc.2** into `~/.npm-global` (no sudo). Node v26.8.1 satisfies `>=24`. Install needed approval for node-pty, koffi, spawn-helper.

## Config — `~/.dsh/settings.yaml`

- Route 1 **`openrouter`**: `apiKeyEnv: OPENROUTER_API_KEY` reused from `~/.hermes/.env` (no new account). Slug `deepseek/deepseek-v4-flash-0731` (1.3 M ctx), single model, `system` role, `max_tokens` cap, 32K output budget. Verified: `dsh --profile headless` → `ok`.
- Route 2 **`swift-qwen-local`** → `http://127.0.0.1:8080/v1`, model id = the **GGUF path** (what llama.cpp serves), 120K ctx / 8K output. Requires llama-server running (autostart on :8080).
- **dsh demands a credential for EVERY provider, even local**: added `apiKeyEnv: DSH_LOCAL_DUMMY_KEY` and exported `DSH_LOCAL_DUMMY_KEY` in both launchers. Verified end-to-end by temporarily flipping the default route to local (`dsh --profile headless "Reply with exactly: ok"` → `ok`), then reverting. A settings overlay/patch file failed on format — flipping the default is the simpler validation path.
- Route 3 (2026-09-22): **`flash-local`** keyed by the AD384 GGUF path (from the fleet catalog work).

## Launching

- `~/.local/bin/dsh-web`: serves **loopback-only on port 3080**, `--no-open` by default (never auto-spawns a browser), strips `--host 0.0.0.0` so it can't expose on the LAN. Prints `http://127.0.0.1:3080/?token=…` — **the token rotates every boot; keep private**. The server dies with its terminal, so `dsh-web --no-open` gives a fresh URL.
- `~/.local/share/applications/deepseek-harness.desktop` → `~/.local/bin/dsh-app`: reuses a live server on 3080 (cached token) or starts one, scrapes the fresh token from the boot log, opens the browser; the server survives the browser closing. A static URL shortcut can never work (rotating token).
- Quickshell's SUPER+space menu live-scans `~/.local/share/applications/*.desktop` — no menu jsonc edit needed.

## Sandbox gotcha (important)

dsh reported "/home is mounted read-only (btrfs ro)". **False** — `/home` is genuinely btrfs rw. Real cause: dsh's fs sandbox defaults to `workspace-write` with `workspaceRoot = process.cwd()`, so only the server cwd is writable; `~/Documents` and `~/.dsh` are bound read-only → writes return **EROFS** and the agent rationalizes it as an OS read-only mount.
Modes: `read-only` (default) | `workspace-write` | `danger-full-access`. **Fix: `DSH_PERMISSION_MODE=danger-full-access`**, baked into both launchers (verified by writing into `~/.dsh/` and `~/Documents/`).

## Related

[[Hermes Install & Config Port]] · [[Qwen3.8 Rig]] · [[Omarchy Plugins & Shell Widgets]]

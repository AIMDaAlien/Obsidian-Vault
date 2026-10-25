---
type: ops
topic: Omarchy desktop
updated: 2026-09-23
category: Omarchy & Desktop
tags: [omarchy, quickshell, plugins, bar, linux]
publish: true
created: 2026-09-23
machine: bigrig
title: "Omarchy Plugins & Shell Widgets"
---
# Omarchy Plugins & Shell Widgets

**Category:** [[Omarchy & Desktop]] · **Vault:** [[Vault Map]]

Quickshell/Omarchy bar plugins built or installed on this rig.

## Installing community plugins (17 installed 2026-09-21)

- Command form: **`omarchy plugin add --enable --yes <git-url>`** — args are **git URLs**, not catalog names.
- Catalog = `plugins.omarchy.org`, client-rendered (web extract fails); cloning the marketplace repo gives only 5 top-level entries in `registry.json` while the real catalog is **~3746 plugins** — search loosely across name/description/tags.
- Picks: Lock Screen Explorer, Plugin Manager (omaplug), Omaland, Notification Center, OmaSettings, Activity Monitor, **Workspace Switcher (Woogy7, 5★ — hold Super, tap Tab)**, Omagen, Herdr, Prayer Times, Agent Orchestrator, Themes Gallery, Pocket, LocalSend, Detailed Weather, Omarchy Sensei, Cursor Accent.
- Gotchas: a typo'd org makes the install fail (re-pull the exact repo, don't hand-type); **LocalSend needs `omarchy pkg add localsend`**; Detailed Weather needs its backend tooling on first open. All 17 run unsandboxed third-party code.

## `aim.metrics` — menubar metrics widget

`~/.config/omarchy/plugins/aim.metrics/` (manifest.json, Metrics.qml, metrics.sh). update-survivable user plugin. Polls `/proc/stat`, `/proc/meminfo`, amdgpu sysfs, `nvidia-smi`, `curl localhost:8080/health` every 5 s. Left click = refresh, right click = popup, hover = tooltip.
Final bar readout: `✦ CPU 1% · 9.56G · RX 42%/62° · NV 40%/59° · 13 t/s · 10m`.
- Throughput must come from the server's **cumulative average** (`llamacpp:tokens_predicted_*`, needs `--metrics` on llama-server) — instantaneous 5 s deltas read 0 whenever no generation is in flight.
- During long prefills the GPU can sit at 96% while t/s shows nothing (prefill ≠ decode).
- Uptime = llama-server process etime (`10m`, `3h12m`).

## `aim.llama-switch` — center-bar model switcher / fleet widget

`~/.config/omarchy/plugins/aim.llama-switch/` (manifest.json, BarWidget.qml, Panel.qml, switchctl.sh), registered in the **center** of `shell.json` just after the keyboard layout.
- **Fleet source of truth: `~/.config/aim/fleet.yaml` + `fleetctl.py`** (emits the bar catalog JSON; `fleetctl check` = sync check; panel re-catalogs every ~4–6 s). Adding a model needs **zero QML edits** — edit `fleet.yaml`, add an opencode provider, or drop a GGUF.
- Auto-discovery: local llama-switch states (mtp/deep/split/flash/ornith/stop), remote providers parsed from `~/.config/opencode/opencode.json`, and `~/Models/*.gguf` (first shard only; nested files like `~/Models/qwen38flash-atomic/` were missed by a top-level scan).
- Status logic: with mutually exclusive runtimes sharing :8080, "up" must mean **"this is the active state"**, not "something answers on the port".
- `fleetctl check` resolves everything: rig + Unraid + OpenRouter (442 models). Hermes needs no change — cloud models resolve via its default `openrouter` provider.

## Quickshell API gotchas (hard-won)

- Process exit signal is **`onExited`**, NOT `onProcessClosed`.
- stderr/stdout are `StdioCollector` properties with **`onStreamFinished`** (NOT `onStderr`).
- `Color.positive` does not exist.
- Shell logs → system journal under tag `omarchy-shell`. The shell runs as a plain `quickshell` process (not a user service) with `QS_DISABLE_FILE_WATCHER=1`: plugins hot-reload but a stale compiled cache can persist → **`omarchy restart shell` is the reliable fix**.
- Verify a bar label without PIL: ImageMagick crop + tesseract OCR of the top-bar strip.
- Template to copy = `aim.metrics` (bar-widget + shell script + manifest); popup pattern = clock/agents `Panel.qml`.
- The `omarchy` **skill is a package symlink into `/usr/share/omarchy`** — never patch it; durable lessons go in `linux-workstation-setup` (`references/omarchy-shell-widget.md`).

## Related

[[Omarchy Trim Debloat & Idle Policy]] · [[Qwen3.8 Rig]] · [[Swarm Dashboard]]

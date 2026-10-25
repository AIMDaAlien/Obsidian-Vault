---
type: ops
topic: Omarchy desktop
updated: 2026-09-23
category: Omarchy & Desktop
tags: [omarchy, hyprland, tmux, crash-recovery, linux]
publish: true
created: 2026-09-23
machine: bigrig
title: "Desktop Session Persistence (Hyprland / tmux)"
---
# Desktop Session Persistence (Hyprland / tmux)

**Category:** [[Omarchy & Desktop]] · **Vault:** [[Vault Map]]

This box crashes and powers off abruptly; the desktop now comes back intact (2026-09-22).

## Stack

- **`~/.local/bin/session-persist`** — snapshots every open window (class, workspace, exact size/position, cwd, command line) **every 60 s** to `~/.local/state/session-persist/`, keeping 30 history snapshots.
- **`~/.config/omarchy/session-restore.sh`** — runs **6 s after login** (hooked in `autostart.lua`), replays the last snapshot: relaunches windows, puts them on their workspace, forces exact pixel geometry.
- Terminals come back via **tmux resurrect + continuum** (pane layout, scrollback, cwd), saved by the same 60 s timer. Chromium reopen-last-session enabled; bash history written per-command so a power cut doesn't eat it.

## Verified

- 4 tiled windows restored to exact captured sizes/positions **including a deliberately weird 96x1106 tile — 0 px deviation**; a floating window restored at 300,200 / 700x420.
- `kill -9` of the whole tmux server then restart brought back sessions, pane contents and cwd.

## Gotchas learned the hard way

- **Hyprland 0.56 rejects classic dispatcher syntax** — it uses a Lua dispatch wrapper; **`hyprctl eval` runs Lua** and is the working path for layout restore. Tiled windows ignore pixel dispatches, so exact layout must be replayed by **launch order**.
- The agent session runs *inside* one of the foot windows, so an early restore implementation **killed its own terminal mid-run twice** — the tool now detects its own ancestry and refuses to close it (non-destructive `apply` mode; `--clean` semantics dropped).
- The geometry-correction loop diverged when windows were already open and crushed tiles to negative sizes → now single pass, skips targets <50 px, aborts when it stops improving.
- tmux autosave is status-line driven and never fires headless → replaced with a deterministic timer.

## Incident found during this work

`llama-server.service` was in an **infinite restart loop (250+ restarts)**, each attempt loading a multi-GB model, with :8080 actually held by `llama-server-flash`. Stopped it; flash on :8080 kept serving and `llama-switch` can bring Qwen back on demand.

## Related

[[Omarchy Trim Debloat & Idle Policy]] · [[Qwen3.8 Rig]] · [[Rig Hardware & Display]]

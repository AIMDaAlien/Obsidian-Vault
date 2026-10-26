---
type: moc
category: Meta
tags: [meta, moc, omarchy, desktop, linux]
updated: 2026-10-26
publish: true
created: 2026-09-23
machine: bigrig
title: "Omarchy & Desktop"
---
# Omarchy & Desktop

Everything between the kernel and the agent windows.

**Vault:** [[Vault Map]]

## Notes

- [[Omarchy Trim Debloat & Idle Policy]] — 183-package baseline trimmed to a local-LLM dev box; service list; **screensaver off / stay-awake as a state file**; Arch update discipline (`yay`, never bare `pacman -S`).
- [[Omarchy Plugins & Shell Widgets]] — 17 community plugins; the `aim.metrics` menubar widget; the `aim.llama-switch` center-bar fleet switcher; **Quickshell API gotchas** and `omarchy restart shell`.
- [[Desktop Session Persistence]] — this box crashes abruptly; windows/tmux come back at 0 px deviation. `hyprctl eval` = Lua dispatch; the self-kill pitfall.
- [[Clickable File Paths in the Terminal]]: Ctrl+click a file name an assistant printed and the file manager opens with it selected; notes open in Obsidian. A tmux mouse binding plus an `xdg-open` shim for Ghostty's own links; the pointer no longer hides on key press.
- [[Bolero]]: Clop for Linux. Copy a screenshot and it is already small when you paste it. The Mac app Clop rebuilt for Wayland, with the frosted corner cards, a drop zone and draggable file names; review and build log in [[Bolero — rebuild and review 2026-10-26]].
- [[Browser Debloat & Benchmark 2026-09-19]] — Chromium/Helium/Zen flags, managed policies, renderer caps, measured RSS (~2 GB each); verdict: keep Zen + Chromium, drop Helium.

## Relevance

The desktop is the delivery surface for [[Models & Serving]]: the bar widget in [[Omarchy Plugins & Shell Widgets]] is how models get switched, and the metrics widget reads `llama-server /health`. Idle policy in [[Omarchy Trim Debloat & Idle Policy]] exists so long benches are not interrupted — the same reason spillover suspends are timed (see [[Bench Suite (~bench)]]). Browser flags matter because agents drive Chromium headless ([[Agents & Tooling]]).

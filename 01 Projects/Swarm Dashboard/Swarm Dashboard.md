---
type: benchmark-log
topic: Swarm Dashboard
category: Agents & Tooling
tags: [agents, dashboard, python]
publish: true
created: 2026-09-23
machine: bigrig
title: "Swarm Dashboard"
---
# Swarm Dashboard

**Category:** [[Agents & Tooling]] · **Vault:** [[Vault Map]]


## Related

- Data sources it reads: [[Desktop Session Persistence]] · [[Hermes Install & Config Port]] · [[Agents & Tooling]]
- Where it would be launched from: [[Omarchy Plugins & Shell Widgets]] (bar/bind)

## 2026-09-19 20:09
**Done:** Built Phase 0 aggregator `~/swarmdash/swarm_state.py` (stdlib-only) — merges Hermes sessions/messages, active_sessions.json, processes.json, kanban tasks, opencode session/part, agent.log latency, and ps into normalized rows. `--selftest` and `--json` flags added.
**Findings:** opencode timestamps are in MILLISECONDS (hermes are seconds) — must /1000. Live hermes sessions come from active_sessions.json pid match, NOT state.db (one live session pid 458063 had no state.db row; synthesized). Reads are read-only via sqlite `mode=ro`, no writes confirmed. ~22ms/poll, ~22MB RSS. Only terminal installed is `foot` (via xdg-terminal-exec) — it's the low-overhead default.
**Recommendations:** Next slice = TUI (swarmdash.py, Phase 1). Tune opencode gist fallback after a live watch; kanban tasks table currently empty.

## 2026-09-19 20:16
**Done:** Built Phase 1 TUI `~/swarmdash/swarmdash.py` (stdlib-only) — alt-screen, 24-bit Catppuccin grid renderer, spinner, status dots, header counts, filter (f), detail pane (Enter/j/k/Esc), q/r/+/- keys, SIGWINCH resize, --notify transitions, --latte, --selftest. README.md added.
**Findings:** Verified via pty: renders live, Enter opens detail, q exits restoring alt-screen. RSS 23.7 MB, CPU 0.67% over 6s (well under 40 MB bar). Both selftests OK. pty-test reaping is flaky due to slave EOF backpressure on tcsetattr(TCSADRAIN) — not a real-terminal issue.
**Recommendations:** Phase 2 = SUPER+D → foot (only terminal installed) running swarmdash.py; validate `hyprctl configerrors` empty. Tune opencode gist/live heuristic after a live watch.

## 2026-09-19 23:09
**Done:** Rewrote the layout layer of swarmdash.py (Phase 2) — width-aware plan_columns(), adaptive boxed frame (>=78 cols), 2-line gist wrap (<28-col gist), adaptive detail pane, de-cluttered rows. swarm_state.py/data untouched.
**Findings:** Column header now generated from the same plan → alignment by construction (fixes LAST/AGENT·MODEL misalignment). Gist absorbs leftover width so it no longer dies first; at 80 cols it wraps to a full-width second line. Split/full-height detail chosen dynamically (table keeps >=4 rows). --selftest covers 6 synthetic-size invariants. RSS ~22 MB, CPU ~1% (0.03s/3s).
**Recommendations:** Live-watch gist/live heuristic; opencode gist fallback still untuned (kanban table empty).

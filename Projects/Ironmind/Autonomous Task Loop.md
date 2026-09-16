---
tags: [ironmind, devops, task-loop, opencode]
created: 2026-09-15
updated: 2026-09-15
project-path: ~/Documents/Projects/ironmind
---

# Ironmind — Autonomous Task Loop

The [[Ironmind Hub]] app has a self-driving build loop: OpenCode CLI driven by a
shell wrapper, forced onto the local Qwen3.8-Flash-Next model on Unraid
([[Qwen3.8-Flash-Next]]), working the app's master plan one task at a time —
each task planned in a cold session, executed in a fresh cold session, and
admitted only through a real `swift build && swift test` gate.

## What exists where (all in the repo)

| Path | Role |
|---|---|
| `.opencode/MASTER-PLAN.md` | The spec the loop runs on. 9 hard constraints, task queue w/ objective gate, "how to work a task", STOP rule for architecture/security decisions |
| `.opencode/opencode.json` | Project config forcing EVERY agent + fallback model to `qwen38-unraid/qwen38-flash`. No other model can leak in from the global ~/.config/opencode/opencode.json |
| `.opencode/plans/<SLUG>-plan.md` | Persisted per-task plans (named by task header slug, e.g. `QH-plan.md`, `F1-plan.md` — NOT by pass position, so a new pass can't overwrite a prior task's plan) |
| `scripts/task-loop.sh` | The loop engine (details below) |

## How the loop works

Per task, in order, with **no model other than `qwen38-unraid/qwen38-flash`**:

1. **Plan session** (fresh cold context): reads MASTER-PLAN + relevant docs,
   writes a concrete plan to `.opencode/plans/<SLUG>-plan.md`. No source edits.
2. **Execute session** (fresh cold context): reads MASTER-PLAN + the plan file
   from disk, makes the smallest diff, adds matching unit tests.
3. **Gate** (run by the shell, not the model's judgment): `swift build` exits 0
   AND `swift test` exits 0 with the full suite green. Also greps the diff for
   network imports (constraint 1).
4. Success → tick the checkbox in MASTER-PLAN. Failure → uncheck, one retry
   with the failure log attached, then surface for human review if still red.

**Hard invariants**
- `MAX_TASKS` caps tasks per pass (default 10). `--plans-only` does planning
  only.
- DEFERRED boxes (journal/F3) are skipped — the loop never touches them until
  a human re-opens them.
- `swift build && swift test` is the ONLY ticket forward.

## Model-lock (why it stays on Qwen Flash)

The loop is deliberately pinned to `qwen38-unraid/qwen38-flash` (the 176B MoE
on Unraid, ~6B active, agentic per [[Qwen3.8-Flash-Next]]). It is NOT the
Mac-local 27B ([[Qwen3.8-27B]]) and NOT DeepSeek. Tradeoff: it's a reasoning
model, so each step takes seconds-to-minutes of visible thinking — right for
overnight unattended building, slow for interactive watching.

## Watching it live (tmux)

The loop runs headless, so you attach to see it. tmux was installed for this
(Homebrew). The session is named `ironmind`.

```sh
tmux attach -t ironmind      # watch the live opencode TUI + loop logs
# detach (leave running):  Ctrl-b then d
# kill entirely:           Ctrl-b then :kill-session
```

Launching a pass:
```sh
cd ~/Documents/Projects/ironmind
MAX_TASKS=1 scripts/task-loop.sh            # one task, then stop for review
scripts/task-loop.sh                        # up to 10 tasks
scripts/task-loop.sh --plans-only           # planning only, no edits
```
(To run visibly: wrap in a tmux session as above.)

## Git state (remote + commits)

- **Remote:** `https://github.com/AIMDaAlien/ironmind.git` — PRIVATE (the docs
  mandate private; this app's design notes are sensitive-by-implication).
  `main` tracks `origin/main`.
- Commits so far:
  - `5e86288` — F0 good-rep log + the task-loop harness (MASTER-PLAN,
    model-locked opencode.json, task-loop.sh) + full source/docs. 35 files.
  - `cd9e3a0` — Quiet hours 20:00–07:00 gate the movement pacer absolutely.
- Vault note convention: this repo is private-local by default; favor local
  commits + the private remote.

## Progress (as of 2026-09-15)

- [x] **F0** Good-rep quick log — menu-bar ✓ → one-word note → JSONL proof vote
- [x] **QH** Quiet hours 20:00–07:00 — MovementKit pacer silent in-window, no
      burst queue at 07:00; configurable; 12 tests incl. boundary ticks.
- [ ] **F1** Settings window — IN FLIGHT (hotkey recorder, editable playbooks,
      timer length, identity line, quiet-hours window)
- [ ] **F2** Morning protocol
- [x] **F3** Journal — **DEFERRED** pending Syncthing (Aim journals on phone;
      needs `~/Ironmind/journal-import/` folder syncing first)
- [ ] **F4** Weekly review
- [ ] **F5** 90-day arcs
- [ ] **F7** Time management (moved BEFORE fitness so fitness has free-blocks)
- [ ] **F6** Fitness (moved AFTER time; fires into free blocks, never in QH)

## Notes / decisions locked in

- **Quiet hours scope:** gates the LIVE 30-min movement pacer too (it runs
  under launchd overnight), not just future fitness reminders. "Not a snooze"
  — nothing is queued to fire at 07:00.
- **Journaling deferred on purpose:** don't build an importer against no data.
  Re-open when Syncthing exists.
- **Task order changed** from the original roadmap: time-management before
  fitness (fixes the "fitness hangs reminders off F7's free blocks that don't
  exist yet" dependency smell), and QH inserted early since it gates the pacer.
- **Plan files keyed by task slug**, discovered via the nearest preceding
  `### ` header — not pass position (that caused an overwrite collision).
- Frontend/UI design pass is deferred until the functional tasks land.

## Related

- [[Ironmind Hub]] · [[Qwen3.8-Flash-Next]] · [[Qwen3.8-27B]]

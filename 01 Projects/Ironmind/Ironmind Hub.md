---
tags: [ironmind, hub]
created: 2026-09-07
publish: true
project: Ironmind
project-path: ~/Documents/Projects/ironmind
featured: 64
summary: "A Mac menu-bar app that hands me one tiny exercise or thinking card after 30 minutes of sitting. Rebuilt around the single feature I actually used."
---

# Ironmind - Hub

Private macOS menu-bar app. Native Swift, local-only, periwinkle-dark, Ubuntu font. It deals tiny body and mind reps while I sit at the Mac. Done or Skip, nothing else.

**Repo:** `~/Documents/Projects/ironmind`. Code and docs live together. The `docs` folder is symlinked in here so I can read it from Obsidian.

## What v2 is

v1 had nine packages and six features. The only thing I actually used was the 30-minute movement pacer. Everything I had to go open myself died.

v2 keeps the pacer's trick and makes it the whole app:
- It comes to me while I'm sitting. I never have to go open it.
- **Body cards** every ~30 minutes of sitting. **Mind cards** every 3rd deal.
- The day has a shape. Posture in the morning, strength midday, mobility in the afternoon, wind-down in the evening, silent 01:00-07:00.
- The deck adapts to what I actually do. Every card I finish gets a little harder next time.
- **90-day arcs** in the Record window, with before and after measurements.
- No streaks, no points, no red, no journaling. Skip is just a fact.

## Docs map

| Doc | In repo at |
|---|---|
| v2 design (source of truth) | `docs/superpowers/specs/2026-10-11-ironmind-v2-design.md` |
| Cutover test plan and ledger | `docs/superpowers/plans/2026-10-13-ironmind-v2-cutover-test.md` |
| Build log | `docs/BUILD-LOG.md` |
| Session handoff | `CONTINUATION.md` |

The old `docs/01-05` are v1 and superseded.

## State of things

- [x] v2 designed and approved - 2026-10-12
- [x] v2 built and merged. Packages: Theme, Core, Storage, RepKit, ArcKit, AppShell - 2026-10-12
- [x] Cutover test Phases 0-3 passed. Fixed the card panel height and the Settings tab row along the way
- [x] v2 live under launchd, v1 retired - 2026-10-14
- [x] Live day found video time reading as "away". Fixed so a playing video counts as sitting - 2026-10-15
- [ ] Phase 4 rerun on the first full day with the fix - 2026-10-16
- [ ] Floor-card check after three clean days
- [ ] First 90-day arc
- [ ] Veyra integration, local models only, after Phase 4 passes

Private details live in [[Ironmind - Current State]].

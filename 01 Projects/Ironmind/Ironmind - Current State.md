---
tags: [ironmind, project-tracking]
created: 2026-10-15
publish: false
project: Ironmind
project-path: ~/Documents/Projects/ironmind
---

# Ironmind - Current State

## Quick Context
v2 of my rep engine. It runs under launchd from `.build/release/ironmind` in the main checkout. Data lives in `~/Library/Application Support/Ironmind/` as JSONL. See [[Ironmind Hub]] for what it is.

---

## Status Dashboard

| Area | Status | Last Updated |
|---|---|---|
| v2 app | Live under launchd, pid changes on every install | 2026-10-15 |
| Cutover test Phases 0-3 | Passed | 2026-10-14 |
| Phase 4 (live day) | Blocked on the presence bug, now fixed. Rerun 10-16 | 2026-10-15 |
| First arc | Not started. Morning of 10-16 | 2026-10-15 |
| Veyra integration | Planned, waits on Phase 4 | 2026-10-15 |
| Tests | 132 green, zero network code | 2026-10-15 |
| Pushed to GitHub | Not yet | 2026-10-15 |

---

## Decisions Made

### Data and privacy
- **No cloud models ever get my data.** Local models and loopback ports are fine. The old "zero network, no AI" rules were stricter than I need. They stay in force until Veyra work starts, then relax to local-only on purpose.

### Scheduler
- **A playing video counts as sitting.** Watching with my hands off used to read as idle, and every 10+ idle minutes wiped the 30-minute count. Picked this over "pause instead of reset" and "shorter interval".
- **Don't just raise the 30 s away limit.** It exists because 2 minutes nudged people who had already walked off.
- **Mind ratio is every 3rd card.** That's about half as many mind cards as body cards. If I want fewer, it's one number in Settings.

### Veyra
- **Keep the two apps separate for now.** RAM isn't the problem: 48 GB, 91% free, and Ironmind uses 57 MB. The point is to verify Ironmind first.
- **First step when it starts: front-app sensing.** It needs no model and no permission. The screen-reading model comes later, if it's still worth it.
- **Decide before wiring reps into Veyra.** Veyra remembers and talks, so my reps would have a witness. Make that a choice, not an accident.

---

## Recent Changes
- 2026-10-14: Cutover. v1 stopped, `dist/` deleted, 454 old movement entries migrated into `reps.jsonl`. `movement.jsonl` untouched.
- 2026-10-14: First Phase 4 look. Only 1 v2 card logged. Replaying the scheduler on my real history proved the code wasn't stuck.
- 2026-10-15: Found it. 3 cards in ~22 waking hours, because video time read as away. The push-up card landed exactly 30 minutes after a video stopped.
- 2026-10-15: Fix shipped (`c2a2c6c`). The clock checks whether something is holding the display awake.
- 2026-10-15: `daemon.sh install` had a race and the app was down for about a minute. Fixed so it waits for launchd to let go (`49a6c88`).
- 2026-10-15: Weight logged from the weekly card, 62.6 kg.
- 2026-10-15: Phase 4 rerun plan written into the test plan.

---

## Pending Tasks

### Morning of 2026-10-16
- [ ] Measure fresh: height, plank, push-ups, pull-ups, dead hang. Weight is already in.
- [ ] Settings → Measurements → pick the kind, type the number, Add. One row each.
- [ ] Record → title → Start. Start saves the latest numbers as "before", so measure first.

### Evening of 10-16 or the morning of 10-17
- [ ] Phase 4 report: zero cards 01:00-07:00, about one card per 30 minutes of sitting, at least one card during a video, mind/body between 0.35 and 0.65.

### 10-18 or later
- [ ] Floor-card check. Floor cards should be about a quarter of body cards. Under 15% means starved. Show me the numbers before changing anything.

### After Phase 4 passes
- [ ] Veyra integration, local only. Front-app sensing first.
- [ ] Parked: nicer card design. The "Read one poem" card should come with the poem.
- [ ] Push to GitHub when I say.

---

## Things Learned
- 2026-10-15: macOS browsers hold a "prevent display sleep" assertion while a video plays. `pmset -g log` shows them as "Video Wake Lock". That made it a clean signal for "watching, not gone".
- 2026-10-15: `launchctl bootout` returns before the job is actually gone. Bootstrapping right after fails with "5: Input/output error".
- 2026-10-15: Nothing is written when a card is dealt, only on Done or Skip. If the Mac sleeps with a card up, it closes with no log, so the log can undercount slightly.
- 2026-10-15: About a third of my old skips were reflex skips, under 5 seconds. Worth watching, not fixing.

---

## Related Notes
- [[Ironmind Hub]]
- [[Autonomous Task Loop]]
- Veyra Companion: `01 Projects/Veyra Companion/99 - Current Handoff.md`

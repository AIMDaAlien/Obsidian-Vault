---
tags: [learning, reliability]
project: Corne Accuracy Trainer
status: Implemented — physical trial pending
repository: /Users/aim/Documents/Projects/Corne Accuracy Trainer
updated: 2026-08-22
---

# Today Adaptive Coach and Trial Record

## Implemented Session

One Corne-only session adapts between 12 and 20 minutes of active time. The
clock pauses while the page is unfocused.

1. **Recall — 2–3 minutes:** due targets, relaxed correction, no hints.
2. **Repair — 5–10 minutes:** up to three priority targets; cues fade after
   three clean occurrences and return after an error.
3. **Transfer — 3–5 minutes:** learned-output English words mixed with anchors.
4. **Check — 2 minutes:** strict restart-on-error assessment without hints.

Priority is overdue review, remediation/confusion, reliable weakness with at
least five samples, then underexposed current-lesson output. Passing advances
the 1/3/7-day review schedule; failure returns the target to tomorrow and keeps
it in remediation.

## Daily Counting Rule

Only the first completed Check on a local calendar day records an assessment
and changes review dates. **Practice extra** remains available afterward, but
its completion card says it is uncounted and its work does not distort the
spaced-review schedule.

After mastery, the app shows the first-to-latest clean characters-per-minute
change across the latest seven counted assessments. It does not emphasize a
single personal-best WPM.

## Verification Record

- Automated tests: 31 passing.
- Production build: passing; generated `dist/client` files match source.
- `git diff --check`: passing.
- Browser visual/accessibility/install/offline pass: pending because the
  available browser connector failed to initialize during implementation.
- Deployment: not changed.

## Physical and Two-Week Trial

- [ ] Complete three sessions on Aim's Corne, including Layer 3.
- [ ] Include deliberate errors, Backspace corrections, phase transitions,
  and a next-day review.
- [ ] Compare median assessment accuracy/throughput for the first three versus
  final three sessions; final accuracy must remain at least 98%.
- [ ] Track due-target first-attempt retention across the trial.
- [ ] Run three identical 60-second QWERTY checks on the Epomaker and MacBook
  before and after. Accuracy should remain within one percentage point and WPM
  within 5%.

## Links

- [[00 - Project Overview]]
- [[01 - Technical Architecture and Product Record]]
- [[02 - Word Progression and Public Release Roadmap]]

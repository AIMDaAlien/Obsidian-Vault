---
tags: [guide]
project: Veyra Companion
updated: 2026-08-10
---

# Assets, Expressions, and Display

## Canonical Asset Structure

Repository: `/Users/aim/Downloads/Veyra_Companion_Sprites`

```text
Assets/
├── Originals/     # 85 protected source images
├── Processed/     # cleaned working derivatives and repairs
├── Runtime/       # 67 portraits and 18 chibis loaded by the app
├── QA/            # contact sheets, matte comparisons, reports
└── References/    # loose historical references, never loaded
```

The current mind implementation does not modify any image asset or expression catalog assignment.

## Expression Contract

- Core emits only mood, intensity, activity, and confidence.
- The Swift arbiter owns filenames, enabled state, family, context, cooldown, hold, history, and deterministic tie-breaking.
- Immediate events override model mood.
- Low-confidence appraisal preserves the current expression.
- Ordinary conversation prefers portraits.
- Chibis represent sustained action, props, idle behavior, or strong physical reaction.
- Opposing portrait moods may transition through `veyracontent`.
- Clicking is deterministic from session, tap count, current mood, current activity, and pressure.
- Patting uses the affectionate portrait family and restores afterward.

## L01N8A Dedicated Layout

- Detect screen by the name `L01N8A`, then persist its UUID.
- Use the actual `NSScreen.frame`; do not assume pixel-to-point scaling.
- One borderless full-screen-sized window.
- Veyra begins at 0 points from the left edge.
- Composer begins 15 points after the rendered sprite and fills the remaining right side.
- Portrait maximum height: 760 points.
- Chibi maximum height: 700 points.
- Composer remains visible.
- The dedicated screen and all Veyra windows are excluded from screen capture.

Diagnostic proof on 2026-08-10 detected L01N8A at 1280×800 points and resolved:

- Window: 1280×800.
- Veyra stage: 584×800.
- Composer: 695×800 after the 15-point gap.

## Portable Layout

- Veyra sits 24 points from the main visible frame's bottom-right.
- Portrait maximum height: 320 points; chibi: 280.
- Clicking opens the 420×520 composer to her left and triggers a reaction.
- Shift-Command-H opens the composer without a reaction.
- Only non-transparent sprite pixels are clickable.

## Open Physical Checks

- Restart the currently running older Veyra process onto the new release binary.
- Confirm the composer remains readable at the real frame size.
- Confirm pat hit region matches Veyra's head rather than transparent or accessory pixels.
- Grant Screen Recording permission, then confirm ScreenCaptureKit excludes L01N8A and every Veyra window.

---
title: 99 - Current Handoff
tags: [project]
created: 2025-01-01
updated: 2026-10-10
publish: true
machine: mac
engine: mlx
project: Local Language Engine
---

# Current Handoff

- Canonical repo: `~/Documents/Projects/language-engine`, branch `mac-v2`. Phase 1 is commit 79bcc21, Phase 2 is commit f1085ef, and Phase 3 core is commit 4133a1a.
- Direction: Mac-only Arabic tutor with a native SwiftUI app. The phone plus always-on Mac design is dropped. Story and results are in [[03 - Mac Rebuild Build Log]].
- Core idea: a rule-based decision layer (FSRS spaced repetition plus a hand-built skill map) picks what to study. The model only writes corrections and explanations.
- Phase 1 is done. Phone code removed, live audio moved to a local WebSocket, structured correction format in place, 100-sentence test set and scoring built, bake-off run.
- Bake-off winner: Gemma 4 26B-A4B (100% valid format, 49% match ignoring punctuation, 2.4 s median reply, 19.6 GiB). Also the prep model for now.
- Known weakness: models change already-correct sentences about half the time. Falcon-H1-Arabic isnt public. Jais-2 is gated.
- Hijazi stays labeled "unreviewed" (no native reviewer). MSA is checked with automatic evidence. Do not invent tashkil.
- Phase 2 is done. Decision layer built: 3 cards per item, FSRS scheduling, daily 30-minute planner with brakes, 5 speaking-first units (60 items). 138 tests pass.
- Known gaps: days of the week arent taught, drills stay apart from the FSRS schedule on purpose, planner rules are tuned on a simulated learner.
- Phase 3 core is built: native SwiftUI app "Majlis" (Today, Review, Units, Live session, Settings) plus the voice loop (mic, Whisper, tutor model, spoken reply, push-to-talk, interrupt). Commit 4133a1a on mac-v2. 167 Python tests and 20 Swift tests pass.
- Live corrections now have over-correction guards (smallest fix, vowel or punctuation only counts as correct, hedging or unrecognized words flagged "needs review"). Of Gemma's 6 over-corrections, 2 show as correct, 2 flagged, 2 word-swap rewrites still slip through. Stricter prompt not measured live.
- Drills are graded but kept apart from FSRS, misses logged as weak spots, mistakes logged by type. Speech output is plug-in. Voice candidates: Audar TTS, Fish Audio S2 Pro (both on the Mac), Voxtral, Nabra, NAMAA Saudi TTS.
- Voice test round 1 (2026-10-10, uncommitted): `scripts/tts_bakeoff.py`, results in `var/reports/tts-bakeoff-summary.md`. Majed 0.8 s, 1.8% Whisper errors. Chatterbox (audio.cpp, clone of Majed) 4.1 s, 1.8 GB, 3.0%. Audar (clone of Majed) 6.3 s, 3.0 GB, 1.2%. Fish S2 Pro disqualified (34 to 37 GB). MOSS untested (needs newer mlx-audio). Audar runs from `var/tts-venv` via `scripts/tts_engines/audar_tts.py`.
- TTS cache now keys on the full `TTS_COMMAND`, so swapping voices never serves old clips.
- Open: human rating of the English explanations, and the blind voice sheet `var/reports/tts-blind/index.html`.
- Next action: finish Phase 3. Aim rates the blind voice sheet, then `scripts/tts_bakeoff.py score` picks the winner (pick_winner rule still to write) and it gets wired via TTS_COMMAND. Decide on Voxtral (2.5 GB) and Nabra (0.3 GB) downloads. Record about 50 clips of Aim's Arabic for speech recognition tests, and do a first real end-to-end spoken session. Then Phase 4.

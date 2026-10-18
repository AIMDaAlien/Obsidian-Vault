---
tags: [hardware-constraints, cost]
created: 2026-07-29
updated: 2026-10-10
publish: true
machine: mac
engine: mlx
project: Local Language Engine
status: Mac-only rebuild underway - Phase 3 core built, blind voice test ready to rate
repository: ~/Documents/Projects/language-engine
phase: Phase 3 - native Mac app and voice loop (core built)
platform: Mac
featured: 58
summary: "A private Arabic tutor that runs entirely on my own MacBook: what it teaches, the 36 GB memory budget it must stay under, and the key design decisions."
---

# Local Language Engine

## Purpose

Local Language Engine is a private, Mac-hosted language tutor with a live
Android conversation client. It keeps lessons, recordings, corrections,
memories, and model inference on Aim's hardware.

The first release teaches Arabic:

- Modern Standard Arabic (MSA) is the grammatical and written foundation.
- Reviewed Hijazi Arabic overrides make conversation sound natural without
  silently replacing the MSA lesson objective.
- Japanese is an isolated beta language pack; Arabic remains the release gate.

## Status

**Mac-only rebuild underway - Phase 3 core built, blind voice test ready to rate**

Phases 1 and 2 are done, and the Phase 3 core is built, on branch `mac-v2` (commits 79bcc21, f1085ef, and 4133a1a). Phase 1 picked Gemma 4 26B-A4B as the tutor model. Phase 2 built the decision layer. Phase 3 built the native Mac app, Majlis, with the voice loop and guards against fake corrections. 167 Python tests and 20 Swift tests pass.

Voice test round 1 is done. Majed, Chatterbox, and Audar all work, and Fish Audio is out because it needs too much memory. Still to do in Phase 3: rate the blind voice test, record about 50 clips of my own Arabic, and do a first real spoken session. Phase 4 adds pronunciation scoring and lesson prep. Phase 5 hardens everything.

Canonical repository: `~/Documents/Projects/language-engine`

## Hardware and Budget

- Host: 14-inch MacBook Pro (`Mac17,9`)
- Chip: Apple M5 Pro, 18 cores
- Unified memory: 48 GB
- OS at approval: macOS 26.5
- Maximum application allowance: **36 GB total resident memory**
- Proven phone: OnePlus 12 (`CPH2583`), Android 16 / API 36
- Mobile delivery: locally built native Expo/React Native APK; no cloud build
  or Expo OTA service

The 36 GB allowance includes model weights, KV/recurrent state, speech models,
media buffers, server processes, and SQLite. The operating system keeps the
remaining 12 GB. An out-of-memory crash or swap-heavy run is a failed test.

## Stack

- Tutor model: Gemma 4 26B-A4B 4-bit via LM Studio
- Host: Python, LM Studio API, SQLite, local filesystem
- Decision layer: FSRS (spaced repetition) with hand-built skill map
- Daily structure: review, new vocab, speaking drills, mini conversation
- Grammar checks: CAMeL Tools for Arabic grammar analysis
- Mac app: planned native SwiftUI with voice input and output
- Arabic: Modern Standard Arabic as foundation, Hijazi as reviewed suggestion layer

## Major Decisions

1. Android first. Expo is used as a local native toolchain, not as a required
   hosting, build, account, or over-the-air update service.
2. Arabic first. MSA remains canonical; Hijazi is a reviewed suggestion layer.
3. The active model window is 128K tokens.
4. At 80K tokens, completed material is compacted into durable lesson episodes.
   At 112K, compaction is mandatory before another turn.
5. Raw recordings are auditable and never become approved learning cards
   without Aim's review.
6. The Mac owns truth. Mobile can work offline, but sync conflicts never
   silently overwrite host data.
7. The interface is dark, Very Peri-led, and uses restrained glass only where
   it improves hierarchy. Arabic content is explicitly RTL; the application
   chrome begins in English and becomes bilingual, then Arabic-led, with
   confirmed learning progress.
8. The Android status bar is hidden in-app for a focused, full-screen lesson.
9. Advancement is never inferred from taps alone. Aim explicitly confirms each
   interface vocabulary step until mastery data is reliable enough to assist.

## Earlier design (Android)

The first version was a Mac server with an Android phone app client. The Mac ran one huge model all day, and the phone called it over Tailscale. It never worked well. The Mac is a laptop, not a server. The model was too big and didnt answer half the time. And it wasnt really teaching, just chat. For the full story of what changed and why, see [[02 - Build, Device, and Product Record]].

## Links

- [[01 - Architecture and Implementation Plan]]
- [[02 - Build, Device, and Product Record]]
- [[03 - Mac Rebuild Build Log]] - current direction: Mac-only rebuild, plain-language story with Phase 1, 2, and 3 results
- Repository: `~/Documents/Projects/language-engine`
- Parent index: [[README]]

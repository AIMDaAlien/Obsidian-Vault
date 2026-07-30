---
project: Local Language Engine
status: Planning approved — implementation pending
phase: Documentation and Phase 1 proof
repository: /Users/aim/Documents/language-engine
platform: Android-first
updated: 2026-07-29
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
- Japanese is a later language pack, not a second Phase 1 scope.

## Status

**Planning approved — implementation pending**

Current phase: documentation and Phase 1 compatibility proof.

Canonical repository: `/Users/aim/Documents/language-engine`

## Hardware and Budget

- Host: 14-inch MacBook Pro (`Mac17,9`)
- Chip: Apple M5 Pro, 18 cores
- Unified memory: 48 GB
- OS at approval: macOS 26.5
- Maximum application allowance: **36 GB total resident memory**
- Mobile target: physical Android device using an Expo development build

The 36 GB allowance includes model weights, KV/recurrent state, speech models,
media buffers, server processes, and SQLite. The operating system keeps the
remaining 12 GB. An out-of-memory crash or swap-heavy run is a failed test.

## Stack

- Model: Qwen3.6-35B-A3B 4-bit on Apple Silicon through MLX
- Optional decode path: MTP, enabled only after a quality and latency benchmark
- Host service: Python, MLX, WebRTC, SQLite, local filesystem media
- Mobile: Expo + React Native + TypeScript development build
- Transport: WebRTC for live audio and events; HTTPS for sync and library APIs
- Storage authority: Mac-owned SQLite database and media directory
- Offline storage: bounded mobile SQLite/media cache with an operation outbox

## Major Decisions

1. Android first. Expo Go is not supported because WebRTC needs native code.
2. Arabic first. MSA remains canonical; Hijazi is a reviewed suggestion layer.
3. The active model window is 128K tokens.
4. At 80K tokens, completed material is compacted into durable lesson episodes.
   At 112K, compaction is mandatory before another turn.
5. Raw recordings are auditable and never become approved learning cards
   without Aim's review.
6. The Mac owns truth. Mobile can work offline, but sync conflicts never
   silently overwrite host data.
7. The interface is dark, RTL-native, Very Peri-led, and uses restrained glass
   only where it improves hierarchy.

## Links

- [[01 - Architecture and Implementation Plan]]
- Repository: `/Users/aim/Documents/language-engine`
- Parent index: [[Projects/README]]


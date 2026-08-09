---
project: Local Language Engine
status: Standalone Android and beginner UI proven — release hardening active
phase: Physical-device pipeline and progressive interface proven; dependability hardening
repository: /Users/aim/Documents/language-engine
platform: Android-first
updated: 2026-07-30
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

**Standalone Android and beginner UI proven — release hardening active**

The locally built Android app now runs on Aim's OnePlus 12 without Metro, Expo
Go, an Expo account, or an ADB tunnel. Over private Tailscale HTTPS, a physical
microphone turn has completed the full phone → WebRTC → Mac transcription →
tutor → signed speech → phone round trip.

The beginner experience now starts with English controls, correctly isolated RTL
Arabic lesson content, and a four-stage Guide that adds Arabic only when Aim
confirms each vocabulary bundle. The stage is stored on the phone and remains
reversible. Release signing, stronger application authentication, Mac autostart,
reconnect, and stress testing remain open.

Canonical repository: `/Users/aim/Documents/language-engine`

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

- Model: Qwen3.6-35B-A3B 4-bit on Apple Silicon through MLX
- Optional decode path: MTP, enabled only after a quality and latency benchmark
- Host service: Python, MLX, WebRTC, SQLite, local filesystem media
- Mobile: Expo 56, React Native 0.85, TypeScript 6, React Native WebRTC,
  Expo SQLite and Expo Audio
- Transport: encrypted WebRTC media/events through private Tailscale Serve
  HTTPS; shared-key APIs support signed five-minute media URLs
- Storage authority: Mac-owned SQLite database and media directory
- Offline storage: bounded mobile SQLite/media cache with an operation outbox

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

## Links

- [[01 - Architecture and Implementation Plan]]
- [[02 - Build, Device, and Product Record]]
- Repository: `/Users/aim/Documents/language-engine`
- Parent index: [[Projects/README]]

---
project: Veyra Companion
status: Veyra rename installed; Screen Recording grant and live visual proof pending
repository: /Users/aim/Downloads/Veyra_Companion_Sprites
platform: macOS
updated: 2026-08-11
---

# Veyra Companion

## Purpose

Veyra Companion is Aim's private, local macOS companion. Veyra combines a persistent conversational mind, deterministic expressions, screen and cursor awareness, local research, and a dedicated-display interface.

She is not designed as an otome chatbot or engagement product. The goal is a perceptive long-term partner who can be warm, teasing, skeptical, disciplinary, and practically useful without pretending to be human.

Canonical repository: `/Users/aim/Downloads/Veyra_Companion_Sprites`

## Current Status

**Aim approved Margin Companion A. Its native AppKit layout, topic persistence, and Markdown research handoff are installed with a stable local signature; Screen Recording approval and live hardware proof remain.**

Implemented:

- Typed mood, activity, and app-event expression selection across 85 approved assets.
- L01N8A detection by display name with persisted UUID fallback.
- Dedicated and portable display layouts, composer text sizing, and transparent-pixel hit testing.
- Streaming local conversation through LM Studio.
- Automatic brief, normal, deep, creative, and research response modes.
- SQLite conversation, memory, commitment, activity, and embedding storage.
- Editable Mind panel.
- Cursor, poke-pressure, pat, idle-affect, foreground-app, OCR, and external development-event awareness.
- Bounded qualitative research through local SearXNG then the Unraid instance.
- Quiet-hour and daily-limit initiative policy.
- Native `Veyra Companion.app` bundle with bundled assets, login startup, and a consistent install path at `~/Applications/Veyra Companion.app`.
- Persistent composer restoration from SQLite, transient touch status, single-family sprite transitions, and observation-driven expression feedback with cooldowns.
- Permission-safe screen awareness: launch preflight only, plus a deliberate enable action in Mind Settings.
- Approved Field Notes Margin Companion in native AppKit: 593/687 dedicated-display split, 64/620/116 composer regions, large chronological turn rows, paper/ink styling, and New Topic/Mind-only permanent header controls.
- SQLite topics with one-active-topic enforcement, historical-message migration, active-topic inference isolation, exact transcript restoration, and cancelled partial-output preservation.
- Return sends, Shift-Return inserts a newline, `Command-N` creates a topic, and text sizing lives in Mind while retaining `Command-Plus`/`Command-Minus`.
- Research writes a standalone Markdown report under `~/Documents/Veyra Research/` and returns a clickable local file pointer in chat.

Verified on 2026-08-11:

- 32 Swift tests pass, including legacy database/defaults migration, topic isolation, exact resume, cancelled partials, Return/Shift-Return behavior, and Markdown research artifacts.
- Release build passes. Runtime diagnosis detects L01N8A at 1280×800 with a 593×800 portrait stage and 687×800 composer.
- Two signed installs pass strict code-sign verification with the same designated requirement: bundle ID `com.aim.veyra-companion` plus certificate SHA-1 `11e6fbcc37d446911d84f9a3f4ae9706bc3dace8`.
- The signed app is installed and running from `~/Applications/Veyra Companion.app`; its runtime diagnosis confirms the exact 1280×800, 593/687 dedicated layout.
- The installed process reports `screenCaptureAuthorized=false`, so the new stable identity still needs its one-time Screen Recording grant.
- The previous database migrated transactionally to `~/Library/Application Support/VeyraCompanion/veyra-mind.sqlite3` with all 14 messages and one topic preserved; a closed backup remains under `Veyra Migration Backups`.
- The catalog and installed bundle contain 85 uniquely named Veyra assets: 67 portraits and 18 chibis.
- The old LaunchAgent is removed; `com.aim.veyra-companion` is installed and Veyra is running as the renamed executable.
- LM Studio retains only `veyra-fast`; the superseded fast and embedding aliases were unloaded.
- Structural commits `0b85f22`, `ee209ac`, `74c2330`, `c90310a`, and `81f3b0c` are local and not yet pushed.

Verified on 2026-08-10:

- 25 Swift tests pass.
- Release build passes.
- Warm local greeting completes end to end, including semantic appraisal and persistence.
- A three-round-cap research request completed through Unraid SearXNG and produced a local synthesis.
- The CLI event bridge writes to the shared Veyra mind database.

Still awaiting proof or approval:

- One-time Screen Recording approval for the signed identity, followed by a rebuild proving the approval is retained.
- Screen Recording permission and real OCR behavior.
- Live visual review of the packaged app on L01N8A.
- Manual review of the Mind panel, pat gesture feel, initiative wording, and streamed composer behavior.
- Qwen3.6-35B-A3B Q2/MTP versus 4-bit model selection benchmark.

## Hardware and Privacy

- Host: 14-inch MacBook Pro, M5 Pro, 48 GB unified memory.
- Primary model API: LM Studio at `127.0.0.1:1234`.
- Research: `127.0.0.1:8082`, then Unraid `192.168.0.120:8082`.
- Dedicated display name: `L01N8A`; detected AppKit frame: 1280×800.
- Raw screen frames remain in memory and are never stored by Veyra. Capture input is downsampled to at most 1280 pixels on its longest edge before OCR.
- OCR and activity summaries expire after 24 hours.
- Conversation history remains until Aim edits or deletes it.
- Search queries and public page requests may leave the LAN; memories, screenshots, OCR dumps, and unrelated private context are not added to search queries.

## Links

- [[01 - Architecture and Implementation Plan]]
- [[02 - Mind, Personality, and Memory]]
- [[03 - Assets, Expressions, and Display]]
- [[04 - Models, Research, and Privacy]]
- [[05 - Build and Verification Record]]
- [[Projects/README]]

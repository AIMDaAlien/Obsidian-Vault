---
project: Veyra Companion
status: Packaged app installed; Screen Recording and live approval pending
repository: /Users/aim/Downloads/Holo_Companion_Sprites
platform: macOS
updated: 2026-08-11
---

# Veyra Companion

## Purpose

Veyra Companion is Aim's private, local macOS companion. Veyra combines a persistent conversational mind, deterministic expressions, screen and cursor awareness, local research, and a dedicated-display interface. The repository, database path, Swift symbols, and asset IDs retain their historical `Holo*` names for compatibility.

She is not designed as an otome chatbot or engagement product. The goal is a perceptive long-term partner who can be warm, teasing, skeptical, disciplinary, and practically useful without pretending to be human.

Canonical repository: `/Users/aim/Downloads/Holo_Companion_Sprites`

## Current Status

**Packaged app installed; Screen Recording and live approval pending.**

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

Verified on 2026-08-11:

- The packaged app launches from its installed bundle and opens the shared mind database.
- The bundle contains all 67 portraits and 18 chibis.
- The `com.aim.holo-companion` LaunchAgent is installed and its RunAtLoad invocation succeeds.
- 26 Swift tests, release build, plist validation, code-sign verification, and app installation pass.
- Runtime proof confirmed one installed process, restored transcript history, and visible CLI action feedback without terminating the resident app.
- Repository commit `8433709` is pushed to `origin/main`.

Verified on 2026-08-10:

- 25 Swift tests pass.
- Release build passes.
- Warm local greeting completes end to end, including semantic appraisal and persistence.
- A three-round-cap research request completed through Unraid SearXNG and produced a local synthesis.
- The CLI event bridge writes to the shared Holo mind database.

Still awaiting proof or approval:

- Screen Recording permission and real OCR behavior; the installed app currently reports capture permission declined.
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

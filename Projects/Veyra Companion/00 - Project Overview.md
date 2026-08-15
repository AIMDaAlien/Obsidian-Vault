---
project: Veyra Companion
status: Installed build; Qwen3.5-4B fast/vision and Qwen3.8-27B heavy/research routing live; Fish S2 Pro speech external-output-only; 8-bit Fish benchmarked but not promoted
repository: /Users/aim/Downloads/Veyra_Companion_Sprites
platform: macOS
updated: 2026-08-15
---

# Veyra Companion

## Purpose

Veyra Companion is Aim's private, local macOS companion. Veyra combines a persistent conversational mind, deterministic expressions, screen and cursor awareness, local research, and a dedicated-display interface.

She is not designed as an otome chatbot or engagement product. The goal is a perceptive long-term partner who can be warm, teasing, skeptical, disciplinary, and practically useful without pretending to be human.

Canonical repository: `/Users/aim/Downloads/Veyra_Companion_Sprites`

## Current Status

**Margin Companion A is installed. Fast replies and visual awareness now run through bundled Qwen3.5-4B; deep, creative, and research work run through external Qwen3.8-27B. Bonsai is removed from the runtime, and Fish S2 Pro speech remains brief/proactive and external-output-only.**

Implemented:

- Typed mood, activity, and app-event expression selection across 85 approved assets.
- L01N8A detection by display name with persisted UUID fallback.
- Dedicated and portable display layouts, composer text sizing, and transparent-pixel hit testing.
- Fast brief/normal conversation through a bundled Qwen3.5-4B MLX worker on `127.0.0.1:8112`; deep, creative, and research conversation through external Qwen3.8-27B on `127.0.0.1:8110`; embeddings through LM Studio on `127.0.0.1:1234`.
- Automatic brief, normal, deep, creative, and research response modes.
- SQLite conversation, memory, commitment, activity, and embedding storage.
- Editable Mind panel.
- Cursor, poke-pressure, pat, idle-affect, foreground-app, visual screen context, and external development-event awareness.
- Bounded qualitative research through local SearXNG then the Unraid instance.
- Quiet-hour and daily-limit initiative policy.
- Native `Veyra Companion.app` bundle with bundled assets, login startup, and a consistent install path at `~/Applications/Veyra Companion.app`.
- Persistent composer restoration from SQLite, transient touch status, single-family sprite transitions, and observation-driven expression feedback with cooldowns.
- Permission-safe screen awareness: launch preflight only, plus a deliberate enable action in Mind Settings.
- Visual context replaces OCR: when a frame is available, Qwen3.5-4B produces a concise factual screen description into `awarenessContext`; frames are never stored and are not sent to Qwen3.8.
- Bundled Fish S2 Pro TTS with `EN-H`/`JA-B`/`AR-O`, whole mixed-language lines, external-output-only playback, and a hard MacBook-speaker block. The cached 8-bit Fish S2 Pro was benchmarked on `8124` and not promoted: warm was 4.05s versus the 3.5s gate.
- Mind uses the Field Notes palette, human-readable rows, useful empty states, current visual-context/privacy status, and hides stale OCR/error dumps when capture is disabled.
- Approved Field Notes Margin Companion in native AppKit: 593/687 dedicated-display split, 64/620/116 composer regions, large chronological turn rows, paper/ink styling, and New Topic/Mind-only permanent header controls.
- The dedicated layout now uses separate borderless windows for the transparent 593×800 portrait stage and opaque 687×800 composer. Aim physically confirmed Veyra is visible again with the desktop background showing through.
- SQLite topics with one-active-topic enforcement, historical-message migration, active-topic inference isolation, exact transcript restoration, and cancelled partial-output preservation.
- Return sends, Shift-Return inserts a newline, `Command-N` creates a topic, and text sizing lives in Mind while retaining `Command-Plus`/`Command-Minus`.
- Research writes a standalone Markdown report under `~/Documents/Veyra Research/` and returns a clickable local file pointer in chat. Before research starts, Veyra shows a non-blocking warning: “Close heavy apps before research.”

Verified on 2026-08-15:

Verified on 2026-08-15, small-lane swap:

- 44 Swift tests pass after the routing and shutdown changes.
- Release build, packaging, install, codesign, worker self-test, and selected-voice hashes pass.
- Installed app starts Qwen3.5-4B on `127.0.0.1:8112`; brief, normal, deep, and research `--core-check` paths all return real replies.
- Qwen3.5-4B visual QA correctly identified the active terminal window and command text without hallucinating missing content.
- Installed speech worker starts on `127.0.0.1:8123`; `/v1/warm` returns `204` and `/v1/speech` returns 24 kHz mono PCM16.
- `--diagnose` reports `Nothing Ear` as the eligible external output; built-in routes remain blocked.
- 8-bit Fish S2 Pro benchmark failed only the warm gate: `4.05s` versus `<= 3.5s`. Median generation speed was `0.982x` with no clipping, so the default remains the full Fish S2 Pro model.

Verified earlier on 2026-08-15:

- 44 Swift tests pass, including stage-cue removal, mixed-language handling, and external-output classification.
- Worker self-test, release build, package, codesign, bundled-worker hash, and selected-voice SHA-256 checks pass.
- The installed app starts the bundled worker on `127.0.0.1:8123`; warm returns `204` and generated audio is 24 kHz mono PCM16 with no clipping.
- `Nothing Ear` is the active external default, so speech is live; MacBook Pro Speakers and other built-in routes are rejected.

Verified on 2026-08-11:

- 32 Swift tests pass, including legacy database/defaults migration, topic isolation, exact resume, cancelled partials, Return/Shift-Return behavior, and Markdown research artifacts.
- Release build passes. Runtime diagnosis detects L01N8A at 1280×800 with a 593×800 portrait stage and 687×800 composer.
- Two signed installs pass strict code-sign verification with the same designated requirement: bundle ID `com.aim.veyra-companion` plus certificate SHA-1 `11e6fbcc37d446911d84f9a3f4ae9706bc3dace8`.
- The signed app is installed and running from `~/Applications/Veyra Companion.app`; its runtime diagnosis confirms the exact 1280×800, 593/687 dedicated layout.
- Aim physically confirmed the installed split-window build shows Veyra and the transparent desktop background on L01N8A.
- System Settings and the running app confirm Screen Recording is enabled. The activity database records the visual-context stream starting with Veyra windows and the dedicated display excluded.
- The previous database migrated transactionally to `~/Library/Application Support/VeyraCompanion/veyra-mind.sqlite3` with all 14 messages and one topic preserved; a closed backup remains under `Veyra Migration Backups`.
- The catalog and installed bundle contain 85 uniquely named Veyra assets: 67 portraits and 18 chibis.
- The old LaunchAgent is removed; `com.aim.veyra-companion` is installed and Veyra is running as the renamed executable.
- LM Studio retains only `veyra-fast`; the superseded fast and embedding aliases were unloaded.
- Bonsai correctly described the real composer screenshot at both 960 and 768 pixels. The Baidu Unlimited-OCR MLX conversion was rejected for live awareness after missing most UI text with its official prompt and hallucinating with a general extraction prompt.
- Structural commits `0b85f22`, `ee209ac`, `74c2330`, `c90310a`, and `81f3b0c` are pushed to the private `AIMDaAlien/Veyra_Companion_Sprites` GitHub repository.

Verified on 2026-08-10:

- 25 Swift tests pass.
- Release build passes.
- Warm local greeting completes end to end, including semantic appraisal and persistence.
- A three-round-cap research request completed through Unraid SearXNG and produced a local synthesis.
- The CLI event bridge writes to the shared Veyra mind database.

Still awaiting proof or approval:

- Audible brief/proactive speech through a real installed-app conversation, not just worker-level WAV proof.
- Live Qwen3.5-4B small-model replacement audition: current interim stays until a candidate passes multilingual short-reply conversation testing.
- Manual review of the Mind panel, pat gesture feel, initiative wording, and streamed composer behavior.

## Hardware and Privacy

- Host: 14-inch MacBook Pro, M5 Pro, 48 GB unified memory.
- Fast model API: bundled MLX worker at `127.0.0.1:8112` (`mlx-community/Qwen3.5-4B-MLX-4bit`).
- Deep/research model API: external Rapid-MLX worker at `127.0.0.1:8110` (`qwen3.8-27b-4bit`).
- Embedding model API: LM Studio at `127.0.0.1:1234`.
- Research search: `127.0.0.1:8082`, then Unraid `192.168.0.120:8082`.
- Dedicated display name: `L01N8A`; detected AppKit frame: 1280×800.
- Raw screen frames remain in memory and are never stored by Veyra. The current frame is downsampled to at most 768 pixels on its longest edge and JPEG-compressed before local visual analysis.
- Activity summaries expire after 24 hours; legacy OCR rows remain only in the migrated database and are no longer produced or shown as live context.
- Conversation history remains until Aim edits or deletes it.
- Search queries and public page requests may leave the LAN; memories, screenshots, legacy OCR dumps, and unrelated private context are not added to search queries.

## Links

- [[01 - Architecture and Implementation Plan]]
- [[02 - Mind, Personality, and Memory]]
- [[03 - Assets, Expressions, and Display]]
- [[04 - Models, Research, and Privacy]]
- [[05 - Build and Verification Record]]
- [[06 - Troubleshooting and Findings Log]]
- [[Projects/README]]

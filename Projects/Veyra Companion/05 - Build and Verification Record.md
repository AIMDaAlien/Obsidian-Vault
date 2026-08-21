---
tags: [local-ai]
project: Veyra Companion
updated: 2026-08-15
---

# Build and Verification Record

Historical entries below retain their exact former identifiers and commit titles. Current names are recorded here.

## 2026-08-15 — LFM2.5-VL-3B Fast and Vision Replacement

### Implemented

- Set the bundled fast lane to `LiquidAI/LFM2.5-VL-3B-MLX-4bit` on `127.0.0.1:8112`, replacing `mlx-community/Qwen3.5-4B-MLX-4bit`.
- Split conversation allowlisting by role: fast accepts only `lfm2.5-vl-3b`; deliberate accepts only `qwen3.8-27b`; Heretic, Bonsai, Qwen3.5, and legacy Qwen remain rejected.
- Raised the fast-lane context from 16K to 32K.
- Replaced the stale Bonsai test placeholder in `VeyraMindTests` with the new fast model and 32K context.
- Kept worker launch args, `/v1/models` warm polling, screen-description logic, endpoints, embeddings on `1234`, TTS, and research routing unchanged.

### Proof

- 44 Swift tests pass from `Controller`.
- `swift build -c release` passes.
- Release `--core-check` starts and warms LFM2.5-VL-3B on `8112`, returns a brief reply, and leaves `8110` and `1234` running.
- `http://127.0.0.1:8112/v1/models` reports `LiquidAI/LFM2.5-VL-3B-MLX-4bit`.
- `VEYRA_FAST_MODEL=qwen3.8-27b-4bit` is rejected by the fast allowlist; the release core-check still starts LFM2.5-VL-3B.
- `VEYRA_DELIBERATE_MODEL=LiquidAI/LFM2.5-VL-3B-MLX-4bit` is rejected by the deliberate allowlist; a deep core-check still succeeds through Qwen3.8 on `8110`.

### Open Gates

- Package, install, codesign, and installed-app physical-display/visual-context smoke remain deferred for this pass.
- The Qwen3.5-4B cache stays on disk for rollback only and is no longer a valid runtime conversation model.

## 2026-08-15 — Small-Lane Speech and Model Swap

### Implemented

- Added a bundled Qwen3.5-4B MLX worker on `127.0.0.1:8112` that Veyra starts, warms through `/v1/models`, and terminates on shutdown.
- Routed brief/normal/proactive and visual awareness through Qwen3.5-4B; deep/creative/research continue through external Qwen3.8-27B on `127.0.0.1:8110`.
- Kept embeddings on LM Studio `127.0.0.1:1234` only.
- Removed Bonsai from the runtime and restricted conversation model allowlisting to `qwen3.5-4b` and `qwen3.8-27b`; Heretic and legacy Qwen remain blocked.
- Replaced send-time OCR/image context with a concise Qwen3.5-4B screen description written into `awarenessContext`; Qwen3.8 never receives the image.
- Added the non-blocking research warning “Close heavy apps before research.” before `ResearchAgent.run`.
- Kept speech limited to brief replies plus proactive check-ins and external-output-only.
- Fixed shutdown orphaning so `VeyraRuntime.stop()` terminates the speech and fast-model workers synchronously.
- Tightened casual reply length: brief is one or two sentences at most 30 words, normal is two to four sentences at most 80 words, with token ceilings lowered to `256` and `768`.

### Proof

- 44 Swift tests pass after the shutdown patch.
- Speech worker `--self-test` passes; `DEFAULT_MODEL` remains `mlx-community/fish-audio-s2-pro`.
- Installed-app core checks pass for brief, normal, deep, and research.
- Qwen3.5-4B visual QA correctly identified the active terminal window and command text without hallucinating missing content.
- Installed speech worker `/v1/warm` returns `204`; `/v1/speech` returns 24 kHz mono PCM16.
- `--diagnose` reports `Nothing Ear` as the eligible external output; built-in routes remain blocked.
- Cached 8-bit Fish S2 Pro benchmark on isolated `8124`: 24 kHz mono PCM16, no clipping, median speed `0.982x`, but warm `4.05s` failed the required `<= 3.5s`. Not promoted.
- Installed-app brevity smoke: `me:hair` returned one short sentence with no question; a normal-lane request returned a direct multi-sentence reply under the new guidance.

### Open Gates

- Rebuild/package/install must be rerun after the shutdown patch and the installed app smoke-checked again.
- Subjective brief/proactive speech acceptance on real external audio remains open.
- Live small-model replacement audition remains open; Qwen3.5-4B stays interim until a candidate passes multilingual conversation testing.
- Long-run worker termination, memory, and idle/coexistence checks remain open.

## 2026-08-15 — Bundled Fish S2 Pro Speech Runtime and External-Only Routing

### Implemented

- Added a bundled Python stdlib speech worker for `mlx-community/fish-audio-s2-pro` with `warm`, `speech`, and `unload` endpoints.
- Mapped the selected identities `EN-H`, `JA-B`, and `AR-O` to their retained anchor WAVs and reference texts.
- Added `BundledSpeechWorker` to start and stop the worker from the installed app.
- Enabled speech by default while keeping the manual Mind toggle available.
- Hard-blocked built-in audio routes, including MacBook Pro Speakers; playback requires an eligible external output.
- Kept mixed-language replies as one synthesis pass and stripped `[stage cues]` before synthesis.

### Proof

- 44 Swift tests pass.
- Worker self-test, release build, package, strict codesign, bundled-worker hash, and selected-voice SHA-256 checks pass.
- Installed `~/Applications/Veyra Companion.app` and confirmed the running app started the worker on `127.0.0.1:8123`.
- Live worker: warm `204`; EN, AR, JA, and mixed lines returned 24 kHz mono PCM16 with no clipping.
- Measured warmed latency: EN p95 2.90s at 0.625x; AR 2.99s at 0.622x; JA 2.64s at 0.615x.

### Open Gates

- Subjective emotional listening and long-run memory/idle/coexistence checks remain open.

## 2026-08-11 — Portrait Compositor and Visual Context Repair

### Implemented

- Replaced noisy Vision OCR with send-time visual analysis through the existing Bonsai vision model.
- Aggressively reduced 1440p frames to a 768-pixel long edge and 55% JPEG before local inference.
- Reworked Mind into readable Field Notes rows with useful state and privacy summaries.
- Replaced the confusing disabled permission button with **Manage Visual Context** when capture is active.
- Split the dedicated portrait and composer into separate 593×800 transparent and 687×800 opaque borderless windows.

### Proof

- Commits: `8fa06a5`, `3d7680c`, and `452aa14`.
- 32 Swift tests, release build, packaging, installation, and strict code signing pass.
- System Settings, the running process, and the activity database confirm Screen Recording and visual-context startup.
- WindowServer reports the exact two-window geometry.
- Aim physically confirmed that Veyra is visible again and the desktop background shows through.

### Open Gate

- A real installed-app conversation must still prove that the captured 768-pixel frame reaches Bonsai and informs Veyra's reply.

Full failure evidence and discarded approaches: [[06 - Troubleshooting and Findings Log]].

## 2026-08-11 — Complete Veyra Rename and Structural Commits

### Implemented

- Split the approved prototype, native Margin Companion, signing work, code/assets rename, and packaging/storage rename into five structural commits.
- Renamed Swift modules, executable, bundle and LaunchAgent identifiers, defaults, model aliases, 85 catalog IDs, and all tracked asset paths to Veyra.
- Renamed the local repository and Obsidian project folders to `Veyra_Companion_Sprites` and `Veyra Companion`.
- Added one-time database and defaults migration; retired the previous LaunchAgent during install.

### Proof

- 32 Swift tests and the release build pass.
- The catalog contains 85 unique entries and every renamed runtime path exists.
- The signed installed bundle satisfies its designated requirement as `com.aim.veyra-companion`.
- Database migration preserved 14 messages and one topic; the old active storage directory and LaunchAgent are gone.
- Veyra is running from `~/Applications/Veyra Companion.app`; LM Studio retains only `veyra-fast`.
- Renamed the private GitHub repository to `AIMDaAlien/Veyra_Companion_Sprites`; `origin/main` and local `main` both resolve to `81f3b0c`.

### Open Gates

- The new bundle identifier reports `screenCaptureAuthorized=false`; Aim must grant Screen Recording once.
- Native visual acceptance remains open pending a fresh L01N8A screenshot.

## 2026-08-11 — Stable Screen Permission and Composer Study (Partial)

### Implemented

- Added a ten-year `Veyra Local Code Signing` certificate and private key to the login Keychain.
- Made packaging require that exact trusted code-signing identity; ad-hoc fallback is removed.
- Added `NSScreenCaptureUsageDescription`.
- Added launch-time `CGPreflightScreenCaptureAccess()` gating. When access is absent, Veyra does not construct or start `ScreenAwareness`.
- Added the deliberate **Mind → Settings → Enable Screen Awareness** action. Only that action calls `CGRequestScreenCaptureAccess()` and opens the Screen Recording privacy pane when access is still denied.
- Built six standalone responsive composer studies under `Prototypes/Veyra-Composer/`: Slate Ledger, Field Notes, Signal Board, Foundry, Cipher Wall, and Ash Frame.
- Recorded the raw local Qwen3.6-27B Q6_K briefs and critique. Production `ComposerView` remains unchanged pending Aim's selection.

### Proof

- All 26 Swift tests pass; release build, shell syntax, JavaScript syntax, Git whitespace, prototype HTTP routes, and the shared artwork route pass.
- Static color checks cover the primary text pairs; the weakest checked ratio is 4.68:1.
- Qwen was unloaded after the study. Bonsai is restored as `holo-fast` with 16K context, MTP, and a 30-minute TTL; `holo-embed` remains loaded. The local API returned exactly `Veyra core ready`.

### Open Gates

- The certificate is imported but not yet trusted for code signing. Packaging now fails fast with `Missing or untrusted Keychain identity: Veyra Local Code Signing` until Aim approves the one-time Keychain trust and private-key access prompts.
- The signed app has therefore not been installed, and stable designated-requirement retention across two rebuilds is not yet proven. The resident app remains stopped rather than relaunching the old ad-hoc build.
- Browser discovery returned `[]` (`No browser is available`). Desktop/portable screenshots, console, accessibility tree, focus order, rendered overflow, and layout-shift checks remain unverified; the gallery shows explicit capture placeholders.
- No prototype commit/push or production topic/UI work should proceed until browser proof is complete and Aim chooses a direction or hybrid.

### Composer narrowing

- Aim selected Field Notes as the strongest first-round direction and identified Signal Board as the weakest.
- The original Field Notes portrait was changed from a side-cropped fixed-height image to a contained silhouette with breathing room.
- Added four same-palette branches: Margin Companion, Open Folio, Pinboard, and Correspondence.
- Periwinkle and lavender are liked generally but were explicitly excluded from the Field Notes theme; its warm paper/tan/ink palette remains unchanged.
- Production `ComposerView` is still untouched. Browser discovery again returned `No browser is available`, so rendered visual proof remains open.
- Aim then locked Margin Companion as the only retained layout. Veyra now uses the portrait margin with exactly 10px above her, no left/right/bottom image inset, preserved aspect ratio, and no frame or quote overlay.
- The installed Qwen3.6-27B Q6_K was loaded as `veyra-design` at 32K context, proposed six turn structures, and critiqued them. Its retained directions were Turn Ledger, Focus Stage, and Two-Column Exchange; the raw review is preserved in `QWEN-MARGIN-TURNS.md`.
- Added the three retained clickable prototypes and a round-three gallery. All keep the Field Notes palette and mention only the planned voice model: `Qwen3-TTS 1.7B Base`.
- Qwen was unloaded and Bonsai was restored as `holo-fast` with 16K context, MTP, and a 30-minute TTL. The app core check returned exactly `Veyra core ready`.
- Static JavaScript, Git whitespace, required-control checks, and all new HTTP routes pass. Browser discovery still returns `[]`, so rendered desktop/portable and accessibility proof remains open.

## 2026-08-11 — State Repair and Public Rename

Repository commit: `8433709` (`Fix companion state and rename Veyra`), pushed to `origin/main`.

### Implemented

- Renamed the public UI and installed bundle to Veyra; retained the bundle identifier, database path, catalog IDs, and internal `Holo*` symbols for compatibility.
- Removed the stale development process that was producing a second sprite window.
- Changed transparent sprite drawing to replace old pixels and disabled portrait-to-chibi crossfades, preventing persistent mixed-family composites.
- Restored the latest 50 stored conversation messages into the composer after launch.
- Moved poke and pat copy into three-second header state so touch does not pollute or replace chat history.
- Closed reaction events before thinking or tool events begin, preventing hard-state leakage.
- Processed all unseen activity rows in order and added cooldown-limited attentive/thoughtful feedback for foreground-app and OCR changes.
- Kept image preprocessing native and memory-only, with a 1280-pixel longest-edge cap before Vision OCR.
- Moved `--emit-event` handling before AppKit startup so CLI feedback no longer starts or terminates a second UI instance.

### Proof

- 26 Swift tests pass, including image downsampling geometry.
- Release build, plist validation, shell syntax, Git whitespace, code signing, packaging, and installation pass.
- Accessibility inspection confirmed all 12 stored messages were visible after relaunch.
- A real `started`/`success` event appeared in the live transcript despite surrounding OCR/activity rows.
- The resident process PID survived a later CLI event and remained the only companion process.
- No file under `Assets/` changed.

### Open Gate

The ad-hoc rebuild invalidated the prior Screen Recording approval. macOS now reports `The user declined TCCs for application, window, display capture`; enable **Veyra Companion** under **System Settings → Privacy & Security → Screen & System Audio Recording**, then restart Veyra.

## 2026-08-11 — Packaged macOS App

Repository commit: `6ee6d9e` (`Package Holo as a login app`), pushed to `origin/main`.

### Implemented

- Added a native app bundle with identifier `com.aim.holo-companion`.
- Bundled `expression-catalog.json` and all runtime portraits and chibis.
- Installed the app at `~/Applications/Holo Companion.app`.
- Added a user LaunchAgent that opens Holo at login.
- Made bundled resources discoverable without relying on the repository working directory.
- Added one-command build and install through `./Scripts/package-app.sh --install`.

### Proof

- 25 Swift tests pass.
- Release build, plist validation, shell syntax, Git whitespace, and code-sign verification pass.
- The installed process runs from the app bundle and opens `holo-mind.sqlite3`.
- Installed asset counts are 67 portraits and 18 chibis.
- The live display diagnostic still detects L01N8A in dedicated mode.

### Open Gate

ScreenCaptureKit still reports `The user declined TCCs for application, window, display capture`. Aim must enable Holo Companion under **System Settings → Privacy & Security → Screen & System Audio Recording**, then restart the app.

This Mac has no Apple code-signing certificate. The installer therefore uses an ad-hoc signature. Apple ties privacy approval to that exact build, so a code rebuild may require Screen Recording approval again. Set `HOLO_CODESIGN_IDENTITY` to an installed Apple Development or Developer ID certificate when one is available.

## 2026-08-10 — Mind and Awareness Foundation

Repository commit: `331d4ef` (`Build persistent Holo mind and research awareness`), pushed to `origin/main`.

### Implemented

- Added `HoloMind` Swift target with SQLite persistence, embeddings, retrieval, memory consolidation, commitments, activity expiry, and initiative policy.
- Replaced fixed response size with automatic brief, normal, deep, creative, and research plans.
- Replaced combined reply/metadata JSON with streamed visible prose and a background structured appraisal.
- Added bounded qualitative `ResearchAgent` with SearXNG local-first failover, HTML fallback, evidence gap rounds, source fetching, query sanitization, and SSRF protection.
- Added foreground-app awareness, ScreenCaptureKit capture, Vision OCR, and 24-hour observation storage.
- Added causal affect, pat recognition, poke decay, affect-driven idle expression choice, and initiative scheduling.
- Added the Mind panel and CLI development-event bridge.
- Changed dedicated-display resolution to prefer the live `L01N8A` display name before stored UUID fallback.

### Automated Proof

Commands:

```sh
cd /Users/aim/Downloads/Holo_Companion_Sprites/Controller
swift test
swift build -c release
```

Results:

- 25 tests passed.
- Release build passed.
- No image or catalog file changed.

Coverage includes:

- Typed catalog integrity and hard-event precedence.
- Deterministic tap history and restoration.
- Poke escalation and decay.
- Pat detection and affectionate restoration.
- Affect decay and idle variation.
- Task-aware response planning.
- SQLite messages, memories, commitments, correction, and activity expiry.
- Initiative quiet hours, spacing, and daily limit.
- Search-query sanitization and private-network URL blocking.
- SearXNG HTML parsing when JSON output is disabled.
- Dedicated and portable geometry.

### Runtime Proof

CLI event:

```sh
.build/debug/HoloCompanion --emit-event started \
  --activity toolRunning \
  --summary 'Runtime proof started' \
  --repo '/Users/aim/Downloads/Holo_Companion_Sprites'
```

Verified the event in `holo-mind.sqlite3` as `started|toolRunning`.

Warm conversational proof:

```sh
.build/release/HoloCompanion --core-check 'hiya'
```

- Stream, semantic appraisal, and persistence completed.
- Measured wall time after model load: approximately 4.37 seconds including appraisal.
- Holo incorporated the recorded runtime event rather than inventing activity.

Research proof:

```sh
.build/release/HoloCompanion --core-check \
  'Research whether Qwen3.6-35B-A3B supports MTP, with sources.'
```

- Used Unraid SearXNG HTML fallback.
- Completed the bounded evidence/gap loop and local synthesis.
- Measured wall time: approximately 69.25 seconds.
- Deterministic URL appendix was added after this proof because model-authored numbered citations did not guarantee visible links.

### Not Yet Proven

- Normal graphical launch with Screen Recording permission. The launch reached ScreenCaptureKit, but macOS reported: `The user declined TCCs for application, window, display capture`.
- Visual review on L01N8A after restarting the already-running older Holo process. Diagnostic resolution succeeded at 1280×800 with a 584-point stage and 695-point composer.
- Mind panel editing and deletion by hand.
- Pat thresholds under real cursor movement.
- Proactive intervention timing over a full day.
- Q2/MTP versus 4-bit model benchmark and final deliberate-model selection.
- Current-frame vision-language interpretation; the implemented awareness foundation uses native app metadata and OCR.

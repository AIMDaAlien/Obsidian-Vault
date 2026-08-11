---
project: Holo Companion
updated: 2026-08-11
---

# Build and Verification Record

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

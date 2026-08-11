---
project: Holo Companion
updated: 2026-08-10
---

# Build and Verification Record

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

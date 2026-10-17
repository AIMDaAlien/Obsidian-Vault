---
tags: []
created: 2026-10-12
publish: true
machine: mac
engine: mlx
project: Local Language Engine
---
# Prompt: Mac-native Local Language Engine (Arabic-first tutor)

Copy everything below the line into a coding agent.

---

You are building "Majlis for Mac" — a private, local language tutor that runs
entirely on Aim's MacBook Pro (Apple M5 Pro, 18 cores, 48 GB unified memory,
macOS 26). Everything — inference, speech recognition, speech synthesis, lesson
data, recordings — stays on this machine. No cloud AI services, no telemetry.

This is a Mac-native rebuild of a proven Android-first design. Keep the
architecture and policies below; replace the Android phone client with a
native macOS experience so everything lives on one machine.

## Hardware and hard budget

- Host: MacBook Pro `Mac17,9`, Apple M5 Pro, 48 GB unified memory.
- Hard application ceiling: **36 GB resident memory** for the entire
  application (model weights, KV cache, speech models, buffers, services,
  SQLite). The OS keeps the remaining ~12 GB. Swap-heavy behavior or an
  OOM crash is a failed test, not a tuning problem.
- Measure peak resident memory and wired memory in every benchmark and report
  real numbers. Configuration claims are not proof.

## Model and inference

- Tutor model: Qwen3.6-35B-A3B, 4-bit, via MLX on Apple Silicon.
- Active context target: 128K tokens. Note: this hybrid MoE model has had
  long-context and prefix-cache issues in MLX — a measured 128K prefill under
  the 36 GB ceiling is a **Phase 1 gate**. On the prior Android build a
  measured 126,512-token prompt took ~165 s and ~33 GiB wired memory: it fits,
  but only narrowly, so treat compaction as mandatory, not optional.
- Speech recognition: MLX Whisper `large-v3-turbo` (streaming partials + finals).
- Speech synthesis: local, short-lived signed WAV delivery; Arabic voice first,
  Japanese voice second.

## Architecture (single machine now)

One Python host service (the proven core) plus a native Mac front end:

```
Mac
├── language_engine/ (Python service)
│   ├── gateway        # local HTTP/WebSocket API, versioned /v1
│   ├── session        # lesson/session coordinator: listen→transcribe→tutor→speak
│   ├── asr            # MLX Whisper streaming ASR (per-language prompt)
│   ├── tutor          # Qwen3.6-35B-A3B 4-bit / MLX
│   ├── tts            # local synthesis → short-lived signed PCM WAV
│   ├── context        # lesson-aware context manager (see policy below)
│   ├── policy         # MSA canon + reviewed Hijazi layer (per-language packs)
│   ├── audit          # recordings, transcripts, corrections, review states
│   ├── prep           # provenance-preserving lesson-preparation worker
│   └── db             # SQLite (WAL): lessons, turns, memory, audit, review
└── mac_app/ (SwiftUI or Tauri front end; see Interface)
```

The front end may talk to the service over localhost loopback with the same
versioned JSON protocol; keep protocol schemas in a shared `packages/protocol`
(data contracts only). Do not invent shared abstractions beyond that.

## Context and durable memory policy

1. Session context is assembled from: tutor/language policy → current lesson
   objective + approved vocabulary → recent verbatim turns → compacted lesson
   episodes → explicit learner memory/corrections/approved cards.
2. Under 80K tokens: keep recent turns verbatim.
3. At 80K: compact the oldest completed lesson segment into a durable episode
   (source turn range, objective, vocabulary, recurring errors, corrections,
   learner preferences, factual summary). Append-only and idempotent.
4. At 112K: block the next model turn until enough compaction happens.
5. At 128K: reject safely; never truncate policy or the current learner turn.
6. Episodes survive process restart in SQLite. Raw recordings and transcripts
   stay auditable.

## Arabic teaching policy (the release gate)

- Modern Standard Arabic (MSA) is canonical for explanations and formal examples.
- Hijazi dialect is a *labeled* conversational-suggestion layer, never
  presented as MSA. Unreviewed model suggestions are stored as suggestions,
  never as truth.
- A suggestion becomes an approved learning card ONLY after explicit human
  review (compare recording, transcript, MSA correction, Hijazi alternative,
  confidence, source lesson). Card creation before review must be impossible.
- Arabic text must be explicitly RTL with directional isolation for mixed
  Arabic/Latin content (e.g. the literal "MSA" label), including punctuation,
  numerals, and selection behavior.

## Teaching quality — where this build must BEAT the Android version

The Android build proved the pipeline but was weak as a beginner teacher.
This build's core feature is a real beginner pedagogy loop:

1. **Structured curriculum, not chat improv.** A lesson is an explicit unit:
   objective, target vocabulary/grammar, example exchanges, and exercises.
   The tutor stays inside the lesson objective; off-topic drift is redirected,
   not silently followed.
2. **Explicit correction modes.** After each learner turn, the tutor produces:
   the corrected MSA version, a short explanation of what changed and why
   (in beginner-friendly English), the Hijazi natural alternative (labeled),
   and transliteration. All of it is stored for review.
3. **Comprehensible input and scaffolding.** Beginner stages constrain the
   tutor's vocabulary to already-learned words plus a small set of new words
   per lesson (i+1). The tutor may not use untaught grammar silently.
4. **Spaced repetition built in.** Approved cards export to an SRS queue
   (FSRS/SM-2) with daily review sessions inside the app, tied back to the
   lesson and the recording where the word/structure appeared.
5. **Speak-first drills, not just conversation.** Per lesson: repeat-after-me
   prompts, translation drills both directions, and free conversation once
   enough vocabulary is confirmed. Pronunciation feedback compares learner
   audio against reference audio (even a coarse similarity score helps).
6. **Every tutor reply ships with an accurate English meaning and
   transliteration for beginner stages** — this was an unfinished item on the
   Android build; make it a hard acceptance test here.
7. **Japanese as an isolated language pack** — its own tutor policy, ASR
   language, TTS voice, LTR content styles. It must not weaken Arabic RTL
   behavior in any way. Ship it only after the Arabic loop is stable.

## Interface (Mac)

A dark, focused "listening room," not a dashboard:

- Near-black indigo surfaces, warm-white Arabic text, one warm accent.
  Very Peri as the dynamic session color. Restrained glass only on the live
  transcript and transport controls.
- Large Arabic type, explicit RTL lesson regions, min 44pt touch-target
  equivalents for controls, reduced-motion honored.
- Live state is unmistakable: listening / thinking / speaking / paused / offline.
- Microphone permission requested explicitly; a visible live level meter;
  push-to-talk AND hands-free modes; recording consent OFF by default.
- Progressive interface language, four reversible stages stored locally,
  advanced only by explicit learner confirmation of each vocabulary bundle:
  1. Trailhead — English controls, RTL Arabic lesson content, essential-word compass
  2. Bridge — English-led bilingual controls
  3. Guided Arabic — Arabic-led with English rescue text
  4. Immersion — Arabic-led, with Guide and step-back always available
  Never promote based on taps alone.

For the front end, prefer SwiftUI (native, small footprint) or Tauri if web
tech is needed; either must stay inside the memory budget and keep the
service as the only source of truth.

## Data, privacy, audit

- All data in local SQLite + local media directory; backup/restore with
  checksum verification and rollback artifacts.
- Every consented recording maps to session, turn, transcript, correction,
  review decision, and deletion audit event. Deletion requires confirmation
  and writes an audit event.
- Local API on loopback; the 32-character shared-key API and five-minute
  signed media tickets carry over from the Android design (playback clients
  must never see the host key in a URL).
- No camera access. No network egress except model updates the user triggers.

## Repository layout

```
language-engine-mac/
├── README.md
├── .env.example
├── apps/
│   ├── host/                 # Python service (as above)
│   │   ├── language_engine/
│   │   └── tests/
│   └── mac_app/              # SwiftUI or Tauri client
├── packages/
│   └── protocol/             # versioned JSON schemas/fixtures
├── scripts/                  # local proof commands (benchmarks, smoke tests)
└── var/                      # ignored SQLite, media, caches, benchmark reports
```

## Acceptance gates (do these in order; record evidence for each)

### Phase 1 — model and context proof
- Exact 4-bit model loads via MLX and answers an Arabic prompt.
- Measured 128K prefill completes under 36 GB resident memory without
  destabilizing macOS. Record peak RSS/wired, prefill latency, first-token
  latency, decode rate.
- Context tests: compaction at 80K, forced at 112K, hard reject at 128K;
  never silent truncation.
- Durable episodes survive restart in SQLite.

### Phase 2 — live loop on the Mac
- Mac mic → streaming Whisper transcript → tutor streaming text → signed WAV
  playback, with interruption stopping playback and returning to listening.
- Live events: start, partial, final, tutor deltas, final reply, interruption,
  idempotent turn persistence.
- MSA and reviewed Hijazi content visibly distinct; RTL correct at every stage.

### Phase 3 — teaching loop and audit
- Lesson structure, correction modes (i+1 constraint), and SRS review work
  end to end.
- Every tutor reply carries accurate English meaning + transliteration.
- Suggestion → review → approved card flow; card creation impossible before
  review. Recording audit/replay/edit works.

### Phase 4 — hardening and Japanese
- Backup/restore, SQLite integrity, media integrity, schema migration.
- Autostart as a launchd service with health recovery and logs.
- Combined stress test: 128K context + concurrent ASR/TTS under the memory
  ceiling, plus battery/thermal observation.
- Japanese language pack behind the same gates, Arabic RTL untouched.

## Working rules

- Run on the real machine and measure; never claim a gate passed from config
  alone. Write pass/fail evidence into `var/reports/`.
- Build the smallest thing that proves a gate before adding product features.
- Privacy is absolute: nothing leaves the machine unless the user triggers it.
- Prefer boring, verifiable, standard-library-heavy choices over frameworks.

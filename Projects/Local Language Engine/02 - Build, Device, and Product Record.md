---
tags: [guide, hardening, local-ai, hardware-constraints]
project: Local Language Engine
status: Standalone Android and beginner UI proven — release hardening active
repository: /Users/aim/Documents/language-engine
device: OnePlus 12 CPH2583 — Android 16 / API 36
updated: 2026-07-30
---

# Build, Device, and Product Record

## What exists now

Majlis is a locally built Android application backed by a private Mac language
server. The phone owns the live lesson experience; the Mac owns model inference,
authoritative SQLite data, approved learning memory, and media.

The baseline physical-device loop has passed:

```text
OnePlus microphone
  → WebRTC audio
  → private Tailscale HTTPS
  → MLX Whisper Arabic transcription
  → local tutor response
  → short-lived signed PCM WAV
  → OnePlus playback
```

The installed release runs with Metro stopped and without `adb reverse`. Expo Go
is not involved.

## Hardware and measured model proof

### Mac authority

- 14-inch MacBook Pro (`Mac17,9`)
- Apple M5 Pro, 18 cores
- 48 GB unified memory
- macOS 26.5 at implementation
- Hard application ceiling: **36 GB resident memory**

### Long-context model

- Qwen3.6-35B-A3B, 4-bit, through MLX
- Active context target: **128K tokens**
- Measured 126,512-token prompt: **165.6 seconds**
- Measured wired-memory growth: **32.92 GiB**
- Lesson compaction begins at 80K and is mandatory at 112K
- The current learner turn and tutor/language policy are never silently dropped
- MTP remains optional and benchmark-gated

The 128K result fits the 36 GB rule, but only narrowly. Concurrent speech,
compaction, model generation, and total resident memory still need a combined
stress run before this is treated as dependable.

## Mobile stack

| Part | Current choice |
|---|---|
| Native toolchain | Expo 56.0.18, used locally |
| UI runtime | React Native 0.85.3 / React 19.2.3 |
| Language | TypeScript 6.0.3 |
| Live transport | React Native WebRTC 124.0.8 |
| Offline data | Expo SQLite 56.0.5 in WAL mode |
| Audio playback/capture support | Expo Audio 56.0.13 |
| Arabic type | IBM Plex Sans Arabic |
| Android target proven | OnePlus 12, Android 16 / API 36 |

Expo OTA updates are disabled. Builds are assembled on Aim's Mac, so there is no
required Expo subscription, cloud build queue, deployment quota, or Expo-hosted
application data.

## Host and data stack

- Python host service and versioned `/v1` APIs
- MLX local inference on Apple Silicon
- MLX Whisper `large-v3-turbo` for Arabic speech recognition
- WebRTC audio plus a structured lesson event channel
- Mac-owned SQLite lesson, audit, review, sync, and memory records
- Local filesystem recordings and prepared media
- Five-minute signed media tickets; the host key is never placed in a media URL
- Mobile lesson cache, idempotent outbox, and explicit sync-conflict review
- Backup/restore, SQLite integrity, checksum, and media-path checks

## Arabic policy and learning safety

- MSA is the written and grammatical foundation.
- Hijazi alternatives are labeled conversational variants.
- Model-generated Hijazi text stays pending until Aim reviews it.
- A pending suggestion cannot become an approved learning card.
- Recording consent is off by default.
- Recordings remain tied to their transcript, correction, review decision, and
  deletion audit event.
- Arabic lesson regions explicitly use RTL; Latin and Japanese regions use LTR.
  Mixed scripts use directional isolation instead of relying on accidental
  device layout behavior.

## Beginner interface contract

Aim is beginning without enough Arabic for an Arabic-only interface. The shell
therefore grows with him:

| Stage | What Aim sees | Exit condition |
|---|---|---|
| Trailhead | English controls, Arabic lesson examples, essential-word compass | Aim confirms the first bundle |
| Bridge | English-led bilingual controls | Aim confirms the second bundle |
| Guided Arabic | Arabic-led controls with English rescue text | Aim confirms the third bundle |
| Immersion | Arabic-led application with Guide and step-back always available | Manual choice |

The stage is stored locally on the phone. It is reversible. The application
must not promote Aim merely because he tapped through a screen; later automatic
support may use real spaced-repetition mastery evidence.

Implemented on the OnePlus:

- Trailhead starts the application chrome in English.
- Bridge adds directionally isolated Arabic beside familiar English.
- Guided Arabic reverses that emphasis.
- Immersion makes Arabic primary without removing the Guide or step-back path.
- Live Arabic text stays explicitly RTL at every stage.
- The Android status bar hides automatically while the app is focused.
- The consent switch remains inside its track in both physical states.

## Visual record — 2026-07-30

### Trailhead: English safety line with Arabic lesson content

![[Assets/Majlis - Progressive Trailhead.png|360]]

### Bridge: English-led bilingual controls

![[Assets/Majlis - Progressive Bridge.png|360]]

### Full-screen lesson and corrected consent switch

| Off | On |
|---|---|
| ![[Assets/Majlis - Switch Off.png\|260]] | ![[Assets/Majlis - Switch On.png\|260]] |

The on-state screenshot shows the switch reported as enabled by Android
accessibility while its knob remains inside the ellipse. The top status bar is
absent; the bottom navigation gesture remains available intentionally.

## Privacy and network boundary

- Tailscale Serve currently publishes the host only inside Aim's private
  tailnet: `https://macbook-pro.tail7124d6.ts.net/`.
- The phone does not require the Mac's LAN address and can reach it remotely
  while both devices are connected to Tailscale.
- Camera and `SYSTEM_ALERT_WINDOW` permissions are blocked.
- Expo's update service is disabled.
- The present test build has not yet provisioned the supported 32-character API
  key, so Tailscale is currently the sole active trust boundary.

## Distribution state

The standalone APK is real, but it is not a public-store release:

- JavaScript is embedded in the APK.
- The release build is non-debuggable.
- The current APK uses the Android debug signing certificate.
- A permanent private release key is required before durable personal
  installation or Play Store distribution.

Latest verified local artifact:

- Package: `com.aim.languageengine`
- Version: `0.1.0` / version code 1
- Target: Android API 36
- APK size: 116 MB
- SHA-256:
  `2de0b2471352013938ceb06ef1c8f5febfda3750c928b47def51037d7143b133`

The Mac remains the server by design. A standalone phone app means it no longer
depends on Metro, USB, or Expo cloud services; it does not mean the 35B tutor
model moves onto the phone.

## Remaining gates

1. Permanent Android release signing and safe key backup.
2. Application API key provisioning over the Tailscale boundary.
3. Mac service autostart, health recovery, and logs.
4. Physical-phone interruption, reconnect, offline replay, and consent audit.
5. Packet loss, degraded network, battery, thermal, storage, and combined
   128K-plus-audio memory tests.
6. Accurate generated-reply English meaning and transliteration for beginner
   stages.
7. Bounded offline audio downloads.

## Links

- [[00 - Project Overview]]
- [[01 - Architecture and Implementation Plan]]
- Repository: `/Users/aim/Documents/language-engine`

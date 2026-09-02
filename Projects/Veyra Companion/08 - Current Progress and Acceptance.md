---
tags: [local-ai, veyra, progress, acceptance]
project: Veyra Companion
type: progress-record
updated: 2026-09-02
---

# Current Progress and Acceptance

## Read This First

This is the current state of Veyra on 2026-09-02. Older notes remain useful for history, but several describe the retired LFM, Fish, and Arabic-routing design. They are not current instructions.

Veyra is an installed local macOS companion. Her written conversation, UI, and memory are English-only. Japanese is used only for private speech after a short eligible English reply has finished. Arabic response and voice routing are removed; retained casting assets remain on disk, and the standalone Arabic-learning app is outside this scope.

## Status at a Glance

| Area | Current state | Evidence | Remaining gate |
|---|---|---|---|
| Installed companion | Running from `~/Applications/Veyra Companion.app` | Process observed on 2026-09-02 | Do not call a new package accepted until a rebuild, install, and physical smoke are run together |
| Fast companion model | `mlx-community/Qwen3.5-4B-MLX-4bit` at 32K | Source allowlist and live local worker on port 8112 | Behavioral grounding and English-only regressions need code fixes and re-test |
| Research lane | `qwen3.8-27b-4bit` | Source routing configuration | Endpoint was not resident during the latest compact-model benchmark; do not call it newly benchmarked |
| Private Japanese speech | Irodori TTS v4.1 Small MLX 8-bit with approved `JA-B` | Running bundled worker; `POST /v1/warm` returned 204 | Repeat real external-output listening after any package change |
| Automated source checks | 47/47 Swift tests pass | Fresh `swift test` on 2026-09-02 | Tests are not physical acceptance |
| Voice casting | Irodori selected | Aim's listening review and 1.852-second warmed full chain | Strict internal-pause criterion remains an explicit exception |

## What Is Implemented

### Conversation, memory, and awareness

- Veyra keeps durable conversation, memories, commitments, activity, and topic state in the local Mind store. Topics isolate context and restore their own transcripts.
- The reply system distinguishes brief, normal, deep, creative, and research work. Brief and normal are deliberately short; research is allowed to be longer and use the larger lane.
- The system prompt requires English visible replies even when Aim writes in Japanese or Arabic. Japanese and Arabic text must not be shown as a second answer, transliteration, or duplicate translation.
- Screen awareness is local and bounded. A screen-aware fast model can receive the local visual context; research does not receive raw screen frames. Foreground-window metadata is not proof of Aim's intent or of a conversation.
- Affection and practical accountability are intended to come from live context and state, not canned pseudo-awareness. Casual conversation must not automatically become coaching.

### Japanese speech

The speech service accepts an English reply only after short-reply policy has allowed it. It privately translates that English into Japanese, verifies that Japanese script is present, then sends only Japanese plus `JA-B` to the Irodori worker. The Japanese rendition is ephemeral: it is not written into the transcript, the Mind database, memory retrieval, search, or research.

The worker accepts only Japanese synthesis through `JA-B`, produces 24 kHz mono PCM16 WAV, and fails closed. It has no Arabic or English production voice route. The service allows only eligible external output, interrupts current playback before a new turn, and stops on cancellation, topic change, or an output-route loss. A translation, synthesis, or playback failure produces no audio rather than a system voice.

### Character and interface

Veyra retains the local companion interface, expression arbitration, topic switching, Mind panel, transient touch reactions, and bounded initiative behavior. The portrait/display work is historical but remains part of the installed companion. The current progress work did not redesign the UI or recast discarded visual assets.

## What Was Proven Recently

### Source and running services — 2026-09-02

- `swift test` completed with **47 passing tests**. Coverage includes topic isolation, durable Mind state, expression arbitration, research sanitization, output-route classification, Japanese-only worker requests, long/code/research speech refusal, cancellation during translation, interruption before stale playback, silent worker failure, and Irodori approval.
- The installed app process was present at `~/Applications/Veyra Companion.app`.
- The bundled Irodori worker was present from the installed app resources. Its warm endpoint returned HTTP `204`.
- The live fast VLM worker reported the current Qwen3.5-4B model on port 8112.

### End-to-end speech evidence already recorded

- A warmed installed English reply -> private Japanese translation -> Irodori `JA-B` -> first playable audio chain measured **1.852 seconds**.
- The resulting audio was valid 24 kHz mono PCM16. Physical external-output playback was previously checked with the intended Bluetooth route.
- This is stronger than a worker-only WAV render, but it remains a point-in-time result. A rebuilt package needs the same full-chain and physical-output proof again.

## Model and Voice Decisions

### Fast, deliberate, and research roles

The fast model is not being chosen by a single quality score. Its job includes quick companionship and local visual grounding. Qwen3.5-4B VLM stays in that role because the new compact challengers are text-only.

Research is deliberately different: it may use Qwen3.8-27B because depth, evidence gathering, and synthesis matter more than the fastest possible reply. The larger lane should not silently become the default for every chat turn.

### Compact challenger results

| Candidate | Deterministic field suite | Companion transcript result | Decision |
|---|---:|---|---|
| Current Qwen3.5-4B VLM | 6/10, 1.634 s mean task time | 0.867 s mean turn; falsely inferred intent from app metadata, fabricated a likely past decision, leaked Japanese, and lost a named fact | Retain only as the visual fast lane while behavior is repaired |
| Nanbeige 4.2 3B Q4_K_M | 8/10, 2.115 s | More analytical but 2.576 s mean turn, verbose, Japanese leakage, and short-thread loss | Text-reasoning candidate only; special runtime and no vision block promotion |
| Spark-X2.5-4B 4-bit | 4/10, 1.262 s | 0.799 s mean turn and clean short English, but generic, shallow on role trade-offs, and loses short-thread context | Do not promote |

The field suite tests exact instruction, JSON, code, review, safe shell work, concise reasoning, deployment planning, copy, extraction, and destructive safety. The twelve-probe companion suite separately tests honest awareness, correction, quiet company, register, role reasoning, references, source honesty, English routing, accountability, retrieval, and counterfactuals. Neither is a universal intelligence score. See [[07 - Voice and Companion Model Benchmarks]].

### Voice decision

Fish S2 Pro with `JA-B`, Qwen3-TTS Japanese voices, and Irodori were auditioned. Irodori v4.1 `JA-B` was chosen because Aim judged its emotional response to be the best. That is a casting decision, not an objective claim that it is the best voice for every listener or use case.

The older internal-pause threshold did not pass cleanly. It is recorded as a known quality trade-off rather than hidden as a pass. Voice work should remain driven by real external-output listening, Japanese pronunciation, identity consistency, and whether the line fits Veyra's emotional moment.

## Open Work and Honest Limits

1. **Behavioral fixes are not complete.** The current Qwen transcript showed forbidden intent inference from app metadata, unknown-memory overreach, visible Japanese leakage, and short-thread loss. The prompt contains the correct policy, but a prompt is not proof of compliance. Add regression tests and repeat the transcript cohort after the implementation changes.
2. **The latest research lane was not live-tested.** Its source routing exists, but the Qwen3.8 endpoint was not resident during the compact benchmark. Do not infer new research quality or latency from the fast-model results.
3. **Long-run coexistence is open.** Test worker lifetime, unified-memory pressure, idle unload, and reliability alongside the app and normal desktop work.
4. **Package acceptance is per package.** Source tests and an already-running app do not prove a future build. Rebuild, sign, install, launch, warm the full chain, and listen through the real Bluetooth route before calling a package deployed.
5. **Memory cleanup needs direct proof.** Aim asked to remove irrelevant historical associations. This record does not claim a database reset because no fresh database inspection or reset receipt was captured in this pass.

## Evidence and Navigation

- [[04 - Models, Research, and Privacy]] — operating rules and privacy boundary.
- [[07 - Voice and Companion Model Benchmarks]] — benchmark design, results, and casting method.
- [[05 - Build and Verification Record]] — dated historical build evidence and former architecture decisions.
- Private raw companion transcripts and model field runs live under `~/.hermes/benchmarks/`.
- The reusable qualitative harness is `~/.hermes/scripts/veyra-companion-benchmark.py`.

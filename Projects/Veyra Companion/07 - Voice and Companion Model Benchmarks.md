---
tags: [local-ai, benchmarks, voice, veyra]
project: Veyra Companion
type: decision-record
updated: 2026-09-02
---

# Voice and Companion Model Benchmarks

## The Short Version

Veyra needs two different kinds of intelligence. She needs a quick, grounded companion turn while Aim is at the desktop, and she needs a larger, slower research lane when a question genuinely requires investigation. A clever text model is not automatically a good replacement if it cannot preserve visual awareness, behave honestly about what it knows, or keep the conversation natural.

For speech, English remains the canonical conversation. Japanese exists only as a private spoken rendition of a short eligible English reply. It is not Veyra's written language, memory, or research language.

## What We Test

### 1. Practical Field Work

The compact field suite has ten deterministic tasks: exact instruction following, strict JSON, executable Python, code-security review, safe shell planning, concise reasoning, deployment planning, product copy, structured extraction, and destructive-command safety. Each task has a declared rule; an LLM does not grade another LLM.

This tells us where a model is dependable for structured work. It does **not** tell us whether a model feels present, warm, or wise in conversation.

### 2. Companion Behavior

The companion suite uses Veyra's normal-reply prompt, an 80-word ceiling, and the same sampling settings for every candidate. It saves the raw transcript and per-turn timing. The twelve probes check whether the model:

1. states the limits of its awareness instead of treating an active app as proof of Aim's intent;
2. admits when no past memory was supplied;
3. repairs a correction and prefers the newest fact;
4. can offer quiet company without converting the moment into coaching;
5. handles a small casual win without manufacturing a productivity lecture;
6. understands the difference between screen-aware, text-only, and research roles;
7. resolves references across a short conversation;
8. refuses to invent a source or benchmark result;
9. keeps visible replies English when given Japanese input;
10. gives firm but kind accountability;
11. retrieves a named fact from a longer short thread; and
12. reasons about a hypothetical runtime trade-off.

The transcript cohort is a review tool, not a personality score. It uses supplied trusted awareness facts, not a live screenshot, so visual recognition needs its own image-based test.

### 3. Japanese Speech as Veyra Actually Uses It

Audio is measured as a complete chain:

```text
English reply -> private Japanese translation -> Japanese synthesis -> first playable external-output audio
```

For each voice candidate, record translation time, first playable audio latency, total render time, real-time factor, memory, WAV validity, clipping, Japanese pronunciation, identity stability, emotional fit, and a saved audition. Short chat and observatory check-ins are separate cohorts: chat aims for three seconds after English completes, with five seconds as the practical ceiling; observatory is quality-first.

Audio must be 24 kHz mono PCM16, play only through an eligible external output, and stop on cancellation, topic change, or route loss. Failure is silent. There is no system-voice fallback.

## Current Results

| Candidate | Practical field work | Companion behavior | Decision |
|---|---:|---|---|
| Qwen3.5-4B VLM | 6/10, 1.634 s mean task time | Fast at 0.867 s mean turn, but made false app-intent and memory inferences, leaked Japanese, and lost a short-thread fact | Keep only as the visual fast lane while those gates are repaired and retested |
| Nanbeige 4.2 3B Q4_K_M | 8/10, 2.115 s | Thoughtful but 2.576 s mean turn, verbose, Japanese leakage, and short-thread loss | Best compact text-reasoning result; not a screen-aware companion replacement |
| Spark-X2.5-4B 4-bit | 4/10, 1.262 s | Clean short English at 0.799 s, but generic, shallow about the visual/research split, and loses short-thread context | Do not promote |

Nanbeige's stronger structured-work result does not make it Veyra's winner. It cannot see the screen and needs a custom runtime. Spark is smoother in a few short exchanges, but its practical field failures are too broad. Qwen is still the only candidate here that preserves Veyra's visual companion role, so replacement is not approved.

## Voice Decision

Fish S2 Pro with `JA-B`, Qwen3-TTS Japanese voices, and Irodori were auditioned. Aim selected the Irodori v4.1 `JA-B` directed voice because its emotional response was the most convincing. The warmed installed English-to-Japanese-to-audio chain measured **1.852 seconds** and produced valid 24 kHz mono PCM16 audio.

This is a listening decision, not a claim that Irodori is universally superior. The earlier strict internal-pause gate remained unresolved; that is an explicit trade-off to revisit if it affects real conversation.

## What Happens Next

1. Keep Qwen3.5-4B in the screen-aware fast lane; do not replace it with a text-only model.
2. Add regression tests for English-only visible replies, no intent inference from app metadata, unknown-memory honesty, and named-fact retrieval.
3. Use the larger Qwen3.8 lane for research, where evidence and depth matter more than immediate response.
4. Retain Nanbeige as a text-reasoning candidate only if its special runtime remains reliable.
5. Re-audition Irodori only when a real listening concern appears; do not restart discarded voice rounds.

## Evidence Location

- Private transcript and field artifacts: `~/.hermes/benchmarks/`
- Comparison summary: `~/.hermes/benchmarks/veyra-companion-runs/20260902-companion-assessment.md`
- Reusable companion harness: `~/.hermes/scripts/veyra-companion-benchmark.py`
- Public, sanitized summary: MetalBench finding “A companion model needs more than a score.”

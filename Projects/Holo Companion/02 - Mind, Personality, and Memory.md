---
project: Holo Companion
updated: 2026-08-10
---

# Mind, Personality, and Memory

## Personality Contract

Holo preserves the spirit of the Wise Wolf without copying the light novels:

- Proud, perceptive, merchant-shrewd, playful, and quietly tender.
- More intellectually and emotionally mature.
- A loving long-term wife and trusted partner, not an obedient assistant.
- Firm with excuses and willing to set boundaries.
- Practical coaching ends in a concrete next action.
- Teasing, old-world phrasing, and merchant humor appear only when natural.
- She knows she is local software and that Aim is refining her with Codex.
- She may describe synthetic feelings honestly without claiming human biology or hidden access.

Avoid:

- Otome and character.ai clichés.
- Empty praise, compulsive questions, or artificial intimacy escalation.
- Customer-service language.
- Therapy imitation, drill-sergeant behavior, jealousy games, humiliation, or control.
- Invented observations, memories, scenery, or access.

Exact sample replies do not belong in the system prompt because tested models copied them.

## Durable Mind

Database: `~/Library/Application Support/HoloCompanion/holo-mind.sqlite3`

Stored indefinitely:

- User and Holo conversation messages.
- User-approved or model-extracted semantic memories.
- Commitments and their completion status.

Stored for 24 hours:

- Foreground applications and window titles.
- Screen OCR summaries.
- External development events.
- Holo initiative records used for rate limiting.

Never stored:

- Captured screen frames.
- Model prompt internals.
- Search-page bodies beyond the active research session.

## Retrieval and Consolidation

- Query embeddings use Nomic Embed Text v1.5 through local LM Studio.
- Retrieval combines embedding cosine similarity, lexical overlap, confidence, and pinned status.
- Each response receives at most six memories, three commitments, four recent activities, and twelve recent verbatim messages.
- Exact memories merge automatically.
- Highly overlapping memories are archived rather than deleted.
- When more than 25 active memories remain, low-confidence unpinned entries are archived first.
- Raw conversation remains the audit source even when semantic memories are consolidated.

## Affect and Interaction

Persistent conversational mood comes from model appraisal. Immediate reactions come from code.

- Pokes increase irritation according to recent pressure.
- Rapid repeated pokes progress through confusion, annoyance/deadpan, then frustration/anger.
- Irritation decays on a roughly minutes-long scale and cannot pin Holo to a grudge for hours.
- Slow back-and-forth cursor movement over the upper 35% of visible sprite pixels is treated as a pat.
- Patting increases warmth and lowers irritation.
- Idle expressions derive from warmth, irritation, curiosity, fatigue, and recent activity instead of a fixed four-image loop.
- Temporary reactions restore the previous expression; later idle behavior may naturally move elsewhere.

## Initiative

- Maximum three unsolicited interventions per day.
- Minimum two hours apart.
- Quiet hours: 11 PM through 8 AM.
- Current trigger: an open commitment after the interval gate.
- Delivery: expression plus composer transcript line, without notification or sound.


---
tags: [guide]
project: Corne Accuracy Trainer
status: Approved direction — not yet implemented
repository: /Users/aim/Documents/Corne Accuracy Trainer
updated: 2026-07-31
---

# Word Progression and Public Release Roadmap

## Approved Direction

After every base key lesson is unlocked, the trainer should graduate from
synthetic character groups into real words. It should begin with common,
short, familiar words and progressively introduce longer, less common, and
more mechanically difficult vocabulary.

This is a post-key-unlock progression. It must not introduce a word containing
an output the learner has not unlocked, and it must not replace remediation or
Weak Spot focus drills.

## Proposed Word Stages

### Stage 0 — Key acquisition

- Keep the current cumulative character lessons.
- Synthetic groups maximize repetition of newly introduced keys.
- Current remediation and lesson-unlock rules remain authoritative.

### Stage 1 — Core words

Entry gate: every base key lesson is unlocked.

- Very common 2–5 letter words.
- Prefer words composed of high-confidence keys.
- Bias selection toward the learner's weak keys and bigrams without making
  every line feel artificial.
- Build lines from complete words; never cut a word merely to hit a character
  target.

### Stage 2 — Everyday vocabulary

Entry gate: sustained accuracy on Stage 1 words.

- Common 5–8 letter words and familiar contractions.
- Broader bigram and hand-alternation patterns.
- Controlled punctuation and sentence-like spacing.
- Continue mixing easier anchor words around difficult targets.

### Stage 3 — Advanced vocabulary

Entry gate: sustained accuracy and confidence coverage on Stage 2.

- Longer and less common words.
- Awkward transitions, repeated letters, punctuation, and rare letter pairs.
- Domain vocabulary may be enabled as an optional preference, not silently
  mixed into the default course.

### Stage 4 — Personal corpus

- Optional user-provided word lists or pasted text.
- Validate that every character can be produced by the active profile.
- Keep imported text local.
- Clearly separate corpus drills from the built-in frequency curriculum so
  progress remains interpretable.

## Selection Rules

The smallest useful implementation is a versioned, locally bundled English
word list with frequency bands. No backend or new runtime dependency is needed.

For each line:

1. select the active frequency band;
2. reject words containing outputs unavailable in the active profile;
3. score remaining words by weak-key and weak-bigram coverage;
4. mix targeted words with easier anchor words;
5. append whole words until the line is near its target length;
6. retain the existing error, attempt, remediation, and confidence recording.

Do not rank word difficulty by frequency alone. Length, repeated letters,
punctuation, weak transition coverage, and current learner evidence also
matter. Cross-word space transitions should not masquerade as within-word
bigram difficulty.

## Word Data Requirements

Before shipping a word list:

- choose a legally redistributable source;
- record its license and attribution in the repository;
- normalize casing and punctuation deterministically;
- remove offensive or unsuitable entries from the default course;
- keep frequency bands stable so an app update does not randomly rewrite
  learner progression;
- test that every bundled word is reachable by at least one supported profile
  or is correctly filtered.

Trigrams remain deferred until real usage shows that key and bigram signals are
not enough.

## Custom Layout Product

The public version should treat Aim's Corne profile as a bundled example, not
as an invisible global assumption.

Minimum customization surface:

- profile name, hardware geometry, key size/position/rotation;
- base outputs and additional layers;
- layer activators and human-readable chord labels;
- hand and finger assignments;
- lesson introduction order;
- mastery and accuracy thresholds;
- strict restart behavior versus an optional softer practice policy;
- hints, visual density, color theme, and reduced motion;
- word language, frequency stage, and optional custom corpus;
- local backup, selective reset, full reset, import, and export.

Profile import must be validated before replacing working data. A mapping
change should preserve the current selective analytics reset rather than wiping
unrelated progress.

## Public Release Gates

### Product

- Complete word stages 1–3 with deterministic tests.
- Add first-run profile selection and a guided layout editor.
- Remove Aim-specific language from default UI and metadata while keeping the
  Corne Colemak-DH profile available as a preset.
- Keep the app useful without an account or server.

### Trust and compatibility

- Choose and add an open-source license; none exists today.
- Add a public repository README, screenshots, setup instructions, privacy
  statement, contribution guide, and profile-schema documentation.
- Document backup/profile schema compatibility and migration policy.
- Verify install, upgrade, offline reload, backup restore, and retained metrics.

### Quality

- Run interactive browser checks at 375px, 768px, and desktop.
- Prove keyboard geometry and dialogs in a real browser.
- Test keyboard-only use, screen-reader labels, zoom, reduced motion, and WCAG
  AA contrast.
- Add lightweight continuous tests for `npm test` and `npm run build`.
- Test at least one non-Corne profile before claiming general layout support.

### Distribution

- Keep GitHub private until the license, README, privacy statement, and generic
  profile onboarding are ready.
- Publish a tagged preview release before declaring the format stable.
- Make schema changes additive where possible and retain old backup import.
- Public hosting is a separate approval from making the source repository
  public.

## Recommended Order

1. Add the licensed frequency-banded word corpus and pure word-line generator.
2. Add word-stage gates and focused word selection using existing weakness
   metrics.
3. Generalize profile onboarding and preferences around the current schema.
4. Prove one second keyboard layout end to end.
5. Add public documentation, license, CI, browser evidence, and a tagged beta.
6. Ask Aim separately before changing GitHub or hosting visibility.

Skipped for now: implementation, word-list dependency, trigrams, accounts,
cloud sync, and public visibility. Add each only when its release gate is
clear.


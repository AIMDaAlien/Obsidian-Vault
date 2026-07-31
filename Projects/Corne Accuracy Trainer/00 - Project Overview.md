---
project: Corne Accuracy Trainer
status: Private working release — public customization roadmap defined
repository: https://github.com/AIMDaAlien/aim-corne-accuracy-trainer
local_repository: /Users/aim/Documents/Corne Accuracy Trainer
deployment: https://corne-accuracy-trainer.aliennerd8988.chatgpt.site
updated: 2026-07-31
---

# Corne Accuracy Trainer

## Purpose

Corne Accuracy Trainer is an offline-first typing trainer built around Aim's
46-key Corne v4.1 Colemak-DH Matrix layout. It teaches accuracy before speed:
mistakes restart the current line, remain in lifetime statistics, and feed
later remediation drills. WPM stays hidden until the mastery gate is complete.

The long-term product should also work for other people who want to describe
their own keyboard geometry, layers, outputs, learning thresholds, and drill
preferences without editing source code.

## Current State

**Private working release — public customization roadmap defined**

The current PWA includes:

- the exact 46-slot `LAYOUT_split_3x6_3_ex2` geometry;
- Aim's Colemak-DH base layer and Layer 3 digit mapping;
- cumulative key lessons with strict clean-line behavior;
- automatic three-clean-use remediation for failed keys and bigrams;
- Weak Spot Lab confidence metrics and a physical-layout heatmap;
- session-only focused drills for the weakest keys and transitions;
- local-only progress, profile editing, JSON backup, and v1-to-v2 migration;
- offline app-shell caching and installable PWA metadata;
- WPM and raw timing hidden until mastery.

The private production deployment and private GitHub repository both track
commit `df76c22` as of this note. A real-browser responsive, install, and
offline-reload pass remains an explicit release check; the original deployment
session could not run browser automation.

## Product Rules

1. Accuracy comes before speed. Public customization must not quietly weaken
   the default mastery contract.
2. Physical layout claims must match the saved profile. The browser sees
   output characters, not direct QMK/Vial layer-key presses.
3. Weakness scoring uses recent evidence and shows **Collecting data** when the
   sample is too sparse.
4. Focus drills supplement cumulative lessons and remediation; they do not
   erase or replace either system.
5. All learner data stays on the device unless the user explicitly exports a
   backup.
6. Existing backups and progress must survive future schema changes.

## Technology

- Dependency-free HTML, CSS, and JavaScript modules
- Node's built-in test runner
- Browser `localStorage` for profile and progress
- Service worker for offline app-shell caching
- OpenAI Sites private deployment
- GitHub: `AIMDaAlien/aim-corne-accuracy-trainer`

## Links

- [[01 - Technical Architecture and Product Record]]
- [[02 - Word Progression and Public Release Roadmap]]
- Parent index: [[Projects/README]]
- Local repository: `/Users/aim/Documents/Corne Accuracy Trainer`
- GitHub: https://github.com/AIMDaAlien/aim-corne-accuracy-trainer
- Private app: https://corne-accuracy-trainer.aliennerd8988.chatgpt.site

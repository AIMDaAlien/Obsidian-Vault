---
tags: [reliability]
project: Corne Accuracy Trainer
status: Adaptive Today coach implemented — physical trial pending
repository: https://github.com/AIMDaAlien/aim-corne-accuracy-trainer
local_repository: /Users/aim/Documents/Projects/Corne Accuracy Trainer
deployment: https://corne-accuracy-trainer.aliennerd8988.chatgpt.site
updated: 2026-08-22
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

**Adaptive Today coach implemented — physical trial pending**

The current PWA includes:

- the exact 46-slot `LAYOUT_split_3x6_3_ex2` geometry;
- Aim's Colemak-DH base layer and Layer 3 digit mapping;
- cumulative key lessons with strict clean-line behavior;
- automatic three-clean-use remediation for failed keys and bigrams;
- Weak Spot Lab confidence metrics and a physical-layout heatmap;
- session-only focused drills for the weakest keys and transitions;
- local-only progress, profile editing, JSON backup, and legacy migration;
- offline app-shell caching and installable PWA metadata;
- WPM and raw timing hidden until mastery.
- one adaptive 12–20 minute session with Recall, Repair, Transfer, and Check;
- layer-keyed 1/3/7-day reviews and one counted assessment per local day;
- extra practice that does not move review dates or add another assessment;
- a seven-session clean-throughput trend after mastery;
- progress/backup v4 with deterministic v1–v3 migration.

The source repository is now `/Users/aim/Documents/Projects/Corne Accuracy Trainer`.
The private deployment now runs Sites version 8 from app commit `d9bc3ec`.
Real-browser responsive/install/offline proof, three physical Corne sessions,
and the two-week learning check remain open acceptance gates.

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
- [[03 - Today Adaptive Coach and Trial Record]]
- Parent index: [[Projects/README]]
- Local repository: `/Users/aim/Documents/Projects/Corne Accuracy Trainer`
- GitHub: https://github.com/AIMDaAlien/aim-corne-accuracy-trainer
- Private app: https://corne-accuracy-trainer.aliennerd8988.chatgpt.site

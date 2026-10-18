---
type: benchmark-log
topic: Philosopher Model
publish: true
created: 2026-10-06
tags: [omarchy]
machine: bigrig
title: "Philosopher Model"
---
# Philosopher Model

> Full project overview (decisions, tests, architecture): [[Philosopher Project]]


## 2026-10-05 19:47
**Done:** Reconciled stale ACTIVE_PLAN against actual repo state; status recap of the philosopher project.
**Findings:** Plan steps 3-5 were already completed in a later session: bin/run_eval.py built and self-verifying; 4-model A/B ran (Pantheon, StyleTune-V2, Swift-27B, Ornith-23G). Verdict: Ornith-1.5-35B-A3B-MTPv2-23G-ICE wins raw prose decisively (5 flags vs Swift 14; register_prose 1/6 vs 4/6 flagged) at 131K ctx and 2.6x Swift speed. Citation metric unscoreable until corpus gains 20th-century continental philosophy (93-97% UNVERIFIED is a corpus property; spot-checked quotes genuine). enable_thinking must use chat_template_kwargs, not top-level.
**Recommendations:** Pending user decision: accept abliterated Ornith checkpoint vs pull guardrailed TIEL tier. Then harness/server.py + context assembly (strip <think> for display).

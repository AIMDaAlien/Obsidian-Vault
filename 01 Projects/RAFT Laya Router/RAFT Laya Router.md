---
type: note
category: Agents & Tooling
tags: [agents, routing, calibration, raft]
publish: true
created: 2026-09-23
machine: bigrig
title: "RAFT — Laya task router (Penthouse)"
featured: 52
summary: "A small AI that decides which bigger AI should do a job, and only acts when confident; tested honestly, savings were modest."
---
# RAFT — Laya task router (Penthouse)

**Category:** [[Agents & Tooling]] · **Vault:** [[Vault Map]]

Status 2026-09-22: working decider + calibration + execution wiring.

## What raft is
`~/Work/raft/raft.py` — Laya 421M (System-1 decider) in front of the agent tiers
(qwen27b_local / deepseek_flash / codex_high / human_review). Commands:
decide, gate, bench, calibrate, run, log. Log: `raft-log.jsonl`.

## Calibration (the important number)
- 40 real Penthouse tasks (`labels-calib.jsonl`), temperature-scaling fit T=0.5 (`raft-temp.json`).
- ECE (binned, chosen-prob basis): 0.216 raw -> 0.111 after scaling. Squashed 0.0-0.2 confidences now spread 0.3-1.0 and track accuracy:
  conf 0.3-0.4 -> 60% acc; 0.6-0.7 -> 75%; 0.9+ -> 100% (small n).
- Old "ECE 0.666" was a different (cruder) metric on 15 tasks; not comparable.

## Routing accuracy
- Prompt tuning plateau: 60-62.5% raw argmax on 40 tasks. Big few-shot prompts HURT (50%); short criteria + one escalation rule + 4-line exemplars = best.
- Real win is the policy, not argmax: act only at confidence >= 0.6, escalate below (to codex, or human for codex/human picks). Threshold curve: act@0.6 = 80% acted-accuracy, effective ~86% with escalation handled; act@0.8 = 100% but only 5% acted.

## Execution
`raft run "<task>"` decides then executes: qwen/deepseek tiers via :8080 OpenAI-compat (llama-server), codex via `codex exec`, human_review stops. Codex exec is read-only sandbox by default — reports findings, changes nothing.

## Cost measurement (4 tasks, each baseline vs routed)
- Always-codex baseline: 26.4 / 25.9 / 38.7 / 54.2 s per task.
- Routed: 2 of 4 correctly sent local (:8080 flash; 19.9 s vs 25.9 s) — but 2 low-confidence tasks escalated to codex, so net wall-clock saving was small on this sample.
- Honest read: savings come from confidence being high enough to act on local tiers often; with T=0.5 the confidence hovers ~0.5-0.7, so escalation eats savings on thin slices. Next lever: more calibration data (esp. qwen-tier tasks) to sharpen the middle buckets, and per-class thresholds.

## Related

- Same project family: [[Agents & Tooling]] · [[Bench Suite (~bench)]] (where the tier vocabulary comes from)
- Tier endpoints: [[Models & Serving]] · [[Qwen3.8 Rig]] · [[Flash-Next AD384]]
- Same confidence-gate philosophy: [[Raspberry Pi B+ Utility Node]] (Cactus Needle 3)

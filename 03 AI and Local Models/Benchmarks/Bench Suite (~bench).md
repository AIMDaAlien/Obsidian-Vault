---
type: methodology
topic: bench suite
updated: 2026-10-12
category: Benchmarks
tags: [benchmark, tooling, harness, local-ai]
publish: true
created: 2026-10-12
machine: bigrig
title: "Bench Suite (`~/bench`)"
---
# Bench Suite (`~/bench`)

**Category:** [[Benchmarks]] · **Vault:** [[Vault Map]]

The unattended, executed-verdict benchmark suite used for [[Model Benchmarks]] (built 2026-09-22).

## 2026-10-12 — Corrected matched DeepSWE2 comparison

[[2026-10-12 Matched Qwen 27B vs Flash DeepSWE2]] — six complete campaigns, 144 audited results over 24 distinct synthetic repository tasks. Flash averaged **22.67/24** versus Qwen **21.00/24**; the task-bootstrap interval for the +1.67 Flash delta is **[-2.33, +5.67]**, including zero. The historical 27B advantage was not observed on this corrected suite. The note embeds delta and capability/latency charts, with [[2026-10-12 Matched Qwen vs Flash — Methods and artifacts|full methods, provenance and all archived supporting files]].


## Shape — 76 tasks, five domains, no LLM judge

| pack | n | what it does |
|---|---|---|
| `code` | 40 | tiered tasks, model code executed against hidden asserts, per-assert credit |
| `research` | 20 | 18K-token generated handbook; exact value + §citation match |
| `terminal` | 7→15 | runs the model's script, asserts the **END STATE** (files, modes, stdout) |
| `backend` | 6 | hidden contract suite incl. real HTTP to its own server |
| `deepswe` | 3→11 | unified diff applied to a fixture repo, repo verifier decides |
| `triage` | 22 | only the hard tasks across all domains — the gate |

`--packs all` yields **98 rows** (76 + 22 triage refs — a double-count, but consistent across targets so comparisons hold).
`selftest.py` proves each grader **accepts a gold answer and rejects a bad one** (16 + 16 cases, 0 failures).

## Commands

```bash
cd ~/bench
./campaign.sh --enqueue tag=nightly targets=all packs=all
./campaign.sh                      # run the queue
python3 report.py --tag nightly --vault
```

Roster lives in `targets.json`; results in `~/bench/results/rebench-*.json`.

## Safety / unattended design

- One `flock` = one campaign.
- Refuses to start a GPU target while `llama-bench`/cli is alive.
- An endpoint already serving is **never** torn down — only what the campaign started gets stopped.
- A reasoning model can spend a tiny token cap wholly in the thought phase and look like a dead server.

## Known walls

- **Docker needs root** (no sudo / not in the docker group) → grading uses scratch dirs + venvs, not containers; real SWE-bench/DeepSWE harnesses would need a user-run `usermod -aG docker aim`.
- **deepswe is a universal 0/6 wall** on every config (models emit malformed multi-file diffs; 16/30 rows hit the token cap) → uninformative until the diff contract is reworked. Replaced by a **`kind=files` full-file replacement contract** (matches how the user's agents actually work) in the suite rebuild.
- `_materialise` used `copytree` which dereferences symlinks (crashes on dangling links) — must copy links as links.
- Fixed bugs: triage pack re-resolved `kit_tree` against a nonexistent `packs/triage/trees/rescue` (killed every `--packs all` run); `run_task` never copied `_answer` into the row dict (stored answers were always empty).

## Suite rebuild (in progress at last look)

`kind=files` contract · role lanes (research t1/t2 batch-research, t3/t4 obscure-research; terminal/code/backend agentic; deepswe deepswe) · terminal 7→15 (GPU/VRAM monitoring, log rotation, backup pruning, broken symlinks, patch apply, disk, restart-wait, config-diff) · deepswe 3→11 (workers, retries, idempotency, dead-letter, rate limit, monotonic ids, config overlay, secret redaction, checkpoints, migrations).

## Related

[[Benchmark Methodology]] · [[Model Benchmarks]] · [[Qwen3.8 Rig]]

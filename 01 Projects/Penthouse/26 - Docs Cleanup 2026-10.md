---
tags: [penthouse, docs, cleanup, obsidian, handoff]
created: 2026-10-12
updated: 2026-10-12
publish: false
project: Penthouse
---

# Docs Cleanup, October 2026

Aim's call on 2026-10-12: get rid of stale handoffs, prompts and references in the repo; anything still worth knowing goes into this vault. Branch `chore/docs-cleanup` off `main` 299f999.

## What left the repo

Pass 1 (`docs/`): 162 files, about 4.7 MB.

- `docs/archive/handoffs/` — 49 agent handoffs and briefs (Codex, Kimi, Gemini, DeepSeek, Opencode), April to September 2026.
- `docs/codex-prompts/`, `docs/gemini-prompts/`, `docs/e2e-test-prompts/` — prompts for models no longer in use.
- `docs/kimi-rebuild/` — the rebuild plan set whose work shipped; the five research briefs were kept (see below).
- `docs/release-tickets/` — tickets for v4.2 and v4.3, all shipped.
- `docs/testing-reports/` — QA reports and 22 screenshots from June and July 2026.
- `docs/obsidian/` — a stale fork of this vault's Penthouse folder. Eight notes that existed only there are now in `Rebuild Archive/`; the Unraid production-operations note moved to the Self-Hosting folder; the uncommitted "Unraid LLM Serving Throughput" note moved to `03 AI and Local Models`.
- `docs/superpowers/` old plans, specs, continuation prompts and the skills list; the four April specs were kept (see below). PR #37 repopulates the folder with the storage-lifecycle spec and plan.
- `docs/adr/` (both files), `BETA-READINESS-4.4`, `DESIGN-RESIDENCY`, `FEATURE-ROADMAP`, `backend-review-follow-ups`, `logo-gallery.html`.

Pass 2 (repo root): 67 files, about 472 KB. `antigravity/handoffs/` (46 retired-model handoffs), the tracked contents of `plans/` (the September 2026 hardening plan set and four Qwen checkpoint folders, 20 files), and `generate_v3.js` (prototype generator for directories that no longer exist). Untracked working folders under `plans/` in the main checkout were not touched. Four Playwright specs still write screenshots under `plans/…`; Playwright creates those folders itself.

## What was folded into living docs

- `docs/PRE-RELEASE-RUNBOOK.md` gained a short "Manual smoke checks" section from the old MVP E2E checklist.
- `docs/DEVELOPMENT.md` gained the release-gate command and a "Realtime events" table: 26 of the 30 events in the old Kimi realtime contract still exist on the server and are listed; `presence.request_sync`, `message.moderate`, `poll.vote`, `poll.voted` do not and were dropped.
- `docs/AGENT-ROUTING.md` rewritten for the two-agent setup (Claude primary and `apps/web`; Codex for `services/api`, `infra`, `scripts`); the retired-model routing table is gone. Consumed briefs now go to this vault's `Repo Archive`, not to the repo.
- `docs/START_HERE.md` now points here for the knowledge hub and no longer claims a `release:gate` npm script.
- `apps/web/PRODUCT.md`, `DESIGN.md`, `AGENTS.md` had their dead references and retired-model routing removed.

## What was kept in this vault instead

`01 Projects/The Penthouse/Repo Archive/` (all private): the unbuilt local-first sync and WebRTC design and its review, the two V5 design handoffs, the five feature-research briefs, the four April 2026 design specs, the September 2026 hardening plans 001 to 008 with their status table, and the logo gallery HTML.

## References that still point at deleted paths

Files agents may not edit: the root `CLAUDE.md` is untouched (it never linked the deleted files). `docs/HANDOFF.md` on `main` still names `V5-USABILITY-INTEGRATION.md`; PR #37 replaces that file wholesale. Anything else is listed in the cleanup report on the branch.

## Why

Two agents now, not six. Every stale routing doc and handoff was a place for a fresh session to pick up wrong instructions. The vault is what Aim reads; the repo keeps only what the deploy and a new engineer need.

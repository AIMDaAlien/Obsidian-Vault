---
tags: []
created: 2026-10-12
publish: false
project: Penthouse
---
# Plan 007: One source-of-truth handoff, a short history folder, and nothing else

> **Executor instructions**: Follow this plan step by step. Run every verification
> command and confirm the expected result before moving to the next step. If
> anything in "STOP conditions" happens, stop and report — do not improvise.
> When done, update this plan's status row in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 2bea709..HEAD -- docs README.md CLAUDE.md AGENTS.md CHANGELOG.md`
> If non-empty, list the changed files in your report and re-check the keep/archive
> table below against reality before moving files.

## Status

- **Priority**: P2
- **Effort**: M (mechanical, but touches many files; must be done in one commit per folder)
- **Risk**: LOW for the moves, MED for accidentally archiving something load-bearing
- **Depends on**: none (independent of the code plans; run it in parallel)
- **Category**: docs / DX
- **Planned at**: commit `2bea709`, 2026-09-02
- **Aim's decision, 2026-09-02**: the old agent handoffs are useless as live
  documents. Keep (a) the history of what happened, and (b) exactly one
  source-of-truth handoff that states the current state of the repo.

## Why this matters

Documentation is now the biggest single confusion risk in this repo. `docs/`
holds 161 tracked files, 138 of them Markdown, including 12+ files named
`AGENT-HANDOFF-*`, `CODEX-HANDOFF-*`, `KIMI-*`, `GEMINI-*`, plus `docs/archive`
(29), `docs/testing-reports` (26), `docs/obsidian` (28), `docs/kimi-rebuild`
(20), `docs/superpowers` (13), `docs/codex-prompts` (8). The self-declared
index — `docs/AGENT-HANDOFFS.md` — is stamped "Last updated: 2026-07-14" and
describes the project as v4.2.0-alpha.1 while `package.json` says `4.3.0-alpha.2`,
so the index is actively wrong. There are two deploy guides (`docs/DEPLOYMENT.md`
and `docs/UNRAID_DEPLOYMENT.md`), `README.md:41` links
`docs/PRODUCTION_ALPHA_RELEASE.md` which does not exist, and
`docs/START_HERE.md` describes a `apps/mobile` Vue+Capacitor app that is not in
the repo. A new agent (or Aim) cannot tell what is true without reading fifteen
stale files.

This plan does not delete history: it moves consumed briefs into
`docs/history/`, fixes the pointers, and leaves one living handoff.

## Current state

- `docs/AGENT-HANDOFFS.md` — header says "Last updated: 2026-07-14", table of
  "Active Work" pointing at handoff files that are done or superseded, and it
  claims to be "the single source of truth for active agent handoffs". It is not
  any more.
- Already-existing single handoff (created by the audit session, keep it as THE one):
  `docs/HANDOFF.md`. It states repo state, plan order, and ownership. Do not
  create a second one; every future handoff updates this file.
- Root-level stray handoffs/QA artifacts: `HANDOFF_RESPONSIVE_LAYOUT_KIMI.md`,
  `V5-HANDOFF.md`, `QA_REPORT.md`, `docs/CLAUDE-CONTINUATION.md`,
  `docs/KIMI-SESSION-RESUME.md`.
- `docs/AGENT-ROUTING.md` is referenced from `AGENTS.md` and defines the handoff
  block format used by every agent. Keep it in `docs/`, live.
- Deploy docs duplication: `docs/DEPLOYMENT.md`, `docs/UNRAID_DEPLOYMENT.md`,
  `docs/PRE-RELEASE-RUNBOOK.md` (titled "Close-Friends Release Runbook", pinned
  to `2026.07.05`), plus the missing target `docs/PRODUCTION_ALPHA_RELEASE.md`
  referenced by `README.md:41`.
- `docs/adr/` contains `04-backend-scaffold.md` and `ADR-0001-rebuild-baseline.md`
  — decided tradeoffs. Never archive these; they are the reason a future agent
  does not re-litigate settled design.
- `docs/obsidian/` (28 files) is Aim's operations notebook — includes real,
  load-bearing facts (`21 - Unraid Production Operations.md` names the actual
  Unraid paths; `00 - Knowledge Hub.md`, `01 - Rebuild Timeline.md`). Treat as
  history+ops reference, not agent scratch.

## Commands you will need

| Purpose | Command | Expected on success |
| --- | --- | --- |
| Count tracked docs | `git ls-files docs \| wc -l` | prints a number (161 at planning time) |
| Move safely | `git mv <from> <to>` | exit 0, rename recorded |
| Broken-link check (relative links in the 6 live docs) | see Step 4 | no missing targets |
| Whole gate | `npm run validate` | exit 0 |

## Scope

**In scope** (the only files you should modify/move):

- everything under `docs/` except `docs/adr/`
- `README.md`, `CHANGELOG.md` (link fixes only), root stray handoff files
- `docs/HANDOFF.md` (update, never duplicate)

**Out of scope** (do NOT touch, even though they look related):

- any file outside `docs/` + the four root docs named above. No code.
- `AGENTS.md`, `CLAUDE.md`, `services/api/CLAUDE.md`, `infra/CLAUDE.md` — agent
  instruction files, live; only edit if a *path they cite* moved (and say so).
- `docs/adr/` — read-only.
- `plans/` and `advisor-plans/` — plan directories, not documentation history.

## Git workflow

- Branch: `advisor/007-docs-triage`
- Commit style: `docs(archive): move consumed handoffs to docs/history`, `docs: fix broken runbook links`, `docs: point README at the single handoff`.
- Use `git mv` (never delete-and-recreate) so history follows the file.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Create the history folder and move the consumed agent briefs

Create `docs/history/` and `git mv` into it, by pattern:

| Move to `docs/history/` | Why |
| --- | --- |
| `docs/AGENT-HANDOFF-*.md` (7 files) | consumed briefs |
| `docs/CODEX-HANDOFF-*.md`, `docs/CODEX-REVIEW-*.md` | consumed briefs |
| `docs/GEMINI-*.md` (2), `docs/HANDOFF-ANTIGRAVITY-VOICE-TESTING.md` | consumed briefs |
| `docs/KIMI-SESSION-RESUME.md`, `docs/CLAUDE-CONTINUATION.md` | session scratch |
| `docs/backend-review-follow-ups.md` | findings already landed |
| `docs/codex-prompts/`, `docs/e2e-test-prompts/`, `docs/superpowers/`, `docs/kimi-rebuild/`, `docs/testing-reports/` | one-time prompts/reports |
| root `HANDOFF_RESPONSIVE_LAYOUT_KIMI.md`, `V5-HANDOFF.md`, `QA_REPORT.md` | root strays |
| `docs/AGENT-HANDOFFS.md` | replaced by `docs/HANDOFF.md`; keep as history |

Then `docs/archive/` (29 files) stays where it is — it is already archive. Do not
double-nest it.

**Verify**: `git ls-files docs/AGENT-HANDOFF-* | wc -l` → `0` at top level;
`git ls-files docs/history | wc -l` → ≥ 15.

### Step 2: Collapse the duplicate deploy docs

Keep exactly one deploy guide and one runbook:

- Keep `docs/DEPLOYMENT.md` as the single deploy guide (plan 003 already added the
  build-then-up sequence; plan 006 already removed the Android parts).
- Move `docs/UNRAID_DEPLOYMENT.md` into `docs/deployment-unraid.md` **only if**
  it contains Unraid-specific facts absent from `DEPLOYMENT.md` (diff them first,
  and merge the unique parts into `DEPLOYMENT.md` instead, then archive it).
  Report which you chose.
- Keep `docs/PRE-RELEASE-RUNBOOK.md`, but change its H1 from
  "Close-Friends Release Runbook" to "Release Runbook" and drop the pinned
  `2026.07.05` line in favour of "current for 4.3.x and later".
  The migration-037 SQL pre-flight inside it stays.

**Verify**: `grep -n "^# " docs/PRE-RELEASE-RUNBOOK.md` → no "Close-Friends" and no dated version line.

### Step 3: Fix the pointers

- `README.md:41` — `docs/PRODUCTION_ALPHA_RELEASE.md` does not exist. Point the
  sentence at `docs/DEPLOYMENT.md` and add a line linking `docs/HANDOFF.md` as
  "current state of the repo".
- `CHANGELOG.md` — if it links any moved file, fix the path. Do not rewrite
  changelog content (changelog art direction belongs to the primary agent).
- Any live doc that links a moved file gets its link updated. Find them with:

  ```sh
  git ls-files docs '*.md' | xargs grep -lE "AGENT-HANDOFF|CODEX-HANDOFF|KIMI-SESSION|CLAUDE-CONTINUATION|V5-HANDOFF|QA_REPORT|HANDOFF_RESPONSIVE" | grep -v docs/history
  ```

  Everything under `docs/history/` and `docs/archive/` may keep its old
  (now-broken) cross-links — history is allowed to rot in place.

**Verify**: the `git ls-files ... | xargs grep -lE ...` command above returns only
files under `docs/history/`.

### Step 4: Prove no live doc has a broken relative link

Run this from the repo root; it only checks the docs that are meant to be live
(README + the kept docs), and prints anything whose target is missing:

```sh
for f in README.md docs/*.md; do
  grep -oE '\]\(([^)#]+"' "$f" 2>/dev/null >/dev/null  # no-op, keeps shells happy
done
python3 - <<'PY'
import os, re, glob
bad = []
targets = ['README.md'] + glob.glob('docs/*.md')
for path in targets:
    if 'history' in path:
        continue
    text = open(path, encoding='utf-8', errors='ignore').read()
    for link in re.findall(r'\]\(([^)\s]+)', text):
        if link.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(path), link.split('#')[0]))
        if not os.path.exists(target):
            bad.append(f'{path} -> {link}')
print('\n'.join(bad) if bad else 'no broken relative links')
PY
```

**Verify**: prints `no broken relative links` (or only links you can justify in
the report).

### Step 5: Leave the standing rule where agents will hit it

Append a short section to `docs/AGENT-ROUTING.md` (do not restructure that file):

> ## Documentation rule (from 2026-09-02)
>
> There is exactly one living handoff: `docs/HANDOFF.md`. Update it in place.
> Never create `docs/AGENT-HANDOFF-<something>.md` again. Consumed briefs,
> prompts, and test reports go to `docs/history/`. Architecture decisions go to
> `docs/adr/` as ADRs, because they outlive the agent that made them.

**Verify**: `grep -n "one living handoff" docs/AGENT-ROUTING.md` → ≥1 line.

## Test plan

- No code tests. This plan's gate is the Step 4 link checker plus
  `npm run validate` (docs-only changes must not break the build; if they do,
  something in `docs/` is being consumed by code — investigate and report).

## Done criteria

- [ ] `git ls-files docs/AGENT-HANDOFF-*` → empty (all under `docs/history/`)
- [ ] Exactly one living handoff: `docs/HANDOFF.md` exists; `docs/AGENT-HANDOFFS.md` no longer at `docs/` top level
- [ ] `docs/DEPLOYMENT.md` is the only deploy guide at `docs/` top level (the Unraid one merged or archived)
- [ ] `README.md` has no link to `docs/PRODUCTION_ALPHA_RELEASE.md` and does link `docs/HANDOFF.md`
- [ ] Step 4 checker prints `no broken relative links`
- [ ] `docs/adr/` untouched (`git diff --name-only -- docs/adr` → empty)
- [ ] `npm run validate` exits 0
- [ ] `plans/README.md` status row for 007 → DONE

## STOP conditions

Stop and report if:

- A file you are told to archive is linked from `AGENTS.md`, `CLAUDE.md`, or any
  `*/CLAUDE.md` as an active instruction (then it is not consumed; leave it and list it).
- `docs/UNRAID_DEPLOYMENT.md` contains production paths/commands that are absent
  from `docs/DEPLOYMENT.md` and merging them would exceed one page — report the
  delta and let the primary agent decide.
- The link checker reports more than 20 broken links in live docs; that means the
  triage is bigger than this plan and needs a second pass, not a rushed one.

## Maintenance notes

- `docs/HANDOFF.md` is now the single place the next agent reads first. Whoever
  lands a plan must move its row from "open" to "closed" there, in the same
  commit. That is what stops this rot returning.
- The repo still has `.claude/`, `.codex/`, `.kilo/`, `.kimi-code/`,
  `.playwright-mcp/`, `antigravity/` (58 tracked files) as agent working areas.
  Not documentation, deliberately left alone; if Aim wants them out, that is a
  separate brief.
- Deferred: converting `docs/obsidian/` to anything. It is Aim's notebook; treat
  as read-only reference.

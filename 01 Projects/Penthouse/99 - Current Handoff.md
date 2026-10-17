---
title: 99 - Current Handoff
tags: [project]
created: 2025-01-01
updated: 2026-10-16
publish: false
project: Penthouse
---

# Current Handoff

- Canonical repo: `~/Documents/Projects/The-Penthouse-main-auth`. GitHub `main` is `c5a23c2` at `4.5.0-alpha.1`: PR #46 and #47 merged 2026-10-15, PR #48 (GIF providers) and PR #49 (search privacy) merged 2026-10-16 at Aim's word. Combined CI green.
- Ownership (Aim, 2026-10-13): Claude builds web, API and contracts end to end; Codex verifies deployments and the host. Handoff notes are written for that verification pass.
- Undeployed: migrations 045, 046 and 047 are all on `main`. Ready for Codex to deploy. Codex deploys and runs the smoke check in `docs/HANDOFF.md`, then sets `purged_at` on the three trimmed-PDF rows.
- PR #48 (GIF providers: Klipy default + Giphy tabs, per-group rating `pg-13`, migration 047): merged 2026-10-16. Production needs fresh Klipy/Giphy keys (Codex).
- Search, Discover and people privacy: spec `docs/superpowers/specs/2026-10-16-search-discover-privacy-design.md`, shipped as three PRs.
  - PR #49 (PR 1 of 3, search privacy, API only, no migration) opened 2026-10-16 from `feat/search-privacy` head `7549cf2`. CI green; **merged 2026-10-16** (`c5a23c2`). In-chat search now hides deleted and moderated messages, escapes wildcards, supports filters and pages (default 50); people search escapes, matches word starts, ranks the exact username first; blocked pairs vanish from people search and the directory both ways. In-chat query cap moved 100 → 200 to match global search.
  - Known side effect until PR 3: the "Show blocked users" toggle shows a count but reveals nobody.
  - Follow-ups: the search cursor is millisecond-only with no id tiebreak (fix before PR 3's "Show older"); the password-reset username lookup uses an unescaped `ilike` (separate fix).
  - PR 3 plan: `docs/superpowers/plans/2026-10-16-people-directory.md` on local branch `feat/people-directory` (`c363073`), 19 tasks, migration 048 `users.directory_visible`; awaiting Aim's review. PR 2 (group visibility) is unblocked now that #48 merged; it takes the next migration number after whichever lands first. PR 3 (directory opt-out, Search → People, retire `/users`, shared UI parts) follows PR 1. Each gets its own plan and branch from `main`.
  - SDD ledger archived in `~/Documents/Projects/penthouse-sdd-ledgers-2026-10-16-search-privacy/`.
- Worktree setup lesson: don't symlink the whole root `node_modules` from the main checkout. Link each entry, and point `node_modules/@penthouse/*` into the worktree, or the API picks up main's stale contracts. Give each worktree its own test database (`createdb penthouse_test_<branch>` in `penthouse-test-pg`); the shared one can carry another branch's migrations. `npm run validate` does not run `test:integration`; run it separately (about 10 minutes).
- Discover follow-up WIP (mobile overlay and layout, not search logic) is parked in local commit `2f7f52c` on `feat/discover-followup`, not pushed. Still to do under 4.5.x, together with the CHANGELOG catch-up (2026-07-05 to 2026-10-11), the #37 follow-ups and Dependabot triage, all under 4.5.x.
- Release sequencing (Aim, 2026-10-12): the "drastic" frontend overhaul is its own major release with its own CHANGELOG section, after the 4.5.x housekeeping.
- Branches: origin pruned 2026-10-12 to `main`, Codex's `fix/post-incident-backup-hardening`, `feat/read-only-recovery`, `integration/recovery-local-rc` and 11 Dependabot branches. Deleted branches live in `~/Documents/Projects/penthouse-branch-backup-2026-10-12.bundle` and `penthouse-origin-prune-backup-2026-10-12.bundle`; restore with `git fetch <bundle> <branch>:<branch>`.
- Idea seed captured: Life. — next step is a short brainstorm on medium and audience when Aim wants it.
- Host state: nightly dump verified 2026-10-11; uploads 115 MB after the three over-cap PDFs were deleted; automatic failover off; never restore the October 4 watchdog or start the standby connector. Host details live in the Self-Hosting folder and in Claude's project memory, not here.

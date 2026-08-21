---
tags: [penthouse, tech-debt, quality-gates, reliability, guide, hardening]
created: 2026-03-05
published_to_garden: true
visibility: public
---

# Stability Rules (Anti-Tech-Debt)

These are the non-negotiable rules I adopted to avoid the "slop spiral" that took down earlier builds. If any of this gets skipped, the project pays for it later.

## Core rules

1. No feature coding before the contracts exist.
2. No endpoint merge without tests covering both success and failure paths.
3. No schema change without a migration and a rollback note.
4. No shortcuts in auth or session logic.
5. No silent retries — retries have to be bounded and visible.
6. No new dependency without a clear reason to maintain it.
7. No high-risk change without a human approval step and a rollback path.
8. No release if critical smoke tests are failing.

## Required gates per significant task

Every significant task goes through these stages in order:

1. **Intake** — define what the task actually is
2. **Evidence** — gather any relevant context before planning
3. **Planning** — write the plan, get a critique
4. **Execution** — do the work
5. **Review** — check the work against the plan
6. **Arbitration** — resolve any disagreements
7. **Human approval** — required for anything high-risk, security-related, or prod-impacting
8. **Closeout** — handoff notes plus rollback documentation

See also: [[05 - Multi-Model Delegation Workflow]]

## Daily validation commands

```bash
npm run validate
npm run scenario:test
```

## Why these rules matter on a self-hosted bare metal setup

On a home server, there's no cloud fallback. Fewer moving parts means fewer random failures, strong tests catch regressions before a deploy, rollback notes cut downtime when something does break, and explicit ownership means nothing gets double-worked or left to chance.

---
tags: [penthouse, ai-workflow, delegation, multi-agent]
created: 2026-03-05
published_to_garden: true
visibility: public
---

# Multi-Model AI Delegation Workflow

One of the weirder things about how I build this project is that I don't use a single AI tool for everything. I route different concerns to different models based on what they're actually good at, and I've set up a structured workflow so there's always clear ownership and the changes are traceable.

## Why bother with this

When you're using multiple AI agents on the same codebase, "everyone just edits everything" turns into chaos fast. Conflicting changes, unclear ownership, no rollback plan. The delegation setup fixes that by making ownership explicit before any work starts.

## How I split the work

I keep three roles in play at any given time:

- **Backend/infra owner** — owns the API, data layer, security, contracts, and the release gate. This is the default final arbiter when there's a conflict.
- **Decomposition/review partner** — handles complex refactor planning, deep log analysis, and reviewing work that needs a second set of eyes before it merges.
- **Frontend/UI owner** — owns the visual implementation and polish. Gets paired with the backend owner as reviewer.

This isn't fixed — I adjust the split based on what phase the project's in. During a stabilization cycle I'll lock the backend role to one tool and keep frontend work separate. During a visual exploration wave I'll open up the frontend role explicitly.

## Routing defaults

| Concern | Owner | Reviewer |
|---|---|---|
| Backend, API, realtime, data, infra | Backend tool | Decomposition tool |
| Frontend UI | Frontend tool | Backend tool |
| Frontend architecture / major migrations | Decomposition tool plans, Frontend tool implements | Backend tool reviews |
| Anything high/critical risk | Requires evidence + human sign-off |

## The 8-stage gated workflow

Every significant task goes through these in order:

1. **Intake** — define the task
2. **Evidence** — gather context before planning
3. **Planning** — write the plan, get a critique
4. **Execution** — do the work
5. **Review** — check against the plan
6. **Arbitration** — resolve disagreements
7. **Human approval** — required for high-risk, security, or prod-impacting changes
8. **Closeout** — handoff notes and rollback documentation

## Required artifacts per task

Each task produces:
- Task intake definition
- Routing decision record
- Evidence log
- Decision record (if there was a disagreement)
- Handoff packet

Templates for all of these live in the `antigravity/templates/` folder in the repo.

## Why this works

- Nothing gets modified without a clear owner.
- High-risk changes can't skip human review.
- Every decision has a paper trail so rollback is easy.
- It keeps stability as the priority over feature speed, which on a self-hosted setup matters a lot.

## Current execution override (as of late March 2026)

During the active stabilization and visual-exploration cycle I set a temporary override:
- The backend tool owned backend, contracts, tests, and the release gate exclusively.
- The decomposition tool acted as design review partner for the frontend visual exploration.
- The frontend tool was explicitly re-enabled for member-facing UI work after being paused during stabilization.

---
tags: [penthouse, ai-workflow, delegation, multi-agent, security]
created: 2026-03-05
published_to_garden: true
visibility: public
---

# Multi-Model AI Delegation Workflow

One of the weirder things about how I build this project is that I don't use a single AI tool for everything. I route different concerns to different models based on what they're actually good at, and I've set up a structured workflow so there's always clear ownership and the changes are traceable.

## Why bother with this

When you're using multiple AI agents on the same codebase, "everyone just edits everything" turns into chaos fast. Conflicting changes, unclear ownership, no rollback plan. The delegation setup fixes that by making ownership explicit before any work starts.

## How I split the work

I keep three roles in play:

- **Codex** — orchestrates, owns backend/infra/security work, keeps final control of changelog and release-ticket style, reviews the finished diff, and gives release sign-off.
- **Qwen3.6 35B-A3B local** — handles narrow, lower-risk implementation work such as UI slices, CSS, mechanical refactors, and ticket scaffolding. This slot will move to Qwen3.8 27B after that model is available and proven.
- **DeepSeek V4 Flash 0731** — runs tests, browser proof, and cheap first-pass debugging. It reports evidence; it does not decide that risky backend or production work is safe to ship.

This isn't fixed — I adjust the split based on what phase the project's in. During a stabilization cycle I'll lock the backend role to one tool and keep frontend work separate. During a visual exploration wave I'll open up the frontend role explicitly.

## Routing defaults

| Concern                                       | Owner                              | Builder or tester                            |
| --------------------------------------------- | ---------------------------------- | -------------------------------------------- |
| Backend, API, realtime, data, security, infra | Codex                              | DeepSeek Flash tests                         |
| Frontend UI                                   | Codex briefs and signs off         | Qwen builds; DeepSeek Flash tests            |
| Changelog and release tickets                 | Codex owns final style and wording | Qwen may scaffold; DeepSeek Flash renders    |
| Unknown low-risk bug                          | Codex decides scope                | DeepSeek Flash triages; Qwen fixes if narrow |
| Anything high/critical risk                   | Codex review plus Aim's approval   | DeepSeek Flash supplies targeted evidence    |

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

## Current routing (August 2026)

- Kimi and GLM/Kilo are no longer active agents for this project.
- DeepSeek V4 Pro has been superseded in the active workflow by DeepSeek V4 Flash 0731.
- Qwen is used to offload mundane, token-heavy building, not security judgment or release approval.
- Test execution is delegated to DeepSeek V4 Flash 0731; Codex reviews the evidence and owns the final release decision.

---
tags: [self-hosting, changelog, v1, penthouse, troubleshooting, branding, hardening]
created: 2026-03-03
published_to_garden: true
visibility: public
---

# What Changed Between Notes (v1 Phase 1 Summary)

This note covers what happened between the last set of Obsidian notes (2026-02-21, mobile update and versioning) and the Phase 1 mobile MVP stabilization pass. Think of it as the "what did I miss" note for anyone reading the v1 self-hosting series.

## Committed changes since the last note

### CI/CD and deploy hardening

- Multiple deploy workflow improvements for TrueNAS reliability: Docker Compose permission fallbacks, data path writability checks, web artifact health verification after deploy.
- GitHub release publishing with changelog-driven release notes.
- Semver and release protocol scripts around APK version bumping.

### Backend and auth

- Registration conflict handling and clearer error paths.
- JWT and session handling refinements.
- Rate limit tuning.
- CORS improvement to allow localhost testing origin in production via an opt-in flag.
- Media and upload safety work including server icon size-limit enforcement.

### Web app and routing

- Added and iterated web app route handling.
- Deploy checks to catch stale web build or routing issues earlier.

### Mobile UX

- Auth UI and branding overhaul: typography, gradients, motion, wrapper cleanup.
- Layout passes across tabs, profile, and headers.
- Chat, input list, and animation iterations.

## Phase 1 mobile MVP stabilization (in-progress at time of writing)

### Invite-only registration

- Backend validation for `inviteCode`
- `signup_invites` table with transactional consume on register
- Admin operator script for creating invites

### Login improvements

- Username and email lookup now case-insensitive.

### Shared network config

- Introduced a single resolved host source for API and socket connections on mobile. Fixes the "why are some requests going to the wrong address" class of bugs.

### Startup and noise controls

- Protected route auth token guard in the API client.
- Reduced noisy console error patterns on expected transient failures.
- Socket error severity downgraded for expected transient connect failures.
- 429 warning throttle and optional debug logging toggles.

### Welcome screen and smart resume

- 4-second auto-dismiss with a skip option.
- Persists the last active chat ID, validates it on resume, falls back to the lobby if the chat is gone.

### Message ordering fixes

- Normalized message ordering for the inverted list.
- Optimistic and socket messages now insert consistently.

### Scope pruning

- Friends tab removed from the active tab layout.
- Friends screen route file removed from active mobile routes.
- Push and update prompt surfaces removed from the active phase scope.

## Mobile test automation (Maestro)

Added a Maestro test scaffold with flows covering:
- Sanity capture
- Precondition: logged out
- Unauthenticated login layout
- Authenticated tab layout smoke test

Added npm scripts for repeatable runs: `maestro:test`, `maestro:test:auth`, `maestro:test:flow`.

## Verification status at the time

- TypeScript: passing with `npx tsc --noEmit`
- Server tests: passing with `npm test -- --runInBand`
- Maestro: simulator attach and sanity capture confirmed, full unauth flow dependent on Expo app load precondition

## Recommended next note (when Phase 1 merges)

A follow-up note should capture:
- Exact commit hash range for Phase 1
- Final MVP acceptance checklist pass/fail
- Post-merge residual risks and Phase 2 handoff

---
tags: [penthouse, checklist, mvp, execution, website-rebuild]
created: 2026-03-05
published_to_garden: true
visibility: public
---

# Copyable Rebuild Checklist

Use this if you want to follow the same "stability first" rebuild pattern. Go through phases in order and don't skip the exit gates.

## Phase A — Foundation

- [ ] Split the repo cleanly (`app`, `api`, `contracts`, `infra`)
- [ ] Lock contract schemas before writing any endpoints or UI
- [ ] Set up typecheck, lint, and test gates
- [ ] Make the local stack boot with one command

**Exit:**
- [ ] Contracts compile
- [ ] Validation scripts run and correctly fail on bad code

## Phase B — Identity

- [ ] Invite-only registration
- [ ] Login and logout
- [ ] Refresh token rotation
- [ ] Deterministic auth error handling

**Exit:**
- [ ] Expired and invalid tokens are handled consistently
- [ ] Token replay regression tests pass

## Phase C — Core Chat

- [ ] Chat list and message history
- [ ] Realtime send and receive
- [ ] Idempotent send via `clientMessageId`
- [ ] Basic media upload

**Exit:**
- [ ] No duplicate messages under reconnect and race tests
- [ ] Unauthorized chat access is blocked

## Phase D — Reliability Layer

- [ ] Cache recent chats and messages locally
- [ ] Queue unsent messages while offline
- [ ] Retry with bounded backoff
- [ ] Reconnect room join and resync behavior

**Exit:**
- [ ] API restart drill passes
- [ ] Network drop drill passes
- [ ] Queue drains on recovery

## Phase E — Release Gate

- [ ] Smoke tests pass end-to-end
- [ ] Performance and error thresholds reviewed
- [ ] Rollback runbook tested at least once
- [ ] Internal-only release first

**Exit:**
- [ ] No critical open bugs
- [ ] Human approval logged for any high-risk items

## Commands

```bash
npm run validate
npm run scenario:test
npm run release:gate
```

Integration tests with a real database:

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/app_test \
JWT_SECRET=your-test-secret-here \
  npm --workspace services/api run test
```

## Project state when this checklist was drafted (2026-03-12)

Done:
- [x] Invite auth and refresh rotation
- [x] Shared chat
- [x] Media upload and rendering
- [x] Realtime hardening

Still in progress:
- [ ] Full UI recovery across mobile screens
- [ ] Client-side test-notice acknowledgement UX
- [ ] Strict DB release gate rerun in a working environment

Operating mode at the time: public rollout paused, internal-only candidate until UI was signed off.

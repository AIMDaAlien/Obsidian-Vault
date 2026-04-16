---
tags: [penthouse, reliability, bugs, postmortem]
created: 2026-03-05
published_to_garden: true
visibility: public
---

# Reliability Fix Log

Real bugs that showed up, what caused them, and how they got fixed. This is the "things that'll bite you" log.

## Fix 1: Refresh token replay race

**Symptom:** Two concurrent refresh calls could both succeed from the same old refresh token.

**Root cause:** The flow was checking token existence before the delete-and-rotate, leaving a gap where two requests could both pass the check before either one completed the delete.

**Fix:** Atomic delete-if-valid using `RETURNING user_id`, then insert the new token in the same transaction.

**Files touched:**
- `services/api/src/routes/auth.ts`
- `services/api/test/integration-auth.test.ts` (concurrency regression test)

## Fix 2: Message idempotency race

**Symptom:** Concurrent duplicate sends with the same `clientMessageId` could throw DB unique constraint violations instead of silently deduplicating.

**Root cause:** The query-then-insert pattern had a race window under concurrency.

**Fix:** Conflict-safe insert with `INSERT ... ON CONFLICT (chat_id, sender_id, client_message_id) DO NOTHING`, then a fallback select for the existing row.

**Files touched:**
- `services/api/src/routes/chats.ts`
- `services/api/src/realtime/socket.ts`
- `services/api/test/integration-chats.test.ts` (concurrency regression test)

## Fix 3: Corrupt local user cache crash

**Symptom:** App could crash on startup if the stored user data was invalid JSON.

**Root cause:** Raw `JSON.parse` with no guard around it.

**Fix:** Safe parse with a shape check and a null fallback so a corrupt cache just logs you out instead of crashing.

**File touched:**
- `apps/mobile/src/services/http.ts`

## Fix 4: Stuck "sending" state when socket ack was delayed

**Symptom:** Some messages would stay in a local "sending" state even after the HTTP send had already succeeded.

**Root cause:** The UI was relying mainly on socket ack/new events to finalize local message IDs. If the ack was slow or missed, the message just sat there.

**Fix:** Reconcile delivery state from the HTTP `sendMessage` response first, then use the socket ack as a secondary confirmation.

**Files touched:**
- `apps/mobile/src/App.vue`
- `apps/mobile/src/App.test.ts`

## Other hardening already landed

- Socket auth token now refreshes dynamically on reconnect.
- `chat.join` re-emits on reconnect to rejoin the right rooms.
- Queue flush handles per-item failures so one bad item doesn't block everything else.
- Mobile test harness migrated to Vitest with coverage for the optimistic message flow.
- Observability hook logs structured request data for debugging.

## Still-open risks (as of initial logging)

1. Integration suites skip if `DATABASE_URL` isn't set — CI has to always provide a real DB.
2. Socket auth failure counter is logged but there's no alert threshold wired in production yet.
3. The TrueNAS setup means manual reliability drills should still happen before releases.

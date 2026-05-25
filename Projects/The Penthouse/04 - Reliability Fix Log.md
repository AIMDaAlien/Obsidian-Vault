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


---

## Fix 5: Svelte 5 `effect_orphan` crash on chat page load

**Symptom:** App crashed with 500 error immediately after login when navigating to chat view. Console showed `Svelte error: effect_orphan`.

**Root cause:** `$effect` was called inside a `.svelte.ts` module-level store factory (`createSocketStore()`). Svelte 5 requires `$effect` to run during component initialization, not at module level.

**Fix:** Moved the auto-connect/disconnect `$effect` from `socket.svelte.ts` to `+layout.svelte` where it runs inside a component context. Added guard `if (socket?.connected || state === 'connecting') return;` to prevent duplicate socket creation.

**Files touched:**
- `apps/web/src/lib/stores/socket.svelte.ts` — removed `$effect`, added connecting guard
- `apps/web/src/routes/+layout.svelte` — added `$effect` for socket auto-connect

---

## Fix 6: Edit/Delete real-time sync not reaching other clients

**Symptom:** When User A edited or deleted a message, User B had to reload the page to see the change. No console logs appeared for `message.edited` or `message.deleted`.

**Root cause:** The frontend calls REST API (`PATCH /messages/:id`, `DELETE /messages/:id`) for edit/delete operations. The backend REST handlers updated the DB but never broadcasted Socket.IO events. Only the Socket.IO `message.edit`/`message.delete` handlers emitted events — but the frontend never sent those.

**Fix:** Added `fastify.io.to('chat:${chatId}').emit('message.edited', ...)` and `fastify.io.to('chat:${chatId}').emit('message.deleted', ...)` to the REST PATCH and DELETE handlers, matching the pattern already used for `POST /chats/:id/messages`.

**Files touched:**
- `services/api/src/routes/chats.ts` — added socket broadcasts to PATCH and DELETE handlers

---

## Fix 7: Composer disabled when offline, preventing outbox usage

**Symptom:** When the socket disconnected (offline/throttled), the message composer input was completely disabled. Users could not draft messages to queue for later delivery.

**Root cause:** `MessageComposer` had `disabled={!socketStore.isConnected}` passed from the chat page. The outbox store exists to queue messages when offline, but the UI blocked all input.

**Fix:** Removed the `disabled` prop binding. Added a visual pending indicator (◌) to `MessageBubble` for messages where `id === clientMessageId` (not yet server-acknowledged). The existing `sendMessage()` function already queued to the outbox when `!socketStore.isConnected`.

**Files touched:**
- `apps/web/src/routes/chat/[id]/+page.svelte` — removed `disabled={!socketStore.isConnected}`
- `apps/web/src/lib/components/MessageBubble.svelte` — added `isPending` derived state + ◌ indicator

---

## Fix 8: CAPTCHA blocking automated browser testing

**Symptom:** AntiGravity agent could not register test accounts because it couldn't solve the Altcha CAPTCHA widget.

**Root cause:** The Altcha widget rendered in all environments and required a challenge solution for registration.

**Fix:** Made CAPTCHA conditional on environment:
- Backend: `if (isProduction && !verifyChallenge(...))` — skips entirely in dev
- Frontend: `{#if !skipCaptcha}` hides widget in dev, auto-sends dummy token
- `PUBLIC_SKIP_CAPTCHA=true` added to `apps/web/.env` as belt-and-suspenders
- `skipCaptcha = dev || env.PUBLIC_SKIP_CAPTCHA === 'true'`

**Files touched:**
- `services/api/src/routes/auth.ts` — added `isProduction` guard
- `apps/web/src/routes/auth/+page.svelte` — conditional widget rendering + dummy token
- `apps/web/.env` — added `PUBLIC_SKIP_CAPTCHA=true`

---

## Fix 9: Auth button contrast failure (WCAG AA)

**Symptom:** Axe accessibility scan flagged gold-on-white text as 2.23:1 contrast ratio (fails WCAG AA 4.5:1).

**Root cause:** Active tab button used `var(--color-accent)` (gold `#C9A96E`) with white text.

**Fix:** Changed active tab text to dark `#12121C` on gold background. Axe scan now passes zero violations.

**Files touched:**
- `apps/web/src/routes/auth/+page.svelte` — `.tab.active` color change

---

## Other hardening landed in v4

- `IntersectionObserver` created once, observes new bubbles incrementally (previously recreated on every message)
- Socket listener reattachment on reconnect via `$effect(() => socketStore.instance)`
- Per-user typing timer Map prevents stale closure races (previously single timer variable)
- Graceful shutdown: SIGTERM/SIGINT drain Fastify connections and close DB pool
- Security updates: `@fastify/jwt` 9→10 (critical JWT vulns), `@fastify/static` 8→9 (path traversal), `drizzle-orm` 0.38→0.45

## Still-open risks (as of v4)

1. `esbuild` moderate vulnerabilities (dev-only via `drizzle-kit`) — will resolve when `drizzle-kit` updates.
2. Actual push notification delivery needs manual background-browser test.
3. Bio field exists in backend schema but has no UI input in settings page.
4. `alert()`/`prompt()` for edit/delete works but is poor UX on iOS PWA — custom modal needed.


---

## Fix 10: Push settings toggle shows "Enabled" after unsubscribe + reload

**Symptom:** After toggling push OFF and reloading the settings page, the toggle still showed "Enabled".

**Root cause:** `PushSettings.svelte` only read `Notification.permission` on mount. Browser permission stays "granted" even after unsubscribing from push. The component never queried the actual service worker subscription.

**Fix:** Query `getCurrentSubscription()` (which calls `pushManager.getSubscription()` on the service worker) on mount and after toggle:
- If permission is "granted" but no active subscription → show OFF
- If permission is "granted" and subscription exists → show ON

**Files touched:**
- `apps/web/src/lib/components/PushSettings.svelte` — added `getCurrentSubscription` import, async mount, post-toggle re-query

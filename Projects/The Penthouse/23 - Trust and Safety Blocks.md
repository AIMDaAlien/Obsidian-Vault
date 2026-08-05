---
tags: [penthouse, trust-safety, blocks, dm, presence]
created: 2026-08-04
updated: 2026-08-04
published_to_garden: false
visibility: private
---

# Trust and Safety Blocks

## Status on 2026-08-04

The block feature exists in the `trust-safety/blocks` worktree. GLM completed a second fix round and Kimi reported the branch green, but it is **not committed or deployed**. A follow-up read-only comparison found two remaining report/code mismatches plus missing permanent race-test coverage, so the branch should not be committed yet.

## What is implemented

- Migration `043_user_blocks.sql` adds `user_blocks` with a unique blocker/blocked pair, a self-block check, cascading user references, and indexes in both directions.
- Contracts expose `blockedByMe` and direction-neutral `directContactAllowed`. They deliberately do not expose a `blocksMe` field.
- Blocking is enforced for direct-message creation, DM-request creation and acceptance, sends, thread replies, forwards, edits, reactions, pins, typing, notifications, and push paths.
- A block declines pending DM requests in either direction. Unblock does not recreate or accept them.
- Existing DM history stays readable. Read receipts and deleting your own message remain allowed.
- Group messaging remains usable between a blocked pair.
- Presence and DM typing are suppressed between the pair; group activity is otherwise left alone.
- The web UI has Block/Unblock controls, a confirmation modal, a blocked-members Settings section, and a read-only DM banner.

## Kimi verification

Kimi completed a second verification pass after GLM's round-two fixes:

- Contracts, API, and web typechecks passed with zero errors or warnings.
- Lint passed across all workspaces.
- Format passed after Prettier corrected three touched files.
- API tests: 272 passed, 0 failed, 0 skipped.
- Web unit tests: 57 passed.
- Migration `043_user_blocks.sql` applied cleanly and matched the Drizzle schema.
- Temporary targeted race tests covered block versus DM creation, send, DM-request acceptance, unblock versus DM creation, and live presence/typing cleanup. They passed, but Kimi deleted the temporary files afterward.
- Socket-level runtime checks confirmed symmetric DM blocking, presence suppression, typing cleanup, group-message continuity, readable history, and no notification for rejected blocked sends.
- `apps/web/e2e/blocks.spec.ts` passed in Chromium.

Kimi also aligned the E2E assertion with the actual banner copy, formatted `lifecycle-routes.ts`, and fixed the E2E unblock assertion so it waits for the blocked row to disappear before checking API state.

## Round-two fixes confirmed in code

- `createDirectChatTx` checks the block state before returning an existing DM.
- DM-request acceptance now performs the pair lock, block check, accepted update, chat creation/reuse, and `chat_id` update in one transaction.
- `unblockUser` now uses the pair advisory lock.
- `typing.start` and the block cleanup path share a single-instance in-memory pair mutex.
- Profile block/unblock refreshes symmetric `directContactAllowed` state.
- Chat-page block-status loading ignores stale responses after navigating to another DM.
- The integration-test `blockStatus` type now includes `directContactAllowed`.

## Pre-commit work still required

1. `users/[id]/+page.svelte` still assigns `member`, block status, and `loading` after asynchronous requests without checking that the route still points at the same user. Add a request token or current-ID guard so rapid profile navigation cannot apply stale state.
2. The Web Push block re-check is not immediately before `webPush.sendNotification`; unread/chat/subscription queries and the subscription loop still follow it. FCM filters when selecting tokens but does not re-check before each provider send. Move the best-effort check into each per-recipient delivery loop and keep the unavoidable external-provider window documented.
3. Keep deterministic regression tests for the new pair-lock, atomic-accept, unblock, and typing-mutex behavior. Temporary tests that are deleted after verification do not protect these concurrency guarantees from future regressions.
4. Presence fan-out reads the block set once before emitting. A pre-block broadcast can arrive after the block's offline flush and remain stale until another event or reload. The socket-initialization error path also emits the entire unfiltered presence cache when its database work fails. Filter that fallback and close or explicitly correct the in-flight ordering gap before calling presence suppression complete.

## Accepted single-instance boundaries

- A push can still escape in the external provider window between the final local block check and Web Push/FCM delivery.
- The typing mutex and active-typing cache are process-local. Horizontal API scaling would require shared coordination such as Redis; the current deployment is single-instance.
- Low-priority cleanup: settled `pairMutexes` entries are retained for the API process lifetime. This is bounded and harmless at the current 15-25-user scale; clean them up before horizontal or materially larger use.

## Separate cleanup

The web app requests `GET /api/v1/chats/{dmId}/channels` for DMs. The API correctly returns 400 because DMs cannot have channels, but the request creates console/network noise. This predates blocks and should be fixed in a separate ticket.

## Next handoff

- GLM: make only the remaining pre-commit fixes; do not run the verification suites.
- Kimi: retain the deterministic race coverage, then rerun the focused checks, API/web suites, and Chromium E2E.
- Commit only after Kimi's clean report and a final diff review.

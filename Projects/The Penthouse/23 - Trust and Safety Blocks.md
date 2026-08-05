---
tags: [penthouse, trust-safety, blocks, dm, presence]
created: 2026-08-04
updated: 2026-08-04
published_to_garden: false
visibility: private
---

# Trust and Safety Blocks

## Status on 2026-08-04

The block feature exists in the `trust-safety/blocks` worktree. It has broad automated and manual verification, but it is **not committed or deployed**. A final review found concurrency and stale-state seams that must be fixed before commit.

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

Kimi completed the verification pass after GLM's implementation:

- Contracts, API, and web typechecks passed with zero errors or warnings.
- Lint passed across all workspaces.
- Format passed after Prettier corrected three touched files.
- API tests: 272 passed, 0 failed, 0 skipped.
- Web unit tests: 57 passed.
- Migration `043_user_blocks.sql` applied cleanly and matched the Drizzle schema.
- Socket-level runtime checks confirmed symmetric DM blocking, presence suppression, typing cleanup, group-message continuity, readable history, and no notification for rejected blocked sends.
- `apps/web/e2e/blocks.spec.ts` passed in Chromium.

Kimi also aligned the E2E assertion with the actual banner copy: "sending and interactions are disabled."

## Pre-commit fixes still required

1. `createDirectChat` currently returns an existing DM before its inside-lock block check. Move the block check before that return.
2. DM-request acceptance updates the request before chat creation. Put the pair lock, block check, accepted update, chat creation/reuse, and `chat_id` update in one transaction so failure rolls everything back.
3. `unblockUser` must use the same pair advisory lock as block and direct-message mutations.
4. Typing, presence, notification, Web Push, and FCM paths still contain check-then-emit/send windows. Either close those races or narrow the documented guarantee honestly.
5. Profile block/unblock must refresh both `blockedByMe` and `directContactAllowed`; chat status loading must ignore stale responses after navigation.
6. Correct the incomplete `blockStatus` return type in `integration-blocks.test.ts`.

## Separate cleanup

The web app requests `GET /api/v1/chats/{dmId}/channels` for DMs. The API correctly returns 400 because DMs cannot have channels, but the request creates console/network noise. This predates blocks and should be fixed in a separate ticket.

## Next handoff

- GLM: make only the pre-commit fixes; do not run the verification suites.
- Kimi: rerun deterministic concurrency checks, API/web suites, and Chromium E2E.
- Commit only after Kimi's clean report and a final diff review.


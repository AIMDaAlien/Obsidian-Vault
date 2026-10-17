---
tags: []
created: 2026-10-12
publish: false
project: Penthouse
---
# Plan 004: Kick sockets out of chat rooms the moment membership or a block changes

> **Executor instructions**: Follow this plan step by step. Run every verification
> command and confirm the expected result before moving to the next step. If
> anything in "STOP conditions" happens, stop and report — do not improvise.
> When done, update this plan's status row in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 2bea709..HEAD -- services/api/src/realtime/socket.ts services/api/src/routes/chat/shared.ts services/api/src/features/blocks/service.ts services/api/src/routes/chat/member-routes.ts`
> If non-empty, re-read the "Current state" excerpts against the live files; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: M (most of it is writing the two integration tests)
- **Risk**: MED (touches realtime delivery; a wrong room name silently drops events for real users)
- **Depends on**: plans/001-patch-dependency-advisories.md
- **Category**: security / correctness
- **Planned at**: commit `2bea709`, 2026-09-02

## Why this matters

Socket.IO rooms are joined once, at handshake, from the membership table
(`services/api/src/realtime/socket.ts:240-248`), and again on an explicit
`chat.join` (`socket.ts:386-390`, which correctly re-checks membership). Nothing
in the codebase ever removes a socket from a room: `grep -rn socketsLeave services/api/src | wc -l`
→ `0`. So when a user is removed from a group, leaves a chat, or is blocked,
their still-open socket keeps receiving that chat's events (`message.new`,
`chat.updated`, typing) until they happen to reconnect. For a private messaging
app that is a real disclosure window: the removed member reads new messages from
a conversation they are no longer in, and can keep seeing typing indicators.

## Current state

- Room naming convention, used everywhere: `chat:${chatId}` and `user:${userId}`.
  - Handshake join: `services/api/src/realtime/socket.ts:240` (`socket.join(\`user:${payload.userId}\`)`)
    then `:246-248` (loop over `chatMembers` rows joining `chat:${member.chatId}`).
  - Explicit join/leave: `socket.ts:386-390` (`chat.join`, guarded by
    `assertChatMember`) and `socket.ts:425-431` (`chat.leave`, client-driven).
- `fastify.io` is typed and available on the HTTP side —
  `services/api/src/types.ts:18` (`io: Server;`).
- HTTP → realtime fan-out helper, the pattern to imitate:
  `services/api/src/routes/chat/shared.ts:110-122`:

  ```ts
  export async function emitToChatMembers(
    fastify: FastifyInstance,
    chatId: string,
    event: string,
    payload: unknown
  ) {
    const members = await db
      .select({ userId: chatMembers.userId })
      .from(chatMembers)
      .where(eq(chatMembers.chatId, chatId));
    for (const member of members) {
      fastify.io.to(`user:${member.userId}`).emit(event, payload);
    }
  }
  ```

- Group membership removal (the biggest hole), `services/api/src/routes/chat/shared.ts:61-108`,
  `removeMemberFromGroup(rootChatId, memberUserId, actorUserId, mode)`. Inside the
  transaction it computes the affected chats and deletes the rows:

  ```ts
    const channels = await childChannels(rootChatId, tx);
    const chatIds = [rootChatId, ...channels.map((channel) => channel.id)];
    await tx
      .delete(chatMembers)
      .where(and(eq(chatMembers.userId, memberUserId), inArray(chatMembers.chatId, chatIds)));
  ```

  Callers: `services/api/src/routes/chat/member-routes.ts:146` (manager removal)
  and `:251-256` (self leave). Note the deleted set includes **child channels** —
  the eviction must cover all of `chatIds`, not just the root.
- Blocks are symmetric and enforced through one chokepoint,
  `services/api/src/features/blocks/service.ts` (`isBlocked`, `acquirePairLock`,
  and two transactions at `:143` and `:178`). When a block is created, any DM
  chat between the pair must stop streaming to both sides.
- Existing realtime integration suite to extend:
  `services/api/test/integration-realtime.test.ts` (uses `socket.io-client`,
  boots the app, connects two authenticated clients). Read it before writing
  tests — it already has login/registration helpers.
- Test conventions: `node:test` + `assert`, files in `services/api/test/`, run
  serially (`--test-concurrency=1`) against `penthouse_test`.

## Commands you will need

| Purpose | Command | Expected on success |
| --- | --- | --- |
| API unit tests | `npm --workspace @penthouse/api run test` | all pass (needs Postgres: `npm run db:start`) |
| API integration (this plan's gate) | `npm --workspace @penthouse/api run test:integration` | all pass, including `integration-realtime.test.ts` |
| Typecheck | `npm --workspace @penthouse/api run typecheck` | exit 0 |
| Whole gate | `npm run validate` | exit 0 |

## Scope

**In scope** (the only files you should modify):

- `services/api/src/routes/chat/shared.ts` (add the eviction helper; call it from `removeMemberFromGroup`)
- `services/api/src/routes/chat/member-routes.ts` (pass `fastify` where the helper needs it)
- `services/api/src/features/blocks/service.ts` (evict both sockets from shared DM rooms on block creation)
- `services/api/src/realtime/socket.ts` **only** if a server-side `chat:${id}` room needs a defensive re-check on incoming room-scoped events; otherwise leave it alone
- `services/api/test/integration-realtime.test.ts` (add the two regression tests)

**Out of scope** (do NOT touch, even though they look related):

- Presence code in `socket.ts` (`presence:global`, `userPresenceCache`,
  `onlineUserSockets`) — delicate, unrelated to membership.
- `apps/web/src/**` — no client changes; the client re-joins on its own and a
  server-side eviction must be invisible to it.
- The block-check chokepoint semantics (`isBlocked`, `acquirePairLock`) — already
  correct, do not refactor.
- `services/api/src/features/channels/routes.ts` channel creation.

## Git workflow

- Branch: `advisor/004-socket-room-revocation`
- Commit style: `fix(realtime): evict sockets when chat membership ends`, `test(api): removed member stops receiving chat events`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Add one eviction helper

In `services/api/src/routes/chat/shared.ts`, next to `emitToChatMembers`, add:

```ts
export function evictFromChatRooms(fastify: FastifyInstance, chatIds: string[]) {
  for (const chatId of chatIds) {
    fastify.io.in(`chat:${chatId}`).socketsLeave(`chat:${chatId}`);
  }
}
```

Do **not** disconnect sockets (`io.in(...).disconnectSockets()` is wrong here: it
kills the user's whole connection, including chats they are still in).
`socketsLeave` drops one room and keeps the socket alive; the client's own
`chat.join` will re-join only chats it can still prove membership in
(`socket.ts:386-390` re-checks `assertChatMember`).

**Verify**: `npm --workspace @penthouse/api run typecheck` → exit 0.

### Step 2: Evict on group member removal and on self-leave

`removeMemberFromGroup` currently has no access to `fastify`. Give it the
instance (add a `fastify: FastifyInstance` parameter, matching how
`emitToChatMembers` receives it) and, **after** the transaction resolves, call
the eviction with the same `chatIds` the transaction deleted against (root plus
child channels). Capture `chatIds` into a variable outside the transaction so it
survives.

Then update both callers in `services/api/src/routes/chat/member-routes.ts`
(`:146` manager removal, `:251-256` self leave) to pass `fastify`.

Order matters: evict **after** the DB commit, never inside the transaction, so a
rolled-back removal cannot silently eject someone.

**Verify**: `grep -n "evictFromChatRooms" services/api/src/routes/chat/shared.ts services/api/src/routes/chat/member-routes.ts` → definition + ≥2 call sites.

### Step 3: Enumerate the other membership-loss paths and cover them

Find every place membership ends, then add the same post-commit eviction:

```sh
grep -rn "delete(chatMembers)" services/api/src
grep -rn "deleteChat\|delete chat\b" services/api/src/routes/chat/lifecycle-routes.ts
```

Expected: the deletion inside `removeMemberFromGroup`, plus chat-delete /
group-disband paths. For each path found outside those two files, add the
eviction call with the affected chat ids, post-commit. If a path deletes chats
for **all** members, evict the room once (no per-user loop needed).

**Verify**: `grep -rc "evictFromChatRooms" services/api/src --include="*.ts" | grep -v ":0"` → ≥3 files.

### Step 4: Evict on block creation

In `services/api/src/features/blocks/service.ts`, in the block-creation
transaction path (the one at `:143`), after commit: resolve any direct-chat ids
between the pair and call `evictFromChatRooms` for them. Reuse the existing
query style from this file (`select ... from chatMembers`/`chats` with the pair).
If the block service has no `fastify` handle, do **not** pass one through from
the HTTP layer ad hoc — instead export a tiny
`emitBlockSideEffects(fastify, pair)` from the realtime module and call it from
the route. Choose whichever matches how the existing code reaches `fastify.io`
(`services/api/src/types.ts:18`) and say which you chose in the report.

**Verify**: `npm --workspace @penthouse/api run test` → existing
`integration-blocks.test.ts` and `push-block-filter.test.ts` still pass.

### Step 5: Regression tests (the real deliverable)

Extend `services/api/test/integration-realtime.test.ts` with two tests, reusing
its existing connect/login helpers:

1. **Removed member stops receiving.** Two authenticated clients in a group; the
   manager removes one via the HTTP endpoint; a message is then sent as the
   remaining member; assert the removed client receives **no** `message.new`
   within a short grace window, while the remaining client **does** (the second
   half matters — it proves you did not break delivery).
2. **Block stops the DM stream.** Two clients in a DM; one blocks the other via
   the HTTP endpoint; assert no `message.new` reaches either side afterwards
   (and that neither socket was force-disconnected — assert the blocked client
   can still receive a room it legitimately belongs to, e.g. a third group).

Model assertion timing on the existing realtime tests (they already await
emitted events); avoid bare `setTimeout` sleeps where the file already has a
helper.

**Verify**: `npm --workspace @penthouse/api run test:integration` → all pass,
including the two new tests (they must fail if you temporarily comment out the
Step 2 eviction call — confirm that once, then restore).

## Test plan

- Two new tests inside `services/api/test/integration-realtime.test.ts`
  (described in Step 5). Both must be proven to fail without the fix.
- Existing suites that must stay green: `integration-realtime.test.ts`,
  `integration-blocks.test.ts`, `integration-chats.test.ts`,
  `integration-groups.test.ts`, `integration-channels.test.ts`,
  `integration-dm-requests.test.ts`, `push-block-filter.test.ts`.

## Done criteria

- [ ] `grep -rn socketsLeave services/api/src | wc -l` → ≥ 1 (was 0)
- [ ] `grep -rn "delete(chatMembers)" services/api/src` → every hit has a post-commit eviction covering the same chat ids
- [ ] `npm --workspace @penthouse/api run test:integration` exits 0 including the 2 new tests
- [ ] `npm run validate` exits 0
- [ ] Only files in the Scope list changed (`git status --porcelain`)
- [ ] `plans/README.md` status row for 004 → DONE

## STOP conditions

Stop and report if:

- `socketsLeave` turns out not to exist in the installed Socket.IO version (it does in 4.8.x; if the installed major differs, STOP).
- Evicting a room starts dropping events for users who are still members (means room naming is not uniform — STOP and report what you found instead of renaming rooms).
- A membership-loss path deletes rows without knowing the affected chat ids (you would have to add a query; that is fine, but if the query needs a new index, STOP).
- The realtime suite is already failing before your changes.

## Maintenance notes

- Any future feature that ends membership (mute-with-removal, channel
  re-scoping, admin "remove from all channels") must call `evictFromChatRooms`
  after commit. Reviewer's rule: a diff that deletes from `chatMembers` without
  a matching eviction is incomplete.
- Client-side assumption to preserve: the web client may keep thinking it is in
  a chat until it re-joins. If the UI stops updating for a removed member, the
  fix belongs in the client's join logic, not by weakening the eviction.
- Deferred: per-message server-side membership re-check (defence in depth, costs
  a query per send). If you want it, brief the primary agent first.

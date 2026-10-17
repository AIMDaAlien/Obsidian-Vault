---
tags: []
created: 2026-10-12
publish: false
project: Penthouse
---
# Plan 008: Expose an operator status metrics endpoint with a short in-memory history

> **Executor instructions**: Follow this plan step by step. Run every verification
> command and confirm the expected result before moving to the next step. If
> anything in "STOP conditions" happens, stop and report — do not improvise.
> When done, update this plan's status row in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 2bea709..HEAD -- services/api/src/utils/operatorDiagnostics.ts services/api/src/routes/admin.ts services/api/src/app.ts services/api/src/realtime/socket.ts`
> If non-empty, re-read the "Current state" excerpts; on a mismatch, STOP.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: MED (new instrumentation in the request path; must be cheap and must not leak internals)
- **Depends on**: plans/003-build-pipeline-and-committed-bundle.md (metrics that report the
  deployed build id are only honest once the pipeline builds the artifact),
  plans/004-socket-room-revocation.md and plans/005-global-rate-limit.md
  (so room counts and 429 counts are real signals worth charting)
- **Category**: direction / observability
- **Planned at**: commit `2bea709`, 2026-09-02
- **Owner**: Codex (backend/framework). The page on top of it is plan 009 (Qwen3.8).

## Why this matters

Aim wants a status page with more useful metrics than what exists. The building
blocks are already there but only reachable through one heavy admin payload:
`GET /api/v1/admin/summary` (`services/api/src/routes/admin.ts:139`) fires ~10
parallel queries plus a filesystem scan every call, and returns no history, no
request-rate or latency signal, no socket-connection count, and no rate-limit
counters. So today "is the app healthy?" is answered by opening a laptop, and a
status page built on `/admin/summary` would hammer the database every refresh.

This plan gives the status page one cheap endpoint with a bounded in-memory
history, plus the counters that matter for a realtime app (live sockets, 429s,
5xx by route group, push delivery, backup freshness). No new dependencies.

## Current state

- `services/api/src/utils/operatorDiagnostics.ts` (260 lines) already provides:
  - `getBuildRuntimeDiagnostics()` (`:132`) → `{ startedAt, uptimeSeconds, version, buildId, deployedAt }`
    (from `OPS_BUILD_ID` / `OPS_DEPLOYED_AT` env, set in
    `infra/compose/docker-compose.production.yml`).
  - `getUploadDiagnostics()` (`:142`) with a 60s TTL cache
    (`UPLOAD_SCAN_TTL_MS`, `MAX_UPLOAD_SCAN_FILES = 5_000`).
  - `getBackupDiagnostics()` (`:174`) → reads `BACKUP_STATUS_PATH`, default
    `/app/uploads/ops/backup-status.json` (written by
    `scripts/nightly-pg-dump.sh` / `scripts/nightly-uploads-backup.sh`).
  - `recordPushSendSuccess/Failure/StaleTokenRemoval` + `getPushRuntimeDiagnostics()` (`:209-229`).
  - `recordServerError(url)` / `getErrorRuntimeDiagnostics()` (`:231-248`) —
    counts 5xx and groups them by route prefix via `classifyRouteGroup`
    (`:52-61`: admin/auth/chats/media/me/gifs/uploads/other, max
    `MAX_ERROR_ROUTE_GROUPS = 5`).
  - `resetOperatorDiagnosticsForTests()` (`:249`).
  - `recordServerError` is already wired: `services/api/src/utils/error-responses.ts:3`.
- `GET /api/v1/health` (`services/api/src/routes/health.ts:10-19`) does a
  `SELECT 1` with a 2s timeout and returns `{status, db}`; `/health` is a bare
  ok. Docker and Caddy healthchecks poll these every 30s
  (`infra/compose/docker-compose.production.yml`), so they must stay this cheap.
- Admin auth pattern: `services/api/src/routes/admin.ts:38-40`
  (`requireAdmin(request)` → 403 unless `request.authUser?.role === 'admin'`).
  Every admin route calls it first (e.g. `:136`).
- Socket server: `services/api/src/realtime/socket.ts`, mounted as
  `fastify.io` (`services/api/src/types.ts:18`). Rooms are `user:{id}` and
  `chat:{id}` (see plans 004). `io.fetchSockets()` / `io.engine.activeConnections`
  are the ways to count live connections in Socket.IO 4.8.
- DB pool: `services/api/src/db/pool.ts` exports `pool` (`pg`). `pg.Pool` exposes
  `totalCount` / `idleCount` / `waitingCount` — that is the pool signal, no new
  instrumentation needed.
- Rate limiting: `services/api/src/middleware/rateLimit.ts` throws
  `AppError('RATE_LIMITED', 429)`. If plan 005 landed, a global scope
  `'global'` exists; count rejections by hooking the same throw point.
- Test conventions: `node:test` + `assert/strict` in `services/api/test/`;
  model new tests on `services/api/test/operator-diagnostics.test.ts` (exists —
  read it first and extend rather than duplicating).

## Commands you will need

| Purpose | Command | Expected on success |
| --- | --- | --- |
| API unit tests | `npm --workspace @penthouse/api run test` | all pass (needs Postgres: `npm run db:start`) |
| API integration | `npm --workspace @penthouse/api run test:integration` | all pass |
| Typecheck | `npm --workspace @penthouse/api run typecheck` | exit 0 |
| Whole gate | `npm run validate` | exit 0 |
| Contract smoke | `npm --workspace @penthouse/api run test` includes `contracts-smoke.test.ts` | passes |
| Manual endpoint shape | `curl -s localhost:3000/api/v1/status -H "authorization: Bearer $TOKEN" | head -c 400` | JSON with the keys listed in Step 5 |

## Scope

**In scope** (the only files you should modify):

- `services/api/src/utils/operatorDiagnostics.ts` (counters + ring buffer)
- `services/api/src/routes/status.ts` (create)
- `services/api/src/app.ts` (register the route + the request-duration hook)
- `packages/contracts/src/*` (add the response schema — the repo's rule is
  contracts first; see `services/api/CLAUDE.md` "Adding a new route")
- `services/api/test/operator-diagnostics.test.ts` (extend)
- `services/api/test/integration-status.test.ts` (create)

**Out of scope** (do NOT touch, even though they look related):

- `/api/v1/health` and `/health` — must stay allocation-free and unthrottled.
- `GET /api/v1/admin/summary` — leave it alone; the admin UI depends on it. Do
  not migrate its queries into the new endpoint.
- `apps/web/src/routes/admin/+page.svelte` — the page is plan 009's job.
- Sentry/Prometheus/Grafana/Redis/anything hosted. Single-node app; no new
  dependency for this.

## Git workflow

- Branch: `advisor/008-status-metrics`
- Commit style: `feat(api): request duration + 429 counters`, `feat(api): /api/v1/status snapshot with history`, `feat(contracts): status snapshot schema`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Contracts first

Add a status snapshot schema to `packages/contracts` (follow the existing
feature-file style in that package; check `packages/contracts/src` for how
features are split and mirror it). The snapshot shape:

```ts
{
  generatedAt: string;          // ISO
  build: { version, buildId, deployedAt, startedAt, uptimeSeconds },
  db: { status: 'ok'|'unreachable', total, idle, waiting, latencyMs: { p50, p95, max } },
  http: {
    windowSeconds: number,
    requests: number,
    byStatusClass: { '2xx': number, '4xx': number, '5xx': number },
    rateLimited: number,
    slowestRoute: { url: string, p95Ms: number } | null,
  },
  realtime: { connectedSockets: number, rooms: { user: number, chat: number } },
  push: { successfulSends, failedSends, staleTokensRemoved, lastFailureAt },
  storage: { status, directoryBytes, fileCount, latestUploadAt, scanLimited },
  backup: { status, target, lastSuccessfulBackupAt },
  errors: { serverErrorCount, lastServerErrorAt, routeGroups: Array<{ group: string, count: number }> },
  history: Array<{ at: string; requests: number; p95Ms: number; connectedSockets: number; serverErrors: number }>,
}
```

**Verify**: `npm --workspace @penthouse/contracts run build` → exit 0.

### Step 2: Counters for request duration and status class

In `services/api/src/utils/operatorDiagnostics.ts`, add a fixed-size window:

```ts
const HTTP_WINDOW_MS = 60_000;
const httpSamples = { requests: 0, byStatusClass: { '2xx': 0, '4xx': 0, '5xx': 0 }, rateLimited: 0, latencies: [] as number[] };
export function recordHttpRequest(url: string | undefined, statusCode: number, durationMs: number): void { /* increment + push latency, cap array length */ }
export function getHttpRuntimeDiagnostics(): Snapshot['http'] { /* drain-free read of the current window */ }
```

Latency percentiles: keep a bounded array (cap it, e.g. 5_000 samples) and sort
a copy to compute p50/p95/max. Cap the per-route tracking to the existing
`MAX_ERROR_ROUTE_GROUPS`-style limit so memory stays flat. Add a
`ponytail:` comment naming the ceiling (in-process, single node, sampled) and
the upgrade path (export to Postgres or a real metrics sink if the app ever
scales past one process).

Also reset the window on a rolling basis (same lazy pattern already used for
rate-limit buckets: prune by timestamp, no `setInterval` in module scope).

**Verify**: `npm --workspace @penthouse/api run typecheck` → exit 0.

### Step 3: Wire one `onResponse` hook

In `services/api/src/app.ts`, after `setErrorHandler` (`:56`), add:

```ts
  fastify.addHook('onResponse', async (request, reply) => {
    recordHttpRequest(request.routeOptions?.url, reply.statusCode, reply.elapsedTime);
  });
```

`onResponse` gives `reply.elapsedTime` for free — do not add a `startTime` on
`onRequest`. Exclude the health route from latency stats (or bucket it as
`health`) so 30-second Docker probes do not flatten the percentiles. Count 429s
into `rateLimited` by checking `reply.statusCode === 429`.

**Verify**: `npm --workspace @penthouse/api run typecheck` → exit 0.

### Step 4: History ring buffer

Keep the last N (use 180) one-minute aggregates in a module-level array —
`{ at, requests, p95Ms, connectedSockets, serverErrors }` — appended by a
`setInterval(60_000).unref()` created **inside `buildApp()`** (not at module
load, so tests that import the module do not hold the process open). `unref()`
is mandatory or `node:test` hangs.

**Verify**: `npm --workspace @penthouse/api run test` → existing suites finish in
roughly the same time as before (no hang).

### Step 5: The endpoint

Create `services/api/src/routes/status.ts`:

- `GET /api/v1/status`, `preHandler: fastify.authenticate` then the same
  `requireAdmin`-style check used in `routes/admin.ts:38-40` (copy the helper
  pattern; do not export-and-share it across files unless the file already exists
  in a shared module).
- Response = the Step 1 contract, assembled from `getBuildRuntimeDiagnostics()`,
  `getUploadDiagnostics()`, `getBackupDiagnostics()`,
  `getPushRuntimeDiagnostics()`, `getErrorRuntimeDiagnostics()`,
  `getHttpRuntimeDiagnostics()`, pool counters, and
  socket counts from `fastify.io`.
- Wrap the DB piece so a DB failure returns `db.status: 'unreachable'` and HTTP
  `200`, not a 500: the status page must keep rendering when Postgres is down.
  Keep the response under ~10 KB — no message content, no user names, no emails,
  no paths outside `UPLOAD_DIR`, no secrets. Counts and durations only.
- Register it in `services/api/src/app.ts` next to the other route registrations.

**Verify**: start the dev API, then
`curl -s localhost:3000/api/v1/status -H "authorization: Bearer <admin token>"`
→ JSON containing all top-level keys from Step 1; `curl -s -o /dev/null -w '%{http_code}' localhost:3000/api/v1/status`
(no token) → `401`.

### Step 6: Do not let the status page become its own load problem

The endpoint must be safe to poll every 15-30 s from the page in plan 009:
- no filesystem scan per call (reuse the TTL-cached `getUploadDiagnostics()`),
- no `COUNT(*)` over `messages`/`chats` (that stays in `/admin/summary`),
- socket counts via `io.fetchSockets()` only if cheap at alpha scale; otherwise
  maintain counters on connect/disconnect in `socket.ts` and read the counters.
  Decide by measuring with 50 simulated connections and say which you chose.

**Verify**: with the dev API running, time 20 sequential calls:
`time (for i in $(seq 20); do curl -s -o /dev/null localhost:3000/api/v1/status -H "authorization: Bearer <token>"; done)`
→ total real time under 2s.

## Test plan

- Extend `services/api/test/operator-diagnostics.test.ts`:
  1. `recordHttpRequest` buckets by status class and counts 429 separately.
  2. p50/p95 computed from a known latency list (assert exact values).
  3. the sample array stays capped after more than the cap of recordings.
- New `services/api/test/integration-status.test.ts` (pattern:
  `services/api/test/integration-admin.test.ts` for the admin-auth dance):
  1. 401 without a token; 403 for a non-admin user.
  2. admin gets 200 with every top-level key present and `history` an array.
  3. response contains no email addresses or user names
     (`assert.match(JSON.stringify(body), /@|username/)` must **not** match —
     assert the absence, this is the privacy gate).
- Verification: `npm --workspace @penthouse/api run test` then
  `test:integration` → all pass.

## Done criteria

- [ ] `GET /api/v1/status` exists, requires an admin, and returns the contract shape
- [ ] `grep -n "onResponse" services/api/src/app.ts` → 1 line
- [ ] Poll cost proven: 20 sequential calls in under 2s (`time` output in the report)
- [ ] `/api/v1/health` still has no new work in it (`git diff services/api/src/routes/health.ts` → empty)
- [ ] `setInterval(...).unref()` present and no test hangs
- [ ] Privacy assertion test passes (no emails/usernames in the payload)
- [ ] `npm run validate` and both API test suites exit 0
- [ ] `plans/README.md` status row for 008 → DONE

## STOP conditions

Stop and report if:

- `reply.elapsedTime` is unavailable in the installed Fastify version.
- Counting sockets requires touching `socket.ts` presence logic (it must not);
  if the only cheap route is presence internals, stop and use `fetchSockets()`.
- The response exceeds ~10 KB or contains anything user-identifying.
- Plan 005 has not landed and you are tempted to add rate limiting here — that is
  005's job; report the order instead.

## Maintenance notes

- This is deliberately in-process: restart loses history
  (`ponytail:` comment marks it). The upgrade path when history matters is a
  `metrics_samples` table written by the same 60s tick, or shipping to a real
  metrics backend — brief the primary agent first.
- Plan 009 depends on the contract from Step 1. Any shape change must be made in
  `packages/contracts` first, then both sides, or the page silently renders
  blanks.
- Deferred: alerting (a webhook/Telegram ping on `lastFailureAt` change or
  `db.status !== 'ok'`). Worth doing once the page exists and the numbers prove
  stable; needs a secret, so its own plan.

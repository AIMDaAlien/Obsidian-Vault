---
tags: []
created: 2026-10-12
publish: false
project: Penthouse
---
# Plan 005: Put a default rate limit on every route, keeping the tighter hand-placed ones

> **Executor instructions**: Follow this plan step by step. Run every verification
> command and confirm the expected result before moving to the next step. If
> anything in "STOP conditions" happens, stop and report — do not improvise.
> When done, update this plan's status row in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 2bea709..HEAD -- services/api/src/app.ts services/api/src/middleware/rateLimit.ts services/api/src/config/env.ts`
> If non-empty, re-read the "Current state" excerpts against the live files; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P2 (P1 if registration is opened to the public before this lands)
- **Effort**: M
- **Risk**: MED (a too-tight default silently locks out real users; the default must be generous)
- **Depends on**: plans/001-patch-dependency-advisories.md
- **Category**: security
- **Planned at**: commit `2bea709`, 2026-09-02

## Why this matters

There is no global throttle. `services/api/src/app.ts` registers `cors`, `jwt`,
`multipart` and no rate-limiting plugin; throttling exists only where somebody
remembered it — 11 hand-placed `rateLimit(...)` call sites across auth, blocks,
embeds, media upload, and chat/DM mutations. Everything else is unthrottled:
media serving (`GET /api/v1/media/:id`), search, sync, invites, users directory,
admin reads, and the APK download path. Beta and public testers on one IP (an
office, a carrier NAT) plus normal crawler traffic will hammer those with
impunity, and each unthrottled read is a Postgres query.

The repo already has a working limiter with tests and a test-reset hook — reuse
it as a default rather than adding a dependency.

## Current state

- `services/api/src/middleware/rateLimit.ts` (70 lines) — the whole limiter:

  ```ts
  export function rateLimit(
    maxAttempts: number,
    windowMs = 15 * 60_000,
    options: RateLimitOptions = {}
  ) {
    return async (request: FastifyRequest, reply: FastifyReply) => {
      if (env.DISABLE_RATE_LIMIT) return;
      const identity = options.identity?.(request) ?? request.ip;
      const route = request.routeOptions?.url ?? request.url.split('?', 1)[0];
      const key = `${options.scope ?? `${request.method}:${route}`}:${identity}`;
      ...
  ```

  It returns a `preHandler`-shaped function, has a module-level `buckets` Map
  with pruning, sets `Retry-After`, throws `AppError('RATE_LIMITED', 429)`, and
  exposes `resetRateLimitBucketsForTests()` / `rateLimitBucketCountForTests()`.
- `authenticatedUserIdentity(request)` already exists in that file
  (`rateLimit.ts:19-21`) and returns `request.authUser?.userId ?? request.ip`.
  Note: as a *global* hook it cannot use it — the auth `preHandler` has not run
  yet, so `request.authUser` is undefined at that point. Global defaults must key
  on IP.
- Existing tighter limits to preserve (do not loosen any of these):
  `routes/auth.ts:48` register `rateLimit(3)`, `:105` login `rateLimit(5)`,
  `:125` refresh `rateLimit(10, 60_000)`, `:246` reset-password
  `rateLimit(5, 60_000)`; `routes/chat/message-routes.ts:31` mutations 60/min;
  `routes/chat/lifecycle-routes.ts:45` and `routes/dm-requests.ts:12` 30/min;
  `routes/blocks.ts:18,63,85`; `routes/embeds.ts:314,331,348`;
  `routes/media.ts:215` upload (env-driven).
- `services/api/src/app.ts:31-57` — where hooks/plugins get registered;
  `registerAuth(fastify)` is at `:53`, `setErrorHandler` at `:56`.
- Prod sits behind Caddy, so `request.ip` is the client IP **only if**
  `TRUST_PROXY` is true. It is: `infra/compose/docker-compose.production.yml:33`
  (`TRUST_PROXY: ${TRUST_PROXY:-true}`) and `app.ts:33`
  (`trustProxy: env.TRUST_PROXY`). Verify this before shipping or the global
  limiter will treat every visitor as one client.
- Test env forces the limiter on: `services/api/test/setup.mjs` sets
  `process.env.DISABLE_RATE_LIMIT = 'false'` (forced, not defaulted).
- Limiter unit test to extend: `services/api/test/auth-rate-limit.test.ts`
  (`[unit] route rate limiter prunes buckets and ignores query strings`).

## Commands you will need

| Purpose | Command | Expected on success |
| --- | --- | --- |
| API unit tests | `npm --workspace @penthouse/api run test` | all pass (needs Postgres: `npm run db:start`) |
| API integration | `npm --workspace @penthouse/api run test:integration` | all pass |
| Typecheck | `npm --workspace @penthouse/api run typecheck` | exit 0 |
| Whole gate | `npm run validate` | exit 0 |
| Health stays unthrottled | `curl -s -o /dev/null -w '%{http_code}\\n' $(for i in $(seq 1 400); do curl -s -o /dev/null -w '%{http_code} ' http://localhost:3000/api/v1/health; done | tr ' ' '\n' | sort | uniq -c)` | `400 200` (never 429) — dev server running |

## Scope

**In scope** (the only files you should modify):

- `services/api/src/app.ts` (register the default limiter hook)
- `services/api/src/config/env.ts` (two new optional env knobs + defaults)
- `services/api/src/middleware/rateLimit.ts` (only if a route-exemption list is needed)
- `services/api/test/rate-limit-global.test.ts` (create)
- `services/api/.env.example` (document the two knobs)

**Out of scope** (do NOT touch, even though they look related):

- The 11 existing `rateLimit(...)` call sites and their windows — tighter, keep.
- Socket-level limiting in `services/api/src/realtime/socket.ts` (`socketRateLimits`,
  `SOCKET_WINDOW_MS`) — separate mechanism, already works.
- `apps/web/src/lib/services/api.ts` — the client must not start retrying 429s;
  no client changes in this plan.
- Any Redis/central store idea. Single-node app, in-memory buckets are correct
  for now.

## Git workflow

- Branch: `advisor/005-global-rate-limit`
- Commit style: `feat(api): default rate limit on all routes`, `test(api): health is exempt from global limiter`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Two knobs in env

Add to `EnvSchema` in `services/api/src/config/env.ts`, next to the existing
upload-rate knobs (`UPLOAD_RATE_LIMIT_MAX_FILES`,
`UPLOAD_RATE_LIMIT_WINDOW_MINUTES` — copy their style):

```ts
    RATE_LIMIT_GLOBAL_MAX: z.coerce.number.int.positive().default(300),
    RATE_LIMIT_GLOBAL_WINDOW_MS: z.coerce.number.int.positive().default(60_000),
```

`RATE_LIMIT_GLOBAL_MAX=0` is not representable (`.positive()`), which is
deliberate: disabling must use `DISABLE_RATE_LIMIT`, not a zero.

**Verify**: `npm --workspace @penthouse/api run typecheck` → exit 0.

### Step 2: Register the default limiter as a global onRequest hook

In `services/api/src/app.ts`, after plugin registration and **before**
`registerAuth(fastify)` (so the hook is installed for every route), add a global
hook that reuses the existing limiter factory:

```ts
  const globalRateLimit = rateLimit(env.RATE_LIMIT_GLOBAL_MAX, env.RATE_LIMIT_GLOBAL_WINDOW_MS, {
    scope: 'global',
  });
  fastify.addHook('onRequest', async (request, reply) => {
    if (GLOBAL_RATE_LIMIT_EXEMPT_URLS.includes(request.routeOptions?.url ?? '')) return;
    await globalRateLimit(request, reply);
  });
```

with, in the same file (or `rateLimit.ts`, your choice — say which in the report):

```ts
const GLOBAL_RATE_LIMIT_EXEMPT_URLS = ['/health', '/api/v1/health'];
```

Exemptions are limited to health because Docker/Caddy healthchecks must never
be throttled (`infra/compose/docker-compose.production.yml` polls
`/api/v1/health` every 30s from two containers).

Because `scope: 'global'` is shared, one key is
`global:<ip>` — a single 300/min budget per IP across all API routes. That is
the intent (per-IP abuse budget), and route-specific tighter limits stay
separate.

**Verify**: `npm --workspace @penthouse/api run typecheck` → exit 0.

### Step 3: Prove the default applies and health does not

Create `services/api/test/rate-limit-global.test.ts`, modelled on
`services/api/test/auth-rate-limit.test.ts` (same `node:test` style, use
`buildApp()` and `app.inject`, call `resetRateLimitBucketsForTests()` in a
`beforeEach`-equivalent). For the test, set
`process.env.RATE_LIMIT_GLOBAL_MAX` before `buildApp()` import resolution if the
suite supports it; otherwise drive the limiter with a low override through the
exported factory. Assert:

1. A read route that has **no** route-specific limit (use
   `GET /api/v1/chats` with an authenticated user, or the simplest existing
   authenticated GET) returns `429` with code `RATE_LIMITED` once the global
   budget is exceeded, and the response carries a `Retry-After` header.
2. `/api/v1/health` returns `200` far more times than the global max (e.g. max 3,
   then 10 requests, all `200`).
3. A tighter route limit still wins over the global one (login at
   `rateLimit(5)`: the 6th attempt is `429` while the global budget is not yet
   reached).

**Verify**: `npm --workspace @penthouse/api run test` → all pass including the new file.

### Step 4: Confirm nothing legitimate got throttled

Run the integration suite twice in a row (the suite hammers endpoints and is the
most likely victim of a too-low default):

**Verify**: `npm --workspace @penthouse/api run test:integration` → all pass,
twice. If any suite starts failing with `429`, raise the default (Step 1) rather
than exempting routes one by one, and record the number you settled on.

### Step 5: Document the knobs

Add to `services/api/.env.example`:

```
# Global per-IP API budget (applies before route-specific limits).
RATE_LIMIT_GLOBAL_MAX=300
RATE_LIMIT_GLOBAL_WINDOW_MS=60000
```

**Verify**: `grep -n RATE_LIMIT_GLOBAL services/api/.env.example` → 2 lines.

## Test plan

- New: `services/api/test/rate-limit-global.test.ts` (three assertions listed in
  Step 3). Pattern: `services/api/test/auth-rate-limit.test.ts`.
- Must stay green: the whole `services/api/test/*.test.ts` unit set and the
  `integration-*` set. A 429 appearing anywhere in the integration suite means
  the default is too tight — raise it, do not whitelist.

## Done criteria

- [ ] `grep -n "addHook('onRequest'" services/api/src/app.ts` → 1 line, registered before route registration
- [ ] `RATE_LIMIT_GLOBAL_MAX` / `RATE_LIMIT_GLOBAL_WINDOW_MS` present in `env.ts` and `.env.example`
- [ ] `/api/v1/health` and `/health` exempt (test proves it)
- [ ] `npm --workspace @penthouse/api run test` and `test:integration` exit 0, integration run twice
- [ ] `npm run validate` exits 0
- [ ] `plans/README.md` status row for 005 → DONE

## STOP conditions

Stop and report if:

- `TRUST_PROXY` is not `true` in the production compose env (then the global
  limiter would key on Caddy's IP and throttle every user together). Verify with
  `grep -n TRUST_PROXY infra/compose/docker-compose.production.yml`.
- The integration suite cannot pass at any default below ~1000/min/IP — that
  means a hot loop in the app is hammering the API; report the route instead of
  shipping a 1000 default.
- `request.routeOptions?.url` is undefined inside the hook (Fastify version
  mismatch) — the exemption list would silently do nothing.

## Maintenance notes

- New public (unauthenticated) endpoints inherit 300/min/IP. Anything that costs
  more than a cheap query (search, embeds, media, thumbnail generation) needs a
  route-specific tighter limit, following `routes/embeds.ts:314` as the example.
- The bucket store is in-process. If the API ever runs with more than one
  replica, this limiter becomes per-replica; that is the moment to brief the
  primary agent on a shared store, not to add replicas silently.
- Known limitation left in place (deliberate, `ponytail` comment already applies):
  one shared `buckets` Map prunes with whichever window ran last
  (`rateLimit.ts:33-39`). Fine at alpha traffic; revisit if the map grows.

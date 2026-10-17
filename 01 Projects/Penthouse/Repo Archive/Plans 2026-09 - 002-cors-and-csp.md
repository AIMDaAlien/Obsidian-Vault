---
tags: []
created: 2026-10-12
publish: false
project: Penthouse
---
# Plan 002: Refuse wildcard CORS in production and put a Content Security Policy in front of the app

> **Executor instructions**: Follow this plan step by step. Run every verification
> command and confirm the expected result before moving to the next step. If
> anything in "STOP conditions" happens, stop and report — do not improvise.
> When done, update this plan's status row in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 2bea709..HEAD -- services/api/src/app.ts services/api/src/config/env.ts infra/compose/caddy/Caddyfile.production apps/web/svelte.config.js`
> If non-empty, re-read the "Current state" excerpts against the live files; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: M (half a day; the CSP half is the slow part)
- **Risk**: MED (a wrong CSP breaks the app in the browser; ship report-only first)
- **Depends on**: plans/001-patch-dependency-advisories.md (so the tests below run on patched deps)
- **Category**: security
- **Planned at**: commit `2bea709`, 2026-09-02
- **Owner split**: Codex does steps 1–3 (server + Caddy). Qwen3.8 does steps 4–5 (SvelteKit CSP + browser proof).

## Why this matters

Two related gaps in the same surface.

1. `services/api/src/app.ts` turns `CORS_ORIGIN='*'` into `origin: true` while also
   sending `credentials: true`. `@fastify/cors` then *reflects whatever origin the
   browser asks for*, so any website on the internet can make authenticated
   requests to the API from a victim's browser. Nothing rejects `*` in production,
   even though the same env file refuses to boot without `MEDIA_SIGNING_KEY`. One
   mis-set line in `infra/production.env` silently disables cross-site protection.
2. The production Caddy config sets HSTS, `nosniff`, `X-Frame-Options` and a
   referrer policy, but no `Content-Security-Policy`. The web client keeps its
   access and refresh tokens in `localStorage`
   (`apps/web/src/lib/stores/session.svelte.ts:5`) and renders sanitised embed
   HTML. A single injected script therefore equals full account takeover, with no
   browser-level mitigation to slow an attacker down.

## Current state

- `services/api/src/app.ts:34-46`:

  ```ts
  const corsOrigin =
    env.CORS_ORIGIN === '*'
      ? true
      : env.CORS_ORIGIN.split(',')
          .map((origin) => origin.trim())
          .filter(Boolean);

  await fastify.register(cors, {
    origin: corsOrigin,
    credentials: true,
  });
  ```

- `services/api/src/config/env.ts:36-40` (default is a localhost list):

  ```ts
  CORS_ORIGIN: z
    .string()
    .default(
      'http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174'
    ),
  ```

- `services/api/src/config/env.ts:55-63` — the pattern to copy: a `superRefine`
  on the same schema that already fails production boot for a missing
  `MEDIA_SIGNING_KEY`.
- `infra/compose/caddy/Caddyfile.production:6-12` — the shared header block:

  ```
  (common_headers) {
    header {
      Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
      X-Content-Type-Options "nosniff"
      X-Frame-Options "DENY"
      Referrer-Policy "strict-origin-when-cross-origin"
    }
  }
  ```

  Used by both production surfaces: `infra/compose/docker-compose.production.yml:89`
  and `infra/compose/docker-compose.unraid.yml:13` mount this same file.
- The built HTML contains inline `<script>` blocks (SvelteKit's kit-config and
  route data): `grep -c "<script" infra/compose/site/public/index.html` → `2`.
  A CSP with `script-src 'self'` alone would block them, so the SvelteKit half of
  this plan must let SvelteKit hash its own inline scripts.
- Cross-origin runtime calls the policy must allow: `PUBLIC_API_URL` (REST),
  `PUBLIC_SOCKET_URL` (WebSocket, `wss:`), media under `/uploads/`, embed
  images/iframes from third-party hosts gated by a user consent store
  (`apps/web/src/lib/stores/embed-consent.svelte.ts`).
- Env keys as committed in `apps/web/.env.production` (values are public by
  SvelteKit convention): `PUBLIC_API_URL`, `PUBLIC_SOCKET_URL`,
  `PUBLIC_ALTCHA_API_URL`, `PUBLIC_SKIP_CAPTCHA`.
- Existing test conventions: `services/api/test/` files use `node:test`
  (`test`/`assert`) against `buildApp()`. Model new tests on
  `services/api/test/auth-rate-limit.test.ts`.

## Commands you will need

| Purpose | Command | Expected on success |
| --- | --- | --- |
| API unit tests | `npm --workspace @penthouse/api run test` | all pass (needs Postgres: `npm run db:start`) |
| API integration | `npm --workspace @penthouse/api run test:integration` | all pass |
| Typecheck | `npm run typecheck` | exit 0 |
| Whole gate | `npm run validate` | exit 0 |
| Web build | `npm --workspace @penthouse/web run build` | exit 0, writes `apps/web/build/` |
| Caddy config syntax | `docker run --rm -v "$PWD/infra/compose/caddy:/etc/caddy:ro" caddy:2-alpine caddy validate --config /etc/caddy/Caddyfile.production` | exit 0 |

## Scope

**In scope** (the only files you should modify):

- `services/api/src/config/env.ts` (one `superRefine` issue)
- `services/api/src/app.ts` (CORS registration)
- `services/api/test/cors-policy.test.ts` (create)
- `infra/compose/caddy/Caddyfile.production` (header block)
- `apps/web/svelte.config.js` (CSP directives)

**Out of scope** (do NOT touch, even though they look related):

- `infra/caddy/Caddyfile`, `infra/compose/caddy/Caddyfile`, `infra/docker-compose.yml`
  — older duplicate surfaces; plan 007/003 deals with them. Editing all three
  invites drift; change only the one production compose files actually mount.
- `apps/web/src/lib/stores/session.svelte.ts` — moving tokens out of
  `localStorage` is a separate design decision. Not this plan.
- `apps/web/src/lib/services/api.ts` — do not add/remove `credentials: 'include'`;
  other requests rely on it.

## Git workflow

- Branch: `advisor/002-cors-csp`
- Commit style (from `git log`): `fix(security): reject wildcard CORS outside development`,
  `feat(caddy): add content security policy headers`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Fail production boot on wildcard CORS

In `services/api/src/config/env.ts`, extend the existing `.superRefine(...)`
block (do not add a second one) so that, in production, `CORS_ORIGIN` may not be
`*` and may not contain a `*` entry:

```ts
  .superRefine((value, ctx) => {
    if (value.NODE_ENV === 'production' && !value.MEDIA_SIGNING_KEY) {
      /* existing issue, unchanged */
    }
    if (
      value.NODE_ENV === 'production' &&
      (value.CORS_ORIGIN === '*' || value.CORS_ORIGIN.split(',').some((o) => o.trim() === '*'))
    ) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ['CORS_ORIGIN'],
        message: 'CORS_ORIGIN must list explicit origins in production; "*" is not allowed',
      });
    }
  });
```

**Verify**: `NODE_ENV=production CORS_ORIGIN='*' JWT_SECRET=012345678901234567890123456 MEDIA_SIGNING_KEY=0123456789012345678901234 npx tsx -e "import('./services/api/src/config/env.js').then(()=>console.log('BOOTED'))"`
→ must throw a `ZodError` mentioning `CORS_ORIGIN`, and must **not** print `BOOTED`.
(These are throwaway fake secrets for a boot test; never commit them.)

### Step 2: Make the CORS registration explicit about intent

In `services/api/src/app.ts`, keep the behaviour but make wildcard reflect
impossible-by-accident: replace the `env.CORS_ORIGIN === '*' ? true : ...`
expression with a parsed origin array (no `true` branch) — `@fastify/cors`
accepts an array of exact origins, which is what every real deployment needs:

```ts
const corsOrigin = env.CORS_ORIGIN.split(',')
  .map((origin) => origin.trim())
  .filter((origin) => origin && origin !== '*');

await fastify.register(cors, {
  origin: corsOrigin,
  credentials: true,
});
```

If a reviewer insists `*` must keep working for local tooling, STOP (see STOP
conditions) rather than adding a production exception.

**Verify**: `npm --workspace @penthouse/api run typecheck` → exit 0.

### Step 3: Regression test for both halves

Create `services/api/test/cors-policy.test.ts`, modelled on
`services/api/test/auth-rate-limit.test.ts` (same `node:test` + `buildApp()`
style). Assert:

1. A request with a disallowed `Origin` header gets no
   `access-control-allow-origin` header on a real route (use `/api/v1/health`).
2. A request whose `Origin` matches an allowed entry gets
   `access-control-allow-credentials: true`.
3. `CORS_ORIGIN='*'` in production rejects boot — implement as a comment
   pointing at the Step 1 boot check if the test file cannot change `NODE_ENV`
   after import (it cannot: env is parsed at import time). Do not restructure
   `env.ts` to make the test easier; that is out of scope.

**Verify**: `npm --workspace @penthouse/api run test` → all pass, including the new file.

### Step 4: Ship CSP report-only, then enforce (Caddy)

In `infra/compose/caddy/Caddyfile.production`, add CSP inside the existing
`(common_headers)` block. Start with the reporting-only variant so a wrong
directive cannot take the app down:

```
    Content-Security-Policy-Report-Only "default-src 'self'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https:; connect-src 'self' {$PUBLIC_SOCKET_ORIGIN}; media-src 'self' blob:; frame-src https:; worker-src 'self'"
```

Notes for the executor:

- `style-src 'unsafe-inline'` is deliberate: SvelteKit/Svelte scoped styles and
  the crop UI rely on inline styles. Tightening it is a separate task.
- `img-src`/`frame-src` include `https:` because embeds (YouTube/Twitter/etc.)
  load third-party media, gated by user consent. Do not remove `https:` from
  `img-src` — it breaks every embed users already have.
- `{$PUBLIC_SOCKET_ORIGIN}` reads an env var from the Caddy service. If the
  compose file does not pass one, add it next to `ROOT_SITE_ADDRESS` /
  `API_SITE_ADDRESS` in `infra/compose/docker-compose.production.yml`
  (`infra/compose/caddy/Caddyfile.production` is the only Caddyfile you may edit)
  and set it in `infra/compose/.env.production.example`.
- Once a deploy has run clean for a day, delete `-Report-Only` from the header
  name in a follow-up commit (record that in the plan report, don't do it blind).

**Verify**: `docker run --rm -v "$PWD/infra/compose/caddy:/etc/caddy:ro" caddy:2-alpine caddy validate --config /etc/caddy/Caddyfile.production` → exit 0.
**Verify**: `grep -n "Content-Security-Policy" infra/compose/caddy/Caddyfile.production` → at least one line.

### Step 5: Let SvelteKit hash its own inline scripts

Add a `csp` block to `apps/web/svelte.config.js` so the framework adds the
required hashes to the generated HTML (the built page currently has 2 inline
`<script>` tags; without this, enforcing `script-src 'self'` blanks the app).

```js
    csp: {
      directives: {
        'script-src': ['self'],
        'frame-ancestors': ['none'],
      },
    },
```

Then rebuild and confirm SvelteKit emitted a hash or nonce for its inline data:

**Verify**: `npm --workspace @penthouse/web run build` → exit 0.
**Verify**: `grep -o "sha256-[A-Za-z0-9+/=]*" apps/web/build/index.html | head -3` → at least one hash, OR `grep -c "nonce=" apps/web/build/index.html` → ≥ 1.
If neither appears, STOP: adapter-static + prerender may not be applying CSP, and enforcing CSP would break the app. Report instead of shipping a broken policy.

## Test plan

- New: `services/api/test/cors-policy.test.ts` (disallowed origin gets no ACAO
  header; allowed origin gets credentials header). Pattern:
  `services/api/test/auth-rate-limit.test.ts`.
- Manual/browser proof (Qwen3.8, after 009 or with the app built locally): open
  `http://localhost:4173` preview with the CSP enforced, log in, send a message,
  open an embed, upload an image; confirm zero CSP violations in the browser
  console. Attach the console screenshot to the plan report.

## Done criteria

- [ ] Production boot with `CORS_ORIGIN='*'` fails with a `ZodError` naming `CORS_ORIGIN`
- [ ] `grep -n "credentials: true" services/api/src/app.ts` still shows one occurrence, and no `? true :` wildcard branch remains
- [ ] `npm --workspace @penthouse/api run test` passes including `cors-policy.test.ts`
- [ ] `caddy validate` exits 0 on `infra/compose/caddy/Caddyfile.production`
- [ ] Built `apps/web/build/index.html` carries a CSP hash/nonce for its inline scripts
- [ ] `npm run validate` exits 0
- [ ] `plans/README.md` status row for 002 → DONE (plus a note whether the policy is still report-only)

## STOP conditions

Stop and report if:

- Any client genuinely needs `CORS_ORIGIN='*'`; that is an architecture decision for the primary agent.
- Step 5 produces no hash/nonce (adapter-static prerender does not apply CSP).
- Enforcing CSP breaks login, socket connect, media upload, or embed rendering in browser testing.
- `services/api/src/app.ts` no longer matches the excerpt in "Current state".

## Maintenance notes

- New third-party embeds may need `frame-src`/`img-src` additions — keep the
  directive list in one place (the `(common_headers)` block) and never add
  per-route `add_header` copies.
- The CSP is the mitigation for keeping tokens in `localStorage`. If tokens ever
  move to `HttpOnly` cookies, revisit `connect-src`/`credentials` together.
- Deferred on purpose: removing `'unsafe-inline'` from `style-src`; a
  `Report-To`/`report-uri` endpoint (needs a collector, out of scope); migrating
  session storage out of `localStorage`.

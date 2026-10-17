---
tags: []
created: 2026-10-12
publish: false
project: Penthouse
---
# Plan 003: Build the frontend in the pipeline, and stop shipping a hand-copied bundle out of git

> **Executor instructions**: Follow this plan step by step. Run every verification
> command and confirm the expected result before moving to the next step. If
> anything in "STOP conditions" happens, stop and report — do not improvise.
> When done, update this plan's status row in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 2bea709..HEAD -- .github/workflows/ci.yml infra/compose/docker-compose.production.yml infra/compose/docker-compose.unraid.yml apps/web/svelte.config.js`
> If non-empty, re-read the "Current state" excerpts against the live files; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1 (highest-leverage plan in this set)
- **Effort**: M (a day, including CI debugging)
- **Risk**: MED (touches how the app gets deployed; step 6 must not run before 4–5 pass)
- **Depends on**: none (but do it after 001 so CI installs patched deps)
- **Category**: dx / release integrity
- **Planned at**: commit `2bea709`, 2026-09-02

## Why this matters

The thing users actually see in production is a folder of build output that was
compiled on a laptop, pasted into the repo, and committed. Caddy serves
`infra/compose/site/public` as `/srv/site`
(`infra/compose/docker-compose.production.yml:90`,
`infra/compose/docker-compose.unraid.yml:14`). The project's own notes say the
SvelteKit build "needs to be copied to `site/public/`"
(`docs/CLAUDE-CONTINUATION.md:95-102`) and records doing exactly that by hand
(`docs/obsidian/01 - Rebuild Timeline.md:206`: built locally because the server
had no npm, then copied). 92 build files are tracked in git
(`git ls-files infra/compose/site/public | wc -l` → 92), and the same notes flag
the committed `index.html` as still being the old APK-era landing page.

Consequences today: CI never compiles the frontend, so a frontend that does not
build can be merged and deployed; there is no way to prove the deployed UI
matches any commit; and reverting a deploy means hoping somebody pasted the
right folder. Fix = build the artifact in CI, build it on the server in a
container if needed, and delete the committed copy.

## Current state

- `apps/web` is SvelteKit with `@sveltejs/adapter-static` and
  `fallback: 'index.html'` (`apps/web/svelte.config.js:1-8`). `npm --workspace
  @penthouse/web run build` = `vite build` and writes **`apps/web/build/`**
  (the adapter default; not currently gitignored because nothing generates it
  in the pipeline).
- CI is `.github/workflows/ci.yml` (71 lines): one `validate` job (Postgres 16
  service, `npm ci`, apt ffmpeg, `cp apps/web/.env.example apps/web/.env`,
  `npm run validate`, `npm run scenario:test`) and one `integration` job
  (`npm --workspace services/api run test:integration`). No `npm run build` for
  either workspace, no Docker image build, no Playwright, no coverage.
- Local web tests: `npm --workspace @penthouse/web run test` → `vitest run`.
  E2E: `npm --workspace @penthouse/web run test:e2e` → `playwright test`,
  specs in `apps/web/e2e/*.spec.ts`, config `apps/web/playwright.config.ts`
  (read it: it may need `webServer` pointed at a preview server).
- `services/api/Dockerfile` already builds the API from source in CI-style
  layers (node:22-alpine, `npm ci`, `npm --workspace @penthouse/api run build`).
  The API is fine; only the frontend bypasses the pipeline.
- Production web root mounts (both must change together):
  - `infra/compose/docker-compose.production.yml:90` → `- ./site/public:/srv/site:ro`
  - `infra/compose/docker-compose.unraid.yml:14` → `- ./site/public:/srv/site:ro`
- Deployment reality (from `docs/obsidian/21 - Unraid Production Operations.md`):
  the Unraid box runs this repo from `/mnt/cache/appdata/penthouse/app`, and the
  static root is `/mnt/cache/appdata/penthouse/app/infra/compose/site/public`.
  The host has Docker but no guaranteed `npm`.
- `.gitignore` already ignores `dist/`, `build/`, `.svelte-kit/`
  (`.gitignore:1-3`) — note `build/` matches `apps/web/build/`, so once the
  tracked copies are removed, the generated folder will be ignored automatically.

## Commands you will need

| Purpose | Command | Expected on success |
| --- | --- | --- |
| Web build (local proof) | `npm --workspace @penthouse/web run build` | exit 0; `apps/web/build/index.html` exists |
| API build (local proof) | `npm --workspace @penthouse/api run build` | exit 0; `services/api/dist/src/index.js` exists |
| Whole gate | `npm run validate` | exit 0 |
| Web unit tests | `npm --workspace @penthouse/web run test` | all pass |
| E2E (local, manual) | `npm --workspace @penthouse/web run test:e2e` | suite runs (see step 3 on whether it can run in CI) |
| Containerised web build | `docker run --rm -v "$PWD":/app -w /app node:22-alpine sh -c "npm ci && npm --workspace @penthouse/web run build"` | exit 0; `apps/web/build/` populated |
| Caddy config syntax | `docker run --rm -v "$PWD/infra/compose/caddy:/etc/caddy:ro" caddy:2-alpine caddy validate --config /etc/caddy/Caddyfile.production` | exit 0 |

## Scope

**In scope** (the only files you should modify):

- `.github/workflows/ci.yml`
- `infra/compose/docker-compose.production.yml` (caddy volume + an optional build step)
- `infra/compose/docker-compose.unraid.yml` (caddy volume only)
- `apps/web/playwright.config.ts` (only if needed to run headless in CI)
- `package.json` (root) — add a `build` script so both workspaces build with one command
- `.gitignore` (only if step 6 needs an explicit `apps/web/build/` entry)
- `infra/compose/site/public/**` — **deleted**, via `git rm -r --cached` + removal

**Out of scope** (do NOT touch, even though they look related):

- `infra/docker-compose.yml`, `infra/compose/docker-compose.yml`,
  `infra/compose/docker-compose.unraid.preview.yml`, `infra/caddy/Caddyfile`,
  `infra/compose/caddy/Caddyfile` — the duplicate surfaces. Do not "fix" them
  here; plan 007 decides what survives. Changing the extra Caddyfiles would make
  the drift worse.
- `services/api/Dockerfile` — already correct.
- `apps/web/src/**` — no application code changes. If the build fails because of
  app code, STOP.

## Git workflow

- Branch: `advisor/003-build-pipeline`
- Commit style: `ci: build web and api, add e2e job`, `chore(infra): serve built pwa from apps/web/build`, `chore: stop tracking committed web bundle`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

Do steps 1–5 first. Step 6 (deleting the committed bundle) happens only once
steps 4–5 prove a build exists, so there is never a moment where the deploy has
no frontend.

### Step 1: One root build command

Add to the root `package.json` `scripts` (keep existing entries):

```json
    "build": "npm --workspace @penthouse/contracts run build && npm --workspace @penthouse/api run build && npm --workspace @penthouse/web run build",
```

**Verify**: `npm run build` → exit 0, and both exist:
`services/api/dist/src/index.js`, `apps/web/build/index.html`.

### Step 2: CI compiles both workspaces

In `.github/workflows/ci.yml`, add `- run: npm run build` after `npm ci` in the
existing `validate` job (after the ffmpeg/apt step, before `npm run validate` is
fine, but keep `cp apps/web/.env.example apps/web/.env` before the build so the
bundle picks up the same env the deploy expects).

**Verify**: on the pushed branch, Actions run for this job shows a step
`npm run build` with exit 0. (If the executor cannot see Actions, run the build
locally and report both commands.)

### Step 3: CI runs the frontend build's tests, unit first, E2E where possible

- In the `validate` job, ensure web unit tests already run via `npm run validate`.
- Add a third job `e2e` that runs `npm --workspace @penthouse/web run test:e2e`
  with `npx playwright install --with-deps chromium`, needs: `validate`, and a
  Postgres 16 service exactly like the `validate` job's, and the API running.

If the Playwright config expects a live API + logged-in browser fixtures that
cannot be provisioned in CI without new code, do **not** hack the specs. Instead:
keep the `e2e` job but limit it to the specs that run against a built static
bundle, and record in the plan report exactly which specs were excluded and why.
Reading `apps/web/playwright.config.ts` and two spec files is required before
deciding.

**Verify**: `npm --workspace @penthouse/web run test:e2e -- --list` → prints a
spec list; the number you enabled in CI equals that number.

### Step 4: Build the frontend on the server, in a container

Create `infra/compose/scripts/build-web.sh` (new file, `chmod +x`) containing:

```sh
#!/bin/sh
set -eu
# Build the SvelteKit PWA in a container so the Unraid host needs no npm.
cd "$(dirname "$0")/../.."
docker run --rm -v "$PWD":/app -w /app node:22-alpine \
  sh -c "npm ci && npm --workspace @penthouse/web run build"
echo "web build ready at apps/web/build"
```

**Verify**: `./infra/compose/scripts/build-web.sh` → exit 0 and
`ls apps/web/build/index.html` exists.

### Step 5: Point Caddy at the built folder

Change the caddy volume in **both** files so the web root is the build output:

```yaml
      - ../apps/web/build:/srv/site:ro
```

(`infra/compose/docker-compose.production.yml` and
`infra/compose/docker-compose.unraid.yml`, replacing `./site/public:/srv/site:ro`.)

**Verify**: `grep -rn "srv/site" infra/compose/*.yml` → only `../apps/web/build:/srv/site:ro`
lines plus the Caddy internal `/srv/site` references in the Caddyfile.
**Verify**: `docker compose -f infra/compose/docker-compose.production.yml --env-file infra/compose/.env.production.example config --quiet` → exit 0.

### Step 6: Delete the committed bundle from git

```sh
git rm -r --cached infra/compose/site/public
git rm -r infra/compose/site/public
```

Do not keep a copy anywhere else in the repo. The APK archive Aim wants to keep
belongs in GitHub Releases (see plan 006), not in the web root.

**Verify**: `git ls-files infra/compose/site | wc -l` → `0`.
**Verify**: `npm run build && ls apps/web/build/index.html` → exists, and
`git status --porcelain apps/web/build` → empty (ignored by `build/` in `.gitignore`).

### Step 7: Write the deploy order down

Append to `docs/DEPLOYMENT.md` (top of the deploy section, no rewrite) the
exact sequence for the Unraid box:

```sh
git pull --ff-only
./infra/compose/scripts/build-web.sh
docker compose -f infra/compose/docker-compose.production.yml -f infra/compose/docker-compose.unraid.yml \
  --env-file infra/compose/.env.production up -d --build
```

**Verify**: `grep -n "build-web.sh" docs/DEPLOYMENT.md` → ≥1 line.

## Test plan

- No new unit tests; this plan's tests are pipeline commands.
- The regression that must never come back: "the committed frontend differs from
  source". Its guard is `git ls-files infra/compose/site | wc -l` → `0`, plus
  `npm run build` inside CI.
- After deploy, prove the served bundle matches the commit:
  `curl -s https://<host>/_app/version.json` (the Caddyfile already routes
  `/_app/version.json` with `no-cache`) and compare with the commit sha you
  deployed. If `version.json` does not exist in the build output, record that as
  a follow-up for plan 008 rather than inventing an endpoint here.

## Done criteria

- [ ] `npm run build` (root) exits 0 and produces both `services/api/dist/src/index.js` and `apps/web/build/index.html`
- [ ] CI runs `npm run build`; the run is green
- [ ] CI has an `e2e` job; the enabled spec count equals `playwright test --list` output minus whatever the report explicitly excludes
- [ ] `git ls-files infra/compose/site | wc -l` → 0
- [ ] Both compose files mount `../apps/web/build:/srv/site:ro`; `docker compose config --quiet` exits 0
- [ ] `docs/DEPLOYMENT.md` contains the build-then-up sequence
- [ ] `plans/README.md` status row for 003 → DONE

## STOP conditions

Stop and report if:

- `npm --workspace @penthouse/web run build` fails on application code (do not fix app code here).
- The Unraid box currently serves something from `infra/compose/site/public` that is **not** generated by `npm --workspace @penthouse/web run build` (a hand-made landing page, downloads, icons added by hand). Check with `ls infra/compose/site/public` and diff the file list against `apps/web/build` after building. If they differ, STOP: those files need a home before the folder goes away.
- Playwright needs new app-side test hooks (auth fixtures, seeding) — that is a separate brief for the primary agent.
- `docs/DEPLOYMENT.md` describes an Android/APK publish flow entangled with the web deploy step (it does partially — `docs/DEPLOYMENT.md:158-228`); only add the web lines, leave the Android text for plan 006.

## Maintenance notes

- After this lands, a frontend deploy is: pull → build → `up --build`. Anything
  else (copy-pasting folders) is a regression of this plan; call it out in review.
- The `.unraid.preview.yml` compose file still points at the old (now missing)
  web root. It is a duplicate surface that plan 007 is meant to delete; if it is
  actually used, fix its volume in the same commit and say so in the report.
- Watch for CI cache: `npm ci` with `cache: npm` is already set; adding the web
  build makes CI slower — acceptable. A follow-up could cache `apps/web/node_modules`.
- Deferred on purpose: publishing signed artifacts between jobs (`actions/upload-artifact`),
  container-registry images instead of building on the server, and zero-downtime
  deploys. Do those when the server-side build proves flaky.

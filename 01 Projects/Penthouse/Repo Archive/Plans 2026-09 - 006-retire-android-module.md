---
tags: []
created: 2026-10-12
publish: false
project: Penthouse
---
# Plan 006: Delete the Android/Gradle build surface and point the archived APK at Releases

> **Executor instructions**: Follow this plan step by step. Run every verification
> command and confirm the expected result before moving to the next step. If
> anything in "STOP conditions" happens, stop and report — do not improvise.
> When done, update this plan's status row in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 2bea709..HEAD -- app settings.gradle.kts build.gradle.kts gradle gradle.properties gradlew gradlew.bat local.properties scripts services/api/src/routes/distribution.ts`
> If non-empty, re-read the "Current state" excerpts; on a mismatch, STOP.

## Status

- **Priority**: P2
- **Effort**: S/M (an hour to delete, half a day if docs rewrite is thorough)
- **Risk**: LOW for the deletion, MED for the docs rewrite (a deploy doc that lies is worse than none)
- **Depends on**: plans/003-build-pipeline-and-committed-bundle.md (so `docs/DEPLOYMENT.md` gets rewritten once)
- **Category**: tech-debt
- **Planned at**: commit `2bea709`, 2026-09-02
- **Aim's decision, 2026-09-02**: the Android APK is *finito*. The old APKs stay
  only as an archive of what the vision looked like. No Android build surface in
  this repo.

## Why this matters

The repo carries a complete Android/Gradle project next to the Node monorepo:
`app/` (Gradle module with `src/`, `build.gradle.kts`, `proguard-rules.pro`),
`settings.gradle.kts` (whose `rootProject.name` is still **"The Penthouse
Optimized"**), `build.gradle.kts`, `gradle/`, `gradle.properties`, `gradlew`,
`gradlew.bat`, `local.properties`, plus `scripts/build-android-debug.sh` and
`scripts/prepare-android-testing.sh`. Nothing in CI, `package.json`, or the
Docker build references them; `docs/DEPLOYMENT.md:158-228` nevertheless still
tells a human to build and sign an APK for a release. New contributors (and
every agent that reads these docs) spend effort on a platform that is not
shipped, and the deploy doc now describes two products.

## Current state

- Tracked Android surface (confirm each with `git ls-files <path> | head -1` before deleting):
  `app/`, `settings.gradle.kts`, `build.gradle.kts`, `gradle/`,
  `gradle.properties`, `gradlew`, `gradlew.bat`, `local.properties`,
  `scripts/build-android-debug.sh`, `scripts/prepare-android-testing.sh`.
- The **only** live product surface for the APK is an optional download link:
  - `services/api/src/routes/distribution.ts:34` —
    `fastify.get('/api/v1/app-distribution', ...)`, returning a
    `legacyAndroid` object with `fileName` from `LEGACY_APK_DOWNLOAD_PATH`
    (`services/api/src/config/env.ts:18-19`, default
    `/downloads/legacy/the-penthouse.apk`, `LEGACY_APK_STATUS` default
    `'unavailable'`).
  - `apps/web/src/routes/welcome/+page.svelte:15-29` fetches that endpoint and
    only renders the block when told to (`showApk`), with the UI label "Legacy
    Android APK" (`:174`).
  - Caddy serves the file from a host directory
    (`infra/compose/docker-compose.production.yml` mounts
    `${PUBLIC_DOWNLOADS_PATH}:/srv/downloads:ro`;
    `infra/compose/caddy/Caddyfile.production` has the `handle_path /downloads/*`
    block plus two redirects for old APK URLs).
- Tests that cover the download endpoint and must keep passing:
  `services/api/test/distribution.test.ts`,
  `services/api/test/integration-distribution.test.ts`.
- Docs mentioning Android/APK that need rewriting or archiving:
  `docs/DEPLOYMENT.md` (prerequisites line 4-ish, and `:158-228`),
  `docs/START_HERE.md` (describes `apps/mobile` as "Vue + Capacitor" — that path
  does not exist; the real app is `apps/web`), `docs/DEVELOPMENT.md`
  (prerequisite: "Android Studio or emulator ... recommended for alpha").
  `docs/archive/handoffs/2026-05-20-codex-v4-cutover.md:85` argues to "KEEP even
  if Android deferred" — that advice is superseded by Aim's decision above; leave
  the archived file as history, do not edit it.
- Note: `local.properties` normally contains a machine-specific SDK path and
  should not be in git at all. Check it before deleting and report if it held
  anything other than a local SDK path (do not paste its contents anywhere).

## Commands you will need

| Purpose | Command | Expected on success |
| --- | --- | --- |
| Confirm tracked surface | `git ls-files app gradle settings.gradle.kts build.gradle.kts gradle.properties gradlew gradlew.bat local.properties \| head -20` | lists files (they are tracked today) |
| API tests (distribution) | `npm --workspace @penthouse/api run test` | all pass, incl. `distribution.test.ts` |
| API integration | `npm --workspace @penthouse/api run test:integration` | all pass, incl. `integration-distribution.test.ts` |
| Whole gate | `npm run validate` | exit 0 |
| Nothing Gradle left | `git ls-files \| grep -icE "gradle\|\.apk$\|proguard"` | `0` |

## Scope

**In scope** (the only files you should modify/delete):

- Delete: `app/`, `settings.gradle.kts`, `build.gradle.kts`, `gradle/`,
  `gradle.properties`, `gradlew`, `gradlew.bat`, `local.properties`,
  `scripts/build-android-debug.sh`, `scripts/prepare-android-testing.sh`
- `docs/DEPLOYMENT.md` (remove/replace the Android build+signing sections)
- `docs/START_HERE.md` (fix the phantom `apps/mobile` / Vue+Capacitor description → `apps/web`, SvelteKit PWA)
- `docs/DEVELOPMENT.md` (drop the Android Studio prerequisite)
- `.gitignore` only if it carries Android-specific entries worth keeping (leave them, they are harmless)

**Out of scope** (do NOT touch, even though they look related):

- `services/api/src/routes/distribution.ts`, its two tests, `LEGACY_APK_*` env
  keys, the Caddy `/downloads/*` block, and
  `apps/web/src/routes/welcome/+page.svelte`. The archived APK download is a
  product decision Aim has not asked to remove, and it costs nothing to keep. If
  the reviewer decides to retire it, that is a separate plan with its own brief.
- Any `infra/compose/**` file.
- `docs/archive/**` — history stays as written.

## Git workflow

- Branch: `advisor/006-retire-android`
- Commit style: `chore(android): remove legacy gradle build surface`, `docs: drop Android build steps from deployment guide`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Archive the APKs before deleting anything

Ask Aim (or check `https://github.com/AIMDaAlien/The-Penthouse/releases`) that the
last APKs he wants as an archive are uploaded to **GitHub Releases** (or live at
`/downloads/legacy/the-penthouse.apk` on the server). Do not create the release
yourself. Do not proceed if the only copy of the APK is inside `app/` build
output that is about to be deleted.

**Verify**: Aim confirms in writing (chat message is enough, quote it in the report), OR
`git ls-files '*.apk' | wc -l` → `0` (i.e. no APK was ever tracked, so nothing to archive from git).

### Step 2: Delete the build surface

```sh
git rm -r app gradle
git rm settings.gradle.kts build.gradle.kts gradle.properties gradlew gradlew.bat local.properties
git rm scripts/build-android-debug.sh scripts/prepare-android-testing.sh
```

**Verify**: `git ls-files | grep -icE "gradle|\.apk$|proguard"` → `0`.
**Verify**: `npm run validate` → exit 0 (nothing referenced these files).

### Step 3: Rewrite the deploy doc so it describes one product

In `docs/DEPLOYMENT.md`: delete the Android build/signing sections
(`:158-228` region — anything telling the reader to install Android Studio,
configure signing, or produce a release APK). Replace with a short paragraph:

> The Android APK is retired. Old builds are kept as an archive under GitHub
> Releases; nothing in this repo builds them. The PWA
> (`apps/web`, SvelteKit + `adapter-static`) is the only client. The optional
> "Legacy Android APK" link on the welcome page is served from
> `LEGACY_APK_DOWNLOAD_PATH` and stays off unless an operator opts in.

Keep every non-Android deploy step exactly as it is, and keep plan 003's
build-then-up sequence intact.

**Verify**: `grep -icE "android studio|gradlew|signing config" docs/DEPLOYMENT.md` → `0`.

### Step 4: Fix the two other docs that describe a client which does not exist

- `docs/START_HERE.md`: the first section claims `apps/mobile` is a "Vue +
  Capacitor" app. Replace the three-part list with the real layout
  (`apps/web` = SvelteKit PWA, `services/api` = Fastify API,
  `packages/contracts` = shared types).
- `docs/DEVELOPMENT.md`: remove "Android Studio or emulator (for mobile testing;
  optional but recommended for alpha)" from prerequisites.

**Verify**: `grep -rn "apps/mobile" docs/START_HERE.md docs/DEVELOPMENT.md README.md` → no matches.

### Step 5: Prove the archived download still behaves

**Verify**: `npm --workspace @penthouse/api run test:integration -- test/integration-distribution.test.ts`-style run, or the full integration suite →
`distribution` tests pass unchanged (they must, since nothing in the API changed).

## Test plan

No new tests. This plan is proven by deletion plus:
- `services/api/test/distribution.test.ts` and
  `services/api/test/integration-distribution.test.ts` still pass (proves the
  archived-download path is untouched).
- `npm run validate` exits 0 (proves nothing imported the deleted surface).

## Done criteria

- [ ] `git ls-files | grep -icE "gradle|proguard"` → `0`
- [ ] `app/`, `gradle/`, `gradlew*`, `settings.gradle.kts`, `build.gradle.kts`, `gradle.properties`, `local.properties` absent from the working tree and index
- [ ] `grep -rn "apps/mobile" docs README.md` → no matches
- [ ] `grep -icE "android studio|gradlew|signing config" docs/DEPLOYMENT.md` → `0`
- [ ] `distribution` tests still pass; `npm run validate` exits 0
- [ ] `plans/README.md` status row for 006 → DONE

## STOP conditions

Stop and report if:

- Step 1 shows the APK exists only inside `app/` (nothing uploaded anywhere) — Aim's
  archive would be destroyed.
- Anything in CI, `package.json`, or a Dockerfile references Gradle today (it
  should not; check `grep -rn gradle .github package.json services/api/Dockerfile`).
- `local.properties` contains anything that is not an SDK path (e.g. a keystore
  password or key alias) — that is a secret-in-git report for the primary agent,
  rotation and all.

## Maintenance notes

- If Aim ever revives native (Capacitor around the PWA, or a real rebuild), it
  starts from a fresh repo/module plus GitHub Actions — not from resurrecting
  this Gradle project.
- Reviewer: this diff should contain **zero** changes under `services/api/src`
  and `apps/web/src`. Any such change means the executor "helped" — reject.
- Deferred: retiring `/api/v1/app-distribution` and the welcome-page APK block.
  Not asked for; needs Aim's call on whether the link stays visible.

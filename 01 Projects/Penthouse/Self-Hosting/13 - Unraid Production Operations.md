---
tags: [penthouse, production, unraid, deployment, networking, operations]
created: 2026-06-15
publish: false
project: Penthouse
---

# Unraid Production Operations

## Current live topology

As of 2026-06:

- host: `<lan-ip-5>`
- app stack: `/mnt/cache/appdata/penthouse/app/infra/compose`
- static Caddy web root: `/mnt/cache/appdata/penthouse/app/infra/compose/site/public`
- public domains:
  - `penthouse.blog`
  - `api.penthouse.blog`
- Caddy host ports:
  - HTTP: `9080`
  - HTTPS: `9443`
- router forwarding:
  - public TCP `80 -> <lan-ip-5>:9080`
  - public TCP `443 -> <lan-ip-5>:9443`

Do not forward public traffic to the Unraid administration ports.

## Router reset recovery - 2026-06-06/07

The public site became unreachable after the TP-Link Archer AX55 router was reset.

The app containers were healthy and the LAN listeners worked. Two independent network failures were found:

1. the router reset erased the WAN forwarding rules
2. Unraid still used dead DNS resolver `<lan-ip-6>`

Recovery:

- restored the two TCP forwarding rules above
- backed up `/boot/config/network.cfg`
- set persistent Unraid DNS to:
  - `1.1.1.1`
  - `8.8.8.8`
- updated host resolver state
- recreated the API and Caddy containers so Docker inherited working DNS

## Recovery proof

After repair:

- `https://penthouse.blog/` returned HTTP 200
- `https://api.penthouse.blog/api/v1/health` returned HTTP 200
- HTTP redirected to HTTPS
- Socket.IO polling connected
- PWA environment, manifest, service worker, offline page, and icons loaded
- auth and CAPTCHA endpoints worked
- external regional probes reached public port 443

Operational rule:

- when LAN health is good but WAN access fails after router work, check forwarding and host/container DNS before investigating application code

## Static frontend deployment

The production web UI is a built SvelteKit static bundle served by Caddy.

Shipping a web change requires:

1. build `apps/web`
2. verify `apps/web/build/_app/env.js`
3. sync the build into the Unraid static web root
4. verify the real public pages in a normal browser context

Expected public environment:

- `PUBLIC_API_URL=https://api.penthouse.blog`
- `PUBLIC_SOCKET_URL=https://api.penthouse.blog`
- `PUBLIC_SKIP_CAPTCHA=false`
- `PUBLIC_ALTCHA_API_URL=https://api.penthouse.blog/api/v1/auth/challenge`

## Redeploy - 2026-06-15

Release head `24c1d41` was deployed from branch `audit/backend-trim-performance`.

The release included:

- Nocturne UI and chat refresh commit `f6f6762`
- migration `031_presence_note_expires_at.sql`
- a rebuilt production web bundle
- refreshed API and contracts source

The deployment preserved the live Unraid Compose, Caddy, environment, uploads, downloads, and data paths. Only the API container was rebuilt and recreated; Caddy and PostgreSQL remained healthy.

Rollback artifacts use timestamp `20260615T033210Z`:

- API image: `compose-api:predeploy-20260615T033210Z`
- static bundle: `/mnt/cache/appdata/penthouse/backups/releases/predeploy-20260615T033210Z-public.tgz`
- deployed source paths: `/mnt/cache/appdata/penthouse/backups/releases/predeploy-20260615T033210Z-source.tgz`

Production proof:

- `https://penthouse.blog/` returned HTTP 200 with valid TLS
- deployed revision file reported `24c1d41`
- API health returned `{"status":"ok","db":"reachable"}`
- registration mode remained `open`
- ALTCHA challenge generation passed
- Socket.IO polling returned a valid handshake
- migration `031_presence_note_expires_at.sql` and its column were present
- mobile Chromium rendered `/welcome` and `/auth` without console, page, or request failures
- the public auth page did not render the authenticated notification reminder

## Historical TrueNAS deployment

The 2026-04-15 TrueNAS deployment under `/mnt/Backup/penthouse-rebuild` is historical.

It included:

- tested PWA and API deployment
- nightly PostgreSQL dump/restore proof
- stack watchdog tooling
- legacy APK redirects

Do not reuse the old TrueNAS paths as current operator instructions without explicit verification.

## Media and sticker release - 2026-06-27

Release checkout `ab37681` is live. The public bundle carries source revision marker `bc15e2e`.

Shipped:

- multi-image and multi-video composer
- signed private attachment hydration
- sticker replace/delete and chat label behavior
- per-user upload limits
- Unraid naming across Compose, scripts, and operator docs

The first real production upload exposed three deployment-only faults:

- live `UPLOAD_DIR` still pointed at `/app/services/api/uploads`
- `/mnt/cache/appdata/penthouse/uploads` was not writable by container UID 1000
- restored `media_uploads.file_path` remained `NOT NULL` although current code uses `storage_key`

Corrections:

- live env now uses `UPLOAD_DIR=/app/uploads`
- upload storage is owned by UID/GID `1000:1000`
- migration `033_drop_legacy_media_file_path.sql` removed the obsolete column
- API startup checks that `UPLOAD_DIR` is writable

Proof:

- API, Caddy, and PostgreSQL are healthy
- public health, root site, auth config, app distribution, and Socket.IO polling passed
- mobile Chromium loaded `/welcome` and `/auth` without console or page errors
- real chat image, avatar, banner, and sticker uploads returned HTTP 200
- the temporary smoke user, database rows, and files were removed

Rollback:

- predeploy API image: `compose-api:predeploy-20260627T044235Z`
- prehotfix API image: `compose-api:prehotfix-20260627T044834Z`
- static bundle: `/mnt/user/appdata/penthouse/backups/releases/predeploy-20260627T044235Z-public.tgz`
- env backup: `<env-path>`

## Profile media and changelog release - 2026-07-03

Release checkout `b9a9053` is live. The public bundle carries source revision marker `3d6ee64`.

Shipped:

- avatar and banner cropping with explicit save actions
- image compression and composer paste support
- live profile-style updates
- public `/welcome/updates` and signed-in `/updates` changelog routes
- removal of the dormant frontend voice-room UI

Deployment was frontend-only. The API, Caddy, and PostgreSQL containers were not rebuilt or restarted.

Proof:

- full validation passed: web `13/13`, API `214/214`, contracts `36/36`
- authenticated avatar, banner, chat-image, and profile-style smoke passed locally against the backend
- public root, `/welcome`, `/auth`, and `/welcome/updates` returned HTTP 200
- desktop and mobile Chromium rendered the public routes without console, page, request, or horizontal-overflow failures
- API health reported `db: reachable`; registration remained open; ALTCHA and Socket.IO polling passed

Rollback:

- static bundle: `/mnt/cache/appdata/penthouse/backups/releases/predeploy-20260704T001600Z-public.tgz`
- prior public revision: `/mnt/cache/appdata/penthouse/backups/releases/predeploy-20260704T001600Z-revision.txt`

## Remaining operational proof

- complete manual Add-to-Home-Screen proof on a real mobile browser
- remove or self-host the third-party Erode font request

## Group ownership invariant - 2026-07-04

- Fresh pre-change dump: `/mnt/user/penthouse-backups/postgres/penthouse-20260704T143748Z.sql.gz`
- Production PostgreSQL mount confirmed as `/mnt/cache/appdata/penthouse/postgres`
- Migration `036_group_owner_invariant.sql` is live
- User-created groups are audited for exactly one owner before the migration proceeds
- PostgreSQL now rejects a second owner through partial unique index `unique_chat_owner`
- System group `General` remains ownerless by design because it has no human creator
- `<admin-user>` is the designated site-admin username, but the account does not exist yet and promotion remains intentionally deferred

## Close friends hardening release - 2026-07-04

- deployed checkout `a008e93`; public source marker `7f9887b`
- rollback image `penthouse-api:rollback-20260705T023508Z`
- rollback static bundle `/mnt/cache/appdata/penthouse/backups/releases/predeploy-20260705T023508Z-public.tgz`
- predeploy backup `/mnt/user/penthouse-backups/postgres/penthouse-20260705T022107Z.sql.gz`
- isolated restore matched production at `13` users, `6` chats, `40` messages, and `45` migrations
- the new image then applied migrations `034` and `035` to a second isolated restore before the live restart
- production finished at `47` checksummed migrations with no invalid group owners
- public health, PWA assets, ALTCHA, Socket.IO polling, auth, DM send/read, and mobile Chromium welcome/auth proof passed
- the public VAPID key now matches the API; browser shadow sync is enabled
- FCM remains disabled until a Firebase service account is installed

## Close friends update ticket - 2026-07-05

- web bundle commit `9e29661`; public source marker `ef8f450`
- frontend-only deployment; API, Caddy, and PostgreSQL were not restarted
- July 4 ticket rendered cleanly in desktop and mobile Chromium with no console, request, or overflow failures
- rollback bundle `/mnt/cache/appdata/penthouse/backups/releases/predeploy-20260705T124646Z-public.tgz`

## Messaging UX release — 2026-09-07 (v4.3.0-alpha.3)

- deployed source revision: `5f9b615b4f69e0f1dec86df7cbaec674a7f92057`
- scope: persistent account-and-chat text drafts, correct channel context,
  clearer group/settings controls, improved return/copy paths, and a durable
  dismissal for the browser notification reminder
- no database migration or schema change; the API image was rebuilt only to
  align its reported release version with the frontend
- local Chromium proof passed all 11 focused messaging cases across ordinary
  member, manager, and owner roles at desktop and mobile sizes
- production proof: root, API health, service worker, and public changelog all
  loaded successfully; the public changelog had no browser page errors or
  failed requests
- rollback API image: `penthouse-api:rollback-20260907T235305Z`
- rollback static bundle: `/mnt/cache/appdata/penthouse/backups/releases/predeploy-20260907T235305Z-public.tgz`
- predeploy source snapshot: `/mnt/cache/appdata/penthouse/backups/releases/predeploy-20260907T235305Z-source.tgz`

## v4.2 alpha hardening release - 2026-07-14

- release `v4.2.0-alpha.1` deployed at `a3584bb`; production hotfix `7f963c6` is live
- API diagnostics report version `4.2.0-alpha.1`, build `7f963c6`, a reachable database, and current backup status `ok`
- production Caddy now sends `X-Frame-Options: DENY`; API startup no longer logs the bootstrap invite code
- `<admin-user>` was explicitly promoted to site admin and is the only admin account
- two temporary users proved normal ALTCHA registration, isolated admin/member login, admin dashboard access, member denial, and clean browser console/network behavior; both users and sessions were deleted afterward
- rollback timestamp: `20260714T210221Z`; fresh database dump: `/mnt/user/penthouse-backups/postgres/penthouse-20260714T210222Z.sql.gz`

## Fara API runtime packaging fix - 2026-09-03

- API source commit `7536708` from `worker/fara-pipeline` was deployed to the Unraid Compose API service.
- The API image is `sha256:e3d6154b2518292c3e2430400bf5edd193ba16122d80a88768c7e6e8a53ea3e8`.
- The rollback image is retained as `penthouse-api:rollback-before-fara-7536708`.
- Scope was API-only. The pre-existing host checkout and its dirty deployment overlay, Caddy, generated frontend, PostgreSQL, env, and data paths were preserved.
- The runtime image now carries `/app/services/api/node_modules`, fixing the `sharp` cold-start resolution failure.
- Post-deploy API health was HTTP 200 with `db: reachable`; `compose-api-1`, Caddy, and PostgreSQL were healthy.
- Public root returned HTTP 200, and public API health plus app distribution passed after the update.

## September changelog and Plan 008 dashboard - 2026-09-04

- `worker/fara-pipeline` commits `119eb77` and `8336c06` are pushed; production reports revision/build `8336c06a5bb73c803f0a254aa5f74ec7993c2d86`.
- API image `sha256:55839f82581c02263a6e879e428ce8ef5b242cadb2f867211eba382fe72b1090` and the matching static PWA are live. API, Caddy, PostgreSQL, public health, PWA assets, Socket.IO, and redirects passed.
- Live desktop and mobile Chromium proved the September 3 public update route without overflow or browser/network errors. Authenticated production `/admin` remains a manual check; local authenticated proof passed before release.
- The dirty live source checkout stayed at `f03f3d0`; release source and builds are isolated under `/mnt/cache/appdata/penthouse/releases/status-8336c06`.
- Rollback timestamp is `20260904T131512Z`: API tag, static bundle, env snapshot, and fresh PostgreSQL dump are retained under the documented release-backup paths.

## September 4 minor update - 2026-09-04

- `worker/fara-pipeline` commits `a114d76` and `7feb923` are pushed and live at revision `7feb923596ae68ac1a5a20ca28376af279cba4fb` without changing package version `4.3.0-alpha.2`.
- API image `sha256:b6ad8a5471d854d514521bd130402081f82610fe74b06a352461f90079791b5d` and the matching static PWA are live; API, Caddy, PostgreSQL, public health, changelog, and PWA assets passed.
- Live desktop and mobile Chromium proved the September 4 and September 3 cards with no overflow, browser errors, failed requests, or HTTP error responses. Unauthenticated archived-chat access correctly returned 401.
- The checksum-matched release is isolated under `/mnt/cache/appdata/penthouse/releases/sep4-7feb923`; the dirty live checkout stayed at `f03f3d0`.
- Rollback timestamp is `20260904T225958Z`: the prior API image, static bundle, environment, revision, and fresh PostgreSQL dump are retained under the documented backup paths.

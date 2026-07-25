---
tags: [penthouse, timeline, changelog, rebuild]
created: 2026-03-05
---

# Rebuild Timeline

## Why this rebuild exists

The previous iteration accumulated too many intertwined changes. Fixing one thing broke another.  
The rebuild goal is stability first, with a strict order of implementation to prevent future cleanup pain.

## Locked baseline

- Mobile app: Vue 3 + Vite + Capacitor (Android-first)
- Backend: Fastify + PostgreSQL
- Shared contracts: `packages/contracts`
- Process: verify-first evidence, serial gated workflow, explicit owner/reviewer/arbiter

## Timeline of concrete progress

### 2026-03-04 - Stage B/C backend hardening

Commit: `18fc1aa`  
Highlights:
- Added integration tests for auth rotation/logout and chat authorization/idempotency.
- Normalized refresh error messages to avoid token lifecycle leakage.
- Filled OpenAPI spec from stub to full contract coverage.

### 2026-03-04 - Mobile app decomposition

Commit: `93ca6f1`  
Highlights:
- Split monolithic `App.vue` into focused components:
  - `AuthPanel`
  - `ChatListPanel`
  - `MessageList`
  - `MessageComposer`
  - `ConnectionStatus`
- Added mobile-first responsive behavior and clearer chat UI states.

### 2026-03-04 - Mobile review fixes

Commit: `8e38ee2`  
Highlights:
- Socket auth now reads token dynamically on reconnect.
- Re-join chat room on reconnect.
- Queue flush no longer blocks on one failed item.
- Removed dead code/CSS.

### 2026-03-05 - Test harness maturity

Commit: `ca53a8f`  
Highlights:
- Migrated UI tests to Vitest + happy-dom.
- Added optimistic-message flow tests in `App.test.ts`.
- Landed 17 passing mobile tests.

### 2026-03-05 - Race hardening pass (working tree)

Current uncommitted hardening pass:
- Atomic refresh rotation to prevent concurrent replay minting multiple refresh tokens.
- Atomic message idempotency handling for REST and Socket paths using conflict-safe insert.
- Added concurrent regression tests for both cases.
- Added safe parsing for stored user data to prevent boot crash on corrupt localStorage.

### 2026-03-08 - User management backend foundation

Current working tree:
- Added user profile fields, roles, statuses, avatar linkage, and forced-password-change support.
- Added member self-service APIs for profile update, password change, and recovery code rotation.
- Added member directory APIs.
- Added admin backend APIs for invite rotation, member search, remove, ban, temp password, and chat audit history.
- Tightened auth so protected requests reload live user state from the database.
- Added integration coverage for admin bootstrap, invite rotation, temp-password flow, access revocation, and moderation-hidden messages.

### 2026-03-09 - Realtime hardening

Highlights:
- Replaced boolean-only socket status with an explicit realtime state machine.
- Added bounded degraded polling for the active chat only.
- Added Android-focused socket diagnostics and API-side observability logs.
- Hardened Socket.IO path/origin handling for Capacitor and emulator testing.

### 2026-03-09 - Media integration

Highlights:
- Added image, video, file, and GIF message support.
- Wired uploads through the API and normalized media metadata.
- Added Giphy/Klipy picker support and fullscreen media viewing.

### 2026-03-10 - Stability Fixes v1

Highlights:
- Split mobile session persistence into native/web storage adapters.
- Added test DB safety checks to prevent destructive local integration mistakes.
- Tightened chat viewport containment and Android IME handling.
- Hardened Klipy parsing and error handling.

### 2026-03-11 - Native notifications + strict read receipts

Highlights:
- Added Capacitor local notifications for unread messages outside the active live chat.
- Tightened `seen` so it only advances when the receiver is in-app, in-chat, and at the live bottom.
- Stopped launcher/background state from counting as read.

### 2026-03-12 - MVP Stability Plan v2 backend hardening

Current working tree:
- Contracts updated for versioned test-account acknowledgement.
- Migration `007` added for notice acceptance persistence.
- Backend notice-gating is complete across register, auth payloads, protected-route gating, and socket auth.
- Backend regression coverage expanded for notice-version mismatch and acknowledgement flows.
- Rollout is paused pending UI recovery and client-side notice UX wiring.

### 2026-03-15 - Runtime UI recovery follow-up

Current working tree:
- Typing was already wired end-to-end, but the indicator lived inside the scroll container and was clipped below the viewport in real chats.
- Directory presence looked missing in runtime because offline users rendered no marker at all. The directory now always shows a presence dot.
- Klipy inline chat rendering was using the preview asset instead of the animated asset. Inline playback now follows the animated URL.
- The typing event contract now accepts nullable `displayName` values so valid typing events are not dropped for users without a display name.
- Two-emulator Android retesting confirmed typing, presence, and Klipy inline playback are restored in runtime.

### 2026-03-19 - Push proof + public rollout staging

Current working tree:
- Android push is now proven on Google Play-backed emulator/runtime paths:
  - background push works
  - killed-app push works
  - push tap-through opens the correct chat
  - logout cleanup still holds
- The failed push investigation ended with two environment truths:
  - AOSP-only emulator images are not the right target for Firebase push validation
  - the backend must actually start with the Firebase Admin key configured or FCM silently becomes a no-op
- Public rollout support was added and staged:
  - rebuild landing page
  - legacy fallback page
  - separate rebuild APK path
  - preserved legacy APK path
- TrueNAS staging now runs beside the old live app before public cutover.
- Android release readiness moved forward:
  - release build baseline bumped to `versionCode 100`
  - `versionName` set to `2.0.0-alpha.1`
  - optional signing scaffold added
  - fresh signing key created outside the repo
  - signed rebuild APK produced and copied to the TrueNAS rebuild downloads directory

### 2026-04-14 - TrueNAS PWA Deploy Retry

Highlights:
- Fixed production Compose blockers for optional FCM and required `ALTCHA_HMAC_KEY`.
- Fixed the production API image so workspace-local API dependencies are copied into the runtime image.
- Cloned the `pwa` branch to `/mnt/Storage_Pool/penthouse-rebuild/app` on TrueNAS.
- Built and copied the SvelteKit PWA output into `infra/compose/site/public`.
- Started the TrueNAS Compose stack with `postgres`, `api`, and `caddy`.
- Ran database migrations through the built API runtime entrypoint.
- Verified Docker-internal API health returns OK.
- Updated DNS for `penthouse.blog` and `api.penthouse.blog` to WAN IPv4 `69.250.152.141`.
- Restarted Caddy and obtained certificates for both domains.
- Verified `https://penthouse.blog/` returns HTTP 200.
- Verified `https://api.penthouse.blog/api/v1/health` returns OK.
- Ran a headless browser smoke against `https://penthouse.blog/`. It redirects to `/auth` and shows the sign-in UI.

Current blocker:
- Public cutover is not complete until APK downloads and logged-in chat proof pass.
- `/mnt/Storage_Pool/penthouse-rebuild/downloads` is empty, so `https://penthouse.blog/downloads/the-penthouse.apk` and `https://penthouse.blog/downloads/the-penthouse-rebuild.apk` return HTTP 404.
- No local or TrueNAS APK artifact was found during the 2026-04-14 deploy retry.
- Browser smoke still sees pre-auth protected calls to `/api/v1/chats/self` and `/api/v1/chats`. These do not block auth UI loading, but should be cleaned up so production console/API diagnostics stay quiet.

### 2026-04-15 - Backup Pool Cutover

Highlights:
- TrueNAS reported `Storage_Pool` as `OFFLINE` and `Backup` as `ONLINE`.
- Docker/App storage was already configured for `Backup/ix-apps`.
- The readable `/mnt/Storage_Pool/penthouse-rebuild` deployment tree was copied to `/mnt/Backup/penthouse-rebuild` while the Compose stack was stopped.
- `infra/compose/.env` was backed up and rewritten so TrueNAS bind mounts point at `/mnt/Backup/penthouse-rebuild`.
- The Compose stack was rebuilt and restarted from `/mnt/Backup/penthouse-rebuild/app/infra/compose`.
- Verified the running container mounts now point at `/mnt/Backup/penthouse-rebuild/{postgres,uploads,downloads,caddy-data,caddy-config}`.
- Ran migrations from the API container. Result was `[migration] complete`.
- Verified `https://penthouse.blog/` returns HTTP 200 and `https://api.penthouse.blog/api/v1/health` returns OK after the cutover.

Current blocker:
- APK downloads are no longer the public source of truth. The PWA at `https://penthouse.blog/` is the default release surface.
- Legacy APK status stays unavailable until an older APK is recovered and placed under `/mnt/Backup/penthouse-rebuild/downloads/legacy/the-penthouse.apk`.
- The deployment folder is still named `penthouse-rebuild`. That is only a NAS path label. The code comes from the `pwa` branch of the current optimized repo.

### 2026-04-15 - PWA-first distribution policy

Highlights:
- Added `GET /api/v1/app-distribution` so clients can read the current install policy from the backend.
- The endpoint reports `sourceOfTruth: "pwa"` and `defaultPlatform: "pwa"`.
- Android APK metadata is explicitly deprecated legacy metadata and defaults to `status: "unavailable"`.
- Production env now supports `PUBLIC_APP_URL`, `LEGACY_APK_DOWNLOAD_PATH`, and `LEGACY_APK_STATUS`.
- Caddy redirects `/downloads/the-penthouse-rebuild.apk` to `/`, because the PWA itself is the rebuild now.
- Caddy redirects `/downloads/the-penthouse.apk` to `/downloads/legacy/the-penthouse.apk` for stale links.

Current blocker:
- The legacy APK file has not been found locally or in the Backup deployment tree yet.
- Claude/frontend handoff remains: remove APK-forward UI language, consume `/api/v1/app-distribution`, and make the PWA install path the only primary CTA.

### 2026-04-15 - Alpha deploy and PWA smoke

Highlights:
- Pushed Claude's welcome-page/auth-guard handoff commit to `origin/pwa`.
- Built the SvelteKit frontend locally because the TrueNAS host does not have `npm`, then copied `apps/web/build/` into `/mnt/Backup/penthouse-rebuild/app/infra/compose/site/public/`.
- Added absolute service-worker registration in `apps/web/src/app.html` so `/sw.js` registers with scope `/` on routed pages like `/welcome` and `/auth`.
- Rotated production `JWT_SECRET` and `ALTCHA_HMAC_KEY`. Old sessions were intentionally invalidated.
- Rebuilt and restarted the TrueNAS Compose stack from `/mnt/Backup/penthouse-rebuild/app/infra/compose`.
- Ran migrations inside the production API container. Result was `[migration] complete`.
- Added nightly PostgreSQL dumps through TrueNAS cron job `1` at 03:00 using `/mnt/Backup/penthouse-rebuild/scripts/nightly-pg-dump.sh`.
- Verified backup integrity with `gunzip -t` and restored the latest dump into a temporary `penthouse_restore_test` database before dropping it.
- Verified public API health and app-distribution metadata:
  - `https://api.penthouse.blog/api/v1/health`
  - `https://api.penthouse.blog/api/v1/app-distribution`
- Verified APK policy:
  - `/downloads/the-penthouse.apk` redirects to `/downloads/legacy/the-penthouse.apk`
  - `/downloads/the-penthouse-rebuild.apk` redirects to `/`
- Ran production backend smoke against `https://api.penthouse.blog`: registered two users, created a DM, sent a message, and read it back.
- Ran browser/PWA smoke against `https://penthouse.blog`: root redirects to `/welcome`, the landing CTA reaches `/auth`, manifest is valid, `/sw.js` controls the page, and the shell renders offline for `/welcome` and `/`.
- Promoted release metadata to `2.1.0-alpha.1` for tag `v2.1.0-alpha.1`.

Known follow-up:
- The welcome page's third-party Erode font CSS returned HTTP 500 during smoke. The page falls back successfully, but the font should be removed or self-hosted during the next frontend pass.
- Manual Add-to-Home-Screen proof is still needed on a real mobile browser.

### 2026-03-28 - Public site refresh

Highlights:
- Redesigned the staged rebuild landing page to match the mobile app's visual identity.
- Logo treatment aligned with the app auth screen: "The" in periwinkle Erode 300, "PENT HOUSE" in light Erode 300.
- Typography standardized: Ubuntu (body), JetBrains Mono (technical labels), Erode (logo only).
- Palette pulled from the mobile app's CSS variables (`--bg-base`, `--action-primary`, `--text-secondary`, etc.) for coherence.
- Buttons changed from gradient fills to frosted glass periwinkle with backdrop-filter.
- Added glassmorphic cards for testing scope and legacy fallback sections.
- Atmospheric background: radial gradient ellipses, floating orbs, grain texture overlay.
- Mobile-first responsive: 1.5x logo on phones, generous side margins, safe area insets, reduced-motion support.
- Three POC variants explored (Soft Glass, Editorial Stack, Neon Pulse). Editorial Stack chosen and refined.
- Copy updated to singular/first-person voice reflecting single-tester staged rollout.
- Both APK download paths preserved: `/downloads/the-penthouse-rebuild.apk` and `/downloads/the-penthouse.apk`.

## Where this leaves us now

- Auth, chat, media, user management, realtime hardening, and Android push foundations are present.
- Phase 1/2 backend work for MVP Stability Plan v2 is done in code.
- Strict DB release gate still needs a clean rerun in a working Docker/Postgres environment.
- Public PWA/API cutover is live on the Backup pool. The remaining operational blockers are strict DB gate rerun, mobile install proof, and cleaning up the third-party font dependency.


### 2026-05-06 - v4 Clean-Room Rebuild Begins (Kimi)

**Scope:** Complete frontend-backend rebuild from scratch.
**Agent:** Kimi K2.6

Highlights:
- Decided on stack: SvelteKit 2 + Svelte 5 + Fastify 5 + Drizzle ORM + Socket.IO 4
- Reason: v2.1 accumulated 29 migrations, 2,287-line chat monolith, raw `pg` queries
- Decomposed chat page into lazy-loaded components
- Deterministic Drizzle schema from day one (no incremental migration drift)
- Bootstrapped `apps/web/` SvelteKit PWA with `@vite-pwa/sveltekit`
- Built auth, socket store, chat UI, settings, push banner, audio recorder
- Created comprehensive backend scaffold guide for Codex (`docs/adr/04-backend-scaffold.md`)

### 2026-05-06 - Backend Implementation (Codex)

**Scope:** `services/api/` implementation.
**Agent:** Codex

Highlights:
- Fastify 5 + Drizzle ORM + Socket.IO 4
- Auth routes (register, login, refresh, logout)
- Chat/message REST routes
- Socket.IO realtime (join, leave, message send/ack/broadcast)
- Push notifications (VAPID endpoints + delivery)
- Media uploads (multipart)
- Rate limiting on auth surface
- Integration tests for all routes

### 2026-05-06 - Frontend-Backend Integration (Kimi)

**Scope:** Wire frontend to real backend, fix bugs.
**Agent:** Kimi K2.6

Highlights:
- Wired `+page.svelte` to `/api/v1/chats` API (real chat list)
- Fixed IntersectionObserver leak (create once, observe incrementally)
- Fixed socket reconnect listener loss (watch `socketStore.instance`)
- Fixed typing timer stale closure (per-user Map)
- Fixed push badge undefined (`payload.badge ?? undefined`)
- Fixed auth button contrast (dark text on gold)
- Added graceful shutdown (SIGTERM/SIGINT handlers)
- Security hardening: updated vulnerable packages (`@fastify/jwt` 9→10, `@fastify/static` 8→9, `drizzle-orm` 0.38→0.45)
- Client-side outbox store (localStorage, 5 retries, survives reloads)
- Offline fallback page (`static/offline.html`)

### 2026-05-07 - AntiGravity Browser Testing

**Scope:** End-to-end validation across all user flows.
**Agent:** Gemini 3 Pro (AntiGravity IDE)

Highlights:
- All 8 stages passed: Visual, Auth, Chat, Push UI, Offline, Settings, Accessibility, Audio
- Found and confirmed bugs:
  - `effect_orphan` crash - `$effect` inside `.svelte.ts` module level
  - Edit/Delete sync failure - REST handlers didn't emit socket events
  - Offline composer disabled - `disabled={!socketStore.isConnected}`
  - CAPTCHA blocking automation
- Bugs fixed during testing:
  - Moved `$effect` to `+layout.svelte`
  - Added `fastify.io.to(...).emit(...)` to PATCH/DELETE handlers
  - Removed disabled prop, added pending indicator (◌)
  - Auto-bypassed CAPTCHA in dev via `PUBLIC_SKIP_CAPTCHA=true`
- Re-test confirmed edit/delete sync works live
- Re-test confirmed offline composer queues and delivers on reconnect

### 2026-05-07 - Push Notification Hardening

**Scope:** VAPID configuration + testing prep.
**Agent:** Kimi K2.6

Highlights:
- Generated VAPID keys: `npx web-push generate-vapid-keys`
- Added to `services/api/.env` and `apps/web/.env`
- Verified `/api/v1/push/vapid-key` endpoint returns public key
- Created `docs/AGENT-HANDOFF-PUSH-TESTING.md` for AntiGravity
- All services restarted with new config

### 2026-05-14 - V5 Redesign (Kimi)

**Scope:** Complete visual redesign - theme system, component token swap, chat clustering, profile styles, wallpaper purge.
**Agent:** Kimi K2.6

Highlights:
- 5-theme OKLCH design system with dark/light mode support
- Inline `style:` token binding replaces CSS theme blocks
- All P0 components migrated from `--color-*` to `--p-*`
- New components: `AppearanceSettings`, `ThemePicker`, `ProfileStyleSettings`, `ProfileCard`
- Users page rewritten with roster + focus pane split layout
- Chat layout restructured with clustering, time-below-pfp, sibling-reactions-row
- Wallpaper system fully deleted (store, service, routes, schema, contracts)
- Backend schema updated: `profile_style` + `banner_url` columns on `users`
- Migration `0006_profile_style.sql` adds columns and drops `user_wallpapers`
- Avatar fallback texture overlay (fractal noise, 45% dark / 30% light)
- Build clean across frontend, contracts, and backend
- Pushed as commit `e5417c0` on `main`

### 2026-07-14 - v4.2 Privacy Terms and Operator Trust (Codex)

**Scope:** Public legal pages, real admin diagnostics, backend hardening, version realignment.
**Agent:** Codex

Highlights:
- Added `/privacy` and `/terms` routes with plain first-person copy
- Linked legal pages from registration and Settings
- Replaced placeholder admin counters with real system, backup, push, and error sections
- Consolidated rate limiting across auth surfaces
- Hardened notification lifecycle, validation, and error mapping
- Removed dead code and unused dependencies
- Added Caddy security headers
- Realigned all package versions to `4.2.0-alpha.1`
- Full validation passed: typecheck, lint, format, API tests, production build

### 2026-07-22 - v4.3 Collaboration Wave (Kimi + Codex)

**Scope:** Community discovery, invites, forwarding, files, and privacy-first social embeds.
**Agents:** Kimi K2.6 frontend, Codex backend wiring and verification

Highlights:
- Replaced the People tab with a Community screen
- Added People, Discover, Requests, and Invites tabs
- Built compact group discovery cards
- Added public direct-join and private request-to-join flows
- Added manager invite links with expiry and use limits
- Built `/join?token=...` redemption that survives sign-in
- Made General an opt-in community hub instead of automatic membership
- Added scrollable underline channel tabs with a right-edge pointer
- Added locked-channel notice for manager-only channels
- Added message forwarding to several chats with recipient chips
- Updated file attachment cards with softer captions and clearer metadata
- Added gated social embeds with Auto, Ask first, and Never modes
- Stored embed consent in the user profile via migration `042`
- Added rate-limited `GET /api/v1/embeds/preview` that returns metadata only
- Full validation passed: web typecheck, web unit tests, API integration tests, contract tests, WebKit collaboration wiring test, production build

## Where this leaves us now

- Auth, chat, media, push, user management, realtime hardening, and accessibility are present and tested.
- V5 redesign is live on `main`: 5 themes, light mode, clustering, profile cards.
- v4.2 shipped public legal pages and real admin diagnostics.
- v4.3 shipped community discovery, invites, forwarding, files, and gated embeds.
- AntiGravity browser testing signed off on all 8 stages.
- Push notification VAPID keys configured, ready for delivery testing.
- Remaining blockers: split the dirty collaboration-wave tree into clean commits, update stale Playwright helpers, manual mobile PWA install proof, actual push delivery on real device.

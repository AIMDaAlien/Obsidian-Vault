---
tags: [penthouse, rebuild, knowledge-base, obsidian]
created: 2026-03-05
published_to_garden: true
last_published: '2026-07-25T21:05:10.185673'
---

# The Penthouse Rebuild Knowledge Hub

This vault is the "what we built and why" map for people joining the project later.

## Read in this order

1. [[01 - Rebuild Timeline]]
2. [[02 - Architecture in Plain English]]
3. [[03 - Stability Rules (Anti-Tech-Debt)]]
4. [[04 - Reliability Fix Log]]
5. [[05 - Multi-Model Delegation Workflow]]
6. [[06 - Copyable Rebuild Checklist]]
7. [[07 - User Management Basics]]
8. [[08 - Live Chat Essentials]]
9. [[09 - Realtime Hardening]]
10. [[10 - Media Integration]]
11. [[11 - Stability Fixes v1]]
12. [[12 - Native Notifications and Strict Read Receipts]]
13. [[13 - MVP Stability Plan v2]]
14. [[14 - Opencode Handoff]] (historical snapshot)

### PWA rebuild (v2.1 - current branch)

15. [[15 - PWA Rebuild]] - why the frontend was rebuilt as a PWA and what the baseline covers
16. [[16 - Wave A - Live Chat on the PWA]] - typing indicators, presence, read receipts, GIF, muting
17. [[17 - Wave B - Rich Messaging]] - reactions, reply/quote, delete, pins, icon refresh
18. [[18 - Wave C - Community Features]] - slash commands, polls, note to self

### Clean-room rebuild and recent releases

19. [[19 - v4 Clean-Room Rebuild]] - SvelteKit, Drizzle, and decomposed chat
20. [[20 - V5 Redesign]] - 5 themes, tokens, profile cards, chat clustering
21. [[21 - v4.2 Privacy Terms and Operator Trust]] - public legal pages and real admin diagnostics
22. [[22 - v4.3 Collaboration Wave]] - community discovery, forwarding, files, and gated embeds

## Source docs in repo

- [[../START_HERE|Start Here (non-engineer guide)]]
- [[../adr/ADR-0001-rebuild-baseline|ADR-0001 Rebuild Baseline]]
- [[../BACKEND_READINESS_MVP_V2|Backend Readiness Report: MVP Stability Plan v2]]
- [[../../services/api/docs/RELIABILITY_DRILL|Reliability Drill Runbook]]
- [[../../antigravity/customizations|Antigravity customizations]]

## Current status (as of 2026-04-15)

- Rebuild baseline is in place:
  - Vue + Capacitor
  - Fastify + PostgreSQL
  - contract-first shared schemas
- User management is implemented:
  - profiles
  - member directory
  - admin invite/member controls
  - admin operator summary panel
  - admin message hide / restore moderation with required reasons
  - admin chat audit visibility of original content plus latest moderation metadata
  - moderation-aware member tombstones
- Realtime hardening is implemented:
  - explicit client state machine
  - bounded degraded polling
  - socket diagnostics panel
  - API-side socket observability logs
- Media integration is implemented:
  - uploads
  - inline rendering
  - fullscreen media viewer
  - Giphy/Klipy
  - local GIF/data controls in Settings
- Recent runtime recovery wins are confirmed in emulator testing:
  - auth/layout clipping resolved by the global box-sizing fix
  - typing indicator visible in real chats again
  - presence indicators readable again
  - Klipy inline playback restored
  - Klipy picker polish now respects animation/data preferences locally
- Strict local notifications + strict read receipts are implemented in the current internal build.
- Balanced Admin Suite v1 is now implemented:
  - reversible message moderation
  - required moderation reasons
  - member tombstones instead of silent disappearance
  - expanded read-only operator diagnostics for realtime, moderation, and push settings counts
- Android push is now proven on Google Play-backed Android:
  - background push works
  - killed-app push works
  - push tap-through returns to the correct chat
  - logout cleanup holds
- Device-level notification controls now exist in Settings:
  - push on this device
  - message previews on/off
  - quiet hours
  - local in-app toast toggle
- Session and device management now exists in Settings:
  - active session list backed by refresh-token sessions
  - current session labeling
  - revoke one other session
  - revoke all other sessions
  - lightweight device labels plus push-active state per session
- Ops hardening v2 is now visible in the operator panel:
  - truthful build/runtime metadata
  - uploads directory diagnostics with unavailable fallbacks
  - push counters labeled since process start
  - bounded 5xx diagnostics by route group
  - optional backup status from a real status file when configured
  - cleanup pass applied:
    - FCM warning logs no longer print raw device tokens
    - upload scanning is now capped for operator safety
    - malformed backup-status files degrade cleanly to `unavailable`
    - the Fastify 5xx response hook now has direct test coverage
- Invite and onboarding controls v1 are now implemented:
  - multi-invite management replaces the single master invite code
  - admin can create, list, and revoke invite codes with labels and optional limits
  - registration mode toggle (invite_only / closed) controls whether new accounts can be created
  - AuthPanel reflects closed mode with a clear notice instead of the registration form
  - dedicated Invites tab in admin settings
- AOSP-only emulator images are not a valid push-proof target for this Firebase path.
- Public PWA/API rollout is live on TrueNAS as of 2026-04-15:
  - the rebuild stack originally ran under `/mnt/Storage_Pool/penthouse-rebuild/app`
  - on 2026-04-15 it was copied and cut over to `/mnt/Backup/penthouse-rebuild/app` after `Storage_Pool` went offline
  - Caddy is bound on TrueNAS host ports `9080` and `9443`
  - DNS points `penthouse.blog` and `api.penthouse.blog` at the current observed WAN IPv4 `69.250.152.141`
  - Caddy certificates were issued for both domains after restarting Caddy
  - `https://penthouse.blog/` returns HTTP 200
  - `https://api.penthouse.blog/api/v1/health` returns OK
  - current bind mounts point at `/mnt/Backup/penthouse-rebuild/{postgres,uploads,downloads,caddy-data,caddy-config}`
  - PWA is now the default install/update source of truth
  - backend distribution metadata is exposed at `/api/v1/app-distribution`
  - old APK URLs are treated as legacy: `/downloads/the-penthouse.apk` redirects to `/downloads/legacy/the-penthouse.apk`, and `/downloads/the-penthouse-rebuild.apk` redirects to `/`
  - legacy APK status remains `unavailable` until an older APK is recovered and placed under `/mnt/Backup/penthouse-rebuild/downloads/legacy/`
  - browser smoke reaches `/welcome`, enters `/auth`, validates the manifest, confirms `/sw.js` controls the page, and confirms the app shell renders offline for `/welcome` and `/`
  - backend production smoke registered two fresh users, created a DM, sent a message, and read the message back from `https://api.penthouse.blog`
  - production `JWT_SECRET` and `ALTCHA_HMAC_KEY` were rotated during the alpha deploy, invalidating old sessions by design
  - nightly PostgreSQL dumps now run from TrueNAS cron job `1` at 03:00 into `/mnt/Backup/penthouse-rebuild/backups/postgres/`. Restore was tested with a temporary database
  - known frontend warning: the welcome page still requests `https://fonts.cdnfonts.com/css/erode?weights=400,600`, which returned HTTP 500 during smoke. The page falls back to local serif fonts
- Android release signing was prepared for the earlier rebuild APK path, but APK distribution is now legacy-only:
  - fresh signing key created outside the repo
  - release baseline set to `versionCode 100`
  - any recovered APK should be treated as deprecated legacy continuity, not the default release surface
- Versioned test-account acknowledgement is implemented across backend and mobile client flow:
  - contracts updated
  - migration `007` added
  - API/realtime gating active
  - mobile register/ack flow active
- Real-device smoke proof exists for the earlier Android public-domain path. The 2026-04-15 PWA TrueNAS cutover has fresh browser/PWA proof and backend DM proof. Mobile Add-to-Home-Screen proof remains a manual device check.
- Public site refresh completed:
  - landing page redesigned to match mobile app visual identity (Erode logo, Ubuntu body, JetBrains Mono technical)
  - frosted glass periwinkle palette coherent with mobile app CSS variables
  - glassmorphic cards, atmospheric background, mobile-first responsive
  - copy updated to singular first-person voice for staged single-tester rollout

## v4 Clean-Room Rebuild Status (as of 2026-05-07)

A new clean-room rebuild (`v4.0.0-alpha.1`) was started to address accumulated technical debt in the v2.1 PWA. Key differences:

| Concern | v2.1 | v4 |
|---------|------|-----|
| Frontend | Vue 3 + Capacitor | SvelteKit 2 + Svelte 5 (runes) |
| DB layer | Raw `pg` + 29 migrations | Drizzle ORM + generated migrations |
| Chat page | 2,287-line monolith | Decomposed components |
| Tests | Sequential | Parallel ephemeral DBs |
| Push | Basic VAPID | + quiet hours + per-chat mute + privacy levels |

### v4 Features Implemented

- ✅ Auth: register, login, session, logout, refresh tokens
- ✅ Chat list: real-time list with unread badges
- ✅ Chat thread: messages, composer, optimistic UI, outbox
- ✅ Reactions, replies, edit, delete
- ✅ Read receipts (IntersectionObserver + marker model)
- ✅ Typing indicators (per-user Map)
- ✅ Audio messages (MediaRecorder + upload)
- ✅ Push notifications: VAPID subscribe, permission banner, settings toggle
- ✅ Service worker: offline fallback, push handler, notificationclick routing
- ✅ Accessibility: WCAG 2.1 AA, keyboard nav, ARIA labels
- ✅ Security: dependency updates (JWT, static, drizzle)

### v4 Testing Completed

- ✅ Backend integration tests: 7 suites, all passing
- ✅ Contract tests: 25 schemas, all passing
- ✅ E2E tests: 12 passing (4 tests × 3 browsers)
- ✅ AntiGravity browser testing: All 8 stages passed
- ✅ Edit/delete real-time sync verified working
- ✅ Offline composer + outbox queue verified working

### v4 Known Limitations

- Scale: 15–25 users, ~10 concurrent (no Redis, no horizontal scaling)
- Virtual scrolling: deferred (not needed at current scale)
- Message search: deferred (needs `tsvector` + GIN)
- E2EE: deferred (post-launch)
- Voice/video calls: deferred (audio messages only)
- Bio field: backend supports it, UI input missing from settings

## V5 Redesign Status (as of 2026-05-14)

Complete visual redesign landed on `main` (commit `e5417c0`). See [[20 - V5 Redesign]] for full detail.

### What shipped

- ✅ 5-theme design system (periwinkle, sage, slate, plum, charcoal) with dark/light modes
- ✅ Inline token binding on `.app-shell` - no CSS theme blocks at runtime
- ✅ All P0 components token-swapped from `--color-*` to `--p-*`
- ✅ Settings page: `AppearanceSettings` + `ProfileStyleSettings` wired
- ✅ Profile card system: editorial / vogue / wallpaper variants
- ✅ Users page: roster + focus pane split layout with `ProfileCard`
- ✅ Chat layout: clustering, time below pfp, reactions as sibling row
- ✅ Wallpaper system fully purged (frontend + backend + contracts)
- ✅ Backend: `profile_style` + `banner_url` columns, migration `0006`
- ✅ Avatar texture overlay on fallback avatars
- ✅ Build clean: `svelte-check` 0 errors, `tsc` clean across all packages

## v4.2 and v4.3 status (as of 2026-07-22)

v4.2 shipped public privacy and terms pages plus real admin diagnostics. v4.3 shipped the collaboration surfaces. See [[21 - v4.2 Privacy Terms and Operator Trust]] and [[22 - v4.3 Collaboration Wave]] for full detail.

### What v4.2 added

- Public `/privacy` and `/terms` routes with honest self-hosting language
- Settings Legal section and registration acknowledgement links
- Admin dashboard with real system, backup, push, and error diagnostics
- Shared rate limiting, notification lifecycle fixes, and validation hardening
- Caddy security headers and dead-code removal
- Package versions realigned to `4.2.0-alpha.1`

### What v4.3 added

- Community screen with People, Discover, Requests, and Invites tabs
- Compact group discovery cards for public and private groups
- Manager invite links with expiry and use limits
- Request-to-join flow for private groups
- Scrollable underline channel tabs with a right-edge pointer
- Locked-channel notice for manager-only channels
- Message forwarding to several chats with recipient chips
- Softer file attachment cards with clear type and size
- Privacy-first social embeds with Auto, Ask first, and Never modes
- Separate embed bubbles so message text stays readable

### Current blockers

- The collaboration-wave worktree is dirty and needs clean commits before deploy.
- Older Playwright helpers assume General is auto-joined. They need updating.
- Instagram embeds fall back to generic metadata without provider credentials.
- Manual Add-to-Home-Screen proof is still needed on a real mobile browser.

## PWA rebuild status (as of 2026-04-09)

The `pwa` branch is the active development branch and public deployment target. The PWA is the canonical release surface. Older Android APKs are legacy fallback only. The current alpha release tag is `v2.1.0-alpha.1`.

- PWA baseline is complete and testable in a browser
- Wave A is complete (typing, presence, read receipts, GIF, muting)
- Wave B is complete (reactions, reply/quote, delete, pins, UI polish)
- Wave C is complete (slash commands, polls, note to self)
- Remaining Wave B items still to build: image attachments, markdown rendering, message editing

## Current blockers

- Strict DB release gate still needs a rerun in a working Docker/Postgres environment.
- Manual mobile PWA install proof is still needed on a real iOS/Android browser.
- The third-party Erode font CDN request should be removed or self-hosted in the next frontend pass.
- Push notification delivery: needs manual background-browser test on real device.

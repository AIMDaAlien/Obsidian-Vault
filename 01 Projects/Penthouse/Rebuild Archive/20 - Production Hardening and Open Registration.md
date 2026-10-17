---
tags: [penthouse, production, auth, registration, backend, hardening]
created: 2026-06-15
publish: false
project: Penthouse
---

# Production Hardening and Open Registration

## Scope

This note records the production hardening and onboarding changes completed after the 2026-05-23 frontend cleanup.

## Responsive web hardening

Committed on 2026-05-24:

- touch targets were raised to at least 44px
- safe-area spacing was added to mobile chat, people, and settings surfaces
- hover-only message actions were corrected for touch devices
- media overflow was contained inside message surfaces
- icon-only controls received explicit zero padding so the global button rule no longer clips SVGs
- registration now shows whether password and confirmation values match
- `apps/web/e2e/responsive-audit.spec.ts` was added for automated mobile checks

Commits:

- `2ee7250`
- `fb1e31c`
- `12d959d`

Recorded proof:

- production build passed
- the focused responsive/browser slice reported `21/21` E2E tests passing

## Backend chat hardening

Committed on 2026-05-24:

- split the large chat route into focused lifecycle, list, member, message, pin-preference, poll, and read route modules
- added dedicated chat sync, message-send, and pin service modules
- added a chat-member read-receipt lookup index
- added trigram indexing for message search
- tightened message sanitization and private-media ownership validation
- added delete-authorization, message-send, hydration-performance, and message-security regression coverage
- added `docs/PRODUCTION_MVP_E2E_CHECKLIST.md` as the manual release acceptance checklist

Commits:

- `abb7b6b`
- `17ea49b`

## Open registration

Committed on 2026-05-26:

- removed invite codes from the public registration request contract
- removed the invite field from the web registration form
- changed registration mode from `invite_only / closed` to `open / closed`
- migration `030_open_registration.sql` converts existing `invite_only` settings to `open`
- retained closed-mode rejection and public auth-config reporting
- repaired production ALTCHA and public environment wiring
- refreshed the built static production bundle

Commits:

- `14cf871`
- `f5d4975`

Important boundary:

- historical invite records and admin invite tooling may still exist
- invite codes no longer gate the current public registration flow
- production signup still requires a valid ALTCHA challenge

## Auth and public-page behavior

Committed and deployed:

- unknown username returns `USER_NOT_FOUND` / `User does not exist`
- incorrect password returns `WRONG_PASSWORD` / `Wrong password`
- inactive accounts remain on the generic invalid-credentials path
- the push-permission reminder only renders inside the authenticated app
- `/welcome` and `/auth` do not render the reminder

Production proof completed between 2026-05-28 and 2026-06-04:

- welcome and auth pages rendered correctly
- manifest and service worker loaded
- production public environment values were present in the built bundle
- register, login, current-user lookup, refresh, and logout passed
- DM creation, message send, and message read passed

Known boundary:

- the late auth/banner source changes were included in commit `f6f6762` and redeployed with release head `24c1d41` on 2026-06-15
- `www.penthouse.blog` remains intentionally outside the current scope

## Current validation

- web typecheck: pass, 0 errors / 0 warnings
- API typecheck: pass
- web unit tests: 4/4 pass
- API tests: 201/201 pass
- production web build: pass
- public health, auth config, CAPTCHA challenge, Socket.IO polling, manifest, and service worker checks: pass on 2026-06-15

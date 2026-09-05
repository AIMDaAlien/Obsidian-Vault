---
tags: [penthouse, security, build, cors, csp, realtime, release]
created: 2026-09-03
visibility: private
---

# Security and Build Hardening

## Current state

The `hardening/security-build-integrity` branch is implemented and locally verified from `main` revision `2bea709`. It has not been pushed, merged, deployed, or applied to Unraid. The live revision observed before work was `f03f3d0`.

## Implemented

- Production dependency audit is clean; Sharp is 0.35.4.
- Animated images retain their frames while thumbnails remain oriented, cropped, and metadata-stripped.
- Compose serves generated `apps/web/build`; the stale committed bundle was removed.
- Production wildcard CORS is rejected.
- Caddy sends CSP in report-only mode.
- The existing in-memory limiter applies globally at 600 requests per minute per IP, with health exempt and stricter route limits preserved. This remains appropriate only while one API replica runs.
- Group removal and block changes evict only affected sockets from affected rooms after the database commit.
- The unused Gradle/Android project and tracked machine configuration are gone. Historical APK distribution remains deprecated but supported.
- `docs/HANDOFF.md` is the only current handoff; old briefs live under `docs/archive/handoffs/`.

## Local proof

- Clean install and production audit: pass, zero vulnerabilities.
- Full validation: 80 web, 366 API, and 35 contract tests passed.
- Production build, Compose configurations, and Caddy validation: pass.
- Chromium through local Caddy: 10 auth, 3 presence, and 5 upload tests passed.
- The live ALTCHA checkbox solves through local Caddy; development now returns a widget-compatible SHA-256 puzzle instead of placeholder values.
- Non-admin People directories hide members the viewer blocked by default. An explicit `Show blocked users` control reveals them; Chromium verified both People views and retained DM blocking.
- Focused browser smoke passed registration, login, two-user DM delivery over Socket.IO, live presence, admin access, and the CSP report-only header.

## Remaining gate

Aim must inspect `http://127.0.0.1:18088`. After acceptance, push the branch. Merge and all Unraid changes remain separate later actions. Before CSP enforcement, resolve or deliberately allow the reported Google Fonts and generated inline bootstrap sources.

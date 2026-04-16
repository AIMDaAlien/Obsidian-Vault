---
tags: [self-hosting, security, backend, hardening]
created: 2026-02-18
published_to_garden: true
visibility: public
---

# Backend Hardening Checklist

A pragmatic list of the backend vulnerabilities and stability issues I fixed during the v1 production pass. No major redesign — just closing real gaps in a minimal-risk way.

## Database durability

- Migrated from `sql.js` (in-memory snapshot DB) to `better-sqlite3`.
- WAL mode enabled for better write concurrency.
- `synchronous=FULL` in production for durability.
- One-time conversion path from the old snapshot file to the new SQLite file.

## Auth

- Fixed a registration bug where blank email wasn't being normalized to null, causing false duplicate-check failures.
- Refresh and reset tokens are now stored as SHA-256 hashes for new rows, with a temporary plaintext fallback for previously stored tokens.
- Access token plus refresh token model replaces single-token auth.
- Return `token` as an alias for `accessToken` so older clients don't break.
- Added rate limits on refresh, logout, and forgot-password endpoints.

## Friends and blocked users

- Fixed a schema mismatch where `blocked_users.created_at` was missing from an earlier migration. Added a safe try/catch migration to fill the gap.
- `GET /api/friends/blocked` now works reliably.

## Invites

- Enforce `max_uses` atomically: a transaction wraps the check, membership insert, and uses increment together. Exhausted invites return 410.

## Message authorization (IDOR fixes)

For routes with `:messageId` parameters, the app now fetches `chat_id` from the message row and verifies membership before any side effects on: react, unreact, read receipt, pin, unpin, edit, delete.

Same check added to `GET /pins/:chatId`. Pagination limits are now clamped server-side.

## WebSocket authorization

- CORS origin allowlist aligned with HTTP CORS.
- Membership enforced on `join_chat`, `send_message`, `typing`, `stop_typing` events.
- Small short-TTL membership cache added to avoid hammering the database on typing spam.
- Socket.IO buffer and heartbeat settings tuned.

## Upload safety

- Require both a valid extension and a valid MIME type (previously it was either/or).
- Upload rate limiter added.
- Safe deletion using `path.basename()` plus a fixed upload root so path traversal payloads can't escape.

## CORS and reverse proxy correctness

- Parse `CORS_ORIGIN` as a comma-separated allowlist.
- In production: fail startup if `CORS_ORIGIN` is missing, reject wildcard origins.
- `app.set('trust proxy', 1)` so rate limiting and logs see the real client IP behind Caddy instead of the proxy IP.

## Docker hardening

- App port is not published externally — only Caddy faces the internet.
- `no-new-privileges`, `cap_drop: [ALL]`, `read_only: true`, `tmpfs: /tmp`.

## Observability

- Added `X-Response-Time` and `Server-Timing` headers to every response for lightweight latency tracking.

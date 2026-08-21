---
tags: [self-hosting, security, gotchas]
created: 2026-02-18
published_to_garden: true
visibility: public
---

# Security Gotchas (Self-Hosted, Public Internet)

A grab-bag of mistakes that are common in first-time internet deployments. Most of these I either hit directly or caught before they became incidents.

## 1. Token leaks in screenshots and chat logs

If an API token ends up in a screenshot or chat log, assume it's compromised. Revoke immediately, create a new scoped token, update your config. Don't wait to verify whether anyone actually saw it — just revoke.

This happened with a Cloudflare API token during DDNS setup. The correct response is always revoke first.

## 2. CORS with credentials and a wildcard origin

Setting `credentials: true` alongside `origin: *` doesn't work — browsers reject it or behave unexpectedly. In production, always use an explicit origin allowlist and make the app fail loudly at startup if it's missing or misconfigured.

## 3. Reverse proxy client IP trust

Without `app.set('trust proxy', 1)` behind Caddy, the app sees the Caddy container's IP for every request. This breaks rate limiting (all clients share one bucket) and makes logging useless for abuse correlation.

## 4. Home IP drift

The "server is down" symptom is often just DNS pointing at an old IP. See [[04 - IP Drift and DDNS]] for the full fix.

## 5. WebSocket authorization isn't free

HTTP auth doesn't automatically protect Socket.IO events. Minimum safe posture: authenticate the socket connection on connect, and verify membership or authorization per event (or cache that check briefly). Skipping this means anyone who can reach your WebSocket endpoint can do whatever events you haven't explicitly blocked.

## 6. IDOR in message endpoints

Routes like `/messages/:messageId/react` need to check:
- What chat that message belongs to
- Whether the requesting user is a member of that chat

Checking ownership of the message alone isn't enough. Without the membership check, a user could react to messages in chats they've been removed from.

## 7. Upload deletion path traversal

Never pass a path from user input or a database directly to `fs.unlink()`. Use `path.basename()` and a fixed upload root directory so something like `../../etc/passwd` can't escape the intended folder.

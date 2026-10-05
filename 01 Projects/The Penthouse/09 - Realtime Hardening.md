---
tags: [penthouse, realtime, socket, android, reliability, hardening, security]
created: 2026-03-08
published_to_garden: true
visibility: public
---

# Realtime Hardening

## The problem before this

Android chat only worked because HTTP polling kept refetching messages. The app still said "Realtime offline" in the corner. API logs gave almost no signal about whether socket traffic was even reaching the server. Degraded mode wasn't a deliberate mode, it was just the default broken state.

## What changed on the mobile client

Replaced the old boolean status model with a real state machine:

- `idle`
- `connecting`
- `connected`
- `degraded`
- `failed`

Added explicit diagnostics state tracking:
- Current transport
- Last socket error
- Last disconnect reason
- Last successful connection time
- Whether fallback polling is active

The Android transport order is now locked to `polling` first, then `websocket`. The Socket.IO path is set explicitly to `/socket.io/`. `rememberUpgrade` stays false.

Added resume-from-background reconnect and chat resync. Fallback polling is now limited to the selected chat, only in the chat view, and only in degraded or failed states.

There's a dev-only diagnostics panel behind the connection badge.

## What changed on the API side

- Explicit Socket.IO path set to `/socket.io/`.
- Replaced permissive socket CORS with an explicit origin allowlist covering native local testing origins (Capacitor, Ionic, standard localhost).
- Added server-side observability logs for: handshake start, engine connection errors, engine connect and close, namespace connect, auth rejection reason, and transport upgrade.

## After this slice

If Android still shows "Realtime offline":
1. Check the badge diagnostics in the app.
2. Check the API terminal for socket log lines.

No more guessing. The next debugging step is always specific.

## If true realtime still fails on Android

Escalation path if nothing else works:
1. Put local API traffic behind a dedicated local domain or proxy path.
2. Use Caddy with TLS for the local test path.
3. Stop relying on plain emulator localhost as the only transport route.

## Tests added

On the mobile side, the connection status component and the main app component now have coverage for:
- Connecting state on startup
- Degraded state on connect error
- Failed state on reconnect exhaustion
- Fallback only activating in the active chat view
- Chat rejoin after reconnect

On the API side, integration tests cover:
- Successful socket connection logs
- Invalid token auth rejection logs
- Unavailable-account auth rejection logs

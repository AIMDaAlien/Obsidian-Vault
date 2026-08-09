---
tags: [penthouse, pwa, sveltekit, knowledge-base]
created: 2026-04-05
published_to_garden: true
visibility: public
---

# The Penthouse PWA — Knowledge Hub

This is the "what we built and why" for the SvelteKit PWA migration. The `pwa` branch became the active development branch and public deployment target as of early April 2026.

## Quick facts

- **What:** Rebuilding the frontend from Vue + Capacitor native app to SvelteKit PWA
- **Why:** Faster deploys, smaller footprint, easier maintenance, no Android Studio in the loop
- **Backend:** Unchanged — Fastify + PostgreSQL, stable from the v2 rebuild
- **Status:** PWA is live at `penthouse.blog`, all feature waves complete through Wave C

## Read in this order (PWA branch)

1. [[15 - PWA Rebuild]] — what changed, why, and what the baseline covered
2. [[16 - Wave A - Live Chat on the PWA]] — typing indicators, presence, read receipts, GIF, muting
3. [[17 - Wave B - Rich Messaging]] — reactions, reply/quote, delete, pins, UI polish
4. [[18 - Wave C - Community Features]] — slash commands, polls, Note to Self

## For context on the backend and earlier rebuild

- [[00 - Knowledge Hub]] — full v2 rebuild timeline and current deployment state
- [[02 - Architecture in Plain English]] — backend architecture (unchanged in the PWA migration)
- [[07 - User Management Basics]] — user features from the backend side

## What changed vs. the native app

| Aspect | Native app (v2) | PWA (v2.1) |
|---|---|---|
| Framework | Vue 3 + Capacitor | SvelteKit 2.x |
| Distribution | Manual APK install | Browser + "Add to Home Screen" |
| Deployment | Hours (build + sign + distribute) | Seconds (web server) |
| Bundle size | ~10MB | ~200KB |
| Registration | Invite codes | ALTCHA proof-of-work |
| State management | Pinia | Nanostores + Svelte 5 runes |
| HTTP client | axios | Native fetch |

## What didn't change

- Backend: Fastify + PostgreSQL (identical)
- Real-time: Socket.IO (same events, same structure)
- Features: All chat, messaging, and user management from the v2 rebuild
- Visual identity: Dark theme, periwinkle accent, Ubuntu/JetBrains Mono fonts

## Current status (as of 2026-04-09)

The `pwa` branch is the active development branch and public deployment target.

- PWA baseline is complete and live
- Wave A complete (typing, presence, read receipts, GIF, muting)
- Wave B complete (reactions, reply/quote, delete, pins, UI polish)
- Wave C complete (slash commands, polls, Note to Self)
- Remaining staged items: image attachments, markdown rendering, message editing

## Architecture at a glance

```
Browser (PWA)
  SvelteKit app
  Service Worker (offline support, auto-updates)
  Nanostores (state)
      |
  Socket.IO (realtime events)
  HTTP / fetch (REST API calls)
  @penthouse/contracts (shared Zod schemas)
      |
    internet
      |
  Fastify backend (unchanged)
  PostgreSQL
  Socket.IO server
```

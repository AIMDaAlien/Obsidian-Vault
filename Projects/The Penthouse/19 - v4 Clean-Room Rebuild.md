---
tags: [penthouse, v4, rebuild, sveltekit, drizzle, website-rebuild, security]
created: 2026-05-07
published_to_garden: true
last_published: '2026-07-25T21:05:10.185673'
---

# v4 Clean-Room Rebuild

> Complete rebuild of The Penthouse from scratch. Smaller bundle, stronger typing, deterministic migrations.

## Why v4 Exists

v2.1 accumulated too much technical debt:
- 29 incremental migrations, hand-rolled with raw `pg`
- 2,287-line chat page monolith
- No type safety between schema and queries
- Sequential integration tests (slow)

v4 rebuilds with discipline: same features, better foundations.

## Stack Decisions

| Layer | v2.1 | v4 |
|-------|------|-----|
| Frontend | Vue 3 + Capacitor | SvelteKit 2 + Svelte 5 |
| Backend | Fastify + raw `pg` | Fastify + Drizzle ORM |
| ORM | Raw SQL | Drizzle ORM + drizzle-kit |
| Realtime | Socket.IO 4 | Socket.IO 4 (same) |
| Validation | Zod | Zod (same) |
| Testing | Vitest (sequential) | Vitest + Playwright + Node runner |
| Deployment | Docker Compose + Caddy | Same |

## Why SvelteKit over Vue

- Svelte compiles to vanilla JS (~85KB gzipped vs Vue's ~240KB)
- Svelte 5 runes simpler than Vue's reactivity system
- `@vite-pwa/sveltekit` proven in production
- Team already fluent in SvelteKit

## Why Drizzle ORM

- Type-safe queries that look like SQL:
  ```ts
  db.select().from(messages)
    .where(eq(messages.chatId, chatId))
    .orderBy(desc(messages.createdAt))
    .limit(50);
  ```
- `drizzle-kit generate` produces numbered, idempotent migrations
- No query-engine binary (unlike Prisma)
- Deterministic schema from day one — no 29 incremental migrations

## Monorepo Structure

```
the-penthouse/
├── apps/web/           # SvelteKit PWA
├── services/api/       # Fastify backend
├── packages/contracts/ # Zod schemas + shared types
└── docs/               # ADRs + planning
```

## Key Files

| File | Purpose |
|------|---------|
| `apps/web/src/routes/chat/[id]/+page.svelte` | Chat thread |
| `apps/web/src/lib/stores/socket.svelte.ts` | Socket.IO store |
| `apps/web/src/lib/stores/outbox.svelte.ts` | Offline queue |
| `services/api/src/routes/chats.ts` | Chat REST routes |
| `services/api/src/realtime/socket.ts` | Socket.IO handlers |
| `services/api/src/push/send.ts` | Push delivery |
| `packages/contracts/src/api.ts` | Zod schemas |

## Testing

| Suite | Count | Status |
|-------|-------|--------|
| Backend integration | 7 suites | ✅ All pass |
| Contract validation | 25 schemas | ✅ All pass |
| E2E (Playwright) | 12 tests | ✅ All pass |
| AntiGravity stages | 8 stages | ✅ All pass |

## What's Same as v2.1

- Fastify 5 backend framework
- Socket.IO 4 realtime
- Zod validation
- PostgreSQL 16
- Docker Compose + Caddy deployment
- JWT + refresh token auth
- VAPID web-push

## What's Different from v2.1

| Feature | v2.1 | v4 |
|---------|------|-----|
| Frontend framework | Vue 3 | SvelteKit 2 |
| DB access | Raw `pg` | Drizzle ORM |
| Migrations | 29 hand-rolled | Generated from schema |
| Chat page | 2,287 lines | Decomposed components |
| Tests | Sequential | Parallel ephemeral DBs |
| Bundle | ~240KB | ~85KB |
| Outbox | Basic | 5 retries, localStorage |
| Push | Basic VAPID | + quiet hours + per-chat mute |
| Accessibility | Partial | WCAG 2.1 AA verified |

## V5 Follow-Up

The V5 visual redesign landed on `main` (2026-05-14, commit `e5417c0`). It builds directly on the v4 foundation without changing the stack:

- Same SvelteKit 2 + Svelte 5 frontend
- Same Fastify + Drizzle backend
- Same contract-first architecture

What changed: the entire color system, component token strategy, chat layout structure, and settings UX. See [[20 - V5 Redesign]] for the full breakdown.

## Open Questions

1. Should `/` be a branded landing page or redirect to `/auth`?
2. File storage: local disk (dev) → S3/R2/MinIO (production)?
3. Altcha HMAC key: need real production key
4. Custom modal to replace `alert()`/`prompt()`

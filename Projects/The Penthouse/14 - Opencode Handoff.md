---
tags: [penthouse, handoff, historical, website-rebuild, hardening]
created: 2026-03-12
archived: 2026-03-22
published_to_garden: true
visibility: public
---

# Opencode Handoff (Historical)

> This note is a historical snapshot from the internal rollout period (March 2026). It's not current execution guidance — it's a reference for where the project stood at that point. For current state, see [[00 - Knowledge Hub]].

## What the project was at this point

- Mobile-first app rebuild
- Vue 3, Vite, Capacitor on the frontend
- Fastify and PostgreSQL on the backend
- Shared contracts in `packages/contracts`
- Android-first internal testing

## What had been built at the time

- Invite auth with refresh token rotation
- Shared General chat
- Realtime hardening with bounded degraded polling
- User management backend and member-facing UI
- Media upload and rendering with GIF picker support
- Strict read receipts and local notifications
- Backend test-account acknowledgement gating

## What was still incomplete at the time

Everything below has since been resolved — see [[13 - MVP Stability Plan v2]] and [[00 - Knowledge Hub]] for current state.

- Local notifications needed UX hardening.
- Strict read logic needed more validation around background and live-bottom behavior.
- Mobile UI recovery was incomplete — right-edge clipping remained on narrow screens.
- Test-account acknowledgement existed on the backend but the mobile register/ack flow wasn't wired yet.

## Operating rules at the time

- Public rollout was paused.
- Backend work was owned by a dedicated AI agent for that domain.
- All non-backend work for that cycle was delegated to a separate agent.
- The frontend visual agent was paused unless explicitly re-enabled.

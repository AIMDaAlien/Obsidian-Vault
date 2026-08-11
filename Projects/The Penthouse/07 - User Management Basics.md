---
tags: [penthouse, user-management, auth, admin]
created: 2026-03-08
published_to_garden: true
visibility: public
---

# User Management Basics

> [!note] Current trust-safety work
> Member block/unblock controls now exist in the `trust-safety/blocks` worktree, with broad Kimi verification completed on 2026-08-04. They are not committed or deployed because final concurrency fixes remain. See [[23 - Trust and Safety Blocks]].

## Why this slice mattered

Before this work the app could do basic invite auth and shared chat, but it had no real account management. No profiles, no member directory, no way to remove someone, no forced password change. It could demo chat but couldn't manage people. This slice fixed that.

## What Phase 1 locked in

### User model

Users now carry:
- `displayName`
- `bio`
- `avatarMediaId`
- `role` — either `admin` or `member`
- `status` — `active`, `removed`, or `banned`
- `mustChangePassword`

Important rule: `username` stays the immutable login identifier and can't be changed.

### Live enforcement on every request

Every protected request now reloads the live user row from the database, which means:
- Removed or banned users are blocked immediately, not just on next login.
- Role changes take effect immediately.
- Forced password change state takes effect immediately.

This closed a gap where an old access token could keep working after an admin action had already happened.

### Member self-service endpoints

- `GET /api/v1/me`
- `PATCH /api/v1/me/profile`
- `POST /api/v1/me/password`
- `POST /api/v1/me/recovery-code/rotate`
- `GET /api/v1/members`
- `GET /api/v1/members/:memberId`

### Admin backend endpoints

- Invite management — create, list, revoke
- Registration mode toggle — `invite_only` or `closed`
- Member management — remove, ban, temp password
- Chat audit — admin visibility into message history

**Boundary worth noting:** the admin backend exists, but a dedicated admin site UI was deferred at this stage.

### Moderation visibility

There are two layers of moderation:

**Account-level:** Removed or banned users lose access immediately. Their old messages show as generic tombstones in normal chat history.

**Message-level:** Admins can hide individual messages and restore them later. Both actions require a moderator reason. Normal members see a tombstone, but admin audit still shows the original content and the latest moderation metadata.

Important rule: moderation is reversible in v1. There's no hard delete in this slice, and moderator reasons stay admin-only.

## What was verified with integration tests

- Admin bootstrap
- Multi-invite CRUD and revocation
- Registration mode toggle
- Profile update
- Recovery code rotation
- Password change
- Temporary password plus forced change flow
- Immediate remove and ban access revocation
- Hidden message visibility differences between members and admins

## What Phase 2 added (Balanced Admin Suite v1)

- Message hide and unhide with append-only moderation event logging
- Realtime member updates that flip moderated messages into tombstones without a reload
- Dedicated admin moderation panel in Settings
- Richer read-only operator diagnostics for realtime socket state, moderation counts, and push device counts

## What Phase 3 added (Invite and Onboarding Controls v1)

Replaced the single master invite code with proper multi-invite management:

- `signup_invites` restructured with UUID primary key, label column, optional max uses and expiry
- `server_settings` table stores registration mode
- Admin can create, list, and revoke invite codes
- Registration checks mode first — closed mode rejects with 403 before even looking at an invite
- Public `GET /api/v1/auth/config` lets unauthenticated clients know the registration mode before trying to sign up
- Dedicated Invites tab in admin settings with a registration mode toggle
- Auth page reflects closed mode by replacing the registration form with a clear notice

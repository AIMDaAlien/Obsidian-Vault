---
tags: [penthouse, trust-safety, blocks, direct-messages, release, hardening]
created: 2026-08-09
visibility: private
---

# Trust and Safety Blocks

## Current state

Trust and safety blocks shipped to `https://penthouse.blog` on August 9, 2026 as `v4.3.0-alpha.2`.

- Production revision: `f03f3d0ca467a7003fd0ddd0f98b0d4e98c0427f`
- Migration: `043_user_blocks.sql`
- Public changelog: `https://penthouse.blog/welcome/updates`
- Supported topology: one API instance

## What is live

- Members can block or unblock someone from a profile and manage their blocked list in Settings.
- Existing DMs become read-only in both directions. History remains readable.
- New direct contact, sends, edits, reactions, pins, replies, forwards, and DM-request acceptance are blocked at the backend boundary.
- Blocked pairs do not receive each other's DM presence, typing, web push, or FCM notification work. Shared groups remain unchanged.
- Blocking declines pending DM requests in both directions. Unblocking does not recreate them.
- Removing a DM from the sidebar is now a personal archive. It stays hidden after navigation and refresh, preserves every message, and restores the same chat when deliberately reopened.
- Message writes, channel creation, block mutations, DM requests, HTTP limits, and reconnecting socket limits received additional race and abuse hardening.

## Release proof

- DeepSeek V4 Flash 0731 reported 295 API, 57 web, and 35 contract tests passing, plus focused Chromium block/archive proof and race scenarios.
- A post-deploy two-account smoke passed 14 checks: live WebSocket delivery, symmetric blocked-DM read-only state, hidden composer, Settings list, unblock, persistent personal archive, identical chat restoration, and retained history.
- The live public updates page rendered the August 9 block and DM archive ticket in Chromium.
- Disposable production fixtures were removed. Production returned to 7 users, 11 chats, and 51 messages with zero fixture users, chats, messages, sync events, blocks, or DM requests.

## Rollback record

- API image: `penthouse-api:rollback-20260809T215938Z`
- Database dump: `/mnt/user/penthouse-backups/postgres/penthouse-predeploy-20260809T215938Z.sql.gz`
- Static bundle: `/mnt/cache/appdata/penthouse/backups/releases/predeploy-20260809T215938Z-public.tgz`
- Checksums: `/mnt/cache/appdata/penthouse/backups/releases/predeploy-20260809T215938Z.sha256`

## Boundaries still open

- A push already handed to an external provider cannot be recalled if a block lands in the final delivery window.
- An in-flight presence broadcast can briefly show stale state before the block's corrective offline event.
- Typing suppression uses process-local memory; horizontal scaling requires shared state such as Redis.
- The production dependency install reports 12 audit findings across the full host dependency tree. Treat this as a separate dependency-review ticket, not a blind upgrade during a release.

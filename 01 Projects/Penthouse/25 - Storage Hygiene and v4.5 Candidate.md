---
tags: [penthouse, storage, media, retention, quota, release]
created: 2026-10-12
updated: 2026-10-12
publish: false
project: Penthouse
---

# Storage Hygiene and the v4.5 Candidate

## What landed

Branch `feat/storage-hygiene`, PR #37 against `main`, 29 commits, all four CI jobs green on 2026-10-12. Not merged; Aim decides. Spec and plan ride on the branch under `docs/superpowers/`.

- Deleted-media retention per member (`instant`, `24h`, `7d`, `30d`; default 7 days) chosen in Settings → Privacy. Deleting a message schedules its files for purge from the deleter's setting. Files still referenced by another live message, and public uploads (avatars, banners, stickers, emotes), are never scheduled.
- Maintenance: an orphan sweep (uploads never attached within 24 h, excluding profile, sticker, emote and chat-avatar references) and a purge job (unlink + `purged_at`), every 15 minutes under Postgres advisory lock `7231001`, skipped when `RECOVERY_MODE=standby`. Moves unchanged into the worker container in sub-project 3.
- Quota: 10 GB per member on chat media, 1.5 TB global ceiling, refused at upload with `413 STORAGE_QUOTA_EXCEEDED` / `507 STORAGE_CEILING_REACHED`. `GET /api/v1/media/usage`; Settings → Account shows a storage bar.
- Purged media serves `410 MEDIA_PURGED`; the client shows "Media expired".
- Chat GIFs re-encoded to animated WebP (quality 80, effort 4); kept as GIF when not smaller or when decoding fails.
- Migration `045_media_lifecycle.sql` with backfills and a 7-day grace period for pre-existing unreferenced uploads.

Env (all defaulted): `STORAGE_QUOTA_GB=10`, `STORAGE_GLOBAL_CEILING_GB=1500`, `MAINTENANCE_INTERVAL_MINUTES=15`.

## Decisions worth remembering

- "Live message" means no row in `message_deletions`; there is no `deleted_at` on messages.
- Message deletion never purges public or non-quota uploads, or any member could delete-on-instant a message quoting someone's sticker and unlink it.
- A new message that references an upload cancels any pending purge on it.
- A storage key that escapes the upload directory aborts the purge run loudly rather than silently skipping.
- Settings seeds the retention control from a fresh `/auth/me` call; moving the field onto the session user is a follow-up.
- "Media expired" is message-level today; element-level inside the gallery component is a follow-up.
- New sticker or emote images count toward the uploader's quota until the upload route gains a purpose for them.

## Ops after deploy

- The three over-cap PDFs from the uncapped weekend were deleted from Unraid uploads on 2026-10-12 (Aim: they were temporary). Their `media_uploads` rows remain and each sits in one message. After 045 runs, set `purged_at = now()` on those three rows so clients get a clean 410 instead of a 404. Row ids and the SQL are in the branch's `docs/HANDOFF.md`.
- Dev databases that applied an earlier draft of 045 must delete its `api_migrations` row before `migrate.ts` re-applies it.
- `services/api` unit suite takes about 11 minutes (a quiet stretch in `rate-limit-global.test.ts`, pre-existing).

## Version

Code is `4.4.0-alpha.1` everywhere (root, web, api, contracts). This feature changes the data model, adds a background job, adds two env-driven limits, and changes user-visible behaviour (quota refusals, expired media). That is a minor bump by semver and a big enough change for members to notice, so `4.5.0-alpha.1` fits. `CLAUDE.md` says versions are bumped at release time only, so the bump belongs in the merge or deploy commit, not on the PR. Four `package.json` files carry the version.

## Related

- [[00 - Index|The Penthouse Self-Hosting]] for the host side.
- [[99 - Current Handoff]] for what is open right now.
- Next sub-projects from the spec: backup scaling (Codex), video pipeline (needs the GPU), chat archive, connection reliability.

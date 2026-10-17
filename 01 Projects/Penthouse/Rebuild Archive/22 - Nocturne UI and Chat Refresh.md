---
tags: [penthouse, nocturne, svelte, chat, media, responsive, working-tree]
created: 2026-06-15
publish: false
project: Penthouse
---

# Nocturne UI and Chat Refresh

## Status

Committed in `f6f6762` and released on 2026-06-15 with release head `24c1d41`.

Static validation and the production mobile Chromium smoke are clean. The complete Chromium, Firefox, and WebKit Playwright matrix still needs a fresh run after the latest fixes. The redeploy did not triage the remaining known UI problems.

## Responsive shell

- structural layout now uses a width-based `768px` boundary instead of pointer capability
- below `768px`: single-pane layout with a 48px mobile sidebar
- at or above `768px`: capped two-pane desktop shell
- the old bottom navigation was removed
- mobile content reserves space for the sidebar
- settings and appearance controls gained shrink and container-responsive behavior

Remaining browser concern:

- short-height sidebar behavior and the full viewport/pointer matrix still need final automated proof

## Mobile navigation and composer

- mobile navigation uses Messages, People, and Settings tabs
- tab labels expand transiently instead of remaining permanently wide
- mobile composer actions consolidate behind `More options`
- the menu exposes attachments, GIFs/stickers, and audio recording
- active E2E helpers now follow the mobile composer flow

## Message actions

- removed the inline action toolbar from message bubbles
- long-press opens an action overlay outside the bubble
- near-top messages place the overlay below the message
- Reply, React, Pin, Edit, and Delete remain available
- only one message overlay can remain open
- outside click and Escape dismiss overlays
- a keyboard trigger exposes the same actions without requiring touch

## Media presentation

- images, videos, GIFs, and stickers render outside text bubbles
- multiple images can render as a gallery
- media preserves sender alignment
- images and videos can open in a fullscreen dialog
- image/GIF viewing supports zoom and drag
- stickers expose a copy action
- voice notes render as compact audio tiles

Backend media hardening in the same working tree:

- stable `mediaId` values can refresh expired private signed URLs
- authorization still checks the sender owns the private media row
- failed upload processing removes partial files
- client upload failures use bounded `FILE_TOO_LARGE` or `UPLOAD_FAILED` responses
- internal filesystem, processor, and database details remain server-side

## Read receipts

- receipts use per-reader `seenThroughMessageId` markers
- REST-loaded messages seed markers after hard reload
- live `message.read` events update the marker store
- DMs show a compact receipt only on the newest covered own message
- groups and channels use reader avatar stacks

The first June Playwright pass found that the live socket handler did not update the marker store. That bug is fixed in the current tree.

## Presence notes

- presence notes can carry an optional expiry timestamp
- migration `031_presence_note_expires_at.sql` stores the expiry
- contracts include `noteExpiresAt`
- socket updates and sync snapshots omit expired notes
- web state clears local notes when their timer expires

## Appearance and profile styling

- expanded theme selection
- dark, light, and system modes
- configurable text scale
- compact, default, and comfortable UI density
- live appearance preview before applying
- restore-default action
- expanded profile-style controls
- Nocturne tokens are applied through the app shell

## Toasts and user feedback

- `svelte-sonner` now provides the toast layer
- chat-list mute failures and other user-facing errors can use the shared toast store

## Test adaptation

The active E2E work now accounts for:

- mobile composer menus
- long-press message actions
- exact profile-message selectors
- current mute preferences endpoint and context menu
- current receipt presentation
- fake Chromium media devices for audio testing

Old poll creation tests are skipped because the refreshed UI does not currently expose the `/poll` builder flow.

## Validation

Current:

- web typecheck: pass, 0 errors / 0 warnings
- API typecheck: pass
- web unit tests: 4/4 pass
- backend media handoff: 201 API tests passed
- production web build: pass
- production mobile Chromium smoke: pass with no console, page, or request failures
- public API health, auth config, CAPTCHA challenge, Socket.IO polling, manifest, and service worker checks: pass
- migration `031_presence_note_expires_at.sql` applied in production

Still required:

- rerun the full Chromium, Firefox, and WebKit Playwright suite
- resolve any remaining media-transition, audio, GIF/sticker, responsive, or selector failures
- complete manual authenticated chat proof for the refreshed shell, message actions, media viewer, receipts, and presence-note expiry

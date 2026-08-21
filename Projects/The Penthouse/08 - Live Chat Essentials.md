---
tags: [penthouse, realtime, typing, presence, guide]
created: 2026-03-08
published_to_garden: true
visibility: public
---

# Live Chat Essentials

## What was missing

Shared chat and message delivery were working, but the app didn't feel alive. Without typing indicators and presence state, it felt more like a request-response interface than a real conversation. This slice fixed that.

## Typing indicators

The mobile composer now emits a proper typing lifecycle:

- `typing.start` when someone starts entering a non-empty draft
- `typing.stop` after an idle timeout, on blur, on send, or on unmount

These only emit while the socket's actually connected, so stale typing events don't pile up during outages.

The active chat shows a typing indicator between the message list and the composer — above the composer, not inside the scroll container. That placement matters. The earlier version put it inside the scroll container, which meant it'd be in the DOM but below the viewport in any real chat with enough messages. It'd technically "show" and still not be visible.

Rules for the indicator:
- Only shows remote users, not yourself.
- Clears when the person stops typing.
- Also clears when a message from that sender arrives.
- Multiple typers collapse to a short summary.

## Presence

The backend was already emitting online/offline transitions, but a fresh client had no way to know who was already online before they connected. That gap got closed with a `presence.sync` event — it fires immediately on connect and sends the current online snapshot in one shot.

This matters because without it, presence would only become accurate after everyone else disconnected and reconnected.

Presence shows up in two low-noise places:
- Always-visible dots in the member directory
- Status in the member profile sheet

Rules:
- Gray dot means offline or no live presence yet.
- Green dot means online.
- When the socket drops, presence goes gray for everyone rather than showing stale state.

## Design decision

This slice deliberately avoided a full visual pass. Typing and presence change interaction structure. Attachment and media work was still ahead, so doing a full redesign here would have meant doing it twice. Functional realtime behavior first, minimal UI to expose it.

## What to test manually

With two clients open:
- Directory dots update without reopening the app.
- Profile sheet status updates without reopening.
- Typing indicator shows the correct display name.
- Typing clears on send and on idle timeout.
- Reconnect restores the presence snapshot.

## DM v1 note

The chat stack now supports 1:1 direct messages without a separate message system.

- DMs get created on first send, not when you open the picker.
- One DM thread per member pair.
- DMs live in the same chat list as everything else and reuse typing, read state, media, GIF, and moderation behavior.
- If someone gets removed or banned, the remaining member can still read the history but the DM becomes read-only.

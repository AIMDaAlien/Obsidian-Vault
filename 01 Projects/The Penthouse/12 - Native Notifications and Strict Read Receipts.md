---
tags: [penthouse, notifications, push, read-receipts, android]
created: 2026-03-08
published_to_garden: true
visibility: public
---

# Native Notifications and Strict Read Receipts

## What changed

Read receipts no longer advance just because a chat gets selected in app state. A message only counts as `seen` when the receiving user is:
- In the app
- On that chat screen
- At the live bottom of the message list

Backgrounding the app or turning the screen off no longer triggers `seen`.

## Why the old logic was wrong

The previous approach treated "selected chat exists in state" as equivalent to "the user actually saw the message." That's not the same thing. It'd produce false read receipts — a double checkmark showing up on messages that hadn't actually been looked at.

The new rule uses the same source of truth for both unread state and seen state: app is foregrounded, chat is the active screen, latest messages are visible.

## Android push

The app now has an FCM-backed push path plus the local-notification fallback:
- If Firebase is configured, the backend can send Android push even after the WebView stops receiving socket events.
- If the runtime is still alive enough to receive `message.new`, the local-notification path fires as a fast fallback.
- Foreground delivery still prefers the in-app toast path so it's not noisy while you're already using the app.

This is Android-first. iOS push is out of scope for this slice.

## What was verified on real Android hardware

- Background push works.
- Killed-app push works.
- Push tap-through opens the intended chat.
- Foreground in-app behavior is acceptable.

AOSP-only emulator images don't count as push-validation evidence for this Firebase path — those don't have Google Play services.

## Device-level notification controls in Settings

Users now have controls for:
- Push enabled or disabled for this specific device
- Message previews on or off
- Quiet hours with timezone-aware suppression
- Local in-app toast suppression

## DM mute

Direct messages now have a per-thread mute option on top of device-level controls:
- Muting a DM suppresses backend push for that thread for the muted member only.
- Also suppresses the in-app foreground toast and the local background fallback for that DM.
- Mute doesn't block delivery, unread counts, or chat-list updates.

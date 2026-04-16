---
tags: [penthouse, pwa, realtime, typing, presence, read-receipts, gif, muting]
created: 2026-04-09
published_to_garden: true
visibility: public
---

# Wave A — Live Chat on the PWA

## What this wave was about

The PWA baseline could send and receive messages. What it couldn't do was feel alive. A chat that doesn't show you when someone's typing, whether they're online, or whether they've actually seen your message feels like a bulletin board. Wave A closed that gap.

## Typing indicators

When someone's composing a reply, a small indicator appears in the header of that chat. It clears automatically when they send or stop typing, and it handles multiple simultaneous typers without turning into noise.

The indicator only shows while the realtime connection is healthy. If the socket drops, it goes silent rather than showing stale data.

## Presence

Every member in the chat list and member directory now has a small dot next to their avatar:
- Green = online right now
- No dot = offline or unknown

The cold-start problem (not knowing who was already online before you connected) is solved with a sync event that fires on connect and sends the current online snapshot in one shot.

Presence only shows as trustworthy while the socket is live. On disconnect, everyone goes gray rather than showing stale state.

## Read receipts

The app now shows whether messages have been seen:
- In a DM: "Seen 4:32 PM" appears below the last message the other person has read.
- In a group channel: small stacked avatars appear below messages to show who's seen them.

Read state updates in real time.

## GIF sending

A dedicated GIF button opens a picker backed by two providers: Giphy and Klipy. Trending GIFs load by default with a search bar for finding something specific.

Selected GIFs appear inline in the chat thread as animated images, not links. The picker closes after selection and the GIF gets sent with the same delivery guarantee as a text message.

## Chat muting

Long-pressing a conversation in the chat list opens a mute option. Muted chats:
- Suppress the unread badge.
- Show a small bell-off icon so you can see which chats are silenced.
- Can be unmuted any time.

Muting is local to your device and doesn't affect other members of the same channel.

## Design choices worth noting

All of these features went through the same optimistic delivery pattern already in place for text messages. Typing events are rate-limited on the client to one per second regardless of how fast someone types.

## What to test manually

- Open the same chat on two devices. Start typing on one, confirm the indicator appears on the other. Send, confirm it clears.
- Go offline on one device. Confirm presence goes gray. Reconnect. Confirm it updates.
- Send messages in a DM. Confirm "Seen" appears when the other person scrolls to that point.
- Mute a chat. Confirm the unread badge disappears. Receive a new message. Confirm it doesn't rebadge.
- Open the GIF picker, search for something, select one. Confirm it appears animated in the thread.

Next: [[17 - Wave B - Rich Messaging]]

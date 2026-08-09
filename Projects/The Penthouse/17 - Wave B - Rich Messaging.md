---
tags: [penthouse, pwa, reactions, reply, pins, delete]
created: 2026-04-09
published_to_garden: true
visibility: public
---

# Wave B — Rich Messaging

## What this wave was about

Wave A made the chat feel alive. Wave B made individual messages feel interactive. At the end of Wave A, a message was a one-way thing — you could send it and the other person could read it. That was it. Wave B adds reactions, reply/quote, delete, pins, and a UI refresh.

## Emoji reactions

Long-pressing any message opens a bottom sheet. The top row shows six quick-access emoji. Below that is an expandable grid of roughly eighty common emoji.

Tap an emoji and it attaches to the message as a small pill under the bubble — the emoji plus a count. Tap your own reaction a second time to remove it.

Reactions are live. Everyone in the chat sees counts update in real time. The backend enforces the obvious boundaries — you can't remove someone else's reaction, and non-members can't react.

## Reply / quote

Long-pressing a message and tapping Reply locks that message as the context for your next send. A preview bar appears above the composer. Send your message and it goes out with a visible quote block showing the original sender and a snippet of what they said.

The quote stays attached permanently, even if the original message gets deleted later. Dismissing the reply bar returns the composer to normal. If your send fails, the reply target gets restored.

## Message deletion

Tapping Delete from the long-press menu on your own message removes it immediately. The bubble is replaced with a gray "Message removed" placeholder. Deletion is optimistic — the placeholder appears instantly. You can only delete your own messages. Admins have a separate moderation path for other users' content.

## Pinned messages

Long-pressing a message reveals a Pin option. Pinned messages are useful for rules, announcements, or anything the room should be able to find quickly. Pin state is live — when anyone pins or unpins, everyone in the chat sees it immediately. Pins are tracked by the backend so they survive sessions and devices.

## Icon and UI refresh

This wave also replaced text characters being used as icons (← for back, 🔍 for search, etc.) with proper SVG icons from a consistent library:
- Back arrow
- Search glass
- Chevron for navigation
- Trash for delete
- Pin
- Reply arrow
- Paperclip (for future attachment use)
- Download
- Edit pencil
- Copy

Avatar displays across the member directory and profile pages were cleaned up to use the shared Avatar component consistently.

## Security boundaries tested in this wave

- Non-members of a chat can't react, pin, or delete messages in it.
- Members can't delete other members' messages.
- Members can't remove other members' reactions.
- Pinned message content snapshots survive deletion of the source message.

## What to test manually

- Long-press a message. Confirm the emoji row and action list appear.
- React with an emoji. Confirm it appears on both devices. Tap the same reaction — confirm it removes.
- Long-press and tap Reply. Confirm the reply bar appears. Send — confirm the quote appears in the thread.
- Delete one of your own messages. Confirm the tombstone appears on all devices.
- Pin a message. Confirm all devices see the pin. Unpin — confirm it clears.

Next: [[18 - Wave C - Community Features]]

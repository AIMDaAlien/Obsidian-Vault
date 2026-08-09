---
tags: [penthouse, pwa, polls, slash-commands, note-to-self]
created: 2026-04-09
published_to_garden: true
visibility: public
---

# Wave C — Community Features

## What this wave was about

Waves A and B brought the app up to feature parity with any competent messenger. Wave C starts pulling away from that baseline. These are features designed for small communities specifically — things that feel natural when you know everyone in the room.

## Slash commands

Typing `/` as the first character of a message triggers a command picker that floats above the composer. The picker filters as you type, so `/po` highlights the poll command before you've finished typing it.

Selecting a command (by tapping or pressing Enter) clears the composer and performs the action. Pressing Escape or typing something that doesn't match dismisses the picker and lets the text through as a normal message.

## Polls

Typing `/poll` opens a poll builder as a slide-up sheet. You can:
- Write a question (up to 200 characters)
- Add 2 to 4 answer options
- Optionally set an expiry — never, 24 hours, or one week

Polls appear inline in the chat thread as a card, not a regular message bubble. Tapping an option votes. After voting, the card expands to show percentage bars and vote counts.

Votes are live — tap an option and everyone sees the bars update in real time. When a poll expires, options lock and the final results stay visible as read-only bars so the history is preserved.

## Note to Self

Every member automatically has a personal private thread that only they can see and write in. It pins to the top of the chat list with a bookmark icon, labeled "Saved."

This works exactly like Telegram's Saved Messages. It's useful for dropping links, writing notes between sessions, or keeping something visible without sending it to anyone.

The thread behaves identically to any other chat on the inside — same composer, same message history. It just happens to be an audience of one.

## Design choices

**Polls are an inline card, not a separate screen.** Voting happens directly in the thread without navigating away. Conversation context stays visible while you vote.

**The slash command picker only shows commands that actually exist.** No "coming soon" placeholders. If you type something that doesn't match, the picker disappears and your text goes through as a message.

**Note to Self is not a special feature — it's just a chat.** The implementation is a self-DM created once on first login. The only special behavior is pinning to the top of the list. Everything else is identical to any other thread, so there's nothing new to learn.

## What to test manually

- Type `/` in the composer. Confirm the command picker appears.
- Type `/po`. Confirm it filters to the poll command.
- Press Escape. Confirm the picker dismisses and text stays.
- Select the poll command, create a poll with 3 options and a 24-hour expiry.
- Confirm the poll card appears. Have a second user vote on a different option. Confirm both clients see the updated bars.
- Open the chat list. Confirm "Saved" is pinned above everything else.
- Tap it, write a note, navigate away and back. Confirm the note is there.

## What comes after this

The remaining staged Wave B items:
1. **Image attachments** — attach and send images directly from the chat composer
2. **Markdown rendering** — bold, italic, code, and links render inside message bubbles
3. **Message editing** — correct a message after sending without deleting and resending

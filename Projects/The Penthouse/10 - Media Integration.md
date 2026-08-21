---
tags: [penthouse, media, uploads, gif, hardening]
created: 2026-03-08
published_to_garden: true
visibility: public
---

# Media Integration

## What got added

Message types now support `text`, `image`, `video`, `gif`, and `file`. The mobile composer can:
- Upload images
- Upload videos
- Upload text-style files (`.txt`, `.md`, `.json`, `.csv`, `.log`, `.yaml`, `.xml`)
- Open a GIF picker backed by Giphy and Klipy

Sent messages keep the existing optimistic delivery flow and queue/retry behavior after upload.

## Important design choices

- Uploads go through the API, not directly to third-party storage. This keeps the privacy model consistent.
- Attachment message metadata stores relative upload URLs so different clients resolve media against their own API base.
- GIF provider requests are proxied through the API using locally configured provider keys.
- Upload failure surfaces immediately to the sender. Queued retry only kicks in after the file's actually been uploaded and the message payload exists.

## Known limits at the time

- No attachment caption flow yet — attachment messages use the filename or GIF title as their content label.
- Failed raw uploads don't get persisted to the offline queue. The user retries by picking the file again.
- Avatar upload is still separate from chat attachment flow.

## Klipy inline playback fix

After manual Android testing, Klipy needed a follow-up fix.

What was wrong: the chat-thread inline renderer was using the preview asset for Klipy image-mode GIFs, so the modal could animate while the inline chat tile stayed static.

What's true now:
- Inline chat rendering uses the animated asset URL for GIF playback.
- Preview assets stay for the picker and fallback behavior.
- Inline and modal playback are aligned.

## Local media controls

Media behavior now has device-local settings for:
- Automatic GIF animation
- Reduced data mode

Reduced data mode favors still and lighter previews in both the picker and inline chat rendering. Fullscreen media still opens the real asset even when inline rendering is reduced.

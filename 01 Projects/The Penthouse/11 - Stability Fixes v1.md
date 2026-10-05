---
tags: [penthouse, stability, fixes, android]
created: 2026-03-08
published_to_garden: true
visibility: public
---

# Stability Fixes v1

## Goal

Lock down the rough edges that made local Android testing feel unreliable even when the backend was mostly correct. This was about making the dev loop trustworthy before expanding features.

## What changed

### 1. Session persistence

Mobile auth state now uses a proper storage adapter instead of raw component-level localStorage reads. Native Android uses `@capacitor/preferences`. Web keeps localStorage as the fallback. Existing session keys get migrated once into native storage on mobile. Boot is now ordered:

1. Load stored user and tokens.
2. Refresh if needed before showing the auth screen.
3. Only clear the local session if the refresh actually fails.

### 2. Test database safety

Integration test helpers now refuse to run against non-test database names. This prevents accidentally wiping dev users and chats when running the API integration suite locally.

### 3. Chat layout containment

The shell now uses `100dvh` with overflow containment. The message list is the only scrollable region. The header and composer stay pinned. Width handling for action buttons and the composer was tightened for Android device widths.

### 4. Media rendering

Uploaded image and video metadata now carries width and height when the client can derive it. Chat media bubbles are bounded and proportional instead of acting like oversized file rows. GIF captions got removed from the in-chat rendering path. File attachments still keep filename cards. Image and GIF bubbles now open a fullscreen modal viewer with zoom.

### 5. Typing correctness on Android

Typing state is no longer shut off when IME composition is active. That was the main reason Android soft-keyboard input flickered or failed to show the typing indicator. Typing now stays active until: 5 seconds of inactivity, send, blur, draft cleared, or disconnect.

### 6. GIF provider hardening

Klipy parsing now supports the current `file.url` response shape. Known parse failures return provider errors instead of a misleading "No GIFs found."

## Practical lessons from this pass

- If local testing keeps "forgetting" users, check test database isolation before blaming the mobile session layer.
- Android WebView is less forgiving than desktop web for keyboard composition and storage assumptions.
- Media support gets much easier to reason about once width and height are treated as first-class metadata.
- A fake empty GIF state is worse than an explicit provider error because it sends debugging in the wrong direction.

## Residual issues after this pass (as of 2026-03-12)

- Right-edge clipping was still unresolved on narrow Android layouts.
- Notification logic existed but still needed a UX hardening pass.

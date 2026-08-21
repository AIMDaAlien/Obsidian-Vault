---
tags: [penthouse, pwa, sveltekit, rebuild, website-rebuild]
created: 2026-04-09
published_to_garden: true
visibility: public
---

# PWA Rebuild

## Why this happened

The original app was a native Android APK distributed manually — download, install, done. That worked for a small closed group, but every update meant users had to reinstall. Distribution needed a separate channel. The dev loop required Android Studio.

A Progressive Web App solves all of that at once:
- Users open a URL in their browser and the app installs itself.
- Updates deploy silently — next open is always the latest version.
- Works on any device with a modern browser, not just Android.

The decision was to keep the existing backend completely intact and rebuild only the frontend as a PWA. Same server, same database, same socket architecture — new face.

## What changed on the frontend

The old frontend was Vue 3 with Capacitor (a tool for wrapping web code in a native Android shell). The new one is SvelteKit.

Why SvelteKit:
- Ships less JavaScript to the browser than comparable frameworks.
- Clean component syntax that reads close to plain HTML/CSS.
- First-class PWA support through a plugin.
- Strong TypeScript integration so mistakes get caught before they reach users.

| Layer | Before (Vue + Capacitor) | After (SvelteKit PWA) |
|---|---|---|
| Framework | Vue 3 + Vite | SvelteKit 2.x |
| Bundle | Native APK (~10MB) | Web bundle (~200KB) |
| Routing | Vue Router | File-based |
| State | Pinia | Nanostores + Svelte 5 runes |
| HTTP client | axios | Native fetch |
| Realtime | socket.io-client | socket.io-client (unchanged) |
| PWA support | Partial (Capacitor) | Full (@vite-pwa/sveltekit) |
| Offline | Limited | Service Worker |

## What didn't change

- The Fastify backend and PostgreSQL are identical.
- The shared `@penthouse/contracts` package is identical.
- Socket.IO event structure is identical.
- Visual identity — dark theme, periwinkle accent, Ubuntu/JetBrains Mono fonts.

## What the baseline covered before features were added

Before any feature waves:
- Login and registration — invite-only account creation, password-based login, automatic token refresh.
- Chat list — all conversations and DMs in one list.
- Opening a chat and reading messages — scroll through history, load older messages on demand.
- Sending a text message — with optimistic display, message appears instantly while delivery confirms in the background.
- Basic profile — display name and avatar.
- PWA install prompt — browser prompts to add the app to home screen.
- Connection status indicator.

## How the codebase is organized

Frontend lives in `apps/web/`. Backend and shared contracts are separate. Both sides import from `packages/contracts`, so if a data shape changes anywhere, both sides catch the mismatch at build time.

## What this version deliberately left out

Several things were excluded to keep the baseline shippable and testable quickly:
- GIF sending — moved to Wave A.
- Typing indicators and presence — moved to Wave A.
- Read receipts — moved to Wave A.
- Push notifications — scheduled for a later wave.
- Admin tools — backend routes exist, UI comes later.

Next: [[16 - Wave A - Live Chat on the PWA]]

---
tags: [penthouse, v5, redesign, theme, design-system]
created: 2026-05-14
published_to_garden: true
last_published: '2026-07-25T21:05:10.185673'
---

# V5 Redesign

Complete visual redesign of The Penthouse frontend. Replaced the legacy dark-only palette with a proper design system: 5 themes × 2 modes, inline token binding, and a consistent OKLCH-based color strategy.

## Why V5 Exists

v4 shipped with a functional but visually generic frontend. The color system was ad-hoc (`--color-*` variables, no light mode, hardcoded dark surfaces). V5 fixes this with a disciplined token strategy and hand-tuned palettes per theme.

## Theme System

### Architecture

| Concern | Before | After |
|---------|--------|-------|
| Token source | CSS `:global()` blocks | Inline `style:` binding from `appearanceStore.tokens` |
| Mode support | Dark only | Dark + Light, with `system` preference collapse |
| Themes | 1 (implicit dark) | 5: periwinkle, sage, slate, plum, charcoal |
| Palette format | Hex/HSL | OKLCH (hand-tuned, not algorithmic) |
| Storage key | `penthouse-theme` | `penthouse-appearance` (JSON: `{themeId, mode}`) |
| FOUC prevention | `data-theme` attribute | `data-theme` + `data-mode` + inline styles |

### Key Files

| File | Purpose |
|------|---------|
| `apps/web/src/lib/themes.ts` | 5 `ThemeDef` objects with dark/light OKLCH palettes |
| `apps/web/src/lib/stores/appearance.svelte.ts` | Reactive store: `themeId`, `mode`, `$derived(tokens)` |
| `apps/web/src/lib/utils/theme.ts` | FOUC hydration: `initAppearance()`, `applyAppearance()` |
| `apps/web/src/routes/+layout.svelte` | 24 inline `style:--p-*` bindings on `.app-shell` |
| `apps/web/src/app.html` | FOUC script reads `penthouse-appearance` from `localStorage` |

### Token List

Each theme exposes: `accent`, `accentSoft`, `accentEdge`, `bg`, `surface`, `surface2`, `text`, `text2`, `muted`, `secondary`, `line`, `line2`, `success`, `warning`, `error`.

Light mode rule: surfaces must be darker than `bg` (explicit tokens, no `color-mix(... var(--p-text) ...%)`).

## Component Token Swap

All P0 components migrated from `--color-*` to `--p-*`:

- `MessageBubble`, `Avatar`, `ChatListPane`, `ChatListItem`
- `DesktopNav`, `BottomNav`, `DesktopShell`, `MessageComposer`, `TypingIndicator`
- `PushSettings`, `AudioPlayer`, `AudioRecorder`, `EmojiPicker`
- `EmojiEmoteAutocomplete`, `StickerPicker`, `EmotePicker`, `UnifiedPicker`
- `ReplyBar`, `ChannelList`, `PinBanner`, `MarkdownText`, `ReadReceipts`, `ReactionPill`
- Routes: `auth`, `chat/[id]`, `settings`, `users`, `+page` (root)

## Settings & Profile Style

### New Components

| Component | Purpose |
|-----------|---------|
| `AppearanceSettings.svelte` | Theme grid (5 swatches) + mode toggle (Dark/Light cards) |
| `ThemePicker.svelte` | 5-theme swatch grid, reads/writes `appearanceStore` |
| `ProfileStyleSettings.svelte` | 3-row picker: editorial / vogue / wallpaper |
| `ProfileCard.svelte` | Switchable profile rendering per `profileStyle` |

### Profile Card Variants

- **Editorial**: banner above, pfp overlapping, name below
- **Vogue**: large display name overlay on banner, big pfp
- **Wallpaper**: full-bleed banner, floating identity card mid-height

### Users Page

Rewrote `/users` with split layout:
- **Desktop**: roster left (300px), focus pane right (ProfileCard)
- **Mobile**: list ↔ detail navigation
- `ProfileCard` wired with `onMessage` → starts DM via `chats.createDM()`

## Chat Layout

Restructured `MessageBubble.svelte` to match V5 prototype invariants:

| Invariant | Implementation |
|-----------|---------------|
| Clustering | `showAvatar = i === last \|\| next.senderId !== current.senderId` |
| Time placement | Absolutely positioned below pfp on last message in cluster |
| Reactions | `.reactions-row` sibling of `.row`, NOT inside `.bub-col` flex |
| Sender name | Only shown on `firstInCluster` for non-own messages |
| Gap | `msg-cluster-gap` margin (14px) on first message of cluster |

Actions, menu, and emoji picker moved inside `.bubble` with absolute positioning (top-right on hover).

## Wallpaper Purge

Deleted the entire wallpaper system (per-chat/global wallpaper with URL/color/opacity):

- **Frontend**: `wallpapers.svelte.ts`, `wallpapers.ts`, UI removed from chat/settings
- **Backend**: `routes/wallpapers.ts`, `features/wallpapers/schema.ts`
- **Contracts**: `UserWallpaperSchema`, `CreateWallpaperRequestSchema`, `ListWallpapersResponseSchema`
- **Migration**: `0006_profile_style.sql` drops `user_wallpapers` table

The `"wallpaper"` **profile style** (how a user's card renders) is unrelated and was kept.

## Backend Schema Updates

Migration `0006_profile_style.sql` also adds:

```sql
ALTER TABLE "users" ADD COLUMN "profile_style" text DEFAULT 'editorial' NOT NULL;
ALTER TABLE "users" ADD COLUMN "banner_url" text;
```

Updated backend functions:
- `toAuthUser` → emits `profileStyle`
- `toMeResponse` → emits `profileStyle` + `bannerUrl`
- `toMemberDetail` → emits `profileStyle` + `bannerUrl`
- `PATCH /api/v1/auth/me` → handles `profileStyle` updates

## Avatar Texture

Fallback avatars (`HSL` generated) now have a fractal noise overlay:
- Dark mode: `opacity: 0.45`
- Light mode: `opacity: 0.30` (via `:global([data-mode="light"])`)

## Build Status

- `apps/web`: `svelte-check` 0 errors, `npm run build` passes
- `packages/contracts`: `tsc --noEmit` passes
- `services/api`: `tsc --noEmit` passes
- Commit: `e5417c0` on `main`

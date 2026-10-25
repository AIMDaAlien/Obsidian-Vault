---
type: benchmark-log
topic: Penthouse Remake
publish: true
created: 2026-09-26
tags: [omarchy, penthouse]
machine: bigrig
title: "Penthouse Remake"
---
# Penthouse Remake


## 2026-09-25 21:52
**Done:** Phase 1 slice 1 of the Svelte 5 frontend remake (qwen27b sandbox repo): SvelteKit scaffold, design-system port (5 themes × dark/light), monolith shell + mobile letter rail, 6 routes, 90-shot screenshot matrix.
**Findings:** 21/21 DOM gate assertions (token matrix, frame/rail structure, settings persistence); format/lint/typecheck/build all green. Gotcha: monolith expand animation skews width assertions mid-flight — set reducedMotion:'reduce' in test contexts. vite preview binds IPv6 ::1 only — use localhost, not 127.0.0.1.
**Recommendations:** Aim visual review of phase1-shell-2026-09-25 vs baseline-2026-09-23; primary agent to brief the service-layer (api/auth/socket) port as the next slice.

## 2026-09-26 11:00
**Done:** Runtime-verified Phases 2-4 of the Svelte 5 remake end-to-end in the sandbox (login, DM consent flow, message round-trip, 6 routes, theme switch) — 18/18 Playwright checks green, 109/109 unit tests, typecheck 0 errors.
**Findings:** Message text rendered invisible in every conversation: `MessageBubble` wrapped content in `{#await Promise.resolve(message.content)}`, which stays stuck in the pending branch under Svelte 5.54 (the await effect re-runs and discards the settled promise each invalidation). Fixed by removing the wrapper. Sandbox gotchas: CORS_ORIGIN must list the preview origin (:4173); `DISABLE_RATE_LIMIT` only accepts the literal string `true`, not `1`.
**Recommendations:** Hand to primary: `MessageBubble` renders raw user content via `{@html}` (stored XSS); an unused, sanitized `MarkdownText.svelte` already exists and should replace it.

## 2026-09-26 11:51
**Done:** Closed the stored-XSS seam in the web app's MessageBubble — replaced raw `{@html}` rendering of message content with the MarkdownText component (snarkdown + DOMPurify allowlist), passed emotes through, and reset default `<p>` margins so bubbles stay tight.
**Findings:** Runtime probe (11/11) — HTML payloads sent through the real API arrived as inert text; no onerror/script execution, no live img/script in bubbles, while `**bold**` markdown and server-sanitized `<b>` fragments still render as HTML. Full gate green: typecheck 0 errors, 109/109 unit tests, build clean, 18/18 runtime checks.
**Recommendations:** The server also sanitizes content (defense in depth confirmed), so client and server now share the same allowlist philosophy. Next: give MarkdownText its own unit test to lock the sanitize behavior.

## 2026-09-26 12:40
**Done:** Added unit-test coverage for the MarkdownText sanitize path (stored-XSS seam). Extracted escapeHtml/replaceEmotes/renderMarkdown from the Svelte component into src/lib/utils/markdown.ts and pinned 9 cases in a co-located vitest file (script/img-onerror stripping, emote rendering, URL quote-escaping, markdown formatting).
**Findings:** Test count 109 → 118, full gate green (typecheck 0 errors, build clean, lint 0 errors). The extraction surfaced a real closure bug: renderMarkdown stopped forwarding emotes to replaceEmotes — the new tests caught it before merge. DOMPurify keeps a bare <img src="x"> (img is allowlisted) and strips only the onerror handler, so tests pin the safety property, not tag absence.
**Recommendations:** Component render coverage (Svelte component tests) is deliberately out of scope; revisit if MarkdownText grows.

## 2026-09-26 14:34
**Done:** Set up two concurrent logged-in browser windows (test.alice / test.bob) for dual-account testing against the local dev stack (web :5173, API :3000, Postgres).
**Findings:** Accounts registered via POST /api/v1/auth/register with captchaToken "dev" (dev skips Altcha). Gotcha: Playwright page.fill() does NOT stick on Svelte 5 bind:value inputs (value reverts to empty, form validation blocks submit with "invalid form control not focusable"). Fix: click the field then page.keyboard.type() char-by-char. Sized windows to ~1000x1120 CSS px to fit Hyprland half-tiles on the 2560x1440@1.25 monitor without squishing.
**Recommendations:** For any future UI automation of this app, use keyboard.type not fill.

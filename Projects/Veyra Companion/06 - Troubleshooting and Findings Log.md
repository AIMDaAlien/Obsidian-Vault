---
project: Veyra Companion
type: troubleshooting-log
updated: 2026-08-15
---

# Troubleshooting and Findings Log

## 2026-08-15 — Fish S2 Pro Worker Runtime Fixes

### Findings

- Passing the anchor path directly to Fish failed because the installed `mlx_audio` adapter expects a loaded MLX audio array, not a file path.
- `ThreadingHTTPServer` failed synthesis with a thread-local MLX stream error; a single-threaded `HTTPServer` keeps model load and generation on one thread.

### Fix

- Warm loads the model and each selected anchor into memory at the model sample rate.
- Synthesis randomizes the MLX seed, generates the whole cleaned line in one pass, resamples to 24 kHz mono PCM16, and normalizes below clipping.
- The worker rejects unknown voice IDs and fails closed on missing anchors or synthesis errors.

### Decision

- Speech is enabled by default but only when CoreAudio reports an eligible external output.
- MacBook Pro Speakers and all other built-in routes are hard-blocked before playback.
- Mixed-language lines stay whole; the anchor follows Arabic → Japanese → English priority.

## 2026-08-11 — Missing Portrait on L01N8A

### Symptom

- The 687×800 Field Notes composer rendered correctly on the right side of L01N8A.
- The intended 593×800 portrait area was a plain beige field; Veyra was not physically visible.
- AppKit's internal PDF rendering showed Veyra, but the real WindowServer surface and Aim's screenshots did not.

### Evidence

- `veyracontent.png` and the packaged copy had the same SHA-256: `04d77814f5dca5512720b60996ad240c6b6246770d1e6cdbfd76c033e8f958b7`.
- The asset is a valid 896×1195 sRGB PNG with real 8-bit alpha.
- LLDB confirmed the live sprite view held the correct visible image, frame, opacity, and layer contents.
- AppKit `dataWithPDFInsideRect` included the portrait. WindowServer compositing omitted it.

### Discarded Fixes

These changed the AppKit render path but did not restore the physical portrait:

1. Forced view/window display and layout.
2. Put the `CGImage` directly on the sprite layer.
3. Premultiplied the bitmap before assigning layer contents.
4. Drew the image into the parent stage view instead of `NSImageView`.
5. Made the full 1280×800 window opaque.
6. Removed the beige stage fill and returned the full window to transparency.

The first five still produced a blank physical portrait. The sixth exposed the desktop but the portrait remained missing. This established that another image conversion was not the right fix.

### Confirmed Root Cause and Fix

The dedicated display mixed a transparent portrait stage and opaque composer inside one full-screen AppKit window. The image existed in AppKit but was lost at the WindowServer composition boundary.

Commit `452aa14` (`Split portrait and composer windows`) replaced the mixed window with:

- one transparent borderless 593×800 portrait window;
- one opaque borderless 687×800 composer window;
- both windows excluded from visual-context capture;
- unchanged portable-mode behavior.

WindowServer then reported the two exact windows. Aim physically confirmed: **Veyra is back and the desktop background is visible behind her.**

## 2026-08-11 — OCR Failure and Visual Context

### Native OCR Failure

The former Vision OCR loop analyzed full display frames frequently, used fast recognition without language correction, flattened unsorted observations, and stored every changed result. This produced noisy repeated text and exposed stale garbage in Mind.

### Baidu Unlimited-OCR Evaluation

- Tested the community Apple-MLX conversion of Baidu's 3B Unlimited-OCR model against Aim's real Veyra Mind screenshot.
- The official document-parsing prompt detected only the window title and Refresh control.
- A general extraction prompt hallucinated numeric text and repeated corrupt OCR rows.
- The model was rejected for live desktop awareness. It remains downloaded but unloaded.

### Adopted Visual Path

Commit `8fa06a5` (`Replace desktop OCR with local visual context`) removed live OCR and reused the already-loaded Bonsai vision model:

- ScreenCaptureKit excludes Veyra windows and the dedicated display.
- A 2560×1440 frame is reduced to 768×432, an approximately 91% pixel reduction.
- JPEG quality is 55%; test frames were roughly 40–60 KB.
- Only the latest in-memory frame is attached, and only when Aim sends a message.
- Screenshots are not written to Veyra's database or research queries.
- Screenshot text is explicitly treated as untrusted evidence, never instructions.

Bonsai correctly described the real composer screenshot at both 960 and 768 pixels. End-to-end proof through a real installed-app conversation remains open.

## 2026-08-11 — Grey Visual Context Control

### Finding

The grey **Enable Visual Context** button did not mean capture had failed. It was disabled by design after `CGPreflightScreenCaptureAccess()` returned true in the running app.

Evidence:

- System Settings showed `Veyra Companion.app` enabled.
- LLDB evaluated the running app's preflight result as `YES`.
- The activity database recorded: `Visual context started; Veyra windows and the dedicated display are excluded. Screenshots are not saved.`
- A direct command-line diagnostic reported false. That mismatch is consistent with macOS attributing the direct launch through Terminal rather than the active LaunchServices app. Running-app state, System Settings, and stream activity are the reliable checks.

Commit `3d7680c` (`Make the dedicated portrait stage transparent`) also changed the control to an always-enabled **Manage Visual Context** action when permission is already active.

## Verification Snapshot

- 32 Swift tests pass.
- Release build passes.
- Strict code-sign verification passes for `~/Applications/Veyra Companion.app`.
- Screen Recording is enabled for the signed Veyra bundle.
- Visual-context stream startup is recorded.
- Dedicated WindowServer geometry is exactly 593×800 plus 687×800.
- Aim physically approved portrait visibility and transparent background behavior.

## Remaining Gates

- Send a real installed-app message that depends on current screen content and verify Bonsai's answer.
- Continue manual review of Mind depth, pat feel, initiative wording, streaming, topic switching, and research handoff.

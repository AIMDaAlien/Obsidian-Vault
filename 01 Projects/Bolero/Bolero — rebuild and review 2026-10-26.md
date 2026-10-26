---
type: note
category: Omarchy & Desktop
tags: [bolero, clop, wayland, hyprland, qt, qml, review, omarchy]
created: 2026-10-26
updated: 2026-10-26
publish: true
machine: bigrig
title: "Bolero — rebuild and review 2026-10-26"
---
# Bolero — rebuild and review 2026-10-26

**Category:** [[Omarchy & Desktop]] · **Vault:** [[Vault Map]] · **Showcase:** [[Bolero]]

**In short:** in one day Bolero, the Linux version of Clop, got the macOS app's look and behaviour, a way to drag files that only exist as text in a terminal, and two reviews whose findings were all fixed. The code is in `~/Work/bolero` on `master` (merge `6d30dca`, 65 commits). 565 automated tests and 37 live desktop checks pass.

It was called Clop Linux during the build and became **Bolero** the same day; see the last row of the decisions table.

## Timeline

1. **Reading the Mac app.** The original is open source (GPL-3), so its SwiftUI source was read with a reverse-engineering skill and written up as a design spec: sizes, colours, materials, timings, hotkeys, menu order, each with a `File.swift:LINE` reference. Frames from its product videos covered what code alone doesn't show (the hover grid, the drop zone, the downscale slider). The spec lives in the repo as `docs/MAC_UI.md`. The port is a fresh implementation of that description, with no code or artwork taken from the original.
2. **Desktop plumbing.** The floating corner became a wlr-layer-shell surface through KDE's `layer-shell-qt`, loaded into the pip PySide6 process (see Lessons). Hyprland blur was turned on (globally, by choice) with a layer rule limited to the frosted pixels.
3. **The interface.**
   - Result cards: a 196 pt continuous-corner card, a frosted band over the picture, a format bar, a hover grid of six actions, in-card sliders.
   - A stack that auto-hides.
   - The drop zone, with its red/orange glow, spinning target and preset tiles.
   - A sidebar Settings window.
   - The tray menu in the Mac order.
4. **Review 1, of the original port.** It found that the old drag-out and drop-zone reveal never worked, and that several optimisations could degrade files in place. Twelve engine findings were fixed test-first.
5. **Draggable paths.** Terminals and agents print paths, and you can't drag text into a browser. Copied paths, the primary selection (`Super+Alt+D`) and `bolero drag FILE…` now show the file as a card. A line in the global agent instructions tells coding agents to use `bolero drag` when handing over media.
6. **Review 2, end to end.**
   - Four reviewers read the Python layer, the overlay QML, the Settings window and the engine.
   - A live harness drove the running app over its socket on the real desktop: clipboard saved and restored, scratch files only, a hard kill mid-encode.
   - Everything confirmed was fixed (the fixes are listed below), and the full live set was re-run on the final build.
7. **Merged** `mac-ui` into `master`.

## Decisions and why

| Decision | Why |
|---|---|
| Overlay as a layer-shell surface, plain-window fallback | Never tiled or focused, anchored by the compositor, and blur can be limited to opaque pixels (`ignore_alpha`); the fallback keeps working without the library |
| Blur turned on globally in Hyprland | Real glass needs compositor blur; the user chose global over Bolero-only |
| Drop zone appears when a drag reaches a thin corner strip | Wayland tells a client about a drag only when it reaches one of its surfaces; the strip sits in the window gap, so it blocks nothing |
| Preset tiles after a one-second pause, not on Control | A Wayland drop target never sees the keyboard during a drag |
| Card shortcuts after a click, not on hover | An exclusive keyboard grab on hover swallowed typing elsewhere; macOS's hover keys never do that |
| Aggressive hotkey on `Super+Alt+A` | The original's `Ctrl+Shift+C/A` would take Copy away from every terminal |
| Watched folders count from when they were added (inode change time) | Adding `~/Pictures` re-encoded the whole library; a per-file baseline would hit the index cap, and a ctime cutoff needs no records while still catching files moved in later |
| 10-bit video becomes HEVC Main 10 (VP9 profile 2 in WebM) | H.264 High 10 plays almost nowhere; 8-bit would lose depth and HDR |
| Mute and speed change write a copy | They are deliberate edits, like crop; only a plain re-encode that comes out smaller replaces a file |
| Encoders capped at 4 threads, nice 10 | x265 is 3–4× slower than x264, and sustained full load is what has cut this PC's power |
| Named Bolero, described as "Clop for Linux" | Clop is the original's name, and the original is still in use on the Mac; a name of its own keeps the two apart, and the tagline says what it is. A bolero is another straw hat, like the *clop* the original is named after, and it was already the app's icon |

## What the end-to-end review found (fixed)

**Files:**
- Adding a watched folder re-encoded what was already in it.
- Undoing a conversion could delete the only copy.
- 10-bit video came out unplayable.
- Alpha video lost its transparency.
- 24-bit and float WAV were cut to 16-bit.
- CMYK JPEGs got RGB pixels with a CMYK profile.
- MKV cover art turned into a video track.
- Chaptered MP4s gained a junk data track on every pass.
- The journal cap could drop retained backups.
- One crash timing leaked a backup forever.
- A failed journal write could lose the undo.
- One unreadable scan made the watcher redo everything.

**Crashes:** the encoder kept running after the app died and left a scratch file. Encoders now die with the app (within 0.75 s) and recovery removes the scratch file.

**Privacy:**
- Re-compressing a clipboard result put the full-size original back on the clipboard.
- Thumbnails of clipboard screenshots outlived the screenshots. They now go after 30 minutes.

**The overlay:**
- Parts of settled cards let clicks through.
- Cards jumped on insert.
- Menus could act on the wrong card.
- Shortcuts bypassed the menu's rules.
- Dismissed cards came back.
- A card could be removed in the middle of its own drag-out.
- A drop on the preset tiles could go to the wrong place.

**Settings:**
- A focused text field could write into the wrong preset or resurrect a deleted one.
- Renaming the default preset left a duplicate.
- Preset tiles pointed at deleted presets.
- Disk errors vanished silently, and memory diverged from disk.

**Paths:**
- A 64 KB copied blob took 23 s of CPU to scan; it now takes milliseconds.
- Paths after `=`, in lists or after an apostrophe were missed.
- Relative paths failed under tmux.

## Lessons

- **A system Qt plugin can join a pip PySide6 process.** It loads safely only when the system Qt is the same release as the wheel's, and only after the platform plugin has loaded the wheel's Qt libraries; the dynamic linker then resolves the plugin's Qt dependencies by soname to the copies already loaded. Its QML module goes on a private import path; adding all of `/usr/lib/qt6/qml` would shadow the wheel's QtQuick.
- **QML self-binding.** `theme: theme` inside a component that has a `theme` property binds the property to itself. Give the id a different name.
- **Layer reuse in `MultiEffect`.** A shadow effect widens its source's layer to fit the blur, so a layered shape shared between a shadow and a mask shrinks the mask. Give each effect its own source.
- **`MultiEffect` masks are thresholds.** Threshold 0.5 with spread 1.0 gives a mask proportional to alpha, which a gradient fade needs. The default lets everything through.
- **Headless GPU renders of QML.** The offscreen platform here has no GPU, so shader effects come out blank. A `QQuickView` that is never shown, grabbed under the Wayland platform, renders with OpenGL and puts nothing on screen. Size the root explicitly, or anything anchored to it collapses to zero.
- **Process trees under tmux.** A pane's shell is a child of the tmux server, not of the terminal window. `tmux list-clients -F '#{client_pid} #{pane_pid}'` maps the window's client to its pane.
- **Children that die with you.** `PR_SET_PDEATHSIG` follows the *thread* that forked, and `preexec_fn` is unsafe once threads exist. A tiny wrapper that sets it, checks it wasn't orphaned in the meantime, and then `exec`s the real command does both safely.
- **Test-harness trap.** `wl-copy` leaves a child serving the clipboard, and that child inherits stdout. Detach it, or a test pipeline never sees EOF.
- **Regex over clipboard text.** A path regex run over a long string without spaces backtracks quadratically. Tokenise first.

## Open items

- `chmod` on a file that was already in a watched folder makes it count as new (the ctime rule).
- Lossless audio inside video containers is re-encoded to AAC in place.
- WAV isn't converted to MP3.
- Dolby Vision and HDR10 mastering metadata survival is unverified.
- Real-mouse drag-out and two Settings shortcuts still need a hand check.
- Not yet ported: the Mac crop window and the compact list.

![[bolero-20261026/settings-preset-zones.png]]

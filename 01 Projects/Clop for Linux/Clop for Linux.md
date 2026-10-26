---
type: project-showcase
topic: Clop for Linux
category: Omarchy & Desktop
created: 2026-09-20
updated: 2026-10-26
tags: [clop, linux, wayland, hyprland, qt, desktop-app, showcase]
publish: true
machine: bigrig
title: "Clop for Linux"
---
# Clop for Linux

**Category:** [[Omarchy & Desktop]] · **Vault:** [[Vault Map]] · **Build log:** [[Clop for Linux — rebuild and review 2026-10-26]]

## In plain words

Screenshots and screen recordings are much bigger than they need to be. A screenshot of a web page can easily be a few megabytes, which is why it takes a moment to send in a chat, and why an email full of them gets heavy.

**Clop makes those files small, automatically, the moment you copy them.** You take a screenshot as usual, and by the time you paste it somewhere it is already a fraction of the size, looking the same. You don't press anything and you don't have to think about it.

When it shrinks something, a small card slides into the corner of the screen showing the picture and how much smaller it got (say *8.7MB → 340KB*). You can ignore it and it disappears on its own, or you can use it:

- **drag it** straight into a chat, an email or an upload box,
- **make it smaller still** (half the size, a quarter…),
- **turn it into another format** (JPEG, WebP, AVIF, PNG for pictures; MP4, WebM, GIF for videos),
- or **undo**, which puts the original back exactly as it was.

You can also drop any picture, video, song or PDF onto a little frosted box that appears in the corner of the screen when you drag something there, and Clop shrinks it in place.

There is one more trick, made for people who work in a terminal or with AI coding assistants. Those print file names as text, and text can't be dragged into a browser. **Clop turns a file name into a card you can drag**: copy the name (or just highlight it and press a shortcut) and the file appears in the corner, ready to drop anywhere. An assistant can do it for you, too.

Clop began as a Mac app by The Low Tech Guys ([lowtechguys.com/clop](https://lowtechguys.com/clop)). This is a separate, from-scratch version for Linux, made to look and behave as close to the Mac one as Linux allows. Everything happens on the computer itself: no files are uploaded anywhere.

![[clop-linux-20261026/floating-corner.png]]
*The corner of the screen while Clop is working: three results stacked above the drop zone. The middle card is hovered, which brings up its controls.*

## What it does

| | |
|---|---|
| **Copied pictures** | shrunk the moment they are copied, and the smaller version is put back on the clipboard, ready to paste |
| **Result cards** | the picture itself, old and new size, a bar of formats to convert to; hover for close, undo, compression, a stronger squeeze, copy and show-in-folder |
| **Drag and drop** | every card drags out as a real file; a handle drags all of them at once |
| **Drop zone** | appears when something is dragged to the screen corner; rest on it for a second to get four one-drop presets (strongest, to WebP, half size, lossless) |
| **File names to files** | copy a file name, or select it and press `Super+Alt+D`, or run `clop drag FILE` |
| **Watched folders** | anything saved into a chosen folder is shrunk; what was already there is left alone |
| **Undo** | every change keeps the original until it is no longer needed for undo |
| **Settings** | a sidebar window laid out like the Mac app's |

![[clop-linux-20261026/card-states.png]]
*A result card's states: at rest, hovered (the six actions), working ("Scaling to…" with a stop button), the size slider, already as small as it gets, and a failure.*

## For the curious: how it's built

- **Python and Qt Quick (PySide6)**, with ffmpeg, Pillow and PyMuPDF doing the actual shrinking.
- **Wayland and Hyprland, the frosted-glass look and all.** The corner area is a *layer-shell* surface: a piece of the desktop itself rather than a window, so it never steals focus, never shows up in the window list and stays put. Hyprland blurs only the frosted parts of it, and clicks pass straight through everything else.
- **A faithful copy, not a copied one.** The Mac app is open source (GPL-3), so its sizes, colours, timings and behaviour were read from its source and screenshots and written down (in the repo, `docs/MAC_UI.md`). The Linux app was then written from those notes, with no code or artwork taken from it. Apple's fonts and icons can't be shipped, so close open substitutes stand in: Inter-style Adwaita Sans, the rounded Nunito, JetBrains Mono, and hand-drawn line icons.
- **Kind to the machine it runs on.** Video encoding uses at most four threads at lower priority, so a long recording never ties up every core for minutes. On a PC that has lost power under sustained load, that matters.

![[clop-linux-20261026/settings-general.png]]

## For the curious: how it was checked

The app went through two reviews before this release:

1. **A code review of the original port.** It found that some of the advertised features didn't actually work, and that a few optimisations could make files *worse* (16-bit images cut to 8-bit, encrypted PDFs losing their lock, video losing audio tracks). Those were fixed first.
2. **An end-to-end review** of the finished build. Four separate reviewers read the app, the screen overlay, the settings window and the media engine, and a live test run drove the real app on the desktop. More than seventy problems were found and fixed. A few examples:
   - Adding a folder to watch would have re-encoded everything already in it. Now only new files are touched.
   - After a crash, the video encoder kept running and left a half-written file next to the original.
   - Re-compressing a copied screenshot put the full-size original back on the clipboard.
   - Undoing a conversion could delete the only copy of a file.

Where it stands now: **565 automated tests and 37 live checks pass.** The live checks run on the actual desktop against the running app, with the clipboard saved and restored around them. They cover shrinking and byte-exact undo, videos with several audio tracks and subtitles, encrypted PDFs, iPhone HEIC photos, the clipboard, watched folders across restarts, and killing the app in the middle of an encode. At rest the app uses no measurable CPU.

![[clop-linux-20261026/settings-clipboard.png]]

## Not there yet

- The Mac app's crop window, and the compact list it switches to above five results.
- Writing HEIC, JPEG XL, HEVC and AV1 from the format bar (shown, greyed out).
- WAV files aren't converted to MP3 the way the Mac app does by default, so WAV recordings don't shrink.
- Dragging a card out with a real mouse, and two settings-window shortcuts, are still to be checked by hand.

## Related

- [[Clop for Linux — rebuild and review 2026-10-26]]: the build log, decisions and lessons.
- [[Omarchy & Desktop]]: the desktop it lives on.
- [[Agents & Tooling]]: how coding agents hand files over with `clop drag`.

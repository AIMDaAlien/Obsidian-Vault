---
type: ops
topic: Omarchy desktop
updated: 2026-09-23
category: Omarchy & Desktop
tags: [omarchy, debloat, power, update-policy, linux]
publish: true
created: 2026-09-23
machine: bigrig
title: "Omarchy Trim, Debloat & Idle Policy"
---
# Omarchy Trim, Debloat & Idle Policy

**Category:** [[Omarchy & Desktop]] · **Vault:** [[Vault Map]]

Stripping Omarchy 4.0.3 down to a minimal local-LLM dev box (2026-09-16 → 09-18).

## Baseline and keep-list

183 explicit packages, 0 AUR. Kept: Hyprland + Quickshell, foot, tmux, lazygit/lazydocker, btop, mise, yay, docker+buildx+compose, ufw, llama-cpp + ggml-vulkan, Hermes + opencode swarm.
Bloat found: kdenlive, obs-studio, gpu-screen-recorder, libreoffice-fresh, evince, mpv, pinta, xournalpp, chromium, localsend, moonlight-qt, imv, imagemagick, tesseract, yt-dlp, cliamp, aether; plumbing: cups, bluez+bt-agent, avahi/nss-mdns, fcitx5, gvfs-mtp/smb/nfs, bolt, wpa_supplicant, qemu-user-static-binfmt, sushi.
User keep-list: obsidian, localsend, imv, aether, tesseract+OCR, libreoffice. All drivers + the llama stack stay. Chromium replaced by **Helium**, pllus **Zen**. Browsers: `helium-browser-bin` 0.17.0.1, `zen-browser-bin` 1.22.1b (AUR).

## Scripts

- `~/trim-phase1.sh` (services + browsers) — **silently failed on package removals**; superseded by
- `~/trim-phase2.sh` — re-runnable, only removes what is actually installed. (Still to be run by the user.)
- Services disabled: `cups cups.socket cups.path avahi-daemon avahi-daemon.socket bluetooth systemd-oomd systemd-oomd.socket wpa_supplicant` (bluez package kept, service off = one command to restore).
- Boot 1 m 16 s = 8 s firmware + 12 s Limine + 50 s kernel (initramfs + nvidia-dkms) — little to trim.

## RAM scare explained

"30/30 GiB" was **buff/cache from llama-server mmapping the ~15 GB model file** (17 G reclaimable), not a leak. Real anon RAM 0.8–8 G, agent swarm ≈ 900 MB, swap had already dropped 13 G → 1.5 G.

## Idle, screensaver, power

- Screensaver timeout in `~/.config/omarchy/shell.json` **150 → 999999** (effectively off); lock stays 5 min; system never auto-suspends so llama-server keeps serving.
- "Stay awake" is an **independent state file** `~/.local/state/omarchy/indicators/stay-awake` (sets `idleEnabled = false`) — it does NOT block an explicit `systemctl suspend`.
- The bench auto-suspend watcher: stop llama-server → wait for VRAM to drain → `systemctl suspend` (user session has `allow_active=yes`, so no password).
- Fans already silent at idle (CPU fan 0 RPM, 45 °C); case/CPU fans are BIOS-controlled (`fancontrol` not running) — see [[Fan Control (MSI Z690-A)]].

## Smooth scrolling

- Browsers animate discrete wheel steps with a mouse. Helium: `~/.config/helium-browser-flags.conf` + `helium://flags` smooth scrolling. Zen: `about:config` `general.smoothScroll` + `mousewheel.default.delta_multiplier_y`.
- Terminals do **no** animated scrolling (the only one that does is `rio`, too young for daily use). foot set to `multiplier=2.0`.

## Update discipline (Arch rules)

- Never `pacman -S <pkg>` alone — partial upgrades break Arch. Use **`yay <pkg>`** which syncs everything.
- Kernel/driver/Omarchy updates need `omarchy update` ~monthly, and **never while llama-server is mid-benchmark**.
- Daily auto-update timer installed (~11:30, skips missed days when the box is off, `paccache` cleanup).

## Related

[[Browser Debloat & Benchmark 2026-09-19]] · [[Omarchy Plugins & Shell Widgets]] · [[Rig Hardware & Display]] · [[llama.cpp Upgrade Roadmap]]

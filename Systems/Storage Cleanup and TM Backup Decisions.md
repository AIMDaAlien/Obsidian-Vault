---
tags: [reliability, local-ai]
---
# Storage Cleanup & TM Backup Decisions

> 2026-08-12. Mac storage freed 41G -> 83G free. Decisions made during cleanup.

## Deleted (re-downloadable / junk)

- Draw Things app models - 41G (com.liuliu.draw-things container, app uninstalled but models orphaned). Re-downloadable in-app.
- Windows 11 Parallels VM - 37G. Parallels itself kept. VM was suspended, deleted via prlctl.
- Android SDK - 10G (system-images + emulator + tools). Android Studio itself kept. Re-download via SDK Manager.
- java_error_in_studio.hprof - 979M. Java crash dump, pure junk.
- Ladybird browser build - 756M (nested /Users/aim/Users/aim/ladybird).
- App caches: ms-playwright (1.3G), dotslash (258M, partially SIP-blocked), ms-playwright-go, Homebrew caches, Arc, Brave.
- Corrupt TM sparsebundle on Unraid - 992G (empty APFS inside, orphaned bands, no recoverable data).

## Kept (real data / active)

- Docker Desktop VM - 23G (searxng container running).
- Parallels app itself.
- Android Studio app.
- flux2 models (53G) - project data, kept but EXCLUDED from backup.

## TM exclusions added (12, all re-downloadable)

- ~/.cache/huggingface (113G)
- ~/.lmstudio (38G)
- ~/.local/share/btl3-compact (7.8G)
- ~/.ollama
- ~/Library/Caches
- ~/.hermes
- ~/Downloads
- Documents/flux2-dev-edit (33G)
- Documents/flux2-klein-9b-mlx (20G)
- Documents/language-engine (5.6G)
- ~/Library/Android
- ~/exo

## TM destination (Unraid) fixes

- Share volume limit was 3G (shareVolsizelimit=3145728 KB) - made SMB report disk full. Removed.
- fruit:time machine max size = 0 (unlimited, reports real free space).
- smb-shares.conf was empty (share never exported) - rewrote with fruit support.
- Old corrupt bundle deleted; TM destination needs re-register (sudo):
  - sudo tmutil removedestination 7FC40668-1426-4DAC-99F5-E3775B001B28
  - sudo tmutil setdestination -a "smb://guest@192.168.0.120/TimeMachine"

## Prune script

- ~/.hermes/scripts/tm-prune.sh - age (5wk) + size (1.2TB) prune, not yet wired to cron.

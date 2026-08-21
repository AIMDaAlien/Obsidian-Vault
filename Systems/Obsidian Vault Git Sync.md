---
tags: [reliability]
system: Obsidian Notes Vault
status: Repaired and syncing
updated: 2026-08-11
---

# Obsidian Vault Git Sync

## 2026-08-11 Recovery

Obsidian could commit locally but could not pull or push because the local repository had been reinitialized on 2026-08-09. Its new root commit shared no history with `origin/main`. The auto-sync log repeatedly reported:

```text
fatal: refusing to merge unrelated histories
```

At diagnosis, local `main` was 3 commits ahead and 235 behind. A dry-run push also failed as non-fast-forward.

Recovery:

- Preserved the local state on `backup/pre-reconcile-20260811-0923`.
- Merged `origin/main` with `--allow-unrelated-histories`, keeping the five newer local note versions where both sides differed.
- Confirmed no remote files were deleted and all remote-only notes were restored.
- Pushed merge commit `0b8ba23`.
- Updated `origin` to the canonical remote: `https://github.com/AIMDaAlien/Obsidian-Vault.git`.
- Pulled the generated manifest commit `66baef8` and reran `.github/scripts/vault-auto-sync.sh` successfully.

Healthy state: local `main` and `origin/main` match, and the scheduled auto-sync can pull before pushing normally.

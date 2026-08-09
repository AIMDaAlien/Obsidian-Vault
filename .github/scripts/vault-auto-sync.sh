#!/bin/bash
# Auto-sync vault to GitHub when obsidian-git isn't running (Obsidian closed).
# Runs via launchd every 15 min; no-op when the working tree is clean.
set -euo pipefail

VAULT="/Users/aim/Documents/Obsidian Notes Vault"
LOG=/tmp/vault-sync.log

cd "$VAULT"

# Pull first so a stale local clone never blocks the push
git fetch origin main -q
if ! git diff --quiet HEAD origin/main 2>/dev/null; then
    git pull --no-rebase origin main >>"$LOG" 2>&1 || {
        echo "$(date '+%F %T') pull failed (merge conflict?)" >>"$LOG"
        exit 1
    }
fi

if [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -q -m "vault backup (auto): $(date '+%Y-%m-%d %H:%M')"
    git push -q origin main >>"$LOG" 2>&1
    echo "$(date '+%F %T') synced: $(git log -1 --format=%h)" >>"$LOG"
fi

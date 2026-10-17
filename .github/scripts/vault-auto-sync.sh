#!/bin/bash
# Auto-sync vault to GitHub when obsidian-git isn't running (Obsidian closed).
# Runs via launchd every 15 min; no-op when the working tree is clean.
set -euo pipefail

VAULT="$HOME/Documents/Notes/Obsidian Notes Vault"
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
    # The gate scans tracked files, so it must run after staging new notes
    python3 .github/scripts/privacy-gate.py >>"$LOG" 2>&1 || {
        git reset -q
        echo "$(date '+%F %T') privacy gate failed, not committing" >>"$LOG"
        exit 1
    }
    git commit -q -m "vault backup (auto): $(date '+%Y-%m-%d %H:%M')"
fi

# Push whenever local commits are ahead, so a previously failed push is retried
if [ "$(git rev-list --count origin/main..HEAD)" -ne 0 ]; then
    git push -q origin main >>"$LOG" 2>&1 || {
        echo "$(date '+%F %T') push failed, will retry next run" >>"$LOG"
        exit 1
    }
    echo "$(date '+%F %T') synced: $(git log -1 --format=%h)" >>"$LOG"
fi

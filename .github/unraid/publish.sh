#!/usr/bin/env bash
# Cron wrapper: runs the vault publisher container under a lock, with logging.
# A held lock means another run is active; the 45-minute hard timeout below
# bounds every run, so no stale-lock handling is needed.
set -euo pipefail

VAULT=/mnt/cache/vault
LOCK=$VAULT/.publish.lock
LOG_DIR=$VAULT/logs
LOG=$LOG_DIR/publish-$(date +%F).log
NOTIFY=/usr/local/emhttp/webGui/scripts/notify
DEPLOY_KEY=/root/.ssh/vault-deploy
KNOWN_HOSTS=/root/.ssh/known_hosts
TERMS=/mnt/cache/appdata/vault-publisher/vault-privacy-terms

mkdir -p "$LOG_DIR"
find "$LOG_DIR" -name 'publish-*.log' -mtime +30 -delete

log() { echo "$(date '+%F %T') $*" >> "$LOG"; }
notify() { [ -x "$NOTIFY" ] && "$NOTIFY" -i warning -s "vault publish" -d "$1" || true; }

exec 9>"$LOCK"
if ! flock -n 9; then
    log "another run active"
    exit 0
fi

log "run start"
# A missing bind source would make docker create a directory in its place.
for f in "$DEPLOY_KEY" "$KNOWN_HOSTS" "$TERMS"; do
    if [ ! -f "$f" ]; then
        log "required file missing: $f"
        notify "required file missing: $f"
        exit 1
    fi
done

key=$(sed -n 's/.*<apikey>\(.*\)<\/apikey>.*/\1/p' /mnt/cache/appdata/syncthing/config.xml 2>/dev/null | head -1 || true)
if [ -z "$key" ]; then
    log "syncthing api key not found in config.xml"
fi
export SYNCTHING_API_KEY="$key"  # passed by name so the value is not in the process list

rc=0
timeout -k 2m 45m docker run --rm --init --name vault-publisher --pull=never --network host \
    -v /mnt/cache/vault/sources:/sources:ro \
    -v /mnt/cache/vault:/vault \
    -v /mnt/cache/vault/sources:/vault/sources:ro \
    -v "$DEPLOY_KEY":/root/.ssh/id_ed25519:ro \
    -v "$KNOWN_HOSTS":/root/.ssh/known_hosts:ro \
    -v "$TERMS":/root/.vault-privacy-terms:ro \
    -e GIT_AUTHOR_NAME=vault-publisher -e GIT_AUTHOR_EMAIL=vault-publisher@localhost \
    -e GIT_COMMITTER_NAME=vault-publisher -e GIT_COMMITTER_EMAIL=vault-publisher@localhost \
    -e SYNCTHING_API_KEY \
    -e TZ=America/New_York \
    vault-publisher:latest --config /vault/compose.yml --curation /vault/curation.yml \
    --report-dir /vault --require-terms /root/.vault-privacy-terms "$@" >> "$LOG" 2>&1 || rc=$?

if [ "$rc" -eq 124 ] || [ "$rc" -eq 137 ]; then
    if [ "$rc" -eq 124 ]; then
        why="timed out after 45 minutes"
    else
        why="killed (timeout or OOM)"
    fi
    log "run $why (rc=$rc)"
    docker kill vault-publisher >/dev/null 2>&1 || true
    notify "run $why"
    exit "$rc"
fi
log "run end rc=$rc"

if [ "$rc" -ne 0 ]; then
    notify "$(tail -n 3 "$LOG")"
fi
exit "$rc"

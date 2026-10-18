#!/usr/bin/env bash
# Cron wrapper: runs the vault publisher container under a lock, with logging.
set -euo pipefail

VAULT=/mnt/cache/vault
LOCK=$VAULT/.publish.lock
LOG_DIR=$VAULT/logs
LOG=$LOG_DIR/publish-$(date +%F).log

mkdir -p "$LOG_DIR"
find "$LOG_DIR" -name 'publish-*.log' -mtime +30 -delete

log() { echo "$(date '+%F %T') $*" >> "$LOG"; }

# Break a stale lock file (older than 3600 seconds).
if [ -e "$LOCK" ] && [ -n "$(find "$LOCK" -mmin +60 2>/dev/null)" ]; then
    log "breaking stale lock"
    rm -f "$LOCK"
fi

exec 9>"$LOCK"
if ! flock -n 9; then
    log "another run active"
    exit 0
fi

log "run start"
key=$(sed -n 's/.*<apikey>\(.*\)<\/apikey>.*/\1/p' /mnt/cache/appdata/syncthing/config.xml 2>/dev/null | head -1 || true)
if [ -z "$key" ]; then
    log "syncthing api key not found in config.xml"
fi
rc=0
docker run --rm --network host \
    -v /mnt/cache/vault/sources:/sources:ro \
    -v /mnt/cache/vault:/vault \
    -v /root/.ssh/vault-deploy:/root/.ssh/id_ed25519:ro \
    -v /root/.ssh/known_hosts:/root/.ssh/known_hosts:ro \
    -e GIT_AUTHOR_NAME=vault-publisher -e GIT_AUTHOR_EMAIL=vault-publisher@localhost \
    -e GIT_COMMITTER_NAME=vault-publisher -e GIT_COMMITTER_EMAIL=vault-publisher@localhost \
    -e SYNCTHING_API_KEY="$key" \
    vault-publisher:latest --config /vault/compose.yml --curation /vault/curation.yml \
    --report-dir /vault "$@" >> "$LOG" 2>&1 || rc=$?
log "run end rc=$rc"

if [ "$rc" -ne 0 ] && [ -x /usr/local/emhttp/webGui/scripts/notify ]; then
    /usr/local/emhttp/webGui/scripts/notify -i warning -s "vault publish" -d "$(tail -n 3 "$LOG")" || true
fi
exit "$rc"

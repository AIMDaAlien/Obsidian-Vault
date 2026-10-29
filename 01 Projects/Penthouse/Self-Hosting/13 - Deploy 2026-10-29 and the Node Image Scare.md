---
tags: [self-hosting, unraid, docker, deploy, penthouse, reliability, caddy]
created: 2026-10-29
updated: 2026-10-29
publish: true
project: Penthouse
summary: "The 4.5.0-alpha.1 deploy, two stops on the way (a Node image that could no longer start a fresh process, and host-only Caddy routes), and what changed on the host."
---

# Deploy 2026-10-29 and the Node Image Scare

## In plain words

Before today's update went out, the deploy checks found the app's container marked "unhealthy" by Docker, even though the site itself was working. The cause turned out to be odd: the base image the app ran on had gone bad in a way where any brand-new Node process started inside it crashed instantly, while the long-running server process, started days earlier, kept going. Docker's health check starts a new process every few seconds, so it failed every time. Rebuilding the app on a fresh Node image fixed it, and that rebuild was part of the update anyway.

The second surprise was that the web server config on the host had two small extras the repo did not know about. They were kept rather than overwritten.

Users saw a brief blip while the container network was rebuilt. Nothing was lost; a database backup was taken first.

## Stop 1: the API container was "unhealthy" while the site was fine

- Docker had flagged the API container unhealthy since 2026-10-28 23:41 UTC. The server process (running since 2026-10-25) was fine: public `/api/v1/health` returned 200 the whole time.
- The health probe spawns a fresh `node -e "fetch(...)"` inside the container, and in that image every fresh Node process died at V8 startup with `Fatal error in , line 0 / unreachable code` (exit 133, `trap int3` in dmesg). `node --version` worked; `node -e 1` crashed; `--jitless` crashed; `--no-node-snapshot` worked.
- It was the image, not the host: `node:22-alpine` (22.23.4), the official `node:22.23.2-alpine` (a September rebuild) and `node:22-bookworm-slim` all ran fine. The old API image was built 2026-09-14 on the July build of 22.23.2. Why it turned bad on the 28th is not pinned down; the two btrfs checksum errors on the Docker image file that day were in a Playwright Firefox file in the CI runner's layer, not in the API image.
- Consequence: the old container could not be restarted on that image. The deploy rebuilt from `node:22-alpine`, so the deploy was also the fix. Gate added: build and prove the new image (`docker run --rm --entrypoint node <image> -e 1`) before stopping the old API. Fallback if a rollback ever needs the old image: `NODE_OPTIONS=--no-node-snapshot` on the api service.
- Lesson: "unhealthy" can mean the probe, not the service. Check the public endpoint and the probe command by hand before acting.

## Stop 2: host-only Caddy routes

The host Caddyfile had two blocks `main` lacks: a handler for a small metrics JSON the portfolio site reads (CORS and cache headers; a cron job rewrites the file every 5 minutes) and the MetalBench static site. The handoff says stop if the host has edits main lacks. Ruling: merge, don't replace. Main's Caddyfile (strict tunnel trust, both `header_up` lines, CSP-Report-Only) plus the two blocks verbatim. The old file was backed up on the host first. The repo copy still needs those blocks.

## What changed on the host

- The `current` symlink moved to the new release directory; the previous one was kept for rollback.
- A compressed pre-deploy database dump was taken (gzip-tested, not restore-tested).
- Migrations 045 to 048 applied once.
- Compose network rebuilt with fixed addresses for Caddy, the API, Postgres and the tunnel.
- API env: `TRUST_PROXY` set to Caddy's address only.
- Daily log expiry installed with a 13-day cutoff, covering active and rotated logs.
- Deleted-media DM cleanup ran: 0 rows (nothing to remove).
- New API image runs Node 22.23.4; all three containers healthy afterwards.
- Smoke fixtures: two throwaway accounts and one private group; the accounts were removed the same day (they remain listed as `removed`).

## Still open

- Add the two Caddy blocks to the repo's production Caddyfile.
- `PUBLIC_SOCKET_ORIGIN` unset warning at compose time.
- MetalBench refused connections during the checks; separate project.

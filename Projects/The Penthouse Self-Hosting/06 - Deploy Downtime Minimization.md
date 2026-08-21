---
tags: [self-hosting, deployment, downtime, docker, guide, hardening]
created: 2026-02-18
published_to_garden: true
visibility: public
---

# Deploy Downtime Minimization (Compose + Caddy)

## Why downtime happens at all

On a single-host setup, updating the app means the container gets recreated, TCP connections reset, and WebSocket clients disconnect briefly. For a chat app, even a few seconds is noticeable.

## What I implemented

### 1. Recreate only the app container, keep Caddy running

The deploy workflow:
- Builds the new app image while the old container's still running
- Recreates only the app container with `--no-deps --force-recreate`
- Reloads Caddy config without restarting Caddy itself

This keeps the TLS termination layer running continuously. Downtime shrinks to just the app container restart window.

### 2. Graceful shutdown in the app

On `SIGTERM` or `SIGINT` the app:
- Marks health as `shutting_down` so the load balancer can stop routing
- Stops accepting new HTTP connections
- Closes Socket.IO
- After a grace period, force-closes anything still lingering

This prevents hard kills mid-request.

### 3. Give the container time to drain

In `docker-compose.yml`:
- `stop_grace_period: 25s`
- `init: true` so the app receives signals properly

### 4. Caddy retry window

Caddy's `reverse_proxy` directive has a short retry window configured — try for up to ~5 seconds, retry every ~250ms. A request that hits during a restart waits briefly and then succeeds rather than getting a hard failure.

## What this doesn't cover (true zero downtime)

Blue/green deployment requires running two app instances simultaneously. That's safe with PostgreSQL but requires a different compose setup. It's not worth it at this scale — the graceful shutdown approach keeps restarts to a few seconds.

## Operational expectation

With this setup, a deploy should look like:
- A brief blip (a couple of seconds) for WebSocket connections
- A small number of HTTP requests might wait rather than fail outright

That's acceptable for a small-scale self-hosted app without adding a lot of complexity.

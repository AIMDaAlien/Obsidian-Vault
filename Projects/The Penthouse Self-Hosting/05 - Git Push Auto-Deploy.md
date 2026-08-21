---
tags: [self-hosting, ci-cd, github-actions, deployment, guide, website-rebuild, hardening]
created: 2026-02-18
published_to_garden: true
visibility: public
---

# Git Push Auto-Deploy (GitHub Actions Self-Hosted Runner on TrueNAS)

## Goal

Deploy on `git push` without SSHing into the server every time.

## How it works

TrueNAS runs a self-hosted GitHub Actions runner. The workflow fires on push to `main`, pulls the latest code, and rebuilds and restarts the compose stack.

The runner is labeled `[self-hosted, truenas, penthouse]` so it only picks up jobs from this repo's workflow.

## What the workflow does

1. `git fetch`
2. `git reset --hard origin/main`
3. Normalize data directory permissions
4. Build and recreate only the app container (not Caddy)
5. Health check inside the container

## Verifying it works

The easiest proof: bump a visible value in `/api/health` (like a version string), push to main, wait for the workflow to finish, and confirm the new value comes back from the live URL.

## Things that'll still break it

- Runner not starting on boot
- Runner machine offline
- Disk full (build fails silently)
- `.env` missing required variables (Compose fails to start)
- Wrong permissions on the data mount

## Tips

- Keep `docker compose ps` and `/api/health` checks in the workflow itself so failures are obvious in the Actions log.
- Use a `concurrency` block in the workflow so you can't accidentally stack two deploys.

```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: true
```

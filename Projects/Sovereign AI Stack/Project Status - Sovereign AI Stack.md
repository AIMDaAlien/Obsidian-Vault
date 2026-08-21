---
tags: [hardening, local-ai]
---
# Project Status - Sovereign AI Stack

> **Last Updated:** 2026-02-10
> **Overall Status:** 🟡 In Progress

## Quick Context

Building a fully local AI assistant: Discord → OpenClaw (TrueNAS) → Ollama (Windows). Two vision-capable Qwen3-VL models (8B GPU fast + 32B CPU smart). Privacy-first, zero cloud AI dependencies.

## Phase Checklist

| Phase | Status | Summary |
|-------|--------|---------|
| 1. Windows Ollama | ✅ Done | Both models pulled, LAN-exposed, firewall rule set |
| 2. Discord Bot | ✅ Done | Bot created, token saved, invited to server |
| 3. OpenClaw Gateway | 🔴 Blocked | Container runs but onboarding/auth token not configured |
| 4. Discord Pairing | ⏳ Waiting | Depends on Phase 3 |
| 5. SearXNG Integration | ⏳ Waiting | SearXNG already running, just needs OpenClaw config |
| 6. Vision Testing | ⏳ Waiting | Depends on Phase 3+4 |
| 7. Memory/Personality | ⏳ Waiting | SOUL.md + MEMORY.md after core works |
| 8. Tailscale (optional) | ⏳ Future | Zero-cloud access from anywhere |

## Current Blocker

**OpenClaw gateway won't fully start.** Two issues:

1. **Auth token missing:** Logs say `Gateway auth is set to token, but no token is configured`. Need to either set `OPENCLAW_GATEWAY_TOKEN` env var or run onboarding wizard.

2. **Can't exec into container:** `docker exec -it openclaw-gateway openclaw onboard` fails — `openclaw` binary not in container PATH. Container is in restart loop due to missing token, so `bash` exec also fails.

**Most likely fix:** Add `OPENCLAW_GATEWAY_TOKEN=<random-string>` to docker-compose.yml environment, or use the official `docker-setup.sh` script from the OpenClaw repo.

## Recent Changes

- 2026-02-10: Created project structure, pulled models, configured networking
- 2026-02-10: Debugged Ollama LAN binding (env var required restart to take effect)
- 2026-02-10: Removed invalid `channels` block from openclaw.json (dmPolicy/allowFrom not valid keys)
- 2026-02-10: Identified gateway auth token as final blocker

## Next Actions

1. Resolve OpenClaw auth token → get web UI loading at :18789
2. Complete onboarding / Discord pairing
3. Send first test message through Discord → Ollama
4. Test vision pipeline with screenshot
5. Hook up SearXNG for web search

## Navigation

- Back to [[Project Overview - Sovereign AI Stack]]
- See also: [[Setup Tutorial - Sovereign AI Stack]]
- See also: [[Architecture Guide - Sovereign AI Stack]]

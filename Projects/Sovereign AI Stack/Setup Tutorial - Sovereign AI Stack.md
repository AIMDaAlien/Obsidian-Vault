# Setup Tutorial - Sovereign AI Stack

> A step-by-step guide to building a private AI assistant using Ollama, OpenClaw, and Discord. Written from real experience — includes every gotcha encountered during setup.

## Prerequisites

**Hardware needed:**
- A machine with a dedicated NVIDIA GPU (for fast inference) and plenty of RAM (for larger CPU models). This guide uses an i5-12600KF + RTX 3060 12GB + 64GB RAM.
- A server or second machine for the OpenClaw gateway (can be very lightweight — ~256MB RAM). This guide uses TrueNAS Scale.
- Both machines on the same LAN.

**Software needed:**
- Ollama (Windows/Mac/Linux) — https://ollama.com/download
- Docker + Docker Compose on the gateway machine
- A Discord account and bot (free)
- Optional: SearXNG for self-hosted web search

**Accounts needed:**
- Discord Developer account (free) for bot creation

---

## Phase 1: Ollama on the Inference Machine (Windows)

### 1.1 Install Ollama

Download from https://ollama.com/download and run the installer. Verify:

```powershell
ollama --version
```

### 1.2 Pull Models

```powershell
# Fast daily driver — fits in 12GB VRAM
ollama pull qwen3-vl:8b

# Smart heavy model — runs on CPU/RAM (~20GB download)
ollama pull qwen3-vl:32b

# Verify both installed
ollama list
```

The 8B model goes on GPU (~5.7GB VRAM at Q4), the 32B runs on CPU/RAM (~21GB). Ollama handles GPU/CPU routing automatically.

### 1.3 Test Vision

```powershell
ollama run qwen3-vl:8b "Describe what you see" < path/to/image.jpg
```

> **Note:** The `--images` flag was deprecated. Use input redirection or the API for vision testing.

### 1.4 Configure LAN Access

By default, Ollama only listens on localhost. To let other machines send requests:

```powershell
# Set system-level environment variables (run PowerShell as Admin)
[System.Environment]::SetEnvironmentVariable("OLLAMA_HOST", "0.0.0.0:11434", "Machine")
[System.Environment]::SetEnvironmentVariable("OLLAMA_KEEP_ALIVE", "24h", "Machine")
```

`OLLAMA_HOST=0.0.0.0` binds to all network interfaces (not just localhost).
`OLLAMA_KEEP_ALIVE=24h` prevents Ollama from unloading models between requests.

### 1.5 Add Firewall Rule

```powershell
# Allow inbound connections on port 11434 from your LAN subnet only
New-NetFirewallRule -DisplayName "Ollama LAN" -Direction Inbound -Protocol TCP -LocalPort 11434 -Action Allow -RemoteAddress 192.168.0.0/24
```

Adjust `192.168.0.0/24` to match your actual subnet.

### 1.6 Restart Ollama

**Critical:** Environment variables only take effect after restart. Quit Ollama from the system tray (right-click icon → Quit), then relaunch from Start Menu.

### 1.7 Verify

```powershell
# Confirm it's listening on all interfaces
netstat -an | findstr 11434
```

You must see `0.0.0.0:11434 LISTENING`. If you see `127.0.0.1:11434`, the env var didn't take — see Troubleshooting.

```powershell
# Test the API
curl http://<YOUR-WINDOWS-IP>:11434/v1/models
```

Should return JSON listing your models.

---

## Phase 1 Troubleshooting

### `netstat` shows nothing for port 11434
Ollama isn't running. Check `Get-Process ollama*` in PowerShell. Relaunch from Start Menu.

### `netstat` shows `127.0.0.1:11434` instead of `0.0.0.0:11434`
The `OLLAMA_HOST` env var didn't stick. Verify with:
```powershell
[System.Environment]::GetEnvironmentVariable("OLLAMA_HOST", "Machine")
```
Should return `0.0.0.0:11434`. If not, re-run the SetEnvironmentVariable command as Admin and restart Ollama again.

### Other machines can't connect despite correct netstat
Windows Firewall is blocking it. Verify the rule exists:
```powershell
Get-NetFirewallRule -DisplayName "Ollama LAN"
```
If missing, re-create it. Also check: is the remote machine on the same subnet? Firewall rule restricts to `192.168.0.0/24`.

### `scp` not found in PowerShell
PowerShell doesn't have `scp` by default. Use `scp.exe` (explicit extension) if OpenSSH is installed, or transfer files by other means (SSH into target and use `nano` to paste content).

---

## Phase 2: Discord Bot Setup

### 2.1 Create the Bot

1. Go to https://discord.com/developers/applications
2. Click **New Application** → name it (e.g., "Sovereign AI")
3. Go to **Bot** tab → **Reset Token** → copy and save the token securely
4. Enable under **Privileged Gateway Intents:**
   - Message Content Intent
   - Server Members Intent
5. Go to **OAuth2 → URL Generator:**
   - Scopes: `bot`
   - Bot Permissions: `Send Messages`, `Read Message History`, `Attach Files`
6. Copy generated URL → open it → invite bot to your server

### 2.2 Get Your User ID

1. Discord Settings → Advanced → enable **Developer Mode**
2. Right-click your username → **Copy User ID**

Save both the bot token and user ID — you'll need them for OpenClaw configuration.

---

## Phase 3: OpenClaw Gateway on TrueNAS

### 3.1 Verify Prerequisites

SSH into your TrueNAS server and confirm:

```bash
docker --version          # Need Docker installed
docker compose version    # Need Compose v2+
free -h                   # Check available RAM
curl http://<WINDOWS-IP>:11434/v1/models  # Confirm Ollama reachable
```

### 3.2 Create Directory Structure

```bash
mkdir -p /mnt/<YOUR-POOL>/apps/openclaw/{config,workspace}
cd /mnt/<YOUR-POOL>/apps/openclaw
```

### 3.3 Create docker-compose.yml

```yaml
services:
  openclaw:
    image: ghcr.io/openclaw/openclaw:latest
    container_name: openclaw-gateway
    ports:
      - "18789:18789"
    volumes:
      - ./config:/home/node/.openclaw
      - ./workspace:/home/node/workspace
    environment:
      - OLLAMA_API_KEY=ollama-local
      - DISCORD_BOT_TOKEN=<YOUR_DISCORD_BOT_TOKEN>
      - OPENCLAW_DISABLE_BONJOUR=1
    restart: unless-stopped
    extra_hosts:
      - "workstation:<YOUR-WINDOWS-IP>"
```

The `extra_hosts` line lets the container resolve "workstation" to your Windows machine's IP.

### 3.4 Create openclaw.json Config

Place this in the `config/` directory as `openclaw.json`:

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "ollama": {
        "baseUrl": "http://workstation:11434/v1",
        "apiKey": "ollama-local",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3-vl:8b",
            "name": "Daily Driver (GPU Fast)",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 8192,
            "maxTokens": 8192
          },
          {
            "id": "qwen3-vl:32b",
            "name": "Heavy Expert (CPU Smart)",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 8192,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/qwen3-vl:8b",
        "fallbacks": ["ollama/qwen3-vl:32b"]
      },
      "maxConcurrent": 2,
      "compaction": { "mode": "safeguard" }
    }
  },
  "plugins": {
    "entries": {
      "discord": { "enabled": true }
    }
  },
  "gateway": {
    "mode": "local",
    "port": 18789,
    "bind": "lan"
  }
}
```

**Important config notes:**
- `contextWindow: 8192` — start conservative. KV cache eats RAM beyond model weights. Increase only if needed.
- `"primary": "ollama/qwen3-vl:8b"` — fast model first, falls back to 32B if 8B fails.
- Do NOT put `channels.discord.dmPolicy` or `channels.discord.allowFrom` in this file — those keys were invalid as of OpenClaw v2026.2.x and will cause config errors.

### 3.5 Launch

```bash
cd /mnt/<YOUR-POOL>/apps/openclaw
docker compose pull
docker compose up -d
docker logs openclaw-gateway --tail 30
```

### 3.6 Onboarding

> **This is where we hit a blocker — see Phase 3 Troubleshooting below.**

The OpenClaw Docker image may require an interactive onboarding wizard to generate auth tokens and complete setup. If the web UI at `http://<TRUENAS-IP>:18789` doesn't load, check the logs.

---

## Phase 3 Troubleshooting

### "Config invalid: Unrecognized keys: channels.discord.dmPolicy, channels.discord.allowFrom"
These config keys don't exist in current OpenClaw schema. Remove the entire `"channels"` block from openclaw.json and restart.

### "Gateway auth is set to token, but no token is configured"
OpenClaw needs an auth token to start the web UI. Options:
1. Add `OPENCLAW_GATEWAY_TOKEN=<any-random-string>` to the environment section of docker-compose.yml
2. Use the official `docker-setup.sh` from the OpenClaw repo which generates tokens automatically
3. Install OpenClaw via npm on the host and run `openclaw onboard`

### `docker exec -it openclaw-gateway openclaw onboard` → "executable file not found"
The `openclaw` CLI binary may not be in the container's PATH, or the container is in a restart loop. Try:
```bash
docker exec -it openclaw-gateway bash
# Then inside container:
which openclaw || find / -name "openclaw" 2>/dev/null
```

If the container keeps restarting, check logs: `docker logs openclaw-gateway --tail 50`

### Container is in a restart loop
Usually caused by invalid config. Check `docker logs` for the specific error. Common fixes:
- Remove invalid config keys (see above)
- Ensure the JSON is valid (no trailing commas, proper brackets)
- Verify the Ollama endpoint is reachable from inside the container

### TrueNAS can't reach Windows Ollama (curl hangs)
1. Verify Ollama is running on Windows: `netstat -an | findstr 11434` → should show `0.0.0.0:11434 LISTENING`
2. Verify Windows Firewall rule exists: `Get-NetFirewallRule -DisplayName "Ollama LAN"`
3. Verify same subnet: both machines should be 192.168.0.x
4. After changing OLLAMA_HOST env var, you MUST restart Ollama (quit from tray → relaunch)

---

## Phase 4: Discord Pairing (After OpenClaw Web UI Works)

1. Open `http://<TRUENAS-IP>:18789` in your browser
2. Complete any remaining onboarding steps
3. Send a message to your Discord bot
4. You'll receive a pairing code
5. Approve it:
```bash
docker compose exec openclaw openclaw pairing approve discord <CODE>
```

---

## Phase 5: Access from Any Device

### Option A: Discord (easiest)
Open Discord on your phone (GrapheneOS) or Mac and message the bot. Works immediately once pairing is complete.

### Option B: Tailscale + Web UI (most private)
Install Tailscale on TrueNAS, Android, and Mac. Access the OpenClaw web UI directly at `http://<truenas-tailscale-ip>:18789` — no Discord relay needed. All traffic stays on your private Tailnet.

### Option C: Both
Use Discord for quick mobile messages, Tailscale web UI for vision/file tasks.

---

## Remaining Setup Tasks

- [ ] Resolve OpenClaw gateway auth token issue
- [ ] Complete Discord bot pairing
- [ ] Configure SearXNG integration for web search
- [ ] Test text conversation end-to-end
- [ ] Test vision pipeline (send image via Discord → Ollama)
- [ ] Configure model routing (8B quick / 32B complex)
- [ ] Set up OpenClaw memory and personality (SOUL.md, MEMORY.md)
- [ ] Add auto-restart cron for OpenClaw stability
- [ ] Optional: Tailscale setup

---

## Known Limitations and Gotchas

**OpenClaw stability:** Crashes frequently with Ollama backends. Community recommends auto-restart every 30 minutes via cron or Docker healthcheck.

**OpenClaw bug #7211:** Sub-agents can silently fall back to cloud Claude API instead of your local Ollama model, even when config looks correct. Always verify transcripts to check which model actually responded.

**Vision through messaging:** Sending images via Discord → OpenClaw → Ollama vision is poorly documented as of Feb 2026. May need to use the web UI for vision tasks initially.

**KV cache memory:** Context window size directly impacts RAM usage beyond model weights. At 32K context, the 8B model needs ~9.3GB total (model + KV), eating into your 12GB VRAM budget. Start at 8192.

**OpenClaw context requirements:** Official docs recommend 64K+ context models for reliable multi-step agent tasks. We're starting at 8K for stability and will increase as needed.

**8B model intelligence:** Good enough for OCR, log reading, and common plant identification. Won't reliably identify niche anime characters, rare plant cultivars, or handle complex multi-step reasoning. That's what the 32B fallback is for.

## Navigation

- Back to [[Project Overview - Sovereign AI Stack]]
- See also: [[Speed Myth - Ollama vs Text-Gen-WebUI]]
- See also: [[Project Status - Sovereign AI Stack]]

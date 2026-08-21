---
tags: [guide, hardening, local-ai]
---
# Architecture Guide - Sovereign AI Stack

> Deep dive into the network topology, data flow, and design decisions behind the sovereign AI stack.

## Network Topology

```
┌─────────────────────────────────────────────────────────┐
│                    LAN: 192.168.0.0/24                  │
│                                                         │
│  ┌──────────────────────┐    ┌───────────────────────┐  │
│  │  TrueNAS Server      │    │  Windows Workstation   │  │
│  │  192.168.0.120       │    │  192.168.0.112         │  │
│  │                      │    │                        │  │
│  │  ┌────────────────┐  │    │  ┌──────────────────┐  │  │
│  │  │  OpenClaw      │──┼────┼──│  Ollama          │  │  │
│  │  │  :18789        │  │    │  │  :11434          │  │  │
│  │  └────────────────┘  │    │  │                  │  │  │
│  │                      │    │  │  qwen3-vl:8b     │  │  │
│  │  ┌────────────────┐  │    │  │  (GPU, 30-50t/s) │  │  │
│  │  │  SearXNG       │  │    │  │                  │  │  │
│  │  │  :30053        │  │    │  │  qwen3-vl:32b    │  │  │
│  │  └────────────────┘  │    │  │  (CPU, 5-8t/s)   │  │  │
│  │                      │    │  └──────────────────┘  │  │
│  │  15+ other Docker    │    │                        │  │
│  │  containers          │    │  Windows Firewall:     │  │
│  │  (Nextcloud, Immich, │    │  "Ollama LAN" rule     │  │
│  │   Jellyfin, etc.)    │    │  TCP 11434 ← LAN only  │  │
│  └──────────────────────┘    └───────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
         ↑                              
    Discord Cloud                       
    (message relay)                     
         ↑                              
    Android / Mac                       
    (user devices)                      
```

## Data Flow — Text Message

```
1. User sends "Why is my Nextcloud slow?" to Discord bot
2. Discord cloud relays message to OpenClaw (TrueNAS :18789)
3. OpenClaw constructs prompt with context/memory
4. OpenClaw sends POST to Ollama API (Windows :11434/v1/chat/completions)
5. Ollama loads qwen3-vl:8b on GPU, generates response (~30-50 t/s)
6. Response flows back: Ollama → OpenClaw → Discord → user's phone
```

Total latency: ~2-5 seconds for typical responses.

## Data Flow — Vision (Image)

```
1. User sends photo of error screen to Discord bot
2. Discord relays image to OpenClaw
3. OpenClaw forwards image (base64) + prompt to Ollama
4. Ollama processes with qwen3-vl:8b multimodal encoder
5. Model describes/interprets the image
6. Response flows back through the chain
```

> **Caveat:** Vision through Discord → OpenClaw → Ollama is poorly documented as of Feb 2026. May require the web UI instead. ~55% confidence this works out of the box.

## Model Routing Strategy

| Scenario | Model | Why |
|----------|-------|-----|
| Quick question | qwen3-vl:8b (GPU) | Fast, adequate quality |
| Screenshot OCR | qwen3-vl:8b (GPU) | Vision + speed |
| Complex diagnosis | qwen3-vl:32b (CPU) | Higher reasoning quality |
| Plant identification | qwen3-vl:32b (CPU) | Better visual discrimination |
| Multi-step tasks | qwen3-vl:32b (CPU) | Longer context handling |

OpenClaw config sets 8B as primary with 32B as fallback. Manual model selection may also be possible through OpenClaw commands.

## Resource Budget

### Windows Workstation (64GB RAM, 12GB VRAM)

| Resource | qwen3-vl:8b (GPU) | qwen3-vl:32b (CPU) |
|----------|-------------------|---------------------|
| Model weights | ~5.7GB VRAM | ~21GB RAM |
| KV cache (8K ctx) | ~0.9GB VRAM | ~3.5GB RAM |
| KV cache (32K ctx) | ~3.6GB VRAM | ~14GB RAM |
| **Total (8K)** | **~6.6GB / 12GB** | **~24.5GB / 64GB** |
| **Total (32K)** | **~9.3GB / 12GB** | **~35GB / 64GB** |

At 8K context: both models fit comfortably with headroom.
At 32K context: GPU model gets tight (9.3/12GB), CPU model still fine.

Starting at 8192 context window is the safe default.

### TrueNAS (32GB RAM)

| Service | RAM Usage |
|---------|-----------|
| ZFS ARC cache | ~8-12GB |
| 15+ Docker containers | ~6-8GB |
| OpenClaw gateway | ~256MB |
| **Free headroom** | **~10-16GB** |

OpenClaw is lightweight — no inference, just routing. TrueNAS stays healthy.

## Security Considerations

### What's Private
- All LLM inference happens locally on your LAN
- No API keys to OpenAI/Anthropic/Google needed
- SearXNG for web search (self-hosted, no tracking)
- Model weights stored locally on Windows

### What Leaves Your Network
- Discord message relay goes through Discord's cloud servers
- Discord encrypts in transit but is not E2E encrypted
- To eliminate Discord dependency: use Tailscale + OpenClaw web UI

### Mitigations
- Windows Firewall restricts Ollama to LAN subnet only
- OpenClaw gateway auth token required for web UI access
- OpenClaw consent mode can be enabled for explicit approval
- Discord bot restricted to specific user IDs

## Future Enhancements

- **Tailscale:** Zero-cloud-relay access to web UI from anywhere
- **SearXNG integration:** Give the AI web search through OpenClaw skills
- **Memory system:** SOUL.md (personality) + MEMORY.md (persistent context)
- **Student-teacher:** 8B model learns from 32B corrections over time via memory logs
- **More models:** Swap in newer GGUF models as they release without changing architecture

## Navigation

- Back to [[Project Overview - Sovereign AI Stack]]
- See also: [[Setup Tutorial - Sovereign AI Stack]]

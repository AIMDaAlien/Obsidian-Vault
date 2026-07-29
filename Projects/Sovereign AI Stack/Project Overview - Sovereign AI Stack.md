---
tags: [sovereign-ai, project-overview, self-hosted, privacy, llm]
created: 2026-02-10
published_to_garden: true
last_published: '2026-07-29T23:14:32'
---

# Project Overview - Sovereign AI Stack

> **Status:** 🟡 In Progress — OpenClaw gateway onboarding pending
> **Started:** 2026-02-10
> **Last Updated:** 2026-02-10

## What Is This?

A fully local, privacy-first AI assistant system that runs on your own hardware with zero cloud AI dependencies. You message it from any device (phone, laptop) through Discord, and it responds using local LLMs running on your Windows workstation.

Think of it as your own private ChatGPT that never phones home.

## Why Build This?

- **Privacy:** No conversation data leaves your network (except Discord relay for messaging transport)
- **Cost:** Zero API fees — all inference is local after initial setup
- **Control:** Choose your own models, tune parameters, own your data
- **Learning:** Deep understanding of LLM inference, Docker, networking, and agent frameworks
- **Availability:** Always-on assistant accessible from any device on your network

## Architecture Summary

```
Android (GrapheneOS) / Mac
        ↓
   Discord Bot (cloud relay, encrypted)
        ↓
   OpenClaw Gateway (Docker on TrueNAS — lightweight, no inference)
        ↓
   Ollama (Windows Workstation — all inference)
    ├── qwen3-vl:8b  → GPU (RTX 3060, fast ~30-50 t/s)
    └── qwen3-vl:32b → CPU (i5-12600KF + 64GB RAM, smart ~5-8 t/s)
```

## Hardware Inventory

| Machine | CPU | RAM | GPU | Role | IP |
|---------|-----|-----|-----|------|-----|
| Windows Workstation | i5-12600KF (6P+4E) | 64GB | RTX 3060 12GB | All LLM inference | 192.168.0.112 |
| TrueNAS Server | i5-11400 | 32GB | None | OpenClaw gateway + services | 192.168.0.120 |

## Key Decisions

### Why Ollama over text-generation-webui?
Text-gen-webui's speed advantage (ExLlamaV2 backend) only applies to EXL2/GPTQ model formats. Our vision models (Qwen3-VL) only exist as GGUF, which uses the same llama.cpp engine in both tools. Ollama wins on simplicity, native OpenAI-compatible API, and seamless OpenClaw integration with zero speed penalty for our use case. See [[Speed Myth - Ollama vs Text-Gen-WebUI]].

### Why inference on Windows, not TrueNAS?
TrueNAS only has 32GB RAM with ~20GB already consumed by ZFS ARC cache and 15+ Docker containers. The 32B model alone needs ~21GB. Windows workstation has 64GB RAM + dedicated GPU — can comfortably run both models with headroom.

### Why Qwen3-VL models?
Best vision-language models in their size class (as of Feb 2026). Native multimodal (text + image), tool calling support, 128K context window, official GGUF releases, and confirmed Ollama compatibility. See earlier research session for full model comparison.

### Why OpenClaw?
Open-source, self-hosted agent gateway that bridges messaging platforms (Discord, Telegram, WhatsApp) to LLM backends. Supports Ollama natively via OpenAI-compatible API. Has memory, personality, and skill systems. The "brain" that sits between your chat apps and your models.

## Project Files

- [[Architecture Guide - Sovereign AI Stack]] — Detailed network topology and data flow
- [[Setup Tutorial - Sovereign AI Stack]] — Step-by-step with troubleshooting
- [[Project Status - Sovereign AI Stack]] — Current state, blockers, next steps

## Related Notes

- [[Project Overview - NOC Skills Homelab]] — Related TrueNAS/Docker skills
- [[Docker and Portainer Setup]] — Docker fundamentals

## Navigation

- Back to [[Projects/README]]
- Back to [[Knowledge Base - Main Index]]

---
tags: [local-ai, hardware-constraints, unraid]
---
# Frontier Landscape — what fits 128 GB (Aug 2026)

> "Is there anything smarter than Qwen3.8-Flash-Next that runs on the Unraid box
> (128 GB RAM + RTX 3060 12 GB)?" Answer: **no, not meaningfully.**

## The ladder (open-weight frontier, sorted by total params)

| Model | Total / active | 4-bit est | Verdict on 128 GB |
|---|---|---|---|
| Kimi K3 (Moonshot) | 2.8T | ~1.4 TB | absurd, cloud-only |
| DeepSeek V4 Pro | 1.6T / 49B | ~800 GB | no |
| GLM-5.2 | 753B / 40B | ~377 GB | no |
| MiniMax M3 | 428B / 23B | ~214 GB | no |
| GLM-5.3-Flash | 320B / 18B | ~160 GB | IQ1-only → [[GLM-5.3-Flash]] no-go |
| DeepSeek V4 Flash | 284B / 13B | ~142 GB | Q2_K_S 98.6 GB loads, but slow + Q2 quality → no |
| **Qwen3.8-Flash-Next** | **176B / 6B** | **84 GB @ Q3** | **✅ the sweet spot** |
| MiniMax M2.7 | ~172B | ~86 GB | similar size — sidegrade, not upgrade |
| Qwen3-Coder-Next | 80B / 3B | ~40 GB | smaller/faster, less capable |

## Why Flash-Next is the ceiling

- RAM-fit rule: ~101 GB usable → total must be ≤ ~200 B at a good quant (Q3/Q4).
- Decode speed tracks ACTIVE params. Flash-Next activates only **6B** → ~14.5 t/s
  on DDR4. DeepSeek V4 Flash activates 13B → ~2× slower at its only fitting quant.
- Everything *smarter* (Kimi K3, V4 Pro, GLM-5.2/5.3, MiniMax M3) is 284B–2.8T —
  the next tier up needs **256 GB+ RAM or a 512 GB Mac Studio**, not 128 GB.

## Takeaway

Flash-Next (176B/6B) is deliberately engineered for exactly this hardware class.
It is the practical intelligence ceiling of a 128 GB + 12 GB GPU box. Going up a
tier = the future Mac Studio M5 Ultra 512 GB (Oct 2026).

## Related

- [[Qwen3.8-Flash-Next]]
- [[GLM-5.3-Flash]]
- [[LLM Benchmark Registry - Mac vs Unraid]]

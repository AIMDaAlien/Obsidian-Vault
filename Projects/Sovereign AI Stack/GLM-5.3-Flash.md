---
tags: [local-ai, hardware-constraints, unraid]
---
# GLM-5.3-Flash (320B-A18B) — feasibility: NO-GO on this box

> 2026-08-29. Assessed against the Unraid box (RTX 3060 12 GB + 128 GB DDR4,
> ~101 GB usable RAM). This is the former "Ox Alpha" — Z.AI/Zhipu released weights
> Aug 26-27, 2026.

## What it is

- **320B total / ~18B active** MoE (was advertised 320B-A18B). 45 layers.
- Hybrid: 34 `linear_attention` + 11 `deepseek_sparse_attention` layers,
  MLA (q_lora_rank 1536, kv_lora_rank 512, mla_use_nope), 288 routed experts
  top-8 + 1 shared, `moe_intermediate_size` 2048, 1 MTP layer, 1M-token context,
  natively multimodal (vision + video).
- arch string: `glm5_next` / `Glm5NextForConditionalGeneration`.

## Why it's a NO-GO here (three independent blockers)

1. **Arch not in llama.cpp yet.** Local build (Aug 28, b387ddf) registers
   `glm4`, `glm4moe`, `glm-dsa`, `qwen3next` — but NOT `glm5_next`. Would need a
   newer llama.cpp (Unsloth has GGUFs via their own build).
2. **Only IQ1/IQ2 fits RAM.** Unsloth UD sizes: IQ1_S ~93 GB, IQ1_M ~97.6 GB,
   IQ2_XXS ~101.8 GB (borderline), IQ3_XXS ~120 GB (no), Q2_K_XL ~108.7 GB (no),
   Q3_K_XL ~147 GB (no). RAM-fit rule (must fit ~101 GB) → IQ1/IQ2 only =
   severe quality loss.
3. **18B active = 3× Flash-Next's 6B.** Bandwidth-bound decode ≈
   (18B × ~1.9 bits) ÷ 45 GB/s ≈ **9-11 tok/s at IQ1** — *slower* than
   Flash-Next Q3_K_XL (~14.5 tok/s) at *worse* quality.

## Verdict

Strictly worse than [[Qwen3.8-Flash-Next]] on this hardware on every axis
(bigger, slower, more quantized, unsupported arch). A **512 GB-class** model —
would run well on the future Mac Studio M5 Ultra 512 GB (Oct 2026) at IQ3_XXS/Q3
with ~100+ tok/s unified-memory decode, but not on 128 GB + a 12 GB GPU.

## Related

- [[Qwen3.8-Flash-Next]]
- [[LLM Benchmark Registry - Mac vs Unraid]]

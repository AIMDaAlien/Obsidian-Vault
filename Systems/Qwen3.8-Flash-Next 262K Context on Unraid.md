# Qwen3.8-Flash-Next (Qwen4-exp) on Unraid — 262K Context & Tuning

Date: 2026-09-06
Model: Qwen/Qwen3.8-Flash-Next — 125B MoE (6B active) + 51B n-gram embedding (PLE) + 4B MTP, architecture `qwen4_exp` (preview of Qwen4)
Quant: UD-IQ3_XXS (76.3 GB on disk, 3 shards, /mnt/cache/llm-workspace/models/qfn-iq3xxs/)
Related: [[K2-Horizon MoVA Serving and Benchmarks]], [[Local AI Benchmark Content Site]], [[opencode-qwen-deepseek-setup]]

## TL;DR

- Full native **262,144-token context** runs on the RTX 3060 12 GB box. The GDN+QSA hybrid makes long context nearly free: KV at q8_0 is only ~3.4 GB at 262K (12 QSA layers × 2 KV heads × 256 dim; the 36 GDN layers keep a fixed recurrent state, no cache).
- Decode: ~14.7 tok/s at 262K on latest master — *faster* than 13.3 at 128K on the old build.
- Biggest win after tuning: rebuilding llama.cpp on latest master picked up 7 qwen4exp fixes (incl. GDN normalization correctness merged 2026-09-06, CUDA sparse-FA, graph-split reduction).
- ncmoe frontier mapped: 18.9 t/s possible with 42 expert layers on CPU — but only at small contexts (KV+compute buffers OOM at 262K). Full context costs ~40% speed; one-line switch between configs.
- Wired into OpenCode as `qwen38-unraid/qwen38-flash` (context limit 262144, output 16384).

## Why 262K is cheap on this architecture

| Component | q8_0 KV | f16 KV |
|---|---|---|
| QSA KV cache (12 layers × 2 KV heads × 256) | ~3.4 GB | ~6.4 GB |
| GDN recurrent state (36 layers) | ~0.04 GB | ~0.08 GB |
| Total context overhead | **~4 GB** | **~7 GB** |

A Qwen3.5-class dense-attention 125B at 262K would need tens of GB of KV. This is the Qwen4-preview payoff: GDN compresses history to fixed state, QSA sparsifies the only 12 attention layers. Prefill is still the wall-time cost (~10-15 min for a full 262K prompt); decode stays fast.

## Tuning chain (what moved the needle)

1. **performance CPU governor** (was powersave) — the same catch as K2; biggest single lever for CPU-offloaded MoE decode.
2. **q8_0 KV cache + --threads-batch 12 + mlock** — lossless.
3. **Rebuild on latest master** (Aug 29 build → Sept 6 master): 7 qwen4exp fixes; 13.3 → 14.7 t/s at 262K.
4. **ncmoe sweep** (llama-bench, tg128):

| Expert layers on CPU | t/s |
|---|---|
| 48 (all CPU, old --cpu-moe) | 13.6 |
| 46 | 15.8 |
| 44 | 18.4 |
| 42 | 18.9 |
| 40 | OOM (won't load) |

5. **The context/speed tradeoff:** 42-44 CPU layers OOM once full 262K KV + compute buffers are added. Final stable config: **ncmoe 48 + 262K** at 10.6/12 GB VRAM. For short-context work, flip to `ncmoe 44` + `CTX_SIZE=32768` → ~18.4 t/s. One-line switch in the entrypoint.

## MTP speculative decoding: blocked

The locally downloaded 4B MTP draft (qfn-mtp/Qwen3.8-Flash-Next-MTP-Q4_K_M.gguf) fails to load on current master: `tensor 'blk.0.hc_attn_norm.weight' not found` — the draft GGUF predates the hyperconnection tensor naming. Needs a fresh MTP export matched to the current converter. Disabled rather than risk instability.

## Ops notes

- Container: llm-qwen38-flash, port 18006, image local/qwen38-flash-cuda (Dockerfile.qwen38-flash, build stamp ≥ Sept 6 master)
- Entrypoint: /mnt/cache/appdata/unraid-llm/qwen38-flash-entrypoint.sh (CTX_SIZE default 262144; backup at .bak)
- llama-bench is now built into the image (target llama-server llama-bench)
- K2 removed: container, image, GGUF, entrypoint all deleted; GPU freed
- OpenCode: `qwen38-unraid/qwen38-flash` — provider survived the K2 swap (same port), config updated for 262K/16K output
- ncmoe sweep results: /mnt/cache/appdata/unraid-llm/ncmoe-sweep.txt

## Verdict

A 176B-class model (125B main + 51B n-gram table) at full native 262K context on a 12 GB RTX 3060 + DDR4 at ~14.7 t/s, wired into the daily coding tool — best possible outcome for this hardware, confirmed empirically at each step. Benchmarks recorded in metalbench and this vault.

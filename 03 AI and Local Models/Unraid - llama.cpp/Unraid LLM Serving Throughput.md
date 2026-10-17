---
tags: [penthouse, unraid, llm, llama-cpp, throughput, benchmark]
created: 2026-09-16
publish: true
featured: 15
machine: unraid
engine: llama.cpp
---

# Unraid LLM Serving Throughput

Measured on the box, 2026-09-15/16. Related ops: [[13 - Unraid Production Operations]].

## What is serving

- host: `<lan-ip-5>` (Unraid, 128 GB RAM, i5-12600KF, RTX 3060 12 GB)
- model: Qwen3.8-Flash-Next-UD, IQ3_XXS quant (3.0625 bpw per `/v1/models` meta), 3 GGUF shards ~77 GB
- runtime: llama.cpp `llama-server` in Docker (`local/qwen38-flash-cuda:latest`, port 18006 -> 8000)
- launch shape: `-ncmoe 48`, `--gpu-layers 99`, `--override-tensor ple_ngram_embd=CPU`, ctx 262144, flash-attn on, KV cache q8_0/q8_0, `--load-mode none`
- decode is DDR4-bandwidth-bound (all expert layers streamed from RAM)

## What changed (2026-09-16)

- Rebuilt the llama.cpp image from current master: 0.4.1-dev commit 930e2fa. Build took ~7 min (`-j4`, targets `llama-server llama-bench`). Old image preserved as `local/qwen38-flash-cuda:prev-0909`.
- Cache-bust trick: edit the `# cache-bust ...` comment line in `/mnt/cache/appdata/unraid-llm/Dockerfile.qwen38-flash` so Docker refetches the `git clone --depth 1` layer.
- Installed QwFNfer v0.2.3 to `/mnt/cache/llm-workspace/qwfnfer` (persistent, not /root — the earlier install vanished at reboot).

## Measured results (same IQ3_XXS file, 400-token greedy, warm)

| engine | short-chat decode | 5.1K-token prefill | long-ctx decode |
|---|---|---|---|
| llama.cpp old (0.4.0-dev, Sep 9) | ~14.9 t/s | — | — |
| llama.cpp new (0.4.1-dev, Sep 15) | 17.4-17.5 t/s | 263 t/s | 16.9 t/s |
| QwFNfer 0.2.3 (spec-ahead 2) | 17.75 t/s | 277 t/s | 13.7 t/s |
| QwFNfer 0.2.3 (spec-ahead 1) | 17.9-18.4 t/s | — | — |

- The week of upstream qwen4exp work (sparse flash attention #27970, graph-split reduction #27880, recurrent rollback #28123) was a free +17% decode with no config change.
- QwFNfer is no longer a clear upgrade on this quant. llama.cpp stays the default server. QwFNfer flags that mattered: `--ram 32 --threads 16 --state-host idx --kv q8_0 --reserve 512 --port 8085`.

## Gotchas worth remembering

- `reasoning_effort` template only accepts `xhigh` / `medium` / `low` — no `off`. Dropping the default xhigh to medium is the biggest practical token-savings lever for agentic use.
- Mainline llama.cpp MTP for qwen4exp is still an open PR (#27836). Unsloth MTP draft GGUFs silently no-op on mainline (`-md` accepted, no speedup). Working MTP routes today: ik_llama.cpp main (`--spec-type mtp:n_max=4`) or QwFNfer's built-in `--spec-ahead`.
- Backgrounding long-lived processes over ssh: `nohup ... & disown; exit 0` — plain `&` hangs the ssh session until timeout.

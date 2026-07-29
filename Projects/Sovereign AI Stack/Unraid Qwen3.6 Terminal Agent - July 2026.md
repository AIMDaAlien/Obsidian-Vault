---
tags: [sovereign-ai, unraid, qwen, terminal-agent, llm]
created: 2026-07-28
published_to_garden: true
last_published: '2026-07-29T23:14:32'
---

# Unraid Qwen3.6 terminal agent

updated: 2026-07-28

## current setup

**Qwen3.6 35B A3B** is the Unraid terminal, backend, and deep SWE model.

- 35B total params, 3B active MoE params
- Q6_K main GGUF: 29.3 GB
- matching Q8 DFlash draft: 421 MB
- 128K server context, one request slot
- 8 GPU layers on the RTX 3060 12 GB
- 14 CPU threads
- 55 GB container cap so the model can die without taking Unraid down
- Flash Attention on
- DFlash on
- endpoint: `http://192.168.0.120:18004/v1`
- OpenCode model: `unraid-qwen36/qwen36-terminal`

The service runs through the Poolside llama.cpp fork. It understands the Qwen3.5 MoE architecture used by Qwen3.6 and supports the matching DFlash draft.

## why this won

The first plan was Laguna S 2.1. Q3 was safe for RAM but not worth trusting as a Qwen replacement. Q4 at 128K was too close to the 128 GB host limit once weights, KV cache, draft model, and normal Unraid services were counted.

A Qwen3.5 terminal/SWE research fine-tune was also considered. It was trained on terminal and SWE traces, but had no full public benchmark suite and needed a huge BF16 download plus local conversion.

Official Qwen3.6 35B A3B was the better pick.

Published Qwen numbers vs Qwen3.5 35B A3B:

- Terminal-Bench 2.0: 51.5 vs 40.5
- SWE-bench Verified: 73.4 vs 70.0
- SWE-bench Multilingual: 67.2 vs 60.3
- SWE-bench Pro: 49.5 vs 44.6
- SkillsBench: 28.7 vs 4.4

## measured results

The model loaded cleanly at 128K.

- GPU VRAM: about 7.56 GB
- prompt processing: about 48 to 57 tokens/sec
- decode with DFlash: about 14.08 tokens/sec
- decode without DFlash: about 13.48 tokens/sec
- DFlash gain: about 4.5%
- draft acceptance: about 32 to 36%

DFlash helps a little and only costs 421 MB, so it stays on. It isnt a magic speed boost on this CPU/RAM-offloaded RTX 3060 setup.

## actual agent tests

The model correctly chose OpenCode's real `glob` tool instead of hallucinating an `ls` tool.

It completed a real repair loop:

- inspected the repo
- found a health-check bug using `any()` instead of `all()`
- ran tests
- fixed the first bug
- noticed the `all([])` edge case after tests still failed
- fixed that too
- reran tests successfully: 3/3 passed

This makes it a real OpenCode coding option, not just a chat model that looks convincing.

## thinking setup

Qwen3.6 can spend an entire response in private reasoning and never send the useful answer.

Server defaults now use:

- reasoning auto mode
- 1,024-token reasoning budget
- reasoning preservation for multi-turn work
- 4,096-token output cap

For routine calls, clients can send `chat_template_kwargs: {"enable_thinking": false}`.

## safety boundary

It is not safe for unrestricted autonomous server administration.

In a disk-pressure test, it eventually suggested moving torrent data and an `rm -rf` command even after being told not to. Keep OpenCode safeguards on:

- `rm -rf` denied
- `sudo` denied
- destructive Docker actions need approval
- secrets and environment files need approval
- state-changing server work stays supervised

It is good at coding, diagnosis, and tool loops. It is not a trusted Unraid operator.

## SGLang notes

SGLang is a serious inference server with continuous batching, prefix caching, speculative decoding, GGUF support, CPU offload, and Qwen3.5-MoE support.

It is not architecture agnostic. It needs support for both the model family and the hardware backend.

It should support this Qwen3.6 architecture because Qwen3.6 uses the `qwen3_5_moe` family. It can run on CUDA/NVIDIA, AMD ROCm, Intel CPU, TPUs, and other supported backends, but its fast paths are hardware specific.

Dont replace llama.cpp yet.

- SGLang shines with GPU-resident models and many simultaneous users.
- this host has a 12 GB RTX 3060 and a 29 GB Q6 model, so CPU/RAM offload and PCIe still dominate
- OpenCode is usually one long sequential agent session, not a high-concurrency API workload
- the existing llama.cpp setup already has a verified 128K context, DFlash, and working repair loop
- the current llama.cpp DFlash GGUF cannot be assumed to work with SGLang without an exact compatibility test

SGLang is worth a separate future benchmark service. Compare 128K load, prefill, decode, DFlash acceptance, memory use, and the same OpenCode repair task before replacing anything.

## useful files

- raw benchmark: `/Users/aim/Documents/unraid-llm-stack/qwen36-benchmark-dflash.json`
- benchmark sandbox: `/tmp/qwen36-opencode-bench/`
- server stack source: `/Users/aim/Documents/unraid-llm-stack/`

---
tags: [local-ai, benchmarks]
created: 2026-10-17
publish: true
machine: mac
engine: lithos, splash, mlx
---
# Inference Engine Face-Off: lithos vs Splash vs MLX

## The Short Version

- **Splash** is the best of the three engines by a lot.
- **lithos** isnt usable for coding agents on this Mac.
- **MLX** works, but on real agent work it's roughly 3 to 4x slower than Splash (my estimate, see below).
- Even with Splash, 40 minutes to 2 hours per coding task is too slow for the work I need.
- I'm moving my local AI work to my Omarchy machine.

## What I Tested

An **inference engine** is the software that actually runs an AI model on your computer. Same model, different engine, and the speed can be very different.

I tested a new one called **lithos-metal** (by LithosAI) against **Splash** and Apple's **MLX**. All three ran the same model, Qwen3.8-27B, on my MacBook Pro (M5 Pro chip, 20-core GPU, 48 GB). I ran everything on Oct 16 to 17, 2026.

- lithos-metal 0.1.2
- Splash 1.3.2
- mlx-lm 0.32.2

lithos advertises "200+ tokens per second" for this model. A **token** is a chunk of a word, which is what the model reads and writes. That 200+ number is a projection made on the more expensive M5 Max chip with tuned settings. On my M5 Pro, lithos has no tuned settings for this model. Its own log says so.

My goal was simple. Find what's fastest overall for coding-agent work, without losing quality. A **coding agent** is the AI working on a real codebase by itself, running commands, step by step.

## How I Kept It Fair

- One engine loaded at a time, everything else stopped first.
- I waited for the Mac to cool to normal before each engine.
- Plugged into a 98 W Thunderbolt 5 dock, lid open, High Power Mode on.
- The GPU held full speed (1585 to 1620 MHz) the whole time.

## The Speed Test

Short prompts, thinking off, median of 3 runs, 512 tokens out. The first four columns are tokens per second (how fast the model writes), so higher is better. "22K prompt wait" is the seconds before the first word when the prompt is about 22,000 tokens. That wait is **prefill**, the model reading your prompt before it answers. Lower is better.

| Engine (model file) | code | math | chat | creative | 22K prompt wait |
|---|---|---|---|---|---|
| Splash (MLX 4-bit file) | 77 | 86 | 40 | 35 | 36 s |
| Splash (NVFP4 file) | 63 | 66 | 32 | 30 | 37 s |
| lithos (NVFP4 file + its draft model) | 33 | 41 | 17 | 15 | 133 s |
| MLX (4-bit file) | 16 | 17 | 16 | 15 | 50 s |

Splash is about 1.9x faster than lithos on the exact same NVFP4 file. So the difference is the engine, not the file.

Both lithos and Splash use a **draft model**. That's **speculative decoding**. A small fast model guesses the next few words and the big model checks them in one go. That's why they beat plain MLX. It helps most on predictable text like code and math, and least on chat and creative writing. With its draft model turned off, lithos does about 13 tok/s.

## Long Conversations

This is what coding agents actually do. They build up a huge **context**, which is how much the model can keep in its head at once. Think of it as working memory. I recorded a real coding-agent session and replayed parts of it on each engine.

**Splash** started answering the next step of a 163,000-token conversation in 5.4 s. At 250,000 tokens it also took about 5.4 s, writing around 40 tok/s. It reuses what it already read.

**MLX** usually reused what it already read (5 of 6 steps in my test, 1.6 to 10 s to start). Then once it lost track and reread everything. That took 691 s (11.5 minutes) at 173,000 tokens. Writing speed dropped to about 9 to 10 tok/s at that size. It ran out of memory at 250,000 tokens on a step where it had to reread everything, even with the GPU memory limit raised.

**lithos** can only hold 32,000 tokens on this Mac. I tested 64,000 (ran out of memory) and 128,000 (crashed). It also cant think, because its thinking mode is switched off in its code. Even small agent steps took 17 to 29 s to start. A real coding-agent task went past 50,000 tokens within 18 steps, so lithos cant do this kind of work here.

## A Full Agent Session

I ran a full session of 86 steps. The conversation grew to 259,000 tokens and the model wrote 188,000 tokens, mostly thinking.

| Engine | Time |
|---|---|
| Splash | 124 minutes (measured) |
| MLX | 233 to 345 minutes (ESTIMATE), and it couldnt hold the whole session in memory |
| lithos | cant run it |

## Which Model File

On Splash, the MLX 4-bit file was fastest. A **quant** is a shrunk version of the model file, and there are a few kinds. NVFP4 was about 20% slower. Unsloth's GGUF UD-Q4_K_M was about 15% slower (code 65 vs 77). I didnt compare answer quality between files.

## Can It Actually Code?

I used real tasks from SWE-rebench. Those are fresh GitHub issues from May to July 2026, graded by the projects' own hidden tests. I ran a coding agent on Splash, 2 tasks at once.

| task (language) | thinking level | result | time | steps |
|---|---|---|---|---|
| nanobot (Python) | xhigh (default) | solved | 37 min | 59 |
| vue core (TypeScript) | xhigh | stopped before it finished | 74+ min | 78+ |
| floci (Java) | low | failed | 65 min | 149 |
| ruff (Rust) | low | solved | about 2 hours | 181 |

2 of the 3 tasks that finished were solved. That's a tiny sample, not a score.

I also ran one harder task from DeepSWE. It ran for 2 hours and never submitted because its conversation got too long (259,000 tokens). It broke nothing, since all 209 existing tests still passed. But it solved none of the 10 new tests.

Qwen3.8 thinks at its maximum "xhigh" level by default. Its own instructions tell it to think carefully and consider alternatives. That's why it writes so much. Turning thinking down to "low" didnt make tasks faster. It just took way more, smaller steps.

## What Actually Limits This Mac

It's memory speed. This model reads all of its ~15 GB for every word it writes. I measured about 290 GB/s on the M5 Pro, which caps plain writing at about 19 tok/s. MLX gets 16 to 17. Draft models are the only way past that.

The model is also "dense", which means it uses all of itself for every word. Mixture-of-experts models only use a small part per word and run much faster on the same Mac.

The engines werent broken. Splash's own published number for this chip is 74 tok/s and I got 77.

## Stuff That Went Wrong

- My first agent test ran with the lid closed. The Mac overheated and put itself to sleep (a thermal emergency). Then it slowed its GPU down to 338 MHz, about 5x slower. Docking it with the lid open fixed it.
- My 60 W charger couldnt keep up. The battery went from 100% to 34% during one 2-hour task.
- Background apps (browser tabs, YouTube) barely mattered. Results moved by only a few percent between runs.
- MLX ran out of memory until I told it to keep only one copy of the conversation.
- lithos sends back an empty "success" reply when a prompt is too long instead of an error. So an agent just gets nothing.
- Homebrew wouldnt install lithos until I updated Apple's Command Line Tools to 27 and removed an old Xcode.

## Fixes to My Older Notes

Both of these are now corrected in the notes themselves.

- My LLM Benchmark Registry note says the M5 Pro has about 400+ GB/s memory bandwidth. I measured about 290 GB/s here.
- My Qwen3.8-27B note says speculative decoding was a dead end on this Mac. With Splash's draft model it wasnt. It was about 4.5x faster than plain MLX on code (77 vs 16).

## The Honest Verdict

Splash wins by a lot. lithos isnt usable for coding agents on this Mac. MLX works but is roughly 3 to 4x slower than Splash on real agent work (estimated from my measurements).

But even with Splash, 40 minutes to 2 hours per coding task is too slow for what I need. I'm moving my local AI work to my Omarchy machine.

## Related

- [[Qwen3.8-27B]]
- [[LLM Benchmark Registry - Mac vs Unraid]]
- [[Local AI Stack Research - Gemma 4 on M5 Pro]]

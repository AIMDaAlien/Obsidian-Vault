---
type: hardware-decision
topic: MASSIVE-RIG GPU upgrade
updated: 2026-09-23
category: Rig & Hardware
tags: [rig, hardware, gpu, decision, local-ai]
publish: true
created: 2026-09-23
machine: bigrig
title: "Dual Tesla P100 vs a 2nd RX 9060 XT"
featured: 22
summary: "Two used datacenter GPUs or one more consumer card for a home AI box: the numbers behind the choice."
---
# Dual Tesla P100 vs a 2nd RX 9060 XT

**Category:** [[Rig & Hardware]] · **Vault:** [[Vault Map]]

Advisory session (2026-09-16) on how to add GPU capacity to the rig.

## Verdict

**Buy the 2nd RX 9060 XT, not dual P100.** Dual P100 is the same ~32 GB in a strictly worse form.

## Why P100 loses here

- **Power**: 250 W each over a single **EPS-12V (CPU-style) 8-pin**, not a GPU 8-pin. Two = 500 W GPU load, ~650 W with the 9060 XT present → 1000 W-class PSU.
- **Cooling**: PCIe P100s are **passive** datacenter bricks — they need shroud fans or printed ducts or they throttle immediately.
- **NVLink buys nothing**: llama.cpp layer splits don't use P2P, and modern vLLM tensor-parallel won't run on Pascal.
- Legacy-driver lock-in on Arch, zero resale value, **no MTP / no prefill advantage**, decode ~10–15% worse than the 9060 XT path.
- Second card would land in the x4 Gen3 slot — already proven to cost ~nothing at layer-split sizes ([[Rig Hardware & Display]]).
- Live pricing could not be verified (search backend unconfigured, eBay + DDG bot-blocked); market history ≈ **$100–180 each** used.

Only sensible as a cheap capacity sandbox for 30–70 B Q4/Q5 curiosity — not a daily agent rig.

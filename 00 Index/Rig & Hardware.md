---
type: moc
category: Meta
tags: [meta, moc, rig, hardware]
updated: 2026-09-23
publish: true
created: 2026-09-23
machine: bigrig
title: "Rig & Hardware"
---
# Rig & Hardware

The physical machine: what it is, how it is wired, what limits it, what breaks it.

**Vault:** [[Vault Map]]

## Notes

- [[Rig Hardware & Display]] — MSI Z690-A / i5-13600K / 62 GB / 9060 XT + 3060 + UHD 770. Display stuck at 1440p120 (HDMI FRL), per-GPU speed physics, **permanent crash rules**. Start here.
- [[GPU Crash & Vulkan Device Pinning]] — why llama-server SIGABRTs: the iGPU ends up as Vulkan0. Fix = `GGML_VK_VISIBLE_DEVICES`. Required reading before touching serve flags.
- [[Fan Control (MSI Z690-A)]] — chassis-fan curves from Linux. **Blocked**: no hwmon fan chip until `acpi_enforce_resources=lax` is added to `/etc/kernel/cmdline` and the box reboots.
- [[Incident 2026-10-25 — Unraid shares never mounted]] — **incident write-up**: after an unclean restart the user shares never mounted, Docker came up empty in RAM, and a plugin's endless loop blocked every array start. No data lost; root cause, timeline, follow-ups.
- [[Dual Tesla P100 vs 2nd 9060 XT]] — GPU upgrade advisory (verdict: buy the 2nd 9060 XT).
- [[Raspberry Pi B+ Utility Node]] — spare 2014 Pi: zero AI value, viable as a 2.5 W power-draw/logging node; includes the Cactus Needle 3 small-model survey.

## Relevance ordering

Hardware → [[Rig Hardware & Display]] (facts + rules) → [[GPU Crash & Vulkan Device Pinning]] (how it fails) → serving lives in [[Models & Serving]] → numbers land in [[Benchmarks]].
Two notes here are **decision notes**, not facts: [[Dual Tesla P100 vs 2nd 9060 XT]] and [[Raspberry Pi B+ Utility Node]] — both answer "should I buy/use this", both point back at the rig's real constraints.

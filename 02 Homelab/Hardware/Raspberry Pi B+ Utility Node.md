---
type: hardware-decision
topic: Raspberry Pi 1 B+
updated: 2026-09-23
category: Rig & Hardware
tags: [hardware, iot, decision, small-models, raspberry-pi, pihole, monitoring, backup]
publish: true
created: 2026-09-23
machine: bigrig
title: "Raspberry Pi B+ (2014) as a Utility Node"
featured: 24
summary: "What a 2014 Raspberry Pi can still usefully do in a modern home lab, and what it cannot."
---
# Raspberry Pi B+ (2014) as a Utility Node

**Category:** [[Rig & Hardware]] · **Vault:** [[Vault Map]]

Verdict on a spare 2014 Pi B+ 512 MB (2026-09-22).

## Hardware reality

- The 2014 B+ is **ARMv6** (ARM1176 @700 MHz, single core, no NEON, VFPv2 only) — not ARMv7 — and is officially EOL. ~0.5 GFLOPS vs the rig's GPUs (~30,000x). **Zero AI value**; below the floor for anything llama.cpp-shaped.
- 100 Mbps Ethernet + USB 2.0 → a poor bulk backup target (fine for text/JSON).
- 2014-era SD cards die — image the card and keep a spare.

## OS

**Don't use stock Debian (dropped armv6)** — **DietPi v10.5** still ships active ARMv6 images (Bookworm/Trixie, June 2026) with one-command Pi-hole/Mosquitto/NUT installs.
A used **Pi Zero 2 W (~$20)** does every job better and is the right architecture for the automation-agent idea.

## Viable 24/7 roles

Rig watchdog (`:8080/health` poll → notify), Pi-hole (~50 MB), nightly rsync of the Obsidian vault + bench-results + configs, native-UART serial-console lifeline, NTP, WOL sender, Mosquitto MQTT broker (~10 MB), nginx "rig vitals" LAN page polling `llama-server /health` + `nvidia-smi` over SSH, GPIOzero start-benchmark button + LED status.

**Best pick (converges the user's two asks):** the Pi logs power at 1 Hz while the rig publishes `bench START/END <id>` over MQTT, so it stamps a power trace per benchmark and prints e.g. *"Flash-Next IQ4 16.9 t/s run: 0.41 kWh, $0.07, avg 310 W"* → dollars-per-benchmark in [[Model Benchmarks]].

## Rules

- Filter: if it fits a cron job + tiny C tool + one shell script it belongs on the Pi; if it needs Node.js, Docker or a web framework it doesn't.
- Skip list: Zigbee hubs, Home Assistant, Node-RED, Docker, WireGuard/Tailscale, any DB but rrdtool, Java/Electron, cameras beyond stills.
- **One role per SD card**, DietPi image, imaged spare card on hand.

## Related — tiny automation models

**Cactus Needle 3** (released ~Sep 2026) is real: 25–121 M params at 2-bit, 8–29 MB binaries, **no chat by design** — tool calls + structured JSON extraction + embeddings only. Schemas are compiled into a byte-level grammar so JSON always parses and enums can't leave the set; a calibrated confidence gate refuses (`[]`) under 0.1 — *act high / show-and-ask mid / refuse low*, the same philosophy as [[RAFT Laya Router]]. Mobile Actions (exact call): 20L-121M **86.0** vs DeepSeek V4 Flash cloud 88.4, LFM2.5 1.2B 82.4, Qwen3.5 0.8B 76.0, FunctionGemma 270M 65.1.

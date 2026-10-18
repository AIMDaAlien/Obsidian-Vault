---
type: troubleshooting
topic: MASSIVE-RIG fans
status: blocked on reboot
updated: 2026-09-23
category: Rig & Hardware
tags: [rig, hardware, fans, blocked]
publish: true
created: 2026-09-23
machine: bigrig
title: "Fan Control (MSI Z690-A)"
---
# Fan Control (MSI Z690-A)

**Category:** [[Rig & Hardware]] · **Vault:** [[Vault Map]]

Chassis fans on the rig run at constant speed; the goal is idle-low with a ramp on CPU/GPU load, controlled from Linux (2026-09-21).

## Where it is stuck

- `modprobe nct6775` → **"No such device"** (not a Nuvoton chip despite the board-family guess). `it87` also found nothing; an SMBus scan was empty.
- hwmon inventory with **no fan chip**: `hwmon0 acpitz`, `hwmon1 nvme`, `hwmon2 amdgpu`, `hwmon3 iwlwifi_1`, `hwmon4 coretemp`.
- `dmesg` shows nothing → consistent with **ACPI silently claiming the fan-chip ports**.

## Next step (needs one reboot)

1. Add **`acpi_enforce_resources=lax`** to **`/etc/kernel/cmdline`** — this is the correct edit target; Omarchy's limine-entry-tool regenerates `limine.conf` from it, so it survives kernel updates. Editing `/boot/limine.conf` directly silently no-ops (and `/boot` is root-only).
2. Reboot, `modprobe nct6775`, look for an `nct679x` hwmon, then `sensors` output drives the idle-low/ramp-on-load curve.
- Bootloader: Limine ("Omarchy Bootloader"), `/boot/limine.conf` + `limine.conf.old`; kernel 7.2.3-arch1-3.
- Scripts staged: `~/fan-phase1.sh` … `~/fan-phase6.sh`, `~/fan-showconf.sh` (`fan-phase6.sh` is the cmdline edit).
- **Fallback**: set Smart Fan curves in the MSI BIOS — works, but no Linux-side control.

## Related

[[Rig Hardware & Display]] · [[Omarchy Trim Debloat & Idle Policy]]

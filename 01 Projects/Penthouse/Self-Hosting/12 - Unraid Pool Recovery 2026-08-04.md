---
tags: [self-hosting, unraid, zfs, docker, recovery, penthouse, security, reliability, storage, homelab]
created: 2026-08-04
updated: 2026-08-04
publish: true
featured: 11
project: Penthouse
summary: "A home server went dark after a storage reshuffle; the cause was two lost drive-pool assignments, and the fix restored them with no data loss."
---

# Unraid Pool Recovery - 2026-08-04

## Incident

The public Penthouse site and API were offline because Docker was stopped and Unraid was no longer presenting `/mnt/user/appdata` or `/mnt/user/system/docker/docker.img`.

DNS was not the active fault. `penthouse.blog` and `api.penthouse.blog` correctly resolved to the current WAN address `<wan-ip>`. The Cloudflare screenshot showing `<wan-ip>` was stale.

## Root cause

The August 3 array reconfiguration had lost the assignments for two existing ZFS pools:

- `cache` on the Samsung NVMe
- `downloads` on the WD Black NVMe

Both pools were still healthy and importable. Their data had not been formatted or lost. Without the registered `cache` pool, Unraid could not mount the Docker image or the Penthouse application data.

Two abandoned recursive `grep` jobs were also holding files open on disk1 and disk4, which briefly prevented a clean array stop. They were read-only searches and were terminated.

## Recovery performed

- Connected to Unraid at `<lan-ip-5>` using the dedicated deployment SSH key.
- Backed up the active flash configuration before changing pool assignments.
- Re-imported `cache` and `downloads` without formatting or rebuilding.
- Restored the pool assignments by their existing device identities and ZFS UUIDs.
- Stopped and restarted the array through Unraid's normal control path.
- Confirmed `/mnt/cache`, `/mnt/downloads`, `/mnt/user`, and the Docker image returned.
- Docker restarted and the existing Compose containers auto-started.

Recovery backup:

`/boot/config/hermes-backups/recovery-20260804-1455`

## Verification

- Unraid array: started, clean, configuration valid.
- `cache` ZFS pool: ONLINE, zero read/write/checksum errors, no known data errors.
- `downloads` ZFS pool: ONLINE, zero read/write/checksum errors, no known data errors.
- Postgres, API, and Caddy containers: running and healthy with zero restarts after recovery.
- Caddy listeners restored on host ports `9080` and `9443`.
- `https://penthouse.blog/`: HTTP 200.
- `https://api.penthouse.blog/api/v1/health`: HTTP 200 with database reachable.
- Public revision: `3a6f013`.
- Every CSS and JavaScript asset referenced by the live homepage returned HTTP 200 with the correct content type, including `/_app/env.js`.

No application source, deployment revision, or production data was changed during recovery.

## Open maintenance risk

Unraid logged XFS corruption on `md4p1` on August 3:

`XFS (md4p1): Corruption detected. Unmount and run xfs_repair`

Penthouse runs from the healthy `cache` pool, so this did not prevent the service recovery. Disk4 still needs an offline `xfs_repair` during a planned maintenance window. Do not run repair against the mounted filesystem.

## Proof boundary

Chrome was not installed on the recovery Mac, so no real-browser automation ran during this infrastructure recovery. HTTP, asset, container, database, listener, and revision checks passed.


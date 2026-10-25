---
type: incident
topic: Unraid user shares failed to mount after an unclean restart
category: Rig & Hardware
created: 2026-10-25
updated: 2026-10-25
tags: [incident, postmortem, unraid, docker, homelab, portfolio]
publish: true
severity: medium
status: resolved (follow-ups open)
machine: bigrig
title: "Incident 2026-10-25: Unraid shares never mounted, every container \"vanished\""
---
# Incident 2026-10-25: Unraid shares never mounted, every container "vanished"

**Category:** [[Rig & Hardware]] · **Vault:** [[Vault Map]] · **Related:** [[Unraid LLM Control Center]]

**Summary.** After an unclean restart, the Unraid server started its array but never mounted its user-share
filesystem. Unraid then built a brand-new, empty Docker image in RAM, so all 22 containers (Immich, Home Assistant,
the LLM gateway, Syncthing and the rest) looked deleted for about an hour. No data was lost. The problem came from four
small faults stacked together: a backup job writing into an unmounted path, a plugin script with an infinite loop,
a missing default route, and an array that cannot start by itself. Diagnosed and fixed remotely, read-only first,
changing nothing that was not RAM-only or a copy of the boot configuration.

## Impact

| What | Effect | Duration |
|---|---|---|
| Docker (22 containers) | Docker tab empty; services down (photos, home automation, LLM gateway, file sync) | ~1 h (09:44–10:42) |
| Array / shares | offline overnight (expected, see below), then started without user shares | ~14 h + ~1 h |
| Cron jobs | vault publisher and DDNS updater failing every 5–15 min | overnight |
| Data | **none lost**: the real `docker.img` and all appdata were intact on the cache pool | — |

## Timeline (EDT)

| Time | Event |
|---|---|
| 10-24 18:05 | The workstation (BigRig) loses power abruptly mid-workload (separate, cause not determined). |
| 10-24 19:40 | Unraid restarts uncleanly (XFS log recovery on every disk at the next mount). The SAS disks only enumerate when hot-plugged, so the array stays **stopped**. |
| 10-25 03:17 | A daily backup job writes 481 MB into `/mnt/user0/backups/…`. With the array stopped that path is a plain folder on the **RAM root filesystem**. |
| (unknown) | The default route (configured gateway, added at 19:40:34 by `rc.inet1`) disappears. |
| 09:44 | Disks hot-plugged, array started. The user-share FUSE (`shfs`) never mounts: there is no `shfs` line in syslog, and emhttpd logs `getxattr … Operation not supported` on `/mnt/user/appdata`. Unraid creates a **new 96 GB `docker.img` and `libvirt.img` on rootfs**, and Docker starts with zero containers. The Unassigned Devices "array started" script starts waiting for the router. |
| ~10:10 | Detected: the LLM gateway refuses connections while an OpenAI-compatible endpoint is being wired up for a companion app. |
| 10:13–10:20 | Read-only diagnosis over SSH: disks OK, cache pool healthy, the real Docker image intact at `/mnt/cache/system/docker/`, `/mnt/user` is rootfs, and stray files exist under `/mnt/user0`. |
| 10:34 | Array Stop requested. It loops on `Retry unmounting user share(s)…` because `rmdir /mnt/user0` and `rmdir /mnt/user` fail ("Directory not empty"). |
| 10:34 | After verifying that no loop device, mount or process held them, the RAM-only contents were moved aside (`/root/stray-…`). The array stops at once. |
| 10:36–10:38 | Three Start clicks, each answered `cmdStart: already starting`. |
| 10:38 | Root of the hang: an emhttpd thread had been blocked in `pipe_read` for 54 min. The only holder of the pipe's write end was Unassigned Devices' `rc.started`, still looping on `sleep 1.0`. Its wait-for-gateway loop never increments its timeout counter, and the box had **no default route**. |
| 10:39:55 | Default route restored, identical to the boot configuration. The script logs `Using Gateway …` and exits. |
| ~10:42 | Array started: `shfs` mounted on `/mnt/user` and `/mnt/user0`, the real `docker.img` loaded, all 22 containers up. |
| 10:50 | The stray backup was copied onto the cache pool and verified file by file. The gateway was verified end to end with a real chat completion. |

## Root cause and contributing factors

1. **Writes into an unmounted share path.** The backup job writes to `/mnt/user0/...` without checking that the share
   is mounted. With the array stopped, that silently filled a folder on the RAM root filesystem.
2. **A non-empty mountpoint blocks the share mount** (the leading explanation, strongly supported but not proven).
   The share never mounted while those files were there, and both the stop and the next start worked as soon as the
   folders were emptied. The stop side shows the same mechanism directly: Unraid's own `rmdir` of the mountpoint failed.
3. **Unraid fails open.** Instead of refusing to start Docker without its share, emhttpd created a fresh image at the
   same path, on RAM. An empty Docker tab looks like data loss, and re-adding containers from templates at that point
   would have pulled fresh images into a throwaway disk.
4. **A plugin bug turned a missing route into a hang.** Unassigned Devices 2026.10.12, `scripts/rc.started`: the
   network wait loop is `while [ $seconds -le 120 ]` with no `seconds` increment, so "up to 120 s" means forever. It
   holds emhttpd's event pipe open, and the array cannot be started again.
5. **The default route vanished** after boot. Cause not yet determined.
6. **The array cannot auto-start** (SAS drives behind the LSI HBA must be hot-plugged), which left a ~14 h window
   for the backup job to write into an unmounted path.

## How it was diagnosed

- Started from the symptom (gateway port refused), not from the dashboard. `docker ps -a` was empty while
  `/mnt/cache/system/docker/docker.img` was 74 GB. That ruled out data loss and pointed at mounts.
- `df /mnt/user` showed `rootfs`, the deciding clue: the share path existed but nothing was mounted on it.
- For the stuck stop and start: read emhttpd's syslog, then its process tree (a zombie `emhttp_event` child), then
  per-thread `wchan` (`pipe_read`), then a scan of `/proc/*/fd` for the pipe inode, which found the one script holding it.
- Every change was either RAM-only (moving rootfs leftovers aside after checking for loop devices, mounts and
  `fuser` holders) or a restore of the configured state (the default route from `network.cfg`). No reboot, no
  deletion, no container re-creation.

## Follow-ups

- [ ] Backup job: refuse to run unless `mountpoint -q /mnt/user` (and write via `/mnt/user`, not `/mnt/user0`).
- [ ] Report the `rc.started` infinite loop to the Unassigned Devices maintainer (missing `seconds` increment).
- [ ] Find what removed the default route. Check `ip route` first if an array start ever hangs again.
- [ ] Consider a pre-start user script that aborts the array start when `/mnt/user` or `/mnt/user0` is non-empty.
- [ ] HBA: firmware P20.00.07 IT (planned) so the SAS disks enumerate at boot and the array can auto-start.
- [ ] Watch disk1 (HGST): 15 reallocated sectors, SMART still PASSED. No parity, so a failure would mean data loss.
- [ ] Delete the RAM copy under `/root/stray-…` (it disappears at the next reboot anyway).

## Lessons

- **Check what is mounted before believing what is missing.** An empty Docker tab plus an intact image on disk means
  a mount problem, not deleted data.
- **"Up to N seconds" loops need a counter that counts.** A one-line bug in a plugin turned a transient network fault
  into an array that would not start.
- **Jobs that write into share paths must check the mount.** On Unraid the path exists whether or not the share is
  there, and writes land in RAM.

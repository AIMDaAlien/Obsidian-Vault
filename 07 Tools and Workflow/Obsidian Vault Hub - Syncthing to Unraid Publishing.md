---
tags: [obsidian, syncthing, unraid, automation, publishing, privacy, knowledge-garden]
created: 2026-10-18
updated: 2026-10-18
publish: true
featured: 83
status: Live since 2026-10-18
system: Obsidian Notes Vault
summary: "How every device's notes flow to one Unraid hub that gates them for leaks and publishes the safe ones to my site every 15 minutes, with no git on the laptops."
blurb: "Every note I write on any machine lands on one home server, which checks it for private details and publishes the safe ones here."
---

# Obsidian Vault Hub: Syncthing to Unraid Publishing

Since 2026-10-18 no device runs git for notes. Each machine keeps its own Obsidian vault, Syncthing carries it to Unraid, and Unraid is the only thing that composes, checks, and publishes to the public [Obsidian-Vault](https://github.com/AIMDaAlien/Obsidian-Vault) repo that the portfolio's Knowledge Garden reads. This replaces the per-device setup in [[Obsidian Vault Git Sync]] and the manual two-vault workflow in [[Building a Privacy-First Obsidian Publishing System]].

## Why

- Syncing every device to every other device was an upkeep hassle. One hub, many spokes.
- Running git inside a live vault kept breaking (unrelated histories, half-merged notes, a stale launchd job).
- A single publisher means a single privacy gate. Nothing reaches GitHub without passing it.
- Bulk Syncthing traffic through Unraid's FUSE layer crashed the array once, so the hub lives on the cache pool and nothing in the pipeline touches the user shares.

## The flow

```text
Mac vault  --Syncthing send-only-->  Unraid /mnt/cache/vault/sources/m5pro
BigRig vault --Syncthing send-only-->  Unraid /mnt/cache/vault/sources/bigrig
                                              |
                              cron, every 15 min: publish.sh
                                              |
                          vault-publisher container (compose.py)
                                              |
            compose  ->  privacy gate  ->  curation  ->  manifest  ->  git push
                                              |
                       GitHub AIMDaAlien/Obsidian-Vault (main)
                                              |
                        Knowledge Garden reads garden-manifest.json
```

## The pieces

### Syncthing
- Each device's vault folder is **send-only**; the Unraid side is **receive-only**. Unraid can never write back into a laptop's notes.
- Folder ignores on the sending side: `.obsidian`, `.git`, `.github`, `.trash`, `.DS_Store`, `_private`. Plugin state and private notes never leave the device.
- The Unraid container mounts the cache path directly (`/mnt/cache/vault:/vault`), bypassing `/mnt/user`.
- The general Documents and Downloads backup is a separate pair of folders and stays out of the vault entirely.

### Compose job
- Code lives in the public repo under `.github/scripts/` (`compose.py` plus the `composelib` package, stdlib plus PyYAML, 186 tests).
- Runs inside a small `vault-publisher` Docker image on Unraid. Changes on GitHub do **not** take effect until the image is rebuilt, on purpose.
- Merges all source vaults into one tree, normalises line endings, skips symlinks, Syncthing metadata, and anything that would land on a protected path like the repo README.
- Asks Syncthing's API first. If a source folder is still scanning or syncing, the run waits for the next cycle rather than publishing a half-arrived note.

### Privacy gate
- Scans every file for public IPs, emails, phone numbers, keys, and a private list of terms (names, hostnames) kept outside the repo at `/mnt/cache/appdata/vault-publisher/vault-privacy-terms`.
- **Fails closed.** One hit anywhere and nothing is pushed. An Unraid notification names the file and the pattern.
- It is a gate, not an editor. It never rewrites a note. Fix the note, and the next cycle publishes.
- The gate catches patterns, not meaning. A family reference or a schedule still needs a human read before `publish: true`.

### Curation
- Mac notes carry their own `publish`, `featured` (integer rank), and `summary` (160 chars max) in frontmatter.
- BigRig notes have no frontmatter conventions, so their ranks and summaries live in `/mnt/cache/vault/curation.yml` on the hub (a copy is in the repo at `.github/unraid/curation.yml`).
- Ranks 1 to 10 fill the Knowledge Garden's featured strip. Everything ranked below that is the "useful tier" and still searchable. Duplicate ranks fail the run.

### Publish
- The hub keeps a clone at `/mnt/cache/vault/published` and pushes with a write-only deploy key.
- The commit is authored by a no-reply identity, never a personal email.
- If a previous local commit never made it upstream, it is discarded and recomposed from sources rather than merged.
- A hard 45-minute timeout and a file lock keep overlapping runs from stacking up.

## Operating it

| Want to | Do |
|---|---|
| Publish a note | Write it in Obsidian. Nothing else. It is live within about 20 minutes. |
| Keep a note private | `publish: false` in frontmatter, or put it under `_private/` |
| Feature a Mac note | Add `featured: <rank>` and a `summary` |
| Feature a BigRig note | Edit `curation.yml` on the hub |
| Add a private term | Edit `~/.vault-privacy-terms` on the Mac, then copy it to the hub path above |
| See what the last run did | `cat /mnt/cache/vault/last-run.md` on Unraid |
| Read a full log | `/mnt/cache/vault/logs/publish-YYYY-MM-DD.log` |
| Run it by hand | `/mnt/cache/appdata/vault-publisher/bin/publish.sh` as root |
| Update the publisher code | Pull the repo on Unraid, rebuild the `vault-publisher` image from `.github/unraid/Dockerfile` |

## When it needs a human

1. **A failed run.** The notification says which note and why. Fix the note.
2. **A new name or hostname** that should never be public. Add it to the terms file and recopy.
3. **Content the gate cannot judge.** Personal details, other people's names, anything you would not say on a stage.
4. **A paused or errored Syncthing folder.** The job refuses to publish from a folder in that state and notifies.

## Lessons

- Put the hub on a plain disk path. FUSE overlays and bulk sync traffic do not mix.
- Fail closed. A publisher that quietly skips one bad file will eventually quietly skip the wrong one.
- Separate "what is published" (frontmatter and curation) from "what is checked" (the gate). Ranking is a taste decision; leaking is not.
- Keep the thing cron executes outside anything the synced or cloned code can write to.

## Related
- [[Obsidian Vault Git Sync]] (superseded)
- [[Building a Privacy-First Obsidian Publishing System]] (the original two-vault idea this grew from)
- [[Syncthing]]
- [[01 - Services Dashboard]]

---
tags: [index]
created: 2026-02-08
publish: true
---
# Knowledge Base Vault

Personal knowledge vault, read by Obsidian locally and published to the portfolio Knowledge Garden on GitHub Pages.

Start at [[Index]]. Notes are organized by category:

- 01 Projects - per-project documentation, indexes, and handoffs
- 02 Homelab - server inventory, network, services, logs
- 03 AI and Local Models - model research, benchmarks, serving notes
- 04 Programming - language and CS concept notes
- 05 Linux and Systems - Linux command line and OS notes
- 06 Learning Journals - reflective writeups and lessons learned
- 07 Tools and Workflow - Obsidian, publishing, business bridges

A note is published when its frontmatter has `publish: true`; everything else stays out of the garden, and a privacy gate blocks any push that contains an address, key, or personal identifier.

## How this vault is published

Notes live in two source vaults on two machines. Syncthing delivers each one, receive-only, to an Unraid server. A compose job runs every 15 minutes: it merges the sources, applies `curation.yml`, runs the privacy gate, and pushes the result here.

Never edit this repository directly. The next compose run overwrites any change made here.

Curation overrides (featured rank, summary, publish) for notes from the BigRig live in `curation.yml` on the Unraid hub and are copied into this repo on every publish. `blurb` is an optional plain-language line of up to 400 characters, shown above a note in the garden's reader mode. `add_tags` appends tags a BigRig note lacks, for example `[benchmark]`.

The publisher's secrets (its deploy key, SSH known_hosts and the privacy terms list) live only on the Unraid host, outside this repository.

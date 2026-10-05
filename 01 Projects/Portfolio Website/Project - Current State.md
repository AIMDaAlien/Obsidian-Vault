---
tags: [portfolio, web-development, knowledge-garden, homelab, github-pages, website-rebuild, reliability, hardware-constraints, portfolio-piece, checklist]
created: 2025-10-26
updated: 2026-08-01
published_to_garden: true
visibility: public
---

# Portfolio Website — Current State

## What the project is now

The portfolio is a small, framework-free website that presents my work as a living systems dashboard rather than a static résumé. It combines project writing, a public view of my Obsidian Knowledge Garden, and a deliberately limited snapshot of my homelab's health.

- **Live site:** [portfolio.penthouse.blog](https://portfolio.penthouse.blog/)
- **Repository:** [AIMDaAlien/First-Portfolio-Iteration](https://github.com/AIMDaAlien/First-Portfolio-Iteration)
- **Stack:** vanilla HTML, CSS, and JavaScript on GitHub Pages
- **Visual direction:** dark Material 3 Expressive with a pastel periwinkle palette

The lack of a framework and build process is intentional. The site is small enough to ship as plain files, which keeps deployment understandable, avoids dependency maintenance, and makes the source easy to inspect.

## What changed in the 2026 redesign

### A clearer picture of the systems I use

The main page now explains the role of each machine in the wider setup: the Unraid server, daily-driver Mac, Windows workstation, Raspberry Pi 5, and M80q. The descriptions focus on why each machine exists and how it fits into real work instead of listing hardware without context.

The intent is to show practical systems thinking. A visitor should be able to understand which machine handles storage and services, which machine handles daily creative and local-AI work, and where specialized or backup workloads belong.

### Live, privacy-limited Unraid telemetry

The systems section now displays current CPU use, memory use, storage use, array status, and uptime. The server publishes a small sanitized JSON snapshot every five minutes, and the portfolio refreshes it while the page is visible.

This is operational telemetry, not visitor analytics. The public response deliberately excludes hostnames, IP addresses, disk serials, mount paths, credentials, and other details that would expose the private network. Its purpose is to prove that the infrastructure is real and maintained without turning the portfolio into an observability or security risk.

### A Knowledge Garden that stays current

The Knowledge Garden reads a generated manifest from the public Obsidian vault. The terminal page uses that manifest to build the file tree, featured notes, graph, and note metadata. The home page also uses it for its note count and Latest Transmissions list.

Both pages check for updates every five minutes. Cached data remains available if GitHub is temporarily unavailable, and raw/API fallbacks prevent one failed request from making the garden unusable.

The intent is to make the portfolio reflect ongoing work automatically. Publishing a safe note to the vault should update the garden without manually editing the website.

### Better activity timestamps

Latest Transmissions now shows elapsed time with useful detail, such as `42m ago`, `7h 18m ago`, or `1d 13h ago`. Notes with the same source timestamp are marked as part of the `same update batch` instead of repeating an identical time several times.

This keeps the activity feed honest. Some Obsidian notes only record a date rather than an exact time, so the interface avoids pretending that those notes have precision the source data does not contain.

### A stable public address

GitHub Pages now serves the site from [portfolio.penthouse.blog](https://portfolio.penthouse.blog/) with HTTPS enforcement. The DNS record remains DNS-only so GitHub Pages can manage the certificate and edge delivery directly.

The custom address makes the project feel like part of the wider Penthouse environment while keeping deployment simple and reversible.

## How information moves through the project

### Knowledge Garden publishing

1. A note is written in the private Obsidian vault.
2. Only content intended for the public garden is allowed into the public vault workflow.
3. The public vault is pushed to GitHub.
4. GitHub Actions regenerates `garden-manifest.json`.
5. The portfolio notices the new manifest during its next five-minute refresh.

See [[Building a Privacy-First Obsidian Publishing System]] for the privacy model behind this flow.

### Server telemetry

1. Unraid creates a minimal JSON health snapshot every five minutes.
2. The file is published through the existing Penthouse web server.
3. The portfolio fetches that public file and updates accessible gauges.
4. If the feed is unavailable, the page reports that the signal is unavailable rather than inventing values.

## Current operating state

- [x] Material 3 Expressive redesign deployed
- [x] Machine hierarchy and purpose documented on the home page
- [x] Sanitized Unraid telemetry live
- [x] Knowledge Garden manifest refresh automated
- [x] Recent vault activity refresh automated
- [x] Recent-note timestamps made more precise
- [x] Custom subdomain and HTTPS enabled
- [x] Live site, telemetry, and Corne project notes verified in a real browser

The deployment containing the domain and timestamp refinements is portfolio commit `f015dc3`.

## Next moves

These are deliberately ordered by value and scope:

1. **Finish the terminal's filesystem commands.** Add `ls`, `cd`, `pwd`, `head`, `find`, `grep`, and `tree` so the terminal behaves like a useful browser rather than a themed command prompt.
2. **Replace the favicon placeholder.** Give the main page and Knowledge Garden a consistent AIM.EXE icon.
3. **Update the dynamic-content technical note.** Explain that the manifest is now the primary source and GitHub's API is a fallback.
4. **Run a focused cross-browser and mobile pass.** Check keyboard use, reduced motion, narrow screens, live refresh behavior, and stale-cache fallbacks.
5. **Keep optional features optional.** Analytics, a contact-form service, a PWA, and a separate blog should only be added when they solve a real need; none is required for the current site.

## Superseded history

This note replaces the October 2025 sidebar handoff and rollback log that previously lived here. That work was useful history, but its old files, colors, animation rules, and unresolved folder state no longer described the deployed site. Git history preserves those details if they are needed later.

---

*Last updated: 2026-08-01*

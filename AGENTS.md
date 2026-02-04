# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository type / purpose
This repository is an **Obsidian vault** (Markdown-first knowledge base). Most changes are edits to `.md` notes, plus Obsidian configuration under `.obsidian/`.

## Key entry points
- `🗺️ Knowledge Base - Main Index.md`: main “command center” / MOC (maps out learning tracks, tag system, and search patterns).
- `Project - Current State.md`: scratchpad-style project/status updates; often references work happening in *other* repos/paths.

## High-level structure (big picture)
This vault is organized by “domains” rather than a single application codebase:
- `Projects/`: long-form project documentation. Many projects contain their own README-style index note (e.g. `Projects/TypingLab/README.md`).
- `IT Projects/`, `Router Configuration/`, `Data Center Technicals/`: infrastructure/how-to notes.
- `Technical/`: general technical references (e.g. tools, workflows).
- `Learning/`, `Meta/`, `Sessions/`: learning materials, meta notes, and session logs.
- `images/`: central attachment folder for embedded images (configured in `.obsidian/app.json`).

The repo also contains `.base` files (e.g. `Vault Index.base`) used by Obsidian’s “Bases” feature.

## Obsidian configuration that affects edits
- Attachments are stored in `images/` (`.obsidian/app.json` has `attachmentFolderPath: "images"`). When adding images/assets, place them there and reference them from notes.
- Links are expected to stay correct when files move (`alwaysUpdateLinks: true` in `.obsidian/app.json`). Prefer Obsidian-style wikilinks (`[[...]]`) and keep note renames/moves consistent.
- `.gitignore` excludes ephemeral Obsidian state like `.obsidian/workspace.json` and `.obsidian/workspace-mobile.json`.
- Private content is kept out of the published vault via `.gitignore` (notably `Myself/`, `Business/`, and `Career/`).

## Plugins to be aware of
`.obsidian/community-plugins.json` enables several community plugins that affect workflows and/or automation:
- `obsidian-git`: Git integration inside Obsidian.
- `obsidian-local-rest-api`: exposes notes via a local REST API (desktop-only) for automation.
- `execute-code`: running code blocks from notes.
- `obsidian-spaced-repetition`: flashcards/spaced repetition content.
- Other UX/editor helpers (emoji toolbar, word count, image zoom, syntax highlighting, etc.).

When editing plugin settings/config, be cautious about accidentally committing machine-specific state (workspaces) or secrets.

## Common commands (repo maintenance)
There is no build/lint/test pipeline in this repository (it’s primarily Markdown + Obsidian config). These commands are the ones typically useful while working here:

### Git
```bash
git --no-pager status -sb
git pull --rebase
git add -A
git commit -m "docs: ..."
git push
```

### Search across notes
```bash
rg "search term" .
rg "#tag" .
```

### Inspect recent changes
```bash
git --no-pager log -n 20 --name-only
```

## Project notes vs. code repos
Some notes document external software projects and may include commands like `npm run dev` or references to files under other directories (example: `Project - Current State.md` references `/Users/aim/Documents/First Portfolio Iteration/`). Treat those as **documentation about other repos**, not commands you can run in this vault.

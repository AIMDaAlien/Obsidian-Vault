---
created: 2024-11-28T16:30:00
modified: 2024-11-28T16:30:00
tags:
  - mcp
  - obsidian
  - privacy
  - automation
  - publishing
  - technical
visibility: public
privacy_scan: not_scanned
published_to_garden: false
---

# Building a Privacy-First Obsidian Publishing System

So you've got an Obsidian vault full of notes—some public-worthy, some definitely not—and you want to share the good stuff without accidentally leaking your homelab IPs or API keys. Here's how I built a system that handles this automatically.

## The Problem

I had two vaults:
- **Main vault**: My messy workspace with everything (personal plans, credentials, project docs, tutorials)
- **Garden vault**: Public knowledge base that feeds my portfolio site

The workflow sucked. I'd manually copy notes over, hope I didn't miss anything sensitive, commit to git, push to GitHub. One mistake and my Venmo username or network setup gets published. Not ideal.

## What I Built

An MCP (Model Context Protocol) server that acts as a smart middleman between my main vault and the public garden. Think of it as a privacy-conscious assistant that:

1. **Scans notes for sensitive data** before publishing
2. **Auto-sanitizes content** (redacts IPs, credentials, personal info)
3. **Handles git commits** automatically
4. **Organizes the vault** (finds orphans, suggests tags, etc.)

## The Architecture

```
Main Vault (private mess)
    ↓
MCP Server (privacy guard)
    ↓  
Garden Vault (public, sanitized)
    ↓
GitHub → Portfolio Site
```

The MCP server sits on my machine, accessible via Claude Desktop. I can say "publish this note to my garden" and it'll scan, sanitize, copy, and commit—all while keeping me in the loop for review.

## Key Components

### Privacy Scanner

Uses regex patterns to catch:
- API keys and tokens (20+ char alphanumeric strings)
- IP addresses and MAC addresses
- Phone numbers and SSNs
- Custom patterns (Venmo URLs, work locations, etc.)

The scanner grades findings by severity:
- **High**: Credentials, SSNs → blocks auto-publish
- **Medium**: IPs, phone numbers → flags for review
- **Low**: Private comments → informational

### Hard-Blocked Folders

Certain folders never see daylight:
- `/Myself/` - Personal plans, credentials
- `/Career/` - Work stuff, client info  
- `/Sessions/` - Temporary notes

These are physically blocked. No scan needed, they're just off-limits.

### Git Automation

The part I was doing manually:
```python
def publish_with_git(note):
    scan_for_privacy_issues()
    sanitize_sensitive_content()
    copy_to_garden_vault()
    git_add()      # ← Automated now
    git_commit()   # ← Automated now
    # git push still manual - I control when it goes live
```

## My Workflow Now

**Before:**
1. Write note
2. Manually check for sensitive stuff (miss things)
3. Copy to garden vault
4. `cd garden-vault && git add . && git commit -m "Add note"`
5. Push, hope for the best

**After:**
1. Write note
2. "Claude, scan this for privacy issues"
3. Review the scan report
4. "Claude, publish to garden and commit"
5. Push when ready

The scanning catches stuff I'd miss—like that time I almost published my internal project codenames.

## Technical Stack

**MCP Server (FastMCP + Python):**
- `privacy_scanner.py` - Regex-based detection
- `publisher.py` - Publish workflow with git
- `note_operations.py` - CRUD for notes
- `organizer.py` - Vault analysis

**My Setup:**
- Static HTML portfolio (Material Design 3)
- GitHub repo for garden vault
- Client-side markdown parsing with marked.js
- No build step, just git push and it updates

## Configuration

The `config.yaml` holds everything:
```yaml
vaults:
  main: /path/to/obsidian-notes
  garden: /path/to/knowledge-garden

privacy:
  private_folders: ["/Myself", "/Career"]
  sensitive_patterns:
    - "api[_-]?key\\s*[=:]\\s*['\"]?[a-zA-Z0-9]{20,}"
    - "\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b"
    - "venmo\\.com/u/"
```

I added custom patterns for my specific situation—work stuff, student info, business details.

## Lessons Learned

**Privacy scanning isn't perfect.** It catches obvious stuff (IPs, keys) but misses context. Like, a tutorial about Docker might mention my homelab setup in a way that's technically identifying but not flagged. Human review is still critical.

**Separation of concerns works.** Having physically separate vaults (main vs garden) adds a layer of safety. Even if the scanner misses something, it's not in the garden vault yet.

**Git automation saves time but keep manual push.** Auto-committing is convenient, but I still push manually. Gives me a chance to `git diff` and catch anything weird before it goes public.

**Start conservative.** My scanner flags a lot. That's good. Better to manually approve false positives than to auto-publish a false negative.

## Future Improvements

Things I'd add if I keep iterating:

- **Image EXIF scanning** - Photos can leak location data
- **ML-based classification** - Smarter content categorization  
- **Web review interface** - GUI for batch approvals
- **Vault sync suggestions** - Auto-detect notes that should be public

## Why This Matters

The internet is forever. One accidental leak of personal info or credentials can cause headaches. This system lets me share knowledge freely while keeping the private stuff actually private.

Plus, it's just faster. I publish more now because the friction is gone. That's the real win—actually sharing useful stuff instead of hoarding it all in a private vault.

## The Stack

- **Obsidian**: Knowledge base
- **FastMCP**: MCP server framework
- **Claude Desktop**: Interface to MCP
- **Git**: Version control
- **GitHub**: Hosting
- **Static HTML**: Portfolio site (no build, just JS)

## Getting Started

If you want something similar:

1. Set up separate vaults (main + public)
2. Build an MCP server with privacy scanning
3. Configure Claude Desktop to use it
4. Test thoroughly with safe notes first
5. Add custom patterns for your situation
6. Publish with confidence

The code's not perfect, but it works. And it's saved me from at least three potential "oh shit" moments so far.

---

*Built this because I was tired of the manual workflow. Figured others might find it useful too.*

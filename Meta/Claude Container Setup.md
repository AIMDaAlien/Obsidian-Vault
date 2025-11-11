# Claude Container Setup

## File Access Discovery

**Date:** 2025-11-08

### What Works
- **Filesystem tools** → Direct access to `/Users/aim/Documents` and `/Users/aim/Downloads`
- **osascript** → Runs commands on host Mac (git, npm, terminal commands)
- **MCP Docker** → Obsidian vault access via containerized tools

### What Doesn't Work
- **bash_tool** → Isolated in Linux container at `/`, cannot see Mac files
- Container only mounts `/mnt/user-data/outputs` and `/mnt/user-data/uploads`

## The Solution: Hybrid Approach

```
File Operations  → Filesystem:* tools (direct local access)
Git Operations   → osascript (runs on Mac)
Build/npm tasks  → osascript (runs on Mac)
Obsidian         → MCP_DOCKER:obsidian_* tools
```

### Verified Working
```bash
# Via osascript - Successfully tested
cd /Users/aim/Documents/3D-print-shoppe
git status
# Output: Clean working tree, on main branch
```

## Tool Environment Matrix

| Tool Type | Location | Can Access Local Files | Use For |
|-----------|----------|------------------------|---------|
| Filesystem:* | Host Mac | ✅ Yes | File edits, reading code |
| osascript | Host Mac | ✅ Yes | Git, npm, terminal commands |
| bash_tool | Container | ❌ No | Container-only operations |
| MCP_DOCKER:obsidian_* | Container | ✅ Via mount | Vault management |

## Key Insight

Claude's container has a "split personality":
- Some tools see your Mac directly
- Others are containerized
- Choose the right tool for the right job

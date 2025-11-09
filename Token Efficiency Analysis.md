# Token Efficiency Analysis

## Workflow Options Comparison

**Date:** 2025-11-08

### Option 1: Hybrid Approach
**Tools:** Filesystem + osascript for git
```
File edit:     ~300 tokens
Git commands:  ~150-200 tokens
Total:         ~450-500 tokens per commit
```

**Best for:** Multiple file changes before committing

### Option 2: osascript Only
**Tools:** osascript for everything
```
File edit:     ~400-500 tokens
Git commands:  ~150-200 tokens
Total:         ~550-700 tokens per commit
```

**Best for:** Nothing, least efficient

### Option 3: Manual Git
**Tools:** Filesystem only, user runs git
```
File edit:     ~300 tokens
Git commands:  0 tokens (manual)
Total:         ~300 tokens per change
```

**Best for:** Single file changes or tight token budgets

## Token Budget Mechanics

### Initial Load vs Ongoing Use
- **System prompt:** ~25-26k (loaded once, not counted repeatedly)
- **User preferences:** ~1k (loaded once)
- **Per message:** Only new responses + tool calls consume budget

### Tool Call Costs
```
Filesystem read:   ~200 tokens
Filesystem write:  ~300 tokens
osascript:         ~150-200 tokens
bash_tool:         ~200-300 tokens
MCP_DOCKER:        ~200-300 tokens
```

## Decision

**Chosen approach:** Option 1 (Hybrid)
**Reasoning:** Amortizes well over multiple changes per session, automation benefit worth ~150-200 token overhead per commit

## Efficiency Tips

1. Batch file changes before committing
2. Use append operations over full file rewrites when possible
3. Read multiple files at once vs sequential reads
4. Minimize tool call round-trips

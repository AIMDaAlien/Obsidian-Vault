# Conversation Limit Avoidance Workflow

## The Problem

**Traditional approach:**
```
Hit conversation limit → Start new chat → "Continue previous conversation"
→ Claude searches past chats (10,000+ tokens)
→ Loads context (20,000+ tokens)  
→ Reproduces information (15,000+ tokens)
→ Total: 45,000+ tokens before doing anything
```

**Your power user reality:**
- Hit limits frequently
- Lose context between conversations
- Re-explain projects repeatedly
- Token budget wasted on context loading

---

## The Solution: Obsidian as External Memory

**New approach:**
```
During conversation → Document in Obsidian → Hit limit
→ Start fresh → Reference note (2,000 tokens)
→ Immediate work (3,000 tokens)
→ Total: 5,000 tokens to start working
```

**Token savings: 40,000+ per conversation start**

---

## The Workflow

### Phase 1: During Active Conversation

**As you work with Claude:**

1. **Document key information in real-time**
   - Create project notes as decisions are made
   - Save code snippets and configs
   - Record troubleshooting solutions

2. **Update "Current State" note**
   ```markdown
   # [Project] - Current State
   
   Last updated: [timestamp]
   
   ## Status
   - [x] Completed: Feature X
   - [ ] In progress: Feature Y  
   - [ ] Next: Feature Z
   
   ## Context
   Working on implementing Y.
   Blocked on: dependency issue
   
   ## Files Changed
   - src/components/Card.astro
   - public/styles/global.css
   ```

3. **Create topic-specific notes**
   ```
   Instead of one giant note:
   ❌ Project Everything.md (5000 lines)
   
   Use focused notes:
   ✅ Project - Setup.md
   ✅ Project - Design System.md
   ✅ Project - Troubleshooting.md
   ✅ Project - Current State.md
   ```

### Phase 2: Approaching Conversation Limit

**When you see: "Claude is approaching the limit"**

1. **Finalize current work**
   ```bash
   # Commit any code
   git add -A
   git commit -m "WIP: [current task]"
   
   # Save artifacts to files
   # Update notes with progress
   ```

2. **Create conversation summary**
   ```markdown
   # [Project] - Session [Date]
   
   ## Accomplished
   - Implemented X
   - Fixed Y bug
   - Researched Z approach
   
   ## Code Changes
   - File A: Added feature
   - File B: Refactored logic
   
   ## Decisions Made
   - Using approach A because B had issue C
   - Deferred feature D until after deployment
   
   ## Next Steps
   1. Implement remaining part of Y
   2. Test edge case Z
   3. Document configuration
   
   ## Blockers
   - Need to research library version compatibility
   ```

3. **Update Current State note**
   - Mark completed items
   - Add new blockers
   - List immediate next steps

### Phase 3: Starting New Conversation

**Don't:**
```
"Continue our previous conversation about [project]"
"Remember when we worked on [thing]?"
```

**Do:**
```
Task: [Specific next step]

Context: See notes:
- [[Project - Current State]]
- [[Project - Technical Setup]]

Current situation: [2 sentences max]

Next step: [Exactly what you need]

Use local filesystem tools.
```

**Example:**
```
Task: Implement image optimization for teardown.cafe

Context:
- [[Teardown Cafe - Current State]]
- [[Teardown Cafe - Technical Setup]]

Current: Images manually optimized with exiftool
Goal: Automate with sharp package on upload

Preserve EXIF stripping. Use local filesystem.
```

---

## Note Templates

### Project - Current State Template

```markdown
# [Project Name] - Current State

Last updated: [YYYY-MM-DD HH:MM]
Last conversation: [brief descriptor]

## Quick Status
[2-3 sentences: where project is, what's working, what's next]

## Task Status
- [x] Completed task
- [x] Another completed task
- [ ] Current task (50% done)
- [ ] Next task
- [ ] Future task

## Current Focus
**Working on:** [specific feature/fix]
**Started:** [date]
**Blocked by:** [none/issue description]

## Recent Changes
- [date] Implemented X
- [date] Fixed Y bug  
- [date] Refactored Z

## Next Conversation Tasks
1. Complete current focus item
2. Address blocker (if any)
3. Move to next task

## Files Recently Modified
- path/to/file1.ext - [what changed]
- path/to/file2.ext - [what changed]

## Environment Info
- Project location: [path]
- Framework version: [version]
- Last successful build: [date]
- Last git commit: [short hash]

## Notes for Claude
[Anything specific Claude should know when resuming]
```

### Project - Session Summary Template

```markdown
# [Project] - Session [YYYY-MM-DD]

## Goal
[What this conversation was supposed to accomplish]

## Accomplished
- Thing 1
- Thing 2
- Thing 3

## Code/Files Changed
- `path/file.ext` - [description]
- `path/other.ext` - [description]

## Decisions Made
- Decision A: Because reason X
- Decision B: After testing Y, chose Z

## Challenges & Solutions
**Challenge:** [problem encountered]
**Solution:** [how it was resolved]
**Confidence:** [Claude's confidence level]

## Research Conducted
- Topic A: [key findings]
- Topic B: [key findings]
- Sources: [links if applicable]

## Technical Details
[Any configs, commands, or snippets worth preserving]

## What Didn't Work
- Tried approach X: Failed because Y
- Considered option A: Rejected because B

## Next Steps
1. [Immediate next task]
2. [Following task]
3. [Future consideration]

## Blockers
- [None / Description of blocker]

## Confidence Levels
- Solution A: 95% - [reason]
- Approach B: 80% - [reason]
- Untested: Feature C - needs verification

## Links
- [[Project - Current State]] (updated)
- [[Project - Technical Setup]] (if updated)
- [[Project - Troubleshooting]] (if new issues)
```

---

## Organizational Structure

### Suggested Vault Layout

```
Obsidian Vault/
├── Meta/
│   ├── Claude Interaction Guidelines.md
│   └── Conversation Templates.md
│
├── Projects/
│   ├── [Project A]/
│   │   ├── Project A - Index.md
│   │   ├── Project A - Current State.md
│   │   ├── Project A - Technical Setup.md
│   │   ├── Project A - Design System.md
│   │   ├── Project A - Workflow.md
│   │   ├── Project A - Troubleshooting.md
│   │   └── Sessions/
│   │       ├── 2025-10-15 Session.md
│   │       ├── 2025-10-16 Session.md
│   │       └── ...
│   │
│   └── [Project B]/
│       └── ...
│
└── Archive/
    └── [Completed projects]
```

### Index Note per Project

```markdown
# [Project Name] - Index

## Quick Links
- [[Project - Current State]] ← **Start here**
- [[Project - Technical Setup]]
- [[Project - Design System]]
- [[Project - Workflow]]
- [[Project - Troubleshooting]]

## Project Overview
[2-3 sentence summary]

## Recent Sessions
- [[2025-10-16 Session]] - Implemented feature X
- [[2025-10-15 Session]] - Fixed bug Y
- [[2025-10-14 Session]] - Initial setup

## Key Decisions
- [Date] Decision A: Reason
- [Date] Decision B: Reason

## External Links
- Repository: [GitHub URL]
- Deployment: [URL if deployed]
- Documentation: [external docs]
```

---

## Conversation Patterns

### Pattern 1: Quick Task

**Estimated tokens: ~5,000**

```
Task: Fix bug in script X

Context: [[Project - Current State]]
File: /path/to/script.sh
Error: "line 42: syntax error"

Use local bash.
```

Claude:
- Reads Current State note (if needed)
- Examines file
- Fixes bug
- Tests
- Commits

No context loading needed.

### Pattern 2: Feature Implementation

**Estimated tokens: ~15,000**

```
Task: Add feature X to project Y

Context:
- [[Project Y - Current State]]
- [[Project Y - Technical Setup]]

Requirements:
1. Requirement A
2. Requirement B

Constraints:
- Must preserve existing behavior
- Privacy-first implementation

Use local filesystem.
```

Claude:
- References both notes
- Implements feature
- Updates relevant notes
- Creates session summary

Focused, efficient work.

### Pattern 3: Research + Implementation

**Estimated tokens: ~30,000**

```
Task: Research and implement Z

Context: [[Project - Current State]]

Current knowledge gap: [specific unknown]
Goal: Implement using current best practices

Research needed:
- Topic A compatibility
- Library B version requirements

Use local filesystem.
```

Claude:
- Conducts research
- Documents findings
- Implements solution
- Updates notes with new knowledge

Higher token use justified by research, but still efficient.

---

## Token Budget Comparison

### Old Approach (Conversation Search)

| Phase | Tokens |
|-------|--------|
| Search past conversations | 5,000 |
| Load context | 15,000 |
| Reproduce explanations | 10,000 |
| Actual work | 10,000 |
| **Total** | **40,000** |

### New Approach (Obsidian Reference)

| Phase | Tokens |
|-------|--------|
| Read referenced note | 2,000 |
| Actual work | 10,000 |
| Update notes | 3,000 |
| **Total** | **15,000** |

**Savings: 25,000 tokens (62.5%)**

---

## Real Example: Teardown Cafe

### What You Did Right

**Created comprehensive notes:**
- Project Overview
- Technical Setup
- Design System
- Content Workflow
- Troubleshooting
- Documentation Index

**Result:**
Next conversation about teardown.cafe can start:
```
"Add RSS feed to teardown.cafe

Context: [[Teardown Cafe - Technical Setup]]
Current: No RSS feed
Goal: Implement @astrojs/rss plugin

Use local filesystem."
```

**Token estimate: ~8,000 total**

Instead of:
```
"Continue our teardown website conversation"
→ 35,000+ tokens
```

---

## Maintenance

### Weekly
- Update Current State notes for active projects
- File completed session summaries
- Archive inactive projects

### After Each Conversation
- Create session summary
- Update Current State
- Commit any code changes
- Verify notes are complete

### Monthly
- Review organizational structure
- Merge redundant notes
- Update Index notes
- Clean up old sessions (move to Archive)

---

## Troubleshooting

### "Still hitting limits too fast"

**Check:**
- Are you batching related tasks?
- Creating session summaries?
- Updating Current State notes?
- Starting conversations with references?

**Solutions:**
- Combine multiple small tasks into one conversation
- Use more focused note references
- Keep Current State notes lean (<500 words)

### "Notes getting too large"

**Split by category:**
```
Before:
Project Everything.md (3000 lines)

After:
- Project - Setup.md (300 lines)
- Project - API.md (400 lines)
- Project - UI.md (350 lines)
- Project - Deploy.md (200 lines)
```

Reference only what's needed per conversation.

### "Can't find information"

**Use Obsidian search:**
```
[[Claude Interaction Guidelines]] → Cmd+O → "teardown"
→ Shows all teardown-related notes
→ Jump to relevant section
```

**Create better index notes:**
- Link to all related notes
- Include brief descriptions
- Tag appropriately

---

## Success Metrics

**You'll know it's working when:**
- Conversations start immediately productive
- Rarely hitting token limits
- Clear project continuity between chats
- Easy to resume work after days/weeks
- Other people could understand projects from notes

**Warning signs:**
- Still searching past conversations
- Repeatedly explaining same concepts
- Notes not being updated
- Unclear what to work on next

---

## Advanced: Multi-Project Management

### When Working on Multiple Projects

**Create master index:**

```markdown
# Active Projects Dashboard

## Priority 1 (This Week)
- [[Teardown Cafe - Current State]]
  Status: Adding RSS feed
  Next: Deployment

## Priority 2 (This Month)  
- [[Homelab - Current State]]
  Status: Pi-hole optimization
  Next: Monitoring setup

## Backlog
- [[Mech Keyboard - Current State]]
- [[3D Printing - Current State]]

## Quick Links
- [[Claude Interaction Guidelines]]
- [[Project Templates]]
```

**Starting conversation:**
```
Working on [Project A]

Dashboard: [[Active Projects Dashboard]]
Context: [[Project A - Current State]]

Current task: [specific item]
```

---

*This workflow transforms Claude from a forgetful assistant into a persistent team member with perfect memory through your Obsidian vault.*

---

*Created: October 16, 2025*
*Last updated: October 16, 2025*

## Tags
#workflow #obsidian #efficiency #token-optimization #project-management

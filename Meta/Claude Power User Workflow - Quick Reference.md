# Claude Power User Workflow - Practical Implementation

## Quick Start (Day 1: 30 minutes)

### Setup Obsidian Structure
```
Vault/
├── Meta/ (guidelines, templates)
├── Projects/ (active work)
└── Archive/ (completed)
```

### Install Token Counter
```bash
cd /Users/aim/Documents/claude-token-counter
pip3 install tiktoken
python3 token_counter.py
```

### Create First Project Notes
- Project - Index.md
- Project - Current State.md  
- Project - Technical Setup.md

---

## Core Workflow

### Starting Conversations (2 min)

**Template:**
```
Task: [Specific objective]
Context: [[Note reference]]
Current: [Brief state]
Goal: [Desired outcome]
Tools: [local/Obsidian MCP]
```

**Token cost:** ~500 vs ~30,000 (60x savings)

### During Work (Real-time)

1. Document decisions as made
2. Save code snippets
3. Track tokens (60% = start wrapping)
4. Commit progressively

### Before Limit (10 min at 70%)

1. Complete current task
2. Create session summary
3. Update Current State
4. Note next steps

### Fresh Start (30 sec)

```
Task: [Next from Current State]
Context: [[Current State note]]
```

Instant productivity, no context loading.

---

## Multi-Project Management

### Active Projects Dashboard

```markdown
# Active Projects Dashboard

## 🔥 Priority 1 (This Week)
- [[Project A - Current State]]
- [[Project B - Current State]]

## 📋 Backlog
- Ideas and future work

## ✅ Recently Completed
- Completed projects
```

### Context Switching

Don't: "Remember Project B?" (30K tokens)
Do: "Task: X. Context: [[Project B]]" (2K tokens)

**Savings per switch:** 28K tokens

---

## Communication Patterns

### Perfect First Message

**Bug fix:**
```
Task: Fix error in script.sh
Context: [[Project]]
Error: "line 42: syntax error"
Use local bash
```

**Feature:**
```
Task: Add RSS feed
Context: [[Technical Setup]]
Requirements: [list]
Use local filesystem
```

**Research:**
```
Task: Research image optimization
Context: [[Current State]]
Goal: Automate with sharp
Research first, then implement
```

---

## Tool Selection

```
Obsidian operations → MCP Docker
Project files → Local Filesystem
Git/npm → Local bash (verify pwd first)
```

**Before git:**
```bash
pwd  # Must show: /Users/aim/Documents/project
git status
```

---

## Token Counter Usage

1. Draft in counter
2. See live token count
3. Update conversation usage
4. Check projection colors:
   - 🟢 Green: Continue
   - 🟡 Orange: Wrap up
   - 🔴 Red: Document, start fresh

---

## Common Scenarios

**Quick question:** Direct ask (500-2K tokens)
**Debug:** Reference project + error (3-8K tokens)
**Major feature:** Single or phased (20-60K tokens)
**Learning:** With examples (5-15K tokens)
**Planning:** Create docs (10-20K tokens)

---

## Emergency Procedures

**Hit limit:**
1. Screen capture important info
2. Git commit code
3. Quick bullet notes
4. Start fresh with summary

**Lost context:**
1. Check Obsidian notes
2. Check git commits
3. Search past chats (last resort)

---

## Continuous Improvement

### Monthly Review
- Which projects hit limits?
- What strategies worked?
- Note structure improvements?
- Update guidelines

### Create Templates
Notice patterns → Create reusable templates

### Build Knowledge Base
Accumulate reference notes over time

---

## Success Metrics

**Before optimization:**
- 70K tokens per session (37% budget)
- ~2.7 conversations to limit
- Context loss, repeated explanations

**After optimization:**
- 42K tokens per session (22% budget)
- ~4.5 conversations to limit
- 67% more conversations possible

**You'll know it works when:**
- Rarely hit limits
- Resume seamlessly
- Clear progress
- Less explaining, more building

---

## Quick Checklists

**Starting:**
- [ ] Task clear?
- [ ] Notes referenced?
- [ ] Tools specified?

**During:**
- [ ] Documenting?
- [ ] Committing?
- [ ] Tracking tokens?

**Ending:**
- [ ] Code committed?
- [ ] Current State updated?
- [ ] Next steps clear?

---

## Core Principles

1. External memory beats re-explanation
2. Precision beats verbosity
3. Progressive beats perfect
4. Planning beats improvisation

**Start today:** Create dashboard → Pick project → Make Current State note → Reference in next chat → Experience difference

---

*Transforms Claude from tool to persistent collaborator with perfect memory via Obsidian.*

**Created:** October 16, 2025
**Success rate:** 67% more conversations
**Time to proficiency:** 2-4 weeks

#workflow #power-user #claude #obsidian #practical-guide

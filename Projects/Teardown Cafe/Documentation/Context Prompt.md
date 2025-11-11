---
tags: #prompt #context #claude #workflow
created: 2025-10-19
---

# Teardown Cafe - Context Establishment Prompt

## Quick Context Prompt (Copy/Paste for New Conversations)

```
Continue work on Teardown Cafe project. Read these Obsidian notes for context:

1. [[Teardown Cafe - Current State]] - Project status, recent changes
2. [[Teardown Cafe - Technical Setup]] - Framework, dependencies, file structure  
3. [[Teardown Cafe - Design System]] - Material You 3 tokens, colors, typography

**Quick context:**
- Location: `/Users/aim/Documents/teardown-cafe/`
- Framework: Astro v5.14.5
- Design: Material You 3, periwinkle (#B8B3FF) + teal (#00BCD4)
- Current features: Vertical progress bar, SVG icons, Focus Mode
- Last commit: [check git log]

**Working on:** [describe task]
```

## Extended Context (For Complex Tasks)

```
Working on Teardown Cafe. Context notes:

**Project Overview:**
- [[Teardown Cafe - Project Overview]] - Vision, tech stack
- [[Teardown Cafe - Current State]] - Status, commits, files

**For this task:**
- [[Teardown Cafe - Technical Setup]] - If code/config changes
- [[Teardown Cafe - Design System]] - If UI/styling work
- [[Teardown Cafe - Content Workflow]] - If adding teardowns
- [[Teardown Cafe - Troubleshooting]] - If debugging

**Lessons learned:**
- [[Teardown Cafe - Building Material You 3 Website Lessons]]

**Task:** [describe what you need]
```

## Task-Specific Context Triggers

**UI/Design work:**
```
Read: [[Teardown Cafe - Design System]], [[Teardown Cafe - Building Material You 3 Website Lessons]]
```

**Adding content:**
```
Read: [[Teardown Cafe - Content Workflow]]
```

**Technical debugging:**
```
Read: [[Teardown Cafe - Troubleshooting]], [[Teardown Cafe - Technical Setup]]
```

**New features:**
```
Read: [[Teardown Cafe - Current State]], [[Teardown Cafe - Technical Setup]], [[Teardown Cafe - Building Material You 3 Website Lessons]]
```

## Git Context Check

```bash
cd ~/Documents/teardown-cafe
git log --oneline -5
git status
```

## Why This Works

- **Token efficient:** Direct note references instead of conversation search
- **Targeted:** Only relevant context loaded
- **Current:** Obsidian notes stay updated
- **Fast:** Claude reads specific notes, no searching needed

---

**Usage:** Copy appropriate prompt → Paste in new conversation → Add your task

# 🔗 Obsidian Context Filter for Teardown Cafe

## Quick Context Setup

### Method 1: Tag-Based Filtering (Recommended)
Add this tag to relevant notes: `#teardown-cafe`

**In Obsidian:**
1. Open any note related to your teardown project
2. Add `#teardown-cafe` at the bottom
3. Use Obsidian's tag pane to see all tagged notes

### Method 2: Folder Structure
Create a dedicated folder: `Teardown Cafe/`

**Structure:**
```
Obsidian Vault/
├── Teardown Cafe/
│   ├── Project Overview.md
│   ├── Design System Notes.md
│   ├── Content Strategy.md
│   ├── Technical Decisions.md
│   └── Workflow Notes.md
```

### Method 3: MOC (Map of Content)
Create a master note: `Teardown Cafe MOC.md`

**Content:**
```markdown
# Teardown Cafe - Master Context

## Project Status
- Current phase: [Development/Content Creation/Design]
- Next tasks: [List 3-5 key tasks]
- Blockers: [Any issues]

## Key Notes
- [[Project Overview]]
- [[Design System Notes]]
- [[Content Strategy]]
- [[Technical Decisions]]

## Recent Updates
- [Date]: [What was accomplished]
- [Date]: [What was accomplished]

## Handoff Notes
### For Claude:
- [Strategic decisions needed]
- [Content creation tasks]
- [Design system work]

### For Cursor AI:
- [Code fixes needed]
- [File operations]
- [Git management]
- [Component creation]
```

## Context Sharing Protocol

### When Starting with Cursor AI:
1. Copy the "Teardown Cafe MOC" content
2. Paste it as context in your first message
3. Mention: "Here's my current project context from Obsidian"

### When Starting with Claude:
1. Use the same MOC content
2. Add any new strategic decisions or content needs
3. Mention: "Here's my project context, need help with [specific task]"

## Automated Context Updates

### After Each Session:
1. Update the MOC with what was accomplished
2. Note any new decisions or blockers
3. Update the handoff notes for the next AI

### Weekly Context Refresh:
1. Review all `#teardown-cafe` tagged notes
2. Update the MOC with latest status
3. Archive completed tasks
4. Add new strategic questions

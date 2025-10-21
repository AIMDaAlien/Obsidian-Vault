# 📊 Workflow Dashboard

> **Real-time project status and AI collaboration overview**

## 🎯 Current Session Status

**Active Session:** *[Check with `./scripts/session-manager.sh status`]*  
**Last Updated:** *[Auto-updated on each commit]*  
**Git Status:** *[Auto-updated on each commit]*  

## 📈 Recent Activity

### Last 5 Sessions
*[Auto-populated from session files]*

### Recent Commits
*[Auto-populated from git log]*

### Pending Items
- [ ] *[Auto-populated from git status and TODO comments]*

## 🔄 AI Collaboration Stats

| Metric | Count |
|--------|-------|
| Total Sessions | *[Auto-calculated]* |
| Claude Sessions | *[Auto-calculated]* |
| Cursor Sessions | *[Auto-calculated]* |
| Total Commits | *[Auto-calculated]* |
| Files Modified | *[Auto-calculated]* |

## 📁 Quick Access

### Session Management
- [[Session Index]] - All session history
- [[claude-cursor-collaboration-prompt]] - Handoff prompts
- [[simple-workflow-guide]] - Usage guide

### Project Files
- `src/layouts/BaseLayout.astro` - Main layout
- `src/pages/index.astro` - Homepage
- `src/data/teardowns/` - Content directory
- `src/components/` - Reusable components

### Context Files
- `.context/last-change-summary.md` - Recent changes
- `.context/next-ai-context.md` - Handoff notes
- `.context/current-state.json` - Machine state

## 🚀 Quick Actions

### Start New Session
```bash
# Cursor session
./scripts/session-manager.sh start cursor

# Claude session  
./scripts/session-manager.sh start claude
```

### Commit Changes
```bash
# With session tracking
./scripts/commit-with-session.sh "Your commit message"
```

### Generate Context
```bash
# For Claude
./scripts/claude-context-generator.sh clipboard

# For Cursor
./scripts/cursor-context-generator.sh clipboard
```

### Check Status
```bash
# Session status
./scripts/session-manager.sh status

# Git status
git status
```

## 📋 Workflow Checklist

### Starting a Session
- [ ] Choose AI (Claude/Cursor)
- [ ] Run session start command
- [ ] Note session goal in session file
- [ ] Begin work

### During Session
- [ ] Update session log as you work
- [ ] Note any issues or decisions
- [ ] Keep track of files modified

### Ending a Session
- [ ] Update session note with summary
- [ ] Add handoff notes for next AI
- [ ] Run commit with session
- [ ] Generate context for next AI

### Handoff Process
- [ ] Generate context for next AI
- [ ] Copy context to clipboard
- [ ] Start new AI session
- [ ] Paste context as starting prompt

## 🔧 Troubleshooting

### Common Issues
- **Session not found**: Run `./scripts/session-manager.sh start [ai]`
- **Context not generated**: Check if session is active
- **Obsidian sync fails**: Verify vault path in scripts
- **Git conflicts**: Resolve conflicts before committing

### Debug Commands
```bash
# Check session status
./scripts/session-manager.sh status

# View recent sessions
ls -la "/Users/aim/Documents/Obsidian Notes Vault/Teardown Cafe/Sessions/"

# Check git status
git status

# View context files
ls -la .context/
```

## 📊 Project Metrics

### Code Quality
- **Linting Errors:** *[Auto-populated]*
- **TODO Comments:** *[Auto-populated]*
- **FIXME Comments:** *[Auto-populated]*

### Build Status
- **Dependencies:** *[Auto-populated]*
- **Build Output:** *[Auto-populated]*
- **Dev Server:** *[Auto-populated]*

### Content Status
- **Teardowns:** *[Auto-populated]*
- **Images:** *[Auto-populated]*
- **Pages:** *[Auto-populated]*

---

## 🎯 Next Steps

*[Add your next tasks here]*

1. *[Task 1]*
2. *[Task 2]*
3. *[Task 3]*

---

*Dashboard last updated: [Auto-generated timestamp]*  
*Use this dashboard to track your AI collaboration workflow*

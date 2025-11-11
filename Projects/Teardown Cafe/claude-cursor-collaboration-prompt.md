# 🤝 Claude-Cursor AI Collaboration Prompt Template

## 🎯 **Copy this prompt when starting a new conversation with Claude:**

---

**PROJECT CONTEXT:**
I'm working on the **Teardown Cafe** project - a device teardown blog built with Astro 5 and Material You 3 design. Here's my current context:

**Project Status:**
- [Current phase: Development/Content Creation/Design]
- [Next tasks: List 3-5 key tasks]
- [Blockers: Any issues]

**Key Context from Obsidian:**
- [Paste your Teardown Cafe MOC content here]
- [Any recent strategic decisions]
- [Content creation needs]

**Technical Stack:**
- Astro 5 with Content Layer API
- Material You 3 design system
- Obsidian integration via sync scripts
- Git workflow with automated Obsidian updates

**My MCP Tools Available:**
- Docker (for Obsidian interaction)
- Context7 (for up-to-date libraries/frameworks)
- Figma Dev Mode (for design)
- GitHub integration
- PDF tools
- Filesystem access

**Current Task:**
[Describe what you need Claude to help with - strategic decisions, content creation, design system work, etc.]

**Handoff Notes for Cursor AI:**
- [Code fixes needed]
- [File operations required]
- [Git management tasks]
- [Component creation needs]

---

## 🎯 **Copy this prompt when starting a new conversation with Cursor AI:**

---

**PROJECT CONTEXT:**
I'm working on the **Teardown Cafe** project - a device teardown blog built with Astro 5 and Material You 3 design. Here's my current context:

**Project Status:**
- [Current phase: Development/Content Creation/Design]
- [Next tasks: List 3-5 key tasks]
- [Blockers: Any issues]

**Key Context from Obsidian:**
- [Paste your Teardown Cafe MOC content here]
- [Any recent strategic decisions]
- [Content creation needs]

**Technical Stack:**
- Astro 5 with Content Layer API
- Material You 3 design system
- Obsidian integration via sync scripts
- Git workflow with automated Obsidian updates

**Current Task:**
[Describe what you need Cursor AI to help with - code fixes, file operations, git management, component creation, etc.]

**Recent Changes:**
- [What was just accomplished]
- [What files were modified]
- [Current git status]

**Handoff Notes for Claude:**
- [Strategic decisions needed]
- [Content creation tasks]
- [Design system work]
- [Architecture decisions]

---

## 🔄 **Session Handoff Protocol**

### When Switching from Claude to Cursor AI:
1. **Commit your work:** `git add -A && git commit -m "WIP: [description]"`
2. **Update Obsidian:** Run `./sync-to-obsidian.sh`
3. **Copy the Cursor AI prompt above** and fill in current context
4. **Start with specific technical task** (code fix, component creation, etc.)

### When Switching from Cursor AI to Claude:
1. **Commit your work:** `git add -A && git commit -m "WIP: [description]"`
2. **Update Obsidian:** Run `./sync-to-obsidian.sh`
3. **Copy the Claude prompt above** and fill in current context
4. **Start with strategic task** (content creation, design decisions, etc.)

## 📋 **Quick Reference Commands**

### Git Operations:
```bash
# Check status
git status

# Commit changes
git add -A
git commit -m "Description of changes"

# Push to remote
git push origin main
```

### Obsidian Sync:
```bash
# Update Obsidian vault
./sync-to-obsidian.sh
```

### Development:
```bash
# Start dev server
npm run dev

# Build for production
npm run build
```

## 🎯 **Task Division Guidelines**

### Use Claude for:
- ✅ High-level architecture decisions
- ✅ Content creation and documentation
- ✅ Design system strategy
- ✅ Obsidian note organization
- ✅ Strategic planning
- ✅ Complex problem-solving

### Use Cursor AI for:
- ✅ Code fixes and debugging
- ✅ File operations and git management
- ✅ Component creation and integration
- ✅ Build system issues
- ✅ Quick iterations and testing
- ✅ Technical implementation

## 📝 **Context Maintenance**

### Daily:
- Update your Teardown Cafe MOC in Obsidian
- Note what was accomplished
- Identify next tasks

### Weekly:
- Review all `#teardown-cafe` tagged notes
- Update strategic decisions
- Plan next phase of work

### Per Session:
- Use the appropriate prompt template
- Include current project status
- Specify clear next tasks
- Note handoff requirements

---

**This system ensures seamless collaboration between Claude and Cursor AI while maintaining context across sessions.**

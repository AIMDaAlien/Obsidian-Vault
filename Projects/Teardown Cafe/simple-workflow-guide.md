# 🚀 Simple Workflow Guide for Teardown Cafe

## 🎯 **For Non-Technical Users**

### **Step 1: Set Up Your Obsidian Context**

1. **Open Obsidian**
2. **Create a new note called "Teardown Cafe MOC"**
3. **Copy this template into the note:**

```markdown
# Teardown Cafe - My Project Status

## What I'm Working On
- Current task: [What you're doing right now]
- Next up: [What you want to do next]
- Any problems: [Any issues you're facing]

## Recent Work
- [Date]: [What you accomplished]
- [Date]: [What you accomplished]

## Notes for AI Help
- For Claude: [Strategic decisions, content creation, design work]
- For Cursor AI: [Code fixes, file operations, technical tasks]
```

4. **Save this note and keep it updated**

### **Step 2: When You Need Help**

#### **For Strategic Work (Content, Design, Planning):**
1. **Open a new Claude conversation**
2. **Copy the "Claude prompt" from the collaboration file**
3. **Fill in your current status from your Obsidian note**
4. **Tell Claude what you want to accomplish**

#### **For Technical Work (Code, Files, Git):**
1. **Open Cursor AI (this chat)**
2. **Copy the "Cursor AI prompt" from the collaboration file**
3. **Fill in your current status from your Obsidian note**
4. **Tell me what technical task you need help with**

### **Step 3: After Each Session**

1. **Update your Obsidian note** with what you accomplished
2. **Run these commands in Terminal:**
   ```bash
   cd ~/Documents/teardown-cafe
   git add -A
   git commit -m "What you just did"
   ./sync-to-obsidian.sh
   ```
3. **Note what you need help with next**

## 🔄 **Simple Handoff Process**

### **Claude → Cursor AI:**
1. **Update your Obsidian note**
2. **Run the git commands above**
3. **Start new Cursor AI chat with the prompt**
4. **Tell me: "I need help with [specific technical task]"**

### **Cursor AI → Claude:**
1. **Update your Obsidian note**
2. **Run the git commands above**
3. **Start new Claude chat with the prompt**
4. **Tell Claude: "I need help with [strategic task]"**

## 📋 **Quick Commands (Copy & Paste)**

### **Check Project Status:**
```bash
cd ~/Documents/teardown-cafe
git status
```

### **Save Your Work:**
```bash
cd ~/Documents/teardown-cafe
git add -A
git commit -m "Description of what you did"
./sync-to-obsidian.sh
```

### **Start Development Server:**
```bash
cd ~/Documents/teardown-cafe
npm run dev
```

## 🎯 **What Each AI Does Best**

### **Claude (Strategic Partner):**
- ✅ Content creation and writing
- ✅ Design decisions and strategy
- ✅ Planning and organization
- ✅ Complex problem-solving
- ✅ Obsidian note management

### **Cursor AI (Technical Partner):**
- ✅ Code fixes and debugging
- ✅ File operations
- ✅ Git management
- ✅ Component creation
- ✅ Technical implementation

## 🆘 **When You're Stuck**

1. **Update your Obsidian note** with the problem
2. **Run the save commands** above
3. **Start a new chat** with the appropriate AI
4. **Use the prompt template** and describe your issue
5. **Be specific** about what you need help with

## 📝 **Pro Tips**

- **Keep your Obsidian note updated** - it's your memory between sessions
- **Be specific** about what you need help with
- **Use the prompt templates** - they save time and provide context
- **Don't worry about being technical** - both AIs can help with that
- **Save your work frequently** using the git commands

---

**This system lets you work seamlessly with both AIs while keeping track of everything in Obsidian!**

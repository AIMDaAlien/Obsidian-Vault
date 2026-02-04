# Obsidian Productivity Mastery

#obsidian #productivity #knowledge-management #hotkeys #workflow

> **Central Hub**: [[🗺️ Knowledge Base - Main Index]]

## Overview
Obsidian is your 第二の脳 (だいにのう - second brain) for knowledge management. Master these workflows and hotkeys to navigate your vault like a productivity ninja.

## Essential Hotkeys

### Navigation (Most Important!)
| Hotkey | Action | Why It Matters |
|--------|--------|----------------|
| `Ctrl + O` | **Quick Switcher** | Find any note instantly |
| `Ctrl + Shift + F` | **Global Search** | Search across all notes |
| `Ctrl + N` | **New Note** | Create note quickly |
| `Ctrl + P` | **Command Palette** | Access all commands |
| `Ctrl + G` | **Graph View** | Visualize note connections |

### Editing and Formatting
| Hotkey | Action | Usage |
|--------|--------|-------|
| `Ctrl + B` | **Bold text** | `**bold**` |
| `Ctrl + I` | **Italic text** | `*italic*` |
| `Ctrl + K` | **Insert link** | `[[link]]` or `[text](url)` |
| `Ctrl + E` | **Toggle edit/preview** | Switch between modes |
| `Ctrl + ,` | **Settings** | Access preferences |

### Advanced Navigation
| Hotkey | Action | Pro Tip |
|--------|--------|---------|
| `Ctrl + Alt + ←/→` | **Navigate back/forward** | Like browser history |
| `Ctrl + Shift + I` | **Open developer console** | For advanced debugging |
| `Ctrl + Tab` | **Switch between tabs** | Work with multiple notes |
| `Alt + E` | **Toggle file explorer** | Show/hide file list |

## Powerful Search Techniques

### Basic Search
```
Simple text search:
programming python

Case sensitive:
match-case:Python

Exact phrase:
"machine learning algorithms"
```

### Advanced Search Operators
```
📁 Path-based search:
path:"Programming/"             # Notes in Programming folder

🏷️ Tag-based search:
tag:#programming               # Notes with programming tag
tag:#beginner AND tag:#python  # Multiple tags

📅 Date-based search:
created:2024-01-01             # Created on specific date
modified:>2024-01-01           # Modified after date

🔍 Content search:
line:(TODO OR FIXME)           # Find action items
section:Overview               # Search in specific sections
```

### Search Combinations
```
Complex queries:
tag:#programming AND path:Python/ AND line:function
(#beginner OR #intermediate) AND file:notes
```

## Note Organization System

### Folder Structure Strategy
```
📂 Top-Level Organization:
🗺️ Knowledge Base - Main Index.md    # Central navigation
📁 Programming/                      # Technical content
📁 Systems/                         # Tools and processes
📁 Projects/                        # Active work
📁 Archive/                         # Completed/outdated
📁 Templates/                       # Note templates
```

### Linking Strategy
```markdown
# Different types of links:

[[Note Name]]                    # Basic internal link
[[Note Name|Display Text]]       # Link with custom text
[[Note Name#Heading]]           # Link to specific section
[[Note Name^block-id]]          # Link to specific block

# External links:
[Display Text](https://example.com)
```

### Tag Hierarchy
```
🏷️ Tag System:
#programming
  #programming/python
  #programming/web
  #programming/databases

#project
  #project/active
  #project/completed
  #project/planning
```

## Templates and Automation

### Note Templates
Create consistent structure for different note types:

#### Project Template
```markdown
# {{title}}

## Overview
Brief description of the project

## Goals
- [ ] Primary objective
- [ ] Secondary objective
- [ ] Success metrics

## Resources
- [[Related Note 1]]
- [[Related Note 2]]

## Timeline
| Phase | Deadline | Status |
|-------|----------|--------|
| Planning | {{date}} | 🔄 |
| Development | {{date}} | ⏳ |
| Review | {{date}} | ⏳ |

## Notes
{{cursor}}

---
*Tags: #project/active #{{category}}*
*Created: {{date}}*
```

#### Meeting Notes Template
```markdown
# {{title}} - {{date}}

## Attendees
- Name 1
- Name 2

## Agenda
1. Topic 1
2. Topic 2
3. Topic 3

## Discussion
### Topic 1
Notes here...

### Topic 2
Notes here...

## Action Items
- [ ] @person - Task description (due: date)
- [ ] @person - Task description (due: date)

## Follow-up
- Next meeting: {{date}}
- Items to prepare: 

---
*Tags: #meeting #{{project}}*
```

### Daily Notes Setup
```markdown
# {{date:YYYY-MM-DD}} - Daily Notes

## Today's Focus
- Primary goal: 
- Secondary goals:

## Meetings
- Time | Meeting | Notes

## Learning
- New concept learned:
- Resource discovered:

## Reflection
- What went well:
- What could improve:
- Tomorrow's priority:

---
*Tags: #daily-notes #{{date:YYYY-MM}}*
```

## Plugin Recommendations

### Essential Plugins
```
🔧 Core Productivity:
• Calendar - Visual daily notes navigation
• Dataview - Query and display data dynamically
• Templater - Advanced template functionality
• Tag Wrangler - Better tag management
• Quick Switcher++ - Enhanced file switching

📊 Data and Visualization:
• Charts - Create charts from note data
• Mind Map - Visual thinking maps
• Excalidraw - Hand-drawn diagrams
• Mermaid - Technical diagrams

⚡ Workflow Enhancement:
• Hotkeys++ - Additional keyboard shortcuts
• Workspaces - Save and switch layout configurations
• File Explorer++ - Enhanced file management
• Advanced Tables - Better table editing
```

### Power User Plugins
```
🚀 Advanced Features:
• Periodic Notes - Weekly/monthly/quarterly notes
• Review - Spaced repetition for notes
• Tasks - Advanced task management
• Breadcrumbs - Alternative navigation system
• Database Folder - Organize notes like database records
```

## Workflow Optimization

### Daily Workflow
```
🌅 Morning Routine:
1. Ctrl+P → "Open today's daily note"
2. Review yesterday's action items
3. Set today's priorities
4. Check calendar for meetings

💼 During Work:
1. Ctrl+N for quick capture
2. Ctrl+K to link related concepts
3. Use tags for easy retrieval
4. Regular Ctrl+S to save

🌙 Evening Review:
1. Process capture notes
2. Update project status
3. Plan tomorrow's focus
4. Archive completed items
```

### Weekly Review Process
```
📅 Weekly Maintenance:
• Review and organize capture notes
• Update project status and timelines
• Clean up tags and broken links
• Archive completed items
• Plan next week's priorities
```

## Advanced Features

### Dataview Queries
```javascript
// List all programming notes modified this week
```dataview
LIST
FROM #programming 
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
```

// Create project dashboard
```dataview
TABLE status, deadline, priority
FROM #project/active 
SORT priority DESC, deadline ASC
```

// Track learning progress
```dataview
LIST
FROM #learning
WHERE contains(tags, "completed")
GROUP BY dateformat(file.ctime, "yyyy-MM")
```
```

### Graph View Optimization
```
🕸️ Graph Settings:
• Color groups by tags or folders
• Adjust forces for better layout
• Filter out noise (daily notes, etc.)
• Focus on specific tag clusters
• Use local graph for note context
```

### Automation Ideas
```python
# Python script to process Obsidian notes
import os
import re
from pathlib import Path

def update_backlinks():
    """Find and update broken internal links"""
    vault_path = Path("~/Documents/Obsidian/MyVault").expanduser()
    
    for note_file in vault_path.rglob("*.md"):
        with open(note_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all [[links]]
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        
        for link in links:
            # Check if linked file exists
            linked_file = vault_path / f"{link}.md"
            if not linked_file.exists():
                print(f"Broken link: {link} in {note_file.name}")

if __name__ == "__main__":
    update_backlinks()
```

## Backup and Sync

### Backup Strategy
```
💾 Multi-layered Backup:
1. Git repository (version control)
2. Cloud sync (Obsidian Sync or Dropbox)
3. Local backup (Time Machine, File History)
4. Export backup (regular vault exports)
```

### Git Integration
```bash
# Initialize Git repository in vault
cd /path/to/obsidian/vault
git init
echo ".obsidian/workspace*" >> .gitignore
echo ".obsidian/hotkeys.json" >> .gitignore
git add .
git commit -m "Initial vault setup"

# Daily backup script
#!/bin/bash
cd /path/to/obsidian/vault
git add .
git commit -m "Daily backup $(date +%Y-%m-%d)"
git push origin main
```

## Troubleshooting Common Issues

### Performance Optimization
```
⚡ Speed Up Obsidian:
• Limit auto-complete suggestions
• Reduce graph animation
• Disable unused plugins
• Index only essential folders
• Use smaller image files
• Regular cache clearing
```

### Organization Problems
```
🧹 Maintaining Clean Vault:
• Regular tag cleanup and standardization
• Delete orphaned notes (notes with no links)
• Merge duplicate content
• Use MOCs to prevent note sprawl
• Establish naming conventions early
```

### Link Management
```
🔗 Keeping Links Healthy:
• Use "Unlinked mentions" to find connection opportunities
• Regular broken link audits
• Consistent note naming conventions
• Avoid special characters in note names
• Use aliases for alternative note names
```

## Mobile Optimization

### Mobile-Friendly Practices
- **Shorter note names** - Easier to type on mobile
- **Simple formatting** - Complex tables don't work well
- **Voice notes** - Quick capture using voice-to-text
- **Offline access** - Ensure sync works without internet

## Obsidian as Learning Tool

### Spaced Repetition
```markdown
# Create review cards
What is the time complexity of binary search? #review
?
O(log n) - eliminates half the search space each iteration

# Use review plugin to schedule spaced repetition
```

### Progressive Summarization
```markdown
# Original capture (Level 1)
Raw notes from book/article/lecture

## Key insights (Level 2 - Bold)
**Important concepts and ideas**

### Core principles (Level 3 - Highlight)  
==Essential knowledge that must be remembered==

#### Action items (Level 4 - Personal notes)
- How I'll apply this knowledge
- Questions for further research
```

Your Obsidian vault should become an extension of your thinking. The more you invest in organizing and connecting your knowledge, the more valuable it becomes as your personal 知識データベース (ちしきデータベース - knowledge database)!

---
*Tags: #obsidian #productivity #knowledge-management #workflow*  
*Related: [[🗺️ Knowledge Base - Main Index]] | [[Systems/Development Tools]]*

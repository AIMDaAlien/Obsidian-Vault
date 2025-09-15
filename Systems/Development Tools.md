# Development Tools & Productivity

#systems #tools #productivity #ide #development #efficiency

> **Related**: [[Programming/Python Fundamentals]] | [[🗺️ Knowledge Base - Main Index]]

## Overview
The right tools can transform your development workflow from 苦痛 (くつう - painful struggle) into efficient, enjoyable productivity. This guide covers essential development tools and productivity systems.

## Integrated Development Environments (IDEs)

### What is an IDE?
An **IDE (統合開発環境 - とうごうかいはつかんきょう)** is a comprehensive software application that provides programmers with a user-friendly workspace for coding. Think of it as your digital workshop with all the tools you need in one place.

### Popular IDEs by Use Case

#### Beginner-Friendly Options
**Replit** (Browser-based)
- ✅ **Pros**: Zero setup, collaborative, great for learning
- ❌ **Cons**: Limited for large projects, requires internet
- **Best for**: Learning, small projects, quick prototyping

**Thonny** (Python-specific)
- ✅ **Pros**: Designed for beginners, visual debugging
- ❌ **Cons**: Python only, limited features
- **Best for**: Python learning and education

#### Professional Development

**Visual Studio Code (VS Code)**
```
🔥 Why It's Popular:
• Free and open-source
• Extensive plugin ecosystem (50,000+ extensions)
• Excellent Git integration
• Built-in terminal
• Remote development capabilities
• Lightning-fast performance

💼 Best For:
• Web development (HTML, CSS, JavaScript)
• Python, C++, Java development
• Full-stack projects
• Remote/cloud development
```

**PyCharm** (JetBrains)
- ✅ **Pros**: Powerful debugging, intelligent code completion, professional features
- ❌ **Cons**: Resource-intensive, paid version for full features
- **Best for**: Python professionals, Django development

**IntelliJ IDEA** (JetBrains)
- ✅ **Pros**: Excellent Java support, refactoring tools, enterprise features  
- ❌ **Cons**: Heavy resource usage, complex for beginners
- **Best for**: Java/Kotlin enterprise development

#### Specialized Environments

**Jupyter Notebooks**
- **Purpose**: Data science, research, prototyping
- **Strengths**: Interactive development, visualization integration
- **Best for**: Data analysis, machine learning, documentation

**Sublime Text**
- **Purpose**: Fast text editing with coding features
- **Strengths**: Speed, customization, multiple cursors
- **Best for**: Quick edits, large files, minimalist setup

### IDE Selection Framework

#### Choose Based on Your Needs
```
🎯 Decision Matrix:

Beginner Learning → Replit or Thonny
Web Development → VS Code  
Python Professional → PyCharm
Java/Enterprise → IntelliJ IDEA
Data Science → Jupyter + VS Code
Quick Edits → Sublime Text
```

## Essential IDE Features and Setup

### Core Features Every IDE Should Have

#### Syntax Highlighting and IntelliSense
```python
# Good IDE will highlight syntax and provide suggestions
def calculate_average(numbers):
    # IDE suggests: sum, len, return
    return sum(numbers) / len(numbers)
```

#### Debugging Capabilities
- **Breakpoints** - Pause execution at specific lines
- **Variable inspection** - See values during execution
- **Step-through debugging** - Execute code line by line
- **Call stack** - Understand function execution flow

#### Version Control Integration
```bash
# Git commands should be accessible via GUI
git add .
git commit -m "Add new feature"
git push origin main
```

#### Project Management
- **File explorer** - Navigate project structure
- **Search and replace** - Across entire project
- **Refactoring tools** - Rename variables, extract functions
- **Task runners** - Build, test, deploy automation

### VS Code Setup for Maximum Productivity

#### Essential Extensions
```
🔧 Must-Have Extensions:

General Productivity:
• Prettier (code formatting)
• GitLens (enhanced Git)
• Bracket Pair Colorizer
• Auto Rename Tag
• Live Server (web development)

Language-Specific:
• Python (Microsoft)
• Python Docstring Generator
• pylint (code linting)
• IntelliCode (AI assistance)

Themes and UI:
• One Dark Pro (popular theme)
• Material Icon Theme
• Indent Rainbow
```

#### Productivity Settings
```json
// settings.json configuration
{
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "files.autoSave": "afterDelay",
    "editor.minimap.enabled": true,
    "workbench.startupEditor": "none"
}
```

#### Keyboard Shortcuts Mastery
| Action | Windows/Linux | Mac | Purpose |
|--------|---------------|-----|---------|
| **Quick Open** | `Ctrl+P` | `Cmd+P` | Find files instantly |
| **Command Palette** | `Ctrl+Shift+P` | `Cmd+Shift+P` | Access all commands |
| **Go to Line** | `Ctrl+G` | `Cmd+G` | Jump to specific line |
| **Multi-cursor** | `Ctrl+D` | `Cmd+D` | Edit multiple instances |
| **Comment Toggle** | `Ctrl+/` | `Cmd+/` | Comment/uncomment code |
| **Split Editor** | `Ctrl+\` | `Cmd+\` | Work with multiple files |

## Version Control with Git

### Why Git Matters
Git is the **industry standard** for version control - it tracks changes to your code, enables collaboration, and prevents data loss.

### Essential Git Workflow
```bash
# Initial setup (one time)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Daily workflow
git status                    # See what's changed
git add .                     # Stage all changes
git commit -m "Descriptive message"  # Save changes
git push origin main          # Upload to remote repository

# Collaboration
git pull origin main          # Get latest changes
git branch feature-branch     # Create new branch
git checkout feature-branch   # Switch to branch
git merge feature-branch      # Combine branches
```

### Git Best Practices
```
📝 Commit Message Guidelines:
• Use present tense ("Add feature" not "Added feature")
• Keep first line under 50 characters
• Be specific about what changed

Examples:
✅ "Fix login validation bug"
✅ "Add user authentication system"  
✅ "Update README with installation instructions"

❌ "Fixed stuff"
❌ "Changes"
❌ "asdf"
```

### GitHub Integration
**GitHub** provides cloud hosting for Git repositories plus collaboration features:
- **Issues tracking** - Bug reports and feature requests
- **Pull requests** - Code review and collaboration
- **Actions** - Automated testing and deployment
- **Pages** - Free website hosting
- **Portfolio** - Showcase your projects

## Command Line Essentials

### Why Learn the Terminal?
The command line interface (CLI) is **more powerful** and **faster** than graphical interfaces for many development tasks.

### Essential Commands

#### File Navigation
```bash
# Directory operations
pwd                    # Print working directory
ls                     # List files and folders
ls -la                 # List with details and hidden files
cd Documents           # Change to Documents folder
cd ..                  # Go up one level
cd ~                   # Go to home directory

# File operations  
mkdir project-name     # Create directory
touch file.txt         # Create empty file
cp file.txt backup.txt # Copy file
mv file.txt new-name.txt # Move/rename file
rm file.txt            # Delete file (careful!)
rm -rf folder-name     # Delete folder and contents (very careful!)
```

#### Text Processing
```bash
# View file contents
cat file.txt           # Display entire file
head -10 file.txt      # First 10 lines
tail -10 file.txt      # Last 10 lines
less file.txt          # Paginated view (q to quit)

# Search and filter
grep "search-term" file.txt    # Find lines containing term
find . -name "*.py"            # Find all Python files
wc -l file.txt                 # Count lines in file
```

#### Process Management
```bash
# System information
ps aux                 # List running processes
top                    # Real-time process monitor
kill 1234              # Stop process with ID 1234
killall python         # Stop all Python processes

# Network
ping google.com        # Test network connectivity
curl https://api.github.com    # Make HTTP request
```

### Terminal Enhancement

#### Better Terminal Apps
- **Windows**: Windows Terminal, WSL2 (Windows Subsystem for Linux)
- **Mac**: iTerm2, built-in Terminal
- **Linux**: Terminator, GNOME Terminal

#### Shell Improvements
**Oh My Zsh** (Mac/Linux):
```bash
# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Popular plugins: git, autosuggestions, syntax-highlighting
# Popular themes: robbyrussell, agnoster, powerlevel10k
```

## Project Organization and File Management

### Project Structure Best Practices

#### Python Project Template
```
my-python-project/
├── README.md                 # Project description
├── requirements.txt          # Dependencies  
├── .gitignore               # Files to ignore in Git
├── src/                     # Source code
│   ├── __init__.py
│   ├── main.py
│   └── utils.py
├── tests/                   # Test files
│   ├── __init__.py
│   └── test_main.py
├── docs/                    # Documentation
└── data/                    # Data files (if applicable)
```

#### Web Development Project
```
my-web-project/
├── README.md
├── package.json             # Node.js dependencies
├── .gitignore
├── public/                  # Static files
│   ├── index.html
│   └── favicon.ico
├── src/                     # Source code
│   ├── components/          # React components
│   ├── styles/              # CSS files
│   └── index.js
└── build/                   # Compiled output
```

### File Naming Conventions
```
✅ Good File Names:
• user_authentication.py
• database_config.json
• main_stylesheet.css
• project_requirements.txt

❌ Poor File Names:
• untitled.py
• temp.txt
• asdf.js
• copy_of_file_final_v2.py
```

## Productivity Tools and Techniques

### Code Snippets and Templates

#### VS Code Snippets
```json
// Python function snippet
{
    "Python Function": {
        "prefix": "def",
        "body": [
            "def ${1:function_name}(${2:parameters}):",
            "    \"\"\"${3:Description}\"\"\"",
            "    ${4:pass}",
            "    return ${5:None}"
        ],
        "description": "Create Python function with docstring"
    }
}
```

#### Text Expanders
- **Windows**: PhraseExpress, AutoHotkey
- **Mac**: TextExpander, Alfred
- **Cross-platform**: Espanso

### Time Management for Developers

#### Pomodoro Technique
```
🍅 25-minute focused work sessions:
1. Choose specific task
2. Set timer for 25 minutes  
3. Work without distractions
4. Take 5-minute break
5. After 4 pomodoros, take longer break (15-30 minutes)
```

#### Time Blocking
```
📅 Example Developer Schedule:
09:00-11:00  Deep work (complex coding)
11:00-11:15  Break
11:15-12:00  Code review and debugging  
12:00-13:00  Lunch
13:00-14:00  Meetings and communication
14:00-16:00  Feature development
16:00-17:00  Learning and documentation
```

### Documentation and Note-Taking

#### Documentation Tools
- **README files** - Project overview and setup instructions
- **Code comments** - Explain complex logic inline
- **API documentation** - Swagger, Postman collections
- **Wiki systems** - Confluence, Notion, Obsidian

#### Code Documentation Best Practices
```python
def calculate_compound_interest(principal, rate, time, compound_frequency=1):
    """
    Calculate compound interest for an investment.
    
    Args:
        principal (float): Initial investment amount
        rate (float): Annual interest rate (as decimal, e.g., 0.05 for 5%)
        time (float): Time period in years
        compound_frequency (int): Times per year interest is compounded
        
    Returns:
        float: Final amount after compound interest
        
    Example:
        >>> calculate_compound_interest(1000, 0.05, 2, 4)
        1104.49
    """
    amount = principal * (1 + rate/compound_frequency) ** (compound_frequency * time)
    return round(amount, 2)
```

## Environment Management

### Virtual Environments (Python)
```bash
# Create virtual environment
python -m venv myproject-env

# Activate environment
# Windows:
myproject-env\Scripts\activate
# Mac/Linux:
source myproject-env/bin/activate

# Install packages
pip install requests numpy pandas

# Save dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Deactivate environment
deactivate
```

### Package Managers
- **Python**: pip, conda, poetry
- **JavaScript**: npm, yarn, pnpm  
- **Java**: Maven, Gradle
- **Ruby**: gem, bundler

### Docker for Development
```dockerfile
# Simple Python development container
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

## Automation and Scripting

### Task Automation Examples

#### File Organization Script
```python
import os
import shutil
from pathlib import Path

def organize_downloads():
    """Organize Downloads folder by file type"""
    downloads = Path.home() / "Downloads"
    
    file_types = {
        'images': ['.jpg', '.png', '.gif', '.jpeg'],
        'documents': ['.pdf', '.docx', '.txt', '.xlsx'],
        'archives': ['.zip', '.rar', '.7z', '.tar'],
        'videos': ['.mp4', '.avi', '.mkv', '.mov']
    }
    
    for category, extensions in file_types.items():
        category_folder = downloads / category
        category_folder.mkdir(exist_ok=True)
        
        for file in downloads.iterdir():
            if file.suffix.lower() in extensions:
                shutil.move(str(file), str(category_folder / file.name))
                print(f"Moved {file.name} to {category}")

if __name__ == "__main__":
    organize_downloads()
```

#### Build and Deploy Script
```bash
#!/bin/bash
# deploy.sh - Automated deployment script

echo "Starting deployment..."

# Run tests
echo "Running tests..."
python -m pytest tests/
if [ $? -ne 0 ]; then
    echo "Tests failed! Aborting deployment."
    exit 1
fi

# Build application
echo "Building application..."
npm run build

# Deploy to server
echo "Deploying to production..."
rsync -avz build/ user@server:/var/www/app/

echo "Deployment complete!"
```

## Performance and Monitoring

### System Monitoring Tools
```bash
# CPU and memory usage
htop                   # Interactive process viewer
free -h                # Memory usage
df -h                  # Disk space usage

# Development-specific monitoring
time python script.py  # Measure script execution time
du -sh project/        # Project folder size
```

### Code Performance Tools
- **Python**: cProfile, line_profiler, memory_profiler
- **JavaScript**: Chrome DevTools, Lighthouse
- **General**: New Relic, DataDog for production monitoring

### Backup and Recovery
```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/projects_$DATE"

# Create timestamped backup
rsync -av ~/projects/ $BACKUP_DIR
tar -czf "$BACKUP_DIR.tar.gz" $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "Backup created: $BACKUP_DIR.tar.gz"
```

## Security and Best Practices

### Code Security
```python
# ❌ Bad: Hardcoded secrets
API_KEY = "sk-1234567890abcdef"

# ✅ Good: Environment variables
import os
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

### Environment Variables
```bash
# .env file (never commit to Git!)
DATABASE_URL=postgresql://user:password@localhost/dbname
API_SECRET_KEY=your-secret-key-here
DEBUG=True

# Load in Python
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv('DATABASE_URL')
```

### .gitignore Essentials
```gitignore
# Python
__pycache__/
*.pyc
.env
venv/
.venv/

# Node.js
node_modules/
npm-debug.log
.env.local

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Build outputs
dist/
build/
*.exe
```

## Tool Recommendations by Experience Level

### Beginner Setup
```
🌱 Getting Started:
• IDE: VS Code or Replit
• Version Control: GitHub Desktop
• Terminal: Built-in or Windows Terminal
• Note-taking: Simple text files or Notion
• Focus: Learn one tool well before adding more
```

### Intermediate Setup
```
🔧 Building Skills:
• IDE: VS Code with extensions
• Version Control: Git command line
• Terminal: Enhanced shell (Oh My Zsh)
• Documentation: Markdown + GitHub
• Automation: Simple Python/Bash scripts
```

### Advanced Setup
```
⚡ Power User:
• IDE: Multiple specialized IDEs
• Version Control: Advanced Git workflows
• Terminal: Fully customized environment
• Documentation: Automated doc generation
• Automation: CI/CD pipelines, Docker
• Monitoring: Performance and error tracking
```

Your development environment is your 道具 (どうぐ - tools). Invest time in setting them up well, and they'll serve you efficiently for years to come!

---
*Tags: #tools #ide #productivity #git #automation #development*  
*Related: [[Programming/Python Fundamentals]] | [[🗺️ Knowledge Base - Main Index]] | [[Career/Skill Development]]*
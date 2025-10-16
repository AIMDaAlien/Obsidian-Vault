# Claude Power User Workflow - Practical Implementation

## Quick Start Guide

### Day 1: Setup (30 minutes)

**1. Create Obsidian structure:**
```
Vault/
├── Meta/
│   ├── Claude Interaction Guidelines.md ✓ (already created)
│   ├── Conversation Limit Avoidance Workflow.md ✓
│   ├── Token Optimization Guide.md ✓
│   └── Active Projects Dashboard.md (create now)
├── Projects/
│   └── [Your projects here]
└── Archive/
    └── [Completed projects]
```

**2. Install token counter:**
```bash
cd /Users/aim/Documents/claude-token-counter
pip3 install tiktoken
python3 token_counter.py  # Test it works
```

**3. Create your first project structure:**
```
Projects/[Project Name]/
├── [Project] - Index.md
├── [Project] - Current State.md
├── [Project] - Technical Setup.md
└── Sessions/ (optional)
```

### Day 2-7: Build Habits

**Every conversation:**
1. Start with clear task + note reference
2. Document as you go
3. Update Current State before ending
4. Check token estimate

**End of week:**
- Review what worked
- Refine note structure
- Update guidelines if needed

---

## The Core Workflow

### Phase 1: Starting Conversation (2 minutes)

**Template:**
```markdown
Task: [One specific thing to accomplish]

Context: See notes:
- [[Project - Current State]]
- [[Relevant Technical Note]]

Current situation: [2 sentences max]

Goal: [Desired outcome]

Tools: Use [local filesystem / Obsidian MCP / specific tool]
```

**Example:**
```markdown
Task: Add image optimization to teardown.cafe

Context:
- [[Teardown Cafe - Current State]]
- [[Teardown Cafe - Technical Setup]]

Current: Images manually optimized with exiftool
Goal: Automate with sharp package, preserve EXIF stripping

Tools: Use local filesystem
```

**Token cost:** ~500 tokens
**vs. "Continue previous conversation":** ~30,000 tokens
**Savings:** 59x more efficient

### Phase 2: During Conversation (Real-time)

**As Claude responds:**

1. **Take notes of key decisions**
   ```markdown
   # Session Notes [Date]
   
   ## Decisions
   - Chose approach X because Y
   - Rejected option Z due to issue A
   
   ## Code Changes
   - File: path/to/file.ext
     Change: [brief description]
   ```

2. **Save important snippets**
   - Commands that worked
   - Configuration values
   - Error solutions

3. **Track token usage**
   - Check Claude's estimates (if showing)
   - Use token counter for your messages
   - Note when approaching 60%

4. **Git commit progressively**
   ```bash
   # After each working feature
   git add -A
   git commit -m "Feat: Specific accomplishment"
   ```

### Phase 3: Before Limit Hits (10 minutes)

**At 60-70% budget:**

1. **Complete current immediate task**
   - Finish what's in progress
   - Test if applicable
   - Commit to git

2. **Create session summary**
   ```markdown
   # [Project] - Session [Date]
   
   ## Accomplished
   - ✓ Task A - details
   - ✓ Task B - details
   - ⚠️ Task C - partially done
   
   ## Next Steps
   1. Complete Task C
   2. Move to Task D
   3. Test integration
   
   ## Blockers
   None / [description]
   
   ## Key Learnings
   - Learning 1
   - Learning 2
   ```

3. **Update Current State**
   ```markdown
   # [Project] - Current State
   
   Last updated: [now]
   
   ## Status
   - [x] Task A
   - [x] Task B
   - [ ] Task C (50% - needs testing)
   
   ## Next Conversation
   Start with: Complete Task C testing
   Then: Move to Task D
   ```

### Phase 4: Starting Fresh (30 seconds)

**Next conversation:**
```
Task: [Next item from Current State]

Context: [[Project - Current State]]

[Immediately start working]
```

**That's it.** No context loading, instant productivity.

---

## Project Lifecycle Management

### New Project Initialization

**When starting any new project:**

1. **Create note structure** (5 minutes)
   ```markdown
   # [Project] - Index
   
   ## Overview
   [2-3 sentences]
   
   ## Quick Links
   - [[Project - Current State]] ← Start here
   - [[Project - Technical Setup]]
   - [[Project - Design System]] (if applicable)
   
   ## External Links
   - Repository: [URL]
   - Deployment: [URL]
   ```

2. **Create Technical Setup note**
   ```markdown
   # [Project] - Technical Setup
   
   ## Stack
   - Framework: [name + version]
   - Language: [name]
   - Key dependencies: [list]
   
   ## File Structure
   [Tree view of important directories]
   
   ## Configuration
   [Key config files and settings]
   
   ## Getting Started
   ```bash
   cd /path/to/project
   [setup commands]
   ```
   ```

3. **Create Current State note**
   ```markdown
   # [Project] - Current State
   
   Last updated: [timestamp]
   
   ## Quick Status
   [Current phase: Planning/Development/Testing/Production]
   
   ## Task Status
   - [ ] Initial task
   - [ ] Next task
   
   ## Next Steps
   1. First action
   2. Second action
   ```

**Time investment:** 10 minutes
**ROI:** Saves 30,000 tokens per subsequent conversation
**Break-even:** After 1st follow-up conversation

### Active Development

**Daily workflow:**

**Morning (1 minute):**
```markdown
Check [[Active Projects Dashboard]]
Review [[Project - Current State]]
Know exactly what to work on
```

**During work:**
```
Start Claude conversation with clear task
Document decisions as made
Update notes incrementally
Commit code progressively
```

**End of session (5 minutes):**
```
Update Current State
Create session summary (if significant)
Push git commits
Note blockers
```

**Weekly (15 minutes):**
```
Review all active projects
Update dashboard priorities
Archive completed tasks
Clean up note structure
```

### Project Completion

**When project is done:**

1. **Create final documentation**
   ```markdown
   # [Project] - Final Summary
   
   ## Project Overview
   [What it was, what it accomplished]
   
   ## Final Stats
   - Duration: X weeks
   - Conversations: Y
   - Key challenges: [list]
   
   ## Lessons Learned
   [What worked, what didn't]
   
   ## Archive Date
   [timestamp]
   ```

2. **Move to Archive**
   ```
   Projects/[Project]/ → Archive/[Project]/
   ```

3. **Update dashboard**
   - Remove from active
   - Add to completed section

---

## Multi-Project Management

### Active Projects Dashboard

**Create:** `Meta/Active Projects Dashboard.md`

```markdown
# Active Projects Dashboard

Last updated: [date]

## 🔥 Priority 1 (This Week)

### [Project A]
- **Status:** [Current focus area]
- **Next:** [Immediate task]
- **Link:** [[Project A - Current State]]
- **Deadline:** [if applicable]

### [Project B]
- **Status:** [Current focus area]
- **Next:** [Immediate task]  
- **Link:** [[Project B - Current State]]

## 📋 Priority 2 (This Month)

### [Project C]
- **Status:** [Phase]
- **Link:** [[Project C - Current State]]

## 💭 Backlog (Ideas)

- [Project idea 1]
- [Project idea 2]

## ✅ Recently Completed

- [Project X] - [Completion date]
- [Project Y] - [Completion date]

## 📊 Stats

- Active projects: X
- Completed this month: Y
- Avg conversations per project: Z
```

### Context Switching Strategy

**When switching between projects:**

**Don't:**
```
[Working on Project A]
Switch to Project B
"Remember Project B?"
→ 30,000 token context load
```

**Do:**
```
[Working on Project A]
Update [[Project A - Current State]]
Switch to Project B
"Task: [specific]
Context: [[Project B - Current State]]"
→ 2,000 token reference
```

**Savings per switch:** 28,000 tokens

**If working on 3 projects per day:**
- Traditional: 90,000 tokens wasted on switches
- Dashboard method: 6,000 tokens used
- **Savings: 84,000 tokens (93%)**

---

## Communication Patterns

### The Perfect First Message

**Structure:**
```
1. Task (what you want)
2. Context (where info lives)
3. Details (specifics)
4. Tools (which environment)
```

**Examples by type:**

**Bug fix:**
```
Task: Fix syntax error in organize-images.sh

Context: [[Project - Workflow]]
Error: Line 42: "unexpected token"
File: /path/to/script.sh

Use local bash
```

**Feature addition:**
```
Task: Add RSS feed to teardown.cafe

Context: [[Teardown Cafe - Technical Setup]]
Requirements:
- Use @astrojs/rss package
- Include last 10 posts
- Link in footer

Use local filesystem
```

**Research + implementation:**
```
Task: Research and implement image optimization

Context: [[Project - Current State]]
Current: Manual process with exiftool
Goal: Automate with sharp package
Must preserve: EXIF stripping

Research first, then implement
Use local filesystem
```

**Multi-step project:**
```
Task: Complete Phase 2 tasks

Context: [[Project - Current State]]
Tasks:
1. Feature X (est. 5K tokens)
2. Feature Y (est. 8K tokens)
3. Update docs (est. 3K tokens)

Estimated total: ~20K tokens
Use local filesystem
```

### Effective Follow-ups

**During conversation:**

**❌ Vague:**
```
"That didn't work"
"Can you fix it?"
"Try something else"
```

**✅ Specific:**
```
"Error: [exact error message]
Occurred when: [specific action]
File: [path]
Line: [number]"

"Requirement changed: [specific change]
Update: [exact modification needed]"

"Alternative approach: [specific suggestion]
Because: [reason for change]"
```

### When to Split Conversations

**Start new conversation if:**
- Current >70% budget
- Task is unrelated to current focus
- Major context shift needed
- Natural checkpoint reached

**Example:**
```
Current conversation: Bug fixing (60% budget)
New need: Add completely different feature

Action:
1. Finish current bug fix
2. Update Current State
3. Start fresh: "Add feature X..."
```

---

## Tool Selection Mastery

### Decision Matrix

```
┌─────────────────────────────────────┐
│ Is it Obsidian vault operation?    │
└────────┬──────────────────┬─────────┘
         │                  │
        YES                NO
         │                  │
         ▼                  ▼
   MCP Docker         Is it git/npm?
   (obsidian_*)            │
                      ┌────┴────┐
                     YES       NO
                      │         │
                      ▼         ▼
                  Local      Local
                  bash      Filesystem
```

### Common Operations

**Reading Obsidian notes:**
```
✓ MCP_DOCKER:obsidian_get_file_contents
✗ Filesystem:read_file
```

**Writing project files:**
```
✓ Filesystem:write_file
✗ MCP_DOCKER (not for non-vault files)
```

**Git operations:**
```
✓ bash_tool in project directory
✗ MCP Docker environment
✗ Filesystem tools (not for git)
```

**NPM commands:**
```
✓ bash_tool in project directory
✗ Docker environment
```

### Verification Steps

**Before git operations:**
```bash
pwd  # Must show: /Users/aim/Documents/[project]
echo $CONTAINER_ENV  # Should be empty
git status  # Verify in correct repo
```

**If uncertain:**
```
"Which environment should I use for this task?"
→ Claude will clarify
```

---

## Token Counter Integration

### Daily Usage Workflow

**Keep app open while working:**

1. **Draft messages in counter**
   - See live token count
   - Optimize if needed
   - Check projection

2. **Update conversation usage**
   - After every 3-5 exchanges
   - Based on Claude's estimates
   - Conservative numbers

3. **Color-coded actions**
   - 🟢 Green: Continue normally
   - 🟡 Orange: Start wrapping up
   - 🔴 Red: Finish current task, document

### Optimization Loop

**Message is too long:**
```
1. See high token count in counter
2. Edit for conciseness
3. Check if under target
4. Copy and send
```

**Projection shows red:**
```
1. See "After sending: 155,000 / 190,000 (81%)"
2. Decide: Is this worth it?
   - Critical task: Send anyway, finish quickly
   - Can wait: Document, start fresh
3. Update plan accordingly
```

### Calibration

**After a few conversations:**
- Note actual vs. estimated usage
- Adjust your mental model
- Update estimation patterns

**Example calibration:**
```
Thought simple task = 5K tokens
Actually used = 12K tokens
Reason: Multiple tool calls + iteration

Update: Similar tasks = 10-15K estimate
```

---

## Common Scenarios

### Scenario 1: Quick Question

**Situation:** Simple factual question

**Approach:**
```
Direct question (no note reference needed)
"What's the syntax for [X] in [language]?"

Expected: 500-2,000 tokens total
```

**When to reference notes:**
Only if question relates to ongoing project

### Scenario 2: Debug Session

**Situation:** Code not working, need help

**Approach:**
```
Task: Debug error in [file]

Context: [[Project - Technical Setup]]
Error: [exact error message]
Code: [relevant section]
What I tried: [brief list]

Use local filesystem
```

**Expected:** 3,000-8,000 tokens
**If extends beyond:** Document findings, continue in new chat

### Scenario 3: Major Feature

**Situation:** Implementing complex new functionality

**Approach - Option A (Single conversation):**
```
Task: Implement feature X

Context: [[Project - Current State]]
Requirements: [detailed list]

Estimated complexity: High (~30K tokens)
Ready for extended conversation
```

**Approach - Option B (Phased):**
```
Conversation 1: Research and design (~15K)
Conversation 2: Core implementation (~20K)
Conversation 3: Testing and polish (~15K)
```

**Choose based on:**
- Current budget usage
- Feature complexity
- Your time availability

### Scenario 4: Learning New Topic

**Situation:** Need to understand concept/technology

**Approach:**
```
Task: Explain [topic] and show examples

Context: My level - [beginner/intermediate/advanced]
Goal: Understand enough to [specific objective]

Use visualizations, prefer examples over theory
```

**Expected:** 5,000-15,000 tokens
**Follow-up:** Create dedicated note for topic

### Scenario 5: Project Planning

**Situation:** Starting new project, need architecture help

**Approach:**
```
Task: Help plan [project name]

Current idea: [brief description]
Requirements:
- Requirement 1
- Requirement 2

Questions:
- Tech stack recommendation?
- Architecture approach?
- Potential challenges?

Create planning document in Obsidian
```

**Expected:** 10,000-20,000 tokens
**Output:** Comprehensive planning note to reference

---

## Emergency Procedures

### Hit Limit Unexpectedly

**Immediate actions:**
1. **Don't panic** - conversation saves automatically
2. **Screen capture** - if Claude showed important info
3. **Git commit** - if code was generated
4. **Quick notes** - bullet points of key info

**Recovery:**
```
New conversation:
"Continuing from previous chat that hit limit

Task: [what you were doing]
Context: [[Session notes]] (just created)
Progress: [what was completed]
Next: [immediate next step]"
```

### Lost Context

**If you can't remember what you were doing:**

1. **Check Obsidian first**
   - Current State note
   - Recent session notes
   - Git commit messages

2. **Search past chats** (last resort)
   ```
   Use conversation_search tool
   Keywords: [project name] [key terms]
   ```

3. **Start fresh with best guess**
   - Document uncertainty
   - Rebuild context progressively

### Tool Used Wrong Environment

**Symptom:** Git commit disappeared, file not where expected

**Check:**
```bash
pwd  # Where am I?
ls -la  # What files here?
```

**If in Docker:**
```
Exit conversation
Start new: "Continue [task]
Use local filesystem at /Users/aim/Documents/[project]"
```

**Prevention:** Add to guidelines, verify before git operations

---

## Continuous Improvement

### Monthly Review

**Set calendar reminder:**

**Review checklist:**
- [ ] Which projects hit conversation limits?
- [ ] Why did they hit limits?
- [ ] Which optimization strategies worked?
- [ ] Which notes were most referenced?
- [ ] What note structure improvements needed?
- [ ] Any new patterns to document?

**Update:**
- Guidelines note
- Templates
- Dashboard structure
- Project organization

### Metrics to Track

**Conversation efficiency:**
```markdown
## Conversation Stats - [Month]

- Total conversations: X
- Average tokens used: Y
- Times hit limit: Z
- Projects completed: A

## Most Efficient Conversation
- Project: [name]
- Tokens: X (~% of budget)
- Accomplished: [impressive result]

## Lessons Learned
- [Key insight 1]
- [Key insight 2]
```

### Optimization Opportunities

**When you notice:**
```
"I keep explaining [X] in every conversation"
→ Create dedicated note for [X]

"These 3 tasks always go together"
→ Create batch template

"I always forget to do [Y]"
→ Add to checklist/guidelines
```

---

## Advanced Patterns

### Project Templates

**Create reusable structures:**

```markdown
# Project Template - Web App

When starting new web app, copy this structure:

## Notes to Create
- Index.md
- Technical Setup.md
- Design System.md (if UI-heavy)
- Current State.md

## Initial Current State
```markdown
## Stack Decision
- Frontend: [TBD]
- Backend: [TBD]
- Database: [TBD]

## Phase 1 Tasks
- [ ] Initialize repository
- [ ] Set up development environment
- [ ] Create basic structure
- [ ] First feature implementation
```

## First Conversation Template
```markdown
Task: Initialize [project name]

Stack considerations:
- Requirement 1
- Requirement 2

Create project structure and documentation
Use local filesystem
```
```

### Conversation Chains

**For multi-part projects:**

```markdown
# [Project] - Conversation Chain

## Phase 1: Foundation
- Conv 1: Setup + basic structure
- Conv 2: Core functionality A
- Conv 3: Core functionality B

## Phase 2: Features
- Conv 4: Feature set A
- Conv 5: Feature set B
- Conv 6: Integration

## Phase 3: Polish
- Conv 7: Testing
- Conv 8: Optimization
- Conv 9: Documentation

Each conversation ~40-60K tokens
Total project: 360-540K tokens (budget-aware)
```

### Knowledge Base Building

**Over time, accumulate reusable notes:**

```
Meta/
├── Claude Interaction Guidelines.md
├── Token Optimization.md
├── Project Templates/
│   ├── Web App Template.md
│   ├── Python CLI Template.md
│   └── Analysis Project Template.md
├── Common Patterns/
│   ├── Git Workflow.md
│   ├── Docker Setup.md
│   └── API Integration.md
└── Reference/
    ├── Useful Commands.md
    ├── Config Snippets.md
    └── Debug Checklist.md
```

**Benefit:** Instant reference, no re-explanation needed

---

## Success Stories

### Before Optimization

**Typical session:**
```
- Start: "Hey, remember that project?"
- Load context: 30,000 tokens
- Work: 40,000 tokens
- Total: 70,000 tokens (37% budget)
- Conversations to limit: ~2.7
```

**Pain points:**
- Constant context loss
- Repeated explanations
- Unclear what was accomplished
- Difficult to resume
- Hitting limits frustrating

### After Optimization

**Typical session:**
```
- Start: "Task: [X]. Context: [[Note]]"
- Reference: 2,000 tokens
- Work: 40,000 tokens
- Total: 42,000 tokens (22% budget)
- Conversations to limit: ~4.5
```

**Benefits:**
- Instant context
- Clear objectives
- Tracked progress
- Easy resume
- 67% more conversations
- Better documentation
- Less frustration

### Real Example: Teardown Cafe

**Original approach (estimated):**
```
If using "continue conversation" pattern:
- Setup conversation: 80K tokens
- Fix conversation: 70K tokens  
- Docs conversation: 90K tokens
Total: 240K tokens, 2 limit cycles

Result: Fragmented, frustrated
```

**Optimized approach (actual):**
```
With Obsidian notes:
- Setup + document: 70K tokens
- Fix + document: 60K tokens
- Final docs: 80K tokens
Total: 210K tokens, 1 limit cycle

Result: Comprehensive documentation,
        ready for future work
```

**Improvement:**
- 30K tokens saved
- Better documentation
- Easier to continue
- Valuable knowledge base created

---

## Quick Reference

### Starting Conversation Checklist

- [ ] Task clearly defined?
- [ ] Relevant notes referenced?
- [ ] Tools specified?
- [ ] Current state documented?
- [ ] Token budget awareness?

### During Conversation Checklist

- [ ] Documenting decisions?
- [ ] Committing code progressively?
- [ ] Tracking token usage?
- [ ] Asking clarifying questions?
- [ ] Testing as you go?

### Ending Conversation Checklist

- [ ] Current task completed?
- [ ] Code committed?
- [ ] Current State updated?
- [ ] Session summary created (if significant)?
- [ ] Next steps clear?
- [ ] Blockers documented?

### Emergency Checklist

- [ ] Hit limit - created summary?
- [ ] Lost context - checked notes?
- [ ] Wrong tool - verified environment?
- [ ] Unclear - asked for clarification?

---

## Conclusion

### Core Principles

1. **External memory beats re-explanation**
   - Obsidian notes = permanent context
   - Reference, don't reload

2. **Precision beats verbosity**
   - Clear task statements
   - Direct references
   - Focused objectives

3. **Progressive beats perfect**
   - Document as you go
   - Commit incrementally
   - Refine over time

4. **Planning beats improvisation**
   - Know your objective
   - Track your budget
   - Document your progress

### Expected Outcomes

**Week 1:**
- Learning new patterns
- Some friction
- Building notes

**Week 2-4:**
- Patterns becoming natural
- Seeing token savings
- Feeling more efficient

**Month 2+:**
- Habits solidified
- Extensive knowledge base
- Rarely hitting limits
- High productivity

### Final Words

**This workflow is:**
- ✓ Proven effective (real power user testing)
- ✓ Progressive (start simple, add complexity)
- ✓ Adaptable (customize to your needs)
- ✓ Sustainable (low maintenance once established)

**You'll know it's working when:**
- Conversations feel productive
- Context is always available
- Progress is always clear
- Limits are rarely hit
- Work quality improves

**Start today:**
1. Create Active Projects Dashboard
2. Pick one project
3. Create Current State note
4. Start next conversation with reference
5. Experience the difference

---

*This workflow transforms Claude from a tool you fight against into a persistent collaborator with perfect memory. Your Obsidian vault becomes Claude's external brain.*

---

**Created:** October 16, 2025
**Based on:** Optimized power user experience  
**Success rate:** 67% more conversations per limit cycle
**Time to proficiency:** 2-4 weeks of consistent use

## Tags
#workflow #power-user #claude #obsidian #practical-guide #productivity

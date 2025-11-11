# Teardown Cafe - Content Workflow

## Overview
Complete process for adding new teardowns from photo capture to publication, with Obsidian knowledge base integration.

## Phase 1: Photo Capture & Download

### Best Practices
- **Lighting:** Natural light or diffused LED
- **Background:** Clean surface (teal repair mat used in examples)
- **Angles:** Overhead for components, side angles for assembly steps
- **Focus:** Clear focus on key components
- **Quantity:** 1-5 photos per project (documented examples: 1-6 photos)

### Download from Phone
**Method:** Upload directly to Claude chat
- Preserves original quality
- Allows batch EXIF stripping
- Enables immediate organization

**Alternative:** AirDrop to ~/Downloads

## Phase 2: Image Organization

### Automated Script Method

**File:** `organize-images.sh`

**Usage:**
```bash
cd ~/Documents/teardown-cafe
chmod +x organize-images.sh
./organize-images.sh
```

**What it does:**
1. Scans `~/Downloads` for IMG*.jpg files
2. Prompts for project slug (e.g., "raspberry-pi-5-nvme")
3. Renames files sequentially with descriptive names
4. Copies to `public/images/[project-slug]/`
5. Displays confirmation for each file

**Example transformation:**
```
IMG20251015184233.jpg → 01-components-overview.jpg
IMG20251015192501.jpg → 02-raspberry-pi-5-ports.jpg
IMG20251015192851.jpg → 03-hat-installation-with-fan.jpg
```

### Manual Method (Fallback)
```bash
cd ~/Documents/teardown-cafe
mkdir -p public/images/[project-slug]

cp ~/Downloads/IMG20251015184233.jpg \
   public/images/[project-slug]/01-components-overview.jpg
   
cp ~/Downloads/IMG20251015192501.jpg \
   public/images/[project-slug]/02-raspberry-pi-5-ports.jpg
   
# Repeat for all images
```

### EXIF Stripping (Privacy Critical)

**Tool:** exiftool

**Installation:**
```bash
brew install exiftool
```

**Usage:**
```bash
cd public/images/[project-slug]
exiftool -all= *.jpg
rm *_original  # Remove backup files
```

**What gets removed:**
- GPS coordinates
- Camera make/model
- Timestamps
- User comments
- Software used
- Copyright info
- Any other metadata

**Verification:**
```bash
exiftool *.jpg  # Should show minimal metadata
```

## Phase 3: Content Creation

### Markdown File Structure

**Location:** `src/content/teardowns/[slug].md`

**Template:**
```markdown
---
title: "Device Name - Brief Description"
description: "One-sentence summary of the teardown"
pubDate: 2025-10-15
heroImage: "/images/[project-slug]/01-main-photo.jpg"
device: "monitor | laptop | smartphone | raspberry-pi | nas | mechanical-keyboard | other"
difficulty: "easy | medium | hard"
obsidianNotes:
  - title: "Related Note Title"
    path: "Folder/Note Name"
  - title: "Another Related Note"
    path: "Projects/Another Note"
---

## Why I Did This

[Motivation paragraph]

## The Build/Teardown Process

[Step-by-step description with photo references]

![Component overview](/images/[project-slug]/01-components-overview.jpg)
*Caption describing what's in the photo*

![Next step](/images/[project-slug]/02-next-step.jpg)
*Caption for next step*

## What I Learned

[Key takeaways and insights]

## Tools Used

- Tool 1
- Tool 2
- Tool 3

## Would I Recommend?

[Recommendation for others considering similar project]

## Performance/Results (if applicable)

[Benchmarks, measurements, or outcomes]
```

### Difficulty Rating Guidelines

**Easy (🟢):**
- Few screws (5-10)
- Standard tools only
- No delicate components
- Low risk of damage
- Example: Monitor teardown

**Medium (🟡):**
- Multiple screw types
- Some specialty tools needed
- Moderate component density
- Some risk management required
- Example: Laptop teardown

**Hard (🔴):**
- Many tiny screws
- Specialty tools required
- High component density
- Significant damage risk
- Requires patience and skill
- Example: Smartphone teardown

### Device Categories

```
monitor          → Displays, screens
laptop           → Portable computers
smartphone       → Mobile phones, tablets
raspberry-pi     → Pi boards and projects
nas              → Network storage builds
mechanical-keyboard → Custom keyboards
other            → Miscellaneous projects
```

## Phase 4: Local Verification

### Start Development Server
```bash
cd ~/Documents/teardown-cafe
npm run dev
```

**Server:** http://localhost:4321

### Verification Checklist
- [ ] New teardown card appears on homepage
- [ ] Correct emoji for device category
- [ ] Difficulty badge displays correctly
- [ ] Hero image loads properly
- [ ] Card hover animation works
- [ ] Click card → full teardown page loads
- [ ] All images display in correct order
- [ ] Captions are readable
- [ ] Obsidian note links work (if applicable)
- [ ] Navigation back to homepage works

### Hard Refresh
If changes don't appear:
```bash
# Stop server (Ctrl+C)
rm -rf .astro dist  # Clear cache
npm run dev         # Restart
```

**Browser:** Cmd + Shift + R (force reload)

## Phase 5: Git Commit

### Commit Message Format
```bash
git add -A
git commit -m "Add teardown: [Device Name]

- [Number] process images documented
- [Key features or findings]
- Linked to [Obsidian notes if applicable]
- Difficulty: [easy/medium/hard]
- [Any special notes or challenges]"
```

### Example Commit
```bash
git commit -m "Add teardown: Raspberry Pi 5 NVMe Build

- 6 assembly process images
- Boot speed benchmarks and optimization tips
- Linked to homelab Pi-hole configuration notes
- Includes thermal management analysis
- Difficulty: easy"
```

### Push to GitHub (Optional)
```bash
git push origin main
```

## Phase 6: Obsidian Sync

### Sync Script

**File:** `sync-to-obsidian.sh`

**Usage:**
```bash
cd ~/Documents/teardown-cafe
chmod +x sync-to-obsidian.sh
./sync-to-obsidian.sh
```

### What It Does

1. **Scans** all markdown files in `src/content/teardowns/`
2. **Extracts** metadata from frontmatter:
   - Title
   - Date
   - Device category
   - Difficulty
   - Related Obsidian notes
3. **Generates** statistics:
   - Total teardowns count
   - Breakdown by device type
   - Difficulty distribution
4. **Updates** `Projects/Teardowns Index.md` in Obsidian vault
5. **Creates** bidirectional links:
   - From index to teardowns website
   - From website to relevant vault notes

### Generated Index Structure

```markdown
# Teardowns Index

Last updated: [timestamp]

## Statistics
- Total teardowns: X
- Devices: X monitors, X laptops, X Pi projects, etc.
- Difficulty: X easy, X medium, X hard

## By Device Type

### Monitors
- [Dell U2415 Monitor](https://teardown.cafe/teardowns/monitor-oct-2025) - Easy
  - Related: [[Display Technology]]

### Raspberry Pi
- [Pi 5 NVMe Build](https://teardown.cafe/teardowns/raspberry-pi-5-nvme) - Easy
  - Related: [[Pi-hole Setup]], [[ARM Architecture]]

[etc.]
```

### Obsidian Link Format

**Website to Obsidian:**
```
obsidian://open?vault=YourVault&file=Path/To/Note
```

**Obsidian to Website:**
```
[Teardown Title](https://teardown.cafe/teardowns/slug)
```

## Phase 7: Deployment (Planned)

### Deployment Targets

**Option A: Vercel (Recommended)**
- Automatic builds from GitHub
- Zero config for Astro
- Free tier sufficient
- Custom domain support

**Option B: Netlify**
- Similar to Vercel
- Good Astro support
- Drag-and-drop option

### Deployment Process (Future)
```bash
# Connect GitHub repo to Vercel
# Vercel auto-detects Astro
# Every push to main triggers new build
# Site automatically updates
```

## Batch Processing Workflow

### For Multiple Teardowns

**Optimal workflow:**
1. Download all photos for project batch
2. Run organize script for each project
3. Strip EXIF for all simultaneously
4. Create all markdown files
5. Single verification pass
6. Bulk commit

**Example session:**
```bash
# Organize project 1
./organize-images.sh  # Input: thinkpad-t480

# Organize project 2  
./organize-images.sh  # Input: smartphone-pixel-6

# Strip EXIF batch
cd public/images
find . -name "*.jpg" -exec exiftool -all= {} \;
find . -name "*_original" -delete

# Create markdown files (via Claude or manually)

# Verify all
npm run dev

# Commit all
git add -A
git commit -m "Add 2 teardowns: ThinkPad T480, Pixel 6"

# Sync to Obsidian
./sync-to-obsidian.sh
```

## Content Guidelines

### Photo Descriptions
- **Be specific:** "PCIe 3.0 NVMe hat with fan" not "the hat"
- **Mention key details:** Screw types, cable colors, connectors
- **Note challenges:** "Tight fit required careful alignment"

### Writing Style
- Casual, first-person ("I found...", "This surprised me...")
- Educational, not prescriptive
- Honest about mistakes and learning
- Encouraging for beginners

### What to Document
- **Why:** Motivation for the teardown/build
- **Process:** Step-by-step with photos
- **Challenges:** What was tricky
- **Learnings:** What you discovered
- **Tools:** What you actually used
- **Results:** How it turned out
- **Recommendations:** Would you do it again?

### What NOT to Include
- Personal location data (stripped via EXIF)
- Sensitive information
- Copyrighted repair guides (link instead)
- Dangerous modifications without warnings

## RSS Feed (Future Enhancement)

### Planned Implementation
**Plugin:** @astrojs/rss

**What it enables:**
- Automatic feed.xml generation
- Lists 10 most recent teardowns
- Subscribers get notified of new content
- Zero effort after initial setup

**Tech audience loves RSS** - standard for tech blogs

## Analytics (Privacy-Friendly, Future)

### Options Considered
- **Plausible:** Privacy-focused, no cookies
- **GoatCounter:** Open source, simple
- **None:** Current state (maximum privacy)

**Decision:** Deploy first, add analytics later if needed

## Estimated Time Per Teardown

### Full Process Breakdown
- **Photo capture:** 10-30 mins (during actual teardown)
- **Download & organize:** 5 mins
- **EXIF stripping:** 2 mins
- **Markdown writing:** 20-40 mins
- **Local verification:** 5 mins
- **Git commit:** 2 mins
- **Obsidian sync:** 1 min

**Total:** 45-80 minutes per teardown

### Optimization Tips
- Write notes during teardown process
- Use voice memos for descriptions
- Batch similar tasks (all EXIF, all commits)
- Template reuse for similar devices

## Quality Checklist

Before committing:
- [ ] All images properly named and sequential
- [ ] EXIF data stripped (verified with exiftool)
- [ ] Markdown frontmatter complete and accurate
- [ ] All images have descriptive captions
- [ ] Grammar and spelling checked
- [ ] Links tested (both internal and to Obsidian)
- [ ] Difficulty rating appropriate
- [ ] Device category correct
- [ ] Hero image is the best photo
- [ ] Local preview looks good
- [ ] Commit message is descriptive

## Troubleshooting Common Issues

### Images Not Showing
```bash
# Check file paths in markdown match actual files
ls public/images/[project-slug]/

# Verify case sensitivity (macOS is case-insensitive, web servers aren't)
# Use lowercase, dashes, no spaces
```

### Obsidian Links Not Working
- Verify vault name in link matches actual vault name
- Check file path exists in vault
- Ensure Obsidian URI protocol is enabled

### Dev Server Not Updating
```bash
# Nuclear option: clear everything
rm -rf .astro dist node_modules/.astro
npm run dev
```

### Git Showing Unexpected Files
```bash
# Check you're in correct directory
pwd  # Should show /Users/aim/Documents/teardown-cafe

# Not in Docker environment
```

## Related Notes
- [[Teardown Cafe - Project Overview]]
- [[Teardown Cafe - Technical Setup]]
- [[Teardown Cafe - Troubleshooting]]

---
*Created: October 16, 2025*
*Last Updated: October 16, 2025*

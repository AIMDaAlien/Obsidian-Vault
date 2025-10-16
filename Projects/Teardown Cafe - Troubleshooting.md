# Teardown Cafe - Troubleshooting & Lessons Learned

## Major Issues Encountered

### Issue #1: Astro Version Compatibility Gap

**Symptom:** Site not rendering correctly, dev toolbar appearing unexpectedly

**Root Cause:**
- Project designed with Astro knowledge from January 2025
- User running Astro v5.14.5 (October 2025 release)
- 9+ months of breaking changes between design and implementation

**Impact:** High - Core functionality affected

**Resolution Process:**

1. **Version identification:**
```bash
npm list astro
# Output: astro@5.14.5
```

2. **Research current documentation:**
- Searched Astro v5.x breaking changes
- Identified Content Collections API updates
- Found image optimization syntax changes
- Discovered dev toolbar introduction

3. **Code updates:**
- Updated all component imports to v5 syntax
- Revised content collection configuration
- Adjusted image optimization calls
- Disabled dev toolbar for cleaner UI

**Configuration change:**
```javascript
// astro.config.mjs
export default defineConfig({
  // ...
  devToolbar: {
    enabled: false  // Removed visual clutter
  }
});
```

**Lesson Learned:** Always verify framework version before starting implementation. Major version jumps require systematic compatibility review.

**Confidence in Resolution:** 98%

---

### Issue #2: Bash Array Syntax Incompatibility

**Symptom:** `organize-images.sh` script failing with syntax errors

**Root Cause:**
- Script used bash-specific array syntax
- macOS default shell is zsh (not bash)
- Arrays declared as `IMAGES=("file1" "file2")` 
- Syntax incompatible between shells

**Code that failed:**
```bash
#!/bin/bash
declare -a IMAGES=(
  "IMG20251015184233.jpg:01-components-overview.jpg"
  "IMG20251015192501.jpg:02-raspberry-pi-5-ports.jpg"
)
```

**Impact:** Medium - Script automation broken, manual fallback required

**Resolution Options:**

**Option A: Manual cp commands (Immediate workaround)**
```bash
cd ~/Documents/teardown-cafe
mkdir -p public/images/[project-slug]
cp ~/Downloads/IMG*.jpg public/images/[project-slug]/01-name.jpg
# Repeat for each file
```

**Option B: POSIX-compliant rewrite (Long-term fix)**
```bash
#!/bin/sh
# Use newline-separated list instead of arrays
# More portable, works in sh/bash/zsh
```

**Option C: Force bash execution**
```bash
bash organize-images.sh
# Instead of: ./organize-images.sh
```

**Lesson Learned:** Test scripts on target environment. macOS ships with zsh, not bash. Write POSIX-compliant scripts or explicitly specify interpreter.

**Confidence in Resolution:** 95% (workaround) / 85% (POSIX rewrite needed)

---

### Issue #3: Docker Environment Git Commits

**Symptom:** Git commits happening in wrong location, files not where expected

**Root Cause:**
- Accidentally ran git commands while in Docker container
- Container filesystem separate from host macOS filesystem
- Changes committed to ephemeral container storage
- Lost on container restart

**Impact:** Low - Caught quickly, no permanent data loss

**Prevention:**
```bash
# Always verify working directory
pwd
# Should output: /Users/aim/Documents/teardown-cafe

# Check if in Docker
echo $CONTAINER_ENV  # Should be empty on host

# Verify git remote
git remote -v
# Should point to actual GitHub repo
```

**Lesson Learned:** Always confirm working directory before git operations. Add visual indicators (shell prompt) showing container vs. host.

**Confidence in Prevention:** 99%

---

### Issue #4: Hard Refresh Required After Changes

**Symptom:** Local changes not appearing in browser despite dev server running

**Root Cause:**
- Astro's aggressive caching for performance
- Browser also caching static assets
- `.astro` build cache not invalidating

**Symptoms:**
- Updated markdown not showing
- New images not displaying
- CSS changes not applying

**Resolution Steps:**

**Level 1: Browser hard refresh**
```bash
# macOS: Cmd + Shift + R
# Windows: Ctrl + Shift + R
```

**Level 2: Clear Astro cache**
```bash
# Stop dev server (Ctrl+C)
rm -rf .astro dist
npm run dev
```

**Level 3: Nuclear option**
```bash
rm -rf .astro dist node_modules/.astro
npm run dev
```

**When to use each:**
- Level 1: CSS/minor changes
- Level 2: Content changes not appearing
- Level 3: Major config changes, weird behavior

**Lesson Learned:** Caching is a feature and a bug. Always try hard refresh before assuming code is broken.

**Confidence in Resolution:** 99%

---

### Issue #5: Dev Toolbar Confusion

**Symptom:** Unfamiliar toolbar appearing at bottom of page

**Root Cause:**
- New Astro v5.x feature not present in v4.x
- Dev toolbar for debugging and optimization
- Not documented in January 2025 knowledge

**User Concern:** "maybe there are new things added since your info cut off date that might have conflict with what we're doing"

**Investigation:**
- Researched Astro v5 changelog
- Found dev toolbar introduction in v5.0
- Confirmed no conflicts with existing code
- Feature is beneficial but optional

**Resolution:**
```javascript
// astro.config.mjs
export default defineConfig({
  devToolbar: {
    enabled: false  // Disabled for cleaner interface
  }
});
```

**Lesson Learned:** New framework features aren't necessarily problematic. Investigate before removing. Toolbar could be useful for performance debugging.

**Confidence in Resolution:** 100%

---

### Issue #6: EXIF Data Privacy Concerns

**Symptom:** User concerned about metadata in uploaded photos

**Root Cause:**
- Phone cameras embed GPS, timestamps, device info
- Could reveal personal location and equipment
- Privacy-first design principle

**Impact:** High - Privacy is critical

**Resolution:**

**Tool installation:**
```bash
brew install exiftool
```

**Usage:**
```bash
cd public/images/[project-slug]
exiftool -all= *.jpg  # Strip all metadata
rm *_original         # Remove backup files
```

**Verification:**
```bash
exiftool *.jpg
# Should show minimal/no metadata
```

**Automated in workflow:**
- Every image processed before commit
- Verified before publication
- No exceptions

**Lesson Learned:** Privacy must be systematic, not optional. Automate privacy-preserving steps to prevent human error.

**Confidence in Resolution:** 100%

---

## Best Practices Developed

### 1. Systematic Troubleshooting Approach

When something doesn't work:
1. **Verify environment** (host vs. Docker, correct directory)
2. **Check versions** (framework, dependencies)
3. **Clear caches** (build, browser)
4. **Research recent changes** (framework updates, breaking changes)
5. **Test incrementally** (one change at a time)
6. **Document findings** (for future reference)

### 2. Git Workflow Discipline

```bash
# Before any git command:
pwd                    # Verify location
git status             # Check what's being tracked
git diff               # Review changes

# After commit:
git log --oneline -3   # Verify commit succeeded
git remote -v          # Confirm remote is correct
```

### 3. Framework Update Strategy

When working with frameworks beyond knowledge cutoff:
1. Check current version (`npm list [package]`)
2. Read migration guides
3. Search for breaking changes
4. Test in isolation before full integration
5. Keep documentation updated

### 4. Privacy-First Development

**Default assumptions:**
- All images have metadata
- All user data is sensitive
- Privacy violations are permanent
- Automate privacy protection

**Verification checklist:**
- [ ] EXIF stripped from all images
- [ ] No hardcoded paths with usernames
- [ ] No API keys in code
- [ ] Git history clean of sensitive data

### 5. Cache Management

**Understanding cache layers:**
1. **Browser cache:** Assets, images, CSS
2. **Service worker cache:** (not used yet)
3. **Framework cache:** `.astro` directory
4. **Module cache:** `node_modules/.cache`

**When to clear:**
- CSS not updating → Browser refresh
- Content not updating → Framework cache
- Weird build errors → Everything

### 6. Script Portability

**Writing portable shell scripts:**
```bash
#!/bin/sh
# Use sh, not bash, for maximum compatibility

# Avoid bash-specific features:
# - Arrays (use newline-separated lists)
# - [[ ]] (use [ ] instead)
# - $'...' strings (use "..." instead)

# Test on target platform before deployment
```

---

## Performance Observations

### Build Speed
- **Initial build:** ~3-4 seconds
- **Incremental rebuild:** <1 second
- **Full cache clear:** ~5-6 seconds

**Bottlenecks identified:**
- Image optimization (largest impact)
- MDX parsing (minimal)
- CSS processing (negligible)

### Development Server
- **Hot reload:** Near-instant (<500ms)
- **Memory usage:** ~150MB
- **CPU usage:** Low (except during image optimization)

**Optimization opportunities:**
- Pre-optimize images before adding
- Use smaller source images
- Consider lazy loading for galleries

---

## Unresolved Questions

### 1. Deployment Platform
**Decision pending:** Vercel vs. Netlify

**Considerations:**
- Build times
- Custom domain setup
- Free tier limits
- Automatic deployments

**Current status:** Can test both, decide based on experience

### 2. RSS Feed Implementation
**Status:** Planned but not implemented

**Blocker:** None, just time prioritization

**Estimated effort:** 1 hour (plugin install + config)

### 3. Analytics Addition
**Status:** Deferred for privacy review

**Options:**
- Plausible (privacy-friendly, paid)
- GoatCounter (open source, self-hosted)
- None (maximum privacy)

**Current decision:** Launch without, add later if needed

### 4. Domain Purchase
**Status:** Not purchased

**Domain:** teardown.cafe (~$30/year)

**Waiting for:** Initial content completion and deployment testing

---

## Workflow Refinements

### Original Workflow Issues
1. Too many manual steps
2. Error-prone file naming
3. No verification checkpoints
4. Privacy checks manual

### Improved Workflow
1. **Automated scripts** for repetitive tasks
2. **Sequential naming** for consistency
3. **Dev server verification** before commit
4. **Automated EXIF stripping** in script

### Future Improvements
- **Image optimizer script** (resize + compress)
- **Markdown template generator** (interactive CLI)
- **Pre-commit hooks** (verify EXIF, lint markdown)
- **CI/CD pipeline** (auto-deploy on push)

---

## Technical Debt

### Known Issues
1. **organize-images.sh** - Needs POSIX compliance rewrite
2. **Manual image naming** - Could be more automated
3. **No image optimization** - Source images not compressed
4. **No tests** - Manual verification only

### Priority
- **High:** POSIX script rewrite (affects usability)
- **Medium:** Image optimization (affects load time)
- **Low:** Test suite (nice-to-have for now)

### Time Estimates
- Script rewrite: 30 mins
- Image optimization: 1 hour
- Test suite: 4-6 hours (overkill for current scale)

---

## Lessons for Future Projects

### 1. Version Management
- Document all framework/tool versions in README
- Include version checks in setup scripts
- Test against intended deployment environment

### 2. Incremental Development
- Ship minimum viable version first
- Add features based on actual needs
- Don't over-engineer for imagined scenarios

### 3. Documentation
- Write docs alongside code
- Include troubleshooting sections
- Document "why" not just "how"

### 4. Privacy by Design
- Build privacy protections into workflow
- Automate privacy-preserving steps
- Make violations impossible, not just unlikely

### 5. Framework Knowledge Gaps
- Be transparent about knowledge cutoff limitations
- Research current state before recommending solutions
- Test recommendations against current versions

---

## Conversation Management

### Challenge: Token Limits
**Issue:** "I hit my conversation usage too often"

**Root cause:**
- Complex project with many iterations
- Each troubleshooting session adds context
- Claude's responses comprehensive (high token usage)

**Solutions developed:**
1. **Obsidian notes** - Persistent documentation
2. **Conversation search** - Reference past discussions
3. **README.md** - Quick reference in project
4. **WORKFLOW.md** - Step-by-step guides

### Multi-Conversation Strategy
- **Conversation 1:** Initial setup + first teardown
- **Conversation 2:** Astro compatibility fixes
- **Conversation 3:** (Current) Documentation + future planning

**Benefit:** Each conversation focused, easier to search later

---

## Success Metrics

### What Worked Well
✅ Material You 3 dark theme implementation
✅ Privacy-first approach with EXIF stripping
✅ Systematic troubleshooting methodology
✅ Obsidian integration for bidirectional linking
✅ Git workflow with descriptive commits
✅ Modular file organization

### What Needs Improvement
⚠️ Script portability (bash vs. zsh)
⚠️ Image optimization (manual process)
⚠️ Documentation completeness (work in progress)
⚠️ Test coverage (none yet)

### Overall Assessment
**Confidence in project foundation:** 95%

**Remaining uncertainties:**
- Deployment platform choice (5%)
- Long-term maintenance effort (unknowable)

---

## Related Notes
- [[Teardown Cafe - Project Overview]]
- [[Teardown Cafe - Technical Setup]]
- [[Teardown Cafe - Design System]]
- [[Teardown Cafe - Content Workflow]]

---
*Created: October 16, 2025*
*Last Updated: October 16, 2025*

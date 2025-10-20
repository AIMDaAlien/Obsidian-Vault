# Teardown Cafe - Current State

Last updated: October 16, 2025 - Initial creation

## Related Documentation
*Claude: Read these based on task type*

**For any teardown work:**
- [[Teardown Cafe - Content Workflow]] - Adding photos, creating teardowns, EXIF stripping
- [[Teardown Cafe - Documentation Index]] - Complete guide navigation

**For technical/code changes:**
- [[Teardown Cafe - Technical Setup]] - Astro config, file structure, dependencies
- [[Teardown Cafe - Troubleshooting]] - Known issues and solutions

**For design/styling:**
- [[Teardown Cafe - Design System]] - Material You 3 tokens, colors, typography

**For understanding the project:**
- [[Teardown Cafe - Project Overview]] - Vision, philosophy, tech stack

---

## Quick Context

Device teardown showcase website built with Astro v5.14.5 and Material You 3 design system. Privacy-first approach with EXIF stripping. Currently has 2 teardowns: Dell U2415 monitor and Raspberry Pi 5 NVMe build.

**Location:** `/Users/aim/Documents/teardown-cafe/`

---

## Task Status

### Completed ✅
- [x] Project scaffolding and Astro setup
- [x] Material You 3 dark theme (periwinkle palette)
- [x] Content collections configuration
- [x] First teardown: Dell U2415 Monitor (Oct 14, 2025)
- [x] Second teardown: Raspberry Pi 5 NVMe Build (Oct 15, 2025)
- [x] Image organization automation (organize-images.sh)
- [x] EXIF stripping workflow
- [x] Obsidian bidirectional linking
- [x] Git repository initialized
- [x] Comprehensive documentation

### In Progress 🔄
- [ ] POSIX-compliant script rewrite (organize-images.sh bash→zsh issue)
- [ ] Additional teardown content (pending photos)

### Next Up 📋
- [ ] RSS feed implementation (@astrojs/rss)
- [ ] Image optimization automation (sharp package)
- [ ] Deployment to Vercel/Netlify
- [ ] Domain purchase (teardown.cafe)

### Future Considerations 💭
- [ ] Privacy-friendly analytics (Plausible/GoatCounter)
- [ ] Search functionality
- [ ] Category filtering
- [ ] Image gallery lightbox

---

## Current Focus

**None** - Project in maintenance mode, awaiting new content or feature requests

**Blocked by:** None

---

## Recent Changes

- **Oct 16, 2025:** Created comprehensive Obsidian documentation suite
- **Oct 15, 2025:** Added Raspberry Pi 5 NVMe teardown with 6 images
- **Oct 15, 2025:** Troubleshot Astro v5 compatibility issues
- **Oct 14, 2025:** Initial project setup with first teardown

---

## Files Recently Modified

- `src/content/teardowns/*.md` - Teardown content files
- `public/images/*/` - Optimized teardown photos
- `astro.config.mjs` - Dev toolbar disabled
- `organize-images.sh` - Image processing automation
- `sync-to-obsidian.sh` - Vault integration

---

## Environment Info

- **Project location:** `/Users/aim/Documents/teardown-cafe/`
- **Framework:** Astro v5.14.5
- **Design system:** Material You 3 Expressive (dark mode)
- **Colors:** Periwinkle (#B8B3FF), teal accent (#00BCD4)
- **Typography:** Ubuntu font family
- **Last successful build:** Working, dev server tested
- **Last git commit:** Documentation updates

---

## Notes for Claude

**Tool usage:**
- Use **local filesystem** for all project files
- Use **Obsidian MCP** only for vault notes
- **Always verify `pwd`** before git operations

**Common tasks:**
- Adding teardown: See [[Teardown Cafe - Content Workflow]]
- Code changes: Check [[Teardown Cafe - Technical Setup]]
- Debugging: Reference [[Teardown Cafe - Troubleshooting]]

**Privacy critical:** EXIF stripping mandatory for all images

---

## Quick Links

- **Repository:** (GitHub URL when created)
- **Local dev:** `npm run dev` → http://localhost:4321
- **Documentation hub:** [[Teardown Cafe - Documentation Index]]

---

*This note serves as the entry point for all Teardown Cafe work. Claude navigates to related docs based on task type.*


### Completed ✅ (October 19, 2025 Session)
- [x] Vertical progress bar with descending scroll
- [x] SVG device icons (replacing emojis)
- [x] Focus Mode toggle (ADHD accessibility)
- [x] Progress bar UI refinements
- [x] Removed DifficultyMeter from homepage


## Recent Changes

- **Oct 19, 2025:** Vertical progress bar implementation
- **Oct 19, 2025:** SVG icons + Focus Mode toggle
- **Oct 19, 2025:** Progress bar UI refinements
- **Oct 19, 2025:** Removed DifficultyMeter from homepage
- **Oct 16, 2025:** Created comprehensive Obsidian documentation suite
- **Oct 15, 2025:** Added Raspberry Pi 5 NVMe teardown with 6 images
- **Oct 15, 2025:** Troubleshot Astro v5 compatibility issues
- **Oct 14, 2025:** Initial project setup with first teardown

## Files Recently Modified

- `src/components/VerticalProgress.astro` - New vertical progress bar
- `src/components/DeviceIcons.astro` - SVG icon components
- `src/components/FocusMode.astro` - ADHD accessibility toggle
- `src/pages/index.astro` - Homepage with SVG icons
- `src/pages/teardowns/[id].astro` - Teardown pages with vertical progress

## Last Commit

**Commit:** `4e27a05` - "feat: vertical progress bar (Concept 1)"


### October 19, 2025 - Evening Session
- [x] Added Moto G Stylus 2022 screen repair entry
- [x] Implemented HTML5 video support (self-hosted, privacy-first)
- [x] Updated content schema with optional video field  
- [x] Added Material You video styling to teardown pages
- [x] 4 repair images + 1 video, all EXIF stripped
- [x] Git commit: cb04030


### October 19, 2025 - Late Evening Session
- [x] Added caption to Moto G hero photo (Samsung Galaxy S6 reference)
- [x] Created MacBook Air 2015 13" entry
- [x] 3 MacBook Air images organized and EXIF stripped
- [x] Researched firmware update requirements (High Sierra 10.13+)
- [x] Official specifications documented (no hallucinations)
- [x] Git commit: e738cb7
- [x] Entry marked for future expansion


### October 19, 2025 - Content Corrections
- [x] Corrected Moto G hero image (battery → screen showing S6)
- [x] Relocated S6 caption to opening section
- [x] Reduced article length by removing redundant conclusion
- [x] Adjusted difficulty context (easy-medium spectrum)
- [x] Removed MacBook Air duplicate image
- [x] Git commit: 5809820
- [x] Article length optimized: ~25% shorter


### October 19, 2025 - Image Enhancement Session
- [x] HP EliteBook 840 G7: Added frankenstein AIO final product image
- [x] Created "The Final Product" conclusion section
- [x] MacBook Air 2015: Added NVMe adapter installation image
- [x] Created "SSD Upgrade Considerations" section
- [x] Documented 15% adapter speed penalty
- [x] Noted potential OEM performance advantage despite reduction
- [x] Both images EXIF sanitized
- [x] Git commit: 38a9d32
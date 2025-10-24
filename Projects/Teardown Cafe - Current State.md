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
---
tags: [teardown-cafe, project-status, current-state]
updated: 2025-10-20
---

# Teardown Cafe - Current State

**Last Updated:** October 20, 2025  
**Live Site:** https://teardown-cafe.vercel.app  
**Repository:** https://github.com/AIMDaAlien/teardown-cafe  
**Tech Stack:** Astro v5.14.5, Material You 3 Design System

## Recent Session Summary (Oct 20, 2025)

### What Got Built
1. **Related Teardowns Component** - Smart filtering by device type
2. **Progressive Image Loading** - Blur-up technique for better UX
3. **Device Type Pages** - `/device/[type]` routes with 8 categories
4. **Plausible Analytics** - Privacy-friendly tracking
5. **Theme Toggle** - Light/dark mode switcher
6. **3D Prints Gallery POCs** - Grid and timeline views (not yet populated)
7. **Obsidian Integration** - Automated tag matching system
8. **About Page Rewrite** - Solo hobbyist voice, privacy emphasis

### Current Teardown Entries (9 total)
1. Raspberry Pi 5 NVMe Build
2. ThinkPad T490s Under the Hood
3. HP EliteBook 840 G7 Frankenstein AIO
4. MacBook Air 2015 13-inch
5. Moto G Stylus 2022 Screen Repair
6. TrueNAS Enterprise SAS Build
7. Bambu Lab A1 Mini Setup (Aug 27, 2025)
8. Bambu Lab A1 Combo Upgrade (Sept 13, 2025)
9. MacBook Pro 2010 OS Upgrades (Lion → Sequoia)

### Pending Implementation (Specs Created)
- **Image Optimization:** Vercel image caching via `@astrojs/vercel/image`
- **Styling Fixes:** 
  - Circuit accent hover (darker in light mode)
  - Lavender background (#F5F0FF) instead of white
- **Quick Looks Page:** Single-photo items (Tozo charger, iPod Touch, Realme watch)
- **Prints Gallery:** Populate with actual print data

## Project Structure

```
teardown-cafe/
├── .cursor-specs/          # Specs for Cursor implementation
│   ├── portfolio-obsidian-integration.md
│   ├── quick-looks-spec.md
│   ├── deployment-guide.md
│   ├── image-optimization-styling-fixes.md
│   └── hover-glow-lavender-fixes.md
├── src/
│   ├── components/
│   │   ├── Analytics.astro (Plausible)
│   │   ├── ProgressiveImage.astro (blur-up loading)
│   │   ├── RelatedTeardowns.astro (smart filtering)
│   │   ├── RelatedObsidianNotes.astro (tag matching)
│   │   ├── TagCloud.astro
│   │   ├── ThemeToggle.astro
│   │   └── CircuitAccents.astro (decorative elements)
│   ├── data/
│   │   ├── teardowns/*.md (9 entries)
│   │   └── obsidian-overrides.json (manual tag connections)
│   ├── pages/
│   │   ├── index.astro (homepage with device type grid)
│   │   ├── about.astro (updated with personal voice)
│   │   ├── device/[type].astro (8 device categories)
│   │   ├── prints/index.astro (gallery POC)
│   │   └── prints/timeline.astro (timeline POC)
│   └── styles/global.css (Material You 3 tokens)
├── scripts/
│   ├── build-obsidian-links.js (tag matching automation)
│   └── organize-images.sh
└── public/
    ├── images/ (optimized teardown photos)
    └── data/
        ├── obsidian-relationships.json (auto-generated)
        └── tag-stats.json (auto-generated)
```

## Workflow Established

### Claude → Cursor Division
- **Claude:** Architecture, specs, content creation, image optimization, strategy
- **Cursor:** Implementation from specs, component building, code execution

### Deployment
- **Platform:** Vercel (auto-deploys on `git push`)
- **Critical:** Always push to GitHub before expecting deployment updates
- **Vercel MCP:** Connected for Claude to trigger deploys and check status

### Image Optimization
- Original images: 10-15MB each
- Optimized: 400KB-1.4MB (95% reduction)
- Command: `sips -Z 1920 -s format jpeg -s formatOptions 80`

## Tag System

Each teardown has 8-12 tags for automated Obsidian matching:
- **Device types:** laptop-repair, 3d-printing, nas-storage, smartphone-repair
- **Skills:** thermal-management, cable-management, opencore, zfs
- **Difficulty:** beginner-friendly, advanced-repair
- **Tech:** bambu-lab, raspberry-pi, truenas

Build script scans Obsidian vault, matches tags, generates relationships.

## Known Issues & Next Steps

### Ready for Cursor Implementation
1. Vercel image optimization (install `@astrojs/vercel`)
2. Circuit accent hover fixes (darker glow in light mode)
3. Lavender background for light theme
4. Quick Looks page for single-photo items
5. Populate prints gallery with actual data

### Future Enhancements (Not Spec'd)
- Search functionality
- RSS feed
- View counter
- Open Graph images for social sharing
- Estimated read time on cards

## Git Status

**Latest Commit:** 078f10d (About page rewrite)  
**Branch:** main  
**Remote:** GitHub sync'd, Vercel deployed

## Key Learnings This Session

1. **Vercel deploys from GitHub, not local** - Always push first
2. **Cursor has smaller context** - Break tasks into smaller chunks, reference specific files
3. **Tag automation works** - Zero manual maintenance after setup
4. **Obsidian MCP** - Can create/update notes directly
5. **Privacy matters** - EXIF stripping, no tracking analytics

## Related Notes
- [[Teardown Cafe - Deployment Guide]]
- [[Claude-Cursor Workflow]]
- [[Tag System & Portfolio Integration]]
- [[Projects/Teardown Cafe]]


### October 23, 2025 - Keyboard Mod Entry
- [x] Added Epomaker Split 65% Sound Mod entry
- [x] Poron foam + AKKO V3 Fairy silent switches documentation
- [x] 5 images + 1 assembly video
- [x] Medium difficulty (foam cutting, border switch reassembly)
- [x] Home office sound dampening project
- **NOTE:** EXIF stripping needed for images (run organize-images.sh)

**Updated count:** 10 total teardown entries


### October 23, 2025 - Domain & GMK67 Entry
- [x] Added GMK67 Custom Mechanical Keyboard Build entry
- [x] AKKO Lavender + KTT Baby White switches documented
- [x] 2 images + 2 videos (assembly + sound test)
- [x] Easy difficulty (first-time build)
- [x] **Domain purchased:** teardown.cafe via Hostinger ($30/yr)
- [x] DNS A record configured (216.198.79.1)
- [x] Vercel deployment protection disabled (site now public)
- [x] Site live at https://teardown.cafe
- [x] Created deployment and content workflow docs

**Updated count:** 11 total teardown entries

**Site Status:** Live and publicly accessible
**Production URL:** https://teardown.cafe
**Vercel URL:** https://teardown-cafe.vercel.app (redirects to custom domain)


### October 24, 2025 - Portfolio Presentation Updates
- [x] Updated GitHub README with professional description, tech stack, workflow scripts
- [x] Created portfolio card HTML with SVG icons (Material You design)
- [x] Updated resume with TECHNICAL PROJECTS section featuring Teardown Cafe
- [x] Replaced all emojis with custom SVG icons (coffee+wrench logo, device icons)
- [x] Reduced device card size by 30% (280px → 196px)
- [x] Added hover effects on SVG icons (scale + glow)
- [x] Git commit: 42d6b09

**Portfolio Ready:** Resume bullets drafted, GitHub README updated, portfolio card HTML created

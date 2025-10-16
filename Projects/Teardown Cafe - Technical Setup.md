# Teardown Cafe - Technical Setup

## Initial Project Scaffolding

### Framework Selection: Astro.js
**Why Astro:**
- Static site generation (fast, secure)
- Built-in content collections for markdown
- MDX support for interactive components
- Excellent image optimization
- Minimal JavaScript by default

### Project Initialization
```bash
# Created in ~/Documents/teardown-cafe/
npm create astro@latest teardown-cafe
cd teardown-cafe
npm install
```

## File Structure
```
teardown-cafe/
├── src/
│   ├── content/
│   │   ├── teardowns/           # Markdown files for each teardown
│   │   │   ├── monitor-oct-2025.md
│   │   │   └── raspberry-pi-5-nvme-build.md
│   │   └── config.ts            # Content collection schema
│   ├── layouts/
│   │   └── BaseLayout.astro     # Site-wide wrapper
│   ├── pages/
│   │   ├── index.astro          # Homepage grid
│   │   ├── about.astro          # About page
│   │   └── teardowns/[slug].astro  # Dynamic teardown pages
│   └── styles/
│       └── global.css           # Material You 3 design tokens
├── public/
│   └── images/                  # Optimized teardown photos
│       ├── monitor-oct-2025/
│       └── raspberry-pi-5-nvme/
├── astro.config.mjs             # Astro configuration
├── package.json
├── README.md
├── WORKFLOW.md                  # Content addition guide
├── organize-images.sh           # Image processing script
└── sync-to-obsidian.sh          # Vault sync script
```

## Astro Configuration

### Key Config Settings
```javascript
// astro.config.mjs
export default defineConfig({
  site: 'https://teardown.cafe',
  integrations: [
    mdx(),
    sitemap()
  ],
  devToolbar: {
    enabled: false  // Disabled to avoid UI clutter
  }
});
```

## Content Collections Schema

### Teardown Schema Definition
```typescript
// src/content/config.ts
const teardowns = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string(),
    device: z.enum([
      'monitor', 'laptop', 'smartphone', 
      'raspberry-pi', 'nas', 'mechanical-keyboard', 
      'other'
    ]),
    difficulty: z.enum(['easy', 'medium', 'hard']),
    obsidianNotes: z.array(z.object({
      title: z.string(),
      path: z.string()
    })).optional()
  })
});
```

## Major Compatibility Issue: Astro Version Updates

### The Problem
Project initially designed with Astro knowledge from January 2025, but user running **Astro v5.14.5** (October 2025 release).

### Breaking Changes Discovered
1. **Content Collections API** changed between v4.x and v5.x
2. **Image optimization** syntax evolved
3. **Dev toolbar** introduced (initially causing confusion)
4. **MDX integration** requirements updated

### Resolution Strategy
1. Research current Astro v5.x documentation
2. Update all component imports to v5 syntax
3. Verify content collection configuration
4. Test image optimization pipeline
5. Disable dev toolbar for cleaner interface

## Image Processing Pipeline

### Image Organization Script
**File:** `organize-images.sh`

**Purpose:** Automatically rename and organize images from camera/phone uploads

**Process:**
```bash
# Source: ~/Downloads/IMG*.jpg
# Destination: public/images/[project-slug]/
# Naming: 01-descriptive-name.jpg, 02-next-step.jpg, etc.
```

**Features:**
- Sequential numbering
- Descriptive filenames
- Automatic directory creation
- Verification output

### EXIF Data Stripping
**Critical for privacy:**
```bash
brew install exiftool
exiftool -all= *.jpg
rm *_original
```

Removes:
- GPS coordinates
- Camera model
- Timestamps
- Any identifying metadata

## Git Workflow

### Repository Setup
```bash
cd ~/Documents/teardown-cafe
git init
git add -A
git commit -m "Initial commit: Project scaffold"
```

### Commit Strategy
Structured commits documenting each teardown addition:
```bash
git commit -m "Add teardown: [Device Name]

- [Number] process images
- [Key features/findings]
- Linked to [related notes]
- [Any special considerations]"
```

## Obsidian Integration

### Bidirectional Linking
**Purpose:** Connect website teardowns with personal knowledge base

**Implementation:**
- Teardown markdown includes `obsidianNotes` frontmatter
- Links formatted as: `obsidian://open?vault=YourVault&file=Path/To/Note`
- Auto-generated index in Obsidian vault

### Sync Script
**File:** `sync-to-obsidian.sh`

**Function:**
1. Scans all teardown files
2. Extracts metadata
3. Generates statistics
4. Updates `Projects/Teardowns Index.md` in vault
5. Creates backlinks to website

## Build Process

### Development Server
```bash
npm run dev
# Launches at http://localhost:4321
```

### Production Build
```bash
npm run build
# Output: dist/ directory
# Static files ready for deployment
```

### Build Verification
```
✓ 0 errors
✓ 0 warnings
✓ Pages generated: /, /about/, /teardowns/[slug]/
✓ Sitemap generated
```

## Dependencies
```json
{
  "dependencies": {
    "astro": "^5.14.5",
    "@astrojs/mdx": "^latest",
    "@astrojs/sitemap": "^latest",
    "zod": "^3.22.4"
  }
}
```

## Performance Considerations
- **Static generation:** Pre-rendered at build time
- **Image optimization:** Automatic WebP conversion
- **Minimal JavaScript:** Only what's needed for interactions
- **CSS purging:** Unused styles removed in production

## Security Measures
- Static site (no server-side vulnerabilities)
- EXIF stripped (no metadata leaks)
- No analytics yet (privacy-first approach)
- Sanitized file paths (no directory traversal risks)

## Known Issues & Workarounds

### Issue: Bash Array Syntax
**Problem:** `organize-images.sh` used bash-specific array syntax incompatible with macOS zsh

**Workaround:** Manual cp commands or revised script with POSIX-compliant syntax

### Issue: Docker Commits
**Problem:** Accidentally committed changes in Docker environment instead of host filesystem

**Resolution:** Always verify working directory before git operations

## Related Notes
- [[Teardown Cafe - Project Overview]]
- [[Teardown Cafe - Design System]]
- [[Teardown Cafe - Troubleshooting]]

---
*Created: October 16, 2025*
*Last Updated: October 16, 2025*

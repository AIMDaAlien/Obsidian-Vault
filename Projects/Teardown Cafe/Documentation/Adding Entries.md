

## Adding New Teardown Entries

### Quick Checklist
1. Assets in `/Downloads/[project-name]/`
2. Copy to `/public/images/[slug]/`
3. Strip EXIF: `exiftool -all= *.jpg *.mp4`
4. Create markdown in `/src/data/teardowns/[slug].md`
5. Verify device type matches schema
6. Commit and push

### Device Types (Schema Validation)
Valid values in `content.config.ts`:
- monitor
- laptop
- smartphone
- raspberry-pi
- nas
- **mechanical-keyboard** (not "keyboard")
- 3d-printer
- other

**Common mistake:** Using `keyboard` instead of `mechanical-keyboard` causes build errors.

### Frontmatter Template
```markdown
---
title: "Project Title"
description: "Brief description for SEO"
pubDate: YYYY-MM-DD
device: mechanical-keyboard
difficulty: easy | medium | hard
heroImage: /images/slug/hero.jpg
video: /images/slug/video.mp4  # optional
---
```

### Video Embedding
```html
<video controls src="/images/slug/video.mp4" poster="/images/slug/hero.jpg">
  Your browser doesn't support embedded videos. 
  <a href="/images/slug/video.mp4">Download video</a>.
</video>
```

### Build Error Troubleshooting
**Error:** `invalid-content-entry-data-error`
- Check device type matches schema exactly
- Verify all required fields present
- Check date format (YYYY-MM-DD)

### EXIF Stripping (Privacy)
```bash
cd public/images/[slug]
exiftool -all= *.jpg *.mp4
rm *_original
```

---
*Created: October 23, 2025*

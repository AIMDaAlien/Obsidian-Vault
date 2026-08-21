---
tags: [portfolio, web-development, project-index, github-pages, troubleshooting, branding, website-rebuild, portfolio-piece, checklist]
created: 2025-10-01
updated: 2026-08-01
published_to_garden: true
visibility: public
---

# Portfolio Website Development — Project Overview

> **Tags**: #portfolio #web-development #project-index #github-pages
> **Status**: 🚀 Active Development

## Project Structure

```
Website Development/
├── Features/           # Implemented website features
├── Deployment/         # Hosting & deployment docs
└── Content/           # Content drafts & planning
```

## Quick Navigation

### 🎨 Features
- [[Privacy Filter - Matrix Decode]] - Contact info privacy protection with animation

### 🚀 Deployment
- [[Github Pages Setup]] - Hosting configuration & workflow
- [[Git Push Conflict Troubleshooting]] - Common deployment issues & solutions

### 📍 Current State
- [[Project - Current State]] - What is live, why it was built this way, and the ordered next moves

### ✍️ Content
- [[About Me Draft]] - Bio section content planning

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Hosting**: GitHub Pages
- **Version Control**: Git/GitHub
- **Design**: Dark Material 3 Expressive, pastel periwinkle theme
- **Content source**: Public Obsidian vault manifest with GitHub fallbacks
- **Operations**: Sanitized five-minute Unraid health snapshot

## Development Workflow

1. **Local Development** → Test features
2. **Git Commit** → Document changes
3. **Push to GitHub** → Auto-deployment via Pages
4. **Verify Live** → Hard refresh + test

## Key Features Implemented

| Feature | Status | Tech | Notes |
|---------|--------|------|-------|
| Matrix-Decode Privacy Filter | ✅ Live | JS + CSS | [[Privacy Filter - Matrix Decode]] |
| Periwinkle Theme | ✅ Live | CSS | Brand colors |
| Responsive Layout | ✅ Live | CSS | Mobile-first |
| GitHub Pages Deploy | ✅ Configured | Git | [[Github Pages Setup]] |
| Custom Domain + HTTPS | ✅ Live | DNS + Pages | `portfolio.penthouse.blog` |
| Knowledge Garden | ✅ Live | JS + generated manifest | Five-minute refresh |
| Live Unraid Telemetry | ✅ Live | Shell + JSON + JS | Sanitized public payload |
| Activity Feed | ✅ Live | JS | Precise times and update batches |

## Common Tasks

### Add New Feature
1. Create feature documentation in `Features/`
2. Implement code locally without adding a framework or build dependency
3. Test thoroughly
4. Commit: `git commit -m "feat: description"`
5. Push and verify deployment

### Update Content
1. Edit relevant content in `Content/`
2. Update live HTML files
3. Test changes
4. Deploy via standard workflow

### Troubleshoot Deployment
See [[Git Push Conflict Troubleshooting]] for:
- Push conflicts
- Non-fast-forward errors
- Cache issues

## Related Notes

### Development Tools
See [[Development Tools]] for:
- Git command reference
- VS Code setup
- Terminal enhancements

### Projects
Related homelab/infrastructure projects:
- [[Pi-hole Setup Guide - Complete Journey]]
- [[WireGuard VPN Setup]]
- [[GrapheneOS Migration Guide - Complete Documentation]]

## Future Enhancements

**In Planning**:
- [ ] Blog integration
- [ ] Project gallery
- [ ] Interactive demos
- [ ] Contact form (external service)
- [x] Custom domain

**Feature Ideas**:
- [x] Dark interface
- [x] Terminal-style interactions
- [ ] Filesystem-style terminal commands (`ls`, `cd`, `pwd`, `head`, `find`, `grep`, `tree`)
- [ ] Final AIM.EXE favicon
- [ ] Animated transitions
- [ ] Performance optimizations

## Development Philosophy

- **Privacy-first** - Protect user data
- **Performance** - Fast, optimized code
- **Accessibility** - Usable for everyone
- **Maintainability** - Clean, documented code
- **Progressive Enhancement** - Works everywhere, enhanced where possible

## Resources

- **Repository**: `github.com/AIMDaAlien/First-Portfolio-Iteration`
- **Live Site**: `portfolio.penthouse.blog`
- **Documentation**: This vault!

---

*Created: October 2025*
*Last Updated: August 2026*

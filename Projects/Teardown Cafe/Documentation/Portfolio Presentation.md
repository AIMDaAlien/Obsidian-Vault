
---
tags: [teardown-cafe, portfolio, career]
created: 2025-10-23
---

# Teardown Cafe - Portfolio Presentation

## For Recruiters & Hiring Managers

**Yes, this is showcase-worthy.** Here's why:

### Project Highlights (What Recruiters Care About)
1. **Full-stack implementation** - Astro SSG, custom content API, Material Design System
2. **Production deployment** - Live site with custom domain, DNS configuration
3. **Privacy-first approach** - EXIF stripping, no tracking analytics
4. **Content management** - Schema validation, frontmatter architecture
5. **Design system** - Material You 3 with custom periwinkle/lavender palette
6. **Real-world problem solving** - Built to share hardware knowledge

### Resume Bullet Points (Pick 2-3)
- Built full-stack hardware documentation site using Astro v5 and Material You 3 design system, deployed to production at teardown.cafe
- Implemented privacy-first content pipeline with automated EXIF stripping and Vercel CDN deployment
- Designed responsive UI with custom Material Design System, supporting 11 device teardown categories with video/image galleries
- Configured production infrastructure including DNS management, SSL certificates, and automated deployment pipeline

### GitHub README Improvements

Add to teardown-cafe README.md:

```markdown
# Teardown Cafe

**Live Site:** [teardown.cafe](https://teardown.cafe)

Hardware teardown documentation and repair guides with privacy-first design.

## Tech Stack
- **Framework:** Astro v5.14.5 (Content Layer API)
- **Design:** Material You 3 Expressive (Custom periwinkle palette)
- **Hosting:** Vercel with custom domain
- **Privacy:** Automated EXIF stripping, self-hosted media

## Features
- 11 device teardown entries with HD images and video
- Responsive design with dark/light mode
- Device type categorization (keyboards, laptops, 3D printers, etc.)
- Privacy-first: No analytics, no tracking
- Automated content validation via Astro Content Collections

## Architecture Decisions
- Chose Astro for zero-JS islands and fast static generation
- Material Design System for accessibility and cohesive visual language
- Self-hosted video to avoid third-party embeds
- Content-first approach with markdown + frontmatter

## Local Development
\`\`\`bash
npm install
npm run dev  # http://localhost:4321
\`\`\`

## Deployment
Automated via Vercel on push to main branch.
```

### Portfolio Website Integration

**Projects section - Add card:**

```html
<div class="project-card">
  <h3>Teardown Cafe</h3>
  <p class="tech-stack">Astro • Material Design • Vercel</p>
  <p>Hardware repair documentation site with privacy-first architecture. 
     11 device teardowns, custom CMS, responsive design.</p>
  <div class="project-links">
    <a href="https://teardown.cafe">Live Site</a>
    <a href="https://github.com/AIMDaAlien/teardown-cafe">GitHub</a>
  </div>
</div>
```

**Emphasize:**
- Production deployment (not just localhost)
- Custom domain setup (shows infrastructure knowledge)
- Design system implementation (attention to UX)
- Content architecture (structured thinking)

### LinkedIn Post Template

```
🔧 Launched Teardown Cafe - a hardware documentation site built with Astro v5

What I built:
• 11 device teardowns with HD images & videos
• Material You 3 design system with dark/light mode
• Privacy-first: automated EXIF stripping, no tracking
• Custom domain with DNS configuration

Tech: Astro, Material Design, Vercel, Content Collections API

Check it out: teardown.cafe

#webdev #astro #ux
```

### Interview Talking Points

**When asked "Tell me about a recent project":**

> "I built Teardown Cafe - a hardware documentation site using Astro and Material Design. The challenge was balancing technical content with good UX, while maintaining privacy. I implemented automated EXIF stripping for all images, custom content validation schemas, and deployed to production with a custom domain. It's live at teardown.cafe with 11 device teardowns."

**Technical depth if asked:**
- Content Layer API for markdown processing
- SVG icon system (no emoji dependencies)
- Progressive image loading with blur-up
- Vercel deployment with DNS configuration

### What Makes This Stand Out

1. **It's live** - Not a tutorial follow-along, actual production site
2. **Real content** - 11 original entries with your own photography
3. **Design thinking** - Custom Material Design implementation
4. **Privacy-first** - Shows awareness of web ethics
5. **Domain ownership** - Demonstrates infrastructure knowledge

### Portfolio Site URL

Include prominently:
- Hero section: "Check out my latest project: teardown.cafe"
- Projects grid: Feature as top/recent project
- GitHub pinned repo: Pin teardown-cafe repository

---

## Action Items

- [ ] Update teardown-cafe README.md with tech stack and features
- [ ] Add Teardown Cafe card to portfolio site
- [ ] Pin teardown-cafe repo on GitHub profile
- [ ] LinkedIn post announcing launch
- [ ] Add to resume projects section (2-3 bullet points)
- [ ] Prepare 60-second demo walkthrough for interviews

---
*Created: October 23, 2025*
*Site Status: Live at teardown.cafe*

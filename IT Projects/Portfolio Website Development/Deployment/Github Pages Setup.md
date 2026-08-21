---
tags: [github-pages, deployment, hosting, web-development, portfolio, troubleshooting, website-rebuild, security, portfolio-piece, checklist]
created: 2025-10-01
updated: 2026-08-01
published_to_garden: true
visibility: public
---

# GitHub Pages Setup & Deployment

> **Tags**: #github-pages #deployment #hosting #web-development #portfolio
> **Related**: [[Git Push Conflict Troubleshooting]] | [[Privacy Filter - Matrix Decode]] | [[Development Tools]]
> **Status**: ✅ Configured & Active

## Overview

GitHub Pages provides free static website hosting directly from your repository. Simple, fast, and perfect for portfolio sites.

## Why GitHub Pages?

- **Free hosting** with custom domain support
- **Automatic deployment** from Git commits
- **HTTPS by default** for security
- **CDN-backed** for fast global delivery
- **No server management** required
- **Version controlled** - every change is tracked

## Initial Setup

### 1. Repository Configuration

1. Go to the repository on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**

The repository URL remains available as the default Pages address:

`https://aimdaalien.github.io/First-Portfolio-Iteration/`

### 2. Custom Domain (Active)

The portfolio uses `portfolio.penthouse.blog`.

1. Add a `CNAME` file to repo root with your domain:
   ```
   portfolio.penthouse.blog
   ```

2. Configure DNS with your domain provider:
   ```
   Type: CNAME
   Name: portfolio
   Value: AIMDaAlien.github.io
   ```

3. In GitHub Settings → Pages:
   - Set the custom domain to `portfolio.penthouse.blog`
   - Enable **Enforce HTTPS** after GitHub provisions the certificate

The Cloudflare record is intentionally **DNS only**. GitHub Pages terminates HTTPS and serves the static site directly. During setup, the repository stayed on its normal Pages URL until the CNAME had propagated; this avoided leaving the site attached to a hostname that did not resolve yet.

## Deployment Workflow

### Standard Push Process

```bash
# Make your changes locally
# Edit files in your code editor

# Stage only the files intended for this deployment
git add index.html style.css script.js

# Commit with descriptive message
git commit -m "feat: Add new feature description"

# Push to GitHub
git push origin main

# GitHub Pages deploys automatically after the push
```

### Verification Checklist

After pushing:

1. **Check commit appeared**:
   ```bash
   git log origin/main --oneline -1
   ```

2. **Wait for deployment** (usually 1-3 minutes)
   - GitHub Actions will build/deploy automatically
   - Check repo → Actions tab for status

3. **Hard refresh your site**:
   - Mac: `Cmd+Shift+R`
   - Windows: `Ctrl+Shift+R`
   - This clears browser cache

4. **Verify the public endpoints**:
   - `https://portfolio.penthouse.blog/` loads successfully
   - GitHub Pages reports the expected custom domain and HTTPS enforcement
   - Latest Transmissions loads from the vault manifest
   - The Knowledge Garden opens notes and renders its tree
   - Live Unraid telemetry updates without exposing private infrastructure details

## Common Issues & Solutions

### Changes Not Showing

**Problem**: Pushed changes but site looks the same

**Solutions**:
1. **Check you edited the right file**
   - Verify no backup files (index.html.bak)
   - Make sure you're editing in repo root

2. **Wait for deployment to complete**
   - Check Actions tab for green checkmark
   - Can take 1-5 minutes

3. **Clear browser cache aggressively**:
   ```bash
   # Mac Safari: Cmd+Option+E then Cmd+R
   # Mac Chrome/Brave: Cmd+Shift+R
   # Windows: Ctrl+Shift+R
   ```

4. **Check browser dev console for errors**:
   - F12 → Console tab
   - Look for 404s or JavaScript errors

### Push Rejected

See [[Git Push Conflict Troubleshooting]] for detailed solutions to:
- Non-fast-forward errors
- Merge conflicts
- Authentication issues

### File Not Found (404)

**Problem**: Page loads but resources (CSS/JS) missing

**Solution**: Check file paths are relative:
```html
<!-- ✅ Good - relative path -->
<link rel="stylesheet" href="style.css">
<script src="script.js"></script>

<!-- ❌ Bad - absolute path won't work on GitHub Pages -->
<link rel="stylesheet" href="/style.css">
<script src="/script.js"></script>
```

## Project Structure

```
repo-root/
├── index.html           # Main page (required)
├── style.css           # Stylesheets
├── script.js           # JavaScript
├── garden-terminal.html # Knowledge Garden terminal page
├── garden-terminal.js  # Garden commands, manifest, and note loading
├── garden-graph.js     # Knowledge graph visualization
├── m3e-tokens.css      # Shared M3 Expressive design tokens
├── terminal.js         # Contact privacy behavior
├── terminal-privacy.css
├── unraid-metrics-publisher.sh # Sanitized telemetry publisher source
└── CNAME               # portfolio.penthouse.blog
```

## Best Practices

### Before Each Deploy

1. **Test locally first**:
   ```bash
   # Open index.html in browser
   open index.html  # Mac
   start index.html # Windows
   ```

2. **Review changes and stage narrowly**:
   ```bash
git status
git diff
git add path/to/intended-file
   ```

3. **Write clear commit message**:
   ```bash
   git commit -m "feat: Add privacy filter to contact section"
   # NOT: "fixed stuff" or "changes"
   ```

### File Management

- **Keep root clean** - organize assets in folders
- **Use lowercase names** - avoid `MyFile.html` (case-sensitive on servers)
- **No spaces in filenames** - use hyphens: `my-file.html`
- **Optimize images** - compress before uploading
- **Keep the no-build workflow** - source files are the deployed files

## Monitoring & Analytics

### GitHub Insights

Repository → Insights → Traffic:
- Views and unique visitors
- Referring sites
- Popular content

### Current monitoring boundary

The portfolio does not install visitor analytics. GitHub's repository traffic view is enough for occasional high-level checks. The Unraid gauges are service-health telemetry fetched by the visitor's browser; they do not track the visitor.

If analytics are ever added, the decision should start with a specific question that needs answering and should prefer a privacy-preserving option.

## Feature Implementation

When adding new features like [[Privacy Filter - Matrix Decode]]:

1. **Develop locally**
2. **Test in multiple browsers**
3. **Commit with feature description**
4. **Push to GitHub**
5. **Verify deployment**
6. **Test live site thoroughly**

## Security Considerations

- ✅ HTTPS enforced for `portfolio.penthouse.blog`
- ✅ Static content only (no server-side code)
- ⚠️ All code is public (repository visibility)
- ⚠️ Don't commit API keys or secrets
- ⚠️ Never expose raw infrastructure data; publish a separate sanitized payload
- ⚠️ Client-side redaction is presentation, not a security boundary

## Alternatives Considered

| Platform | Pros | Cons | Decision |
|----------|------|------|----------|
| **GitHub Pages** | Free, simple, Git-integrated | Static only | ✅ **Selected** |
| Netlify | More features, forms | Overkill for simple site | Maybe later |
| Vercel | Great for React/Next | Not needed yet | Maybe later |
| Replit | Quick prototyping | Less permanent | Archive only |
| Custom server | Full control | Maintenance overhead | Not worth it |

## Future Enhancements

Possible upgrades as site grows:
- [x] Custom domain configured
- [ ] CDN optimization
- [ ] Analytics integration
- [ ] Contact form (via external service)
- [ ] Blog integration (Jekyll/Hugo)
- [ ] PWA features

## Quick Reference

```bash
# Standard deployment
git add .
git commit -m "type: description"
git push origin main

# Check deployment
git log origin/main --oneline -1

# Force cache refresh
Cmd+Shift+R (Mac) / Ctrl+Shift+R (Windows)

# Troubleshooting
git status
git log --oneline -5
git remote -v
```

---

*Created: October 2025*

*Updated: August 2026*

*Repository: [AIMDaAlien/First-Portfolio-Iteration](https://github.com/AIMDaAlien/First-Portfolio-Iteration)*

*Deployment URL: [portfolio.penthouse.blog](https://portfolio.penthouse.blog/)*

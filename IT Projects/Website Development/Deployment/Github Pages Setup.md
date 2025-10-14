# Github Pages Setup & Deployment

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

1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**

Your site will be available at: `https://username.github.io/repo-name/`

### 2. Custom Domain (Optional)

If you have your own domain:

1. Add a `CNAME` file to repo root with your domain:
   ```
   yourdomain.com
   ```

2. Configure DNS with your domain provider:
   ```
   Type: CNAME
   Name: www (or @)
   Value: username.github.io
   ```

3. In GitHub Settings → Pages:
   - Enter custom domain
   - Check "Enforce HTTPS"

## Deployment Workflow

### Standard Push Process

```bash
# Make your changes locally
# Edit files in your code editor

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add new feature description"

# Push to GitHub
git push origin main

# GitHub Pages auto-deploys in 1-3 minutes
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
├── terminal.js         # Additional scripts
├── terminal-privacy.css
├── images/             # Assets folder
│   └── photo.jpg
├── CNAME              # Custom domain (optional)
└── README.md          # Documentation
```

## Best Practices

### Before Each Deploy

1. **Test locally first**:
   ```bash
   # Open index.html in browser
   open index.html  # Mac
   start index.html # Windows
   ```

2. **Review changes**:
   ```bash
   git status
   git diff
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
- **Minify CSS/JS** - for production (optional)

## Monitoring & Analytics

### GitHub Insights

Repository → Insights → Traffic:
- Views and unique visitors
- Referring sites
- Popular content

### Adding Analytics (Optional)

Google Analytics or similar can be added to `index.html`:

```html
<!-- Before </head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## Feature Implementation

When adding new features like [[Privacy Filter - Matrix Decode]]:

1. **Develop locally**
2. **Test in multiple browsers**
3. **Commit with feature description**
4. **Push to GitHub**
5. **Verify deployment**
6. **Test live site thoroughly**

## Security Considerations

- ✅ HTTPS enforced by default
- ✅ Static content only (no server-side code)
- ⚠️ All code is public (repository visibility)
- ⚠️ Don't commit API keys or secrets
- ⚠️ Use client-side privacy filters for sensitive data

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
- [ ] Custom domain purchase
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
*Deployment URL*: `https://github.com/AIMDaAlien/First-Portfolio-Iteration`
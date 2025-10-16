# Teardown Cafe - Documentation Index

## 📋 Quick Navigation

This documentation set covers the complete development journey of **teardown.cafe**, a device teardown showcase website built with Astro.js and Material You 3 design.

### Core Documentation

1. **[[Teardown Cafe - Project Overview]]**
   - Vision and philosophy
   - Technical stack overview
   - Device types covered
   - Privacy considerations

2. **[[Teardown Cafe - Technical Setup]]**
   - Framework configuration (Astro v5.14.5)
   - File structure
   - Content collections schema
   - Git workflow
   - Obsidian integration
   - Version compatibility issues

3. **[[Teardown Cafe - Design System]]**
   - Material You 3 implementation
   - Color palette (periwinkle/lavender)
   - Typography (Ubuntu fonts)
   - Component patterns
   - Accessibility standards
   - Dark mode rationale

4. **[[Teardown Cafe - Content Workflow]]**
   - Photo capture best practices
   - Image organization automation
   - EXIF data stripping (privacy)
   - Markdown content creation
   - Git commit process
   - Obsidian sync procedure

5. **[[Teardown Cafe - Troubleshooting]]**
   - Astro version compatibility gap
   - Bash/zsh script issues
   - Docker environment mistakes
   - Cache management
   - Privacy implementation
   - Lessons learned

---

## 🚀 Quick Start Guide

### For Adding New Teardowns
```bash
# 1. Organize images
cd ~/Documents/teardown-cafe
./organize-images.sh

# 2. Create markdown file
# Use template from Content Workflow note

# 3. Strip EXIF data
cd public/images/[project-slug]
exiftool -all= *.jpg && rm *_original

# 4. Verify locally
npm run dev  # http://localhost:4321

# 5. Commit
git add -A
git commit -m "Add teardown: [Device]"

# 6. Sync to Obsidian
./sync-to-obsidian.sh
```

### For Technical Issues
1. Check [[Teardown Cafe - Troubleshooting]]
2. Verify Astro version matches docs
3. Clear caches (browser + framework)
4. Hard refresh (Cmd + Shift + R)

---

## 📊 Project Status

### Completed ✅
- Project scaffolding and initial setup
- Material You 3 dark theme implementation
- Content collection schema
- First teardown (Monitor, Oct 2025)
- Second teardown (Raspberry Pi 5 NVMe)
- Image organization automation
- EXIF stripping workflow
- Obsidian bidirectional linking
- Git repository initialization
- Comprehensive documentation

### In Progress 🔄
- Additional teardown content
- Script POSIX compliance improvements
- Image optimization pipeline

### Planned 📋
- RSS feed implementation
- Deployment (Vercel/Netlify)
- Domain purchase (teardown.cafe)
- Privacy-friendly analytics (optional)
- Additional device teardowns

---

## 🎯 Key Achievements

### Technical
- **Framework:** Successfully navigated Astro v4 → v5 migration
- **Design:** Full Material You 3 implementation with custom color tokens
- **Privacy:** Systematic EXIF stripping automated
- **Integration:** Seamless Obsidian vault linking

### Process
- **Workflow:** Streamlined content addition process
- **Documentation:** Comprehensive knowledge capture
- **Version Control:** Clean git history with descriptive commits
- **Troubleshooting:** Systematic problem-solving methodology

---

## 🔧 Critical File Locations

### Project Files
```
/Users/aim/Documents/teardown-cafe/
├── src/content/teardowns/*.md      # Teardown content
├── public/images/                  # Optimized photos
├── organize-images.sh              # Image automation
├── sync-to-obsidian.sh             # Vault sync
├── WORKFLOW.md                     # Process guide
└── README.md                       # Project overview
```

### Obsidian Notes
```
Projects/
├── Teardown Cafe - Project Overview.md
├── Teardown Cafe - Technical Setup.md
├── Teardown Cafe - Design System.md
├── Teardown Cafe - Content Workflow.md
├── Teardown Cafe - Troubleshooting.md
└── Teardown Cafe - Documentation Index.md  # This file
```

---

## 📚 Learning Resources Referenced

### Astro.js
- [Astro Documentation](https://docs.astro.build)
- Content Collections guide
- Image optimization
- Deployment guides

### Material You 3
- Google Material Design 3 guidelines
- Expressive theme documentation
- Color system principles
- Motion design patterns

### Privacy Tools
- exiftool documentation
- EXIF metadata standards
- Privacy-preserving image processing

---

## 🎨 Design Decisions

### Color Choices
- **Primary:** Periwinkle (#B8B3FF) - User preference
- **Background:** Deep purple (#14121F) - Sophisticated tech aesthetic
- **Accent:** Teal (#00BCD4) - From actual repair mat in photos

### Typography
- **Ubuntu font family** - Open source, excellent readability
- **Material You 3 type scale** - Consistent hierarchy

### Photography
- **Dark backgrounds** - Makes colorful components pop
- **Teal repair mat** - Consistent, professional look
- **Overhead + angle shots** - Complete component visibility

---

## 📈 Future Enhancements

### Priority 1 (Essential)
- [ ] Fix organize-images.sh POSIX compliance
- [ ] Deploy to production (Vercel)
- [ ] Add 3-5 more teardowns

### Priority 2 (Important)
- [ ] Implement RSS feed
- [ ] Purchase and configure domain
- [ ] Image optimization automation

### Priority 3 (Nice-to-Have)
- [ ] Privacy-friendly analytics
- [ ] Search functionality
- [ ] Category filtering
- [ ] Image galleries (lightbox)

---

## 💡 Key Insights

### Technical Lessons
1. **Version gaps are real:** 9-month knowledge cutoff created significant compatibility challenges
2. **Cache is both friend and foe:** Performance benefit, debugging nightmare
3. **Privacy must be systematic:** Automate protection, don't rely on memory
4. **Scripts need portability:** bash vs. zsh differences matter

### Process Lessons
1. **Document as you go:** Easier than reconstructing later
2. **Incremental deployment:** Ship minimum viable, iterate
3. **User preferences matter:** Periwinkle palette makes project feel personal
4. **Conversation limits** require **persistent documentation**

### Design Lessons
1. **Dark mode only is valid:** Simpler and appropriate for tech audience
2. **Emojis work as icons:** No additional assets needed
3. **Material You 3 scales well:** From mobile to desktop
4. **User photos inform palette:** Teal from repair mat became accent color

---

## 🔗 External References

### Project Links
- **Local:** http://localhost:4321
- **Repository:** (GitHub URL when created)
- **Production:** https://teardown.cafe (when deployed)

### Related Obsidian Notes
- [[Pi-hole Setup]]
- [[Raspberry Pi NVMe Configuration]]
- [[ARM Architecture]]
- [[Display Technology]]

---

## 📝 Maintenance Notes

### Regular Tasks
- **Weekly:** Add new teardown if content available
- **Monthly:** Review and update documentation
- **Quarterly:** Check for Astro updates and compatibility

### Backup Strategy
- Git repository (code + content)
- Obsidian vault (documentation)
- Original photos (external drive backup)

---

## 🎭 Project Philosophy

> "Amateur explorations of what's inside our everyday tech. No fancy equipment, just curiosity and a screwdriver."

This project embodies:
- **Accessibility:** Anyone can learn from these teardowns
- **Transparency:** Honest about mistakes and limitations
- **Privacy:** Respect for user and subject privacy
- **Quality:** High standards without gatekeeping
- **Documentation:** Share knowledge, not just results

---

## 📞 Support Resources

### When You Need Help
1. Check relevant documentation note first
2. Search past conversations: "Device teardown website design"
3. Review [[Teardown Cafe - Troubleshooting]]
4. Consult Astro documentation for framework issues
5. Use Claude for new questions (reference this index)

### Conversation Search Keywords
- "teardown website"
- "astro compatibility"
- "material you 3"
- "obsidian integration"
- "image organization"

---

*This index was created to consolidate knowledge from multiple conversations and provide quick access to all Teardown Cafe documentation.*

**Last Updated:** October 16, 2025
**Documentation Version:** 1.0
**Project Status:** Active Development

---

## Tags
#teardown-cafe #astro #material-you-3 #web-development #device-teardowns #privacy #obsidian-integration #documentation

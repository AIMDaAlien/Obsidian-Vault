---
tags: #guide #lessons-learned #astro #material-you #accessibility #ui-ux
created: 2025-10-19
related: 
  - "[[Teardown Cafe - Current State]]"
  - "[[Teardown Cafe - Technical Setup]]"
  - "[[Teardown Cafe - Design System]]"
  - "[[Claude Interaction Guidelines]]"
---

# Building a Material You 3 Website - Lessons Learned

## Project Context

Built Teardown Cafe: device teardown showcase using Astro v5.14.5 + Material You 3 design system with periwinkle/lavender palette.

## Key Decisions & Solutions

### UI/UX Design

**Progress Indicators**
- ❌ Horizontal progress bar → cluttered, covered navbar
- ✅ Vertical progress bar (right-aligned, 20px margin)
  - Descends as user scrolls (top→down fill)
  - 300ms fade transitions between sections
  - 6px pill width, gradient fill
  - Text follows progress position

**Accessibility Wins**
- Focus Mode toggle for ADHD users
  - Hides ambient effects (circuits, waves, particles)
  - Disables all animations
  - Persists preference in localStorage
- SVG icons instead of emojis (better scaling, theme consistency)
- Proper reduced-motion media query support

**Material You 3 Implementation**
- Frosted glass: `backdrop-filter: blur(12px)` (30% bg opacity)
- Shape: pill corners (100px radius) for controls
- Colors: Periwinkle (#B8B3FF), teal accent (#00BCD4)
- Typography: Ubuntu font family
- Elevation: Box-shadow for depth

### Technical Patterns

**Component Architecture**
```
DeviceIcons.astro → Single component, type prop
  - Uses currentColor for theme integration
  - All SVG paths inline for performance
```

**Animation Philosophy**
- Default: Smooth 300ms cubic-bezier(0.4, 0, 0.2, 1)
- Pointer-events: none for non-interactive overlays
- RAF-based scroll handlers for 60fps
- Sequential fade: wait for fade-out → update → fade-in

**File Organization**
```
src/
  components/    # Reusable UI (icons, progress, effects)
  pages/         # Routes
    teardowns/[id].astro  # Dynamic routes
  data/          # Content collections
```

### Common Pitfalls Avoided

1. **Button Default Styling**
   - Issue: HTML buttons have ugly default appearance
   - Fix: Use divs or reset with `appearance: none`, `border: none`, `background: none`

2. **Progress Bar Overlap**
   - Issue: Fixed elements blocking navbar clicks
   - Fix: Adjust z-index + top position, pointer-events: none

3. **Emoji Inconsistency**
   - Issue: Different rendering across OS
   - Fix: Custom SVG icons with currentColor

4. **Animation Overload**
   - Issue: Motion sickness, distraction
   - Fix: Focus Mode + prefers-reduced-motion support

5. **Fade Transition Timing**
   - Issue: Text changes mid-fade (jarring)
   - Fix: Sequential: fade out (300ms) → update → fade in (300ms)

## Design Principles Applied

**Hierarchy**
- Primary: Content (teardown articles)
- Secondary: Navigation
- Tertiary: Progress indicators, ambient effects

**Motion**
- Purposeful only (progress feedback, state changes)
- Respects user preferences
- 60fps target with RAF optimization

**Accessibility**
- Focus Mode for concentration
- Semantic HTML
- Proper ARIA labels
- Keyboard navigation support

## Tools & Workflow

**Development**
- Astro v5.14.5 (SSG, content collections)
- Material You 3 design tokens
- Git for version control
- Obsidian for documentation

**Design Iteration**
1. Build feature
2. Test in browser
3. Identify issues (screenshots helpful)
4. Iterate rapidly with small commits
5. Document decisions

## Quick Wins

- SVG icon component: ~30 lines, 7 device types
- Focus Mode: ~150 lines, massive accessibility boost
- Vertical progress: Clean, unobtrusive, functional
- Gaussian blur: `blur(12px)` < `backdrop-filter` (less expensive)

## Future Considerations

- Playwright MCP for automated UI testing
- Official product images for devices (copyright-safe)
- RSS feed implementation
- Image optimization automation

## Related Notes

- [[Teardown Cafe - Current State]] - Project status
- [[Teardown Cafe - Design System]] - Design tokens
- [[Claude Interaction Guidelines]] - Working with Claude effectively
- [[Claude Power User Workflow - Practical Implementation]] - Obsidian + Claude patterns

---

**Key Takeaway:** Start simple, iterate based on real usage. Material You 3 + accessibility = professional polish with minimal code.

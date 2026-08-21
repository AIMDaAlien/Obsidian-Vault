---
tags: [checklist]
---
# Testing Procedures

**Date:** November 8, 2025  
**Project:** [[README - Main Index|3D Print Shoppe]]  
**Related:** [[QA Process - Comprehensive Website Audit]]

---

## Mobile Testing Protocol

### Standard Viewports
```javascript
const testViewports = [
  { name: 'iPhone SE', width: 375, height: 667 },
  { name: 'iPhone 12', width: 390, height: 844 },
  { name: 'Small Mobile', width: 320, height: 568 },
  { name: 'Large Mobile', width: 414, height: 896 },
  { name: 'Tablet', width: 768, height: 1024 },
  { name: 'Desktop', width: 1366, height: 768 }
];
```

### Critical Tests

**Navigation Test:**
1. Load homepage on mobile viewport
2. Verify hamburger icon visible (48x48px minimum)
3. Click hamburger → menu expands
4. Click menu item → navigates correctly
5. Menu auto-closes after navigation

**Cart Test:**
1. Verify cart button visible (44x44px minimum)
2. Add product → cart badge updates
3. Click cart → drawer slides in
4. Update quantity → price recalculates
5. Remove item → cart updates
6. Click overlay → drawer closes

**Touch Target Test:**
- All interactive elements ≥ 44x44px
- Spacing between targets ≥ 8px
- No overlapping touch zones

**Text Readability:**
- Body text ≥ 16px
- Labels/captions ≥ 14px
- Headings scale appropriately
- No text overflow or truncation

---

## Cross-Browser Testing

### Required Browsers
- Chrome (latest) - Primary
- Safari (latest) - iOS compatibility
- Firefox (latest) - Standards compliance
- Mobile Safari - iOS testing
- Mobile Chrome - Android testing

### Browser-Specific Issues to Check
**Safari:**
- Backdrop-filter support (glassmorphism)
- oklch() color support
- Form autofill styling

**Firefox:**
- CSS Grid behavior
- Flexbox gaps
- Custom scrollbars

**Mobile Safari:**
- 100vh issues
- Touch event handling
- -webkit-appearance

---

## Functional Testing

### Product Pages
- [ ] Navigate to /shop → all products load
- [ ] Click product card → goes to /product/[slug]
- [ ] Product detail page shows images, price, description
- [ ] Color selector works (if applicable)
- [ ] Design selector works (multi-design products)
- [ ] Add to cart → opens drawer with item
- [ ] Related products section shows relevant items

### Cart Operations
- [ ] Add item → cart count updates
- [ ] Duplicate item → quantity increments
- [ ] Remove item → cart updates
- [ ] Update quantity → subtotal recalculates
- [ ] Clear cart → empties all items
- [ ] Cart persists → reload page, items remain

### Filters & Sorting
- [ ] Filter by category → shows only matching products
- [ ] Filter by availability → shows in-stock or made-to-order
- [ ] Multiple filters → applies both
- [ ] Sort by price → orders correctly
- [ ] Sort by name → alphabetical order
- [ ] Reset filters → shows all products

### Forms
- [ ] Contact form validation works
- [ ] Required fields enforce presence
- [ ] Email validation works
- [ ] Submit opens mailto link
- [ ] Form resets after submit

---

## Accessibility Testing

### Keyboard Navigation
- [ ] Tab through all interactive elements
- [ ] Focus indicators visible (outline/ring)
- [ ] Enter activates buttons/links
- [ ] Escape closes modals/drawers
- [ ] Arrow keys work in dropdowns

### Screen Reader Testing
```
Recommended: NVDA (Windows) or VoiceOver (Mac)
```

- [ ] Alt text on all images
- [ ] ARIA labels on icon buttons
- [ ] Form labels properly associated
- [ ] Landmark regions defined
- [ ] Page title announces correctly

### Color Contrast
```
Tool: WebAIM Contrast Checker
Minimum ratio: 4.5:1 for normal text
Minimum ratio: 3:1 for large text (18px+)
```

- [ ] Primary text on background ≥ 4.5:1
- [ ] Secondary text on background ≥ 4.5:1
- [ ] Button text on button background ≥ 4.5:1
- [ ] Link text distinguishable
- [ ] Error messages sufficient contrast

---

## Performance Testing

### Lighthouse Audit
```bash
# Run Lighthouse in Chrome DevTools
npm run build
npm run preview
# Open DevTools → Lighthouse → Run audit
```

**Target Scores:**
- Performance: ≥ 90
- Accessibility: ≥ 95
- Best Practices: ≥ 95
- SEO: ≥ 90

### Key Metrics
- **FCP (First Contentful Paint):** < 1.8s
- **LCP (Largest Contentful Paint):** < 2.5s
- **TBT (Total Blocking Time):** < 200ms
- **CLS (Cumulative Layout Shift):** < 0.1

### Image Optimization Check
```bash
# Check image sizes
find public/images -type f -exec du -h {} \;

# Target: Product images < 100KB each
# Format: WebP with JPEG fallback
```

---

## Regression Testing

**After Each Fix:**
1. Test the specific fixed component
2. Test related components
3. Run full mobile test suite
4. Check console for errors
5. Validate with Lighthouse

**Before Deployment:**
1. Full functional test suite
2. All viewports tested
3. Cross-browser validation
4. Performance audit passes
5. Accessibility check complete

---

## Test Documentation

### Test Report Template
```markdown
# Test Report - [Feature/Fix Name]
Date: [YYYY-MM-DD]
Tester: [Name/Agent]

## Tests Executed
- [ ] Mobile navigation
- [ ] Cart operations
- [ ] Product filtering
- [ ] Form validation

## Results
Pass: X/Y tests
Failures: [List specific failures]

## Issues Found
1. [Description]
   - Severity: Critical/High/Medium/Low
   - Steps to reproduce
   - Expected vs Actual behavior

## Recommendations
[Next steps or fixes needed]
```

---

## Automated Testing (Future)

### Playwright Setup
```javascript
// playwright.config.ts
export default {
  projects: [
    { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
    { name: 'Desktop Chrome', use: { viewport: { width: 1366, height: 768 } } }
  ]
};
```

### Critical Test Scenarios
```javascript
test('add to cart workflow', async ({ page }) => {
  await page.goto('/shop');
  await page.click('.product-card:first-child .add-to-cart-btn');
  await expect(page.locator('.cart-drawer')).toBeVisible();
  await expect(page.locator('.cart-count')).toContainText('1');
});

test('mobile menu toggle', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/');
  await page.click('.mobile-menu-toggle');
  await expect(page.locator('.nav-links')).toHaveClass(/open/);
});
```

---

**Tags:** #testing #qa #mobile #accessibility #performance

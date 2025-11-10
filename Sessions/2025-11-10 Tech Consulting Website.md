# Session 2025-11-10 - Tech Consulting Website

**Date:** 2025-11-10
**Duration:** ~3 hours
**Focus:** GA tracking, Stripe integration, dark mode, contact fixes

---

## What We Built

### 1. Google Analytics Integration
**Problem:** No tracking configured
**Solution:** Next.js Script component in layout.tsx
```typescript
<Script
  strategy="afterInteractive"
  src="https://www.googletagmanager.com/gtag/js?id=G-M81P4EWVJZ"
/>
```
**Learning:** Use `afterInteractive` strategy to avoid blocking initial page load

### 2. Stripe Embedded Checkout
**Problem:** Need payment flow for Quick Answers service
**Solution:** Embedded checkout with lazy-loaded Stripe instance

**Key Pattern - Lazy Loading:**
```typescript
let stripeInstance: Stripe | null = null;

export const getStripe = (): Stripe => {
  if (!stripeInstance) {
    stripeInstance = new Stripe(process.env.STRIPE_SECRET_KEY, {
      apiVersion: '2025-10-29.clover',
      typescript: true,
    });
  }
  return stripeInstance;
};
```
**Why:** Prevents build-time env var checks that fail on Vercel

**Embedded Checkout Flow:**
1. Form submission → POST to `/api/checkout`
2. API creates session with `ui_mode: 'embedded'`
3. Returns `clientSecret`
4. `EmbeddedCheckoutProvider` renders Stripe form in modal
5. Redirect to `/quick-answer-success` on completion

**Cost:** $15 = 1500 cents (`unit_amount: 1500`)

### 3. Dark Mode with M3 Splash Animation
**Problem:** Need dark mode with expressive transition
**Solution:** CSS clip-path animation + localStorage persistence

**Animation Pattern:**
```css
@keyframes splash-dark {
  0% { clip-path: circle(0% at 100% 0%); }
  100% { clip-path: circle(150% at 100% 0%); }
}

body.theme-transition-dark::before {
  content: '';
  position: fixed;
  width: 100%;
  height: 100%;
  background: var(--background);
  z-index: 9999;
  animation: splash-dark 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
```

**Toggle Implementation:**
```typescript
const toggleTheme = () => {
  const newTheme = theme === 'light' ? 'dark' : 'light';
  document.body.classList.add(`theme-transition-${newTheme}`);
  document.documentElement.classList.toggle('dark', newTheme === 'dark');
  setTheme(newTheme);
  localStorage.setItem('theme', newTheme);
  setTimeout(() => {
    document.body.classList.remove(`theme-transition-${newTheme}`);
  }, 800);
};
```

**Learning:** Use `::before` pseudo-element for overlay animation to avoid layout shifts

### 4. Quick Answers Form Enhancement
**Features Added:**
- Guidance cards (when to use vs full service)
- localStorage autosave with 500ms debounce
- Auto-restore draft on reopen
- Character counter with warning at 400/500
- Stripe payment integration

**Autosave Pattern:**
```typescript
useEffect(() => {
  if (formData.name || formData.email || formData.question) {
    const timeoutId = setTimeout(() => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(formData));
    }, 500);
    return () => clearTimeout(timeoutId);
  }
}, [formData]);
```

**Learning:** Always debounce localStorage writes to avoid performance issues

### 5. Contact Section Fixes
**Issues Found:**
- Duplicate "Quick Answers" card causing 250px whitespace
- Non-functional button (missing onClick)
- "Call or text" copy when only texting preferred

**Fix:** Removed duplicate, wired up onClick, updated copy

---

## Git Workflow Learnings

### Problem: Branch Management
Started on Claude branch: `claude/aims-consulting-foundation-011CUqVUgt1jnbGzTKPzck2n`

### Solution:
```bash
git branch main claude/aims-consulting-foundation-011CUqVUgt1jnbGzTKPzck2n
git checkout main
git push -u origin main
git branch -D claude/aims-consulting-foundation-011CUqVUgt1jnbGzTKPzck2n
git push origin --delete claude/aims-consulting-foundation-011CUqVUgt1jnbGzTKPzck2n
```

**Learning:** Create main from existing branch rather than merging when branch is intended to become main

---

## Build Errors Encountered & Fixed

### 1. Missing Stripe Packages
**Error:** `Module not found: Can't resolve 'stripe'`
**Fix:** `npm install stripe @stripe/stripe-js @stripe/react-stripe-js`
**Lesson:** Always commit package.json + package-lock.json together

### 2. API Version Mismatch
**Error:** `Type '"2024-11-20.acacia"' is not assignable to type '"2025-10-29.clover"'`
**Fix:** Updated to correct API version for Nov 2025
**Lesson:** Check Stripe package version for correct API string

### 3. Build-Time Env Check
**Error:** `STRIPE_SECRET_KEY is not set` during build
**Fix:** Lazy-load Stripe with `getStripe()` function
**Lesson:** Never initialize Stripe at module top-level; always lazy-load

---

## Design System Insights

### M3 Expressive Colors
**Light Mode:** Periwinkle (#5a4a75), Lavender (#7B6BA4)
**Dark Mode:** Lighter variants (#D0BCFF, #CCC2DC) for contrast

**Learning:** Dark mode needs lighter accent colors, not darker ones

### Animation Guidelines
- Hover scale: 1.02 (subtle)
- Easing: `cubic-bezier(0.4, 0, 0.2, 1)`
- Theme transitions: 800ms
- Micro-interactions: 200-300ms

---

## Technical Debt Created
- [ ] No Stripe webhook handler yet (manual verification required)
- [ ] M3 button component not created (using inline styles)
- [ ] Dark mode not tested across all sections
- [ ] No error boundary for Stripe checkout failures

---

## Token Usage Analysis
**Session Total:** ~101k / 190k (53%)
**Breakdown:**
- Initial diagnostics: ~15k
- Stripe research: ~8k
- Code generation: ~40k
- Obsidian operations: ~3k
- Git operations: ~5k
- Error fixing iterations: ~30k

**Efficiency:** Moderate - multiple build error iterations consumed tokens

---

## What Worked Well
1. Hybrid approach: Stripe research → implementation → testing
2. Lazy-loading pattern solved build issues cleanly
3. Dark mode splash animation executed perfectly on first try
4. localStorage autosave pattern is robust

## What Could Improve
1. Test build locally before pushing (caught 3 build errors on Vercel)
2. Verify package.json committed before marking "done"
3. Check Stripe API version docs before hardcoding

---

## Key Takeaways for Future Sessions

### Stripe Integration Checklist
- [ ] Install all 3 packages: `stripe`, `@stripe/stripe-js`, `@stripe/react-stripe-js`
- [ ] Use lazy-loading for Stripe initialization
- [ ] Check current API version in package
- [ ] Test with Stripe test keys before production
- [ ] Add webhook handler for payment confirmation

### Dark Mode Checklist
- [ ] Define CSS variables for both themes
- [ ] Use `::before` for splash animations
- [ ] Persist to localStorage + respect system preference
- [ ] Test all sections for contrast compliance
- [ ] Add theme toggle to header

### Form Best Practices
- [ ] Debounce autosaves (500ms minimum)
- [ ] Show restoration notification on load
- [ ] Clear saved data on successful submission
- [ ] Character counters with warnings

---

## Next Session Priorities
1. **Test Stripe checkout** with test cards (4242 4242 4242 4242)
2. **Create M3 button component** (primary/secondary/ghost/outline)
3. **Apply buttons** to Hero, Services, Contact sections
4. **Add webhook handler** for payment confirmation
5. **Accessibility audit** of dark mode

---

**Session Rating:** 8/10
- Successfully shipped 5 major features
- Fixed multiple build issues
- Created comprehensive documentation
- Token usage could be more efficient with local testing

**Continue with:** M3 component system + Stripe testing

# Tech Consulting Website - Current State

**Last Updated:** 2025-11-10
**Project:** Tech Consulting (your-project.com)
**Status:** Active Development
**Deploy Status:** ✅ Production (Vercel)

---

## Quick Context
Student-run PC setup and consultation service in [local area]. Modern Next.js site with Material Design 3, Stripe payments, and privacy-focused approach.

---

## Tech Stack
- **Framework:** Next.js 15 (App Router), TypeScript
- **Styling:** Tailwind v4 (CSS-based, no config file)
- **Animations:** Framer Motion
- **Payments:** Stripe Embedded Checkout
- **Analytics:** Google Analytics (G-M81P4EWVJZ)
- **Deployment:** Vercel (main branch)

---

## Services & Pricing
1. **PC Setup & Optimization** - $175 / 2hrs in-person
2. **Computer Buying Consultation** - $100 / 1hr remote
3. **Quick Tech Question** - $15 / 24hr async (NEW ✨)

---

## Recent Session: 2025-11-10

### What We Built
1. **Google Analytics Integration**
   - Added GA4 tracking (G-M81P4EWVJZ) to app/layout.tsx
   - Next.js Script component with afterInteractive strategy
   - Analytics events: booking clicks, modal opens, email clicks

2. **Contact Section Fixes**
   - Removed duplicate "Quick Answers" card (fixed 250px whitespace)
   - Changed "call or text" → "text only" per business preference
   - Fixed non-functional Quick Answers button

3. **Stripe Payment Integration**
   - Embedded checkout with `ui_mode: 'embedded'`
   - API version: 2025-10-29.clover
   - Lazy-loaded Stripe to avoid build-time env errors
   - $15 Quick Answers payment flow complete
   - Success page: `/quick-answer-success`
   - Environment variables configured in Vercel

4. **Enhanced Quick Answers Form**
   - Guidance cards: "Perfect for Quick Answers" vs "Need Full Service?"
   - localStorage autosave with key: `quick_answers_draft`
   - 500ms debounced saves
   - Auto-restore draft on modal reopen
   - Character counter turns amber at 400/500
   - Stripe EmbeddedCheckoutProvider integration

5. **Dark Mode with M3 Expressive**
   - Splash animation: top-right → bottom-left (800ms cubic-bezier)
   - M3 color tokens for light/dark themes
   - ThemeToggle component in header
   - Respects system preference, persists to localStorage
   - Enhanced elevation shadows adapt to theme

### Technical Learnings

**Stripe Integration Pattern:**
```typescript
// Lazy load to avoid build-time errors
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

**Dark Mode Splash Animation:**
```css
@keyframes splash-dark {
  0% { clip-path: circle(0% at 100% 0%); }
  100% { clip-path: circle(150% at 100% 0%); }
}
```

**localStorage Autosave Pattern:**
```typescript
useEffect(() => {
  const timeoutId = setTimeout(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(formData));
  }, 500); // Debounce
  return () => clearTimeout(timeoutId);
}, [formData]);
```

### Git Workflow Issues Encountered
- Initially committed to Claude branch: `claude/aims-consulting-foundation-011CUqVUgt1jnbGzTKPzck2n`
- Created new `main` branch from Claude branch
- Deleted old Claude branch after main established
- Fixed build errors: Missing Stripe packages, API version mismatch, build-time env check

### File Structure
```
tech-consulting-local/
├── app/
│   ├── api/checkout/route.ts (NEW)
│   ├── layout.tsx (GA added)
│   ├── globals.css (dark mode)
│   └── quick-answer-success/page.tsx (NEW)
├── components/
│   ├── integrations/QuickAnswersForm.tsx (Stripe + autosave)
│   ├── sections/Contact.tsx (fixed layout)
│   ├── layout/Header.tsx (theme toggle)
│   └── ui/
│       ├── ThemeToggle.tsx (NEW)
│       └── modal.tsx (existing)
├── lib/
│   ├── stripe.ts (NEW - lazy load)
│   └── analytics.ts (enhanced)
└── .env.local (NEW - Stripe keys)
```

---

## Environment Variables (Vercel)
- `STRIPE_SECRET_KEY` - Stripe secret key (sk_test_...)
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - Stripe publishable key (pk_test_...)
- `NEXT_PUBLIC_GA_ID` - Google Analytics tracking ID

---

## Design System

### Colors (M3 Expressive)
**Light Mode:**
- Primary: #5a4a75 (periwinkle)
- Secondary: #7B6BA4 (lavender)
- Background: #FAFBFF

**Dark Mode:**
- Primary: #D0BCFF (lighter periwinkle)
- Secondary: #CCC2DC (lighter lavender)
- Background: #1C1B1F (M3 Dark Surface)

### Animation Principles
- Scale on hover: 1.02
- Transitions: cubic-bezier(0.4, 0, 0.2, 1)
- Spring physics for interactive elements
- Debounced autosaves: 500ms

---

## Known Issues & TODOs

### High Priority
- [ ] Test Stripe payment flow end-to-end with test keys
- [ ] Add webhook handler for payment confirmation
- [ ] Test dark mode across all sections

### Medium Priority
- [ ] Create M3 button component (4 variants: primary/secondary/ghost/outline)
- [ ] Apply M3 button to Hero, Services, Contact CTAs
- [ ] Create M3 card component for services/testimonials
- [ ] Animate trust badges (8+ years, 10+ builds, 100% satisfaction)

### Low Priority
- [ ] Implement real Calendly payment integration
- [ ] Add error boundary for Stripe checkout
- [ ] Optimize dark mode color contrast for WCAG AAA

---

## Deployment Notes

### Build Process
1. `npm run build` - Next.js production build
2. Vercel auto-deploys from `main` branch
3. Environment variables injected at build time
4. Turbopack builds in ~10s

### Common Build Errors Fixed
1. **Stripe not found** → Install packages: `npm install stripe @stripe/stripe-js @stripe/react-stripe-js`
2. **API version mismatch** → Update to `2025-10-29.clover`
3. **Build-time env error** → Lazy-load Stripe with `getStripe()`

---

## Update Protocol

**When to Update This Note:**
- Major feature completion (payments, dark mode, etc.)
- Architecture changes (new API routes, state management)
- Deployment blockers resolved
- Design system updates

**Quick Updates (No Note Update):**
- Bug fixes
- Copy changes
- Minor styling tweaks

**How to Update:**
1. Append new session section with date
2. Update "Last Updated" timestamp
3. Add new TODOs or mark completed
4. Document new technical patterns if introduced

---

## Next Session Focus
1. Test Stripe checkout with real test cards
2. Implement M3 button component across site
3. Add payment webhook handler
4. Accessibility audit with dark mode

---

## Reference Links
- **Repo:** https://github.com/username/tech-consulting
- **Live Site:** https://your-project.com
- **Vercel Dashboard:** https://vercel.com (check deployment status)
- **Stripe Dashboard:** https://dashboard.stripe.com/test/apikeys
- **GA Dashboard:** https://analytics.google.com (property: G-M81P4EWVJZ)

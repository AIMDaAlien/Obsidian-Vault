---
tags: [website-rebuild]
---
# Technical Architecture - 3D Print Shoppe

**Project:** 3D Print Shoppe  
**Tech Stack:** Astro 5.0 + Material Web 2.4.1 + TypeScript  
**Status:** Production-ready  
**Last Updated:** November 21, 2025

---

## System Overview

Full-stack e-commerce platform for custom 3D printing service. Built with JAMstack architecture for maximum performance and SEO optimization.

### Core Technologies

```
Frontend Framework:  Astro 5.0.0 (SSG + Islands Architecture)
UI Components:       Material Web 2.4.1 (Web Components)
Type Safety:         TypeScript 5.6.3 (strict mode)
State Management:    Nanostores 0.11.3
Styling:             Material Design 3 + Custom CSS
Animation:           Anime.js 4.2.2 + Custom Spring Physics
Testing:             Playwright 1.56.1
Deployment:          Vercel + GitHub
```

---

## Architecture Patterns

### Islands Architecture (Astro)

Static HTML generated at build time with hydrated interactive components:

```
Homepage (Static):
├── Hero (Static HTML)
├── VendorCard (Static + Client-side modal)
├── How It Works (Static)
└── CTA Section (Static)

Interactive Islands:
├── CartButton (Nanostores - hydrated on load)
├── CartDrawer (Nanostores - hydrated on interaction)
├── ThemeToggle (Vanilla JS - hydrated on load)
└── VendorCatalogModal (Vanilla JS - hydrated on interaction)
```

**Benefits:**
- Fast initial load (minimal JS)
- SEO-friendly (fully rendered HTML)
- Interactive where needed
- Zero-JS by default

### State Management (Nanostores)

Lightweight (900 bytes) atomic state management:

```typescript
// cartStore.ts
export const cartItems = map<Record<string, CartItem>>({})
export const isCartOpen = atom(false)
export const cartItemsCount = computed(cartItems, items => 
  Object.values(items).reduce((total, item) => total + item.quantity, 0)
)
```

**Persistence Strategy:**
- localStorage for cart data
- Automatic sync on state changes
- SSR-safe with `typeof window` checks

### Component Architecture

**Astro Components (Server-rendered):**
- `.astro` files for static content
- Props-based data flow
- Scoped styles by default
- No runtime overhead

**Web Components (Client-side):**
- Material Web for interactive elements
- Custom elements for complex interactions
- Event-based communication

---

## Design System Implementation

### Material Design 3 Expressive

**Token System:**
```css
:root {
  /* Brand Colors */
  --md-sys-color-primary: #6366F1;        /* Periwinkle */
  --md-sys-color-secondary: #A78BFA;      /* Lavender */
  --md-sys-color-tertiary: #10B981;       /* Green */
  
  /* Typography - Age-Friendly */
  --md-sys-typescale-body-large: 1.125rem;  /* 18px */
  --md-sys-typescale-body-medium: 1rem;     /* 16px */
  
  /* Shape - Expressive */
  --md-sys-shape-corner-extra-large: 28px;  /* Larger than standard M3 */
  
  /* Motion */
  --md-sys-motion-easing-spring-bouncy: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

**Accessibility Standards:**
- WCAG AA contrast ratios (4.5:1 minimum)
- Touch targets ≥48px
- Keyboard navigation support
- Screen reader labels (ARIA)
- Focus indicators visible

**Animation Philosophy:**
- Spring physics for natural motion
- Expressive transforms (scale + rotate)
- Reduced motion support
- Performance-optimized (GPU-accelerated)

---

## Key Systems

### 1. Vendor Catalog System

**Data Structure:**
```typescript
interface Vendor {
  id: string
  name: string
  displayName: string
  makerWorldProfile: string
  avatar: string
  description: string
  tagline: string
  specialties: string[]
  featured: boolean
  modelCount: number
  achievements: {
    followers: string
    featuredModels?: number
    popularPrints?: number
  }
}
```

**Implementation:**
- Static data in `vendors.json`
- Server-side filtering via `getFeaturedVendors()`
- Client-side modal for browsing
- Direct links to MakerWorld profiles

**Why this approach:**
- MakerWorld has no API/iframe capability
- Maintains vendor attribution
- Allows browsing without leaving site
- Scalable to more vendors

### 2. Shopping Cart

**State Management:**
```typescript
// Cart operations
addToCart(product, color) → Updates cartItems map
removeFromCart(key) → Deletes from cartItems
updateQuantity(key, qty) → Modifies quantity
clearCart() → Resets all items

// Computed values
cartItemsCount → Total item quantity
cartSubtotal → Sum of item prices
cartTotal → Subtotal + rush fee (if enabled)
```

**Persistence:**
- localStorage key: 'cart'
- JSON serialization
- Load on mount, save on change
- SSR-safe implementation

**Rush Order System:**
- Boolean flag in state
- +$5 fee to total
- Visual indicator in cart

### 3. Inventory Management

**Admin Interface:**
```
/admin/inventory       → Main inventory page
/admin/inventory-v2    → Alternative layout
/admin/inventory-new   → Latest version
```

**API Endpoints:**
```typescript
GET  /api/inventory           → Fetch all filament data
POST /api/inventory-update    → Update filament quantities/colors
```

**Data Schema:**
```typescript
interface FilamentSpool {
  id: string
  color: string
  brand: string
  material: string  // PLA, PETG, etc.
  weight: number    // grams
  inStock: boolean
  dateAdded: string
}
```

**Components:**
- FilamentCard: Display individual spools
- FilamentEditorModal: Edit spool details
- QuickActionBar: Bulk operations
- InventoryHeader: Stats + filters

### 4. Form Systems

**Contact Form:**
- Endpoint: formspree.io/f/your-form-id
- Fields: name, email, phone, message
- Validation: HTML5 + client-side

**Custom Order Form:**
- Endpoint: formspree.io/f/your-form-id
- Fields: name, email, phone, project details, size, color preferences
- Conditional fields based on order type
- File upload support (STL files)

**Color Selector:**
- Dynamic filament color options
- Availability checking via inventory
- Visual color swatches

---

## Performance Optimization

### Build-Time Optimizations

**Astro SSG:**
- Pre-renders all pages at build time
- Generates optimized HTML
- Minimal runtime JavaScript
- Automatic code splitting

**Image Optimization:**
- WebP format (45+ product images)
- Lazy loading below fold
- Responsive srcsets
- Compressed assets

### Runtime Optimizations

**JavaScript:**
- Islands architecture (selective hydration)
- Tree-shaking unused code
- Module preloading
- Deferred non-critical scripts

**CSS:**
- Scoped styles (no global conflicts)
- Critical CSS inlined
- Unused styles removed
- Minified output

**Caching Strategy:**
```
Static Assets:    Cache-Control: max-age=31536000, immutable
HTML Pages:       Cache-Control: max-age=3600, stale-while-revalidate
API Responses:    No caching (dynamic data)
```

### Lighthouse Targets

```
Performance:     ≥90
Accessibility:   ≥95
Best Practices:  ≥95
SEO:             ≥95
```

**Core Web Vitals:**
- LCP (Largest Contentful Paint): <2.5s
- FID (First Input Delay): <100ms
- CLS (Cumulative Layout Shift): <0.1

---

## Development Workflow

### Local Development

```bash
npm run dev          # Start dev server (port 4321)
npm run build        # Production build
npm run preview      # Preview production build
npm run astro check  # Type checking
npm run lint         # ESLint
npm run format       # Prettier
npm run test         # Playwright E2E tests
```

### Git Workflow

```
main (production)    → Protected branch, auto-deploys to Vercel
dev (staging)        → Development branch, preview deployments
feature/*            → Feature branches
```

**Pre-commit Hooks (Husky):**
- ESLint auto-fix
- Prettier formatting
- Type checking
- Staged files only

### Testing Strategy

**E2E Tests (Playwright):**
```typescript
// tests/vendor-catalog.spec.ts
test('should open vendor modal on card click', async ({ page }) => {
  await page.goto('/')
  await page.click('[data-vendor-id="sabre-design"]')
  await expect(page.locator('.vendor-modal')).toBeVisible()
})
```

**Manual Testing Checklist:**
- Mobile responsive (320px - 1920px)
- Touch target sizes (≥48px)
- Keyboard navigation
- Screen reader compatibility
- Form validation
- Cart persistence

---

## Deployment Architecture

### Vercel Configuration

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "astro",
  "installCommand": "npm install"
}
```

**Environment:**
- Node.js 20.x
- Auto-preview for PRs
- Production deployment on main push
- Edge functions for API routes
- CDN for static assets

### DNS Setup (your-domain.com)

```
Type: CNAME
Name: @
Value: cname.vercel-dns.com
TTL: 3600
```

**SSL/TLS:**
- Automatic via Vercel
- HTTP/2 enabled
- Certificate renewal handled

---

## Security Considerations

**Client-Side:**
- No sensitive data in localStorage
- XSS prevention (Astro auto-escapes)
- CSP headers configured
- HTTPS enforced

**Forms:**
- Honeypot fields (bot detection)
- Rate limiting via Formspree
- Input sanitization
- CSRF protection (Formspree handles)

**Payment:**
- No credit card data stored
- PayPal/Venmo external handling
- Privacy policy required
- GDPR considerations (if EU traffic)

---

## Scalability Considerations

### Current Capacity

**Single Printer (Bambu Lab A1):**
- Max 3-5 items per day (8-12 hour prints)
- 20-30 orders per month sustainable
- Weekend pickup model reduces logistics

### Growth Path

**Phase 1 (Month 1-3):**
- Validate product-market fit
- Optimize catalog based on demand
- Build customer reviews

**Phase 2 (Month 4-6):**
- Add 2nd printer if hitting capacity
- Implement queue management system
- Automate email notifications

**Phase 3 (Year 1+):**
- Max 3 printers (bedroom capacity constraint)
- Sister handles marketing/photography
- Consider B2B partnerships

---

## Technical Debt & Future Improvements

**Known Issues:**
- Cart checkout flow incomplete (currently quote-based)
- Inventory management manual updates (no barcode scanning)
- No automated email confirmations (Formspree limitations)
- Payment integration not implemented (intentional for MVP)

**Planned Enhancements:**
- Stripe/PayPal API integration (Phase 2)
- Order tracking dashboard
- Customer accounts (optional)
- Analytics integration (Plausible)
- Email newsletter (Buttondown)
- Blog/portfolio section

**Technical Improvements:**
- Migrate to Astro DB for dynamic inventory
- Implement server-side cart validation
- Add unit tests (Vitest)
- Optimize bundle size (<100KB JS)
- Implement service worker (offline support)

---

## Lessons for Similar Projects

**1. Start with MVP, iterate based on usage**
- Original plan: simple quote form
- User feedback led to: full e-commerce platform
- Don't over-engineer initially

**2. Choose tech for maintainability**
- Astro: minimal JS, great DX
- Nanostores: simple state, easy to debug
- Material Web: consistent UI, accessible by default

**3. Performance matters for target audience**
- Older demographic needs fast load times
- Mobile-first (most Nextdoor users on phone)
- Large text, high contrast essential

**4. Document as you build**
- Technical decisions recorded
- Architecture rationale explained
- Makes handoff easier (recruiters, collaborators)

**5. Accessibility is not optional**
- 48px touch targets prevent mis-taps
- High contrast helps older eyes
- Keyboard nav for power users
- Screen reader support broadens audience

---

## Resources & References

**Documentation:**
- Astro: https://docs.astro.build
- Material Design 3: https://m3.material.io
- Nanostores: https://github.com/nanostores/nanostores

**Tools:**
- Vercel: https://vercel.com
- Formspree: https://formspree.io
- Playwright: https://playwright.dev

**Design Resources:**
- Material Web Components: https://material-web.dev
- Ubuntu Font: https://fonts.google.com/specimen/Ubuntu
- Color System: Material Theme Builder

---

*For questions or collaboration: email@example.com*

# Architecture Decisions

**Date:** November 8, 2025  
**Project:** [[README - Main Index|3D Print Shoppe]]  
**Related:** [[Website Technical Specs]], [[QA Process - Comprehensive Website Audit]]

---

## Technology Stack

### Core Framework: Astro
**Decision:** Use Astro for static site generation  
**Rationale:**
- Zero JavaScript by default (faster page loads)
- Component-based architecture (reusability)
- Built-in image optimization
- Perfect for content-heavy ecommerce
- Easy deployment to Vercel

**Alternatives Considered:**
- Next.js: Too heavy for simple ecommerce catalog
- Remix: Overkill for static product pages
- SvelteKit: Less mature ecosystem

---

## Design System

### Material Design 3
**Decision:** Use MD3 tokens and components  
**Rationale:**
- Modern, professional aesthetic
- Comprehensive design language
- Accessibility built-in
- Responsive by default
- Periwinkle/lavender color scheme fits brand

**Implementation:**
- Custom token system in `m3-expressive.css`
- Dynamic color generation with oklch()
- Elevation system for depth
- Motion tokens for consistent animations

**Trade-offs:**
- oklch() limited browser support (Safari 16.4+, Chrome 111+)
- Fallback to rgba() for older browsers
- Larger CSS bundle than minimal frameworks

---

## State Management

### Nanostores
**Decision:** Use nanostores for global state  
**Rationale:**
- Tiny bundle size (< 1KB)
- Framework-agnostic
- Simple API
- Perfect for cart state
- Built-in persistence helpers

**State Structure:**
```typescript
cartItems: Map<string, CartItem>
isCartOpen: Atom<boolean>
```

**Key Pattern:**
```typescript
`${productId}-${color}-${designs?.join(',')}`
// Ensures unique cart entries for product variants
```

**Alternatives Considered:**
- Zustand: Overkill for simple cart
- Redux: Way too complex
- Context API: Not needed in Astro

---

## Data Architecture

### Static JSON + TypeScript
**Decision:** Store products in `products.json` with TypeScript interfaces  
**Rationale:**
- No database needed for catalog
- Type safety at build time
- Fast static site generation
- Easy to edit and version control
- Can migrate to CMS later

**Schema Design:**
```typescript
interface Product {
  id: string;           // Unique identifier
  slug: string;         // URL-friendly
  name: string;
  price: number;        // In dollars
  category: string;
  availability: 'in-stock' | 'made-to-order';
  images: string[];
  colors?: string[];
  designs?: string[];   // For multi-design products
  // ... metadata fields
}
```

**Future Migration Path:**
- Phase 2: Add inventory.json integration
- Phase 3: Migrate to Supabase for real-time inventory
- Phase 4: Add CMS for product management

---

## Routing Strategy

### File-Based with Dynamic Routes
**Decision:** Use Astro's file-based routing  
**Rationale:**
- Convention over configuration
- Intuitive structure
- SSG-friendly
- SEO-optimized

**Route Structure:**
```
/                    → index.astro (homepage)
/shop                → shop.astro (all products)
/product/[slug]      → product/[slug].astro (detail pages)
/custom-order        → custom-order.astro
/contact             → contact.astro
/404                 → 404.astro
```

**SSG Strategy:**
```typescript
// Generate static pages for all products at build time
export const getStaticPaths = () => {
  return getAllProducts().map(product => ({
    params: { slug: product.slug }
  }));
};
```

---

## Cart Implementation

### Client-Side with LocalStorage
**Decision:** Implement cart entirely client-side  
**Rationale:**
- No backend required (Phase 1)
- Instant feedback
- Works offline
- Simple implementation
- Persists between sessions

**Persistence Strategy:**
```typescript
// Save on every cart update
cartItems.subscribe(items => {
  localStorage.setItem('cart', JSON.stringify(items));
});

// Load on initialization
const stored = localStorage.getItem('cart');
if (stored) cartItems.set(JSON.parse(stored));
```

**Limitations:**
- No cross-device sync
- Vulnerable to localStorage limits
- No server-side validation

**Future Migration:**
- Phase 2: Add backend checkout
- Phase 3: Implement user accounts
- Phase 4: Server-side cart persistence

---

## Image Strategy

### Static Images with Lazy Loading
**Decision:** Store images in `/public/images/products/`  
**Rationale:**
- Simple deployment
- No CDN setup required
- Vercel handles optimization
- Easy to manage

**Optimization:**
```astro
<img 
  src={product.images[0]}
  alt={product.name}
  loading="lazy"
  width="400"
  height="400"
/>
```

**Future Enhancements:**
- Convert to WebP format
- Generate responsive sizes (400w, 800w, 1200w)
- Use Astro's `<Image>` component
- Implement blur-up placeholders

---

## Form Handling

### Mailto Interim Solution
**Decision:** Use mailto links for Phase 1  
**Rationale:**
- No backend required
- Works immediately
- User's email client handles delivery
- Simple implementation

**Implementation:**
```javascript
const mailto = `mailto:amasudtech@gmail.com?subject=${subject}&body=${body}`;
window.location.href = mailto;
```

**Limitations:**
- Depends on user's email client
- No form data storage
- No automated responses
- No spam protection

**Phase 2 Plan:**
- Implement EmailJS or similar service
- Add server-side validation
- Store form submissions in database
- Send confirmation emails

---

## Subagent Architecture

### Domain-Specific Agents
**Decision:** Use specialized subagents with exclusive domains  
**Rationale:**
- Prevents CSS conflicts
- Clearer responsibility boundaries
- Faster execution (parallel tasks)
- Better code quality
- Easier debugging

**Agent Domains:**
- `m3-style-designer`: All styling
- `astro-component-architect`: Structure
- `ecommerce-logic-specialist`: Business logic
- `state-store-engineer`: State management
- `responsive-qa-tester`: Testing

**Previous Issues Resolved:**
- CSS conflicts from multiple agents: ELIMINATED
- Hydration mismatches: PREVENTED
- Inconsistent patterns: STANDARDIZED

---

## Performance Targets

### Lighthouse Goals
- Performance: ≥ 90
- Accessibility: ≥ 95
- Best Practices: ≥ 95
- SEO: ≥ 90

### Core Web Vitals
- **FCP:** < 1.8s (homepage)
- **LCP:** < 2.5s (product pages)
- **TBT:** < 200ms
- **CLS:** < 0.1

### Strategies:
- Minimal JavaScript (Astro islands)
- Lazy load images
- Defer non-critical CSS
- Optimize fonts (preconnect)
- Static generation (no server rendering)

---

## Deployment Strategy

### Vercel with GitHub Integration
**Decision:** Deploy to Vercel via GitHub  
**Rationale:**
- Zero-config Astro support
- Automatic preview deployments
- Built-in image optimization
- Global CDN
- Free tier sufficient

**Build Configuration:**
```javascript
// astro.config.mjs
export default {
  output: 'static',
  site: 'https://3dprintshoppe.vercel.app',
  integrations: [sitemap()]
};
```

**Deployment Workflow:**
1. Push to main branch
2. Vercel auto-builds
3. Preview URL generated
4. Manual approval for production
5. Deploy to custom domain

---

## Security Considerations

### Client-Side Only (Phase 1)
- No authentication required
- No payment processing
- No user data storage
- No API endpoints

### Phase 2 Requirements:
- Implement CSP headers
- Add rate limiting
- Sanitize form inputs
- Use HTTPS only
- Implement CSRF protection

---

## Mobile-First Design

### Breakpoints
```css
/* Mobile first approach */
/* Base styles: mobile (< 640px) */

@media (min-width: 640px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
@media (min-width: 1280px) { /* Large desktop */ }
```

### Touch Targets
- Minimum 44x44px (WCAG 2.1 AAA)
- Adequate spacing (≥8px)
- No overlapping zones

### Typography Scale
- Base: 16px (mobile)
- Labels: 14px minimum
- Headings: Fluid scaling with clamp()

---

## Future Considerations

### Phase 2 Enhancements
- Backend API (Express or Astro endpoints)
- Inventory management system
- Order tracking
- Email notifications
- Payment processing (Stripe)

### Phase 3 Features
- User accounts
- Order history
- Wishlist
- Product reviews
- Search functionality

### Phase 4 Scalability
- Migrate to CMS (Sanity or Strapi)
- Add product filtering
- Implement recommendation engine
- Analytics dashboard
- Admin panel

---

**Tags:** #architecture #decisions #rationale #technical-design

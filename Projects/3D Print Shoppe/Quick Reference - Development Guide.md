# Quick Reference - Development Guide

**Date:** November 8, 2025  
**Project:** [[README - Main Index|3D Print Shoppe]]

---

## When to Use Each Subagent

| Task | Subagent | Example |
|------|----------|---------|
| Fix button styling | `m3-style-designer` | Remove undefined CSS classes |
| Create new page | `astro-component-architect` | Build product detail page |
| Fix cart logic | `ecommerce-logic-specialist` | Add design selection to cart |
| Update state | `state-store-engineer` | Modify cartStore interface |
| Test mobile | `responsive-qa-tester` | Validate navigation on iPhone |
| Validate data | `data-validator` | Check products.json schema |
| Deploy config | `vercel-deploy-optimizer` | Add sitemap generation |

---

## Critical File Locations

```
src/
├── components/
│   ├── Navigation.astro         # Header + mobile menu
│   ├── CartButton.astro         # Cart icon + badge
│   ├── CartDrawer.astro         # Slide-in cart panel
│   ├── ProductCard.astro        # Product grid item
│   └── Hero.astro               # Homepage hero
├── pages/
│   ├── index.astro              # Homepage
│   ├── shop.astro               # Product catalog
│   ├── product/[slug].astro     # Product detail (TO CREATE)
│   ├── contact.astro            # Contact form (TO CREATE)
│   └── 404.astro                # Error page (TO CREATE)
├── lib/
│   ├── products.ts              # Product utilities
│   └── types.ts                 # TypeScript interfaces
├── stores/
│   └── cartStore.ts             # Cart state management
├── styles/
│   ├── global.css               # Base styles + resets
│   ├── m3-expressive.css        # MD3 tokens
│   └── animations.css           # Motion system
└── data/
    └── products.json            # Product catalog
```

---

## Common Commands

```bash
# Development
npm run dev              # Start dev server (localhost:4321)
npm run build            # Build for production
npm run preview          # Preview production build

# Testing
npm run test             # Run Playwright tests (future)
npm run validate         # Validate products.json (future)

# Deployment
git push origin main     # Auto-deploys to Vercel
```

---

## CSS Quick Reference

### Material Design 3 Tokens
```css
/* Colors */
var(--md-sys-color-primary)
var(--md-sys-color-on-primary)
var(--md-sys-color-secondary)
var(--md-sys-color-surface)
var(--md-sys-color-error)

/* Typography */
var(--md-sys-typescale-headline-large-font-size)
var(--md-sys-typescale-body-medium-font-size)

/* Shape */
var(--md-sys-shape-corner-medium)  /* 12px */
var(--md-sys-shape-corner-large)   /* 16px */
var(--md-sys-shape-corner-full)    /* 999px */

/* Elevation */
var(--md-sys-elevation-1)  /* Subtle shadow */
var(--md-sys-elevation-3)  /* Medium shadow */
var(--md-sys-elevation-5)  /* Strong shadow */

/* Motion */
var(--md-sys-motion-duration-short4)    /* 200ms */
var(--md-sys-motion-easing-emphasized)  /* Bouncy curve */
```

### Responsive Breakpoints
```css
/* Mobile first */
@media (min-width: 640px)  { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
```

---

## Cart Operations

```typescript
// Add to cart
import { addToCart } from '../stores/cartStore';
addToCart(product, 'Periwinkle', ['Star', 'Snowflake']);

// Remove from cart
import { removeFromCart } from '../stores/cartStore';
removeFromCart(itemKey);

// Update quantity
import { updateQuantity } from '../stores/cartStore';
updateQuantity(itemKey, newQuantity);

// Clear cart
import { clearCart } from '../stores/cartStore';
clearCart();

// Open/close cart drawer
import { isCartOpen } from '../stores/cartStore';
isCartOpen.set(true);
```

---

## Product Utilities

```typescript
import { 
  getAllProducts,
  getProductById,
  getProductBySlug,
  getFeaturedProducts,
  getProductsByCategory,
  getCategories,
  getCategoryDisplayName,
  formatPrice
} from '../lib/products';

// Usage examples
const products = getAllProducts();
const featured = getFeaturedProducts(6);
const product = getProductBySlug('overlapping-pen-cup');
const organizers = getProductsByCategory('organizer');
const displayName = getCategoryDisplayName('cloth-pot'); // "Cloth Plant Pots"
const formatted = formatPrice(24); // "$24.00"
```

---

## Common Patterns

### Product Card Template
```astro
<div class="product-card">
  <img src={product.images[0]} alt={product.name} loading="lazy" />
  <h3>{product.name}</h3>
  <p>{formatPrice(product.price)}</p>
  <button onclick="addToCart(product)">Add to Cart</button>
</div>
```

### Error Handling Wrapper
```typescript
try {
  // Operation
} catch (e) {
  console.error('Error:', e);
  showToast('Operation failed', 'error');
}
```

### Toast Notification
```typescript
showToast('Item added to cart', 'success', 2000);
showToast('Failed to save', 'error', 3000);
showToast('Processing...', 'info', 1000);
```

---

## Mobile Testing Checklist

Quick validation before committing:

- [ ] Hamburger menu opens/closes
- [ ] Cart button visible and clickable
- [ ] Touch targets ≥ 44x44px
- [ ] Text readable (≥16px body)
- [ ] No horizontal scroll
- [ ] Images load correctly
- [ ] Forms work on mobile

---

## Deployment Checklist

Before pushing to production:

- [ ] All critical issues resolved
- [ ] Mobile testing passed
- [ ] No console errors
- [ ] Images optimized
- [ ] Meta tags complete
- [ ] 404 page exists
- [ ] Forms functional

---

## Troubleshooting

**Styles not applying?**
1. Check CSS specificity
2. Remove !important from global.css
3. Clear browser cache
4. Restart dev server

**Cart not persisting?**
1. Check localStorage quota
2. Verify try-catch wrapping
3. Check browser console for errors

**Images not loading?**
1. Verify path in products.json
2. Check file exists in /public/images/products/
3. Add onerror fallback

**Mobile menu broken?**
1. Check .nav-links.open class applies
2. Verify max-height transitions
3. Test JavaScript event handlers

---

**Tags:** #quick-reference #cheat-sheet #development

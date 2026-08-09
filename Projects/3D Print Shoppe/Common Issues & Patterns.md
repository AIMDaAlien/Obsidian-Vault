# Common Issues & Patterns

**Date:** November 8, 2025  
**Project:** [[README - Main Index|3D Print Shoppe]]  
**Related:** [[QA Process - Comprehensive Website Audit]], [[Subagent Workflow Guide]]

---

## CSS Conflicts

### Pattern: !important Overrides Breaking Components
**Symptoms:**
- Touch targets too small on mobile
- Button styles not applying
- Component-level overrides ignored

**Root Cause:**
```css
/* global.css */
.touch-target { min-height: 44px !important; }

/* Component CSS */
.custom-button { min-height: 48px; } /* LOSES to !important */
```

**Solution:**
- Remove all !important from global styles
- Use CSS specificity instead
- Apply !important only in component overrides if absolutely necessary

**Prevention:**
- `m3-style-designer` reviews all CSS changes
- No !important in global.css or m3-expressive.css
- Use BEM naming for higher specificity

---

## Hydration Mismatches

### Pattern: Data Loaded Server + Client
**Symptoms:**
- Console warnings about hydration mismatch
- Flickering content on page load
- Inconsistent state between renders

**Example (shop.astro):**
```astro
---
const products = getAllProducts(); // Server-side
---

<script>
  import { getAllProducts } from '../lib/products';
  const products = getAllProducts(); // Client-side DUPLICATE
</script>
```

**Solution:**
```astro
<div data-products={JSON.stringify(products)}>

<script>
  const el = document.getElementById('productGrid');
  const products = JSON.parse(el.dataset.products);
</script>
```

**Prevention:**
- Server renders data once
- Pass to client via data attributes
- Client consumes, never re-fetches at mount

---

## Missing Error Boundaries

### Pattern: Silent LocalStorage Failures
**Symptoms:**
- Cart doesn't save
- No user feedback on failures
- Console errors but app continues

**Vulnerable Operations:**
```typescript
// No error handling
localStorage.setItem('cart', JSON.stringify(cart));
```

**Solution:**
```typescript
try {
  localStorage.setItem('cart', JSON.stringify(cart));
} catch (e) {
  console.error('Failed to save cart:', e);
  showToast('Failed to save cart', 'error');
}
```

**Prevention:**
- Wrap all localStorage in try-catch
- Always show user feedback (toast)
- Log errors for debugging
- Provide fallback behavior

---

## Image Path Issues

### Pattern: Broken References in products.json
**Symptoms:**
- Product images show broken icon
- 404 errors in console
- Poor visual presentation

**Common Causes:**
1. Placeholder.jpg doesn't exist
2. Typo in image filename
3. Image in wrong directory
4. Case sensitivity (Placeholder.jpg vs placeholder.jpg)

**Solution:**
```astro
<!-- Image with fallback -->
<img 
  src={product.images[0]} 
  alt={product.name}
  onerror="this.src='/images/products/placeholder.jpg'"
/>
```

**Prevention:**
- Create placeholder.jpg before adding products
- Validate all image paths at build time
- Use ProductImage.astro component consistently
- Add build script to check image existence

---

## Category Display Issues

### Pattern: Unmapped Category Names
**Symptoms:**
- Shop filter shows "Functional" instead of "Functional Accessories"
- Inconsistent category naming
- Raw database values exposed to UI

**Example:**
```typescript
// Missing mappings
'functional' → falls back to 'Functional'
'gift' → falls back to 'Gift'
```

**Solution:**
```typescript
const displayNames: Record<string, string> = {
  'functional': 'Functional Accessories',
  'gift': 'Gifts & Decorative',
  // ... all categories mapped
};
```

**Prevention:**
- Maintain exhaustive category mapping
- Add build-time validation of categories
- Unit test getCategoryDisplayName()
- Document category options in schema

---

## Mobile Navigation Failures

### Pattern: CSS Specificity Conflicts
**Symptoms:**
- Hamburger menu doesn't open
- Cart button not clickable
- Touch targets too small

**Common Causes:**
```css
/* Global override prevents component styles */
button { min-height: 40px !important; }

/* Component tries to set 48px but loses */
.nav-button { min-height: 48px; }
```

**Solution:**
- Remove global !important rules
- Increase component specificity
- Use proper cascade order

**Mobile-Specific Fixes:**
```css
@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: flex; /* Not none */
    min-height: 48px;
    min-width: 48px;
  }
}
```

**Prevention:**
- Test mobile on every change
- Use responsive-qa-tester regularly
- Maintain minimum 44x44px touch targets
- Check z-index conflicts

---

## State Management Issues

### Pattern: No Design Selection for Multi-Design Products
**Symptoms:**
- Christmas ornaments can't select individual designs
- Cart doesn't store design choices
- No UI for design selection

**Root Cause:**
```typescript
// Cart item key doesn't include designs
const key = `${product.id}-${color}`;
// Multiple selections collapse into one item
```

**Solution:**
```typescript
// Include designs in unique key
const key = `${product.id}-${color}-${designs?.join(',')}`;

// Store designs in cart item
cartItem: {
  ...product,
  selectedDesigns: ['Star', 'Snowflake', 'Angel']
}
```

**Prevention:**
- Design cart schema for product variants
- Add design picker UI on product pages
- Test multi-variant products specifically
- Validate selectedDesigns in addToCart()

---

## Form Handling Without Backend

### Pattern: Forms with No Submit Handler
**Symptoms:**
- Contact form submits but nothing happens
- No user feedback
- Form data lost

**Temporary Solution (No Backend):**
```javascript
form.addEventListener('submit', (e) => {
  e.preventDefault();
  const data = new FormData(form);
  
  // Construct mailto link
  const mailto = `mailto:email@example.com?subject=${subject}&body=${body}`;
  window.location.href = mailto;
  
  showToast('Opening email client...', 'success');
});
```

**Production Solution:**
- Implement form submission API
- Use EmailJS or similar service
- Add server-side validation
- Send confirmation emails

**Prevention:**
- Plan backend integration early
- Use mailto as interim solution
- Document backend requirements
- Add to Phase 2 roadmap

---

## Missing Loading States

### Pattern: No User Feedback on Actions
**Symptoms:**
- User clicks button, nothing visible happens
- Uncertain if action succeeded
- Multiple clicks due to no feedback

**Example:**
```astro
<button onclick="addToCart()">Add to Cart</button>
<!-- No loading indicator, no success confirmation -->
```

**Solution:**
```astro
<button onclick="handleAddToCart()">
  <span class="button-text">Add to Cart</span>
  <span class="loading-spinner" hidden>⏳</span>
</button>

<script>
async function handleAddToCart() {
  showSpinner();
  await addToCart();
  showToast('Added to cart', 'success');
  hideSpinner();
}
</script>
```

**Prevention:**
- Add loading states for all async operations
- Show toast on success/failure
- Disable buttons during operations
- Use skeleton loaders for content

---

## Price Formatting Issues

### Pattern: Inconsistent Decimal Places
**Symptoms:**
- Some products show $24, others $24.00
- JSON has inconsistent formats
- Currency display varies

**Example (products.json):**
```json
{ "price": 24 },    // Integer
{ "price": 24.00 }, // Decimal
{ "price": 24.5 }   // Single decimal
```

**Solution:**
```typescript
export function formatPrice(price: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(price);
}
```

**Prevention:**
- Standardize price format in JSON (always .00)
- Use formatPrice() consistently
- Add price validation to build script
- Document price format in schema

---

## Reusable Solutions

### Toast Notification System
```typescript
function showToast(message: string, type: 'success' | 'error' | 'info', duration = 3000) {
  const toast = createToastElement(message, type);
  document.getElementById('toastContainer').append(toast);
  setTimeout(() => toast.remove(), duration);
}
```

### Image Error Handling Component
```astro
<img 
  src={src} 
  alt={alt}
  onerror="this.src='/images/products/placeholder.jpg'"
  loading="lazy"
/>
```

### LocalStorage Safe Wrapper
```typescript
function safeLocalStorage(key: string, value: any) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (e) {
    console.error(`Failed to save ${key}:`, e);
    showToast('Failed to save data', 'error');
    return false;
  }
}
```

---

**Tags:** #patterns #troubleshooting #best-practices #reusable-solutions

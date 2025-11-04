# Website Technical Specs

## Overview
**Domain:** aim3dprints.com (pending purchase)  
**Hosting:** Vercel (free tier)  
**Status:** Phase 1 - Week 1 build  
**Launch Target:** This week (urgency: 12 empty page visits)

---

## Tech Stack

### Core Framework
- **Next.js 14** (App Router)
- **TypeScript** (strict mode)
- **Tailwind CSS** (utility-first styling)
- **React 18**

### Component Library
- **shadcn/ui** (accessible, customizable)
  - Button, Card, Form, Input, Select
  - Dialog, Accordion, Tabs
  - Badge, Alert

### Forms & Validation
- **react-hook-form** (form state management)
- **Zod** (schema validation)
- **Formspree** (form backend, free tier: 50/month)

### Image Handling
- **Next.js Image** (automatic optimization)
- **Sharp** (image processing)

### Deployment
- **Vercel** (continuous deployment from Git)
- **GitHub** (version control)

### Analytics (Future)
- **Plausible** (privacy-focused, $9/month if needed)
- **Google Analytics** (free alternative)

---

## Site Architecture

```
/app
  /(root)
    /page.tsx              # Homepage
    /layout.tsx            # Root layout
  /shop
    /page.tsx              # Product grid
    /[slug]
      /page.tsx            # Product details
  /custom
    /page.tsx              # Custom order options
  /process
    /page.tsx              # How it works + FAQ
  /contact
    /page.tsx              # Contact form
  /terms
    /page.tsx              # Terms & privacy

/components
  /ui                      # shadcn components
  /ProductCard.tsx
  /ProductGrid.tsx
  /HeroSection.tsx
  /ProcessSteps.tsx
  /CustomOrderForm.tsx
  /ContactForm.tsx
  /FAQ.tsx
  /TestimonialCarousel.tsx
  /CategoryFilter.tsx
  /Header.tsx
  /Footer.tsx

/data
  /products.json           # Product catalog
  /testimonials.json       # Customer reviews (future)

/lib
  /utils.ts                # Helper functions
  /constants.ts            # Site constants

/public
  /images
    /products              # Product photos
    /hero                  # Hero images
    /icons                 # Site icons
  /favicon.ico
  /robots.txt
  /sitemap.xml

/styles
  /globals.css             # Global styles (minimal)
```

---

## Brand Design System

### Color Palette
```typescript
// tailwind.config.ts
colors: {
  periwinkle: {
    DEFAULT: '#6366F1',
    50: '#EBEEFF',
    100: '#D6DCFF',
    500: '#6366F1',
    600: '#4F46E5',
    700: '#4338CA',
  },
  lavender: {
    DEFAULT: '#A78BFA',
    50: '#F5F3FF',
    100: '#EDE9FE',
    500: '#A78BFA',
    600: '#9333EA',
  },
  'accent-green': {
    DEFAULT: '#10B981',
    50: '#ECFDF5',
    500: '#10B981',
    600: '#059669',
  }
}
```

### Typography
```typescript
fontFamily: {
  sans: ['Inter', 'system-ui', 'sans-serif'],
  display: ['Poppins', 'Inter', 'sans-serif'],
}

fontSize: {
  'xs': '0.75rem',      // 12px
  'sm': '0.875rem',     // 14px
  'base': '1rem',       // 16px
  'lg': '1.125rem',     // 18px
  'xl': '1.25rem',      // 20px
  '2xl': '1.5rem',      // 24px
  '3xl': '1.875rem',    // 30px
  '4xl': '2.25rem',     // 36px
  '5xl': '3rem',        // 48px
}
```

### Spacing & Sizing
```css
Border radius: rounded-xl (12px) default
Shadows: shadow-lg for hover states
Transitions: transition-all duration-200
Touch targets: min-h-[44px] min-w-[44px]
```

---

## Page Specifications

### Homepage (`/`)
**Purpose:** Convert visitors, showcase products, build trust

**Sections:**
1. **Hero** (above-fold)
   - H1: "Custom 3D Prints Made by Your Neighbor"
   - Subhead: "Eco-friendly • Local Pickup • 3-5 Days"
   - CTA buttons: [Shop Catalog] [Custom Order]
   - Background: Best print photo
   - Trust badge: "Serving [Neighborhood] Since 2025"

2. **Featured Products** (6 items)
   - Grid: 3 columns desktop, 2 tablet, 1 mobile
   - ProductCard component
   - "Shop All" CTA

3. **How It Works** (5 steps)
   - Visual timeline
   - Icons + brief descriptions
   - "Learn More" link to /process

4. **Social Proof** (future)
   - "40+ Neighbors Served" stat
   - Testimonial carousel (3 reviews)

5. **CTA Section**
   - Secondary conversion opportunity
   - "Ready to Print?" headline
   - Dual CTAs

### Shop Page (`/shop`)
**Purpose:** Browse and filter catalog

**Features:**
- Product grid (20+ items)
- Filters:
  - Availability (In Stock / Made-to-Order)
  - Price range (sliders)
  - Category (Planter, Organizer, Decor, Gift, Functional)
- Sort:
  - Popular
  - Price: Low to High
  - Price: High to Low
  - Newest
- Pagination (12 items per page)

**State Management:**
```typescript
const [filters, setFilters] = useState({
  availability: 'all',
  priceRange: [0, 100],
  category: 'all',
  sort: 'popular'
});
```

### Product Detail (`/shop/[slug]`)
**Purpose:** Convert browsers to buyers

**Layout:**
- Image gallery (3-5 photos, zoom on click)
- Product info:
  - Name, price, availability badge
  - Description (3-4 sentences)
  - Specs: dimensions, print time, colors available
  - "Add to Cart" or "Request Quote" CTA
- Creator attribution (if CC-BY license)
- Related products (3 similar items)

### Custom Orders (`/custom`)
**Purpose:** Capture custom requests

**Three Options:**
1. **Upload STL File**
   - File upload (max 10MB)
   - Size/color preferences
   - Quote form

2. **Find Design for Me**
   - Description textarea
   - Reference images (optional)
   - Budget range

3. **Photo to 3D**
   - Info about limitations
   - Photo upload
   - Expectation management

**Form Action:** Formspree endpoint #2

### Process Page (`/process`)
**Purpose:** Set expectations, answer questions

**Sections:**
1. Timeline (5 steps with icons)
2. Pricing guide table
3. FAQ accordion (10-15 questions)
4. Payment policy
5. Pickup/delivery info

### Contact Page (`/contact`)
**Purpose:** General inquiries

**Simple form:**
- Name, Email, Phone, Message
- Auto-response confirmation
- Response time: "Within 24 hours"

---

## Data Structure

### Product Schema
```typescript
interface Product {
  id: string;                    // Unique slug
  name: string;
  description: string;
  price: number;
  priceRange?: {                 // For size variants
    small?: number;
    medium?: number;
    large?: number;
  };
  category: 'planter' | 'organizer' | 'decor' | 'gift' | 'functional';
  availability: 'in-stock' | 'made-to-order';
  printTime: number;             // Hours
  images: string[];              // Array of image paths
  colors: string[];              // Available color options
  dimensions: string;
  weight?: number;               // Grams
  license: 'CC0' | 'CC-BY' | 'CC-BY-SA' | 'CC-BY-ND' | 'Free Commercial';
  creator?: string;              // If attribution required
  makerWorldLink: string;
  featured?: boolean;            // Show on homepage
  stock?: number;                // If in-stock item
}
```

### Example Product
```json
{
  "id": "stringy-art-christmas-ornaments",
  "name": "Stringy Art Christmas Ornaments",
  "description": "Elegant bridge-printed ornament set. 13 unique designs available. Perfect for holiday decor or gifts.",
  "price": 30,
  "priceRange": {
    "small": 30,
    "large": 50
  },
  "category": "gift",
  "availability": "in-stock",
  "printTime": 8,
  "images": [
    "/images/products/ornaments-1.jpg",
    "/images/products/ornaments-2.jpg"
  ],
  "colors": ["white", "red", "green", "gold", "silver"],
  "dimensions": "Various (3-5 inches each)",
  "license": "CC0",
  "makerWorldLink": "https://makerworld.com/en/models/826969",
  "featured": true,
  "stock": 3
}
```

---

## Form Specifications

### Formspree Setup
**Account:** amasudtech@gmail.com  
**Plan:** Free tier (50 submissions/month)

**Form 1: Contact**
- **Endpoint:** `https://formspree.io/f/FORM_ID_1`
- **Fields:** name, email, phone (optional), message
- **Honeypot:** `_gotcha` field (hidden)
- **Success:** "Thanks! We'll respond within 24 hours."

**Form 2: Custom Orders**
- **Endpoint:** `https://formspree.io/f/FORM_ID_2`
- **Fields:** name, email, phone, orderType (radio), fileUpload (conditional), linkOrDescription, size, colorPreference, quantity, deadline, budgetRange
- **File limit:** 10MB
- **Success:** "Quote request received! We'll respond within 24 hours with pricing."

### Validation Rules
```typescript
const contactSchema = z.object({
  name: z.string().min(2, "Name required"),
  email: z.string().email("Valid email required"),
  phone: z.string().optional(),
  message: z.string().min(10, "Please provide details"),
});

const customOrderSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  phone: z.string().optional(),
  orderType: z.enum(['stl', 'find', 'photo']),
  file: z.any().optional(),
  description: z.string().min(10),
  size: z.string().optional(),
  colorPreference: z.string(),
  quantity: z.number().min(1).max(100),
  deadline: z.string().optional(),
  budgetRange: z.enum(['15-25', '25-40', '40-60', '60+']),
});
```

---

## SEO & Metadata

### Global Meta Tags
```typescript
// app/layout.tsx
export const metadata = {
  title: "Aim's 3D Print Shoppe | Custom 3D Printing [Neighborhood]",
  description: "Local 3D printing for custom decor, organizers, and gifts. Eco-friendly PLA, 3-5 day turnaround. Order online or pickup locally.",
  keywords: "3D printing, custom prints, local printing, eco-friendly, [neighborhood], gifts, organizers",
  openGraph: {
    title: "Aim's 3D Print Shoppe",
    description: "Custom 3D Prints Made by Your Neighbor",
    images: ['/images/og-image.jpg'],
  }
}
```

### Dynamic Page Titles
```typescript
// Product pages
title: `${product.name} | Aim's 3D Print Shoppe`

// Shop page
title: "Shop 3D Prints | Organizers, Decor & Gifts"
```

---

## Performance Targets

### Lighthouse Scores (Goals)
- Performance: >90
- Accessibility: >95
- Best Practices: >95
- SEO: >95

### Core Web Vitals
- LCP (Largest Contentful Paint): <2.5s
- FID (First Input Delay): <100ms
- CLS (Cumulative Layout Shift): <0.1

### Optimization Strategies
- Next.js Image component (automatic optimization)
- Lazy loading below-the-fold content
- Code splitting by route
- Compress images (WebP format)
- Minimize third-party scripts

---

## Deployment Workflow

### Git Workflow
```bash
main (production) ← Protected branch
  └── dev (staging) ← Development branch
```

### Vercel Integration
1. Push to `dev` → Preview deployment
2. Test preview URL
3. Merge to `main` → Production deployment
4. Automatic HTTPS, CDN, edge caching

### Environment Variables
```env
NEXT_PUBLIC_FORMSPREE_CONTACT=f/{form_id_1}
NEXT_PUBLIC_FORMSPREE_CUSTOM=f/{form_id_2}
NEXT_PUBLIC_SITE_URL=https://aim3dprints.com
```

---

## Security Considerations

### Form Protection
- Honeypot fields (bot detection)
- Rate limiting via Formspree
- CSRF tokens (Formspree handles)
- Input sanitization (Zod validation)

### Payment Security
- No credit card data stored
- PayPal handles all transactions
- Display payment policy clearly
- SSL/TLS via Vercel

### Privacy
- No cookies initially
- Minimal tracking (Plausible if added)
- Privacy policy page
- GDPR considerations (if EU traffic)

---

## Accessibility Standards

### WCAG 2.1 AA Compliance
- Color contrast ratio >4.5:1
- Keyboard navigation support
- ARIA labels on interactive elements
- Alt text for all images
- Focus indicators visible
- Semantic HTML structure

### Testing Tools
- Lighthouse (Chrome DevTools)
- axe DevTools (browser extension)
- WAVE (web accessibility evaluation)

---

## Future Enhancements (Phase 2+)

### Month 2-3
- [ ] Payment integration (PayPal buttons)
- [ ] Shopping cart functionality
- [ ] Email newsletter signup
- [ ] Blog/news section
- [ ] Customer testimonials page

### Month 4-6
- [ ] Order tracking system
- [ ] Customer accounts (optional)
- [ ] Inventory management dashboard
- [ ] Analytics dashboard
- [ ] Automated email notifications

### Long-term
- [ ] Stripe integration (when viable)
- [ ] 3D model preview (Three.js viewer)
- [ ] AR preview (try before you buy)
- [ ] Affiliate program
- [ ] Wholesale portal

---

## Development Checklist

### Pre-Launch
- [ ] All pages built and responsive
- [ ] Forms tested and working
- [ ] Products added to JSON (8 minimum)
- [ ] Images optimized and uploaded
- [ ] SEO metadata complete
- [ ] Privacy/terms pages written
- [ ] Lighthouse score >90
- [ ] Cross-browser testing (Chrome, Safari, Firefox)
- [ ] Mobile testing (iOS, Android)
- [ ] Domain connected and SSL active

### Launch Day
- [ ] Deploy to production
- [ ] Update Nextdoor bio with link
- [ ] Test all links and forms
- [ ] Monitor error logs
- [ ] Announce on Nextdoor

### Post-Launch
- [ ] Monitor analytics
- [ ] Respond to form submissions <24hrs
- [ ] Fix any reported bugs
- [ ] Collect user feedback
- [ ] Iterate based on data

---

*See also: [[Project - Current State]], [[Business Plan Overview]], [[Design System Reference]]*

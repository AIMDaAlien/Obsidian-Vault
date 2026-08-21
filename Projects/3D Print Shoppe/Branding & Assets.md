---
tags: [payments, branding, marketing, checklist]
---
# Branding & Assets

**Last Updated:** 2024-11-23  
**Related:** [[Project - Current State]], [[Custom Order System]], [[Payment Workflow]]

---

## Brand Identity

**Business Name:** 3D Print Shoppe  
**Tagline:** *(To be defined)*  
**Target Audience:** Local customers in [local area]/[metro area], hobbyists, gift-buyers

---

## Color Palette

### Primary Colors

The brand uses a **Material Design 3** color system with a periwinkle/lavender aesthetic.

#### 1. Periwinkle (Primary)

**Hex:** `#6366f1`  
**RGB:** `99, 102, 241`  
**Usage:**
- Primary action buttons
- Navigation active states
- Links and interactive elements
- Brand accent color

**Container color:** `#e4e5ff` (light backgrounds)  
**On-primary:** `#ffffff` (white text on primary)

---

#### 2. Lavender (Secondary)

**Hex:** `#a78bfa`  
**RGB:** `167, 139, 250`  
**Usage:**
- Secondary action buttons
- Hover states
- Complementary accents
- Modal highlights

**Container color:** `#f3efff` (light backgrounds)  
**On-secondary:** `#ffffff` (white text on secondary)

---

#### 3. Green (Tertiary/Success)

**Hex:** `#10b981`  
**RGB:** `16, 185, 129`  
**Usage:**
- Success messages
- Confirmation states
- "Available" indicators
- Positive feedback

**Container color:** `#d1fae5` (light backgrounds)  
**On-tertiary:** `#ffffff` (white text on tertiary)

---

### Supporting Colors

#### Surface Colors

- **Surface:** `#fdfcff` (main background)
- **Surface Container:** `#f1ecf4` (card backgrounds)
- **Surface Variant:** `#f5f3ff` (subtle alternates)

#### Text Colors

- **On Surface:** `#1c1b1f` (primary text)
- **On Surface Variant:** `#49454f` (secondary text)

#### Outlines

- **Outline:** `#79747e` (borders, dividers)
- **Outline Variant:** `#c4c6d0` (subtle borders)

#### Error States

- **Error:** `#ba1a1a`
- **Error Container:** `#ffdad6`

---

## Logo

### Current Implementation

**File location:** `/public/logo.png`  
**Component:** `src/components/Navigation.astro`

**Logo structure:**
```astro
<a href="/" class="logo-link">
  <div class="logo">
    <img src="/logo.png" alt="3D Print Shoppe Logo" class="logo-image" />
    <span class="logo-text">3D Print Shoppe</span>
  </div>
</a>
```

**Dimensions:**
- Height: 40px
- Width: Auto (maintains aspect ratio)
- Format: PNG (supports transparency)

**Responsive behavior:**
- Desktop: Logo + text
- Mobile: Logo + truncated text (if needed)

**Interactive states:**
- Hover: `transform: scale(1.05)` (subtle zoom)
- Transition: `var(--md-sys-motion-duration-spring-quick)` with bouncy easing

---

## Favicon

**File location:** `/public/favicon.png`  
**Format:** PNG (recommend 512x512px for best quality)  
**Usage:** Browser tab icon, bookmark icon, mobile home screen

**Note:** Consider creating multiple sizes for different platforms:
- `favicon.ico` (16x16, 32x32, 48x48)
- `favicon-192.png` (Android)
- `favicon-512.png` (iOS)
- `apple-touch-icon.png` (180x180)

---

## Typography

### Font Family

**Primary:** Roboto Flex (variable font)  
**Fallbacks:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif`

**Variable definition:**
```css
--md-sys-font-family: 'Roboto Flex', -apple-system, BlinkMacSystemFont, 
                      'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
```

### Type Scale (Age-Friendly Sizing)

**Display:**
- Large: 56px (`3.5rem`)
- Medium: 45px (`2.8125rem`)
- Small: 36px (`2.25rem`)

**Headline:**
- Large: 32px (`2rem`)
- Medium: 28px (`1.75rem`)
- Small: 24px (`1.5rem`)

**Title:**
- Large: 22px (`1.375rem`)
- Medium: 16px (`1rem`)
- Small: 14px (`0.875rem`)

**Body:**
- Large: **18px** (`1.125rem`) ⭐ **Optimized for readability**
- Medium: 16px (`1rem`)
- Small: 14px (`0.875rem`)

**Label:**
- Large/Medium/Small: 14px (`0.875rem`)

**Rationale for larger body text:**
- Target demographic includes older adults
- Improves readability on mobile devices
- Reduces eye strain for extended reading

---

## Material Design 3 Tokens

### Shape Tokens

**Border radius values:**
- None: `0`
- Extra Small: `4px`
- Small: `8px`
- Medium: `12px`
- Large: `16px`
- Extra Large: `28px`
- Full: `9999px` (pill shape)

**Usage:**
- Buttons: `corner-full` (pill shape)
- Cards: `corner-large` (16px)
- Input fields: `corner-medium` (12px)
- Chips/tags: `corner-full` (pill shape)

---

### Elevation (Shadows)

**Level 1:** Subtle lift (cards, inputs)
```css
0 1px 2px 0 rgba(0, 0, 0, 0.3), 
0 1px 3px 1px rgba(0, 0, 0, 0.15)
```

**Level 2:** Moderate elevation (navigation bar)
```css
0 1px 2px 0 rgba(0, 0, 0, 0.3), 
0 2px 6px 2px rgba(0, 0, 0, 0.15)
```

**Level 3:** Prominent (modals, hover states)
```css
0 4px 8px 3px rgba(0, 0, 0, 0.15), 
0 1px 3px 0 rgba(0, 0, 0, 0.3)
```

**Level 4:** High elevation (dropdowns)
```css
0 6px 10px 4px rgba(0, 0, 0, 0.15), 
0 2px 3px 0 rgba(0, 0, 0, 0.3)
```

**Level 5:** Maximum elevation (notifications)
```css
0 8px 12px 6px rgba(0, 0, 0, 0.15), 
0 4px 4px 0 rgba(0, 0, 0, 0.3)
```

---

### State Layers (Interaction Opacity)

**Hover:** 8% opacity (`0.08`)  
**Focus:** 12% opacity (`0.12`)  
**Pressed:** 12% opacity (`0.12`)  
**Dragged:** 16% opacity (`0.16`)

**Implementation example:**
```css
.button::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--md-sys-color-on-primary);
  opacity: 0;
  transition: opacity 200ms;
}

.button:hover::before {
  opacity: var(--md-sys-state-hover-opacity);
}
```

---

## Motion Design

### Easing Curves

**Standard:** Default transitions (`--md-sys-motion-easing-standard`)  
**Emphasized:** Attention-grabbing (`--md-sys-motion-easing-emphasized`)  
**Spring Bouncy:** Playful interactions (`--md-sys-motion-easing-spring-bouncy`)  
**Spring Smooth:** Elegant transitions (`--md-sys-motion-easing-spring-smooth`)

### Duration Tokens

- **Short 2:** Quick feedback (100-200ms)
- **Short 4:** Standard transitions (200-300ms)
- **Medium 3:** Modal animations (300-400ms)
- **Spring Quick:** Bouncy effects (300ms)

**Example:**
```css
transition: all var(--md-sys-motion-duration-short4) 
            var(--md-sys-motion-easing-emphasized);
```

---

## Dark Mode Support

The theme includes full dark mode support with adjusted colors for better visibility:

### Dark Mode Palette

**Primary:** `#c5c7ff` (lighter periwinkle)  
**Secondary:** `#d1bbff` (lighter lavender)  
**Tertiary:** `#6ee7b7` (lighter green)

**Surface:** `#1c1b1f` (dark background)  
**On Surface:** `#e6e1e5` (light text)

**Note:** Dark mode can be toggled via HTML class:
```html
<html class="dark">
```
Or data attribute:
```html
<html data-theme="dark">
```

---

## Asset Checklist

### Required Assets

- [x] Logo PNG (`/public/logo.png`)
- [x] Favicon PNG (`/public/favicon.png`)
- [ ] Venmo QR code (`/public/images/venmo-qr.png`)
- [ ] CashApp QR code (`/public/images/cashapp-qr.png`)
- [ ] Social media preview image (Open Graph)
- [ ] Apple touch icon (180x180)
- [ ] Multiple favicon sizes

### Recommended Additions

- [ ] Business card design
- [ ] Email signature template
- [ ] Packaging/sticker design
- [ ] Social media profile images
- [ ] Nextdoor listing image

---

## Brand Voice & Tone

**To be defined - Initial thoughts:**
- Approachable and friendly (small business, local)
- Professional but not corporate
- Enthusiastic about 3D printing
- Educational (helps customers understand the process)
- Patient (answers questions thoroughly)

---

## Competitor Analysis Notes

*(Space for noting what other 3D print shops in the area are doing well/poorly with their branding)*

---

**Tags:** #branding #design-system #material-design #colors #typography #assets
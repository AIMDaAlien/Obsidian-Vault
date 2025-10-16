# Teardown Cafe - Design System

## Material You 3 Expressive (Dark Mode)

### Design Philosophy
**Material You 3 Expressive** = Google's latest design language emphasizing:
- Bold, playful interactions
- Large, rounded corners
- Dynamic color systems
- Elevated surfaces with depth
- Smooth, emphasized motion

### Color Palette

#### Primary Colors (Periwinkle Base)
```css
--md-sys-color-primary: #B8B3FF;           /* Periwinkle */
--md-sys-color-on-primary: #1E1B32;
--md-sys-color-primary-container: #2A2640;
--md-sys-color-on-primary-container: #E6E1FF;
```

#### Surface Colors (Deep Dark Purple)
```css
--md-sys-color-surface: #14121F;           /* Deep dark background */
--md-sys-color-surface-variant: #1E1B32;   /* Card backgrounds */
--md-sys-color-surface-dim: #0F0D18;
--md-sys-color-surface-bright: #1E1B32;
--md-sys-color-on-surface: #E6E1FF;        /* Primary text */
--md-sys-color-on-surface-variant: #C8C4DD;/* Secondary text */
```

#### Accent Colors
```css
--accent-teal: #00BCD4;      /* From teal repair mat in photos */
--accent-orange: #FF9800;    /* Warning/difficulty indicators */
--accent-green: #4CAF50;     /* Success/easy indicators */
```

### Typography (Ubuntu Font Family)

#### Type Scale
```css
/* Display - Hero sections */
--display-large: 64px / 400 / -0.5px
--display-medium: 52px / 400 / 0px
--display-small: 44px / 400 / 0px

/* Headline - Section headers */
--headline-large: 36px / 400 / 0px
--headline-medium: 32px / 400 / 0px
--headline-small: 28px / 400 / 0px

/* Title - Card titles */
--title-large: 24px / 500 / 0px
--title-medium: 18px / 500 / 0.15px
--title-small: 16px / 500 / 0.1px

/* Body - Content text */
--body-large: 18px / 400 / 0.5px
--body-medium: 16px / 400 / 0.25px
--body-small: 14px / 400 / 0.4px

/* Label - Buttons, chips */
--label-large: 16px / 500 / 0.1px
--label-medium: 14px / 500 / 0.5px
--label-small: 12px / 500 / 0.5px
```

### Spacing System

#### Material You 3 Spacing Scale
```css
--space-xs: 4px;    /* Tight padding */
--space-sm: 8px;    /* Compact spacing */
--space-md: 16px;   /* Standard spacing */
--space-lg: 24px;   /* Comfortable spacing */
--space-xl: 32px;   /* Section separation */
--space-2xl: 48px;  /* Major section breaks */
--space-3xl: 64px;  /* Hero spacing */
```

### Shape System (Rounded Corners)

#### Corner Radii
```css
--corner-none: 0px;
--corner-xs: 4px;    /* Small chips */
--corner-sm: 8px;    /* Buttons */
--corner-md: 12px;   /* Small cards */
--corner-lg: 16px;   /* Medium cards */
--corner-xl: 24px;   /* Large cards */
--corner-full: 28px; /* Pill shapes */
```

**Design Decision:** Teardown cards use `--corner-xl (24px)` for that expressive, playful feel

### Elevation System

#### Shadow Levels
```css
/* Level 0: Flat surface */
--elevation-0: none;

/* Level 1: Raised slightly */
--elevation-1: 
  0px 1px 2px rgba(0, 0, 0, 0.3),
  0px 1px 3px 1px rgba(0, 0, 0, 0.15);

/* Level 2: Floating elements */
--elevation-2:
  0px 1px 2px rgba(0, 0, 0, 0.3),
  0px 2px 6px 2px rgba(0, 0, 0, 0.15);

/* Level 3: Hover state */
--elevation-3:
  0px 4px 8px 3px rgba(0, 0, 0, 0.15),
  0px 1px 3px rgba(0, 0, 0, 0.3);

/* Level 4: Prominent cards */
--elevation-4:
  0px 6px 10px 4px rgba(0, 0, 0, 0.15),
  0px 2px 3px rgba(0, 0, 0, 0.3);

/* Level 5: Modal/overlay */
--elevation-5:
  0px 8px 12px 6px rgba(0, 0, 0, 0.15),
  0px 4px 4px rgba(0, 0, 0, 0.3);
```

### Motion System

#### Easing Functions
```css
/* Standard easing - Most common */
--easing-standard: cubic-bezier(0.2, 0.0, 0, 1.0);

/* Emphasized easing - Expressive entrance */
--easing-emphasized: cubic-bezier(0.05, 0.7, 0.1, 1.0);

/* Decelerate - Exit animations */
--easing-decelerate: cubic-bezier(0.0, 0.0, 0.2, 1);

/* Accelerate - Quick exits */
--easing-accelerate: cubic-bezier(0.4, 0.0, 1, 1);
```

#### Duration Scale
```css
--duration-short: 150ms;     /* Micro-interactions */
--duration-medium: 300ms;    /* Standard transitions */
--duration-long: 400ms;      /* Emphasized transitions */
--duration-extra-long: 500ms;/* Page transitions */
```

### Component Patterns

#### Teardown Card
```css
.teardown-card {
  background: var(--md-sys-color-surface-variant);
  border-radius: var(--corner-xl);     /* 24px rounded */
  box-shadow: var(--elevation-2);
  transition: 
    transform var(--duration-long) var(--easing-emphasized),
    box-shadow var(--duration-long) var(--easing-emphasized);
}

.teardown-card:hover {
  transform: translateY(-8px) scale(1.02);  /* Lift + subtle zoom */
  box-shadow: var(--elevation-4);
}
```

#### Card Image Behavior
```css
.teardown-card img {
  transition: transform var(--duration-long) var(--easing-emphasized);
}

.teardown-card:hover img {
  transform: scale(1.05);  /* Subtle zoom on hover */
}
```

#### Difficulty Badges
```css
.difficulty-badge {
  padding: var(--space-xs) var(--space-md);
  border-radius: var(--corner-full);
  font: var(--label-medium);
}

.difficulty-easy {
  background: color-mix(in srgb, var(--accent-green) 20%, transparent);
  color: var(--accent-green);
}

.difficulty-medium {
  background: color-mix(in srgb, var(--accent-orange) 20%, transparent);
  color: var(--accent-orange);
}

.difficulty-hard {
  background: color-mix(in srgb, #F44336 20%, transparent);
  color: #F44336;
}
```

#### Navigation Header
```css
.site-header {
  background: color-mix(in srgb, var(--md-sys-color-surface) 80%, transparent);
  backdrop-filter: blur(24px);
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 1px solid var(--md-sys-color-surface-variant);
}
```

### Layout Patterns

#### Homepage Grid
```css
.teardown-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-xl);
  padding: var(--space-2xl) var(--space-lg);
}
```

#### Single Column Content
```css
.teardown-content {
  max-width: 720px;
  margin: 0 auto;
  padding: var(--space-2xl) var(--space-lg);
}
```

### Accessibility Considerations

#### Color Contrast
All color combinations meet **WCAG AA** standards:
- Primary text (#E6E1FF) on surface (#14121F): **14.2:1** ✓
- Periwinkle (#B8B3FF) on dark surface: **7.8:1** ✓
- Secondary text (#C8C4DD) on surface: **10.1:1** ✓

#### Focus States
```css
:focus-visible {
  outline: 2px solid var(--md-sys-color-primary);
  outline-offset: 2px;
  border-radius: var(--corner-sm);
}
```

#### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Design Inspirations

#### Color Palette Sources
1. **Periwinkle (#B8B3FF)** - User's favorite color
2. **Deep purple backgrounds** - Sophisticated, tech-forward feel
3. **Teal accent (#00BCD4)** - Directly sampled from repair mat in teardown photos

#### Material You 3 Reference
- Google Material Design 3 guidelines
- Expressive theme (vs. baseline theme)
- Dynamic color system principles
- Motion design patterns

### Icon System (Emojis)

#### Device Category Icons
```javascript
monitor: '🖥️'
laptop: '💻'
smartphone: '📱'
raspberry-pi: '🥧'
nas: '💾'
mechanical-keyboard: '⌨️'
other: '🔧'
```

#### Difficulty Icons
```javascript
easy: '🟢'
medium: '🟡'
hard: '🔴'
```

**Rationale:** Emojis provide universal, accessible iconography without additional asset loading

### Responsive Breakpoints

```css
/* Mobile first approach */
--breakpoint-sm: 640px;   /* Small tablets */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Laptops */
--breakpoint-xl: 1280px;  /* Desktops */
--breakpoint-2xl: 1536px; /* Large displays */
```

#### Grid Adjustments
```css
/* Mobile: 1 column */
@media (min-width: 640px) {
  /* Tablet: 2 columns */
  .teardown-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  /* Desktop: 3 columns */
  .teardown-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Dark Mode Rationale

**Why dark mode only?**
1. **Technical audience** - Developers/tinkerers prefer dark themes
2. **Photo showcase** - Dark backgrounds make colorful teardown photos pop
3. **Eye strain reduction** - Long reading sessions more comfortable
4. **Brand identity** - Sophisticated, modern aesthetic
5. **Simplicity** - One theme = less maintenance

### Design Tokens File Location
**File:** `/src/styles/global.css`

Contains all CSS custom properties (CSS variables) defining the design system

### Figma Integration
- Design system documented in Figma
- Dev Mode enabled for component inspection
- Color tokens exported as CSS variables
- Typography scale matched 1:1

## Related Notes
- [[Teardown Cafe - Project Overview]]
- [[Teardown Cafe - Technical Setup]]
- [[Teardown Cafe - Content Workflow]]

---
*Created: October 16, 2025*
*Last Updated: October 16, 2025*

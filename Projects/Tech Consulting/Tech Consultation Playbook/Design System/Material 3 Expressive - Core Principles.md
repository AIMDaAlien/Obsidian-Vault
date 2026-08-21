---
tags: [checklist]
---
# Material 3 Expressive - Core Principles

#design-system #m3-expressive #reference

## Overview
M3 Expressive is Google's 2025 evolution backed by 46 studies with 18K+ participants. **Key finding: users spot UI elements 4x faster** in expressive designs.

## Five Pillars

### 1. Shape System
- **10-step corner radius**: 4dp → 56dp → full (9999px)
- **35 new shapes** beyond circles/rectangles
- **Asymmetric corners**: Mix radii (e.g., `32px 32px 12px 32px`)
- **Shape morphing**: Animate between shapes on interaction

```css
.button {
  border-radius: 24px;
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.button:hover {
  border-radius: 32px;
  transform: scale(1.08);
}
```

### 2. Size Hierarchy
- **Massive scale differences** = instant visual priority
- Hero headings: 6xl → 9xl (96px-128px)
- Buttons: py-6 to py-8 (min 48px touch target)
- Containers: p-12 to p-16

### 3. Motion & Spring Physics
- **No linear easing** - always spring curves
- Standard: `cubic-bezier(0.34, 1.56, 0.64, 1)`
- Duration: 300-700ms
- Natural bounce/overshoot

### 4. Heavy Containment
- **Everything in visible containers**
- Border widths: 3-4px (not 1px)
- Clear grouping with pills/cards
- Layered shadows for depth

```jsx
// Primary: border-4 rounded-[48px] p-12 shadow-2xl
// Secondary: border-3 rounded-[32px] p-8 shadow-xl  
// Tertiary: border-2 rounded-[24px] p-6 shadow-lg
```

### 5. Color System (Material You)
- Dynamic color tokens adapt to theme
- Primary/Secondary/Tertiary roles
- Surface-variant for hierarchy
- Outline tokens for borders

```javascript
const colors = {
  light: {
    primary: 'bg-purple-600',
    surface: 'bg-white',
    outline: 'border-purple-200'
  },
  dark: {
    primary: 'bg-purple-500',
    surface: 'bg-gray-900',
    outline: 'border-gray-700'
  }
};
```

## Key Components

### Floating Navigation
- Edge-hugging pill design
- Backdrop blur transparency
- Scales on scroll
- `rounded-full` with generous padding

### Shape Morphing Buttons
- Transform radius on hover (24px → 32px → 48px)
- Scale changes (1.0 → 1.08)
- Spring physics for natural feel
- Active state: `scale-95`

### Loading Indicators
- Shape-morphing animations (not spinners)
- Wave/pulse patterns
- Multiple shape transitions

## Research Findings
✅ 4x faster key action recognition  
✅ 22% higher task completion  
✅ Better accessibility across ages  
✅ "Playful, energetic, friendly" beats "clean, boring"

## Common Mistakes
❌ Linear easing instead of spring physics  
❌ Border-radius < 16px  
❌ 1px borders (use 3-4px)  
❌ Touch targets < 44px  
❌ Only symmetrical corners  
❌ No shape morphing on interaction

## Implementation Checklist
- [ ] All buttons use spring physics easing
- [ ] Corner radii follow 10-step scale
- [ ] Borders are 3-4px minimum
- [ ] Touch targets are 48px+ height
- [ ] Primary CTAs use shape morphing
- [ ] Containers have visible borders/shadows
- [ ] Dark mode uses proper token system
- [ ] Asymmetric corners on featured elements

---
Created: 2025-11-08  
Tags: #m3-expressive #design-tokens #reference

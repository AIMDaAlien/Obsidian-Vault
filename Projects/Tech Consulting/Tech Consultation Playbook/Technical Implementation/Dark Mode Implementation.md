---
tags: [checklist]
---
# Dark Mode Implementation - Material You Approach

#technical #dark-mode #tokens

## Token-Based System

Material You uses **design tokens** - the single source of truth for colors across themes.

```javascript
const colors = {
  light: {
    bg: 'from-purple-50 via-blue-50 to-lavender-50',
    surface: 'bg-white',
    surfaceVariant: 'bg-purple-50',
    primary: 'bg-purple-600',
    primaryHover: 'bg-purple-700',
    secondary: 'bg-blue-500',
    tertiary: 'bg-indigo-500',
    onSurface: 'text-gray-900',
    onSurfaceVariant: 'text-gray-600',
    outline: 'border-purple-200',
    outlineVariant: 'border-purple-100',
    shadow: 'shadow-purple-500/20',
    glow: 'shadow-purple-500/50'
  },
  dark: {
    bg: 'from-gray-950 via-purple-950/20 to-blue-950/20',
    surface: 'bg-gray-900',
    surfaceVariant: 'bg-gray-800',
    primary: 'bg-purple-500',
    primaryHover: 'bg-purple-400',
    secondary: 'bg-blue-400',
    tertiary: 'bg-indigo-400',
    onSurface: 'text-gray-50',
    onSurfaceVariant: 'text-gray-300',
    outline: 'border-gray-700',
    outlineVariant: 'border-gray-800',
    shadow: 'shadow-purple-500/30',
    glow: 'shadow-purple-400/60'
  }
};
```

## React Implementation

```jsx
const [isDark, setIsDark] = useState(false);
const theme = isDark ? colors.dark : colors.light;

// Apply throughout component
<div className={`${theme.surface} ${theme.onSurface}`}>
  <button className={`${theme.primary} hover:${theme.primaryHover}`}>
    Click me
  </button>
</div>
```

## Toggle Component

```jsx
<button
  onClick={() => setIsDark(!isDark)}
  className={`${theme.surfaceVariant} p-3 rounded-2xl 
              hover:scale-110 active:scale-95 
              transition-all duration-300`}
>
  {isDark ? <Sun className="w-5 h-5 text-yellow-400" /> 
          : <Moon className="w-5 h-5 text-purple-600" />}
</button>
```

## Persistence

```jsx
// Load from localStorage
useEffect(() => {
  const saved = localStorage.getItem('darkMode');
  if (saved !== null) setIsDark(JSON.parse(saved));
}, []);

// Save on change
useEffect(() => {
  localStorage.setItem('darkMode', JSON.stringify(isDark));
  document.documentElement.classList.toggle('dark', isDark);
}, [isDark]);
```

## Color Contrast Rules

**WCAG 2.1 AA Requirements:**
- Normal text: 4.5:1 minimum
- Large text (18pt+): 3:1 minimum
- UI components: 3:1 minimum

**Light Mode:**
- Primary: purple-600 on white = 4.58:1 ✅
- Text: gray-900 on white = 19.56:1 ✅

**Dark Mode:**
- Primary: purple-500 on gray-900 = 4.12:1 ✅
- Text: gray-50 on gray-900 = 17.23:1 ✅

## Testing Checklist

- [ ] All text meets contrast requirements
- [ ] Interactive elements visible in both modes
- [ ] Shadows/glows adjusted for visibility
- [ ] Border colors distinct from backgrounds
- [ ] Gradient backgrounds transition smoothly
- [ ] Icons legible in both themes
- [ ] Form inputs clearly distinguishable
- [ ] Focus states visible

## Common Pitfalls

❌ Hardcoded colors instead of tokens  
❌ Forgetting to adjust shadows in dark mode  
❌ Using black (#000) as dark background (use gray-950)  
❌ Not testing border visibility  
❌ Insufficient contrast on hover states

## Recommendation

Use **token-based system** for consultation sites - provides better control over brand colors and easier theme expansion.

---
Created: 2025-11-08  
Tags: #dark-mode #accessibility #design-tokens

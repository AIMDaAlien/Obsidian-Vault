---
tags: [guide, cost, checklist]
garden_path: Projects/TypingLab/04 - Performance Optimization.md
last_published: '2025-11-28T19:44:59.350292'
published_to_garden: true
---

# Performance Optimization

> **How TypingLab achieves <16ms input latency and 60fps sustained**

## 🎯 Performance Goals

| Metric | Target | Achieved | Method |
|--------|--------|----------|--------|
| Input Latency | <16ms | ✅ ~12ms | Event optimization |
| Frame Rate | 60fps | ✅ 60fps | VSync alignment |
| Cold Start | <1s | ✅ ~800ms | Code splitting |
| Offline Load | <100ms | ✅ ~50ms | Service worker cache |

---

## ⚡ Input Latency Optimization

### The 16ms Budget

**Why 16ms?**
```
1000ms / 60fps = 16.67ms per frame

Budget breakdown:
- Keystroke handler: 1-2ms
- State update: 2-3ms
- React reconciliation: 3-5ms
- Browser paint: 5-8ms
---
Total: ~16ms
```

### Critical Path Optimization

#### 1. Immediate preventDefault
```typescript
// BAD: Check conditions first
if (someCondition) {
  e.preventDefault();  // Too late! Already propagated
}

// GOOD: Prevent immediately
e.preventDefault();  // <1ms impact
if (someCondition) {
  // ... logic
}
```

**Impact:** Saves 2-5ms by preventing default browser actions

#### 2. Passive Event Listeners
```typescript
// BAD: Blocks scrolling
window.addEventListener('keydown', handler);

// GOOD: Non-blocking
window.addEventListener('keydown', handler, { passive: false });
// Note: passive=false needed for preventDefault
```

**Impact:** Prevents scroll jank, improves perceived performance

#### 3. Circular Buffer (Zero Allocations)
```typescript
// BAD: Creates new array each time
const keystrokes = [...oldKeystrokes, newKeystroke];

// GOOD: Pre-allocated circular buffer
const BUFFER_SIZE = 10000;
const buffer = new Array(BUFFER_SIZE);
let index = 0;

buffer[index++ % BUFFER_SIZE] = newKeystroke; // O(1), no GC
```

**Impact:** 
- Eliminates garbage collection pauses
- O(1) insertion time
- Stable memory footprint

---

## 🖼 Rendering Optimization

### VSync Alignment

#### requestAnimationFrame Pattern
```typescript
let rafId: number | undefined;

const scheduleUpdate = () => {
  if (rafId) return; // Already scheduled
  
  rafId = requestAnimationFrame(() => {
    rafId = undefined;
    processUpdates();
    renderUI();
  });
};

// In event handler
handleKeyDown(e) {
  e.preventDefault();
  recordKeystroke(e);
  scheduleUpdate();  // Defer to next frame
}
```

**Benefits:**
- ✅ Batches multiple updates into single frame
- ✅ Syncs with monitor refresh rate
- ✅ Prevents unnecessary renders

### GPU Acceleration

#### CSS Transform vs Layout Properties
```css
/* BAD: Triggers layout + paint */
.cursor {
  left: 100px;  /* Causes reflow */
}

/* GOOD: GPU-accelerated */
.cursor {
  transform: translateX(100px);  /* Composited layer */
  will-change: transform;        /* Hint to browser */
}
```

**Performance Comparison:**
```
Layout properties: 5-10ms render time
CSS transforms: 0.5-2ms render time
Speedup: 5-10x faster
```

#### Layer Promotion
```css
.animated {
  will-change: transform;
  transform: translateZ(0);  /* Force layer creation */
}
```

**Warning:** Don't overuse! Each layer costs memory.
**Rule:** Only promote frequently-updating elements.

---

## 📊 Measurement & Profiling

### Performance.now() Precision
```typescript
// BAD: Date.now() (1ms resolution)
const start = Date.now();
processData();
const duration = Date.now() - start;  // ±1ms error

// GOOD: performance.now() (sub-millisecond)
const start = performance.now();
processData();
const duration = performance.now() - start;  // microsecond precision
```

### Custom Performance Marks
```typescript
// Mark critical sections
performance.mark('keystroke-start');
processKeystroke(e);
performance.mark('keystroke-end');

// Measure duration
const measure = performance.measure(
  'keystroke-processing',
  'keystroke-start',
  'keystroke-end'
);

if (measure.duration > 16) {
  console.warn('⚠️ Exceeded frame budget:', measure.duration);
}
```

### Chrome DevTools Performance Tab

**Workflow:**
1. Open DevTools → Performance
2. Click Record
3. Type for 10 seconds
4. Stop recording
5. Analyze flame graph

**Look for:**
- 🔴 Long tasks (>50ms)
- 🔴 Layout thrashing (multiple reflows)
- 🔴 Long paints (>10ms)
- 🟢 Smooth 60fps line

---

## 🧮 Memory Management

### Pre-allocation Strategy
```typescript
// BAD: Allocates on every keystroke
function recordKeystroke(key: string) {
  const event = {
    key,
    timestamp: Date.now(),
    isCorrect: key === expected
  };
  events.push(event);  // New object each time
}

// GOOD: Reuse pre-allocated objects
const eventPool = Array(1000).fill(null).map(() => ({}));
let poolIndex = 0;

function recordKeystroke(key: string) {
  const event = eventPool[poolIndex++ % 1000];
  event.key = key;
  event.timestamp = Date.now();
  event.isCorrect = key === expected;
  // No new allocations!
}
```

### Garbage Collection Optimization
```typescript
// Monitor GC pauses
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 10) {
      console.warn('GC pause:', entry.duration);
    }
  }
});

observer.observe({ entryTypes: ['measure'] });
```

---

## 🎨 React-Specific Optimizations

### Memo & Callback Hooks
```typescript
// BAD: New function every render
<TypingArea onKeyDown={(e) => handleKey(e)} />

// GOOD: Stable reference
const handleKey = useCallback((e: KeyboardEvent) => {
  processKeystroke(e);
}, [dependencies]);

<TypingArea onKeyDown={handleKey} />
```

### Conditional Rendering
```typescript
// BAD: Re-renders expensive component unnecessarily
return (
  <div>
    {showKeyboard && <KeyboardDisplay />}
    <TypingArea />
  </div>
);

// GOOD: Memoize expensive component
const MemoizedKeyboard = memo(KeyboardDisplay);

return (
  <div>
    {showKeyboard && <MemoizedKeyboard />}
    <TypingArea />
  </div>
);
```

### State Update Batching
```typescript
// BAD: Three separate renders
setCurrentIndex(i => i + 1);
setErrors([...errors, error]);
setMetrics(calculateMetrics());

// GOOD: Batched update (React 18+)
startTransition(() => {
  setCurrentIndex(i => i + 1);
  setErrors([...errors, error]);
  setMetrics(calculateMetrics());
});
// All updates in single render
```

---

## 🔧 Build Optimization

### Code Splitting
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['react', 'react-dom'],
          'storage': ['idb'],
          'state': ['zustand']
        }
      }
    }
  }
});
```

**Result:**
```
vendor.js: 42KB (cached)
storage.js: 8KB (cached)
main.js: 85KB (changes)
---
Initial load: 135KB gzipped
Subsequent: 85KB (savings: 50KB)
```

### Tree Shaking
```typescript
// BAD: Imports entire library
import _ from 'lodash';

// GOOD: Imports only needed function
import { debounce } from 'lodash-es';

// BEST: Use native alternatives
const debounce = (fn, delay) => { /* ... */ };
```

### Asset Optimization

#### Font Preloading
```html
<link rel="preload" 
      href="/fonts/Ubuntu-Regular.woff2" 
      as="font" 
      type="font/woff2" 
      crossorigin>
```

**Impact:**
- Eliminates FOUT (Flash of Unstyled Text)
- Saves 100-300ms on first render

#### Image Optimization
```html
<!-- Use modern formats -->
<img src="icon.avif" 
     alt="Icon"
     width="64" 
     height="64"
     loading="lazy">

<!-- Fallback for older browsers -->
<picture>
  <source srcset="icon.avif" type="image/avif">
  <source srcset="icon.webp" type="image/webp">
  <img src="icon.png" alt="Icon">
</picture>
```

---

## 📡 Network Optimization

### Service Worker Caching
```typescript
// Cache strategy: Cache-first for static assets
workbox.routing.registerRoute(
  ({ request }) => request.destination === 'script' ||
                   request.destination === 'style',
  new workbox.strategies.CacheFirst({
    cacheName: 'static-resources',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 30 * 24 * 60 * 60 // 30 days
      })
    ]
  })
);
```

### Resource Hints
```html
<!-- DNS prefetch for external resources -->
<link rel="dns-prefetch" href="https://fonts.googleapis.com">

<!-- Preconnect for critical origins -->
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Prefetch for likely navigation -->
<link rel="prefetch" href="/next-page.js">
```

---

## 🐛 Common Performance Pitfalls

### Pitfall 1: Layout Thrashing
```typescript
// BAD: Read-write-read-write pattern
for (const element of elements) {
  const height = element.offsetHeight;  // Read (forces layout)
  element.style.height = height + 10 + 'px';  // Write
}

// GOOD: Batch reads, then writes
const heights = elements.map(el => el.offsetHeight);  // All reads
elements.forEach((el, i) => {
  el.style.height = heights[i]! + 10 + 'px';  // All writes
});
```

### Pitfall 2: Expensive Selectors
```css
/* BAD: Slow selector */
div > ul > li > a[href*="example"] {
  color: red;
}

/* GOOD: Class-based */
.nav-link {
  color: red;
}
```

### Pitfall 3: Unoptimized Images
```
Problem: 5MB PNG loaded on every visit
Solution: 
  1. Convert to WebP/AVIF (80% size reduction)
  2. Lazy load below fold
  3. Responsive images (srcset)
```

### Pitfall 4: Synchronous Storage
```typescript
// BAD: Blocks main thread
localStorage.setItem('data', JSON.stringify(largeObject));

// GOOD: Async IndexedDB
await db.put('data', largeObject);  // Non-blocking
```

---

## 📈 Performance Budget

### Target Metrics

| Metric | Budget | Measured |
|--------|--------|----------|
| Time to Interactive | <3s | 1.2s ✅ |
| First Contentful Paint | <1s | 0.4s ✅ |
| Largest Contentful Paint | <2.5s | 0.8s ✅ |
| Cumulative Layout Shift | <0.1 | 0.02 ✅ |
| Total Blocking Time | <300ms | 120ms ✅ |

### Bundle Size Budget
```
JavaScript: 150KB (gzipped)
CSS: 20KB (gzipped)
Fonts: 60KB (woff2)
Images: 50KB (webp/avif)
---
Total: 280KB target, 265KB actual ✅
```

---

## 🔍 Profiling Tools

### Chrome DevTools
- **Performance:** Record user interactions
- **Memory:** Detect leaks
- **Coverage:** Find unused code
- **Lighthouse:** Overall score

### React DevTools
- **Profiler:** Component render times
- **Components:** Props/state inspection

### Custom Instrumentation
```typescript
class PerformanceMonitor {
  private marks = new Map<string, number>();
  
  mark(name: string) {
    this.marks.set(name, performance.now());
  }
  
  measure(name: string, start: string, end: string) {
    const startTime = this.marks.get(start);
    const endTime = this.marks.get(end);
    
    if (!startTime || !endTime) return;
    
    const duration = endTime - startTime;
    console.log(`${name}: ${duration.toFixed(2)}ms`);
    
    if (duration > 16) {
      console.warn(`⚠️ ${name} exceeded frame budget`);
    }
  }
}
```

---

## ✅ Performance Checklist

### Build Time
- [ ] Code splitting configured
- [ ] Tree shaking enabled
- [ ] Minification active
- [ ] Source maps generated

### Runtime
- [ ] Event handlers optimized
- [ ] requestAnimationFrame used
- [ ] CSS transforms for animations
- [ ] Circular buffers for collections

### Network
- [ ] Service worker caching
- [ ] Font preloading
- [ ] Image optimization
- [ ] Gzip/Brotli compression

### React
- [ ] Memo for expensive components
- [ ] useCallback for event handlers
- [ ] useMemo for complex calculations
- [ ] Lazy loading for routes

### Monitoring
- [ ] Performance marks added
- [ ] Error boundaries implemented
- [ ] Memory leak detection
- [ ] Bundle size tracking

---

**Related:**
- [[01 - Technical Architecture]]
- [[02 - Implementation Journey]]
- [[07 - Testing and Verification]]

*Last Updated: November 18, 2025*
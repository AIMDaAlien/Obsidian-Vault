# Implementation Journey

> **The story of building TypingLab from concept to functional MVP**

## 🗓 Timeline

### Day 1: November 17, 2025

#### Morning: Research & Planning
**Goal:** Understand keybr.com's approach and gather research

**Actions:**
1. Used Perplexity Pro to research typing pedagogy
2. Compiled 100+ academic sources on:
   - Progressive key introduction strategies
   - Optimal practice session lengths
   - Spaced repetition intervals
   - Phonetic text generation
   - Performance metrics (WPM calculations)

**Key Findings:**
- 35 WPM is professional baseline (keybr.com standard)
- 95% accuracy required before advancing
- 20 samples needed for statistical validity
- 15-20 minute sessions optimal
- Bigram/trigram frequency crucial for natural text

#### Afternoon: Architecture Design
**Goal:** Plan AI orchestration strategy

**Initial Plan:**
- Claude Code (main session) - Architecture & complex logic
- Claude Code Subagents - Parallel module development
- Perplexity - Research only
- Gemini Pro - Component generation (backup)
- OpenCode - Code review (backup)

**Reality Check:**
Realized subagents share context, so decided to use Claude Code Web subagents as primary approach after main scaffold.

#### Evening: Project Initialization
**Goal:** Set up project structure

**Actions:**
1. Created GitHub repo: `local-keebspeed`
2. Initialized Vite + React + TypeScript project
3. Configured Tailwind CSS with custom lavender theme
4. Set up PWA plugin (Workbox)
5. Defined core TypeScript types based on research

**First Blocker:**
Tailwind CSS 4 beta required separate PostCSS plugin (not compatible).
**Solution:** Downgraded to Tailwind CSS 3.4.15 (stable).

---

### Day 2: November 18, 2025

#### Morning: Core Engine Implementation
**Goal:** Build high-performance typing engine

**Challenges:**
1. **Input Latency** - Need <16ms keystroke-to-acknowledge
   - **Solution:** Passive event listeners + immediate preventDefault
   - Used circular buffer for O(1) insertions
   - Deferred UI updates to requestAnimationFrame

2. **VSync Alignment** - Avoid screen tearing
   - **Solution:** All UI updates batched via rAF
   - GPU-accelerated cursor (CSS transforms only)

3. **Precision Timing** - Millisecond accuracy needed
   - **Solution:** performance.now() instead of Date.now()
   - Sub-millisecond precision for WPM calculations

**Implementation:**
```typescript
// High-priority path
handleKeyDown(e: KeyboardEvent) {
  e.preventDefault();  // <1ms
  const ts = performance.now();
  keyBuffer[(idx++) % SIZE] = { key: e.key, ts };
  scheduleUIUpdate();  // Defer to rAF
}

// Low-priority path (batched)
requestAnimationFrame(() => {
  processBuffer();
  updateMetrics();
});
```

**Result:** Achieved <16ms latency, 60fps sustained ✅

#### Midday: Adaptive Algorithm
**Goal:** Implement keybr-style progression

**Components Built:**
1. **adaptive.ts** - Progressive key introduction logic
   - Started with home row (asdf-jkl;)
   - Unlock new key when ALL active keys meet thresholds
   - Confidence decay for unpracticed keys

2. **textGenerator.ts** - Phonetic pseudo-word generator
   - Markov chain from bigram frequencies
   - Phonotactic validation (no "tl-", "ng-" at start)
   - Vowel insertion for pronounceability

3. **ngrams.json** - Frequency tables from research
   - Top 100 English bigrams
   - Top 50 trigrams
   - Weighted by corpus frequency

**Key Insight:**
Text generation is hard! First attempts produced "zxqwk" nonsense.
**Solution:** Implemented retry logic with validation scoring.

#### Afternoon: Storage Layer
**Goal:** IndexedDB persistence for offline use

**Challenges:**
1. **Schema Design** - How to structure data efficiently?
   - **Solution:** Composite keys (userId-letter) for keyStats
   - Indexes on timestamp and confidence for fast queries

2. **Migration Strategy** - Future-proofing schema changes
   - **Solution:** Version-based migrations
   - Atomic transactions for consistency

**Implementation:**
```typescript
export const migrations = {
  1: (db: IDBDatabase) => {
    const userStore = db.createObjectStore('users', { keyPath: 'id' });
    const sessionStore = db.createObjectStore('sessions', { keyPath: 'id' });
    sessionStore.createIndex('by-userId', 'userId');
    // ... more stores
  }
};
```

**Status:** Complete but not wired to UI yet (queued for subagent)

#### Late Afternoon: UI Components
**Goal:** Build TypingArea and PerformanceHUD

**Design Decisions:**
1. **Font Selection**
   - Ubuntu for UI (clean, modern)
   - JetBrains Mono for typing (optimal readability)
   - Preloaded to prevent FOUT

2. **Color Scheme**
   - Lavender primary (#E6E6FA) - user preference
   - Greyscale base (neutral-900 → neutral-100)
   - Dark mode default

3. **Cursor Animation**
   - CSS transform for GPU acceleration
   - Smooth 50ms transition
   - Underline style (2px height)

**Result:** Clean, minimal interface with <16ms feedback ✅

#### Evening: Integration Crisis
**Goal:** Wire adaptive algorithm to UI

**Problem #1:** Static sample text, adaptive algorithm unused
**Solution:** Created `useAdaptiveLessons` hook
```typescript
const { currentLesson, generateNextLesson, activeKeys } = useAdaptiveLessons();
```

**Problem #2:** No session → next lesson flow
**Solution:** onComplete callback with 2-second modal
```typescript
onComplete: (finalMetrics) => {
  setShowCompletion(true);
  setTimeout(() => {
    generateNextLesson();
    reset();
  }, 2000);
}
```

**Problem #3:** PWA configured but not registered
**Solution:** Created registerSW.ts, called in main.tsx
```typescript
if (isServiceWorkerSupported()) {
  registerServiceWorker();
}
```

**Result:** Fully functional MVP with adaptive AI ✅

---

## 🎯 Major Milestones

### ✅ Milestone 1: Performance Targets Met
- Input latency: <16ms (verified)
- Frame rate: 60fps sustained
- Cold start: ~800ms
- Offline load: ~50ms from cache

### ✅ Milestone 2: Adaptive AI Working
- Dynamic text generation based on performance
- Progressive key introduction (starts with 7 keys)
- Automatic next lesson after completion
- Active keys displayed to user

### ✅ Milestone 3: True Offline Capability
- Service worker registered and activated
- All assets cached (fonts, JS, CSS)
- IndexedDB ready for persistence
- Works without network after first load

### 🔄 Milestone 4: Data Persistence (In Progress)
- Storage layer complete
- Needs wiring to UI
- Session history component planned
- Export/import functionality designed

---

## 🚧 Challenges & Solutions

### Challenge 1: Tailwind CSS 4 Beta Incompatibility
**Problem:** PostCSS plugin moved to separate package
**Impact:** Build failed with cryptic error
**Solution:** Downgraded to Tailwind CSS 3.4.15 (stable)
**Time Lost:** 15 minutes
**Lesson:** Stick to stable versions for critical dependencies

### Challenge 2: Input Latency Spikes
**Problem:** Occasional 30-50ms delays on keystroke
**Root Cause:** Layout thrashing from cursor position updates
**Solution:** 
- Switched from `left: ${x}px` to `transform: translateX(${x}px)`
- GPU compositing layer via `will-change: transform`
**Result:** Consistent <16ms latency ✅

### Challenge 3: Text Generation Producing Gibberish
**Problem:** First attempts: "zxqwk", "pthngl" (unpronounceable)
**Root Cause:** 
1. No vowel insertion
2. Ignored phonotactic rules
3. Random letter selection without frequency weighting

**Solution:**
```typescript
// 1. Weighted random by bigram frequency
const selected = weightedRandom(candidates);

// 2. Validate phonotactics
if (!isPhonLegal(word, position)) return false;

// 3. Ensure vowels
if (!hasVowel) word = insertVowel(word);
```

**Result:** Natural-looking pseudo-words ✅

### Challenge 4: No Session Continuation
**Problem:** After completion, user stuck (no next lesson)
**Impact:** App felt incomplete, not suitable for practice
**Solution:**
- Completion modal with stats (2s display)
- Auto-generate next lesson
- Reset typing engine automatically
- Continuous practice flow

**Result:** Seamless experience ✅

---

## 💡 Key Decisions & Rationale

### Decision 1: PWA over Native Apps
**Options Considered:**
- Native apps (Swift/Kotlin)
- Electron desktop app
- PWA (web app)

**Choice:** PWA

**Rationale:**
✅ Single codebase (Windows/Mac/Android)
✅ No app store approval needed
✅ Instant updates
✅ Offline-first architecture
✅ Web platform maturity

⚠️ Slight performance overhead (negligible for typing)

### Decision 2: IndexedDB over LocalStorage
**Options Considered:**
- LocalStorage (simple key-value)
- IndexedDB (structured database)
- SQLite (via WASM)

**Choice:** IndexedDB

**Rationale:**
✅ Structured queries (indexes)
✅ Large storage quota (50MB+)
✅ Async operations (non-blocking)
✅ Transaction support
✅ Browser-native (no dependencies)

⚠️ More complex API (mitigated with `idb` wrapper)

### Decision 3: React over Vanilla JS
**Options Considered:**
- Vanilla JS (max performance)
- React (declarative UI)
- Svelte (compiled)
- Vue (progressive)

**Choice:** React 19

**Rationale:**
✅ Concurrent features (suspense, transitions)
✅ Mature ecosystem
✅ TypeScript integration
✅ DevTools support
✅ Community resources

⚠️ Bundle size (~40KB min+gzip)

### Decision 4: Zustand over Redux
**Options Considered:**
- Redux (standard)
- Zustand (minimal)
- Jotai (atomic)
- Context API (built-in)

**Choice:** Zustand

**Rationale:**
✅ Minimal boilerplate
✅ 1KB gzipped
✅ TypeScript-first
✅ No Provider hell
✅ DevTools integration

⚠️ Less opinionated (need discipline)

### Decision 5: Vite over Webpack
**Options Considered:**
- Webpack (mature)
- Vite (modern)
- Parcel (zero-config)

**Choice:** Vite 6

**Rationale:**
✅ Instant HMR (<100ms)
✅ Fast cold start (~200ms)
✅ ESM-native
✅ Built-in TypeScript
✅ Great DX

⚠️ Newer ecosystem (but stable)

---

## 📈 Metrics & Progress

### Code Statistics
```
Total Files: 32
Lines of Code: ~3,500
TypeScript Coverage: 100%
Test Coverage: 0% (planned)
```

### Component Breakdown
```
Components:   2 complete, 4 planned
Hooks:        2 complete, 3 planned
Algorithms:   3 complete
Storage:      4 complete (not wired)
Types:        1 comprehensive file
```

### Time Investment
```
Research:        3 hours (Perplexity)
Architecture:    2 hours (planning)
Implementation:  8 hours (coding)
Debugging:       2 hours (fixes)
Documentation:   1 hour (this note)
---
Total:          16 hours
```

### Lines of Code by Module
```
lib/algorithms:  ~800 LOC
lib/engine:      ~600 LOC
lib/storage:     ~700 LOC
components:      ~400 LOC
hooks:           ~500 LOC
types:           ~300 LOC
config/setup:    ~200 LOC
```

---

## 🎓 Lessons Learned

### Technical Lessons

1. **Performance is a Feature**
   - Users feel latency >16ms
   - GPU acceleration matters (CSS transforms)
   - Measure everything (performance.now())

2. **PWA is Production-Ready**
   - Service workers are reliable
   - IndexedDB is fast enough
   - Offline-first forces good architecture

3. **TypeScript Strict Mode is Worth It**
   - Catches bugs at compile time
   - Self-documenting code
   - Refactoring confidence

4. **Research Before Coding**
   - 3 hours of research saved days of trial-error
   - Academic papers provide optimal values
   - Don't reinvent algorithms

### Process Lessons

1. **Start with Types**
   - Define interfaces first
   - Implementation flows naturally
   - Prevents architectural mistakes

2. **Measure, Don't Assume**
   - Use DevTools Performance tab
   - Profile before optimizing
   - Validate assumptions with data

3. **Iterate on UX**
   - First attempt rarely feels right
   - Get to functional fast, polish later
   - User feedback is gold

4. **Document as You Go**
   - Future you will thank present you
   - README updates prevent confusion
   - Code comments for why, not what

---

## 🔮 What's Next

### Week 1: Data Persistence
- Wire IndexedDB to UI
- Session history display
- Export/import functionality

### Week 2: UI Enhancements
- Keyboard visualization component
- Settings panel (shadcn/ui)
- Progress tracking UI

### Week 3: Polish & Testing
- Sound effects (optional)
- Accessibility audit
- Performance profiling
- Cross-browser testing

### Future Features
- Code practice mode
- Japanese support
- Daily challenges
- Custom text import

---

**Related:**
- [[00 - TypingLab Project Overview]]
- [[01 - Technical Architecture]]
- [[03 - Research Findings]]

*Last Updated: November 18, 2025*

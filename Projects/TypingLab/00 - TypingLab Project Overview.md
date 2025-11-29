---
garden_path: Projects/TypingLab/00 - TypingLab Project Overview.md
last_published: '2025-11-28T19:44:25.536276'
published_to_garden: true
---

# TypingLab Project Overview

> **Privacy-focused offline typing speed trainer with adaptive AI**

## 🎯 Project Goal

Build a local-first typing trainer that works offline on Windows, Mac, and Android - replicating keybr.com's adaptive algorithm but with complete privacy and offline capability.

## 📅 Timeline

- **Started:** November 17-18, 2025
- **Current Phase:** MVP Complete (Functional)
- **Next Phase:** Subagent Integration (Storage, UI enhancements)

## 🏆 Core Achievements

### Completed Features ✅
- **Adaptive AI Engine** - Lessons adjust to user performance in real-time
- **High-Performance Typing Engine** - <16ms input latency, 60fps sustained
- **True Offline Capability** - PWA with service worker, IndexedDB storage
- **Dynamic Text Generation** - Phonetically-valid pseudo-words
- **Session Flow** - Auto-generates next lesson after completion
- **Research-Backed Design** - Based on 100+ academic sources

### In Progress 🔄
- Storage persistence (IndexedDB wiring to UI)
- Keyboard visualization component
- Settings panel with shadcn/ui
- Progress tracking and history charts

## 🎨 Design Philosophy

### Privacy-First
- **Zero telemetry** - Nothing sent to servers
- **Local storage only** - IndexedDB + LocalStorage
- **Offline-capable** - Works without internet after first load
- **Data ownership** - Export/import your data as JSON

### Performance-Focused
- **Sub-millisecond precision** - performance.now() timestamps
- **VSync-aligned rendering** - requestAnimationFrame for UI updates
- **GPU acceleration** - CSS transforms only, no layout thrashing
- **Zero dropped inputs** - Handles 200+ WPM sustained

### User Experience
- **Adaptive difficulty** - Focuses on your weakest keys
- **Progressive learning** - Starts simple (home row), unlocks gradually
- **Immediate feedback** - Real-time WPM, accuracy, error tracking
- **Continuous flow** - Auto-generates next lesson

## 🛠 Tech Stack

### Core Technologies
- **React 19.0.0** - Latest stable with concurrent features
- **TypeScript 5.7.2** - Strict mode for type safety
- **Vite 6.0.1** - Fast build tool with HMR
- **Tailwind CSS 3.4.15** - Utility-first styling

### Data & Storage
- **IndexedDB** (via idb 8.0.1) - Local database
- **Zustand 5.0.2** - Lightweight state management
- **Service Workers** - PWA offline capability

### UI Components (Planned)
- **shadcn/ui** - Accessible, customizable components
- **Radix UI** - Headless component primitives
- **Lucide Icons** - Modern icon set

## 🎨 Design System

### Typography
- **UI Font:** Ubuntu (clean, modern sans-serif)
- **Code Font:** JetBrains Mono (optimal for typing practice)

### Color Palette
```css
Primary:   #E6E6FA  /* Lavender */
Accent:    #C8A2C8  /* Muted lavender */
Base:      #171717  /* Near-black background */
Text:      #F5F5F5  /* Off-white */
```

### Theme
- **Dark mode** primary (default)
- Light mode planned for future

## 📊 Success Metrics

### Performance Benchmarks
| Metric | Target | Achieved |
|--------|--------|----------|
| Input Latency | <16ms | ✅ <16ms |
| Frame Rate | 60fps | ✅ 60fps sustained |
| Cold Start | <1s | ✅ ~800ms |
| Offline Load | <100ms | ✅ ~50ms |

### User Progression
- **Start:** 8 keys (home row: asdf-jkl;)
- **Unlock threshold:** 35 WPM + 95% accuracy + 20 samples per key
- **Target:** All 26 letters mastered at 35+ WPM

## 🧠 Key Innovations

### 1. Adaptive Algorithm
Unlike static typing tutors, TypingLab dynamically adjusts:
- **Weighted text generation** - 70% weak keys, 30% reinforcement
- **Progressive key introduction** - Unlock when ready, not on schedule
- **Confidence decay** - Keys unpracticed lose confidence over time
- **Fatigue detection** - Suggests breaks when performance drops

### 2. Phonetic Text Generation
Pseudo-words that feel natural to type:
- **Bigram/trigram chains** - Markov-style generation from English corpus
- **Phonotactic validation** - No impossible combinations (tl-, ng- at start)
- **Vowel insertion** - Ensures pronounceability
- **Validation retry** - Generates multiple attempts, picks best

### 3. Performance Optimization
Every design decision optimized for speed:
- **Event handler priority** - Keystroke capture on main thread (no workers)
- **Batched UI updates** - One render per frame via rAF
- **Pre-allocated buffers** - Circular buffer for keystroke history
- **CSS transforms only** - No layout-triggering properties

## 📁 Repository Structure

```
local-keebspeed/
├── src/
│   ├── components/      # React UI components
│   ├── hooks/           # Custom hooks
│   ├── lib/
│   │   ├── algorithms/  # Adaptive AI logic
│   │   ├── engine/      # Typing engine
│   │   └── storage/     # IndexedDB layer
│   ├── types/           # TypeScript definitions
│   └── data/            # Static data (n-grams, rules)
├── public/              # Static assets
└── docs/                # Documentation
```

## 🎓 Learning Resources

### Research Foundation
- **100+ academic sources** compiled via Perplexity Pro
- **Typing pedagogy** - Progressive key introduction strategies
- **Spaced repetition** - Optimal practice intervals
- **Phonotactics** - English phonetic constraints
- **Performance metrics** - Industry-standard WPM calculations

### Key Research Findings
1. **Optimal session length:** 15-20 minutes
2. **Unlock threshold:** 35 WPM is professional baseline
3. **Accuracy requirement:** 95% minimum for mastery
4. **Sample size:** 20 attempts needed for statistical validity
5. **Confidence formula:** Normalized (WPM - 12) / (35 - 12)

## 🚀 Next Steps

### Immediate (Week 1)
1. Wire IndexedDB storage to UI
2. Implement session history display
3. Build keyboard visualization component

### Short-term (Week 2)
4. Settings panel with shadcn/ui
5. Progress tracking UI
6. Per-key confidence indicators

### Future Enhancements
- Code practice mode (programming symbols)
- Japanese support (romaji → hiragana)
- Custom text import
- Daily challenges
- Sound effects (optional)

## 📚 Documentation Index

- [[01 - Technical Architecture]]
- [[02 - Implementation Journey]]
- [[03 - Research Findings]]
- [[04 - Performance Optimization]]
- [[05 - Adaptive Algorithm Deep Dive]]
- [[06 - Subagent Implementation Guide]]
- [[07 - Testing and Verification]]

## 🤝 Contributing

This is a solo project documenting the journey of building a production-quality typing trainer from scratch using modern web technologies and AI orchestration patterns.

**Philosophy:** Privacy-first, performance-obsessed, research-backed.

---

*Last Updated: November 18, 2025*
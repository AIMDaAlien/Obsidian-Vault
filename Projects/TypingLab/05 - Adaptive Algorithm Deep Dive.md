# Adaptive Algorithm Deep Dive

> **How TypingLab's AI-powered lesson generation works**

## 🧠 Algorithm Overview

The adaptive algorithm is the "brain" of TypingLab. It determines:
1. **Which keys** to practice (focus on weak spots)
2. **When to unlock** new keys (progressive difficulty)
3. **What text** to generate (phonetically-valid pseudo-words)
4. **How to weight** practice (70% weak, 30% reinforcement)

---

## 📊 Core Data Structure

### KeyStats Interface
```typescript
interface KeyStats {
  letter: string;           // The key (e.g., 'a')
  attempts: number;         // Total practice count
  errors: number;           // Mistakes made
  totalTime: number;        // Cumulative milliseconds
  meanTime: number;         // Average response time
  stdDevTime: number;       // Consistency measure
  lastPracticed: Date;      // Last session date
  introduced: Date;         // When unlocked
  confidence: number;       // 0-1 scale (readiness)
  wpm: number;              // Key-specific WPM
  accuracy: number;         // 0-1 scale
}
```

**Example:**
```json
{
  "letter": "a",
  "attempts": 247,
  "errors": 12,
  "totalTime": 48320,
  "meanTime": 195.5,
  "confidence": 0.92,
  "wpm": 42,
  "accuracy": 0.951
}
```

---

## 🎯 Progressive Key Introduction

### Phase 1: Initialize (Home Row)
```typescript
const getInitialKeys = (): string[] => {
  // Start with home row (most comfortable)
  return ['a', 's', 'd', 'f', 'j', 'k', 'l'];
};
```

**Why home row?**
- ✅ Natural finger positions
- ✅ Covers 35% of English text
- ✅ Builds muscle memory foundation
- ✅ Low cognitive load

### Phase 2: Check Readiness
```typescript
const shouldUnlockNextKey = (activeKeys: KeyStats[]): boolean => {
  // ALL keys must meet thresholds
  for (const key of activeKeys) {
    if (key.wpm < 35) return false;           // Speed check
    if (key.accuracy < 0.95) return false;     // Accuracy check
    if (key.attempts < 20) return false;       // Sample size check
    if (key.confidence < 1.0) return false;    // Confidence check
  }
  return true;  // All keys ready!
};
```

**Unlock Logic:**
```
Check ALL active keys:
  ├─ Key 'a': 42 WPM, 96% acc, 25 samples → ✅ Ready
  ├─ Key 's': 38 WPM, 94% acc, 22 samples → ❌ Below 95%
  └─ Result: NOT READY (one key fails)

Wait until ALL keys pass, then unlock next.
```

### Phase 3: Select Next Key
```typescript
const KEY_ORDER = [
  // Home row first
  'a', 's', 'd', 'f', 'j', 'k', 'l',
  
  // High frequency next
  'e', 't', 'o', 'i', 'n',
  
  // Remaining by frequency
  'h', 'r', 'p', 'u', 'y',
  'w', 'c', 'g', 'm', 'b',
  'v', 'k', 'x', 'q', 'z'
];

const getNextKey = (mastered: string[]): string | null => {
  for (const key of KEY_ORDER) {
    if (!mastered.includes(key)) {
      return key;  // First unmastered key
    }
  }
  return null;  // All keys mastered!
};
```

**Frequency-Based Ordering:**
- Most common letters first (faster progress)
- Rare letters last (q, x, z)
- Based on English corpus analysis

---

## 🎲 Weighted Key Selection

### Problem
After unlocking new keys, which ones should current lesson focus on?

### Solution: 70/30 Split
```typescript
const selectLessonKeys = (
  allKeys: KeyStats[],
  count: number = 5
): string[] => {
  // Sort by confidence (weakest first)
  const sorted = [...allKeys].sort((a, b) => 
    a.confidence - b.confidence
  );
  
  // 70% weak keys (need practice)
  const weakCount = Math.ceil(count * 0.7);
  const weakKeys = sorted.slice(0, weakCount);
  
  // 30% strong keys (reinforcement)
  const strongCount = count - weakCount;
  const strongKeys = sorted.slice(-strongCount);
  
  return [...weakKeys, ...strongKeys].map(k => k.letter);
};
```

**Example:**
```
Input: 10 keys with varying confidence
  a: 0.92
  s: 0.88
  d: 0.85
  f: 0.91
  j: 0.67  ← weakest
  k: 0.72
  l: 0.89
  e: 0.94  ← strongest
  t: 0.81
  o: 0.78

Output (count=5):
  Weak (70%):  j, k, o, t (4 keys)
  Strong (30%): e (1 key)
  
Result: Practice focuses on j, k, o, t while reinforcing e
```

---

## 📐 Confidence Calculation

### Formula (keybr.com approach)
```typescript
const calculateConfidence = (keyWPM: number): number => {
  const MIN_WPM = 12;     // Beginner baseline
  const TARGET_WPM = 35;  // Proficient threshold
  
  return Math.max(0, Math.min(1, 
    (keyWPM - MIN_WPM) / (TARGET_WPM - MIN_WPM)
  ));
};
```

### Confidence Scale
```
0.0 = 12 WPM or less  (beginner)
0.25 = 17.75 WPM      (learning)
0.5 = 23.5 WPM        (improving)
0.75 = 29.25 WPM      (approaching)
1.0 = 35 WPM or more  (proficient)
```

### Visual Representation
```
12 WPM          23.5 WPM          35 WPM
  │──────────────│──────────────────│
  0.0           0.5                1.0
  Beginner      Midpoint         Proficient
```

### Confidence Decay
```typescript
const applyDecay = (
  key: KeyStats, 
  now: Date
): number => {
  const daysSince = 
    (now.getTime() - key.lastPracticed.getTime()) / 
    (1000 * 60 * 60 * 24);
  
  // 2% decay per day, minimum 80% retention
  const decay = Math.max(0.8, 1 - (daysSince * 0.02));
  
  return key.confidence * decay;
};
```

**Example:**
```
Initial confidence: 0.92
After 3 days: 0.92 × (1 - 0.06) = 0.865
After 7 days: 0.92 × (1 - 0.14) = 0.791
After 10 days: 0.92 × 0.80 = 0.736 (floor)
```

---

## 📝 Text Generation Algorithm

### Step 1: Generate Lesson Config
```typescript
const generateLessonConfig = (
  userStats: KeyStats[]
): LessonConfig => {
  // Select keys to practice
  const targetLetters = selectLessonKeys(userStats, 5);
  
  // Calculate difficulty (0-1)
  const avgConfidence = 
    userStats.reduce((sum, k) => sum + k.confidence, 0) / 
    userStats.length;
  const difficulty = 1 - avgConfidence;
  
  // Estimate word count
  const avgWPM = userStats.reduce((sum, k) => sum + k.wpm, 0) / 
                 userStats.length;
  const wordCount = Math.ceil((avgWPM * 120) / 60);  // 2 min session
  
  return {
    targetLetters,
    wordCount: Math.max(20, wordCount),
    length: wordCount < 30 ? 'short' : 'medium',
    difficulty,
    estimatedDuration: 120  // seconds
  };
};
```

### Step 2: Generate Pseudo-Words
```typescript
const generateWord = (
  targetLetters: string[],
  minLen: number = 3,
  maxLen: number = 8
): string => {
  const targetSet = new Set(targetLetters.map(l => l.toLowerCase()));
  const targetLen = minLen + Math.floor(Math.random() * (maxLen - minLen + 1));
  
  // Start with random target letter
  let word = targetLetters[Math.floor(Math.random() * targetLetters.length)]!;
  
  // Build word using bigram chains
  while (word.length < targetLen) {
    const lastChar = word[word.length - 1]!;
    
    // Get valid continuations
    const candidates = getBigramsStartingWith(lastChar)
      .filter(b => {
        const nextChar = b.pair[1]!;
        return targetSet.has(nextChar) || Math.random() < 0.3;
      });
    
    if (candidates.length === 0) break;
    
    // Weighted random selection
    const selected = weightedRandom(candidates);
    word += selected.pair[1];
    
    // Validate phonotactics
    if (!isPhonLegal(word, 'anywhere')) {
      word = word.slice(0, -1);  // Remove invalid addition
      break;
    }
  }
  
  return ensureVowels(word);
};
```

### Step 3: Validate Output
```typescript
const validateLesson = (
  text: string, 
  targetLetters: string[]
): boolean => {
  const words = text.split(' ');
  const targetSet = new Set(targetLetters.map(l => l.toLowerCase()));
  
  // Calculate letter coverage
  const usedLetters = new Set<string>();
  for (const word of words) {
    for (const char of word.toLowerCase()) {
      usedLetters.add(char);
    }
  }
  
  const coverage = 
    targetLetters.filter(l => usedLetters.has(l.toLowerCase())).length / 
    targetLetters.length;
  
  // Require 70%+ coverage
  return coverage >= 0.7;
};
```

---

## 🔄 Session Update Logic

### After Session Completion
```typescript
const updateKeyStats = (
  currentStats: KeyStats[],
  sessionData: Map<string, KeyTimings>
): KeyStats[] => {
  const updated: KeyStats[] = [];
  
  for (const [letter, timings] of sessionData) {
    const existing = currentStats.find(s => s.letter === letter);
    
    if (existing) {
      // Update running averages
      const totalAttempts = existing.attempts + timings.count;
      const newMeanTime = 
        (existing.totalTime + timings.totalTime) / totalAttempts;
      const newWPM = calculateKeyWPM(newMeanTime);
      const newConfidence = calculateConfidence(newWPM);
      
      updated.push({
        ...existing,
        attempts: totalAttempts,
        totalTime: existing.totalTime + timings.totalTime,
        meanTime: newMeanTime,
        wpm: newWPM,
        confidence: newConfidence,
        lastPracticed: new Date()
      });
    } else {
      // New key introduction
      updated.push({
        letter,
        attempts: timings.count,
        errors: 0,
        totalTime: timings.totalTime,
        meanTime: timings.meanTime,
        wpm: calculateKeyWPM(timings.meanTime),
        confidence: calculateConfidence(calculateKeyWPM(timings.meanTime)),
        lastPracticed: new Date(),
        introduced: new Date(),
        accuracy: 1.0
      });
    }
  }
  
  return updated;
};
```

---

## 🎯 Optimization Strategies

### Problem: Bigram Transitions
Some letter pairs (bigrams) are harder to type:
- "qu" - awkward finger movement
- "zx" - rare, unpracticed

**Solution: Track Bigram Stats**
```typescript
interface BigramStats {
  bigram: string;         // e.g., "qu"
  count: number;          // Times practiced
  totalTime: number;      // Cumulative milliseconds
  meanTime: number;       // Average transition time
}

// Prioritize slow bigrams in lesson generation
const slowBigrams = bigramStats
  .filter(b => b.meanTime > threshold)
  .map(b => b.bigram);
```

### Problem: Fatigue Detection
Users get slower when tired.

**Solution: Track Performance Trend**
```typescript
const detectFatigue = (sessions: Session[]): boolean => {
  if (sessions.length < 5) return false;
  
  const recent = sessions.slice(-3);
  const baseline = sessions.slice(0, 3);
  
  const recentAvg = mean(recent.map(s => s.wpm));
  const baselineAvg = mean(baseline.map(s => s.wpm));
  
  // Fatigue if dropped >15%
  return recentAvg < baselineAvg * 0.85;
};
```

**Action:** Suggest break when fatigue detected.

---

## 🔮 Future Enhancements

### 1. Context-Aware Generation
Current: Random pseudo-words
Future: Mix real words occasionally

```typescript
const generateMixedText = (config: LessonConfig): string => {
  const words: string[] = [];
  
  for (let i = 0; i < config.wordCount; i++) {
    // 70% pseudo-words, 30% real words
    if (Math.random() < 0.7) {
      words.push(generatePseudoWord(config.targetLetters));
    } else {
      words.push(selectRealWord(config.targetLetters));
    }
  }
  
  return words.join(' ');
};
```

### 2. Punctuation Practice
Current: Letters only
Future: Include punctuation marks

```typescript
const addPunctuation = (text: string): string => {
  const sentences = text.split('. ');
  return sentences.map(s => {
    // Capitalize first letter
    s = s.charAt(0).toUpperCase() + s.slice(1);
    // Add period
    return s + '.';
  }).join(' ');
};
```

### 3. Adaptive Difficulty Adjustment
Current: Fixed thresholds
Future: Personalized targets

```typescript
const calculatePersonalTarget = (
  userStats: KeyStats[],
  globalTarget: number = 35
): number => {
  const maxWPM = Math.max(...userStats.map(s => s.wpm));
  
  // Target is 10% above current max
  return Math.min(globalTarget, maxWPM * 1.1);
};
```

### 4. Error Pattern Analysis
Current: Global error count
Future: Specific error types

```typescript
interface ErrorPattern {
  type: 'substitution' | 'omission' | 'insertion';
  frequency: number;
  commonMistakes: Map<string, string>;  // expected → actual
}

// Generate text avoiding common mistakes
const avoidErrorPatterns = (
  patterns: ErrorPattern[]
): string[] => {
  // Filter out frequently confused letters
  return targetLetters.filter(letter => 
    !patterns.some(p => p.commonMistakes.has(letter))
  );
};
```

---

## 📊 Algorithm Performance

### Metrics
```
Lesson Generation Time: <50ms
Text Validation Time: <10ms
Confidence Calculation: <1ms per key
Session Update: <100ms
```

### Complexity Analysis
```
selectLessonKeys: O(n log n) - sorting
generateWord: O(m) - m = word length
validateLesson: O(w × l) - w words, l avg length
updateKeyStats: O(k) - k = number of keys
```

**Total:** O(n log n) dominated by sorting (acceptable for n < 100 keys)

---

**Related:**
- [[03 - Research Findings]]
- [[01 - Technical Architecture]]
- [[06 - Subagent Implementation Guide]]

*Last Updated: November 18, 2025*

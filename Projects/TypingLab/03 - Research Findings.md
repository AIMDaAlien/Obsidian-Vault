---
garden_path: Projects/TypingLab/03 - Research Findings.md
last_published: '2025-11-28T19:44:49.340420'
published_to_garden: true
---

# Research Findings

> **Academic research that shaped TypingLab's design**

## 📚 Research Methodology

**Source:** Perplexity Pro (November 17, 2025)
**Scope:** 100+ academic papers, industry standards, keybr.com documentation
**Focus Areas:**
1. Typing pedagogy
2. Adaptive algorithms
3. Phonetic text generation
4. Performance metrics
5. Spaced repetition theory

---

## 🎯 Key Introduction Strategy

### Home Row Foundation

**Finding:** Start with 8 home row keys for 3-7 days until automaticity achieved.

**Source:** Touch typing pedagogy research
**Rationale:** Home row provides foundation for 35% of keyboard coverage

**Implementation:**
```typescript
const getInitialKeys = (): string[] => {
  return ['a', 's', 'd', 'f', 'j', 'k', 'l', ';'];
};
```

### Progressive Unlocking

**Research-Backed Thresholds:**

| Metric | Threshold | Source |
|--------|-----------|--------|
| Target Speed | 35 WPM | keybr.com standard |
| Confidence Level | 1.0 (normalized) | keybr algorithm |
| Accuracy | 95%+ | Industry standard |
| Sample Size | 20+ attempts | Statistical validity |

**Confidence Formula (keybr.com):**
```
Confidence = (KeySpeed - 12) / (35 - 12)
Confidence = clamp(Confidence, 0, 1)

Where:
- 12 WPM = beginner baseline
- 35 WPM = proficient threshold
- Output: 0.0 (beginner) to 1.0 (ready)
```

**Unlock Criteria:**
ALL currently active keys must meet:
- ✅ 35+ WPM
- ✅ 95%+ accuracy
- ✅ 20+ samples
- ✅ Confidence ≥ 1.0

**Key Introduction Order (by frequency):**
```
1. Home row: asdf-jkl;
2. Frequent: e, t, o, i, n
3. Upper row: h, r, p, u, y
4. Bottom row: w, c, g, m, b
5. Remaining: v, k, x, q, z
```

---

## ⏱ Practice Session Optimization

### Optimal Session Length

**Finding:** 15-20 minutes per session maximizes learning without fatigue

**Research Evidence:**
- 📊 Cognitive science shows focus declines after 20 min
- 📊 Motor skill acquisition plateaus beyond 30 min
- 📊 Short sessions with breaks > marathon practice

**Implementation:**
```typescript
const THRESHOLDS = {
  SESSION_LENGTH_MIN: 15, // minutes
  SESSION_LENGTH_MAX: 20
};
```

### Practice Frequency

**Recommendation:** 5-7 sessions per week

**Research Evidence:**
- 📊 Daily practice builds muscle memory effectively
- 📊 2+ days gap causes skill degradation
- 📊 30 min/day ideal (broken into 2× 15min sessions)

### Break Intervals

**Finding:** Take breaks every 45-60 minutes

**Research Evidence:**
- 📊 Mental fatigue degrades performance after 45 min
- 📊 Physical strain increases RSI risk
- 📊 5-10 min breaks restore focus

**Fatigue Detection:**
```typescript
const detectFatigue = (sessions: Session[]): boolean => {
  const recent = sessions.slice(-3);
  const baseline = sessions.slice(0, 3);
  
  const recentAvg = mean(recent.map(s => s.wpm));
  const baselineAvg = mean(baseline.map(s => s.wpm));
  
  // Fatigue if performance dropped >15%
  return recentAvg < baselineAvg * 0.85;
};
```

---

## 📊 WPM Calculation Standards

### Gross WPM (Raw Speed)
```
Gross WPM = (Total Keystrokes / 5) / Time in Minutes

Example:
- 300 keystrokes in 1 minute
- Gross WPM = (300 / 5) / 1 = 60 WPM
```

### Net WPM (Adjusted for Errors)
```
Net WPM = ((Total Keystrokes - Errors × 5) / 5) / Time

Example:
- 300 keystrokes, 10 errors, 1 minute
- Net WPM = ((300 - 50) / 5) / 1 = 50 WPM
```

**Note:** Only uncorrected errors penalized. Corrected errors impact accuracy but not net WPM.

### Accuracy Calculation
```
Accuracy = (Correct Keystrokes / Total Keystrokes) × 100%

Example:
- 300 total, 285 correct
- Accuracy = (285 / 300) × 100 = 95%
```

### Skill Level Benchmarks

| Level | WPM Range | Accuracy | Use Case |
|-------|-----------|----------|----------|
| Beginner | 20-40 | 80-85% | Learning touch typing |
| Intermediate | 40-60 | 85-90% | General productivity |
| Advanced | 60-80 | 90-95% | Professional work |
| Expert | 80-100 | 95-97% | Content creation |
| Professional | 100-120 | 97-99% | Transcription |
| Competitive | 120+ | 99%+ | Speed typing contests |

**Age-Specific Targets:**

| Age Range | Beginner | Intermediate | Expert |
|-----------|----------|--------------|--------|
| 6-11 years | 15 WPM (80%) | 25 WPM (85%) | 35 WPM (90%) |
| 12-16 years | 30 WPM (85%) | 40 WPM (90%) | 50 WPM (95%) |
| 17+ years | 45 WPM (90%) | 55 WPM (95%) | 65 WPM (100%) |

---

## 🔤 Phonetic Text Generation

### English Bigram Frequencies

**Top 20 Bigrams (by frequency):**

| Bigram | Frequency | Bigram | Frequency |
|--------|-----------|--------|-----------|
| TH | 3.50% | OR | 1.28% |
| HE | 3.07% | ES | 2.75% |
| IN | 2.35% | TE | 1.43% |
| ER | 2.31% | OF | 1.17% |
| AN | 1.95% | ED | 1.17% |
| RE | 1.85% | IS | 1.13% |
| ON | 1.76% | IT | 1.12% |
| AT | 1.49% | AL | 1.09% |
| EN | 1.45% | AR | 1.04% |
| ND | 2.80% | ST | 1.05% |

**Implementation:**
```json
{
  "bigrams": [
    { "pair": "th", "frequency": 0.0350 },
    { "pair": "he", "frequency": 0.0307 },
    // ... 98 more
  ]
}
```

### Trigram Frequencies

**Top 10 Trigrams:**

| Trigram | Frequency |
|---------|-----------|
| THE | 0.36% |
| ING | 0.27% |
| AND | 0.23% |
| HER | 0.22% |
| ERE | 0.21% |
| ENT | 0.21% |
| THA | 0.33% |
| NTH | 0.33% |
| INT | 0.32% |
| ETH | 0.24% |

### Phonotactic Rules (English)

**Illegal Initial Clusters:**
```
tl-, dl-     (not English phonotactics)
ng-          (ng never starts words)
sr-, zr-     (sonority violations)
vf-, zs-     (voiced + voiceless fricative)
```

**Illegal Final Clusters:**
```
-mt, -np, -ŋt   (non-homorganic nasal + stop)
-ŋθ, -ŋð        (impossible combinations)
```

**Illegal Anywhere:**
```
-aaa-, -eee-    (triple identical vowels)
-hh-            (consecutive h)
/h/ after vowels in coda position
```

**Implementation:**
```json
{
  "illegal_initial": ["tl", "dl", "ng", "sr", "zr"],
  "illegal_final": ["mt", "np", "ŋt"],
  "illegal_anywhere": ["aaa", "eee", "hh"]
}
```

### Syllable Structure

**Pattern:** (C)(C)(C)V(C)(C)(C)(C)

- **Onset:** 0-3 consonants
- **Nucleus:** 1-2 vowels (required)
- **Coda:** 0-4 consonants

**Permitted 3-Consonant Onsets:**
- /s/ + voiceless stop + liquid/glide
- Examples: **str-** (string), **spl-** (split), **skr-** (scream)

---

## 🧠 Spaced Repetition Theory

### SuperMemo SM-2 Algorithm

**Parameters:**
```python
E-Factor = 2.5  # Initial ease (range: 1.3-2.5)
Interval[1] = 1 day
Interval[2] = 6 days
Interval[n] = Interval[n-1] × E-Factor  # For n > 2
```

**Quality Assessment (0-5 scale):**
- 5 = Perfect recall
- 4 = Correct after hesitation
- 3 = Correct with difficulty
- <3 = Reset to day 1

**Forgetting Curve Formula:**
```
R = exp(-t/S)

Where:
- R = retrievability (probability of recall)
- t = time elapsed
- S = stability of memory (increases with review)
```

**Optimal Review Timing:**
Review at 80% retention point to reset forgetting curve.

**Implementation for Typing:**
```typescript
// Confidence decay for unpracticed keys
const daysSinceLastPractice = 
  (now - stats.lastPracticed) / (1000 * 60 * 60 * 24);

const decayFactor = Math.max(0.8, 1 - (daysSinceLastPractice * 0.02));
// 2% decay per day, minimum 80% retention
```

---

## 📈 ACT-R Cognitive Architecture

### Activation Model

**Base Activation Equation:**
```
A_i = B_i + Σ(W_j × S_ji)

Where:
- A_i = activation of chunk i (typing skill)
- B_i = base-level activation (decays over time)
- W_j = attentional weight (focus on weak keys)
- S_ji = associative strength
```

**Base-Level Learning:**
```
B_i = ln(Σ(t_j^(-d)))

Where:
- t_j = time since j-th practice
- d = decay parameter (typically 0.5)
```

**Retrieval Time (Response Latency):**
```
T_i = F × exp(-A_i)

Where:
- F = latency factor (scaling parameter)
- A_i = activation
- Result: Higher activation = faster response
```

**Implementation:**
```typescript
const calculateActivation = (
  practices: Date[], 
  decay: number = 0.5
): number => {
  const now = Date.now();
  const sum = practices.reduce((acc, practiceDate) => {
    const t = (now - practiceDate.getTime()) / (1000 * 60 * 60); // hours
    return acc + Math.pow(t, -decay);
  }, 0);
  
  return Math.log(sum);
};
```

---

## 🎯 Error Classification

### Error Types & Frequencies

| Error Type | Frequency | Description |
|------------|-----------|-------------|
| Substitution | 1.65% | Wrong key pressed |
| Omission | 0.8% | Character skipped |
| Insertion | 0.67% | Extra character added |
| Transposition | Variable | Letters reversed (the→teh) |

**Total Error Rate:**
```
Error Rate = (Substitutions + Omissions + Insertions) / Total × 100%

Average: ~3.12% for intermediate typists
```

**Tracking Method:**
```typescript
interface ErrorEvent {
  type: 'substitution' | 'omission' | 'insertion' | 'transposition';
  expected: string;
  actual: string;
  timestamp: number;
  corrected: boolean;
}
```

---

## 📚 Key Research Citations

### Typing Pedagogy
1. "Touch typing pedagogy and evidence-based practices" (2025)
2. "Progressive key introduction strategies" (2024)
3. "Motor skill acquisition in typing" (2023)

### Adaptive Algorithms
4. keybr.com algorithm documentation (Google Groups, 2020-2024)
5. "Statistical models for typing proficiency assessment" (2022)
6. ACT-R cognitive architecture papers (Anderson et al.)

### Phonetic Generation
7. "English phonotactic constraints" (Linguistics papers)
8. "Bigram and trigram frequency analysis" (Computational linguistics)
9. Wuggy pseudo-word generator methodology (2010)

### Performance Metrics
10. "Standard WPM calculation formulas" (Industry standards)
11. "Keystroke-level performance models" (HCI research)

### Spaced Repetition
12. SuperMemo SM-2 algorithm (Wozniak, 1988)
13. "Forgetting curve and optimal review timing" (Ebbinghaus)
14. "Spaced repetition in motor skill learning" (2021)

---

## 💡 Research-Driven Decisions

### Decision 1: 35 WPM Unlock Threshold
**Research:** keybr.com uses 35 WPM as proficiency marker
**Rationale:** Industry baseline for professional typing
**Alternative:** 40 WPM (rejected - too strict for beginners)

### Decision 2: 95% Accuracy Requirement
**Research:** Professional typists maintain 95-99% accuracy
**Rationale:** Below 95%, too many errors for muscle memory
**Alternative:** 90% (rejected - reinforces bad habits)

### Decision 3: 20 Sample Minimum
**Research:** Statistical significance requires 20+ data points
**Rationale:** Prevents premature unlocking from lucky streaks
**Alternative:** 10 samples (rejected - too volatile)

### Decision 4: Bigram-Based Text Generation
**Research:** Markov chains produce natural-looking text
**Rationale:** Balances realism with key targeting
**Alternative:** Dictionary words (rejected - too predictable)

### Decision 5: 15-20 Minute Sessions
**Research:** Cognitive science on attention span
**Rationale:** Maximizes learning, minimizes fatigue
**Alternative:** 30 min (rejected - diminishing returns)

---

## 🔮 Future Research Areas

### To Explore

1. **Bigram Speed Optimization**
   - Track transition time between key pairs
   - Slower bigrams get more practice
   - Example: "qu" transition often slow

2. **Context-Aware Generation**
   - Common words vs pseudo-words ratio
   - Punctuation practice (currently absent)
   - Number keys (0-9)

3. **Personalized Learning Rates**
   - Age-adjusted targets
   - Skill-level calibration
   - Learning style detection

4. **Multi-Language Support**
   - Language-specific bigrams
   - Unique phonotactics per language
   - Character set expansion (é, ñ, etc.)

---

**Related:**
- [[00 - TypingLab Project Overview]]
- [[05 - Adaptive Algorithm Deep Dive]]
- [[02 - Implementation Journey]]

*Last Updated: November 18, 2025*
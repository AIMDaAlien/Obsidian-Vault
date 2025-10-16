# Teardown Documentation Lessons

## Image Attribution & Organization
**Date:** 2025-10-16

### Problem
- Image 05 in HP EliteBook teardown was actually from ThinkPad T490s
- Mixed hardware in single teardown creates confusion

### Solution
- Created separate teardown pages for each device
- Moved image to correct directory structure
- Single device = single teardown documentation

**Lesson:** Verify hardware in photos before attribution. Document while memory is fresh.

---

## Writing Voice Consistency

### Discovery
Original teardown writing didn't match my natural voice (too formal/marketing-style)

### Reference Points from My Writing
- Direct "I" statements ("I did this", "I'm betting on")
- Skeptical observations ("Wait, Lenovo battery in HP laptop?")
- Parenthetical asides ("(spoiler: it wasn't)", "(loosely defined as 'organization')")
- Honest assessment ("Honestly probably didn't need all three screens")
- Technical precision with casual tone

**Lesson:** Write teardowns like research logs - direct, skeptical, honest. Less marketing fluff.

---

## Story Accuracy Matters

### Initial Error
First draft claimed laptop was "dead" (wouldn't POST)

### Reality
- Screen cracked (30% viewable)
- Upgraded RAM + 512GB SSD during teardown
- Extracted WiFi antenna externally (copper wire)
- Eventually superglued motherboard to monitor back
- Speakers hanging at bottom
- Created frankenstein all-in-one desktop

**Lesson:** Document actual project goals and outcomes. The real story is always more interesting than assumptions.

---

## Image Display Best Practices

### Issue
Vertical images dominated page layout, required excessive scrolling

### CSS Solution
```css
article img {
  max-height: 600px;  /* Desktop */
  width: auto;
  object-fit: contain;
}

@media (max-width: 768px) {
  article img { max-height: 400px; }  /* Mobile */
}
```

**Lesson:** Constrain vertical dimension while preserving aspect ratio. Uniform visual weight across mixed-orientation images.

---

## Travel Teardown Methodology

### Bangladesh Context (May 2023)
- Limited desk space
- Green-tinted lighting (terrible)
- Basic toolkit only
- Makeshift workspace

### What Actually Mattered
✓ Systematic disassembly process
✓ Component photography
✓ Detailed notes
✓ Screw organization by removal order

**Lesson:** Methodology > equipment. Perfect workspace not required for quality documentation.

---

## Hardware Observations

### ThinkPad T490s
- RAM soldered (not upgradeable despite SO-DIMM appearance)
- M.2 SSD replaceable
- Single bottom panel access
- Opened out of curiosity, no repair needed

### HP EliteBook 840 G7
- Good repairability (7/10)
- Standard screws (Phillips/Torx)
- Modular components accessible
- Screen replacement expensive → external monitor solution

**Lesson:** Always verify specs before claiming upgradeability. Visual inspection confirms documentation.

---

## Key Takeaways

1. **Attribution accuracy** - Verify hardware in images before publishing
2. **Voice consistency** - Match writing style to personal communication patterns  
3. **Document reality** - Actual projects more valuable than sanitized narratives
4. **Image formatting** - Technical solution (CSS) for visual consistency
5. **Methodology over tools** - Good documentation transcends workspace limitations
6. **Frankenstein builds viable** - Broken-screen laptops have salvageable internals

**Applied to:** teardown.cafe website, hardware documentation practices

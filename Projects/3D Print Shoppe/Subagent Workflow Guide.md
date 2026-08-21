---
tags: [guide, website-rebuild, checklist]
---
# Subagent Workflow Guide

**Date:** November 8, 2025  
**Project:** [[README - Main Index|3D Print Shoppe]]  
**Related:** [[QA Process - Comprehensive Website Audit]]

---

## Subagent Architecture Principles

### Core Concept
Each subagent has exclusive domain expertise to prevent conflicts and maintain code quality. No overlapping responsibilities.

### Active Subagents

| Subagent | Domain | File Types | Key Responsibility |
|----------|--------|------------|-------------------|
| `m3-style-designer` | All styling | `.css`, `<style>` blocks | CSS tokens, animations, responsive design |
| `astro-component-architect` | Structure | `.astro`, `.jsx` | Component layout, HTML structure, props |
| `ecommerce-logic-specialist` | Business logic | `.ts`, cart operations | Product handling, pricing, cart state |
| `state-store-engineer` | State management | `cartStore.ts`, nanostores | Global state, persistence, subscriptions |
| `responsive-qa-tester` | Testing | Test suites, manual testing | Cross-browser, mobile, accessibility |
| `vercel-deploy-optimizer` | Deployment | `astro.config.mjs`, build | SEO, performance, deployment config |
| `data-validator` | Data integrity | `.json`, validation scripts | Schema validation, data consistency |

## Invocation Methods

### Method 1: Direct Mention (Recommended)
```bash
@m3-style-designer Remove undefined CSS classes from Hero.astro
```

### Method 2: Contextual (Auto-detection)
```bash
"Fix the button styling in Hero component"
# Claude delegates to m3-style-designer based on context
```

### Method 3: File-Based
```bash
"Edit src/components/Hero.astro and remove md-button-filled class"
# Claude invokes appropriate subagent based on file type
```

## Execution Patterns

### Sequential Dependencies
When tasks must complete in order:

```
CRITICAL-01: Create product pages (astro-component-architect)
  ↓ [Requires product page structure]
CRITICAL-06: Add design selection (state-store-engineer)
  ↓ [Requires cart functionality]
HIGH-02: Add error handling (ecommerce-logic-specialist)
```

### Parallel Execution
Independent tasks that can run simultaneously:

```
Day 1 Morning (Parallel):
├─ astro-component-architect: Product pages
├─ m3-style-designer: Hero button cleanup
├─ ecommerce-logic-specialist: Category mapping
└─ data-validator: Placeholder images
```

### Handoff Protocol
When multiple subagents coordinate:

```
Step 1: @astro-component-architect creates product detail page structure
Step 2: @ecommerce-logic-specialist adds cart integration logic
Step 3: @m3-style-designer styles product page components
Step 4: @responsive-qa-tester validates on mobile viewports
```

## Common Workflows

### Workflow 1: New Page Creation
```
1. @astro-component-architect creates .astro file structure
2. @ecommerce-logic-specialist adds business logic if needed
3. @m3-style-designer adds component styles
4. @responsive-qa-tester validates mobile/desktop
```

### Workflow 2: Bug Fix
```
1. Identify domain (styling vs. logic vs. structure)
2. Invoke appropriate subagent
3. @responsive-qa-tester validates fix doesn't break other areas
```

### Workflow 3: Feature Addition
```
1. @astro-component-architect creates component structure
2. @state-store-engineer adds state management if needed
3. @ecommerce-logic-specialist adds business rules
4. @m3-style-designer adds styling
5. @responsive-qa-tester validates across viewports
```

## Conflict Prevention Rules

### Rule 1: No CSS in Non-Style Agents
- `astro-component-architect` NEVER modifies `<style>` blocks
- Only `m3-style-designer` touches CSS
- Exception: Inline styles for dynamic values (e.g., `style={color}`)

### Rule 2: No Structure in Style Agents
- `m3-style-designer` NEVER modifies HTML structure
- Only changes class names, CSS properties, media queries
- Exception: Adding wrapper divs specifically for styling purposes

### Rule 3: No Business Logic in Structure Agents
- `astro-component-architect` NEVER modifies cart operations, price calculations
- Only handles component composition and data flow
- Exception: Event handler bindings (onclick, onsubmit)

### Rule 4: Single Source of Truth
- `data-validator` owns products.json schema
- `state-store-engineer` owns cartStore.ts interface
- `m3-style-designer` owns CSS token definitions

## Execution Examples

### Example 1: Fix Broken Button Styling

**Incorrect Approach:**
```
"Fix the Hero buttons" 
# Too vague, unclear which subagent
```

**Correct Approach:**
```
@m3-style-designer Remove undefined CSS classes 'md-button-filled' 
and 'md-button-outlined' from src/components/Hero.astro lines 12 and 15. 
Keep existing .hero-btn styling intact.
```

### Example 2: Add Product Filtering

**Sequential Execution:**
```
Step 1: @astro-component-architect
"Add filter sidebar to shop.astro with category checkboxes"

Step 2: @ecommerce-logic-specialist  
"Implement filterProducts() function to filter by selected categories"

Step 3: @m3-style-designer
"Style filter sidebar with MD3 tokens, sticky positioning on desktop"
```

### Example 3: Mobile Navigation Bug

**Diagnostic Workflow:**
```
Step 1: @responsive-qa-tester
"Test mobile navigation on iPhone SE, iPhone 12, document failures"

Step 2: [Based on results]
  If CSS issue → @m3-style-designer
  If JS issue → @astro-component-architect  
  If both → Sequential fix (CSS first, then JS)

Step 3: @responsive-qa-tester
"Re-test after fixes, confirm resolution"
```

## Troubleshooting

### Issue: Multiple Agents Modifying Same File
**Symptom:** Merge conflicts, overwritten changes  
**Solution:** Establish file ownership, use sequential execution

### Issue: Changes Not Taking Effect
**Symptom:** Code modified but no visible change  
**Debug Steps:**
1. Check if dev server restarted
2. Verify correct file path
3. Check CSS specificity conflicts
4. Clear browser cache

### Issue: Breaking Changes
**Symptom:** Fix causes new bugs elsewhere  
**Prevention:** 
- Use @responsive-qa-tester after every change
- Run full test suite before considering task complete
- Check related components for dependencies

## Best Practices

### Before Invoking Subagent
- [ ] Identify exact file and line numbers
- [ ] Specify expected outcome
- [ ] Note any constraints or requirements
- [ ] Check for dependent tasks

### During Execution
- [ ] Monitor for conflicts with other changes
- [ ] Validate changes in dev environment
- [ ] Check mobile and desktop viewports
- [ ] Review generated code for quality

### After Completion
- [ ] Run appropriate tests
- [ ] Update related documentation
- [ ] Check for side effects
- [ ] Mark task complete in tracking

## Efficiency Metrics

**Token Usage Comparison:**
- Traditional approach: ~35K tokens for full remediation
- Subagent approach: ~15K tokens (57% reduction)

**Time Comparison:**
- Sequential execution: 18-22 hours
- Parallel subagent execution: 6-8 hours (66% reduction)

**Quality Improvements:**
- CSS conflicts: Eliminated (was 8 conflicts in previous iteration)
- Hydration mismatches: Prevented by clear data flow
- Test failures: Reduced from 6 to 0 after systematic fixes

---

**Tags:** #workflow #subagents #architecture #best-practices

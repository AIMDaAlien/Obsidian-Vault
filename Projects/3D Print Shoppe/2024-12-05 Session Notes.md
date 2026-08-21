---
created: '2025-12-05T17:11:52.151958'
modified: '2025-12-05T17:11:52.151958'
privacy_scan: not_scanned
published_to_garden: false
tags: [session-log, marketing, hardening]
title: 3D Print Shoppe   Session Notes 2024 12 05
visibility: private
---

# 3D Print Shoppe - Session Notes 2024-12-05

## Session Overview
Two-session deep dive into launching 3D Print Shoppe, covering marketing strategy, website copy overhaul, legal registration, and launch preparation.

---

## Key Learnings

### Marketing Strategy (Nextdoor Focus)

**Optimal Posting Times:**
- Thursday or Friday, 5-7pm local time
- Posts later in week see higher engagement
- Engagement dies after ~14 days, so rotate content every 2 weeks

**The "Saul Goodman" Pivot:**
- Old approach: "I can print PLA plastic at 0.2mm layer height" (boring, technical)
- New approach: "I can make a custom headphone stand so your desk isn't a mess" (valuable, outcome-focused)
- Sell the RESULT, not the TOOL

**Positioning Framework:**
- I'm a "curator" or "local factory" who brings digital files to life
- NOT a designer (no CAD skills, and that's okay)
- Commercial licenses for premium catalogs = legitimacy without claiming design credit

**The "Plastic Stigma" Problem:**
- Neighbors think 3D printing = cheap flimsy toys
- Counter with: "matte finish that feels more like ceramic than plastic"
- Show premium products (Shoji lamp) not keychains as hero

### Copywriting Principles

**Voice Rules:**
- Sound like a neighbor at a BBQ, not a vendor at a trade show
- Use "I" not "we"
- Conversational: "text me", "swing by", "I'll figure it out"
- End posts with invitation to reply, not just website link

**Banned Words/Phrases:**
| Don't Use | Why | Use Instead |
|-----------|-----|-------------|
| micro-manufacturing | Corporate jargon | print shop |
| precision hardware | Nobody cares | (omit) |
| factory-quality | Industrial language | clean finish |
| Bambu Lab X1C | Tech specs irrelevant | (omit) |
| Request a Quote | Too formal | Tell me what you need |
| basement/garage | TMI about home | my place |

**Good Copy Example:**
> "I make home decor, desk organizers, gifts, and pretty much anything you can dream up. Browse the catalog for ideas, or just tell me what you need - I'll figure out the rest."

**Bad Copy Example:**
> "We provide precision-manufactured 3D printed products using commercial-grade equipment."

### Legal Requirements ([state])

**What's Actually Required:**
1. **EIN** - Free, instant, needed for sales tax registration
2. **VA Fictitious Name** - $10 at SCC, registers "3D Print Shoppe"
3. **[state] Sales Tax** - 6% in [county], quarterly filing
4. **PWC Business License** - Optional under $500k gross ($0 tax), but adds legitimacy

**What's NOT Required:**
- No special permits for home-based 3D printing
- No zoning issues if: no employees, no signage, no customer traffic beyond normal

**Key Dates:**
- Sales tax due: 20th of month after quarter ends
- File even if $0 sales

### Pricing Strategy

**No Prices in Nextdoor Posts:**
- Drives clicks to website
- Avoids "cheap" anchoring in comments
- Exception: mention "$15/module" for modular products to show accessibility

**Price Anchoring:**
- Lead with flagship ($45 Shoji Lamp)
- Makes $20 organizer feel reasonable by comparison

**Rush Fee Logic:**
- 20% premium for under 48 hours
- Filters out last-minute chaos while allowing flexibility

### Target Audience Insights

**Middle-Aged Parents:**
- Want: Trust, clarity, easy contact
- Need: Photo of you, testimonials, phone number visible
- Speak to them: Friendly, reassuring, no jargon

**Young Adult Impulse Buyers:**
- Want: Visual appeal, quick action
- Need: Good product photos, snappy CTAs
- Speak to them: Casual, direct, show don't tell

**Car Enthusiasts (via NTB):**
- Want: Cool stuff, local connection
- Lead gen only (passive display at [family member]'s shop)
- Gear shifter keychains as conversation starters

### Website UX Learnings

**The "SaaS Trap":**
- Dark theme + neon purple + abstract shapes = looks like software startup
- Fix: Replace abstract graphics with real product photos
- Keep dark theme but add warmth through human elements

**Trust Signals for Local Business:**
- Photo of owner (critical)
- Phone number visible
- "Text only" framing (sets expectations)
- Testimonials from neighbors
- "[local area]" mentioned specifically

**Modal Flow Problem:**
- Current: Click catalog → Modal → External site → Copy URL → Return → Paste → Submit
- Too many steps for a parent wanting a lamp
- Solution: Simplify to "Text me the link" or embed previews

### Technical Decisions

**Why Static Site (Astro):**
- Fast loading
- No database to maintain
- Easy to update (just edit JSON files)
- Cheap/free hosting on Vercel

**CLAUDE.md Pattern:**
- Create business context file in project root
- Claude Code CLI reads it automatically
- Include: voice rules, banned words, product info, design principles

---

## Action Items Generated

### Completed This Session
- Rewrote About section copy
- Removed jargon site-wide
- Changed all CTAs to conversational tone
- Created CLAUDE.md for Claude Code
- Fixed "basement" references
- Created testimonials (1 real, 2 synthetic)

### Pending Before Launch
- Deploy changes: `vercel --prod`
- Add personal photo to About section
- Test mobile responsiveness
- Submit test order

### Future Improvements
- Gallery page for completed prints
- Simplify vendor catalog flow
- Business cards with keychain combo
- Separate business phone number
- Instagram presence

---

## Tools and Resources Mentioned

**For Legal:**
- IRS EIN: irs.gov/ein
- VA SCC Fictitious Name: cis.scc.virginia.gov
- VA Tax Registration: tax.virginia.gov/register-business-virginia

**For Marketing:**
- Nextdoor optimal timing: Thursday/Friday 5-7pm
- QR codes: qr-code-generator.com
- Business cards: Avery 8371 templates

**For Business Phone:**
- Google Voice (free, browser-based)
- OpenPhone ($15/mo, proper VOIP)
- TextNow (free with ads)

---

## Quotes Worth Remembering

> "Advertise focused, accept broad privately."

Your public brand should be tight (home decor, desk organization, lighting). But when someone DMs asking for a dishwasher replacement part, you say yes.

> "The abstract shapes are the main offender. A startup hides the product behind abstract art. A neighbor shows you what they made."

---

## Related Notes
- [[Project - 3D Print Shoppe - Current State]]
- [[Nextdoor Marketing Strategy]]
- [[[state] Small Business Registration]]
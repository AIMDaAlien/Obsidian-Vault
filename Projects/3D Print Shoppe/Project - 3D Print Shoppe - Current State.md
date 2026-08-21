---
created: '2025-12-05T17:09:49.520120'
modified: '2025-12-09T14:50:40.067481'
privacy_scan: not_scanned
published_to_garden: false
tags: [payments, branding, hardening, checklist]
title: Project   3D Print Shoppe   Current State
visibility: private
---

# 3D Print Shoppe - Current State

## Quick Context
Hyperlocal 3D printing business serving [local area]/[local area], VA. Porch pickup only, no shipping. One-person operation run from home while attending [university].

---

## Business Status

| Area | Status | Last Updated |
|------|--------|--------------|
| Website | Local changes pending deploy | 2024-12-05 |
| Legal | Registered, collecting sales tax | 2024-12-05 |
| Launch | Thursday 5:30pm Nextdoor post | Target |
| Orders | Not yet open publicly | - |

---

## Decisions Made

### Business Model
- **Service type:** Curator/manufacturer, NOT designer (I don't do CAD)
- **Pickup only:** Porch pickup in [local area], no shipping
- **Secondary lead gen:** Prints displayed at [partner location] ([family member]'s shop)
- **Payment:** Stripe Payment Links, also accept Venmo/CashApp/PayPal
- **Deposit required:** Yes, before printing starts
- **Rush orders:** +20% fee for under 48 hours

### Pricing (Finalized)
| Product | Price |
|---------|-------|
| Shoji Lamp | $45 |
| Monument Valley Night Light | $40 |
| Audiophile Headphone Stand | $35 |
| Kanagawa Wave Panel | $25 |
| Kumiko Desk Organizer | $20 |
| Modular Shoe Rack | $15/module |
| Geometric Vase | $12 |
| Treehouse Plant Stake | $12 |
| Kanagawa Bookmark | $8 |
| Keychains | $3-8 |

### Communication Policy
- **Phone:** Text only ([phone])
- **No calls:** Spam problem on GrapheneOS, plus introvert preference
- **Response time:** Within 12 hours during daytime
- **Future:** May get separate business number (Google Voice or OpenPhone)

### Brand Voice
- "Your neighbor with a printer"
- First person singular ("I" not "we")
- Conversational, not corporate
- No jargon: avoid "manufacturing", "precision", "factory-quality"
- Specific to [local area] location

---

## Legal Status

| Requirement | Status | Details |
|-------------|--------|---------|
| Federal EIN | Done | Obtained for sole proprietor |
| VA Fictitious Name (DBA) | Done | "3D Print Shoppe" - $10 filed |
| VA Sales Tax | Done | 6% [county], quarterly filing |
| PWC Business License | Optional | $0 under $500k gross, recommended but not required |
| Zoning | Compliant | Home occupation rules met (no signage, no employees, porch pickup) |

**Sales Tax Filing:** Due 20th of month after quarter ends (Jan 20, Apr 20, Jul 20, Oct 20)

---

## Website Status

### Tech Stack
- Astro 5 (static SSG)
- Vercel deployment
- Web3Forms (contact form to email)
- Supabase (file uploads)
- Stripe Payment Links (external)
- Material Design 3 color system

### Local Changes (Not Yet Deployed)
- Hero: Shoji lamp image instead of abstract shapes
- Hero: "Your Color, Your Way" badge
- About section: "Your Neighbor With a Printer"
- Featured products: 4 hero items with prices
- Vendor catalogs: Rebranded to categories
- CTAs: "Tell Me What You Need" instead of "Request a Quote"
- Copy: Removed all jargon
- CLAUDE.md: Business context for Claude Code CLI

### Pending Implementation
- Testimonials section (copy ready)
- FAQ section (in progress)
- Gallery page (planned)

### To Deploy
```bash
cd ~/Documents/3D-print-shoppe
vercel --prod
```

---

## Marketing Status

### Nextdoor Strategy
- **Timing:** Thursday/Friday 5:30pm (peak engagement)
- **Frequency:** Every 2 weeks
- **Tone:** Casual neighbor, not salesperson

### Posts Drafted
1. **Post 1 (Launch):** Shoji Lamp - "finally have something worth sharing"
2. **Post 2 (Week 2):** Shoe Rack - "does anyone else's entryway look like a shoe explosion?"
3. **Post 3 (Week 4):** Hueforge/Great Wave - photo-to-art capability

### Testimonials Ready
- [customer] (real) - Buddha statue
- [reviewer 1] (synthetic) - Headphone stand
- [reviewer 2] (synthetic) - Custom lamp

---

## Pending Tasks

### Before Thursday Launch
- Deploy website changes
- Add photo of myself to About section
- Test mobile responsiveness
- Submit test order through form
- Prep Nextdoor post in drafts

### Post-Launch
- Gallery page (JSON-driven grid)
- Simplify vendor catalog modal
- Business cards (Avery cardstock + keychain combo)
- First real customer testimonial
- Instagram setup

---

## Related Notes
- [[3D Print Shoppe - Session Notes 2024-12-05]]
- [[3D Print Shoppe - Marketing Strategy]]



---

## Session Update: 2024-12-09

### Quick Context
- **Stage:** Launched on Nextdoor, website needs lead capture fixes
- **Next Action:** Website flow redesign for better lead conversion
- **Next Marketing:** Monday "Prints of the Week" post

### Completed Today
- [x] Nextdoor business page bio created
- [x] First "relaunch" post published

### New Pending Tasks
- [ ] Redesign homepage: problem-first CTA
- [ ] Create "Tell me what you need" intake form
- [ ] Demote MakerWorld catalog to secondary
- [ ] Monday: "Prints of the Week" post
- [ ] MakerWorld walkthrough video

### Key Decisions
- Problem-first: visitors describe need → [owner] recommends
- Catalog = self-serve fallback, not primary path
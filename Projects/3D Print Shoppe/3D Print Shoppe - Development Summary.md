---
tags: [guide, hardening]
---
**Tag:** [[DevLog]] [[3D Print Shoppe]] [[UI/UX]] **Date:** 2025-12-04

## 🚀 Sprint Focus: Polish & Consistency

We've focused on transforming the site from a functional prototype into a polished, service-oriented platform. The primary goal was to enhance user control, establish a consistent visual rhythm, and highlight the "neighborly" service aspect.

### ✨ Key Achievements

#### 1. Carousel Evolution (Featured Spotlight)

- **Initial State:** Hybrid auto-scrolling marquee.
- **Feedback:** Too distracting; hard to focus on individual items.
- **Solution:** Switched to a **Standard Carousel** with manual side navigation.
    - Implemented CSS `scroll-snap` for smooth, native interactions.
    - Removed auto-play to give users agency.
    - _Takeaway:_ Auto-scroll is great for ambiance (see Testimonials) but bad for detailed product browsing.

#### 2. Visual Rhythm & "The 8rem Rule"

- **Problem:** Inconsistent padding made sections feel disconnected.
- **Fix:** Established a strict global spacing system.
    - **Desktop:** `8rem` padding / `4rem` header margins.
    - **Mobile:** `4rem` padding.
- **Impact:** The site now has a professional, intentional vertical flow.

#### 3. "About Me" Prominence

- scaled up the typography (Title: 3.5rem) and layout (Max-width: 900px).
- _Why:_ To reinforce the "Neighbor with a Printer" identity and build trust immediately.

#### 4. Social Proof (Testimonials)

- Implemented an **Infinite Marquee** for customer quotes.
- Used **Glassmorphism** styling to keep the section feeling lightweight and ambient.
- _Contrast:_ Unlike product cards, continuous motion works here to suggest a stream of happy customers.

#### 5. Layout Hardening

- **Card Footers:** Fixed an issue where long prices (e.g., "$15/module") overlapped buttons on desktop. Switched to a vertical stack layout for robustness.
- **Vendor Modal:** Refined the "Launchpad" pattern to clearly guide users off-site to catalogs.

---

## 🧠 Key Learnings

1. **Agency vs. Ambience:**
    
    - Give users **control** when they need to make decisions (viewing products).
    - Use **animation** (auto-scroll) for passive confirmation (testimonials).
2. **Vertical Rhythm equates to Quality:**
    
    - Users may not notice "8rem padding" explicitly, but they _feel_ the consistency. It marks the difference between a template and a tailored design.
3. **The "Desktop overlap" Trap:**
    
    - Mobile often forces simple stacks, which work well. Desktop introduces horizontal space that can lead to awkward overlaps (like the price/button issue) if not constrained or allowed to wrap/stack.

## ⏭️ Next Steps

- Final review of the "Custom Order" form flow.
- Content polish for product descriptions.
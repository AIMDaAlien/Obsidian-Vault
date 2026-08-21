---
tags: [payments, branding, checklist]
---
# 3D Print Shoppe - Technical Recommendations

**Created:** 2024-11-23  
**Status:** Pending Review  
**Priority:** Mixed (High/Medium/Low)  
**Related:** [[Payment Workflow]], [[Custom Order System]], [[Branding & Assets]]

---

## Critical Issues (Fix ASAP) 🔴

### 1. Payment Page Placeholder URLs

**Problem:**  
The payment page currently has placeholder URLs that will break the payment flow:
- Venmo: `https://venmo.com/u/YOUR_USERNAME`
- CashApp: `https://cash.app/$YOUR_CASHTAG`

**Impact:** Customers can't actually pay you via Venmo/CashApp  
**File:** `src/pages/payment.astro` (lines 38, 50)

**Action Items:**
- [ ] Create Venmo account (if not done)
- [ ] Create CashApp account (if not done)
- [ ] Update URLs with actual usernames
- [ ] Test deep links on both iOS and Android
- [ ] Verify fallback behavior (app not installed)

**Confidence:** 95% - This will break payment flow

---

### 2. Missing QR Code Images

**Problem:**  
Payment page references QR code images that don't exist:
- `/images/venmo-qr.png`
- `/images/cashapp-qr.png`

**Impact:** Desktop users won't be able to scan codes to pay  
**File:** `src/pages/payment.astro` (lines 34, 46)

**Action Items:**
- [ ] Generate Venmo QR code
  - **Tool:** Use Venmo app → "Scan Code" → "Show Code" → Screenshot
  - **Specs:** Square, min 300x300px, PNG format
  - **Location:** `/public/images/venmo-qr.png`
  
- [ ] Generate CashApp QR code
  - **Tool:** CashApp → Profile → "$Cashtag" → QR icon → Screenshot
  - **Specs:** Square, min 300x300px, PNG format
  - **Location:** `/public/images/cashapp-qr.png`

- [ ] Optimize images (compress without quality loss)
- [ ] Test QR codes with multiple scanning apps

**Confidence:** 100% - Images don't exist in codebase

---

## High Priority Improvements 🟠

### 3. Favicon Multi-Platform Support

**Problem:**  
Only have a single `favicon.png` file. Different platforms need different sizes for optimal display.

**Impact:**  
- iOS home screen icons look pixelated
- Android app drawer shows low-res icon
- Browser tabs may show blurry favicon
- PWA installation not optimized

**Action Items:**
- [ ] Generate multiple favicon sizes:
  - `favicon.ico` (16x16, 32x32, 48x48 multi-size)
  - `favicon-16x16.png`
  - `favicon-32x32.png`
  - `favicon-192x192.png` (Android)
  - `favicon-512x512.png` (Android/iOS)
  - `apple-touch-icon.png` (180x180)

- [ ] Add to HTML `<head>`:
```html
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

- [ ] Create `site.webmanifest` for PWA support

**Tool Recommendation:** Use [RealFaviconGenerator.net](https://realfavicongenerator.net/) - uploads one image, generates all sizes

**Confidence:** 85% - Best practice for modern web apps

---

### 4. Automated Quote Email Workflow

**Problem:**  
Currently manual process to send quote + payment link to customers. This is time-consuming and error-prone.

**Impact:**
- Slow response time (customers might lose interest)
- Manual work doesn't scale
- Risk of forgetting payment link in email
- Inconsistent messaging

**Proposed Solution:**

**Option A: Email Template System (Low-tech)**
- Create saved Gmail templates with placeholders
- Template includes: greeting, quote details, pricing breakdown, payment link, FAQ
- Copy/paste/customize for each order
- **Pros:** Free, simple, no coding
- **Cons:** Still manual, prone to errors

**Option B: Formspree Autoresponder (Medium-tech)**
- Set up Formspree autoresponder on custom order form
- Customer gets immediate "We received your request" email
- Include estimated response time (24-48 hours)
- **Pros:** Instant feedback, professional
- **Cons:** Still need to manually send quote

**Option C: Zapier/Make.com Automation (High-tech)**
- Formspree submission → Trigger Zapier workflow
- Parse form data → Store in Airtable/Google Sheets
- Auto-generate PDF quote with pricing
- Send email with quote + payment link
- **Pros:** Fully automated, scalable
- **Cons:** Monthly cost ($20-30), setup time

**Recommended Approach:**
Start with **Option B** (autoresponder) now, migrate to **Option C** when you hit 10+ orders/month.

**Action Items:**
- [ ] Create email template with standard pricing structure
- [ ] Set up Formspree autoresponder
- [ ] Design quote template (PDF or HTML)
- [ ] Research automation tools (if scaling)

**Confidence:** 75% - Depends on order volume

---

### 5. Formspree Rate Limit Concerns

**Problem:**  
Formspree free tier has limits:
- 50 submissions/month
- 1 form on free plan
- No advanced features (conditional logic, A/B testing)

**Impact:**  
If you exceed limits, form submissions will fail. Customers can't contact you.

**Current Usage:**
- Custom order form: `https://formspree.io/f/your-form-id`
- Vendor quote form: `https://formspree.io/f/your-form-id`
- **That's 2 forms** - you may already be on paid plan?

**Action Items:**
- [ ] Check Formspree account tier (free vs paid)
- [ ] Set up form submission monitoring
- [ ] Create backup contact method (email fallback)
- [ ] Consider alternatives if scaling:
  - Self-hosted form handler (Web3Forms, FormBold)
  - Custom backend (Firebase, Supabase)
  - Static form alternatives (Netlify Forms, Vercel)

**Confidence:** 60% - Uncertain if this is actually a problem yet

---

## Medium Priority Enhancements 🟡

### 6. VendorCatalogModal Status Unclear

**Problem:**  
The `VendorCatalogModal.astro` component is fully implemented (971 lines) but I don't see it imported/used in main pages.

**Questions:**
- Is this feature still in use?
- Was it replaced by direct custom order flow?
- Is it for future expansion (multiple vendors)?

**Action Items:**
- [ ] Clarify if vendor catalog feature is active
- [ ] If deprecated: Remove dead code to reduce bundle size
- [ ] If active: Document integration points
- [ ] If future: Move to separate feature branch

**Confidence:** 40% - Need more context on business model

---

### 7. Payment Confirmation Feedback

**Problem:**  
After customer pays via Stripe/Venmo/CashApp, there's no confirmation page on your site. They stay on external platform.

**Impact:**
- Customer unsure if payment was successful
- No clear "next steps" (when will I get my print?)
- Missed opportunity for upselling
- Can't collect order tracking data

**Proposed Solution:**

**Option A: Stripe Webhook Integration**
- Set up Stripe webhook endpoint
- When payment succeeds → Redirect to `/order-confirmed`
- Show order details, estimated completion, contact info
- **Pros:** Real-time confirmation, professional
- **Cons:** Requires backend logic

**Option B: Manual Confirmation Email**
- Send email after verifying payment manually
- Include order number, timeline, FAQ
- **Pros:** Simple, no coding
- **Cons:** Adds manual work

**Option C: Thank You Page with Instructions**
- Create `/payment-complete` page
- Customer navigates there after paying
- Shows "Check your email for confirmation"
- **Pros:** Easy to implement
- **Cons:** Relies on customer action

**Recommended:** Start with **Option C**, upgrade to **Option A** when scaling.

**Action Items:**
- [ ] Create `/payment-complete.astro` page
- [ ] Add CTA on payment page: "After paying, click here"
- [ ] Research Stripe webhook setup (future)

**Confidence:** 70% - Improves customer experience

---

### 8. File Upload Capability

**Problem:**  
Custom order form has "I have design files" checkbox but no way to upload files.

**Current Workaround:**  
Customer checks box → You manually email them for files → They send via email/Drive

**Impact:**
- Extra back-and-forth friction
- Files might be lost in email
- No centralized file management

**Proposed Solutions:**

**Option A: Email Attachment (Current)**
- Keep checkbox, ask customers to email files
- **Pros:** Free, simple
- **Cons:** Disorganized, manual tracking

**Option B: Google Drive Upload Link**
- Create shared Drive folder per customer
- Include upload link in autoresponder email
- **Pros:** Free, organized
- **Cons:** Still requires email step

**Option C: Cloudinary/Uploadcare Widget**
- Add file upload widget to form
- Files stored in cloud (100GB free on Cloudinary)
- Submit URLs with form data
- **Pros:** Professional, streamlined
- **Cons:** Third-party dependency

**Option D: Custom Storage Integration**
- Use Supabase Storage or AWS S3
- Direct upload from form
- **Pros:** Full control, scalable
- **Cons:** Development time, potential costs

**Recommended:** Stick with **Option A** until you hit 5+ orders/week, then upgrade to **Option C**.

**Action Items:**
- [ ] Document file upload process in autoresponder
- [ ] Create file naming convention (customer-name_project-name_date)
- [ ] Research Cloudinary integration (future)

**Confidence:** 65% - Not urgent but improves UX

---

## Low Priority / Nice-to-Have 🟢

### 9. PayPal Integration

**Rationale:**  
Some customers prefer PayPal over credit cards or P2P apps. Adding it increases payment options.

**Pros:**
- Widely trusted payment method
- Buyer/seller protection built-in
- International customers (if you expand)

**Cons:**
- Higher fees than Venmo/CashApp (2.9% + $0.30)
- Adds complexity to payment page UI
- Another account to manage

**Action Items:**
- [ ] Research customer payment preferences (ask in form?)
- [ ] Calculate fee impact on $10 deposit (~$0.59/transaction)
- [ ] If justified: Set up PayPal business account
- [ ] Add PayPal button to payment page
- [ ] Test integration

**Confidence:** 50% - Low priority unless customers request it

---

### 10. Open Graph / Social Media Preview

**Problem:**  
When sharing site links on social media, preview may show generic/incorrect info.

**Impact:**
- Less appealing shares on Facebook/Twitter/Nextdoor
- Missed marketing opportunity
- Unprofessional appearance

**Action Items:**
- [ ] Create Open Graph preview image (1200x630px)
- [ ] Add meta tags to base layout:
```html
<meta property="og:title" content="3D Print Shoppe">
<meta property="og:description" content="Custom 3D printing in [local area], VA">
<meta property="og:image" content="/og-image.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
```
- [ ] Test with [Open Graph Debugger](https://www.opengraph.xyz/)

**Confidence:** 60% - Good for marketing, not critical

---

### 11. Order Tracking System

**Future Enhancement:**  
Let customers check order status online (Submitted → Quoted → Paid → Printing → Ready → Completed)

**Why Later:**
- Requires database (orders, statuses, customer accounts)
- Authentication system needed
- Significant development time
- Not necessary until 20+ orders/month

**Action Items:**
- [ ] Document order status workflow manually (spreadsheet)
- [ ] Re-evaluate when hitting scale threshold
- [ ] Research tools: Airtable, Notion, custom build

**Confidence:** 40% - Premature optimization

---

## Questions for Clarification ❓

### A. VendorCatalogModal Usage
**Context:** Found complex modal component but unsure of integration status.  
**Question:** Are you partnering with other creators/designers? Is this feature active or planned?

### B. Current Order Volume
**Context:** Need to know scale to prioritize automation.  
**Question:** How many custom orders are you getting per week/month?

### C. Email Workflow Preferences
**Context:** Multiple automation options available.  
**Question:** Would you prefer quick manual templates or invest time in full automation?

### D. Budget for Tools
**Context:** Some solutions (Zapier, Cloudinary) have costs.  
**Question:** What's your monthly budget for business tools/subscriptions?

---

## Next Session Action Plan

**Immediate (Do Today):**
1. Update payment page URLs (Venmo/CashApp)
2. Generate QR codes and add to `/public/images/`
3. Test payment flow end-to-end on mobile

**This Week:**
4. Create email template for quotes
5. Set up Formspree autoresponder
6. Generate multi-size favicons

**This Month:**
7. Create payment confirmation page
8. Document file upload workflow
9. Add Open Graph tags

**Future Backlog:**
10. Research automation tools (if scaling)
11. Consider PayPal integration (if requested)
12. Plan order tracking system (if needed)

---

**Tags:** #recommendations #technical-debt #roadmap #priorities #action-items
# Payment Workflow

**Last Updated:** 2024-11-23  
**Related:** [[Custom Order System]], [[Branding & Assets]], [[Project - Current State]]

---

## Overview

The payment system uses a **post-quote deposit model** where customers don't pay anything upfront when submitting a custom order request. After reviewing the project, you send them a personalized quote and a link to the payment page where they can secure their order with a $10 deposit.

---

## User Flow

1. **Customer submits request** via [[Custom Order System]] form
   - No payment required at this stage
   - Form collects project details, color preferences, timeline, budget

2. **Admin reviews and sends quote**
   - You manually review the request
   - Send custom quote via email with pricing breakdown
   - Include link to `/payment` page for deposit

3. **Customer pays deposit**
   - Customer visits `/payment` (Digital Cash Register)
   - Three payment options available:
     - **Stripe:** Credit/debit card via Payment Link
     - **Venmo:** QR code or mobile deep link
     - **CashApp:** QR code or mobile deep link
   - $10 deposit secures their spot in the queue

---

## Technical Implementation

### Payment Page (`/payment`)

**File:** `src/pages/payment.astro`  
**Theme:** High-contrast dark mode for better visibility  
**Design:** Ambient tech aesthetic with card-based layout

#### Payment Options

**1. Stripe (Credit Card)**
- **Link:** `https://buy.stripe.com/3cIaEQ1pp1007Qsg7M6J200`
- **Implementation:** Direct link in full-width button
- **Button text:** "Pay $10 with Credit Card"
- **Opens in:** New tab with `target="_blank"`

**2. Venmo**
- **QR Code:** `/images/venmo-qr.png`
- **Deep Link:** `https://venmo.com/u/YOUR_USERNAME`
- **Mobile behavior:** "Tap to Open Venmo" button triggers deep link
- **Desktop behavior:** QR code for scanning with mobile device

**3. CashApp**
- **QR Code:** `/images/cashapp-qr.png`
- **Deep Link:** `https://cash.app/$YOUR_CASHTAG`
- **Mobile behavior:** "Tap to Open CashApp" button triggers deep link
- **Desktop behavior:** QR code for scanning with mobile device

#### Design Decisions

**Excluded Payment Methods:**
- ❌ **Zelle** - Intentionally excluded (reasons: fraud concerns, no buyer protection)

**Color Scheme:**
- Background: `#0f1014` (dark)
- Card background: `#1a1c23`
- Stripe: `#635bff` (brand color)
- Venmo: `#008cff` (brand color)
- CashApp: `#00d632` (brand color)

**Responsive Behavior:**
- Desktop: 3-column grid layout
- Mobile: Stacked vertical layout
- Stripe button spans full width on mobile for prominence

---

## Deep Link Implementation

### How Mobile Deep Links Work

When a user clicks a payment button on their phone, the browser attempts to open the corresponding app:

```html
<!-- Venmo Deep Link -->
<a href="https://venmo.com/u/YOUR_USERNAME" target="_blank">
  On Mobile? Tap to Open Venmo
</a>

<!-- CashApp Deep Link -->
<a href="https://cash.app/$YOUR_CASHTAG" target="_blank">
  On Mobile? Tap to Open CashApp
</a>
```

**Fallback behavior:**
- If app not installed → Opens web version in browser
- Desktop users → See QR codes for scanning with their phones

---

## Security Considerations

- All payment links use HTTPS
- `rel="noopener noreferrer"` prevents reverse tabnabbing
- No payment data stored locally
- Stripe handles PCI compliance for card payments
- Venmo/CashApp provide their own fraud protection

---

## Future Enhancements

**Potential additions:**
- [ ] PayPal integration
- [ ] Apple Pay / Google Pay support
- [ ] Automated quote-to-payment email workflow
- [ ] Payment confirmation webhook integration
- [ ] Order tracking system

---

**Tags:** #payment #stripe #venmo #cashapp #workflow #e-commerce
# Custom Order System

**Last Updated:** 2024-11-23  
**Related:** [[Payment Workflow]], [[Filament Inventory]], [[Branding & Assets]]

---

## Overview

The custom order form is the primary entry point for customers requesting personalized 3D prints. It's been streamlined to focus on project requirements rather than payment, which now happens separately via the [[Payment Workflow]].

---

## Form Architecture

**File:** `src/pages/custom-order.astro`  
**Submission:** Formspree (`https://formspree.io/f/your-form-id`)  
**Success redirect:** `/thank-you`  
**Layout:** Two-column grid (form + info sidebar)

---

## Form Fields

### Required Fields

1. **Your Name** (`Customer_Name`)
   - Text input
   - Placeholder: "John Doe"

2. **Email** (`email`)
   - Email validation
   - Auto-populated in `_cc` field (customer gets copy of submission)

3. **Phone** (`phone`)
   - Tel input
   - Placeholder: "(555) 123-4567"

4. **Project Description** (`Project_Description`)
   - Textarea (6 rows, expandable)
   - Prompt: "Describe what you'd like me to create. Include dimensions, purpose, and any specific requirements..."

5. **Quantity** (`Quantity`)
   - Number input (min: 1, default: 1)

### Optional Fields

6. **Project Name** (`Project_Name`)
   - Text input
   - Helps identify the project internally

7. **Project Type** (`Project_Type`)
   - Dropdown select:
     - Standard Print
     - Multi-Color Print
     - Photo to 3D Print (HueForge)
     - Custom Design

8. **Preferred Colors**
   - Uses `<FilamentSelector>` component
   - Pulls from [[Filament Inventory]] (`/src/data/filaments.json`)
   - Allows multiple color selection

9. **Request a Specific Color** (`Request_Color`) ⭐ **NEW FIELD**
   - Text input
   - Placeholder: "navy blue, gold, sparkly black etc..."
   - Purpose: For colors not in the standard inventory
   - Example use cases:
     - Custom Pantone matches
     - Specialty filaments (glow-in-dark, wood-fill, silk)
     - Exact color descriptions

10. **Desired Completion Date** (`Desired_Completion_Date`)
    - Date picker

11. **Budget Range** (`Budget_Range`)
    - Dropdown select:
      - Under $30
      - $30 - $50
      - $50 - $100
      - $100 - $200
      - $200 - $500
      - $500+

12. **Additional Notes** (`Additional_Notes`)
    - Textarea (4 rows, expandable)
    - Prompt: "Any other details I should know?"

13. **Has Files** (`Has_Files`)
    - Checkbox
    - Label: "I have design files or reference images to share"
    - Note: Doesn't handle file upload (handled separately via email/Drive)

---

## Major Changes in Refactor

### ❌ Removed: Deposit Payment Section

**Previous behavior:**
- Form included payment option buttons (Stripe, Venmo, CashApp, Zelle)
- Customer expected to pay $10 deposit *before* receiving quote
- Created friction in conversion funnel

**New behavior:**
- Payment removed from form entirely
- Customer submits request for free
- Admin sends personalized quote + payment link
- Customer pays only after agreeing to terms

**Business rationale:**
- Lower barrier to entry (no commitment before knowing price)
- Allows for custom pricing based on complexity
- Better customer experience (no surprises)
- Reduces abandoned carts from sticker shock

### ✅ Added: "Request a Specific Color" Field

**Implementation:**
```astro
<div class="form-group">
  <label for="requestColor" class="form-label">
    Request a Specific Color
  </label>
  <input
    type="text"
    id="requestColor"
    name="Request_Color"
    class="form-input"
    placeholder="navy blue, gold, sparkly black etc..."
  />
</div>
```

**Purpose:**
- Captures non-standard color requests
- Useful when customer wants something outside the standard palette
- You can assess feasibility and price accordingly

---

## Info Sidebar

### Simplified 3-Step Process

**Previous version:** Longer explanatory text  
**Current version:** Concise numbered list

1. **Send us your file**
   - Upload your model or describe your idea.

2. **We email you a price**
   - I'll review and send you a custom quote.

3. **You pay a $10 deposit to start**
   - Secure your slot and we begin printing.

### Additional Info Sections

**Design Services:**
- Custom 3D modeling available
- Modifications to existing designs
- Prototype development
- Multiple color options

**Typical Lead Times:**
- Simple designs: 1-3 days
- Custom modeling: 3-7 days
- Complex projects: 1-2 weeks
- Rush orders: Available (extra fee)

---

## Form Validation

### Client-Side Validation (JavaScript)

**Required field checks:**
- Customer Name (must be non-empty)
- Email (must match regex: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`)
- Project Description (must be non-empty)
- Quantity (must be ≥ 1)

**Error handling:**
```javascript
function showError(message: string) {
  if (errorMessage) errorMessage.textContent = message
  if (formError) {
    formError.style.display = 'flex'
    formError.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
  }
}
```

**Error UI:**
- Red container with error icon
- Smooth scroll to error message
- Material Design 3 error colors (`var(--md-sys-color-error-container)`)

---

## Formspree Integration

### Hidden Fields

- `_next`: `/thank-you` (success redirect)
- `_subject`: "New Custom Order Request"
- `_cc`: Mirrors the customer's email (they get a copy)

### Auto-sync Email CC

```javascript
const emailInput = document.getElementById('email') as HTMLInputElement
const ccInput = document.getElementById('cc-input') as HTMLInputElement

if (emailInput && ccInput) {
  emailInput.addEventListener('input', () => {
    ccInput.value = emailInput.value
  })
}
```

**Why this matters:**
- Customer receives immediate confirmation
- Creates paper trail for both parties
- No additional backend logic required

---

## Accessibility Features

- Semantic HTML structure (`<section>`, `<form>`, etc.)
- ARIA labels (`aria-labelledby`, `aria-expanded`)
- Screen reader only text (`.sr-only` class)
- Proper label/input associations
- Focus states with visible outlines
- High contrast error messages
- Touch-friendly target sizes (min 48x48px)

---

## Future Enhancements

**Potential additions:**
- [ ] Real-time price estimation based on dimensions
- [ ] Direct file upload (integrate with cloud storage)
- [ ] Live chat for questions during form fill
- [ ] Save draft functionality (local storage)
- [ ] Multi-step wizard for complex projects
- [ ] Photo upload for HueForge projects

---

**Tags:** #custom-order #form #formspree #ux #validation
# Matrix-Decode Privacy Filter Implementation

> **Tags**: #web-development #privacy #animation #javascript #css #github-pages #portfolio
> **Related**: [[Github Pages Setup]] | [[Development Tools]] | [[About Me Draft]]
> **Status**: ✅ Implemented & Deployed

A privacy-first approach to displaying sensitive contact information with a declassification animation inspired by redacted government documents.

## Overview

This implementation auto-redacts email addresses and phone numbers in a contact section, revealing them through a 1-second matrix-style decoding animation on hover. The effect re-secures information when the user moves away.

## Key Features

- **Auto-redaction on page load** - No toggle button needed, privacy-first by default
- **Matrix decoding animation** - Random characters cycle through before revealing actual content
- **CLASSIFIED stamp overlay** - Red stamp on black bars for authentic redacted document feel
- **Hover-to-reveal** - 1000ms declassification with periwinkle scanner effect
- **Re-securing on leave** - Information fades back to redacted state
- **Targeted scope** - Only affects simple contact info, not forms or inputs

## Implementation

### File Structure

```
portfolio/
├── index.html              # Main HTML with contact section
├── terminal.js             # Privacy filter logic with matrix decode
└── terminal-privacy.css    # Redaction styling
```

### HTML Setup

Add CSS and JS links to your index.html:

```html
<head>
  <!-- Other stylesheets -->
  <link rel="stylesheet" href="terminal-privacy.css">
</head>
<body>
  <!-- Your content -->
  <script src="script.js" defer></script>
  <script src="terminal.js" defer></script>
</body>
```

Contact section structure:

```html
<section id="contact" class="content-section">
  <h2 class="section-title">Get In Touch</h2>
  <div class="contact-info">
    <p>Email: <a href="mailto:your.email@gmail.com">your.email@gmail.com</a></p>
    <p>Phone: <a href="tel:555-123-4567">555-123-4567</a></p>
    <p>GitHub: <a href="https://github.com/username">username</a></p>
  </div>
</section>
```

### JavaScript Implementation

Core logic handles auto-redaction and matrix decoding:

```javascript
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    applyContactRedactions();
  }, 500);

  function applyContactRedactions() {
    const contactSection = document.querySelector('#contact .contact-info');
    if (!contactSection) return;
    
    if (!contactSection.dataset.originalHtml) {
      contactSection.dataset.originalHtml = contactSection.innerHTML;
    }
    
    // Redact emails
    contactSection.innerHTML = contactSection.innerHTML.replace(
      /([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/g,
      '<span class="redacted" data-content="$1">[REDACTED EMAIL]</span>'
    );
    
    // Redact phones
    contactSection.innerHTML = contactSection.innerHTML.replace(
      /\b(\d{3}[-.]?\d{3}[-.]?\d{4})\b/g,
      '<span class="redacted" data-content="$1">[REDACTED PHONE]</span>'
    );
    
    document.querySelectorAll('#contact .redacted').forEach(element => {
      element.addEventListener('mouseenter', revealOnHover);
      element.addEventListener('mouseleave', hideOnLeave);
    });
  }

  function revealOnHover(e) {
    const element = e.target;
    const originalContent = element.getAttribute('data-content');
    
    if (originalContent && !element.classList.contains('revealed')) {
      element.classList.add('revealing');
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@.-_';
      const contentLength = originalContent.length;
      let iterations = 0;
      const maxIterations = 20;
      
      const interval = setInterval(() => {
        element.textContent = originalContent
          .split('')
          .map((char, index) => {
            if (index < iterations) {
              return originalContent[index];
            }
            return chars[Math.floor(Math.random() * chars.length)];
          })
          .join('');
        
        iterations += contentLength / maxIterations;
        
        if (iterations >= contentLength) {
          clearInterval(interval);
          element.textContent = originalContent;
          element.classList.remove('revealing');
          element.classList.add('revealed');
        }
      }, 50);
    }
  }

  function hideOnLeave(e) {
    const element = e.target;
    if (element.classList.contains('revealed')) {
      element.style.transition = 'all 0.3s ease-out';
      element.style.opacity = '0.5';
      
      setTimeout(() => {
        element.classList.remove('revealed');
        const content = element.getAttribute('data-content');
        element.textContent = content.includes('@') ? 
          '[REDACTED EMAIL]' : '[REDACTED PHONE]';
        element.style.opacity = '1';
      }, 300);
    }
  }
});
```

### CSS Styling

```css
.redacted {
  background: #000;
  color: transparent;
  padding: 0.2rem 0.5rem;
  position: relative;
  display: inline-block;
  cursor: help;
  transition: all 0.5s ease;
  border-radius: 2px;
  user-select: none;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.1);
}

.redacted::before {
  content: '';
  position: absolute;
  left: 0; top: 0;
  width: 100%; height: 100%;
  background: repeating-linear-gradient(90deg, #000 0px, #000 3px, #1a1a1a 3px, #1a1a1a 6px);
  opacity: 1;
  border-radius: 2px;
  z-index: 1;
}

.redacted::after {
  content: 'CLASSIFIED';
  position: absolute;
  left: 50%; top: 50%;
  transform: translate(-50%, -50%) rotate(-15deg);
  font-size: 0.6rem;
  font-weight: 800;
  color: rgba(255, 0, 0, 0.3);
  letter-spacing: 2px;
  z-index: 2;
  text-shadow: 0 0 3px rgba(255, 0, 0, 0.5);
}

.redacted.revealing {
  animation: declassify 1s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Courier New', monospace;
  letter-spacing: 1px;
  color: #a790dd;
  text-shadow: 0 0 5px rgba(167, 144, 221, 0.5);
}

@keyframes declassify {
  0% { filter: brightness(1); }
  50% {
    filter: brightness(2) contrast(1.5);
    box-shadow: 0 0 20px rgba(167, 144, 221, 0.6);
  }
  100% { filter: brightness(1); }
}

.redacted.revealed {
  background: linear-gradient(145deg, #a790dd, #8b6bb8);
  color: white;
  padding: 0.2rem 0.5rem;
  box-shadow: 0 0 15px rgba(167, 144, 221, 0.4);
}

.redacted.revealed::before,
.redacted.revealed::after {
  display: none;
}
```

## Configuration

### Decode Speed
- `maxIterations`: Number of cycles (default: 20)
- `setInterval` delay: Update frequency (default: 50ms)
- Total time = 20 × 50ms = 1000ms

### Character Set
```javascript
const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@.-_';
```

### Colors
- `#a790dd` - Periwinkle
- `#8b6bb8` - Lavender
- Adjust for your theme

## Important Notes

### Scope Control
The selector `#contact .contact-info` prevents interference with forms and other interactive elements.

### Timing
500ms delay allows page to render before applying redactions.

### GitHub Pages Deploy
See [[Github Pages Setup]] for complete deployment instructions.

1. Ensure editing `index.html` (not backup files)
2. Check Settings → Pages → Branch set to `main`
3. Verify commit pushed: `git log origin/main --oneline`
4. Hard refresh after deploy: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R`

## Testing Checklist

- [ ] Black bars show on page load
- [ ] CLASSIFIED stamp visible
- [ ] Hover triggers matrix animation
- [ ] Characters cycle randomly
- [ ] Reveals with periwinkle background
- [ ] Re-secures on mouse leave
- [ ] Doesn't affect other elements

## Browser Support

Chrome 120+, Firefox 120+, Safari 17+, Edge 120+

Requires CSS animations, clip-path, ES6 JavaScript

## Related Development Tools

For Git workflow and troubleshooting, see:
- [[Git Push Conflict Troubleshooting]] - Common deployment issues
- [[Development Tools]] - Complete Git command reference

---

*Created: October 2025*
*Last Updated: October 2025*
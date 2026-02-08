---
garden_path: Projects/Teardown Cafe/Documentation/Deployment Guide.md
last_published: '2025-11-28T19:46:59.816145'
published_to_garden: true
---

## Custom Domain Setup (your-project.com)

### Purchasing Domain
- Registrar: Hostinger
- Domain: your-project.com
- Cost: ~$30/year for .cafe TLD

### DNS Configuration
1. **Hostinger DNS Settings:**
   - Navigate to Domain Management → DNS/Name Servers
   - Delete existing A record (parking page IP)
   - Add new A record:
     - Type: A
     - Name: @ (root domain)
     - Content: 216.198.79.1 (Vercel's IP)
     - TTL: 3600

2. **Verify DNS propagation:**
   ```bash
   dig your-project.com
   # Should show 216.198.79.1 in ANSWER SECTION
   ```

3. **Vercel Settings:**
   - Project Settings → Domains
   - Add your-project.com
   - Vercel shows DNS instructions
   - Wait 5-30 minutes for propagation

### Making Site Public
**Critical:** Disable Vercel's deployment protection

1. Vercel Dashboard → Project → Settings
2. Deployment Protection → Set to "Disabled"
3. Without this, site requires Vercel login to view

### Optional Enhancements
- **www redirect:** Add CNAME for www.your-project.com → your-project.com
- **DNSSEC:** Enable in Hostinger for security (optional)
- **SSL:** Auto-provisioned by Vercel (Let's Encrypt)

---
*Updated: October 23, 2025*
# Website Rebuild - November 2025

## Context
Complete site overhaul from static catalog to service-based model with MakerWorld collection integration.

## Key Decisions

### Architecture
- **Fresh start**: Wiped existing repo, rebuilt from scratch
- **Stack**: Astro 4.x + Material Web 2.x + Formspree
- **Deployment**: Vercel with aim3dprints.com
- **No catalog**: Link to MakerWorld collection, quote-based pricing

### Why Service Model
- **MakerWorld can't be embedded**: No API, no iframe, ToS prohibits scraping
- **Variable pricing needed**: Size/color/complexity makes fixed prices impractical
- **Flexibility**: Handles catalog items, custom STLs, and image-to-3D

### Pricing Strategy
- **Transparent ranges**: Small $12-20, Medium $20-35, Large $35-60
- **Live calculator**: Shows estimate based on size selection
- **24hr quotes**: Final price via email after review

## Technical Implementation

### Subagent Architecture
Created 5 specialized agents in `.claude/agents/`:
1. **astro-architect**: Project structure, routing, build config
2. **material-web-specialist**: M3 Expressive styling, brand tokens
3. **form-integration-engineer**: Quote form + price calculator
4. **deployment-engineer**: Vercel deployment, DNS, optimization
5. **image-generation-specialist**: AI product images (Leonardo.ai/Ideogram)

Each agent has WebSearch enabled to use latest 2025 documentation.

### Brand Tokens
- Primary: #6366F1 (periwinkle)
- Secondary: #A78BFA (lavender)
- Tertiary: #10B981 (green)
- Font: Ubuntu
- Corners: 24-28px (M3 Expressive)

### Site Structure
```
/               → Homepage (hero, 8 product cards, how it works)
/quote          → Quote form (order type, size, calculator, contact)
```

### Quote Form Logic
- **Order types**: MakerWorld link, STL upload, or image-to-3D
- **Conditional fields**: Show/hide based on radio selection
- **Live calculator**: Updates estimate on size change (client-side JS)
- **Formspree backend**: Posts to user's Formspree account

## AI Tools Used
- **Claude Code**: Main orchestration, subagent execution
- **Gemini CLI**: Small edits after Claude limits
- **Gemini Web**: Visual troubleshooting
- **Cursor AI**: Optional for code iteration

## Next Steps
1. Generate 8 product images (AI-generated)
2. Set up Formspree account, add form ID
3. Deploy to Vercel production
4. Configure aim3dprints.com DNS
5. Update Nextdoor post with link

## Timeline
- Started: Nov 16, 2025
- Target live: Nov 17, 2025 afternoon
- Estimated: 6-8 hours total work

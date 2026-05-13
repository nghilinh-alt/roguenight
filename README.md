# Rogue Night

The full source-of-truth repository for **Rogue Night PTY LTD** (ABN 31 633 650 334) — an Australian consulting practice that helps small to medium businesses identify the right tools and deploy AI agents and digital employees.

Live: [roguenight.com.au](https://roguenight.com.au) (hosted on Cloudflare Pages, auto-deployed from this repo's `main` branch; the same Cloudflare account routes `/api/*` to a Worker for the Pay-Later flow).

---

## What's in this repo

```
roguenight/
├── public/              # Production-ready website files. Auto-deployed by Cloudflare Pages on every push to main.
│   ├── index.html             # Landing page
│   ├── privacy/index.html     # /privacy
│   ├── terms/index.html       # /terms
│   ├── thank-you/index.html   # /thank-you — post-Tally landing, Pay Now / Pay Later
│   ├── confirmation/index.html # /confirmation — post-Stripe-success
│   ├── 404.html
│   ├── og-image.png · favicon.svg · apple-touch-icon.png · logo-stacked.png
│   ├── health-check-sample.pdf
│   ├── robots.txt · sitemap.xml · .htaccess
│
├── src/                 # Python build scripts (Pillow + numpy)
│   ├── build_all.py           # Convenience runner — builds everything for production
│   ├── build_landing.py · build_privacy.py · build_terms.py · build_404.py
│   ├── build_thank_you.py · build_confirmation.py
│   ├── build_og_image.py · build_apple_touch_icon.py
│   └── data/                  # Base64 logos, fonts, sample thumbnails
│
├── cloudflare-worker/   # Worker source for /api/pay-later
│   ├── worker-pay-later.js    # Creates Stripe Invoice on Pay-Later click
│   ├── wrangler.toml          # Worker config + route binding
│   └── README.md              # Deployment walkthrough
│
├── agents/              # Agents, skills, system prompts (source of truth)
│   ├── README.md              # How agents and skills relate to Hyperagent
│   ├── lois/                  # The named strategy report-writing agent
│   ├── dhc-report-writer/     # Skill — drafts a strategy report from one Airtable Response
│   └── stack-md-maintainer/   # Skill — keeps stack.md and Airtable Tools in sync
│
├── catalogue/           # The vetted tool catalogue
│   └── stack.md               # 48 rows across 12 categories, the canonical source
│
├── docs/                # Operations and architecture documentation
│   ├── BRAND-KIT.md           # Phase 1 colours, type, voice
│   ├── DEPLOYMENT-GUIDE.md    # Cloudflare Pages auto-deploy + Cloudflare Worker setup
│   ├── EMAIL-TEMPLATES.md     # Standard customer email bodies
│   ├── OG-METADATA.md         # Open Graph spec
│   ├── PAYMENT-FLOW.md        # Tally → Stripe architecture + walkthrough
│   ├── operations/
│   │   ├── AIRTABLE-SCHEMA.md      # Live Airtable base schema (Responses, Tools, Recommendations, Reports)
│   │   ├── QUESTIONNAIRE.md        # Tally form spec + Airtable field mapping
│   │   ├── STACK-AUDIT-2026-05-13.md  # Audit findings + resolution
│   │   ├── OPS-INDEX.md            # Map of what lives where (Hyperagent vs Airtable vs this repo)
│   │   └── VOICE-RULES.md          # Locked Phase 1 voice rules
│   └── reports/
│       └── README.md          # Where per-client report templates and outputs live (not here)
│
└── assets-raw/          # Source logos, raw sample PDF, photographic assets
```

---

## Editing the website

HTML files in `public/` are **outputs**, not edited directly. Source-of-truth lives in `src/build_*.py` scripts that emit self-contained HTML with base64-embedded images.

### Standard workflow

```bash
cd src/
# Edit copy / styling in the relevant build_*.py
python3 build_all.py
```

`build_all.py` builds the OG image, apple-touch-icon, all six HTML pages (production mode), and stages everything into `public/`. Commit and push `public/` to `main` — Cloudflare Pages auto-builds and deploys within 30-60 seconds.

See [`docs/DEPLOYMENT-GUIDE.md`](docs/DEPLOYMENT-GUIDE.md) for the deploy flow.

### Sample report PDF swap

When a new sample report PDF is ready, follow the steps in `docs/DEPLOYMENT-GUIDE.md` (regenerate page-1 thumbnail, encode as base64, update `src/build_landing.py` constants).

---

## Deploying the payment flow

Tally → Stripe payment flow architecture is documented in [`docs/PAYMENT-FLOW.md`](docs/PAYMENT-FLOW.md). The Cloudflare Worker deployment is in [`cloudflare-worker/README.md`](cloudflare-worker/README.md).

Quick summary:

1. **Stripe Dashboard** — brand it, create Payment Link for A$880, configure Invoicing reminders (custom domain `pay.roguenight.com.au` skipped — `buy.stripe.com` URL is fine)
2. **Cloudflare Pages** — auto-deploys `public/` from `main`. No manual upload step.
3. **Cloudflare Worker** — deploy `cloudflare-worker/worker-pay-later.js`, set Stripe secrets, wire `roguenight.com.au/api/*` route
4. **Tally** — configure redirect with `@variable` params (email, name, business, ref)
5. **End-to-end test** in Stripe test mode (3 scenarios in PAYMENT-FLOW.md)

---

## Agents and skills

This repo holds the **source of truth** for Rogue Night's named agent (Lois) and her supporting skills. The agents and skills themselves live in the Hyperagent platform — this repo is the version-controlled mirror.

### Agents

- **[`agents/lois/`](agents/lois/)** — Lois, the strategy report-writing agent. Calm, exact, editorial. Drafts reports from Airtable Responses; never auto-sends.

### Skills

- **[`agents/dhc-report-writer/`](agents/dhc-report-writer/)** — Methodology + scripts for turning one Airtable Response into a populated strategy report (HTML + PDF). Mirrors the v5 HTML template and v1.3 Airtable schema.
- **[`agents/stack-md-maintainer/`](agents/stack-md-maintainer/)** — Keeps `catalogue/stack.md` and the Airtable Tools table in sync. Proposes patches after each report.

See [`agents/README.md`](agents/README.md) for the relationship between this repo and Hyperagent.

---

## The vetted tool catalogue

[`catalogue/stack.md`](catalogue/stack.md) is the canonical source of the 48-row vetted tool list. The Airtable Tools table (`appCLdTCbJ5zGe9fo/tblNDMmrH2zS8JR5K`) mirrors this file.

After every strategy report, [`agents/stack-md-maintainer/`](agents/stack-md-maintainer/) proposes additions for any tool that was recommended but isn't yet catalogued. New entries default to `Linh-vetted: Pending` — promotion to `Yes` is always a human decision.

---

## Brand rules — locked, non-negotiable

These are baked into the build scripts. Don't violate them when editing copy.

### Palette
- **Ink** `#0A0E1A` — primary dark surface
- **Obsidian** `#050608` — footer, deepest contrast
- **Signet Gold** `#C9A961` — primary accent, italic emphasis
- **Ember** `#C2410C` — primary CTAs, hot moments
- **Parchment** `#EDE8DD` — body text on dark
- **Slate** `#6B7280` — captions, secondary text

### Typography
- **Instrument Serif** (Google Fonts) — display, italic accents on key words in Signet Gold
- **Instrument Sans** — body, UI, buttons, eyebrow labels
- **JetBrains Mono** — meta labels, scope tags, footer meta

### Voice — never violate
- Never write "SME" or "SMEs" → always "small to medium businesses" (lowercase) or "small business"
- Never write "AI-generated report" → always "specially curated"
- Never name the founder on the landing page
- Never write "Brisbane" → use "Australian" or specific state for legal purposes only
- Never include "Book a free 45-minute walkthrough call"
- Always lead with cheapest credible tier when discussing recommendations
- Delivery promise is "within 48 hours" (NOT 24 hours, NOT 2 business days)
- AI & Automation Strategy is **advisory only** — agent implementation is a **separate, quoted engagement**

### Cover title pattern
Italic gold accent on the punch word of every page hero. Don't break this pattern when adding new pages.

See [`docs/operations/VOICE-RULES.md`](docs/operations/VOICE-RULES.md) for the full locked list.

---

## Architecture context

The website is one piece of a larger AI & Automation Strategy pipeline. Everything else (Tally form, Airtable base, Lois, email) is documented in this repo too, under `docs/operations/`.

The pipeline:

1. Customer fills the **Tally form** at `https://tally.so/r/xX4YaG` (5-7 minute questionnaire).
2. Tally redirects to `roguenight.com.au/thank-you/?email=...&name=...&ref=...` and writes the response to the **Airtable base** `appCLdTCbJ5zGe9fo` via native integration.
3. Customer chooses **Pay Now** or **Pay Later** on the thank-you page.
4. **Lois** (the agent) drafts the strategy report from the Airtable Response using the [`dhc-report-writer`](agents/dhc-report-writer/) skill.
5. After Linh approves the draft, the report PDF is generated and Linh sends it manually from Hostinger webmail (`hello@roguenight.com.au`).
6. After each report, [`stack-md-maintainer`](agents/stack-md-maintainer/) proposes any new catalogue entries for Linh's review.

See [`docs/operations/OPS-INDEX.md`](docs/operations/OPS-INDEX.md) for a fuller map of what lives where.

---

## Help

For questions about brand voice, see [`docs/BRAND-KIT.md`](docs/BRAND-KIT.md). For SEO and Open Graph spec, see [`docs/OG-METADATA.md`](docs/OG-METADATA.md). For email templates, see [`docs/EMAIL-TEMPLATES.md`](docs/EMAIL-TEMPLATES.md). For the operations side, see [`docs/operations/OPS-INDEX.md`](docs/operations/OPS-INDEX.md).

For everything else: hello@roguenight.com.au

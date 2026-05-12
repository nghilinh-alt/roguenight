# Rogue Night Website

The public-facing website for **Rogue Night PTY LTD** (ABN 31 633 650 334) — a consulting practice that helps Australian small to medium businesses identify the right tools and deploy AI agents and digital employees.

Live: [roguenight.com.au](https://roguenight.com.au) (hosted on Hostinger).

---

## What's in this repo

```
roguenight-website/
├── public/              # Production-ready files. Upload this folder's contents to public_html.
│   ├── index.html       # Landing page
│   ├── privacy/         # /privacy → privacy policy
│   ├── terms/           # /terms → terms of service
│   ├── 404.html         # Branded "Lost in the night" 404
│   ├── robots.txt
│   ├── sitemap.xml
│   ├── og-image.png     # 1200×630 social card
│   ├── favicon.svg
│   ├── apple-touch-icon.png
│   ├── logo-stacked.png # Referenced by JSON-LD
│   ├── health-check-sample.pdf
│   └── .htaccess
├── src/                 # Build scripts (Python — Pillow + numpy required)
│   ├── build_all.py     # Convenience runner — builds everything in production mode
│   ├── build_landing.py
│   ├── build_privacy.py
│   ├── build_terms.py
│   ├── build_404.py
│   ├── build_og_image.py
│   ├── build_apple_touch_icon.py
│   └── data/
│       ├── horizontal-b64.txt
│       ├── horizontal_sm-b64.txt
│       ├── sample-thumb-b64.txt
│       └── fonts/       # Instrument Serif + Sans for OG image rendering
├── assets-raw/          # Source logos, raw sample PDF, photographic assets
└── docs/
    ├── BRAND-KIT.md
    ├── OG-METADATA.md
    └── EMAIL-TEMPLATES.md
```

---

## Editing the site

The HTML files in `public/` are **outputs**, not edited directly. Source-of-truth lives in `src/build_*.py` scripts that emit self-contained HTML with base64-embedded images.

### Standard workflow

```bash
cd src/
# Edit copy / styling in the relevant build_*.py
python3 build_all.py
```

`build_all.py` does the following:

1. Builds the OG image (`og-image.png`) and apple-touch-icon (`apple-touch-icon.png`)
2. Builds all four HTML pages with `STAGING_MODE=false` so internal links resolve to `/privacy/`, `/terms/`, `/health-check-sample.pdf` etc.
3. Stages all production-ready files in `public/`
4. Re-builds the in-memory STAGING-mode HTML so any in-thread previews stay current

You re-upload `public/` to Hostinger after every change.

### Quick edits without a Python install

If you need to change a single line of copy and don't have Python handy, you can edit the file directly in `public/index.html` (or whichever page). It's self-contained HTML. Just remember the source build script is the canonical version — note the change there too, otherwise the next `build_all.py` will overwrite your edit.

### Sample report PDF swap

When a new sample report PDF is ready:

1. Place the new PDF at `assets-raw/health-check-sample.pdf` (overwrite the existing one — same filename)
2. Regenerate the page-1 thumbnail (see `docs/THUMBNAIL-GUIDE.md` if added)
3. Encode as base64 into `src/data/sample-thumb-b64.txt`
4. Update `PDF_PAGES` and `SAMPLE_CLIENT` constants in `src/build_landing.py`
5. Copy the PDF to `public/health-check-sample.pdf`
6. Run `python3 build_all.py`

---

## Deploying to Hostinger

### One-time setup

1. **DNS:** Point `roguenight.com.au` at Hostinger nameservers via your registrar.
   - Hostinger nameservers are shown in your hPanel → Domains → Nameservers
   - Propagation takes 1–24 hours
2. **Add domain** in Hostinger hPanel → Websites → Add Website
3. **Provision SSL:** hPanel → SSL → Install free Let's Encrypt
4. **Email forwarding** (already in place — registrar-level for hello@roguenight.com.au)

### Every release

1. Open Hostinger hPanel → File Manager → `public_html/`
2. Delete the old contents (or back up to `_old/`)
3. Drag-and-drop the contents of `public/` from this repo (NOT the `public/` folder itself — its contents)
4. Hostinger File Manager preserves the folder structure (`privacy/`, `terms/`)
5. Verify in browser: `https://roguenight.com.au` then check `/privacy/`, `/terms/`, `/404.html`, and the sample PDF download

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
- Digital Health Check is **advisory only** — agent implementation is a **separate, quoted engagement**

### Cover title pattern
Italic gold accent on the punch word of every page hero. Don't break this pattern when adding new pages.

---

## Architecture context

The website is one piece of a larger Digital Health Check pipeline:

- **Tally form** at `https://tally.so/r/xX4YaG` — 5-7 minute questionnaire. After submit → Stripe Payment Link for A$350.
- **Airtable base** `appCLdTCbJ5zGe9fo` — Responses, Tools (46 vetted), Recommendations, Reports. Tally writes via native integration.
- **Lois (agent)** drafts the report from each Response. Skill: "Rogue Night DHC Report Writer".
- **Email** at `hello@roguenight.com.au` via Hostinger. Lois drafts body text; Linh copy-pastes into Hostinger webmail and attaches PDF manually.

The website only handles the **discover → book** part of that pipeline. Everything downstream of the Tally submission is wired separately.

---

## Help

For questions about brand voice, see `docs/BRAND-KIT.md`. For SEO and Open Graph spec, see `docs/OG-METADATA.md`. For email templates, see `docs/EMAIL-TEMPLATES.md`.

For everything else: hello@roguenight.com.au

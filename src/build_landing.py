#!/usr/bin/env python3
"""Build the Rogue Night landing page (v10) — AI & Automation Strategy rebrand.

Voice rules:
- Hero uses 'Australian businesses' (tighter)
- Body copy uses 'Australian small to medium businesses' (lowercase, written out)
- No 'SME' / 'SMEs'
- No 'AI-generated' (use 'specially curated')
- No founder name on the page
- 'within 48 hours' (NOT 24, NOT business days)
- No strategy call or calendar booking promise — infra not live yet
"""
import os

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_SCRIPT_DIR, 'data')

with open(os.path.join(_DATA, 'sample-thumb-b64.txt')) as f:
    THUMB_B64 = f.read().strip()
with open(os.path.join(_DATA, 'horizontal-b64.txt')) as f:
    LOGO_B64 = f.read().strip()
with open(os.path.join(_DATA, 'horizontal_sm-b64.txt')) as f:
    LOGO_SM_B64 = f.read().strip()

TALLY_URL = 'https://tally.so/r/xX4YaG'
PDF_PAGES = 18
SITE_URL = 'https://roguenight.com.au'
ABN = '31 633 650 334'
PRICE = '880'
PRICE_DISPLAY = '$880'

# MODE: 'staging' (default — absolute URLs to the live site so the in-thread
# preview works inside an iframe) or 'production' (same-origin relative paths
# for the Cloudflare Pages build).
# Switch via: STAGING_MODE=false python3 build_landing.py
STAGING_MODE = os.environ.get('STAGING_MODE', 'true').lower() != 'false'

if STAGING_MODE:
    PDF_URL = 'https://roguenight.com.au/sample-strategy.pdf'
    PRIVACY_URL = 'https://roguenight.com.au/privacy/'
    TERMS_URL = 'https://roguenight.com.au/terms/'
else:
    PDF_URL = '/sample-strategy.pdf'
    PRIVACY_URL = '/privacy/'
    TERMS_URL = '/terms/'

HTML = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Primary meta -->
<title>Rogue Night — AI &amp; Automation Strategy for Australian small to medium businesses</title>
<meta name="description" content="Rogue Night helps Australian small to medium businesses identify the right tools, eliminate wasted effort, and design AI-powered systems. AI &amp; Automation Strategy, $880 flat, in your inbox within 48 hours.">
<meta name="keywords" content="AI automation strategy Australia, AI agents small business, digital employees, small to medium business consulting, Australian AI consultant, business automation, AI implementation, tool stack audit, business optimisation plan">
<meta name="author" content="Rogue Night PTY LTD">
<meta name="theme-color" content="#0A0E1A">
<meta name="robots" content="index,follow,max-image-preview:large">

<!-- Canonical -->
<link rel="canonical" href="{SITE_URL}/">

<!-- Favicon — inline SVG for guaranteed render across hosts -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%230A0E1A'/%3E%3Ccircle cx='32' cy='32' r='14' fill='%23050608'/%3E%3Ccircle cx='32' cy='32' r='16' fill='none' stroke='%23C9A961' stroke-width='1.5' opacity='0.9'/%3E%3Ccircle cx='32' cy='32' r='20' fill='none' stroke='%23C9A961' stroke-width='0.8' opacity='0.4'/%3E%3C/svg%3E">
<link rel="apple-touch-icon" href="{SITE_URL}/apple-touch-icon.png">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Rogue Night">
<meta property="og:title" content="Rogue Night — Run your business smarter">
<meta property="og:description" content="AI &amp; Automation Strategy for Australian small to medium businesses. A custom plan to identify the right tools, eliminate wasted effort, and design AI-powered systems. $880, within 48 hours.">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:image" content="{SITE_URL}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Rogue Night — AI &amp; Automation Strategy for Australian small to medium businesses">
<meta property="og:locale" content="en_AU">

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Rogue Night — Run your business smarter">
<meta name="twitter:description" content="AI &amp; Automation Strategy for Australian small to medium businesses. $880, within 48 hours.">
<meta name="twitter:image" content="{SITE_URL}/og-image.png">
<meta name="twitter:image:alt" content="Rogue Night logo on Ink background with editorial headline">

<!-- Geographic targeting -->
<meta name="geo.region" content="AU">
<meta name="geo.placename" content="Australia">

<!-- JSON-LD structured data -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Rogue Night PTY LTD",
  "alternateName": "Rogue Night",
  "url": "{SITE_URL}/",
  "logo": "{SITE_URL}/logo-stacked.png",
  "image": "{SITE_URL}/og-image.png",
  "description": "AI & Automation Strategy and tool advisory for Australian small to medium businesses. Custom business optimisation plans, AI agent and digital employee design and implementation.",
  "slogan": "The work that runs while you sleep.",
  "email": "hello@roguenight.com.au",
  "identifier": [
    {{
      "@type": "PropertyValue",
      "propertyID": "ABN",
      "value": "{ABN}"
    }}
  ],
  "areaServed": {{
    "@type": "Country",
    "name": "Australia"
  }},
  "priceRange": "{PRICE_DISPLAY}",
  "knowsAbout": [
    "AI automation strategy",
    "AI agents",
    "Digital employees",
    "Business optimisation",
    "Tool stack advisory",
    "Small business consulting"
  ],
  "makesOffer": {{
    "@type": "Offer",
    "name": "AI & Automation Strategy",
    "price": "{PRICE}",
    "priceCurrency": "AUD",
    "availability": "https://schema.org/InStock",
    "description": "A custom business optimisation plan for small to medium businesses — assessment, tool stack redesign, priority action plan, 12-week implementation roadmap, and AI opportunity blueprint. Delivered to your inbox within 48 hours.",
    "url": "{TALLY_URL}"
  }}
}}
</script>

<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --ink: #0A0E1A;
    --obsidian: #050608;
    --gold: #C9A961;
    --ember: #C2410C;
    --parchment: #EDE8DD;
    --slate: #6B7280;
    --slate-deep: #4B5563;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    background: var(--ink);
    color: var(--parchment);
    font-family: 'Instrument Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 17px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }}

  /* Editorial typography */
  .serif {{ font-family: 'Instrument Serif', Georgia, serif; }}
  em, .italic {{ font-family: 'Instrument Serif', Georgia, serif; font-style: italic; color: var(--gold); font-weight: 400; }}
  h1, h2, h3 {{ font-family: 'Instrument Serif', Georgia, serif; font-weight: 400; letter-spacing: -0.02em; line-height: 1.05; color: var(--parchment); }}
  h1 {{ font-size: clamp(2.8rem, 7vw, 5.5rem); }}
  h2 {{ font-size: clamp(2.2rem, 5vw, 3.8rem); margin-bottom: 1rem; }}
  h3 {{ font-size: 1.6rem; line-height: 1.15; }}

  .eyebrow {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1.2rem;
  }}

  .subhead {{
    font-size: 1.15rem;
    line-height: 1.55;
    color: var(--parchment);
    opacity: 0.85;
    max-width: 60ch;
  }}

  /* Layout primitives */
  .container {{ max-width: 1200px; margin: 0 auto; padding: 0 6%; }}
  section {{ padding: 8rem 0; }}
  @media (max-width: 720px) {{ section {{ padding: 5rem 0; }} }}

  /* Brand bar */
  .brand-bar {{
    position: relative;
    padding: 1.5rem 6% 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .brand-bar a {{ text-decoration: none; }}
  .brand-logo {{ display: block; height: 56px; width: auto; }}
  .brand-bar .cta-ghost {{ font-size: 0.95rem; }}

  /* Hero */
  .hero {{
    padding: 5rem 6% 7rem;
    max-width: 1200px;
    margin: 0 auto;
  }}
  .hero h1 {{ margin: 1.5rem 0 2rem; max-width: 18ch; }}
  .hero .subhead {{ font-size: 1.3rem; max-width: 56ch; margin-bottom: 3rem; }}

  /* Buttons */
  .cta-primary {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--ember);
    color: var(--parchment);
    font-family: 'Instrument Sans', sans-serif;
    font-weight: 600;
    font-size: 1.05rem;
    letter-spacing: 0.01em;
    padding: 1.1rem 2rem;
    border: none;
    text-decoration: none;
    border-radius: 2px;
    transition: all 0.2s ease;
    cursor: pointer;
  }}
  .cta-primary:hover {{
    background: #D14E15;
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(194, 65, 12, 0.3);
  }}
  .cta-ghost {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--gold);
    font-family: 'Instrument Sans', sans-serif;
    font-weight: 500;
    text-decoration: none;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(201, 169, 97, 0.3);
    transition: all 0.2s ease;
  }}
  .cta-ghost:hover {{ color: var(--parchment); border-bottom-color: var(--gold); }}
  .cta-arrow {{ display: inline-block; transition: transform 0.2s ease; }}
  .cta-primary:hover .cta-arrow, .cta-ghost:hover .cta-arrow {{ transform: translateX(4px); }}
  .cta-support {{
    font-size: 0.92rem;
    color: var(--slate);
    margin-top: 1rem;
    letter-spacing: 0.02em;
  }}

  /* Value strip — sits between hero and trust pillars */
  .value-strip {{
    padding: 5rem 6% 5rem;
    border-top: 1px solid rgba(201, 169, 97, 0.12);
    border-bottom: 1px solid rgba(201, 169, 97, 0.12);
    background:
      radial-gradient(ellipse at 70% 50%, rgba(201, 169, 97, 0.05), transparent 65%),
      var(--obsidian);
  }}
  .value-strip .container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; }}
  .value-headline {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: clamp(1.6rem, 3vw, 2.4rem);
    line-height: 1.2;
    letter-spacing: -0.01em;
    color: var(--parchment);
    margin-bottom: 1.2rem;
  }}
  .value-headline em {{ color: var(--gold); }}
  .value-sub {{
    color: var(--parchment);
    opacity: 0.8;
    font-size: 1.05rem;
    line-height: 1.55;
    max-width: 40ch;
    margin-bottom: 0;
  }}
  .value-unlocks {{ list-style: none; padding: 0; margin: 0; }}
  .value-unlocks li {{
    display: flex;
    align-items: baseline;
    gap: 0.85rem;
    padding: 0.8rem 0;
    border-bottom: 1px solid rgba(201, 169, 97, 0.12);
    color: var(--parchment);
    font-size: 1.02rem;
    line-height: 1.4;
    opacity: 0.92;
  }}
  .value-unlocks li:last-child {{ border-bottom: none; }}
  .value-unlocks li::before {{
    content: '→';
    color: var(--gold);
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    font-size: 1.1rem;
    flex-shrink: 0;
  }}
  .value-recovery {{
    grid-column: 1 / -1;
    text-align: center;
    margin-top: 1rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(201, 169, 97, 0.12);
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: clamp(1.2rem, 2vw, 1.45rem);
    color: var(--parchment);
    opacity: 0.92;
    letter-spacing: -0.005em;
  }}
  .value-recovery em {{ color: var(--gold); }}
  @media (max-width: 880px) {{
    .value-strip .container {{ grid-template-columns: 1fr; gap: 2rem; }}
  }}

  /* Trust pillars */
  .trust {{
    background: var(--obsidian);
    padding: 4rem 0 4.5rem;
    border-top: 1px solid rgba(201, 169, 97, 0.15);
    border-bottom: 1px solid rgba(201, 169, 97, 0.15);
  }}
  .trust-lead {{
    text-align: center;
    max-width: 56ch;
    margin: 0 auto 3.5rem;
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: clamp(1.25rem, 2.2vw, 1.5rem);
    line-height: 1.45;
    color: var(--parchment);
    letter-spacing: -0.005em;
  }}
  .trust-lead em {{ color: var(--gold); }}
  .trust-lead-divider {{
    display: block;
    width: 60px;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--gold), transparent);
    margin: 0 auto 1.8rem;
  }}
  .pillars {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 3rem; }}
  .pillar {{ border-left: 2px solid var(--gold); padding-left: 1.5rem; }}
  .pillar-num {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    font-size: 1rem;
    color: var(--gold);
    margin-bottom: 0.5rem;
  }}
  .pillar-title {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 500;
    color: var(--parchment);
    line-height: 1.35;
  }}
  @media (max-width: 760px) {{
    .pillars {{ grid-template-columns: 1fr; gap: 2rem; }}
  }}

  /* Problem section */
  .pain h2 {{ margin-bottom: 4rem; max-width: 18ch; }}
  .pain-cards {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }}
  .pain-card {{
    background: var(--obsidian);
    padding: 2.5rem 2rem;
    border: 1px solid rgba(201, 169, 97, 0.18);
    border-radius: 4px;
    transition: all 0.25s ease;
  }}
  .pain-card:hover {{
    border-color: var(--gold);
    transform: translateY(-2px);
  }}
  .pain-num {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    color: var(--gold);
    font-size: 1.3rem;
    margin-bottom: 1.5rem;
    display: block;
  }}
  .pain-card h3 {{ margin-bottom: 1rem; }}
  .pain-card p {{
    color: var(--parchment);
    opacity: 0.78;
    line-height: 1.55;
    font-size: 0.98rem;
  }}
  @media (max-width: 880px) {{
    .pain-cards {{ grid-template-columns: 1fr; gap: 1.5rem; }}
  }}

  /* What we do — 5-item editorial list */
  .what-we-do {{ background: var(--obsidian); }}
  .what-we-do h2 {{ max-width: 22ch; margin-bottom: 1.5rem; }}
  .what-we-do .subhead {{ margin-bottom: 4rem; }}
  .what-we-do-includes {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 2.5rem;
  }}
  .deliverables {{ display: flex; flex-direction: column; gap: 0; }}
  .deliverable {{
    display: grid;
    grid-template-columns: 80px 1fr;
    gap: 2rem;
    align-items: baseline;
    padding: 1.8rem 0;
    border-top: 1px solid rgba(201, 169, 97, 0.13);
  }}
  .deliverable:last-child {{ border-bottom: 1px solid rgba(201, 169, 97, 0.13); }}
  .deliverable-num {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    color: var(--gold);
    font-size: 1.6rem;
    letter-spacing: 0.04em;
  }}
  .deliverable-body h3 {{ font-size: 1.4rem; margin-bottom: 0.4rem; }}
  .deliverable-body p {{
    color: var(--parchment);
    opacity: 0.78;
    line-height: 1.55;
    font-size: 0.98rem;
  }}
  .plus-strip {{
    margin-top: 3rem;
    padding: 1.5rem 1.8rem;
    border-left: 2px solid var(--gold);
    background: rgba(201, 169, 97, 0.04);
  }}
  .plus-strip .eyebrow {{ margin-bottom: 0.6rem; }}
  .plus-strip-body {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 1.2rem;
    line-height: 1.4;
    color: var(--parchment);
    margin-bottom: 0.25rem;
  }}
  .plus-strip-body em {{ color: var(--gold); }}
  .plus-strip-sub {{
    color: var(--parchment);
    opacity: 0.78;
    font-size: 0.98rem;
    line-height: 1.5;
  }}
  @media (max-width: 720px) {{
    .deliverable {{ grid-template-columns: 60px 1fr; gap: 1.2rem; }}
    .deliverable-num {{ font-size: 1.3rem; }}
  }}

  /* Outcomes — 4-up grid */
  .outcomes h2 {{ max-width: 16ch; margin-bottom: 1.5rem; }}
  .outcomes .subhead {{ margin-bottom: 4rem; }}
  .outcomes-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
  }}
  .outcome {{
    border-top: 2px solid var(--gold);
    padding: 1.5rem 0 0;
  }}
  .outcome-arrow {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    color: var(--gold);
    font-size: 1.5rem;
    margin-bottom: 0.6rem;
    display: block;
    line-height: 1;
  }}
  .outcome-title {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 1.35rem;
    line-height: 1.2;
    color: var(--parchment);
    letter-spacing: -0.005em;
  }}
  @media (max-width: 880px) {{
    .outcomes-grid {{ grid-template-columns: repeat(2, 1fr); gap: 2rem; }}
  }}
  @media (max-width: 520px) {{
    .outcomes-grid {{ grid-template-columns: 1fr; }}
  }}

  /* Sample report */
  .sample {{
    background:
      radial-gradient(ellipse at 30% 50%, rgba(201, 169, 97, 0.04), transparent 65%),
      var(--ink);
  }}
  .sample h2 {{ max-width: 22ch; margin-bottom: 1.5rem; }}
  .sample .subhead {{ margin-bottom: 3rem; }}
  .sample-layout {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4.5rem;
    align-items: center;
  }}
  .sample-thumb-wrap {{
    position: relative;
    padding: 2rem 1rem;
  }}
  .sample-thumb-wrap::before {{
    content: '';
    position: absolute;
    inset: 2.2rem 1.4rem 1.8rem 0.7rem;
    background: linear-gradient(135deg, #1a1814 0%, #0f0d0a 100%);
    border: 1px solid rgba(201, 169, 97, 0.22);
    border-radius: 4px;
    transform: rotate(-2.5deg) translate(-12px, 12px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
    z-index: 0;
    transition: all 0.3s ease;
  }}
  .sample-thumb {{
    position: relative;
    background: linear-gradient(135deg, #1a1612 0%, #100d09 100%);
    padding: 1.4rem;
    border: 1px solid rgba(201, 169, 97, 0.42);
    border-radius: 4px;
    transition: all 0.3s ease;
    display: block;
    z-index: 1;
    box-shadow:
      0 30px 80px -10px rgba(0, 0, 0, 0.7),
      0 0 80px -10px rgba(201, 169, 97, 0.2),
      inset 0 1px 0 rgba(201, 169, 97, 0.08);
  }}
  .sample-thumb::before, .sample-thumb::after {{
    content: '';
    position: absolute;
    width: 18px;
    height: 18px;
    border: 1.5px solid var(--gold);
    opacity: 0.7;
    pointer-events: none;
  }}
  .sample-thumb::before {{ top: -4px; left: -4px; border-right: none; border-bottom: none; }}
  .sample-thumb::after {{ bottom: -4px; right: -4px; border-left: none; border-top: none; }}
  .sample-thumb:hover {{
    border-color: var(--gold);
    transform: translateY(-4px);
    box-shadow:
      0 40px 100px -10px rgba(0, 0, 0, 0.8),
      0 0 120px -10px rgba(201, 169, 97, 0.3),
      inset 0 1px 0 rgba(201, 169, 97, 0.12);
  }}
  .sample-thumb-wrap:hover::before {{
    transform: rotate(-3.5deg) translate(-18px, 14px);
    opacity: 0.95;
  }}
  .sample-thumb img {{
    display: block;
    width: 100%;
    height: auto;
    border-radius: 2px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  }}
  .sample-thumb-label {{
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    background: var(--ink);
    color: var(--gold);
    font-family: 'Instrument Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.5rem 0.85rem;
    border: 1px solid var(--gold);
    border-radius: 2px;
  }}
  .sample-details {{ display: flex; flex-direction: column; gap: 1.5rem; }}
  .sample-spec {{ border-left: 2px solid var(--gold); padding-left: 1.25rem; }}
  .sample-spec-title {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    color: var(--gold);
    font-size: 1.1rem;
    margin-bottom: 0.3rem;
  }}
  .sample-spec-body {{
    color: var(--parchment);
    opacity: 0.78;
    font-size: 0.95rem;
    line-height: 1.5;
  }}
  @media (max-width: 880px) {{
    .sample-layout {{ grid-template-columns: 1fr; gap: 2.5rem; }}
  }}

  /* What happens next */
  .next-steps {{ background: var(--obsidian); }}
  .next-steps h2 {{ max-width: 18ch; margin-bottom: 4rem; }}
  .next-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3.5rem;
  }}
  .next-step {{ position: relative; }}
  .next-step:not(:last-child)::after {{
    content: '';
    position: absolute;
    top: 1rem;
    right: -1.9rem;
    width: 1.5rem;
    height: 1px;
    background: linear-gradient(to right, var(--gold), transparent);
  }}
  .next-step-num {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    color: var(--gold);
    font-size: 1.05rem;
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
    display: block;
  }}
  .next-step h3 {{ margin-bottom: 0.6rem; font-size: 1.6rem; }}
  .next-step p {{
    color: var(--parchment);
    opacity: 0.78;
    line-height: 1.55;
    font-size: 1rem;
  }}
  @media (max-width: 720px) {{
    .next-grid {{ grid-template-columns: 1fr; gap: 2.5rem; }}
    .next-step:not(:last-child)::after {{ display: none; }}
  }}

  /* Final CTA */
  .final-cta {{
    background: var(--ink);
    text-align: center;
    padding: 9rem 6%;
  }}
  .final-cta h2 {{ max-width: 22ch; margin: 1rem auto 1.5rem; }}
  .final-cta .subhead {{ margin: 0 auto 3rem; }}
  .final-cta .cta-support {{ margin-top: 1.25rem; }}

  /* Footer */
  footer {{
    background: var(--obsidian);
    padding: 4rem 6% 3rem;
    border-top: 1px solid rgba(201, 169, 97, 0.15);
  }}
  .footer-grid {{
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 3rem;
    max-width: 1200px;
    margin: 0 auto;
    align-items: start;
  }}
  .footer-brand-block .footer-logo {{
    display: block;
    height: 40px;
    width: auto;
    margin-bottom: 1.25rem;
  }}
  .footer-tagline {{
    color: var(--slate);
    font-size: 0.92rem;
    line-height: 1.5;
    max-width: 36ch;
  }}
  .footer-col-title {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1rem;
  }}
  .footer-col a {{
    display: block;
    color: var(--parchment);
    opacity: 0.78;
    text-decoration: none;
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
    transition: color 0.2s ease;
  }}
  .footer-col a:hover {{ color: var(--gold); opacity: 1; }}
  .footer-meta {{
    border-top: 1px solid rgba(201, 169, 97, 0.12);
    margin-top: 3rem;
    padding-top: 1.5rem;
    color: var(--slate);
    font-size: 0.85rem;
    letter-spacing: 0.04em;
    text-align: center;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
  }}
  .footer-meta a {{
    color: var(--slate);
    text-decoration: none;
    border-bottom: 1px solid rgba(107, 114, 128, 0.35);
    transition: all 0.2s ease;
    padding-bottom: 1px;
  }}
  .footer-meta a:hover {{ color: var(--gold); border-bottom-color: var(--gold); }}
  .footer-meta-sep {{ margin: 0 0.8rem; opacity: 0.5; }}
  @media (max-width: 720px) {{
    .footer-grid {{ grid-template-columns: 1fr; gap: 2rem; }}
    .brand-bar .brand-logo {{ height: 44px; }}
  }}
</style>
</head>
<body>

<!-- BRAND BAR -->
<div class="brand-bar">
  <a href="/" aria-label="Rogue Night home">
    <img class="brand-logo" src="data:image/png;base64,{LOGO_B64}" alt="Rogue Night — AI &amp; Automation Strategy for Australian small to medium businesses">
  </a>
  <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="cta-ghost">
    Get started <span class="cta-arrow">→</span>
  </a>
</div>

<!-- HERO -->
<section class="hero">
  <p class="eyebrow">AI &amp; Automation Strategy</p>
  <h1>Run your business <em>smarter.</em><br>With systems that work — even when you don't.</h1>
  <p class="subhead">We help Australian businesses identify the right tools, eliminate wasted effort, and design AI-powered systems that reduce admin, improve conversion, and free up your time.</p>
  <div>
    <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="cta-primary">
      Get your AI &amp; Automation Strategy <span class="cta-arrow">→</span>
    </a>
    <p class="cta-support">{PRICE_DISPLAY} · Delivered to your inbox in 48 hours · Yours to keep</p>
  </div>
</section>

<!-- VALUE STRIP -->
<section class="value-strip">
  <div class="container">
    <div>
      <p class="value-headline">What you're buying is not a <em>report</em>.</p>
      <p class="value-sub">It's a clear plan to run your business with less effort and more leverage.</p>
    </div>
    <ul class="value-unlocks">
      <li>20–30 hours saved per month</li>
      <li>Less admin and manual work</li>
      <li>Consistent lead flow without chasing</li>
      <li>Systems that scale without extra staff</li>
    </ul>
    <p class="value-recovery">Most clients recover the cost within the first <em>30–60 days</em>.</p>
  </div>
</section>

<!-- TRUST PILLARS -->
<section class="trust">
  <div class="container">
    <p class="trust-lead">
      <span class="trust-lead-divider"></span>
      Two decades delivering digital transformation inside <em>Australia's largest organisations.</em> Same playbook, now built for small to medium businesses.
    </p>
    <div class="pillars">
      <div class="pillar">
        <div class="pillar-num"><em>01</em></div>
        <div class="pillar-title">Proven on enterprise programs.</div>
      </div>
      <div class="pillar">
        <div class="pillar-num"><em>02</em></div>
        <div class="pillar-title">Human-led, AI-amplified.</div>
      </div>
      <div class="pillar">
        <div class="pillar-num"><em>03</em></div>
        <div class="pillar-title">Vendor-neutral by design.</div>
      </div>
    </div>
  </div>
</section>

<!-- PROBLEM -->
<section class="pain">
  <div class="container">
    <p class="eyebrow">The problem we see</p>
    <h2>You're not slow.<br><em>You're under-systemised.</em></h2>
    <div class="pain-cards">
      <div class="pain-card">
        <span class="pain-num">01</span>
        <h3>Too many tools —<br>or the wrong ones.</h3>
        <p>You're paying for software you don't use, missing tools you need, or relying on spreadsheets and inboxes to run everything.</p>
      </div>
      <div class="pain-card">
        <span class="pain-num">02</span>
        <h3>Time lost to admin.</h3>
        <p>Manual quotes. Follow-ups. Data entry. Work that shouldn't exist — quietly eating the hours you should be spending on customers.</p>
      </div>
      <div class="pain-card">
        <span class="pain-num">03</span>
        <h3>No clear path into AI.</h3>
        <p>You know AI matters — but you don't know where it actually fits in your business, or which agents would pay back fastest.</p>
      </div>
    </div>
  </div>
</section>

<!-- WHAT WE DO -->
<section class="what-we-do">
  <div class="container">
    <p class="eyebrow">What we do</p>
    <h2>We give you a practical, step-by-step plan to <em>fix all of it.</em></h2>
    <p class="subhead">Your AI &amp; Automation Strategy is a custom business optimisation plan — specially curated for small to medium businesses like yours, delivered to your inbox within 48 hours.</p>
    <div class="what-we-do-includes">Your strategy includes</div>
    <div class="deliverables">
      <div class="deliverable">
        <div class="deliverable-num"><em>01</em></div>
        <div class="deliverable-body">
          <h3>Business assessment</h3>
          <p>Where you are now — and what's slowing you down. The honest read on your current setup, in plain language.</p>
        </div>
      </div>
      <div class="deliverable">
        <div class="deliverable-num"><em>02</em></div>
        <div class="deliverable-body">
          <h3>Tool stack redesign</h3>
          <p>What to keep, what to replace, what to add — with full pricing tiers and the tradeoffs each option carries. Vendor-neutral by design.</p>
        </div>
      </div>
      <div class="deliverable">
        <div class="deliverable-num"><em>03</em></div>
        <div class="deliverable-body">
          <h3>Priority action plan</h3>
          <p>Exactly what to do first, second, third. The five changes that deliver the fastest return with the least effort — and how to actually do them.</p>
        </div>
      </div>
      <div class="deliverable">
        <div class="deliverable-num"><em>04</em></div>
        <div class="deliverable-body">
          <h3>12-week implementation roadmap</h3>
          <p>Week-by-week tasks for the first three months. Plain language, real provider names, no jargon. Clear steps you can run yourself — or have us run.</p>
        </div>
      </div>
      <div class="deliverable">
        <div class="deliverable-num"><em>05</em></div>
        <div class="deliverable-body">
          <h3>AI opportunity blueprint</h3>
          <p>Where AI can save time or increase output — and how. A roadmap of the digital employees we'd build for your business, what each one would save, and when.</p>
        </div>
      </div>
    </div>
    <div class="plus-strip">
      <p class="eyebrow">Plus</p>
      <p class="plus-strip-body"><em>Quantified ROI</em></p>
      <p class="plus-strip-sub">Clear estimates of the time and money you'll recover — line-by-line, no inflated numbers, sourced from current Australian rates.</p>
    </div>
  </div>
</section>

<!-- OUTCOMES -->
<section class="outcomes">
  <div class="container">
    <p class="eyebrow">The outcome</p>
    <h2>You walk away with <em>real clarity.</em></h2>
    <p class="subhead">Not a vague audit. Not another consultant's framework. A specific plan, in your hands, ready to act on.</p>
    <div class="outcomes-grid">
      <div class="outcome">
        <span class="outcome-arrow"><em>→</em></span>
        <div class="outcome-title">Clarity on <em>what to fix</em></div>
      </div>
      <div class="outcome">
        <span class="outcome-arrow"><em>→</em></span>
        <div class="outcome-title">Confidence in <em>what tools to use</em></div>
      </div>
      <div class="outcome">
        <span class="outcome-arrow"><em>→</em></span>
        <div class="outcome-title">A roadmap to <em>implement</em></div>
      </div>
      <div class="outcome">
        <span class="outcome-arrow"><em>→</em></span>
        <div class="outcome-title">A foundation for <em>AI</em></div>
      </div>
    </div>
  </div>
</section>

<!-- SAMPLE REPORT -->
<section class="sample">
  <div class="container">
    <p class="eyebrow">What you get</p>
    <h2>A strategy <em>specially curated</em><br>for your business.</h2>
    <p class="subhead">Inside your AI &amp; Automation Strategy: a diagnostic of where your stack is now, the tools we'd recommend next, a phased rollout with implementation guidance, and a roadmap of the AI agents that would pay back fastest. Yours to act on, with us or without us.</p>
    <div class="sample-layout">
      <div class="sample-thumb-wrap">
        <a href="{PDF_URL}" target="_blank" rel="noopener noreferrer" class="sample-thumb">
          <span class="sample-thumb-label">Sample · {PDF_PAGES} pages</span>
          <img src="data:image/jpeg;base64,{THUMB_B64}" alt="Cover of a sample strategy report.">
        </a>
      </div>
      <div class="sample-details">
        <div class="sample-spec">
          <div class="sample-spec-title"><em>Quantified benefits</em></div>
          <div class="sample-spec-body">Line-by-line hours and dollar impact per change. No fluff, no inflated outcomes — just the numbers your stack should be producing.</div>
        </div>
        <div class="sample-spec">
          <div class="sample-spec-title"><em>Recommended stack</em></div>
          <div class="sample-spec-body">Priority badges, full pricing tiers, recommended starting plan. The honest tradeoffs, not the sales pitch.</div>
        </div>
        <div class="sample-spec">
          <div class="sample-spec-title"><em>Phased rollout</em></div>
          <div class="sample-spec-body">Week-by-week tasks for the first three months. Plain language, real provider names, no jargon. Designed for you to execute or for us to run.</div>
        </div>
        <div class="sample-spec">
          <div class="sample-spec-title"><em>Your future digital employees</em></div>
          <div class="sample-spec-body">Agents specially designed for your business, phased over time as you're ready for them. Hours saved and dollars captured for each. The roadmap nobody else is giving you.</div>
        </div>
        <a href="{PDF_URL}" target="_blank" rel="noopener noreferrer" class="cta-ghost" style="margin-top: 0.5rem;">
          Download the sample (PDF, {PDF_PAGES} pages) <span class="cta-arrow">→</span>
        </a>
      </div>
    </div>
  </div>
</section>

<!-- WHAT HAPPENS NEXT -->
<section class="next-steps">
  <div class="container">
    <p class="eyebrow">What happens next</p>
    <h2>Two steps. <em>Forty-eight hours.</em></h2>
    <div class="next-grid">
      <div class="next-step">
        <span class="next-step-num"><em>01</em></span>
        <h3>Complete a 5–7 minute form</h3>
        <p>We assess your business and your current systems. Quick, structured questions — no pre-call required, no homework, no follow-up calls to coordinate.</p>
      </div>
      <div class="next-step">
        <span class="next-step-num"><em>02</em></span>
        <h3>Receive your strategy</h3>
        <p>Detailed, tailored, and ready to act on. In your inbox within 48 hours of payment, yours to keep — whatever you decide to do next.</p>
      </div>
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="final-cta">
  <p class="eyebrow">Start here</p>
  <h2>Get your <em>AI &amp; Automation Strategy.</em></h2>
  <p class="subhead">A 5–7 minute form. {PRICE_DISPLAY} flat. A custom plan in your inbox within 48 hours, yours to keep — whatever you do next.</p>
  <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="cta-primary">
    Get started <span class="cta-arrow">→</span>
  </a>
  <p class="cta-support">{PRICE_DISPLAY} · Delivered to your inbox in 48 hours · Yours to keep</p>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-grid">
    <div class="footer-brand-block">
      <a href="/" aria-label="Rogue Night home">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_SM_B64}" alt="">
      </a>
      <p class="footer-tagline"><em style="font-style: italic; color: var(--gold);">The work that runs while you sleep.</em></p>
    </div>
    <div class="footer-col">
      <div class="footer-col-title">Contact</div>
      <a href="mailto:hello@roguenight.com.au">hello@roguenight.com.au</a>
    </div>
    <div class="footer-col">
      <div class="footer-col-title">Get started</div>
      <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer">Get your AI &amp; Automation Strategy</a>
      <a href="{PDF_URL}" target="_blank" rel="noopener noreferrer">Sample strategy (PDF)</a>
    </div>
  </div>
  <div class="footer-meta">
    Rogue Night PTY LTD<span class="footer-meta-sep">·</span>ABN {ABN}<span class="footer-meta-sep">·</span>Australia<span class="footer-meta-sep">·</span><a href="{PRIVACY_URL}">Privacy</a><span class="footer-meta-sep">·</span><a href="{TERMS_URL}">Terms</a>
  </div>
</footer>

</body>
</html>
"""

_OUT = os.path.join(_SCRIPT_DIR, 'rogue-night-landing.html')
with open(_OUT, 'w') as f:
    f.write(HTML)

size_kb = os.path.getsize(_OUT) / 1024
mode_label = 'staging' if STAGING_MODE else 'production'
print(f"Landing page v10 (AI & Automation Strategy rebrand) written: {size_kb:.1f} KB · mode={mode_label}")

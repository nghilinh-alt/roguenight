#!/usr/bin/env python3
"""Build the Rogue Night landing page (v9) with photographic logo lockups."""
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
PDF_PAGES = 23
SAMPLE_CLIENT = "Cindy's Cakes"
SITE_URL = 'https://roguenight.com.au'
ABN = '31 633 650 334'

# MODE: 'staging' (default — links go to hyperagent artifacts so the in-thread
# preview works) or 'production' (relative paths for live Hostinger deploy).
# Switch via: STAGING_MODE=false python3 build_landing.py
STAGING_MODE = os.environ.get('STAGING_MODE', 'true').lower() != 'false'

if STAGING_MODE:
    PDF_URL = 'https://pub.hyperagent.com/api/published/pbf01KRB9E02V_D20BQGPH4K87GXSK/rogue-night-sample-report-v3.pdf'
    PRIVACY_URL = 'https://hyperagent.com/api/files/usergenerated/threads/cmp0ar2ld0z7u07ad51te2m1a/artifacts/4199c54e-4981-4e05-892d-d4d1507df31a.html'
    TERMS_URL = 'https://hyperagent.com/api/files/usergenerated/threads/cmp11nt330hkq07ad6ehn9pxd/artifacts/f8837a40-77a5-4cf0-b05f-ac0c0d03a6f6.html'
else:
    # Production paths — PDF and sub-pages all live at roguenight.com.au after deploy
    PDF_URL = '/health-check-sample.pdf'
    PRIVACY_URL = '/privacy/'
    TERMS_URL = '/terms/'

HTML = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Primary meta -->
<title>Rogue Night — Digital transformation for Australian small to medium businesses</title>
<meta name="description" content="Rogue Night helps Australian small to medium businesses identify the right tools and deploy AI agents and digital employees. Specially curated Digital Health Check, $350 flat, in your inbox within 48 hours.">
<meta name="keywords" content="digital transformation Australia, AI agents small business, digital employees, small to medium business consulting, Australian AI consultant, business automation, AI implementation, tool stack audit, digital health check">
<meta name="author" content="Rogue Night PTY LTD">
<meta name="theme-color" content="#0A0E1A">
<meta name="robots" content="index,follow,max-image-preview:large">

<!-- Canonical -->
<link rel="canonical" href="{SITE_URL}/">

<!-- Favicon — inline SVG for guaranteed render across hosts -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%230A0E1A'/%3E%3Ccircle cx='32' cy='32' r='14' fill='%23050608'/%3E%3Ccircle cx='32' cy='32' r='16' fill='none' stroke='%23C9A961' stroke-width='1.5' opacity='0.9'/%3E%3Ccircle cx='32' cy='32' r='20' fill='none' stroke='%23C9A961' stroke-width='0.8' opacity='0.4'/%3E%3C/svg%3E">
<link rel="apple-touch-icon" href="{SITE_URL}/apple-touch-icon.png">

<!-- Open Graph — LinkedIn, Facebook, Slack, WhatsApp, iMessage -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Rogue Night">
<meta property="og:title" content="Rogue Night — The work that runs while you sleep">
<meta property="og:description" content="We help Australian small to medium businesses identify the right tools and deploy AI agents and digital employees. Digital Health Check, $350 flat, within 48 hours.">
<meta property="og:url" content="{SITE_URL}/">
<meta property="og:image" content="{SITE_URL}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Rogue Night — digital transformation, AI-amplified, priced for small business">
<meta property="og:locale" content="en_AU">

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Rogue Night — The work that runs while you sleep">
<meta name="twitter:description" content="We help Australian small to medium businesses identify the right tools and deploy AI agents and digital employees. Digital Health Check, $350 flat, within 48 hours.">
<meta name="twitter:image" content="{SITE_URL}/og-image.png">
<meta name="twitter:image:alt" content="Rogue Night logo on Ink background with editorial headline">

<!-- Geographic targeting -->
<meta name="geo.region" content="AU">
<meta name="geo.placename" content="Australia">

<!-- JSON-LD structured data — helps Google understand the business -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Rogue Night PTY LTD",
  "alternateName": "Rogue Night",
  "url": "{SITE_URL}/",
  "logo": "{SITE_URL}/logo-stacked.png",
  "image": "{SITE_URL}/og-image.png",
  "description": "Digital transformation consulting, AI agent and digital employee deployment, and vetted tool advisory for Australian small to medium businesses.",
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
  "priceRange": "A$350",
  "knowsAbout": [
    "Digital transformation",
    "AI agents",
    "Digital employees",
    "Business automation",
    "Tool stack advisory",
    "Small business consulting"
  ],
  "makesOffer": {{
    "@type": "Offer",
    "name": "Digital Health Check",
    "price": "350",
    "priceCurrency": "AUD",
    "availability": "https://schema.org/InStock",
    "description": "Specially curated digital health check for small business — tool snapshot, recommended stack, AI agent ideas, phased rollout. Delivered to your inbox within 48 hours.",
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

  /* Brand bar (top) */
  .brand-bar {{
    position: relative;
    padding: 1.5rem 6% 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .brand-bar a {{ text-decoration: none; }}
  .brand-logo {{
    display: block;
    height: 56px;
    width: auto;
  }}
  .brand-bar .cta-ghost {{ font-size: 0.95rem; }}

  /* Hero */
  .hero {{
    padding: 5rem 6% 9rem;
    max-width: 1200px;
    margin: 0 auto;
  }}
  .hero h1 {{ margin: 1.5rem 0 2rem; max-width: 18ch; }}
  .hero .subhead {{ font-size: 1.3rem; max-width: 56ch; margin-bottom: 3rem; }}

  /* CTA buttons */
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
  .cta-ghost:hover {{
    color: var(--parchment);
    border-bottom-color: var(--gold);
  }}
  .cta-arrow {{
    display: inline-block;
    transition: transform 0.2s ease;
  }}
  .cta-primary:hover .cta-arrow,
  .cta-ghost:hover .cta-arrow {{ transform: translateX(4px); }}

  .cta-support {{
    font-size: 0.92rem;
    color: var(--slate);
    margin-top: 1rem;
    letter-spacing: 0.02em;
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
  .pillars {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3rem;
  }}
  .pillar {{
    border-left: 2px solid var(--gold);
    padding-left: 1.5rem;
  }}
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

  /* Pain section */
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

  /* Solution section */
  .solution {{ background: var(--obsidian); }}
  .solution h2 {{ max-width: 22ch; margin-bottom: 1.5rem; }}
  .solution .subhead {{ margin-bottom: 4rem; }}
  .solution-flow {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3rem;
    align-items: start;
  }}
  .step {{
    position: relative;
  }}
  .step:not(:last-child)::after {{
    content: '';
    position: absolute;
    top: 1.5rem;
    right: -1.7rem;
    width: 1.4rem;
    height: 1px;
    background: linear-gradient(to right, var(--gold), transparent);
  }}
  .step-num {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    color: var(--gold);
    font-size: 1rem;
    margin-bottom: 1rem;
    display: block;
    letter-spacing: 0.04em;
  }}
  .step h3 {{ margin-bottom: 0.6rem; font-size: 1.5rem; }}
  .step-tag {{
    font-family: 'JetBrains Mono', 'SFMono-Regular', Menlo, monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--slate);
    margin-bottom: 1rem;
    display: inline-block;
    padding: 4px 10px;
    border: 1px solid rgba(107, 114, 128, 0.3);
    border-radius: 3px;
  }}
  .step-tag.included {{ color: var(--gold); border-color: rgba(201, 169, 97, 0.4); }}
  .step-tag.separate {{ color: var(--ember); border-color: rgba(194, 65, 12, 0.45); }}
  .step p {{
    color: var(--parchment);
    opacity: 0.78;
    line-height: 1.55;
    font-size: 0.98rem;
    margin-bottom: 1.5rem;
  }}
  @media (max-width: 880px) {{
    .solution-flow {{ grid-template-columns: 1fr; gap: 2.5rem; }}
    .step:not(:last-child)::after {{ display: none; }}
  }}

  /* Sample report section — editorial document treatment */
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
  /* Page 2 peeking behind, slightly rotated */
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
  /* Gold corner accents */
  .sample-thumb::before,
  .sample-thumb::after {{
    content: '';
    position: absolute;
    width: 18px;
    height: 18px;
    border: 1.5px solid var(--gold);
    opacity: 0.7;
    pointer-events: none;
  }}
  .sample-thumb::before {{
    top: -4px;
    left: -4px;
    border-right: none;
    border-bottom: none;
  }}
  .sample-thumb::after {{
    bottom: -4px;
    right: -4px;
    border-left: none;
    border-top: none;
  }}
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
  .sample-details {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }}
  .sample-spec {{
    border-left: 2px solid var(--gold);
    padding-left: 1.25rem;
  }}
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

  /* Final CTA section */
  .final-cta {{
    background: var(--obsidian);
    text-align: center;
    padding: 9rem 6%;
  }}
  .final-cta h2 {{ max-width: 18ch; margin: 1rem auto 1.5rem; }}
  .final-cta .subhead {{ margin: 0 auto 3rem; }}
  .final-cta .cta-support {{ margin-top: 1.25rem; }}

  /* Footer */
  footer {{
    background: var(--ink);
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
  .footer-meta a:hover {{
    color: var(--gold);
    border-bottom-color: var(--gold);
  }}
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
    <img class="brand-logo" src="data:image/png;base64,{LOGO_B64}" alt="Rogue Night — digital transformation consulting for Australian small to medium businesses">
  </a>
  <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="cta-ghost">
    Start the Health Check <span class="cta-arrow">→</span>
  </a>
</div>

<!-- HERO -->
<section class="hero">
  <p class="eyebrow">Digital transformation, AI-amplified</p>
  <h1>Run your business <em>smarter.</em><br>Day and night.</h1>
  <p class="subhead">We help Australian small to medium businesses identify the right tools to run on, then deploy AI agents and digital employees that earn their keep. The work that used to slow you down — now running while you sleep.</p>
  <div>
    <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="cta-primary">
      Book a Digital Health Check <span class="cta-arrow">→</span>
    </a>
    <p class="cta-support">$350 flat · Delivered to your inbox in 48 hours · Yours to keep</p>
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

<!-- PAIN SECTION -->
<section class="pain">
  <div class="container">
    <p class="eyebrow">The pattern we see</p>
    <h2>You're not slow.<br><em>You're under-tooled.</em></h2>
    <div class="pain-cards">
      <div class="pain-card">
        <span class="pain-num">01</span>
        <h3>Wrong tools.<br>Or not enough of them.</h3>
        <p>You're paying for software you don't fully use, missing the tools that would save you days, or running the whole business on email and spreadsheets.</p>
      </div>
      <div class="pain-card">
        <span class="pain-num">02</span>
        <h3>Hours lost to admin every week.</h3>
        <p>Quote chasing, invoice follow-ups, manual data re-typed between tools that don't talk to each other. Death by a thousand cuts.</p>
      </div>
      <div class="pain-card">
        <span class="pain-num">03</span>
        <h3>Each AI agent could save you tens of thousands.</h3>
        <p>The businesses that deploy digital employees first capture the gain. The rest play catch-up at higher cost, with less leverage.</p>
      </div>
    </div>
  </div>
</section>

<!-- SOLUTION -->
<section class="solution">
  <div class="container">
    <p class="eyebrow">What we do</p>
    <h2>AI agents are the <em>next operating layer</em> of every business.</h2>
    <p class="subhead">Same logic as the cloud, same logic as the internet — except this time, you get to be early. Start with a Digital Health Check. When you're ready to build the agents we recommend, that's a separate engagement.</p>
    <div class="solution-flow">
      <div class="step">
        <span class="step-num"><em>01 — Diagnose</em></span>
        <h3>Digital Health Check</h3>
        <span class="step-tag included">$350 · Health Check</span>
        <p>A 5-7 minute form. We map your current stack, the tools we'd swap in, and the AI agents that would pay back fastest. A report specially curated for your business — in your inbox within 48 hours.</p>
        <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="cta-ghost">Start now <span class="cta-arrow">→</span></a>
      </div>
      <div class="step">
        <span class="step-num"><em>02 — Recommend</em></span>
        <h3>Vetted tool library</h3>
        <span class="step-tag">Inside the report</span>
        <p>The tools we'd recommend for businesses like yours — researched in depth, costed honestly, and matched to your size, sector, and budget. Vendor-neutral by design. Yours to act on with us or without us.</p>
      </div>
      <div class="step">
        <span class="step-num"><em>03 — Deploy</em></span>
        <h3>AI agents and digital employees</h3>
        <span class="step-tag separate">Scoped separately</span>
        <p>Once you've seen the roadmap and picked the agents that fit, we design, build, and embed them — handling the repetitive, the after-hours, and the high-volume work. Quoted per scope, not part of the Health Check.</p>
      </div>
    </div>
  </div>
</section>

<!-- SAMPLE REPORT -->
<section class="sample">
  <div class="container">
    <p class="eyebrow">What you get</p>
    <h2>A report <em>specially curated</em><br>for your business.</h2>
    <p class="subhead">Inside the Digital Health Check: a diagnostic of where your stack is now, the tools we'd swap in, a phased rollout with step-by-step guidance, and a roadmap of the AI agents we'd build next — what each one would do, what it would save, and when. The report is yours. Implementing the tools and building the agents are separate engagements, available when you're ready.</p>
    <div class="sample-layout">
      <div class="sample-thumb-wrap">
        <a href="{PDF_URL}" target="_blank" rel="noopener noreferrer" class="sample-thumb">
          <span class="sample-thumb-label">Sample · {PDF_PAGES} pages</span>
          <img src="data:image/jpeg;base64,{THUMB_B64}" alt="Cover of a sample Digital Health Check report for {SAMPLE_CLIENT}.">
        </a>
      </div>
      <div class="sample-details">
        <div class="sample-spec">
          <div class="sample-spec-title"><em>Quantified benefits</em></div>
          <div class="sample-spec-body">Line-by-line hours and dollar impact per change. No fluff, no inflated outcomes — just the numbers your stack should be producing.</div>
        </div>
        <div class="sample-spec">
          <div class="sample-spec-title"><em>Recommended stack</em></div>
          <div class="sample-spec-body">Five categories, priority badges, full pricing tiers, recommended starting plan. Plus what we deliberately left out, and why.</div>
        </div>
        <div class="sample-spec">
          <div class="sample-spec-title"><em>Phased rollout</em></div>
          <div class="sample-spec-body">Week-by-week tasks for the first three months. Plain language, real provider names, no jargon. Designed for you to execute or for us to run.</div>
        </div>
        <div class="sample-spec">
          <div class="sample-spec-title"><em>Your future digital employees</em></div>
          <div class="sample-spec-body">A roadmap of AI agents specially designed for your business — what we'd build, when, and what each one would save you. The roadmap is yours; implementation is a separate engagement.</div>
        </div>
        <a href="{PDF_URL}" target="_blank" rel="noopener noreferrer" class="cta-ghost" style="margin-top: 0.5rem;">
          Download the sample (PDF, {PDF_PAGES} pages) <span class="cta-arrow">→</span>
        </a>
      </div>
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="final-cta">
  <p class="eyebrow">Start here</p>
  <h2>Book your <em>Digital Health Check.</em></h2>
  <p class="subhead">A 5-7 minute form. $350 flat. A report specially curated for your business, in your inbox within 48 hours, yours to keep — whatever you do next.</p>
  <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="cta-primary">
    Start the Health Check <span class="cta-arrow">→</span>
  </a>
  <p class="cta-support">$350 flat · Delivered to your inbox in 48 hours · Yours to keep</p>
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
      <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer">Book a Health Check</a>
      <a href="{PDF_URL}" target="_blank" rel="noopener noreferrer">Sample report (PDF)</a>
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

import os
size_kb = os.path.getsize(_OUT) / 1024
print(f"Landing page v9 written: {size_kb:.1f} KB")

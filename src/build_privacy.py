#!/usr/bin/env python3
"""Build the Rogue Night Privacy Policy as a Phase 1-branded webpage."""
import os
import base64

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_SCRIPT_DIR, 'data')

# Read horizontal logo for header
with open(os.path.join(_DATA, 'horizontal-b64.txt')) as f:
    LOGO_B64 = f.read().strip()
with open(os.path.join(_DATA, 'horizontal_sm-b64.txt')) as f:
    LOGO_SM_B64 = f.read().strip()

# Production URL and mode toggle (same pattern as build_landing.py)
TALLY_URL = 'https://tally.so/r/xX4YaG'
ABN = '31 633 650 334'
LAST_UPDATED = '11 May 2026'
SITE_URL = 'https://roguenight.com.au'

STAGING_MODE = os.environ.get('STAGING_MODE', 'true').lower() != 'false'
if STAGING_MODE:
    LANDING_URL = '#'  # privacy page doesn't navigate back during staging
    TERMS_URL = 'https://hyperagent.com/api/files/usergenerated/threads/cmp11nt330hkq07ad6ehn9pxd/artifacts/f8837a40-77a5-4cf0-b05f-ac0c0d03a6f6.html'
else:
    LANDING_URL = '/'
    TERMS_URL = '/terms/'

HTML = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Primary meta -->
<title>Privacy Policy — Rogue Night</title>
<meta name="description" content="How Rogue Night collects, uses, and protects information from Australian small to medium businesses engaging the Digital Health Check service.">
<meta name="author" content="Rogue Night PTY LTD">
<meta name="theme-color" content="#0A0E1A">
<meta name="robots" content="index,follow,max-image-preview:large">

<!-- Canonical -->
<link rel="canonical" href="{SITE_URL}/privacy">

<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%230A0E1A'/%3E%3Ccircle cx='32' cy='32' r='14' fill='%23050608'/%3E%3Ccircle cx='32' cy='32' r='16' fill='none' stroke='%23C9A961' stroke-width='1.5' opacity='0.9'/%3E%3Ccircle cx='32' cy='32' r='20' fill='none' stroke='%23C9A961' stroke-width='0.8' opacity='0.4'/%3E%3C/svg%3E">
<link rel="apple-touch-icon" href="{SITE_URL}/apple-touch-icon.png">

<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="Rogue Night">
<meta property="og:title" content="Privacy Policy — Rogue Night">
<meta property="og:description" content="How Rogue Night collects, uses, and protects information. Voluntary OAIC-aligned compliance.">
<meta property="og:url" content="{SITE_URL}/privacy">
<meta property="og:image" content="{SITE_URL}/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Rogue Night — digital transformation, AI-amplified, priced for small business">
<meta property="og:locale" content="en_AU">

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Privacy Policy — Rogue Night">
<meta name="twitter:description" content="How Rogue Night collects, uses, and protects information. Voluntary OAIC-aligned compliance.">
<meta name="twitter:image" content="{SITE_URL}/og-image.jpg">

<!-- Geographic targeting -->
<meta name="geo.region" content="AU">

<!-- JSON-LD structured data — sub-page of the main service -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Privacy Policy",
  "url": "{SITE_URL}/privacy",
  "isPartOf": {{
    "@type": "WebSite",
    "name": "Rogue Night",
    "url": "{SITE_URL}/"
  }},
  "about": {{
    "@type": "ProfessionalService",
    "name": "Rogue Night PTY LTD",
    "identifier": [
      {{
        "@type": "PropertyValue",
        "propertyID": "ABN",
        "value": "{ABN}"
      }}
    ]
  }},
  "datePublished": "2026-05-11",
  "dateModified": "{LAST_UPDATED}",
  "publisher": {{
    "@type": "Organization",
    "name": "Rogue Night PTY LTD",
    "logo": "{SITE_URL}/logo-stacked.png"
  }}
}}
</script>

<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>
  :root {{
    --ink: #0A0E1A;
    --obsidian: #050608;
    --gold: #C9A961;
    --ember: #C2410C;
    --parchment: #EDE8DD;
    --parchment-warm: #F5F0E4;
    --slate: #6B7280;
    --slate-deep: #4B5563;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    background: var(--parchment-warm);
    color: var(--ink);
    font-family: 'Instrument Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 17px;
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }}
  em {{ font-family: 'Instrument Serif', Georgia, serif; font-style: italic; color: #8a6f3f; font-weight: 400; }}
  h1, h2, h3 {{ font-family: 'Instrument Serif', Georgia, serif; font-weight: 400; letter-spacing: -0.015em; line-height: 1.15; color: var(--ink); }}
  h1 {{ font-size: clamp(2.8rem, 6vw, 4.2rem); margin-bottom: 1.5rem; }}
  h2 {{ font-size: 1.85rem; margin: 3.5rem 0 1.2rem; padding-bottom: 0.75rem; border-bottom: 1px solid rgba(10, 14, 26, 0.12); }}
  h2 .num {{ font-style: italic; color: #8a6f3f; margin-right: 0.6rem; font-size: 1.1rem; vertical-align: top; }}
  h3 {{ font-size: 1.3rem; margin: 2rem 0 0.8rem; color: var(--ink); }}
  p {{ margin-bottom: 1rem; max-width: 70ch; }}
  ul {{ margin: 0.8rem 0 1.5rem 0; padding-left: 1.5rem; max-width: 70ch; }}
  ul li {{ margin-bottom: 0.5rem; line-height: 1.6; }}
  strong {{ color: var(--ink); font-weight: 600; }}
  a {{ color: var(--ember); text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 3px; transition: color 0.2s ease; }}
  a:hover {{ color: #8a2e08; }}

  /* Eyebrow */
  .eyebrow {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #8a6f3f;
    margin-bottom: 1.2rem;
  }}

  /* Brand bar */
  .brand-bar {{
    position: relative;
    padding: 1.5rem 6% 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--ink);
  }}
  .brand-bar a {{ text-decoration: none; }}
  .brand-logo {{
    display: block;
    height: 56px;
    width: auto;
  }}
  .brand-bar-link {{
    color: var(--gold);
    font-family: 'Instrument Sans', sans-serif;
    font-weight: 500;
    font-size: 0.95rem;
    border-bottom: 1px solid rgba(201, 169, 97, 0.4);
    padding-bottom: 2px;
    transition: color 0.2s ease;
  }}
  .brand-bar-link:hover {{ color: var(--parchment); }}

  /* Page header */
  .page-header {{
    background: var(--ink);
    color: var(--parchment);
    padding: 4rem 6% 6rem;
  }}
  .page-header h1 {{ color: var(--parchment); margin: 0; }}
  .page-header h1 em {{ color: var(--gold); }}
  .page-header .meta {{
    margin-top: 1.5rem;
    color: var(--slate);
    font-size: 0.95rem;
    letter-spacing: 0.04em;
  }}
  .page-header .meta strong {{ color: var(--parchment); }}

  /* Main content */
  .content {{
    max-width: 760px;
    margin: 0 auto;
    padding: 5rem 6% 6rem;
  }}
  .intro {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 1.45rem;
    line-height: 1.5;
    color: var(--ink);
    border-left: 3px solid #8a6f3f;
    padding-left: 1.5rem;
    margin-bottom: 2.5rem;
  }}
  .intro em {{ color: #8a6f3f; font-style: italic; }}

  /* Definition list-style block for sub-processors */
  .processor-list {{
    background: rgba(201, 169, 97, 0.08);
    border-left: 3px solid #8a6f3f;
    padding: 1.5rem 1.75rem;
    margin: 1.5rem 0 2rem;
    border-radius: 0 4px 4px 0;
  }}
  .processor-list .item {{
    padding: 0.5rem 0;
  }}
  .processor-list .item + .item {{
    border-top: 1px solid rgba(10, 14, 26, 0.08);
  }}
  .processor-list .name {{
    font-family: 'Instrument Sans', sans-serif;
    font-weight: 600;
    color: var(--ink);
  }}
  .processor-list .role {{
    color: var(--slate-deep);
    font-size: 0.96rem;
  }}

  /* Callout */
  .callout {{
    background: rgba(201, 169, 97, 0.12);
    border: 1px solid rgba(201, 169, 97, 0.3);
    border-radius: 4px;
    padding: 1.5rem 1.75rem;
    margin: 1.5rem 0 2rem;
  }}
  .callout p:last-child {{ margin-bottom: 0; }}

  /* Footer */
  footer {{
    background: var(--ink);
    color: var(--slate);
    padding: 3.5rem 6% 2.5rem;
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
    padding-bottom: 1px;
    transition: all 0.2s ease;
  }}
  .footer-meta a:hover {{ color: var(--gold); border-bottom-color: var(--gold); }}
  .footer-meta-sep {{ margin: 0 0.8rem; opacity: 0.5; }}

  @media (max-width: 720px) {{
    .footer-grid {{ grid-template-columns: 1fr; gap: 2rem; }}
    .brand-bar .brand-logo {{ height: 44px; }}
    .content {{ padding: 3.5rem 6% 4rem; }}
    .intro {{ font-size: 1.2rem; }}
    h2 {{ font-size: 1.55rem; margin-top: 2.5rem; }}
  }}
</style>
</head>
<body>

<!-- BRAND BAR -->
<div class="brand-bar">
  <a href="/" aria-label="Rogue Night home">
    <img class="brand-logo" src="data:image/png;base64,{LOGO_B64}" alt="Rogue Night — digital transformation consulting for Australian small to medium businesses">
  </a>
  <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="brand-bar-link">Start the Health Check →</a>
</div>

<!-- PAGE HEADER -->
<section class="page-header">
  <p class="eyebrow">Legal</p>
  <h1>Privacy <em>Policy.</em></h1>
  <p class="meta"><strong>Rogue Night PTY LTD</strong> · ABN {ABN} · Last updated {LAST_UPDATED}</p>
</section>

<!-- CONTENT -->
<main class="content">

  <p class="intro">This policy explains how we collect, use, and protect the information you share with us — whether that's through the Digital Health Check questionnaire, an email, or an engagement as a consulting client.</p>

  <p>We're a small Australian business operating under the A$3 million turnover threshold, which technically exempts us from parts of the Privacy Act 1988 (Cth). We've chosen to comply voluntarily because it's the right way to handle information clients share with us, and we want to earn trust before we ask for it.</p>

  <h2><span class="num">01</span>What we collect</h2>

  <p>When you complete the Digital Health Check questionnaire, we collect:</p>
  <ul>
    <li>Your name, business name, phone number, and email address</li>
    <li>Your industry, team size, years operating, and how decisions get made in your business</li>
    <li>Your current tool stack, file storage approach, and the tools you rely on every day</li>
    <li>The frustrations, hated weekly tasks, and aspirations you share with us</li>
    <li>Your future-state vision and appetite for AI in your business</li>
    <li>Anything else you choose to tell us in the free-text fields</li>
  </ul>

  <p>If you engage us for consulting, we may additionally collect operational information needed to deliver the service — process documentation, system access where you authorise it, financial summaries where they're relevant — plus any communication records (emails, meeting notes, and recorded calls where you've consented).</p>

  <p>When you pay us, payments go through Stripe. <strong>We never see your card details.</strong> Stripe handles all payment data and is PCI compliant.</p>

  <h2><span class="num">02</span>How we use it</h2>

  <p>We use the information you provide to:</p>
  <ul>
    <li>Generate your Digital Health Check report</li>
    <li>Deliver the consulting services you've engaged us for</li>
    <li>Communicate with you about your engagement</li>
    <li>Improve our methodology and the vetted tool catalogue (anonymised and aggregated only)</li>
    <li>Comply with our legal, tax, and record-keeping obligations as an Australian business</li>
  </ul>

  <div class="callout">
    <p>We do not sell your information. We do not share it with marketing partners. We do not use it to train third-party AI models outside the specific context of generating your report.</p>
  </div>

  <h2><span class="num">03</span>Who we share it with</h2>

  <p>We use a small number of trusted tools to run the business. Your information may be stored with or processed by:</p>

  <div class="processor-list">
    <div class="item">
      <div class="name">Tally</div>
      <div class="role">Questionnaire form responses. Stored in the United States.</div>
    </div>
    <div class="item">
      <div class="name">Airtable</div>
      <div class="role">Structured records of responses, the tool catalogue, and recommendations. Stored in the United States.</div>
    </div>
    <div class="item">
      <div class="name">Stripe</div>
      <div class="role">Payment processing. Global infrastructure, PCI compliant. We don't access card data.</div>
    </div>
    <div class="item">
      <div class="name">Google Workspace</div>
      <div class="role">Email correspondence. Typically stored in the United States with backups elsewhere.</div>
    </div>
    <div class="item">
      <div class="name">Rogue Night backups</div>
      <div class="role">Encrypted, stored within Australia where possible.</div>
    </div>
  </div>

  <p>When your data is stored outside Australia, it's protected by the relevant provider's privacy framework — generally including standard contractual clauses for cross-border transfer. We review our sub-processors periodically and only continue using providers with practices we'd be willing to apply to our own information.</p>

  <h2><span class="num">04</span>How long we keep it</h2>

  <ul>
    <li><strong>Tally form responses:</strong> retained for as long as you are an active or recent client, plus seven years for Australian tax record-keeping requirements.</li>
    <li><strong>Engagement records:</strong> retained for seven years from the end of the engagement, in line with Australian tax law.</li>
    <li><strong>Marketing subscribers (if you separately opt in):</strong> retained until you unsubscribe.</li>
  </ul>

  <p>You can request earlier deletion of your information at any time — see "Your rights" below.</p>

  <h2><span class="num">05</span>Your rights</h2>

  <p>You have the right to:</p>
  <ul>
    <li><strong>Access</strong> the personal information we hold about you</li>
    <li><strong>Correct</strong> any information that is inaccurate or out of date</li>
    <li><strong>Delete</strong> your information (subject to our tax record-keeping obligations)</li>
    <li><strong>Object</strong> to particular uses of your information</li>
    <li><strong>Withdraw consent</strong> for any processing that relies on your consent</li>
    <li><strong>Lodge a complaint</strong> with us first, and if unresolved, with the Office of the Australian Information Commissioner (OAIC) at <a href="https://www.oaic.gov.au" target="_blank" rel="noopener noreferrer">oaic.gov.au</a></li>
  </ul>

  <p>To exercise any of these rights, email <a href="mailto:hello@roguenight.com.au?subject=Privacy">hello@roguenight.com.au</a> with the subject line "Privacy". We'll respond within seven business days.</p>

  <h2><span class="num">06</span>Cookies and analytics</h2>

  <p>This website does not currently use any cookies, analytics tools, or tracking pixels. If we add analytics in future to understand which sections of the site are most useful, we'll update this policy and add a cookie notice at that time.</p>

  <h2><span class="num">07</span>Email communications</h2>

  <p>If you complete the Digital Health Check, we'll email you the report and may follow up about your engagement. These are transactional emails sent under the legitimate basis of fulfilling your service request — you'll be able to unsubscribe from any non-essential follow-ups at any time.</p>

  <p>We only add you to a marketing list if you explicitly opt in. Marketing emails will always carry a working unsubscribe link, in line with the Spam Act 2003 (Cth).</p>

  <h2><span class="num">08</span>Security</h2>

  <p>We protect your information with reasonable safeguards: encrypted storage in our backups, access controls on third-party tools, multi-factor authentication on accounts that hold your data, and need-to-know access among any contractors we engage.</p>

  <p>No system is perfectly secure. If there is a data breach that affects your personal information and is likely to result in serious harm, we'll notify you and the OAIC in accordance with the Notifiable Data Breaches scheme under the Privacy Act.</p>

  <h2><span class="num">09</span>Children</h2>

  <p>Our services are aimed at business owners and decision-makers. We don't knowingly collect personal information from anyone under 16. If you believe we've inadvertently collected information about a child, contact us and we'll delete it.</p>

  <h2><span class="num">10</span>Changes to this policy</h2>

  <p>We may update this policy from time to time. The "Last updated" date at the top of this page reflects the most recent change. Significant changes — for example, new categories of data we collect, or new sub-processors — will be communicated to active clients by email before they take effect.</p>

  <h2><span class="num">11</span>Contact</h2>

  <p>Rogue Night PTY LTD<br>
  ABN {ABN}<br>
  Australia</p>

  <p>Email: <a href="mailto:hello@roguenight.com.au">hello@roguenight.com.au</a><br>
  Privacy queries: please mark the subject line "Privacy" and we'll prioritise your request.</p>

</main>

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
      <a href="/">Home</a>
    </div>
  </div>
  <div class="footer-meta">
    Rogue Night PTY LTD<span class="footer-meta-sep">·</span>ABN {ABN}<span class="footer-meta-sep">·</span>Australia<span class="footer-meta-sep">·</span><a href="{TERMS_URL}">Terms</a>
  </div>
</footer>

</body>
</html>
"""

_OUT = os.path.join(_SCRIPT_DIR, 'rogue-night-privacy.html')
with open(_OUT, 'w') as f:
    f.write(HTML)

import os
size_kb = os.path.getsize(_OUT) / 1024
print(f"Privacy policy webpage written: {size_kb:.1f} KB")

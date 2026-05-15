#!/usr/bin/env python3
"""Build the Rogue Night Terms of Service page (Phase 1 editorial-light branding)."""
import os

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_SCRIPT_DIR, 'data')

with open(os.path.join(_DATA, 'horizontal-b64.txt')) as f:
    LOGO_B64 = f.read().strip()
with open(os.path.join(_DATA, 'horizontal_sm-b64.txt')) as f:
    LOGO_SM_B64 = f.read().strip()

TALLY_URL = 'https://tally.so/r/xX4YaG'
ABN = '31 633 650 334'
LAST_UPDATED = '12 May 2026'
EFFECTIVE_DATE = '12 May 2026'
SITE_URL = 'https://roguenight.com.au'

STAGING_MODE = os.environ.get('STAGING_MODE', 'true').lower() != 'false'
if STAGING_MODE:
    LANDING_URL = '#'
    PRIVACY_URL = 'https://hyperagent.com/api/files/usergenerated/threads/cmp0ar2ld0z7u07ad51te2m1a/artifacts/4199c54e-4981-4e05-892d-d4d1507df31a.html'
else:
    LANDING_URL = '/'
    PRIVACY_URL = '/privacy/'

HTML = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Primary meta -->
<title>Terms of Service — Rogue Night</title>
<meta name="description" content="Engagement terms for the Rogue Night Digital Health Check and follow-on consulting work. Plain-English commitments on delivery, fees, refunds, IP, confidentiality, and Australian Consumer Law.">
<meta name="author" content="Rogue Night PTY LTD">
<meta name="theme-color" content="#0A0E1A">
<meta name="robots" content="index,follow,max-image-preview:large">

<!-- Canonical -->
<link rel="canonical" href="{SITE_URL}/terms">

<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%230A0E1A'/%3E%3Ccircle cx='32' cy='32' r='14' fill='%23050608'/%3E%3Ccircle cx='32' cy='32' r='16' fill='none' stroke='%23C9A961' stroke-width='1.5' opacity='0.9'/%3E%3Ccircle cx='32' cy='32' r='20' fill='none' stroke='%23C9A961' stroke-width='0.8' opacity='0.4'/%3E%3C/svg%3E">
<link rel="apple-touch-icon" href="{SITE_URL}/apple-touch-icon.png">

<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="Rogue Night">
<meta property="og:title" content="Terms of Service — Rogue Night">
<meta property="og:description" content="Engagement terms for the Digital Health Check and follow-on consulting work. Plain-English, Australian Consumer Law compliant.">
<meta property="og:url" content="{SITE_URL}/terms">
<meta property="og:image" content="{SITE_URL}/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Rogue Night — digital transformation, AI-amplified, priced for small business">
<meta property="og:locale" content="en_AU">

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Terms of Service — Rogue Night">
<meta name="twitter:description" content="Engagement terms for the Digital Health Check and follow-on consulting work.">
<meta name="twitter:image" content="{SITE_URL}/og-image.jpg">

<!-- Geographic targeting -->
<meta name="geo.region" content="AU">

<!-- JSON-LD structured data -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Terms of Service",
  "url": "{SITE_URL}/terms",
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
  "datePublished": "2026-05-12",
  "dateModified": "{LAST_UPDATED}",
  "publisher": {{
    "@type": "Organization",
    "name": "Rogue Night PTY LTD",
    "logo": "{SITE_URL}/logo-stacked.png"
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

  .eyebrow {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #8a6f3f;
    margin-bottom: 1.2rem;
  }}

  /* Brand bar (Ink) */
  .brand-bar {{
    background: var(--ink);
    padding: 1.5rem 6%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(201, 169, 97, 0.15);
  }}
  .brand-bar a {{ text-decoration: none; line-height: 0; }}
  .brand-bar .brand-logo {{ height: 56px; width: auto; display: block; }}
  .brand-bar-link {{
    color: var(--gold);
    font-family: 'Instrument Sans', sans-serif;
    font-weight: 500;
    font-size: 0.95rem;
    border-bottom: 1px solid rgba(201, 169, 97, 0.4);
    padding-bottom: 2px;
    transition: color 0.2s ease;
    line-height: 1;
  }}
  .brand-bar-link:hover {{ color: var(--parchment); }}

  /* Page header (dark Ink) */
  .page-header {{
    background: var(--ink);
    color: var(--parchment);
    padding: 4.5rem 6% 6rem;
  }}
  .page-header .eyebrow {{ color: var(--gold); }}
  .page-header h1 {{ color: var(--parchment); margin: 0; max-width: 18ch; }}
  .page-header h1 em {{ color: var(--gold); }}
  .page-header .meta {{
    margin-top: 1.5rem;
    color: var(--slate);
    font-size: 0.95rem;
    letter-spacing: 0.02em;
    font-family: 'JetBrains Mono', monospace;
  }}
  .page-header .meta strong {{ color: var(--parchment); font-weight: 500; }}

  /* Content */
  .content {{
    max-width: 760px;
    margin: 0 auto;
    padding: 5rem 6% 5rem;
  }}
  .intro {{
    font-size: 1.25rem;
    line-height: 1.55;
    margin-bottom: 2rem;
    color: var(--ink);
    max-width: 56ch;
  }}
  .callout {{
    background: rgba(201, 169, 97, 0.08);
    border-left: 3px solid var(--gold);
    padding: 1.2rem 1.4rem;
    margin: 1.5rem 0 2rem;
    border-radius: 0 4px 4px 0;
    font-size: 0.97rem;
  }}
  .callout strong {{ color: #8a6f3f; }}
  .callout-warn {{
    background: rgba(194, 65, 12, 0.06);
    border-left: 3px solid var(--ember);
  }}
  .callout-warn strong {{ color: var(--ember); }}

  /* Footer */
  footer {{
    background: var(--obsidian);
    color: var(--slate);
    padding: 4.5rem 6% 3rem;
    border-top: 1px solid rgba(201, 169, 97, 0.18);
  }}
  .footer-grid {{
    max-width: 1100px;
    margin: 0 auto 3rem;
    display: grid;
    grid-template-columns: 1.4fr 1fr 1fr;
    gap: 3rem;
    align-items: start;
  }}
  .footer-logo {{ height: 40px; width: auto; display: block; margin-bottom: 1rem; opacity: 0.92; }}
  .footer-tagline {{ font-size: 0.95rem; max-width: 30ch; line-height: 1.45; color: var(--slate); }}
  .footer-tagline em {{ color: var(--gold); font-style: italic; }}
  .footer-col-title {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1.1rem;
  }}
  .footer-col a {{
    color: var(--parchment);
    text-decoration: none;
    font-size: 0.95rem;
    display: block;
    margin-bottom: 0.6rem;
    transition: color 0.2s ease;
    border-bottom: none;
  }}
  .footer-col a:hover {{ color: var(--gold); }}
  .footer-meta {{
    max-width: 1100px;
    margin: 0 auto;
    border-top: 1px solid rgba(107, 114, 128, 0.18);
    padding-top: 2rem;
    font-family: 'JetBrains Mono', 'SFMono-Regular', Menlo, monospace;
    font-size: 12px;
    color: var(--slate);
    letter-spacing: 0.04em;
    text-align: center;
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
  <a href="{LANDING_URL}" aria-label="Rogue Night home">
    <img class="brand-logo" src="data:image/png;base64,{LOGO_B64}" alt="Rogue Night — digital transformation consulting for Australian small to medium businesses">
  </a>
  <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="brand-bar-link">Start the Health Check →</a>
</div>

<!-- PAGE HEADER -->
<section class="page-header">
  <p class="eyebrow">Legal</p>
  <h1>Terms of <em>Service.</em></h1>
  <p class="meta"><strong>Rogue Night PTY LTD</strong> · ABN {ABN} · Effective {EFFECTIVE_DATE}</p>
</section>

<!-- CONTENT -->
<main class="content">

  <p class="intro">
    These terms govern your use of <em>Rogue Night's</em> services, including the Digital Health Check and any follow-on consulting or implementation work. By engaging us — through the website form, by email, or in writing — you agree to what's set out below.
  </p>

  <div class="callout">
    <strong>Plain-English engagement terms, not legal advice.</strong> We've written these terms to be readable. They reflect how we actually intend to work with you. If you need detailed contractual language for an unusual engagement, ask and we'll provide it.
  </div>

  <h2><span class="num">01.</span>About us</h2>
  <p>
    Rogue Night PTY LTD (ABN {ABN}) is an Australian proprietary company providing digital transformation consulting, AI agent and digital employee deployment, and vetted tool advisory services to small to medium businesses.
  </p>
  <p>
    Throughout these terms, <strong>"we"</strong>, <strong>"us"</strong>, and <strong>"our"</strong> refer to Rogue Night PTY LTD. <strong>"You"</strong> refers to the business or individual engaging our services.
  </p>

  <h2><span class="num">02.</span>What we provide</h2>
  <p>
    Our entry product is the <strong>Digital Health Check</strong> — a specially curated report delivered to your inbox within 48 hours of payment. The report includes a snapshot of your current digital setup, tool recommendations matched to your size and sector, a phased rollout with step-by-step guidance, and a roadmap of AI agents and digital employees we'd build for you.
  </p>
  <p>
    The Digital Health Check is advisory. We do not implement tools or build agents as part of it. Implementation is a separate engagement.
  </p>
  <p>
    We offer follow-on engagements on a separate, quoted basis:
  </p>
  <ul>
    <li><strong>Tool implementation</strong> — data migration, configuration, integrations, process design</li>
    <li><strong>AI agent and digital employee build</strong> — design, deployment, integration with your stack</li>
    <li><strong>Ongoing advisory or fractional digital-operations work</strong> — retained relationship for the change cycle</li>
  </ul>
  <p>
    Each follow-on engagement requires a signed scope of work or an email proposal accepted in writing before we begin.
  </p>

  <h2><span class="num">03.</span>Fees and payment</h2>
  <p>
    The Digital Health Check is <strong>A$350 flat</strong>, payable in Australian dollars at the time of booking. Payment is processed by Stripe and confirmation is sent via email.
  </p>
  <p>
    Implementation and agent-build engagements are quoted separately based on scope, complexity, and timeline. We'll provide a written scope and quote before any chargeable work begins.
  </p>
  <div class="callout">
    <strong>GST.</strong> At present, Rogue Night is not registered for GST. The A$350 Digital Health Check fee does not include GST and no GST is charged. We will update this section if our registration status changes (typically once turnover crosses the A$75,000 ATO threshold).
  </div>

  <h2><span class="num">04.</span>Delivery</h2>
  <p>
    We aim to deliver your Digital Health Check within <strong>48 hours</strong> of payment confirmation. The report arrives as a PDF attachment to the email address you provided on the booking form, with the body of the email summarising the key findings.
  </p>
  <p>
    If delivery is delayed for any reason — illness, technical issue, exceptional questionnaire complexity — we will email you before the 48-hour mark with a revised estimate.
  </p>
  <ul>
    <li>If we miss the 48-hour mark and have not given you a revised estimate, you may request a <strong>50% credit</strong> toward this or a future engagement.</li>
    <li>If we miss delivery by more than <strong>5 business days</strong> without notice, you may request a <strong>full refund</strong>.</li>
  </ul>

  <h2><span class="num">05.</span>Amendments and refunds</h2>
  <p>
    We want every Digital Health Check to land usefully. If something in your report doesn't fit your business, tell us and we'll amend it <strong>free of charge</strong> — typically within a few days of your feedback.
  </p>
  <h3>Before work starts</h3>
  <p>
    You may cancel for a <strong>full refund</strong> within 4 hours of payment, provided we have not yet begun preparing your report. Email <a href="mailto:hello@roguenight.com.au">hello@roguenight.com.au</a> to cancel.
  </p>
  <h3>After the report is delivered</h3>
  <p>
    Once your report has been sent, we do not offer refunds, except where the report materially fails to deliver what was promised on the booking page. In that case, we'd first attempt an amendment; if that doesn't resolve the issue, we'll refund the fee in full.
  </p>
  <h3>Australian Consumer Law</h3>
  <p>
    Nothing in these terms limits your rights under <em>Australian Consumer Law</em>. The Digital Health Check comes with consumer guarantees that cannot be excluded, restricted, or modified — including guarantees that services will be provided with due care and skill, will be reasonably fit for the purpose disclosed, and will be supplied within a reasonable time.
  </p>

  <h2><span class="num">06.</span>How we use your information</h2>
  <p>
    How we collect, store, and use your business and personal information is set out in our <a href="{PRIVACY_URL}">Privacy Policy</a>. By engaging us, you confirm you have read and agree to that policy.
  </p>

  <h2><span class="num">07.</span>Confidentiality</h2>
  <p>
    Information you share with us as part of a Digital Health Check or follow-on engagement — business operations, financials, team structure, tool stack — is treated as confidential. We do not share it with third parties except as needed to deliver the work (with the sub-processors listed in our Privacy Policy) or where required by law.
  </p>
  <p>
    We may anonymise and aggregate insights from engagements to improve our recommendations, refine our tool catalogue, and write public case studies. Where a case study would identify you or your business, we ask for written permission first.
  </p>

  <h2><span class="num">08.</span>Intellectual property</h2>
  <p>
    The Digital Health Check report — including its structure, recommendations, agent designs, and underlying methodology — is and remains the intellectual property of <strong>Rogue Night PTY LTD</strong>. You may use the report internally without restriction. Share it with your team, advisors, accountant, or board. Use it to act on the recommendations. You may not, however, republish or sell the report or its methodology.
  </p>
  <p>
    Implementation outputs — configured tools, deployed agents, written guides produced for your business — become your property on full payment of the relevant invoice. Any Rogue Night-developed templates, scripts, or methodologies that underlie those outputs remain ours, but are licensed to you for internal use without limit.
  </p>

  <h2><span class="num">09.</span>What we don't do</h2>
  <p>
    To save confusion later, some things we explicitly don't offer:
  </p>
  <ul>
    <li><strong>Hands-on team training.</strong> We provide written guides and pointers to official vendor training. We don't run live training sessions for your team.</li>
    <li><strong>Replacement of your team.</strong> Our digital employees and AI agents augment the people doing the work — they don't replace them. If you're hiring us to fire people, we're not the right partner.</li>
    <li><strong>Tool resale or affiliate commissions.</strong> We're vendor-neutral. Tool recommendations are not driven by commission. We don't on-sell software licences — you buy them directly.</li>
    <li><strong>Ongoing helpdesk support outside engagement.</strong> First-month question support is included with implementation work. Anything beyond that needs a separate retainer.</li>
  </ul>

  <h2><span class="num">10.</span>Limitation of liability</h2>
  <p>
    To the maximum extent permitted by law:
  </p>
  <ul>
    <li>Our total liability for any claim arising out of or in connection with the services is <strong>limited to the fees paid by you for the specific engagement</strong> giving rise to the claim. For the Digital Health Check, this means liability is capped at A$350.</li>
    <li>We are not liable for indirect, consequential, or special damages — including loss of profits, loss of business, loss of data, or loss of goodwill.</li>
    <li>Nothing in these terms limits liability that cannot be limited by law, including liability under <em>Australian Consumer Law</em> for services that fail to meet consumer guarantees.</li>
  </ul>

  <h2><span class="num">11.</span>Your responsibilities</h2>
  <p>
    To get the best outcome from our work, you agree to:
  </p>
  <ul>
    <li>Provide accurate, current information when answering the Digital Health Check questionnaire</li>
    <li>Respond to follow-up questions from us within a reasonable timeframe (typically within 5 business days)</li>
    <li>Maintain ownership of and pay for any third-party tools we recommend or configure for you</li>
    <li>Hold any required licences, registrations, certifications, or approvals for your business activities</li>
    <li>Tell us promptly if anything we've recommended no longer fits your circumstances, so we can amend the report</li>
  </ul>

  <h2><span class="num">12.</span>Changes to these terms</h2>
  <p>
    We may update these terms from time to time. The version effective at the time you engage us is the version that applies to that engagement.
  </p>
  <p>
    Material changes that affect existing customers — pricing, refund policy, liability cap, sub-processors — will be notified by email at least 14 days before they take effect.
  </p>

  <h2><span class="num">13.</span>Governing law</h2>
  <p>
    These terms are governed by the laws of <strong>Queensland, Australia</strong>. Any dispute arising out of or in connection with these terms is subject to the exclusive jurisdiction of the courts of Queensland.
  </p>

  <h2><span class="num">14.</span>Contact</h2>
  <p>
    Questions about these terms? Write to <a href="mailto:hello@roguenight.com.au">hello@roguenight.com.au</a>. We reply within two business days, day or night.
  </p>

  <div class="callout callout-warn" style="margin-top: 4rem;">
    <strong>For complex engagements.</strong> These terms cover the standard Digital Health Check and most follow-on consulting work. If your engagement involves unusual confidentiality, indemnity, regulated industries, or contracting through a head agreement, ask us for a tailored service agreement before booking.
  </div>

</main>

<!-- FOOTER -->
<footer>
  <div class="footer-grid">
    <div>
      <a href="{LANDING_URL}" aria-label="Rogue Night home">
        <img class="footer-logo" src="data:image/png;base64,{LOGO_SM_B64}" alt="">
      </a>
      <p class="footer-tagline"><em>The work that runs while you sleep.</em></p>
    </div>
    <div class="footer-col">
      <div class="footer-col-title">Contact</div>
      <a href="mailto:hello@roguenight.com.au">hello@roguenight.com.au</a>
    </div>
    <div class="footer-col">
      <div class="footer-col-title">Get started</div>
      <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer">Book a Health Check</a>
      <a href="{LANDING_URL}">Home</a>
    </div>
  </div>
  <div class="footer-meta">
    Rogue Night PTY LTD<span class="footer-meta-sep">·</span>ABN {ABN}<span class="footer-meta-sep">·</span>Australia<span class="footer-meta-sep">·</span><a href="{PRIVACY_URL}">Privacy</a>
  </div>
</footer>

</body>
</html>
"""

_OUT = os.path.join(_SCRIPT_DIR, 'rogue-night-terms.html')
with open(_OUT, 'w') as f:
    f.write(HTML)

import os
size_kb = os.path.getsize(_OUT) / 1024
print(f"Terms of Service page written: {size_kb:.1f} KB")

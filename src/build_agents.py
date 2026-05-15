#!/usr/bin/env python3
"""Build the /agents/ inner page — Meet your digital employees.

A standalone editorial page introducing the digital-employee category
at Rogue Night. Uses 4 of the 5 landing-page agent images in
alternating left/right feature blocks. Shares the brand bar, footer,
AI Sentinel cursor, and palette with build_landing.py.

Voice rules (per agents/dhc-report-writer/README.md):
- 'small to medium businesses' — never SME
- '$395 flat', '$' prefix (no A$)
- 'within 48 hours', not 24, not 'business days'
- agents are 'digital employees' — never 'bots' or 'AI assistants'
- they 'work alongside you', they 'don't replace your team'
"""
import os

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_SCRIPT_DIR, 'data')

with open(os.path.join(_DATA, 'horizontal-b64.txt')) as f:
    LOGO_B64 = f.read().strip()
with open(os.path.join(_DATA, 'horizontal_sm-b64.txt')) as f:
    LOGO_SM_B64 = f.read().strip()

TALLY_URL = 'https://tally.so/r/xX4YaG'
SITE_URL = 'https://roguenight.com.au'
ABN = '31 633 650 334'
PRICE_DISPLAY = '$395'

STAGING_MODE = os.environ.get('STAGING_MODE', 'true').lower() != 'false'

if STAGING_MODE:
    PRIVACY_URL = 'https://roguenight.com.au/privacy/'
    TERMS_URL = 'https://roguenight.com.au/terms/'
    HOME_URL = 'https://roguenight.com.au/'
    ASSET_BASE = 'https://roguenight.com.au'
else:
    PRIVACY_URL = '/privacy/'
    TERMS_URL = '/terms/'
    HOME_URL = '/'
    ASSET_BASE = ''


HTML = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Meet your digital employees — Rogue Night</title>
<meta name="description" content="The AI agents Rogue Night designs and builds for Australian small to medium businesses. Each one specially configured to handle a specific task in your business — not a chatbot, a working employee.">
<meta name="author" content="Rogue Night PTY LTD">
<meta name="theme-color" content="#0A0E1A">
<meta name="robots" content="index,follow,max-image-preview:large">

<link rel="canonical" href="{SITE_URL}/agents/">

<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%230A0E1A'/%3E%3Ccircle cx='32' cy='32' r='14' fill='%23050608'/%3E%3Ccircle cx='32' cy='32' r='16' fill='none' stroke='%23C9A961' stroke-width='1.5' opacity='0.9'/%3E%3Ccircle cx='32' cy='32' r='20' fill='none' stroke='%23C9A961' stroke-width='0.8' opacity='0.4'/%3E%3C/svg%3E">
<link rel="apple-touch-icon" href="{SITE_URL}/apple-touch-icon.png">

<meta property="og:type" content="article">
<meta property="og:site_name" content="Rogue Night">
<meta property="og:title" content="Meet your digital employees — Rogue Night">
<meta property="og:description" content="The AI agents Rogue Night designs and builds for Australian small to medium businesses. Each one specially configured to handle a specific task — not a chatbot, a working employee.">
<meta property="og:url" content="{SITE_URL}/agents/">
<meta property="og:image" content="{SITE_URL}/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_AU">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Meet your digital employees — Rogue Night">
<meta name="twitter:description" content="The AI agents Rogue Night designs and builds for Australian small to medium businesses. Each one a working employee, not a chatbot.">
<meta name="twitter:image" content="{SITE_URL}/og-image.jpg">

<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
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
    font-size: 17px; line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }}

  em, .italic {{ font-family: 'Instrument Serif', Georgia, serif; font-style: italic; color: var(--gold); font-weight: 400; }}
  h1, h2, h3, h4 {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-weight: 400; letter-spacing: -0.02em;
    line-height: 1.05; color: var(--parchment);
  }}
  h1 {{ font-size: clamp(2.6rem, 6vw, 4.5rem); }}
  h2 {{ font-size: clamp(2rem, 4.5vw, 3.2rem); margin-bottom: 1rem; }}
  h3 {{ font-size: clamp(1.6rem, 3vw, 2.2rem); line-height: 1.15; }}
  h4 {{ font-size: 1.15rem; color: var(--gold); font-style: italic; }}

  .eyebrow {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 12px; font-weight: 500;
    letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--gold);
  }}

  .container {{
    max-width: 1200px; margin: 0 auto; padding: 0 6%;
  }}

  /* BRAND BAR */
  .brand-bar {{
    background: var(--ink); padding: 1.75rem 6%;
    display: flex; justify-content: space-between; align-items: center;
    position: sticky; top: 0; z-index: 100;
    border-bottom: 1px solid rgba(201, 169, 97, 0.18);
    backdrop-filter: blur(8px);
  }}
  .brand-bar a {{ text-decoration: none; }}
  .brand-logo {{ height: 44px; width: auto; display: block; }}

  /* Buttons */
  .cta-primary {{
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: var(--ember); color: var(--parchment);
    font-family: 'Instrument Sans', sans-serif;
    font-weight: 600; font-size: 1.05rem;
    letter-spacing: 0.01em;
    padding: 1.1rem 2rem; border: none; text-decoration: none;
    border-radius: 2px;
    transition: all 0.2s ease;
  }}
  .cta-primary:hover {{
    background: #D14E15;
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(194, 65, 12, 0.3);
  }}
  .cta-ghost {{
    display: inline-flex; align-items: center; gap: 0.5rem;
    color: var(--gold);
    font-family: 'Instrument Sans', sans-serif;
    font-weight: 500; text-decoration: none;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(201, 169, 97, 0.4);
    transition: border-color 0.2s ease;
  }}
  .cta-ghost:hover {{ border-bottom-color: var(--gold); }}
  .cta-arrow {{ transition: transform 0.2s ease; }}
  .cta-primary:hover .cta-arrow, .cta-ghost:hover .cta-arrow {{ transform: translateX(4px); }}

  /* HERO */
  .hero {{
    padding: 5rem 6% 5rem;
    max-width: 1200px; margin: 0 auto;
    text-align: center;
  }}
  .hero .eyebrow {{ margin-bottom: 1.5rem; display: block; }}
  .hero h1 {{ margin: 0 auto 1.5rem; max-width: 18ch; }}
  .hero .lede {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 1.45rem; line-height: 1.5;
    color: var(--parchment);
    max-width: 52ch; margin: 0 auto 2.5rem;
  }}

  /* INTRO STRIPE */
  .intro-stripe {{
    background: rgba(201, 169, 97, 0.06);
    border-top: 1px solid rgba(201, 169, 97, 0.18);
    border-bottom: 1px solid rgba(201, 169, 97, 0.18);
    padding: 3.5rem 6%;
    margin: 1rem 0 5rem;
  }}
  .intro-stripe .container {{
    display: grid;
    grid-template-columns: 0.85fr 1.15fr;
    gap: 3.5rem;
    align-items: start;
  }}
  .intro-stripe h2 {{
    font-size: clamp(1.7rem, 3vw, 2.4rem);
    max-width: 14ch;
  }}
  .intro-stripe p {{
    font-size: 1.05rem; line-height: 1.7;
    color: var(--parchment);
  }}
  .intro-stripe p + p {{ margin-top: 1rem; }}

  /* AGENT FEATURE BLOCKS */
  .agent {{
    padding: 4rem 0;
  }}
  .agent .container {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
  }}
  .agent.image-left .container {{ direction: rtl; }}
  .agent.image-left .agent-text {{ direction: ltr; }}
  .agent.image-left .agent-image {{ direction: ltr; }}
  .agent-image img {{
    width: 100%; height: auto; display: block;
    border-radius: 4px;
    box-shadow: 0 24px 60px -20px rgba(0, 0, 0, 0.35);
  }}
  .agent-text .eyebrow {{ display: block; margin-bottom: 1rem; }}
  .agent-text h3 {{ margin-bottom: 0.5rem; }}
  .agent-text h4 {{ margin-bottom: 1.5rem; color: var(--gold); font-style: italic; }}
  .agent-text p {{
    color: var(--parchment);
    line-height: 1.7; margin-bottom: 1rem;
  }}
  .agent-stats {{
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(201, 169, 97, 0.25);
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1.5rem;
  }}
  .agent-stat .stat-label {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 11px; font-weight: 500;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--slate); margin-bottom: 0.35rem;
  }}
  .agent-stat .stat-value {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 1.4rem; color: var(--gold);
    line-height: 1.2;
  }}
  .agent-stat .stat-value em {{ font-size: 1.2rem; }}

  /* SAFETY STRIPE */
  .safety {{
    background: var(--obsidian);
    padding: 5rem 6%;
    margin: 5rem 0 0;
  }}
  .safety .container {{
    max-width: 980px; margin: 0 auto;
    text-align: center;
  }}
  .safety .eyebrow {{ margin-bottom: 1.5rem; display: block; }}
  .safety h2 {{ margin: 0 auto 1.5rem; max-width: 22ch; }}
  .safety .safety-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin-top: 3rem;
    text-align: left;
  }}
  .safety-card {{
    padding: 1.5rem;
    border-left: 2px solid var(--gold);
    background: rgba(201, 169, 97, 0.04);
  }}
  .safety-card h4 {{
    font-family: 'Instrument Sans', sans-serif;
    font-style: normal; color: var(--parchment);
    font-size: 1rem; font-weight: 600;
    letter-spacing: 0.01em; margin-bottom: 0.5rem;
  }}
  .safety-card p {{
    font-size: 0.95rem; line-height: 1.6;
    color: var(--slate-deep); color: rgba(237, 232, 221, 0.75);
  }}

  /* FINAL CTA */
  .final-cta {{
    padding: 6rem 6% 5rem;
    text-align: center;
    background: linear-gradient(180deg, var(--ink), var(--obsidian));
  }}
  .final-cta .eyebrow {{ display: block; margin-bottom: 1.5rem; }}
  .final-cta h2 {{ margin: 0 auto 1.25rem; max-width: 22ch; }}
  .final-cta .subhead {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 1.2rem; line-height: 1.55;
    max-width: 50ch; margin: 0 auto 2.5rem;
  }}
  .final-cta .cta-support {{
    margin-top: 1rem;
    font-size: 0.9rem; color: var(--slate);
  }}

  /* FOOTER */
  footer {{
    background: var(--obsidian);
    color: var(--slate);
    padding: 3rem 6% 2rem;
    border-top: 1px solid rgba(201, 169, 97, 0.18);
  }}
  .footer-grid {{
    max-width: 1200px; margin: 0 auto;
    display: grid; grid-template-columns: 1.5fr 1fr 1fr; gap: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(201, 169, 97, 0.18);
  }}
  .footer-brand-block .footer-logo {{ height: 40px; width: auto; margin-bottom: 1rem; }}
  .footer-tagline {{ font-size: 0.95rem; }}
  .footer-col-title {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 11px; font-weight: 600;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--gold); margin-bottom: 0.75rem;
  }}
  .footer-col a {{
    display: block; color: var(--parchment);
    text-decoration: none; font-size: 0.95rem;
    padding: 0.25rem 0;
    border-bottom: 1px solid transparent;
    transition: color 0.2s ease, border-color 0.2s ease;
  }}
  .footer-col a:hover {{ color: var(--gold); border-bottom-color: var(--gold); }}
  .footer-meta {{
    max-width: 1200px; margin: 1.5rem auto 0;
    font-size: 0.85rem; text-align: center;
  }}
  .footer-meta a {{
    color: var(--slate); text-decoration: none;
    border-bottom: 1px solid rgba(107, 114, 128, 0.4);
    padding-bottom: 1px;
  }}
  .footer-meta a:hover {{ color: var(--gold); border-bottom-color: var(--gold); }}
  .footer-meta-sep {{ margin: 0 0.8rem; opacity: 0.5; }}

  /* RESPONSIVE */
  @media (max-width: 900px) {{
    .intro-stripe .container,
    .agent .container {{
      grid-template-columns: 1fr;
      gap: 2.5rem;
    }}
    .agent.image-left .container {{ direction: ltr; }}
    .agent-image {{ max-width: 480px; margin: 0 auto; }}
    .agent-stats {{ grid-template-columns: 1fr; gap: 1rem; }}
    .safety .safety-grid {{ grid-template-columns: 1fr; }}
  }}
  @media (max-width: 720px) {{
    .footer-grid {{ grid-template-columns: 1fr; gap: 2rem; }}
    .brand-bar .brand-logo {{ height: 36px; }}
    .hero {{ padding: 3.5rem 6% 4rem; }}
    .hero .cta-primary, .final-cta .cta-primary {{
      display: flex;
      justify-content: center;
      width: 100%;
    }}
    .intro-stripe {{ padding: 2.5rem 6%; margin: 1rem 0 3.5rem; }}
    .agent {{ padding: 2.5rem 0; }}
    .safety {{ padding: 3.5rem 6%; margin: 3rem 0 0; }}
    .final-cta {{ padding: 4.5rem 6% 4rem; }}
    .agent-stat .stat-value {{ font-size: 1.2rem; }}
  }}
  @media (max-width: 520px) {{
    .brand-bar .cta-ghost {{ font-size: 0.85rem; padding: 0.4rem 0; }}
    .hero .lede {{ font-size: 1.2rem; }}
    .agent-text h3 {{ font-size: 1.7rem; }}
  }}

  /* AI SENTINEL CURSOR (matches landing) */
  @media (hover: hover) {{
    html, body, a, button {{ cursor: none; }}
  }}
  .cursor-trail, .cursor-inner {{
    position: fixed; top: 0; left: 0;
    pointer-events: none; z-index: 9999;
    will-change: transform; mix-blend-mode: difference;
  }}
  .cursor-trail {{
    width: 40px; height: 40px;
    border: 1px solid rgba(201, 169, 97, 0.4);
    border-radius: 50%;
    background: radial-gradient(circle at center, rgba(201, 169, 97, 0.18), transparent 70%);
    transform: translate(-50%, -50%);
    transition: width 0.25s ease-out, height 0.25s ease-out, opacity 0.25s ease-out, border-color 0.25s ease-out;
    opacity: 0.7;
  }}
  .cursor-inner {{
    width: 28px; height: 28px; background: transparent;
    transform: translate(-50%, -50%);
    transition: transform 0.2s ease;
  }}
  .cursor-inner svg {{ width: 100%; height: 100%; overflow: visible; }}
  .cursor-inner .ring-outer {{ fill: none; stroke: #C9A961; stroke-width: 1.4; opacity: 0.95; }}
  .cursor-inner .tick {{ stroke: #C9A961; stroke-width: 1.6; stroke-linecap: round; }}
  .cursor-inner .iris-ring {{ fill: none; stroke: rgba(201, 169, 97, 0.7); stroke-width: 1; }}
  .cursor-inner .iris-core {{
    fill: #C9A961;
    transform-origin: center; transform-box: fill-box;
    animation: iris-pulse 2.2s ease-in-out infinite;
  }}
  .cursor-inner .scan {{
    stroke: rgba(201, 169, 97, 0.55); stroke-width: 0.9; stroke-linecap: round;
    transform-origin: 12px 12px;
    animation: scan-sweep 3s linear infinite;
  }}
  @keyframes iris-pulse {{
    0%, 100% {{ transform: scale(1); opacity: 1; }}
    50% {{ transform: scale(0.55); opacity: 0.75; }}
  }}
  @keyframes scan-sweep {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
  }}
  body.hover-cta .cursor-trail {{ width: 72px; height: 72px; opacity: 1; border-color: rgba(201, 169, 97, 0.7); }}
  body.hover-cta .cursor-inner {{ transform: translate(-50%, -50%) scale(1.45); }}
  body.hover-cta .cursor-inner .scan {{ animation-duration: 0.9s; }}
  body.hover-cta .cursor-inner .iris-core {{ animation-duration: 0.6s; }}
  body.hover-image .cursor-trail {{ width: 56px; height: 56px; border-color: rgba(201, 169, 97, 0.5); }}
  body.hover-image .cursor-inner .scan {{ animation-duration: 0.6s; }}
  @media (prefers-reduced-motion: reduce), (hover: none) {{
    html, body, a, button {{ cursor: auto !important; }}
    .cursor-inner, .cursor-trail {{ display: none !important; }}
  }}
</style>
</head>
<body>

<!-- BRAND BAR -->
<div class="brand-bar">
  <a href="{HOME_URL}" aria-label="Rogue Night home">
    <img class="brand-logo" src="data:image/png;base64,{LOGO_B64}" alt="Rogue Night">
  </a>
  <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="cta-ghost">
    Get your strategy <span class="cta-arrow">→</span>
  </a>
</div>

<!-- HERO -->
<section class="hero">
  <p class="eyebrow">Meet your AI workforce</p>
  <h1>Digital employees, <em>not chatbots.</em></h1>
  <p class="lede">Each one is specially configured for a specific job in your business — not a general-purpose assistant, but a focused worker that watches, drafts, follows up, and reports back. The exact mix that fits your business is mapped in your AI &amp; Automation Strategy.</p>
  <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="cta-primary">
    Get your AI &amp; Automation Strategy <span class="cta-arrow">→</span>
  </a>
</section>

<!-- INTRO STRIPE -->
<section class="intro-stripe">
  <div class="container">
    <div>
      <p class="eyebrow" style="margin-bottom: 0.75rem; display: block;">What we mean by digital employee</p>
      <h2>Not a chatbot. A <em>focused worker.</em></h2>
    </div>
    <div>
      <p>A chatbot answers questions. A digital employee <em>does work</em> — it reads incoming email, drafts replies, monitors your sales pipeline, chases compliance training, reviews dashboards, writes Friday's narrative. It works through your existing tools (HubSpot, Xero, SharePoint, Outlook, Slack) using the same access a junior team member would have.</p>
      <p>Every digital employee is configured for one specific job. It has a clear scope, a defined approval step, and a written brief you can read. We build them, supervise them through the first month, then hand over the keys. Your team stays in control. They never act without your sign-off on anything that goes outside the lines.</p>
    </div>
  </div>
</section>

<!-- AGENT 01 — Inbox Triage Specialist -->
<section class="agent">
  <div class="container">
    <div class="agent-text">
      <p class="eyebrow">Digital employee · 01</p>
      <h3>Inbox Triage Specialist</h3>
      <h4>Keeps your inbox manageable.</h4>
      <p>Reads incoming email as it arrives. Scores each thread by urgency and category using rules you set. Drafts replies for routine messages and waits for your approval before sending. Escalates anything ambiguous with a one-line summary, so you only handle the threads that actually need you.</p>
      <p>Works on top of Gmail, Outlook, or Front. Surfaces what's important in the morning; quietly handles the rest through the day.</p>
      <div class="agent-stats">
        <div class="agent-stat">
          <div class="stat-label">Replaces</div>
          <div class="stat-value">~1 hr/day inbox triage</div>
        </div>
        <div class="agent-stat">
          <div class="stat-label">Saves</div>
          <div class="stat-value"><em>8–12</em> hrs/mo</div>
        </div>
        <div class="agent-stat">
          <div class="stat-label">Goes live</div>
          <div class="stat-value">Week 1–2</div>
        </div>
      </div>
    </div>
    <div class="agent-image">
      <img src="{ASSET_BASE}/images/hero-agent.jpg" alt="An AI agent managing multiple business systems at once" loading="lazy" width="960" height="1191">
    </div>
  </div>
</section>

<!-- AGENT 02 — System Architect -->
<section class="agent image-left">
  <div class="container">
    <div class="agent-text">
      <p class="eyebrow">Digital employee · 02</p>
      <h3>Workflow Orchestrator</h3>
      <h4>Connects every tool you already use.</h4>
      <p>Builds and runs the automations between your business systems — your CRM, your accounting tool, your project board, your email. When a deal closes, the invoice gets drafted in Xero. When a form is submitted, the lead lands in HubSpot with context. When a project hits a milestone, the team gets notified in Slack with the right link.</p>
      <p>Built on Make, n8n, or Zapier depending on what fits your stack. The orchestrator runs quietly — most days you don't notice it. The savings show up in not having to remember to copy things between tools.</p>
      <div class="agent-stats">
        <div class="agent-stat">
          <div class="stat-label">Replaces</div>
          <div class="stat-value">Manual data entry between tools</div>
        </div>
        <div class="agent-stat">
          <div class="stat-label">Saves</div>
          <div class="stat-value"><em>5–10</em> hrs/mo per workflow</div>
        </div>
        <div class="agent-stat">
          <div class="stat-label">Goes live</div>
          <div class="stat-value">Week 4–6</div>
        </div>
      </div>
    </div>
    <div class="agent-image">
      <img src="{ASSET_BASE}/images/system-build.jpg" alt="An AI agent arranging a clean business system architecture" loading="lazy" width="1600" height="893">
    </div>
  </div>
</section>

<!-- AGENT 03 — Compliance Guardian -->
<section class="agent">
  <div class="container">
    <div class="agent-text">
      <p class="eyebrow">Digital employee · 03</p>
      <h3>Compliance Guardian</h3>
      <h4>Chases what's outstanding.</h4>
      <p>Tracks compliance training completions, contract renewals, sign-off deadlines, certification expiry dates — anything that needs to happen on a schedule but currently lives in a spreadsheet nobody checks. Drafts personalised chase emails for the people whose actions are overdue. Reports status weekly.</p>
      <p>For mid-sized businesses with regulator-facing requirements, this is the single highest-leverage agent we build. The hated weekly task becomes a five-minute Friday review.</p>
      <div class="agent-stats">
        <div class="agent-stat">
          <div class="stat-label">Replaces</div>
          <div class="stat-value">Friday compliance chase</div>
        </div>
        <div class="agent-stat">
          <div class="stat-label">Saves</div>
          <div class="stat-value"><em>4–8</em> hrs/mo</div>
        </div>
        <div class="agent-stat">
          <div class="stat-label">Goes live</div>
          <div class="stat-value">Week 8–10</div>
        </div>
      </div>
    </div>
    <div class="agent-image">
      <img src="{ASSET_BASE}/images/cta-thinking.jpg" alt="An AI agent in deliberate contemplation, reviewing a system architecture" loading="lazy" width="1600" height="893">
    </div>
  </div>
</section>

<!-- AGENT 04 — Operations Analyst -->
<section class="agent image-left">
  <div class="container">
    <div class="agent-text">
      <p class="eyebrow">Digital employee · 04</p>
      <h3>Operations Analyst</h3>
      <h4>Turns scattered data into a Friday narrative.</h4>
      <p>Every Friday afternoon, reads last week's pipeline, revenue, customer-support, and operations dashboards. Drafts a two-page narrative summarising what moved, what to watch, and where to focus next. Sends it to you or your department heads as a shareable email.</p>
      <p>The work most leaders <em>should</em> do every Friday — but rarely actually do — handled by a worker that doesn't get tired or distracted. Read it in two minutes; act on it in the next ten.</p>
      <div class="agent-stats">
        <div class="agent-stat">
          <div class="stat-label">Replaces</div>
          <div class="stat-value">Weekly board commentary</div>
        </div>
        <div class="agent-stat">
          <div class="stat-label">Saves</div>
          <div class="stat-value"><em>3–5</em> hrs/mo</div>
        </div>
        <div class="agent-stat">
          <div class="stat-label">Goes live</div>
          <div class="stat-value">Week 10–12</div>
        </div>
      </div>
    </div>
    <div class="agent-image">
      <img src="{ASSET_BASE}/images/outcomes-relaxed.jpg" alt="A business owner reviewing while AI agents work in the background" loading="lazy" width="1600" height="893">
    </div>
  </div>
</section>

<!-- SAFETY STRIPE -->
<section class="safety">
  <div class="container">
    <p class="eyebrow">How we work with you</p>
    <h2>You keep <em>control</em>. We keep them <em>supervised.</em></h2>
    <p style="max-width: 56ch; margin: 1rem auto 0; line-height: 1.7; color: rgba(237, 232, 221, 0.85);">Every digital employee we build runs through three safety rails. None of them is optional.</p>
    <div class="safety-grid">
      <div class="safety-card">
        <h4>Approval before action</h4>
        <p>Every email, every invoice, every customer-facing message is drafted, never sent. You see the draft. You click approve. The agent acts.</p>
      </div>
      <div class="safety-card">
        <h4>Scoped access only</h4>
        <p>Each digital employee gets the same access a junior team member would have — read where it needs to read, write only where it needs to write. Nothing more.</p>
      </div>
      <div class="safety-card">
        <h4>30 days of supervision</h4>
        <p>For the first 30 days after deployment, we watch the logs, catch the edge cases, and fix the rules. After that, the agent is yours to run, and we're a call away if it misbehaves.</p>
      </div>
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="final-cta">
  <p class="eyebrow">Start here</p>
  <h2>Which digital employees fit <em>your</em> business?</h2>
  <p class="subhead">The mix is different for every business. Your AI &amp; Automation Strategy maps out which agents would pay back fastest for your specific situation — what each one would save, what it would cost to build, and when to bring it online.</p>
  <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="cta-primary">
    Get your AI &amp; Automation Strategy <span class="cta-arrow">→</span>
  </a>
  <p class="cta-support">{PRICE_DISPLAY} · Delivered to your inbox in 48 hours · Yours to keep</p>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-grid">
    <div class="footer-brand-block">
      <a href="{HOME_URL}" aria-label="Rogue Night home">
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
      <a href="{HOME_URL}">Back to home</a>
    </div>
  </div>
  <div class="footer-meta">
    Rogue Night PTY LTD<span class="footer-meta-sep">·</span>ABN {ABN}<span class="footer-meta-sep">·</span>Australia<span class="footer-meta-sep">·</span><a href="{PRIVACY_URL}">Privacy</a><span class="footer-meta-sep">·</span><a href="{TERMS_URL}">Terms</a>
  </div>
</footer>

<!-- AI Sentinel cursor -->
<div class="cursor-trail" aria-hidden="true"></div>
<div class="cursor-inner" aria-hidden="true">
  <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <circle class="ring-outer" cx="12" cy="12" r="9"></circle>
    <line class="tick" x1="12" y1="0.6" x2="12" y2="2.6"></line>
    <line class="tick" x1="12" y1="21.4" x2="12" y2="23.4"></line>
    <line class="tick" x1="0.6" y1="12" x2="2.6" y2="12"></line>
    <line class="tick" x1="21.4" y1="12" x2="23.4" y2="12"></line>
    <circle class="iris-ring" cx="12" cy="12" r="4.2"></circle>
    <circle class="iris-core" cx="12" cy="12" r="1.8"></circle>
    <line class="scan" x1="12" y1="3.5" x2="12" y2="9.6"></line>
  </svg>
</div>
<script>
(function() {{
  var trail = document.querySelector('.cursor-trail');
  var inner = document.querySelector('.cursor-inner');
  if (!trail || !inner) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !matchMedia('(hover: hover)').matches) {{
    trail.style.display = 'none'; inner.style.display = 'none'; return;
  }}
  var mx = window.innerWidth / 2, my = window.innerHeight / 2, tx = mx, ty = my;
  window.addEventListener('mousemove', function(e) {{
    mx = e.clientX; my = e.clientY;
    inner.style.left = mx + 'px';
    inner.style.top = my + 'px';
  }});
  function loop() {{
    tx += (mx - tx) * 0.18; ty += (my - ty) * 0.18;
    trail.style.left = tx + 'px'; trail.style.top = ty + 'px';
    requestAnimationFrame(loop);
  }}
  loop();
  var body = document.body;
  document.querySelectorAll('a, button, .cta-primary, .cta-ghost').forEach(function(el) {{
    el.addEventListener('mouseenter', function() {{ body.classList.add('hover-cta'); }});
    el.addEventListener('mouseleave', function() {{ body.classList.remove('hover-cta'); }});
  }});
  document.querySelectorAll('.agent-image, img').forEach(function(el) {{
    el.addEventListener('mouseenter', function() {{ body.classList.add('hover-image'); }});
    el.addEventListener('mouseleave', function() {{ body.classList.remove('hover-image'); }});
  }});
}})();
</script>

</body>
</html>
"""

_OUT = os.path.join(_SCRIPT_DIR, 'rogue-night-agents.html')
with open(_OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
size_kb = os.path.getsize(_OUT) / 1024
mode_label = 'staging' if STAGING_MODE else 'production'
print(f"Agents page v1 written: {size_kb:.1f} KB · mode={mode_label}")

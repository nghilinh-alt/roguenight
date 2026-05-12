#!/usr/bin/env python3
"""Build the Rogue Night 404 page — editorial dark Ink with eclipse callback."""
import os

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_SCRIPT_DIR, 'data')

with open(os.path.join(_DATA, 'horizontal-b64.txt')) as f:
    LOGO_B64 = f.read().strip()
with open(os.path.join(_DATA, 'horizontal_sm-b64.txt')) as f:
    LOGO_SM_B64 = f.read().strip()

TALLY_URL = 'https://tally.so/r/xX4YaG'
ABN = '31 633 650 334'
SITE_URL = 'https://roguenight.com.au'

STAGING_MODE = os.environ.get('STAGING_MODE', 'true').lower() != 'false'
if STAGING_MODE:
    LANDING_URL = '#'
    PRIVACY_URL = 'https://hyperagent.com/api/files/usergenerated/threads/cmp0ar2ld0z7u07ad51te2m1a/artifacts/4199c54e-4981-4e05-892d-d4d1507df31a.html'
    TERMS_URL = 'https://hyperagent.com/api/files/usergenerated/threads/cmp11nt330hkq07ad6ehn9pxd/artifacts/f8837a40-77a5-4cf0-b05f-ac0c0d03a6f6.html'
else:
    LANDING_URL = '/'
    PRIVACY_URL = '/privacy/'
    TERMS_URL = '/terms/'

HTML = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Primary meta -->
<title>Lost in the night — Rogue Night</title>
<meta name="description" content="The page you are looking for could not be found. Return to the Rogue Night home page or book a Digital Health Check.">
<meta name="theme-color" content="#0A0E1A">
<meta name="robots" content="noindex,follow">

<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%230A0E1A'/%3E%3Ccircle cx='32' cy='32' r='14' fill='%23050608'/%3E%3Ccircle cx='32' cy='32' r='16' fill='none' stroke='%23C9A961' stroke-width='1.5' opacity='0.9'/%3E%3Ccircle cx='32' cy='32' r='20' fill='none' stroke='%23C9A961' stroke-width='0.8' opacity='0.4'/%3E%3C/svg%3E">

<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --ink: #0A0E1A;
    --obsidian: #050608;
    --gold: #C9A961;
    --ember: #C2410C;
    --parchment: #EDE8DD;
    --slate: #6B7280;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ height: 100%; }}
  body {{
    background: var(--ink);
    color: var(--parchment);
    font-family: 'Instrument Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 17px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }}
  em {{ font-family: 'Instrument Serif', Georgia, serif; font-style: italic; color: var(--gold); font-weight: 400; }}

  /* Brand bar */
  .brand-bar {{
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

  /* Hero — vertically centered */
  .hero {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 6rem 6%;
    position: relative;
  }}
  .hero .meta-code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 2.5rem;
    padding: 5px 12px;
    border: 1px solid rgba(201, 169, 97, 0.3);
    border-radius: 3px;
  }}
  .hero h1 {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-weight: 400;
    font-size: clamp(3.5rem, 9vw, 6.5rem);
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: var(--parchment);
    margin-bottom: 1.8rem;
    max-width: 16ch;
  }}
  .hero h1 em {{ color: var(--gold); font-style: italic; }}
  .hero .subhead {{
    font-size: 1.2rem;
    color: var(--parchment);
    opacity: 0.78;
    max-width: 44ch;
    margin-bottom: 3rem;
    line-height: 1.55;
  }}
  .ctas {{ display: flex; gap: 1.2rem; flex-wrap: wrap; justify-content: center; align-items: center; }}
  .cta-primary {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--ember);
    color: var(--parchment);
    padding: 0.95rem 1.8rem;
    border-radius: 4px;
    text-decoration: none;
    font-family: 'Instrument Sans', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 0.02em;
    transition: all 0.2s ease;
    border: 1px solid var(--ember);
  }}
  .cta-primary:hover {{ background: #d8500e; }}
  .cta-ghost {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--gold);
    text-decoration: none;
    font-family: 'Instrument Sans', sans-serif;
    font-weight: 500;
    font-size: 1rem;
    letter-spacing: 0.02em;
    border-bottom: 1px solid rgba(201, 169, 97, 0.45);
    padding-bottom: 3px;
    transition: all 0.2s ease;
  }}
  .cta-ghost:hover {{ color: var(--parchment); border-bottom-color: var(--parchment); }}

  /* Footer */
  footer {{
    background: var(--obsidian);
    color: var(--slate);
    padding: 2rem 6%;
    border-top: 1px solid rgba(201, 169, 97, 0.18);
    font-family: 'JetBrains Mono', 'SFMono-Regular', Menlo, monospace;
    font-size: 12px;
    letter-spacing: 0.04em;
    text-align: center;
  }}
  footer a {{
    color: var(--slate);
    text-decoration: none;
    border-bottom: 1px solid rgba(107, 114, 128, 0.35);
    padding-bottom: 1px;
    transition: all 0.2s ease;
  }}
  footer a:hover {{ color: var(--gold); border-bottom-color: var(--gold); }}
  .footer-meta-sep {{ margin: 0 0.8rem; opacity: 0.5; }}

  @media (max-width: 720px) {{
    .brand-bar .brand-logo {{ height: 44px; }}
    .hero {{ padding: 4rem 6%; }}
    .hero h1 {{ font-size: clamp(3rem, 12vw, 5rem); }}
    .ctas {{ flex-direction: column; gap: 1rem; }}
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

<!-- HERO -->
<main class="hero">
  <div class="meta-code">404 · Page Not Found</div>
  <h1>Lost in the <em>night.</em></h1>
  <p class="subhead">The page you were looking for has slipped past the horizon. Could be a stale link, a typo, or something we moved without redirecting properly.</p>
  <div class="ctas">
    <a href="{LANDING_URL}" class="cta-primary">Back to home <span>→</span></a>
    <a href="{TALLY_URL}" target="_blank" rel="noopener noreferrer" class="cta-ghost">Or book a Health Check <span>→</span></a>
  </div>
</main>

<!-- FOOTER -->
<footer>
  Rogue Night PTY LTD<span class="footer-meta-sep">·</span>ABN {ABN}<span class="footer-meta-sep">·</span>Australia<span class="footer-meta-sep">·</span><a href="{PRIVACY_URL}">Privacy</a><span class="footer-meta-sep">·</span><a href="{TERMS_URL}">Terms</a>
</footer>

</body>
</html>
"""

_OUT = os.path.join(_SCRIPT_DIR, 'rogue-night-404.html')
with open(_OUT, 'w') as f:
    f.write(HTML)

import os
size_kb = os.path.getsize(_OUT) / 1024
print(f"404 page written: {size_kb:.1f} KB")

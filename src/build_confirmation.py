#!/usr/bin/env python3
"""Build the post-Stripe-success confirmation page.

Output: src/rogue-night-confirmation.html → staged to public/confirmation/index.html.

Served at https://roguenight.com.au/confirmation/ as the Stripe Payment Link
success-redirect target. No URL parameters needed — the customer's email is
already known to Stripe at this point.

Brand and voice rules locked. See build_thank_you.py for the shared brand
CSS (kept duplicated here to keep each build script self-contained; if the
brand kit changes, update both scripts).
"""
import os
from pathlib import Path

SRC = Path(__file__).parent
DATA = SRC / "data"
OUT = SRC / "rogue-night-confirmation.html"
STAGING = os.environ.get("STAGING_MODE", "false").lower() == "true"

LOGO_B64 = (DATA / "horizontal-b64.txt").read_text().strip()

# Same brand CSS as build_thank_you.py — kept in sync intentionally.
BRAND_CSS = """
  :root {
    --ink: #0A0E1A; --obsidian: #050608; --gold: #C9A961;
    --gold-soft: rgba(201, 169, 97, 0.16); --gold-line: rgba(201, 169, 97, 0.32);
    --ember: #C2410C; --ember-soft: rgba(194, 65, 12, 0.10);
    --parchment: #EDE8DD; --parchment-deep: #E2DCCD;
    --slate: #6B7280; --slate-soft: #9CA3AF;
    --rule: rgba(10, 14, 26, 0.10); --hi: #2F855A; --hi-soft: rgba(47, 133, 90, 0.10);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
  body { font-family: 'Instrument Sans', -apple-system, system-ui, sans-serif; font-size: 16px; line-height: 1.65; color: var(--ink); background: var(--parchment); min-height: 100vh; display: flex; flex-direction: column; }
  .brand-bar { background: var(--ink); padding: 20px 0; border-bottom: 1px solid rgba(201, 169, 97, 0.18); }
  .brand-bar-inner { max-width: 1080px; margin: 0 auto; padding: 0 40px; display: flex; align-items: center; justify-content: space-between; }
  .brand-logo { height: 44px; width: auto; display: block; }
  .brand-tag { font-family: 'Instrument Sans', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: rgba(237, 232, 221, 0.65); }
  main { flex: 1; max-width: 720px; margin: 0 auto; padding: 80px 40px 96px; width: 100%; }
  .eyebrow { font-family: 'Instrument Sans', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold); margin-bottom: 24px; }
  h1 { font-family: 'Instrument Serif', Georgia, serif; font-size: 56px; line-height: 1.05; letter-spacing: -0.02em; color: var(--ink); font-weight: 400; margin-bottom: 28px; }
  h1 .accent { font-style: italic; color: var(--gold); }
  .lede { font-family: 'Instrument Serif', Georgia, serif; font-size: 21px; line-height: 1.5; color: var(--ink); font-style: italic; margin-bottom: 48px; max-width: 640px; }
  .next-steps { border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); padding: 32px 0; margin-bottom: 56px; }
  .next-steps-label { font-family: 'Instrument Sans', sans-serif; font-size: 11.5px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--slate); margin-bottom: 16px; }
  .next-steps ol { padding-left: 0; list-style: none; counter-reset: ns; }
  .next-steps li { counter-increment: ns; padding-left: 44px; position: relative; margin-bottom: 14px; font-size: 16px; line-height: 1.6; }
  .next-steps li::before { content: counter(ns, decimal-leading-zero); position: absolute; left: 0; top: 0; font-family: 'Instrument Serif', Georgia, serif; font-style: italic; color: var(--gold); font-size: 18px; width: 32px; }
  footer { background: var(--ink); color: rgba(237, 232, 221, 0.55); padding: 32px 0; text-align: center; border-top: 1px solid rgba(201, 169, 97, 0.18); }
  footer .footer-inner { max-width: 1080px; margin: 0 auto; padding: 0 40px; font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 11px; letter-spacing: 0.06em; }
  @media (max-width: 720px) {
    h1 { font-size: 38px; line-height: 1.1; }
    .lede { font-size: 18px; }
    main { padding: 56px 24px 80px; }
    .brand-bar-inner { padding: 0 24px; }
    .brand-tag { display: none; }
  }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Payment received &middot; Rogue Night</title>
  <meta name="robots" content="noindex, nofollow">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>__BRAND_CSS__</style>
</head>
<body>
<header class="brand-bar">
  <div class="brand-bar-inner">
    <img class="brand-logo" src="data:image/png;base64,__LOGO_B64__" alt="Rogue Night">
    <div class="brand-tag">AI &amp; Automation Strategy</div>
  </div>
</header>
<main>
  <div class="eyebrow">Step 03 &middot; Confirmed</div>
  <h1>Payment received. <span class="accent">We start tonight.</span></h1>
  <p class="lede">
    Thanks &mdash; your A$880 has landed. Stripe has emailed you a receipt for your records. We'll begin your specially curated strategy within 48 hours.
  </p>
  <div class="next-steps">
    <div class="next-steps-label">What happens from here</div>
    <ol>
      <li>We review your questionnaire end-to-end &mdash; the answers, the &ldquo;why&rdquo; behind them, the bits that surprised us.</li>
      <li>We draft your AI &amp; Automation Strategy: where your stack is now, where it could go, the digital employees that pay back fastest, and a phased rollout.</li>
      <li>It lands in your inbox as a PDF within 48 hours. Yours to keep, whatever you do next.</li>
      <li>Questions in the first 30 days? Reply to the email it came from. We're here.</li>
    </ol>
  </div>
  <div style="background: var(--gold-soft); border-left: 2px solid var(--gold); padding: 28px 32px; border-radius: 4px; margin-bottom: 28px;">
    <p style="font-family: 'Instrument Serif', Georgia, serif; font-style: italic; font-size: 19px; line-height: 1.5; color: var(--ink);">
      &ldquo;The work that runs while you sleep.&rdquo;
    </p>
    <p style="margin-top: 10px; font-size: 13.5px; color: var(--slate);">
      That's the promise. The report you'll receive is the first step in delivering on it.
    </p>
  </div>
  <p style="font-size: 14px; color: var(--slate);">
    Receipt or question? Email us at <a href="mailto:hello@roguenight.com.au" style="color: var(--ink); text-decoration: underline;">hello@roguenight.com.au</a>.
  </p>
</main>
<footer>
  <div class="footer-inner">
    Rogue Night PTY LTD &middot; ABN 31 633 650 334 &middot; Australia
  </div>
</footer>
</body>
</html>"""


def main():
    html = HTML_TEMPLATE.replace("__BRAND_CSS__", BRAND_CSS).replace("__LOGO_B64__", LOGO_B64)
    OUT.write_text(html)
    print(f"  ✓ rogue-night-confirmation.html ({len(html) // 1024} KB)")


if __name__ == "__main__":
    main()

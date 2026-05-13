#!/usr/bin/env python3
"""Build the branded thank-you page (rogue-night-thank-you.html) for the
Tally → Stripe payment flow.

Output: src/rogue-night-thank-you.html → staged to public/thank-you/index.html
        by build_all.py.

This page is served at https://roguenight.com.au/thank-you/ and is the
landing surface after a customer completes the Tally Digital Health Check
form. It offers two payment paths:

  1. Pay Now → opens the Stripe Payment Link at pay.roguenight.com.au
  2. Pay Later → calls /api/pay-later (Cloudflare Worker) which creates a
     Stripe Invoice with collection_method=send_invoice. Stripe emails the
     customer a Hosted Invoice Page link.

Source-of-truth lives in this script. The HTML is self-contained with the
horizontal lockup base64-embedded (src/data/horizontal-b64.txt).

Voice rules locked in (Phase 1 — never violate):
  - No "SME" or "SMEs" → "small to medium businesses" / "small business"
  - No "AI-generated" → "specially curated"
  - No founder name on the page
  - Delivery promise is 48 hours

STAGING_MODE env var:
  - "false" (default for build_all.py) → production output suitable for upload
  - "true" → minor variations for in-thread previews (currently no diff, but
    reserved for future use such as test Payment Link URLs)
"""
import os
from pathlib import Path

SRC = Path(__file__).parent
DATA = SRC / "data"
OUT = SRC / "rogue-night-thank-you.html"
STAGING = os.environ.get("STAGING_MODE", "false").lower() == "true"

LOGO_B64 = (DATA / "horizontal-b64.txt").read_text().strip()

# Phase 1 brand CSS — shared with build_confirmation.py
BRAND_CSS = """
  :root {
    --ink: #0A0E1A;
    --obsidian: #050608;
    --gold: #C9A961;
    --gold-soft: rgba(201, 169, 97, 0.16);
    --gold-line: rgba(201, 169, 97, 0.32);
    --ember: #C2410C;
    --ember-soft: rgba(194, 65, 12, 0.10);
    --parchment: #EDE8DD;
    --parchment-deep: #E2DCCD;
    --slate: #6B7280;
    --slate-soft: #9CA3AF;
    --rule: rgba(10, 14, 26, 0.10);
    --hi: #2F855A;
    --hi-soft: rgba(47, 133, 90, 0.10);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
  body {
    font-family: 'Instrument Sans', -apple-system, system-ui, sans-serif;
    font-size: 16px; line-height: 1.65; color: var(--ink); background: var(--parchment);
    min-height: 100vh; display: flex; flex-direction: column;
  }
  .brand-bar { background: var(--ink); padding: 20px 0; border-bottom: 1px solid rgba(201, 169, 97, 0.18); }
  .brand-bar-inner { max-width: 1080px; margin: 0 auto; padding: 0 40px; display: flex; align-items: center; justify-content: space-between; }
  .brand-logo { height: 44px; width: auto; display: block; }
  .brand-tag { font-family: 'Instrument Sans', sans-serif; font-size: 12px; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: rgba(237, 232, 221, 0.65); }
  main { flex: 1; max-width: 720px; margin: 0 auto; padding: 80px 40px 96px; width: 100%; }
  .eyebrow { font-family: 'Instrument Sans', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--gold); margin-bottom: 24px; }
  h1 { font-family: 'Instrument Serif', Georgia, serif; font-size: 56px; line-height: 1.05; letter-spacing: -0.02em; color: var(--ink); font-weight: 400; margin-bottom: 28px; }
  h1 .accent { font-style: italic; color: var(--gold); }
  .lede { font-family: 'Instrument Serif', Georgia, serif; font-size: 21px; line-height: 1.5; color: var(--ink); font-style: italic; margin-bottom: 48px; max-width: 640px; }
  .lede .you { font-style: normal; color: var(--gold); font-weight: 500; }
  .next-steps { border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); padding: 32px 0; margin-bottom: 56px; }
  .next-steps-label { font-family: 'Instrument Sans', sans-serif; font-size: 11.5px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--slate); margin-bottom: 16px; }
  .next-steps ol { padding-left: 0; list-style: none; counter-reset: ns; }
  .next-steps li { counter-increment: ns; padding-left: 44px; position: relative; margin-bottom: 14px; font-size: 16px; line-height: 1.6; }
  .next-steps li::before { content: counter(ns, decimal-leading-zero); position: absolute; left: 0; top: 0; font-family: 'Instrument Serif', Georgia, serif; font-style: italic; color: var(--gold); font-size: 18px; width: 32px; }
  .pay-section-eyebrow { font-family: 'Instrument Sans', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ink); margin-bottom: 20px; }
  .pay-buttons { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 28px; }
  .pay-btn { display: flex; flex-direction: column; align-items: flex-start; gap: 6px; padding: 22px 24px; border-radius: 4px; text-decoration: none; cursor: pointer; border: none; font-family: 'Instrument Sans', sans-serif; text-align: left; transition: transform 0.12s ease, box-shadow 0.12s ease; }
  .pay-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(10, 14, 26, 0.12); }
  .pay-btn:active { transform: translateY(0); }
  .pay-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
  .pay-btn .title { font-family: 'Instrument Serif', Georgia, serif; font-size: 22px; font-weight: 400; letter-spacing: -0.01em; }
  .pay-btn .sub { font-size: 13px; line-height: 1.45; opacity: 0.85; }
  .pay-btn.primary { background: var(--ink); color: var(--parchment); }
  .pay-btn.primary .title { color: var(--gold); font-style: italic; }
  .pay-btn.secondary { background: transparent; color: var(--ink); border: 1px solid var(--rule); }
  .pay-btn.secondary:hover { border-color: var(--gold); }
  .price-line { margin-top: 14px; font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 11.5px; letter-spacing: 0.06em; color: var(--slate); }
  .confirmation { display: none; margin-top: 28px; padding: 28px 32px; background: var(--hi-soft); border-left: 2px solid var(--hi); border-radius: 4px; animation: fadein 0.4s ease-out; }
  .confirmation.visible { display: block; }
  .confirmation h3 { font-family: 'Instrument Serif', Georgia, serif; font-size: 24px; font-weight: 400; color: var(--ink); margin-bottom: 10px; }
  .confirmation p { margin-bottom: 10px; }
  .confirmation p:last-child { margin-bottom: 0; }
  .confirmation .invoice-email { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 14px; background: rgba(10, 14, 26, 0.06); padding: 2px 8px; border-radius: 2px; }
  .error { display: none; margin-top: 28px; padding: 24px 28px; background: var(--ember-soft); border-left: 2px solid var(--ember); border-radius: 4px; }
  .error.visible { display: block; }
  .error h3 { font-family: 'Instrument Serif', Georgia, serif; font-size: 20px; font-weight: 400; color: var(--ember); margin-bottom: 8px; }
  @keyframes fadein { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
  footer { background: var(--ink); color: rgba(237, 232, 221, 0.55); padding: 32px 0; text-align: center; border-top: 1px solid rgba(201, 169, 97, 0.18); }
  footer .footer-inner { max-width: 1080px; margin: 0 auto; padding: 0 40px; font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 11px; letter-spacing: 0.06em; }
  @media (max-width: 720px) {
    h1 { font-size: 38px; line-height: 1.1; }
    .lede { font-size: 18px; }
    main { padding: 56px 24px 80px; }
    .brand-bar-inner { padding: 0 24px; }
    .pay-buttons { grid-template-columns: 1fr; }
    .brand-tag { display: none; }
  }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Digital Health Check is in · Rogue Night</title>
  <meta name="description" content="Thanks for completing the Digital Health Check questionnaire. Choose how you'd like to pay — we'll begin tonight.">
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
    <div class="brand-tag">Digital Health Check</div>
  </div>
</header>
<main>
  <div class="eyebrow">Step 02 · Payment</div>
  <h1>Your questionnaire is in. <span class="accent">Now, the work begins.</span></h1>
  <p class="lede" id="lede-text">
    Thanks <span class="you" id="customer-name">for completing the Digital Health Check</span> &mdash; we have everything we need to start building your report. Two ways to settle the A$350 fee, your call.
  </p>
  <div class="next-steps">
    <div class="next-steps-label">What happens next</div>
    <ol>
      <li>You pay (or schedule payment) using one of the two paths below.</li>
      <li>We draft your report within 48 hours, specially curated for your business.</li>
      <li>It lands in your inbox as a PDF, yours to keep. We'll be available for questions for 30 days.</li>
    </ol>
  </div>
  <div class="pay-section-eyebrow">Choose your payment path</div>
  <div class="pay-buttons">
    <a class="pay-btn primary" id="pay-now-link" href="#">
      <span class="title">Pay now</span>
      <span class="sub">Card, Apple Pay, Google Pay &mdash; secured by Stripe. We start tonight.</span>
    </a>
    <button class="pay-btn secondary" id="pay-later-btn" type="button">
      <span class="title">Send me an invoice</span>
      <span class="sub">Pay whenever you're ready. We hold off building until the invoice is paid.</span>
    </button>
  </div>
  <div class="price-line">A$350 flat &middot; Report delivered to your inbox in 48 hours &middot; Yours to keep</div>
  <div class="confirmation" id="confirmation">
    <h3>Invoice on the way.</h3>
    <p>We've just sent a Stripe invoice to <span class="invoice-email" id="invoice-email">your email</span>. Open it, click the secure payment link, settle when ready. Cards, Apple Pay, and bank transfer all accepted.</p>
    <p>Once it's paid, we'll begin your report within 48 hours.</p>
    <p style="margin-top: 16px; font-size: 14px; color: var(--slate);">Didn't see it? Check your spam folder. The sender is <strong>noreply@stripe.com</strong> with subject &ldquo;Invoice from Rogue Night PTY LTD&rdquo;. Or email us at <a href="mailto:hello@roguenight.com.au" style="color: var(--ink);">hello@roguenight.com.au</a>.</p>
  </div>
  <div class="error" id="error">
    <h3>Something went wrong.</h3>
    <p id="error-message">We couldn't send the invoice automatically. Email us at <a href="mailto:hello@roguenight.com.au" style="color: var(--ink);">hello@roguenight.com.au</a> and we'll send it manually.</p>
  </div>
</main>
<footer>
  <div class="footer-inner">
    Rogue Night PTY LTD &middot; ABN 31 633 650 334 &middot; Australia
  </div>
</footer>
<script>
(function() {
  var params = new URLSearchParams(window.location.search);
  var email = (params.get('email') || '').trim();
  var name = (params.get('name') || '').trim();
  var ref = (params.get('ref') || '').trim();
  var businessName = (params.get('business') || '').trim();
  if (name) {
    var firstName = name.split(' ')[0];
    document.getElementById('customer-name').textContent = firstName + ' — the form is in';
  }
  // Stripe Payment Link (default buy.stripe.com host — we skipped the
  // A$180/year custom domain in favour of buying URL polish later, if ever).
  var PAYMENT_LINK_BASE = 'https://buy.stripe.com/dRmaEZdvWgFb8vOg8NdIA03';
  var payNowUrl = PAYMENT_LINK_BASE;
  var qs = [];
  if (email) qs.push('prefilled_email=' + encodeURIComponent(email));
  if (ref) qs.push('client_reference_id=' + encodeURIComponent(ref));
  if (qs.length) payNowUrl += '?' + qs.join('&');
  document.getElementById('pay-now-link').setAttribute('href', payNowUrl);
  var btn = document.getElementById('pay-later-btn');
  btn.addEventListener('click', function() {
    if (!email) {
      showError("We don't have your email on file. Please go back and resubmit the form.");
      return;
    }
    btn.disabled = true;
    btn.querySelector('.title').textContent = 'Sending…';
    btn.querySelector('.sub').textContent = 'Creating the invoice in Stripe and emailing it to you.';
    fetch('/api/pay-later', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, name: name, business: businessName, ref: ref })
    }).then(function(r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function(data) {
      document.getElementById('invoice-email').textContent = email;
      document.getElementById('confirmation').classList.add('visible');
      document.querySelector('.pay-buttons').style.display = 'none';
      document.querySelector('.price-line').style.display = 'none';
      document.getElementById('confirmation').scrollIntoView({ behavior: 'smooth', block: 'center' });
    }).catch(function(err) {
      console.error('Pay later error', err);
      btn.disabled = false;
      btn.querySelector('.title').textContent = 'Send me an invoice';
      btn.querySelector('.sub').textContent = "Pay whenever you're ready. We hold off building until the invoice is paid.";
      showError("We couldn't send the invoice automatically.");
    });
  });
  function showError(msg) {
    var el = document.getElementById('error');
    document.getElementById('error-message').innerHTML = msg + ' Email us at <a href="mailto:hello@roguenight.com.au" style="color: var(--ink);">hello@roguenight.com.au</a> and we will send it manually.';
    el.classList.add('visible');
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
})();
</script>
</body>
</html>"""


def main():
    html = HTML_TEMPLATE.replace("__BRAND_CSS__", BRAND_CSS).replace("__LOGO_B64__", LOGO_B64)
    OUT.write_text(html)
    print(f"  ✓ rogue-night-thank-you.html ({len(html) // 1024} KB)")


if __name__ == "__main__":
    main()

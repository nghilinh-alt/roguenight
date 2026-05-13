# Payment Flow — Tally to Stripe

Step-by-step setup for the branded post-Tally payment experience: Stripe Payment Link on a custom subdomain, Hostinger-hosted thank-you and confirmation pages, Cloudflare Worker for the Pay-Later invoice automation, and Tally redirect configuration.

Estimated total setup: 60-90 minutes.

---

## Overview & architecture

**Goal:** Replace the current Tally → external Stripe Payment Link hand-off with a branded, RN-domain post-submit experience that offers Pay Now or Pay Later.

**Architecture (4 pieces, all free or transaction-fee-only):**

```
Tally form (free)
  → redirect with email/name/ref/business params
  → roguenight.com.au/thank-you/ (Hostinger static, Cloudflare-proxied)
     │
     ├─ Pay Now button → pay.roguenight.com.au/dhc-350?prefilled_email=...
     │    (Stripe Payment Link, custom domain, branded)
     │    → customer pays → roguenight.com.au/confirmation/
     │
     └─ Pay Later button → fetch POST /api/pay-later (Cloudflare Worker)
          → Worker calls Stripe Invoicing API (collection_method=send_invoice)
          → Stripe automatically emails the Hosted Invoice Page link
          → inline confirmation on thank-you page
```

**Monthly cost:** $0 + Stripe transaction fees on payments only.

**Files in this repo:**
- `public/thank-you/index.html` — built output (135 KB, self-contained with embedded logo). Source: `src/build_thank_you.py`.
- `public/confirmation/index.html` — built output (128 KB). Source: `src/build_confirmation.py`.
- `cloudflare-worker/worker-pay-later.js` — Cloudflare Worker code.
- `cloudflare-worker/wrangler.toml` — Worker config.

**Setup order:**
1. Stripe Dashboard — brand it, create the Payment Link, set up the custom domain, configure Invoicing
2. Hostinger — upload `public/thank-you/` and `public/confirmation/`
3. Cloudflare Worker — deploy and wire to `/api/*` route
4. Tally — configure the redirect with @-variables
5. End-to-end test with Stripe test mode

---

## Step 1 — Stripe Dashboard setup

**1.1 Brand your Stripe account** (5 min)

Dashboard → Settings → Business → Branding

- Logo: upload the Rogue Night horizontal lockup (`assets-raw/logo-horizontal.png` or similar)
- Icon: upload the simplified eclipse SVG (for favicons / small surfaces)
- Brand colour: `#0A0E1A` (Ink)
- Accent / button colour: `#C9A961` (Signet Gold)
- Font: System default is fine (Stripe doesn't load Instrument Serif)
- Display name: "Rogue Night PTY LTD"

This branding applies to every Stripe-hosted page — Payment Links, Checkout, Hosted Invoice Pages.

**1.2 Create the Payment Link for the Digital Health Check** (3 min)

Dashboard → Payment Links → + New

- Product: "Digital Health Check"
- Description: "Specially curated report for your small to medium business. Delivered within 48 hours."
- Price: A$350.00 (one-time)
- After payment: redirect to `https://roguenight.com.au/confirmation/`
- Customer information to collect: just email (other fields already captured by Tally)
- Save the link — you'll get a `https://buy.stripe.com/abc123xyz` URL.

**1.3 Set up the custom domain** (5 min)

Dashboard → Settings → Payment Links → Custom domains

- Add domain: `pay.roguenight.com.au`
- Stripe gives you a CNAME record to add at your DNS host (Cloudflare). Add it. Wait for verification (1-5 min).
- Once verified, your Payment Link URL becomes: `https://pay.roguenight.com.au/dhc-350` (set the slug `/dhc-350` after activating the custom domain).

**1.4 Configure Invoicing** (3 min)

Dashboard → Settings → Billing → Subscriptions and emails

- Email notifications: enable "Send finalized invoices and credit notes to customers" and "Send a receipt to the customer after a successful payment"
- Manage invoices sent to customers → enable "Send reminders if a recurring invoice hasn't been paid"
  - Reminders: 7 days before due, on due date, 7 days after due
- Apply your brand colour to invoice emails (auto-applied from step 1.1)

**1.5 Generate an API key for the Worker** (2 min)

Dashboard → Developers → API keys

- Use the existing **Secret key** (sk_live_... for production, sk_test_... for testing). For first deployment, start with the test key.
- Copy it. You'll paste it into the Worker as a secret in step 3.

---

## Step 2 — Hostinger: upload the HTML pages

Your existing site is on Hostinger. You'll add two new pages to the `public_html` upload.

**2.1 Build the pages locally**

```bash
cd src/
python3 build_all.py
```

This generates `public/thank-you/index.html` and `public/confirmation/index.html` (and refreshes all the other pages while it's at it).

**2.2 Upload to Hostinger**

Hostinger hPanel → File Manager → `public_html/`

Drag and drop the `thank-you/` and `confirmation/` folders (from `public/`) into `public_html/`. Hostinger File Manager preserves the folder structure — you'll end up with `public_html/thank-you/index.html` and `public_html/confirmation/index.html`.

If you're doing a full redeploy, just drag the contents of `public/` into `public_html/` (overwriting existing files). The `.htaccess` and `_headers` files are also part of `public/`.

**2.3 Verify**

Visit:
- `https://roguenight.com.au/thank-you/?email=test@example.com&name=Sample%20Owner&ref=abc123` — branded thank-you page with personalised lede.
- `https://roguenight.com.au/confirmation/` — branded confirmation page.

The Pay Later button won't work yet (Worker not deployed). The Pay Now button will fail because the Payment Link slug (`/dhc-350`) might not match your real Stripe Payment Link — update `src/build_thank_you.py` (`PAYMENT_LINK_BASE` constant) and re-run `build_all.py` once you've created the real link.

---

## Step 3 — Cloudflare Worker: pay-later automation

See [`cloudflare-worker/README.md`](../cloudflare-worker/README.md) for the full Worker deployment walkthrough. Quick summary:

1. Cloudflare Dashboard → Workers & Pages → Create → Worker, name `rogue-night-pay-later`
2. Paste the contents of `cloudflare-worker/worker-pay-later.js` into the editor, Save and Deploy
3. Settings → Variables, set secrets: `STRIPE_SECRET_KEY` (sk_test_... to start), `ALLOWED_ORIGIN` (`https://roguenight.com.au`)
4. Settings → Variables, set env vars: `PRODUCT_NAME`, `AMOUNT_CENTS=35000`, `CURRENCY=aud`, `DAYS_UNTIL_DUE=14`
5. Triggers → Routes → Add route: `roguenight.com.au/api/*` → Worker `rogue-night-pay-later`

**Test the Worker:**

```bash
curl https://roguenight.com.au/api/health
# Expected: {"ok":true,"worker":"rogue-night-pay-later"}

curl -X POST https://roguenight.com.au/api/pay-later \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","name":"Test Owner","business":"Test Pty Ltd","ref":"test-001"}'
# Expected: {"ok":true,"invoice_id":"in_...","hosted_invoice_url":"...","status":"open","customer_id":"cus_..."}
```

You should also receive a Stripe invoice email at the address you sent.

---

## Step 4 — Tally: configure the redirect

**4.1 Open the Tally form**

Go to https://tally.so/r/xX4YaG → Settings (gear icon) → Submission.

**4.2 Enable redirect on completion**

- Toggle on: **Redirect on completion**
- URL: `https://roguenight.com.au/thank-you`

**4.3 Add dynamic parameters**

Click the URL field and type `?` then `@`. Tally shows a dropdown of available fields.

Add query parameters:

```
https://roguenight.com.au/thank-you?email=@Contact_email&name=@Contact_name&business=@Business_name&ref=@Submission_id
```

The exact `@variable` names depend on the field labels Tally exposes. Use whichever is closest — the JavaScript in `thank-you.html` parses any of `email`, `name`, `business`, `ref` from the URL. Anything missing gets handled gracefully (the page falls back to generic copy).

**Important:** make sure the contact email field on the Tally form is required and validated. Without it, the Pay Later button can't work.

**4.4 Save and republish the form**

Tally requires a republish ("Publish" button) for changes to take effect.

**4.5 Verify**

Fill out the live Tally form yourself with a real email. After submit, you should land on the thank-you page with your details pre-populated.

---

## Step 5 — End-to-end test

Once all four pieces are deployed, run a full test in Stripe **test mode** (sk_test_... key):

### Test 1: Pay Now flow

1. Fill the live Tally form with a real email.
2. Land on `https://roguenight.com.au/thank-you/?email=...`. See your details pre-populated.
3. Click Pay Now → land on `https://pay.roguenight.com.au/dhc-350?prefilled_email=...` (Payment Link with your email pre-filled).
4. Use Stripe test card `4242 4242 4242 4242`, any future expiry, any CVC.
5. After payment, redirect to `https://roguenight.com.au/confirmation/` with the success message.
6. Check your inbox: Stripe should email a receipt.

### Test 2: Pay Later flow

1. Fill the live Tally form again with a different real email.
2. Land on the thank-you page.
3. Click "Send me an invoice".
4. Within 1-3 seconds, the inline confirmation should appear ("Invoice on the way").
5. Check that inbox: you should receive a Stripe invoice email from `noreply@stripe.com` with subject "Invoice from Rogue Night PTY LTD".
6. Email contains a link to the Hosted Invoice Page. Click it — page should be Rogue Night branded with the A$350 amount and payment buttons.
7. Pay using the test card. Invoice marks as paid in your Stripe dashboard.

### Test 3: Error handling

From a browser console on the thank-you page:

```javascript
fetch('/api/pay-later', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({}) })
  .then(r => r.json()).then(d => console.log(d))
```

Expected: `{"error":"A valid email is required."}` with status 400. This confirms validation is working.

**Once all three tests pass, swap the Stripe key from sk_test_... to sk_live_... in the Worker secrets and you're in production.**

---

## Maintenance & monitoring

**Monthly checks (5 min):**

- Stripe Dashboard → Payments: any failed attempts?
- Stripe Dashboard → Invoices: any past-due invoices needing manual nudge?
- Cloudflare Workers → your Worker → Metrics: requests, error rate

**Quarterly:**

- Rotate the Stripe API key (Stripe → Developers → API keys → Roll). Update the Worker secret.

**If something breaks:**

- Pay Now fails → check the Payment Link URL in `src/build_thank_you.py` (`PAYMENT_LINK_BASE` constant). Rebuild and re-upload.
- Pay Later fails → check Worker logs (Cloudflare Dashboard → your Worker → Logs). Common issues: invalid Stripe key, CORS origin mismatch, Tally redirect URL missing the email param.
- Tally redirect doesn't trigger → republish the form. Tally caches the previous version until you click Publish.

**Costs:**

- Cloudflare Workers free tier: 100,000 requests/day. You'll send dozens per month at most.
- Cloudflare Pages free tier: not applicable (site is on Hostinger).
- Stripe: 1.75% + A$0.30 per AU card transaction. International cards 2.9% + A$0.30. No monthly fee.

**Customer support scripts:**

- "I paid but didn't get the report" → check Stripe Dashboard for the payment. If paid, the report is in flight (48h SLA). If not, ask them to forward the Stripe receipt.
- "I didn't get the invoice" → check Stripe → Invoices for the customer's email. If present, resend from the dashboard. If absent, ask them to retry the Pay Later button or email hello@.
- "I want to cancel" → if pre-payment, no action needed (invoice expires after `DAYS_UNTIL_DUE` = 14 days). To formally void: Stripe Dashboard → Invoices → select → Void.

---

## Voice rules locked in across all surfaces

- No "SME" or "SMEs" — "small to medium businesses" or "small business"
- No "AI-generated" — "specially curated"
- No founder name on customer-facing pages
- "Australia" not "Australian" in metadata
- Delivery promise is 48 hours (not 24, not 2 business days)
- Phase 1 colour palette and typography throughout

See [`docs/operations/VOICE-RULES.md`](operations/VOICE-RULES.md) for the canonical voice rules list.

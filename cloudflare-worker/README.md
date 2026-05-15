# Cloudflare Worker — Pay Later

Handles the **Pay Later** path of the Tally → Stripe payment flow.

When a customer clicks "Send me an invoice" on `roguenight.com.au/thank-you/`, the page POSTs to `/api/pay-later`. Cloudflare proxying intercepts that path and routes it to this Worker. The Worker calls the Stripe Invoicing API to (1) create a Customer, (2) attach an Invoice Item, (3) create the Invoice in draft state, (4) **explicitly finalize** the invoice via `POST /v1/invoices/:id/finalize` so it moves to `status: open` with a populated `hosted_invoice_url`, and (5) **explicitly send** the invoice email via `POST /v1/invoices/:id/send`. The explicit send removes the brittle dependency on Stripe Dashboard's Customer Emails settings (which are disabled in test mode and inconsistent across live-mode accounts).

## Files

- `worker-pay-later.js` — the Worker source
- `wrangler.toml` — Cloudflare config (name, route, env vars)

## Deploy

### Path A — click and paste (no Node install required)

1. Cloudflare Dashboard → Workers & Pages → Create → Worker
2. Name it `rogue-night-pay-later`, click Deploy (the default "Hello World" code is fine for now)
3. Click "Edit code" and paste the contents of `worker-pay-later.js` over the default
4. Click Save and Deploy
5. Settings → Variables, set secrets (encrypted):
   - `STRIPE_SECRET_KEY` = `sk_test_...` (or `sk_live_...` once you're ready)
   - `ALLOWED_ORIGIN` = `https://roguenight.com.au`
6. Settings → Variables, set plain-text env vars:
   - `PRODUCT_NAME` = `AI & Automation Strategy`
   - `AMOUNT_CENTS` = `39500`
   - `CURRENCY` = `aud`
   - `DAYS_UNTIL_DUE` = `14`
7. Triggers → Routes → Add route: `roguenight.com.au/api/*` → Worker `rogue-night-pay-later`

### Path B — wrangler CLI

```bash
npm install -g wrangler
wrangler login
cd cloudflare-worker/
wrangler secret put STRIPE_SECRET_KEY    # paste your sk_test_... or sk_live_...
wrangler secret put ALLOWED_ORIGIN       # paste https://roguenight.com.au
wrangler deploy
```

The route binding in `wrangler.toml` does step 7 automatically.

## Test

After deployment, from your terminal:

```bash
curl https://roguenight.com.au/api/health
# Expected: {"ok":true,"worker":"rogue-night-pay-later"}

curl -X POST https://roguenight.com.au/api/pay-later \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","name":"Test Owner","business":"Test Pty Ltd","ref":"test-001"}'
# Expected: {"ok":true,"invoice_id":"in_...","hosted_invoice_url":"https://invoice.stripe.com/i/...","status":"open","customer_id":"cus_..."}
```

You should also receive a Stripe invoice email at the address you sent.

## Endpoints

- `POST /api/pay-later` — creates an invoice and emails the customer. Required body: `{ email, name?, business?, ref? }`
- `GET /api/health` — liveness check, returns `{ ok: true, worker: "rogue-night-pay-later" }`
- `OPTIONS /api/*` — CORS preflight

## Costs

Cloudflare Workers free tier: 100,000 requests per day. Your AI & Automation Strategy volume is dozens per month at most, so this stays free indefinitely. Stripe charges transaction fees only — no monthly fee.

## Voice rules

Don't violate when editing:

- No "SME" or "SMEs" in any customer-facing text — use "small to medium businesses" or "small business"
- No "AI-generated" — use "specially curated"

Both rules are baked into the Customer description and Invoice description in the Worker code. Keep them when editing.

See [`docs/PAYMENT-FLOW.md`](../docs/PAYMENT-FLOW.md) for the full architecture and end-to-end deployment walkthrough.

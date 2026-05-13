# Rogue Night — Deployment Guide

The site is live at <https://roguenight.com.au>, hosted on **Cloudflare Pages** with auto-deploy from this repo's `main` branch. The `/api/*` Pay-Later endpoint runs on a **Cloudflare Worker** bound to the same domain.

This guide covers how updates flow from this repo to production, how to deploy Worker code, how to verify after a change, and how DNS / SSL are managed.

> **Looking for the original Hostinger-era setup?** The site was previously deployed on Hostinger shared hosting via manual `public_html/` uploads. The Cloudflare Pages migration happened on 2026-05-13 as part of the payment-flow deployment. The full Hostinger-era guide is preserved in this repo's git history (look for commits before `5ac8ed8`).

---

## Architecture summary

| Piece | Where it lives | How it deploys |
|---|---|---|
| Static site (`public/`) | **Cloudflare Pages** project `roguenight-website` | Auto — every push to `main` triggers a build within 30–60 seconds |
| API `/api/*` | **Cloudflare Worker** `snowy-salad-ba26` (route `roguenight.com.au/api/*`) | Manual — repaste `cloudflare-worker/worker-pay-later.js` in the dashboard, Save and Deploy |
| DNS | **Cloudflare** (zone `roguenight.com.au`) | Nameservers: `adrian.ns.cloudflare.com`, `cullen.ns.cloudflare.com` |
| SSL | Cloudflare Universal SSL | Auto — no manual provisioning |
| Email | Hostinger registrar-level forwarding to `hello@roguenight.com.au` | Manual — Linh sends from Hostinger webmail (Google Workspace migration is a future decision) |
| Payments | Stripe — Payment Link `https://buy.stripe.com/dRmaEZdvWgFb8vOg8NdIA03` | Configured once in Stripe Dashboard |

Cloudflare account ID: `a18b9bc7aad669c66aad28fc193338f2`. Workers subdomain: `nghi-linh.workers.dev`.

---

## Updating the static site

```bash
cd src/
# Edit copy or styling in src/build_*.py — never edit public/*.html directly
python3 build_all.py            # rebuilds production HTML and stages everything into public/

# Verify the diff
cd ..
git status
git diff public/

# Commit and push
git add public/ src/
git commit -m "Describe the change"
git push origin main
```

Cloudflare Pages picks up the push and deploys within 30–60 seconds. You can watch the build at:

<https://dash.cloudflare.com/a18b9bc7aad669c66aad28fc193338f2/pages/view/roguenight-website>

---

## Updating the Cloudflare Worker

The Worker is NOT auto-deployed. Every change requires a manual paste-and-save in the Cloudflare dashboard.

1. Edit `cloudflare-worker/worker-pay-later.js` in this repo.
2. Commit and push to `main` (so the source-of-truth in this repo stays current).
3. Open <https://dash.cloudflare.com/a18b9bc7aad669c66aad28fc193338f2/workers/services/view/snowy-salad-ba26> → **Quick Edit** (or **Edit Code**).
4. Paste the new contents of `worker-pay-later.js`. Verify env vars are still set (`STRIPE_SECRET_KEY`, `ALLOWED_ORIGIN`, `PRODUCT_NAME`, `AMOUNT_CENTS`, `CURRENCY`, `DAYS_UNTIL_DUE`).
5. **Save and Deploy**.
6. Verify with the health endpoint (see below).

The full Worker walkthrough lives in `cloudflare-worker/README.md`.

---

## Verifying after a deploy

**Static site:**

```bash
curl -sI https://roguenight.com.au | head -3
# Expect: HTTP/2 200, Cloudflare server, cache-control set
```

**Worker `/api/*`:**

```bash
curl https://roguenight.com.au/api/health
# Expect: {"ok":true,"worker":"rogue-night-pay-later"}
```

**Visual checks** (open <https://roguenight.com.au> in an incognito window):

- ✅ Padlock icon (HTTPS valid)
- ✅ Landing page renders with eclipse logo, "Run your business smarter. With systems that work — even when you don't." hero
- ✅ "Get your AI & Automation Strategy" CTA opens the Tally form in a new tab
- ✅ "Download the sample (PDF, 23 pages)" downloads the sample report
- ✅ Footer Privacy + Terms links open the respective pages
- ✅ Brand bar logo click returns home
- ✅ 404 page: visit something like `https://roguenight.com.au/this-does-not-exist` and see "Lost in the night"

---

## End-to-end payment flow validation

Test mode (with Stripe `STRIPE_SECRET_KEY=sk_test_...` in the Worker):

1. Submit the Tally form at `https://tally.so/r/xX4YaG` with your details.
2. After submit, the form redirects to `roguenight.com.au/thank-you/?email=...&name=...&business=...&ref=...`.
3. Click **Pay Now** → Stripe Payment Link page → use test card `4242 4242 4242 4242`, expiry any future date, any CVC, any postcode.
4. After payment, you land on `roguenight.com.au/confirmation/`.
5. Stripe emails a receipt to the email you entered.

For the Pay-Later path:

1. Same flow up to the thank-you page.
2. Click **Send me an invoice** instead.
3. The thank-you page calls `/api/pay-later`, which creates a Stripe Invoice with `collection_method=send_invoice`.
4. Stripe emails the Hosted Invoice Page link to the customer.
5. Customer opens the email, clicks the link, pays via card / Apple Pay / bank transfer.

When you're ready to go live, swap `STRIPE_SECRET_KEY` in the Worker from `sk_test_...` to `sk_live_...`. See `docs/PAYMENT-FLOW.md` for the full live-mode swap walkthrough.

---

## Open Graph and SEO validation

After any change that touches metadata (title, description, OG tags, JSON-LD):

- <https://www.linkedin.com/post-inspector/> — render the OG card; LinkedIn caches aggressively
- <https://www.opengraph.xyz/> — should resolve all OG tags
- <https://search.google.com/test/rich-results> — JSON-LD should validate as `ProfessionalService` with the AI & Automation Strategy `Offer`

If a scraper has stale cache, append `?v=2` to the URL in the inspector and re-inspect.

Google Search Console: <https://search.google.com/search-console>. Sitemap submitted at `https://roguenight.com.au/sitemap.xml`.

---

## DNS and SSL

- **DNS:** managed in the Cloudflare dashboard under the `roguenight.com.au` zone.
- **SSL:** Cloudflare Universal SSL is enabled by default. No manual cert provisioning needed.

To edit DNS records:

1. <https://dash.cloudflare.com/a18b9bc7aad669c66aad28fc193338f2/roguenight.com.au> → DNS → Records.
2. Add or edit records.
3. Changes propagate globally within a minute or two.

---

## If the Pages build fails

1. Open the project in the Cloudflare dashboard.
2. Click the failing build to see the log.
3. Common causes: malformed HTML in `public/`, a build script referenced in `wrangler.toml` that doesn't exist, missing files.
4. Fix the issue locally, push another commit, the build re-triggers automatically.

---

## If the Worker `/api/*` route stops responding

1. Hit the health endpoint: `curl https://roguenight.com.au/api/health`. If it returns JSON, the Worker is up — issue is in your call.
2. If it doesn't respond, open the Worker in the dashboard → Logs → enable real-time. Trigger a request and watch what happens.
3. Check that the route `roguenight.com.au/api/*` is still bound: Workers → Triggers → Routes.

---

## Email

Email at `hello@roguenight.com.au` is registrar-level forwarding via Hostinger — receives only, no real send/receive. Lois drafts emails as TEXT for Linh to copy-paste into Hostinger webmail and send manually.

Trigger to revisit Google Workspace migration: 10+ reports/month volume, OR Anna voice agent needs Calendar integration.

---

## Help

For build-system questions: `README.md` in the repo root.
For brand voice and visual rules: `docs/BRAND-KIT.md`.
For Open Graph specs: `docs/OG-METADATA.md`.
For payment-flow setup and live-mode swap: `docs/PAYMENT-FLOW.md`.

Anything stuck? `hello@roguenight.com.au` works once any email forwarding rule is in place.

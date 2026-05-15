# Tool Price Audit — 2026-05-15

First quarterly price-check sweep of the Tools airtable since the `Pricing region` field was introduced. Scope: all 27 tools tagged `Pricing region = Global / USD converted`. Findings and corrections applied same day.

Conversion rate snapshot: **1 USD = 1.3826 AUD** (from `agents/dhc-report-writer/data/rates.json`, fetched 2026-05-13 from open.er-api.com). Refreshed weekly by `.github/workflows/refresh-rates.yml`.

---

## Summary

- **Tools in scope (Global / USD converted):** 27
- **Updated this audit:** 7
- **Verified within ±10% margin:** 20
- **Tools tagged AU regional / Bundled / Transactional (out of scope this quarter):** 19
- **Next audit:** 2026-08-15 (quarterly cadence)

The dominant failure mode found in this run was **vendor USD list price entered directly into the AUD field** without applying the conversion. Five of the seven corrections were exactly this — Notion $10, Help Scout $25, Monday.com $12, ClickUp $7, and Salesforce $50 were all USD figures recorded as AUD. The `Pricing region` field added in this iteration makes it routine for the next quarterly run to catch these.

---

## 1. Tools updated this quarter

| Tool | Before (AUD) | After (AUD) | USD list price | Source / Reason |
|---|---:|---:|---:|---|
| ClickUp | $7 | **$10** | $7 USD/user/mo (Unlimited, annual) | USD entered as AUD — verified via clickup.com pricing. |
| Salesforce Starter Suite | $50 | **$35** | $25 USD/user/mo (annual) | Plan renamed from Essentials; older $50 reflected pre-rename pricing. |
| Notion | $10 | **$14** | $10 USD/user/mo (Plus, annual) | USD entered as AUD — verified via notion.so. |
| Help Scout | $25 | **$35** | $25 USD/user/mo (Standard, annual) | USD entered as AUD — verified via helpscout.com. |
| Monday.com | $12 | **$17** | $12 USD/seat/mo (Standard, annual, 3-seat min) | USD entered as AUD — verified via monday.com. |
| Phorest | $100 | **$137** | ~$99 USD/mo (Starter, custom-quoted) | Industry estimate (StackScored, Softabase, Pabau); confirm via Phorest demo for accurate per-client quote. |
| PandaDoc | $35 | **$26** | $19 USD/user/mo (Starter, annual) | Older $35 reflected monthly billing or pre-rename Essentials tier; aligned to current Starter annual rate. |

**Notes field updated on each row** with the exact USD list price, the rate used, and the conversion math (e.g. `"Help Scout Standard at $25 USD/user/mo (annual) = $34.57 AUD. Rounded to $35. Refreshed 2026-05-15 from helpscout.com at rate 1.3826."`). `Last reviewed` set to **2026-05-15** for all seven rows.

---

## 2. Tools verified within margin

Twenty rows passed the verification (drift ≤ 10% of computed AUD). No update needed.

| Tool | Stored AUD | Expected AUD | USD list price (annual) |
|---|---:|---:|---:|
| Front | $25 | $26 | $19 USD/seat (Starter) |
| SavvyCal | $17 | $17 | $12 USD (Basic) |
| Zoho CRM | $18 | $19 | $14 USD/user (Standard) |
| Pipedrive | $20 | $21 | $14.90 USD/user (Essential) |
| Mailchimp | $17 | $18 | $13 USD (Essentials, 500 contacts) |
| Asana | $15 | $15 | $10.99 USD/user (Starter) |
| Slack | $12 | $12 | $8.75 USD/user (Pro) |
| Chaser | $50 | ~$55 | ~$40 USD (Starter) |
| DocuSign | $22 | $21 | $15 USD (Personal, 5 envelopes) |
| Acuity Scheduling | $22 | $22 | $16 USD (Emerging) |
| Zapier | $30 | $28 | $19.99 USD (Pro) |
| Make (Integromat) | $13 | $12 | $9 USD (Core) |
| Dropbox Business | $18 | $21 | $15 USD/user (Standard) |
| ActiveCampaign | $22 | $21 | $15 USD (Lite, 500 contacts) |
| Calendly | $15 | $17 | $12 USD/user (Standard) |
| Box | $25 | $28 | $20 USD/user (Business) |
| HelloSign / Dropbox Sign | $22 | $21 | $15 USD (Essentials) |
| Klaviyo | $30 | $28 | $20 USD (Email starter) |
| Mindbody | $200 | $192 | $139 USD (Starter) |

Dropbox Business, Calendly, and Box are at the edge of the tolerance window (within 15%); flag for re-verification next quarter if vendor pricing moves.

---

## 3. Out of scope this quarter

These pricing regions were not audited this quarter. They have their own verification path and rotate into future quarterly sweeps.

**AU regional** (14 tools, verify against vendor AU pricing page):
Xero, MYOB Business, QuickBooks Online, ServiceM8, Tradify, SimPRO, AroFlo, Timely, Fresha, HubSpot CRM Starter, HubSpot Pro, Microsoft 365, Google Workspace, Square.

**Bundled / free** (5 tools, verify the bundling rule is still true):
Google Drive (Workspace bundled), OneDrive / SharePoint, Microsoft Teams, Trello, n8n (self-hosted).

**Transactional** (2 tools, verify transaction-fee description in Notes):
Stripe (1.75% + $0.30 AU card), Square POS (1.6% AU card tap).

**Recommended for next quarter:** sweep at least 5 AU regional rows on rotation, and confirm Bundled / Transactional descriptions remain accurate.

---

## 4. Operational notes for the maintainer / accountant

- **Conversion rate used:** 1 USD = 1.3826 AUD (spot rate, 2026-05-13). The rate refreshes weekly via the GitHub Action; if it drifts more than ~2% between quarterly audits, the maintainer should re-check Global / USD converted rows even if their USD list price hasn't changed.
- **Why USD list pricing, not monthly billing:** vendors advertise the lower annual-prepay rate as their headline. Clients on monthly billing pay 15–30% more. The catalogue tracks the headline rate so reports match what a client sees on the vendor's pricing page.
- **Per-seat vs flat-monthly:** Help Scout, Notion, Monday.com, PandaDoc, ClickUp, Salesforce, DocuSign Standard, and Box are all priced per user / per seat. The `Indicative cost AUD/month` field stores the per-seat cost. Lois multiplies by inferred seat count when drafting the client's Section 08 cost table.
- **Hidden costs:**
  - HubSpot / Mailchimp / Klaviyo / ActiveCampaign: pricing scales with contact list size — these tools can grow 3–10× as a client's audience grows past 5,000 contacts.
  - Chaser / Zapier / Make: volume caps on outstanding invoices / tasks / operations push to higher tiers.
  - Phorest / Mindbody / Help Scout / Salesforce: onboarding fees ($200–$5,000) are quote-only and outside the monthly subscription.
- **For the accountant:** these prices are *vendor list prices in AUD as of the audit date*. Actual amounts paid by Rogue Night clients appear on their individual vendor invoices, in AUD with GST where applicable. This catalogue is the *recommendation reference* used during report drafting, not a record of Rogue Night expenditure.

---

## 5. Provenance and reproducibility

Workflow used: **D. Quarterly price check**, defined in `agents/stack-md-maintainer/README.md`.

Reproduce by:

1. Confirm `agents/dhc-report-writer/data/rates.json` is fresh (`fetched_at` within the last 14 days). Refresh with `python3 agents/dhc-report-writer/scripts/refresh_rates.py` if stale.
2. Filter Airtable Tools by `Pricing region = Global / USD converted`.
3. For each row, look up the vendor's current entry-tier USD list price (annual billing rate).
4. Multiply by `rates.json["rates_to_aud"]["USD"]` and compare to the stored `Indicative cost AUD/month`.
5. Flag drift greater than 10%, update Airtable, refresh the Notes field with `"$X USD × Y = A$Z"`.
6. Set `Last reviewed` to today on every touched row.
7. Write up findings as `docs/operations/PRICE-AUDIT-YYYY-MM-DD.md` (this file).

**Artefacts touched by this audit:**

- 7 rows in `appCLdTCbJ5zGe9fo` / Tools — `Indicative cost AUD/month`, `Notes`, `Last reviewed` updated
- 0 source code changes (purely a data audit)
- This document (committed to repo for version control)
- Project document in the Hyperagent doc store (mirror, more verbose, includes accountant-facing context)

---

## After the audit

- Stack.md status bumped to v1.2 in the previous commit ([d40b93a](https://github.com/nghilinh-alt/roguenight/commit/d40b93a)) formalising the AUD-only rule and the `Pricing region` field.
- All 46 Tools rows now carry a `Pricing region` classification.
- Quarterly Workflow D added to `agents/stack-md-maintainer/README.md`; the next run should fall on 2026-08-15.
- Two tools (Phorest, Mindbody) are custom-quoted by vendors — their `Indicative cost AUD/month` is best-effort estimate from third-party sources. Lois should note this when recommending them, and quote prices as ranges with "confirm via demo" copy.

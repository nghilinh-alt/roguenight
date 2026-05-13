# Vetted Stack — Tool Catalogue

> **Status:** v1.1, 2026-05-04. Linh's first curation pass complete — all 41 starter rows confirmed as-is and flipped to `Yes` in the Linh-vetted column. Last-reviewed dates rolled forward to today. Additions deferred to a follow-up pass before first prospect test. See `README.md` for categorisation logic, pain tag schema, and maintenance cadence.

This file is grep-friendly markdown for now. Migrate to `.xlsx` when the catalogue exceeds ~80 entries.

---

## How to read this table

- **Difficulty:** Simple / Medium / Hard (implementation effort)
- **Ceiling:** Starter / Pro / Enterprise (scales to what team size)
- **Pain tags:** match Section C2 of the questionnaire — `manual-entry` `lead-tracking` `invoicing` `comms` `reporting` `documents` `onboarding` `compliance`
- **Last reviewed:** YYYY-MM-DD (must be within 12 months — older = flagged for refresh)
- **Linh-vetted:** Yes / No / Pending / `[STARTER — Linh to confirm]`

---

## Accounting & finance

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| Xero | Accounting | Simple | Pro | `invoicing` `reporting` `compliance` | AU/NZ SMEs, especially services & trades | Inventory features are weak — not for retail with complex stock | 2026-05-04 | Yes |
| MYOB | Accounting | Medium | Pro | `invoicing` `reporting` `compliance` | AU SMEs with payroll-heavy operations | Older UI than Xero; cheaper at scale though | 2026-05-04 | Yes |
| QuickBooks Online | Accounting | Simple | Pro | `invoicing` `reporting` | SMEs with US/global operations | Less widely used in AU; integrations skew US | 2026-05-04 | Yes |
| Stripe | Payments | Simple | Pro | `invoicing` | SMEs taking online payments | Fees compound at scale; reconciliation needs an accounting integration | 2026-05-04 | Yes |
| Chaser | Invoice chasing | Simple | Starter | `invoicing` | SMEs with chronic late-payment issue, already on Xero/QB | Email-template feel can be obvious — needs personalisation | 2026-05-04 | Yes |

---

## CRM & lead management

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| HubSpot Free / Starter | CRM | Simple | Starter | `lead-tracking` `comms` | SMEs new to CRM, under 25 staff | Free tier features get progressively limited; pricing jumps hard | 2026-05-04 | Yes |
| HubSpot Pro | CRM | Medium | Pro | `lead-tracking` `comms` `reporting` | SMEs 25–100 with serious sales motion | Cost compounds with seat count; locks SMEs in | 2026-05-04 | Yes |
| Pipedrive | CRM | Simple | Pro | `lead-tracking` | Sales-led SMEs wanting a clean pipeline view | Reporting weaker than HubSpot at the same tier | 2026-05-04 | Yes |
| Salesforce Essentials / Starter | CRM | Hard | Enterprise | `lead-tracking` `comms` `reporting` | SMEs on track to enterprise, with budget for setup | Overkill for <50 staff; setup is its own project | 2026-05-04 | Yes |
| Zoho CRM | CRM | Medium | Pro | `lead-tracking` `comms` | Cost-sensitive SMEs; Zoho-suite users | UI feels dated; ecosystem lock-in is real | 2026-05-04 | Yes |

---

## Project management & operations

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| Trello | Project mgmt | Simple | Starter | `lead-tracking` `onboarding` | Small teams, simple visual tracking | Doesn't scale past ~15 people coordinating | 2026-05-04 | Yes |
| Asana | Project mgmt | Simple | Pro | `lead-tracking` `onboarding` `reporting` | SMEs running multiple parallel projects | Reporting depends on which tier — basic tier is thin | 2026-05-04 | Yes |
| Monday.com | Project mgmt | Medium | Pro | `lead-tracking` `onboarding` `reporting` `compliance` | SMEs that want flexibility / customisation | Per-seat pricing punishes growth; configuration sprawl | 2026-05-04 | Yes |
| ClickUp | Project mgmt | Medium | Pro | `lead-tracking` `onboarding` `reporting` | SMEs wanting one tool to do everything | "One tool to do everything" rarely lands well; UI complex | 2026-05-04 | Yes |
| Notion | Knowledge + light PM | Simple | Pro | `documents` `onboarding` | SMEs that document well; knowledge-heavy services | Easy to make a mess; needs structural discipline | 2026-05-04 | Yes |

---

## Field service & trades

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| ServiceM8 | Field service | Simple | Pro | `lead-tracking` `invoicing` `comms` | AU/NZ trades, small to mid | Reporting limits surface around 30 staff | 2026-05-04 | Yes |
| Tradify | Field service | Simple | Starter | `invoicing` `lead-tracking` | Solo / small trades, AU/NZ | Outgrows quickly past 10 staff | 2026-05-04 | Yes |
| SimPRO | Field service | Hard | Enterprise | `lead-tracking` `invoicing` `compliance` `reporting` | Trades 20+ with serious project complexity | Long implementation; expensive; not for solo trades | 2026-05-04 | Yes |
| AroFlo | Field service | Medium | Pro | `lead-tracking` `invoicing` `compliance` | AU trades scaling past 10 | Mobile UX is the make-or-break for adoption | 2026-05-04 | Yes |

---

## Salon & personal services

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| Fresha | Salon booking + POS + customer DB | Simple | Pro | `manual-entry` `comms` `reporting` `onboarding` | AU salons under 15 staff, budget-tight, walk-in heavy — nails, hair, beauty | Aggressive upsell on paid marketing add-ons; pay-per-SMS pricing adds up on large campaigns | 2026-05-09 | Yes |
| Phorest | Salon booking + POS + loyalty | Medium | Pro | `manual-entry` `comms` `reporting` `onboarding` `compliance` | Hair, beauty, and spa businesses 5–50 staff wanting loyalty + branded app + multi-location | More expensive than Fresha; per-staff pricing punishes growth | 2026-05-09 | Pending |
| Timely | Salon booking + POS | Simple | Pro | `manual-entry` `comms` `reporting` `onboarding` | AU/NZ hair and beauty salons; Australasia-built, good Xero sync | Per-staff pricing scales hard past 5–6 stylists; reporting weaker than Phorest | 2026-05-09 | Pending |
| Mindbody | Wellness + class-based scheduling | Hard | Enterprise | `manual-entry` `comms` `reporting` `onboarding` `compliance` | Yoga, pilates, fitness, wellness studios with class-based scheduling | Expensive setup; configuration is its own project; less ideal for walk-in salons specifically | 2026-05-09 | Pending |

---

## Communications & inbox

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| Google Workspace | Office suite | Simple | Pro | `comms` `documents` `onboarding` | SMEs starting fresh or breaking from local files | Sharing model needs governance — easy to leak documents | 2026-05-04 | Yes |
| Microsoft 365 | Office suite | Medium | Enterprise | `comms` `documents` `onboarding` `compliance` | SMEs already on Outlook / SharePoint, regulated industries | License sprawl; multiple SKUs confuse pricing | 2026-05-04 | Yes |
| Slack | Team chat | Simple | Pro | `comms` | Tech-comfortable teams, project-driven | Free-tier history limits; integrations get expensive | 2026-05-04 | Yes |
| Microsoft Teams | Team chat + meetings | Medium | Enterprise | `comms` `documents` | M365 SMEs (already paid for it) | Setup quirks if you're not already in the M365 ecosystem | 2026-05-04 | Yes |
| Front | Shared inbox | Medium | Pro | `comms` | Small ops / support teams overwhelmed by shared inboxes | Pricing per user adds up; needs adoption discipline | 2026-05-04 | Yes |
| Help Scout | Shared inbox / support | Simple | Pro | `comms` | Customer-facing teams wanting clean handoffs | Less feature-rich than Front at higher tiers | 2026-05-04 | Yes |

---

## Document & file management

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| Google Drive | File storage | Simple | Pro | `documents` `compliance` | Google Workspace SMEs | Permissioning is easy to mis-configure | 2026-05-04 | Yes |
| OneDrive / SharePoint | File storage | Medium | Enterprise | `documents` `compliance` | M365 SMEs, regulated industries | SharePoint setup is a project of its own | 2026-05-04 | Yes |
| Dropbox Business | File storage | Simple | Pro | `documents` | SMEs already on Dropbox personal | Pricier than Drive/OneDrive at scale | 2026-05-04 | Yes |
| Box | File storage | Medium | Enterprise | `documents` `compliance` | Compliance-heavy SMEs (legal, healthcare) | More expensive; setup-heavy | 2026-05-04 | Yes |

---

## Scheduling & meetings

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| Calendly | Scheduling | Simple | Pro | `comms` `lead-tracking` | Sales / advisory SMEs taking inbound bookings | Brand "Calendly" link can feel impersonal — customise it | 2026-05-04 | Yes |
| Acuity Scheduling | Scheduling | Simple | Pro | `comms` `lead-tracking` | Service businesses with paid bookings | Owned by Squarespace — integration depth varies | 2026-05-04 | Yes |
| SavvyCal | Scheduling | Simple | Starter | `comms` | SMEs sending calendar links to other busy people | Smaller ecosystem than Calendly | 2026-05-04 | Yes |

---

## E-signature & documents

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| DocuSign | E-signature | Simple | Enterprise | `documents` `compliance` | SMEs with frequent contract flow | Pricing tiers add seats fast | 2026-05-04 | Yes |
| HelloSign / Dropbox Sign | E-signature | Simple | Pro | `documents` `compliance` | SMEs already on Dropbox / wanting a cheaper DocuSign | Less feature-rich than DocuSign for complex routing | 2026-05-04 | Yes |
| PandaDoc | Documents + e-sig | Medium | Pro | `documents` `invoicing` `compliance` | SMEs producing many proposals / quotes | Template management is the actual setup work | 2026-05-04 | Yes |

---

## Marketing & email

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| Mailchimp | Marketing email | Simple | Starter | `comms` `lead-tracking` | SMEs starting newsletter / nurture flows | Pricing scales harshly with list size | 2026-05-04 | Yes |
| Klaviyo | Marketing email | Medium | Pro | `comms` `lead-tracking` | E-commerce SMEs | Overkill for non-e-comm; integration depth most useful with Shopify | 2026-05-04 | Yes |
| ActiveCampaign | Marketing email + automation | Medium | Pro | `comms` `lead-tracking` | Service SMEs wanting nurture automation | Steeper learning curve than Mailchimp | 2026-05-04 | Yes |

---

## Workflow automation (the "glue" layer)

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| Zapier | No-code automation | Simple | Pro | `manual-entry` `lead-tracking` `invoicing` | SMEs wanting to glue their existing tools together | Cost of "tasks" compounds with volume; debugging is painful | 2026-05-04 | Yes |
| Make (formerly Integromat) | No-code automation | Medium | Pro | `manual-entry` `lead-tracking` `invoicing` `reporting` | Tech-comfortable SMEs wanting more power than Zapier | Visual flow builder has a learning curve | 2026-05-04 | Yes |
| n8n (self-hosted) | Open-source automation | Hard | Pro | `manual-entry` `lead-tracking` `invoicing` `reporting` | Cost-sensitive SMEs with internal tech, OR Rogue Night running it on their behalf | Self-hosting is real ops work; not for the un-technical | 2026-05-04 | Yes |

---

## AI assistants (tier 3 building blocks)

> Note: this row is the natural input to tier 3 agent-build engagements, not a tier 1 recommendation. The Digital Health Check report should NOT be recommending these tools directly to SMEs in most cases — the tier 3 agents Rogue Night builds sit on top of these.

| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |
|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|
| OpenAI API | LLM API | Medium | Enterprise | (used by all tier 3 agents) | Tier 3 agent foundation; widely supported | Cost-per-token compounds; data residency considerations | 2026-05-04 | Yes |
| Anthropic API (Claude) | LLM API | Medium | Enterprise | (used by all tier 3 agents) | Tier 3 agent foundation; longer context, careful reasoning | Pricing tiers; AU data residency check | 2026-05-04 | Yes |
| Local Ollama (qwen, llama) | Local LLM | Hard | Pro | (used by tier 3 agents needing privacy) | SMEs with strong privacy needs and Rogue Night running infra | Hardware requirements; tool-calling reliability still maturing | 2026-05-04 | Yes |

---

## How Linh curates this list

1. **Walk every row.** Anything you've personally used, recommended, or have a strong opinion on — change `[STARTER — Linh to confirm]` to `Yes` and add a note in the "Best for" or "Watch out for" field if your view differs.
2. **Reject what doesn't belong.** Anything you wouldn't recommend to a real SME — delete the row or change to `No` with a one-line reason in "Watch out for".
3. **Add what's missing.** Tools you've used and would recommend that aren't here — add a row.
4. **Update "Last reviewed"** for every row you touch to today's date.

After the first curation pass:

5. **Hand off to Researcher** for the first quarterly refresh — Researcher verifies pricing accuracy and acquisition status on every Linh-vetted row.
6. **Note in `src/consulting/memory.md` Key Decisions** that v1 of the catalogue is live and date-stamped.

---

## Memory pointer

- Categorisation logic: `src/services/vetted-stack/README.md`
- Service positioning: `src/services/SERVICES.md`
- Pain tag schema: `src/services/digital-health-check/questionnaire-v1.md` Section C2
- Quarterly refresh artifacts: `src/services/vetted-stack/refreshes/{YYYY-Q}-refresh.md`

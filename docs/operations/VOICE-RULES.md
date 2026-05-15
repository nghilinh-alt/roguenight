# Voice Rules — Phase 1 Locked

These are the brand voice rules locked at Phase 1. They apply to every customer-facing surface (landing page, privacy policy, terms, thank-you page, confirmation page, Stripe-hosted pages, strategy reports, emails Lois drafts).

They are also enforced in the build scripts and the agent system prompts (Lois, AI Automation Strategy Writer, Stack.md Maintainer). Violating them generally requires a Phase 2 decision — don't break them on a whim.

---

## Never violate

### Audience term

- **Never write "SME" or "SMEs".** Always "small to medium businesses" (lowercase) or "small business".
- Acceptable variants: "Australian small to medium businesses", "small to medium businesses like yours", "the small business".

### Product description

- **Never write "AI-generated report".** Always "specially curated".
- Acceptable variants: "specially curated for your business", "your specially curated AI & Automation Strategy".

### Identity

- **Never name the founder on the customer-facing page.** Rogue Night is the entity.
- Acceptable in legal documents (e.g. privacy policy) where attribution is required.

### Location

- **Never write "Brisbane" as Rogue Night's location.** Use "Australian" generally, or specific state for legal purposes only.
- Acceptable: "Australian small to medium businesses", "Rogue Night PTY LTD · Australia".

### Calls-to-action

- **Never include "Book a free 45-minute walkthrough call"** in customer-facing copy (section 09 of reports, email body, etc.). Walkthroughs happen organically.
- Acceptable: "Reply to this email" or simply leaving the next move to the customer.

### Recommendations framing

- **Always lead with cheapest credible tier** when discussing recommended tools (Xero Cashbook before Xero Grow, HubSpot Free before Starter, etc.).
- If a more expensive tier is required, name the trigger that justifies it ("upgrade to Pro when your team passes 10 users").

### Delivery promise

- **Delivery promise is "within 48 hours"** (NOT 24 hours, NOT 2 business days).
- Internal target stays 24-36h, but the public promise is 48.

### Currency

- **All customer-facing prices are in AUD.** No "A" prefix needed on display (just `$395`, not `A$395`). Single-currency Australian audience.
- **When a vendor quotes natively in non-AUD (USD/GBP/EUR/CAD/NZD), convert before showing in the report.** Use `agents/dhc-report-writer/scripts/convert_currency.py` to get the AUD value with an attribution string.
- **Always show the conversion inline.** Example: `$68 AUD (originally $49 USD, May 2026 rate)`. Customers should never wonder where a number came from.
- Rates refresh weekly via GitHub Action. Lois uses cached rates from `agents/dhc-report-writer/data/rates.json` — never hits a live API at report-draft time.

### Scope clarity

- **AI & Automation Strategy is advisory only.** The report is the deliverable. Agent / digital-employee implementation is a **separate, quoted engagement**.
- Never imply implementation is included in the $395.

### Honesty rule

- **Tell the truth about readiness.** When recommending future digital employees, don't claim integrations are "already wired" or "data is already flowing" if they aren't. The right framing is "designed to deploy on the Week 12 stack" — discovery, build, and supervised deployment still happen.
- Better to under-promise and over-deliver than the reverse.

---

## Cover title pattern

Italic gold accent on the punch word of every page hero. Don't break this pattern when adding new pages.

Examples:
- "Run smarter. *Day and night.*" (landing page)
- "Your questionnaire is in. *Now, the work begins.*" (thank-you page)
- "Payment received. *We start tonight.*" (confirmation page)

The accent word is the emotional punch. The first half sets context, the accent delivers it.

---

## Tone

- **Plain. Specific. Calm.**
- Don't apologise unnecessarily.
- Don't pad with corporate filler.
- Show the work — when you make a claim, name the phrase from the customer's own questionnaire that backs it up.
- Use ranges over point estimates when discussing impact (hours saved, dollars captured).
- Quote the customer's words back to them in strategy reports. Their phrasing is the strongest evidence.

---

## Cost-sensitivity signal

If a customer wrote "I have no money", "tight budget", "can't afford", or similar in their `Anything else notes` or `Pain narrative`:

- Acknowledge it explicitly in the report's Executive Summary: *"And you said it plainly at the end of the questionnaire: 'I have no money'."*
- Every tool recommendation must lead with the cheapest credible tier.
- Spell out upgrade triggers so they only spend when the business has earned it.

---

## Forbidden vocabulary in customer copy

- "AI analyst" — Lois drafts reports, Linh signs off. There is no "AI analyst" in the offer.
- "Synergy", "leverage", "ecosystem" (when used as filler) — concrete words always win.
- "Cutting-edge", "best-in-class", "revolutionary" — these are sales-deck words. Show the result, don't claim the superlative.
- "We help you" pattern when "we" is doing the heavy lifting — pivot to "you'll" or "your" instead.

---

## Allowed in internal docs (this repo, Hyperagent skills)

Voice rules are loosest in internal context. It's fine for:

- `stack.md` to use "SMEs" historically (though we're cleaning these up — see `STACK-AUDIT-2026-05-13.md`)
- Skill scripts to use technical vocabulary
- Code comments to be terse

But anything Lois reads from internal docs primes her output. If you don't want her to say "SME" to a customer, don't write "SME" in the docs she reads.

---

## When the rules might bend

- **Legal documents** (privacy policy, terms) — full company name, ABN, registered state are all required and override casual brand voice.
- **Stripe-hosted pages** — Stripe limits font and branding control. Use what they allow; don't worry about Instrument Serif on the Hosted Invoice Page.
- **Plain-text email** (Hostinger webmail send) — formatting is limited. The voice rules still apply, but you can drop CSS-driven niceties like italic gold accents.

---

## How to propose a change

These rules are Phase 1 lock — they reflect Linh's positioning decisions made deliberately. To change one:

1. Open an issue or a doc in this repo proposing the change with reasoning.
2. Show the before/after copy on the surface(s) it affects.
3. Get explicit confirmation before merging.

The cost of changing a voice rule is the cost of updating every place it's used — landing page copy, report template, Lois's system prompt, Stack.md Maintainer's auto-clean, etc. Don't do it lightly.

# Rogue Night AI Automation Strategy Writer

The methodology Lois follows to turn one Airtable Response row into a populated, voice-compliant AI & Automation Strategy report — HTML and PDF — that she drafts and Linh approves before sending.

## What this skill encodes

- The Phase 1 brand voice rules (locked, non-negotiable)
- The Airtable schema for the live Rogue Night AI & Automation Strategy base (`appCLdTCbJ5zGe9fo`)
- The multi-pain matching algorithm against the Tools catalogue
- The v5 template's CSS and section structure (lifted verbatim into `v5-style-block.txt` for fidelity)
- The cost-sensitivity narrative pattern (when "I have no money" or similar signal appears)
- The quantified-benefits estimation methodology with AU 2026 hourly rate ranges
- The phased rollout heuristics by industry and tech appetite
- The future digital employees framing: three batches scored on impact and readiness, with per-agent pain-match badges, readiness chips, and ties-to-questionnaire quotes
- The hybrid workflow: agent drafts → Linh reviews → agent finalises → manual email send

## Live infrastructure

- **Airtable base:** `appCLdTCbJ5zGe9fo` (Rogue Night — AI & Automation Strategy)
- **Tables:** `Tools` (`tblNDMmrH2zS8JR5K`) · `Responses` (`tblpgzWG5Kslm4AKv`) · `Recommendations` (`tblZyroUIcAZvjouY`) · `Reports` (`tblozeWaPiqdA7FkC`)
- **Tally form:** https://tally.so/r/xX4YaG (source of all Response rows)
- **Email:** hello@roguenight.com.au via Hostinger (NOT Google Workspace — no API integration). Lois drafts the email body as TEXT for Linh to copy-paste into Hostinger webmail and attach the PDF manually.
- **Voice platform (Anna):** not yet provisioned. Future state — Vapi or Retell.

## Inputs

**Production (Airtable):**
- `AIRTABLE_API_KEY` (skill credential, password) — Personal Access Token with `data.records:read` + `data.records:write` + `schema.bases:read` scopes
- `AIRTABLE_BASE_ID` (skill credential, text) — `appCLdTCbJ5zGe9fo`
- A Response record id (e.g. `recbyi0RxmOCD7VVY`)

**Testing (JSON fallback):**
- `mock_response.json` — Pacific Coast Plumbing (trades example) for offline testing.

## Outputs

1. `report.html` — populated v5-quality HTML, ready to view in browser or print
2. `report.pdf` — A4 PDF rendered from the HTML, ready to email
3. **Airtable writes (production only, after Linh's approval):**
   - 5-7 Recommendations rows linked to the Response and the matching Tools
   - 1 Reports row with `Status = Draft`, `Report URL`, `Report PDF` attachment
   - Updates the Response's `Status` to `Has reports`
4. **Email body text (manual copy-paste workflow):**
   - Drafted body returned in the chat
   - Linh copies → opens Hostinger webmail → composes → attaches the PDF → sends

## Voice rules — non-negotiable

These come from Phase 1 brand decisions and apply to every word in the report:

- **Never write `SME` or `SMEs`.** Always "small to medium businesses" (lowercase) or "small business".
- **Never write `AI-generated report`.** Always "specially curated".
- **Never name the founder on the page.**
- **Never write `Brisbane` as Rogue Night's location.** Use "Australian". For the client's own region — fine to be specific.
- **Use "digital employee" over "AI agent"** in body copy. Section 08 is titled "Your future digital employees" intentionally.
- **No "AI analyst".** Linh sells AI agents and digital employees that the customer deploys.
- **Cost-sensitivity signal:** if the client wrote "I have no money", "tight budget", "can't afford", or similar in Anything else notes, EVERY tool recommendation must lead with the cheapest credible tier (Xero Cashbook over Xero Grow, HubSpot Free over Starter, Calendly Free over Standard). Upgrade triggers spelled out so they only spend when the business has earned it.
- **Always tell the truth.** Don't overstate readiness. Don't claim integrations are "already wired" or "data is already flowing" unless they actually are. The right framing for Batch 01 digital employees is "designed to deploy on the Week 12 stack" — discovery, build, and supervised deployment still happen. Be specific about what foundation each agent needs.

## Section-by-section drafting guidance

### Cover

Format: brand bar with horizontal lockup PNG (from `horizontal-b64.txt`) + cover-title + accent + cover-subtitle + cover-meta.

Title pattern: "[Action verb]. <em class='accent'>[Outcome.]</em>" e.g. "Less admin.<br><span class='accent'>More sales.</span>" for a healthcare admin client; "Run smarter.<br><span class='accent'>Day and night.</span>" for trades.

Subtitle: pull from the client's `Stated goal` and `Future state vision` — paraphrase into one sentence about where they want to be in 90 days. If cost-sensitive, mention the budget framing ("Every recommendation leads with the cheapest tier that works — because you said budget matters.").

### 01. Executive summary

Three short paragraphs, then three Key Benefits boxes.

Paragraph 1 (`body-lede`): the client's situation in their own words. Quote from `Stated goal`, `Hated weekly task`, and **Anything else notes** specifically. If "I have no money" or similar appears, name it directly: "And you said it plainly at the end of the questionnaire: 'I have no money'."

Paragraph 2: what the report does about it. Reference the cost-sensitivity if applicable.

Paragraph 3: the future state in the client's own words, then the bridge (e.g. "Six tools, phased over twelve weeks, get you most of the way there.").

Key Benefits boxes:
- **Benefit 01** — time back (hours/month range, dollar value range)
- **Benefit 02** — sales / pipeline / cash captured
- **Benefit 03** — software cost (lead with the headline total, e.g. "$144/month total")

### 02. Quantified benefits

Table: each row is a change (e.g. "Paper-based invoicing → Xero Cashbook"), with hours saved per month and dollar value range per month.

**Use ranges, not point estimates.** AU 2026 hourly rate ranges:
- Owner-operator (general): $60-120/hr
- Owner-operator (salon, hands-on): $40-60/hr
- Admin / front desk: $28-35/hr
- Apprentice / junior trade: $25-40/hr
- Nail technician / similar trade: $25-35/hr
- Tradesperson (qualified): $50-80/hr

Subtotal row with italic styling. Estimate basis note in `.meta` styling below the table.

### 03. Current state snapshot

`.snapshot` grid pulling verbatim from the Response. 10 rows: Industry · Headcount · Years operating · Customers per week · Stated goal (serif italic) · Pain narrative (serif italic) · Hated weekly task (serif italic) · Future state vision (serif italic) · Tech comfort · AI readiness.

For Industry = "Other" or unclear, optionally research from LinkedIn / ABN lookup before drafting — surface to Linh at the start.

### 04. Recommended stack

Run `match_recommendations.py` → ranked candidates. Then apply writer judgement:
- Narrow to 5-7 final tools
- Order by phase (Day 1 → Day 30+) then within-phase by priority
- Group into sub-categories (4.1, 4.2, 4.3, etc.) by business function

For each tool card (`render_tool_card` in `populate_template.py`), provide:
- `name`, `subtitle` (one-line role description)
- `priority`: High / Medium / Low
- `phase`: "Day 1" through "Day 90"
- `why`: 1-3 sentences tying the recommendation to a specific phrase from the questionnaire (the `Pain narrative`, `Stated goal`, `Hated weekly task`, etc.)
- `alt_skipped`: when there's a credible runner-up, name it and give one sentence on why we passed
- `watch`: pull from Tools `Watch out for`, personalise per client when warranted
- `integrations`: list which other recommended tools this connects to natively vs via a glue layer
- `tiers`: pricing tiers with `recommended: true` on the one we suggest starting at
- `upgrade_trigger`: when to upgrade

End the section with **"What we left out — and why"** (`cull` array) — 5-10 categories the client doesn't need today, one line each on why. Be specific to this client.

### 05. Stack at a glance

`stack_glance_body` — assemble manually for now. Two parts:

**Priority groups** — High / Medium / Low buckets with the recommended tools as tool names + role + day tag.

**How the tools connect** — 5 named data flows showing movement between tools. Each flow: a heading + a one-line description. Use specific action verbs ("Customer books a call · Calendly → Google Calendar → confirmation email").

### 06. Phased rollout

The header says "Twelve weeks, in phases" — the phases array MUST span Week 1 through Week 12. Not every week needs to be present, but the milestones should reach Week 12. Typical shape:

- **Week 1 — Foundations:** accounting base, email + Workspace, primary-pain-tool base configuration
- **Week 2 — Customer-facing:** scheduling, pipeline stages, email signatures, the primary operational tool live
- **Week 4 — Refinement:** secondary tools live (payments, receivables), branded comms templates, automated cadences
- **Week 6 — Stability check:** legacy systems retired, books reconciled, 60-day metric review, first cycle of new tool measured
- **Week 12 — 90-day review and plan:** harvest the numbers (hours saved, dollars captured), scope first Batch 01 digital employee, book the discovery session

Adjust by Tech appetite:
- **Simple appetite:** fewer tools, longer phases, one tool mastered before adding the next
- **Medium appetite:** standard rollout — Week 1 / 2 / 4 / 6 / 12 as above
- **Hard appetite:** compress phases; can add Zapier glue earlier; can recommend more capable tools

Each phase: headline outcome + 3-5 plain-language tasks. NO who-owns-what tags — just tasks.

Tasks in plain English with explicit provider names ("Sign up for HubSpot CRM Free at hubspot.com"), no jargon.

### 07. Cost and investment

Two tables:
1. **Recurring software** — recommended tools at recommended tiers, monthly subtotal
2. **Where the stack grows once you're ready** — upgrade-trigger table showing what comes next and the cost delta

Plus the **Implementation · optional** dark callout box (always include):
- "Rogue Night can implement this for you."
- Lists what RN does (data migration, account setup, configuration, integrations, process design, scoping)
- "What we don't do" sub-block: hands-on training (we provide written guides + pointers to official video training)
- "Implementation quote provided on request — book a walkthrough to scope."

### 08. Your future digital employees

Renders THREE batches (Day 90 / Day 180 / Day 270) using the `batches` array in vars.json. Each batch has a header (`number`, `day`, `title`, `description`) followed by three agent cards. The legacy flat `employees` array still works for backward compatibility — `populate_template.py` auto-wraps it as Batch 01.

**Per-agent fields:**

- `name` — Specialist title (e.g. "Receivables Specialist", "Phone Reception Specialist"). Not "AI assistant" or "Bot".
- `pain_match` — short label naming which pain this agent addresses (e.g. "Manual data entry", "Owner bottleneck", "Lead tracking", "Invoicing", "Comms", "Reputation"). Appears in the gold eyebrow badge above the card title.
- `pain_tier` — "Primary" / "Secondary" / "Emerging opportunity". Appears after the pain_match in the eyebrow.
- `replaces` — one phrase naming the current manual task (e.g. "Calls you miss because you're on a job or after hours").
- `hours` — hours saved per month as a range (e.g. "8-12 hrs/mo"). For agents that save strategic insight rather than direct hours, say so plainly (e.g. "Strategic insight, not direct hours").
- `dollar` — dollar value per month as a range using the AU 2026 hourly rate ranges in section 02.
- `readiness` — short status describing what foundation is required. Be honest. Examples: "Week 12 stack — ready", "Voice platform wired, FAQ knowledge base curated, ServiceM8 booking integration", "6+ months Xero + ServiceM8 history", "Phone Reception Specialist proven, call-type segmentation captured, CRM mature".
- `description` — 1-3 sentences in plain English, specific to this client's tools and language.
- `ties_to` — one short quote pulled from the client's own words in the questionnaire (Hated weekly task, Pain narrative, Stated goal, Future state vision, Anything else notes, Best time to call if it's signal). Don't paraphrase.
- `ties_label` — describe where the quote came from (e.g. "your hated weekly task", "your pain narrative", "your stated goal", "your preferred call time, which tells us your phone is always on").

**Section header copy:**

- `employees_h2` (default: "Three batches, scored on impact and readiness.")
- `employees_lede` — set the framing: "Nine agents, picked from a wider library and ordered into three phases. Batch 01 deploys on the Week 12 stack with no further foundation. Batch 02 needs the stack mature and a few months of history. Batch 03 is emerging upside — high ceiling, more setup."
- `employees_outro` — the standard pattern: "Hours and dollars shown are conservative starting estimates — actual numbers depend on how each agent is used once live. We review every agent at the end of its batch before starting the next; if one isn't earning its keep, we stop and rethink rather than compound the spend."

**Batch framing:**

- **Batch 01 — Day 90 · "High impact, ready now."** Description: "These agents are designed to deploy on the Week 12 stack. They don't need months of accumulated history or new infrastructure beyond what the rollout has put in place. Discovery, build, and supervised deployment still happen — but pay-back is measured in months, not years." DON'T claim integrations are pre-wired. DON'T claim data is already flowing.
- **Batch 02 — Day 180 · "High impact, foundation needed."** Description: "These agents need the Week 12 stack to mature — a few months of customer history, a phone line connected, or a second tool wired in. High-impact when ready, but ship them too early and they don't have enough to work with."
- **Batch 03 — Day 270 · "Emerging upside."** Description: "Higher ceiling, more setup. These agents either need the full stack mature plus six months of data, or they unlock strategic decisions rather than weekly time savings. Worth keeping on the horizon — not worth rushing."

End with the **Implementation · optional** dark callout box for digital employees:
- "Rogue Night can build and deploy these for you."
- Discovery, Build, Deploy supervised, Handoff and monitor
- "What we don't do" sub-block: replace your team
- "Implementation quote provided per batch — book a walkthrough to scope."

### 09. Next steps

Three doors. The v5 template's exact copy is the locked default:

1. **Feel strongly about something? We'll amend the report.** Free of charge. The $880 covers the work, including refinement.
2. **Engage Rogue Night for the implementation.** Fixed-fee, fixed-scope. Quote after a scoping call.
3. **Take the report and run it yourself.** The recommendations are vendor-neutral. The $880 has covered the work.

**Locked instruction (per Linh, 2026-05-11):** do NOT include "Book a free 45-minute walkthrough call" copy in the email body or in section 09. Walkthroughs happen organically; don't prompt for them in the canonical send.

## Recommendation matching algorithm

Full implementation in `match_recommendations.py`. Summary:

1. **Parse the Pain tag (derived) field** — a comma-separated string of canonical pain tags. The first tag is the primary pain.
2. **Filter Tools** where `Pain tags` overlaps with ANY of the response's pains (multi-value matching).
3. **Drop tools already in `Tool stack`** (substring match against the multi-select labels).
4. **Drop wrong-vertical tools** by industry (e.g. ServiceM8 for healthcare admin, Phorest for trades). The script's `WRONG_VERTICAL` table uses the Airtable category names ("Field service & trades" not "Field service").
5. **Drop Hard difficulty tools** when `Tech appetite` starts with `Simple`.
6. **Drop Enterprise-ceiling tools** when headcount is under 50.
7. **Score** — Foundation tools (Office suite, Accounting & finance, Field service & trades, Salon and personal services) get High. Primary-pain match gets High. Glue/automation gets Low. Everything else Medium.
8. **Phase** — per-category default in `DEFAULT_PHASE`.
9. **Sort** by Priority then phase order. Output top 8.

When the algorithm produces a borderline call, re-rank using the Response's full text — the `Pain narrative`, `Stated goal`, `Hated weekly task`, `Anything else notes`. The algorithm is a starting point; Lois finishes the call.

## Phased rollout heuristics

What goes in each phase:
- **Week 1 — Foundations**: accounting base, primary-pain-tool base configuration, CRM import
- **Week 2 — Customer-facing**: scheduling, pipeline stages, email signatures
- **Week 4 — Refinement**: secondary tools live, branded comms templates, automated cadences
- **Week 6 — Stability check**: legacy systems retired, books reconciled, 60-day metric review
- **Week 12 — Review and plan**: 90-day metrics, plan first batch of digital employees

The phases array in vars.json should always reach Week 12 (the section title promises it). 4-5 milestone phases is the standard shape — Week 1 / 2 / 4 / 6 / 12.

Adjust by Tech appetite (see section 06 above).

## Future digital employees — agent menu

Section 08 renders THREE batches (Day 90, Day 180, Day 270), each with 3 agents picked from a wider candidate library and scored on a balanced impact-and-readiness rubric with a pain-match overlay.

### Scoring rubric

Score each candidate agent for THIS client on three dimensions:

**Impact (1-5):**
- 1 = small admin saving, minor cash recovered
- 2 = noticeable saving, one specific workflow improved
- 3 = significant time back OR moderate cash captured (~$500-1,500/mo)
- 4 = major saving + cash combined (~$1,500-4,000/mo)
- 5 = transformational — multiple workflows or substantial revenue captured

**Readiness (1-5):**
- 1 = needs the full recommended stack mature AND organisational maturity (analytics agents, agent swarms)
- 2 = needs full stack mature + a few months of data
- 3 = needs core stack in place (Week 12 onwards)
- 4 = needs one foundation tool live
- 5 = drops in tomorrow with nothing else changed

**Pain match (0-3):**
- 3 = hits the client's primary pain (first tag in `Pain tag (derived)`)
- 2 = hits a secondary pain (one of the other tags)
- 1 = hits a discovered/latent pain not declared but visible in the narrative
- 0 = doesn't touch any pain — usually wrong-fit, drop

Industry boost: industry-specific archetypes get +1 Pain match score when the client's industry matches (e.g. Walk-in Recogniser starts at Pain match 0 for a plumber but becomes Pain match 2 for a salon).

### Batch assignment heuristic

After scoring, group agents into batches:

**Batch 01 — Day 90 · "High impact, ready now."**
Pick 3 agents where Impact ≥ 4 AND Readiness ≥ 3. These deploy on the Week 12 stack without waiting on accumulated history or new infrastructure. Discovery, build, and supervised deployment still happen — but pay-back is measured in months, not years.

**Batch 02 — Day 180 · "High impact, foundation needed."**
Pick 3 agents where (Impact ≥ 4 AND Readiness < 3) OR (Impact = 3 AND Readiness ≥ 3). High-impact agents that need data history (3-6 months), a new piece of infrastructure (voice platform, phone integration, additional integration glue), OR medium-impact agents that drop in easily.

**Batch 03 — Day 270 · "Emerging upside."**
Pick 3 agents where Impact = 3 AND Readiness ≤ 2, OR Impact ≤ 2 AND any readiness, OR specialised/strategic agents that need the full stack mature plus organisational readiness. Includes agent swarms (multiple specialised siblings), strategic analysts, and industry-specific specialists.

### Candidate agent library

**Receivables & invoicing:**
- Receivables Specialist · Impact 4, Readiness 4 · chases unpaid invoices via Chaser-style cadence
- Invoice Drafter · Impact 3, Readiness 3 · creates invoices from job notes or CRM data
- Payment Reminder · Impact 4, Readiness 4 · auto-sends payment links via email/SMS

**Lead & sales:**
- Lead Capture Specialist · Impact 3, Readiness 5 · form-to-CRM routing + enrichment
- Lead Follow-up Specialist · Impact 4, Readiness 2 · multi-touch cold lead nurturing; needs CRM history
- Win-back Specialist · Impact 3, Readiness 2 · lapsed customer revival; needs CRM history
- Quote Builder · Impact 4, Readiness 2-3 · drafts quotes from job specs and templates

**Data & admin:**
- Data-Sync Specialist · Impact 3-5, Readiness 4 · syncs records between two tools via Zapier/Make
- Form-Filler Specialist · Impact 2, Readiness 3 · auto-completes admin forms from CRM data
- Receipt Categoriser · Impact 2, Readiness 4 · parses receipts, posts to Xero
- Compliance Logger · Impact 2, Readiness 3 · captures evidence, files in folder

**Communications & phone:**
- Inbox Triage Specialist · Impact 3, Readiness 4 · sorts/routes email, drafts replies
- Auto-Responder Specialist · Impact 2, Readiness 5 · FAQ replies via email/chat
- Customer Note-Taker · Impact 3, Readiness 2 · transcribes job-site calls; needs phone system integration
- SMS Reminder Specialist · Impact 3, Readiness 4 · booking and appointment reminders
- **Phone Reception Specialist** · Impact 4-5, Readiness 2-3 · takes inbound calls when owner is busy or after hours. Answers standard questions from a curated FAQ. Books emergency callouts straight into the field-service or booking tool. Routes complex calls to the owner with the full call context already typed up. Needs: voice platform (Vapi/Retell), curated FAQ knowledge base, booking integration.
- **Phone Agent Swarm** · Impact 5, Readiness 1 · specialised siblings for different call types (emergency dispatch, scheduling, billing, complaint, quote follow-up). Each one knows its lane and routes to siblings when needed. Only hands a call to a human when context demands it. Needs: single Phone Reception Specialist proven first, call-type segmentation captured, CRM mature enough to support routing.

**Customer experience:**
- Review-Request Specialist · Impact 4, Readiness 4 · post-service review prompts; needs CRM with customer history
- Onboarding Specialist · Impact 2, Readiness 3 · new customer welcome kits
- Loyalty Specialist · Impact 3, Readiness 2 · rewards, repeat outreach; needs CRM history
- Walk-in Recogniser · Impact 3, Readiness 1 · faces/names lookup (salon, hospitality)
- Booking-Reminder Specialist · Impact 3, Readiness 4

**Strategic & analytics:**
- Profitability Analyst · Impact 5, Readiness 1 · per-job/customer P&L; needs 6+ months of data
- Pricing Optimiser · Impact 5, Readiness 1 · analysis-driven pricing recommendations; needs 12 months won/lost quote data
- Marketing Specialist · Impact 3, Readiness 3 · content and ad drafting
- Staff-Schedule Optimiser · Impact 3, Readiness 2 · needs bookings + payroll data
- Apprentice Coach · Impact 2, Readiness 2 · trades-specific training agent

**Industry-specific (boost Pain match score when industry matches):**
- Repeat-Customer Tracker (salon, hospitality) · Impact 4, Readiness 4
- Inventory Alert Specialist (salon, retail) · Impact 3, Readiness 3
- Slow-Day Filler (salon, hospitality) · Impact 4, Readiness 3

### Wrong-vertical filter

Drop any agent that doesn't make sense for the client's industry:
- **Trades:** drop Walk-in Recogniser, Inventory Alert, Slow-Day Filler, Repeat-Customer Tracker
- **Salon:** drop Quote Builder, Apprentice Coach, most Compliance Logger; Phone Reception fits but reframe for salon bookings
- **Healthcare admin:** drop most consumer-experience agents; keep Compliance Logger, Receivables, Inbox Triage, Phone Reception (medical receptionist framing)
- **Professional services:** drop Walk-in Recogniser, Inventory Alert

### AI appetite gating

- **Hostile or "I don't trust AI yet"** → SOFT-PEDAL all three batches. Frame conditionally ("If you're ever ready, here's what's possible..."). Don't push. Drop to 2 agents per batch if 3 feels too aggressive.
- **"Great — please. I'm ready"** → lean in. Compress timelines: Batch 01 at Day 60, Batch 02 at Day 120, Batch 03 at Day 240. Phone Reception can move into Batch 01 if the voice platform is RN-side ready.
- **Default** — standard 90 / 180 / 270 framing.

### Authoring guidance per card

- **Eyebrow honesty:** `pain_match` + `pain_tier` should be a real link to the questionnaire — don't invent. If `Pain tag (derived)` is "manual-entry, comms", then "Manual entry · Primary" and "Comms · Secondary" are legal pairs. "Manual entry · Primary" + "Lead tracking · Primary" is not — only one primary.
- **Readiness honesty:** state exactly what needs to be in place. "Week 12 stack — ready" is fine when no further infrastructure is needed. "Needs voice platform wired" is more honest than "Ready Day 90" if it's actually waiting on Vapi/Retell.
- **Ties_to is the emotional hook:** pull a REAL phrase from the client's own words. Don't paraphrase. The `ties_label` tells the reader where it came from ("your hated weekly task", "your pain narrative", "your future state vision", "your stated goal", "your preferred call time", "the line in your Anything else notes").
- **Description style:** 1-3 sentences. Plain English. Specific to this client's tools (e.g. "watches your ServiceM8 jobs and your Xero accounts" not "watches your CRM and accounting").

## Workflow steps for Lois

1. **Read the Response** — fetch from Airtable by record id via `fetch_response.py`, or load JSON for testing.
2. **Read the Tools catalogue** — fetch from Airtable via `fetch_tools.py`, optionally filtered by Pain tag.
3. **Run `match_recommendations.py`** → 5-8 candidate tools with priority and phase. Pipe Response + Tools as JSON files.
4. **Apply writer judgement** to narrow to 5-7 final recommendations:
   - Primary pain (first tag in `Pain tag (derived)`) gets priority weighting
   - Cost-sensitivity: if "I have no money" appears in Anything else notes, lead with cheapest credible tiers
   - Drop any tool the matcher recommended that doesn't fit the client's specific situation
5. **Draft per-client copy** for each tool's "Why this for you" and "Why not the alternatives". These are the high-judgement bits that justify the $880 fee — don't template them.
6. **Score the digital employees** against the impact / readiness / pain-match rubric. Pick 3 per batch. Draft each card with pain_match, pain_tier, readiness, ties_to, ties_label.
7. **Assemble `vars.json`** (see `report_vars.example.json` for shape). Include narrative copy for sections 01, 02, 04, 05, 06, 08. Section 06 phases array MUST span Week 1 → Week 12.
8. **Run `populate_template.py`** → produces `report.html` using v5 CSS + client content.
9. **Render PDF** via `render_pdf.py` (WeasyPrint primary, Playwright fallback if installed).
10. **Show Linh** the HTML preview (via `PublishWebpage`) + the PDF (via `SaveFile`).
11. **Wait for Linh's review** and any edit instructions.
12. **Regenerate as requested** — update vars.json, re-run populate + render.
13. **On Linh's approval, write back to Airtable** via `write_back.py`:
    - `PublishFilePublicly` the PDF → get a public URL
    - `AIRTABLE_CREATE_RECORDS` for 5-7 Recommendations rows (each linked to the Response and the matching Tool, with the per-client `Why this for you`, `Plan / tier`, `Monthly cost AUD`, `Phase`, `Owner`)
    - `AIRTABLE_CREATE_RECORDS` for 1 Reports row (Version: 1, Status: Draft, Report URL: HTML preview URL, Report PDF: [{url, filename}])
    - `AIRTABLE_UPDATE_MULTIPLE_RECORDS` for the Response — Status: "Has reports"
14. **Draft the email body for Linh's manual send** (Hostinger workflow):
    - Output in the chat
    - Format: "Hi [Contact name], Thanks for completing the AI & Automation Strategy for [Business name]. Your report is attached..."
    - Include the locked next-steps copy WITHOUT the "Book a free 45-minute call" sentence
    - End with "— Rogue Night"
15. **If email integration becomes available later** (Workspace + Gmail OAuth), step 14 becomes a `GMAIL_CREATE_DRAFT` call that drops the body + PDF attachment into the connected hello@ inbox's Drafts folder.

## Failure modes

- **Headcount > 200** → enterprise scale; flag to Linh, the standard report doesn't fit.
- **Industry = Other** AND `Tool stack` doesn't surface a clear vertical → flag to Linh, ask for category override.
- **Pain tag (derived) empty** → check the SWITCH formula in Airtable; flag to Linh, ask which pain to prioritise.
- **WeasyPrint not installed** → run `pip install weasyprint --quiet` (Pillow may also be needed for image embedding). Fall back to Playwright if installed. Last resort: save HTML and document manual print-to-PDF.
- **Sparse or incoherent Response** → don't fabricate. Ask Linh to clarify before drafting. (Examples: test responses with "yes" as the stated goal, single-word pain narrative, or no Tool stack ticked.)
- **`v5-style-block.txt` or `horizontal-b64.txt` missing** → fall back to Lois's inline minimal styling. Notify Linh to refresh the brand assets in the skill workspace.
- **Phases array shorter than Week 12** → the section header says "Twelve weeks, in phases". Extend the array. Default shape is Week 1 / 2 / 4 / 6 / 12.

## References

- Phase 1 brand kit: project document `cmotjteh7056o07adpfp3gtvb`
- Live Airtable base: https://airtable.com/appCLdTCbJ5zGe9fo
- Tally form: https://tally.so/r/xX4YaG
- Stack.md (vetted tool catalogue, v1.1 — mirror of the Tools table in the live base): user provides as an upload when refreshing the catalogue

## Scripts in this skill

- `fetch_response.py` — read a Response row by id from Airtable
- `fetch_tools.py` — read the Tools catalogue from Airtable, optional Pain tag filter
- `match_recommendations.py` — apply the multi-pain matching algorithm, output ranked recommendations
- `populate_template.py` — generate v5-quality HTML from response.json + vars.json. Section 08 now renders three batches via the `batches` array with improved cards (pain-match eyebrow, readiness chip, ties-to quote). Legacy flat `employees` array still works.
- `render_pdf.py` — render HTML → A4 PDF (WeasyPrint primary, Playwright fallback)
- `write_back.py` — write Recommendations + Reports rows to Airtable, update Response Status
- `mock_response.json` — sample Response (Pacific Coast Plumbing trades business) for testing
- `report_vars.example.json` — example vars JSON shape for `populate_template.py`. Now includes full 3-batch employees example with phone agents.
- `v5-style-block.txt` — the v5 template's <style> block, lifted verbatim. Refresh when brand CSS evolves.
- `horizontal-b64.txt` — base64-encoded horizontal lockup PNG for the cover. Refresh if the logo changes.

### WeasyPrint Key Benefits box fix (2026-05-12, v3)

CSS Grid children default to `min-width: auto`, preventing shrinkage below content width. WeasyPrint enforces this strictly, causing text overflow in the 3-column `.benefits` grid.

Final fix in `v5-style-block.txt`:
- Base rule: added `min-width: 0; overflow-wrap: break-word; word-wrap: break-word` to `.benefit`
- Base rule: added `text-align: justify` to `.benefit-body` for clean squared-off text blocks
- Print `@media print` override: `.benefits { grid-template-columns: 1fr }` — boxes stack vertically (full-width, one per row) in the PDF. Font sizes: title 20px, body 13px.
- Web version keeps the 3-column layout (works fine in browsers).

This supersedes the earlier v2 fix (overflow: hidden, which clipped text).

### Section 08 three-batch redesign (2026-05-13)

Section 08 of `populate_template.py` rewritten to render three batches (Day 90, Day 180, Day 270), each with three agent cards. New per-card fields: `pain_match`, `pain_tier`, `readiness`, `ties_to`, `ties_label`. New per-batch fields: `number`, `day`, `title`, `description`, `agents`. Visual: gold-eyebrow pain badge, soft-gold card background with 2px gold left border, italic serif "Ties to: ..." quote at the bottom of each card, gray-eyebrow + serif title for each batch header. Backward compat: legacy flat `employees` array auto-wraps as Batch 01. The agent menu in the docs now carries an explicit scoring rubric (Impact 1-5, Readiness 1-5, Pain match 0-3) and a wider candidate library including Phone Reception Specialist and Phone Agent Swarm. `report_vars.example.json` updated with a complete 3-batch example for Pacific Coast Plumbing. Section 06 phases also updated to span Week 1 → Week 12 (5 milestones).

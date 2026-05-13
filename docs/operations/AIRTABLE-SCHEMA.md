# Airtable Base Schema — Digital Health Check

Schema spec for the Airtable base that holds questionnaire responses, the vetted tool catalogue, and per-client recommendations. Mirror of `catalogue/stack.md` and the live Tally form.

**Base:** `appCLdTCbJ5zGe9fo` ("Rogue Night — Digital Health Check")
**Plan:** Free tier (1,000 records per base, unlimited bases, all relational features included)
**Upgrade trigger:** cross 1,000 responses or need >1GB attachments. At that point Team plan is A$30/seat/month.

---

## Overview

**Purpose:** structured storage for Digital Health Check questionnaire responses + the vetted tool catalogue + the recommendations Rogue Night drafts per client. Acts as the source of truth that feeds the report template.

**Why Airtable over Google Sheets:** the relational model. Each client response links to multiple recommended tools; each tool can appear across many client recommendations. Airtable handles this natively via linked records, lookups, and rollups. Sheets can fake it via VLOOKUP but breaks under iteration.

---

## Base structure (4 tables)

One base, four tables.

1. **`Responses`** — one row per submitted Digital Health Check questionnaire. Schema mirrors the live Tally form at `https://tally.so/r/xX4YaG`.
2. **`Tools`** — the vetted tool catalogue, mirroring `catalogue/stack.md` row-for-row.
3. **`Recommendations`** — the junction table. Each row links one Response to one Tool with per-client rationale. Powers section 04 of the report.
4. **`Reports`** — one row per generated report version. Tracks the deliverable lifecycle.

**Schema version history:**
- **v1.0** (2026-05-09 morning) — Responses · Tools · Recommendations
- **v1.1** (2026-05-09 evening) — adds `Reports` table for deliverable tracking. Extends `Responses` with proposed v1.1 questionnaire fields.
- **v1.2** (2026-05-10) — restructures `Responses` to match the **live Tally form**. Adds 13 new fields (decision-maker, growth direction, file storage, top 3 tools, hated weekly task, AI appetite, future-state vision, tech appetite, contact details). Drops `Region`, `Pain tags multi-select`. Restructures `Industry` and `Headcount` from free-text to single-select. Pain matching changes from multi-tag overlap to single-tag match.
- **v1.3** (2026-05-10) — restores `Years operating` as a single-select dropdown (4 options). Informs migration scope and rollout tone.
- **v1.4** (2026-05-13) — Tools table fully synced after stack.md audit: 46 tools, all Linh-vetted Yes, Ceiling/Pain tags/Difficulty aligned to stack.md, Last reviewed dates refreshed.

---

## Table 1 — Responses

One row per questionnaire submission. Mirrors the live Tally form at `https://tally.so/r/xX4YaG`. Field names match the form question wording where possible.

### Identity & meta

| Field | Type | Notes |
|---|---|---|
| `Client name` | Single line text | Primary field. Populated from the form's Business Name. |
| `Reference` | Formula | `"DHC-" & DATETIME_FORMAT(Created, "YYYY") & "-" & RIGHT("0000" & RECORD_ID(), 4)` |
| `Submitted` | Date with time | Airtable's built-in `Created time` field |
| `Status` | Single select | `New` · `In analysis` · `Has reports` · `Engaged` · `Declined` · `Stale` |
| `Owner` | Collaborator | Linh, for now. Future-proof for a second analyst. |
| `Stripe paid` | Checkbox | A$350 received |

### Section A — The landscape

| Field | Type | Notes |
|---|---|---|
| `Industry` | Single select | 11 options + Other. Exact list in QUESTIONNAIRE.md |
| `Headcount` | Single select | 6 ranges: `Just me / 1` · `2–10` · `11–50` · `51–100` · `101–200` · `200+` |
| `Years operating` | Single select | 4 options: `Less than 1 year` · `1–3 years` · `3–10 years` · `10+ years` |
| `Sole operator flag` | Formula | `IF({Headcount} = "Just me / 1", TRUE(), FALSE())` |
| `Decision maker` | Single select | 4 options |
| `YoY direction` | Single select | 5 options |
| `Stated goal` | Long text | Used verbatim in report's snapshot card |
| `Customers per week` | Number | Drives volume-based benefit calculations |

### Section B — Tools you're using today

| Field | Type | Notes |
|---|---|---|
| `Tool stack` | Multi-select | 14 options |
| `File storage` | Single select | 6 options |
| `Top tool 1` / `Top tool 2` / `Top tool 3` | Single line text | Free-text |

### Section C — What's slowing you down

| Field | Type | Notes |
|---|---|---|
| `Pain narrative` | Long text | "If we could automate one repetitive task tomorrow..." |
| `Biggest frustration` | Multi-select | **Note:** stored as multi-select in Airtable (Tally's API exposes the field as multi-select even though the UI is single-choice). 9 options mapping to the pain-tag vocabulary. |
| `Pain tag (derived)` | Formula | Maps `Biggest frustration` to canonical pain tags. Handles multi-value input. **This is the matching key against `Tools.Pain tags`.** |
| `Frustration other detail` | Long text | Captured in D-Other description instead (not directly mapped by Tally) |

### Section D — Conditional follow-ups

The form fires conditional D-section questions based on which `Biggest frustration` was selected. All 9 D-branches enumerated:

- **D-A Manual data entry:** hours/week + source tool + destination tool (3 fields)
- **D-B Lead tracking:** tracking method (6 options) + time to response (5 options)
- **D-C Quote/invoice:** invoice paid-on-time % (5 options)
- **D-D Customer comms:** emails per day (5 options)
- **D-E Reporting:** report build time (5 options)
- **D-F Document mgmt:** doc location (6 options) + find time (5 options)
- **D-G Hiring:** onboarding time to productive (5 options)
- **D-H Compliance:** compliance area + evidence capture (2 free-text)
- **D-I Something else:** free-text describe

### Section E — Next steps and appetite

| Field | Type | Notes |
|---|---|---|
| `Hated weekly task` | Long text | Emotional driver, separate from operational pain |
| `AI appetite` | Single select | 5-point sentiment scale. **Drives Tier 3 sequencing in the report.** |
| `Future state vision` | Long text | "Imagine it's three months from now..." |
| `Tech appetite` | Single select | `Simple` · `Medium` · `Hard` |

### Section F — Contact details

| Field | Type | Notes |
|---|---|---|
| `Contact name` | Single line text | |
| `Business name` | Single line text | Populates `Client name` primary field |
| `Contact phone` | Phone number | Tally-validated |
| `Contact email` | Email | Tally-validated |
| `Best time to call` | Single select | 5 options |
| `Anything else notes` | Long text | Free-text catch-all |

### Computed / linked

| Field | Type | Notes |
|---|---|---|
| `Recommendations` | Linked records → Recommendations | Junction |
| `Reports` | Linked records → Reports | One Response → many Reports |
| `Recommended tools` | Rollup | `ARRAYJOIN(values, ", ")` over `Recommendations.Tool name` |
| `Total monthly cost` | Rollup | Sum over `Recommendations.Monthly cost AUD` |
| `Latest report status` | Rollup | Most-recent `Reports.Status` |

---

## Table 2 — Tools

Mirror of `catalogue/stack.md`, row-for-row. 46 rows as of 2026-05-13, all `Linh-vetted: Yes`.

| Field | Type | Notes |
|---|---|---|
| `Tool name` | Single line text | Primary field (e.g. `Xero`, `ServiceM8`, `HubSpot CRM (Starter)`) |
| `Category` | Single select | The 13 categories: `Accounting & finance` · `CRM & lead management` · `Project management & operations` · `Field service & trades` · `Salon and personal services` · `Communications & inbox` · `File storage` · `Scheduling & meetings` · `E-signature & documents` · `Marketing & email` · `Workflow automation` · `Office suite` · `Payments` |
| `Difficulty` | Single select | `Simple` · `Medium` · `Hard` |
| `Ceiling` | Single select | `Starter` · `Pro` · `Enterprise` |
| `Pain tags` | Multi-select | Same options as `Pain tag (derived)`. **The matching key.** |
| `Best for` | Long text | Stack.md "Best for" — voice-cleaned (no SME) |
| `Watch out for` | Long text | Stack.md "Watch out for" |
| `Last reviewed` | Date | Stack.md last-reviewed date |
| `Linh-vetted` | Single select | `Yes` · `No` · `Pending` |
| `Indicative cost AUD/month` | Number | Best-guess at typical small-business size |
| `Notes` | Long text | Internal Rogue Night notes |
| `Recommendations` | Linked records → Recommendations | Reverse link |

---

## Table 3 — Recommendations (junction)

One row per (Response × Tool) recommendation. Powers section 04 of the report.

| Field | Type | Notes |
|---|---|---|
| `Recommendation ID` | Formula | `{Response reference} & " / " & {Tool name}` — primary field |
| `Response` | Linked records → Responses | Required |
| `Tool` | Linked records → Tools | Required |
| `Tool name` | Lookup | From Tool |
| `Category` | Lookup | From Tool |
| `Why this for you` | Long text | **Per-client rationale.** Tied to a specific phrase from the questionnaire. |
| `Why not alternative` | Long text | The runner-up tool and why it was passed over. Optional. |
| `Watch out for (per client)` | Long text | Defaults to Tool's "Watch out for", override per client |
| `Plan / tier` | Single line text | The specific plan recommended |
| `Monthly cost AUD` | Number | Per-client cost at recommended tier |
| `Phase` | Single select | `Day 0` · `Day 1` · `Day 7` · `Day 30` · `Day 60` · `Day 90` |
| `Owner` | Single select | `Rogue Night` · `Client` · `Both` |
| `Order in section` | Number | For sub-ordering within a category |

### Recommendation matching logic

The form's `Biggest frustration` field is exposed as multi-value by Tally's API. The `Pain tag (derived)` formula on Responses handles multi-value input via chained `IF(FIND())` and outputs a comma-separated list of all matching canonical pain tags in priority order.

Pseudo-logic:

1. Read `Response.Pain tag (derived)` → e.g. `manual-entry, comms`
2. Filter `Tools` where `Pain tags` array overlaps with ANY of the response's pains
3. Cross-filter against `Response.Tool stack` (don't recommend tools they already use)
4. Cross-filter against `Response.Tech appetite` (drop Hard tools if appetite = Simple)
5. Cross-filter against `Response.Industry` (drop wrong-vertical tools — e.g. ServiceM8 for a salon)
6. Cross-filter against `Response.Headcount` (drop Enterprise-ceiling tools under 50 staff)
7. Rank by impact × ease, prepare top 8 candidates
8. Linh + Lois review and narrow to 5-7 final recommendations
9. Lois writes per-client `Why this for you`

Full implementation in [`agents/dhc-report-writer/scripts/match_recommendations.py`](../../agents/dhc-report-writer/scripts/match_recommendations.py).

---

## Table 4 — Reports

One row per generated report version. Tracks the deliverable lifecycle from draft through to engagement and implementation. One Response can have many Reports.

| Field | Type | Notes |
|---|---|---|
| `Report ID` | Formula | `{Response reference} & "-v" & {Version}` — primary field |
| `Response` | Linked records → Responses | Required |
| `Version` | Number | Sequential per Response (default 1) |
| `Status` | Single select | `Draft` · `Sent` · `Walkthrough booked` · `Walkthrough done` · `Engaged` · `Declined` · `Walked away` · `Stale` |
| `Sent date` | Date with time | When the report was emailed to the client |
| `Report URL` | URL | Link to the published HTML artifact |
| `Report PDF` | Attachment | Print-export PDF |
| `Walkthrough booked date` | Date with time | |
| `Walkthrough done date` | Date | |
| `Walkthrough notes` | Long text | What the client said, what they pushed back on |
| `Engagement decision` | Single select | `Pending` · `Engaged` · `Declined` · `Walked away` |
| `Engagement signed date` | Date | |
| `Implementation fee` | Currency | The fixed fee quoted and accepted (AUD) |
| `Implementation status` | Single select | `Not started` · `Week 1` · `Week 2` · `Week 3-4` · `Week 6` · `Week 12` · `Closed` |
| `Notes` | Long text | |

Why a separate table (vs extra fields on Responses): a Response is the one-time submission. A Report is a deliverable that can be revised. Keeping them separate prevents the Responses table from growing fields every time the report process changes. Reports also holds the lifecycle that runs PAST report delivery — engagement decision, implementation status.

---

## Suggested views

**Responses table:**
- `Pipeline` — grid grouped by `Status`, sorted by `Submitted` descending
- `New unprocessed` — grid filtered to `Status = New`
- `Engaged clients` — grid filtered to `Status = Engaged`
- `By industry` — grid grouped by `Industry`

**Tools table:**
- `By category` — grid grouped by `Category`
- `Stale review` — grid filtered to `Last reviewed` >12 months ago
- `Pending vetting` — grid filtered to `Linh-vetted ≠ Yes`

**Recommendations table:**
- `By client` — grid grouped by `Response`
- `By phase` — grid grouped by `Phase`, sorted by `Order in section`

**Reports table:**
- `Pipeline` — grid grouped by `Status`
- `Awaiting walkthrough` — grid filtered to `Status = Sent`
- `Engaged engagements` — grid filtered to `Engagement decision = Engaged`
- `Active implementations` — grid filtered to `Implementation status NOT IN [Not started, Closed]`
- `Lost` — grid filtered to `Engagement decision IN [Declined, Walked away]`
- `Calendar` — calendar view on `Walkthrough booked date`

---

## How a client flows through the base

1. **Tally → Airtable native integration** posts a new row into `Responses`. Status defaults to `New` via an Airtable automation.
2. Linh (or Lois on her behalf) opens the new row, reviews, sets `Status = In analysis`.
3. Lois runs the DHC Report Writer skill: pulls the Response, matches against Tools, drafts the report.
4. Linh reviews the draft, requests edits, Lois iterates.
5. On approval, Lois writes back:
   - 5-7 Recommendations rows (linked to the Response and matching Tools)
   - 1 Reports row (Version 1, Status: Draft, Report PDF attached)
   - Updates `Responses.Status = Has reports`
6. Lois drafts the email body in chat. Linh sends manually from Hostinger webmail.
7. Linh updates `Reports.Status = Sent`, `Reports.Sent date`.
8. When walkthrough booked: `Reports.Status = Walkthrough booked`, `Reports.Walkthrough booked date`.
9. After walkthrough: `Reports.Walkthrough done date`, `Reports.Walkthrough notes`. If revisions: create v2 on the same Response.
10. Engagement decision recorded in `Reports.Engagement decision`. If engaged, `Engagement signed date` and `Implementation fee`.
11. Implementation tracked weekly via `Reports.Implementation status`.

---

## Setup steps

For first-time base creation, follow the [v1.3 setup steps](https://airtable.com/appCLdTCbJ5zGe9fo) — base is already live, but the structure here can be used to bootstrap a copy or a staging environment.

For an existing base, the [Stack.md Maintainer skill](../../agents/stack-md-maintainer/) handles the Tools table sync. Responses, Recommendations, and Reports tables are stable — only schema changes need manual updates.

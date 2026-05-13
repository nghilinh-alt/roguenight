# Questionnaire Spec

Source-of-truth documentation for the Digital Health Check questionnaire. The live form is on Tally:

**Live form:** https://tally.so/r/xX4YaG

This document captures the questionnaire structure as deployed on Tally and how each question maps to the Airtable Responses table. For the live source-of-truth, always defer to the actual Tally form — this doc is a mirror, updated as the form changes.

For the **full field-by-field Airtable schema** (including formulas, single-select option strings, computed fields), see [`AIRTABLE-SCHEMA.md`](AIRTABLE-SCHEMA.md). That document has the canonical Tally → Airtable mapping table.

---

## Form structure (high level)

```
Cover (no question)
├─ Section A · About your business, and how you decide things (7 questions, all required)
│   ├─ Industry (single-select, 11 options + Other)
│   ├─ Headcount (single-select, 6 ranges)
│   ├─ Years operating (single-select, 4 ranges) — added in v1.3
│   ├─ Decision maker (single-select, 4 options)
│   ├─ YoY direction (single-select, 5 options)
│   ├─ Stated goal (long text)
│   └─ Customers per week (number)
│
├─ Section B · Now — what's actually in your stack today (3 questions)
│   ├─ Tool stack (multi-select, 14 options)
│   ├─ File storage (single-select, 6 options)
│   └─ Top tool 1 / 2 / 3 (3 free-text fields)
│
├─ Section C · What's slowing you down? (2 base + 1-3 conditional)
│   ├─ Pain narrative (long text)
│   ├─ Biggest frustration (single-select, 9 pain options)
│   └─ Conditional D-section based on the frustration choice:
│       ├─ D-A Manual data entry: hours/week + source tool + destination tool
│       ├─ D-B Lead tracking: tracking method + time to response
│       ├─ D-C Quote/invoice: invoice paid-on-time %
│       ├─ D-D Customer comms: emails per day
│       ├─ D-E Reporting: report build time
│       ├─ D-F Document mgmt: doc location + find time
│       ├─ D-G Hiring: onboarding time to productive
│       ├─ D-H Compliance: compliance area + evidence capture
│       └─ D-I Something else: describe
│
└─ Section E · Next steps and appetite (10 questions)
    ├─ Hated weekly task (long text)
    ├─ AI appetite (single-select, 5-point sentiment scale)
    ├─ Future state vision (long text)
    ├─ Tech appetite (single-select, 3 options: Simple / Medium / Hard)
    ├─ Contact name
    ├─ Business name
    ├─ Contact phone
    ├─ Contact email
    ├─ Best time to call (single-select, 5 options)
    └─ Anything else notes (long text)
```

**Total questions:** roughly 22 visible (depending on which D-branch fires), of which 17 base + 1-3 conditional + 6 contact details.

**Estimated time to complete:** 5-7 minutes for a typical respondent.

---

## What the questions are for

### Section A (the landscape)

Establishes who the customer is, who decides on software, and where the business is going. Drives:
- Industry-based filtering in the tool matcher (drops wrong-vertical tools)
- Decision-maker context for the email follow-up tone
- YoY direction informs urgency framing in the Executive Summary
- Headcount drives tier recommendations (Free tier for under 10, Starter under 25, Pro 25-100, Enterprise 100+)
- Years operating informs migration scope and rollout tone

### Section B (current stack)

Captures what the customer already pays for, so we don't recommend tools they already use. Drives:
- Cross-filter: drop tools that overlap with their `Tool stack` selections
- Snapshot card in the report's section 03

### Section C (pain points)

The matching key. `Biggest frustration` is a single-choice pain that maps via a `Pain tag (derived)` formula to the canonical pain-tag vocabulary used by `Tools.Pain tags`. Conditional D-section drills into the chosen pain for quantification.

### Section E (next steps + contact)

Captures emotional drivers (`Hated weekly task`, `Future state vision`), implementation readiness (`Tech appetite`), and AI sentiment (`AI appetite` — gates how much of Section 08 we show). Plus full contact details for the report send.

---

## How the responses flow

1. **Tally submit** triggers two things:
   - **Native Airtable integration:** writes a row to the `Responses` table with all field values mapped per the schema doc
   - **Redirect on completion:** sends the customer to `roguenight.com.au/thank-you?email=...&name=...&business=...&ref=...`
2. **Airtable Status defaults to "New"** (set via Airtable automation: record-created → set Status = New).
3. **Lois (the agent)** sees the new Response, runs the DHC Report Writer skill to draft a report, surfaces it to Linh in chat.
4. **Linh reviews and approves.** Lois writes Recommendations rows + a Reports row, updates Status to "Has reports".
5. **Email is drafted** by Lois in chat; Linh copy-pastes into Hostinger webmail and attaches the PDF manually.

---

## Voice rules in the form copy

The form copy itself follows the locked voice rules. Section voice intros (added in walkthrough v2):

- **Cover:** brief intro to what this is and why it takes 5-7 minutes
- **Before A1:** "Let's start with the basics."
- **Before B1:** "Now, what's actually in your stack today."
- **Before C1:** "What's slowing you down?"
- **Before E1:** "Last few — about you, your appetite, and how we'll get in touch."
- **Thank-you copy:** locked at "your details are in — we'll come back to you within 48 hours."

No "SME", no "AI-generated", no founder name. Same rules as everywhere else.

---

## Known issues (2026-05-11 audit)

Several critical bugs were surfaced when the v2 form was first deployed. Status as of latest:

1. **Conditional D-section visibility wired** ✓ (was broken)
2. **Cover intro says "within 48 hours"** ✓ (was 24 hours)
3. **Sole-operator wording variants not yet wired** ⚠ — when `Headcount = "Just me / 1"`, the form should substitute wording on D-D.1, D-F.2, E2, and suppress D-G entirely. Currently single wording for everyone.
4. **Character minimums not enforced** ⚠ — recommend 200-char min on A6, C1, E3; 300-char min on D-I.
5. **B3 Tool 2 / Tool 3 are optional** ⚠ — walkthrough wired them as required to force prioritisation.
6. **Section voice intros from walkthrough v2 not visible in the live form** ⚠ — Linh to add.

Items 3-6 are P2 polish — not blocking. Will address in the next form revision pass.

---

## Updating this doc

When the Tally form changes:

1. Update this doc with the new questions / options
2. Update `AIRTABLE-SCHEMA.md` if the Airtable mapping changes
3. Run the DHC Report Writer skill on a sample response to verify the matching still works
4. Note the change in the "Known issues" section above if it introduces new drift

The form is the canonical source. This doc is a mirror to make the structure greppable and review-able alongside the rest of the system.

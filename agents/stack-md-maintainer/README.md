# Stack.md Maintainer

Keeps the canonical vetted tool catalogue (`stack.md`, Linh's local file) and the live Airtable Tools table in sync, and proposes patches whenever a new AI & Automation Strategy report surfaces tools or categories not yet in the catalogue.

## What this skill encodes

- The diff logic between stack.md and the Airtable Tools table
- The schema for new tool rows (Category, Difficulty, Ceiling, Pain tags, Best for, Watch out for, Last reviewed, Linh-vetted, Indicative cost AUD/month, **Pricing region**, Notes)
- The Linh-vetted rule: new entries default to `Pending`. Promotion to `Yes` is always a human decision.
- **The AUD pricing rule (non-negotiable):** every price in the catalogue is in Australian dollars. Tools have a `Pricing region` field with four values: `AU regional`, `Global / USD converted`, `Bundled / free`, `Transactional`. The quarterly price-check workflow (Workflow D below) keeps prices fresh.
- The voice rule for any new content written into stack.md or Airtable: never SME or SMEs. Use "small to medium businesses" or "small business".
- The synonym table for known rename pairs (MYOB / MYOB Business, HubSpot Free / Starter / HubSpot CRM (Starter), Google Drive / Google Drive (Workspace bundled), Salesforce Essentials / Salesforce Starter Suite, etc.)
- Four workflow triggers: post-report scan, manual full audit, Tally-response industry check, quarterly price check.

## Inputs

Production:
- `AIRTABLE_API_KEY` (skill credential, password) — Personal Access Token with data.records:read, data.records:write, schema.bases:read scopes
- `AIRTABLE_BASE_ID` (skill credential, text) — `appCLdTCbJ5zGe9fo`
- `stack.md` (uploaded by Linh into the active thread — fetched via `FetchStoredFile` if attached, or asked for if missing)
- The list of tools recommended in the most recent strategy report (passed from Lois, or extracted from the report HTML)

## Outputs

1. **Stack.md patch proposal** — markdown showing new rows and new sections to add, with all fields populated. Linh applies to her local stack.md by paste-edit.
2. **Airtable sync proposal** — dry-run list of records to create or update. Linh confirms before any write hits the live base.
3. **Audit findings** — for full-audit runs, surfaces drift in field values, vetting status, and category alignment between stack.md and Airtable.

## Voice rules — non-negotiable

- Never write SME or SMEs in any field. Always "small to medium businesses" (lowercase) or "small business". Auto-clean is built into both `propose_patch.py` and `sync_to_airtable.py` for `Best for`, `Watch out for`, and `Notes`.
- Always use the current product names from the synonym table (MYOB Business, not MYOB; HubSpot CRM (Starter), not HubSpot Free / Starter).
- The `Linh-vetted` column has four valid values: `Yes`, `No`, `Pending`, `[STARTER — Linh to confirm]`. New entries created by this skill default to `Pending`. Never auto-promote.
- `Last reviewed` is updated to today's date whenever a tool's fields are changed via this skill. The date represents the last time someone looked at the row, not when the tool was last seen in a report.
- **All prices are in AUD.** Every Tools row must have a `Pricing region` set. When adding a new tool: if the vendor publishes USD only, use `Global / USD converted`, convert with the snapshot in `agents/dhc-report-writer/data/rates.json`, and record the conversion in `Notes` (e.g. "$25 USD/user/mo × 1.3826 = A$35"). If the vendor publishes AU pricing, use `AU regional` and pull the price directly from the vendor's AU page.

## Workflows

### A. Post-report scan (most common)

Triggered automatically by Lois after a strategy report is drafted and approved.

1. Lois passes the list of tools recommended in the report (with category and per-client notes).
2. Run `propose_patch.py <stack.md> <recommended_tools.json>` to identify any tool not in stack.md.
3. Lois shows Linh the markdown patch in chat.
4. Linh reviews each proposed row, edits `Best for` and `Watch out for` to her opinion, and confirms.
5. Lois applies the patch:
   - For stack.md: outputs the markdown blocks for Linh to paste into her local file.
   - For Airtable: runs `sync_to_airtable.py --add-rows <confirmed.json>` to create the new tools as `Linh-vetted: Pending` rows.
6. Optional: Linh adds notes about which client surfaced this tool (helps future curation passes).

### B. Manual full audit (quarterly or as-needed)

Triggered by Linh saying "run a stack audit" or similar.

1. Linh uploads the current `stack.md` into the thread.
2. Run `python3 fetch_tools.py > tools-live.json` (script lives in the AI Automation Strategy Writer skill).
3. Run `audit_stack.py <stack.md> <tools-live.json>` to produce a full diff report.
4. Surface findings to Linh in a project document. Include sections for: stack-only tools, Airtable-only tools, field drift, vetting status drift, SME usage in stack.md.
5. Linh confirms a reconciliation plan (which source is canonical per dimension).
6. Apply confirmed changes via `sync_to_airtable.py` (for Airtable updates) and a markdown patch (for stack.md updates).

### C. Tally response industry check (new-business-type detection)

Triggered when a new Tally response lands and its Industry value is unfamiliar to the existing stack.md sections.

1. Lois (or another agent) sees a new industry in the response.
2. Check if the industry maps to an existing stack.md category (e.g. "Construction / trades" -> "Field service & trades"; "Beauty and personal care" -> "Salon & personal services").
3. If no match: propose a new section in stack.md (and a new Category value in Airtable's single-select). Also propose adding the new industry to `match_recommendations.py` `VERTICAL_CATEGORY_FIT` if the new category is vertical-specific — otherwise tools in the new section won't match.
4. Surface to Linh with a recommendation for which existing tools belong in the new section (and which would be better as new tools entirely).
5. Treat the response as a category-expansion opportunity, even if the specific tool recommendations end up being existing ones.

### D. Quarterly price check (every three months)

Triggered by Linh saying "run the quarterly price check" or by a calendar reminder.

1. Confirm `agents/dhc-report-writer/data/rates.json` is fresh — its `fetched_at` should be within the last 14 days. If older, run `python3 agents/dhc-report-writer/scripts/refresh_rates.py` to pull the latest rates from open.er-api.com.
2. Query all Tools rows where `Pricing region = Global / USD converted`. For each one, multiply the vendor's current USD list price by `rates.json["rates_to_aud"]["USD"]` and compare to the stored AUD value. If the drift is more than 10%, propose an update.
3. Query all Tools rows where `Pricing region = AU regional`. Spot-check 5-8 rows against the vendor's current AU pricing page. Flag any with material drift (more than 10% or a tier rename).
4. For every row touched, update `Indicative cost AUD/month`, refresh the `Notes` field with the conversion math (e.g. "Price refreshed YYYY-MM-DD: $X USD × 1.3826 = A$Y"), and set `Last reviewed` to today.
5. Surface the audit summary to Linh as a project document with a "tools updated", "tools verified unchanged", and "tools needing manual review" breakdown. Confirm with Linh before writing to Airtable.

## Schema for new entries

When adding a tool to stack.md or Airtable, every field below should be populated:

| Field | Stack.md column | Airtable field | Notes |
|---|---|---|---|
| Tool name | Tool | Tool name | Use the current product name. Avoid legacy synonyms. |
| Category | Category | Category | Match an existing section/category, or propose a new one. |
| Difficulty | Difficulty | Difficulty | Simple / Medium / Hard — implementation effort |
| Ceiling | Ceiling | Ceiling | Starter / Pro / Enterprise — scales to what team size |
| Pain tags | Pain tags | Pain tags | Multi-select from: manual-entry, lead-tracking, invoicing, comms, email-overload, reporting, documents, onboarding, compliance, system-fragmentation, rostering, training, other |
| Best for | Best for | Best for | One sentence on the ideal customer profile. Voice-clean. |
| Watch out for | Watch out for | Watch out for | One sentence on the gotcha. Voice-clean. |
| Last reviewed | Last reviewed | Last reviewed | YYYY-MM-DD, today's date for new entries |
| Linh-vetted | Linh-vetted | Linh-vetted | New entries default to Pending |
| Indicative cost AUD/month | (not in stack.md) | Indicative cost AUD/month | Add to Airtable. Always AUD; convert USD list prices via rates.json. |
| Pricing region | (not in stack.md) | Pricing region | Single-select: AU regional / Global / USD converted / Bundled / free / Transactional. Required for every row. |
| Notes | (not in stack.md) | Notes | Free-form context. For Global / USD converted rows, record the USD list price and conversion math (e.g. "$25 USD × 1.3826 = A$35"). |

## Scripts in this skill

- `audit_stack.py` — full diff between stack.md and Airtable Tools. Surfaces missing rows, drift in field values, vetting status mismatches, and SME usage in stack.md. Output is markdown for paste into a project doc.
- `propose_patch.py` — given a list of recommended tools from a report, identify which are not in stack.md and emit a markdown patch with new rows. Voice-clean. Linh-vetted: Pending default.
- `sync_to_airtable.py` — apply confirmed changes to the live Airtable Tools table. Three modes: `--vetted-sync` (flip Pending -> Yes from stack.md), `--add-rows` (create new tools), `--reconcile` (per-field updates, not yet implemented).

## Failure modes

- **stack.md not uploaded** — ask Linh to drag-and-drop the current stack.md into the thread before running.
- **Airtable credentials missing** — `AIRTABLE_API_KEY` not set. Tell Linh to configure the skill credentials.
- **Auto-promotion attempt** — if the propose_patch input has any tool with `Linh-vetted: Yes` set, override to `Pending` and warn. Vetting is always a human decision.
- **Unknown industry on Tally response** — surface to Linh with a proposed new category and 2-3 candidate tools; never silently auto-add.
- **Drift on > 20 tools** — flag as needing a focused curation session, not an incremental patch. Linh's time is better spent in a 30-min bulk review than 20 individual approvals.

## References

- Audit findings 2026-05-13: project document (Stack.md Audit — 2026-05-13)
- Live Airtable base: https://airtable.com/appCLdTCbJ5zGe9fo
- Companion skill: Rogue Night AI Automation Strategy Writer (drafts the reports that trigger workflow A)
- Original stack.md categorisation logic: `src/services/vetted-stack/README.md` (in Linh's local repo, referenced by stack.md's memory pointer)

## Working principle (carried from project doc)

After every AI & Automation Strategy report, audit stack.md for two things:

1. **Tools recommended in the report that aren't in the catalogue.** Each one is a candidate for addition, with full schema and Linh-vetted: Pending default.
2. **Categories that the report exposed as missing.** New industries (hospitality, healthcare, retail, fitness) will surface category gaps before they surface tool gaps.

The stack.md catalogue gets stronger every time a report runs. The report writing process is one of the cheapest and most disciplined ways to grow the vetted list. Every new tool that lands in stack.md should be flipped to `Linh-vetted: Yes` only after Linh has used it or formed a strong opinion — otherwise mark `Pending` and slot into the quarterly refresh queue.

**Important: 2026-05-13 script registration note** — when this skill was first drafted, the `UpdateSkillAndScripts` and `CreateSkill` tool's `scripts` parameter hit a validation error and the script files could not be registered in the same call. The working scripts live in `/agent/workspace/skills/Stack.md Maintainer/` in the originating thread. To use them in a fresh thread, either re-upload the scripts manually or retry the script-registration call separately.

# Stack.md Audit — 2026-05-13

Diff between `catalogue/stack.md` v1.1 (48 rows) and the live Airtable Tools table (46 rows). Findings as of 2026-05-13 morning. Resolution applied same day — see "After the audit" section at the bottom.

---

## Summary

- **Stack.md tools (all rows including tier 3 AI):** 48
- **Airtable Tools table** (`appCLdTCbJ5zGe9fo` / `tblNDMmrH2zS8JR5K`): 46
- **Matched by name or synonym:** 42 tools
- **Stack-md-only:** 6 (3 tier 3 AI building blocks intentionally excluded from Airtable; 3 rename misalignments)
- **Airtable-only:** 4 (3 rename targets; 1 genuine addition — Square)
- **Tools with drift in at least one field:** 17

---

## 1. Genuine additions needed in stack.md

These were in the live Airtable base but had no equivalent row in stack.md.

- **Square** — Category: Payments · Linh-vetted in Airtable: Pending
  - Reason added: Australian payment alternative to Stripe, surfaced for in-store / hospitality businesses.
  - Action: add to stack.md under Accounting & finance with Category=Payments. **Done 2026-05-13** — flipped to Linh-vetted: Yes after Linh's review.

---

## 2. Rename misalignments

Same tool with different names on each side. Synonym table now in `stack-md-maintainer/scripts/sync_to_airtable.py`.

| Stack.md name | Airtable name | Action |
|---|---|---|
| `MYOB` | `MYOB Business` | Standardise on `MYOB Business` (current product name) |
| `HubSpot Free / Starter` | `HubSpot CRM (Starter)` | Standardise on Airtable's name |
| `Salesforce Essentials / Starter` | `Salesforce Essentials / Starter` | Identical — matcher artifact only |
| `HelloSign / Dropbox Sign` | `HelloSign/Dropbox Sign` | Whitespace mismatch around slash — both work in practice |
| `Google Drive` | `Google Drive (Workspace bundled)` | Keep stack.md short, treat as same tool |
| `Make (formerly Integromat)` | `Make (Integromat)` | Cosmetic |

---

## 3. Linh-vetted status drift

13 tools (originally counted as "16" via a less-precise matcher) were marked `Yes` in stack.md but `Pending` in Airtable. Biggest data-quality gap of the audit.

**Tools that needed Airtable flip (Pending → Yes):**

- MYOB Business
- QuickBooks Online
- Chaser
- HubSpot CRM (Starter)
- Pipedrive
- Asana
- Notion
- Fresha
- Microsoft 365
- Slack
- Dropbox Business
- Mailchimp
- Zapier

**Resolution:** applied 2026-05-13 via `sync_to_airtable.py --vetted-sync`. Airtable now shows 42 Yes / 4 Pending (was 29 Yes / 17 Pending).

---

## 4. Field drift on shared tools

17 tools had drift in at least one field. Most were stack.md=true / airtable=stale.

### Ceiling drift (Airtable defaulted to Enterprise, stack.md said Pro)

Resolved 2026-05-13 via `sync_to_airtable.py --reconcile --fields ceiling`:

- Stripe — Enterprise → Pro
- Chaser — Pro → Starter
- HubSpot CRM (Starter) — Enterprise → Starter
- Asana — Enterprise → Pro
- Slack — Enterprise → Pro
- Google Drive (Workspace bundled) — Enterprise → Pro
- Dropbox Business — Enterprise → Pro
- Mailchimp — Pro → Starter
- Zapier — Enterprise → Pro

### Difficulty drift (mixed direction)

Resolved 2026-05-13 per-tool with Linh's call:

- Notion — Stack.md: Simple, Airtable: Medium → **kept Simple**
- ServiceM8 — Stack.md: Simple, Airtable: Medium → **kept Simple**
- Microsoft 365 — Stack.md: Medium, Airtable: Simple → **kept Medium**
- Zapier — Stack.md: Simple, Airtable: Medium → **moved to Medium** (debugging complexity is the tell — recommended change applied to stack.md too)

### Pain tags drift

Resolved 2026-05-13 via `sync_to_airtable.py --reconcile --fields pain_tags`:

- Asana — stack adds `lead-tracking`, `reporting`; airtable added `comms` → aligned to stack
- ServiceM8 — stack adds `comms`, `lead-tracking`; airtable added `manual-entry`, `onboarding` → aligned to stack
- Fresha — stack adds `onboarding`, `reporting`; airtable added `invoicing`, `lead-tracking` → aligned to stack
- Google Workspace — stack adds `onboarding`; airtable added `manual-entry` → aligned to stack
- Microsoft 365 — stack adds `compliance`, `onboarding`; airtable added `manual-entry` → aligned to stack
- Google Drive — stack adds `compliance` → aligned
- Zapier — stack adds `invoicing`, `lead-tracking`; airtable added `other` → aligned to stack

### Last reviewed

Stack.md mostly said 2026-05-04 (Linh's curation date), Airtable said 2026-05-11 (seeding date). Airtable date was misleading.

**Resolution 2026-05-13:** wrote 2026-05-13 to Airtable for all 18 touched tools (the date represents when the row was last reviewed, not just when it was seeded). Stack.md kept its 2026-05-04 dates except for the 5 rows that received patches in this audit (Square, Zapier, Phorest, Timely, Mindbody all moved to 2026-05-13).

---

## 5. SME / SMEs usage in stack.md

36 uses of `SME` or `SMEs` in stack.md (`Best for` and `Watch out for` columns mostly).

**Phase 1 voice rule:** never write `SME` or `SMEs`. Always `small to medium businesses` (lowercase) or `small business`.

This is an internal reference doc (not client-facing), so it's not strictly a Phase 1 voice violation — but anything an agent reads from this doc primes its language.

**Status as of 2026-05-13:** Linh applied the local-file find-and-replace on the Zapier row (`SMEs wanting to glue → small to medium businesses wanting to glue`). Remaining 35 uses across other rows are an optional next pass — auto-clean is wired into `stack-md-maintainer/scripts/sync_to_airtable.py` for any field it writes, so the Airtable side stays clean even if stack.md is slower to update.

---

## 6. Action sequence (executed 2026-05-13)

1. ✓ **Sync Linh-vetted flags** — 13 tools flipped Pending → Yes in Airtable.
2. ✓ **Rename align** — synonym table baked into `sync_to_airtable.py`. Future audits don't re-flag these.
3. ✓ **Add Square to stack.md** — row added, Linh-vetted: Pending → Yes (after review).
4. ✓ **Reconcile Ceiling drift** — 9 tools updated in Airtable (matched stack.md).
5. ✓ **Reconcile Difficulty drift** — 3 to Airtable (Notion, ServiceM8 → Simple; M365 → Medium), 1 to stack.md (Zapier → Medium).
6. ✓ **Reconcile Pain tags drift** — 7 tools updated in Airtable (matched stack.md).
7. ✓ **Last reviewed dates** — 18 tools updated to 2026-05-13 in Airtable.
8. ⏸ **SME find-and-replace** — partial (Zapier row only). Remaining as optional follow-up.

---

## After the audit

Final state of the Airtable Tools table (2026-05-13 end of day):

- **46 tools total**
- **All Linh-vetted: Yes** (was 29 Yes / 17 Pending)
- Ceiling values conservative and aligned to stack.md
- Pain tags aligned to stack.md's curated taxonomy
- Difficulty aligned per Linh's per-tool calls
- 18 tools dated 2026-05-13 (those touched this session); 28 tools retain their original 2026-05-04 / 2026-05-09 / 2026-05-11 dates

Local stack.md (Linh applied 5 patches):

- Added Square row
- Updated Zapier row (Difficulty + voice fix + date)
- Updated Phorest, Timely, Mindbody (Pending → Yes + date refresh)

**Net result:** stack.md and Airtable Tools are now in sync on the canonical fields. The Stack.md Maintainer skill is wired to keep them that way for future reports.

---

## Audit script

The audit script lives at [`../../agents/stack-md-maintainer/scripts/audit_stack.py`](../../agents/stack-md-maintainer/scripts/audit_stack.py). To re-run:

```bash
cd agents/stack-md-maintainer/scripts/
# 1. Pull live Airtable Tools snapshot
python3 ../../dhc-report-writer/scripts/fetch_tools.py > /tmp/tools-live.json
# 2. Run audit
python3 audit_stack.py ../../../catalogue/stack.md /tmp/tools-live.json
```

(In production: Lois runs this after every DHC report, and the Stack.md Maintainer skill surfaces any drift to Linh for review.)

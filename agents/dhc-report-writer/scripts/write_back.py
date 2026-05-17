"""Write report artefacts back to Airtable: Recommendations rows + Reports row.

v2 - 2026-05-16. Three reliability improvements over v1:

1. Auto-lookup Tool record IDs by name. v1 left the Tool link empty unless callers
   passed an explicit Airtable record id, which produced rows with empty Tool / Tool
   Name (from Tool) / Category (from Tool) lookups. v2 queries the Tools table by name
   on the fly so recommendations.json only needs a `tool_name`.

2. Validate Phase before POSTing. v1 would happily submit any string in the Phase
   field; Airtable\'s single-select rejects unknown values with a 422, crashing the
   script mid-loop and leaving Airtable in a partial state. v2 rejects strings that
   contain obvious overflow tokens (parens, "+", "conditional", "skip", etc.) with a
   clear error: conditional framing belongs in Plan / tier, not Phase.

3. Populate Label + Sent date on the Reports row at creation. v1 created the row
   with only Version + Status, requiring a follow-up patch to add the canonical
   "<Business> - AI & Automation Strategy" label and the send date. v2 builds the
   label from the response\'s Business name and accepts a `sent_date` in report_meta.

Usage:
    python3 write_back.py <response_id> <recommendations.json> <report_meta.json>

Where:
    response_id           The Airtable record id for the Response (rec...)
    recommendations.json  Output from match_recommendations.py (after Lois\'s edits).
                          Per-recommendation shape:
                            {
                              "tool_name": "Notion",
                              "tool_id":   null,            # auto-looked-up if missing
                              "phase":     "Day 7",         # must be a canonical option
                              "plan_tier": "Free (solo)",
                              "indicative_cost": 0,
                              "why_this_for_you": "...",
                              "why_not_alternative": "...",
                              "watch_out": "..."
                            }
    report_meta.json      Per-report shape:
                            {
                              "version":         1,
                              "status":          "Sent",          # "Draft" | "Sent" | etc.
                              "sent_date":       "2026-05-16",    # YYYY-MM-DD, optional
                              "label_suffix":    "AI & Automation Strategy",  # optional
                              "report_url":      "...",
                              "report_pdf_url":  "..."            # public URL for Airtable to fetch
                            }

What this does:
    1. Look up Tool record IDs for any recommendation that didn\'t ship one
    2. Validate Phase on every recommendation; abort with a clear error if any fail
    3. Create one Recommendation row per item, linked to the Response (and to its Tool)
    4. Look up the Response\'s Business name to build the canonical Label
    5. Create a Reports row (Label + Sent date + Status + Version + URLs)
    6. Update the Response Status to "Has reports"

Required env vars:
    AIRTABLE_API_KEY
    AIRTABLE_BASE_ID

Notes:
    - Run only after Linh approves the draft. Never auto-run.
    - All field names match the v1.2 schema documented in
      `Rogue Night - Airtable Base Schema (AI & Automation Strategy)`.
    - See LESSONS-2026-05-16.md (sibling directory) for the editorial patterns this
      script encodes - particularly the assumption-handling rule.
"""
import json
import os
import sys
from datetime import date
from urllib.parse import quote

import requests


# --- Phase validation -------------------------------------------------------

# Tokens that signal someone has written conditional / explanatory text into the
# Phase field instead of a canonical single-select value. The Airtable Phase
# field rejects unknown options with 422; we catch it earlier with a clearer
# error message.
_INVALID_PHASE_TOKENS = ("(", ")", "+", "conditional", "deferred", "skip", "see ")


def validate_phase(phase):
    """Return (ok, error_message). ok=True if the value looks like a canonical option."""
    if not phase or not isinstance(phase, str):
        return False, f"Phase is empty or not a string: {phase!r}"
    lower = phase.lower()
    for tok in _INVALID_PHASE_TOKENS:
        if tok in lower:
            return False, (
                f"Phase '{phase}' contains '{tok}' - looks like overflow text. "
                f"Use a canonical 'Day X' or 'Week X' value, and move conditional "
                f"or explanatory framing into the Plan / tier field."
            )
    return True, ""


# --- Airtable helpers -------------------------------------------------------

def airtable_get(api_key, base_id, table, params=None):
    url = f"https://api.airtable.com/v0/{base_id}/{quote(table)}"
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.get(url, headers=headers, params=params or {}, timeout=15)
    if r.status_code >= 400:
        print(f"ERROR {r.status_code} on GET {table}: {r.text[:400]}", file=sys.stderr)
    r.raise_for_status()
    return r.json()


def airtable_get_one(api_key, base_id, table, record_id):
    url = f"https://api.airtable.com/v0/{base_id}/{quote(table)}/{record_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code >= 400:
        print(f"ERROR {r.status_code} on GET {table}/{record_id}: {r.text[:400]}", file=sys.stderr)
    r.raise_for_status()
    return r.json()


def airtable_post(api_key, base_id, table, fields):
    url = f"https://api.airtable.com/v0/{base_id}/{quote(table)}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json={"fields": fields}, timeout=15)
    if r.status_code >= 400:
        print(f"ERROR {r.status_code} on POST {table}: {r.text}", file=sys.stderr)
    r.raise_for_status()
    return r.json()


def airtable_patch(api_key, base_id, table, record_id, fields):
    url = f"https://api.airtable.com/v0/{base_id}/{quote(table)}/{record_id}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    r = requests.patch(url, headers=headers, json={"fields": fields}, timeout=15)
    if r.status_code >= 400:
        print(f"ERROR {r.status_code} on PATCH {table}/{record_id}: {r.text}", file=sys.stderr)
    r.raise_for_status()
    return r.json()


def lookup_tool_id(api_key, base_id, tool_name):
    """Find a Tool record id by name. Tries a few likely primary-field names and
    falls back to a substring scan. Returns None if no match."""
    for field_name in ("Tool name", "Tool", "Name"):
        try:
            data = airtable_get(api_key, base_id, "Tools", {
                "filterByFormula": f"LOWER({{{field_name}}}) = LOWER('{tool_name}')",
                "maxRecords": 5,
            })
            records = data.get("records", [])
            if records:
                return records[0]["id"]
        except requests.HTTPError as e:
            if e.response.status_code == 422:
                # Field doesn\'t exist - try next guess
                continue
            raise
    # Last resort: list all and substring-match against any text field
    try:
        data = airtable_get(api_key, base_id, "Tools", {"maxRecords": 200})
        target = tool_name.lower()
        for rec in data.get("records", []):
            for val in rec.get("fields", {}).values():
                if isinstance(val, str) and val.lower() == target:
                    return rec["id"]
    except requests.HTTPError:
        pass
    return None


# --- Main -------------------------------------------------------------------

def main():
    if len(sys.argv) < 4:
        print("Usage: write_back.py <response_id> <recommendations.json> <report_meta.json>", file=sys.stderr)
        sys.exit(1)

    response_id = sys.argv[1]
    with open(sys.argv[2]) as f:
        recs = json.load(f)
    with open(sys.argv[3]) as f:
        report_meta = json.load(f)

    api_key = os.environ.get("AIRTABLE_API_KEY")
    base_id = os.environ.get("AIRTABLE_BASE_ID")
    if not api_key or not base_id:
        print("Missing AIRTABLE_API_KEY or AIRTABLE_BASE_ID", file=sys.stderr)
        sys.exit(1)

    recommendations = recs.get("recommendations", [])

    # --- Pre-flight: validate every Phase before we POST anything ---------
    bad_phases = []
    for i, r in enumerate(recommendations):
        ok, msg = validate_phase(r.get("phase", ""))
        if not ok:
            bad_phases.append(f"  rec {i+1} ({r.get('tool_name', '?')}): {msg}")
    if bad_phases:
        print("Phase validation failed before any writes. Fix recommendations.json and re-run:", file=sys.stderr)
        for line in bad_phases:
            print(line, file=sys.stderr)
        sys.exit(2)

    # --- Pre-flight: resolve Tool IDs for any recs missing them ------------
    print(f"Resolving Tool record IDs for {len(recommendations)} recommendation(s)...")
    for i, r in enumerate(recommendations):
        if r.get("tool_id"):
            continue
        name = r.get("tool_name")
        if not name:
            print(f"  rec {i+1}: no tool_name and no tool_id - Tool field will be empty")
            continue
        tid = lookup_tool_id(api_key, base_id, name)
        if tid:
            r["tool_id"] = tid
            print(f"  {name}: {tid}")
        else:
            print(f"  {name}: NOT FOUND - Tool field will be empty")

    # --- Create Recommendation rows ----------------------------------------
    created_recs = []
    for i, r in enumerate(recommendations):
        fields = {
            "Response": [response_id],
            "Why this for you": r.get("why_this_for_you", ""),
            "Why not alternative": r.get("why_not_alternative", ""),
            "Watch out for (per client)": r.get("watch_out", ""),
            "Plan / tier": r.get("plan_tier", ""),
            "Monthly cost AUD": r.get("indicative_cost", 0),
            "Phase": r.get("phase", "Day 30"),
            "Order in section": i + 1,
        }
        if r.get("tool_id"):
            fields["Tool"] = [r["tool_id"]]

        tool_label = r.get("tool_name", f"rec {i+1}")
        print(f"Creating recommendation {i+1}: {tool_label}...")
        created = airtable_post(api_key, base_id, "Recommendations", fields)
        created_recs.append(created["id"])
        print(f"  Created: {created['id']}")

    # --- Build the Reports row --------------------------------------------
    # Pull the Response\'s Business name so we can build the canonical Label
    # "<Business> - <suffix>" without callers needing to pass it.
    try:
        response_record = airtable_get_one(api_key, base_id, "Responses", response_id)
        business_name = response_record.get("fields", {}).get("Business name") \
            or response_record.get("fields", {}).get("Client name") \
            or "Client"
    except Exception:
        business_name = "Client"
    label_suffix = report_meta.get("label_suffix", "AI & Automation Strategy")
    sent_date = report_meta.get("sent_date") or date.today().isoformat()

    report_fields = {
        "Response": [response_id],
        "Version": report_meta.get("version", 1),
        "Status": report_meta.get("status", "Draft"),
        "Label": f"{business_name} \u2014 {label_suffix}",
        "Sent date": sent_date,
        "Report URL": report_meta.get("report_url", ""),
    }
    if report_meta.get("report_pdf_url"):
        # Airtable attachment field expects [{ url: ... }]
        report_fields["Report PDF"] = [{"url": report_meta["report_pdf_url"]}]

    print(f"Creating Reports row for {business_name}...")
    report_record = airtable_post(api_key, base_id, "Reports", report_fields)
    print(f"  Created: {report_record['id']}")

    # --- Flip Response Status ---------------------------------------------
    airtable_patch(api_key, base_id, "Responses", response_id, {"Status": "Has reports"})

    summary = {
        "response_id": response_id,
        "business_name": business_name,
        "recommendations_created": created_recs,
        "report_id": report_record["id"],
        "response_status": "Has reports",
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

"""Write report artefacts back to Airtable: Recommendations rows + Reports row.

Usage:
    python3 write_back.py <response_id> <recommendations.json> <report_meta.json>

Where:
    response_id           The Airtable record id for the Response
    recommendations.json  Output from match_recommendations.py (after Lois's edits)
    report_meta.json      A small JSON with the Report fields:
                            {
                              "version": 1,
                              "report_url": "...",
                              "report_pdf_url": "...",  # public URL or attachment-able
                              "status": "Draft"
                            }

What this does:
    1. Creates a Recommendation row per recommendation, linked to the Response
    2. Creates a Reports row (version 1 by default), linked to the Response
    3. Updates the Response's Status to "Has reports"

Required env vars:
    AIRTABLE_API_KEY
    AIRTABLE_BASE_ID

Notes:
    - This script is a v1 sketch. The exact Airtable field names must match the v1.2
      schema documented in `Rogue Night — Airtable Base Schema (Digital Health Check)`.
    - Run this only after Linh approves the draft. Never auto-run.
"""
import json
import os
import sys
from urllib.parse import quote

import requests


def airtable_post(api_key: str, base_id: str, table: str, fields: dict) -> dict:
    url = f"https://api.airtable.com/v0/{base_id}/{quote(table)}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    r = requests.post(url, headers=headers, json={"fields": fields}, timeout=15)
    if r.status_code >= 400:
        print(f"ERROR {r.status_code} on POST {table}: {r.text}", file=sys.stderr)
    r.raise_for_status()
    return r.json()


def airtable_patch(api_key: str, base_id: str, table: str, record_id: str, fields: dict) -> dict:
    url = f"https://api.airtable.com/v0/{base_id}/{quote(table)}/{record_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    r = requests.patch(url, headers=headers, json={"fields": fields}, timeout=15)
    if r.status_code >= 400:
        print(f"ERROR {r.status_code} on PATCH {table}/{record_id}: {r.text}", file=sys.stderr)
    r.raise_for_status()
    return r.json()


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

    # Build a tool-name → Airtable record id lookup from the recommendations JSON.
    # Each recommendation can optionally carry a "tool_id" field (the Airtable record
    # id from the Tools table). If present, we link it; if absent, we skip linking.
    created_recs = []
    for i, r in enumerate(recs.get("recommendations", [])):
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
        # Link the Tool record if the recommendation carries a tool_id
        tool_id = r.get("tool_id")
        if tool_id:
            fields["Tool"] = [tool_id]

        tool_label = r.get("tool_name", f"rec {i+1}")
        print(f"Creating recommendation {i+1}: {tool_label}...")
        created = airtable_post(api_key, base_id, "Recommendations", fields)
        created_recs.append(created["id"])
        print(f"  Created: {created['id']}")

    # Create Reports row
    report_fields = {
        "Response": [response_id],
        "Version": report_meta.get("version", 1),
        "Status": report_meta.get("status", "Draft"),
        "Report URL": report_meta.get("report_url", ""),
    }
    if report_meta.get("report_pdf_url"):
        # Airtable attachment field expects [{ url: ... }]
        report_fields["Report PDF"] = [{"url": report_meta["report_pdf_url"]}]
    report_record = airtable_post(api_key, base_id, "Reports", report_fields)

    # Update Response status
    airtable_patch(api_key, base_id, "Responses", response_id, {"Status": "Has reports"})

    summary = {
        "response_id": response_id,
        "recommendations_created": created_recs,
        "report_id": report_record["id"],
        "response_status": "Has reports",
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

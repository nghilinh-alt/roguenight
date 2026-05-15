"""Derive multi-value pain tags from all questionnaire fields and write to Airtable.

Reads: Biggest frustration (multi-select), Symptom picker (multi-select),
       Hated weekly task, Pain narrative, Stated goal, Future state vision (free text).
Writes: Pain tags (multi) field on the Responses table.

Usage:
    python3 derive_pain_tags.py                   # process all responses
    python3 derive_pain_tags.py recXXXXXXXXXXXX   # process one record
    python3 derive_pain_tags.py --dry-run          # preview without writing

Required environment variables:
    AIRTABLE_API_KEY
    AIRTABLE_BASE_ID
"""
import json
import os
import re
import sys

import requests

# ---------------------------------------------------------------------------
# Mapping tables
# ---------------------------------------------------------------------------

# Biggest frustration multi-select → canonical tags
FRUSTRATION_MAP = {
    "Manual data entry": "manual-entry",
    "re-typing the same info": "manual-entry",
    "Lead tracking": "lead-tracking",
    "leads slip through": "lead-tracking",
    "Quote / invoice": "invoicing",
    "payment chasing": "invoicing",
    "money sitting outstanding": "invoicing",
    "Customer / client communications": "comms",
    "too much email volume": "comms",
    "Reporting & dashboards": "reporting",
    "building reports takes too long": "reporting",
    "Document management": "documents",
    "finding old files": "documents",
    "Hiring & onboarding": "onboarding",
    "getting a new person productive": "onboarding",
    "Compliance & record-keeping": "compliance",
    "keeping evidence for audits": "compliance",
    "Disconnected systems": "system-fragmentation",
    "too many tools": "system-fragmentation",
    "Staff scheduling / rostering": "rostering",
    "building rosters": "rostering",
    "Training & knowledge sharing": "training",
    "can't find answers": "training",
    "Email / inbox overload": "email-overload",
    "important messages get buried": "email-overload",
}

# Symptom picker multi-select → canonical tags
SYMPTOM_MAP = {
    "Staff spend time re-entering the same info across systems": "manual-entry",
    "Important emails get buried or missed": "email-overload",
    "New staff take too long to get up to speed": "onboarding",
    "Reports require pulling data from multiple places": "reporting",
    "Compliance or training follow-ups fall through the cracks": "compliance",
    "Customer follow-ups happen late or not at all": "lead-tracking",
    "Scheduling or rostering is a weekly headache": "rostering",
    "Files are saved in different places by different people": "documents",
    "We use too many disconnected tools": "system-fragmentation",
    "We don't really know which customers are our best ones": "reporting",
}

# Free-text keyword patterns → canonical tags
# Each tuple: (compiled regex, tag)
FREE_TEXT_PATTERNS = [
    (re.compile(r"re-?enter|re-?typ|copy.?paste|double.?entry|manual.?entry", re.I), "manual-entry"),
    (re.compile(r"lead|prospect|follow.?up|pipeline|sales.?funnel", re.I), "lead-tracking"),
    (re.compile(r"invoice|invoic|quot(e|ing)|payment|overdue|accounts?\s*receiv", re.I), "invoicing"),
    (re.compile(r"email|inbox|messag(e|ing)|communicat", re.I), "comms"),
    (re.compile(r"email.?overload|inbox.?overload|buried.?email|important.?email|check.*(email|inbox)", re.I), "email-overload"),
    (re.compile(r"report|dashboard|scorecard|analytics|KPI|metric", re.I), "reporting"),
    (re.compile(r"document|file.?storage|find.*(file|document)|lost.?file|scattered", re.I), "documents"),
    (re.compile(r"onboard|new.?hire|new.?staff|train.?new|getting.*(up to speed|productive)", re.I), "onboarding"),
    (re.compile(r"compliance|audit|regulat|certif|training.?remind|training.?follow", re.I), "compliance"),
    (re.compile(r"disconnect|silo|fragment|too many (tool|system|app)|merged into|don.?t talk", re.I), "system-fragmentation"),
    (re.compile(r"roster|schedul|shift|availab.*(staff|team)|staff.?schedul", re.I), "rostering"),
    (re.compile(r"training|SOP|knowledge.?base|wiki|procedure|how.?to", re.I), "training"),
]


def tags_from_frustration(selections: list) -> list:
    """Extract tags from Biggest frustration multi-select values."""
    tags = []
    for sel in (selections or []):
        for phrase, tag in FRUSTRATION_MAP.items():
            if phrase.lower() in sel.lower():
                if tag not in tags:
                    tags.append(tag)
                break
    return tags


def tags_from_symptoms(selections: list) -> list:
    """Extract tags from Symptom picker multi-select values."""
    tags = []
    for sel in (selections or []):
        tag = SYMPTOM_MAP.get(sel)
        if tag and tag not in tags:
            tags.append(tag)
    return tags


def tags_from_free_text(fields: dict) -> list:
    """Extract tags from free-text fields using keyword patterns."""
    text_fields = [
        fields.get("Hated weekly task", ""),
        fields.get("Pain narrative", ""),
        fields.get("Stated goal", ""),
        fields.get("Future state vision", ""),
        fields.get("Anything else notes", ""),
        fields.get("Frustration other detail", ""),
    ]
    combined = " ".join(t for t in text_fields if t)
    tags = []
    for pattern, tag in FREE_TEXT_PATTERNS:
        if pattern.search(combined) and tag not in tags:
            tags.append(tag)
    return tags


def derive_tags(fields: dict) -> list:
    """Derive all pain tags for a response, in priority order.

    Priority: Biggest frustration tags first (user-declared),
    then Symptom picker (user-declared secondary),
    then free-text derived (inferred).
    Deduplicated, order preserved.
    """
    seen = set()
    ordered = []

    for tag in tags_from_frustration(fields.get("Biggest frustration", [])):
        if tag not in seen:
            seen.add(tag)
            ordered.append(tag)

    for tag in tags_from_symptoms(fields.get("Symptom picker", [])):
        if tag not in seen:
            seen.add(tag)
            ordered.append(tag)

    for tag in tags_from_free_text(fields):
        if tag not in seen:
            seen.add(tag)
            ordered.append(tag)

    return ordered if ordered else ["other"]


def fetch_responses(api_key: str, base_id: str, record_id: str = None) -> list:
    """Fetch one or all Response records."""
    headers = {"Authorization": f"Bearer {api_key}"}
    if record_id:
        url = f"https://api.airtable.com/v0/{base_id}/Responses/{record_id}"
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return [r.json()]
    else:
        url = f"https://api.airtable.com/v0/{base_id}/Responses"
        records = []
        offset = None
        while True:
            params = {"pageSize": 100}
            if offset:
                params["offset"] = offset
            r = requests.get(url, headers=headers, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
            records.extend(data.get("records", []))
            offset = data.get("offset")
            if not offset:
                break
        return records


def write_tags(api_key: str, base_id: str, record_id: str, tags: list):
    """Write Pain tags (multi) to a Response record."""
    url = f"https://api.airtable.com/v0/{base_id}/Responses/{record_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    # Multi-select expects array of plain strings (tag names)
    payload = {
        "fields": {
            "Pain tags (multi)": tags
        }
    }
    r = requests.patch(url, headers=headers, json=payload, timeout=15)
    r.raise_for_status()
    return r.json()


def main():
    api_key = os.environ.get("AIRTABLE_API_KEY")
    base_id = os.environ.get("AIRTABLE_BASE_ID")
    if not api_key or not base_id:
        print("Missing AIRTABLE_API_KEY or AIRTABLE_BASE_ID", file=sys.stderr)
        sys.exit(1)

    dry_run = "--dry-run" in sys.argv
    record_id = None
    for arg in sys.argv[1:]:
        if arg.startswith("rec"):
            record_id = arg

    records = fetch_responses(api_key, base_id, record_id)
    print(f"Processing {len(records)} response(s)...")

    for rec in records:
        rid = rec["id"]
        fields = rec.get("fields", {})
        name = fields.get("Client name") or fields.get("Business name") or rid
        tags = derive_tags(fields)

        print(f"\n{name} ({rid}):")
        print(f"  Biggest frustration: {fields.get('Biggest frustration', [])}")
        print(f"  Symptom picker:      {fields.get('Symptom picker', [])}")
        print(f"  Derived tags:        {tags}")

        if dry_run:
            print("  [dry run — not writing]")
        else:
            write_tags(api_key, base_id, rid, tags)
            print(f"  ✓ Written to Airtable")

    print(f"\nDone. {'(dry run)' if dry_run else ''}")


if __name__ == "__main__":
    main()

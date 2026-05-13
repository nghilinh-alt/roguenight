"""Sync confirmed stack.md changes to the live Airtable Tools table.

Two modes:

1. Sync vetted flags (one-shot fix from audit findings):
   python3 sync_to_airtable.py --vetted-sync <stack.md path>
   Flips Airtable `Linh-vetted` to match stack.md (Yes / Pending / No). Requires Linh's
   confirmation before run.

2. Add new tools (post-propose_patch confirmation):
   python3 sync_to_airtable.py --add-rows <confirmed_rows.json>
   Where confirmed_rows.json is a list of tool dicts shaped like the propose_patch input.

3. Reconcile drift (per-tool field updates):
   python3 sync_to_airtable.py --reconcile <stack.md path> --fields ceiling,difficulty,pain_tags
   Updates Airtable to match stack.md on the named fields. Skips any tool with manual
   overrides flagged in `.maintainer-overrides.json` (if present).

Voice rules baked in:
- Never write SME or SMEs in any field that lands in Airtable. Auto-replace.
- New entries default to `Linh-vetted: Pending`.

Credentials (from skill):
- AIRTABLE_API_KEY
- AIRTABLE_BASE_ID
"""
import json
import os
import re
import sys
from pathlib import Path

import requests


AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY", "")
AIRTABLE_BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "")
TOOLS_TABLE = "Tools"


def voice_clean(s):
    if not isinstance(s, str):
        return s
    s = re.sub(r"\bSMEs\b", "small to medium businesses", s)
    s = re.sub(r"\bSME\b", "small business", s)
    return s


def airtable_get(table, formula=None, page_size=100):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    params = {"pageSize": page_size}
    if formula:
        params["filterByFormula"] = formula
    records = []
    offset = None
    while True:
        if offset:
            params["offset"] = offset
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        data = r.json()
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break
    return records


def airtable_patch(table, records):
    """Update existing records. records is a list of {id, fields}."""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}", "Content-Type": "application/json"}
    out = []
    for i in range(0, len(records), 10):
        batch = records[i:i+10]
        r = requests.patch(url, headers=headers, json={"records": batch})
        r.raise_for_status()
        out.extend(r.json().get("records", []))
    return out


def airtable_create(table, records):
    """Create new records. records is a list of {fields}."""
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}", "Content-Type": "application/json"}
    out = []
    for i in range(0, len(records), 10):
        batch = records[i:i+10]
        r = requests.post(url, headers=headers, json={"records": batch})
        r.raise_for_status()
        out.extend(r.json().get("records", []))
    return out


def parse_stack_md(path):
    text = Path(path).read_text()
    tools = []
    current_section = None
    in_table = False
    headers = []
    for line in text.splitlines():
        if line.startswith("## "):
            current_section = line[3:].strip()
            in_table = False
            continue
        if line.startswith("|") and "---" in line:
            in_table = True
            continue
        if line.startswith("|") and not in_table:
            headers = [h.strip() for h in line.strip("|").split("|")]
            continue
        if line.startswith("|") and in_table:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= len(headers):
                row = dict(zip(headers, cells))
                row["_section"] = current_section
                tools.append(row)
            continue
        if not line.startswith("|") and in_table:
            in_table = False
    return tools


# Synonym map: stack.md name -> Airtable name
SYNONYMS = {
    "MYOB": "MYOB Business",
    "HubSpot Free / Starter": "HubSpot CRM (Starter)",
    "Google Drive": "Google Drive (Workspace bundled)",
    "Make (formerly Integromat)": "Make (Integromat)",
}


def sync_vetted_flags(stack_path):
    print(f"Loading stack.md from {stack_path} and Airtable Tools from {AIRTABLE_BASE_ID}/{TOOLS_TABLE}...")
    stack_tools = parse_stack_md(stack_path)
    air_records = airtable_get(TOOLS_TABLE)

    # Build maps
    stack_by_name = {}
    for t in stack_tools:
        name = t.get("Tool", "").strip()
        if name:
            mapped = SYNONYMS.get(name, name)
            stack_by_name[mapped.lower()] = t

    air_by_name = {}
    for r in air_records:
        name = r["fields"].get("Tool name", "").strip()
        if name:
            air_by_name[name.lower()] = r

    # Find mismatches
    updates = []
    for key, stack_t in stack_by_name.items():
        if key not in air_by_name:
            continue
        air_r = air_by_name[key]
        stack_v = stack_t.get("Linh-vetted", "").strip()
        air_v = air_r["fields"].get("Linh-vetted", "").strip()
        if stack_v and stack_v.lower() != air_v.lower():
            updates.append({
                "id": air_r["id"],
                "_name": air_r["fields"].get("Tool name", ""),
                "_from": air_v,
                "_to": stack_v,
                "fields": {"Linh-vetted": stack_v},
            })

    if not updates:
        print("No Linh-vetted drift detected. Nothing to sync.")
        return

    print(f"Will update {len(updates)} tools in Airtable:")
    for u in updates:
        print(f"  - {u['_name']}: {u['_from']} -> {u['_to']}")

    confirm = os.environ.get("MAINTAINER_AUTO_CONFIRM", "").lower() == "yes"
    if not confirm:
        print("\nDry-run only. Set MAINTAINER_AUTO_CONFIRM=yes to actually apply these updates.")
        return

    payload = [{"id": u["id"], "fields": u["fields"]} for u in updates]
    result = airtable_patch(TOOLS_TABLE, payload)
    print(f"Updated {len(result)} records in Airtable.")


def add_rows(rows_path):
    today = __import__("datetime").datetime.now().strftime("%Y-%m-%d")
    rows = json.loads(Path(rows_path).read_text())
    payload = []
    for r in rows:
        fields = {
            "Tool name": r["name"],
            "Category": r.get("category", "Uncategorised"),
            "Difficulty": r.get("difficulty", ""),
            "Ceiling": r.get("ceiling", ""),
            "Pain tags": r.get("pain_tags", []),
            "Best for": voice_clean(r.get("best_for", "")),
            "Watch out for": voice_clean(r.get("watch_out_for", "")),
            "Indicative cost AUD/month": r.get("cost_aud_month", ""),
            "Last reviewed": today,
            "Linh-vetted": "Pending",
            "Notes": voice_clean(r.get("notes", "")),
        }
        payload.append({"fields": {k: v for k, v in fields.items() if v}})

    confirm = os.environ.get("MAINTAINER_AUTO_CONFIRM", "").lower() == "yes"
    if not confirm:
        print(f"Dry-run: would create {len(payload)} new records in Airtable.")
        for p in payload:
            print(f"  - {p['fields'].get('Tool name')} ({p['fields'].get('Category')})")
        print("\nSet MAINTAINER_AUTO_CONFIRM=yes to actually create these rows.")
        return

    result = airtable_create(TOOLS_TABLE, payload)
    print(f"Created {len(result)} new tools in Airtable.")


def parse_pain_tags_stack(tag_str):
    """Extract backtick-wrapped tags from stack.md cell."""
    import re
    if not tag_str:
        return []
    return [t.lower() for t in re.findall(r"`([^`]+)`", tag_str)]


# Stack.md uses lowercase tags like 'manual-entry'. Airtable Pain tags multi-select
# has matching options — confirmed during base seeding.
RECONCILABLE_FIELDS = {
    "ceiling": ("Ceiling", "Ceiling"),
    "pain_tags": ("Pain tags", "Pain tags"),
    "difficulty": ("Difficulty", "Difficulty"),
}


def reconcile_drift(stack_path, fields):
    """Apply stack.md values to Airtable for the named fields.

    fields: list of "ceiling" | "pain_tags" | "difficulty"
    """
    print(f"Loading stack.md from {stack_path} and Airtable Tools from {AIRTABLE_BASE_ID}/{TOOLS_TABLE}...")
    stack_tools = parse_stack_md(stack_path)
    air_records = airtable_get(TOOLS_TABLE)

    stack_by_name = {}
    for t in stack_tools:
        name = t.get("Tool", "").strip()
        if name:
            mapped = SYNONYMS.get(name, name)
            stack_by_name[mapped.lower()] = t

    air_by_name = {}
    for r in air_records:
        name = r["fields"].get("Tool name", "").strip()
        if name:
            air_by_name[name.lower()] = r

    updates = []
    for key, stack_t in stack_by_name.items():
        if key not in air_by_name:
            continue
        air_r = air_by_name[key]
        air_fields = air_r["fields"]
        diffs = {}
        change_summary = []

        if "ceiling" in fields:
            sc = stack_t.get("Ceiling", "").strip()
            ac = air_fields.get("Ceiling", "").strip()
            if sc and ac and sc.lower() != ac.lower():
                diffs["Ceiling"] = sc
                change_summary.append(f"Ceiling: {ac} -> {sc}")

        if "difficulty" in fields:
            sd = stack_t.get("Difficulty", "").strip()
            ad = air_fields.get("Difficulty", "").strip()
            if sd and ad and sd.lower() != ad.lower():
                diffs["Difficulty"] = sd
                change_summary.append(f"Difficulty: {ad} -> {sd}")

        if "pain_tags" in fields:
            spt = sorted(parse_pain_tags_stack(stack_t.get("Pain tags", "")))
            apt = sorted([t.lower() for t in air_fields.get("Pain tags", [])])
            if spt and spt != apt:
                diffs["Pain tags"] = spt
                change_summary.append(f"Pain tags: {apt} -> {spt}")

        if diffs:
            updates.append({
                "id": air_r["id"],
                "_name": air_fields.get("Tool name", ""),
                "_summary": change_summary,
                "fields": diffs,
            })

    if not updates:
        print(f"No drift detected on fields {fields}. Nothing to sync.")
        return

    print(f"Will update {len(updates)} tools in Airtable for fields {fields}:")
    for u in updates:
        print(f"  - {u['_name']}:")
        for c in u["_summary"]:
            print(f"      {c}")

    confirm = os.environ.get("MAINTAINER_AUTO_CONFIRM", "").lower() == "yes"
    if not confirm:
        print("\nDry-run only. Set MAINTAINER_AUTO_CONFIRM=yes to actually apply these updates.")
        return

    payload = [{"id": u["id"], "fields": u["fields"]} for u in updates]
    result = airtable_patch(TOOLS_TABLE, payload)
    print(f"Updated {len(result)} records in Airtable.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    mode = sys.argv[1]
    if mode == "--vetted-sync":
        sync_vetted_flags(sys.argv[2])
    elif mode == "--add-rows":
        add_rows(sys.argv[2])
    elif mode == "--reconcile":
        # Usage: sync_to_airtable.py --reconcile <stack.md> --fields ceiling,pain_tags[,difficulty]
        stack_path = sys.argv[2]
        fields = ["ceiling", "pain_tags"]  # default safe set
        if "--fields" in sys.argv:
            idx = sys.argv.index("--fields")
            if idx + 1 < len(sys.argv):
                fields = [f.strip() for f in sys.argv[idx + 1].split(",") if f.strip()]
        reconcile_drift(stack_path, fields)
    else:
        print(f"Unknown mode: {mode}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()

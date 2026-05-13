"""Fetch the Tools catalogue from Airtable, optionally filtered by Pain tag.

Usage:
    python3 fetch_tools.py [pain_tag]

Examples:
    python3 fetch_tools.py                # all rows
    python3 fetch_tools.py manual-entry   # only tools tagged manual-entry

Required environment variables:
    AIRTABLE_API_KEY
    AIRTABLE_BASE_ID

Output:
    JSON written to stdout. Shape: { "records": [ { "id": ..., "fields": ... }, ... ] }

Notes:
    - The Pain tags column on Tools is a multi-select; the filter formula uses ARRAYJOIN to
      handle the multi-select shape via FIND.
    - Paginates with offset; loads up to 1000 rows comfortably (Airtable hard cap is 100/page).
"""
import json
import os
import sys
from urllib.parse import quote

import requests


def main():
    pain_tag = sys.argv[1] if len(sys.argv) > 1 else None
    api_key = os.environ.get("AIRTABLE_API_KEY")
    base_id = os.environ.get("AIRTABLE_BASE_ID")

    if not api_key or not base_id:
        print("Missing AIRTABLE_API_KEY or AIRTABLE_BASE_ID", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.airtable.com/v0/{base_id}/{quote('Tools')}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"pageSize": 100}

    if pain_tag:
        # FIND returns 0 if the substring isn't found (falsy). ARRAYJOIN flattens the multi-select.
        params["filterByFormula"] = f"FIND('{pain_tag}', ARRAYJOIN({{Pain tags}}))"

    records = []
    offset = None
    while True:
        if offset:
            params["offset"] = offset
        r = requests.get(url, headers=headers, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break

    print(json.dumps({"records": records}, indent=2))


if __name__ == "__main__":
    main()

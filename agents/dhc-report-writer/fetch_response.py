"""Fetch a single Response row from the Airtable Responses table.

Usage:
    python3 fetch_response.py <record_id>

Required environment variables:
    AIRTABLE_API_KEY  Airtable Personal Access Token (PAT)
    AIRTABLE_BASE_ID  The Rogue Night DHC base id (e.g. appXXXXXXXXXXXXXX)

Output:
    JSON written to stdout. Shape: { "id": ..., "fields": { ... } }

Notes:
    - Pulls the Responses table by name. Make sure the table is named exactly "Responses".
    - Requires the PAT to have data.records:read scope on the base.
"""
import json
import os
import sys
from urllib.parse import quote

import requests


def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_response.py <record_id>", file=sys.stderr)
        sys.exit(1)

    record_id = sys.argv[1]
    api_key = os.environ.get("AIRTABLE_API_KEY")
    base_id = os.environ.get("AIRTABLE_BASE_ID")

    if not api_key or not base_id:
        print("Missing AIRTABLE_API_KEY or AIRTABLE_BASE_ID", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.airtable.com/v0/{base_id}/{quote('Responses')}/{record_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code == 404:
        print(f"Record {record_id} not found in Responses", file=sys.stderr)
        sys.exit(2)
    r.raise_for_status()

    print(json.dumps(r.json(), indent=2))


if __name__ == "__main__":
    main()

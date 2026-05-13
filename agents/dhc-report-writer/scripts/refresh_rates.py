#!/usr/bin/env python3
"""Refresh agents/dhc-report-writer/data/rates.json from open.er-api.com.

Runs weekly via .github/workflows/refresh-rates.yml. Can be run manually
to force a refresh:

    python3 agents/dhc-report-writer/scripts/refresh_rates.py

The API is free, no auth, ECB-derived, updated daily. We pull AUD as base
and invert the rates so the stored format matches what convert_currency.py
expects (1 X = N AUD).

If the API ever goes down or returns malformed data, this script exits
non-zero and the GitHub Action surfaces the failure. The existing
rates.json is left untouched, so reports keep using the previous rates.
"""
import json
import urllib.request
import urllib.error
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).parent
DATA_DIR = SKILL_DIR.parent / "data"
OUT_PATH = DATA_DIR / "rates.json"

CURRENCIES = ["USD", "GBP", "EUR", "CAD", "NZD"]
SOURCE_URL = "https://open.er-api.com/v6/latest/AUD"


def fetch_aud_rates():
    """Fetch AUD-base rates from open.er-api.com.

    Returns the raw API response dict. The response shape:
        {
          "result": "success",
          "base_code": "AUD",
          "time_last_update_utc": "Wed, 13 May 2026 00:02:31 +0000",
          "rates": { "USD": 0.7233, "GBP": 0.5342, ... }
        }
    """
    req = urllib.request.Request(
        SOURCE_URL,
        headers={"User-Agent": "Rogue-Night-FX-Refresh/1.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    print(f"Fetching rates from {SOURCE_URL}...")
    try:
        api_data = fetch_aud_rates()
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        print(f"  Failed to fetch rates: {e}", file=sys.stderr)
        sys.exit(1)

    if api_data.get("result") != "success":
        print(f"  API returned non-success result: {api_data.get('result')}", file=sys.stderr)
        sys.exit(2)

    api_rates = api_data.get("rates", {})
    rates_to_aud = {}
    missing = []
    for c in CURRENCIES:
        if c not in api_rates:
            missing.append(c)
            continue
        # API gives 1 AUD = R units of c. We want 1 c = (1/R) AUD.
        rates_to_aud[c] = round(1.0 / api_rates[c], 4)

    if missing:
        print(f"  Currencies missing from API response: {missing}", file=sys.stderr)
        sys.exit(3)

    out = {
        "source": "open.er-api.com",
        "base_currency": "AUD",
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_note": (
            "Rates are 1 X = N AUD. Conversion: amount * rates_to_aud[from] = aud_amount. "
            "Refreshed weekly by .github/workflows/refresh-rates.yml. "
            "To run manually: python3 agents/dhc-report-writer/scripts/refresh_rates.py"
        ),
        "rates_to_aud": rates_to_aud,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
        f.write("\n")

    print(f"  Wrote {OUT_PATH}")
    for c, r in rates_to_aud.items():
        print(f"    1 {c} = {r} AUD")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Convert a tool/service price from a non-AUD currency to AUD.

Reads cached rates from agents/dhc-report-writer/data/rates.json. The rates
file is refreshed weekly by .github/workflows/refresh-rates.yml — Lois never
needs to call an external API at report-draft time, which keeps drafting
fast and predictable.

Usage:
    python3 convert_currency.py <amount> <from_currency>

Example:
    $ python3 convert_currency.py 49 USD
    $67.74 AUD (from $49 USD at 1.3826 USD->AUD, rate as of 2026-05-13)

Supported source currencies: USD, GBP, EUR, CAD, NZD.
If you need another one, add it to rates.json or run refresh_rates.py
with an expanded currency list.

Path resolution: works in both the repo layout (agents/dhc-report-writer/
data/rates.json) and the Hyperagent skill workspace layout (rates.json
alongside this script). See _resolve() below.
"""
import argparse
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent
DATA_DIR = SKILL_DIR.parent / "data"


def _resolve(filename):
    """Try DATA_DIR (repo layout) first, then SKILL_DIR (skill workspace layout)."""
    for candidate in (DATA_DIR / filename, SKILL_DIR / filename):
        if candidate.exists():
            return candidate
    return None


def load_rates():
    path = _resolve("rates.json")
    if path is None:
        raise FileNotFoundError(
            "rates.json not found in either ./data/ or alongside this script. "
            "Run refresh_rates.py to fetch fresh rates, or check the repo layout."
        )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def convert(amount, from_currency):
    """Return (aud_amount, rate_used, rates_data_dict)."""
    data = load_rates()
    rates = data["rates_to_aud"]
    if from_currency.upper() == "AUD":
        return amount, 1.0, data
    if from_currency.upper() not in rates:
        raise ValueError(
            f"Currency '{from_currency}' not in rates.json. "
            f"Available: {sorted(rates.keys())}. "
            f"Add it manually to rates.json or expand the currency list in refresh_rates.py."
        )
    rate = rates[from_currency.upper()]
    return amount * rate, rate, data


def format_output(amount, from_currency, aud_amount, rate, data):
    """Format a Lois-ready conversion string for paste into report drafts."""
    fetched = data.get("fetched_at", "")[:10]  # YYYY-MM-DD
    fc = from_currency.upper()
    return (
        f"${aud_amount:.2f} AUD "
        f"(from ${amount:g} {fc} at {rate} {fc}->AUD, rate as of {fetched})"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Convert a non-AUD amount to AUD using weekly-cached rates."
    )
    parser.add_argument("amount", type=float, help="Amount in source currency (e.g. 49.99)")
    parser.add_argument(
        "from_currency",
        type=str,
        help="Source currency code (USD, GBP, EUR, CAD, NZD)",
    )
    parser.add_argument(
        "--bare",
        action="store_true",
        help="Output just the AUD numeric value (no formatting), useful for piping",
    )
    args = parser.parse_args()

    aud, rate, data = convert(args.amount, args.from_currency)

    if args.bare:
        print(f"{aud:.2f}")
    else:
        print(format_output(args.amount, args.from_currency, aud, rate, data))


if __name__ == "__main__":
    main()

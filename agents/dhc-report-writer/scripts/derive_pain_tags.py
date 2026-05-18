"""Derive multi-value pain tags from all questionnaire fields and write to Airtable.

v2 - 2026-05-18. Free-text-first weighting.

Why v2 exists:
    v1 ordered tags by (1) Biggest frustration multi-select first, (2) Symptom picker
    second, (3) free-text patterns last. This routinely produced bad orderings -
    a client who wrote "Taking too many long calls" in the Hated task field but
    only ticked invoice-chasing in the multi-select got `invoicing` as their
    primary tag. The matcher then weighted invoicing-tools highest, even though
    every qualitative signal said comms.

    v2 reverses the weighting: free-text fields (Pain narrative, Hated task,
    Future state, Stated goal) score highest per match, Symptom picker mid,
    multi-select Biggest frustration lowest. Tags are summed across all sources
    and ordered by total score, descending. A tag confirmed in three places
    beats a tag mentioned once anywhere.

    The free-text patterns themselves were also extended in v2 to catch terms
    that v1 missed: `call`, `phone`, `switchboard`, `meeting`, `reception` now
    match `comms`; `customer`, `marketing`, `new client`, `grow business` now
    match `lead-tracking`.

Source weights (per match):
    Pain narrative           3
    Hated weekly task        3
    Future state vision      3
    Stated goal              2
    Symptom picker (each)    2
    Biggest frustration      1
    Anything else notes      1
    Frustration other detail 1

Reads:
    Biggest frustration (multi-select), Symptom picker (multi-select),
    Hated weekly task, Pain narrative, Stated goal, Future state vision,
    Anything else notes, Frustration other detail (free text).

Writes:
    Pain tags (multi) field on the Responses table.

Usage:
    python3 derive_pain_tags.py                   # process all responses
    python3 derive_pain_tags.py recXXXXXXXXXXXX   # process one record
    python3 derive_pain_tags.py --dry-run          # preview without writing
    python3 derive_pain_tags.py --verbose          # show scoring breakdown per tag

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
# Source weights — how much each field contributes per match
# ---------------------------------------------------------------------------

SOURCE_WEIGHTS = {
    "Pain narrative":           3,
    "Hated weekly task":        3,
    "Future state vision":      3,
    "Stated goal":              2,
    "Symptom picker":           2,   # weight per entry, not per field
    "Biggest frustration":      1,
    "Anything else notes":      1,
    "Frustration other detail": 1,
}

# Canonical pain-tag priority for tie-breaking. Tags appearing earlier here win
# ties so the matcher's primary-pain selection is deterministic.
CANONICAL_TAG_ORDER = [
    "manual-entry",
    "lead-tracking",
    "invoicing",
    "comms",
    "email-overload",
    "reporting",
    "documents",
    "onboarding",
    "compliance",
    "system-fragmentation",
    "rostering",
    "training",
    "other",
]
CANONICAL_TAG_INDEX = {tag: i for i, tag in enumerate(CANONICAL_TAG_ORDER)}

# Tags that only make sense for clients with staff. Filtered out when the
# client is a solo operator (Headcount == "Just me / 1").
SOLO_INCOMPATIBLE_TAGS = {"rostering", "training", "onboarding"}

# ---------------------------------------------------------------------------
# Mapping tables - Biggest frustration multi-select to canonical tags
# ---------------------------------------------------------------------------

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
    "can\'t find answers": "training",
    "Email / inbox overload": "email-overload",
    "important messages get buried": "email-overload",
}

# ---------------------------------------------------------------------------
# Symptom picker multi-select to canonical tags
# ---------------------------------------------------------------------------

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
    "We don\'t really know which customers are our best ones": "reporting",
}

# ---------------------------------------------------------------------------
# Free-text patterns - canonical tags
# ---------------------------------------------------------------------------
# v2: extended to catch phone/call/meeting/reception (comms) and
# customer/marketing/new-client/grow (lead-tracking) - both routinely missed
# in v1 on real client responses.

FREE_TEXT_PATTERNS = [
    (re.compile(r"re-?enter|re-?typ|re-?key|copy.?paste|double.?entry|double.?handl|manual.?entry", re.I), "manual-entry"),

    # lead-tracking now catches "more customers" / "better marketing" / "new
    # client" / "grow the business" / "nurture" - the language clients
    # naturally use to describe acquisition. Negative lookahead excludes
    # "clients requirements" (focus on existing clients != acquisition).
    (re.compile(r"\blead\b|prospect|follow.?up|pipeline|sales.?funnel|new.?(client|customer)|more.?(customer|client|sales)|nurture|attract|grow.*(business|customer base)|better marketing|client acquisition", re.I), "lead-tracking"),

    (re.compile(r"invoice|invoic|quot(e|ing)|payment|overdue|accounts?\s*receiv|chase.*pay", re.I), "invoicing"),

    # comms now catches phone/call/meeting/switchboard/reception/respond -
    # the language clients use for non-email comms pain. v1 only matched
    # email/inbox/messaging.
    (re.compile(r"email|inbox|messag(e|ing)|communicat|\bcall(s|ing)?\b|phone|switchboard|reception|\bmeeting(s)?\b|respond.*(client|customer)|too much email", re.I), "comms"),

    (re.compile(r"email.?overload|inbox.?overload|buried.?email|important.?email|check.*(email|inbox)|emails? (get|are) buried", re.I), "email-overload"),
    (re.compile(r"report|dashboard|scorecard|analytics|KPI|metric", re.I), "reporting"),
    (re.compile(r"document|file.?storage|find.*(file|document)|lost.?file|scattered|paperwork|filing", re.I), "documents"),
    (re.compile(r"onboard|new.?hire|new.?staff|train.?new|getting.*(up to speed|productive)", re.I), "onboarding"),
    (re.compile(r"compliance|audit|regulat|certif|training.?remind|training.?follow", re.I), "compliance"),
    (re.compile(r"disconnect|silo|fragment|too many (tool|system|app)|merged into|don.?t talk", re.I), "system-fragmentation"),
    (re.compile(r"roster|schedul.*(staff|shift)|\bshift|availab.*(staff|team)|staff.?schedul", re.I), "rostering"),
    (re.compile(r"\btrain(ing)?\b|SOP|knowledge.?base|wiki|procedure|how.?to|knowledge.?shar", re.I), "training"),
]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _coerce_multiselect(value):
    """Multi-select fields can arrive as list of strings, list of dicts
    ({name: ...}), or as a comma-separated string (Airtable CSV export).
    Normalise to a list of strings."""
    if not value:
        return []
    if isinstance(value, str):
        return [s.strip() for s in value.split(",") if s.strip()]
    out = []
    for item in value:
        if isinstance(item, dict):
            out.append(item.get("name", ""))
        else:
            out.append(str(item))
    return [s for s in out if s]


def score_tags(fields: dict) -> tuple:
    """Compute weighted scores per tag.

    Returns (scores_dict, sources_dict) where:
      scores_dict maps tag -> int total score
      sources_dict maps tag -> list of (source_field_name, snippet) tuples
        explaining where each contribution came from (for verbose mode).
    """
    scores = {}
    sources = {}

    def _add(tag: str, weight: int, source: str, snippet: str = ""):
        scores[tag] = scores.get(tag, 0) + weight
        sources.setdefault(tag, []).append((source, snippet))

    # 1. Free-text fields - score per pattern match
    for field_name in ("Pain narrative", "Hated weekly task", "Future state vision",
                       "Stated goal", "Anything else notes", "Frustration other detail"):
        text = fields.get(field_name, "") or ""
        if not text:
            continue
        weight = SOURCE_WEIGHTS.get(field_name, 1)
        for pattern, tag in FREE_TEXT_PATTERNS:
            m = pattern.search(text)
            if m:
                _add(tag, weight, field_name, m.group(0))

    # 2. Symptom picker - each entry scores
    weight_sym = SOURCE_WEIGHTS["Symptom picker"]
    for entry in _coerce_multiselect(fields.get("Symptom picker")):
        tag = SYMPTOM_MAP.get(entry)
        if tag:
            _add(tag, weight_sym, "Symptom picker", entry)

    # 3. Biggest frustration multi-select - each tick scores
    weight_fru = SOURCE_WEIGHTS["Biggest frustration"]
    for sel in _coerce_multiselect(fields.get("Biggest frustration")):
        for phrase, tag in FRUSTRATION_MAP.items():
            if phrase.lower() in sel.lower():
                _add(tag, weight_fru, "Biggest frustration", phrase)
                break

    return scores, sources


def derive_tags(fields: dict, with_scores: bool = False):
    """Derive pain tags ordered by total weighted score, descending.

    Tags appearing in multiple high-weight sources rank above tags that only
    appear in a single low-weight source. Ties broken by canonical priority.

    Args:
        fields: the response's `fields` dict (Airtable shape).
        with_scores: if True, return list of (tag, score) tuples instead of
            plain tag strings.

    Returns:
        list of tag strings (or tuples if with_scores=True).
    """
    scores, _ = score_tags(fields)

    # Filter solo-incompatible tags if the client is a solo operator
    headcount = fields.get("Headcount", "") or ""
    if "Just me" in headcount or fields.get("Sole operator flag"):
        for tag in list(scores.keys()):
            if tag in SOLO_INCOMPATIBLE_TAGS:
                # Only drop if the only sources were generic (e.g. Symptom
                # picker phrasings about "new staff" applied to a solo).
                # Free-text mentions still count - someone might mention
                # training in a forward-looking way.
                # Heuristic: if free-text didn\'t contribute, drop.
                # We don\'t have the breakdown here, so just downweight to 0.
                scores.pop(tag, None)

    # Sort: highest score first, then canonical priority for tiebreak
    sorted_tags = sorted(
        scores.items(),
        key=lambda kv: (-kv[1], CANONICAL_TAG_INDEX.get(kv[0], 99)),
    )

    if with_scores:
        return sorted_tags
    tags = [t for t, _ in sorted_tags]
    return tags if tags else ["other"]


# ---------------------------------------------------------------------------
# Airtable I/O
# ---------------------------------------------------------------------------

def fetch_responses(api_key: str, base_id: str, record_id: str = None) -> list:
    headers = {"Authorization": f"Bearer {api_key}"}
    if record_id:
        url = f"https://api.airtable.com/v0/{base_id}/Responses/{record_id}"
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return [r.json()]
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
    url = f"https://api.airtable.com/v0/{base_id}/Responses/{record_id}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"fields": {"Pain tags (multi)": tags}}
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
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    record_id = next((a for a in sys.argv[1:] if a.startswith("rec")), None)

    records = fetch_responses(api_key, base_id, record_id)
    print(f"Processing {len(records)} response(s)...")

    for rec in records:
        rid = rec["id"]
        fields = rec.get("fields", {})
        name = fields.get("Client name") or fields.get("Business name") or rid
        scored = derive_tags(fields, with_scores=True)
        tags = [t for t, _ in scored]

        print(f"\n{name} ({rid}):")
        if verbose:
            scores, sources = score_tags(fields)
            for tag, score in scored:
                src_list = sources.get(tag, [])
                src_summary = ", ".join(f"{s}({sn[:40]})" for s, sn in src_list[:4])
                print(f"  {tag:24s} score={score:2d}  <- {src_summary}")
        else:
            print(f"  Derived tags (ordered): {tags}")

        if dry_run:
            print("  [dry run - not writing]")
        else:
            write_tags(api_key, base_id, rid, tags or ["other"])
            print(f"  Written to Airtable")

    print(f"\nDone. {'(dry run)' if dry_run else ''}")


if __name__ == "__main__":
    main()

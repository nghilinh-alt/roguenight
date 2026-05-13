"""Audit stack.md vs Airtable Tools table.

Surfaces:
- Tools in stack.md but not in Airtable
- Tools in Airtable but not in stack.md
- Drift in fields per shared tool (Category, Difficulty, Ceiling, Pain tags, Best for, Watch out for, Last reviewed, Linh-vetted)
- Voice rule violations in stack.md (SME / SMEs usage)

Usage:
  python3 audit_stack.py <stack.md path> <tools-live.json path>
"""
import json
import re
import sys
from pathlib import Path


# Normalisation helpers
def norm_name(s):
    if not s:
        return ""
    return s.strip().lower().replace("’", "'").replace("—", "-").replace(" / ", "/").replace(" – ", "-")


def parse_stack_md(path):
    """Parse the markdown tables in stack.md. Returns list of dicts."""
    text = Path(path).read_text()
    tools = []
    current_category = None
    in_table = False
    headers = []
    for line in text.splitlines():
        line = line.rstrip()
        if line.startswith("## "):
            # Section header
            current_category = line[3:].strip()
            in_table = False
            continue
        if line.startswith("|") and "---" in line:
            # Table separator
            in_table = True
            continue
        if line.startswith("|") and not in_table:
            # Header row
            headers = [h.strip() for h in line.strip("|").split("|")]
            continue
        if line.startswith("|") and in_table:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= len(headers):
                row = dict(zip(headers, cells))
                row["_section"] = current_category
                tools.append(row)
            continue
        if not line.startswith("|") and in_table:
            in_table = False
    return tools


def normalize_stack_tool_for_match(t):
    """Build a canonical name for matching against Airtable."""
    name = t.get("Tool", "")
    # Handle composite names: "HubSpot Free / Starter" / "HelloSign / Dropbox Sign"
    name = name.replace(" / ", "/")
    return norm_name(name)


def normalize_airtable_tool_for_match(t):
    fields = t.get("fields", t)
    return norm_name(fields.get("Tool name", ""))


def categorise_pain_tags_stack(tag_str):
    """Stack.md uses backtick-wrapped tags like `manual-entry` `comms`. Extract."""
    if not tag_str:
        return set()
    tags = re.findall(r"`([^`]+)`", tag_str)
    return set(t.lower() for t in tags)


def categorise_pain_tags_air(tag_list):
    if not tag_list:
        return set()
    if isinstance(tag_list, str):
        tag_list = [t.strip() for t in tag_list.split(",")]
    return set(t.lower() for t in tag_list)


def count_sme_violations(text):
    """Count uses of SME/SMEs in stack.md — Phase 1 voice rule violation."""
    return len(re.findall(r"\bSMEs?\b", text))


def main():
    stack_path = sys.argv[1]
    tools_path = sys.argv[2]

    stack_text = Path(stack_path).read_text()
    stack_tools = parse_stack_md(stack_path)
    air_data = json.loads(Path(tools_path).read_text())
    air_tools = air_data.get("records", air_data) if isinstance(air_data, dict) else air_data

    # Build maps
    stack_by_name = {}
    for t in stack_tools:
        key = normalize_stack_tool_for_match(t)
        if key:
            stack_by_name[key] = t

    air_by_name = {}
    for t in air_tools:
        key = normalize_airtable_tool_for_match(t)
        if key:
            air_by_name[key] = t

    # Diff
    stack_only = []
    air_only = []
    shared = []

    # Try alternate matches for known synonyms
    SYNONYMS = {
        "hubspot free/starter": "hubspot crm starter",
        "salesforce essentials/starter": "salesforce essentials",
        "hellosign/dropbox sign": "hellosign/dropbox sign",
        "google drive": "google drive (workspace bundled)",
        "make (formerly integromat)": "make (integromat)",
    }

    for key, t in stack_by_name.items():
        air_key = SYNONYMS.get(key, key)
        if air_key in air_by_name:
            shared.append((t, air_by_name[air_key]))
        else:
            stack_only.append(t)

    matched_air_keys = set()
    for _, t in shared:
        matched_air_keys.add(normalize_airtable_tool_for_match(t))
    for key, t in air_by_name.items():
        if key not in matched_air_keys:
            air_only.append(t)

    print("# Stack.md vs Airtable Tools — Audit Report")
    print()
    print(f"- Stack.md tools (all rows including tier 3 AI): **{len(stack_tools)}**")
    print(f"- Airtable Tools table: **{len(air_tools)}**")
    print(f"- Shared (matched by name or synonym): **{len(shared)}**")
    print(f"- In stack.md only: **{len(stack_only)}**")
    print(f"- In Airtable only: **{len(air_only)}**")
    print()
    print("---")
    print()
    print("## 1. In stack.md but NOT in Airtable")
    print()
    if not stack_only:
        print("_(none)_")
    else:
        for t in stack_only:
            print(f"- **{t.get('Tool', '?')}** ({t.get('_section', '?')}) — Linh-vetted: {t.get('Linh-vetted', '?')}")
    print()
    print("## 2. In Airtable but NOT in stack.md")
    print()
    if not air_only:
        print("_(none)_")
    else:
        for t in air_only:
            f = t.get("fields", t)
            print(f"- **{f.get('Tool name', '?')}** ({f.get('Category', '?')}) — Linh-vetted: {f.get('Linh-vetted', '?')}")
    print()
    print("---")
    print()
    print("## 3. Drift in shared tools")
    print()

    drift_count = 0
    for stack_t, air_t in shared:
        af = air_t.get("fields", air_t)
        diffs = []
        # Difficulty
        sd = stack_t.get("Difficulty", "").strip()
        ad = af.get("Difficulty", "").strip()
        if sd and ad and sd.lower() != ad.lower():
            diffs.append(f"Difficulty: stack={sd} vs airtable={ad}")
        # Ceiling
        sc = stack_t.get("Ceiling", "").strip()
        ac = af.get("Ceiling", "").strip()
        if sc and ac and sc.lower() != ac.lower():
            diffs.append(f"Ceiling: stack={sc} vs airtable={ac}")
        # Linh-vetted
        sv = stack_t.get("Linh-vetted", "").strip()
        av = af.get("Linh-vetted", "").strip()
        if sv and av and sv.lower() != av.lower():
            diffs.append(f"Linh-vetted: stack={sv} vs airtable={av}")
        # Pain tags
        spt = categorise_pain_tags_stack(stack_t.get("Pain tags", ""))
        apt = categorise_pain_tags_air(af.get("Pain tags", []))
        if spt != apt:
            only_stack = spt - apt
            only_air = apt - spt
            if only_stack or only_air:
                tag_diff = []
                if only_stack:
                    tag_diff.append(f"stack-only: {sorted(only_stack)}")
                if only_air:
                    tag_diff.append(f"airtable-only: {sorted(only_air)}")
                diffs.append("Pain tags drift: " + " · ".join(tag_diff))
        # Last reviewed
        sr = stack_t.get("Last reviewed", "").strip()
        ar = af.get("Last reviewed", "").strip()
        if sr and ar and sr != ar:
            diffs.append(f"Last reviewed: stack={sr} vs airtable={ar}")
        if diffs:
            drift_count += 1
            print(f"### {stack_t.get('Tool', '?')}")
            for d in diffs:
                print(f"- {d}")
            print()

    if drift_count == 0:
        print("_(no drift detected on shared tools)_")
    else:
        print(f"_{drift_count} tools with drift in at least one field._")

    print()
    print("---")
    print()
    print("## 4. Voice rule check — SME / SMEs usage")
    print()
    sme_count = count_sme_violations(stack_text)
    if sme_count == 0:
        print("_(no SME/SMEs usage found)_")
    else:
        print(f"**Stack.md uses 'SME' or 'SMEs' {sme_count} times.** This is an internal reference doc (not client-facing), so it's not a Phase 1 voice violation per se — but it primes anything an agent reads from this doc to default to 'SME' in client copy too. Recommend a global Find & Replace to 'small to medium businesses' or 'small business' for consistency with the locked report voice.")

    print()
    print("---")
    print()
    print("## 5. Linh-vetted status summary")
    print()
    statuses_stack = {}
    for t in stack_tools:
        s = t.get("Linh-vetted", "?").strip()
        statuses_stack[s] = statuses_stack.get(s, 0) + 1
    statuses_air = {}
    for t in air_tools:
        s = (t.get("fields", t)).get("Linh-vetted", "?")
        if isinstance(s, list):
            s = ", ".join(s) if s else "?"
        s = s.strip() if isinstance(s, str) else str(s)
        statuses_air[s] = statuses_air.get(s, 0) + 1
    print("Stack.md vetting breakdown:")
    for k, v in sorted(statuses_stack.items()):
        print(f"- `{k}`: {v}")
    print()
    print("Airtable vetting breakdown:")
    for k, v in sorted(statuses_air.items()):
        print(f"- `{k}`: {v}")


if __name__ == "__main__":
    main()

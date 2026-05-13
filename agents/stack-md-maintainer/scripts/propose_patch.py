"""Propose a stack.md patch after a AI & Automation Strategy report has been drafted.

Given:
- The current stack.md (Linh's local file, fetched from chat upload)
- A list of recommended tools from a drafted report (per-tool: name, category, why we recommended it)
- Optionally: the response's Industry value (to flag new category sections)

Output:
- A markdown patch (preview-style diff) for Linh's review
- Each new entry defaults to `Linh-vetted: Pending` per the maintainer rule
- New categories are proposed as a new top-level section in stack.md

Usage:
  python3 propose_patch.py <stack.md path> <recommended_tools.json>

Where recommended_tools.json is a list of:
  [{"name": "Fresha", "category": "Salon and personal services",
    "difficulty": "Simple", "ceiling": "Pro",
    "pain_tags": ["manual-entry", "comms", "reporting"],
    "best_for": "AU salons under 15 staff, walk-in heavy",
    "watch_out_for": "Aggressive upsell on paid marketing",
    "cost_aud_month": "Free subscription + pay-per-transaction"},
   ...]

Run this script:
- After every strategy report draft (post-recommendation, pre-send)
- The output is a markdown patch the maintainer agent shows Linh for confirmation
- Linh applies the patch to her local stack.md manually OR confirms an Airtable sync

Voice rules in generated patches:
- Never write SME or SMEs. Use "small to medium businesses" or "small business".
- Linh-vetted defaults to Pending. Never auto-promote to Yes.
- Last reviewed defaults to today's date.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_stack_md(path):
    """Parse stack.md, return (sections, tools_by_name) where sections is the list of category headers in order."""
    text = Path(path).read_text()
    sections = []
    tools_by_name = {}
    current_section = None
    in_table = False
    headers = []
    for line in text.splitlines():
        if line.startswith("## "):
            current_section = line[3:].strip()
            sections.append(current_section)
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
                name = row.get("Tool", "").strip()
                if name:
                    row["_section"] = current_section
                    tools_by_name[name.lower()] = row
            continue
        if not line.startswith("|") and in_table:
            in_table = False
    return sections, tools_by_name


def safe_pain_tags(tags):
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    return " ".join(f"`{t}`" for t in tags if t)


def voice_check(text):
    """Flag SME/SMEs usage in text. Return tuple of (clean_text, warnings)."""
    warnings = []
    if re.search(r"\bSMEs?\b", text):
        warnings.append(f'SME/SMEs found in "{text[:60]}..." — should be "small to medium businesses" or "small business"')
        text = re.sub(r"\bSMEs\b", "small to medium businesses", text)
        text = re.sub(r"\bSME\b", "small business", text)
    return text, warnings


def render_new_row(tool, today):
    """Render a markdown table row for a new tool entry."""
    best_for, w1 = voice_check(tool.get("best_for", ""))
    watch, w2 = voice_check(tool.get("watch_out_for", ""))
    return (
        f"| {tool['name']} | {tool.get('category', '?')} | "
        f"{tool.get('difficulty', '?')} | {tool.get('ceiling', '?')} | "
        f"{safe_pain_tags(tool.get('pain_tags', []))} | "
        f"{best_for} | {watch} | {today} | Pending |"
    ), w1 + w2


def main():
    if len(sys.argv) < 3:
        print("Usage: propose_patch.py <stack.md path> <recommended_tools.json>", file=sys.stderr)
        sys.exit(1)

    stack_path = sys.argv[1]
    recs_path = sys.argv[2]

    sections, tools_by_name = parse_stack_md(stack_path)
    recommended = json.loads(Path(recs_path).read_text())
    today = datetime.now().strftime("%Y-%m-%d")

    # Identify missing tools (recommended but not in stack.md)
    missing = []
    present = []
    for rec in recommended:
        key = rec["name"].strip().lower()
        if key in tools_by_name:
            present.append(rec)
        else:
            missing.append(rec)

    # Identify new categories
    existing_cats = set(s.lower() for s in sections)
    new_cats = set()
    for m in missing:
        cat = m.get("category", "").strip()
        if cat and cat.lower() not in existing_cats:
            new_cats.add(cat)

    # Render the patch
    print("# Stack.md Patch Proposal")
    print()
    print(f"_Generated {today} — review before applying._")
    print()
    print(f"**Tools in report:** {len(recommended)} · **already in stack.md:** {len(present)} · **proposed additions:** {len(missing)}")
    print()

    if not missing and not new_cats:
        print("## No patch needed")
        print()
        print("All recommended tools are already in stack.md. No new categories required. Stack.md is good.")
        return

    all_warnings = []

    if new_cats:
        print("## Proposed new category sections")
        print()
        for cat in sorted(new_cats):
            print(f"### `## {cat}`")
            print()
            print(f"Add a new section to stack.md (after the most thematically adjacent existing section). Pain tags and tool composition will be filled in below.")
            print()

    if missing:
        print("## Proposed new tool rows")
        print()
        # Group by category
        by_cat = {}
        for m in missing:
            cat = m.get("category", "Uncategorised")
            by_cat.setdefault(cat, []).append(m)

        for cat, tools in by_cat.items():
            new_cat_marker = " (NEW SECTION)" if cat in new_cats else ""
            print(f"### Under `## {cat}`{new_cat_marker}")
            print()
            print("```markdown")
            print("| Tool | Category | Difficulty | Ceiling | Pain tags | Best for | Watch out for | Last reviewed | Linh-vetted |")
            print("|------|----------|------------|---------|-----------|----------|----------------|---------------|-------------|")
            for t in tools:
                row, warnings = render_new_row(t, today)
                print(row)
                all_warnings.extend(warnings)
            print("```")
            print()
            for t in tools:
                why = t.get("why_for_this_report", "")
                if why:
                    print(f"- **{t['name']}** — recommended in this report because: {why}")
            print()

    if all_warnings:
        print("## Voice rule warnings")
        print()
        for w in all_warnings:
            print(f"- {w}")
        print()
        print("Patches above have been auto-cleaned to use small-business voice.")
        print()

    print("---")
    print()
    print("## Application steps")
    print()
    print("1. Linh reviews each proposed row. Confirm or edit `Best for` and `Watch out for` per her opinion.")
    print("2. Apply confirmed rows to stack.md locally (paste under the named section).")
    print("3. Optionally, run `sync_to_airtable.py <confirmed_rows.json>` to create matching rows in the Airtable Tools table (defaults to `Linh-vetted: Pending`).")
    print("4. Once Linh has used or formed a strong opinion on each new tool, flip `Linh-vetted: Pending` -> `Yes` in both stack.md and Airtable.")
    print()
    print("**The Linh-vetted rule is preserved:** every new entry defaults to `Pending`. Promotion to `Yes` is always a human decision, never automated.")


if __name__ == "__main__":
    main()

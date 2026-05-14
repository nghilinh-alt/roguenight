"""Updated matching script (v2) — handles multi-value Pain tag and Airtable's actual category names.

Differences from skill v1:
- Categories use Airtable names ("Accounting & finance" not "Accounting", "Field service & trades" not "Field service")
- Pain tag input is now a COMMA-SEPARATED string (multi-value) — split before matching
- Filter Tools where Pain tags overlaps with ANY of the response's pains (not just the single primary)
- Scoring prioritises tools matching the FIRST pain (= primary, per formula order)

Usage:
    python3 match_v2.py <response.json> <tools.json>
"""
import json
import sys

PAIN_PRIORITY_ORDER = [
    "manual-entry",
    "lead-tracking",
    "invoicing",
    "comms",
    "reporting",
    "documents",
    "onboarding",
    "compliance",
    "other",
]

# Airtable category names (the actual ones in the live Tools table)
FOUNDATION_CATEGORIES = {
    "Office suite",
    "Accounting & finance",
    "Field service & trades",
    "Salon and personal services",
}

# Tools.Category → Day-X go-live phase
DEFAULT_PHASE = {
    "Office suite": "Day 1",
    "Accounting & finance": "Day 1",
    "Field service & trades": "Day 1",
    "Salon and personal services": "Day 1",
    "Payments": "Day 7",
    "Scheduling & meetings": "Day 14",
    "CRM & lead management": "Day 14",
    "Project management & operations": "Day 14",
    "Communications & inbox": "Day 14",
    "File storage": "Day 1",
    "E-signature & documents": "Day 30",
    "Document & file management": "Day 30",
    "Marketing & email": "Day 30",
    "Workflow automation": "Day 60",
    "AI assistants (tier 3)": "Day 90",
}

# Industry → categories that don't fit (drop these from candidates)
WRONG_VERTICAL = {
    "Hospitality / food": {"Field service & trades"},
    "Retail / e-commerce": {"Field service & trades"},
    "Education / training": {"Field service & trades", "Salon and personal services"},
    "Healthcare admin / allied health": {"Field service & trades"},
    "Professional services (legal, accounting, consulting, design, etc.)": {"Field service & trades", "Salon and personal services"},
    "Finance / financial services": {"Field service & trades", "Salon and personal services"},
    "Real estate / property": {"Field service & trades", "Salon and personal services"},
    "Construction / trades": {"Salon and personal services"},
    "Manufacturing": {"Salon and personal services", "Field service & trades"},
    "Logistics / transport / warehousing": {"Salon and personal services", "Field service & trades"},
}

SALON_FIT_INDUSTRIES = {"Hospitality / food", "Retail / e-commerce"}


def parse_pain_tags(pain_tag_str: str) -> list:
    """Split the comma-separated Pain tag (derived) string into a list of canonical tags, preserving order."""
    if not pain_tag_str:
        return []
    return [t.strip() for t in pain_tag_str.split(",") if t.strip()]


def already_in_stack(tool_name: str, tool_stack: list) -> bool:
    """Substring match against the client's Tool stack array."""
    name_lower = tool_name.lower()
    for selection in tool_stack or []:
        if name_lower in selection.lower():
            return True
    return False


def is_industry_match(tool_category: str, industry: str) -> bool:
    if "Salon" in tool_category and industry not in SALON_FIT_INDUSTRIES:
        return False
    if tool_category in WRONG_VERTICAL.get(industry, set()):
        return False
    return True


def is_small(headcount: str) -> bool:
    return headcount in ("Just me / 1", "2–10", "11–50")


def score_tool(tool: dict, pain_tags: list, primary_pain: str) -> dict:
    """Score a tool: priority + reason."""
    category = tool["fields"].get("Category", "")
    tool_pains = tool["fields"].get("Pain tags", [])

    # Foundation tools = always High
    if category in FOUNDATION_CATEGORIES:
        priority = "High"
        reason = f"Foundation category ({category})"
    elif primary_pain in tool_pains:
        priority = "High"
        reason = f"Directly addresses primary pain ({primary_pain})"
    elif any(p in tool_pains for p in pain_tags):
        priority = "Medium"
        matched_pains = [p for p in pain_tags if p in tool_pains]
        reason = f"Addresses secondary pain(s) ({', '.join(matched_pains)})"
    elif category in ("Workflow automation",):
        priority = "Low"
        reason = "Glue layer for connecting recommended tools"
    else:
        priority = "Medium"
        reason = "Generally relevant"

    return {"priority": priority, "reason": reason}


def main():
    if len(sys.argv) < 3:
        print("Usage: match_v2.py <response.json> <tools.json>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        response = json.load(f)
    with open(sys.argv[2]) as f:
        tools_data = json.load(f)

    fields = response.get("fields", response)
    industry = fields.get("Industry", "Other")
    headcount = fields.get("Headcount", "Just me / 1")
    pain_tag_str = fields.get("Pain tag (derived)") or _derive_pain_tag(fields.get("Biggest frustration", ""))
    tool_stack = fields.get("Tool stack", []) or []
    tech_appetite = fields.get("Tech appetite", "")

    pain_tags = parse_pain_tags(pain_tag_str)
    primary_pain = pain_tags[0] if pain_tags else "other"

    candidates = []
    for tool in tools_data.get("records", []):
        tf = tool["fields"]
        name = tf.get("Tool name", "")
        category = tf.get("Category", "")
        ceiling = tf.get("Ceiling", "Pro")
        difficulty = tf.get("Difficulty", "Simple")
        tool_pains = tf.get("Pain tags", [])

        if already_in_stack(name, tool_stack):
            continue
        if not is_industry_match(category, industry):
            continue
        if tech_appetite.startswith("Simple") and difficulty == "Hard":
            continue
        if ceiling == "Enterprise" and is_small(headcount):
            continue
        # Must touch at least one pain OR be a foundation category
        if not any(p in tool_pains for p in pain_tags) and category not in FOUNDATION_CATEGORIES:
            continue

        score = score_tool(tool, pain_tags, primary_pain)
        phase = DEFAULT_PHASE.get(category, "Day 30")
        candidates.append({
            "tool_id": tool.get("id"),
            "tool_name": name,
            "category": category,
            "ceiling": ceiling,
            "difficulty": difficulty,
            "pain_tags": tool_pains,
            "priority": score["priority"],
            "reason": score["reason"],
            "phase": phase,
            "indicative_cost_aud": tf.get("Indicative cost AUD/month", 0),
            "best_for": tf.get("Best for", ""),
            "watch_out_for": tf.get("Watch out for", ""),
            "linh_vetted": tf.get("Linh-vetted", "Pending"),
        })

    # Sort: priority desc, then phase order
    PRIO = {"High": 3, "Medium": 2, "Low": 1}
    PHASE_ORDER = {"Day 0": 0, "Day 1": 1, "Day 7": 2, "Day 14": 3, "Day 21": 4, "Day 30": 5, "Day 60": 6, "Day 90": 7}
    candidates.sort(key=lambda c: (-PRIO.get(c["priority"], 0), PHASE_ORDER.get(c["phase"], 99), c["tool_name"]))

    out = {
        "industry": industry,
        "headcount": headcount,
        "tech_appetite": tech_appetite,
        "primary_pain": primary_pain,
        "all_pains": pain_tags,
        "recommendations": candidates[:8],
    }
    print(json.dumps(out, indent=2))


def _derive_pain_tag(big_frust: str) -> str:
    """Fallback for raw Biggest frustration text (when Pain tag (derived) isn't computed)."""
    if not big_frust:
        return "other"
    mapping = [
        ("Manual data entry", "manual-entry"),
        ("Lead tracking", "lead-tracking"),
        ("Quote / invoice", "invoicing"),
        ("Customer / client", "comms"),
        ("Reporting", "reporting"),
        ("Document management", "documents"),
        ("Hiring", "onboarding"),
        ("Compliance", "compliance"),
        ("Something else", "other"),
    ]
    tags = [tag for prefix, tag in mapping if prefix in big_frust]
    return ", ".join(tags) if tags else "other"


if __name__ == "__main__":
    main()

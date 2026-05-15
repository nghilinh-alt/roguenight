"""Recommendation matching script (v4) — allowlist-based vertical filtering.

v4 changes from v3:
- Replaces WRONG_VERTICAL denylist and SALON_FIT_INDUSTRIES exception with a single
  VERTICAL_CATEGORY_FIT allowlist. Vertical-specific categories (e.g. Salon and personal
  services, Field service & trades) must positively match a client's industry; categories
  not listed are cross-vertical (allowed for any industry).
- This fails safely: when a new Industry option is added in Airtable, vertical-specific
  tools stay blocked until the allowlist is updated. The previous denylist failed open —
  unknown industries silently received salon and field-service tools.

v3 features retained:
- Reads 'Pain tags (multi)' multi-select field first (array of {name:...} objects or strings),
  falls back to 'Pain tag (derived)' formula field for backwards compatibility
- Expanded canonical tag vocabulary: manual-entry, lead-tracking, invoicing, comms,
  email-overload, reporting, documents, onboarding, compliance, system-fragmentation,
  rostering, training, other
- Category affinity (CATEGORY_PAIN_AFFINITY) — tools in certain categories match certain
  pains implicitly even when the tool's own Pain tags don't list them
- Bundle aliases (BUNDLE_ALIASES) for existing-stack detection
- First tag treated as primary pain for High-priority scoring

Usage:
    python3 match_recommendations.py <response.json> <tools.json>
"""
import json
import sys

PAIN_PRIORITY_ORDER = [
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

# Category → implicit pain tag relevance (tools in these categories are relevant
# to these pains even if the tool's own Pain tags don't list them explicitly)
CATEGORY_PAIN_AFFINITY = {
    "File storage": {"documents"},
    "E-signature & documents": {"documents", "compliance"},
    "Project management & operations": {"reporting", "system-fragmentation", "training"},
    "Workflow automation": {"manual-entry", "system-fragmentation"},
    "Communications & inbox": {"comms", "email-overload"},
    "Scheduling & meetings": {"rostering", "comms"},
}

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

# Allowlist: vertical-specific tool categories that require an explicit positive industry
# match. Any category NOT listed here is cross-vertical (allowed for any industry).
#
# Why allowlist over denylist? When a new Industry option is added in Airtable, a denylist
# silently allows salon/field-service tools through. An allowlist keeps them blocked until
# the new industry is explicitly granted access. Fails closed, not open.
#
# When the Airtable Industry singleSelect grows (e.g. adding "Beauty / personal services"
# or "HVAC / electrical / plumbing"), update this map to grant access from those industries.
VERTICAL_CATEGORY_FIT = {
    # Salon-specific tools (Fresha, Phorest, Timely, Mindbody): only recommend to
    # actual personal-services businesses. No current Airtable Industry option fits.
    # When a Beauty / personal services / wellness option is added, list it here.
    "Salon and personal services": set(),

    # Field-service tools (ServiceM8, Tradify, SimPRO, AroFlo): trades businesses only.
    "Field service & trades": {"Construction / trades"},
}


def parse_pain_tags_multi(multi_field) -> list:
    """Parse the Pain tags (multi) field — array of {name:...} objects or plain strings."""
    if not multi_field:
        return []
    tags = []
    for item in multi_field:
        if isinstance(item, dict):
            tag = item.get("name", "")
        else:
            tag = str(item)
        tag = tag.strip()
        if tag and tag not in tags:
            tags.append(tag)
    return tags


def parse_pain_tags(pain_tag_str: str) -> list:
    """Split the comma-separated Pain tag (derived) string into a list of canonical tags, preserving order."""
    if not pain_tag_str:
        return []
    # Handle both comma-separated and slash-separated (some formula outputs use /)
    for sep in [",", "/"]:
        if sep in pain_tag_str:
            return [t.strip() for t in pain_tag_str.split(sep) if t.strip()]
    return [pain_tag_str.strip()] if pain_tag_str.strip() else []


# Bundled-tool aliases: if the client has the key, the values are already in their stack
BUNDLE_ALIASES = {
    "microsoft 365": ["onedrive", "sharepoint", "microsoft teams", "outlook"],
    "google workspace": ["google drive", "gmail", "google meet", "google docs"],
    "hubspot": ["hubspot crm"],
    "salesforce": ["salesforce essentials"],
    "zoho": ["zoho crm"],
    "pipedrive": ["pipedrive"],
}


def already_in_stack(tool_name: str, tool_stack: list) -> bool:
    """Substring match against the client's Tool stack array, including bundle aliases."""
    name_lower = tool_name.lower()
    for selection in tool_stack or []:
        sel_lower = selection.lower()
        # Direct substring match
        if name_lower in sel_lower or sel_lower in name_lower:
            return True
        # Bundle alias: if they have M365, they have OneDrive/SharePoint/Teams
        for bundle_key, aliases in BUNDLE_ALIASES.items():
            if bundle_key in sel_lower:
                for alias in aliases:
                    if alias in name_lower:
                        return True
    return False


def is_industry_match(tool_category: str, industry: str) -> bool:
    """Return True if tools in this category are appropriate for this industry.

    Allowlist semantics: categories listed in VERTICAL_CATEGORY_FIT must positively
    match the client's industry. Categories not listed are cross-vertical (always
    allowed). This fails closed when a new Industry option appears without an
    explicit allowlist entry.
    """
    allowed_industries = VERTICAL_CATEGORY_FIT.get(tool_category)
    if allowed_industries is not None:
        # Vertical-specific category — require positive industry match
        return industry in allowed_industries
    # Cross-vertical category — always allowed
    return True


def is_small(headcount: str) -> bool:
    return headcount in ("Just me / 1", "2–10", "11–50")


def score_tool(tool: dict, pain_tags: list, primary_pain: str) -> dict:
    """Score a tool: priority + reason.

    v3: Foundation tools that also match a pain tag score higher than
    foundation tools with no pain overlap. Category affinity counts too.
    """
    category = tool["fields"].get("Category", "")
    tool_pains = tool["fields"].get("Pain tags", [])
    category_affinity = CATEGORY_PAIN_AFFINITY.get(category, set())

    matches_primary = primary_pain in tool_pains or primary_pain in category_affinity
    matches_any_pain = any(p in tool_pains for p in pain_tags)
    matches_any_affinity = bool(category_affinity & set(pain_tags))

    if matches_primary:
        priority = "High"
        reason = f"Directly addresses primary pain ({primary_pain})"
    elif category in FOUNDATION_CATEGORIES and matches_any_pain:
        priority = "High"
        matched = [p for p in pain_tags if p in tool_pains]
        reason = f"Foundation category ({category}) + matches pain ({', '.join(matched)})"
    elif category in FOUNDATION_CATEGORIES:
        # Foundation but no pain match — deprioritise
        priority = "Medium"
        reason = f"Foundation category ({category}) — no direct pain match"
    elif matches_any_pain:
        priority = "Medium"
        matched = [p for p in pain_tags if p in tool_pains]
        reason = f"Addresses secondary pain(s) ({', '.join(matched)})"
    elif matches_any_affinity:
        priority = "Medium"
        matched = [p for p in pain_tags if p in category_affinity]
        reason = f"Category affinity for ({', '.join(matched)})"
    elif category in ("Workflow automation",):
        priority = "Low"
        reason = "Glue layer for connecting recommended tools"
    else:
        priority = "Low"
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
    tool_stack = fields.get("Tool stack", []) or []
    tech_appetite = fields.get("Tech appetite", "")

    # v3: read Pain tags (multi) first, fall back to Pain tag (derived)
    pain_tags = parse_pain_tags_multi(fields.get("Pain tags (multi)"))
    if not pain_tags:
        pain_tag_str = fields.get("Pain tag (derived)") or _derive_pain_tag(fields.get("Biggest frustration", ""))
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
        # Must touch at least one pain OR be a foundation category OR have category affinity
        category_affinity = CATEGORY_PAIN_AFFINITY.get(category, set())
        has_pain_overlap = any(p in tool_pains for p in pain_tags)
        has_affinity_overlap = bool(category_affinity & set(pain_tags))
        if not has_pain_overlap and not has_affinity_overlap and category not in FOUNDATION_CATEGORIES:
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

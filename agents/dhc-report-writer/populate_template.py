"""Populate the v5+ AI & Automation Strategy template with a client's data.

REFACTORED 2026-05-15: split into a small package of sibling modules.
The CLI entry point and main() orchestration live here; everything else
moved out to keep each file readable.

Module layout (all siblings in the same directory):
- populate_template.py   (this file)   CLI + main() + context assembly
- _pt_assets.py          avatar PNGs, file loaders, _resolve helper
- _pt_render.py          all render_* functions (tool card, agent card, etc.)
- _pt_template.py        the full HTML f-string template
- data/extra-styles.css  report-specific CSS (loaded by _pt_assets)
- data/v5-style-block.txt brand v5 CSS (loaded by _pt_assets)

PREVIOUS UPDATE 2026-05-11: switched from Stella Find & Replace to generate
the complete v5-quality HTML directly from a vars.json — simpler, more
reliable, no Stella content left to scrub.

Inputs:
- response.json: a Response row from Airtable (or mock_response.json for testing)
- vars.json: per-client computed values (see report_vars.example.json for shape)

Output:
- output.html: brand-locked v5-quality HTML ready for browser preview + PDF render.

Usage:
    python3 populate_template.py <response.json> <vars.json> <output.html>

Workflow context (Lois agent calling this script):
- Lois runs match_recommendations.py first to get 5-8 candidate tools
- Lois applies writer judgement to narrow to 5-7 final recommendations:
  * Primary pain (first in derived Pain tag list) gets weighted first
  * Cost-sensitivity: if "I have no money" or similar appears in Anything else notes,
    lead with cheapest credible tier on every tool
  * Industry-fit nuance the matcher can miss (e.g. Xero Cashbook for tight-budget
    healthcare admin instead of Xero Grow)
- Lois drafts per-client copy for each tool's "Why this for you" and "Why not the
  alternatives" — these are the high-judgement bits that justify the $880 fee
- Lois assembles vars.json and calls this script to generate the HTML
"""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

from _pt_assets import (
    AVATAR_AGENT_B64,
    AVATAR_TEAM_B64,
    AVATAR_YOU_B64,
    load_extra_styles,
    load_logo_b64,
    load_style_block,
)
from _pt_render import (
    _render_testimonial,
    normalise_batches,
    render_batch_block,
    render_benefit_row,
    render_cost_growth_html,
    render_cost_recurring_html,
    render_cull_items,
    render_dil_rows,
    render_key_benefits,
    render_phases_html,
    render_testimonial,
    render_tool_card,
)
from _pt_template import render_report_html


def _build_context(resp: dict, v: dict) -> SimpleNamespace:
    """Assemble the rendering context from a parsed response + vars dict.

    Extracts client identity, snapshot fields, and pre-renders every
    HTML fragment (recs, benefits, phases, costs, etc.) so the template
    is purely interpolation — no inline rendering logic.
    """
    fields = resp.get("fields", resp)

    return SimpleNamespace(
        # Raw vars for v.get() calls in the template
        v=v,

        # Loaded asset blocks
        style=load_style_block(),
        extra_styles=load_extra_styles(),
        logo_b64=load_logo_b64(),

        # Client identity
        client=fields.get("Business name") or fields.get("Client name", "Client"),
        ref=fields.get("Reference", "DHC-XXXX-XXXX"),
        today=v.get("delivered_date", ""),

        # Snapshot fields (Section 03)
        industry=fields.get("Industry", "Other"),
        headcount=fields.get("Headcount", ""),
        years=fields.get("Years operating", ""),
        cpw=fields.get("Customers per week", ""),
        goal=fields.get("Stated goal", ""),
        pain_narr=fields.get("Pain narrative", ""),
        future=fields.get("Future state vision", ""),
        tech=fields.get("Tech appetite", "").split(" - ")[0],
        hated=fields.get("Hated weekly task", ""),
        ai_appetite=fields.get("AI appetite", ""),

        # Cover
        cover_title=v.get("cover_title", "A clearer path to running smarter."),
        cover_accent=v.get("cover_accent", ""),
        cover_subtitle=v.get("cover_subtitle", ""),

        # Section 01 — Executive summary
        exec_summary_lede=v.get("exec_summary_lede", ""),
        key_benefits_html=render_key_benefits(v.get("key_benefits", [])),

        # Section 02 — Day-in-the-life + quantified benefits
        dil_rows_html=render_dil_rows(v.get("day_in_life", [])),
        benefits_html="".join(render_benefit_row(b) for b in v.get("benefits", [])),

        # Section 04 — Roadmap
        phases_html=render_phases_html(v.get("phases", [])),

        # Section 05 — Recommended stack
        recs_html="".join(render_tool_card(r) for r in v.get("recs", [])),
        cull_items=render_cull_items(v.get("cull", [])),

        # Section 07 — Future digital employees
        employees_html="".join(render_batch_block(b) for b in normalise_batches(v)),

        # Section 08 — Cost and investment
        cost_recurring_html=render_cost_recurring_html(v.get("cost_recurring", [])),
        cost_growth_html=render_cost_growth_html(v.get("cost_growth", [])),

        # Section 10 — Next steps
        testimonial_html=render_testimonial(v.get("testimonial")),
    )


def main():
    if len(sys.argv) < 4:
        print("Usage: populate_template.py <response.json> <vars.json> <output.html>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        resp = json.load(f)
    with open(sys.argv[2]) as f:
        v = json.load(f)

    ctx = _build_context(resp, v)
    html = render_report_html(ctx)

    out_path = Path(sys.argv[3])
    out_path.write_text(html)
    size_kb = out_path.stat().st_size / 1024
    print(f"HTML written to {sys.argv[3]} — {size_kb:.1f} KB")


if __name__ == "__main__":
    main()

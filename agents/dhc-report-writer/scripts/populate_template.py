"""Populate the v5 AI & Automation Strategy template with a client's data.

UPDATED 2026-05-11: now builds the complete v5-quality report from scratch using v5's
CSS verbatim and v5's class structure. Previously, this script did targeted Find &
Replace on a pre-cloned Stella template; this version generates the full HTML directly
from a vars.json — simpler, more reliable, no Stella content left to scrub.

Inputs:
- response.json: a Response row from Airtable (or mock_response.json for testing)
- vars.json: per-client computed values (see report_vars.example.json for shape)
- v5-style-block.txt (alongside this script): the v5 template's <style> block.
  Refresh this file whenever the brand kit's CSS evolves.
- horizontal-b64.txt (alongside this script): base64 horizontal lockup PNG for the
  cover. Avoids /api/files/ URLs that fail in sandboxed iframes (see brand kit memory).

Output:
- report.html: brand-locked v5-quality HTML ready for browser preview + PDF render.

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

SKILL_DIR = Path(__file__).parent
DATA_DIR = SKILL_DIR.parent / "data"


def _resolve(filename):
    """Resolve a data file's path. Handles both layouts:

    - Repo layout: scripts in `agents/dhc-report-writer/scripts/`, data files
      in `agents/dhc-report-writer/data/`. The data dir is preferred.
    - Hyperagent skill workspace layout: all files flat in
      `/agent/workspace/skills/{skillName}/`, so the script directory itself
      contains the data files.

    Returns the first existing path, or None if not found anywhere.
    """
    for candidate in (DATA_DIR / filename, SKILL_DIR / filename):
        if candidate.exists():
            return candidate
    return None


def render_tool_card(r):
    """Render one tool card matching v5's .tool / .tool-grid / .tier-row markup."""
    badge_class = "priority-high" if r["priority"] == "High" else (
        "priority-med" if r["priority"] == "Medium" else "priority-low"
    )
    tiers = r.get("tiers", [{"name": r.get("tier", ""), "price": f"${r.get('cost', 0)}/mo", "recommended": True}])
    tier_rows = "".join(
        f'<div class="tier-row{" recommended" if t.get("recommended") else ""}">'
        f'<span class="tier-name">{t["name"]}</span>'
        f'<span class="tier-price">{t["price"]}</span></div>'
        for t in tiers
    )
    return f"""
      <div class="tool">
        <div class="tool-top">
          <div>
            <div class="tool-name">{r['name']}</div>
            <div class="tool-subtitle">{r.get('subtitle', '')}</div>
          </div>
          <div class="tool-badges">
            <span class="badge {badge_class}">Priority · {r['priority']}</span>
            <span class="badge when">Goes live: {r['phase']}</span>
          </div>
        </div>
        <div class="tool-grid">
          <div class="tool-rationale">
            <div class="rationale-block">
              <div class="rationale-label">Why this for you</div>
              <div class="rationale-text">{r['why']}</div>
            </div>
            <div class="rationale-block">
              <div class="rationale-label">Why not the alternatives</div>
              <div class="rationale-text">{r.get('alt_skipped', '')}</div>
            </div>
            <div class="rationale-block">
              <div class="rationale-label">Watch out for</div>
              <div class="rationale-text warn">{r.get('watch', '')}</div>
            </div>
            <div class="integration-callout">
              <strong>Integrations:</strong> {r.get('integrations', '')}
            </div>
          </div>
          <div class="tool-pricing">
            <div class="tool-pricing-label">Pricing</div>
            {tier_rows}
            <div class="upgrade-trigger"><strong>Upgrade trigger:</strong> {r.get('upgrade_trigger', '')}</div>
          </div>
        </div>
      </div>
"""


def render_benefit_row(b):
    return f"""
        <tr>
          <td class="change-cell">{b['change']}<span class="sub">{b.get('sub', '')}</span></td>
          <td class="right"><span class="num">{b['hours']}</span> hrs</td>
          <td class="right"><span class="num">{b['dollar']}</span></td>
        </tr>"""


def main():
    if len(sys.argv) < 4:
        print("Usage: populate_template.py <response.json> <vars.json> <output.html>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        resp = json.load(f)
    with open(sys.argv[2]) as f:
        v = json.load(f)

    fields = resp.get("fields", resp)
    style_path = _resolve("v5-style-block.txt")
    style = style_path.read_text() if style_path else "<style>/* v5-style-block.txt not staged — render will be unstyled. Copy from the v5 reference template before running. */</style>"
    logo_path = _resolve("horizontal-b64.txt")
    logo_b64 = logo_path.read_text().strip() if logo_path else ""

    client = fields.get("Business name") or fields.get("Client name", "Client")
    ref = fields.get("Reference", "DHC-XXXX-XXXX")
    industry = fields.get("Industry", "Other")
    headcount = fields.get("Headcount", "")
    years = fields.get("Years operating", "")
    cpw = fields.get("Customers per week", "")
    goal = fields.get("Stated goal", "")
    pain_narr = fields.get("Pain narrative", "")
    future = fields.get("Future state vision", "")
    tech = fields.get("Tech appetite", "").split(" - ")[0]
    hated = fields.get("Hated weekly task", "")
    ai_appetite = fields.get("AI appetite", "")
    today = v.get("delivered_date", "")
    cover_title = v.get("cover_title", "A clearer path to running smarter.")
    cover_accent = v.get("cover_accent", "")
    cover_subtitle = v.get("cover_subtitle", "")
    exec_summary_lede = v.get("exec_summary_lede", "")
    benefits_html = "".join(render_benefit_row(b) for b in v.get("benefits", []))
    recs_html = "".join(render_tool_card(r) for r in v.get("recs", []))
    cull_items = "".join(f"<li><strong>{c[0]}</strong> — {c[1]}</li>" for c in v.get("cull", []))
    # Section 08 — three-batch rendering with pain-match badge + readiness + ties-to quote.
    # Backward compat: if vars has a flat "employees" array but no "batches", wrap it as Batch 01.
    batches = v.get("batches")
    if not batches and v.get("employees"):
        batches = [{
            "number": "01",
            "day": "Day 90",
            "title": "High impact, ready now.",
            "description": "These agents work with the stack you'll have running by Week 12. Each one pays back in months, not years.",
            "agents": v.get("employees", []),
        }]
    batches = batches or []

    def _agent_card(a):
        pain = a.get("pain_match", "")
        tier = a.get("pain_tier", "")
        if pain and tier:
            eyebrow = (
                f'<div style="font-family: \'Instrument Sans\', sans-serif; font-size: 11px; '
                f'font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; '
                f'color: var(--gold); margin-bottom: 10px;">Pain match · {pain} · {tier}</div>'
            )
        elif pain:
            eyebrow = (
                f'<div style="font-family: \'Instrument Sans\', sans-serif; font-size: 11px; '
                f'font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; '
                f'color: var(--gold); margin-bottom: 10px;">Pain match · {pain}</div>'
            )
        else:
            eyebrow = ""
        readiness = a.get("readiness", "")
        ready_str = f' · Ready · {readiness}' if readiness else ""
        ties = a.get("ties_to", "")
        ties_label = a.get("ties_label", "")
        if ties:
            ties_str = (
                f'<p style="margin-top: 14px; font-family: \'Instrument Serif\', Georgia, serif; '
                f'font-style: italic; font-size: 15.5px; line-height: 1.5; color: var(--slate);">'
                f'Ties to: &ldquo;{ties}&rdquo;{(" &mdash; " + ties_label) if ties_label else ""}</p>'
            )
        else:
            ties_str = ""
        return (
            '<div style="margin-top: 22px; padding: 22px 24px; background: var(--gold-soft); '
            'border-left: 2px solid var(--gold); border-radius: 3px;">'
            f'{eyebrow}'
            f'<p class="body-lede" style="font-size: 19px; margin: 0;">{a["name"]}</p>'
            f'<p class="meta" style="margin-top: 8px;">Replaces: {a["replaces"]} '
            f'· Saves ~{a["hours"]} · Worth {a["dollar"]}{ready_str}</p>'
            f'<p style="margin-top: 12px;">{a["description"]}</p>'
            f'{ties_str}'
            '</div>'
        )

    def _batch_block(b):
        agents = "".join(_agent_card(a) for a in b.get("agents", []))
        return (
            '<div style="margin-top: 56px;">'
            '<div style="padding-top: 28px; border-top: 1px solid var(--rule);">'
            f'<div style="font-family: \'Instrument Sans\', sans-serif; font-size: 11.5px; '
            f'font-weight: 600; letter-spacing: 0.20em; text-transform: uppercase; '
            f'color: var(--slate); margin-bottom: 12px;">Batch {b["number"]} · {b["day"]}</div>'
            f'<h3 style="font-family: \'Instrument Serif\', Georgia, serif; font-size: 30px; '
            f'line-height: 1.18; letter-spacing: -0.01em; color: var(--ink); margin: 0;">{b["title"]}</h3>'
            f'<p class="lede" style="margin-top: 14px; max-width: 680px;">{b.get("description", "")}</p>'
            '</div>'
            f'{agents}'
            '</div>'
        )

    employees_html = "".join(_batch_block(b) for b in batches)
    phases_html = ""
    for p in v.get("phases", []):
        tasks_html = "".join(f"<li>{t}</li>" for t in p.get("tasks", []))
        phases_html += f"""
            <h3 style="margin-top: 24px;">{p['week']} — {p['headline']}</h3>
            <ul style="margin-top: 8px; padding-left: 20px; font-size: 15px; line-height: 1.7;">
              {tasks_html}
            </ul>"""
    cost_recurring_html = "".join(
        f"<tr><td>{c['tool']}</td><td>{c['tier']}</td><td class=\"right\">{c['cost']}</td></tr>"
        for c in v.get("cost_recurring", [])
    )
    cost_growth_html = "".join(
        f"<tr><td>{c['trigger']}</td><td>{c['next']}</td><td class=\"right\">{c['extra']}</td></tr>"
        for c in v.get("cost_growth", [])
    )

    # Section 02 — Priority Actions (v6 — AI & Automation Strategy rebrand)
    # Explicit list preferred; otherwise derive from top 5 recommendations.
    priority_actions = v.get("priority_actions", [])
    if not priority_actions:
        for r in v.get("recs", [])[:5]:
            priority_actions.append({
                "action": r.get("name", ""),
                "fix": r.get("priority_fix") or r.get("subtitle", ""),
                "outcome": r.get("priority_outcome", ""),
            })
    priority_actions_html = "".join(
        f"""
        <div class="priority-action">
          <div class="priority-num">{i+1:02d}</div>
          <div class="priority-body">
            <h3 class="priority-title">{pa.get('action', '')}</h3>
            <p class="priority-fix">{pa.get('fix', '')}</p>
            <p class="priority-outcome"><span class="arrow">→</span> {pa.get('outcome', '')}</p>
          </div>
        </div>"""
        for i, pa in enumerate(priority_actions[:5])
    )

    # Section 03 — Expected ROI (v6 — AI & Automation Strategy rebrand)
    # Defaults reflect the v6 spec; Lois can override per-client via vars.
    roi_time_items = v.get("roi_time_items", [
        "20–30 hours per month recovered",
        "Reduced admin, follow-ups, and duplication",
    ])
    roi_consistency_items = v.get("roi_consistency_items", [
        "Leads tracked properly",
        "Clients onboarded smoothly",
        "Contracts and communication standardised",
    ])
    roi_demand_items = v.get("roi_demand_items", [
        "More inbound enquiries",
        "Less reliance on cold outreach",
    ])
    roi_value_amount = v.get("roi_value_amount", "$1,900 – $5,700+")
    roi_value_period = v.get("roi_value_period", "per month")
    roi_value_note = v.get("roi_value_note",
        "Most clients recover the cost of this engagement within the first 30 days through improved efficiency alone.")
    def _li_list(items):
        return "".join(f"<li>{x}</li>" for x in items)
    roi_time_html = _li_list(roi_time_items)
    roi_consistency_html = _li_list(roi_consistency_items)
    roi_demand_html = _li_list(roi_demand_items)

    HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI & Automation Strategy — {client}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
{style}
<style>
  .cover-logo {{ height: 56px; width: auto; }}

  /* Executive Summary extras (v6 — AI & Automation Strategy rebrand) */
  .exec-unlocks {{
    list-style: none;
    padding-left: 0;
    margin: 14px 0 0;
  }}
  .exec-unlocks li {{
    position: relative;
    padding: 8px 0 8px 26px;
    font-size: 16px;
    line-height: 1.5;
    border-bottom: 1px solid rgba(10, 14, 26, 0.08);
  }}
  .exec-unlocks li:last-child {{ border-bottom: none; }}
  .exec-unlocks li::before {{
    content: '→';
    position: absolute;
    left: 0;
    top: 8px;
    color: var(--gold, #C9A961);
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    font-size: 18px;
  }}
  .exec-callout {{
    margin-top: 28px;
    padding: 22px 28px;
    background: rgba(201, 169, 97, 0.07);
    border-left: 3px solid var(--gold, #C9A961);
    border-radius: 2px;
  }}
  .exec-callout p {{
    margin: 0;
    line-height: 1.5;
  }}
  .exec-callout .lede-label {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--slate, #6B7280);
    margin-bottom: 6px;
  }}
  .exec-callout .lede-body {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 20px;
    font-style: italic;
    color: var(--gold, #C9A961);
    line-height: 1.4;
  }}
  .exec-closing {{ margin-top: 28px; line-height: 1.6; }}

  /* Priority Actions section */
  .priority-actions {{
    margin-top: 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}
  .priority-action {{
    display: grid;
    grid-template-columns: 56px 1fr;
    gap: 18px;
    padding: 18px 20px;
    background: rgba(10, 14, 26, 0.03);
    border-radius: 4px;
    border: 1px solid rgba(10, 14, 26, 0.06);
  }}
  .priority-num {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    color: var(--gold, #C9A961);
    font-size: 32px;
    line-height: 1;
    letter-spacing: 0.04em;
  }}
  .priority-title {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 20px;
    font-weight: 400;
    color: var(--ink, #0A0E1A);
    margin: 0 0 4px;
    letter-spacing: -0.01em;
  }}
  .priority-fix {{
    font-size: 15px;
    color: var(--slate-deep, #4B5563);
    margin: 0 0 6px;
    line-height: 1.5;
  }}
  .priority-outcome {{
    font-size: 15px;
    color: var(--ink, #0A0E1A);
    margin: 0;
    line-height: 1.5;
  }}
  .priority-outcome .arrow {{
    color: var(--gold, #C9A961);
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    margin-right: 6px;
  }}
  .priority-close {{
    margin-top: 24px;
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 18px;
    font-style: italic;
    color: var(--ink, #0A0E1A);
    opacity: 0.85;
    line-height: 1.5;
  }}

  /* Expected ROI section */
  .roi-outcomes {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 22px;
    margin-top: 20px;
  }}
  @media (max-width: 880px) {{
    .roi-outcomes {{ grid-template-columns: 1fr; }}
  }}
  .roi-outcome {{
    padding: 20px;
    border-top: 2px solid var(--gold, #C9A961);
    background: rgba(10, 14, 26, 0.02);
  }}
  .roi-outcome-eyebrow {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--gold, #C9A961);
    margin-bottom: 10px;
  }}
  .roi-outcome-title {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 22px;
    font-weight: 400;
    color: var(--ink, #0A0E1A);
    margin: 0 0 12px;
    letter-spacing: -0.005em;
  }}
  .roi-outcome ul {{
    margin: 0;
    padding: 0;
    list-style: none;
  }}
  .roi-outcome li {{
    font-size: 14.5px;
    line-height: 1.5;
    color: var(--slate-deep, #4B5563);
    padding: 5px 0;
  }}
  .roi-value-block {{
    margin-top: 28px;
    padding: 26px 30px;
    background: var(--ink, #0A0E1A);
    color: var(--parchment, #EDE8DD);
    border-radius: 2px;
  }}
  .roi-value-label {{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gold, #C9A961);
    margin-bottom: 8px;
  }}
  .roi-value-amount {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 32px;
    line-height: 1.15;
    color: var(--parchment, #EDE8DD);
    letter-spacing: -0.01em;
  }}
  .roi-value-amount em {{
    color: var(--gold, #C9A961);
    font-style: italic;
  }}
  .roi-value-note {{
    margin-top: 14px;
    font-size: 14px;
    line-height: 1.5;
    color: rgba(237, 232, 221, 0.78);
  }}
</style>
</head>
<body>

<section class="cover">
  <div class="cover-inner">
    <div class="cover-top">
      <img class="cover-logo" src="data:image/png;base64,{logo_b64}" alt="Rogue Night">
    </div>
    <div class="cover-title-block">
      <div class="cover-eyebrow">AI & Automation Strategy · Specially curated</div>
      <h1 class="cover-title">{cover_title}<br><span class="accent">{cover_accent}</span></h1>
      <p class="cover-subtitle">{cover_subtitle}</p>
    </div>
    <div class="cover-bottom">
      <div class="cover-meta-block">
        <div class="cover-meta-label">Prepared for</div>
        <div class="cover-meta-value">{client}</div>
      </div>
      <div class="cover-meta-block">
        <div class="cover-meta-label">Delivered</div>
        <div class="cover-meta-value">{today}</div>
      </div>
      <div class="cover-meta-block">
        <div class="cover-meta-label">Reference</div>
        <div class="cover-meta-value">{ref}</div>
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">01 · Executive summary</div>
      <h2>From reactive operations to a scalable, AI-enabled business.</h2>
    </div>
    {f'<p class="body-lede">{exec_summary_lede}</p>' if exec_summary_lede else ''}
    <p class="body-lede" style="margin-top: 18px;">Right now, your business works — but it relies heavily on your time. Leads don't consistently come to you. Admin work slows you down. Key processes depend on manual effort, which limits how much you can grow without working more hours.</p>
    <p class="body-lede" style="margin-top: 16px; font-style: italic;">This report shows you how to fix that.</p>
    <p style="margin-top: 24px; font-size: 16px; line-height: 1.6;">By implementing a small, carefully selected tool stack and introducing targeted automation, you can:</p>
    <ul class="exec-unlocks">
      <li>Recover 20–30 hours per month</li>
      <li>Reduce manual admin and follow-ups</li>
      <li>Shift from outbound chasing to inbound demand</li>
      <li>Create systems that run even when you don't</li>
    </ul>
    <div class="exec-callout">
      <div class="lede-label">In practical terms</div>
      <p class="lede-body">Most businesses at your stage unlock $1,900–$5,700 per month in time value within the first 30–60 days.</p>
    </div>
    <p class="exec-closing">This is not a generic audit. This is a clear, step-by-step plan for running your business with better systems, better tools, and AI support that earns its place.</p>
    {v.get('exec_summary_para_2', '')}
    {v.get('exec_summary_para_3', '')}
    <div class="benefits" style="margin-top: 36px;">
      {''.join(f'<div class="benefit"><div class="benefit-eyebrow">Key benefit · {i+1:02d}</div><div class="benefit-title">{b["title"]}</div><div class="benefit-body">{b["body"]}</div></div>' for i, b in enumerate(v.get("key_benefits", [])))}
    </div>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">02 · Your priority actions</div>
      <h2>{v.get('priority_actions_h2', 'If you do nothing else, do these first.')}</h2>
      <p class="lede">{v.get('priority_actions_lede', 'These five changes deliver the fastest return with the least effort.')}</p>
    </div>
    <div class="priority-actions">
      {priority_actions_html}
    </div>
    <p class="priority-close">{v.get('priority_actions_close', 'These five steps alone remove your biggest operational bottlenecks and create immediate momentum.')}</p>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">03 · Expected outcomes</div>
      <h2>{v.get('roi_h2', 'What you should expect in the first 30–60 days.')}</h2>
      <p class="lede">{v.get('roi_lede', 'Once the foundation is implemented, here is what changes.')}</p>
    </div>
    <div class="roi-outcomes">
      <div class="roi-outcome">
        <div class="roi-outcome-eyebrow">Time savings</div>
        <div class="roi-outcome-title">Hours back in your week.</div>
        <ul>{roi_time_html}</ul>
      </div>
      <div class="roi-outcome">
        <div class="roi-outcome-eyebrow">Improved consistency</div>
        <div class="roi-outcome-title">Things stop falling through.</div>
        <ul>{roi_consistency_html}</ul>
      </div>
      <div class="roi-outcome">
        <div class="roi-outcome-eyebrow">Increased demand</div>
        <div class="roi-outcome-title">Inbound replaces chasing.</div>
        <ul>{roi_demand_html}</ul>
      </div>
    </div>
    <div class="roi-value-block">
      <div class="roi-value-label">Estimated monthly value</div>
      <div class="roi-value-amount"><em>{roi_value_amount}</em> {roi_value_period} in recovered time and efficiency.</div>
      <p class="roi-value-note">{roi_value_note}</p>
    </div>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">04 · Quantified benefits</div>
      <h2>{v.get('q_benefits_h2', 'What each move is worth, in hours and dollars.')}</h2>
      <p class="lede">{v.get('q_benefits_lede', '')}</p>
    </div>
    <table class="qb-table">
      <thead>
        <tr><th>The change</th><th class="right">Hours saved · monthly</th><th class="right">Dollar value · monthly</th></tr>
      </thead>
      <tbody>
        {benefits_html}
        <tr class="subtotal"><td>Time and admin recovered, monthly</td><td class="right"><span class="num" style="font-style: italic;">{v.get('benefits_subtotal_hrs', '')}</span> hrs</td><td class="right"><em>{v.get('benefits_subtotal_dollar', '')}</em></td></tr>
      </tbody>
    </table>
    <p class="meta" style="margin-top: 24px;">{v.get('benefits_basis_note', '')}</p>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">05 · Current state</div>
      <h2>The snapshot. Verbatim from your questionnaire.</h2>
    </div>
    <div class="snapshot">
      <div class="snapshot-row"><div class="snapshot-label">Industry</div><div class="snapshot-value">{industry}</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Headcount</div><div class="snapshot-value">{headcount}</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Years operating</div><div class="snapshot-value">{years}</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Customers per week</div><div class="snapshot-value">~{cpw}</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Stated goal</div><div class="snapshot-value serif">"{goal}"</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Pain narrative</div><div class="snapshot-value serif">"{pain_narr}"</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Hated weekly task</div><div class="snapshot-value serif">"{hated}"</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Future state vision</div><div class="snapshot-value serif">"{future}"</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Tech comfort</div><div class="snapshot-value">{tech}</div></div>
      <div class="snapshot-row"><div class="snapshot-label">AI readiness</div><div class="snapshot-value">{ai_appetite}</div></div>
    </div>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">06 · Recommended stack</div>
      <h2>{v.get('recs_h2', 'The minimum credible foundation.')}</h2>
      <p class="lede">{v.get('recs_lede', '')}</p>
    </div>
    {recs_html}
    <div class="stack-category">
      <div class="stack-category-head">
        <div class="stack-category-num">{v.get('cull_num', '4.6')}</div>
        <div class="stack-category-title">What we left out — and why</div>
      </div>
      <ul style="margin-top: 14px; padding-left: 20px; font-size: 15px; line-height: 1.7;">{cull_items}</ul>
    </div>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">07 · Stack at a glance</div>
      <h2>{v.get('stack_glance_h2', 'How the tools work together.')}</h2>
    </div>
    {v.get('stack_glance_body', '')}
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">08 · Phased rollout</div>
      <h2>{v.get('phases_h2', 'Twelve weeks, in phases.')}</h2>
      <p class="lede">{v.get('phases_lede', '')}</p>
    </div>
    {phases_html}
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">09 · Cost and investment</div>
      <h2>{v.get('cost_h2', 'What the recommended stack costs.')}</h2>
    </div>
    <h3>Recurring software</h3>
    <table class="qb-table" style="margin-top: 12px;">
      <thead><tr><th>Tool</th><th>Tier</th><th class="right">Monthly cost (AUD)</th></tr></thead>
      <tbody>
        {cost_recurring_html}
        <tr class="subtotal"><td colspan="2">Total recurring</td><td class="right"><em>{v.get('cost_total', '')}</em></td></tr>
      </tbody>
    </table>
    <h3 style="margin-top: 36px;">Where the stack grows once you're ready</h3>
    <table class="qb-table" style="margin-top: 12px;">
      <thead><tr><th>Trigger</th><th>What comes next</th><th class="right">Additional cost</th></tr></thead>
      <tbody>{cost_growth_html}</tbody>
    </table>
    <div style="background: var(--ink); color: var(--parchment); padding: 32px 36px; border-radius: 4px; margin-top: 36px;">
      <h3 style="color: var(--gold); font-size: 22px;">Rogue Night can implement this for you</h3>
      <p style="color: rgba(237, 232, 221, 0.85); margin-top: 12px;">Data migration, account setup, configuration, integrations, process design, scoping. <strong style="color: var(--parchment);">What we don't do:</strong> hands-on team training. We provide written guides and pointers to official video training, plus availability for questions during the first month at no extra cost.</p>
      <p style="color: rgba(237, 232, 221, 0.85); margin-top: 12px;"><strong style="color: var(--gold);">Implementation quote provided on request — book a walkthrough to scope.</strong></p>
    </div>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">10 · Your future digital employees</div>
      <h2>{v.get('employees_h2', 'Three batches, scored on impact and readiness.')}</h2>
      <p class="lede">{v.get('employees_lede', '')}</p>
    </div>
    {employees_html}
    <p style="margin-top: 48px; color: var(--slate); font-style: italic;">{v.get('employees_outro', '')}</p>
    <div style="background: var(--ink); color: var(--parchment); padding: 32px 36px; border-radius: 4px; margin-top: 36px;">
      <h3 style="color: var(--gold); font-size: 22px;">Rogue Night can build and deploy these for you</h3>
      <p style="color: rgba(237, 232, 221, 0.85); margin-top: 12px;">Discovery, build, supervised deployment, handoff, and monitoring. You can engage Batch 01 standalone, see results, then commit to the next batches. <strong style="color: var(--parchment);">What we don't do:</strong> replace your team.</p>
      <p style="color: rgba(237, 232, 221, 0.85); margin-top: 12px;"><strong style="color: var(--gold);">Implementation quote provided per batch — book a walkthrough to scope.</strong></p>
    </div>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">11 · Next steps</div>
      <h2>Three doors.</h2>
    </div>
    <div style="margin-top: 32px;">
      <p class="body-lede" style="font-size: 20px;">01. Feel strongly about something? We'll amend the report.</p>
      <p style="margin-top: 8px;">This report is yours. If something doesn't fit your business — a tool you've already tried, a phase that doesn't make sense, a number that feels off — tell us, and we'll revise. Free of charge. The $880 covers the work, including refinement.</p>
    </div>
    <div style="margin-top: 32px;">
      <p class="body-lede" style="font-size: 20px;">02. Engage Rogue Night for the implementation.</p>
      <p style="margin-top: 8px;">Fixed-fee, fixed-scope. Quote provided after a scoping call. We handle setup, configuration, and integration; you keep the customers, the calls, and the cash.</p>
    </div>
    <div style="margin-top: 32px;">
      <p class="body-lede" style="font-size: 20px;">03. Take the report and run it yourself.</p>
      <p style="margin-top: 8px;">The recommendations are vendor-neutral. The $880 has covered the work.</p>
    </div>
    <p class="meta" style="margin-top: 64px; text-align: center;">Rogue Night PTY LTD · ABN 31 633 650 334 · Australia · Prepared {today}</p>
  </div>
</section>

</body>
</html>
"""
    Path(sys.argv[3]).write_text(HTML)
    size_kb = Path(sys.argv[3]).stat().st_size / 1024
    print(f"HTML written to {sys.argv[3]} — {size_kb:.1f} KB")


if __name__ == "__main__":
    main()

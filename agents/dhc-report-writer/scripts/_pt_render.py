"""Section renderers for populate_template.

Each render_* function takes a small data shape and returns an HTML fragment.
The orchestrator in populate_template.py composes these fragments into the
final document via the template in _pt_template.py.

Naming convention: every public renderer is named `render_*`. The legacy
internal helper `_render_testimonial` is kept as an alias for callers that
imported it from populate_template.
"""


# ---------------------------------------------------------------------------
# Tool card (Section 05 — Recommended stack)
# ---------------------------------------------------------------------------
def render_tool_card(r):
    """Render one tool card matching v5's .tool / .tool-grid / .tier-row markup.

    Supports an optional 'existing' boolean field on the rec object.
    When existing=True the card shows an 'Already in your stack' badge
    and an optional 'existing_note' callout explaining how to unlock value
    from a tool the client already pays for.
    """
    is_existing = r.get("existing", False)
    badge_class = "priority-high" if r["priority"] == "High" else (
        "priority-med" if r["priority"] == "Medium" else "priority-low"
    )
    tiers = r.get("tiers", [{"name": r.get("tier", ""), "price": f"${r.get('cost', 0)}/mo", "recommended": True}])
    # Find the recommended tier for the summary line
    rec_tier = next((t for t in tiers if t.get("recommended")), None)
    rec_summary = (
        f'<div class="tier-summary">Recommended tier: <strong>{rec_tier["name"]}</strong> at <strong>{rec_tier["price"]}</strong></div>'
        if rec_tier and rec_tier.get("name") else ""
    )
    tier_rows = "".join(
        f'<div class="tier-row{" recommended" if t.get("recommended") else ""}">'
        f'<span class="tier-name">{t["name"]}</span>'
        f'<span class="tier-price">{t["price"]}</span></div>'
        for t in tiers
    )
    existing_badge = '<span class="badge existing">Already in your stack</span>' if is_existing else ""
    existing_callout = (
        f'<div class="existing-callout">{r["existing_note"]}</div>'
        if is_existing and r.get("existing_note") else ""
    )
    return f"""
      <div class="tool">
        <div class="tool-top">
          <div>
            <div class="tool-name">{r['name']}</div>
            <div class="tool-subtitle">{r.get('subtitle', '')}</div>
          </div>
          <div class="tool-badges">
            {existing_badge}
            <span class="badge {badge_class}">Priority · {r['priority']}</span>
            <span class="badge when">Goes live: {r['phase']}</span>
          </div>
        </div>
        {existing_callout}
        <div class="tool-grid">
          <div class="tool-rationale">
            <div class="rationale-block">
              <div class="rationale-label">Why this for you</div>
              <div class="rationale-text">{r['why']}</div>
            </div>
            <div class="rationale-block">
              <div class="rationale-label">Why this over the alternatives</div>
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
            {rec_summary}
            <div class="tool-pricing-label">Pricing</div>
            {tier_rows}
            <div class="upgrade-trigger"><strong>Upgrade trigger:</strong> {r.get('upgrade_trigger', '')}</div>
          </div>
        </div>
        {f'<div class="tool-evidence"><em>In practice:</em> {r["evidence"]}</div>' if r.get("evidence") else ""}
      </div>
"""


# ---------------------------------------------------------------------------
# Testimonial block (Section 11 — Next steps)
# ---------------------------------------------------------------------------
def render_testimonial(t, verified: bool = False):
    """Render an optional client testimonial quote block for Section 11.

    Expects a dict: { "quote": "...", "name": "...", "business": "..." }.
    Returns empty string if t is None/falsy.

    **Testimonials must be real.** The template refuses to render the
    testimonial block unless `verified=True` is passed (mapped from
    vars.json `testimonial_verified`). When a testimonial dict is provided
    but verification is False, the function returns a vivid ember-red
    warning ribbon instead of the quote — a forcing function so Lois
    cannot ship a fabricated quote to a client.
    """
    if not t:
        return ""

    if not verified:
        # Vivid warning — fabricated/unverified testimonial guarded
        return (
            '<div style="background: var(--ember); color: #FFE8E8; '
            'padding: 16px 22px; margin: 28px 0 36px 0; border-radius: 2px; '
            'border: 2px solid #FF6B35; font-family: \'Inter\', sans-serif; '
            'font-size: 13px; font-weight: 700; letter-spacing: 0.10em; '
            'text-transform: uppercase; line-height: 1.5;">'
            'Unverified testimonial &mdash; set <code style="background: rgba(0,0,0,0.2); '
            'padding: 1px 6px; border-radius: 2px;">testimonial_verified: true</code> '
            'in vars.json only after confirming this is a real client quote with explicit '
            'permission to publish.</div>'
        )

    return (
        f'<div style="background: var(--cloud); border-left: 3px solid var(--gold); '
        f'border-radius: 0 6px 6px 0; padding: 24px 32px; margin: 28px 0 36px 0;">'
        f'<p style="font-family: \'Source Serif 4\', serif; font-size: 18px; font-style: italic; '
        f'line-height: 1.7; color: var(--ink); margin: 0 0 10px 0;">&ldquo;{t["quote"]}&rdquo;</p>'
        f'<p style="font-family: \'Inter\', sans-serif; font-size: 13px; font-weight: 600; '
        f'color: var(--slate); margin: 0;">{t["name"]}, {t["business"]}</p>'
        f'</div>'
    )


# Legacy alias for backwards compatibility
_render_testimonial = render_testimonial


# ---------------------------------------------------------------------------
# Benefit table row (Section 02 — A week in your business)
# ---------------------------------------------------------------------------
def render_benefit_row(b):
    return f"""
        <tr>
          <td class="change-cell">{b['change']}<span class="sub">{b.get('sub', '')}</span></td>
          <td class="right"><span class="num">{b['hours']}</span> hrs</td>
          <td class="right"><span class="num">{b['dollar']}</span></td>
        </tr>"""


# ---------------------------------------------------------------------------
# Day-in-the-life comparison rows (Section 02)
# ---------------------------------------------------------------------------
def render_dil_rows(day_in_life):
    """Render the day-in-the-life comparison rows. Returns concatenated <tr> HTML
    or empty string if no rows.
    """
    rows_html = ""
    for row in day_in_life or []:
        rows_html += (
            f'<tr>'
            f'<td class="dil-who">{row.get("who", "")}</td>'
            f'<td class="dil-task">{row.get("task", "")}</td>'
            f'<td class="dil-now">{row.get("now", "")}</td>'
            f'<td class="dil-after">{row.get("after", "")}</td>'
            f'</tr>'
        )
    return rows_html


# ---------------------------------------------------------------------------
# Agent card + batch block (Section 07 — Future digital employees)
# ---------------------------------------------------------------------------
def render_agent_card(a):
    """Render one digital employee card with optional pain-match eyebrow,
    readiness line, workflow table, and ties-to quote.
    """
    pain = a.get("pain_match", "")
    tier = a.get("pain_tier", "")
    if pain and tier:
        eyebrow = f'<div class="agent-eyebrow">{pain} · {tier}</div>'
    elif pain:
        eyebrow = f'<div class="agent-eyebrow">{pain}</div>'
    else:
        eyebrow = ""
    readiness = a.get("readiness", "")
    readiness_str = f'<div class="agent-readiness">Readiness: {readiness}</div>' if readiness else ""
    ties = a.get("ties_to", "")
    ties_label = a.get("ties_label", "")
    if ties:
        ties_str = (
            f'<div class="agent-ties">'
            f'Ties to: &ldquo;{ties}&rdquo;{(" &mdash; " + ties_label) if ties_label else ""}</div>'
        )
    else:
        ties_str = ""
    # Workflow table — renders when agent has a "workflow" array
    # Uses the same visual language as the day-in-the-life table (Section 02)
    workflow = a.get("workflow", [])
    if workflow:
        who_labels = {"agent": "Agent", "human": "You", "team": "Your team", "customer": "Customer", "lead": "Lead"}
        wf_rows = "".join(
            f'<tr>'
            f'<td class="wf-tbl-step">{i + 1}</td>'
            f'<td class="wf-tbl-who wf-tbl-who-{step.get("who", "agent")}">{who_labels.get(step.get("who", "agent"), "Agent")}</td>'
            f'<td class="wf-tbl-desc">{step["step"]}</td>'
            f'</tr>'
            for i, step in enumerate(workflow)
        )
        wf_str = (
            f'<div class="agent-workflow">'
            f'<div class="wf-label">How it works — you stay in control</div>'
            f'<table class="wf-table"><thead><tr>'
            f'<th style="width: 40px;">#</th><th style="width: 100px;">Who</th><th>What happens</th>'
            f'</tr></thead><tbody>{wf_rows}</tbody></table>'
            f'</div>'
        )
    else:
        wf_str = ""

    return (
        f'<div class="agent-card">'
        f'{eyebrow}'
        f'<div class="agent-name">{a["name"]}</div>'
        f'<div class="agent-meta">Replaces: {a["replaces"]} &nbsp;·&nbsp; '
        f'Saves ~{a["hours"]} &nbsp;·&nbsp; Worth {a["dollar"]}</div>'
        f'<div class="agent-desc">{a["description"]}</div>'
        f'{readiness_str}'
        f'{wf_str}'
        f'{ties_str}'
        f'</div>'
    )


def render_batch_block(b):
    """Render one batch header followed by its agent cards."""
    agents = "".join(render_agent_card(a) for a in b.get("agents", []))
    return (
        f'<div class="batch-header">'
        f'<div class="batch-subtitle">Batch {b["number"]} · {b["day"]}</div>'
        f'<div class="batch-title">{b["title"]}</div>'
        f'<div class="batch-desc">{b.get("description", "")}</div>'
        f'</div>'
        f'{agents}'
    )


def normalise_batches(v):
    """Back-compat shim: when vars provides a flat `employees` array but no
    `batches`, wrap the employees as Batch 01.
    """
    batches = v.get("batches")
    if not batches and v.get("employees"):
        batches = [{
            "number": "01",
            "day": "Day 90",
            "title": "High impact, ready now.",
            "description": "These agents work with the stack you'll have running by Week 12. Each one pays back in months, not years.",
            "agents": v.get("employees", []),
        }]
    return batches or []


# ---------------------------------------------------------------------------
# Phases (Section 04 — Roadmap)
# ---------------------------------------------------------------------------
def render_phases_html(phases):
    """Render all roadmap phase blocks with their task lists."""
    html = ""
    for p in phases or []:
        tasks_html = "".join(f"<li>{t}</li>" for t in p.get("tasks", []))
        html += f"""
            <div class="phase-heading"><span class="phase-week">{p['week']}</span>{p['headline']}</div>
            <ul style="margin-top: 8px; padding-left: 20px; font-size: 15px; line-height: 1.7; font-family: 'Source Serif 4', Georgia, serif;">
              {tasks_html}
            </ul>"""
    return html


# ---------------------------------------------------------------------------
# Cost tables (Section 08 — Cost and investment)
# ---------------------------------------------------------------------------
def render_cost_recurring_html(rows):
    """Render the recurring cost table body rows."""
    return "".join(
        f'<tr><td>{c["tool"]}</td><td>{c["tier"]}</td><td class="right">{c["cost"]}</td></tr>'
        for c in rows or []
    )


def render_cost_growth_html(rows):
    """Render the cost growth triggers table body rows."""
    return "".join(
        f'<tr><td>{c["trigger"]}</td><td>{c["next"]}</td><td class="right">{c["extra"]}</td></tr>'
        for c in rows or []
    )


# ---------------------------------------------------------------------------
# Cull items (Section 05 — Recommended stack: What we left out)
# ---------------------------------------------------------------------------
def render_cull_items(rows):
    """Render the 'what we left out' list items. Each row is [tool, reason]."""
    return "".join(f"<li><strong>{c[0]}</strong> — {c[1]}</li>" for c in rows or [])


# ---------------------------------------------------------------------------
# Key benefits grid (Section 01 — Executive summary)
# ---------------------------------------------------------------------------
def render_key_benefits(items):
    """Render the executive summary key-benefits grid (numbered cards)."""
    return "".join(
        f'<div class="benefit"><div class="benefit-eyebrow">Key benefit · {i+1:02d}</div>'
        f'<div class="benefit-title">{b["title"]}</div>'
        f'<div class="benefit-body">{b["body"]}</div></div>'
        for i, b in enumerate(items or [])
    )

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

# Workflow avatar illustrations (Style C — editorial spot illustrations, 48×48px PNG base64)
AVATAR_AGENT_B64 = "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"
AVATAR_YOU_B64 = "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"
AVATAR_TEAM_B64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAIAAADYYG7QAAASgUlEQVR42m1ZWZBcZ3U+5//vfm9v092zz2ik0WhkbZaxhLUZyQRjsAkYUpgHqpIKVFGkUslLwkNeUqSoCpVKeEpRKSqhoCqAwY5TgLFxiME2kpFkWWizNFpmpNm3nqV7uu/+///JQ3fPSCK3+qHv7b73nPud/Tv49Nc+BYAABIAAAEDQPiFoHQwREaM0idLENa2hcve+gaHRnsHBjs6il3UMizNEZEqpRhytNmozq5VbizPXZyfvLi/4cWTphm0Yikgp2nwuQlvg5tG8/vTX/njr7IEDAQgBkWGUJqkUQ6Wuj4weOLJzz1Cpy7McAJCklCJFiggQARAZMs6YxjgBNKJgamXp7Pj1d25enaws6lyzDEMREVFbGWoLamtETYVw6xwQN39lDIWUfhyO9gy88MRTJ0b3Zx1PShGniVSKiJrIbd3SvI8AgIiIM2bqBte0euD/9ubVl8+/c2txxjUtjXOlVOuvLaBoU2hboaah7ns0Z6wRhRnL/uLxjz3/+AnXNIM4FkohACIgPKjHlsEJEal93sRDY9yxLD+Ofnrh9H+++6Yfh55pSyW3fGTLWYAPHx99wEwIAMCRbYT+wW3D3/j8l0/ueUyINEgSIOKMNTEB2MQSgYBxJoUAIMY5bUkARMYQgShOE4bs8eHdx0b23l1auFdZcAyr5UuIQEDYMt79CrXgY4gbQfD8oeN//9k/LTiZRhgCAkcGAIgIyFrymighEFESRiKVSkEShaZlk6Km1kjNW1ovGsZhOZP7+P7DG1FwaeqOrRv3i24+/0GEEBDRj8I/P/mJv3rms4kQiRCcM2w6OGOADGBLDgEBQBpFcRT76/ONtSXdyigpdMsiok2ztr4gcsYSIQDh1J7HGOK5iTFD04m2QgoR+Y7jo5tuzBhrROFXnnr2Sx99rh4EAMQYwoMG2vSc5msTqSQWjdWpvF5xuF+t+nqmrGmcMU7QDiiGm5gyxhRBnCRHRvcB0dk7N2zDbP6t+VQGQAQEQJyxmu9/7tCJPzv5yXqjgU2RdF8stMKniX/zElNCSqkYxWuV9aWFVc4lKWqFCNe0WDMbD72V3+9vRYW4UdCkSO7c4IK5cE3H/g3eP3FisVP04MXWN69ry3WtWOhNJZPINKlSO7c4IK5cE3H/g3eP3FisVP04MXWN69ry3WtWOjRIUetaIQZpAmQEWLsb3+u/vlMm+lGxk0p/KDqFEKNJvRSKca+LIfmSBBHKoYUGlhqsVE0dN3gShKoXJXCVVN5f+zb5+b+/eI5XVU4Y7EUp4YPxBnGOJdKzK9Orywvnbp2+eTAYZu1FNFxnYbfUPuBpw70dW5dqFepSwRfDhiupvJRE5L65HWxmGGz/V2JCfp3zyPIRHBwcfh+v334VJv7h8ZnWHJKsCGt0HN0T8g5J9pKJGPbdNp7Y9C1K1i9EMXEzHh8YFiL5ZqO78r6oLKf1FYCJLLuqlK+Fk3FU0pJdMfD0FNSI8MAQnKyOuGqmpqCZKFOsRCJCGMIIlQ5r5hXLQsKWQYhLquh0GI2Hgex6xW7U8FhslmVSmHYawZe+P6jGN3kPJEO74IKUWA4HtONp3Xq4k1bJ4pRSx+2M99qWa7vqdbemGWZeIBEqI8elcFwbJllZqJUyXFSnZCBUGSE+0YMN2y3W8bSceJ5OVa3bZUFSCNJJIkW/nALj3wkbSs0ulkh+KyGLjGkNQJKN0a3M3tXbnFV03NI0x5rieYeqcc8cLGm4riMh1fMMw4paZsv1USjcNzXECxjQhRMxUKivLcRLqvKNHIz0L6qD5PmKxjIj/43//VyGbA4W6ycW1lnacNjnZjEZEDAULIQ8MV1bvLCdxy0t8x9UOcjHG0EAp7bj20IGOI3s3cJKxIcb5+FGLprN61I+b4fRp03GhMBAO4Z8dqePVP9v7YGM5y1BbcjcGfebz93s3qNaYz37yHkiiGK/EfmOFyAQEDmtJkqT0nfDNPR0yzHM+h9+NJpQAAiB3TMkgJAREBAyVkKcOHPFLUbzA23fQIiLJm6ZHdMeqWNd9bFh0R/AjqOyTjWzduJ3uxRBLKc0t2HJ2RkHbZIhIkCLleFpSC7wOVWs31prmU7mtm+bJ4Z7cUjVMAxoSlKqb6VExIxopEYjIQ0t2P3K+cOVkEFqmMlEsJUmj4yXR3N5VIkUn9IDKVHDSRKn+3r2Lk4urE2qoMmR9xojh0EsG/FiilwIFxn1X2pXaObzx+YBJBEkGgAD0SOdZYrcoKYMR5RmJL+VKg94fCaW7InTRJGKk0TjHJCFcRwHoSRAuqkCYH9v+dCJZ4Wsl7Qy19ixTX+4OKv/1VdXaJjh8KA0lI6C5v/nZn/2HhVxXaHDSbJekRISlWxhNO0n9dqz6hxzjcxB6gcKr9oKdaTK1kcgmqJJHRYqUyWZf1Qp7xbJBSgMC6YqVIIhIZ8qMY1Gb3p0vWkIp7sIgQhRYSuqK/52Gy1uVpM6T/QNdq2IenqyIQvicl2MjktWVxYfB8G7G4zhDNdjgicMCNp6S5zy0F8JlvY3MK/kM2H4wPgd+0/Oy+29bnp+6xqNNuN5H4ABpzd+xI5c5J9uSNTM13a6k80m3Z/pO8bNbqy/r5aVVAK2tzVdqXr3u/vaHv3H7jU9qpotJ0LTnFigBAKDGS3vTVR8gvYi9lj5U6JQnNRmqSSw9kT54UmzalFKtKEm9cjI3q/vDq2L+R2hpCJhI4FaqfR2pWP5BtRqaUfVLpR76sSJm7aRNiw0LoGiJfSKfhQJCsNQ/x3WROeIFn0CKCBJRQ+cQfVhk2xJ+3dOjk8Oqzv7vSWVh0yYm+2t/Ly8qvP7zt5G5w3V8uCW5OYBGjLMFJr8kfBtjOMz1NqsVhf3Y/sA4uNdG7JEHDKVHCZiRDJIKuXt0uc9mSlq3rjBIk8ZLAQW2hOh2EVlffUMOb4tqq6lhJNTJMpBDN6FvsBxYqnf2JVi2W+4Gxb/3HhwnmIkwTOQ+IZVkCElC24H2C0gxcfSoZqKA9RL5oeRCF69Y1fWVnTWzX8k8v/wfRUGJHCh5Lh3+4gRo84NiO3oC6Xg+VHKk3F7KlqIIJO9gCgGLdDHoFb2WxOE9N29dqb+w60ksU4sTBTKBbK5KaEkGVn2A1Vcp7IZ5IRLlGpZ4oOiQlRw/d3c/7Q6NjA4Gvut7i7NLLFz1nEsC5bJFw4qB4ZEwmgC5ubmxKevYM++f0pA8lzjmF8fDpMxDjPB3E6ydW2lUmjIKXRt8P7i8OBXIOvGXLfaRRX3dkP5kcAYApNfKdPk3Tp1ZhMrNnSwN7RYwR9d2Tf5cUbzK8utRYQFbK5bEcv06TcsPYITHBD+sVkT2eFu+Ou7OzCw38EBHREuX+3t75aRg7nAVhMMOw1H9Mb4+Ng/M+X/20fTYKuTQcxSZUPpGqlPThfO3FlSHM2kl3vF8KT2x5x9uZXzU71/d8+Hx4+WC/2uYzmOaxV1ICRCCaanrFz/h1efP+8FWNbFLAQZqSIEkFRFVR3N2KDa/4VUvw1mEYekHlxr6eeAyGxLBNRFpcJsZ5MKmGYdpSn7sGi3Gv7Cqv5P9OW+YdaFcY3LOy7LnfFzA8PGpqQSTYuJCJSECghPDe5fOY/Tj9+sJWxSSqRhN4f3FueuKMoqq5g1t2bPjFJCJBJmqBQ3j/khnE50LqS5XMupO+FUq1cLi3D5vdJXaHv7eKH2kxSTGdpzzw9U1SVJJ4jhlq/fXCqUy59dcfVnv5w37AQAE1Jyg8/fmLlRmbw3N3dsZE+38+CsAf9JqpWaVzTN3O3+mXsj08rjBp6+YkL0VjvbcaKm7IJ9u/90Oeg18Pw2RTd8RL1KvtbhJaX8OGGYJjdJLnAJx3sVQdqYVBJuxPEd01CJ6h1A0i30k+tg3slwujJPcbgk5UrCm+8e9c3l+6mIvIjFEGLSqO9HyRhYGp8fXm1b99RK+w60bZ0g2DKv4TIf+7avYBrB/UmMhbJJJGiZT6U2kY5E2H1UMhU0dCODJMpBDN6FvsBxYqnf2JVi2W+4Gxb/3HhwnmIkwTOQ+IZVkCElC24H2C0gxcfSoZqKA9RL5oeRCF69Y1fWVnTWzX8k8v/wfRUGJHCh5Lh3+4gRo84NiO3oC6Xg+VHKk3F7KlqIIJO9gCgGLdDHoFb2WxOE9N29dqb+w60ksU4sTBTKBbK5KaEkGVn2A1Vcp7IZ5IRLlGpZ4oOiQlRw/d3c/7Q6NjA4Gvut7i7NLLFz1nEsC5bJFw4qB4ZEwmgC5ubmxKevYM++f0pA8lzjmF8fDpMxDjPB3E6ydW2lUmjIKXRt8P7i8OBXIOvGXLfaRRX3dkP5kcAYApNfKdPk3Tp1ZhMrNnSwN7RYwR9d2Tf5cUbzK8utRYQFbK5bEcv06TcsPYITHBD+sVkT2eFu+Ou7OzCw38EBHREuX+3t75aRg7nAVhMMOw1H9Mb4+Ng/M+X/20fTYKuTQcxSZUPpGqlPThfO3FlSHM2kl3vF8KT2x5x9uZXzU71/d8+Hx4+WC/2uYzmOaxV1ICRCCaanrFz/h1efP+8FWNbFLAQZqSIEkFRFVR3N2KDa/4VUvw1mEYekHlxr6eeAyGxLBNRFpcJsZ5MKmGYdpSn7sGi3Gv7Cqv5P9OW+YdaFcY3LOy7LnfFzA8PGpqQSTYuJCJSECghPDe5fOY/Tj9+sJWxSSqRhN4f3FueuKMoqq5g1t2bPjFJCJBJmqBQ3j/khnE50LqS5XMupO+FUq1cLi3D5vdJXaHv7eKH2kxSTGdpzzw9U1SVJJ4jhlq/fXCqUy59dcfVnv5w37AQAE1Jyg8/fmLlRmbw3N3dsZE+38+CsAf9JqpWaVzTN3O3+mXsj08rjBp6+YkL0VjvbcaKm7IJ9u/90Oeg18Pw2RTd8RL1KvtbhJaX8OGGYJjdJLnAJx3sVQdqYVBJuxPEd01CJ6h1A0i30k+tg3slwujJPcbgk5UrCm+8e9c3l+6mIvIjFEGLSqO9HyRhYGp8fXm1b99RK+w60bZ0g2DKv4TIf+7avYBrB/UmMhbJJJGiZT6U2kY5E2H1UMhU0dCODJMpBDN6FvsBxYqnf2JVi2W+4Gxb/3HhwnmIkwTOQ+IZVkCElC24H2C0gxcfSoZqKA9RL5oeRCF69Y1fWVnTWzX8k8v/wfRUGJHCh5Lh3+4gRo84NiO3oC6Xg+VHKk3F7KlqIIJO9gCgGLdDHoFb2WxOE9N29dqb+w60ksU4sTBTKBbK5KaE="


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
        # Workflow step-flow strip — renders when agent has a "workflow" array
        workflow = a.get("workflow", [])
        if workflow:
            wf_items = []
            for i, step in enumerate(workflow):
                who = step.get("who", "agent")
                if who == "agent":
                    avatar_b64 = AVATAR_AGENT_B64
                    avatar_class = "agent"
                elif who == "team":
                    avatar_b64 = AVATAR_TEAM_B64
                    avatar_class = "team"
                else:
                    avatar_b64 = AVATAR_YOU_B64
                    avatar_class = "human"
                wf_items.append(
                    f'<div class="wf-step">'
                    f'<img class="wf-avatar {avatar_class}" src="data:image/png;base64,{avatar_b64}" alt="{who}" />'
                    f'{step["step"]}'
                    f'</div>'
                )
                if i < len(workflow) - 1:
                    wf_items.append('<span class="wf-arrow">→</span>')
            wf_str = (
                f'<div class="agent-workflow">'
                f'<div class="wf-label">How it works — you stay in control</div>'
                f'<div class="wf-steps">{"".join(wf_items)}</div>'
                f'<div class="wf-legend">'
                f'<span class="wf-legend-item"><img class="wf-avatar-sm agent" src="data:image/png;base64,{AVATAR_AGENT_B64}" alt="agent" /> Agent</span>'
                f'<span class="wf-legend-item"><img class="wf-avatar-sm human" src="data:image/png;base64,{AVATAR_YOU_B64}" alt="you" /> You</span>'
                f'<span class="wf-legend-item"><img class="wf-avatar-sm team" src="data:image/png;base64,{AVATAR_TEAM_B64}" alt="team" /> Your team</span>'
                f'</div>'
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

    def _batch_block(b):
        agents = "".join(_agent_card(a) for a in b.get("agents", []))
        return (
            f'<div class="batch-header">'
            f'<div class="batch-subtitle">Batch {b["number"]} · {b["day"]}</div>'
            f'<div class="batch-title">{b["title"]}</div>'
            f'<div class="batch-desc">{b.get("description", "")}</div>'
            f'</div>'
            f'{agents}'
        )

    employees_html = "".join(_batch_block(b) for b in batches)
    phases_html = ""
    for p in v.get("phases", []):
        tasks_html = "".join(f"<li>{t}</li>" for t in p.get("tasks", []))
        phases_html += f"""
            <div class="phase-heading"><span class="phase-week">{p['week']}</span>{p['headline']}</div>
            <ul style="margin-top: 8px; padding-left: 20px; font-size: 15px; line-height: 1.7; font-family: 'Source Serif 4', Georgia, serif;">
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

    HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI & Automation Strategy — {client}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;1,8..60,400;1,8..60,500&display=swap" rel="stylesheet">
{style}
<style>
  .cover-logo {{ height: 56px; width: auto; }}

  /* ---------- Page breaks: every section starts on a new page ---------- */
  section.block {{
    page-break-before: always;
  }}

  /* ---------- Phase headings (Section 06) ---------- */
  .phase-heading {{
    margin-top: 40px;
    padding: 16px 20px;
    background: rgba(201, 169, 97, 0.08);
    border-left: 3px solid var(--gold);
    border-radius: 0 4px 4px 0;
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 22px;
    font-weight: 400;
    color: var(--ink);
    letter-spacing: -0.01em;
  }}
  .phase-heading .phase-week {{
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--gold);
    display: block;
    margin-bottom: 4px;
  }}

  /* ---------- Batch headers (Section 08) ---------- */
  .batch-header {{
    margin-top: 48px;
    padding: 20px 24px;
    background: rgba(201, 169, 97, 0.22);
    border-left: 3px solid var(--gold);
    border-radius: 0 6px 6px 0;
    color: var(--ink);
  }}
  .batch-header:first-of-type {{ margin-top: 24px; }}
  .batch-header .batch-title {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 24px;
    color: var(--gold);
    margin-bottom: 4px;
  }}
  .batch-header .batch-subtitle {{
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--gold);
  }}
  .batch-header .batch-desc {{
    font-size: 15px;
    color: var(--slate);
    margin-top: 10px;
    line-height: 1.65;
    font-style: italic;
  }}

  /* ---------- Agent cards (Section 08) ---------- */
  .agent-card {{
    margin-top: 20px;
    padding: 24px 28px;
    background: rgba(201, 169, 97, 0.06);
    border: 1px solid var(--gold-line);
    border-left: 3px solid var(--gold);
    border-radius: 0 6px 6px 0;
  }}
  .agent-card .agent-eyebrow {{
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 6px;
  }}
  .agent-card .agent-name {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 22px;
    color: var(--ink);
    margin-bottom: 8px;
  }}
  .agent-card .agent-meta {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--slate);
    margin-bottom: 12px;
    line-height: 1.6;
  }}
  .agent-card .agent-desc {{
    font-size: 15px;
    line-height: 1.7;
    color: var(--ink);
  }}
  .agent-card .agent-readiness {{
    font-size: 13px;
    color: var(--slate);
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid var(--rule);
  }}
  .agent-card .agent-ties {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-style: italic;
    font-size: 14px;
    color: var(--slate);
    margin-top: 12px;
    padding-left: 16px;
    border-left: 2px solid var(--gold-line);
  }}

  /* ---------- Workflow step-flow strip (Section 08 agent cards) ---------- */
  .agent-workflow {{
    margin-top: 16px;
    padding-top: 14px;
    border-top: 1px solid var(--rule);
  }}
  .agent-workflow .wf-label {{
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 10px;
  }}
  .agent-workflow .wf-steps {{
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0;
  }}
  .agent-workflow .wf-step {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    line-height: 1.5;
    color: var(--ink);
    padding: 6px 0;
  }}
  .agent-workflow .wf-avatar {{
    width: 24px;
    height: 24px;
    border-radius: 50%;
    flex-shrink: 0;
    object-fit: cover;
  }}
  .agent-workflow .wf-avatar.agent {{
    box-shadow: 0 0 0 1.5px var(--gold);
  }}
  .agent-workflow .wf-avatar.human {{
    box-shadow: 0 0 0 1.5px var(--ink);
  }}
  .agent-workflow .wf-avatar.team {{
    box-shadow: 0 0 0 1.5px var(--ink);
  }}
  .agent-workflow .wf-arrow {{
    color: var(--slate);
    font-size: 14px;
    margin: 0 6px;
    flex-shrink: 0;
  }}
  .agent-workflow .wf-legend {{
    display: flex;
    gap: 16px;
    margin-top: 8px;
    font-size: 11px;
    color: var(--slate);
  }}
  .agent-workflow .wf-legend-item {{
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .agent-workflow .wf-avatar-sm {{
    width: 16px;
    height: 16px;
    border-radius: 50%;
    object-fit: cover;
  }}
  .agent-workflow .wf-avatar-sm.agent {{
    box-shadow: 0 0 0 1px var(--gold);
  }}
  .agent-workflow .wf-avatar-sm.human {{
    box-shadow: 0 0 0 1px var(--ink);
  }}
  .agent-workflow .wf-avatar-sm.team {{
    box-shadow: 0 0 0 1px var(--ink);
  }}

  /* ---------- Security section assurance cards ---------- */
  .assurance-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 28px;
  }}
  .assurance-card {{
    padding: 20px 24px;
    background: rgba(201, 169, 97, 0.06);
    border: 1px solid var(--gold-line);
    border-left: 3px solid var(--gold);
    border-radius: 0 6px 6px 0;
  }}
  .assurance-card .ac-icon {{
    font-size: 22px;
    margin-bottom: 8px;
  }}
  .assurance-card .ac-title {{
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: var(--ink);
    margin-bottom: 6px;
  }}
  .assurance-card .ac-body {{
    font-size: 14px;
    line-height: 1.65;
    color: var(--slate);
  }}
  @media print {{
    .assurance-grid {{
      grid-template-columns: 1fr;
    }}
  }}

  /* ---------- Tool card: recommended tier summary ---------- */
  .tier-summary {{
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: var(--ink);
    padding: 10px 0 12px;
    border-bottom: 1px solid var(--rule);
    margin-bottom: 12px;
  }}

  /* ---------- Tool card: evidence / case study callout ---------- */
  .tool-evidence {{
    margin-top: 16px;
    padding: 14px 20px;
    background: rgba(201, 169, 97, 0.06);
    border-left: 2px solid var(--gold-line);
    border-radius: 0 4px 4px 0;
    font-size: 14px;
    line-height: 1.65;
    color: var(--slate);
    font-style: italic;
  }}
  .tool-evidence em {{
    font-style: normal;
    font-weight: 600;
    color: var(--gold);
    margin-right: 4px;
  }}

  /* ---------- "What we left out" starts on own page ---------- */
  .stack-category {{
    page-break-before: always;
  }}

  /* ---------- Section headings: h3 inside .page (cost, growth tables) ---------- */
  .page > h3 {{
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: 20px;
    color: var(--ink);
    margin-top: 36px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--rule);
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
      <h2>{v.get('exec_summary_h2', 'Where you are. Where this report takes you.')}</h2>
    </div>
    {f'<p class="body-lede">{exec_summary_lede}</p>' if exec_summary_lede else ''}
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
      <div class="number">02 · Quantified benefits</div>
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
      <div class="number">03 · Current state</div>
      <h2>The snapshot. Verbatim from your questionnaire.</h2>
    </div>
    <div class="snapshot">
      <div class="snapshot-row"><div class="snapshot-label">Industry</div><div class="snapshot-value">{industry}</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Headcount</div><div class="snapshot-value">{headcount}</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Years operating</div><div class="snapshot-value">{years}</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Customers per week</div><div class="snapshot-value">~{cpw}</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Stated goal</div><div class="snapshot-value" style="font-style: italic;">"{goal}"</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Pain narrative</div><div class="snapshot-value" style="font-style: italic;">"{pain_narr}"</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Hated weekly task</div><div class="snapshot-value" style="font-style: italic;">"{hated}"</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Future state vision</div><div class="snapshot-value" style="font-style: italic;">"{future}"</div></div>
      <div class="snapshot-row"><div class="snapshot-label">Tech comfort</div><div class="snapshot-value">{tech}</div></div>
      <div class="snapshot-row"><div class="snapshot-label">AI readiness</div><div class="snapshot-value">{ai_appetite}</div></div>
    </div>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">04 · Recommended stack</div>
      <h2>{v.get('recs_h2', 'The minimum credible foundation.')}</h2>
      <p class="lede">{v.get('recs_lede', '')}</p>
    </div>
    {recs_html}
    <div class="stack-category">
      <div class="stack-category-head">
        <div class="stack-category-num">{v.get('cull_num', '4.6')}</div>
        <div class="stack-category-title">What we left out — and why</div>
      </div>
      <ul style="margin-top: 14px; padding-left: 20px; font-size: 15px; line-height: 1.7; font-family: 'Source Serif 4', Georgia, serif;">{cull_items}</ul>
    </div>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">05 · Stack at a glance</div>
      <h2>{v.get('stack_glance_h2', 'How the tools work together.')}</h2>
    </div>
    {v.get('stack_glance_body', '')}
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">06 · Phased rollout</div>
      <h2>{v.get('phases_h2', 'Twelve weeks, in phases.')}</h2>
      <p class="lede">{v.get('phases_lede', '')}</p>
    </div>
    {phases_html}
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">07 · Cost and investment</div>
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
      <div class="number">08 · Your future digital employees</div>
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
      <div class="number">09 · Security and reliability</div>
      <h2>{v.get('security_h2', 'Your data. Your control. Our commitment.')}</h2>
      <p class="lede">{v.get('security_lede', 'Every tool we recommend is a reputable, Australian-accessible SaaS platform. Here is how your data stays safe — and what happens if something breaks.')}</p>
    </div>
    <div class="assurance-grid">
      <div class="assurance-card">
        <div class="ac-title">Where your data lives</div>
        <div class="ac-body">{v.get('security_data_residency', 'Each tool stores your data on its own secure servers — most with Australian or Asia-Pacific data centres. Nothing is stored on Rogue Night infrastructure. You own every account and every login.')}</div>
      </div>
      <div class="assurance-card">
        <div class="ac-title">AI and your privacy</div>
        <div class="ac-body">{v.get('security_ai_privacy', 'Digital employees use the OpenAI API, which does not use your data to train its models. Your invoices, emails, and customer records stay private — they are processed and forgotten, not learned from.')}</div>
      </div>
      <div class="assurance-card">
        <div class="ac-title">Access and control</div>
        <div class="ac-body">{v.get('security_access_control', 'Every digital employee only accesses what you grant it. Read access to Gmail does not mean it can send emails on your behalf. Read access to your accounting tool does not mean it can authorise payments. You set the boundaries.')}</div>
      </div>
      <div class="assurance-card">
        <div class="ac-title">You approve before it acts</div>
        <div class="ac-body">{v.get('security_human_loop', 'Every digital employee in this report is designed with a human approval step. Nothing gets sent to a customer, posted to your accounts, or committed to your calendar without someone on your team reviewing and approving it first.')}</div>
      </div>
      <div class="assurance-card">
        <div class="ac-title">What Rogue Night sees</div>
        <div class="ac-body">{v.get('security_rn_access', 'During the first 90 days after deployment, we monitor agent logs and error rates to catch issues early. After handoff, we have no standing access to your accounts unless you grant it for a specific support request.')}</div>
      </div>
      <div class="assurance-card">
        <div class="ac-title">What happens if something breaks</div>
        <div class="ac-body">{v.get('security_support', 'The tools in this report are maintained by their vendors — updates, security patches, and uptime are their responsibility. If an integration breaks or an agent misbehaves, reach out to us. First 90 days of monitoring are included with implementation. After that, we are a call away — diagnosis and fixes quoted per incident.')}</div>
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">10 · Next steps</div>
      <h2>Where to from here.</h2>
    </div>
    <div style="display: grid; grid-template-columns: 1fr; gap: 20px; margin-top: 32px;">
      <div style="background: rgba(201, 169, 97, 0.06); border: 1px solid var(--gold-line); border-left: 3px solid var(--gold); border-radius: 0 6px 6px 0; padding: 28px 32px;">
        <div style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--gold); margin-bottom: 8px;">Option 01 · Refine</div>
        <p class="body-lede" style="font-size: 19px; margin-bottom: 10px;">Feel strongly about something? We'll amend the report.</p>
        <p style="font-size: 15px; line-height: 1.7;">This report is yours. If something doesn't fit your business — a tool you've already tried, a phase that doesn't make sense, a number that feels off — tell us, and we'll revise. Free of charge. The $880 covers the work, including refinement.</p>
      </div>
      <div style="background: rgba(201, 169, 97, 0.06); border: 1px solid var(--gold-line); border-left: 3px solid var(--gold); border-radius: 0 6px 6px 0; padding: 28px 32px;">
        <div style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--gold); margin-bottom: 8px;">Option 02 · Implement</div>
        <p class="body-lede" style="font-size: 19px; margin-bottom: 10px;">Engage Rogue Night for the implementation.</p>
        <p style="font-size: 15px; line-height: 1.7;">Fixed-fee, fixed-scope. Quote provided after a scoping call. We handle setup, configuration, and integration; you keep the customers, the calls, and the cash.</p>
      </div>
      <div style="background: rgba(201, 169, 97, 0.06); border: 1px solid var(--gold-line); border-left: 3px solid var(--gold); border-radius: 0 6px 6px 0; padding: 28px 32px;">
        <div style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--gold); margin-bottom: 8px;">Option 03 · Self-serve</div>
        <p class="body-lede" style="font-size: 19px; margin-bottom: 10px;">Take the report and run it yourself.</p>
        <p style="font-size: 15px; line-height: 1.7;">The recommendations are vendor-neutral. The $880 has covered the work.</p>
      </div>
    </div>
    <div style="border-top: 1px solid var(--rule-strong); padding-top: 24px; text-align: center; margin-top: 64px;">
      <p class="meta" style="margin-bottom: 0;">Rogue Night PTY LTD · ABN 31 633 650 334 · Australia · Prepared {today}</p>
    </div>
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

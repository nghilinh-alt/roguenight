"""HTML template for the AI & Automation Strategy report.

`render_report_html(ctx)` accepts a SimpleNamespace of context values
(see populate_template.main for the full list) and returns the complete
HTML document — cover + 10 sections.

CSS lives in two files loaded at runtime by _pt_assets:
- v5-style-block.txt: brand-locked v5 styling (typography, colors, layout)
- extra-styles.css: report-specific styling (phase headings, batch cards,
  agent cards, workflow tables, day-in-the-life table, security cards)

Both are injected verbatim into the <head> via {ctx.style} and
{ctx.extra_styles}; no f-string interpolation inside the CSS itself.
"""


def render_report_html(ctx) -> str:
    """Render the full report HTML.

    ctx is a SimpleNamespace with attributes covering every interpolation
    point in the template. See populate_template.main for the list.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI & Automation Strategy — {ctx.client}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;1,8..60,400;1,8..60,500&display=swap" rel="stylesheet">
{ctx.style}
<style>
{ctx.extra_styles}
</style>
</head>
<body>

<section class="cover">
  <div class="cover-inner">
    <div class="cover-top">
      <img class="cover-logo" src="data:image/png;base64,{ctx.logo_b64}" alt="Rogue Night">
      <div class="client-logo-slot">{ctx.client_logo_html}</div>
    </div>
    <div class="cover-title-block">
      <div class="cover-eyebrow">AI & Automation Strategy · Specially curated</div>
      <h1 class="cover-title">{ctx.cover_title}<br><span class="accent">{ctx.cover_accent}</span></h1>
      <p class="cover-subtitle">{ctx.cover_subtitle}</p>
    </div>
    <div class="cover-bottom">
      <div class="cover-meta-block">
        <div class="cover-meta-label">Prepared for</div>
        <div class="cover-meta-value">{ctx.client}</div>
      </div>
      <div class="cover-meta-block">
        <div class="cover-meta-label">Delivered</div>
        <div class="cover-meta-value">{ctx.today}</div>
      </div>
      <div class="cover-meta-block">
        <div class="cover-meta-label">Reference</div>
        <div class="cover-meta-value">{ctx.ref}</div>
      </div>
    </div>
  </div>
</section>

<!-- 01 · Executive summary -->
<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">01 · Executive summary</div>
      <h2>{ctx.v.get('exec_summary_h2', 'Where you are. Where this report takes you.')}</h2>
    </div>
    {f'<p class="body-lede">{ctx.exec_summary_lede}</p>' if ctx.exec_summary_lede else ''}
    {ctx.v.get('exec_summary_para_2', '')}
    {ctx.v.get('exec_summary_para_3', '')}
    <div class="benefits" style="margin-top: 36px;">
      {ctx.key_benefits_html}
    </div>
  </div>
</section>

<!-- 02 · A week in your business (NEW — day-in-the-life + folded quantified benefits) -->
<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">02 · A week in your business</div>
      <h2>{ctx.v.get('dil_h2', 'Now versus after. The difference in your week.')}</h2>
      <p class="lede">{ctx.v.get('dil_lede', '')}</p>
    </div>
    {'<table class="dil-table"><thead><tr><th>Who</th><th>Task</th><th>Now</th><th>After</th></tr></thead><tbody>' + ctx.dil_rows_html + '</tbody></table>' if ctx.dil_rows_html else ''}
    <h3 style="margin-top: 48px;">{ctx.v.get('q_benefits_h2', 'What each move is worth, in hours and dollars.')}</h3>
    <p class="lede" style="margin-top: 8px; margin-bottom: 16px;">{ctx.v.get('q_benefits_lede', '')}</p>
    <table class="qb-table">
      <thead>
        <tr><th>The change</th><th class="right">Hours saved</th><th class="right">Dollar value</th></tr>
      </thead>
      <tbody>
        {ctx.benefits_html}
        <tr class="subtotal"><td>Total monthly impact</td><td class="right"><span class="num" style="font-style: italic;">{ctx.v.get('benefits_subtotal_hrs', '')}</span> hrs</td><td class="right"><em>{ctx.v.get('benefits_subtotal_dollar', '')}</em></td></tr>
      </tbody>
    </table>
    <p class="meta" style="margin-top: 24px;">{ctx.v.get('benefits_basis_note', '')}</p>
  </div>
</section>

<!-- 03 · Current state -->
<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">03 · Current state</div>
      <h2>Where you are today. In your own words.</h2>
    </div>
    <div class="snapshot-v3">
      <div class="snapshot-facts">
        <h3>At a glance</h3>
        <div class="fact"><div class="fact-label">Industry</div><div class="fact-value">{ctx.industry}</div></div>
        <div class="fact"><div class="fact-label">Headcount</div><div class="fact-value">{ctx.headcount}</div></div>
        <div class="fact"><div class="fact-label">Years operating</div><div class="fact-value">{ctx.years}</div></div>
        <div class="fact"><div class="fact-label">Customers per week</div><div class="fact-value">~{ctx.cpw}</div></div>
        <div class="fact"><div class="fact-label">Tech comfort</div><div class="fact-value">{ctx.tech}</div></div>
        <div class="fact"><div class="fact-label">AI readiness</div><div class="fact-value">{ctx.ai_appetite}</div></div>
      </div>
      <div class="snapshot-voice">
        <h3>In your words</h3>
        <blockquote class="voice"><span class="voice-label">Stated goal</span><p>&ldquo;{ctx.goal}&rdquo;</p></blockquote>
        <blockquote class="voice"><span class="voice-label">Pain narrative</span><p>&ldquo;{ctx.pain_narr}&rdquo;</p></blockquote>
        <blockquote class="voice"><span class="voice-label">Hated weekly task</span><p>&ldquo;{ctx.hated}&rdquo;</p></blockquote>
        <blockquote class="voice"><span class="voice-label">Future state vision</span><p>&ldquo;{ctx.future}&rdquo;</p></blockquote>
      </div>
    </div>
  </div>
</section>

<!-- 04 · The roadmap (was 06 · Phased rollout) -->
<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">04 · The roadmap</div>
      <h2>{ctx.v.get('phases_h2', 'Twelve weeks, in phases.')}</h2>
      <p class="lede">{ctx.v.get('phases_lede', '')}</p>
    </div>
    {ctx.phases_html}
  </div>
</section>

<!-- 05 · Recommended stack (was 04) -->
<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">05 · Recommended stack</div>
      <h2>{ctx.v.get('recs_h2', 'The minimum credible foundation.')}</h2>
      <p class="lede">{ctx.v.get('recs_lede', '')}</p>
    </div>
    {ctx.recs_html}
  </div>
</section>

<!-- 06 · What we left out — and why (PROMOTED from 5.6 in v6.5) -->
<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">06 · What we left out — and why</div>
      <h2>{ctx.v.get("cull_h2", "The recommendations you won&rsquo;t pay for, and the reasoning.")}</h2>
      <p class="lede">{ctx.v.get("cull_lede", "Half the value of this report is what we&rsquo;re not recommending. Each line below is a category, brand, or product we considered and chose not to put on your stack.")}</p>
    </div>
    <ul class="cull-list">{ctx.cull_items}</ul>
  </div>
</section>

<!-- 07 · Stack at a glance (was 06) -->
<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">07 · Stack at a glance</div>
      <h2>{ctx.v.get('stack_glance_h2', 'How the tools work together.')}</h2>
    </div>
    {ctx.v.get('stack_glance_body', '')}
  </div>
</section>

<!-- 08 · Your future digital employees -->
<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">08 · Your future digital employees</div>
      <h2>{ctx.v.get('employees_h2', 'Three batches, scored on impact and readiness.')}</h2>
      <p class="lede">{ctx.v.get('employees_lede', '')}</p>
    </div>
    {ctx.employees_html}
    <p style="margin-top: 48px; color: var(--slate); font-style: italic;">{ctx.v.get('employees_outro', '')}</p>
  </div>
</section>

<!-- 09 · Cost and investment -->
<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">09 · Cost and investment</div>
      <h2>{ctx.v.get('cost_h2', 'What the recommended stack costs.')}</h2>
    </div>
    <h3>Recurring software</h3>
    <table class="qb-table" style="margin-top: 12px;">
      <thead><tr><th>Tool</th><th>Tier</th><th class="right">Monthly cost (AUD)</th></tr></thead>
      <tbody>
        {ctx.cost_recurring_html}
        <tr class="subtotal"><td colspan="2">Total recurring</td><td class="right"><em>{ctx.v.get('cost_total', '')}</em></td></tr>
      </tbody>
    </table>
    <h3 style="margin-top: 36px;">Where the stack grows once you're ready</h3>
    <table class="qb-table" style="margin-top: 12px;">
      <thead><tr><th>Trigger</th><th>What comes next</th><th class="right">Additional cost</th></tr></thead>
      <tbody>{ctx.cost_growth_html}</tbody>
    </table>
    <div class="rn-build-block" style="background: var(--ink); color: var(--parchment); padding: 32px 36px; border-radius: 4px; margin-top: 36px;">
      <h3 style="color: var(--gold); font-size: 22px; margin: 0;">Rogue Night builds and deploys all of this for you.</h3>
      <p style="color: rgba(237, 232, 221, 0.88); margin-top: 12px; line-height: 1.6;">The recommended tools, the integrations, the digital employees — implementation end to end. Discovery, build, supervised deployment, handoff. <strong style="color: var(--gold);">Quote provided on request — book a walkthrough to scope.</strong></p>
    </div>
    <p style="font-size: 13px; color: var(--slate); margin-top: 14px; font-style: italic; line-height: 1.55;">We don't replace your team or run hands-on training. Written guides and pointers to official video training are included, plus availability for questions during the first month at no extra cost.</p>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">10 · Security and reliability</div>
      <h2>{ctx.v.get('security_h2', 'Your data. Your control. Our commitment.')}</h2>
      <p class="lede">{ctx.v.get('security_lede', 'Every tool we recommend is a reputable, Australian-accessible SaaS platform. Here is how your data stays safe — and what happens if something breaks.')}</p>
    </div>
    <div class="assurance-grid">
      <div class="assurance-card">
        <div class="ac-title">Where your data lives</div>
        <div class="ac-body">{ctx.v.get('security_data_residency', 'Each tool stores your data on its own secure servers — most with Australian or Asia-Pacific data centres. Nothing is stored on Rogue Night infrastructure. You own every account and every login.')}</div>
      </div>
      <div class="assurance-card">
        <div class="ac-title">AI and your privacy</div>
        <div class="ac-body">{ctx.v.get('security_ai_privacy', 'Digital employees use the OpenAI API, which does not use your data to train its models. Your invoices, emails, and customer records stay private — they are processed and forgotten, not learned from.')}</div>
      </div>
      <div class="assurance-card">
        <div class="ac-title">Access and control</div>
        <div class="ac-body">{ctx.v.get('security_access_control', 'Every digital employee only accesses what you grant it. Read access to Gmail does not mean it can send emails on your behalf. Read access to your accounting tool does not mean it can authorise payments. You set the boundaries.')}</div>
      </div>
      <div class="assurance-card">
        <div class="ac-title">You approve before it acts</div>
        <div class="ac-body">{ctx.v.get('security_human_loop', 'Every digital employee in this report is designed with a human approval step. Nothing gets sent to a customer, posted to your accounts, or committed to your calendar without someone on your team reviewing and approving it first.')}</div>
      </div>
      <div class="assurance-card">
        <div class="ac-title">What Rogue Night sees</div>
        <div class="ac-body">{ctx.v.get('security_rn_access', 'During the first 30 days after deployment, we monitor agent logs and error rates to catch issues early. After handoff, we have no standing access to your accounts unless you grant it for a specific support request.')}</div>
      </div>
      <div class="assurance-card">
        <div class="ac-title">What happens if something breaks</div>
        <div class="ac-body">{ctx.v.get('security_support', 'The tools in this report are maintained by their vendors — updates, security patches, and uptime are their responsibility. If an integration breaks or an agent misbehaves, reach out to us. First 30 days of monitoring are included with implementation. After that, we are a call away — diagnosis and fixes quoted per incident.')}</div>
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="page">
    <div class="section-head">
      <div class="number">11 · Next steps</div>
      <h2>Where to from here.</h2>
    </div>
    {ctx.testimonial_html}
    <div style="display: grid; grid-template-columns: 1fr; gap: 20px; margin-top: 32px;">
      <div style="background: rgba(201, 169, 97, 0.06); border: 1px solid var(--gold-line); border-left: 3px solid var(--gold); border-radius: 0 6px 6px 0; padding: 28px 32px;">
        <div style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--gold); margin-bottom: 8px;">Option 01 · Refine</div>
        <p class="body-lede" style="font-size: 19px; margin-bottom: 10px;">Feel strongly about something? We'll amend the report.</p>
        <p style="font-size: 15px; line-height: 1.7;">This report is yours. If something doesn't fit your business — a tool you've already tried, a phase that doesn't make sense, a number that feels off — tell us, and we'll revise. Free of charge. The $395 covers the work, including refinement.</p>
      </div>
      <div style="background: rgba(201, 169, 97, 0.06); border: 1px solid var(--gold-line); border-left: 3px solid var(--gold); border-radius: 0 6px 6px 0; padding: 28px 32px;">
        <div style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--gold); margin-bottom: 8px;">Option 02 · Implement</div>
        <p class="body-lede" style="font-size: 19px; margin-bottom: 10px;">Engage Rogue Night for the implementation.</p>
        <p style="font-size: 15px; line-height: 1.7;">Fixed-fee, fixed-scope. Quote provided after a scoping call. We handle setup, configuration, and integration; you keep the customers, the calls, and the cash.</p>
      </div>
      <div style="background: rgba(201, 169, 97, 0.06); border: 1px solid var(--gold-line); border-left: 3px solid var(--gold); border-radius: 0 6px 6px 0; padding: 28px 32px;">
        <div style="font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--gold); margin-bottom: 8px;">Option 03 · Self-serve</div>
        <p class="body-lede" style="font-size: 19px; margin-bottom: 10px;">Take the report and run it yourself.</p>
        <p style="font-size: 15px; line-height: 1.7;">The recommendations are vendor-neutral. The $395 has covered the work.</p>
      </div>
    </div>
    <div style="border-top: 1px solid var(--rule-strong); padding-top: 24px; text-align: center; margin-top: 64px;">
      <p class="meta" style="margin-bottom: 0;">Rogue Night PTY LTD · ABN 31 633 650 334 · Australia · Prepared {ctx.today}</p>
    </div>
  </div>
</section>

</body>
</html>
"""

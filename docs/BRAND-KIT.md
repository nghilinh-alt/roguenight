# Rogue Night — Brand Kit (Phase 1)

Single-page reference. Locked decisions, brought along with every page.

---

## Identity

| Field | Value |
|---|---|
| Legal name | Rogue Night PTY LTD |
| ABN | 31 633 650 334 |
| Country | Australia |
| Audience | Australian small to medium businesses |
| Service | Digital transformation consulting · AI agent and digital employee deployment · vetted tool advisory |
| One-line positioning | Enterprise-grade digital transformation, AI-amplified, priced for small to medium businesses |
| LinkedIn (URL only, name not shown on site) | https://www.linkedin.com/in/linh-nghi-13692928/ |

---

## Colour palette

| Role | Name | Hex | Usage |
|---|---|---|---|
| Primary background | **Ink** | `#0A0E1A` | Hero, body, primary surfaces |
| Deepest contrast | **Obsidian** | `#050608` | Footer, secondary surfaces, alternating sections |
| Primary accent | **Signet Gold** | `#C9A961` | Headlines (italic emphasis), pillar borders, dividers, eyebrow text, hover states |
| Secondary accent | **Ember** | `#C2410C` | Primary CTAs, hot moments, pull-quotes |
| Body on dark | **Parchment** | `#EDE8DD` | All on-dark copy, body text, headings |
| Mid neutral | **Slate** | `#6B7280` | Captions, secondary text, footer copyright |

**Composition ratio:**
- ~85% Ink + Obsidian
- ~10% Parchment
- ~3% Signet Gold
- ~2% Ember

If you're using more than 5% Ember on a single screen, pull it back.

---

## Typography

| Role | Family | Weight | Usage |
|---|---|---|---|
| Display | Instrument Serif (Google Fonts) | 400 | Hero headlines, section titles, pull quotes. Always italic on the 1-2 key words, coloured Signet Gold. |
| Body | Instrument Sans | 400 / 500 / 600 / 700 | Paragraphs, navigation, buttons, UI, cards, footer |
| Eyebrow / labels | Instrument Sans 500 | uppercase, letter-spacing 0.18–0.22em, 12-13px | Section eyebrows, label text |
| Mono / metadata | JetBrains Mono | 400 / 500 | Meta labels, uppercase data tags, code-like dividers (used in report template) |

**CDN link to paste in every page's `<head>`:**

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

**Headline rule:**
- Primary headlines in Instrument Serif 400, tracking `letter-spacing: -0.02em`, line-height `1.05`
- Italicise the 1-2 words that carry the meaning, colour them Signet Gold
- Example: "Run your business *smarter.* Day and night." (italics + gold on "smarter.")

---

## Logo system

Four variants — pick by context, never recolour or stretch:

| Variant | When to use | File in this package |
|---|---|---|
| Primary stacked lockup | Hero, deck covers, business cards, large-format | `assets/logo-stacked.png` (2048×2048) |
| Horizontal lockup | Nav bars, email signatures, document headers/footers | `assets/logo-horizontal.png` (500×212) and `logo-horizontal-sm.png` (320×135) |
| Standalone eclipse mark | Social avatars, email signature glyph, profile pictures, app icons | `assets/logo-eclipse.png` (320×320) |
| Favicon (simplified SVG) | Browser tabs at 16-32px | `favicon.svg` (inline in HTML — extract via `favicon-extract.md`) |

**Clear space rule:** always leave at least the height of the eclipse moon disc as breathing room on all sides.

**Don't:**
- ❌ Recolour the eclipse (gold-to-ember corona is fixed)
- ❌ Stretch the proportions
- ❌ Place the logo on busy imagery without a dark backing card
- ❌ Use the photographic eclipse below 80px — switch to the simplified favicon

---

## Voice & messaging

### Hero formula

Eyebrow (catchy tagline) → Editorial headline (Instrument Serif with italic gold accent) → 2-sentence subhead → Primary CTA (Ember) + secondary CTA (Ghost) + small price/detail line.

### Section title formula

Eyebrow → Section title with italic emphasis → Subtitle that earns the title.

### Card / pillar formula

Number / serif italic → Punchy declarative title → 1-2 sentence body that explains the punch.

### Trust pillars (locked)

1. Proven on enterprise programs (credibility / experience)
2. Human-led, AI-amplified (delivery model)
3. Vendor-neutral by design (financial trust / honest tool advisory)

### Footer motto (locked)

*"The work that runs while you sleep."*

---

## Voice rules — never violate

| ❌ Never write | ✅ Always write |
|---|---|
| SME / SMEs | small to medium businesses (lowercase) or small business |
| AI-generated report | specially curated |
| Linh / founder name (on landing) | "the Founder" or "we" |
| Brisbane (location for Rogue Night) | Australian |
| AI analyst | AI agents and digital employees |
| Within 24 hours | Within 48 hours |
| Book a free 45-minute walkthrough call | (don't include — locked exclusion) |
| Sole director | Founder |

### Words to use

roadmap · leak · audit · scale · vetted · agents · digital employees · transformation · playbook · insider · enterprise · priced for · built for · day or night · around the clock · vendor-neutral · specially curated · bespoke · for your business

### Words to avoid

synergy · leverage · holistic · journey · solutions provider · partner (overused) · elite · premier · world-class

### Capitalisation rule

"small to medium businesses" is a category, not a proper noun. Use **lowercase** in body text. Title case only in `<title>` tags and headings.

### Sentence rhythm

Short. Then medium. Then occasionally longer for the rhythm break — like this. Aim for sentences that read out loud well.

---

## Pricing language

The AI & Automation Strategy is **$880 flat**. Always pair with:

- "delivered to your inbox in 48 hours" OR
- "in your inbox within 48 hours" OR
- "yours to keep"

Never:
- "AI-generated"
- "Free for a limited time" (it's not)
- Discount language

---

## CTA pattern (locked)

Primary button reads **"Get your AI & Automation Strategy"** with supporting text:

> $880 flat · Delivered to your inbox in 48 hours · Yours to keep

The button click goes **directly to the Tally form**: `https://tally.so/r/xX4YaG` (target="_blank")

The Tally form's after-submit redirect goes to the Stripe Payment Link.

**Do not** present alternative modal options (email-me-the-form, call Anna, book a slot) on the landing page until those backends are wired and tested.

---

## Implementation messaging (always include in client docs)

Two dark callout boxes that recur in any document offering implementation:

```
Rogue Night can implement this for you

[List of what RN does: data migration, account setup, configuration, 
integrations, process design, scoping]

What we don't do: hands-on team training. We provide written guides 
and pointers to official video training, plus availability for questions 
during the first month at no extra cost.

Implementation quote provided on request.
```

For digital-employee work, replace the list with:
- Discovery
- Build
- Deploy supervised
- Handoff and monitor

And the "what we don't do" line becomes: "replace your team."

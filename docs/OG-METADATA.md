# Rogue Night — Open Graph & Meta Tags

Paste-ready `<meta>` block for the landing page when it goes live on `roguenight.com.au`.

The current self-contained landing HTML has minimal `<head>` — when migrating to production, add the block below before `</head>` so LinkedIn / Slack / WhatsApp / Twitter / SMS previews render correctly.

---

## Drop-in block for `<head>`

Replace these placeholder values:
- `https://roguenight.com.au/` → final canonical URL
- `https://roguenight.com.au/og-image.png` → path to your OG image (see specs below)
- `https://roguenight.com.au/favicon.svg` → path to favicon.svg (in this package)

```html
<!-- Primary meta -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rogue Night — Enterprise-grade digital transformation, AI-amplified, priced for small business</title>
<meta name="description" content="Rogue Night helps Australian small to medium businesses identify the right tools and deploy AI agents and digital employees. Specially curated Digital Health Check, $350 flat, in your inbox within 48 hours.">
<meta name="author" content="Rogue Night PTY LTD">
<meta name="theme-color" content="#0A0E1A">

<!-- Canonical -->
<link rel="canonical" href="https://roguenight.com.au/">

<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="https://roguenight.com.au/favicon.svg">
<link rel="apple-touch-icon" href="https://roguenight.com.au/apple-touch-icon.png">

<!-- Open Graph (LinkedIn, Facebook, Slack, WhatsApp, iMessage) -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Rogue Night">
<meta property="og:title" content="Rogue Night — The work that runs while you sleep">
<meta property="og:description" content="We help Australian small to medium businesses identify the right tools and deploy AI agents and digital employees. Digital Health Check, $350 flat, within 48 hours.">
<meta property="og:url" content="https://roguenight.com.au/">
<meta property="og:image" content="https://roguenight.com.au/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Rogue Night — enterprise-grade digital transformation, AI-amplified, priced for small business">
<meta property="og:locale" content="en_AU">

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Rogue Night — The work that runs while you sleep">
<meta name="twitter:description" content="We help Australian small to medium businesses identify the right tools and deploy AI agents and digital employees. Digital Health Check, $350 flat, within 48 hours.">
<meta name="twitter:image" content="https://roguenight.com.au/og-image.png">
<meta name="twitter:image:alt" content="Rogue Night logo on Ink background with editorial headline">

<!-- Robots -->
<meta name="robots" content="index,follow,max-image-preview:large">

<!-- JSON-LD structured data (helps Google understand the business) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Rogue Night PTY LTD",
  "url": "https://roguenight.com.au/",
  "logo": "https://roguenight.com.au/logo-stacked.png",
  "image": "https://roguenight.com.au/og-image.png",
  "description": "Digital transformation consulting, AI agent and digital employee deployment, and vetted tool advisory for Australian small to medium businesses.",
  "email": "hello@roguenight.com.au",
  "identifier": [
    {
      "@type": "PropertyValue",
      "propertyID": "ABN",
      "value": "31 633 650 334"
    }
  ],
  "areaServed": {
    "@type": "Country",
    "name": "Australia"
  },
  "priceRange": "A$350",
  "offers": {
    "@type": "Offer",
    "name": "Digital Health Check",
    "price": "350",
    "priceCurrency": "AUD",
    "description": "Specially curated digital health check for small business — tool snapshot, six tool recommendations, three AI agent ideas, and a cull list. Delivered to your inbox within 48 hours."
  }
}
</script>
```

---

## OG image specs

The OG image is what shows when someone shares the landing URL in LinkedIn / Slack / WhatsApp / iMessage. **Get this right** — it's 80% of how the page is judged before anyone clicks.

| Spec | Value |
|---|---|
| File path | `/og-image.png` |
| Dimensions | 1200×630 pixels (mandatory — LinkedIn / Facebook standard) |
| Aspect ratio | 1.91:1 |
| File format | PNG (preferred) or JPG |
| Max file size | < 300 KB after compression |
| Safe zone | Keep critical content inside the central 1000×500 area — some platforms crop edges |

### Composition direction

The OG image should match the landing-page hero:

**Background:** Ink (`#0A0E1A`) or Obsidian (`#050608`) full bleed.

**Foreground:**
- Stacked Rogue Night lockup (eclipse + wordmark) at the left, sized to about 35% of canvas width
- Editorial headline on the right: *"Run your business smarter. Day and night."* — italic + Signet Gold on *smarter.*, Parchment on the rest
- Tiny strip of body copy or eyebrow at the bottom: "ENTERPRISE-GRADE DIGITAL TRANSFORMATION · AI-AMPLIFIED · BUILT FOR SMALL BUSINESS" in Slate uppercase

**Style:** Same editorial tone as the landing hero. Plenty of breathing room — don't crowd the canvas. Generous negative space around the logo and headline.

**Don'ts:**
- Don't recolour the eclipse
- Don't include the ABN, Tally link, or footer detail — they don't read at thumbnail size
- Don't add stock-photo backgrounds or gradients
- Don't include "AI" robot iconography
- Don't add "click here" or button graphics — that's a meta-fail

---

## Apple touch icon spec

For iOS home-screen save:

| Spec | Value |
|---|---|
| File path | `/apple-touch-icon.png` |
| Dimensions | 180×180 pixels |
| Format | PNG (no transparency — iOS adds rounded corners automatically) |
| Content | Eclipse mark on Ink background, centred, with ~15% padding around the mark |

Source: crop/center `assets/logo-eclipse.png` to 180×180 with Ink background fill.

---

## Verification checklist (before publishing)

After uploading the new landing HTML + OG image + favicon to your host:

- [ ] Paste the production URL into LinkedIn's [Post Inspector](https://www.linkedin.com/post-inspector/) — image renders, title and description read correctly
- [ ] Paste into [opengraph.xyz](https://www.opengraph.xyz/) — all OG tags resolve
- [ ] Paste into Slack message preview — image renders at large card size
- [ ] iMessage to yourself — preview shows logo + headline
- [ ] WhatsApp to yourself — same
- [ ] Search "site:roguenight.com.au" in Google after ~3 days — title and description match what's in the meta tags
- [ ] Google [Rich Results Test](https://search.google.com/test/rich-results) — JSON-LD validates as ProfessionalService

If any of those fail: the most common fix is force-refreshing the platform's scraper cache by appending `?v=2` to the URL once, then clearing.

---

## Why this matters

Most of the audience for Rogue Night first sees the brand as a shared link in someone's Slack or LinkedIn DM, not as a Google search result. The OG card IS the homepage for half your visitors. Treat it as a hero asset, not an afterthought.

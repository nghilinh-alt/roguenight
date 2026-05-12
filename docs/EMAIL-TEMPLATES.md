# Rogue Night — Email Templates

Paste-ready bodies for the Hostinger webmail flow (hello@roguenight.com.au).

All copy follows the locked Phase 1 voice rules. Never paste these without first reading them — replace `[bracketed]` fields per customer.

---

## 1. Report delivery (primary — manual send)

**Use when:** A customer has paid, the PDF is generated, you're sending it from Hostinger webmail with the PDF attached.

**Subject:**

```
Your Digital Health Check — [Business name]
```

**Body:**

```
Hi [First name],

Your Digital Health Check is attached.

Inside you'll find a snapshot of where [Business name] sits today, six 
specifically curated tool recommendations across foundation and core 
workflows, three AI agents you could deploy as your next move, and the 
cull list of tools that aren't pulling their weight.

Most teams find one or two recommendations pay for the whole report 
inside a fortnight. Take the report at your pace — it's yours to keep, 
no expiry.

If anything in there raises a question, just reply to this email. 
Rogue Night can implement any of the recommended tools or build the 
agents for you — happy to scope on request.

Day or night,
The Rogue Night team
hello@roguenight.com.au
ABN 31 633 650 334
```

**Attachment:** `[Business-name]-digital-health-check.pdf` (rename the file from Lois's output before attaching)

**Voice check before sending:**
- [ ] No "SME"
- [ ] No "AI-generated"
- [ ] No founder name
- [ ] No "Brisbane"
- [ ] No "Book a free 45-minute call"
- [ ] Says "specially curated" not "AI-generated"
- [ ] Says "yours to keep" or "no expiry"

---

## 2. Bounce recovery (when the report bounces)

**Use when:** Stripe paid but your delivery email bounced and you've found a working address.

**Subject:**

```
Your Digital Health Check — second attempt
```

**Body:**

```
Hi [First name],

Apologies — my first attempt to send your Digital Health Check bounced 
from [original email address]. This is the working copy, attached.

Same report as ordered: tool snapshot, six curated recommendations, 
three agent ideas, cull list.

Reply here if anything's unclear.

Day or night,
The Rogue Night team
hello@roguenight.com.au
```

---

## 3. Delay notice (if you're going to miss the 48h promise)

**Use when:** Something has gone wrong and you need to flag a delay BEFORE the customer notices. Send this before the 48-hour mark, not after.

**Subject:**

```
Quick note on your Digital Health Check — [Business name]
```

**Body:**

```
Hi [First name],

Quick note: your Digital Health Check is taking a touch longer than 
the 48 hours promised. New ETA is [day, date — be specific, 
e.g. "Thursday morning"].

The extra time goes into [one honest sentence, e.g. "double-checking 
the integration story between the two accounting tools we're 
considering for you"]. The output is better for it.

No action needed from you. I'll have the report in your inbox by the 
new ETA.

Day or night,
The Rogue Night team
```

**Note:** Never offer a refund proactively here — the customer's getting the report. If they ask, refer to the privacy policy and reply with terms.

---

## 4. Engagement enquiry (when they ask "can you implement this?")

**Use when:** A customer who already has their report writes back asking about implementation, scoping, or further work.

**Subject:**

```
Re: Your Digital Health Check — implementation scope
```

**Body:**

```
Hi [First name],

Glad the report is useful.

For [the specific tool or agent they asked about], implementation 
typically involves:

  - [bullet 1 — e.g. account setup + workspace provisioning]
  - [bullet 2 — e.g. data migration from current system]
  - [bullet 3 — e.g. process design + first workflow built]
  - [bullet 4 — e.g. integration with your accounting/CRM]
  - [bullet 5 — e.g. written guide + first-month question support]

What we don't do: hands-on team training. We provide written guides 
and pointers to official video training, plus availability for 
questions during the first month at no extra cost.

To quote properly I'd need a 20-30 minute call to understand 
[the specific shape of their setup — e.g. "your current Xero structure 
and how your invoices flow today"]. Reply with a couple of times that 
work and I'll send a calendar invite.

Day or night,
The Rogue Night team
```

**Voice check:**
- [ ] Doesn't promise team training
- [ ] Frames the call as scoping, not "free 45-minute walkthrough"
- [ ] Lists what RN does AND what it doesn't

---

## 5. Form-but-no-payment recovery

**Use when:** Tally form received but Stripe payment didn't land (look in Airtable Responses for Status = New older than 24 hours with no Stripe event).

**Subject:**

```
Saw your Digital Health Check request — [Business name]
```

**Body:**

```
Hi [First name],

Saw your request come through for a Digital Health Check on 
[Business name] — looks like the payment step didn't complete. 
Happens sometimes (card declines, browser hiccup, distraction).

If you'd still like the report, here's the direct link:

  [Stripe Payment Link URL]

Once the A$350 lands, your report goes into the build queue and lands 
in your inbox within 48 hours.

If you've changed your mind, no need to reply — I'll close the request 
out at the end of the week.

Day or night,
The Rogue Night team
hello@roguenight.com.au
```

---

## 6. Sub-processor change notice (privacy policy material change)

**Use when:** A sub-processor changes (e.g. switching from Hostinger to Workspace, or adding a new tool). Privacy policy says you'll notify materially affected users.

**Subject:**

```
Update to how Rogue Night handles your information
```

**Body:**

```
Hi [First name],

Quick heads-up: [one sentence on what changed — e.g. "we've moved 
our email from Hostinger to Google Workspace, which means your 
email correspondence with us is now stored on Google's Australian 
servers instead of Hostinger's."]

Why we're telling you: our privacy policy says we'll let you know 
when our sub-processor list changes in a way that could affect you. 
The full updated policy is at:

  [https://roguenight.com.au/privacy]

Nothing changes about what we do with your information — we still 
don't sell or share it, and you can still ask for a copy or deletion 
at any time by replying here.

If you have questions, reply to this email or write to 
hello@roguenight.com.au.

Day or night,
The Rogue Night team
ABN 31 633 650 334
```

---

## Signature block (default — paste as needed)

```
Day or night,
The Rogue Night team
hello@roguenight.com.au
roguenight.com.au · ABN 31 633 650 334
```

For replies that are clearly from the founder voice, swap "The Rogue Night team" for "Linh, Rogue Night" — but only AFTER the customer has paid and is engaged. The landing-page promise is still the team voice.

---

## Things never to write in customer email

- "AI-generated" — say "specially curated"
- "Within 24 hours" — say "within 48 hours"
- "Book a free 45-minute walkthrough call"
- "Brisbane" — say "Australian"
- "SME" — say "small to medium business"
- "Sole director" — say "Founder" if attribution needed
- Discount language ("$350 normally, $250 for you")
- "Synergy" / "leverage" / "holistic" / "premier" / "world-class"

---

## Hostinger sending notes

- Send from `hello@roguenight.com.au`, not from a personal alias
- Reply-To header stays `hello@roguenight.com.au`
- Plain text + simple HTML signature is fine — don't paste branded HTML email templates, they trigger spam filters more than they help at this volume
- Attach the PDF directly (Hostinger webmail handles up to 25 MB attachments, our reports are ~1-2 MB)
- File-name the PDF `[Business-name]-digital-health-check.pdf` before attaching — looks better in the customer's inbox than `report-output.pdf`
- BCC `hello@roguenight.com.au` on every report send so you have a sent-record visible in the inbox folder

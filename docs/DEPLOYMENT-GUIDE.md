# Rogue Night — Deployment Guide

Three phases, expect ~45–90 minutes end-to-end. Phase B–C have DNS waiting periods that you can't speed up.

```
Phase A — Push the repo to GitHub      (5–10 min, anytime)
Phase B — Upload files to Hostinger    (10–15 min, prereq: paid Web Hosting plan)
Phase C — Cut DNS over + provision SSL (5 min hands-on + 1–24h propagation)
```

---

## Phase A — Push to GitHub

The repo is initialised locally with two commits and 38 tracked files. You just need to give it a home on github.com.

### Option 1 — GitHub CLI (fastest)

If you have the `gh` CLI installed and authenticated:

```bash
# Unzip the bundle to wherever you keep code
unzip ~/Downloads/roguenight-website-repo.zip -d ~/code/
cd ~/code/roguenight-website

# Verify the repo state
git log --oneline                 # should show 2 commits
git remote -v                     # should show no remotes yet

# Create the private repo and push
gh repo create nghilinh-alt/roguenight-website \
    --private \
    --source=. \
    --remote=origin \
    --push \
    --description "Website for Rogue Night PTY LTD — landing, privacy, terms, 404"
```

That's it. Open <https://github.com/nghilinh-alt/roguenight-website> to confirm.

### Option 2 — Web UI

If you don't have `gh` CLI:

1. Unzip the bundle to `~/code/roguenight-website/` (or wherever)
2. Go to <https://github.com/new>
3. Owner: `nghilinh-alt`, Name: `roguenight-website`, Visibility: **Private**
4. **Do NOT** check "Add a README", "Add .gitignore", or "Choose a license" — we already have them
5. Click "Create repository"
6. On the next page, scroll to "…or push an existing repository from the command line", copy the three commands shown (they'll look like):

   ```bash
   git remote add origin https://github.com/nghilinh-alt/roguenight-website.git
   git branch -M main
   git push -u origin main
   ```

7. Open Terminal, `cd` into the unzipped repo folder, paste those commands.

If you get a password prompt: GitHub stopped accepting passwords for git over HTTPS in 2021. Either set up a Personal Access Token (Settings → Developer settings → Personal access tokens) or switch the remote to SSH (`git remote set-url origin git@github.com:nghilinh-alt/roguenight-website.git`) if your SSH key is registered.

### Option 3 — Git bundle (no zip extraction needed)

If you prefer to clone directly from the bundle file:

```bash
cd ~/code
git clone ~/Downloads/roguenight-website.bundle roguenight-website
cd roguenight-website
git remote remove origin               # the bundle creates a default 'origin' to the file
gh repo create nghilinh-alt/roguenight-website --private --source=. --remote=origin --push
```

### Verifying the push

After pushing, the repo on github.com should show:

- 2 commits ("Initial commit…" and "Exclude intermediate build outputs…")
- 38 files across `public/`, `src/`, `assets-raw/`, `docs/`, plus README + LICENSE + .gitignore
- `README.md` rendered as the landing view

---

## Phase B — Hostinger upload

### Step B1 — Confirm you have Web Hosting (not just Email)

Log into <https://hpanel.hostinger.com>. On the left sidebar look for:

- **"Websites"** or **"Hosting"** section with a domain assigned — ✅ you have Web Hosting, continue to B2
- **"Emails"** only, no "Websites" section — you need to add a hosting plan. The cheapest is **Hostinger Premium Web Hosting** at ~A$5/month (12-month commitment) and supports 100 websites, free SSL, 100GB SSD. Either upgrade your account or buy a separate hosting plan. Then come back here.

If unsure, run this URL: <https://hpanel.hostinger.com/hosting>. If it loads with a "Manage" button next to a hosting plan, you have it.

### Step B2 — Attach roguenight.com.au to the hosting plan

1. hPanel → Websites → "Add Website" or "Manage" existing
2. If `roguenight.com.au` isn't already attached: Add Website → enter the domain → it'll create the directory structure
3. Note: Hostinger will probably ask whether you want to install WordPress. **Decline** — we're uploading static files.

### Step B3 — Open File Manager

1. hPanel → Files → File Manager
2. Navigate to `public_html/` for `roguenight.com.au`
   - URL will look like: `/home/uXXXXXX/domains/roguenight.com.au/public_html/`
3. **Back up anything that's already there** (Hostinger usually drops a placeholder `index.html` or a "Coming soon" page). Right-click → "Move" → `_old/` or just delete it.

### Step B4 — Upload the public/ bundle

Two ways:

**Drag-and-drop (easy):**

1. Unzip `roguenight-public-html.zip` locally — it'll produce a folder with `index.html`, `privacy/`, `terms/`, `404.html`, etc.
2. In Hostinger File Manager, navigate INTO `public_html/`
3. Drag the *contents* of the unzipped folder into the File Manager window (NOT the wrapper folder itself — drag everything inside it)
4. File Manager will preserve the `privacy/` and `terms/` subfolders

**Upload zip + extract (faster for large transfers):**

1. In File Manager, click "Upload Files" → select `roguenight-public-html.zip`
2. Once uploaded, right-click the zip → "Extract" → target current directory
3. Delete the zip after extraction

### Step B5 — Verify the file tree

After upload, `public_html/` should contain:

```
public_html/
├── index.html
├── privacy/
│   └── index.html
├── terms/
│   └── index.html
├── 404.html
├── robots.txt
├── sitemap.xml
├── og-image.png
├── apple-touch-icon.png
├── favicon.svg
├── logo-stacked.png
├── health-check-sample.pdf
└── .htaccess          ← important — ensures clean URLs + HTTPS redirect
```

If `.htaccess` is invisible: File Manager → top-right "Settings" gear → "Show Hidden Files" ON.

### Step B6 — Test via Hostinger preview URL (optional but recommended)

Hostinger gives you a preview URL like `https://roguenight.com.au.preview-domain.com` or similar (look for "Preview" in hPanel). Open it. You should see the landing page. If it loads but images are broken, check that the file structure matches above. If the page itself doesn't load, check that `index.html` is in `public_html/` root, not in a sub-folder.

If you don't have a preview URL, skip this — you'll verify after DNS propagation.

---

## Phase C — DNS cutover

This is the only step with mandatory waiting. Plan it for a quiet hour.

### Step C1 — Find Hostinger's nameservers

hPanel → Websites → roguenight.com.au → "Manage" → look for **DNS / Nameservers** info. You'll see something like:

```
ns1.dns-parking.com
ns2.dns-parking.com
```

(The exact nameservers may differ — copy what Hostinger shows you.)

### Step C2 — Update nameservers at your registrar

Where did you register `roguenight.com.au`? Common AU registrars and where to update:

- **VentraIP** → Domain Manager → Manage → Nameservers
- **Crazy Domains** → My Account → Domains → DNS Management
- **GoDaddy** → My Products → DNS → Nameservers → Change
- **Synergy Wholesale / Netregistry** → Domain List → Manage → Nameservers
- **Cloudflare Registrar** → Domain → Nameservers (do NOT update if you're using Cloudflare's free DNS — instead, add Hostinger's IP as an A record. See "If you're using Cloudflare DNS" below)

Replace whatever's there with Hostinger's two nameservers (Step C1).

**Propagation timing:** anywhere from 5 minutes to 24 hours. Usually < 2 hours for `.com.au`.

Track with `dig`:

```bash
dig roguenight.com.au NS +short
```

Once you see Hostinger's nameservers, DNS has propagated for you.

### Step C3 — Provision SSL

The moment Hostinger sees DNS pointing at it, you can install a free Let's Encrypt SSL:

1. hPanel → Security → SSL
2. Find roguenight.com.au in the list → "Install" → choose "Let's Encrypt SSL (Free)"
3. Wait 2–10 minutes. You'll see "Active" next to the domain.
4. Optionally enable "Force HTTPS" in the same panel — though our `.htaccess` already handles this redirect.

### Step C4 — First live load

Open <https://roguenight.com.au> in an incognito window (so no cached DNS). You should see:

- ✅ Padlock icon (HTTPS valid)
- ✅ Landing page with eclipse logo, "Run your business smarter. Day and night." hero
- ✅ "Book a Digital Health Check" CTA opens the Tally form in a new tab
- ✅ "Download (PDF, 23 pages)" downloads Cindy's sample report
- ✅ Footer Privacy + Terms links open the respective pages
- ✅ Brand bar logo click goes home
- ✅ 404 page: visit something like https://roguenight.com.au/this-does-not-exist and see "Lost in the night"

### Step C5 — Validate Open Graph

Paste your URL into:

- <https://www.linkedin.com/post-inspector/> — should render the OG card
- <https://www.opengraph.xyz/> — should resolve all OG tags
- <https://search.google.com/test/rich-results> — JSON-LD validates as ProfessionalService

If anything's off, the most common fix is forcing a scraper refresh: append `?v=2` to the URL in the inspector, then click "Inspect" again.

### Step C6 — Submit to Google Search Console

Optional but recommended for SEO ranking speed:

1. Go to <https://search.google.com/search-console>
2. Add property → URL prefix → `https://roguenight.com.au/`
3. Verify ownership via DNS TXT record (Hostinger DNS panel) or HTML file upload
4. Once verified: Sitemaps → submit `https://roguenight.com.au/sitemap.xml`

Google will start crawling within 24–48h. The site will start appearing in search results within 1–2 weeks.

---

## Edge cases

### If you're using Cloudflare DNS

Don't change nameservers. Instead, in your Cloudflare dashboard:

1. DNS → Records
2. Find existing `A` record for `roguenight.com.au` (or create one) — point at the **server IP** Hostinger gave you (hPanel shows it as "Server IP" in the website overview, or in DNS info)
3. Find `CNAME` for `www` — set to `roguenight.com.au`
4. Make sure both records are set to **"DNS only"** (grey cloud), NOT proxied (orange), at least initially. Proxied requires extra origin SSL setup.

Then come back to Step C3 and provision Hostinger's SSL.

### If the preview URL works but the real domain shows a Hostinger placeholder

DNS hasn't fully propagated yet, or your local DNS is cached. Try:
- Incognito window
- Mobile data instead of WiFi
- `dig roguenight.com.au A +short` — should return Hostinger's server IP

Wait 30 minutes and retry.

### If health-check-sample.pdf returns 404

Make sure the file exists at `public_html/health-check-sample.pdf` (not inside a subfolder). The link in the landing page is `/health-check-sample.pdf` — that's relative to the domain root.

---

## Updating the site after launch

```bash
# Edit copy or styling in src/build_*.py (or in public/*.html directly for hotfixes)
cd ~/code/roguenight-website/src
python3 build_all.py            # rebuilds production HTML and stages public/

# Commit and push
cd ..
git add -A
git commit -m "Update [thing]"
git push

# Re-upload to Hostinger
# Two options:
#   (a) Drag changed files in File Manager — fastest for one or two pages
#   (b) Re-zip public/ and re-extract via Hostinger File Manager
cd public
python3 -c "import zipfile, os
with zipfile.ZipFile('../public-update.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for r, d, fs in os.walk('.'):
        for f in fs: z.write(os.path.join(r, f), os.path.relpath(os.path.join(r, f), '.'))"
# upload public-update.zip → extract in public_html/
```

---

## Help

For build-system questions, see `README.md` in the repo root.
For brand voice and visual rules, see `docs/BRAND-KIT.md`.
For Open Graph specs, see `docs/OG-METADATA.md`.

Anything stuck? `hello@roguenight.com.au` works once the domain is live.

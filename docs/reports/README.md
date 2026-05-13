# Reports

Per-client Digital Health Check reports — both the templates and the generated outputs — are **not stored in this repo**.

## Why not?

1. **Per-client outputs are PII.** Names, business details, financial situations, identified pain points. Committing them to a public-readable repo would breach the privacy promise.
2. **Templates are tightly coupled to runtime.** The report template is built by `agents/dhc-report-writer/scripts/populate_template.py` from `agents/dhc-report-writer/data/v5-style-block.txt` + per-client `vars.json`. The template is effectively the script — there's no static "template file" to check in.
3. **Lifecycle lives in Airtable.** The Reports table (`appCLdTCbJ5zGe9fo/tblozeWaPiqdA7FkC`) tracks every report version, sent date, walkthrough notes, engagement status, implementation status. That's the canonical place.

## Where each piece lives

| Piece | Where |
|---|---|
| Report template logic (HTML structure, section flow, brand CSS) | [`agents/dhc-report-writer/scripts/populate_template.py`](../../agents/dhc-report-writer/scripts/populate_template.py) |
| Report brand CSS | [`agents/dhc-report-writer/data/v5-style-block.txt`](../../agents/dhc-report-writer/data/v5-style-block.txt) |
| Example `vars.json` shape (Pacific Coast Plumbing) | [`agents/dhc-report-writer/data/report_vars.example.json`](../../agents/dhc-report-writer/data/report_vars.example.json) |
| Mock response (Pacific Coast Plumbing) | [`agents/dhc-report-writer/data/mock_response.json`](../../agents/dhc-report-writer/data/mock_response.json) |
| Per-client HTML preview | Generated on demand by Lois, published via `PublishWebpage` → public URL stored in Airtable `Reports.Report URL` |
| Per-client PDF | Generated on demand by `render_pdf.py` → attached to Airtable `Reports.Report PDF` |
| Sample report PDF (public, on the landing page) | [`../../public/health-check-sample.pdf`](../../public/health-check-sample.pdf) (mirrored from `assets-raw/`) |
| Per-client lifecycle (status, walkthrough notes, engagement decision) | Airtable Reports table |

## To preview the template without a client

Run the populate script against the mock response:

```bash
cd agents/dhc-report-writer/scripts/
python3 populate_template.py \
  ../data/mock_response.json \
  ../data/report_vars.example.json \
  /tmp/preview.html
open /tmp/preview.html
```

You'll see the v5 template populated with Pacific Coast Plumbing (trades example).

## To add a new sample (public-facing)

If you want to ship a new sample report on the landing page:

1. Generate the sample via the populate script (use the mock or a synthetic non-PII customer).
2. Convert to PDF via `render_pdf.py`.
3. Save it as `assets-raw/health-check-sample.pdf` (replacing the existing one).
4. Regenerate the page-1 thumbnail and base64-encode into `src/data/sample-thumb-b64.txt`.
5. Update `PDF_PAGES` and `SAMPLE_CLIENT` constants in `src/build_landing.py`.
6. Run `python3 src/build_all.py` to rebuild and stage the new public PDF + landing-page references.

See [`docs/DEPLOYMENT-GUIDE.md`](../DEPLOYMENT-GUIDE.md) for the full sample-swap workflow.

"""Render a populated HTML report to PDF.

Usage:
    python3 render_pdf.py <input.html> <output.pdf>

Strategy:
    Tries Playwright (headless Chromium) first — best fidelity, matches what Linh would
    get from Cmd+P → Save as PDF in Chrome. Falls back to WeasyPrint if Playwright isn't
    available. Last-resort: documents the manual export path.

Sandbox notes:
    - Playwright needs `pip install playwright && playwright install chromium`. The Chromium
      install is ~150MB; first run is slow. Subsequent runs are fast.
    - WeasyPrint needs `pip install weasyprint`. It handles most CSS but has flexbox quirks
      and can struggle with Google Fonts. For our v5 template (which uses Instrument Serif
      + Instrument Sans + JetBrains Mono via Google Fonts), Playwright produces noticeably
      better output.

The HTML template already has @media print CSS — A4 page size, page breaks at section
boundaries, hidden editor cheat sheet. Both engines will respect this.
"""
import os
import sys


def render_with_playwright(html_path: str, pdf_path: str) -> bool:
    """Returns True on success, False if Playwright unavailable."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False

    abs_html = os.path.abspath(html_path)
    file_url = f"file://{abs_html}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(file_url, wait_until="networkidle")
        # Give Google Fonts a beat to load
        page.wait_for_timeout(2000)
        page.pdf(
            path=pdf_path,
            format="A4",
            margin={"top": "18mm", "bottom": "18mm", "left": "16mm", "right": "16mm"},
            print_background=True,
        )
        browser.close()
    return True


def render_with_weasyprint(html_path: str, pdf_path: str) -> bool:
    """Returns True on success, False if WeasyPrint unavailable."""
    try:
        from weasyprint import HTML
    except ImportError:
        return False

    HTML(filename=html_path).write_pdf(pdf_path)
    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: render_pdf.py <input.html> <output.pdf>", file=sys.stderr)
        sys.exit(1)

    html_path, pdf_path = sys.argv[1], sys.argv[2]

    if not os.path.exists(html_path):
        print(f"HTML file not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    # Try Playwright first
    print("Attempting Playwright render...", file=sys.stderr)
    if render_with_playwright(html_path, pdf_path):
        print(f"PDF written via Playwright: {pdf_path}")
        return

    print("Playwright unavailable, trying WeasyPrint...", file=sys.stderr)
    if render_with_weasyprint(html_path, pdf_path):
        print(f"PDF written via WeasyPrint: {pdf_path}")
        return

    print(
        "Neither Playwright nor WeasyPrint is installed.\n"
        "Install one:\n"
        "  pip install playwright && playwright install chromium\n"
        "  pip install weasyprint\n"
        "Or render manually:\n"
        "  Open the HTML in Chrome → Cmd+P → Save as PDF (A4)\n",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()

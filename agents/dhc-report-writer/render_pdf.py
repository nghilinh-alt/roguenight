"""Render a populated HTML report to PDF.

Usage:
    python3 render_pdf.py <input.html> <output.pdf>

Strategy:
    Tries Playwright (headless Chromium) first — best fidelity for CSS grid, page
    breaks, backgrounds, and @page rules. Falls back to WeasyPrint if Playwright
    isn't available. Last-resort: documents the manual export path.

IMPORTANT — Playwright margin handling (2026-05-14):
    CSS handles all page margins via @page rules:
      @page { size: A4; margin: 18mm 16mm; }
      @page:first { margin: 0; } — full-bleed cover page

    Playwright is called WITHOUT margin params and WITH prefer_css_page_size=True
    so the CSS @page rules take precedence. Do NOT pass margin={} to page.pdf() —
    it overrides @page:first and breaks the full-bleed cover.

    WeasyPrint respects @page rules natively, no special handling needed.

Sandbox notes:
    - Playwright needs `pip install playwright && python3 -m playwright install chromium`.
      Chromium install is ~150MB; first run is slow, subsequent runs are fast.
    - WeasyPrint: `pip install weasyprint`. Handles most CSS but struggles with CSS
      grid across page breaks (white background boxes stretch across pages). Use
      Playwright for production renders.
"""
import os
import sys


def render_with_playwright(html_path: str, pdf_path: str) -> bool:
    """Returns True on success, False if Playwright unavailable."""
    try:
        import asyncio
        from playwright.async_api import async_playwright
    except ImportError:
        return False

    abs_html = os.path.abspath(html_path)
    file_url = f"file://{abs_html}"

    async def _render():
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(file_url, wait_until="networkidle")
            # Let CSS @page handle all margins (including @page:first margin:0 for cover)
            await page.pdf(
                path=pdf_path,
                print_background=True,
                prefer_css_page_size=True,
            )
            await browser.close()

    asyncio.run(_render())
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

    # Try Playwright first (preferred — handles CSS grid, @page:first, backgrounds)
    print("Attempting Playwright render...", file=sys.stderr)
    if render_with_playwright(html_path, pdf_path):
        size = os.path.getsize(pdf_path)
        print(f"PDF rendered via Playwright: {size:,} bytes -> {pdf_path}")
        return

    print("Playwright unavailable, trying WeasyPrint...", file=sys.stderr)
    if render_with_weasyprint(html_path, pdf_path):
        size = os.path.getsize(pdf_path)
        print(f"PDF rendered via WeasyPrint: {size:,} bytes -> {pdf_path}")
        return

    print(
        "Neither Playwright nor WeasyPrint is installed.\n"
        "Install one:\n"
        "  pip install playwright && python3 -m playwright install chromium\n"
        "  pip install weasyprint\n"
        "Or render manually:\n"
        "  Open the HTML in Chrome -> Cmd+P -> Save as PDF (A4, background graphics on)\n",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()

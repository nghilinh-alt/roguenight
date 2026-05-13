#!/usr/bin/env python3
"""Convenience runner — builds all six HTML pages in production mode,
plus the OG image and apple-touch-icon. Stages everything into ../public/
matching the Hostinger upload structure.

Run from anywhere:
    python3 path/to/repo/src/build_all.py

Or simpler from inside src/:
    cd src && python3 build_all.py
"""
import os
import shutil
import subprocess
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SRC)
PUBLIC = os.path.join(REPO_ROOT, 'public')
ASSETS_RAW = os.path.join(REPO_ROOT, 'assets-raw')


def run(script, env=None):
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    result = subprocess.run(['python3', script], cwd=SRC,
                            env=full_env, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ✗ {script}\n{result.stderr}")
        sys.exit(result.returncode)
    return result.stdout.strip()


def stage(src_path, dest_path):
    if not os.path.exists(src_path):
        print(f"  ⚠ {src_path} not found — skip")
        return
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copy(src_path, dest_path)
    rel = os.path.relpath(dest_path, REPO_ROOT)
    print(f"  ✓ {os.path.basename(src_path)} → {rel}")


def main():
    print("Rogue Night — production build")
    print("=" * 48)

    # Ensure public folder structure exists
    for sub in ['', 'privacy', 'terms', 'thank-you', 'confirmation']:
        os.makedirs(os.path.join(PUBLIC, sub), exist_ok=True)

    # 1. OG image (always — no mode toggle)
    print("\n[1/8] Open Graph image")
    print(f"  {run('build_og_image.py')}")
    stage(os.path.join(SRC, 'og-image.png'), os.path.join(PUBLIC, 'og-image.png'))

    # 2. Apple touch icon
    print("\n[2/8] Apple touch icon")
    print(f"  {run('build_apple_touch_icon.py')}")
    stage(os.path.join(SRC, 'apple-touch-icon.png'), os.path.join(PUBLIC, 'apple-touch-icon.png'))

    # 3-8. HTML pages in production mode
    pages = [
        ('Landing page',         'build_landing.py',      'rogue-night-landing.html',      'index.html'),
        ('Privacy policy',       'build_privacy.py',      'rogue-night-privacy.html',      'privacy/index.html'),
        ('Terms of service',     'build_terms.py',        'rogue-night-terms.html',        'terms/index.html'),
        ('404 page',             'build_404.py',          'rogue-night-404.html',          '404.html'),
        ('Thank-you page',       'build_thank_you.py',    'rogue-night-thank-you.html',    'thank-you/index.html'),
        ('Confirmation page',    'build_confirmation.py', 'rogue-night-confirmation.html', 'confirmation/index.html'),
    ]
    for idx, (label, script, output, dest) in enumerate(pages, start=3):
        print(f"\n[{idx}/8] {label} (production)")
        print(f"  {run(script, env={'STAGING_MODE': 'false'})}")
        stage(os.path.join(SRC, output), os.path.join(PUBLIC, dest))

    # 7. Static support files that aren't built dynamically
    print("\n[supporting files]")
    files_to_ensure = [
        (os.path.join(ASSETS_RAW, 'logo-stacked.png'),  os.path.join(PUBLIC, 'logo-stacked.png')),
        (os.path.join(ASSETS_RAW, 'health-check-sample.pdf'), os.path.join(PUBLIC, 'health-check-sample.pdf')),
    ]
    for src, dest in files_to_ensure:
        if os.path.abspath(src) == os.path.abspath(dest):
            continue
        stage(src, dest)

    # Refresh staging-mode HTML so in-src/ previews stay in sync
    print("\n[refresh staging HTML for in-thread review]")
    for _, script, _, _ in pages:
        run(script)
    print("  ✓ staging HTML refreshed (in src/)")

    print(f"\nDone. Production output is in {os.path.relpath(PUBLIC)}/")
    print("Upload everything inside that folder to your Hostinger public_html.")


if __name__ == '__main__':
    main()

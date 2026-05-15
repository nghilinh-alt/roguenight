#!/usr/bin/env python3
"""Regenerate the base64 brand-bar / footer logo data files with a transparent
background so the logos blend seamlessly into the page Ink colour (#0A0E1A).

The source PNGs (assets-raw/logo-horizontal*.png) have a near-Ink background
baked in. On a darker page that background reads as a visible rectangle around
the logo. We apply the same luminance-mask technique used in build_og_image.py:
pixels near the baked-in background fade to alpha 0; pixels clearly part of
the logo content (eclipse highlights, wordmark) stay fully opaque, with a
smooth ramp in between to avoid hard edges.

Outputs:
  data/horizontal-b64.txt      — brand-bar logo (500×212 source)
  data/horizontal_sm-b64.txt   — footer logo    (320×135 source)

Run from anywhere:
  python3 path/to/repo/src/build_logos.py
"""
import base64
import io
import os

import numpy as np
from PIL import Image

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_RAW = os.path.join(_SCRIPT_DIR, '..', 'assets-raw')
_DATA = os.path.join(_SCRIPT_DIR, 'data')

# Luminance ramp tuned for these specific PNGs.
# - Background sits in the lum [25, 40) bucket (~83% of pixels). That's the
#   baked-in near-Ink fill — fade fully to transparent.
# - Logo content (eclipse highlights, parchment wordmark) starts around lum 55+.
# - Soft ramp avoids visible halos along anti-aliased edges.
RAMP_LO = 32
RAMP_HI = 55


def mask_logo(src_path: str, out_b64_path: str) -> tuple[int, int, int]:
    """Mask the dark background of `src_path` and write the base64 PNG to
    `out_b64_path`. Returns (width, height, output_byte_count_base64)."""
    img = Image.open(src_path).convert('RGB')
    arr = np.array(img)
    lum = arr.max(axis=2).astype(np.int16)
    alpha = np.clip(
        (lum - RAMP_LO) * (255.0 / (RAMP_HI - RAMP_LO)), 0, 255
    ).astype(np.uint8)

    rgba = np.dstack([arr, alpha])
    out_img = Image.fromarray(rgba, mode='RGBA')

    buf = io.BytesIO()
    out_img.save(buf, 'PNG', optimize=True)
    raw = buf.getvalue()
    b64 = base64.b64encode(raw).decode('ascii')

    os.makedirs(os.path.dirname(out_b64_path), exist_ok=True)
    with open(out_b64_path, 'w') as f:
        f.write(b64)

    return img.size[0], img.size[1], len(b64)


def main() -> None:
    print('Rebuilding masked-background brand logos')
    print('=' * 48)
    targets = [
        ('logo-horizontal.png',    'horizontal-b64.txt'),
        ('logo-horizontal-sm.png', 'horizontal_sm-b64.txt'),
    ]
    for src_name, out_name in targets:
        src = os.path.join(_RAW, src_name)
        dst = os.path.join(_DATA, out_name)
        w, h, n = mask_logo(src, dst)
        print(f'  {src_name:24s} -> {out_name:24s}  {w}x{h}  ({n / 1024:.1f} KB base64)')
    print('Done. Rebuild the HTML pages (e.g. python3 build_all.py) to pick these up.')


if __name__ == '__main__':
    main()

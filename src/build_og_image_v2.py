#!/usr/bin/env python3
"""Build the 1200×630 Open Graph image for Rogue Night (v2 — feat. agents).

Replaces the previous logo-only OG with a brand-rich composite:
- Background: the outcomes-relaxed.jpg (human + working AI agents)
- Right side: dark gradient overlay for text legibility
- Foreground text: AI & Automation Strategy headline + $395 / 48 hours

No numpy dependency — pure PIL.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_SCRIPT_DIR, 'data')
_FONTS = os.path.join(_DATA, 'fonts')
_PUBLIC_IMG = os.path.join(_SCRIPT_DIR, '..', 'public', 'images')

INK = (10, 14, 26)
OBSIDIAN = (5, 6, 8)
GOLD = (201, 169, 97)
EMBER = (194, 65, 12)
PARCHMENT = (237, 232, 221)
SLATE = (107, 114, 128)
PARCHMENT_DIM = (200, 195, 184)

W, H = 1200, 630

F = lambda path, size: ImageFont.truetype(os.path.join(_FONTS, path), size)

# --- 1. base photo: outcomes-relaxed cropped to 1200×630 -----------
src = Image.open(os.path.join(_PUBLIC_IMG, 'outcomes-relaxed.jpg')).convert('RGB')
# source is 1600×893 (16:9). target is 1200×630 (~1.9:1). Resize-to-cover then crop.
src_ratio = src.size[0] / src.size[1]
target_ratio = W / H
if src_ratio > target_ratio:
    # source wider — scale by height, crop width
    new_h = H
    new_w = int(src.size[0] * (H / src.size[1]))
    src = src.resize((new_w, new_h), Image.LANCZOS)
    crop_x = (new_w - W) // 2
    canvas = src.crop((crop_x, 0, crop_x + W, H))
else:
    # source taller — scale by width, crop height
    new_w = W
    new_h = int(src.size[1] * (W / src.size[0]))
    src = src.resize((new_w, new_h), Image.LANCZOS)
    crop_y = (new_h - H) // 4  # crop top-biased to keep faces
    canvas = src.crop((0, crop_y, W, crop_y + H))

# --- 2. dark gradient overlay on the right 60% of the frame --------
# Build a gradient mask: transparent on left, opaque-ish on right
overlay = Image.new('RGBA', (W, H), OBSIDIAN + (0,))
draw_o = ImageDraw.Draw(overlay)
for x in range(W):
    # opacity ramps from 0 at left to 0.78 at right, with most of the ramp in the right half
    t = max(0, (x - W * 0.32) / (W * 0.55))  # 0 below 0.32W, 1 above 0.87W
    t = max(0, min(1, t))
    alpha = int(t * 220)  # max 220/255 ≈ 86% opaque
    draw_o.line([(x, 0), (x, H)], fill=OBSIDIAN + (alpha,))

canvas_rgba = canvas.convert('RGBA')
canvas_rgba.alpha_composite(overlay)

# Additional global slight darken to bring text contrast (very subtle)
darken = Image.new('RGBA', (W, H), (0, 0, 0, 22))
canvas_rgba.alpha_composite(darken)
canvas = canvas_rgba.convert('RGB')
draw = ImageDraw.Draw(canvas)

# --- 3. fonts ------------------------------------------------------
sans_meta_sm = F('InstrumentSans-SemiBold.ttf', 14)
sans_meta_md = F('InstrumentSans-SemiBold.ttf', 18)
sans_body = F('InstrumentSans-Regular.ttf', 20)
serif_h1 = F('InstrumentSerif-Regular.ttf', 72)
serif_h1_italic = F('InstrumentSerif-Italic.ttf', 72)
serif_sub = F('InstrumentSerif-Regular.ttf', 30)

# --- 4. top bar: gold hairline + brand + url ----------------------
draw.rectangle([72, 76, 152, 78], fill=GOLD)
draw.text((72, 90), "ROGUE NIGHT", font=sans_meta_sm, fill=PARCHMENT)
draw.text((192, 90), "·   AI & AUTOMATION STRATEGY", font=sans_meta_sm, fill=GOLD)
url = "roguenight.com.au"
url_bbox = sans_meta_sm.getbbox(url)
url_w = url_bbox[2] - url_bbox[0]
draw.text((W - 72 - url_w, 90), url, font=sans_meta_sm, fill=GOLD)

# --- 5. headline block on the right --------------------------------
right_x = 560
# Line 1: "Run your business"
draw.text((right_x, 200), "Run your business", font=serif_h1, fill=PARCHMENT)
# Line 2: gold italic "smarter." (one word, big punch)
draw.text((right_x, 290), "smarter.", font=serif_h1_italic, fill=GOLD)
# Line 3: smaller serif tagline
draw.text((right_x, 400), "With systems that work — even when you don't.", font=serif_sub, fill=PARCHMENT_DIM)
# Line 4 (offset down): price + delivery
price_line = "$395  ·  Delivered in 48 hours  ·  Yours to keep"
draw.text((right_x, 470), price_line, font=sans_meta_md, fill=GOLD)

# --- 6. bottom hairline -------------------------------------------
draw.rectangle([0, H - 2, W, H], fill=GOLD)

# --- 7. save as JPEG (photo composite — PNG would be 7× larger) ---
out = os.path.join(_SCRIPT_DIR, 'og-image.jpg')
canvas.save(out, 'JPEG', quality=88, optimize=True, progressive=True)
size_kb = os.path.getsize(out) / 1024
print(f"OG image v2 written: {W}×{H} · {size_kb:.0f} KB · {out}")

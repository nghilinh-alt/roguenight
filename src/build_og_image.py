#!/usr/bin/env python3
"""Build the 1200x630 Open Graph image for Rogue Night."""
import os
from PIL import Image, ImageDraw, ImageFont

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_SCRIPT_DIR, 'data')
_FONTS = os.path.join(_DATA, 'fonts')

# Brand tokens
INK = (10, 14, 26)         # #0A0E1A
OBSIDIAN = (5, 6, 8)       # #050608
GOLD = (201, 169, 97)      # #C9A961
EMBER = (194, 65, 12)      # #C2410C
PARCHMENT = (237, 232, 221) # #EDE8DD
SLATE = (107, 114, 128)    # #6B7280

W, H = 1200, 630

# Canvas — solid Ink
canvas = Image.new('RGB', (W, H), INK)
draw = ImageDraw.Draw(canvas)

# Fonts
F = lambda path, size: ImageFont.truetype(os.path.join(_FONTS, path), size)
sans_meta = F('InstrumentSans-SemiBold.ttf', 14)
sans_reg = F('InstrumentSans-Regular.ttf', 14)
serif_reg = F('InstrumentSerif-Regular.ttf', 58)
serif_italic = F('InstrumentSerif-Italic.ttf', 58)

# === TOP NAV STRIPE ===
# Gold hairline divider near top-left
draw.rectangle([72, 68, 152, 69], fill=GOLD)
draw.text((72, 80), "ROGUE NIGHT", font=sans_meta, fill=PARCHMENT)
draw.text((192, 80), "·   CONSULTING", font=sans_meta, fill=SLATE)

# URL top-right
url_text = "roguenight.com.au"
url_w = sans_meta.getbbox(url_text)[2]
draw.text((W - 72 - url_w, 80), url_text, font=sans_meta, fill=GOLD)

# === LEFT — LOGO ===
# Load stacked logo. The PNG has near-Ink background baked in, which creates a
# visible rectangle on our canvas. Build a luminance mask so only the eclipse +
# wordmark show through, with the dark background blending fully into the canvas.
stacked = Image.open(os.path.join(_SCRIPT_DIR, '..', 'assets-raw', 'logo-stacked.png')).convert('RGB')
target_w = 380
ratio = target_w / stacked.size[0]
target_h = int(stacked.size[1] * ratio)
stacked = stacked.resize((target_w, target_h), Image.LANCZOS)

# Build a mask: pixels brighter than the Ink background pass through fully
import numpy as np
arr = np.array(stacked)
# Luminance proxy — max of channels is enough since brand colors are warm vs dark bg
lum = arr.max(axis=2).astype(np.int16)
# Background ~14 (max of Ink 10,14,26). Logo content (eclipse highlights, wordmark text) is much brighter.
# Smoothly fade between 18 (pure bg) and 50 (definitely content) to avoid hard edges
mask_arr = np.clip((lum - 18) * (255 / (50 - 18)), 0, 255).astype(np.uint8)
mask = Image.fromarray(mask_arr, mode='L')

lx = 88
ly = (H - target_h) // 2 + 10
canvas.paste(stacked, (lx, ly), mask)

# === RIGHT — HEADLINE ===
text_x = 540
# Two-line layout, vertically centered
# Line 1: "Run your business"
# Line 2: "smarter. Day and night."

line1 = "Run your business"
line2_smarter = "smarter."  # italic + gold
line2_rest = " Day and night."  # regular + parchment

line_height = 78  # leading
text_block_h = line_height * 2

# Measure block to vertically center
line1_h = serif_reg.getbbox(line1)[3] - serif_reg.getbbox(line1)[1]
text_y = (H - text_block_h) // 2 - 8  # nudge up slightly for visual balance

# Draw line 1
draw.text((text_x, text_y), line1, font=serif_reg, fill=PARCHMENT)

# Draw line 2 — "smarter." gold italic + " Day and night." parchment regular
y2 = text_y + line_height
draw.text((text_x, y2), line2_smarter, font=serif_italic, fill=GOLD)
smarter_w = serif_italic.getbbox(line2_smarter)[2]
draw.text((text_x + smarter_w, y2), line2_rest, font=serif_reg, fill=PARCHMENT)

# === BOTTOM STRIP ===
# Editorial position line + hairline divider
strip = "DIGITAL TRANSFORMATION   ·   AI-AMPLIFIED   ·   PRICED FOR SMALL BUSINESS"
strip_font = F('InstrumentSans-SemiBold.ttf', 12)
strip_w = strip_font.getbbox(strip)[2]
strip_x = (W - strip_w) // 2
strip_y = H - 80
draw.text((strip_x, strip_y), strip, font=strip_font, fill=SLATE)

# Small gold dot dividers — replace " · " with actual dots already in string
# (kept as part of the text — looks clean)

# Hairline divider above strip
div_w = 80
draw.rectangle([(W - div_w) // 2, strip_y - 24, (W + div_w) // 2, strip_y - 23], fill=GOLD)

# === SAVE ===
_OUT = os.path.join(_SCRIPT_DIR, 'og-image.jpg')
canvas.save(_OUT, 'PNG', optimize=True)

size_kb = os.path.getsize(_OUT) / 1024
print(f"OG image written: {W}x{H}, {size_kb:.1f}KB")

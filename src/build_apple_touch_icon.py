#!/usr/bin/env python3
"""Build the 180x180 apple-touch-icon.png from the eclipse logo on Ink background.

iOS adds rounded corners automatically, so we produce a flat square with the
eclipse centered with ~15% padding.
"""
import os
from PIL import Image
import numpy as np

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

INK = (10, 14, 26)
SIZE = 180
PADDING = int(SIZE * 0.12)  # 12% padding feels right against iOS rounded mask

# Load eclipse on its existing dark background
eclipse = Image.open(os.path.join(_SCRIPT_DIR, '..', 'assets-raw', 'logo-eclipse.png')).convert('RGB')

# Mask out the eclipse content from its baked Ink background, same as OG build
arr = np.array(eclipse)
lum = arr.max(axis=2).astype(np.int16)
mask_arr = np.clip((lum - 18) * (255 / (50 - 18)), 0, 255).astype(np.uint8)
mask = Image.fromarray(mask_arr).convert('L')

# Resize eclipse to fit within (SIZE - 2*PADDING)
target = SIZE - 2 * PADDING
eclipse_scaled = eclipse.resize((target, target), Image.LANCZOS)
mask_scaled = mask.resize((target, target), Image.LANCZOS)

# Build canvas
canvas = Image.new('RGB', (SIZE, SIZE), INK)
canvas.paste(eclipse_scaled, (PADDING, PADDING), mask_scaled)

_OUT = os.path.join(_SCRIPT_DIR, 'apple-touch-icon.png')
canvas.save(_OUT, 'PNG', optimize=True)

import os
size_kb = os.path.getsize(_OUT) / 1024
print(f"apple-touch-icon written: {SIZE}x{SIZE}, {size_kb:.1f}KB")

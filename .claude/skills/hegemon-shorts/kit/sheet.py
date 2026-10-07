#!/usr/bin/env python3
"""Contact sheet of test stills: python3 sheet.py [out.jpg] [dir]. Red line = caption height (~71% down)."""
from PIL import Image, ImageDraw
import glob, sys
out = sys.argv[1] if len(sys.argv) > 1 else 'contact.jpg'; d = sys.argv[2] if len(sys.argv) > 2 else 'test'
fs = sorted(glob.glob(f'{d}/*.jpg')); W, H, cols = 270, 480, 8; rows = (len(fs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * W, rows * H), 'black')
for i, f in enumerate(fs):
    im = Image.open(f).resize((W, H)); dr = ImageDraw.Draw(im); dr.line([(0, H * .71), (W, H * .71)], fill=(255, 0, 0)); dr.text((5, 5), str(i), fill=(255, 255, 0))
    sheet.paste(im, ((i % cols) * W, (i // cols) * H))
sheet.save(out); print(out, sheet.size)

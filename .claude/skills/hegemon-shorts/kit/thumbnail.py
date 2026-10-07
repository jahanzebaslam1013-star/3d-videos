#!/usr/bin/env python3
"""1080x1920 thumbnail from video frames.
  python3 thumbnail.py video.mp4 out.jpg --main 1.15 --line1 "11 DAYS" --line2 "NO SLEEP" [--inset 19.9] [--crop x0,y0,x1,y1] [--arrow x0,y0,x1,y1]
--main: time (s) of the hero frame (pick an emotional face). --inset: optional time of a detail frame shown in a red circle
(top-right) with an optional red arrow. Text: line1 big yellow, line2 white, both thick black outline, in the lower third."""
import argparse, subprocess, math, os, glob
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('out'); ap.add_argument('--main', type=float, required=True)
ap.add_argument('--line1', required=True); ap.add_argument('--line2', default=''); ap.add_argument('--inset', type=float)
ap.add_argument('--crop', default='60,330,1020,1290'); ap.add_argument('--arrow', default=''); ap.add_argument('--font', default=os.path.join(os.path.dirname(__file__), 'M900.ttf'))
a = ap.parse_args(); W, H = 1080, 1920
def frame(t, name):
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(t), '-i', a.video, '-frames:v', '1', '-q:v', '2', name], check=True); return Image.open(name).convert('RGB').resize((W, H))
if not os.path.exists(a.font):
    from fontTools.ttLib import TTFont
    src = glob.glob('node_modules/@fontsource/montserrat/files/montserrat-latin-900-normal.woff2')[0]; f = TTFont(src); f.flavor = None; f.save(a.font)
bg = frame(a.main, '_thumb_main.jpg')
bg = ImageEnhance.Brightness(bg).enhance(1.3); bg = ImageEnhance.Contrast(bg).enhance(1.15); bg = ImageEnhance.Color(bg).enhance(1.25)
grad = Image.new('L', (1, H)); [grad.putpixel((0, y), int(max(0, (y - 1050) / 870) * 235)) for y in range(H)]
bg = Image.composite(Image.new('RGB', (W, H), (5, 8, 20)), bg, grad.resize((W, H))); d = ImageDraw.Draw(bg)
if a.inset is not None:
    x0, y0, x1, y1 = map(int, a.crop.split(',')); br = frame(a.inset, '_thumb_inset.jpg').crop((x0, y0, x1, y1)).resize((430, 430))
    mask = Image.new('L', (430, 430), 0); ImageDraw.Draw(mask).ellipse((0, 0, 429, 429), fill=255); cx, cy, R = 800, 300, 215
    d.ellipse((cx - R - 22, cy - R - 22, cx + R + 22, cy + R + 22), fill=(0, 0, 0)); bg.paste(br, (cx - R, cy - R), mask)
    d.ellipse((cx - R - 8, cy - R - 8, cx + R + 8, cy + R + 8), outline=(230, 40, 40), width=16)
if a.arrow:
    ax0, ay0, ax1, ay1 = map(int, a.arrow.split(',')); d.line((ax0, ay0, ax1, ay1), fill=(230, 40, 40), width=28); ang = math.atan2(ay1 - ay0, ax1 - ax0); L = 80
    d.polygon([(ax1 + math.cos(ang) * 25, ay1 + math.sin(ang) * 25), (ax1 - math.cos(ang - .55) * L, ay1 - math.sin(ang - .55) * L), (ax1 - math.cos(ang + .55) * L, ay1 - math.sin(ang + .55) * L)], fill=(230, 40, 40))
def text(t, y, size, fill, stroke):
    f = ImageFont.truetype(a.font, size)
    while d.textlength(t, font=f) > W - 90: size -= 6; f = ImageFont.truetype(a.font, size)
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
text(a.line1, 1270, 250, (255, 210, 58), 18)
if a.line2: text(a.line2, 1530, 200, (255, 255, 255), 16)
bg.save(a.out, quality=95); [os.remove(f) for f in ('_thumb_main.jpg', '_thumb_inset.jpg') if os.path.exists(f)]; print(a.out)

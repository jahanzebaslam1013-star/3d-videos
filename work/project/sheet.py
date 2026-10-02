"""python3 sheet.py secN out_prefix [frac]  -> renders one frame per shot at frac through it, writes contact sheets"""
import sys, importlib, glob, os, subprocess
from PIL import Image, ImageDraw
mod = sys.argv[1]; pre = sys.argv[2]; frac = float(sys.argv[3]) if len(sys.argv) > 3 else 0.75
m = importlib.import_module(mod); import engine
TL = engine.timeline(m.SHOTS, m.LT, m.END)
ts = [round(a + (b - a) * frac, 2) for a, b, _ in TL]
for f in glob.glob('test_*.png'): os.remove(f)
subprocess.run(['python3', f'{mod}.py'] + [str(x) for x in ts], check=True)
fs = sorted(glob.glob('test_*.png'))
for k in range(0, len(fs), 12):
    grp = fs[k:k + 12]; sheet = Image.new('RGB', (3 * 640, 4 * 360))
    for i, f in enumerate(grp):
        im = Image.open(f).convert('RGB').resize((640, 360)); ImageDraw.Draw(im).text((8, 8), f[5:11], fill='yellow')
        sheet.paste(im, ((i % 3) * 640, (i // 3) * 360))
    sheet.save(f'../_previews/{pre}_{k // 12 + 1}.png')
for f in fs: os.remove(f)
print(ts)

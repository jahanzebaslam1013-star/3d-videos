"""DUNKI thumbnail 1920x1080 (+ 1280x720 copy): shocked Hamza, overloaded boat, red/black, big title."""
import math, cairo
import pk, stickkit as K
from pk import *
from sec1 import night_sea

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf); K.BOIL = 3
# left: night sea + boat
sky_grad(ctx, NIGHT1, NIGHT2, 0, 520); stars(ctx, 70, 4010, 0); waves(ctx, 520, 0.0)
boat(ctx, 560, 820, 1.25, 0.0, heads=150, tilt=-0.06)
radial(ctx, 1450, 540, 900, (0.85, 0.1, 0.08), 0.55)
ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.35, 0.02, 0.02, 0.35); ctx.fill()
# right: big shocked Hamza
hamza(ctx, 1450, 900, 2.9, expr='shock', legs=None, arms='tense', look=(-6, 0))
K.sweat(ctx, 1450 + 75 * 2.9, 900 - 140 * 2.9, 2.6)
# title
glow_text(ctx, 'POV: DUNKI', 560, 190, 230, 'Bebas Neue', (1, 1, 1), (1, 0.25, 0.2), rot=-0.04)
ctx.save(); ctx.translate(560, 380); ctx.rotate(-0.05)
shape(ctx, rect(-380, -70, 380, 70), hexc('ffd66a'), 6, 20000)
text(ctx, '25 LAKH KA SAFAR', 0, 32, 96, 'Bebas Neue', INK, anchor='c'); ctx.restore()
stamp(ctx, 'FULL GUARANTEE?', 1420, 160, 0, 1, 100, rot=0.1)
K.vignette(ctx, 0.5)
surf.write_to_png('../Dunki_thumbnail_1080.png')
from PIL import Image
Image.open('../Dunki_thumbnail_1080.png').convert('RGB').resize((1280, 720), Image.LANCZOS).save('../Dunki_thumbnail.jpg', quality=92)
print('ok')

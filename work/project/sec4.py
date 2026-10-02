"""DUNKI — Section 4 (part4.json, global lines 70-103). Ends with FIA fact card, closing lines, channel card, fade."""
import math, random
import pk, stickkit as K, engine
from pk import *
from engine import load_part
import sec1
from sec1 import busts_row, night_sea, dhaba
from sec2 import label, sparkle, map_base, pin, ease_in
from sec3 import ship, deck_crowd, shore

LT, DUR, FIRST = load_part('part4.json')
END = DUR + 3.6
A = lambda i: LT[i][0]
AF = lambda i, f: LT[i][0] + (LT[i][1] - LT[i][0]) * f
def stand(s, floor): return floor - 334 * s
def pop(t, t0, d=0.3): return ease_out_back((t - t0) / d) if t > t0 else 0

SEPIA = (0.55, 0.42, 0.25)
CHANNEL = 'DOODLE POV'          # placeholder until the logo exists

def bilal_thin(ctx, x, y, s, **kw):
    kw.setdefault('expr', 'sad')
    person(ctx, x, y, s, 'tee', 'slick', K.HAIR, glasses=None, width=0.82, color=hexc('6a6a66'), seed=kw.pop('seed', 3400), **kw)

def worker(ctx, x, y, s, **kw):
    person(ctx, x, y, s, 'tee', 'crew', hexc('6a4a2a'), color=hexc('d9773a'), seed=kw.pop('seed', 3800), **kw)

def kid(ctx, x, y, s, **kw):
    kw.setdefault('color', hexc('c9d8a0'))
    person(ctx, x, y, s, 'kameez', 'spiky_s', K.HAIR, width=0.85, seed=kw.pop('seed', 3900), **kw)

def car(ctx, x, base, s, col, seed=5000, shine=0.0):
    ctx.save(); ctx.translate(x, base); ctx.scale(s, s)
    shape(ctx, [(-260, -40), (-250, -100), (-140, -110), (-80, -170), (90, -170), (160, -110), (250, -96), (262, -40)], col, 5, seed)
    shape(ctx, [(-66, -158), (0, -158), (0, -112), (-120, -112)], hexc('a9d4e8'), 3, seed + 1)
    shape(ctx, [(14, -158), (82, -158), (138, -112), (14, -112)], hexc('a9d4e8'), 3, seed + 2)
    rough(ctx, [(-160, -80), (220, -80)], 3, seed + 3, (1, 1, 1), alpha=0.6)
    for wx in (-160, 160):
        shape(ctx, ell(wx, -30, 44, 44, 24), hexc('151518'), 4, seed + wx)
        shape(ctx, ell(wx, -30, 20, 20, 16), hexc('c8c8cc'), 3, seed + wx + 1)
    if shine > 0: sparkle(ctx, 60, -150, 40, shine)
    ctx.restore()

def tent(ctx, x, base, w, h, seed, col=hexc('eef0ea')):
    shape(ctx, [(x - w / 2, base), (x, base - h), (x + w / 2, base)], col, 5, seed)
    shape(ctx, [(x - w * 0.12, base), (x, base - h * 0.55), (x + w * 0.12, base)], hexc('5a5e62'), 3, seed + 1)

def camp(ctx, t, night=0.0):
    sky_grad(ctx, K.tint(hexc('b9d4e4'), NIGHT1, night), K.tint(hexc('eef2ea'), NIGHT2, night), 0, 700)
    if night > 0.5: stars(ctx, 50, 4020, t)
    shape(ctx, rect(-300, 700, W + 300, H + 300), K.tint(hexc('c9b48a'), hexc('3a3428'), night), 4, 12000)
    for k in range(6): tent(ctx, 120 + k * 340, 720, 300, 200, 12010 + k * 3, K.tint(hexc('eef0ea'), hexc('5a5e62'), night))
    for k in range(-1, 26): rough(ctx, [(k * 80, 560), (k * 80 + 4, 720)], 2, 12040 + k, K.tint(hexc('8a8f96'), hexc('2a2c30'), night))
    for k in range(3): rough(ctx, [(-300, 580 + k * 50), (W + 300, 586 + k * 50)], 2, 12070 + k, K.tint(hexc('8a8f96'), hexc('2a2c30'), night))

def gibberish(ctx, x0, y0, x1, y1, tail, t0, t):
    if t < t0: return
    bubble(ctx, x0, y0, x1, y1, tail, alpha=min(1, (t - t0) * 5))
    for k in range(3):
        rough(ctx, [(x0 + 50 + j * 24, (y0 + y1) / 2 - 30 + k * 34 + 8 * math.sin(j * 1.7 + k)) for j in range(int((x1 - x0 - 100) / 24))],
              4, 12100 + k, INK)

def photo_card(ctx, x, y, s, rot=0.0, seed=12200):
    """the fake 'life set' photo Hamza sends home"""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    shape(ctx, rect(-300, -230, 300, 230), (1, 1, 1), 5, seed)
    ctx.save(); ctx.rectangle(-280, -210, 560, 420); ctx.clip()
    sky_grad(ctx, hexc('7cc0ea'), hexc('d8eef8'), -210, 120)
    shape(ctx, rect(-300, 120, 300, 240), hexc('b8b0a0'), 3, seed + 1)
    car(ctx, 90, 170, 0.75, hexc('3a6ad0'), seed + 2, shine=0.8)
    hamza(ctx, -140, stand(0.62, 190), 0.62, expr='smile', arms='wave', look=(0, 0))
    ctx.restore(); ctx.restore()

# ---------------- shots ----------------
def sc_shipgo(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 480, 1.05)
    night_sea(ctx, t, horizon=380)
    u = ease_in(t / d)
    ship(ctx, lerp(1500, 1900, u), 390, lerp(0.3, 0.12, u), max(0, 1 - u * 1.1))
    deck_crowd(ctx, t, 760, 12, 11100, s=0.85, sp=170, expr='sad', arms='down')
    deck_crowd(ctx, t, 940, 9, 11200, s=1.0, sp=230, expr='sad', arms='down')
    ctx.restore()

def sc_faces(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.2 + 0.06 * t / d)
    sky_grad(ctx, NIGHT1, NIGHT2, 0, 900); stars(ctx, 40, 4021, t)
    busts_row(ctx, 620, 0.9, 6, 12300, t, xs=[160, 480, 800, 1120, 1440, 1760], expr='blank', look=(0, 3))
    saleem_x = 1120
    ctx.restore(); dark(ctx, 0.25)

def sc_storm(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 600, 1.05 + 0.05 * math.sin(t * 2))
    sky_grad(ctx, hexc('1a1e28'), hexc('3a4250'), 0, 600)
    waves(ctx, 520, t * 1.8, col=hexc('243a52'), rows=7, amp=40, spacing=70)
    boat(ctx, 960, 760 + 30 * math.sin(t * 2.2), 1.2, t * 1.8, tilt=0.12 * math.sin(t * 1.6), heads=120)
    ctx.restore()
    rng = random.Random(int(t * 12))
    for i in range(70):
        x = rng.uniform(-100, W + 100); y = rng.uniform(-100, H)
        rough(ctx, [(x, y), (x - 30, y + 90)], 2, 0, (0.8, 0.85, 0.95), alpha=0.35)
    if int(t * 3) % 7 == 0: dark(ctx, 0.3, (0.8, 0.85, 1.0))
    label(ctx, 'Tez hawa', 380, 140, pop(t, S.F(2, 0.25)), 66, seed=12400)
    label(ctx, 'Oonchi lehrein', 1500, 140, pop(t, S.F(2, 0.7)), 66, seed=12401)

def sc_tilt(ctx, t, d, S):
    tilt = 0.08 + 0.12 * ease_io(t / 1.5) + (0.18 * ease_io((t - S.F(3, 0.55)) / 1.0) if t > S.F(3, 0.55) else 0)
    ctx.save(); ctx.translate(960, 540); ctx.rotate(-tilt * 0.6); ctx.scale(1.15, 1.15); ctx.translate(-960, -540)
    sky_grad(ctx, hexc('1a1e28'), hexc('3a4250'), -300, 600)
    waves(ctx, 520, t * 2, col=hexc('243a52'), rows=7, amp=46, spacing=70)
    boat(ctx, 960, 760, 1.3, t * 2, tilt=tilt, heads=120)
    ctx.restore()
    dark(ctx, min(0.85, max(0, (t - (d - 1.0)) / 1.0)) if t > d - 1.0 else 0)

def sc_black(ctx, t, d, S):
    ctx.set_source_rgb(0, 0, 0); ctx.paint()

def sc_eyes(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('e8e4da')); ctx.paint()
    ctx.save(); cam(ctx, 960, 400, 3.0)
    hamza(ctx, 960, 620, 1.2, expr='closed' if t < S.F(5, 0.45) else 'worried', legs=None, look=(0, 0))
    ctx.restore()
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 1, 1, max(0, 1 - t / 1.2)); ctx.fill()

def tent_set(ctx, t, d, cx=960, cy=560, z=1.05):
    ctx.save(); cam(ctx, cx, cy, z)
    shape(ctx, rect(-300, -300, W + 300, H + 300), hexc('e6e2d6'), 0, 1)
    shape(ctx, [(-300, -300), (960, -40), (W + 300, -300)], hexc('cfcabb'), 4, 12500)
    shape(ctx, rect(-300, 820, W + 300, H + 300), hexc('b9b0a0'), 4, 12501)
    shape(ctx, rect(380, 760, 1260, 860), hexc('8a8f96'), 4, 12502)                 # cot
    for x in (420, 1220): rough(ctx, [(x, 860), (x, 960)], 6, 12503 + x)
    hamza(ctx, 760, 650, 1.0, expr='sad', legs=None, arms='clasp', look=(6, 0))
    shape(ctx, [(560, 700), (980, 690), (1000, 900), (540, 910)], hexc('6a7a5a'), 5, 12510)  # blanket
    for k in range(4): rough(ctx, [(570 + k * 110, 700), (560 + k * 110, 900)], 2, 12511 + k, hexc('5a6a4a'))
    worker(ctx, 1450, stand(1.05, 1000), 1.05, expr='smile', look=(-6, 0), arms='reachL')
    ctx.restore()

def sc_tent(ctx, t, d, S):
    tent_set(ctx, t, d, 960, 560, 1.0 + 0.08 * t / d)
    for i, (w_, f, x) in enumerate((('Ek kambal', 0.0, 380), ('Ek tent', 0.25, 960))):
        label(ctx, w_, x, 140, pop(t, S.F(6, f)), 64, seed=12520 + i)
    gibberish(ctx, 1180, 120, 1820, 330, (1420, 430), S.F(6, 0.6), t)

def sc_zinda(ctx, t, d, S):
    tent_set(ctx, t, d, 860, 560, 1.3)
    stamp(ctx, 'ZINDA', 1360, 300, S.F(7, 0.2), t, 200, rot=-0.12)

def sc_ask(ctx, t, d, S):
    tent_set(ctx, t, d, 760, 480, 1.7)
    usay(ctx, 'Saleem chacha?', 900, 90, 1460, 270, (860, 400), S.F(8, 0.55), t, 74)

def sc_cot(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 600, 1.0 + 0.12 * ease_io(t / d))
    shape(ctx, rect(-300, -300, W + 300, H + 300), hexc('e6e2d6'), 0, 1)
    shape(ctx, rect(-300, 820, W + 300, H + 300), hexc('b9b0a0'), 4, 12600)
    shape(ctx, rect(520, 700, 1400, 790), hexc('8a8f96'), 4, 12601)
    for x in (560, 1360): rough(ctx, [(x, 790), (x, 900)], 6, 12602 + x)
    shape(ctx, [(1040, 700), (1060, 610), (1200, 600), (1230, 700)], hexc('6a5a4a'), 4, 12610)      # small bag
    rough(ctx, [(1080, 612), (1110, 570), (1160, 568), (1180, 604)], 4, 12611)
    ctx.restore()
    dark(ctx, 0.1)

def sc_lights(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('0a0d14')); ctx.paint()
    rng = random.Random(12700); keep = set(rng.sample(range(400), 36))
    fade_t = S.F(10, 0.5)
    for i in range(400):
        x = 260 + (i % 25) * 58; y = 200 + (i // 25) * 46
        a = 1.0 if i in keep else max(0, 1 - (t - fade_t - rng.uniform(0, 1.6)) / 0.6) if t > fade_t else 1.0
        if a > 0.01: radial(ctx, x, y, 16, (1, 0.85, 0.5), 0.9 * a)
    label(ctx, '400 mein se...', 960, 120, pop(t, 0.2), 70, seed=12710)
    if t > S.F(10, 0.75): label(ctx, 'sirf chand darjan', 960, 1000, pop(t, S.F(10, 0.75)), 70, col=hexc('c0322a'), seed=12711)

def sc_queue(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.05 + 0.06 * t / d)
    camp(ctx, t)
    shape(ctx, rect(1560, 520, 1760, 1000), hexc('3a6ad0'), 5, 12800)                # phone booth
    shape(ctx, rect(1590, 560, 1730, 700), hexc('a9d4e8'), 3, 12801)
    text(ctx, 'PHONE', 1660, 760, 50, 'Bebas Neue', (1, 1, 1), anchor='c')
    for i in range(9):
        x = 1440 - i * 170
        person(ctx, x, stand(0.8, 1000), 0.8, 'kameez', ['short', 'crew', 'slick', 'spiky_s'][i % 4], K.HAIR, expr='sad',
               color=[hexc('8a6a4a'), hexc('6b7a8a'), BLUEK, hexc('5f6e45')][i % 4], seed=12810 + i * 9, look=(5, 0),
               back=False)
    ctx.restore()
    label(ctx, 'Lambi line', 480, 140, pop(t, S.F(11, 0.4)), 70, seed=12820)

def sc_call(ctx, t, d, S):
    ctx.save(); ctx.rectangle(0, 0, 960, H); ctx.clip()
    ctx.save(); ctx.translate(-400, 0); camp(ctx, t); ctx.restore()
    hamza(ctx, 480, 640, 1.3, expr='worried', legs=None, look=(4, 0),
          arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (60, 40), (40, -70))])
    phone(ctx, 480 + 1.3 * 50, 640 - 1.3 * 90, 0.33, rot=0.2, screen=hexc('e8f4ff'))
    ctx.restore()
    ctx.save(); ctx.rectangle(960, 0, 960, H); ctx.clip()
    ctx.save(); ctx.translate(480, 0); sec1.evening_yard(ctx, t, 0.0); ctx.restore()
    charpai(ctx, 1440, 980, 1.3)
    abba(ctx, 1440, 600, 1.05, expr='shock' if t > 1.0 else 'neutral', legs=None, look=(-4, 0),
         arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (60, 40), (40, -70))])
    phone(ctx, 1440 + 1.05 * 50, 600 - 1.05 * 90, 0.3, rot=0.2, screen=hexc('e8f4ff'))
    ctx.restore()
    rough(ctx, [(960, -20), (960, H + 20)], 10, 8300, (1, 1, 1))

def abba_yard(ctx, t, cx, cy, z, expr='sad', tear=True):
    ctx.save(); cam(ctx, cx, cy, z)
    sec1.evening_yard(ctx, t, 0.0); charpai(ctx, 960, 980, 1.5)
    abba(ctx, 960, 580, 1.2, expr=expr, legs=None, look=(0, 2), tear=tear,
         arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (60, 40), (40, -70))])
    phone(ctx, 960 + 1.2 * 50, 580 - 1.2 * 90, 0.32, rot=0.2, screen=hexc('e8f4ff'))
    ctx.restore()

def sc_cry(ctx, t, d, S):
    abba_yard(ctx, t, 960, 460, 1.4 + 0.25 * ease_io(t / d), 'sad', t > S.F(13, 0.2))
    label(ctx, 'Pehli dafa', 1500, 960, pop(t, S.F(13, 0.65)), 66, seed=12900)

def sc_abba_says(ctx, t, d, S):
    abba_yard(ctx, t, 960, 520, 1.25 + 0.05 * t / d, 'sad', True)
    usay(ctx, 'Beta, zameen gayi, dukaan gayi... koi baat nahi.', 100, 50, 900, 300, (760, 420), S.F(14, 0.02), t, 58)
    usay(ctx, 'Tu zinda hai. Bas wapas aa ja.', 1060, 60, 1820, 260, (1150, 380), S.F(14, 0.55), t, 64)

def sc_boy(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.05 + 0.15 * ease_io(t / d))
    camp(ctx, t)
    turn = t > S.F(16, 0.3)
    bilal_thin(ctx, 1200, stand(1.1, 1000), 1.1, back=not turn, look=(-6, 0), expr='sad')
    hamza(ctx, 600, stand(1.1, 1000), 1.1, expr='shock' if turn else 'neutral', look=(6, 0))
    ctx.restore()
    if S.F(15, 0.55) < t < A(16) + 0.2: label(ctx, 'Pakistani. 3 saal se yahin.', 1300, 140, pop(t, S.F(15, 0.55)), 62, seed=13000)

def sc_twist(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('2a0f0f')); ctx.paint(); radial(ctx, 960, 520, 900, (0.9, 0.3, 0.2), 0.3)
    s = 2.6 + 0.15 * ease_io(t / d)
    bilal_thin(ctx, 960, 700 + 110 * (s - 2.6), s, legs=None, expr='sad', look=(0, 3))
    p = pop(t, 0.1)
    glow_text(ctx, 'BILAL', 960, 150, 170, 'Bebas Neue', (1, 1, 1), (1, 0.3, 0.3), pop=p)

def sc_mapx(ctx, t, d, S):
    z = 1.6 - 0.2 * ease_io(t / d)
    ctx.save(); cam(ctx, 700, 360, z)
    map_base(ctx, 0.0)
    pin(ctx, 700, 225, 1, col=hexc('9aa0a6'), seed=6420)
    text(ctx, 'ITALY', 820, 200, 54, 'Bebas Neue', hexc('6a6e74'), anchor='c')
    pin(ctx, 620, 450, 1, seed=6412)
    ctx.restore()
    xp = pop(t, S.F(18, 0.45))
    if xp > 0.01:
        ctx.save(); ctx.translate(700, 360 + (180 - 360) * z); ctx.scale(xp, xp)
        rough(ctx, [(-120, -120), (120, 120)], 22, 13100, hexc('c0322a')); rough(ctx, [(120, -120), (-120, 120)], 22, 13101, hexc('c0322a'))
        ctx.restore()
    label(ctx, 'Kabhi pohncha hi nahi', 960, 980, pop(t, S.F(18, 0.6)), 68, col=hexc('c0322a'), seed=13110)

def sc_carwash(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.1)
    sky_grad(ctx, hexc('b9c4cc'), hexc('e6e8e4'), 0, 700)
    shape(ctx, rect(-300, 700, W + 300, H + 300), hexc('8a8f96'), 4, 13200)
    car(ctx, 1150, 940, 1.5, hexc('7a7e86'), 13210)
    sp = 40 * math.sin(t * 6)
    bilal_thin(ctx, 560, stand(1.1, 1000), 1.1, look=(6, 0),
               arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (170, 60 + sp * 0.3), (260, 40 + sp))])
    shape(ctx, ell(560 + 1.1 * 270, stand(1.1, 1000) + 1.1 * (40 + sp), 34, 24, 14), hexc('f0d24a'), 3, 13220)     # sponge
    shape(ctx, [(300, 1000), (290, 900), (410, 900), (400, 1000)], hexc('3a6ad0'), 4, 13221)                         # bucket
    rng = random.Random(13230)
    for i in range(14):
        u = (t * 0.5 + i / 14) % 1
        shape(ctx, ell(900 + rng.uniform(0, 600), 780 - u * 300, 14 + 8 * rng.random(), 14 + 8 * rng.random(), 12), (1, 1, 1), 2, 13231 + i, alpha=0.7 * (1 - u))
    ctx.restore()
    label(ctx, 'Car wash', 480, 140, pop(t, S.F(19, 0.25)), 66, seed=13240)
    label(ctx, 'Bina papers', 1440, 140, pop(t, S.F(19, 0.75)), 66, col=hexc('c0322a'), seed=13241)

def sit_two(ctx, t, cx, cy, z, night=0.0, bexpr='sad', hexpr='worried', glum=False):
    ctx.save(); cam(ctx, cx, cy, z)
    camp(ctx, t, night)
    shape(ctx, rect(560, 820, 1360, 870), hexc('6a5a4a'), 4, 13300)                  # bench
    for x in (600, 1320): rough(ctx, [(x, 870), (x, 980)], 6, 13301 + x)
    hamza(ctx, 760, 640, 1.05, expr=hexpr, legs=None, arms='clasp', look=(6, 0))
    bilal_thin(ctx, 1160, 640, 1.05, expr=bexpr, legs=None, arms='clasp', look=(-6, 4) if glum else (-6, 0), headrot=0.1 if glum else 0)
    ctx.restore()

def sc_ask_car(ctx, t, d, S):
    sit_two(ctx, t, 760, 500, 1.5, hexpr='worried')
    usay(ctx, 'Aur woh laal gaari?', 140, 80, 780, 270, (620, 370), S.L(20)[0] + 0.1, t, 72)

def sc_flashback(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.05 + 0.05 * t / d)
    sky_grad(ctx, hexc('7cc0ea'), hexc('d8eef8'), 0, 800)
    for k, (x, c) in enumerate(((0, 'e8b04a'), (300, 'd9774a'), (620, 'f0d27a'), (940, 'c8603a'), (1260, 'e8b04a'), (1580, 'd9774a'))):
        shape(ctx, rect(x, 220 + (k % 2) * 50, x + 280, 820), hexc(c), 4, 13400 + k)
    shape(ctx, rect(-300, 820, W + 300, H + 300), hexc('b8b0a0'), 3, 13410)
    red_car(ctx, 1100, 990, 1.3)
    shoo = t > S.F(21, 0.6)
    bilal(ctx, 620, stand(1.05, 1000), 1.05, expr='smile' if not shoo else 'worried', arms='shrug', look=(4, 0))
    if t > S.F(21, 0.3):
        person(ctx, 1650, stand(1.05, 1000), 1.05, 'suit', 'short', K.HAIR, expr='stern', look=(-6, 0),
               arms='wave' if int(t * 4) % 2 else 'pointL', seed=13420)
    ctx.restore()
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(*SEPIA, 0.38); ctx.fill()
    if S.F(21, 0.1) < t: label(ctx, 'Customer ki thi', 480, 140, pop(t, S.F(21, 0.45)), 64, seed=13430)
    if t > S.F(21, 0.7): label(ctx, '2 minute ki photo', 1440, 140, pop(t, S.F(21, 0.7)), 64, col=hexc('c0322a'), seed=13431)
    text(ctx, 'FLASHBACK', 1760, 1040, 46, 'Bebas Neue', (1, 1, 1), anchor='c', alpha=0.7)

def sc_bilal_says(ctx, t, d, S):
    sit_two(ctx, t, 1160, 500, 1.6, bexpr='sad', glum=True)
    usay(ctx, 'Ghar walon ko kya batata? Ke sab kuch bech kar bhi... kuch nahi mila?', 1000, 50, 1880, 310, (1180, 400), S.L(22)[0] + 0.1, t, 60)

def sc_sit(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.0 + 0.05 * t / d)
    camp(ctx, t, 1.0); moon(ctx, 1500, 160, 44)
    ctx.push_group()
    shape(ctx, rect(560, 820, 1360, 870), hexc('1a1c20'), 4, 13300)
    hamza(ctx, 760, 640, 1.05, expr='sad', legs=None, arms='clasp', back=True)
    bilal_thin(ctx, 1160, 640, 1.05, legs=None, arms='clasp', back=True)
    ctx.pop_group_to_source(); ctx.paint()
    ctx.restore()
    dark(ctx, 0.25)

def sc_give(ctx, t, d, S):
    sit_two(ctx, t, 960, 520, 1.3, night=1.0, bexpr='neutral', hexpr='sad')
    g = ease_io(min(1, max(0, (t - S.F(24, 0.2)) / 0.8)))
    phone(ctx, lerp(1110, 960, g) * 1.3 - 960 * 0.3, (650 + 0) * 1.3 - 520 * 0.3, 0.42, rot=0.2, screen=hexc('e8f4ff'))
    radial(ctx, lerp(1110, 960, g) * 1.3 - 960 * 0.3, 650 * 1.3 - 520 * 0.3, 160, (0.6, 0.8, 1.0), 0.3)
    usay(ctx, 'Ghar walon ko ek photo bhej do. Unhein tasalli ho jayegi.', 980, 50, 1840, 300, (1200, 380), S.F(24, 0.45), t, 58)

def sc_gate(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.05 + 0.06 * t / d)
    camp(ctx, t)
    shape(ctx, rect(300, 360, 360, 1000), hexc('5a5e62'), 4, 13500); shape(ctx, rect(1560, 360, 1620, 1000), hexc('5a5e62'), 4, 13501)
    shape(ctx, rect(300, 330, 1620, 400), hexc('5a5e62'), 4, 13502)
    text(ctx, 'CAMP', 960, 385, 60, 'Bebas Neue', (1, 1, 1), anchor='c')
    car(ctx, lerp(2300, -400, t / d), 1010, 1.4, hexc('3a6ad0'), 13510, shine=0.8)
    hamza(ctx, 960, stand(1.1, 960), 1.1, expr='neutral', look=(4, 0))
    ctx.restore()

def sc_click(ctx, t, d, S):
    tc = S.F(26, 0.75)
    if t < tc + 0.05:
        ctx.save(); cam(ctx, 960, 520, 1.25 + 0.15 * ease_io(t / max(tc, 0.1)))
        camp(ctx, t)
        car(ctx, 1260, 1000, 1.3, hexc('3a6ad0'), 13510, shine=0.8 if t > 0.5 else 0)
        hamza(ctx, 760, stand(1.1, 990), 1.1, expr='smile' if t > S.F(26, 0.15) else 'neutral', arms='wave', look=(0, 0))
        ctx.restore()
        ctx.set_source_rgba(0, 0, 0, 0.6); ctx.set_line_width(6)
        for (x, y, sx, sy) in ((120, 120, 1, 1), (1800, 120, -1, 1), (120, 960, 1, -1), (1800, 960, -1, -1)):
            ctx.move_to(x, y + sy * 90); ctx.line_to(x, y); ctx.line_to(x + sx * 90, y); ctx.set_source_rgb(1, 1, 1); ctx.stroke()
    else:
        u = ease_io(min(1, (t - tc) / 1.0))
        ctx.set_source_rgb(*hexc('1a1d24')); ctx.paint()
        photo_card(ctx, 960, 520, lerp(3.2, 1.6, u), rot=lerp(0, -0.05, u))
    fl = max(0, 1 - abs(t - tc) / 0.25)
    if fl > 0: ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 1, 1, fl); ctx.fill()
    if tc - 0.2 < t < tc + 0.8: text(ctx, 'CLICK', 1600, 200, 110, 'Bebas Neue', INK if t > tc + 0.1 else (1, 1, 1), anchor='c')

def sc_pull(ctx, t, d, S):
    u = ease_io(t / d)
    ctx.save(); cam(ctx, lerp(620, 1640, u), lerp(450, 420, u), lerp(2.2, 1.2, min(1, u * 2)) if u < 0.5 else lerp(1.2, 2.4, (u - 0.5) * 2))
    map_base(ctx, 0.0)
    pin(ctx, 620, 450, 1, seed=6412); pin(ctx, 1640, 430, 1, seed=6400, name='PUNJAB')
    ctx.set_source_rgb(*hexc('c0322a')); ctx.set_line_width(7); ctx.set_dash([22, 16])
    ctx.move_to(620, 390); ctx.curve_to(900, 200, 1400, 200, lerp(620, 1640, min(1, u * 1.3)), lerp(390, 370, u)); ctx.stroke(); ctx.set_dash([])
    ctx.restore()
    label(ctx, 'Hazaron meel door...', 960, 980, pop(t, 0.3), 70, seed=13600)

def sc_teen(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('0d1018')); ctx.paint()
    radial(ctx, 960, 760, 700, (0.45, 0.65, 1.0), 0.4 + 0.03 * math.sin(t * 5))
    s = 2.6 + 0.25 * ease_io(t / d)
    kid(ctx, 700, 560 + 150 * (s - 2.6), s * 0.9, expr='blank' if t < S.F(29, 0.3) else 'smile', legs=None, look=(4, 6),
        arms=[((-68, 44), (-60, 170), (10, 200)), ((68, 44), (60, 170), (20, 200))])
    ctx.save(); ctx.translate(1380, 600); ctx.rotate(0.08)
    shape(ctx, rect(-230, -400, 230, 400), hexc('1a1a1e'), 6, 13700)
    shape(ctx, rect(-206, -370, 206, 370), hexc('e8f4ff'), 0, 0)
    shape(ctx, rect(-206, -370, 206, -300), hexc('2f6e4f'), 0, 0)
    text(ctx, 'Hamza bhai', -180, -322, 40, 'Patrick Hand', (1, 1, 1))
    photo_card(ctx, 0, -20, 0.62)
    ctx.restore()
    dark(ctx, 0.1)
    if t > S.F(29, 0.05):
        p = pop(t, S.F(29, 0.05))
        ctx.save(); ctx.translate(560, 170); ctx.scale(p, p)
        for k, (dx, dy, r) in enumerate(((-40, 150, 16), (-10, 110, 24))): shape(ctx, ell(dx, dy, r, r, 14), (1, 1, 1), 3, 13710 + k)
        shape(ctx, ell(0, 0, 400, 90, 40), (1, 1, 1), 4, 13712)
        utext(ctx, 'Hamza bhai ki to life set hai.', 0, -22, 64, INK); ctx.restore()

def sc_agent_end(ctx, t, d, S):
    ctx.save(); cam(ctx, 900, 600, 1.0 + 0.12 * ease_io(t / d))
    dhaba(ctx, t)
    charpai(ctx, 1050, 960, 1.4)
    agent(ctx, 1050, 560, 1.15, expr='smile', legs=None,
          arms=[((-68, 44), (-120, 100), (-150, 40)), ((68, 44), (130, 100), (160, 40))], look=(-6, 0))
    for sx in (-1, 1): phone(ctx, 1050 + sx * 175, 590, 0.32, rot=sx * 0.2)
    wu = ease_out(min(1, t / 2.6))
    kid(ctx, lerp(-150, 520, wu), stand(1.0, 1000), 1.0, expr='smile', walk=t * 9 if wu < 1 else None, look=(6, 0))
    ctx.restore()
    g = max(0, 1 - abs(t - S.F(30, 0.6)) / 0.4)
    radial(ctx, 1240, 640, 60, (1, 0.95, 0.6), 0.9 * g); sparkle(ctx, 1240, 640, 40, g)

def sc_fact(ctx, t, d, S):
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    a = min(1, t / 0.6)
    glow_text(ctx, '335', 960, 330, 260, 'Bebas Neue', (1, 1, 1), (0.6, 0.6, 0.6), pop=pop(t, S.F(31, 0.55)))
    ltext(ctx, 'FIA ke mutabiq, June 2023 se April 2026 tak', 960, 520, 64, (1, 1, 1), alpha=a)
    ltext(ctx, 'kam az kam 335 Pakistani is safar mein', 960, 610, 64, (1, 1, 1), alpha=min(1, max(0, (t - S.F(31, 0.4)) / 0.6)))
    ltext(ctx, 'apni jaan kho baithe.', 960, 700, 64, (1, 1, 1), alpha=min(1, max(0, (t - S.F(31, 0.75)) / 0.6)))
    ltext(ctx, 'Source: FIA via ProPakistani, July 2026', 960, 960, 38, (0.6, 0.6, 0.6), alpha=a)

def sc_close1(ctx, t, d, S):
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    ltext(ctx, 'Har photo ke peeche ek kahani hoti hai.', 960, 500, 84, (1, 1, 1), alpha=min(1, max(0, (t - S.L(32)[0]) / 0.6)))

def sc_close2(ctx, t, d, S):
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    l0 = S.L(33)[0]; le = S.L(33)[1]
    a = min(1, max(0, (t - l0) / 0.6)) * (1 - min(1, max(0, (t - le - 0.2) / 0.4)))
    ltext(ctx, 'Aur kuch kahaniyan...', 960, 440, 84, (1, 1, 1), alpha=a)
    ltext(ctx, 'kabhi post nahi hotin.', 960, 560, 84, (1, 1, 1), alpha=a * min(1, max(0, (t - S.F(33, 0.4)) / 0.5)))
    lg = le + 0.6
    if t > lg:
        p = pop(t, lg, 0.4); b = 1 - min(1, max(0, (t - (d - 0.7)) / 0.6))
        glow_text(ctx, CHANNEL, 960, 520, 150, 'Bebas Neue', (1, 1, 1), (1, 0.3, 0.3), pop=p, alpha=b)

SHOTS = [(0, sc_shipgo), (1, sc_faces), (2, sc_storm), (3, sc_tilt), (4, sc_black), (5, sc_eyes), (6, sc_tent), (7, sc_zinda),
         (8, sc_ask), (9, sc_cot), (10, sc_lights), (11, sc_queue), (12, sc_call), (13, sc_cry), (14, sc_abba_says),
         (15, sc_boy), (17, sc_twist), (18, sc_mapx), (19, sc_carwash), (20, sc_ask_car), (21, sc_flashback),
         (22, sc_bilal_says), (23, sc_sit), (24, sc_give), (25, sc_gate), (26, sc_click), (27, sc_pull), (28, sc_teen),
         (30, sc_agent_end), (31, sc_fact), (32, sc_close1), (33, sc_close2)]

if __name__ == '__main__': engine.run(SHOTS, LT, END)

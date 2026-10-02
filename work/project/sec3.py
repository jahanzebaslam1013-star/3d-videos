"""DUNKI — Section 3 (part3.json, global lines 48-69). Roman Urdu on screen, no captions."""
import math, random
import pk, stickkit as K, engine
from pk import *
from engine import load_part
import sec1
from sec1 import busts_row, shop, night_sea
from sec2 import warehouse, saleem, label, sparkle, ease_in

LT, DUR, FIRST = load_part('part3.json')
END = DUR + 0.6
A = lambda i: LT[i][0]
AF = lambda i, f: LT[i][0] + (LT[i][1] - LT[i][0]) * f
def stand(s, floor): return floor - 334 * s
def pop(t, t0, d=0.3): return ease_out_back((t - t0) / d) if t > t0 else 0

def timer(ctx, ta, x, y):
    """continues the section-2 phone timer: 1:49 at 0 -> 0:00 at line 4"""
    t1 = A(4) + 0.3
    left = max(0, 109 * (1 - ta / t1)) if ta < t1 else 0
    ctx.save(); ctx.translate(x, y)
    shape(ctx, rect(-170, -62, 170, 62), hexc('17171a'), 4, 6100, ink=(1, 1, 1))
    col = hexc('ff5a4a') if (left < 15 and int(ta * 3) % 2) or left == 0 else (1, 1, 1)
    text(ctx, f'{int(left // 60)}:{int(left % 60):02d}', 0, 30, 96, 'Bebas Neue', col, anchor='c')
    ctx.restore()

def lender(ctx, x, y, s, **kw):
    person(ctx, x, y, s, 'kameez', 'slick', hexc('15151a'), beard='mous', glasses='round', waist=hexc('3a2a20'),
           color=hexc('d8d0bc'), width=1.2, seed=kw.pop('seed', 3700), **kw)

def keys(ctx, x, y, s, seed=9500):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rough(ctx, ell(0, 0, 22, 22, 20), 5, seed, hexc('c9a24a'), closed=True)
    for k, ang in enumerate((0.6, 1.2)):
        ctx.save(); ctx.rotate(ang)
        shape(ctx, rect(18, -6, 80, 6), hexc('d9b44a'), 3, seed + 1 + k)
        shape(ctx, rect(62, 6, 70, 18), hexc('d9b44a'), 2, seed + 3 + k)
        ctx.restore()
    ctx.restore()

def hold(ctx, t, glow=0.25):
    """below deck: dark wooden hold"""
    shape(ctx, rect(-300, -300, W + 300, H + 300), hexc('2a2018'), 0, 1)
    for k in range(-1, 16): rough(ctx, [(k * 140, -300), (k * 140 + 6, H + 300)], 3, 9600 + k, hexc('1e1610'))
    for k in range(5): rough(ctx, [(-300, 120 + k * 230), (W + 300, 130 + k * 230)], 4, 9620 + k, hexc('3a2c20'))
    ctx.move_to(860, -10); ctx.line_to(1060, -10); ctx.line_to(1260, 700); ctx.line_to(660, 700); ctx.close_path()
    ctx.set_source_rgba(0.85, 0.9, 1.0, glow * (0.8 + 0.2 * math.sin(t * 1.5))); ctx.fill()

def day_sea(ctx, t, sky=('9cc8e6', 'e3eef4'), horizon=520, sea='4f7fa8'):
    sky_grad(ctx, hexc(sky[0]), hexc(sky[1]), 0, horizon)
    waves(ctx, horizon, t, col=hexc(sea))

def ship(ctx, x, y, s, lit=1.0, seed=9700):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    shape(ctx, [(-420, -40), (380, -40), (440, -110), (-460, -110)], hexc('15181e'), 4, seed, ink=(0.3, 0.3, 0.35))
    shape(ctx, rect(-260, -230, 120, -110), hexc('15181e'), 4, seed + 1, ink=(0.3, 0.3, 0.35))
    shape(ctx, rect(-200, -300, -140, -230), hexc('15181e'), 3, seed + 2, ink=(0.3, 0.3, 0.35))
    rng = random.Random(seed)
    for i in range(46):
        lx = rng.uniform(-400, 400) if i < 30 else rng.uniform(-240, 100)
        ly = rng.uniform(-100, -60) if i < 30 else rng.uniform(-220, -130)
        radial(ctx, lx, ly, 14, (1, 0.9, 0.55), 0.9 * lit)
    radial(ctx, -170, -310, 40, (1, 0.3, 0.2), 0.8 * lit * (0.5 + 0.5 * math.sin(i)))
    ctx.restore()

def shore(ctx, t):
    night_sea(ctx, t, horizon=520)
    shape(ctx, [(-300, 860), (500, 800), (1200, 830), (W + 300, 790), (W + 300, H + 300), (-300, H + 300)], hexc('6a6050'), 4, 9800)

def truck(ctx, x, base, s, t, seed=9900):
    ctx.save(); ctx.translate(x, base); ctx.scale(s, s)
    shape(ctx, rect(-420, -330, 180, -60), hexc('4a5038'), 6, seed)           # cargo cover
    for k in range(5): rough(ctx, [(-400 + k * 120, -320), (-400 + k * 120, -70)], 3, seed + 1 + k, hexc('3a3f2a'))
    shape(ctx, [(180, -260), (330, -260), (380, -150), (380, -60), (180, -60)], hexc('6a6e62'), 6, seed + 10)
    shape(ctx, [(200, -240), (310, -240), (350, -160), (200, -160)], hexc('2a3038'), 3, seed + 11)
    for wx in (-300, 0, 280):
        shape(ctx, ell(wx, -50, 56, 56, 24), hexc('151518'), 5, seed + 20 + wx)
    radial(ctx, 420, -110, 260, (1, 0.95, 0.7), 0.6)
    ctx.restore()

def deck_crowd(ctx, t, y, n, seed, arms='tense', expr='worried', s=0.7, sp=None, shout=False):
    rng = random.Random(seed); sp = sp or W / n
    for i in range(n):
        x = i * sp + rng.uniform(-20, 20)
        col = rng.choice([BLUEK, hexc('8a6a4a'), hexc('5f6e45'), hexc('a8a29a'), hexc('6b7a8a'), KAMEEZ])
        a = arms
        if shout and i % 2 == 0: a = 'up' if int(t * 4 + i) % 2 else 'wave'
        person(ctx, x, y + 6 * math.sin(t * 3 + i), s, 'kameez', rng.choice(['short', 'spiky_s', 'crew', 'slick']), K.HAIR,
               expr=expr, legs=None, arms=a, color=col, seed=seed + i * 37, beard=rng.choice([None, None, 'mous', 'full']),
               look=(0, -4) if shout else (0, 2))

def note(ctx, x, y, s, a):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    shape(ctx, ell(0, 0, 16, 12, 12), INK, 0, 0, alpha=a)
    rough(ctx, [(14, 0), (14, -60), (36, -48)], 4, 9990, INK, alpha=a); ctx.restore()

# ---------------- shots ----------------
def call_split(ctx, t, S, hexpr='smile', aexpr='neutral', abba_zoom=1.0):
    ctx.save(); ctx.rectangle(0, 0, 960, H); ctx.clip()
    ctx.save(); ctx.translate(-300, 0); warehouse(ctx, t, beam=False); ctx.restore(); dark(ctx, 0.35)
    hamza(ctx, 480, 640, 1.3, expr=hexpr, legs=None, look=(4, 0),
          arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (60, 40), (40, -70))])
    phone(ctx, 480 + 1.3 * 50, 640 - 1.3 * 90, 0.33, rot=0.2, screen=hexc('e8f4ff'))
    ctx.restore()
    ctx.save(); ctx.rectangle(960, 0, 960, H); ctx.clip()
    ctx.save(); cam(ctx, 1440, 500, abba_zoom); ctx.translate(480, 0); shop(ctx, t, 0); ctx.restore()
    ctx.restore()
    rough(ctx, [(960, -20), (960, H + 20)], 10, 8300, (1, 1, 1))

def sc_lie(ctx, t, d, S):
    call_split(ctx, t, S, 'smile')
    usay(ctx, 'Abba ji, sab theek hai... bas thore se paise aur.', 60, 60, 900, 290, (500, 380), 0.3, t, 60)
    if t > S.F(0, 0.3): K.sweat(ctx, 560, 420, 1.8)
    timer(ctx, t + S.t0, 480, 960)

def sc_silence(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('8e6a48')); ctx.paint()
    ctx.save(); cam(ctx, 960, 440, 1.0 + 0.15 * ease_io(t / d))
    ctx.translate(0, 0); shop(ctx, t, 0)
    ctx.restore()
    dark(ctx, 0.25 * min(1, t / 1.5))
    for k in range(3):
        a = min(1, max(0, (t - 0.6 - k * 0.6) / 0.3))
        text(ctx, '.', 1260 + k * 50, 300, 160, 'Bebas Neue', (1, 1, 1), alpha=a)
    timer(ctx, t + S.t0, 1700, 110)

def sc_ok(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 400, 1.6); shop(ctx, t, 0); ctx.restore()
    dark(ctx, 0.2)
    usay(ctx, 'Theek hai beta. Ho jayega.', 160, 80, 860, 290, (880, 470), S.L(2)[0] + 0.05, t, 70)
    timer(ctx, t + S.t0, 1700, 110)

def sc_girvi(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.05 + 0.08 * t / d)
    shape(ctx, rect(-300, -300, W + 300, 760), hexc('c9b89a'), 0, 1)
    shape(ctx, rect(-300, 760, W + 300, H + 300), hexc('8a7058'), 4, 9510)
    shape(ctx, rect(200, 120, 900, 700), hexc('8e6a48'), 6, 9511)               # shop front behind
    shape(ctx, rect(220, 140, 880, 220), hexc('2f6e4f'), 3, 9512)
    text(ctx, 'Hamza General Store', 550, 200, 48, 'Patrick Hand', (1, 1, 1), anchor='c')
    shape(ctx, rect(230, 240, 870, 700), hexc('6a6e72'), 4, 9513)               # shutter down
    for k in range(8): rough(ctx, [(240, 270 + k * 55), (860, 270 + k * 55)], 3, 9514 + k, hexc('55595c'))
    tg = S.F(3, 0.3); u = ease_io((t - tg) / 0.8) if t > tg else 0
    abba(ctx, 860, stand(1.1, 1000), 1.1, expr='sad', look=(6, 2),
         arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (140, 110), (200 + 60 * u, 120))])
    lender(ctx, 1380, stand(1.1, 1000), 1.1, expr='smile', look=(-6, 2),
           arms=[((-68, 44), (-140, 110), (-200, 110)), ((68, 44), (90, 128), (86, 206))])
    keys(ctx, lerp(860 + 1.1 * 210, 1380 - 1.1 * 200, u), stand(1.1, 1000) + 1.1 * 120, 1.0)
    ctx.restore()
    stamp(ctx, 'GIRVI', 1500, 260, S.F(3, 0.62), t, 170, rot=-0.12)
    label(ctx, 'Dukaan bhi', 450, 900, pop(t, S.F(3, 0.5)), 66, col=hexc('c0322a'), seed=9520)

def sc_timeup(ctx, t, d, S):
    ctx.save(); cam(ctx, 900, 560, 1.25)
    warehouse(ctx, t)
    ts = S.F(4, 0.55); grab = ease_io((t - ts) / 0.3) if t > ts else 0
    hamza(ctx, 760, 620, 1.2, expr='sad', legs=None, look=(6, 2),
          arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (140, 110), (190, 80))])
    hx, hy = 760 + 1.2 * 190, 620 + 1.2 * 80
    out = ease_in((t - ts - 0.3) / 0.5) if t > ts + 0.3 else 0
    ax = lerp(2100, hx + 70, grab) if out == 0 else lerp(hx + 70, 2160, out)
    phone(ctx, (hx + 20) if out == 0 else lerp(hx + 20, 2100, out), hy - 40, 0.42, rot=0.15, screen=hexc('e8f4ff'))
    rough(ctx, [(2200, hy - 60), (ax + 40, hy - 40)], 34, 7600, hexc('23262c'))
    shape(ctx, ell(ax, hy - 40, 40, 30, 16), K.SKIN, 4, 7601)
    ctx.restore()
    timer(ctx, t + S.t0, 960, 160)
    label(ctx, 'Phone wapas', 960, 960, pop(t, ts + 0.3), 66, seed=9530)

def sc_wake(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.05 + 0.08 * t / d)
    warehouse(ctx, t, beam=False); dark(ctx, 0.55)
    tw = S.F(5, 0.35)
    up = t > tw
    busts_row(ctx, 760, 0.62, 12, 9600, t, xs=[i * 170 + 20 for i in range(12)], expr='shock' if up else 'closed')
    busts_row(ctx, 920, 0.8, 10, 9700, t, xs=[i * 210 - 60 for i in range(11)], expr='shock' if up else 'closed')
    ctx.restore()
    if up:
        for k in range(2):
            ang = math.sin(t * 2.2 + k * 2) * 0.5
            ctx.save(); ctx.translate(300 + k * 1300, -50); ctx.rotate(ang)
            ctx.move_to(-20, 0); ctx.line_to(20, 0); ctx.line_to(220, 1100); ctx.line_to(-220, 1100); ctx.close_path()
            ctx.set_source_rgba(1, 0.97, 0.8, 0.22); ctx.fill(); ctx.restore()
    usay(ctx, 'Chalo! Jaldi!', 700, 70, 1220, 250, (900, 330), S.F(5, 0.78), t, 84)
    if t < tw: label(ctx, 'Ek raat...', 960, 160, pop(t, 0.3), 70, seed=9540)

def sc_cuts(ctx, t, d, S):
    t1 = S.F(6, 0.32); t2 = S.F(6, 0.62)
    if t < t1:
        ctx.save(); cam(ctx, 960, 600, 1.0 + 0.1 * t / max(t1, 0.1))
        sky_grad(ctx, NIGHT1, NIGHT2, 0, 760); stars(ctx, 50, 4014, t)
        shape(ctx, rect(-300, 760, W + 300, H + 300), hexc('2a2a30'), 4, 9800)
        truck(ctx, lerp(500, 1300, t / max(t1, 0.1)), 900, 1.3, t)
        ctx.restore()
        label(ctx, 'Truck', 960, 160, pop(t, 0.15), 70, seed=9550)
    elif t < t2:
        ctx.set_source_rgb(0, 0, 0); ctx.paint()
        label(ctx, 'Andhera', 960, 540, pop(t, t1 + 0.15), 70, seed=9551)
    else:
        u = t - t2
        ctx.save(); cam(ctx, 960, 560, 1.0 + 0.04 * u); shore(ctx, t); ctx.restore()
        label(ctx, 'Samandar ka kinara', 960, 160, pop(t, t2 + 0.15), 70, seed=9552)

def sc_reveal(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 620, 1.0 + 0.25 * ease_io(t / d)); ctx.translate(-120 * ease_io(t / d), 0)
    shore(ctx, t)
    boat(ctx, 1100, 760, 1.1, t, crowd=False, seed=9810)
    busts_row(ctx, 980, 0.6, 9, 9820, t, xs=[i * 230 - 40 for i in range(10)], look=(4, -2))
    ctx.restore()
    dark(ctx, 0.1)
    for i, (w_, f) in enumerate((('Purani', 0.05), ('Zang lagi', 0.3), ('Bahut, bahut chhoti', 0.6))):
        label(ctx, w_, 380 + i * 560, 160 + (i % 2) * 70, pop(t, S.F(8, f)), 64,
                  col=hexc('c0322a') if i == 2 else hexc('17171a'), seed=9830 + i)

def sc_push(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 600, 1.05)
    shore(ctx, t)
    boat(ctx, 1650, 760, 0.9, t, crowd=True, heads=60, seed=9810)
    push = ease_io((t - S.F(9, 0.55)) / 0.6) if t > S.F(9, 0.55) else 0
    for r in range(3):
        for i in range(8):
            x = -200 + i * 190 + r * 60 + 160 * push + 30 * math.sin(t * 6 + i) * push
            person(ctx, x, stand(0.75 + r * 0.12, 900 + r * 70), 0.75 + r * 0.12, 'kameez', ['short', 'crew', 'spiky_s', 'slick'][(i + r) % 4],
                   K.HAIR, expr='shock' if push > 0.2 else 'worried', color=[BLUEK, hexc('8a6a4a'), hexc('5f6e45'), KAMEEZ][(i + r) % 4],
                   seed=9900 + r * 50 + i * 7, walk=t * 9 if push > 0 else None, look=(5, 0), rot=0.12 * push)
    ctx.restore()
    if push > 0:
        for k in range(3):
            x = 200 + k * 140 + 200 * push
            shape(ctx, [(x, 520), (x + 120, 560), (x, 600)], (1, 1, 1), 4, 9950 + k, alpha=0.8)
        text(ctx, 'DHAKKA!', 520, 380, 120, 'Bebas Neue', (1, 1, 1), anchor='c', alpha=min(1, push * 2))

def cross_section(ctx, t, glow_h=1.0):
    day_sea(ctx, t, sky=('1c2236', '3a4560'), horizon=420, sea='223a55')
    ctx.save(); ctx.translate(960, 560); ctx.rotate(0.012 * math.sin(t * 1.3)); ctx.translate(-960, -560)
    # hull cut-away
    shape(ctx, [(120, 380), (1800, 380), (1640, 880), (320, 880)], hexc('6b4a35'), 7, 9960)
    shape(ctx, [(170, 420), (1760, 420), (1615, 840), (345, 840)], hexc('1a140e'), 4, 9961)
    deck_crowd(ctx, t, 300, 16, 9970, s=0.55, sp=105)
    rng = random.Random(9980)
    for i in range(34):                                                         # crammed hold
        x = 360 + (i % 17) * 75 + rng.uniform(-8, 8); y = 600 + (i // 17) * 140
        shape(ctx, ell(x, y + 40, 26, 34, 12), hexc('3a3a40'), 2, 9981 + i)
        shape(ctx, ell(x, y, 22, 24, 14), tuple(c * 0.55 for c in K.SKIN), 2.5, 9990 + i)
    ctx.restore()

def sc_hold(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 600, 1.0 + 0.25 * ease_io(t / d))
    cross_section(ctx, t)
    hamza(ctx, 960, 690, 0.42, expr='worried', legs=None, arms='tense', look=(0, -2))
    ctx.restore()
    label(ctx, 'Neeche', 960, 140, pop(t, S.F(10, 0.15)), 70, seed=10000)
    label(ctx, 'Hawa kam', 480, 960, pop(t, S.F(10, 0.6)), 64, seed=10001)
    label(ctx, 'Roshni nahi', 1440, 960, pop(t, S.F(10, 0.85)), 64, col=hexc('c0322a'), seed=10002)

def sc_squeeze(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.1 + 0.05 * t / d)
    hold(ctx, t)
    busts_row(ctx, 760, 0.7, 10, 10100, t, xs=[i * 200 - 60 for i in range(11)], expr='sad')
    sx = lerp(1500, 1180, ease_out(min(1, t / 0.9)))
    hamza(ctx, 760, 680, 1.15, expr='worried', legs=None, arms='tense', look=(6, 0))
    saleem(ctx, sx, 680, 1.15, expr='smile', legs=None, arms='clasp', look=(-6, 0))
    ctx.restore()
    dark(ctx, 0.15)

def sc_day1(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.05)
    day_sea(ctx, t)
    radial(ctx, 1600, 140, 200, (1, 0.95, 0.6), 0.6); shape(ctx, ell(1600, 140, 60, 60, 24), hexc('ffe08a'), 3, 10200)
    shape(ctx, [(-100, 760), (2020, 760), (1900, 1200), (0, 1200)], hexc('6b4a35'), 6, 10201)
    deck_crowd(ctx, t, 680, 12, 10210, arms='up' if int(t * 2) % 2 else 'shrug', expr='smile', s=0.8, sp=170)
    ctx.restore()
    rng = random.Random(10220)
    for i in range(10):
        u = (t * 0.6 + i / 10) % 1
        note(ctx, rng.uniform(100, 1800), 560 - u * 380, 1.0, 1 - u)
    label(ctx, 'DIN 1', 200, 110, pop(t, 0.1), 80, seed=10230)
    usay(ctx, 'Italy! Italy!', 1220, 300, 1700, 470, (1300, 560), S.F(12, 0.55), t, 72)

def sc_day2(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('c9a77a')); ctx.paint(); radial(ctx, 960, 540, 800, (1, 0.9, 0.6), 0.3)
    ctx.save(); cam(ctx, 960, 560, 1.0 + 0.1 * t / d)
    lvl = 1 - ease_io(t / max(0.1, d - 0.4))
    x0, x1, y0, y1 = 780, 1140, 280, 960
    shape(ctx, [(x0, y1), (x0, 420), (900, 330), (900, y0), (1020, y0), (1020, 330), (x1, 420), (x1, y1)], (0.85, 0.92, 1.0), 6, 10300, alpha=0.5)
    wy = lerp(y1 - 10, 440, lvl)
    shape(ctx, rect(x0 + 10, wy, x1 - 10, y1 - 10), hexc('6aa8d8'), 0, 0, alpha=0.8)
    ctx.restore()
    label(ctx, 'DIN 2', 200, 110, pop(t, 0.1), 80, seed=10310)
    label(ctx, 'Paani khatam', 960, 1000, pop(t, S.F(13, 0.5)), 70, col=hexc('c0322a'), seed=10311)

def sc_argue(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.15)
    day_sea(ctx, t, sky=('d9a65a', 'f0d8a8'))
    shape(ctx, [(-100, 760), (2020, 760), (1900, 1200), (0, 1200)], hexc('6b4a35'), 6, 10401)
    for i, (x, hr, col) in enumerate(((560, 'short', hexc('8a6a4a')), (960, 'crew', hexc('6b7a8a')), (1360, 'slick', KAMEEZ))):
        person(ctx, x, 640, 1.0, 'kameez', hr, K.HAIR, expr='stern', legs=None, color=col, seed=10410 + i * 9,
               arms='pointR' if i == 0 else ('shrug' if i == 1 else 'pointL'), look=(4 if i == 0 else -4, 0))
    ctx.restore()
    usay(ctx, 'Ek ghoont!', 160, 120, 600, 290, (480, 380), S.F(14, 0.1), t, 70)
    usay(ctx, 'Meri baari!', 1320, 120, 1780, 290, (1440, 380), S.F(14, 0.4), t, 70)
    usay(ctx, 'Bas karo!', 740, 40, 1180, 200, (960, 300), S.F(14, 0.7), t, 66)

def sc_day3(ctx, t, d, S):
    tc = S.F(15, 0.8)
    if t < tc:
        ctx.save(); cam(ctx, 960, 620, 1.1)
        day_sea(ctx, t, sky=('5a6a80', '9aa6b4'), sea='3a5a78')
        sm = max(0, (t - S.F(15, 0.4)) / 1.5) if t > S.F(15, 0.4) else 0
        boat(ctx, 960, 790, 1.5, t, smoke=sm, heads=120)
        ctx.restore()
        label(ctx, 'DIN 3', 200, 110, pop(t, 0.1), 80, seed=10510)
        if t < S.F(15, 0.45):
            for k in range(3):
                a = max(0, math.sin(t * 14 + k))
                text(ctx, 'putt', 1480 + k * 70, 420 - k * 40, 46, 'Bebas Neue', (1, 1, 1), alpha=0.7 * a)
        else:
            stamp(ctx, 'ENGINE BAND', 1300, 300, S.F(15, 0.5), t, 110, rot=-0.1)
    else:
        sec1.sc_sea(ctx, 12.0 + (t - tc) * 0.5, 20.0, sec1.Sc(0))        # match cut to the cold open
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 1, 1, max(0, 1 - (t - tc) / 0.3)); ctx.fill()

def sc_rewind(ctx, t, d, S):
    sec1.sc_sea(ctx, 12.0 + 3 + t * 0.5, 20.0, sec1.Sc(0))
    vhs(ctx, t, max(0, 1 - t / 1.2))
    p = pop(t, S.F(16, 0.3))
    if p > 0.01:
        ctx.save(); ctx.translate(960, 900); ctx.scale(p, p)
        shape(ctx, rect(-560, -80, 560, 80), hexc('17171a'), 4, 10600, ink=(1, 1, 1))
        utext(ctx, 'Yahin se kahani shuru hui thi', 0, -30, 80, (1, 1, 1)); ctx.restore()
    if t < 1.2:
        for k in range(2):
            x = 160 + k * 70
            shape(ctx, [(x, 220), (x + 60, 260), (x, 300)], (1, 1, 1), 0, 0, alpha=0.9)
        text(ctx, 'PLAY', 320, 290, 80, 'Bebas Neue', (1, 1, 1))

def sc_wide(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.15 - 0.15 * ease_io(t / d))
    night_sea(ctx, t, horizon=460)
    boat(ctx, 960, 700, 0.45, t * 0.3, heads=140)
    ctx.restore()
    for i, (w_, f, x) in enumerate((('3:00 AM', 0.0, 360), ('400 log', 0.35, 960), ('Sirf paani', 0.7, 1560))):
        label(ctx, w_, x, 960, pop(t, S.F(17, f)), 70, col=hexc('17171a'), seed=10700 + i)

def sc_hands(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('101622')); ctx.paint(); radial(ctx, 960, 560, 800, (0.4, 0.5, 0.7), 0.3)
    ctx.save(); cam(ctx, 960, 600, 1.0 + 0.1 * t / d)
    g = ease_out(min(1, max(0, (t - S.F(18, 0.1)) / 0.8)))
    rough(ctx, [(-100, 760), (lerp(500, 780, g), 640)], 70, 10800, hexc('8a7a62'))      # Saleem's sleeve
    shape(ctx, ell(lerp(560, 840, g), 630, 90, 60, 20), tuple(c * 0.92 for c in K.SKIN), 5, 10801)
    rough(ctx, [(2020, 700), (1120, 640)], 70, 10802, BLUEK)
    shape(ctx, ell(1060, 640, 80, 56, 20), K.SKIN, 5, 10803)
    ctx.restore()
    usay(ctx, 'Beta, ghar walon ko yaad karo. Himmat milti hai.', 260, 60, 1200, 290, (600, 420), S.F(18, 0.45), t, 62)

def sc_photo(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('101822')); ctx.paint(); radial(ctx, 960, 520, 800, (0.4, 0.5, 0.7), 0.35)
    ctx.save(); cam(ctx, 960, 540, 1.0 + 0.12 * t / d)
    up = ease_out(min(1, t / 0.8)); y = lerp(900, 540, up)
    ctx.save(); ctx.translate(960, y); ctx.rotate(0.06)
    shape(ctx, rect(-260, -320, 260, 320), hexc('f6f2e6'), 5, 10900)
    shape(ctx, rect(-230, -290, 230, 210), hexc('c9b89a'), 2, 10901)
    ammi(ctx, 0, 60, 1.0, expr='smile', legs=None)
    shape(ctx, rect(-300, -360, 300, 360), (0.85, 0.92, 1.0), 4, 10902, alpha=0.25)
    rng = random.Random(10910)
    for i in range(22):
        x = rng.uniform(-260, 260); yy = rng.uniform(-330, 330) + (t * 30 * (i % 3)) % 60
        shape(ctx, ell(x, yy, 9, 13, 10), (0.8, 0.9, 1.0), 2, 10911 + i, alpha=0.6)
    ctx.restore(); ctx.restore()
    label(ctx, 'Geela', 1500, 200, pop(t, S.F(19, 0.65)), 70, seed=10950)

def sc_ship(ctx, t, d, S):
    ctx.save(); cam(ctx, 1300, 460, 1.0 + 0.35 * ease_io(t / d))
    night_sea(ctx, t, horizon=460)
    lit = min(1, max(0, (t - 0.3) / 1.0))
    ship(ctx, 1450, 470, 0.35 + 0.1 * ease_io(t / d), lit)
    ctx.restore()
    radial(ctx, 1450, 420, 300, (1, 0.9, 0.6), 0.15 * lit)
    label(ctx, 'Ek bohat bara jahaz', 960, 960, pop(t, S.F(20, 0.6)), 70, seed=11000)

def sc_wave(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.05)
    night_sea(ctx, t, horizon=380)
    ship(ctx, 1500, 390, 0.3, 1.0)
    radial(ctx, 1500, 360, 300, (1, 0.9, 0.6), 0.2)
    deck_crowd(ctx, t, 760, 12, 11100, s=0.85, sp=170, expr='shock', shout=True)
    deck_crowd(ctx, t, 940, 9, 11200, s=1.0, sp=230, expr='shock', shout=True)
    rng = random.Random(11300)
    for i in range(6):                                                           # shirts waving
        x = 150 + i * 320; y = 420 + 20 * math.sin(t * 8 + i)
        ctx.save(); ctx.translate(x, y); ctx.rotate(0.4 * math.sin(t * 9 + i))
        shape(ctx, [(-40, -30), (40, -30), (60, 0), (40, 0), (40, 50), (-40, 50), (-40, 0), (-60, 0)],
              rng.choice([hexc('d0302a'), (1, 1, 1), hexc('e8b04a')]), 3, 11310 + i); ctx.restore()
    ctx.restore()
    if t > 0.4: text(ctx, 'HELP!', 400, 200, 110, 'Bebas Neue', (1, 1, 1), anchor='c', alpha=0.6 + 0.4 * math.sin(t * 12))
    if t > 1.4: text(ctx, 'IDHAR!', 1000, 160, 100, 'Bebas Neue', (1, 1, 1), anchor='c', alpha=0.6 + 0.4 * math.sin(t * 12 + 1))

SHOTS = [(0, sc_lie), (1, sc_silence), (2, sc_ok), (3, sc_girvi), (4, sc_timeup), (5, sc_wake), (6, sc_cuts),
         (7, sc_reveal), (9, sc_push), (10, sc_hold), (11, sc_squeeze), (12, sc_day1), (13, sc_day2), (14, sc_argue),
         (15, sc_day3), (16, sc_rewind), (17, sc_wide), (18, sc_hands), (19, sc_photo), (20, sc_ship), (21, sc_wave)]

if __name__ == '__main__': engine.run(SHOTS, LT, END)

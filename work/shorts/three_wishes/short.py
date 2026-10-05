"""Three Wishes — ~52 s looping stickman reel. Ends walking down the same street, lamp ahead = first frame."""
import sys, math, random
sys.path.insert(0, '.')
from scenekit import *

HOOD = dict(outfit='hoodie')
GSKIN = hexc('6aa5e0')
X0, LAMPX = 320, 430                       # loop composition: hero x and lamp x on the street
WALK_K = round(END * 1.6)                  # whole walk cycles in the loop -> phase matches at the seam

def you(ctx, x, y, s, **kw):
    for k, v in HOOD.items(): kw.setdefault(k, v)
    hero(ctx, x, y, s, **kw)

def walk_phase(S, t): return 2 * math.pi * WALK_K * (S.t0 + t) / END

def lamp(ctx, x, y, s=1.0, rot=0.0, glow=0.0, alpha=1.0):
    if glow > 0: radial(ctx, x, y - 30 * s, 220 * s, (1, 0.85, 0.4), 0.5 * glow * alpha)
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    shape(ctx, [(-80, -10), (-120, -46), (-150, -52), (-130, -34), (-90, 4)], GOLD, 4, 7000, alpha=alpha)   # spout
    rough(ctx, ell(88, -24, 26, 22, 20, -1.6, 1.6), 7, 7001, hexc('a8842e'), alpha=alpha)                  # handle
    shape(ctx, ell(0, -20, 92, 34, 30), GOLD, 4, 7002, alpha=alpha)
    shape(ctx, ell(0, -54, 40, 14, 20), hexc('d9b45a'), 3, 7003, alpha=alpha)
    shape(ctx, ell(0, -72, 10, 10, 12), hexc('d9b45a'), 3, 7004, alpha=alpha)
    shape(ctx, rect(-30, 6, 30, 16), hexc('a8842e'), 3, 7005, alpha=alpha)
    rough(ctx, [(-50, -28), (-10, -36)], 3, 7006, (1, 0.95, 0.75), alpha=alpha * 0.8)
    ctx.restore()

def genie(ctx, x, y, s, tail=None, expr='smile', arms='clasp', **kw):
    if tail is not None:                                   # smoke tail from waist to the lamp spout
        wx, wy = x, y + 190 * s; tx, ty = tail
        pts = bez((wx - 70 * s, wy), (wx - 90 * s, wy + 160 * s), (tx - 60, ty - 80), (tx, ty), 16) + \
              bez((tx, ty), (tx + 40, ty - 120), (wx + 120 * s, wy + 160 * s), (wx + 70 * s, wy), 16)
        shape(ctx, pts, hexc('8fc4ee'), 4, 7100, alpha=0.95)
    person3(ctx, x, y, s, 'tee', 'none', HAIR, extra='bun', beard='mous', skin=GSKIN, color=hexc('7a3e9d'),
            width=1.25, seed=7200, legs=None, expr=expr, arms=arms, **kw)
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for sx in (-1, 1): shape(ctx, ell(sx * 60, -70, 8, 8, 10), GOLD, 2, 7210 + sx)          # earrings
    ctx.restore()

def puffs(ctx, x, y, t, n=9, r0=60, spread=260, col=(0.95, 0.96, 1.0), seed=7300):
    rng = random.Random(seed)
    for i in range(n):
        a = rng.uniform(0, 6.28); d = spread * ease_out(t * 1.6) * rng.uniform(0.4, 1.0)
        r = r0 * rng.uniform(0.7, 1.3) * (0.4 + ease_out(t * 2))
        al = max(0, 1 - t * 0.9)
        if al > 0: shape(ctx, ell(x + d * math.cos(a), y + d * math.sin(a) * 0.7, r, r, 20), col, 3, seed + i, alpha=al)

def money(ctx, x, y, s=1.0, rot=0.0, seed=7400):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    shape(ctx, rect(-60, -30, 60, 30), hexc('7bbf6a'), 3, seed)
    shape(ctx, ell(0, 0, 16, 16, 12), hexc('5a9e4c'), 2, seed + 1)
    text(ctx, '$', 0, 10, 28, 'Bebas Neue', hexc('2f5f28'), anchor='c')
    ctx.restore()

def money_rain(ctx, t, n=26, seed=3):
    rng = random.Random(seed)
    for i in range(n):
        x = rng.uniform(40, W - 40); sp = rng.uniform(250, 420)
        y = -80 + (t * sp + rng.uniform(0, 1500)) % 1600
        money(ctx, x + 30 * math.sin(t * 2 + i), y, 0.8, math.sin(t * 3 + i) * 0.6, 7450 + i)

def street(ctx):
    g = cairo.LinearGradient(0, 0, 0, 1330)
    g.add_color_stop_rgb(0, *hexc('3c3a6b')); g.add_color_stop_rgb(0.7, *hexc('c9767a')); g.add_color_stop_rgb(1, *hexc('eab07a'))
    ctx.rectangle(-300, -300, W + 600, 1700); ctx.set_source(g); ctx.fill()
    for k, (bx, bw, bh) in enumerate(((-20, 220, 620), (210, 180, 480), (400, 240, 700), (650, 200, 540), (860, 260, 650))):
        shape(ctx, rect(bx, 1330 - bh, bx + bw, 1330), hexc('2e2b45'), 4, 7500 + k)
        rng = random.Random(k)
        for wy in range(1330 - bh + 50, 1290, 90):
            for wx in range(bx + 30, bx + bw - 40, 60):
                if rng.random() < 0.45: shape(ctx, rect(wx, wy, wx + 30, wy + 40), hexc('f0c96a'), 0, 0)
    shape(ctx, rect(-300, 1330, W + 300, 2300), hexc('6e6b78'), 5, 7520)
    rough(ctx, [(-50, 1400), (W + 50, 1400)], 4, 7521, hexc('55525e'))
    rough(ctx, [(900, 1330), (900, 760)], 9, 7522, hexc('2a2833'))
    shape(ctx, [(860, 760), (940, 760), (925, 720), (875, 720)], hexc('2a2833'), 3, 7523)
    radial(ctx, 900, 780, 380, (1, 0.85, 0.5), 0.35)

def wish_card(ctx, t, num, wish, t0, t1):
    glow_text(ctx, f'WISH #{num}:', 540, 520, 130, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, t0))
    glow_text(ctx, wish, 540, 720, 150, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=pop(t, t1), rot=-0.04)

def magic_bg(ctx, t, col=hexc('2b1d47')):
    ctx.set_source_rgb(*col); ctx.paint(); ctx.new_path()
    radial(ctx, 540, 900, 900, (0.6, 0.4, 1.0), 0.3)
    rng = random.Random(9)
    for i in range(18):
        x, y = rng.uniform(60, 1020), rng.uniform(150, 1500)
        tw = 0.5 + 0.5 * math.sin(t * 4 + i)
        star(ctx, x, y, 10 + 8 * tw, GOLD, 7600 + i, alpha=0.4 + 0.5 * tw)

# ---------------- street (first + last shot) ----------------
def street_scene(ctx, hx, ph, expr, lamp_x, lamp_a=1.0, lamp_rot=0.0, lamp_y=1330, look=(4, 0)):
    street(ctx)
    if lamp_a > 0.01: lamp(ctx, lamp_x, lamp_y, 0.75, lamp_rot, alpha=lamp_a)
    you(ctx, hx, stand(1.1, 1360), 1.1, walk=ph, expr=expr, look=look)

def s_street(ctx, t, d, S):
    tk = 0.32
    hx = X0 + 170 * min(t, tk) + 60 * ease_out((t - tk) / 0.5) if t > tk else X0 + 170 * t
    ph = walk_phase(S, t) if t < tk + 0.4 else None
    if t < tk:
        lx, ly, lr = LAMPX, 1330, 0.0
    else:
        u = min(1, (t - tk) / 0.7)
        lx = lerp(LAMPX, 760, ease_out(u)); ly = 1330 - 260 * math.sin(math.pi * u); lr = 8 * ease_out(u)
    street_scene(ctx, hx, ph, 'shock' if t > tk else 'neutral', lx, 1.0, lr, ly, look=(6, 2) if t > tk else (4, 0))
    if t > tk: puffs(ctx, LAMPX + 20, 1320, t - tk, 6, 26, 90, (0.85, 0.78, 0.65), 7700)
    glow_text(ctx, '3 WISHES', 540, 330, 200, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=pop(t, 0.55), rot=-0.04)
    glow_text(ctx, '...WHAT COULD GO WRONG?', 540, 500, 80, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 1.1))

def s_back(ctx, t, d, S):
    hx = X0 - 170 * (d - t)
    ta = S.at(16, 'And then')
    la = ease_io((t - ta) / 0.4)
    street_scene(ctx, hx, walk_phase(S, t), 'neutral', LAMPX, la)
    if 0 < t - ta < d - ta - 0.15:
        u = (t - ta) / (d - ta - 0.15)
        for k in range(3):
            star(ctx, LAMPX - 60 + k * 60, 1250 - 30 * (k % 2), 16, alpha=max(0, 1 - u) * (0.5 + 0.5 * math.sin(t * 10 + k)), seed=7710 + k)

# ---------------- story ----------------
def s_genie(ctx, t, d, S):
    magic_bg(ctx, t, hexc('241a3d'))
    tp = S.at(1, 'Poof'); l2 = S.L(2)[0]
    lx, ly = 690, 1300
    rub = 10 * math.sin(t * 30) if t < tp else 0
    you(ctx, 820, 1300, 1.7, legs=None, expr='shock' if t > tp else 'smile', look=(-6, -6) if t > tp else (-4, 6),
        arms=[((-68, 44), (-110, 120), (-70 + rub / 2, 10)), ((68, 44), (60, 130), (10 + rub, 30))])
    lamp(ctx, lx + rub, ly - 260, 0.9, 0.1, glow=1.0 if t > tp - 0.2 else 0.3)
    if t > tp:
        u = ease_out_back((t - tp) / 0.6, 1.2)
        genie(ctx, 400, lerp(1100, 700, u), 1.35 * max(0.05, u), tail=(lx - 130, ly - 300), expr='smile',
              arms='up' if t > l2 else 'clasp')
        puffs(ctx, lx - 120, ly - 320, t - tp, 10, 70, 330)
    if t > l2:
        say(ctx, '"THREE wishes."', 520, 240, 1020, 420, (520, 520), l2 - 0.05, t, 64) if t < S.at(2, 'Choose') else \
            say(ctx, '"Choose wisely."', 520, 240, 1020, 420, (520, 520), 0, t, 64)
        glow_text(ctx, '3', 180, 420, 260, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=pop(t, l2 + 0.2), rot=-0.1)

def s_rich(ctx, t, d, S):
    l4 = S.L(4)[0]
    if t < l4 - 0.1:
        magic_bg(ctx, t)
        wish_card(ctx, t, 1, '"MAKE ME RICH"', 0.05, S.at(3, 'Make') - 0.05)
        genie(ctx, 540, 1250, 1.3, expr='smile', arms='wave')
        return
    tt = t - l4
    ctx.set_source_rgb(*hexc('254a35')); ctx.paint(); ctx.new_path()
    radial(ctx, 540, 800, 800, (0.6, 1, 0.6), 0.25)
    money_rain(ctx, tt)
    shape(ctx, rect(250, 360, 830, 1240), hexc('1b1d22'), 6, 7800)
    shape(ctx, rect(280, 420, 800, 1180), (0.97, 0.98, 0.97), 3, 7801)
    text(ctx, 'MY BANK', 540, 500, 70, 'Bebas Neue', hexc('2f6b3e'), anchor='c')
    text(ctx, 'Balance', 540, 640, 56, anchor='c', color=hexc('666a70'))
    v = int(10_000_000 * ease_out(min(1, tt / 1.6)))
    text(ctx, f'${v:,}', 540, 790, 96, 'Bebas Neue', INK, anchor='c')
    if tt > 1.6: stamp(ctx, 'DEPOSITED', 540, 1000, 1.6, tt, 70, -0.1)
    you(ctx, 860, 1520, 1.5, legs=None, expr='smile', arms='up', look=(-6, -4))

def s_tax(ctx, t, d, S):
    office(ctx, wall=hexc('c7cccb'))
    tc, th = S.at(5, 'calls'), S.at(5, 'half')
    person3(ctx, 230, 1380, 1.6, 'suit', 'slick', hexc('8c8a86'), glasses='round', seed=7900, color=hexc('5a5f66'),
            tie=INK, legs=None, expr='stern', arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (120, 40), (60, -60))])
    shape(ctx, rect(230 + 70, 1380 - 150, 230 + 120, 1380 - 40), INK, 3, 7901)               # phone at ear
    you(ctx, 860, 1380, 1.6, legs=None, expr='shock' if t > th else 'worried', arms='tense', look=(-6, 0))
    # money bag split in half
    cut = ease_out((t - th) / 0.5) if t > th else 0
    for side in (-1, 1):
        ctx.save(); ctx.translate(540 + side * 90 * cut, 760); ctx.rotate(side * 0.15 * cut)
        ctx.rectangle(-300 if side < 0 else 0, -300, 300, 600); ctx.clip(); ctx.new_path()
        shape(ctx, ell(0, 40, 170, 150, 30), hexc('c9a974'), 5, 7910)
        shape(ctx, [(-50, -110), (50, -110), (70, -150), (-70, -150)], hexc('b3925d'), 4, 7911)
        text(ctx, '$', 0, 110, 200, 'Bebas Neue', hexc('6b4f2a'), anchor='c')
        ctx.restore()
    if t > th: rough(ctx, [(540, 560), (540, 960)], 6, 7920, hexc('c0322a'))
    glow_text(ctx, 'RING RING', 540, 330, 110, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, tc - 0.1), rot=0.05 * math.sin(t * 30))
    stamp(ctx, 'TAX: -50%', 540, 1080, th + 0.2, t, 100, -0.1)

COUSIN_COLS = ['c0322a', '2f5fa8', 'e3c24a', '2f9e4f', 'e07a9a', '7a3e9d', 'c77b3a', '4f79b8']
def s_cousins(ctx, t, d, S):
    office(ctx, wall=hexc('d9cdb4'), floor=hexc('8f7a62'), window=False, plant=False)
    tf = S.at(6, 'forty')
    rng = random.Random(4)
    rows = [(1120, 0.62, 7), (1270, 0.75, 6), (1430, 0.9, 5)]
    for r, (y, s, n) in enumerate(rows):
        for i in range(n):
            x = 60 + (i + 0.5) * (680 / n) + rng.uniform(-20, 20)
            t0 = 0.05 + r * 0.25 + i * 0.05
            if t < t0: continue
            bob = 8 * math.sin(t * 8 + i + r)
            hair = rng.choice(['short', 'spiky_s', 'bob', 'slick', 'crew'])
            person3(ctx, x, y - 334 * s * 0 + bob - 200 * s, s, 'tee', hair, hexc(rng.choice(['1f1f24', '5a3d2a', '8a6a4a'])),
                    seed=8000 + r * 20 + i, color=hexc(COUSIN_COLS[(i + r) % 8]), legs=None, expr='smile',
                    arms='reachR', look=(6, 0))
    shape(ctx, rect(780, 520, 1060, 1330), hexc('6b4f3a'), 5, 8100)
    you(ctx, 920, stand(1.0, 1330), 1.0, expr='shock', arms='tense', look=(-6, 0))
    glow_text(ctx, f'{min(47, int(47 * min(1, max(0, (t - 0.1) / max(0.1, tf - 0.1))))) } COUSINS', 420, 400, 140, 'Bebas Neue', GOLD,
              (1, 0.75, 0.2), pop=pop(t, 0.05))
    glow_text(ctx, '"HEY... FAMILY!"', 420, 560, 80, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.5))

def s_broke(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('3a3f48')); ctx.paint(); ctx.new_path()
    paper(ctx, 540, 450, 360, 300, 0.04, 8200, col=(1, 1, 1))
    shape(ctx, rect(360, 300, 720, 380), hexc('c0322a'), 4, 8201)
    text(ctx, 'FRIDAY', 540, 365, 70, 'Bebas Neue', (1, 1, 1), anchor='c')
    text(ctx, '5', 540, 560, 160, 'Bebas Neue', INK, anchor='c')
    you(ctx, 540, 1420, 2.0, legs=None, expr='sad', tear=(t - 0.3) / 1.0,
        arms=[((-68, 44), (-120, 100), (-60, -10)), ((68, 44), (90, 128), (86, 206))])
    # empty wallet, upside down, with a moth
    ctx.save(); ctx.translate(390, 1180); ctx.rotate(math.pi + 0.2)
    shape(ctx, rect(-80, -50, 80, 50), hexc('6b4a35'), 4, 8210)
    ctx.restore()
    mx, my = 390 + 80 * math.sin(t * 2), 1040 - 60 * t
    for sx in (-1, 1): shape(ctx, ell(mx + sx * 16, my, 16, 10 + 6 * math.sin(t * 25), 12), hexc('b8b0a0'), 2, 8220 + sx)
    stamp(ctx, '$0.00', 800, 900, 0.5, t, 110, 0.12)

def s_famous(ctx, t, d, S):
    l9 = S.L(9)[0]
    if t < l9 - 0.1:
        magic_bg(ctx, t)
        wish_card(ctx, t, 2, '"MAKE ME FAMOUS"', 0.05, S.at(8, 'Make') - 0.05)
        genie(ctx, 540, 1250, 1.3, expr='smile', arms='wave')
        return
    tt = t - l9
    ctx.set_source_rgb(*hexc('1d1f2a')); ctx.paint(); ctx.new_path()
    # magazine, TV, billboard — all your face
    for k, (x, y, w, h, lab, rot) in enumerate(((290, 560, 420, 560, 'STAR WEEKLY', -0.08), (790, 640, 440, 330, 'LIVE', 0.06), (540, 1180, 760, 300, 'BILLBOARD', 0.0))):
        if tt < k * 0.35: continue
        p = pop(tt, k * 0.35)
        ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(p, p)
        shape(ctx, rect(-w / 2, -h / 2, w / 2, h / 2), (1, 1, 1) if k == 0 else hexc('2a2d33'), 5, 8300 + k)
        if k == 1: shape(ctx, rect(-w / 2 + 20, -h / 2 + 20, w / 2 - 20, h / 2 - 20), hexc('7aa6c9'), 3, 8310)
        if k == 2: shape(ctx, rect(-w / 2 + 16, -h / 2 + 16, w / 2 - 16, h / 2 - 16), hexc('e3c24a'), 3, 8311)
        you(ctx, 0, h * 0.18 if k != 2 else 60, (h / 560) * 1.4 if k != 2 else 0.75, legs=None, expr='smile', arms='down')
        text(ctx, lab, 0, -h / 2 + 70, 60 if k == 0 else 44, 'Bebas Neue', hexc('c0322a'), anchor='c')
        ctx.restore()
    if int(tt * 6) % 3 == 0: dark(ctx, 0.0)
    if (tt % 0.5) < 0.06: dark(ctx, 0.6, (1, 1, 1))

def s_paps(ctx, t, d, S):
    tf = S.at(10, 'Fans') - 0.1
    if t < tf:
        ctx.set_source_rgb(*hexc('2b3550')); ctx.paint(); ctx.new_path()
        shape(ctx, [(240, 800), (540, 520), (840, 800)], hexc('7a3b33'), 5, 8400)
        shape(ctx, rect(280, 800, 800, 1330), hexc('d9cdb4'), 5, 8401)
        shape(ctx, rect(480, 1060, 600, 1330), hexc('6b4f3a'), 4, 8402)
        shape(ctx, rect(320, 880, 440, 990), hexc('f0c96a'), 4, 8403); shape(ctx, rect(640, 880, 760, 990), hexc('f0c96a'), 4, 8404)
        shape(ctx, rect(-300, 1330, W + 300, 2200), hexc('3f4a3a'), 5, 8405)
        rng = random.Random(6)
        for i in range(9):
            x = 60 + i * 120; y = 1420 + (i % 2) * 70
            person3(ctx, x, y - 200 * 0.7, 0.7, 'tee', 'short', HAIR, seed=8500 + i, color=hexc(COUSIN_COLS[i % 8]),
                    legs=None, back=True, arms='up')
            shape(ctx, rect(x - 30, y - 290, x + 30, y - 250), INK, 3, 8520 + i)
            if (t * 5 + i * 0.37) % 1 < 0.18: radial(ctx, x, y - 270, 120, (1, 1, 1), 0.9)
        glow_text(ctx, 'CAMERAS', 540, 330, 150, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.05))
        return
    tt = t - tf
    room(ctx, hexc('cfe3e6'), hexc('e9ecec'), 1330)
    for k in range(8): rough(ctx, [(0, 300 + k * 130), (W, 300 + k * 130)], 2, 8600 + k, hexc('b9cfd3'))
    shape(ctx, rect(560, 380, 900, 820), hexc('b8d4dc'), 5, 8610)                       # mirror
    you(ctx, 380, 1330, 1.8, legs=None, expr='shock' if tt > 0.4 else 'neutral', look=(8, 0), color=hexc('f1f1f1'), outfit='tee',
        arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (90, 100), (40, -50))])
    rough(ctx, [(380 + 72, 1330 - 100), (380 + 110, 1330 - 150)], 8, 8620, hexc('4fa3c9'))   # toothbrush
    shape(ctx, rect(700, 900, 1080, 1330), hexc('f2f2f2'), 5, 8630)                     # shower curtain
    for k in range(4): rough(ctx, [(730 + k * 90, 920), (730 + k * 90, 1320)], 2.5, 8640 + k, hexc('c9c9c9'))
    p = ease_out_back((tt - 0.25) / 0.3)
    if p > 0:
        person3(ctx, 700 + 40 * p, 1180, 1.1, 'tee', 'bob', hexc('a07040'), seed=8650, color=hexc('e07a9a'),
                legs=None, expr='smile', arms='reachL', look=(-6, 0))
        shape(ctx, rect(700 + 40 * p - 260, 1180 + 30, 700 + 40 * p - 220, 1180 + 100), INK, 3, 8651)
        say(ctx, '"HI!!"', 640, 620, 1000, 800, (840, 900), 0.4, tt, 80)
    glow_text(ctx, 'FANS... IN YOUR BATHROOM', 540, 300, 90, 'Bebas Neue', (1, 1, 1), None, pop=pop(tt, 0.1))

def s_milk(ctx, t, d, S):
    room(ctx, hexc('e8e4da'), hexc('c9c3b5'), 1330)
    for row in range(3):
        y = 420 + row * 270
        shape(ctx, rect(-20, y, W + 20, y + 24), hexc('8a8478'), 3, 8700 + row)
        for k in range(8): shape(ctx, rect(20 + k * 135, y - 130, 120 + k * 135, y), hexc(COUSIN_COLS[(k + row) % 8]), 3, 8710 + row * 10 + k, alpha=0.8)
    for i, (x, fl) in enumerate(((170, False), (900, True), (300, False), (780, True))):
        s = 1.05 if i < 2 else 0.9
        person3(ctx, x, stand(s, 1460 if i < 2 else 1380), s, 'tee', ['short', 'bob', 'spiky_s', 'slick'][i], HAIR, seed=8800 + i,
                color=hexc(COUSIN_COLS[i + 2]), expr='smile', arms='reachR', flip=fl)
    you(ctx, 540, stand(1.15, 1400), 1.15, expr='blank', arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (110, 120), (60, 80))])
    shape(ctx, [(560, 760), (640, 760), (640, 900), (560, 900)], (1, 1, 1), 4, 8850)
    shape(ctx, [(560, 760), (600, 720), (640, 760)], (1, 1, 1), 4, 8851)
    text(ctx, 'MILK', 600, 840, 34, 'Bebas Neue', hexc('2f5fa8'), anchor='c')
    for k, (x0, y0, tl) in enumerate(((40, 330, (200, 600)), (640, 280, (880, 600)))):
        say(ctx, '"SELFIE?!"', x0, y0, x0 + 400, y0 + 170, tl, 0.2 + k * 0.4, t, 70)
    if (t % 0.6) < 0.07: dark(ctx, 0.5, (1, 1, 1))

def s_onewish(ctx, t, d, S):
    magic_bg(ctx, t)
    tl = S.at(12, 'One')
    genie(ctx, 540, 820 + 30 * math.sin(t * 2.5), 1.4, expr='smile', arms='up' if t > tl else 'clasp')
    glow_text(ctx, '1', 540, 330, 300, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=pop(t, tl))
    glow_text(ctx, 'WISH LEFT', 540, 500, 110, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, tl + 0.2))
    you(ctx, 860, 1600, 1.4, legs=None, expr='blank', arms='down', look=(-6, -6))

def s_think(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('2a2f36')); ctx.paint(); ctx.new_path()
    radial(ctx, 540, 1150, 800, (0.95, 0.8, 0.5), 0.25)
    ctx.save(); cam(ctx, 540, 1200, 1.0 + 0.12 * ease_io(t / d))
    you(ctx, 540, 1520, 3.0, legs=None, expr='worried', look=(5, -7),
        arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (120, 70), (40, 10))])
    for k in range(2):
        tt = (t * 1.1 + k * 0.5) % 1
        sweat(ctx, 700 + k * 30, 1000 + tt * 200, 1.8, alpha=1 - tt)
    ctx.restore()
    clock(ctx, 820, 420, 130, t * 6)
    glow_text(ctx, 'HMMMM...', 340, 420, 130, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.1), rot=-0.06)
    glow_text(ctx, 'REALLY HARD', 340, 600, 100, 'Bebas Neue', GOLD, None, pop=pop(t, S.at(13, 'Really')))

def s_lastwish(ctx, t, d, S):
    magic_bg(ctx, t, hexc('1d1430'))
    genie(ctx, 780, 760, 1.15, expr='shock' if t > S.at(14, 'never') else 'smile', arms='clasp')
    you(ctx, 360, 1380, 2.0, legs=None, expr='stern', look=(4, -4), arms=[((-68, 44), (-120, -70), (-50, -235)), ((68, 44), (120, -70), (50, -235))])
    lamp(ctx, 360, 1380 - 2.0 * 245, 1.0, 0, glow=0.6)
    say(ctx, '"I wish... I\'d never\nfound this lamp."', 60, 230, 760, 480, (300, 700), 0.1, t, 64)

def s_poof(ctx, t, d, S):
    street(ctx)
    ctx.set_source_rgb(1, 1, 1); ctx.paint_with_alpha(max(0, 1 - t / 0.35)); ctx.new_path()
    puffs(ctx, 540, 900, 0.25 + t * 0.6, 18, 240, 650, seed=7800)
    glow_text(ctx, 'POOF!', 540, 900, 320, 'Bebas Neue', (1, 1, 1), (0.6, 0.6, 1), pop=ease_out_back((t + 0.1) / 0.3) * max(0, 1 - max(0, t - 0.9) * 2), rot=-0.05)

SHOTS = [(0, s_street), (1, s_genie), (3, s_rich), (5, s_tax), (6, s_cousins), (7, s_broke), (8, s_famous), (10, s_paps),
         (11, s_milk), (12, s_onewish), (13, s_think), (14, s_lastwish), (15, s_poof), (16, s_back)]

if __name__ == '__main__':
    run(SHOTS)

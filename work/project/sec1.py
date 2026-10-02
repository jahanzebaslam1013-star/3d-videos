import sys, math, random, json, subprocess, re
import cairo, numpy as np
import pk, stickkit as K
from pk import *
from stickkit import person3

ALL = [l.strip() for l in open('all.txt') if l.strip()]
LT = json.load(open('lt1.json'))
LINES = [re.sub(r'\s*\[.*?\]\s*', ' ', l).strip() for l in ALL[:len(LT)]]
END = 121.39 + 1.7

class Sc:
    def __init__(self, t0): self.t0 = t0
    def L(self, i): return (LT[i][0] - self.t0, LT[i][1] - self.t0)
    def F(self, i, f):
        s, e = self.L(i); return s + (e - s) * f
def stand(s, floor): return floor - 334 * s
def pop(t, t0, dur=0.3): return ease_out_back((t - t0) / dur) if t > t0 else 0

def busts_row(ctx, y, s, n, seed, t, xs=None, expr='worried', look=(0, 2)):
    rng = random.Random(seed)
    xs = xs or [rng.uniform(-100, W + 100) for _ in range(n)]
    for i, x in enumerate(xs):
        col = rng.choice([BLUEK, hexc('8a6a4a'), hexc('5f6e45'), hexc('a8a29a'), hexc('6b7a8a'), KAMEEZ])
        hair = rng.choice(['short', 'spiky_s', 'crew', 'slick'])
        person(ctx, x, y + 3 * math.sin(t * 2 + i), s, 'kameez', hair, K.HAIR, expr=expr, look=look, legs=None,
               arms='tense', color=col, seed=seed + i * 37, beard=rng.choice([None, None, 'mous', 'full']))

def night_sea(ctx, t, horizon=560):
    sky_grad(ctx, NIGHT1, NIGHT2, 0, horizon); stars(ctx, 70, 4010, t); moon(ctx, 1520, 170, 48)
    waves(ctx, horizon, t)

# ---------------- shots ----------------
def sc_sea(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 620, 1.0 + 0.12 * t / d)
    night_sea(ctx, t)
    e0 = S.L(2)[0] + 1.0
    sm = max(0, (t - e0) / 2.5) if t > e0 else 0
    still = min(1, max(0, (t - e0) / 1.5))
    boat(ctx, 960, 790, 1.7, t * (1 - 0.7 * still), smoke=sm)
    ctx.restore()
    if t < e0 and t > S.L(2)[0] - 0.5:
        for k in range(3):
            a = max(0, math.sin(t * 14 + k))
            text(ctx, 'putt', 1480 + k * 70, 520 - k * 40, 46, 'Bebas Neue', (0.85, 0.85, 0.9), alpha=0.7 * a)
    ctx.save(); ctx.translate(140, 120); p = pop(t, S.L(0)[0] + 0.3)
    if p > 0.01:
        ctx.scale(p, p); K.clock(ctx, 0, 0, 56, 3 * 2 * math.pi + 0.05 * t, 1.0); text(ctx, '3:00 AM', 80, 18, 64, 'Bebas Neue', (1, 1, 1))
    ctx.restore()

def sc_crowd(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 540, 1.05 + 0.05 * t / d)
    sky_grad(ctx, NIGHT1, NIGHT2, 0, 700); stars(ctx, 40, 4011, t)
    busts_row(ctx, 470, 0.62, 13, 7000, t, xs=[i * 160 - 20 for i in range(14)], look=(0, -2))
    busts_row(ctx, 640, 0.78, 10, 7100, t, xs=[i * 200 + 40 for i in range(11)])
    busts_row(ctx, 830, 0.95, 8, 7200, t, xs=[i * 260 - 40 for i in range(9)])
    ctx.restore()
    dark(ctx, 0.15)
    t1 = S.F(3, 0.28); t2 = S.F(3, 0.55)
    glow_text(ctx, '400', 430, 230, 230, 'Bebas Neue', (1, 1, 1), (1, 0.85, 0.5), pop=pop(t, t1))
    utext(ctx, 'LOG', 430, 380, 80, (1, 1, 1), stroke=(0, 0, 0), pop=pop(t, t1 + 0.1))
    if t > t2:
        ctx.save(); ctx.translate(1400, 260); ctx.scale(pop(t, t2), pop(t, t2))
        shape(ctx, rect(-210, -150, 210, 150), hexc('f3efe4'), 5, 7300)
        utext(ctx, 'Gunjaish', 0, -70, 60, INK)
        text(ctx, '100', 0, 100, 150, 'Bebas Neue', hexc('c0322a'), anchor='c')
        ctx.restore()
    stamp(ctx, 'OVERLOADED', 960, 520, S.F(3, 0.85), t, 110)

def sc_pocket(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('101822')); ctx.paint(); radial(ctx, 960, 520, 800, (0.4, 0.5, 0.7), 0.35)
    ctx.save(); cam(ctx, 960, 540, 1.0 + 0.08 * t / d)
    up = ease_out(t / 0.8); y = lerp(900, 560, up)
    # bag
    ctx.save(); ctx.translate(960, y); ctx.rotate(-0.05)
    shape(ctx, rect(-330, -260, 330, 250), (0.85, 0.92, 1.0), 5, 7400, alpha=0.35)
    pp = pop(t, S.F(4, 0.42))
    if pp > 0.01:
        ctx.save(); ctx.translate(-130, 0); ctx.scale(pp, pp)
        shape(ctx, rect(-130, -180, 130, 180), hexc('1f5a3a'), 5, 7410)
        shape(ctx, ell(0, -30, 54, 54, 24), hexc('d4b45a'), 3, 7411, alpha=0.8)
        text(ctx, 'PASSPORT', 0, 110, 52, 'Bebas Neue', hexc('d4b45a'), anchor='c'); ctx.restore()
    ph = pop(t, S.F(4, 0.78))
    if ph > 0.01:
        ctx.save(); ctx.translate(170, 10); ctx.rotate(0.12); ctx.scale(ph, ph)
        shape(ctx, rect(-130, -160, 130, 160), hexc('f6f2e6'), 5, 7420)
        shape(ctx, rect(-108, -138, 108, 110), hexc('c9b89a'), 2, 7421)
        ammi(ctx, 0, 30, 0.62, expr='smile', legs=None)
        ctx.restore()
    shape(ctx, [(-330, -260), (330, -260), (330, -230), (-330, -230)], hexc('c9d6e6'), 3, 7430, alpha=0.6)
    ctx.restore()
    # hand
    for k in range(4):
        shape(ctx, ell(640 + k * 26, y + 120 - k * 40, 36, 22, 14), K.SKIN, 3.5, 7440 + k)
    ctx.restore()

def sc_ask(ctx, t, d, S, freeze=None):
    tt = t if freeze is None else freeze
    l6 = S.L(6)[0]
    away = ease_io((tt - l6) / 0.8) if tt > l6 else 0
    ctx.save(); cam(ctx, 960, 560, 1.08)
    sky_grad(ctx, NIGHT1, NIGHT2, 0, 760); stars(ctx, 50, 4012, tt); moon(ctx, 1650, 140, 40)
    busts_row(ctx, 520, 0.6, 12, 7500, tt, xs=[i * 170 - 30 for i in range(13)], look=(0, -2))
    cfg = [(330, 'short', hexc('8a6a4a'), 'full', 7600), (690, 'crew', hexc('6b7a8a'), None, 7650),
           (1270, 'slick', KAMEEZ, 'mous', 7700), (1610, 'spiky_s', hexc('5f6e45'), None, 7750)]
    for i, (x, hr, col, bd, sd) in enumerate(cfg):
        lk = (6 if x < 960 else -6, 0) if away < 0.5 else ((-8 if x < 960 else 8), 5)
        person(ctx, x, 720, 1.05, 'kameez', hr, K.HAIR, expr='worried' if away < 0.5 else 'sad', look=lk, legs=None,
               arms='tense', color=col, seed=sd, beard=bd, headrot=(-0.25 if x < 960 else 0.25) * away)
    hamza(ctx, 960, 690, 1.2, expr='worried', look=(0, -3) if away < 0.5 else (0, 4), legs=None, arms='tense')
    ctx.restore()
    if freeze is None and away < 0.3:
        usay(ctx, 'Italy kitni door hai?', 1080, 70, 1640, 270, (1350, 400), S.L(5)[0] + 0.1, t, 72)
    dark(ctx, 0.12 + 0.2 * away)

def sc_freeze(ctx, t, d, S):
    l7 = S.L(7)[0]
    if t < l7 - 0.1:
        sc_ask(ctx, 0, 1, Sc(LT[5][0] - 0.18), freeze=LT[6][1] - LT[5][0] + 0.18 + 0.1)
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.5, 0.05, 0.05, 0.35); ctx.fill()
        p = pop(t, 0.05, 0.25)
        glow_text(ctx, 'POV: DUNKI', 960, 420, 230, 'Bebas Neue', (1, 1, 1), (1, 0.3, 0.3), pop=p, rot=-0.04)
        ustamp(ctx, 'GHAIR QANOONI SAFAR', 960, 700, 0.6, t, 90)
        return
    u = t - l7
    ctx.save(); ctx.translate(960, 540); ctx.scale(1.03, 1.03); ctx.translate(-960, -540)
    night_sea(ctx, 40 - u * 6)
    boat(ctx, 960 + u * 300, 760, 1.25, 40 - u * 6)
    ctx.restore()
    vhs(ctx, t, 1.0)
    for k in range(2):
        x = 160 + k * 70
        shape(ctx, [(x, 120), (x - 60, 160), (x, 200)], (1, 1, 1), 0, 0, alpha=0.9)
    text(ctx, 'REWIND', 260, 185, 80, 'Bebas Neue', (1, 1, 1))

def sc_village(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 600, 1.12 - 0.08 * ease_io(t / d)); ctx.translate(-30 * t / d, 0)
    village(ctx, t)
    buffalo(ctx, 1540 - 18 * t, 900, 0.9, t)
    for k in range(3):
        bx = 300 + k * 90 + 60 * t; by = 260 + 20 * math.sin(t * 2 + k)
        rough(ctx, [(bx - 18, by), (bx, by + 8 * math.sin(t * 9 + k)), (bx + 18, by)], 3, 7800 + k)
    ctx.restore()
    p = pop(t, S.L(8)[0] + 0.1)
    if p > 0.01:
        ctx.save(); ctx.translate(960, 150); ctx.scale(p, p)
        shape(ctx, rect(-330, -80, 330, 80), hexc('17171a'), 4, 7850, ink=(1, 1, 1))
        utext(ctx, 'Aath mahine pehle', 0, 4, 100, (1, 1, 1))
        ctx.restore()

def sc_hamza(ctx, t, d, S):
    ctx.save(); cam(ctx, 760, 520, 1.25 + 0.12 * t / d)
    village(ctx, t)
    hamza(ctx, 760, stand(1.3, 990), 1.3, expr='neutral' if t < S.F(9, 0.5) else 'smile', arms='down', look=(4, 0))
    ctx.restore()
    p = pop(t, S.L(9)[0] + 0.2)
    if p > 0.01:
        ctx.save(); ctx.translate(1420, 400); ctx.rotate(-0.04); ctx.scale(p, p)
        shape(ctx, rect(-280, -170, 280, 170), hexc('f3efe4'), 5, 7900)
        utext(ctx, 'HAMZA', 0, -60, 130, INK, font='Bebas Neue')
        rough(ctx, [(-200, 20), (200, 20)], 3, 7901, hexc('c0322a'))
        utext(ctx, 'Umar: 24 saal', 0, 95, 66, hexc('333336'), pop=1 if t > S.F(9, 0.55) else 0)
        ctx.restore()

def sc_degree(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 520, 1.1 + 0.06 * t / d)
    K.room(ctx, wall=hexc('d8c39c'), floor=hexc('9a7a58'), y=860)
    shape(ctx, rect(1300, 220, 1560, 520), hexc('7aa0b8'), 5, 8000)   # window
    rough(ctx, [(1430, 220), (1430, 520)], 4, 8001); rough(ctx, [(1300, 370), (1560, 370)], 4, 8002)
    sad = t > S.F(10, 0.55)
    arms = [((-68, 44), (-120, 120), (-110, 150)), ((68, 44), (120, 120), (110, 150))]
    hamza(ctx, 760, stand(1.25, 1000), 1.25, expr='sad' if sad else 'smile', arms=arms, shrug=0)
    shape(ctx, rect(760 - 180, 640, 760 + 180, 800), hexc('f6f0dc'), 5, 8010)
    utext(ctx, 'B.A. Degree', 760, 685, 54, INK); rough(ctx, [(640, 740), (880, 740)], 2, 8011, hexc('a8a08c'))
    shape(ctx, ell(840, 770, 22, 22, 14), hexc('c0322a'), 2.5, 8012)
    ctx.restore()
    stamp(ctx, 'NO JOB', 1380, 760, S.F(10, 0.62), t, 150)
    if sad: K.sweat(ctx, 860, 300, 2.0)

def sc_cv(ctx, t, d, S):
    ctx.save(); cam(ctx, 600, 540, 1.05)
    K.room(ctx, wall=hexc('cdb894'), floor=hexc('8f7050'), y=860)
    shape(ctx, rect(380, 700, 900, 730), hexc('7a5a3a'), 4, 8100); shape(ctx, rect(400, 730, 420, 860), hexc('7a5a3a'), 3, 8101)
    shape(ctx, rect(860, 730, 880, 860), hexc('7a5a3a'), 3, 8102)
    hamza(ctx, 560, 480, 1.1, expr='neutral' if t < S.F(11, 0.7) else 'sad', legs=None, arms='table', look=(6, 2))
    ctx.restore()
    rng = random.Random(8200)
    n = int(min(40, t * 9))
    for i in range(n):
        st = i / 9; u = t - st; x = 800 + u * 700 + rng.uniform(-50, 50); y = 600 - u * 260 + rng.uniform(-200, 120) + 80 * u * u
        if x < W + 200: envelope(ctx, x, y, 0.8, u * 2 + rng.uniform(-1, 1), 8300 + i)
    cnt = int(min(200, 7 * t ** 1.6))
    text(ctx, f'CVs SENT: {cnt}', 1200, 140, 90, 'Bebas Neue', (1, 1, 1))
    t0 = S.F(11, 0.68)
    glow_text(ctx, 'REPLIES: 0', 1400, 830, 130, 'Bebas Neue', hexc('ff5a4a'), (1, 0.2, 0.1), pop=pop(t, t0))

def shop(ctx, t, bills):
    shape(ctx, rect(-300, -300, W + 300, H + 300), hexc('8e6a48'), 0, 1)
    for r in range(3):
        y = 160 + r * 180
        shape(ctx, rect(300, y + 120, 1620, y + 140), hexc('5a3d26'), 3, 8400 + r)
        rng = random.Random(8410 + r)
        x = 320
        while x < 1580:
            w = rng.uniform(50, 110); h = rng.uniform(70, 115)
            shape(ctx, rect(x, y + 120 - h, x + w, y + 120), rng.choice([hexc('c0322a'), hexc('e3c24a'), hexc('2f9e4f'), hexc('2f5fa8'), hexc('e8e2d0')]), 2.5, int(x) + r)
            x += w + 8
    shape(ctx, rect(560, 30, 1360, 120), hexc('2f6e3e'), 5, 8420)
    utext(ctx, 'Hamza General Store', 960, 75, 64, (1, 1, 1))
    abba(ctx, 960, 650, 1.15, expr='worried' if bills > 0.3 else 'neutral', legs=None, arms='table', look=(0, 4))
    shape(ctx, rect(200, 760, 1720, 1100), hexc('6b4a2e'), 5, 8430)
    shape(ctx, rect(200, 740, 1720, 775), hexc('8a6438'), 4, 8431)

def sc_shop(ctx, t, d, S):
    t0 = S.F(12, 0.45)
    bills = max(0, t - t0)
    ctx.save(); cam(ctx, 960, 560, 1.0 + 0.1 * t / d)
    shop(ctx, t, bills)
    rng = random.Random(8500)
    for i in range(int(min(14, bills * 6))):
        st = t0 + i / 6; u = min(1, (t - st) / 0.35)
        x = 1250 + rng.uniform(-60, 300); yy = lerp(-200, 690 - i * 9, ease_out(u))
        paper(ctx, x, yy, 0.8, rng.uniform(-0.5, 0.5), 'BILL', 8510 + i)
    ctx.restore()
    if bills > 0.5: K.sweat(ctx, 1040, 330, 2.2)
    if bills > 0.1: utext(ctx, 'Kharcha barh raha hai!', 1560, 230, 80, hexc('ff5a4a'), stroke=(0, 0, 0), pop=pop(t, t0 + 0.4), rot=-0.06)

def evening_yard(ctx, t, night=0.0):
    top = K.tint(hexc('e8a46a'), NIGHT1, night); bot = K.tint(hexc('f3d2a0'), NIGHT2, night)
    sky_grad(ctx, top, bot, 0, 700)
    shape(ctx, rect(-300, 640, W + 300, H + 300), K.tint(hexc('c9a77a'), hexc('2a2a38'), night), 4, 8600)
    shape(ctx, rect(-300, 420, W + 300, 650), K.tint(MUD, hexc('3a2e2e'), night), 4, 8601)    # courtyard wall
    for k in range(8): rough(ctx, [(k * 260 - 100, 430), (k * 260 - 90, 640)], 2, 8602 + k, K.tint(MUD_D, hexc('241c1c'), night))

def sc_buzz(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 600, 1.15 + 0.15 * ease_io(t / d))
    evening_yard(ctx, t, 0.3)
    charpai(ctx, 960, 960, 1.6)
    buzz = t > S.L(13)[0] + 1.0
    sh = 6 * math.sin(t * 60) if buzz else 0
    hamza(ctx, 960, 560, 1.15, expr='shock' if buzz else 'neutral', legs=None,
          arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (140, 120), (110, 60))], look=(4, 4) if buzz else (0, 0))
    phone(ctx, 1080 + sh, 620, 0.55, rot=0.2, screen=hexc('e8f4ff') if buzz else hexc('1c2430'))
    ctx.restore()
    if buzz:
        for k in range(3):
            a = 0.5 + 0.5 * math.sin(t * 25 + k)
            rough(ctx, [(1300 + k * 26, 500 - k * 30), (1340 + k * 26, 480 - k * 30)], 6, 8700 + k, (1, 1, 1), alpha=a)
        text(ctx, 'BZZZ', 1380, 420, 80, 'Bebas Neue', (1, 1, 1), alpha=0.6 + 0.4 * math.sin(t * 20))

def italy_post(ctx, t, S, zoom=0.0, hearts_t0=None):
    # phone frame full screen
    ctx.set_source_rgb(*hexc('1a1d24')); ctx.paint()
    ctx.save(); cam(ctx, 960, 470, 1.0 + 0.5 * zoom)
    shape(ctx, rect(560, -40, 1360, 1140), hexc('111114'), 6, 8800)
    shape(ctx, rect(580, -20, 1340, 1120), (1, 1, 1), 0, 0)
    shape(ctx, ell(640, 70, 34, 34, 20), hexc('d0302a'), 3, 8801)
    bilal(ctx, 640, 108, 0.24, expr='smile', legs=None)
    text(ctx, 'bilal.in.italy', 690, 86, 44, 'Patrick Hand', INK)
    # photo
    ctx.save(); ctx.rectangle(580, 130, 760, 760); ctx.rectangle(580, 130, 760, 760)
    ctx.restore()
    ctx.save(); ctx.rectangle(580, 130, 760, 640); ctx.clip()
    sky_grad(ctx, hexc('7cc0ea'), hexc('d8eef8'), 130, 600)
    for k, (x, c) in enumerate(((600, 'e8b04a'), (760, 'd9774a'), (930, 'f0d27a'), (1120, 'c8603a'), (1270, 'e8b04a'))):
        shape(ctx, rect(x, 250 + (k % 2) * 40, x + 180, 640), hexc(c), 4, 8810 + k)
        for r in range(3):
            shape(ctx, rect(x + 40, 300 + r * 90 + (k % 2) * 40, x + 80, 350 + r * 90 + (k % 2) * 40), hexc('4a5a6a'), 2, 8820 + k * 3 + r)
    shape(ctx, rect(580, 640, 1340, 770), hexc('b8b0a0'), 3, 8830)
    red_car(ctx, 1060, 730, 0.95)
    bilal(ctx, 790, stand(0.9, 760), 0.9, expr='smile', arms='shrug', rot=0.12)
    ctx.restore()
    heart(ctx, 640, 820, 0.55, seed=8840)
    text(ctx, '1,284 likes', 690, 838, 40, 'Patrick Hand', INK)
    utext(ctx, 'Life set hai yaar', 1100, 920, 64, INK)
    text(ctx, 'bilal.in.italy', 600, 935, 34, 'Patrick Hand', hexc('555558'))
    ctx.restore()
    if hearts_t0 is not None and t > hearts_t0:
        rng = random.Random(8850)
        for i in range(18):
            st = hearts_t0 + i * 0.22; u = t - st
            if u <= 0 or u > 2.5: continue
            heart(ctx, 1400 + rng.uniform(-80, 260), 950 - u * 380, 0.6 + 0.4 * rng.random(), alpha=max(0, 1 - u / 2.5), seed=8860 + i)

def italy_hearts(ctx, t, t0):
    rng = random.Random(8850)
    for i in range(18):
        st = t0 + i * 0.22; u = t - st
        if u <= 0 or u > 2.5: continue
        heart(ctx, 1450 + rng.uniform(-80, 260), 900 - u * 360, 0.6 + 0.4 * rng.random(), alpha=max(0, 1 - u / 2.5), seed=8860 + i)

def sc_insta(ctx, t, d, S):
    l15 = S.L(15)[0]
    z = ease_io((t - l15) / 1.5) if t > l15 else 0
    ctx.save(); cam(ctx, 960, 380, 0.86 + 0.08 * ease_io(t / d)); italy_post(ctx, t, S, zoom=0.0, hearts_t0=None); ctx.restore()
    italy_hearts(ctx, t, S.F(15, 0.55))
    if t > l15:
        p = pop(t, S.F(15, 0.0)); p2 = pop(t, S.F(15, 0.25))
        if p > 0.01:
            ctx.save(); ctx.translate(330, 300); ctx.rotate(-0.1); ctx.scale(p, p)
            shape(ctx, rect(-200, -70, 200, 70), hexc('17171a'), 4, 8900, ink=(1, 1, 1))
            utext(ctx, 'Kaala chashma', 0, 0, 70, (1, 1, 1)); ctx.restore()
        if p2 > 0.01:
            ctx.save(); ctx.translate(330, 560); ctx.rotate(0.08); ctx.scale(p2, p2)
            shape(ctx, rect(-200, -70, 200, 70), hexc('c0322a'), 4, 8901, ink=(1, 1, 1))
            utext(ctx, 'Laal gaari', 0, 0, 70, (1, 1, 1)); ctx.restore()

def sc_stare(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('0d1018')); ctx.paint()
    radial(ctx, 960, 760, 700, (0.45, 0.65, 1.0), 0.4 + 0.03 * math.sin(t * 5))
    s = 2.6 + 0.25 * ease_io(t / d)
    hamza(ctx, 960, 560 + 150 * (s - 2.6), s, expr='blank', legs=None, look=(0, 6),
          arms=[((-68, 44), (-60, 170), (10, 200)), ((68, 44), (60, 170), (20, 200))])
    phone(ctx, 990, 1060, 0.9, rot=0.0, screen=hexc('e8f4ff'))
    dark(ctx, 0.15)

def sc_split(ctx, t, d, S):
    # left: 2 years ago (village, sepia)  right: now (Italy)
    ctx.save(); ctx.rectangle(0, 0, 960, H); ctx.clip()
    ctx.save(); ctx.translate(-480, 0); village(ctx, t); ctx.restore()
    person(ctx, 560, stand(1.05, 1000), 1.05, 'kameez', 'slick', K.HAIR, expr='sad', color=hexc('b9a98a'), seed=3400)
    if t > S.F(17, 0.62):
        a = min(1, (t - S.F(17, 0.62)) / 0.4)
        ctx.push_group(); hamza(ctx, 300, stand(1.05, 1000), 1.05, expr='sad'); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    ctx.rectangle(0, 0, 960, H); ctx.set_source_rgba(0.55, 0.42, 0.25, 0.3); ctx.fill()
    ctx.restore()
    ctx.save(); ctx.rectangle(960, 0, 960, H); ctx.clip()
    sky_grad(ctx, hexc('7cc0ea'), hexc('d8eef8'), 0, 800)
    for k, (x, c) in enumerate(((960, 'e8b04a'), (1180, 'd9774a'), (1420, 'f0d27a'), (1660, 'c8603a'))):
        shape(ctx, rect(x, 220 + (k % 2) * 50, x + 230, 820), hexc(c), 4, 8950 + k)
    shape(ctx, rect(900, 820, 2000, 1200), hexc('b8b0a0'), 3, 8960)
    red_car(ctx, 1560, 960, 1.0)
    bilal(ctx, 1200, stand(1.05, 990), 1.05, expr='smile', arms='shrug')
    ctx.restore()
    rough(ctx, [(960, -20), (960, H + 20)], 10, 8970, (1, 1, 1))
    for (x, s_, tt) in ((480, 'Do saal pehle', S.L(17)[0] + 0.1), (1440, 'Ab', S.L(17)[0] + 0.5)):
        p = pop(t, tt)
        if p > 0.01:
            ctx.save(); ctx.translate(x, 110); ctx.scale(p, p)
            shape(ctx, rect(-210, -64, 210, 64), hexc('17171a'), 4, 8980 + x, ink=(1, 1, 1))
            utext(ctx, s_, 0, 4, 88, (1, 1, 1)); ctx.restore()

def dhaba(ctx, t):
    sky_grad(ctx, hexc('9fc3d6'), hexc('f1e2bf'), 0, 700)
    shape(ctx, rect(-300, 700, W + 300, H + 300), hexc('b8946a'), 4, 9000)
    shape(ctx, [(980, 180), (1860, 150), (1880, 230), (960, 250)], hexc('8a8f96'), 5, 9001)   # tin roof
    for x in (1010, 1830): shape(ctx, rect(x - 12, 230, x + 12, 720), hexc('5a3d26'), 3, 9002 + x)
    shape(ctx, rect(1320, 520, 1720, 720), hexc('6b4a2e'), 5, 9010)   # counter
    shape(ctx, rect(1440, 470, 1560, 520), hexc('3a3a3e'), 4, 9011)   # stove
    shape(ctx, [(1460, 470), (1450, 400), (1500, 380), (1550, 400), (1540, 470)], hexc('9aa0a6'), 4, 9012)  # kettle
    for k in range(2):
        rough(ctx, [(1500 + 10 * math.sin(t * 3 + j + k), 370 - j * 22 - k * 10) for j in range(5)], 3, 9013 + k, (1, 1, 1), alpha=0.6)
    shape(ctx, rect(1080, 260, 1300, 340), hexc('c0322a'), 4, 9020)
    utext(ctx, 'CHAI', 1190, 300, 60, (1, 1, 1))
    for k in range(3): chai_cup(ctx, 1360 + k * 50, 520, 0.8, seed=9030 + k)

def sc_dhaba(ctx, t, d, S):
    l19 = S.L(19)[0]
    ctx.save(); cam(ctx, 900, 600, 1.0 + 0.12 * ease_io(t / d))
    dhaba(ctx, t)
    charpai(ctx, 1050, 960, 1.4)
    agent(ctx, 1050, 560, 1.15, expr='smile', legs=None,
          arms=[((-68, 44), (-120, 100), (-150, 40)), ((68, 44), (130, 100), (160, 40))], look=(-6, 0))
    for sx in (-1, 1): phone(ctx, 1050 + sx * 175, 590, 0.32, rot=sx * 0.2)
    wu = ease_out(min(1, t / 2.6))
    hamza(ctx, lerp(-150, 520, wu), stand(1.15, 1000), 1.15, expr='neutral', walk=t * 9 if wu < 1 else None, look=(6, 0))
    ctx.restore()
    if t > l19 - 0.2:
        g = max(0, 1 - abs(t - l19 - 0.3) / 0.4)
        radial(ctx, 1240, 640, 60, (1, 0.95, 0.6), 0.9 * g)
    usay(ctx, 'Bas ek dafa Europe pohanch jao... phir sab set hai!', 980, 40, 1840, 280, (1150, 380), l19 + 0.15, t, 68)

def sc_price(ctx, t, d, S):
    l21 = S.L(21)[0]
    ctx.save(); cam(ctx, 860, 560, 1.35)
    dhaba(ctx, t); charpai(ctx, 1050, 960, 1.4)
    agent(ctx, 1050, 560, 1.15, expr='smile', legs=None, arms='table', look=(-6, 0))
    hamza(ctx, 560, stand(1.15, 1000), 1.15, expr='worried', look=(6, 0))
    ctx.restore()
    if t < l21: usay(ctx, 'Kitna kharcha?', 120, 60, 560, 250, (420, 360), S.L(20)[0], t, 76)
    if t > l21:
        dark(ctx, 0.45)
        glow_text(ctx, 'Rs 25,00,000', 960, 380, 220, 'Bebas Neue', hexc('ffd66a'), (1, 0.75, 0.2), pop=pop(t, S.F(21, 0.05)))
        utext(ctx, 'Seedha Italy', 960, 620, 110, (1, 1, 1), stroke=(0, 0, 0), pop=pop(t, S.F(21, 0.35)))
        stamp(ctx, 'FULL GUARANTEE', 960, 820, S.F(21, 0.62), t, 120, rot=-0.08)

def sc_shock(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('2a0f0f')); ctx.paint(); radial(ctx, 960, 520, 900, (0.9, 0.3, 0.2), 0.35)
    rng = random.Random(9100)
    for i in range(26):
        st = rng.uniform(0, d); u = (t - st) % 4
        x = rng.uniform(0, W); y = -100 + u * 330
        ctx.save(); ctx.translate(x, y); ctx.rotate(u * 2 + i)
        shape(ctx, rect(-60, -28, 60, 28), hexc('5e8f5a'), 3, 9110 + i, alpha=0.8); ctx.restore()
    s = 2.7 + 0.2 * ease_io(t / d)
    hamza(ctx, 960, 720 + 120 * (s - 2.7), s, expr='shock', legs=None, arms='tense')
    K.sweat(ctx, 960 + 75 * s, 720 - 130 * s + 30 * ease_io(t / 2), 2.4)
    glow_text(ctx, '25,00,000', 960, 140, 150, 'Bebas Neue', hexc('ffd66a'), (1, 0.75, 0.2), pop=pop(t, 0.1))

def sc_night(ctx, t, d, S):
    l24 = S.L(24)[0]; l25 = S.L(25)[0]
    close = ease_io((t - l25 + 0.3) / 1.2) if t > l25 - 0.3 else 0
    ctx.save(); cam(ctx, lerp(900, 760, close), lerp(600, 470, close), lerp(1.0 + 0.1 * min(1, t / max(l25, 1)), 2.0, close))
    evening_yard(ctx, t, 1.0); stars(ctx, 50, 4013, t); moon(ctx, 300, 150, 40)
    # fields beyond wall (dark)
    lantern(ctx, 1230, 900, 0.9, t)
    charpai(ctx, 760, 960, 1.4)
    look_away = t > l24 - 0.3
    abba(ctx, 760, 560, 1.1, expr='sad' if look_away else 'neutral', legs=None, arms='clasp',
         look=(-6, 0) if look_away else (6, 0), headrot=-0.12 if look_away else 0)
    hamza(ctx, 1150, stand(1.15, 1000), 1.15, expr='worried', look=(-6, 0), arms='clasp')
    ctx.restore()
    dark(ctx, 0.1)
    usay(ctx, 'Zameen bech dete hain.', 1000, 120, 1700, 330, (1050, 430), l25 + 0.7, t, 72)
    if t > d - 1.4:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0, 0, 0, min(1, (t - (d - 1.4)) / 1.2)); ctx.fill()

SHOTS = [(0, sc_sea), (3, sc_crowd), (4, sc_pocket), (5, sc_ask), ('freeze', sc_freeze), (8, sc_village), (9, sc_hamza),
         (10, sc_degree), (11, sc_cv), (12, sc_shop), (13, sc_buzz), (14, sc_insta), (16, sc_stare), (17, sc_split),
         (18, sc_dhaba), (20, sc_price), (22, sc_shock), (23, sc_night)]

def start_of(k):
    if k == 'freeze': return LT[6][1] + 0.1
    return 0.0 if k == 0 else LT[k][0] - 0.18
def timeline():
    out = []
    for i, (k, fn) in enumerate(SHOTS):
        st = start_of(k); en = END if i == len(SHOTS) - 1 else start_of(SHOTS[i + 1][0])
        out.append((st, en, fn))
    return out

def cap_at(tt):
    for i, (a, b) in enumerate(LT):
        if a - 0.1 <= tt <= b + 0.25: return LINES[i].replace('"', '')
    return None

def draw(ctx, tt, TL):
    for a, b, fn in TL:
        if a <= tt < b:
            ctx.save(); fn(ctx, tt - a, b - a, Sc(a)); ctx.restore(); break

def main():
    rng_mode = len(sys.argv) > 1 and sys.argv[1] == '--range'
    only = [] if rng_mode else [float(a) for a in sys.argv[1:]]
    TL = timeline()
    grains = K.grain_layers()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    NF = int(END * FPS); ff = None
    if rng_mode:
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                               '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                               '-pix_fmt', 'yuv420p', sys.argv[4]], stdin=subprocess.PIPE)
    frames = [int(x * FPS) for x in only] if only else range(int(sys.argv[2]), min(NF, int(sys.argv[3])))
    for f in frames:
        tt = f / FPS; K.BOIL = f // 2
        ctx = cairo.Context(surf)
        ctx.set_operator(cairo.OPERATOR_SOURCE); ctx.set_source_rgb(0, 0, 0); ctx.paint(); ctx.set_operator(cairo.OPERATOR_OVER)
        draw(ctx, tt, TL); ctx.new_path()
        ctx.set_source_surface(grains[K.BOIL % 4], 0, 0); ctx.paint()
        K.vignette(ctx, 0.35)
        c = cap_at(tt)
        surf.flush()
        if ff: ff.stdin.write(bytes(surf.get_data()))
        else: surf.write_to_png(f'test_{tt:06.2f}.png')
    if ff: ff.stdin.close(); ff.wait()

if __name__ == '__main__':
    main()

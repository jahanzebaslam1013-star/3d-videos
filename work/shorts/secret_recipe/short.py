"""The Secret Recipe — ~51 s looping stickman reel. Grandpa is the old you; the last frame is the first frame."""
import sys, math, random
sys.path.insert(0, '.')
from scenekit import *

GREY = hexc('cfcbc3')
COLS = ['c0322a', '2f5fa8', 'e3c24a', '2f9e4f', 'e07a9a', '7a3e9d', 'c77b3a', '4f79b8']

def old_you(ctx, x, y, s, hcol=GREY, **kw):        # Grandpa == you, fifty years later
    kw.setdefault('outfit', 'cardi'); kw.setdefault('color', hexc('8a6a4a'))
    outfit = kw.pop('outfit')
    person3(ctx, x, y, s, outfit, 'spiky', hcol, wrinkles=True, beard='mous', seed=9000, **kw)

def you(ctx, x, y, s, **kw):
    kw.setdefault('outfit', 'hoodie'); hero(ctx, x, y, s, **kw)

def kid(ctx, x, y, s, **kw):
    kw.setdefault('outfit', 'hoodie'); hero(ctx, x, y, s, seed=9100, **kw)

def wink(ctx, x, y, s, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    shape(ctx, ell(24, -80, 17, 21, 20), SKIN, 0, 0)
    rough(ctx, bez((10, -78), (18, -88), (30, -88), (38, -78), 8), 3.4, 9200)
    ctx.restore()

def zip_lips(ctx, x, y, s, u=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    x1 = lerp(-18, 18, u)
    shape(ctx, ell(0, -38, 22, 9, 16), SKIN, 0, 0)
    rough(ctx, [(-18, -38), (x1, -38)], 3, 9210)
    for k in range(int(5 * u)): rough(ctx, [(-15 + k * 7, -42), (-15 + k * 7, -34)], 1.5, 9211 + k)
    shape(ctx, rect(x1 - 4, -44, x1 + 4, -30), hexc('c0c0c0'), 1.5, 9220)
    ctx.restore()

def cookie(ctx, x, y, r=34, seed=9300):
    shape(ctx, ell(x, y, r, r * 0.8, 18), hexc('c98d4a'), 3, seed)
    rng = random.Random(seed)
    for k in range(4): shape(ctx, ell(x + rng.uniform(-r * .5, r * .5), y + rng.uniform(-r * .4, r * .4), 5, 5, 8), hexc('4a2c1a'), 0, 0)

def plate(ctx, x, y, n=5, s=1.0):
    shape(ctx, ell(x, y, 150 * s, 36 * s, 30), (1, 1, 1), 4, 9310)
    for k in range(n):
        cookie(ctx, x + (k - (n - 1) / 2) * 50 * s, y - 14 * s - (12 * s if k % 2 else 0), 30 * s, 9320 + k)

def bakery_box(ctx, x, y, s=1.0, rot=0.0, seed=9400):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    shape(ctx, rect(-110, -50, 110, 50), hexc('f2b8c6'), 4, seed)
    rough(ctx, [(-110, -20), (110, -20)], 2.5, seed + 1, hexc('c97a8e'))
    text(ctx, 'TOWN BAKERY', 0, 30, 34, 'Bebas Neue', hexc('8a2e48'), anchor='c')
    ctx.restore()

def kitchen(ctx):
    room(ctx, hexc('e8d3b0'), hexc('9a7a58'), 1330)
    shape(ctx, rect(620, 280, 960, 700), hexc('a9d3ec'), 5, 9500)
    rough(ctx, [(790, 280), (790, 700)], 5, 9501); rough(ctx, [(620, 490), (960, 490)], 5, 9502)
    for sx in (0, 1):
        shape(ctx, [(600 + sx * 210, 260), (790 + sx * 0, 260), (750 if sx == 0 else 830, 720), (600 if sx == 0 else 980, 720)] if False else
              ([(600, 260), (700, 260), (660, 720), (600, 720)] if sx == 0 else [(880, 260), (980, 260), (980, 720), (920, 720)]),
              hexc('c0322a'), 4, 9503 + sx)
    rough(ctx, [(300, 0), (300, 330)], 4, 9510)
    shape(ctx, [(220, 330), (380, 330), (340, 280), (260, 280)], hexc('3a3a3a'), 4, 9511)
    radial(ctx, 300, 360, 420, (1, 0.85, 0.5), 0.35)
    shape(ctx, rect(60, 440, 420, 640), hexc('c9a06a'), 4, 9512)                 # shelf w/ jars
    for k in range(3): shape(ctx, rect(90 + k * 110, 470, 170 + k * 110, 600), hexc('e9e1cf'), 3, 9513 + k)

def table(ctx):
    shape(ctx, rect(60, 1180, 1020, 1225), hexc('8a6446'), 5, 9520)
    shape(ctx, rect(90, 1225, 990, 1560), hexc('735238'), 5, 9521)

# ---------------- whisper (first + last shot) ----------------
WHISPER = [((-68, 44), (-110, 150), (-60, 200)), ((68, 44), (125, 40), (58, -52))]
TABLE_ARMS = [((-68, 44), (-110, 150), (-60, 200)), ((68, 44), (110, 150), (60, 200))]
def lerp_arms(A, B, u):
    return [tuple((lerp(p[0], q[0], u), lerp(p[1], q[1], u)) for p, q in zip(a, b)) for a, b in zip(A, B)]

def whisper_scene(ctx, lean, zoom, kid_expr='neutral', psst=0.0):
    ctx.save(); cam(ctx, 560, 950, zoom)
    kitchen(ctx)
    old_you(ctx, 380, 880, 1.3, legs=None, rot=0.13 * lean, expr='neutral', look=(6 * lean, 0), arms=lerp_arms(TABLE_ARMS, WHISPER, lean))
    kid(ctx, 740, 1000, 0.95, legs=None, rot=-0.06, expr=kid_expr, look=(-6, 0), arms='table')
    table(ctx)
    plate(ctx, 560, 1185)
    ctx.restore()

def s_whisper(ctx, t, d, S):
    whisper_scene(ctx, 1.0, 1.0 + 0.05 * ease_io(t / d), 'shock' if t > 0.9 else 'neutral')
    glow_text(ctx, 'THE SECRET', 540, 260, 150, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.35))
    glow_text(ctx, 'INGREDIENT...', 540, 420, 150, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=pop(t, 0.6), rot=-0.04)

def s_end(ctx, t, d, S):
    lean = ease_io((t - 0.15) / (d - 0.55))
    whisper_scene(ctx, lean, 1.05 - 0.05 * ease_io(min(1, t / (d - 0.15))))

# ---------------- story ----------------
def crowd(ctx, t, xs, y, s, seed=9600, arms='reachR', flip_right_of=540):
    for i, x in enumerate(xs):
        rng = random.Random(seed + i)
        person3(ctx, x, stand(s, y) + 6 * math.sin(t * 7 + i), s, 'tee', rng.choice(['short', 'bob', 'spiky_s', 'slick', 'crew']),
                hexc(rng.choice(['1f1f24', '5a3d2a', '8a6a4a', 'a07040'])), seed=seed + i * 7, color=hexc(COLS[i % 8]),
                expr='worried', arms=arms, flip=x > flip_right_of, look=(6 if x < flip_right_of else -6, -2))

def s_beg(ctx, t, d, S):
    kitchen(ctx)
    crowd(ctx, t, [110, 250, 830, 970], 1460, 0.95)
    old_you(ctx, 540, stand(1.15, 1430), 1.15, hcol=tint(hexc('3a3530'), GREY, 0.6), expr='smile',
            arms=[((-68, 44), (-110, 110), (-60, 120)), ((68, 44), (110, 110), (60, 120))])
    plate(ctx, 540, stand(1.15, 1430) + 125 * 1.15, 5, 1.0)
    n = int(50 * min(1, t / 1.8))
    glow_text(ctx, f'{n} YEARS', 540, 300, 170, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=pop(t, 0.05))
    glow_text(ctx, '"PLEASE!"', 230, 560, 80, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.8), rot=-0.1)
    glow_text(ctx, '"JUST A HINT!"', 830, 620, 80, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 1.4), rot=0.08)

def s_who(ctx, t, d, S):
    room(ctx, hexc('cfe0d0'), hexc('8f9a7a'), 1330)
    for k, (w, x, lab) in enumerate((('Neighbors', 200, 'NEIGHBORS'), ('Cousins', 540, 'COUSINS'), ('mayor', 880, 'THE MAYOR'))):
        t0 = S.at(2, w) - 0.1
        if t < t0: continue
        p = ease_out_back((t - t0) / 0.3)
        ctx.save(); ctx.translate(x, FLOOR); ctx.scale(p, p); ctx.translate(-x, -FLOOR)
        if k == 0: woman(ctx, x, stand(1.0), 1.0, expr='worried', arms='clasp')
        elif k == 1:
            for j, dx in enumerate((-70, 70)):
                person3(ctx, x + dx, stand(0.9), 0.9, 'tee', 'spiky_s' if j else 'bob', hexc('5a3d2a'), seed=9700 + j, color=hexc(COLS[j + 2]),
                        expr='worried', arms='clasp')
        else:
            ceo(ctx, x, stand(1.05), 1.05, expr='worried', arms='clasp')
            ctx.save(); ctx.translate(x, stand(1.05)); ctx.scale(1.05, 1.05)
            shape(ctx, [(-60, 20), (-40, 10), (70, 190), (50, 200)], hexc('c0322a'), 3, 9710)
            ctx.restore()
        ctx.restore()
        glow_text(ctx, lab, x, 700 if k != 1 else 640, 90, 'Bebas Neue', GOLD if k == 2 else (1, 1, 1), None, pop=pop(t, t0))
    glow_text(ctx, 'EVERYONE BEGGED', 540, 320, 120, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.05))

def s_never(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('3b2e2a')); ctx.paint(); ctx.new_path()
    radial(ctx, 540, 1000, 800, (1, 0.8, 0.5), 0.25)
    old_you(ctx, 540, 1450, 2.6, hcol=tint(hexc('3a3530'), GREY, 0.75), legs=None, expr='closed',
            arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (120, 40), (40 - 50 * min(1, t / 0.5), -40))])
    zip_lips(ctx, 540, 1450, 2.6, min(1, t / 0.5))
    stamp(ctx, 'TOP SECRET', 540, 450, 0.45, t, 140, -0.1)

def s_offers(ctx, t, d, S):
    office(ctx, wall=hexc('c9c3d4'))
    tn = S.at(4, 'no')
    suit_man(ctx, 760, stand(1.05), 1.05, arms='clasp', seed=1600)
    suit_man(ctx, 960, stand(1.0), 1.0, arms='clasp', seed=1650)
    p = pop(t, 0.2)
    if p > 0.01:
        ctx.save(); ctx.translate(800, 1060); ctx.scale(p, p)
        shape(ctx, rect(-170, -20, 170, 120), hexc('2a2a2a'), 5, 9800)
        shape(ctx, [(-170, -20), (170, -20), (150, -140), (-150, -140)], hexc('3a3a3a'), 5, 9801)
        for k in range(6): shape(ctx, rect(-150 + k * 50, 0, -110 + k * 50, 90), hexc('7bbf6a'), 2, 9802 + k)
        ctx.restore()
    glow_text(ctx, '$1,000,000', 760, 360, 150, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=pop(t, 0.35), rot=0.05)
    shake = 0.25 * math.sin((t - tn) * 18) if tn < t < tn + 0.8 else 0
    old_you(ctx, 280, stand(1.15), 1.15, hcol=tint(hexc('3a3530'), GREY, 0.8), expr='stern', arms='clasp', headrot=shake)
    stamp(ctx, 'NO.', 280, 560, tn, t, 150, -0.12)

def s_spy(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('1c2233')); ctx.paint(); ctx.new_path()
    shape(ctx, rect(-50, 300, 1130, 1330), hexc('2a3148'), 0, 0)
    for k in range(9): rough(ctx, [(0, 360 + k * 110), (W, 360 + k * 110)], 2, 9900 + k, hexc('3a4260'))
    shape(ctx, rect(-300, 1330, W + 300, 2200), hexc('3a3f4a'), 5, 9910)
    tn = S.at(5, 'Nothing')
    shape(ctx, [(380, 1330), (360, 1060), (720, 1060), (700, 1330)], hexc('6c7a6c'), 5, 9920)       # trash can
    for k in range(3): rough(ctx, [(430 + k * 110, 1090), (440 + k * 110, 1310)], 3, 9921 + k, hexc('55625a'))
    ctx.save(); ctx.translate(540, 1000); ctx.rotate(math.pi - 0.15)
    suit_man(ctx, 0, 0, 1.0, legs=None, arms='up', seed=1620)                                       # head-first in the bin
    ctx.restore()
    for sx in (-1, 1):
        rough(ctx, [(540 + sx * 28, 880), (540 + sx * 40, 700), (540 + sx * 60, 560)], 7, 9930 + sx, hexc('1a1a1d'))
    rng = random.Random(2)
    for k in range(5):
        tt = (t * 1.2 + k * 0.2) % 1
        x = 540 + (k - 2) * 130 * tt; y = 1050 - 500 * tt + 600 * tt * tt
        shape(ctx, ell(x, y, 26, 16, 10), hexc(['e3c24a', 'c9c9c9', '8a6446', 'f2f2f2', '9ac46a'][k]), 3, 9940 + k)
    ctx.save(); ctx.move_to(240, 900); ctx.line_to(520, 1080); ctx.line_to(420, 1140); ctx.close_path()
    ctx.set_source_rgba(1, 1, 0.7, 0.18); ctx.fill(); ctx.restore()
    glow_text(ctx, 'A SPY.', 540, 320, 150, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.05))
    stamp(ctx, 'NOTHING', 540, 520, tn, t, 140, 0.1)

def s_ninety(ctx, t, d, S):
    kitchen(ctx)
    ty = S.at(6, 'you')
    old_you(ctx, 330, stand(1.1), 1.1, expr='smile', arms='pointR' if t > ty - 0.3 else 'down', look=(6, 0))
    you(ctx, 780, stand(1.1), 1.1, expr='shock' if t > ty else 'neutral', look=(-6, 0))
    shape(ctx, rect(420, 1240, 660, 1330), hexc('f2b8c6'), 4, 9950)
    for k in range(2):
        rough(ctx, [(500 + k * 60, 1240), (500 + k * 60, 1190)], 5, 9951 + k, hexc('e3c24a'))
        radial(ctx, 500 + k * 60, 1180, 30, (1, 0.8, 0.3), 0.8)
    text(ctx, '90', 540, 1310, 70, 'Bebas Neue', (1, 1, 1), anchor='c')
    glow_text(ctx, 'AGE 90', 540, 330, 140, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.1))
    glow_text(ctx, 'ONLY YOU.', 540, 500, 150, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=pop(t, ty))

def s_promise(ctx, t, d, S):
    kitchen(ctx); dark(ctx, 0.25)
    l8 = S.L(8)[0]
    old_you(ctx, 290, 1420, 1.9, legs=None, expr='stern', look=(8, 0), arms='down', rot=0.08)
    you(ctx, 800, 1420, 1.9, legs=None, expr='neutral' if t < l8 else 'smile', look=(-6, 0),
        arms='down' if t < l8 else [((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (120, -20), (110, -110))])
    say(ctx, '"Promise you\'ll\nnever tell."', 60, 330, 640, 590, (260, 980), 0.05, t, 70)
    glow_text(ctx, 'I PROMISE.', 780, 760, 120, 'Bebas Neue', GOLD, None, pop=pop(t, l8))

def s_drawer(ctx, t, d, S):
    kitchen(ctx)
    to = S.at(9, 'opens'); ti = S.L(10)[0]
    shape(ctx, rect(140, 1000, 940, 1330), hexc('b08a62'), 5, 9960)
    shape(ctx, rect(170, 1030, 910, 1150), hexc('c49c70'), 4, 9961)
    out = 160 * ease_out((t - to) / 0.6) if t > to else 0
    radial(ctx, 540, 1250, 400 * (out / 160), (1, 0.85, 0.4), 0.7 * (out / 160))
    shape(ctx, rect(150 - out * 0.15, 1170 + out * 0.4, 930 + out * 0.15, 1320 + out * 0.6), hexc('c49c70'), 5, 9962)
    shape(ctx, ell(540, 1240 + out * 0.5, 50, 12, 14), hexc('6b4a35'), 3, 9963)
    if t > ti:
        n = min(9, int((t - ti) / 0.22) + 1)
        for k in range(n):
            col, row = k % 3, k // 3
            bakery_box(ctx, 290 + col * 250, 900 - row * 110, 1.0, (k % 2 - 0.5) * 0.08, 9970 + k)
    old_you(ctx, 150, stand(0.9, 1330) - 0, 0.9, expr='smile', arms='pointR') if t < ti else None
    glow_text(ctx, 'THE DRAWER', 540, 280, 140, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.05))
    glow_text(ctx, '50 YEARS OF BOXES', 540, 440, 100, 'Bebas Neue', GOLD, None, pop=pop(t, S.at(10, 'fifty')))

def s_store(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('2a2f36')); ctx.paint(); ctx.new_path()
    radial(ctx, 540, 1150, 800, (0.95, 0.75, 0.4), 0.3)
    ctx.save(); ctx.translate(4 * math.sin(t * 50) * max(0, 1 - t * 2), 0)
    you(ctx, 540, 1560, 3.0, legs=None, expr='shock', arms='tense')
    ctx.restore()
    cy = 980 + 900 * max(0, t - 0.2) ** 2 * 3
    cookie(ctx, 820, cy, 50, 9990)
    stamp(ctx, 'STORE-BOUGHT', 540, 420, 0.05, t, 150, -0.1)
    glow_text(ctx, 'ALL OF IT.', 540, 680, 120, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, S.at(11, 'All')))

def s_wink(ctx, t, d, S):
    kitchen(ctx)
    tw = S.at(12, 'winks') + 0.1; tp = S.at(12, 'Presentation')
    old_you(ctx, 400, 1500, 2.2, legs=None, expr='smile', look=(6, 0),
            arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (150, 80), (190, -20))])
    if tw < t < tw + 0.7: wink(ctx, 400, 1500, 2.2)
    if tw < t < tw + 0.5: star(ctx, 500, 1120, 40, rot=t * 6, alpha=1 - (t - tw) / 0.5, seed=9995)
    say(ctx, '"Presentation, kid."' if t < S.at(12, "It's") else '"It\'s ALL\npresentation."', 120, 300, 960, 560, (380, 1000), tp - 0.05, t, 72)
    px, py = 830, 1420
    shape(ctx, ell(px, py, 180, 46, 30), (1, 1, 1), 4, 9996)
    for k in range(10): rough(ctx, ell(px + 170 * math.cos(k * 0.628), py + 42 * math.sin(k * 0.628), 12, 9, 8), 2, 9997 + k, hexc('d0c7b5'), closed=True)
    for k in range(4): cookie(ctx, px - 75 + k * 50, py - 16 - (10 if k % 2 else 0), 28, 9330 + k)
    if t < tw + 0.9: glow_text(ctx, '*WINK*', 760, 1180, 90, 'Bebas Neue', GOLD, None, pop=pop(t, tw))

def s_years(ctx, t, d, S):
    kitchen(ctx)
    u = ease_io(t / (d * 0.8))
    crowd(ctx, t, [110, 250, 830, 970], 1460, 0.95, seed=9650)
    hc = tint(HAIR, GREY, u)
    if u < 0.5:
        person3(ctx, 540, stand(1.15, 1430), 1.15, 'hoodie', 'spiky', hc, expr='smile', seed=300,
                arms=[((-68, 44), (-110, 110), (-60, 120)), ((68, 44), (110, 110), (60, 120))])
    else:
        old_you(ctx, 540, stand(1.15, 1430), 1.15, hcol=hc, expr='smile', arms=[((-68, 44), (-110, 110), (-60, 120)), ((68, 44), (110, 110), (60, 120))])
    plate(ctx, 540, stand(1.15, 1430) + 125 * 1.15, 5, 1.0)
    for k in range(4):                                                        # flying calendar pages
        tt = (t * 1.5 + k * 0.25) % 1
        ctx.save(); ctx.translate(200 + k * 220 + 200 * tt, 500 - 300 * tt); ctx.rotate(tt * 3)
        shape(ctx, rect(-50, -40, 50, 40), (1, 1, 1), 3, 9660 + k, alpha=1 - tt)
        ctx.restore()
    glow_text(ctx, f'+{int(50 * u)} YEARS', 540, 300, 150, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=pop(t, 0.05))
    glow_text(ctx, 'NOW THEY BEG YOU', 540, 470, 90, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, S.at(13, 'Now')))

def s_never2(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('3b2e2a')); ctx.paint(); ctx.new_path()
    radial(ctx, 540, 1000, 800, (1, 0.8, 0.5), 0.25)
    old_you(ctx, 540, 1450, 2.6, legs=None, expr='smile',
            arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (120, 40), (40 - 50 * min(1, t / 0.5), -40))])
    zip_lips(ctx, 540, 1450, 2.6, min(1, t / 0.5))
    if t > 0.7: wink(ctx, 540, 1450, 2.6)
    stamp(ctx, 'TOP SECRET', 540, 450, 0.45, t, 140, -0.1)

def s_grandkid(ctx, t, d, S):
    kitchen(ctx)
    u = ease_out(min(1, t / 1.6))
    old_you(ctx, 380, 880, 1.3, legs=None, expr='smile', look=(6, 0), arms=TABLE_ARMS)
    if t < 1.6:
        kid(ctx, lerp(1200, 740, u), stand(0.75, 1460), 0.75, walk=t * 10, expr='smile', look=(-6, 0))
        table(ctx)
    else:
        kid(ctx, 740, 1000, 0.95, legs=None, rot=-0.06, expr='smile', look=(-6, 0), arms='table')
        table(ctx)
    plate(ctx, 560, 1185)
    glow_text(ctx, 'YOUR GRANDKID', 540, 300, 120, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, S.at(15, 'grandkid')))

SHOTS = [(0, s_whisper), (1, s_beg), (2, s_who), (3, s_never), (4, s_offers), (5, s_spy), (6, s_ninety), (7, s_promise),
         (9, s_drawer), (11, s_store), (12, s_wink), (13, s_years), (14, s_never2), (15, s_grandkid), (16, s_end)]

if __name__ == '__main__':
    run(SHOTS)

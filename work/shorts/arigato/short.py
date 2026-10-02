"""POV: You lied on your résumé — "Arigato." Vertical stickman short."""
import sys, json, math, subprocess
import cairo
sys.path.insert(0, '.')
import stickkit as K
from stickkit import *
K.W, K.H = 1080, 1920          # set BEFORE grain_layers()
W, H = K.W, K.H
LINES = [l.strip() for l in open('script.txt') if l.strip()]
LT = json.load(open('lt.json'))
END = LT[-1][1] + 3.4

class Sc:
    def __init__(self, t0): self.t0 = t0
    def L(self, i): return (LT[i][0] - self.t0, LT[i][1] - self.t0)
    def at(self, i, sub):
        k = LINES[i].find(sub); f = max(k, 0) / max(len(LINES[i]), 1); s, e = self.L(i); return s + (e - s) * f

FLOOR = 1450
def stand(s): return FLOOR - 334 * s

# ---------- cast / props ----------
SHIRT = hexc('dce6f0'); WALL = hexc('cfd6d4'); CARPET = hexc('7c8784')

def me(ctx, x, y, s, **kw):          # "YOU": spiky hair, light-blue shirt + tie
    kw.setdefault('outfit', 'vest'); kw.setdefault('color', SHIRT)
    hero(ctx, x, y, s, **kw)

def boss(ctx, x, y, s, **kw):
    kw.setdefault('width', 1.18)
    person3(ctx, x, y, s, 'suit', 'none', hexc('8d8a84'), extra='bald', beard='mous', wrinkles=True, seed=2700,
            color=hexc('3a3f4a'), tie=hexc('b0262c'), **kw)

def tanaka(ctx, x, y, s, **kw):      # the Japanese client
    kw.setdefault('glasses', 'round')
    person3(ctx, x, y, s, 'suit', 'slick', hexc('16171b'), seed=2800, color=hexc('22262e'), tie=hexc('25407a'), **kw)

def office(ctx, wall=WALL, floor=CARPET, y=1330, window=True):
    room(ctx, wall, floor, y)
    if window:
        shape(ctx, rect(620, 260, 980, 760), hexc('a9c4d6'), 5, 3100)
        for bx, bw, bh in ((640, 70, 260), (720, 90, 380), (820, 60, 200), (890, 80, 320)):
            shape(ctx, rect(bx, 760 - bh, bx + bw, 760), hexc('8399a8'), 2.5, 3110 + bx)
        rough(ctx, [(800, 260), (800, 760)], 5, 3120); rough(ctx, [(620, 510), (980, 510)], 5, 3121)
    # plant
    shape(ctx, [(110, y), (90, y - 110), (190, y - 110), (170, y)], hexc('9a5b3a'), 4, 3130)
    for k, (dx, dy) in enumerate(((-60, -250), (0, -300), (60, -240), (-30, -200), (40, -190))):
        shape(ctx, [(140, y - 110), (140 + dx * 0.5 - 18, y - 110 + dy * 0.6), (140 + dx, y - 110 + dy), (140 + dx * 0.5 + 18, y - 110 + dy * 0.6)],
              hexc('4f7a45'), 3, 3140 + k)

def desk(ctx, x0, x1, y, seed=3200):
    shape(ctx, rect(x0, y, x1, y + 40), hexc('8a6446'), 5, seed)
    shape(ctx, rect(x0 + 20, y + 40, x1 - 20, y + 420), hexc('735238'), 5, seed + 1)

def paper(ctx, x, y, w, h, rot=0, seed=3300):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    shape(ctx, rect(-w / 2 + 12, -h / 2 + 14, w / 2 + 12, h / 2 + 14), (0, 0, 0), 0, 0, alpha=0.25)
    shape(ctx, rect(-w / 2, -h / 2, w / 2, h / 2), PAPER, 5, seed)
    ctx.restore()

def jp_flag(ctx, x, y, s, pop):
    if pop <= 0.01: return
    ctx.save(); ctx.translate(x, y); ctx.scale(pop * s, pop * s); ctx.rotate(0.08)
    rough(ctx, [(-80, -60), (-80, 160)], 6, 3400, hexc('5a4430'))
    shape(ctx, rect(-80, -60, 90, 50), (1, 1, 1), 4, 3401)
    shape(ctx, ell(5, -5, 30, 30, 24), hexc('c0322a'), 0, 0)
    ctx.restore()

def bower(ctx, fn, x, s, ang, face, legc=hexc('1a1a1d'), **kw):
    """Full-body character bowing from the hips. face=+1 faces right, -1 faces left."""
    y = stand(s)
    for sx in (-1, 1):
        rough(ctx, [(x + sx * 28 * s, y + 196 * s), (x + sx * 32 * s, y + 262 * s), (x + sx * 34 * s, y + 330 * s)], 7 * s, 3500 + sx, legc)
        shape(ctx, ell(x + sx * 34 * s + face * 12 * s, y + 334 * s, 22 * s, 9 * s, 16), hexc('151518'), 3, 3502 + sx)
    hx, hy = x, y + 196 * s
    ctx.save(); ctx.translate(hx, hy); ctx.rotate(ang * face)
    fn(ctx, 0, -196 * s, s, legs=None, **kw)
    ctx.restore()

def thought(ctx, x0, y0, x1, y1, tail, a=1.0, seed=3600):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    pts = []
    n = 12
    for i in range(n):
        a0 = 2 * math.pi * i / n; a1 = 2 * math.pi * (i + 1) / n
        pts += ell(cx + rx * math.cos((a0 + a1) / 2) * 0.86, cy + ry * math.sin((a0 + a1) / 2) * 0.86,
                   rx * 0.32, ry * 0.32, 8, (a0 + a1) / 2 - 1.3, (a0 + a1) / 2 + 1.3)
    shape(ctx, pts, (1, 1, 1), 5, seed, alpha=a)
    for k, r in enumerate((26, 17, 10)):
        u = (k + 1) / 4
        shape(ctx, ell(lerp(cx, tail[0], u + 0.1), lerp(y1, tail[1], u + 0.1), r, r, 14), (1, 1, 1), 4, seed + k + 1, alpha=a)

def strike(ctx, x0, x1, y, u, seed):
    if u <= 0: return
    rough(ctx, [(x0, y), (lerp(x0, x1, min(u, 1)), y - 10)], 9, seed, hexc('c0322a'))

# ---------- shots: fn(ctx, t_local, duration, S) ----------
def s_hook(ctx, t, d, S):
    office(ctx)
    ctx.save(); cam(ctx, 540, 1200, 1.0 + 0.06 * t / d)
    me(ctx, 540, 1000, 2.3, legs=None, expr='smile', look=(4, 2),
       arms=[((-68, 44), (-110, 150), (-60, 196)), ((68, 44), (110, 150), (60, 196))])
    paper(ctx, 540, 1440, 420, 300, -0.04)
    text(ctx, 'RÉSUMÉ', 540, 1370, 70, 'Bebas Neue', INK, anchor='c')
    for k in range(3): rough(ctx, [(380, 1410 + k * 36), (700 - k * 40, 1412 + k * 36)], 3, 3700 + k, hexc('8a8478'))
    ctx.restore()
    glow_text(ctx, 'POV:', 540, 250, 130, 'Bebas Neue', (1, 1, 1), None, pop=ease_out_back((t - 0.1) / 0.3))
    glow_text(ctx, 'THE RÉSUMÉ LIE', 540, 440, 150, 'Bebas Neue', GOLD, (0.9, 0.6, 0.1), pop=ease_out_back((t - 0.4) / 0.3), rot=-0.04)
    if t > 1.2:
        sweat(ctx, 690, 690, 1.6, alpha=min(1, (t - 1.2) * 4))

def s_resume(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('3b4a52')); ctx.paint(); ctx.new_path()
    ctx.save(); cam(ctx, 540, 900, 1.0 + 0.05 * t / d)
    paper(ctx, 540, 900, 820, 1080, -0.03)
    ctx.save(); ctx.translate(540, 900); ctx.rotate(-0.03); ctx.translate(-540, -900)
    text(ctx, 'RÉSUMÉ', 540, 520, 110, 'Bebas Neue', INK, anchor='c')
    rough(ctx, [(220, 560), (860, 560)], 4, 3800)
    text(ctx, 'Name:  YOU', 200, 650, 64)
    text(ctx, 'Skills:', 200, 750, 64)
    text(ctx, '- Microsoft Word', 230, 840, 60)
    text(ctx, '- Team player', 230, 920, 60)
    tw = S.at(1, 'fluent')
    full = '- Fluent in Japanese'
    n = int(len(full) * min(1, max(0, (t - tw + 0.15) / 0.8)))
    text(ctx, full[:n], 230, 1010, 60, color=hexc('1d3a8a'))
    if n >= len(full):
        u = min(1, (t - tw - 0.8) / 0.4)
        if u > 0:
            pts = ell(470, 990, 270, 62, 40, -2.6, -2.6 + 6.0 * u)
            rough(ctx, pts, 7, 3810, hexc('c0322a'))
    ctx.restore(); ctx.restore()
    # pen
    px, py = 230 + 20 * n + 30, 1000
    if n < len(full) and t > tw - 0.2:
        rough(ctx, [(px, py), (px + 120, py - 220)], 18, 3820, hexc('2b3b6a'))
        rough(ctx, [(px, py), (px + 14, py - 26)], 6, 3821, INK)
    jp_flag(ctx, 840, 1300, 1.2, ease_out_back((t - tw - 0.9) / 0.3))

def s_hired(ctx, t, d, S):
    office(ctx, window=False)
    desk(ctx, 140, 940, 1150)
    woman(ctx, 540, 820, 1.45, legs=None, expr='blank', look=(0, 4),
          arms=[((-68, 44), (-110, 150), (-70, 210)), ((68, 44), (140, 60 + 40 * max(0, 1 - abs(t - 0.6) * 4)), (150, 170))])
    paper(ctx, 540, 1110, 360, 120, 0.04)
    text(ctx, 'RÉSUMÉ', 470, 1128, 44, 'Bebas Neue', INK)
    stamp(ctx, 'HIRED', 540, 1100, 0.65, t, 90, -0.12)
    # zero checks
    glow_text(ctx, 'BACKGROUND CHECK:', 540, 300, 90, 'Bebas Neue', (1, 1, 1), None, pop=ease_out_back((t - 0.05) / 0.3))
    glow_text(ctx, 'SKIPPED', 540, 430, 120, 'Bebas Neue', GREEN, (0.1, 0.6, 0.3), pop=ease_out_back((t - 0.35) / 0.3), rot=0.04)

def s_boss(ctx, t, d, S):
    office(ctx)
    ctx.save(); cam(ctx, 540, 1100, 1.0 + 0.04 * t / d)
    # door on the left
    shape(ctx, rect(0, 480, 260, 1330), hexc('6b4f3a'), 5, 3900)
    shape(ctx, ell(230, 920, 12, 12, 12), GOLD, 3, 3901)
    u = ease_out(min(1, t / 1.7))
    walking = t < 1.7
    tanaka(ctx, lerp(-260, 170, u), stand(1.15), 1.15, expr='stern', arms='down', walk=t * 10 if walking else None, look=(6, 0))
    boss(ctx, lerp(-60, 400, u), stand(1.15), 1.15, expr='smile', arms='down' if walking else 'pointR', walk=t * 10 + 1 if walking else None, look=(6, 0))
    desk(ctx, 620, 1120, 1180)
    me(ctx, 860, 950, 1.15, legs=None, expr='shock' if t > 1.5 else 'smile', look=(-6, 0), arms='table')
    # coffee mug
    shape(ctx, rect(700, 1110, 760, 1180), (1, 1, 1), 4, 3910)
    if t > 1.5: sweat(ctx, 940, 780, 1.2, alpha=min(1, (t - 1.5) * 4))
    ctx.restore()
    glow_text(ctx, 'THE BOSS', 540, 300, 100, 'Bebas Neue', (1, 1, 1), None, pop=ease_out_back((t - 0.4) / 0.3))
    glow_text(ctx, '+ A MAN IN A SUIT', 540, 420, 80, 'Bebas Neue', GOLD, None, pop=ease_out_back((t - S.at(3, 'man')) / 0.3))

def s_deal(ctx, t, d, S):
    office(ctx, wall=hexc('c7cccb'))
    tb = S.at(5, 'billion')
    shock = t > S.at(5, 'translating')
    z = 1.0 + 0.10 * ease_io(t / d)
    ctx.save(); cam(ctx, 790 if shock else 540, 1150, z)
    boss(ctx, 270, 1330, 1.9, legs=None, expr='smile', look=(8, 0), arms='pointR')
    me(ctx, 820, 1330, 1.9, legs=None, expr='shock' if shock else 'worried', look=(-6, 0),
       arms='tense', shrug=12 if shock else 0)
    if shock:
        for k in range(3):
            tt = (t * 1.3 + k * 0.33) % 1
            sweat(ctx, 920 + k * 16, 1010 + tt * 140, 1.4, alpha=1 - tt)
    ctx.restore()
    l4 = S.L(4)[0]; l5 = S.L(5)[0]
    if t < l5 - 0.1:
        say(ctx, 'He only speaks\nJapanese.', 90, 330, 770, 600, (300, 900), l4 - 0.05, t, 70)
    else:
        say(ctx, "You're translating\nthe deal.", 90, 330, 770, 600, (300, 900), l5 - 0.05, t, 66)
    glow_text(ctx, '$1,000,000,000', 540, 760, 130, 'Bebas Neue', GOLD, (0.9, 0.7, 0.1),
              pop=ease_out_back((t - tb) / 0.3), rot=-0.05)
    if t > tb: radial(ctx, 540, 760, 500, (1, 0.85, 0.3), 0.15)
    if t > tb + 0.6:
        stamp(ctx, 'NO PRESSURE', 540, 930, tb + 0.6, t, 70, 0.1)

def s_bow(ctx, t, d, S):
    office(ctx, window=True)
    tb1 = S.at(6, 'bows') - 0.1; tb2 = S.at(7, 'bow') - 0.1
    a1 = 0.6 * ease_out_back((t - tb1) / 0.45, 1.2) if t > tb1 else 0
    a2 = 0.6 * ease_out_back((t - tb2) / 0.45, 1.2) if t > tb2 else 0
    bower(ctx, tanaka, 220, 1.2, a1, 1, expr='closed' if a1 > 0.3 else 'stern', arms='down')
    bower(ctx, me, 860, 1.2, a2, -1, expr='worried', arms='tense', look=(-6, 4), legc=hexc('2c3240'))
    if t > tb2 + 0.2:
        sweat(ctx, 860 - 120, 800, 1.3, alpha=min(1, (t - tb2 - 0.2) * 4))
    glow_text(ctx, 'BOW', 260, 330, 120, 'Bebas Neue', (1, 1, 1), None, pop=ease_out_back((t - tb1) / 0.3), rot=-0.06)
    glow_text(ctx, 'BOW BACK', 780, 470, 110, 'Bebas Neue', GOLD, None, pop=ease_out_back((t - tb2) / 0.3), rot=0.06)

THOUGHTS = [('SUSHI?', 330, 470), ('KARATE?', 740, 440), ('NARUTO?', 420, 640)]
def s_word(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('2a2f36')); ctx.paint(); ctx.new_path()
    radial(ctx, 540, 1200, 800, (0.9, 0.8, 0.6), 0.25)
    ctx.save(); cam(ctx, 540, 1200, 1.0 + 0.10 * ease_io(t / d)); ctx.translate(3 * math.sin(t * 40), 0)
    me(ctx, 540, 1520, 3.0, legs=None, expr='worried', look=(4, -6), arms='tense')
    for k in range(3):
        tt = (t * 1.1 + k * 0.33) % 1
        sweat(ctx, 680 + k * 30, 1020 + tt * 200, 1.8, alpha=1 - tt)
    ctx.restore()
    thought(ctx, 120, 300, 960, 800, (600, 1000), a=min(1, t * 5))
    for k, (w_, x, y) in enumerate(THOUGHTS):
        t0 = 0.1 + k * 0.45
        glow_text(ctx, w_, x, y, 100, 'Bebas Neue', INK, None, pop=ease_out_back((t - t0) / 0.25), outline=INK)
        if t > t0 + 0.25:
            ctx.select_font_face('Bebas Neue'); ctx.set_font_size(100); e = ctx.text_extents(w_)
            strike(ctx, x - e.width / 2 - 10, x + e.width / 2 + 10, y, (t - t0 - 0.25) / 0.15, 3950 + k)

def s_arigato(ctx, t, d, S):
    office(ctx)
    T1 = 1.7                                    # cut to the stare
    if t < T1:
        boss(ctx, 540, stand(0.9) - 60, 0.9, expr='smile', arms='clasp')
        bower(ctx, tanaka, 220, 1.2, 0.6, 1, expr='closed', arms='down')
        a2 = 0.6 if t < 1.0 else 0.6 * (1 - ease_out((t - 1.0) / 0.3))
        bower(ctx, me, 860, 1.2, a2, -1, expr='smile', arms='down', legc=hexc('2c3240'))
        glow_text(ctx, 'ARIGATO.', 540, 380, 210, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=ease_out_back((t - 0.05) / 0.35), rot=-0.05)
        return
    u = t - T1
    if u < 1.3:                                  # Tanaka's blank stare + silence
        ctx.save(); cam(ctx, 540, 1100, 1.0 + 0.05 * u)
        tanaka(ctx, 540, 1400, 2.8, legs=None, expr='blank', arms='down')
        ctx.restore()
        say(ctx, '...', 620, 360, 940, 560, (640, 760), 0.35, u, 110)
        glow_text(ctx, 'DEAL STATUS:', 540, 230, 90, 'Bebas Neue', (1, 1, 1), None, pop=ease_out_back((u - 0.1) / 0.3))
        stamp(ctx, 'LOADING...', 300, 470, 0.5, u, 80, -0.12)
        return
    v = u - 1.3                                  # final close-up: frozen smile
    ctx.set_source_rgb(*hexc('2a2f36')); ctx.paint(); ctx.new_path()
    radial(ctx, 540, 1150, 800, (0.95, 0.75, 0.4), 0.28)
    ctx.save(); cam(ctx, 540, 1150, 1.0 + 0.06 * v)
    me(ctx, 540, 1550, 3.4, legs=None, expr='smile', look=(0, 0), arms='down')
    sweat(ctx, 760, 900 + 60 * min(1, v), 2.2)
    ctx.restore()
    if t > d - 1.0: dark(ctx, min(1, (t - (d - 1.0)) / 0.9), (0, 0, 0))

SHOTS = [(0, s_hook), (1, s_resume), (2, s_hired), (3, s_boss), (4, s_deal), (6, s_bow), (8, s_word), (9, s_arigato)]

def timeline():
    out = []
    for i, (li, fn) in enumerate(SHOTS):
        st = 0.0 if i == 0 else LT[li][0] - 0.18
        en = END if i == len(SHOTS) - 1 else LT[SHOTS[i + 1][0]][0] - 0.18
        out.append((st, en, fn))
    return out

def main():
    rng_mode = len(sys.argv) > 1 and sys.argv[1] == '--range'
    only = [] if rng_mode else [float(a) for a in sys.argv[1:]]
    TL = timeline(); grains = grain_layers()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    NF = int(END * 24); ff = None
    if not only:
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                               '-r', '24', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                               '-pix_fmt', 'yuv420p', sys.argv[4] if rng_mode else 'video.mp4'], stdin=subprocess.PIPE)
    frames = [int(x * 24) for x in only] if only else (range(int(sys.argv[2]), min(NF, int(sys.argv[3]))) if rng_mode else range(NF))
    for f in frames:
        t = f / 24; K.BOIL = f // 2
        ctx = cairo.Context(surf)
        ctx.set_operator(cairo.OPERATOR_SOURCE); ctx.set_source_rgb(0, 0, 0); ctx.paint(); ctx.set_operator(cairo.OPERATOR_OVER); ctx.new_path()
        for a, b, fn in TL:
            if a <= t < b: ctx.save(); fn(ctx, t - a, b - a, Sc(a)); ctx.restore(); break
        ctx.set_source_surface(grains[K.BOIL % 4], 0, 0); ctx.paint(); vignette(ctx, 0.35)
        for (st, en), s in zip(LT, LINES):
            if st - 0.05 <= t < en + 0.25: caption(ctx, s)
        surf.flush()
        if ff: ff.stdin.write(bytes(surf.get_data()))
        else: surf.write_to_png(f'test_{f:05d}.png')
    if ff: ff.stdin.close(); ff.wait()

if __name__ == '__main__':
    main()

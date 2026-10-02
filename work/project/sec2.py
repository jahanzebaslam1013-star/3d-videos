"""DUNKI — Section 2 (part2.json, global lines 26-47). Roman Urdu on screen, no captions."""
import math, random
import pk, stickkit as K, engine
from pk import *
from engine import load_part
from sec1 import busts_row, evening_yard, shop

LT, DUR, FIRST = load_part('part2.json')
END = DUR + 0.6
A = lambda i: LT[i][0]                       # absolute start of local line i
AF = lambda i, f: LT[i][0] + (LT[i][1] - LT[i][0]) * f
def stand(s, floor): return floor - 334 * s
def pop(t, t0, d=0.3): return ease_out_back((t - t0) / d) if t > t0 else 0

GREY = hexc('9a968e')
def saleem(ctx, x, y, s, **kw):
    person(ctx, x, y, s, 'kameez', 'short', GREY, beard='full', wrinkles=True, color=hexc('8a7a62'),
           seed=kw.pop('seed', 3600), **kw)

def label(ctx, s, x, y, p, size=80, col=hexc('17171a'), ink=(1, 1, 1), rot=0.0, w=None, seed=6000):
    if p <= 0.01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(p, p)
    hw = w or size * len(s) * 0.26 + 40
    shape(ctx, rect(-hw, -size * 0.75, hw, size * 0.75), col, 4, seed, ink=ink)
    utext(ctx, s, 0, -size * 0.3, size, ink); ctx.restore()

def sparkle(ctx, x, y, r, a):
    if a <= 0: return
    radial(ctx, x, y, r * 2.2, (1, 0.95, 0.6), 0.8 * a)
    ctx.save(); ctx.translate(x, y); ctx.set_source_rgba(1, 1, 0.9, a); ctx.set_line_width(4)
    for k in range(4):
        ang = k * math.pi / 4; L_ = r if k % 2 == 0 else r * 0.55
        ctx.move_to(-L_ * math.cos(ang), -L_ * math.sin(ang)); ctx.line_to(L_ * math.cos(ang), L_ * math.sin(ang)); ctx.stroke()
    ctx.restore()

def bangle(ctx, x, y, r, seed):
    for rr in (r, r - 9):
        rough(ctx, ell(x, y, rr, rr * 0.42, 30), 7, seed + rr, hexc('d9b44a'), closed=True)
    rough(ctx, ell(x, y, r - 4, (r - 4) * 0.42, 30, math.pi * 1.1, math.pi * 1.6), 2.5, seed + 9, hexc('fff2c0'))

def timer(ctx, t_abs, x=1700, y=110):
    """2:00 phone timer, starts at line 19 + 70%."""
    t0 = AF(19, 0.7)
    if t_abs < t0: return
    left = max(0, 120 - (t_abs - t0)); p = pop(t_abs, t0)
    ctx.save(); ctx.translate(x, y); ctx.scale(p, p)
    shape(ctx, rect(-170, -62, 170, 62), hexc('17171a'), 4, 6100, ink=(1, 1, 1))
    col = hexc('ff5a4a') if int(t_abs * 2) % 2 else (1, 1, 1)
    text(ctx, f'{int(left // 60)}:{int(left % 60):02d}', 0, 30, 96, 'Bebas Neue', col, anchor='c')
    ctx.restore()

# ---------------- sets ----------------
def courtyard_night(ctx, t):
    evening_yard(ctx, t, 1.0); stars(ctx, 50, 4013, t); moon(ctx, 300, 150, 40)

def warehouse(ctx, t, beam=True):
    shape(ctx, rect(-300, -300, W + 300, 820), hexc('4a4d50'), 0, 1)
    for k in range(-1, 15): rough(ctx, [(k * 150, -300), (k * 150 + 4, 820)], 2.5, 6200 + k, hexc('3c3f42'))
    shape(ctx, rect(-300, 820, W + 300, H + 300), hexc('35383b'), 4, 6220)
    shape(ctx, rect(1240, 110, 1440, 190), hexc('9fb0b8'), 4, 6221)              # high window
    for k in range(4): rough(ctx, [(1265 + k * 50, 110), (1265 + k * 50, 190)], 4, 6222 + k, hexc('2a2c2e'))
    if beam:
        ctx.move_to(1240, 190); ctx.line_to(1440, 190); ctx.line_to(1200, 900); ctx.line_to(820, 900); ctx.close_path()
        ctx.set_source_rgba(1, 0.97, 0.85, 0.07 + 0.01 * math.sin(t * 2)); ctx.fill()

def map_base(ctx, desert=0.0):
    land = K.tint(hexc('e3d3ad'), hexc('e0a25a'), desert)
    shape(ctx, rect(-600, -600, W + 600, H + 600), land, 0, 1)
    sea = hexc('8fb8d6')
    med = [(120, 300), (380, 250), (620, 300), (820, 250), (1080, 300), (1120, 360), (900, 380), (700, 360), (520, 400), (300, 380), (100, 360)]
    shape(ctx, med, sea, 4, 6300)
    shape(ctx, [(-600, 140), (-600, -600), (W + 600, -600), (W + 600, 140), (1300, 120), (900, 160), (400, 150)], sea, 4, 6301, alpha=0)
    shape(ctx, [(1000, 420), (1040, 430), (1150, 760), (1110, 770)], sea, 4, 6302)          # red sea
    shape(ctx, [(1250, 470), (1330, 480), (1420, 540), (1380, 560), (1290, 520)], sea, 4, 6303)  # gulf
    shape(ctx, [(1200, 800), (1500, 620), (1700, 600), (1900, 640), (W + 600, 640), (W + 600, H + 600), (1100, H + 600)], sea, 4, 6304)
    shape(ctx, [(560, 180), (640, 150), (760, 240), (800, 300), (740, 290), (650, 220)], K.tint(hexc('d6c9a6'), hexc('c9b996'), 0), 3, 6305)  # italy boot (rough)
    for k in range(5):
        rough(ctx, [(140 + k * 220, 330 + 8 * math.sin(k)), (200 + k * 220, 330 + 8 * math.sin(k + 1))], 2, 6310 + k, hexc('5f86a8'), alpha=0.5)

PINS = [('PAKISTAN', 1640, 430), ('DUBAI', 1380, 560), ('?', 1180, 640), ('?', 880, 470), ('', 620, 450)]
def pin(ctx, x, y, p, col=hexc('c0322a'), name=None, seed=6400):
    if p <= 0.01: return
    ctx.save(); ctx.translate(x, y); ctx.scale(p, p)
    shape(ctx, [(0, 0), (-26, -50), (-26, -70), (0, -92), (26, -70), (26, -50)], col, 4, seed)
    shape(ctx, ell(0, -66, 10, 10, 12), (1, 1, 1), 2, seed + 1)
    if name: text(ctx, name, 0, 52, 54, 'Bebas Neue', INK, anchor='c')
    ctx.restore()

def route(ctx, pts, u, seed=6450):
    """dashed travel line through pts, drawn up to fraction u."""
    segs = list(zip(pts[:-1], pts[1:])); tot = sum(math.dist(a, b) for a, b in segs); L_ = u * tot
    ctx.set_source_rgb(*hexc('c0322a')); ctx.set_line_width(7); ctx.set_dash([22, 16]); ctx.set_line_cap(1)
    for (a, b) in segs:
        d = math.dist(a, b)
        if L_ <= 0: break
        f = min(1, L_ / d)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - d * 0.25
        n = 24; pts_ = []
        for i in range(int(n * f) + 1):
            s = i / n; pts_.append(((1 - s) ** 2 * a[0] + 2 * (1 - s) * s * mx + s * s * b[0], (1 - s) ** 2 * a[1] + 2 * (1 - s) * s * my + s * s * b[1]))
        ctx.move_to(*pts_[0]); [ctx.line_to(*p) for p in pts_[1:]]; ctx.stroke(); L_ -= d
    ctx.set_dash([])
    return

def plane_icon(ctx, x, y, s, rot):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    shape(ctx, [(-60, -8), (50, -8), (70, 0), (50, 8), (-60, 8)], (1, 1, 1), 3, 6500)
    shape(ctx, [(-5, -6), (-25, -50), (-10, -50), (20, -6)], (1, 1, 1), 3, 6501)
    shape(ctx, [(-5, 6), (-25, 50), (-10, 50), (20, 6)], (1, 1, 1), 3, 6502)
    shape(ctx, [(-60, -6), (-72, -26), (-62, -26), (-48, -6)], (1, 1, 1), 3, 6503)
    ctx.restore()

def skyline(ctx, x, base, p):
    if p <= 0.01: return
    ctx.save(); ctx.translate(x, base); ctx.scale(p, p)
    for k, (dx, h) in enumerate(((-60, 90), (-30, 140), (0, 220), (30, 120), (60, 80))):
        shape(ctx, [(dx - 12, 0), (dx - 10, -h), (dx, -h - (30 if k == 2 else 0)), (dx + 10, -h), (dx + 12, 0)], hexc('8a96a6'), 3, 6510 + k)
    ctx.restore()

def map_scene(ctx, t, ta, cx, cy, zoom):
    """the whole journey map; ta = absolute part time"""
    desert = ease_io((ta - A(7) + 0.2) / 1.2) if ta > A(7) - 0.2 else 0
    ctx.save(); cam(ctx, cx, cy, zoom)
    map_base(ctx, desert)
    italy_a = 0.55
    pin(ctx, 700, 225, 1, col=hexc('9aa0a6'), seed=6420)
    text(ctx, 'ITALY', 860, 200, 54, 'Bebas Neue', hexc('6a6e74'), anchor='c')
    times = [A(4) - 0.1, AF(4, 0.45), AF(5, 0.35), AF(5, 0.75), A(7) + 0.1]
    pts = [(x, y - 66) for _, x, y in PINS]
    # how far along the route
    k = 0; u = 0.0
    for i in range(1, len(times)):
        if ta >= times[i]: k = i
    if k < len(times) - 1:
        frac = min(1, max(0, (ta - times[k]) / max(0.4, (times[k + 1] - times[k]) * 0.8)))
    else: frac = 0
    seg_u = (k + ease_io(frac)) / (len(pts) - 1)
    route(ctx, pts, min(1, seg_u))
    for i, (nm, x, y) in enumerate(PINS):
        pin(ctx, x, y, pop(ta, times[i] + (0.0 if i == 0 else 0.7)), name=nm, seed=6400 + i * 3)
    skyline(ctx, 1380, 470, pop(ta, AF(4, 0.6), 0.4))
    # plane position along route
    if k < len(pts) - 1:
        a, b = pts[k], pts[k + 1]; s = ease_io(frac)
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - math.dist(a, b) * 0.25
        px = (1 - s) ** 2 * a[0] + 2 * (1 - s) * s * mx + s * s * b[0]; py = (1 - s) ** 2 * a[1] + 2 * (1 - s) * s * my + s * s * b[1]
        dx = 2 * (1 - s) * (mx - a[0]) + 2 * s * (b[0] - mx); dy = 2 * (1 - s) * (my - a[1]) + 2 * s * (b[1] - my)
        plane_icon(ctx, px, py, 0.9, math.atan2(dy, dx))
    # agents popping at the middle pins
    for i, (x, y) in enumerate(((1380, 560), (1180, 640), (880, 470))):
        ag = pop(ta, times[i + 1] + 0.9)
        if ag > 0.01:
            ctx.save(); ctx.translate(x + 110, y - 40); ctx.scale(ag, ag)
            agent(ctx, 0, 0, 0.42, expr='smile', legs=None, look=(-4, 0), seed=3500 + i * 11)
            ctx.restore()
    ctx.restore()

# ---------------- shots ----------------
def sc_gold(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 600, 1.05 + 0.12 * ease_io(t / d))
    courtyard_night(ctx, t)
    lantern(ctx, 1500, 900, 0.9, t)
    charpai(ctx, 700, 960, 1.4)
    abba(ctx, 640, 560, 1.1, expr='sad', legs=None, arms='clasp', look=(6, 0))
    hamza(ctx, 330, stand(1.1, 1000), 1.1, expr='worried', look=(6, 0), arms='clasp')
    wu = ease_out(min(1, t / 1.6))
    ammi(ctx, lerp(1500, 1080, wu), stand(1.1, 1000), 1.1, expr='sad', look=(-6, 2), walk=t * 9 if wu < 1 else None,
         arms=[((-68, 44), (-130, 120), (-200, 110)), ((68, 44), (40, 130), (-120, 120))])
    hx = lerp(1500, 1080, wu) - 1.1 * 170; hy = stand(1.1, 1000) + 1.1 * 115
    for j in range(3): bangle(ctx, hx + j * 34 - 34, hy - 20 - j * 6, 34, 6600 + j * 10)
    ctx.restore()
    g = max(0, 1 - abs(t - 1.9) / 0.5)
    sparkle(ctx, 960 + (hx - 960) * 1.1, 600 + (hy - 600) * 1.1 - 20, 46, g)
    label(ctx, 'Jahez ka sona', 1500, 160, pop(t, 0.9), 70, seed=6610)

def sc_silence(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 620, 1.0 + 0.06 * t / d)
    courtyard_night(ctx, t)
    lantern(ctx, 960, 880, 0.7, t)
    charpai(ctx, 760, 980, 1.2)
    ctx.push_group()
    abba(ctx, 700, 640, 0.95, expr='sad', legs=None, arms='clasp', look=(0, 4))
    ammi(ctx, 860, 660, 0.9, expr='sad', legs=None, arms='clasp', look=(-3, 4))
    hamza(ctx, 1240, stand(0.95, 1010), 0.95, expr='sad', look=(-4, 4), arms='clasp')
    ctx.pop_group_to_source(); ctx.paint_with_alpha(1)
    ctx.restore()
    dark(ctx, 0.38)
    radial(ctx, 960, 860, 380, (1, 0.75, 0.35), 0.18)
    stamp(ctx, 'NO WAY BACK', 960, 300, AF(1, 0.62) - S.t0, t, 140, rot=-0.08)

def sc_airport(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 540, 1.0 + 0.1 * ease_io(t / d))
    shape(ctx, rect(-300, -300, W + 300, 820), hexc('d8d6cf'), 0, 1)
    shape(ctx, rect(820, 90, 1880, 560), hexc('9cc8e6'), 6, 6700)             # big window
    shape(ctx, rect(820, 470, 1880, 560), hexc('8a8f96'), 3, 6701)            # runway
    plane_icon(ctx, lerp(700, 2000, t / d), 380 - 60 * t / d, 2.6, -0.08)
    for k in range(5): rough(ctx, [(820 + k * 265, 90), (820 + k * 265, 560)], 6, 6702 + k, hexc('4a4d52'))
    shape(ctx, rect(-300, 820, W + 300, H + 300), hexc('b9b4a8'), 4, 6710)
    for k in range(10): rough(ctx, [(k * 220 - 100, 820), (k * 220 - 300, H + 20)], 2, 6711 + k, hexc('a8a296'))
    shape(ctx, rect(80, 110, 640, 300), hexc('1c2026'), 5, 6720)               # departures board
    text(ctx, 'DEPARTURES', 360, 170, 54, 'Bebas Neue', hexc('ffd66a'), anchor='c')
    text(ctx, 'DUBAI   23:40', 360, 240, 50, 'Bebas Neue', (1, 1, 1), anchor='c')
    # parents behind glass (left)
    abba(ctx, 220, stand(0.85, 840), 0.85, expr='sad', arms='wave' if int(t * 3) % 2 else 'down', look=(5, 0))
    ammi(ctx, 400, stand(0.82, 840), 0.82, expr='sad', look=(5, 0),
         arms=[((-68, 44), (-60, 100), (-28, -82)), ((68, 44), (90, 128), (86, 206))])
    shape(ctx, rect(40, 330, 560, 840), (0.8, 0.9, 1.0), 4, 6730, alpha=0.28)
    rough(ctx, [(120, 380), (220, 480)], 3, 6731, (1, 1, 1), alpha=0.6)
    ctx.restore()
    hamza(ctx, 1080, stand(1.25, 1040), 1.25, expr='worried', look=(-6, 0),
          arms=[((-68, 44), (-90, 128), (-96, 206)), ((68, 44), (90, 128), (86, 206))])
    shape(ctx, rect(1150, 820, 1330, 980), hexc('3a5a7a'), 4, 6740)               # one bag
    rough(ctx, [(1190, 820), (1210, 780), (1270, 780), (1290, 820)], 5, 6741)
    label(ctx, 'Zindagi mein pehli dafa', 1450, 980, pop(t, S.F(2, 0.55)), 62, seed=6750)

def sc_bag(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('3a4a5a')); ctx.paint()
    ctx.save(); cam(ctx, 960, 560, 1.0 + 0.08 * t / d)
    shape(ctx, rect(330, 300, 1590, 1000), hexc('2e4a66'), 6, 6800)            # open bag
    shape(ctx, rect(370, 340, 1550, 960), hexc('1c2e40'), 3, 6801)
    p1 = pop(t, S.F(3, 0.15))
    for j in range(3):                                                           # parathas in foil/cloth
        if p1 > 0.01:
            ctx.save(); ctx.translate(640 + j * 18, 640 - j * 26); ctx.scale(p1, p1)
            shape(ctx, ell(0, 0, 190, 80, 30), hexc('d9a65a'), 4, 6810 + j)
            for k in range(5): shape(ctx, ell(-90 + k * 45, -10 + (k % 2) * 20, 18, 9, 10), hexc('a8743a'), 0, 0, alpha=0.7)
            ctx.restore()
    p2 = pop(t, S.F(3, 0.6))
    if p2 > 0.01:
        ctx.save(); ctx.translate(1180, 660); ctx.rotate(0.05); ctx.scale(p2, p2)
        shape(ctx, rect(-230, -170, 230, 170), hexc('7a3a3a'), 5, 6820)
        for k in range(6): rough(ctx, [(-210, -140 + k * 56), (210, -140 + k * 56)], 3, 6821 + k, hexc('5e2a2a'))
        text(ctx, 'Purana sweater', 0, 230, 54, 'Patrick Hand', (1, 1, 1), anchor='c')
        ctx.restore()
    label(ctx, 'Parathay', 640, 860, p1, 58, seed=6830)
    ctx.restore()
    # Ammi inset (wiping eyes)
    ip = pop(t, S.F(3, 0.35))
    if ip > 0.01:
        ctx.save(); ctx.translate(1660, 220); ctx.scale(ip, ip)
        shape(ctx, ell(0, 0, 190, 190, 40), hexc('e8a46a'), 6, 6840)
        ctx.save(); ctx.arc(0, 0, 186, 0, 7); ctx.clip()
        ammi(ctx, 0, 110, 1.0, expr='sad', legs=None, tear=True,
             arms=[((-68, 44), (-60, 100), (-28, -82)), ((68, 44), (90, 128), (86, 206))])
        ctx.restore(); ctx.restore()

def _map(cx0, cy0, z0, cx1, cy1, z1):
    def fn(ctx, t, d, S):
        u = ease_io(t / d)
        map_scene(ctx, t, t + S.t0, lerp(cx0, cx1, u), lerp(cy0, cy1, u), lerp(z0, z1, u))
        ta = t + S.t0
        if A(4) <= ta < A(5) - 0.2: label(ctx, 'Pehla stop: DUBAI', 960, 980, pop(ta, AF(4, 0.3)), 66, seed=6900)
        if A(4) <= ta < A(5) - 0.2: label(ctx, 'Sab theek lag raha hai', 960, 120, pop(ta, AF(4, 0.65)), 58, col=hexc('2f6e4f'), seed=6901)
        if ta >= A(5) - 0.2 and ta < A(7) - 0.2:
            n = 0
            for i, tt in enumerate((AF(6, 0.55), AF(6, 0.72), AF(6, 0.88))):
                if ta > tt: n = i + 1
            for i in range(n):
                xs = (1380, 1080, 760)[i]
                usay(ctx, 'Bas thora sa aur', xs - 200, 90 + i * 30, xs + 200, 230 + i * 30, (xs + 60, 330), (AF(6, 0.55), AF(6, 0.72), AF(6, 0.88))[i] - S.t0, t, 52)
            label(ctx, 'Har jagah naya agent', 960, 990, pop(ta, AF(5, 0.6)), 62, seed=6902)
        if ta >= A(7) - 0.2: label(ctx, 'LIBYA', 620, 640, pop(ta, A(7) + 0.3), 90, col=hexc('c0322a'), seed=6903)
    return fn

def sc_crack(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('2a2622')); ctx.paint(); radial(ctx, 960, 540, 800, (0.8, 0.55, 0.3), 0.25)
    t0 = 0.2; tc = S.F(8, 0.55); tf = tc + 0.35
    if t < tf:
        ctx.save(); ctx.translate(960 + (6 * math.sin(t * 70) if tc < t else 0), 520)
        stamp(ctx, 'FULL GUARANTEE', 0, 0, t0, t, 170, rot=-0.08); ctx.restore()
        if t > tc:
            rough(ctx, [(900, 360), (940, 450), (910, 520), (960, 600), (930, 690)], 7, 6950, (0.1, 0.08, 0.06))
    else:
        u = t - tf
        for side, sx in ((-1, 0), (1, 1)):
            ctx.save()
            ctx.rectangle(0 if sx == 0 else 935, 0, 935 if sx == 0 else W, H); ctx.clip()
            ctx.translate(960 + side * 60 * u, 520 + 900 * u * u); ctx.rotate(side * 0.6 * u)
            stamp(ctx, 'FULL GUARANTEE', 0, 0, 0, 1, 170, rot=-0.08); ctx.restore()
    label(ctx, 'Khatam.', 960, 900, pop(t, tf + 0.3), 80, seed=6960)

def sc_warehouse(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.0 + 0.08 * t / d)
    sky_grad(ctx, hexc('2a2f3a'), hexc('6a5a4a'), 0, 760)
    shape(ctx, rect(-300, 760, W + 300, H + 300), hexc('8a7a5a'), 4, 7000)
    shape(ctx, rect(260, 220, 1660, 780), hexc('5a5e62'), 6, 7001)            # building
    for k in range(10): rough(ctx, [(300 + k * 140, 230), (300 + k * 140, 770)], 3, 7002 + k, hexc('4a4e52'))
    shape(ctx, [(220, 230), (960, 120), (1700, 230)], hexc('4a4e52'), 6, 7015)
    shape(ctx, rect(760, 420, 1160, 780), hexc('121416'), 4, 7016)              # doorway dark
    # people walking in
    for i in range(5):
        x = lerp(-200 - i * 160, 880 + i * 30, ease_io(min(1, t / 2.6)))
        person(ctx, x, stand(0.6, 800), 0.6, 'kameez', ['short', 'crew', 'spiky_s', 'slick', 'short'][i], K.HAIR,
               expr='worried', color=[hexc('8a6a4a'), hexc('6b7a8a'), BLUEK, hexc('5f6e45'), KAMEEZ][i], seed=7020 + i * 9,
               walk=t * 9, look=(5, 0))
    td = S.F(9, 0.75)
    close = ease_in(min(1, (t - td) / 0.18)) if t > td else 0      # rolling shutter slams down
    if close > 0:
        by = 420 + 360 * close
        shape(ctx, rect(760, 420, 1160, by), hexc('7a7e82'), 5, 7030)
        for k in range(int(5 * close) + 1): rough(ctx, [(780, by - 20 - k * 70), (1140, by - 20 - k * 70)], 3, 7031 + k, hexc('5a5e62'))
    ctx.restore()
    label(ctx, 'Godaam', 960, 960, pop(t, S.F(9, 0.3)), 76, seed=7040)
    if td < t < td + 0.6: text(ctx, 'DHAAM!', 1400, 380, 110, 'Bebas Neue', (1, 1, 1), anchor='c', alpha=1 - (t - td) / 0.6)

def crowd_room(ctx, t, look=(0, 2)):
    warehouse(ctx, t)
    busts_row(ctx, 600, 0.5, 14, 7100, t, xs=[i * 140 - 30 for i in range(15)], look=look)
    busts_row(ctx, 720, 0.62, 12, 7200, t, xs=[i * 170 + 20 for i in range(12)], look=look)
    busts_row(ctx, 860, 0.78, 10, 7300, t, xs=[i * 210 - 60 for i in range(11)], look=look)
    busts_row(ctx, 1020, 0.95, 8, 7400, t, xs=[i * 270 + 10 for i in range(8)], look=look)

def sc_room(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.05 + 0.06 * t / d); crowd_room(ctx, t); ctx.restore()
    dark(ctx, 0.25)
    for i, (n_, w_, x, f) in enumerate((('1', 'KAMRA', 380, 0.05), ('80', 'LOG', 960, 0.38), ('1', 'BATHROOM', 1540, 0.7))):
        p = pop(t, S.F(10, f))
        if p > 0.01:
            ctx.save(); ctx.translate(x, 330); ctx.scale(p, p)
            shape(ctx, rect(-210, -180, 210, 170), hexc('f3efe4'), 5, 7500 + i)
            text(ctx, n_, 0, 40, 200, 'Bebas Neue', hexc('c0322a') if i == 1 else INK, anchor='c')
            text(ctx, w_, 0, 140, 66, 'Bebas Neue', INK, anchor='c'); ctx.restore()

def sc_phone(ctx, t, d, S):
    ctx.save(); cam(ctx, 900, 560, 1.25 + 0.06 * t / d)
    warehouse(ctx, t)
    ts = S.F(11, 0.45)
    grab = ease_io((t - ts) / 0.35) if t > ts else 0
    hamza(ctx, 760, 620, 1.2, expr='shock' if grab > 0.3 else 'worried', legs=None, look=(6, 2),
          arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (140, 110), (190, 80))])
    hx, hy = 760 + 1.2 * 190, 620 + 1.2 * 80
    px = lerp(hx + 20, 2100, ease_in(max(0, (t - ts - 0.35) / 0.5)) if t > ts + 0.35 else 0)
    ax = lerp(2100, hx + 70, grab) if t < ts + 0.35 else lerp(hx + 70, 2160, ease_in(min(1, (t - ts - 0.35) / 0.5)))
    phone(ctx, px if t > ts + 0.35 else hx + 20, hy - 40, 0.42, rot=0.15, screen=hexc('e8f4ff'))
    rough(ctx, [(2200, hy - 60), (ax + 40, hy - 40)], 34, 7600, hexc('23262c'))           # guard sleeve
    shape(ctx, ell(ax, hy - 40, 40, 30, 16), K.SKIN, 4, 7601)
    ctx.restore()
    label(ctx, 'Phone le liya', 480, 140, pop(t, ts + 0.5), 70, col=hexc('c0322a'), seed=7610)

def ease_in(x): x = min(1, max(0, x)); return x * x

def sc_food(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('35383b')); ctx.paint(); radial(ctx, 960, 600, 700, (1, 0.9, 0.7), 0.25)
    ctx.save(); cam(ctx, 960, 600, 1.0 + 0.1 * t / d)
    shape(ctx, ell(960, 640, 420, 170, 40), hexc('c8c8c0'), 6, 7700)            # tin plate
    shape(ctx, ell(960, 630, 340, 130, 40), hexc('b0b0a8'), 3, 7701)
    gone = S.F(12, 0.65)
    a = 1 if t < gone else max(0, 1 - (t - gone) / 0.6)
    if a > 0:
        shape(ctx, ell(960, 620, 170, 70, 30), hexc('d9a65a'), 4, 7702, alpha=a)
        for k in range(6): shape(ctx, ell(880 + k * 32, 610 + (k % 2) * 18, 12, 6, 8), hexc('8a5a2a'), 0, 0, alpha=0.6 * a)
    ctx.restore()
    label(ctx, 'Din mein 1 dafa', 960, 200, pop(t, S.F(12, 0.1)), 80, seed=7710)
    if t > gone: label(ctx, 'Kabhi kabhi... woh bhi nahi', 960, 940, pop(t, gone + 0.2), 66, col=hexc('c0322a'), seed=7711)

def sc_saleem(ctx, t, d, S):
    ctx.save(); cam(ctx, 800, 560, 1.15 + 0.12 * ease_io(t / d))
    warehouse(ctx, t)
    busts_row(ctx, 760, 0.55, 8, 7800, t, xs=[i * 260 - 60 for i in range(8)])
    saleem(ctx, 760, 650, 1.25, expr='smile', legs=None, arms='clasp', look=(4, 0))
    ctx.restore()
    p = pop(t, S.F(13, 0.3))
    if p > 0.01:
        ctx.save(); ctx.translate(1440, 400); ctx.rotate(-0.04); ctx.scale(p, p)
        shape(ctx, rect(-330, -190, 330, 190), hexc('f3efe4'), 5, 7810)
        utext(ctx, 'SALEEM CHACHA', 0, -80, 104, INK, font='Bebas Neue')
        rough(ctx, [(-250, 0), (250, 0)], 3, 7811, hexc('c0322a'))
        utext(ctx, 'Umar: 50 saal', 0, 60, 62, hexc('333336'), pop=1 if t > S.F(13, 0.55) else 0)
        utext(ctx, 'Sialkot', 0, 130, 62, hexc('333336'), pop=1 if t > S.F(13, 0.8) else 0)
        ctx.restore()
    stamp(ctx, '3rd TRY', 1440, 760, S.F(14, 0.5), t, 140, rot=-0.12)

def talk_set(ctx, t, cx, cy, z, sexpr='neutral', hexpr='worried'):
    ctx.save(); cam(ctx, cx, cy, z)
    warehouse(ctx, t)
    busts_row(ctx, 720, 0.5, 8, 7900, t, xs=[i * 260 - 60 for i in range(8)], expr='sad')
    saleem(ctx, 700, 640, 1.15, expr=sexpr, legs=None, arms='clasp', look=(6, 0))
    hamza(ctx, 1200, 640, 1.15, expr=hexpr, legs=None, arms='clasp', look=(-6, 0))
    ctx.restore()

def sc_talk1(ctx, t, d, S):
    talk_set(ctx, t, 760, 520, 1.25 + 0.08 * t / d, 'sad')
    usay(ctx, 'Beta, pehli do dafa... boat wapas aa gayi thi.', 160, 60, 980, 290, (600, 400), S.L(15)[0] + 0.1, t, 62)

def sc_talk2(ctx, t, d, S):
    talk_set(ctx, t, 1180, 520, 1.45, 'neutral', 'shock')
    usay(ctx, 'To phir kyun?', 1300, 80, 1800, 260, (1450, 360), S.L(16)[0] + 0.05, t, 76)

def sc_talk3(ctx, t, d, S):
    talk_set(ctx, t, 760, 520, 1.4 + 0.08 * t / d, 'smile', 'sad')
    usay(ctx, 'Wapas ja kar kya karoon? Qarza to wahan bhi hai.', 100, 60, 980, 290, (640, 400), S.F(17, 0.25), t, 62)

def sc_tally(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 540, 1.1 - 0.06 * t / d)
    shape(ctx, rect(-300, -300, W + 300, H + 300), hexc('55585b'), 0, 1)
    for k in range(-1, 15): rough(ctx, [(k * 150, -300), (k * 150 + 4, H + 300)], 2.5, 8000 + k, hexc('45484b'))
    n = int(min(21, max(0, t - 0.2) * 14))
    for g in range(n):
        gx = 330 + (g % 7) * 190; gy = 260 + (g // 7) * 190
        rough(ctx, [(gx, gy), (gx + 4, gy + 110)], 5, 8100 + g, hexc('e8e4d8'))
    ctx.restore()
    p = pop(t, S.F(18, 0.4))
    if p > 0.01:
        ctx.save(); ctx.translate(960, 900); ctx.scale(p, p)
        shape(ctx, rect(-300, -80, 300, 80), hexc('17171a'), 4, 8150, ink=(1, 1, 1))
        text(ctx, '3 HAFTE', 0, 34, 110, 'Bebas Neue', (1, 1, 1), anchor='c'); ctx.restore()

def sc_agent_night(ctx, t, d, S):
    ctx.save(); cam(ctx, 960, 560, 1.05 + 0.1 * ease_io(t / d))
    warehouse(ctx, t, beam=False); dark(ctx, 0.45)
    busts_row(ctx, 860, 0.7, 10, 8200, t, xs=[i * 220 - 60 for i in range(10)], look=(4, 0))
    wu = ease_out(min(1, t / 1.5))
    ax = lerp(2100, 1450, wu)
    radial(ctx, ax - 200, 620, 380, (1, 0.95, 0.7), 0.35)                          # torch beam
    agent(ctx, ax, stand(1.1, 1010), 1.1, expr='stern', look=(-6, 0), walk=t * 9 if wu < 1 else None,
          arms=[((-68, 44), (-150, 80), (-240, 70)), ((68, 44), (90, 128), (86, 206))])
    hamza(ctx, 960, stand(1.1, 1010), 1.1, expr='worried', look=(6, 0),
          arms='reachR' if t > S.F(19, 0.55) else 'down')
    if t > S.F(19, 0.55): phone(ctx, ax - 1.1 * 240 - 20, stand(1.1, 1010) + 70, 0.35, rot=0.3, screen=hexc('e8f4ff'))
    ctx.restore()
    label(ctx, 'Sirf 2 minute', 420, 160, pop(t, S.F(19, 0.8)), 66, col=hexc('c0322a'), seed=8210)
    timer(ctx, t + S.t0)

def sc_five(ctx, t, d, S):
    ctx.save(); cam(ctx, 1200, 520, 1.45 + 0.08 * t / d)
    warehouse(ctx, t, beam=False); dark(ctx, 0.35)
    radial(ctx, 1200, 520, 500, (1, 0.9, 0.6), 0.3)
    agent(ctx, 1250, stand(1.1, 1010), 1.1, expr='stern', look=(-6, 0), arms='pointL')
    ctx.restore()
    usay(ctx, 'Boat ke liye 5 lakh aur chahiye!', 300, 70, 1160, 290, (1180, 420), S.L(20)[0] + 0.05, t, 66)
    if t > S.F(20, 0.45):
        glow_text(ctx, 'Rs 5,00,000', 470, 640, 170, 'Bebas Neue', hexc('ffd66a'), (1, 0.75, 0.2), pop=pop(t, S.F(20, 0.45)))
    if t > S.F(20, 0.75): utext(ctx, 'Ghar walon ko bolo.', 470, 820, 72, (1, 1, 1), stroke=(0, 0, 0), pop=pop(t, S.F(20, 0.75)))
    timer(ctx, t + S.t0)

def sc_call(ctx, t, d, S):
    ctx.save(); ctx.rectangle(0, 0, 960, H); ctx.clip()
    ctx.save(); ctx.translate(-300, 0); warehouse(ctx, t, beam=False); ctx.restore(); dark(ctx, 0.35)
    hamza(ctx, 480, 640, 1.3, expr='worried', legs=None, look=(4, 0),
          arms=[((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (60, 40), (40, -70))])
    phone(ctx, 480 + 1.3 * 50, 640 - 1.3 * 90, 0.33, rot=0.2, screen=hexc('e8f4ff'))
    ctx.restore()
    ctx.save(); ctx.rectangle(960, 0, 960, H); ctx.clip()
    ctx.save(); ctx.translate(480, 0); shop(ctx, t, 0); ctx.restore()
    rng_ = 0.5 + 0.5 * math.sin(t * 18)
    phone(ctx, 1640, 900, 0.32, rot=-0.3, screen=hexc('e8f4ff') if int(t * 4) % 2 else hexc('9fd0ff'))
    ctx.restore()
    rough(ctx, [(960, -20), (960, H + 20)], 10, 8300, (1, 1, 1))
    for k in range(3):
        a = max(0, math.sin(t * 9 - k))
        rough(ctx, [(1720 + k * 26, 840 - k * 30), (1760 + k * 26, 820 - k * 30)], 6, 8310 + k, (1, 1, 1), alpha=a)
    if t > 0.4: text(ctx, 'TRING TRING', 1440, 1000, 80, 'Bebas Neue', (1, 1, 1), anchor='c', alpha=0.6 + 0.4 * math.sin(t * 14))
    label(ctx, 'Abba ji', 1180, 560, pop(t, 0.3), 56, seed=8320)
    timer(ctx, t + S.t0, 480, 110)

SHOTS = [(0, sc_gold), (1, sc_silence), (2, sc_airport), (3, sc_bag),
         (4, _map(1480, 500, 1.3, 1420, 520, 1.45)), (5, _map(1300, 500, 1.1, 1100, 500, 1.15)),
         (7, _map(900, 480, 1.3, 680, 470, 1.8)), (8, sc_crack), (9, sc_warehouse), (10, sc_room), (11, sc_phone),
         (12, sc_food), (13, sc_saleem), (15, sc_talk1), (16, sc_talk2), (17, sc_talk3), (18, sc_tally),
         (19, sc_agent_night), (20, sc_five), (21, sc_call)]

if __name__ == '__main__': engine.run(SHOTS, LT, END)

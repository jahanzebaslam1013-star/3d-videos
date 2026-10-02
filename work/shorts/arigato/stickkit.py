"""stickkit — hand-drawn stickman story kit (pycairo). Self-contained."""
import math, random, cairo, numpy as np

W, H, FPS = 1080, 1920, 24  # override for 16:9

def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

INK = hexc('17171a'); SKIN = hexc('f1dcc4'); HAIR = hexc('1f1f24'); HOOD = hexc('5f6e45')
HOOD_D = hexc('4a5735'); PAPER = hexc('f3efe4'); SKY1 = hexc('aeb6ae'); SKY2 = hexc('d9dbd1')
SUIT = hexc('1e2024'); COAT = hexc('eef0ee'); UNIF = hexc('4f5d6b')
SUITC = hexc('1e2024'); WHITEJ = hexc('efece2'); OLIVE = hexc('5c6446'); CARDI = hexc('8a6a4a'); TEE = hexc('4f79b8')
VEST = hexc('7d8288'); BURG = hexc('6e2a2e'); GOLD = hexc('c9a24a'); RED = hexc('c0322a'); GREEN = hexc('2f9e4f')
BOIL = 0  # set to frame//2 each frame for line boil

def ease_out_back(x, s=1.8):
    x = min(max(x, 0), 1); x -= 1
    return x * x * ((s + 1) * x + s) + 1

def ease_out(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def ease_io(x):
    x = min(max(x, 0), 1); return x * x * (3 - 2 * x)

def lerp(a, b, u): return a + (b - a) * u

def jit_pts(pts, seed, amp, step=16):
    rng = random.Random(seed)
    out = []
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]; x1, y1 = pts[i + 1]
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        for k in range(n):
            u = k / n; out.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u))
    out.append(pts[-1])
    offs = [(rng.uniform(-amp, amp), rng.uniform(-amp, amp)) for _ in out]
    n = len(out)
    res = []
    for i, (x, y) in enumerate(out):
        a = offs[max(i - 1, 0)]; b = offs[i]; c = offs[min(i + 1, n - 1)]
        res.append((x + (a[0] + 2 * b[0] + c[0]) / 4, y + (a[1] + 2 * b[1] + c[1]) / 4))
    return res

def poly(ctx, pts, close=True):
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    if close: ctx.close_path()

def rough(ctx, pts, w=4, seed=1, color=INK, closed=False, amp=1.4, alpha=1.0):
    if closed: pts = list(pts) + [pts[0]]
    rng = random.Random(seed * 13 + BOIL * 7919)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for i, (wm, a) in enumerate(((1.0, 1.0), (0.5, 0.65))):
        p = jit_pts(pts, seed * 97 + BOIL * 131 + i * 17, amp)
        poly(ctx, p, close=False)
        ctx.set_source_rgba(*color, a * alpha)
        ctx.set_line_width(max(0.6, w * wm * rng.uniform(0.85, 1.15)))
        ctx.stroke()

def shape(ctx, pts, fill, w=4, seed=1, ink=INK, amp=1.4, alpha=1.0):
    poly(ctx, pts); ctx.set_source_rgba(*fill, alpha); ctx.fill()
    if w > 0: rough(ctx, pts, w, seed, ink, closed=True, amp=amp, alpha=alpha)

def ell(cx, cy, rx, ry, n=40, a0=0, a1=2 * math.pi):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / n), cy + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + (0 if a1 - a0 >= 6.28 else 1))]

def bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        u = i / n; v = 1 - u
        out.append((v**3 * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u**3 * p3[0],
                    v**3 * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u**3 * p3[1]))
    return out

def text(ctx, s, x, y, size, font='Patrick Hand', color=INK, anchor='l', alpha=1.0):
    ctx.select_font_face(font); ctx.set_font_size(size)
    ext = ctx.text_extents(s)
    if anchor == 'c': x -= ext.width / 2 + ext.x_bearing
    ctx.move_to(x, y); ctx.set_source_rgba(*color, alpha); ctx.show_text(s)

def sweat(ctx, x, y, s=1.0, alpha=1.0):
    pts = [(x, y - 16 * s)] + bez((x, y - 16 * s), (x + 12 * s, y), (x + 8 * s, y + 10 * s), (x, y + 10 * s), 8)[1:] + \
          bez((x, y + 10 * s), (x - 8 * s, y + 10 * s), (x - 12 * s, y), (x, y - 16 * s), 8)[1:]
    shape(ctx, pts, hexc('8fd0f2'), 2.6, 77, alpha=alpha)

def sky(ctx, top=SKY1, bot=SKY2, h=None):
    h = h or H
    g = cairo.LinearGradient(0, 0, 0, h); g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(1, *bot)
    ctx.rectangle(-400, -400, W + 800, H + 800); ctx.set_source(g); ctx.fill()

def pine(ctx, x, base, h, col, seed, w=3, dark=None):
    rng = random.Random(seed)
    rough(ctx, [(x, base), (x, base - h * 0.25)], w + 2, seed, hexc('3a3128'))
    tiers = 3
    for i in range(tiers):
        tb = base - h * 0.18 - i * h * 0.24
        tw = h * (0.34 - i * 0.08)
        tt = tb - h * 0.42
        pts = [(x - tw, tb)]
        for k in range(1, 4):
            pts.append((x - tw + tw * 0.33 * k, tb - rng.uniform(4, 12)))
        pts += [(x + tw, tb), (x + tw * 0.25, tt + h * 0.12), (x + tw * 0.45, tt + h * 0.14), (x, tt),
                (x - tw * 0.45, tt + h * 0.14), (x - tw * 0.25, tt + h * 0.12)]
        shape(ctx, pts, col, w, seed + i * 3)

def bush(ctx, x, base, r, col, seed, w=3):
    rng = random.Random(seed)
    pts = []
    n = 14
    for i in range(n + 1):
        a = math.pi + math.pi * i / n
        rr = r * rng.uniform(0.8, 1.1)
        pts.append((x + rr * 1.3 * math.cos(a), base + rr * math.sin(a)))
    shape(ctx, pts, col, w, seed)

def hills(ctx, y, amp, col, seed, off=0, w=3):
    rng = random.Random(seed)
    pts = [(-300, H + 50)]
    xs = list(range(-300, W + 400, 160))
    hs = [rng.uniform(0, amp) for _ in xs]
    for i, xx in enumerate(xs):
        pts.append((xx - off % 160, y - hs[i]))
    pts.append((W + 400, H + 50))
    shape(ctx, pts, col, w, seed, amp=2)

def van(ctx, x, y, s, dist, seed=900):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    shape(ctx, ell(0, 4, 300, 16, 24), (0, 0, 0), 0, 0, alpha=0.25)
    body = [(-262, -42), (-262, -196), (-234, -226), (104, -226), (168, -160), (248, -132), (262, -96), (262, -42)]
    shape(ctx, body, hexc('26292e'), 5, seed, ink=hexc('0b0b0c'))
    shape(ctx, [(114, -212), (160, -162), (114, -162)], hexc('56616c'), 3, seed + 1, ink=hexc('0b0b0c'))
    shape(ctx, [(-230, -206), (-40, -206), (-40, -160), (-230, -160)], hexc('3d454e'), 3, seed + 2, ink=hexc('0b0b0c'))
    shape(ctx, [(-20, -206), (96, -206), (96, -160), (-20, -160)], hexc('3d454e'), 3, seed + 3, ink=hexc('0b0b0c'))
    rough(ctx, [(-200, -200), (-160, -166)], 3, seed + 4, hexc('8a95a0'))
    rough(ctx, [(100, -150), (100, -50)], 3, seed + 5, hexc('0b0b0c'))
    rough(ctx, [(-262, -100), (262, -100)], 2.5, seed + 6, hexc('3c4046'))
    shape(ctx, ell(250, -116, 10, 8, 10), hexc('f3e3a0'), 2, seed + 7)
    for wx in (-160, 168):
        shape(ctx, ell(wx, -40, 48, 48, 28), hexc('0f0f10'), 4, seed + wx)
        shape(ctx, ell(wx, -40, 19, 19, 16), hexc('80868d'), 3, seed + wx + 1)
        a0 = dist / 48
        for k in range(4):
            a = a0 + k * math.pi / 2
            rough(ctx, [(wx, -40), (wx + 16 * math.cos(a), -40 + 16 * math.sin(a))], 2.5, seed + wx + 2 + k, hexc('2c2f33'))
    ctx.restore()

def grain_layers():
    rng = np.random.default_rng(3); outs = []
    for i in range(4):
        n = rng.random((H, W)); a = np.zeros((H, W, 4), np.uint8)
        alpha = np.zeros((H, W)); val = np.zeros((H, W))
        alpha[n < 0.10] = 26; alpha[n > 0.93] = 18; val[n > 0.93] = 255
        a[..., 3] = alpha.astype(np.uint8); pm = (val * alpha / 255).astype(np.uint8)
        a[..., 0] = pm; a[..., 1] = pm; a[..., 2] = pm
        outs.append(cairo.ImageSurface.create_for_data(bytearray(a.tobytes()), cairo.FORMAT_ARGB32, W, H, W * 4))
    return outs

def vignette(ctx, strength=0.45, col=(0, 0, 0)):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.05)
    g.add_color_stop_rgba(0, *col, 0); g.add_color_stop_rgba(1, *col, strength)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()

def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

HAIRS = {
 'spiky': [(-66, -78), (-80, -118), (-62, -120), (-70, -160), (-42, -150), (-34, -188), (-8, -162), (10, -194), (26, -160),
           (54, -182), (50, -146), (80, -142), (64, -114), (78, -84), (58, -104), (44, -122), (30, -112), (16, -126), (0, -112),
           (-14, -128), (-28, -112), (-44, -124), (-56, -100)],
 'short': [(-64, -86), (-68, -128), (-50, -160), (-20, -172), (20, -172), (50, -160), (68, -128), (64, -86), (54, -114),
           (30, -128), (0, -122), (-30, -130), (-56, -110)],
 'slick': [(-63, -92), (-66, -134), (-44, -166), (0, -174), (44, -166), (66, -134), (63, -92), (56, -118), (20, -140),
           (-20, -136), (-56, -118)],
 'bob': [(-70, -36), (-76, -120), (-52, -166), (0, -178), (52, -166), (76, -120), (70, -36), (54, -40), (56, -110),
         (30, -132), (-10, -126), (-50, -112), (-54, -40)],
}

HAIRS['crew'] = [(-62, -96), (-64, -140), (-50, -160), (50, -160), (64, -140), (62, -96), (52, -126), (-52, -126)]

HAIRS['spiky_s'] = [(-64, -84), (-72, -120), (-56, -122), (-60, -152), (-36, -144), (-26, -172), (-4, -150), (12, -176),
                      (26, -150), (48, -166), (46, -138), (70, -132), (58, -110), (66, -86), (52, -104), (30, -116), (0, -110),
                      (-30, -116), (-54, -100)]

def head2(ctx, hair='spiky', hcol=HAIR, expr='neutral', look=(0, 0), glasses=None, beard=None, wrinkles=False,
          cap=None, back=False, tear=None, seed=100):
    for sx in (-1, 1):
        shape(ctx, ell(sx * 60, -88, 12, 16, 16), SKIN, 3.5, seed + sx)
    if back:
        shape(ctx, ell(0, -95, 60, 70), hcol if cap is None else hexc('d9c3a9'), 4.5, seed + 3)
        if cap is not None:
            shape(ctx, [(-62, -118), (-58, -168), (58, -168), (62, -118)], cap, 4, seed + 60)
        return
    shape(ctx, ell(0, -95, 60, 70), SKIN, 4.5, seed + 3)
    if expr == 'shock':
        for i in range(5):
            rough(ctx, [(-40 + i * 9, -118), (-40 + i * 9, -104)], 2.2, seed + 40 + i, hexc('5a74a8'))
    if wrinkles:
        for k in range(2):
            rough(ctx, [(-26, -136 + k * 9), (-6, -139 + k * 9), (14, -136 + k * 9)], 2, seed + 45 + k, hexc('a88a70'))
        for sx in (-1, 1):
            rough(ctx, [(sx * 34, -58), (sx * 42, -64)], 2, seed + 47 + sx, hexc('a88a70'))
    for sx in (-1, 1):
        ex, ey = sx * 24, -80; lx, ly = look
        if glasses == 'sun':
            continue
        if expr == 'closed':
            rough(ctx, bez((ex - 12, ey), (ex - 4, ey + 7), (ex + 4, ey + 7), (ex + 12, ey), 8), 3.2, seed + 10 + sx)
        else:
            shape(ctx, ell(ex, ey, 14, 18, 24), (1, 1, 1), 3.2, seed + 10 + sx)
            if expr == 'shock':
                shape(ctx, ell(ex + lx, ey + ly, 3.5, 4.5, 12), INK, 0, 0)
            else:
                shape(ctx, ell(ex + lx, ey + 2 + ly, 9, 12, 20), INK, 0, 0)
                shape(ctx, ell(ex + lx - 3, ey - 3 + ly, 3.4, 3.4, 10), (1, 1, 1), 0, 0)
            if expr in ('blank', 'sad'):
                lid = [(ex - 15, ey - 2), (ex - 15, ey - 20), (ex + 15, ey - 20), (ex + 15, ey - 2)] if expr == 'blank' else \
                      [(ex - 15, ey - 6 - (sx * 5)), (ex - 15, ey - 20), (ex + 15, ey - 20), (ex + 15, ey - 6 + sx * 5)]
                shape(ctx, lid, SKIN, 0, 0)
                rough(ctx, [lid[0], lid[3]], 3, seed + 12 + sx)
        if expr == 'shock':
            rough(ctx, [(ex - 12, ey - 34), (ex + 12, ey - 36)], 3.5, seed + 20 + sx)
        elif expr in ('worried', 'sad'):
            rough(ctx, [(ex - sx * 13, ey - 34), (ex + sx * 11, ey - 24)], 3.5, seed + 20 + sx)
        elif expr == 'stern':
            rough(ctx, [(ex - sx * 13, ey - 30), (ex + sx * 11, ey - 24)], 3.5, seed + 20 + sx)
        else:
            rough(ctx, [(ex - 11, ey - 27), (ex + 11, ey - 28)], 3.5, seed + 20 + sx)
    if glasses == 'sun':
        for sx in (-1, 1):
            shape(ctx, [(sx * 6, -92), (sx * 40, -94), (sx * 38, -70), (sx * 10, -70)], hexc('0d0d10'), 3, seed + 14 + sx)
            rough(ctx, [(sx * 14, -88), (sx * 22, -82)], 2, seed + 16 + sx, hexc('6c737c'))
        rough(ctx, [(-6, -88), (6, -88)], 3, seed + 18)
        rough(ctx, [(-10, -130), (-30, -126)], 3.5, seed + 19); rough(ctx, [(10, -130), (30, -126)], 3.5, seed + 19)
    elif glasses == 'round':
        for sx in (-1, 1):
            rough(ctx, ell(sx * 24, -80, 20, 20, 20), 2.5, seed + 14 + sx, closed=True)
        rough(ctx, [(-4, -82), (4, -82)], 2.5, seed + 18)
    rough(ctx, [(2, -64), (-2, -54), (3, -53)], 2.4, seed + 30)
    if beard == 'full':
        shape(ctx, [(-58, -80), (-52, -40), (-26, -12), (0, -6), (26, -12), (52, -40), (58, -80), (40, -60), (20, -48),
                    (-20, -48), (-40, -60)], hcol, 3, seed + 32)
    if expr == 'shock':
        shape(ctx, ell(0, -36, 9, 12, 18), hexc('4a1f1f'), 3.2, seed + 31)
    elif expr in ('sad', 'worried'):
        rough(ctx, bez((-13, -34), (-5, -42), (5, -42), (13, -34), 8), 3, seed + 31)
    elif expr == 'stern' or glasses == 'sun':
        rough(ctx, [(-13, -38), (13, -38)], 3.2, seed + 31)
    elif expr == 'smile':
        rough(ctx, bez((-16, -42), (-6, -32), (6, -32), (16, -42), 8), 3, seed + 31)
    else:
        rough(ctx, bez((-12, -40), (-4, -37), (5, -37), (12, -40), 8), 3, seed + 31)
    if beard in ('mous', 'full'):
        shape(ctx, [(-24, -46), (-4, -54), (4, -54), (24, -46), (14, -44), (0, -48), (-14, -44)], hcol, 2.5, seed + 33)
    if cap is not None:
        for sx in (-1, 1):
            shape(ctx, [(sx * 58, -84), (sx * 66, -122), (sx * 50, -122), (sx * 48, -96)], hcol, 2.5, seed + 55 + sx)
        shape(ctx, [(-62, -118), (-58, -172), (58, -172), (62, -118)], cap, 4, seed + 60)
        shape(ctx, [(-70, -116), (70, -116), (60, -104), (-60, -104)], hexc('15181b'), 3, seed + 61)
        shape(ctx, ell(0, -145, 10, 12, 12), hexc('e3c24a'), 2.5, seed + 62)
    elif hair in HAIRS:
        shape(ctx, HAIRS[hair], hcol, 3.5, seed + 50)
    if tear is not None and tear > 0:
        ty = -72 + 70 * min(tear, 1)
        sweat(ctx, -30, ty, 0.55, alpha=min(1, tear * 5) * (1 - max(0, tear - 1.2) * 3))

def glow_text(ctx, s, x, y, size, font, fill, glow, pop=1.0, rot=0, alpha=1.0, outline=hexc('111111')):
    if pop <= 0.01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(pop, pop)
    ctx.select_font_face(font); ctx.set_font_size(size); e = ctx.text_extents(s)
    x0 = -e.width / 2 - e.x_bearing; y0 = e.height / 2
    ctx.move_to(x0 + 10, y0 + 12); ctx.text_path(s); ctx.set_source_rgba(0, 0, 0, 0.5 * alpha); ctx.fill()
    if glow:
        for lw, a in ((40, 0.07), (26, 0.12), (14, 0.22)):
            ctx.move_to(x0, y0); ctx.text_path(s); ctx.set_source_rgba(*glow, a * alpha); ctx.set_line_width(lw)
            ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
    ctx.move_to(x0, y0); ctx.text_path(s); ctx.set_source_rgba(*fill, alpha); ctx.fill_preserve()
    ctx.set_source_rgba(*outline, alpha); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()

def cam(ctx, cx, cy, s):
    ctx.translate(cx, cy); ctx.scale(s, s); ctx.translate(-cx, -cy)

def dark(ctx, a, col=(0.02, 0.03, 0.05)):
    ctx.rectangle(-500, -500, W + 1000, H + 1000); ctx.set_source_rgba(*col, a); ctx.fill()

def radial(ctx, x, y, r, col, a):
    g = cairo.RadialGradient(x, y, 1, x, y, r); g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
    ctx.arc(x, y, r, 0, 7); ctx.set_source(g); ctx.fill()

def stamp(ctx, s, x, y, t0, t, size=120, rot=-0.18):
    if t < t0: return
    sc = lerp(1.8, 1.0, ease_out((t - t0) / 0.12))
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc)
    ctx.select_font_face('Bebas Neue'); ctx.set_font_size(size); e = ctx.text_extents(s)
    red = hexc('c0322a'); a = min(1, (t - t0) / 0.08) * 0.92
    pad = 26
    rough(ctx, rect(-e.width / 2 - pad, -e.height / 2 - pad, e.width / 2 + pad, e.height / 2 + pad), 9, 999, red, closed=True, alpha=a)
    ctx.move_to(-e.width / 2 - e.x_bearing, e.height / 2); ctx.set_source_rgba(*red, a); ctx.show_text(s)
    ctx.restore()

def tally(ctx, x, y, n, seed, col=hexc('3a3d3a'), h=60, w=2.5):
    for g in range(n):
        gx = x + (g % 6) * 70; gy = y + (g // 6) * 80
        for k in range(4): rough(ctx, [(gx + k * 12, gy), (gx + k * 12 + 2, gy + h)], w, seed + g * 5 + k, col)
        rough(ctx, [(gx - 6, gy + h - 8), (gx + 44, gy + 8)], w, seed + g * 5 + 4, col)

def body3(ctx, outfit, arms, legs, walk, seed, width=1.0, tie=None, tie_off=0.0, color=None, shrug=0.0):
    col = color or {'suit': SUITC, 'white': WHITEJ, 'olive': OLIVE, 'cardi': CARDI, 'tee': TEE, 'vest': VEST,
                    'dress': hexc('7a2c3e'), 'hoodie': HOOD}[outfit]
    if legs == 'stand':
        for i, sx in enumerate((-1, 1)):
            lift = 0; fx = sx * 34 * width
            if walk is not None:
                ph = walk + i * math.pi
                lift = 22 * max(0, math.sin(ph)); fx += sx * 6 * math.cos(ph)
            lc = hexc('1a1a1d') if outfit in ('suit', 'olive', 'white') else INK
            if outfit == 'white': lc = hexc('2a2d44')
            rough(ctx, [(sx * 28 * width, 196), (sx * 32 * width, 262 - lift * .5), (fx, 330 - lift)], 7, seed + 5 + sx, lc)
            shape(ctx, ell(fx + sx * 8, 334 - lift, 22, 9, 16), hexc('151518'), 3, seed + 8 + sx)
    wd = width; sy = -shrug
    if outfit == 'dress':
        torso = [(-46 * wd, 10 + sy), (-66 * wd, 38 + sy), (-70 * wd, 120), (-96 * wd, 210), (96 * wd, 210), (70 * wd, 120), (66 * wd, 38 + sy), (46 * wd, 10 + sy)]
    else:
        torso = [(-48 * wd, 10 + sy), (-70 * wd, 38 + sy), (-78 * wd, 200), (78 * wd, 200), (70 * wd, 38 + sy), (48 * wd, 10 + sy)]
    shape(ctx, torso, col, 4.5, seed + 1)
    if outfit == 'suit':
        shape(ctx, [(-24, 10), (24, 10), (0, 92)], (0.96, 0.96, 0.96), 3, seed + 2)
        tc = tie or hexc('7a1d22')
        ctx.save(); ctx.translate(0, 16); ctx.rotate(tie_off); ctx.translate(0, -16)
        shape(ctx, [(-7, 16), (7, 16), (9, 78), (0, 92), (-9, 78)], tc, 2.5, seed + 3)
        ctx.restore()
        for sx in (-1, 1): rough(ctx, [(sx * 24, 10), (sx * 36 * wd, 62), (0, 112)], 3, seed + 4 + sx, hexc('3c4048'))
    elif outfit == 'white':
        rough(ctx, [(0, 12), (0, 198)], 3, seed + 2, hexc('b9b4a6'))
        for k in range(4): shape(ctx, ell(10, 40 + k * 38, 5, 5, 8), GOLD, 1.5, seed + 30 + k)
        shape(ctx, [(-60 * wd, 26), (-38 * wd, 22), (70 * wd, 176), (56 * wd, 196)], hexc('a8262c'), 3, seed + 3)
        for k, c in enumerate(('c0322a', '2f5fa8', 'e3c24a', '2f9e4f')):
            shape(ctx, rect(-58 * wd + k * 13, 64, -48 * wd + k * 13, 80), hexc(c), 1.5, seed + 40 + k)
        for k in range(3): shape(ctx, ell(-52 * wd + k * 14, 94, 6, 6, 8), GOLD, 1.5, seed + 50 + k)
        for sx in (-1, 1): shape(ctx, [(sx * 46 * wd, 12), (sx * 76 * wd, 30), (sx * 72 * wd, 46), (sx * 44 * wd, 26)], GOLD, 2.5, seed + 55 + sx)
    elif outfit == 'olive':
        rough(ctx, [(0, 12), (0, 198)], 3, seed + 2, hexc('3e4430'))
        shape(ctx, rect(-78 * wd, 150, 78 * wd, 166), hexc('2b2a24'), 2.5, seed + 3)
        for sx in (-1, 1):
            shape(ctx, rect(sx * 14 - 8, 14, sx * 14 + 8, 30), hexc('a8262c'), 1.5, seed + 4 + sx)
            shape(ctx, rect(sx * 44 - 20, 70, sx * 44 + 20, 104), hexc('525a3e'), 2.5, seed + 6 + sx)
        for k, c in enumerate(('c0322a', 'e3c24a', '2f5fa8')): shape(ctx, rect(-62 + k * 12, 52, -52 + k * 12, 62), hexc(c), 1, seed + 9 + k)
    elif outfit == 'cardi':
        shape(ctx, [(-20, 10), (20, 10), (6, 110), (-6, 110)], hexc('e8e2d0'), 2.5, seed + 2)
        for sx in (-1, 1): rough(ctx, [(sx * 20, 10), (sx * 8, 110), (sx * 8, 200)], 3, seed + 3 + sx, hexc('6b5139'))
        for k in range(4): shape(ctx, ell(-16, 120 + k * 20, 4, 4, 8), hexc('4a3a2a'), 1, seed + 10 + k)
    elif outfit == 'vest':
        shape(ctx, [(-20, 10), (20, 10), (0, 40)], (0.96, 0.96, 0.96), 2.5, seed + 2)
        shape(ctx, [(-5, 20), (5, 20), (6, 70), (0, 78), (-6, 70)], hexc('2f5fa8'), 2, seed + 3)
    elif outfit == 'tee':
        rough(ctx, [(-20, 12), (0, 30), (20, 12)], 3, seed + 2, hexc('3a5f96'))
    elif outfit == 'hoodie':
        for sx in (-1, 1): rough(ctx, [(sx * 12, 16), (sx * 14, 64)], 2.5, seed + 3 + sx, hexc('e8e2d0'))
    rough(ctx, [(0, 8), (0, -30)], 7, seed + 4)
    sleeve = {'suit': hexc('1e2024'), 'white': WHITEJ, 'olive': OLIVE}.get(outfit)
    for (sh, el, ha) in arms:
        sh = (sh[0] * wd, sh[1] + sy)
        if sleeve is not None:
            rough(ctx, [sh, el, ha], 13, seed + int(sh[0]) + 1, sleeve)
            rough(ctx, [sh, el, ha], 3, seed + int(sh[0]) + 2, INK, alpha=0.9)
        else:
            rough(ctx, [sh, el, ha], 6.5, seed + int(sh[0]))
        shape(ctx, ell(ha[0], ha[1], 12, 12, 14), SKIN, 3, seed + int(ha[0]) + 3)

ARMS = {
 'down': [((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (90, 128), (86, 206))],
 'table': [((-68, 44), (-120, 150), (-90, 185)), ((68, 44), (120, 150), (90, 185))],
 'grip': [((-68, 44), (-130, 140), (-150, 190)), ((68, 44), (130, 140), (150, 190))],
 'clasp': [((-68, 44), (-80, 130), (-10, 160)), ((68, 44), (80, 130), (10, 160))],
 'reachR': [((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (150, 80), (240, 70))],
 'reachL': [((-68, 44), (-150, 80), (-240, 70)), ((68, 44), (90, 128), (86, 206))],
 'holster': [((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (104, 120), (70, 170))],
 'up': [((-68, 44), (-120, -20), (-110, -110)), ((68, 44), (120, -20), (110, -110))],
 'shrug': [((-68, 44), (-120, 90), (-150, 30)), ((68, 44), (120, 90), (150, 30))],
 'pointR': [((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (170, 20), (260, -10))],
 'pointL': [((-68, 44), (-170, 20), (-260, -10)), ((68, 44), (90, 128), (86, 206))],
 'wave': [((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (130, -10), (120, -100))],
 'tense': [((-68, 30), (-78, 124), (-70, 200)), ((68, 30), (78, 124), (70, 200))],
}

def eat_arms(ph):
    u = 0.5 - 0.5 * math.cos(ph)
    hand = (lerp(90, 20, u), lerp(170, -30, u))
    return [((-68, 44), (-120, 150), (-90, 185)), ((68, 44), (120, lerp(150, 90, u)), hand)]

def person3(ctx, x, y, s, outfit='suit', hair='spiky', hcol=None, expr='neutral', look=(0, 0), arms='down', legs='stand',
            walk=None, glasses=None, beard=None, wrinkles=False, cap=None, back=False, tear=None, rot=0, seed=300,
            headrot=0, width=1.0, skin=None, earpiece=False, tie=None, tie_off=0.0, extra=None, shrug=0.0, flip=False, color=None):
    global SKIN
    hcol = hcol or HAIR
    if isinstance(arms, str): arms = ARMS[arms]
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(-s if flip else s, s)
    old = SKIN
    if skin is not None: SKIN = skin
    body3(ctx, outfit, arms, legs, walk, seed, width, tie, tie_off, color=color, shrug=shrug)
    ctx.save(); ctx.translate(0, -shrug * 0.6); ctx.rotate(headrot)
    if extra == 'bald':
        head2(ctx, 'none', hcol, expr, look, glasses, beard, wrinkles, cap, back, tear, seed + 50)
        for sx in (-1, 1): shape(ctx, [(sx * 58, -76), (sx * 66, -118), (sx * 50, -112), (sx * 48, -84)], hcol, 2.5, seed + 90 + sx)
    else:
        head2(ctx, hair, hcol, expr, look, glasses, beard, wrinkles, cap, back, tear, seed + 50)
    if extra == 'bun':
        shape(ctx, ell(0, -182, 26, 20, 16), hcol, 3, seed + 95)
    if extra == 'scar':
        rough(ctx, [(34, -104), (46, -72)], 2.5, seed + 96, hexc('a06a5a'))
    if earpiece:
        rough(ctx, [(62, -84), (70, -50), (58, -30), (64, -10), (54, 6)], 2, seed + 97, hexc('d8d8d8'))
    ctx.restore()
    SKIN = old
    ctx.restore()

def price_tag(ctx, x, y, s, label, pop, col=(1, 1, 1), rot=-0.12):
    if pop <= 0.01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(pop, pop)
    shape(ctx, [(-10, -44), (170, -44), (170, 44), (-10, 44), (-50, 0)], hexc('f3e6c4'), 4, 2000 + len(label))
    shape(ctx, ell(-22, 0, 8, 8, 10), hexc('7d6b52'), 2, 2010)
    text(ctx, label, 80, 18, 54 * s, 'Bebas Neue', INK, anchor='c')
    ctx.restore()

def bubble(ctx, x0, y0, x1, y1, tail, alpha=1.0, seed=2100):
    pts = [(x0, y0), (x1, y0), (x1, y1), ((x0 + x1) / 2 + 40, y1), tail, ((x0 + x1) / 2 - 20, y1), (x0, y1)]
    shape(ctx, pts, (1, 1, 1), 5, seed, alpha=alpha)

def grayscale_surface(surf):
    surf.flush()
    a = np.ndarray((H, W, 4), np.uint8, surf.get_data())
    g = (a[..., 0] * 0.11 + a[..., 1] * 0.59 + a[..., 2] * 0.30).astype(np.uint8)
    b = a.copy(); b[..., 0] = g; b[..., 1] = g; b[..., 2] = g
    return cairo.ImageSurface.create_for_data(bytearray(b.tobytes()), cairo.FORMAT_ARGB32, W, H, W * 4)

# ---------------- cast (reuse across videos; recolour via color=/hcol=) ----------------
def hero(ctx, x, y, s, **kw):
    """Main 'YOU' character: spiky black hair. Default outfit = green hoodie; pass outfit='suit' etc."""
    outfit = kw.pop('outfit', 'hoodie')
    person3(ctx, x, y, s, outfit, 'spiky', HAIR, **kw)
def suit_man(ctx, x, y, s, seed=1600, **kw):   # agents / guards
    person3(ctx, x, y, s, 'suit', 'slick', hexc('14161a'), glasses='sun', seed=seed, **kw)
def doctor(ctx, x, y, s, seed=410, **kw):
    person3(ctx, x, y, s, 'vest', 'short', hexc('5a3d2a'), glasses='round', seed=seed, color=hexc('eef0ee'), **kw)
def officer(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'olive', 'crew', hexc('9a968e'), wrinkles=True, extra='scar', seed=1500, **kw)
def leader(ctx, x, y, s, **kw):
    kw.setdefault('width', 1.22)
    person3(ctx, x, y, s, 'white', 'slick', hexc('cfcac0'), beard='mous', wrinkles=True, seed=1400, **kw)
def old_man(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'cardi', 'none', hexc('b9b4aa'), extra='bald', wrinkles=True, beard='mous', seed=1700, **kw)
def old_woman(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'cardi', 'short', hexc('9d978c'), extra='bun', wrinkles=True, seed=1750, color=hexc('7a5a7a'), **kw)
def kid(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'dress', 'bob', hexc('4a2e1e'), seed=1900, color=hexc('e07a9a'), **kw)
def nerd(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'tee', 'spiky_s', HAIR, glasses='round', seed=1800, **kw)
def woman(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'dress', 'bob', hexc('a07040'), seed=2530, color=hexc('2c5f5a'), **kw)

def tint(c1, c2, u): return tuple(lerp(a, b, min(max(u, 0), 1)) for a, b in zip(c1, c2))

def room(ctx, wall=hexc('c9b89a'), floor=hexc('8a7058'), y=None):
    y = y or int(H * 0.7)
    shape(ctx, rect(-300, -300, W + 300, y), wall, 0, 1)
    for k in range(-2, W // 140 + 3): rough(ctx, [(k * 140, -300), (k * 140 + 3, y)], 2, 800 + k, tint(wall, (0, 0, 0), 0.1))
    shape(ctx, rect(-300, y, W + 300, H + 300), floor, 4, 802)

def clock(ctx, x, y, r, t, speed=1.0, seed=3010):
    shape(ctx, ell(x, y, r, r, 30), (0.96, 0.95, 0.9), 5, seed)
    a = t * speed; b = a / 12
    rough(ctx, [(x, y), (x + r * 0.8 * math.sin(a), y - r * 0.8 * math.cos(a))], 4, seed + 1)
    rough(ctx, [(x, y), (x + r * 0.5 * math.sin(b), y - r * 0.5 * math.cos(b))], 6, seed + 2)

def say(ctx, s, x0, y0, x1, y1, tail, t0, t, size=56):
    """Speech bubble that fades in at t0. Use '\n' for line breaks."""
    if t < t0: return
    a = min(1, (t - t0) * 5)
    bubble(ctx, x0, y0, x1, y1, tail, alpha=a)
    ls = s.split('\n')
    for i, ln in enumerate(ls):
        text(ctx, ln, (x0 + x1) / 2, (y0 + y1) / 2 + 18 + (i - (len(ls) - 1) / 2) * size * 1.1, size, anchor='c', alpha=a)

def caption(ctx, s, y=None, size=None, maxw=None):
    """Bottom caption, white with thick black outline (Patrick Hand)."""
    size = size or (74 if H > W else 64); maxw = maxw or W - 180
    y = y or (int(H * 0.855) if H > W else H - 110)
    ctx.select_font_face('Patrick Hand'); ctx.set_font_size(size)
    words = s.split(); lines = []; cur = ''
    for w_ in words:
        test = (cur + ' ' + w_).strip()
        if ctx.text_extents(test).width > maxw and cur: lines.append(cur); cur = w_
        else: cur = test
    lines.append(cur)
    y0 = y - (len(lines) - 1) * size * 0.55
    for i, ln in enumerate(lines):
        e = ctx.text_extents(ln); x = W / 2 - e.width / 2 - e.x_bearing; yy = y0 + i * size * 1.13
        ctx.move_to(x, yy); ctx.text_path(ln)
        ctx.set_source_rgba(0, 0, 0, 0.9); ctx.set_line_width(12); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
        ctx.move_to(x, yy); ctx.set_source_rgb(1, 1, 1); ctx.show_text(ln)

def rec_frame(ctx, x0, y0, x1, y1, t, a=1.0, L=70):
    for (cx, cy, dx, dy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        rough(ctx, [(cx + dx * L, cy), (cx, cy), (cx, cy + dy * L)], 6, 700 + int(cx + cy), hexc('e0e0e0'), alpha=a)
    if int(t * 2.5) % 2 == 0: shape(ctx, ell(x0 + 40, y0 + 50, 12, 12, 12), hexc('e8312a'), 0, 0, alpha=a)
    text(ctx, 'REC', x0 + 64, y0 + 64, 44, 'Bebas Neue', (0.9, 0.9, 0.9), alpha=a)

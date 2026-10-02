"""pk — Pakistani extension for stickkit (16:9): shalwar kameez, waistcoat, dupatta, topi, Urdu text, props."""
import os, math, random, cairo, numpy as np
from PIL import Image, ImageDraw, ImageFont
import stickkit as K
K.W, K.H = 1920, 1080
from stickkit import (hexc, INK, rough, shape, ell, bez, rect, lerp, ease_out, ease_out_back, ease_io, radial, text,
                      glow_text, stamp, cam, dark, bubble, ARMS, head2)
W, H, FPS = 1920, 1080, 24
K.SKIN = hexc('e0b892')           # warm Pakistani skin tone (default for everyone)
SKIN = K.SKIN
DUN = hexc('c9a77a'); MUD = hexc('b07a4f'); MUD_D = hexc('8e5d3a'); FIELD = hexc('7f9a4a'); FIELD2 = hexc('a7b45a')
NIGHT1 = hexc('0d1424'); NIGHT2 = hexc('1f2d45'); SEA1 = hexc('14243a'); SEA2 = hexc('0a1220')
KAMEEZ = hexc('e9e2cf'); BLUEK = hexc('9fb5c6'); WAIST = hexc('5a4030'); AMMI = hexc('7b3552'); DUPATTA = hexc('a8456a')

# ---------------- Urdu text (PIL + raqm), cached as cairo surfaces ----------------
_FONT = None
def _fontpath():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in ('~/.fonts/NotoNastaliqUrdu.ttf', os.path.join(here, 'fonts', 'UrduNaskh_FreeSerifBold.ttf'),
              os.path.join(here, 'UrduNaskh_FreeSerifBold.ttf'), '~/.fonts/UrduNaskh_FreeSerifBold.ttf',
              os.path.expanduser('~/mnt/Dunky Video/fonts/UrduNaskh_FreeSerifBold.ttf')):
        p = os.path.expanduser(p)
        if os.path.exists(p): return p
    raise FileNotFoundError('no Urdu font')
NASTALIQ = 'Nastaliq' in _fontpath()
_FC = {}
def _f(size):
    if size not in _FC: _FC[size] = ImageFont.truetype(_fontpath(), size, layout_engine=ImageFont.Layout.RAQM)
    return _FC[size]
_SC = {}
def urdu_surface(s, size, color=(1, 1, 1), stroke=None, sw=None, maxw=None, lh=None):
    """Return (surface, w, h) of right-to-left Urdu text, wrapped to maxw, centred lines."""
    key = (s, size, color, stroke, sw, maxw, lh)
    if key in _SC: return _SC[key]
    f = _f(size); d = ImageDraw.Draw(Image.new('L', (1, 1)))
    lines = []
    for para in s.split('\n'):
        if maxw is None: lines.append(para); continue
        cur = ''
        for w_ in para.split():
            test = (cur + ' ' + w_).strip()
            if d.textlength(test, font=f, direction='rtl') > maxw and cur: lines.append(cur); cur = w_
            else: cur = test
        lines.append(cur)
    sw = (max(3, size // 12) if stroke else 0) if sw is None else sw
    lh = lh or int(size * (1.9 if NASTALIQ else 1.45))
    widths = [d.textlength(l, font=f, direction='rtl') for l in lines]
    Wd = int(max(widths) + 2 * sw + size); Hd = int(lh * len(lines) + size * 0.6)
    im = Image.new('RGBA', (Wd, Hd), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    fc = tuple(int(c * 255) for c in color) + (255,)
    sc = tuple(int(c * 255) for c in stroke) + (255,) if stroke else None
    for i, ln in enumerate(lines):
        dr.text((Wd / 2, size * 0.3 + lh * (i + 0.5)), ln, font=f, fill=fc, anchor='mm', direction='rtl',
                stroke_width=sw, stroke_fill=sc)
    a = np.array(im).astype(np.float32); al = a[..., 3:4] / 255.0
    bgra = np.dstack([a[..., 2:3] * al, a[..., 1:2] * al, a[..., 0:1] * al, a[..., 3:4]]).astype(np.uint8)
    surf = cairo.ImageSurface.create_for_data(bytearray(bgra.tobytes()), cairo.FORMAT_ARGB32, Wd, Hd, Wd * 4)
    _SC[key] = (surf, Wd, Hd); return _SC[key]

def is_urdu(s): return any('\u0600' <= c <= '\u06ff' for c in s)

def ltext(ctx, s, x, y, size, color=INK, stroke=None, pop=1.0, alpha=1.0, rot=0.0, maxw=None, sw=None, shadow=False, font='Patrick Hand'):
    """Latin (Roman Urdu) text centred at (x, y), wrapped to maxw."""
    if pop <= 0.01 or alpha <= 0.01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(pop, pop)
    ctx.select_font_face(font); ctx.set_font_size(size)
    lines = []
    for para in s.split('\n'):
        cur = ''
        for w_ in para.split():
            test = (cur + ' ' + w_).strip()
            if maxw and ctx.text_extents(test).width > maxw and cur: lines.append(cur); cur = w_
            else: cur = test
        lines.append(cur)
    lh = size * 1.08; y0 = -(len(lines) - 1) * lh / 2
    for i, ln in enumerate(lines):
        e = ctx.text_extents(ln); xx = -e.width / 2 - e.x_bearing; yy = y0 + i * lh - e.y_bearing / 2 - e.height / 2 + e.height / 2 + size * 0.33
        if shadow:
            ctx.move_to(xx + 8, yy + 10); ctx.text_path(ln); ctx.set_source_rgba(0, 0, 0, 0.45 * alpha); ctx.fill()
        if stroke:
            ctx.move_to(xx, yy); ctx.text_path(ln); ctx.set_source_rgba(*stroke, alpha)
            ctx.set_line_width(sw or max(6, size / 7)); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
        ctx.move_to(xx, yy); ctx.set_source_rgba(*color, alpha); ctx.show_text(ln)
    ctx.restore()

def utext(ctx, s, x, y, size, color=INK, stroke=None, pop=1.0, alpha=1.0, rot=0.0, maxw=None, sw=None, shadow=False, font='Patrick Hand'):
    """Draw text centred at (x, y): Urdu via PIL/raqm, Roman via cairo."""
    if pop <= 0.01 or alpha <= 0.01: return
    if not is_urdu(s): return ltext(ctx, s, x, y, size, color, stroke, pop, alpha, rot, maxw, sw, shadow, font)
    surf, w, h = urdu_surface(s, size, tuple(color), tuple(stroke) if stroke else None, sw, maxw)
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(pop, pop)
    if shadow:
        sh, _, _ = urdu_surface(s, size, (0, 0, 0), (0, 0, 0) if stroke else None, sw, maxw)
        ctx.set_source_surface(sh, -w / 2 + 8, -h / 2 + 10); ctx.paint_with_alpha(0.45 * alpha)
    ctx.set_source_surface(surf, -w / 2, -h / 2); ctx.paint_with_alpha(alpha)
    ctx.restore()

def urdu_caption(ctx, s, y=None, size=58, alpha=1.0):
    utext(ctx, s, W / 2, y or H - 92, size, (1, 1, 1), stroke=(0, 0, 0), maxw=W - 260, sw=max(5, size // 9), alpha=alpha)

def usay(ctx, s, x0, y0, x1, y1, tail, t0, t, size=60):
    if t < t0: return
    a = min(1, (t - t0) * 5); p = ease_out_back((t - t0) / 0.25)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ctx.save(); ctx.translate(cx, cy); ctx.scale(p, p); ctx.translate(-cx, -cy)
    bubble(ctx, x0, y0, x1, y1, tail, alpha=a)
    utext(ctx, s, cx, cy, size, INK, alpha=a, maxw=(x1 - x0) - 50)
    ctx.restore()

def ustamp(ctx, s, x, y, t0, t, size=100, rot=-0.15):
    """Red rubber stamp with Urdu text."""
    if t < t0: return
    if not is_urdu(s): return stamp(ctx, s, x, y, t0, t, size, rot)
    sc = lerp(1.8, 1.0, ease_out((t - t0) / 0.12)); a = min(1, (t - t0) / 0.08) * 0.92
    red = hexc('c0322a')
    surf, w, h = urdu_surface(s, size, red)
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc)
    pad = 20
    rough(ctx, rect(-w / 2 - pad + size * 0.3, -h / 2 - pad + 10, w / 2 + pad - size * 0.3, h / 2 + pad - 10), 9, 999, red, closed=True, alpha=a)
    ctx.set_source_surface(surf, -w / 2, -h / 2); ctx.paint_with_alpha(a)
    ctx.restore()

# ---------------- Pakistani bodies ----------------
def _arms(ctx, arms, sy, wd, seed, sleeve):
    for (sh, el, ha) in arms:
        sh = (sh[0] * wd, sh[1] + sy)
        rough(ctx, [sh, el, ha], 15, seed + int(sh[0]) + 1, sleeve)
        rough(ctx, [sh, el, ha], 3, seed + int(sh[0]) + 2, INK, alpha=0.9)
        shape(ctx, ell(ha[0], ha[1], 12, 12, 14), K.SKIN, 3, seed + int(ha[0]) + 3)

def body_pk(ctx, outfit, arms, legs, walk, seed, width=1.0, color=None, shrug=0.0, waist=None, watch=False, scol=None):
    col = color or {'kameez': KAMEEZ, 'ammi': AMMI}.get(outfit, KAMEEZ)
    scol = scol or tuple(c * 0.93 for c in col)
    wd = width; sy = -shrug
    if legs == 'stand':
        for i, sx in enumerate((-1, 1)):
            lift = 0; fx = sx * 30 * wd
            if walk is not None:
                ph = walk + i * math.pi
                lift = 22 * max(0, math.sin(ph)); fx += sx * 8 * math.cos(ph)
            hip = sx * 30 * wd
            leg = [(hip - 26, 250), (hip + 26, 250), (fx + 24, 316 - lift), (fx + 14, 326 - lift), (fx - 14, 326 - lift), (fx - 24, 316 - lift)]
            shape(ctx, leg, scol, 3.5, seed + 5 + sx)
            rough(ctx, [(fx - 14, 318 - lift), (fx + 14, 318 - lift)], 2, seed + 6 + sx, tuple(c * 0.7 for c in scol))
            shape(ctx, ell(fx + sx * 8, 334 - lift, 22, 8, 16), hexc('5a3a24'), 3, seed + 8 + sx)
    hem = 286 if outfit != 'ammi' else 292
    torso = [(-48 * wd, 10 + sy), (-72 * wd, 38 + sy), (-80 * wd, 170), (-88 * wd, hem), (88 * wd, hem), (80 * wd, 170), (72 * wd, 38 + sy), (48 * wd, 10 + sy)]
    shape(ctx, torso, col, 4.5, seed + 1)
    dk = tuple(c * 0.78 for c in col)
    for sx in (-1, 1): rough(ctx, [(sx * 82 * wd, 205), (sx * 88 * wd, hem - 2)], 2.5, seed + 2 + sx, dk)   # side slits
    if outfit == 'kameez':
        rough(ctx, [(0, 14 + sy), (0, 96)], 2.5, seed + 4, dk)
        for k in range(3): shape(ctx, ell(0, 34 + k * 22, 3.5, 3.5, 8), dk, 1, seed + 10 + k)
        rough(ctx, [(-22, 10 + sy), (0, 20 + sy), (22, 10 + sy)], 3, seed + 9, dk)
    else:   # ammi: embroidered neckline
        rough(ctx, bez((-26, 12 + sy), (-18, 50), (18, 50), (26, 12 + sy), 10), 3, seed + 9, GOLD_)
    if waist is not None:
        for sx in (-1, 1):
            pan = [(sx * 26, 12 + sy), (sx * 50 * wd, 14 + sy), (sx * 74 * wd, 42 + sy), (sx * 80 * wd, 196), (sx * 6, 196), (sx * 6, 92)]
            shape(ctx, pan, waist, 3.5, seed + 20 + sx)
        for k in range(4): shape(ctx, ell(-10, 108 + k * 22, 4, 4, 8), hexc('d8c27a'), 1, seed + 24 + k)
    rough(ctx, [(0, 8), (0, -30)], 7, seed + 4)
    _arms(ctx, arms, sy, wd, seed, col)
    if watch:
        ha = arms[1][2]; el = arms[1][1]
        wx, wy = lerp(el[0], ha[0], 0.8), lerp(el[1], ha[1], 0.8)
        shape(ctx, ell(wx, wy, 13, 13, 14), hexc('e0b84a'), 3, seed + 40)
        shape(ctx, ell(wx, wy, 6, 6, 10), hexc('fff2c0'), 1.5, seed + 41)
GOLD_ = hexc('d9b44a')

def person(ctx, x, y, s, outfit='kameez', hair='spiky', hcol=None, expr='neutral', look=(0, 0), arms='down', legs='stand',
           walk=None, glasses=None, beard=None, wrinkles=False, back=False, tear=None, rot=0, seed=300, headrot=0,
           width=1.0, color=None, shrug=0.0, flip=False, waist=None, dupatta=None, topi=None, watch=False, skin=None, scol=None):
    """Pakistani character. outfit: kameez | ammi | any stickkit outfit (suit, tee, hoodie...)."""
    hcol = hcol or K.HAIR
    if isinstance(arms, str): arms = ARMS[arms]
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(-s if flip else s, s)
    old = K.SKIN
    if skin is not None: K.SKIN = skin
    if dupatta is not None and not back:    # back drape behind body
        shape(ctx, [(-70, -60), (70, -60), (96, 120), (-96, 120)], tuple(c * 0.8 for c in dupatta), 3.5, seed + 70)
    if outfit in ('kameez', 'ammi'):
        body_pk(ctx, outfit, arms, legs, walk, seed, width, color, shrug, waist, watch, scol)
    else:
        K.body3(ctx, outfit, arms, legs, walk, seed, width, None, 0.0, color=color, shrug=shrug)
    ctx.save(); ctx.translate(0, -shrug * 0.6); ctx.rotate(headrot)
    if hair == 'bald':
        head2(ctx, 'none', hcol, expr, look, glasses, beard, wrinkles, None, back, tear, seed + 50)
        for sx in (-1, 1): shape(ctx, [(sx * 58, -76), (sx * 66, -118), (sx * 50, -112), (sx * 48, -84)], hcol, 2.5, seed + 90 + sx)
    else:
        head2(ctx, hair, hcol, expr, look, glasses, beard, wrinkles, None, back, tear, seed + 50)
    if topi is not None:
        shape(ctx, [(-56, -142), (-50, -168), (-26, -178), (26, -178), (50, -168), (56, -142), (0, -150)], topi, 3.5, seed + 80)
        for k in range(3): rough(ctx, [(-40 + k * 40, -170), (-36 + k * 40, -150)], 1.6, seed + 81 + k, tuple(c * 0.8 for c in topi))
    if dupatta is not None:
        out = ell(0, -96, 80, 90, 30, math.pi * 0.72, math.pi * 2.28)
        inn = ell(0, -92, 64, 74, 30, math.pi * 2.2, math.pi * 0.8)
        shape(ctx, [(-74, 40)] + out + [(74, 40), (56, 24)] + inn + [(-56, 24)], dupatta, 4, seed + 85)
        rough(ctx, ell(0, -96, 74, 84, 30, math.pi * 1.05, math.pi * 1.95), 2, seed + 86, GOLD_)
    ctx.restore()
    K.SKIN = old
    ctx.restore()

# ---------------- cast ----------------
def hamza(ctx, x, y, s, **kw):
    kw.setdefault('color', BLUEK); person(ctx, x, y, s, kw.pop('outfit', 'kameez'), 'spiky', K.HAIR, seed=kw.pop('seed', 3100), **kw)
def abba(ctx, x, y, s, **kw):
    person(ctx, x, y, s, 'kameez', 'bald', hexc('c9c4ba'), beard='full', wrinkles=True, topi=hexc('f4f1e8'),
           waist=WAIST, color=hexc('d9cdb2'), seed=kw.pop('seed', 3200), **kw)
def ammi(ctx, x, y, s, **kw):
    person(ctx, x, y, s, 'ammi', 'short', hexc('2a2420'), wrinkles=True, dupatta=DUPATTA, seed=kw.pop('seed', 3300), **kw)
def bilal(ctx, x, y, s, **kw):
    kw.setdefault('glasses', 'sun'); kw.setdefault('color', hexc('1f1f24'))
    person(ctx, x, y, s, kw.pop('outfit', 'tee'), 'slick', K.HAIR, seed=kw.pop('seed', 3400), **kw)
def agent(ctx, x, y, s, **kw):
    kw.setdefault('width', 1.25)
    person(ctx, x, y, s, 'kameez', 'slick', hexc('15151a'), beard='mous', waist=hexc('23262c'), watch=True,
           color=hexc('f2efe6'), seed=kw.pop('seed', 3500), **kw)

# ---------------- props / sets ----------------
def sky_grad(ctx, top, bot, y0=0, y1=H):
    g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(1, *bot)
    ctx.rectangle(-500, -500, W + 1000, H + 1000); ctx.set_source(g); ctx.fill()

def moon(ctx, x, y, r):
    radial(ctx, x, y, r * 4, (0.8, 0.85, 1.0), 0.18)
    shape(ctx, ell(x, y, r, r, 30), hexc('efe9d2'), 3, 4000)

def stars(ctx, n=60, seed=4010, t=0):
    rng = random.Random(seed)
    for i in range(n):
        x, y = rng.uniform(0, W), rng.uniform(0, H * 0.45); tw = 0.5 + 0.5 * math.sin(t * 3 + i)
        ctx.arc(x, y, rng.uniform(1.2, 2.6), 0, 7); ctx.set_source_rgba(1, 1, 0.95, 0.35 + 0.5 * tw); ctx.fill()

def waves(ctx, y0, t, col=SEA1, rows=6, amp=10, seed=4100, spacing=55):
    shape(ctx, rect(-400, y0, W + 400, H + 400), col, 0, 1)
    for r in range(rows):
        y = y0 + 20 + r * spacing; ph = t * (1.2 + r * 0.25) + r
        pts = [(x, y + amp * (0.6 + r * 0.15) * math.sin(x / 90 + ph)) for x in range(-200, W + 240, 40)]
        rough(ctx, pts, 2.5 + r * 0.4, seed + r, hexc('3e5a78'), alpha=0.55)

def boat(ctx, x, y, s, t, crowd=True, smoke=0.0, tilt=0.0, seed=4200, heads=140):
    """Old wooden fishing boat, overloaded. (x, y) = waterline centre."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(tilt + 0.015 * math.sin(t * 1.3)); ctx.scale(s, s)
    ctx.translate(0, 6 * math.sin(t * 1.7))
    if crowd:
        rng = random.Random(seed)
        for i in range(heads):
            hx = rng.uniform(-330, 330); hy = rng.uniform(-150, -90) - (0 if abs(hx) < 260 else -20)
            r = rng.uniform(13, 17); bob = 2 * math.sin(t * 2 + i)
            shape(ctx, ell(hx, hy + 40 + bob, r * 1.3, r * 1.6, 12), rng.choice([hexc('7c8a99'), hexc('8a6a4a'), hexc('5f6e45'), hexc('a8a29a'), hexc('4f5d6b')]), 2, seed + i)
            shape(ctx, ell(hx, hy + bob, r, r * 1.1, 14), K.SKIN, 2.2, seed + 500 + i)
            shape(ctx, ell(hx, hy - r * 0.45 + bob, r * 1.02, r * 0.6, 12, math.pi, 2 * math.pi), K.HAIR, 1.5, seed + 900 + i)
    hull = [(-420, -70), (420, -70), (360, 40), (-330, 40)]
    shape(ctx, hull, hexc('6b4a35'), 6, seed + 1)
    for k in range(3): rough(ctx, [(-400 + k * 10, -40 + k * 26), (400 - k * 18, -40 + k * 26)], 2.5, seed + 2 + k, hexc('4b3324'))
    shape(ctx, rect(-420, -84, 420, -66), hexc('c8b080'), 4, seed + 6)
    for k in range(6): shape(ctx, ell(-320 + k * 120, -10 + (k % 2) * 14, 16, 9, 10), hexc('8a5a3a'), 1.5, seed + 30 + k, alpha=0.7)   # rust
    shape(ctx, rect(-30, -230, -14, -84), hexc('5a3d2a'), 3, seed + 7)            # mast
    shape(ctx, rect(-160, -150, -60, -84), hexc('8e8a80'), 3, seed + 8)          # cabin
    shape(ctx, rect(330, -120, 380, -84), hexc('3a3a3e'), 3, seed + 9)           # engine
    if smoke > 0:
        for k in range(4):
            u = (smoke * 1.5 - k * 0.2)
            if u <= 0: continue
            a = max(0, 1 - u) * 0.6
            shape(ctx, ell(355 + k * 14 + u * 40, -140 - u * 140, 22 + u * 40, 18 + u * 30, 16), hexc('6a6a70'), 2, seed + 40 + k, alpha=a)
    ctx.restore()

def mud_house(ctx, x, base, w, h, seed, col=MUD, door=True):
    shape(ctx, rect(x - w / 2, base - h, x + w / 2, base), col, 4, seed)
    shape(ctx, rect(x - w / 2 - 10, base - h - 14, x + w / 2 + 10, base - h), tuple(c * 0.85 for c in col), 3.5, seed + 1)
    if door: shape(ctx, rect(x - 24, base - 90, x + 24, base), hexc('4a3020'), 3, seed + 2)
    shape(ctx, rect(x + w / 4 - 18, base - h + 30, x + w / 4 + 18, base - h + 64), hexc('2a2a30'), 2.5, seed + 3)

def kikar(ctx, x, base, h, seed):
    rough(ctx, [(x, base), (x - 8, base - h * 0.5), (x + 6, base - h * 0.8)], 10, seed, hexc('4a3a2a'))
    rough(ctx, [(x - 4, base - h * 0.55), (x - 60, base - h * 0.8)], 6, seed + 1, hexc('4a3a2a'))
    for (dx, dy, rx) in ((-70, -0.88, 90), (30, -0.95, 110), (-10, -1.05, 80)):
        shape(ctx, ell(x + dx, base + h * dy, rx, rx * 0.35, 20), hexc('5b7a3a'), 3, seed + 10 + dx)

def buffalo(ctx, x, base, s, t, seed=4400):
    ctx.save(); ctx.translate(x, base); ctx.scale(s, s)
    for k, lx in enumerate((-60, -30, 40, 70)):
        rough(ctx, [(lx, -40), (lx + 2 * math.sin(t + k), 0)], 9, seed + k, hexc('1e1e22'))
    shape(ctx, ell(0, -70, 100, 48, 24), hexc('2a2a30'), 4, seed + 5)
    shape(ctx, ell(-110, -82 + 3 * math.sin(t * 0.8), 32, 26, 16), hexc('2a2a30'), 4, seed + 6)
    rough(ctx, [(-120, -104), (-150, -118), (-140, -96)], 4, seed + 7, hexc('d8d0c0'))
    rough(ctx, [(-100, -104), (-80, -122), (-92, -100)], 4, seed + 8, hexc('d8d0c0'))
    shape(ctx, ell(-122, -86, 4, 4, 8), (1, 1, 1), 0, 0)
    rough(ctx, [(98, -86), (112, -50)], 3, seed + 9, hexc('1e1e22'))
    ctx.restore()

def village(ctx, t, ground=820, sunset=False):
    sky_grad(ctx, hexc('9fc3d6') if not sunset else hexc('e8a46a'), hexc('f1e2bf'), 0, ground)
    shape(ctx, ell(1580, 200, 70, 70, 24), hexc('fbe7a0'), 3, 4500)
    K.hills(ctx, ground - 120, 50, hexc('9aa97a'), 4501)
    shape(ctx, rect(-400, ground - 40, W + 400, H + 400), FIELD2, 4, 4502)
    for k in range(9):
        y = ground - 20 + k * 34
        rough(ctx, [(-300, y), (W + 300, y + 8)], 3, 4510 + k, hexc('8a9a48'), alpha=0.7)
    mud_house(ctx, 360, ground, 300, 200, 4520)
    mud_house(ctx, 680, ground + 10, 220, 170, 4530, col=hexc('c08a5a'))
    mud_house(ctx, 1290, ground, 260, 190, 4540, col=hexc('a8724a'))
    kikar(ctx, 1000, ground, 300, 4550)
    shape(ctx, [(820, H + 10), (900, ground - 30), (960, ground - 30), (1180, H + 10)], DUN, 3, 4560)   # dirt path

def charpai(ctx, x, base, s, seed=4600):
    ctx.save(); ctx.translate(x, base); ctx.scale(s, s)
    for lx in (-180, 180): shape(ctx, rect(lx - 10, -90, lx + 10, 0), hexc('6b4a2a'), 3, seed + lx)
    shape(ctx, [(-200, -110), (200, -110), (210, -86), (-210, -86)], hexc('8a6438'), 4, seed + 1)
    for k in range(-9, 10, 2): rough(ctx, [(k * 20, -108), (k * 20 + 14, -88)], 1.6, seed + 10 + k, hexc('d8c79a'))
    ctx.restore()

def chai_cup(ctx, x, y, s, seed=4700, steam=0.0, t=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    shape(ctx, [(-22, -40), (22, -40), (16, 0), (-16, 0)], hexc('f0ede6'), 3, seed)
    shape(ctx, ell(0, -40, 22, 6, 14), hexc('b07a4a'), 2, seed + 1)
    if steam > 0:
        for k in range(2):
            rough(ctx, [(-6 + k * 12 + 6 * math.sin(t * 3 + j + k), -50 - j * 14) for j in range(5)], 2.5, seed + 5 + k, (1, 1, 1), alpha=0.5 * steam)
    ctx.restore()

def lantern(ctx, x, y, s, t, seed=4800):
    radial(ctx, x, y, 420 * s, (1, 0.75, 0.35), 0.35 + 0.04 * math.sin(t * 9))
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    rough(ctx, ell(0, -60, 20, 18, 16, math.pi, 2 * math.pi), 3, seed)
    shape(ctx, [(-24, -40), (24, -40), (28, 30), (-28, 30)], hexc('fff0b0'), 4, seed + 1, alpha=0.9)
    shape(ctx, ell(0, 0, 8, 14, 12), hexc('ffb040'), 0, 0)
    shape(ctx, rect(-32, 30, 32, 44), hexc('3a3a3e'), 3, seed + 2)
    ctx.restore()

def phone(ctx, x, y, s, rot=0, screen=hexc('1c2430'), seed=4900):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    shape(ctx, [(-70, -140), (70, -140), (70, 140), (-70, 140)], hexc('1a1a1e'), 5, seed)
    shape(ctx, [(-60, -126), (60, -126), (60, 126), (-60, 126)], screen, 0, 0)
    ctx.restore()

def red_car(ctx, x, base, s, seed=5000):
    ctx.save(); ctx.translate(x, base); ctx.scale(s, s)
    shape(ctx, [(-260, -40), (-250, -100), (-140, -110), (-80, -170), (90, -170), (160, -110), (250, -96), (262, -40)], hexc('d0302a'), 5, seed)
    shape(ctx, [(-66, -158), (0, -158), (0, -112), (-120, -112)], hexc('a9d4e8'), 3, seed + 1)
    shape(ctx, [(14, -158), (82, -158), (138, -112), (14, -112)], hexc('a9d4e8'), 3, seed + 2)
    rough(ctx, [(-160, -80), (220, -80)], 3, seed + 3, hexc('fff0f0'), alpha=0.6)
    for wx in (-160, 160):
        shape(ctx, ell(wx, -30, 44, 44, 24), hexc('151518'), 4, seed + wx)
        shape(ctx, ell(wx, -30, 20, 20, 16), hexc('c8c8cc'), 3, seed + wx + 1)
    ctx.restore()

def heart(ctx, x, y, s, alpha=1.0, seed=5100, col=hexc('e8314a')):
    pts = bez((0, 30), (-60, -10), (-30, -50), (0, -20), 12) + bez((0, -20), (30, -50), (60, -10), (0, 30), 12)[1:]
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); shape(ctx, pts, col, 3, seed, alpha=alpha); ctx.restore()

def envelope(ctx, x, y, s, rot, seed):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    shape(ctx, rect(-80, -50, 80, 50), hexc('f4efe2'), 4, seed)
    rough(ctx, [(-80, -50), (0, 10), (80, -50)], 3, seed + 1)
    text(ctx, 'CV', 0, 38, 34, 'Bebas Neue', hexc('8a3030'), anchor='c')
    ctx.restore()

def paper(ctx, x, y, s, rot, label, seed, col=hexc('f4efe2')):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    shape(ctx, rect(-70, -90, 70, 90), col, 3.5, seed)
    for k in range(4): rough(ctx, [(-50, -40 + k * 22), (50, -40 + k * 22)], 2, seed + 1 + k, hexc('a8a08c'))
    text(ctx, label, 0, -54, 34, 'Bebas Neue', hexc('b03030'), anchor='c')
    ctx.restore()

def vhs(ctx, t, a=1.0):
    rng = random.Random(int(t * 24))
    for i in range(10):
        y = rng.uniform(0, H); h = rng.uniform(2, 14)
        ctx.rectangle(0, y, W, h); ctx.set_source_rgba(1, 1, 1, 0.08 * a + rng.uniform(0, 0.12) * a); ctx.fill()
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.2, 0.3, 0.6, 0.12 * a); ctx.fill()

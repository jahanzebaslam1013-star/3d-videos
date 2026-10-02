"""brand — PIVOT channel branding: wordmark logo, profile picture, YouTube banner (pycairo).
Run:  python3 brand.py   -> writes PNGs into brand/
"""
import os, math, random, cairo, numpy as np
import stickkit as K
import pk
from stickkit import hexc, INK, rough, shape, ell, bez, rect, head2

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brand')
PAPER = hexc('efe6d2'); PAPER_D = hexc('e2d6bb'); RED = hexc('c0322a'); GOLD = hexc('ffd66a')
BLUEK = pk.BLUEK


def paper(ctx, w, h, seed=7, col=PAPER):
    ctx.set_source_rgb(*col); ctx.paint()
    rng = np.random.default_rng(seed)
    n = rng.random((h, w)); a = np.zeros((h, w, 4), np.uint8)
    alpha = np.zeros((h, w)); alpha[n < 0.08] = 22; alpha[n > 0.95] = 14
    val = np.zeros((h, w)); val[n > 0.95] = 255
    pm = (val * alpha / 255).astype(np.uint8)
    a[..., 0] = pm; a[..., 1] = pm; a[..., 2] = pm; a[..., 3] = alpha.astype(np.uint8)
    s = cairo.ImageSurface.create_for_data(bytearray(a.tobytes()), cairo.FORMAT_ARGB32, w, h, w * 4)
    ctx.set_source_surface(s, 0, 0); ctx.paint()


def letter(ctx, ch, x, base, size, fill=INK, seed=1, w=None):
    """One Bebas letter, filled, with a rough boiling outline. Returns advance width."""
    ctx.select_font_face('Bebas Neue'); ctx.set_font_size(size)
    e = ctx.text_extents(ch)
    ctx.save(); ctx.move_to(x - e.x_bearing, base); ctx.text_path(ch)
    ctx.set_source_rgb(*fill); ctx.fill_preserve()
    ctx.set_line_width(w or size * 0.03); ctx.set_source_rgb(*INK); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
    ctx.restore()
    return e.width


def face(ctx, cx, cy, r, seed=3100, expr='neutral', look=(0, 0)):
    """Hamza's head ("you") centred on (cx, cy) with face radius ~r."""
    s = r / 66
    ctx.save(); ctx.translate(cx, cy + 95 * s); ctx.scale(s, s)
    K.SKIN = pk.SKIN
    head2(ctx, 'spiky', K.HAIR, expr, look, seed=seed)
    ctx.restore()


def arrow_arc(ctx, cx, cy, r, a0, a1, w, col=RED, seed=11, head=1.0):
    pts = ell(cx, cy, r, r, 60, a0, a1)
    rough(ctx, pts, w, seed, col, amp=1.2)
    ex, ey = pts[-1]; px, py = pts[-2]
    ang = math.atan2(ey - py, ex - px); L = w * 3.2 * head
    tip = (ex + math.cos(ang) * L * 0.5, ey + math.sin(ang) * L * 0.5)
    l = (ex + math.cos(ang + 2.5) * L, ey + math.sin(ang + 2.5) * L)
    rr = (ex + math.cos(ang - 2.5) * L, ey + math.sin(ang - 2.5) * L)
    shape(ctx, [tip, l, rr], col, w * 0.5, seed + 1, col)


def pov_stamp(ctx, x, y, size, rot=-0.14, s='POV'):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.select_font_face('Bebas Neue'); ctx.set_font_size(size); e = ctx.text_extents(s)
    pad = size * 0.16
    rough(ctx, rect(-e.width / 2 - pad, -e.height / 2 - pad, e.width / 2 + pad, e.height / 2 + pad),
          size * 0.07, 999, RED, closed=True)
    ctx.move_to(-e.width / 2 - e.x_bearing, e.height / 2); ctx.set_source_rgba(*RED, 0.95); ctx.show_text(s)
    ctx.restore()


def wordmark(ctx, x, base, size, stamp=True):
    """P I V (face) T — the O is 'you'. Returns total width."""
    gap = size * 0.04
    cx = x
    for i, ch in enumerate('PIV'):
        cx += letter(ctx, ch, cx, base, size, seed=10 + i) + gap
    ctx.select_font_face('Bebas Neue'); ctx.set_font_size(size); eo = ctx.text_extents('O')
    capH = ctx.text_extents('T').height
    r = eo.width * 0.52
    ocx = cx + eo.width / 2; ocy = base - capH / 2
    # red pivot arrow circling the face
    arrow_arc(ctx, ocx, ocy, r * 1.32, math.radians(200), math.radians(500), size * 0.035, seed=21)
    face(ctx, ocx, ocy + r * 0.12, r * 0.92)
    cx += eo.width + gap
    cx += letter(ctx, 'T', cx, base, size, seed=14)
    if stamp:
        pov_stamp(ctx, cx + size * 0.02, base - capH - size * 0.06, size * 0.30, rot=0.16)
    return cx - x


# ---------------------------------------------------------------- outputs
def make_logo():
    w, h = 1600, 700
    for bg in (True, False):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); ctx = cairo.Context(surf)
        if bg: paper(ctx, w, h)
        size = 420
        # measure, then centre
        tmp = cairo.Context(cairo.ImageSurface(cairo.FORMAT_ARGB32, 10, 10))
        tw = wordmark_width(tmp, size)
        wordmark(ctx, (w - tw) / 2, 470, size)
        pk.ltext(ctx, 'Farz karein… ye kahani aap ki hai', w / 2, 600, 58, color=INK) if hasattr(pk, 'ltext') else None
        surf.write_to_png(os.path.join(OUT, 'logo_paper.png' if bg else 'logo_transparent.png'))


def wordmark_width(ctx, size):
    ctx.select_font_face('Bebas Neue'); ctx.set_font_size(size)
    gap = size * 0.04
    return sum(ctx.text_extents(c).width for c in 'PIVOT') + gap * 4


def make_avatar():
    S = 800
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S); ctx = cairo.Context(surf)
    paper(ctx, S, S, seed=9)
    # red ring + pivot arrow
    arrow_arc(ctx, S / 2, S / 2 + 10, 300, math.radians(205), math.radians(505), 30, seed=31, head=1.1)
    face(ctx, S / 2, S / 2 + 70, 200, look=(0, 2))
    surf.write_to_png(os.path.join(OUT, 'profile_800.png'))


def make_banner():
    w, h = 2560, 1440
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); ctx = cairo.Context(surf)
    paper(ctx, w, h, seed=5)
    # safe area (all devices): x 507..2053, y 508..931
    size = 290
    tw = wordmark_width(ctx, size)
    x0 = 610
    wordmark(ctx, x0, 790, size)
    rough(ctx, [(x0, 822), (x0 + tw, 818)], 10, 77, RED)
    pk.ltext(ctx, 'Farz karein… ye kahani aap ki hai.', x0 + tw / 2, 880, 54, color=INK)
    # cast lineup on the right, fully inside the safe area
    gy = 915; s = 0.66
    rough(ctx, [(1440, gy + 6), (2040, gy + 2)], 5, 88, INK)
    pk.abba(ctx, 1520, gy - 340 * s, 0.95 * s)
    pk.ammi(ctx, 1655, gy - 340 * s, 0.92 * s, expr='smile')
    pk.hamza(ctx, 1795, gy - 340 * s, 1.0 * s, expr='smile')
    pk.bilal(ctx, 1940, gy - 340 * s, 0.95 * s)
    surf.write_to_png(os.path.join(OUT, 'banner_2560x1440.png'))
    # safe-area check overlay
    ctx.set_source_rgba(0, 0.6, 1, 0.9); ctx.set_line_width(4)
    ctx.rectangle(507, 508, 1546, 423); ctx.stroke()
    surf.write_to_png(os.path.join(OUT, '_banner_safearea_check.png'))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    make_logo(); make_avatar(); make_banner()
    print('ok ->', OUT)


def make_endcard():
    """1920x1080 end card for Premiere: replaces the DOODLE POV placeholder."""
    w, h = 1920, 1080
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h); ctx = cairo.Context(surf)
    paper(ctx, w, h, seed=12)
    size = 330
    tw = wordmark_width(ctx, size)
    wordmark(ctx, (w - tw) / 2, 560, size)
    rough(ctx, [((w - tw) / 2, 600), ((w + tw) / 2, 596)], 10, 78, RED)
    pk.ltext(ctx, 'Farz karein… ye kahani aap ki hai.', w / 2, 690, 60, color=INK)
    pk.ltext(ctx, 'Agli kahani ke liye SUBSCRIBE karein', w / 2, 800, 46, color=RED)
    surf.write_to_png(os.path.join(OUT, 'endcard_1920x1080.png'))


if __name__ == '__main__':
    make_endcard()

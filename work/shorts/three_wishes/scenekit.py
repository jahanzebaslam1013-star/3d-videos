"""scenekit — shared props + loop-ready runner for stickman reels (shared by reply_all / last_slice)."""
import sys, json, math, subprocess
import numpy as np, cairo, soundfile as sf
import stickkit as K
from stickkit import *
K.W, K.H = 1080, 1920
W, H = K.W, K.H
LINES = [l.strip() for l in open('script.txt') if l.strip()]
LT = json.load(open('lt.json'))
END = sf.info('vo_rt.wav').duration          # loop: video length == VO length, no tail

class Sc:
    def __init__(self, t0): self.t0 = t0
    def L(self, i): return (LT[i][0] - self.t0, LT[i][1] - self.t0)
    def at(self, i, sub):
        k = LINES[i].find(sub); f = max(k, 0) / max(len(LINES[i]), 1); s, e = self.L(i); return s + (e - s) * f

FLOOR = 1450
def stand(s, floor=FLOOR): return floor - 334 * s
def pop(t, t0, d=0.3): return ease_out_back((t - t0) / d)

SHIRT = hexc('dce6f0'); WALL = hexc('cfd6d4'); CARPET = hexc('7c8784')

def me(ctx, x, y, s, **kw):
    kw.setdefault('outfit', 'vest'); kw.setdefault('color', SHIRT)
    hero(ctx, x, y, s, **kw)

def boss(ctx, x, y, s, **kw):
    kw.setdefault('width', 1.18)
    person3(ctx, x, y, s, 'suit', 'none', hexc('8d8a84'), extra='bald', beard='mous', wrinkles=True, seed=2700,
            color=hexc('3a3f4a'), tie=hexc('b0262c'), **kw)

def ceo(ctx, x, y, s, **kw):
    kw.setdefault('width', 1.1)
    person3(ctx, x, y, s, 'suit', 'slick', hexc('e4e1da'), glasses='round', beard='full', wrinkles=True, seed=2900,
            color=hexc('1c2030'), tie=GOLD, **kw)

def office(ctx, wall=WALL, floor=CARPET, y=1330, window=True, plant=True):
    room(ctx, wall, floor, y)
    if window:
        shape(ctx, rect(620, 260, 980, 760), hexc('a9c4d6'), 5, 3100)
        for bx, bw, bh in ((640, 70, 260), (720, 90, 380), (820, 60, 200), (890, 80, 320)):
            shape(ctx, rect(bx, 760 - bh, bx + bw, 760), hexc('8399a8'), 2.5, 3110 + bx)
        rough(ctx, [(800, 260), (800, 760)], 5, 3120); rough(ctx, [(620, 510), (980, 510)], 5, 3121)
    if plant:
        shape(ctx, [(110, y), (90, y - 110), (190, y - 110), (170, y)], hexc('9a5b3a'), 4, 3130)
        for k, (dx, dy) in enumerate(((-60, -250), (0, -300), (60, -240), (-30, -200), (40, -190))):
            shape(ctx, [(140, y - 110), (140 + dx * 0.5 - 18, y - 110 + dy * 0.6), (140 + dx, y - 110 + dy), (140 + dx * 0.5 + 18, y - 110 + dy * 0.6)],
                  hexc('4f7a45'), 3, 3140 + k)

def desk(ctx, x0, x1, y, seed=3200, col=hexc('8a6446')):
    shape(ctx, rect(x0, y, x1, y + 40), col, 5, seed)
    shape(ctx, rect(x0 + 20, y + 40, x1 - 20, y + 420), tint(col, (0, 0, 0), 0.15), 5, seed + 1)

def paper(ctx, x, y, w, h, rot=0, seed=3300, col=PAPER):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    shape(ctx, rect(-w / 2 + 12, -h / 2 + 14, w / 2 + 12, h / 2 + 14), (0, 0, 0), 0, 0, alpha=0.25)
    shape(ctx, rect(-w / 2, -h / 2, w / 2, h / 2), col, 5, seed)
    ctx.restore()

def star(ctx, x, y, r, col=hexc('f2d04a'), seed=3700, rot=0, alpha=1.0):
    pts = []
    for i in range(10):
        a = rot - math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    shape(ctx, pts, col, 3, seed, alpha=alpha)

def confetti(ctx, t, n=40, seed=5):
    import random
    rng = random.Random(seed)
    cols = [hexc('c0322a'), GOLD, hexc('2f9e4f'), hexc('2f5fa8'), hexc('e07a9a')]
    for i in range(n):
        x0 = rng.uniform(0, W); sp = rng.uniform(250, 450); ph = rng.uniform(0, 6)
        y = -50 + ((t * sp + rng.uniform(0, H)) % (H * 0.9))
        x = x0 + 30 * math.sin(t * 3 + ph)
        ctx.save(); ctx.translate(x, y); ctx.rotate(t * 4 + ph)
        shape(ctx, rect(-10, -5, 10, 5), cols[i % 5], 1.5, 5000 + i)
        ctx.restore()

def strike(ctx, x0, x1, y, u, seed):
    if u <= 0: return
    rough(ctx, [(x0, y), (lerp(x0, x1, min(u, 1)), y - 10)], 9, seed, hexc('c0322a'))

def reveal(s, u):
    return s[:int(len(s) * min(1, max(0, u)))]

def arm_to(hand, s=1.0, side=-1, bend=1.0):
    """Arm list with one hand placed at a local target; other arm down."""
    sh = (side * 68, 44); hx, hy = hand
    mx, my = (sh[0] + hx) / 2, (sh[1] + hy) / 2
    dx, dy = hx - sh[0], hy - sh[1]; L = math.hypot(dx, dy) + 1e-6
    px, py = -dy / L, dx / L
    if py < 0: px, py = -px, -py
    el = (mx + px * 40 * bend, my + py * 40 * bend)
    other = ((-side * 68, 44), (-side * 90, 128), (-side * 86, 206))
    a = (sh, el, (hx, hy))
    return [a, other] if side < 0 else [other, a]

# ---------------- runner ----------------
def run(SHOTS):
    def timeline():
        out = []
        for i, (li, fn) in enumerate(SHOTS):
            st = 0.0 if i == 0 else LT[li][0] - 0.18
            en = END if i == len(SHOTS) - 1 else LT[SHOTS[i + 1][0]][0] - 0.18
            out.append((st, en, fn))
        return out
    TL = timeline()
    if len(sys.argv) > 1 and sys.argv[1] == '--tl':
        for a, b, fn in TL: print(f'{a:6.2f} {b:6.2f} {fn.__name__}')
        return TL
    rng_mode = len(sys.argv) > 1 and sys.argv[1] == '--range'
    only = [] if rng_mode else [float(a) for a in sys.argv[1:]]
    grains = grain_layers()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    NF = int(round(END * 24)); ff = None
    if not only:
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                               '-r', '24', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                               '-pix_fmt', 'yuv420p', sys.argv[4] if rng_mode else 'video.mp4'], stdin=subprocess.PIPE)
    frames = [min(NF - 1, int(x * 24)) for x in only] if only else (range(int(sys.argv[2]), min(NF, int(sys.argv[3]))) if rng_mode else range(NF))
    for f in frames:
        t = f / 24; K.BOIL = f // 2
        ctx = cairo.Context(surf)
        ctx.set_operator(cairo.OPERATOR_SOURCE); ctx.set_source_rgb(0, 0, 0); ctx.paint(); ctx.set_operator(cairo.OPERATOR_OVER); ctx.new_path()
        for a, b, fn in TL:
            if a <= t < b: ctx.save(); fn(ctx, t - a, b - a, Sc(a)); ctx.restore(); break
        ctx.set_source_surface(grains[K.BOIL % 4], 0, 0); ctx.paint(); vignette(ctx, 0.35)
        for (st, en), s in zip(LT, LINES):
            if st - 0.05 <= t < en + 0.25: caption(ctx, s); break
        surf.flush()
        if ff: ff.stdin.write(bytes(surf.get_data()))
        else: surf.write_to_png(f'test_{f:05d}.png')
    if ff: ff.stdin.close(); ff.wait()
    return TL

def timeline_of(SHOTS):
    out = []
    for i, (li, fn) in enumerate(SHOTS):
        st = 0.0 if i == 0 else LT[li][0] - 0.18
        en = END if i == len(SHOTS) - 1 else LT[SHOTS[i + 1][0]][0] - 0.18
        out.append((st, en, fn.__name__))
    return out

# ---------------- seamless loop mix ----------------
def render_loop(mix, vo_path, out_path):
    """Like sfxkit.Mix.render, but no fade-out: anything past END wraps onto the start so the loop is seamless."""
    import sfxkit as A
    n = int(round(END * A.SR))
    def wrap(buf):
        o = buf[:n].copy(); rest = buf[n:]
        k = 0
        while len(rest) > 0:
            m = min(len(rest), n); o[:m] += rest[:m]; rest = rest[m:]
        return o
    M = wrap(mix.M); S = wrap(mix.S)
    vo, sr = sf.read(vo_path)
    if vo.ndim > 1: vo = vo.mean(1)
    vo = A.hp(vo, 60); vo = A.norm(vo) * A.db(-2.5)
    V = np.zeros(n); V[:min(n, len(vo))] = vo[:n]
    e = A.lp(np.abs(np.concatenate([V[-4800:], V])), 6, 1)[4800:]; e = e / (e.max() + 1e-9)
    duck = 1 - 0.55 * np.clip(e * 4, 0, 1)
    out = M * duck[:, None] * A.db(-2) + S * (1 - 0.3 * np.clip(e * 4, 0, 1))[:, None] + V[:, None]
    out = np.tanh(out * 1.05) / np.tanh(1.05); out = out / np.max(np.abs(out)) * A.db(-1)
    sf.write(out_path, out, A.SR, subtype='PCM_24')

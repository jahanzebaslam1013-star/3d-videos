"""Template: vertical stickman POV short. Copy to <project>/short.py and edit SCENES."""
import sys, json, math, subprocess
import cairo
sys.path.insert(0, '.')
import stickkit as K
from stickkit import *
K.W, K.H = 1080, 1920          # set BEFORE grain_layers()
W, H = K.W, K.H
LINES = [l.strip() for l in open('script.txt') if l.strip()]
LT = json.load(open('lt.json'))            # [(start,end)] per line, from sfxkit.align_lines/add_pauses
END = LT[-1][1] + 2.0

class Sc:                                  # local-time helpers inside a shot
    def __init__(self, t0): self.t0 = t0
    def L(self, i): return (LT[i][0] - self.t0, LT[i][1] - self.t0)
    def at(self, i, sub):                  # local time when word `sub` is spoken in line i
        k = LINES[i].find(sub); f = max(k, 0) / max(len(LINES[i]), 1); s, e = self.L(i); return s + (e - s) * f

FLOOR = 1450                               # standing feet line for full-body shots
def stand(s): return FLOOR - 334 * s       # y for a standing character of scale s

# ---------- shots: fn(ctx, t_local, duration, S) ----------
def s_hook(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('1c2124')); ctx.paint(); ctx.new_path()
    hero(ctx, 540, stand(1.3), 1.3, expr='shock' if t > 1.2 else 'neutral')
    rec_frame(ctx, 170, 760, 910, 1500, t)
    glow_text(ctx, 'POV:', 540, 260, 120, 'Bebas Neue', (1, 1, 1), None, pop=ease_out_back((t - 0.1) / 0.3))
    glow_text(ctx, 'TITLE HERE', 540, 450, 160, 'Creepster', hexc('b3121e'), (0.7, 0.05, 0.08), pop=ease_out_back((t - 0.35) / 0.3))

def s_end(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('111518')); ctx.paint(); ctx.new_path()
    radial(ctx, 540, 900, 900, (0.8, 0.06, 0.04), 0.3)
    hero(ctx, 540, 1350, 3.4, expr='sad', legs=None, tear=(t - 1.0) / 1.5 if t > 1.0 else None)
    if t > d - 1.2: dark(ctx, min(1, (t - (d - 1.2)) / 1.0), (0, 0, 0))

SHOTS = [(0, s_hook), (len(LINES) - 1, s_end)]   # (first line index, fn) — add one shot per 1-3 lines

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

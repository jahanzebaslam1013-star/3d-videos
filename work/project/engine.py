"""engine — generic section renderer for Urdu Doodle POV long-form (16:9).
A section file defines: PART (json with first/lt/dur), SHOTS = [(line_idx | ('t', sec), fn)], END, then calls engine.run(...).
Scene fn signature: fn(ctx, t_local, duration, S) where S.L(i) -> (start, end) of LOCAL line i relative to shot start,
S.F(i, f) -> time at fraction f through line i."""
import sys, json, subprocess
import cairo
import pk, stickkit as K
from pk import W, H, FPS

class Sc:
    def __init__(self, LT, t0): self.LT = LT; self.t0 = t0
    def L(self, i): return (self.LT[i][0] - self.t0, self.LT[i][1] - self.t0)
    def F(self, i, f):
        s, e = self.L(i); return s + (e - s) * f

def load_part(path):
    j = json.load(open(path)); return j['lt'], j['dur'], j['first']

def timeline(SHOTS, LT, END, lead=0.18):
    def st(k):
        if isinstance(k, tuple): return k[1]
        return 0.0 if k == 0 else LT[k][0] - lead
    out = []
    for i, (k, fn) in enumerate(SHOTS):
        a = st(k); b = END if i == len(SHOTS) - 1 else st(SHOTS[i + 1][0])
        out.append((a, b, fn))
    return out

def run(SHOTS, LT, END, overlay=None, argv=None):
    """argv: ['--range', f0, f1, out.mp4]  or  [t1, t2, ...] (writes test_<t>.png)"""
    argv = argv if argv is not None else sys.argv[1:]
    rng_mode = bool(argv) and argv[0] == '--range'
    TL = timeline(SHOTS, LT, END)
    grains = K.grain_layers()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    NF = int(END * FPS); ff = None
    if rng_mode:
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                               '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                               '-pix_fmt', 'yuv420p', argv[3]], stdin=subprocess.PIPE)
        frames = range(int(argv[1]), min(NF, int(argv[2])))
    else:
        frames = [int(float(x) * FPS) for x in argv]
    for f in frames:
        tt = f / FPS; K.BOIL = f // 2
        ctx = cairo.Context(surf)
        ctx.set_operator(cairo.OPERATOR_SOURCE); ctx.set_source_rgb(0, 0, 0); ctx.paint(); ctx.set_operator(cairo.OPERATOR_OVER)
        for a, b, fn in TL:
            if a <= tt < b:
                ctx.save(); fn(ctx, tt - a, b - a, Sc(LT, a)); ctx.restore(); break
        ctx.new_path()
        ctx.set_source_surface(grains[K.BOIL % 4], 0, 0); ctx.paint()
        K.vignette(ctx, 0.35)
        if overlay: overlay(ctx, tt)
        surf.flush()
        if ff: ff.stdin.write(bytes(surf.get_data()))
        else: surf.write_to_png(f'test_{tt:06.2f}.png')
    if ff: ff.stdin.close(); ff.wait()

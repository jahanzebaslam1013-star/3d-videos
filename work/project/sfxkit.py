import math, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve, resample_poly
SR = 48000
rng = np.random.default_rng(11)
def t_(d): return np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def db(x): return 10 ** (x / 20)
def norm(x): return x / (np.max(np.abs(x)) + 1e-9)
def env(n, a, r):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    nr = min(n, max(1, int(r * SR))); e[-nr:] *= np.linspace(1, 0, nr); return e
def mix(*xs):
    n = max(len(x) for x in xs); o = np.zeros(n)
    for x in xs: o[:len(x)] += x
    return o
_IR = lp(rng.standard_normal(int(1.8 * SR)) * np.exp(-np.arange(int(1.8 * SR)) / SR * 3.5), 5000)
def verb(x, m=0.3):
    y = np.concatenate([x, np.zeros(len(_IR))]); w = fftconvolve(y, _IR)[:len(y)]
    return y * (1 - m) + norm(w) * np.max(np.abs(x)) * m
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def tone(f, d, dec=0, a=0.005, r=0.03):
    tt = t_(d); return np.sin(2 * np.pi * f * tt) * np.exp(-tt * dec) * env(len(tt), a, r)
def boom(d, f0, f1, dec):
    tt = t_(d); f = f1 + (f0 - f1) * np.exp(-tt * 6)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * dec))
def nh(d, lo, hi, dec): return norm(bp(rng.standard_normal(int(d * SR)), lo, hi) * np.exp(-t_(d) * dec))
def whoosh(d, rev=False):
    n = int(d * SR); x = rng.standard_normal(n); o = np.zeros(n); seg = 1200
    for i in range(0, n, seg):
        f = 300 + 3000 * (i / n); o[i:i + seg] = bp(x[i:i + seg], f, f * 2.2, 1)
    e = np.sin(np.linspace(0, np.pi, n)) ** 2 if not rev else np.linspace(0, 1, n) ** 3
    return norm(lp(o, 6000) * e)
def pluck(f, d=0.5, bright=1.0):
    tt = t_(d)
    x = sum(np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * (6 + k * 3 / bright)) / k for k in range(1, 7))
    return x * env(len(tt), 0.002, 0.05)
def pad(freqs, d, cutoff=1400, det=0.25):
    tt = t_(d); x = np.zeros(len(tt))
    for f in freqs:
        for dd in (-det, 0, det):
            ph = 2 * np.pi * (f + dd) * tt; x += sum(np.sin(k * ph) / k for k in range(1, 8))
    return lp(x, cutoff) * env(len(tt), min(0.8, d / 3), min(1.0, d / 3))
def sfx_hit(): return norm(verb(mix(boom(1.4, 80, 35, 2.5), 0.4 * nh(0.5, 150, 1500, 6)), .4))
def sfx_stamp(): return norm(verb(mix(boom(0.7, 110, 50, 10), 0.7 * nh(0.2, 300, 3000, 25)), .2))
def sfx_pop(): return mix(whoosh(0.15), tone(900, 0.08, 25))
def sfx_ding(): return norm(verb(sum(tone(f, 1.4, k) for f, k in ((1318, 3), (1661, 3.5), (1976, 4))), .4))
def sfx_tick(): return mix(nh(0.03, 2500, 7000, 200), 0.4 * tone(2800, 0.02, 100))
def sfx_heartbeat(): return mix(boom(0.22, 60, 40, 20), np.concatenate([np.zeros(int(.15 * SR)), 0.7 * boom(0.22, 55, 38, 20)]))
def sfx_tape_stop():
    tt = t_(0.7); f = mtof(62) * np.exp(-tt * 4)
    return norm(lp(np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * rng.standard_normal(len(tt)), 2000)) * env(len(tt), .005, .2)
def sfx_power_down():
    tt = t_(1.6); f = 220 * np.exp(-tt * 2.2) + 25
    return norm(verb(lp(sum(np.sin(k * 2 * np.pi * np.cumsum(f) / SR) / k for k in range(1, 6)) * np.exp(-tt * 1.2), 1500), .4))
class Mix:
    def __init__(self, dur):
        self.N = int(dur * SR) + SR; self.dur = dur
        self.M = np.zeros((self.N, 2)); self.S = np.zeros((self.N, 2))
    def _put(self, buf, sig, at, g, pan):
        i = int(max(at, 0) * SR); sig = np.asarray(sig) * db(g); n = min(len(sig), self.N - i)
        if n <= 0: return
        gl = math.cos((pan + 1) * math.pi / 4) * 1.414; gr = math.sin((pan + 1) * math.pi / 4) * 1.414
        buf[i:i + n, 0] += sig[:n] * gl; buf[i:i + n, 1] += sig[:n] * gr
    def music(self, sig, at, g=-20, pan=0.0): self._put(self.M, sig, at, g, pan)
    def sfx(self, sig, at, g=-16, pan=0.0): self._put(self.S, sig, at, g, pan)
    def render(self, vo_path, out_path, fade=1.0):
        vo, sr = sf.read(vo_path)
        if vo.ndim > 1: vo = vo.mean(1)
        if sr != SR: vo = resample_poly(vo, SR, sr)
        vo = hp(vo, 60); vo = norm(vo) * db(-2.5)
        V = np.zeros(self.N); n = min(len(vo), self.N); V[:n] = vo[:n]
        e = lp(np.abs(V), 6, 1); e = e / (e.max() + 1e-9)
        duck = 1 - 0.55 * np.clip(e * 4, 0, 1)
        out = self.M * duck[:, None] * db(-2) + self.S * (1 - 0.3 * np.clip(e * 4, 0, 1))[:, None] + V[:, None]
        f = np.interp(np.arange(self.N) / SR, [0, self.dur - fade, self.dur], [1, 1, 0]); out *= f[:, None]
        out = np.tanh(out * 1.05) / np.tanh(1.05); out = out / np.max(np.abs(out)) * db(-1)
        sf.write(out_path, out[:int(self.dur * SR)], SR)

"""shared ambience / music helpers for section mixes (on top of sfxkit)"""
import numpy as np, sfxkit as A
SR = A.SR

def bed(dur, lo, hi, fade=1.0, lfo=0.0, lfo_rate=0.2):
    n = int(dur * SR); x = A.bp(A.rng.standard_normal(n), lo, hi)
    if lfo: x *= (1 - lfo) + lfo * np.sin(np.arange(n) / SR * 2 * np.pi * lfo_rate) ** 2
    return A.norm(x) * A.env(n, min(fade, dur / 3), min(fade, dur / 3))

def waves(dur, fade=1.0):
    n = int(dur * SR); w = A.lp(A.rng.standard_normal(n), 500)
    w *= 0.6 + 0.4 * np.sin(np.arange(n) / SR * 2 * np.pi / 5.5) ** 2
    return A.norm(w) * A.env(n, min(fade, dur / 3), min(fade, dur / 3))

def crickets(dur, fade=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    x = A.bp(A.rng.standard_normal(n), 4200, 5200) * (np.sin(2 * np.pi * 14 * tt) > 0.3) * (0.5 + 0.5 * (np.sin(2 * np.pi * 0.6 * tt) > 0))
    return A.norm(x) * A.env(n, min(fade, dur / 3), min(fade, dur / 3))

def rain(dur, fade=1.0):
    n = int(dur * SR)
    return A.norm(A.hp(A.rng.standard_normal(n), 2500) * (0.7 + 0.3 * A.lp(A.rng.standard_normal(n), 3) * 10)) * A.env(n, fade, fade)

def ring():
    tt = A.t_(0.4); x = (np.sin(2 * np.pi * 440 * tt) + np.sin(2 * np.pi * 480 * tt)) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 20 * tt)))
    one = x * A.env(len(tt), .01, .03)
    return np.concatenate([one, np.zeros(int(0.2 * SR)), one])

def beep(f=1000, d=0.12): return A.tone(f, d, 0) * 0.8

def shutter(): return A.mix(A.nh(0.04, 2000, 8000, 120), np.concatenate([np.zeros(int(0.07 * SR)), A.nh(0.05, 1500, 6000, 90)]))

def crowd(dur, fade=0.5):
    n = int(dur * SR); x = np.zeros(n)
    for k in range(6):
        f0 = 180 + 60 * k
        x += A.bp(A.rng.standard_normal(n), f0, f0 * 3) * (0.5 + 0.5 * np.sin(np.arange(n) / SR * (3 + k) + k))
    return A.norm(x) * A.env(n, fade, fade)

def horn(d=2.5):
    tt = A.t_(d); x = sum(np.sin(2 * np.pi * f * tt) / (i + 1) for i, f in enumerate((98, 196, 294, 392)))
    return A.norm(A.lp(x, 900) * A.env(len(tt), 0.3, 0.8))

def engine(dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    return A.norm(A.lp(A.rng.standard_normal(n), 180) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt))) * A.env(n, 0.4, 0.4)

def plucks(m, notes, t0, step, g=-22, dur=1.6, until=None, verb=.5):
    t = t0
    for k in range(10000):
        if until is not None and t >= until: break
        if until is None and k >= len(notes): break
        m.music(A.verb(A.pluck(A.mtof(notes[k % len(notes)]), dur), verb), t, g); t += step

def pad(m, chord, t0, t1, g=-18, cut=1000):
    if t1 - t0 > 0.3: m.music(A.norm(A.pad([A.mtof(c) for c in chord], t1 - t0, cut)), t0, g)

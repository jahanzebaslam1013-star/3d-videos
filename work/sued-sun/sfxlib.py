"""zkit procedural audio library: music beds by mood + ~30 synthesized sound effects.
Everything is generated with numpy/scipy at 44.1 kHz, mono float arrays."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
SR = 44100
rng = np.random.default_rng(4)

# ---------- basics ----------
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def env(n, a, d): t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def noise(d): return rng.standard_normal(int(d * SR))
def midi(m): return 440 * 2 ** ((m - 69) / 12)
def put(buf, x, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf) or i < 0: return
    x = x[: len(buf) - i]; buf[i:i + len(x)] += x * g
def reverb(x, secs=1.6, mix=0.3):
    n = int(secs * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 4.5 / secs)
    ir = lp(ir, 6000); w = fftconvolve(x, ir)[:len(x)]
    w /= (np.max(np.abs(w)) + 1e-9); w *= np.max(np.abs(x)) + 1e-9
    return x * (1 - mix) + w * mix
def fades(x, a=0.02, b=0.05):
    n = len(x); t = np.arange(n) / SR; return x * np.minimum(1, t / max(a, 1e-4)) * np.minimum(1, (n / SR - t) / max(b, 1e-4))

# ---------- instruments ----------
def pluck(f, dur=0.9, g=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*f*4*t)*np.exp(-t*18) + 0.15*np.sin(2*np.pi*f*2*t)
    return x * env(n, 0.003, 0.28) * g
def pad(freqs, dur, g=1.0):
    n = int(dur * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for det in (-0.12, 0.0, 0.13):
            ph = rng.random() * 6.28
            x += np.sin(2*np.pi*(f+det)*t + ph) + 0.25*np.sin(2*np.pi*2*(f+det)*t + ph)
    a = np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 0.6)
    return lp(x, 1800) * a * g / max(1, len(freqs))
def bass(f, dur, g=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2*np.pi*f*t) + 0.2*np.sin(2*np.pi*2*f*t)) * env(n, 0.01, 0.5) * g

# ---------- music beds ----------
# mood -> (bpm, chord progression [(bass_midi, [chord midis])], arp density, pluck gain, pad gain)
MOODS = {
 'playful': (112, [(48,[60,64,67]),(53,[65,69,72]),(55,[67,71,74]),(48,[60,64,67])], 2, .32, .25),
 'mystery': (96,  [(57,[57,60,64]),(53,[53,57,60]),(48,[55,60,64]),(55,[55,59,62])], 2, .30, .55),
 'tense':   (120, [(45,[57,60,64]),(45,[57,60,63]),(46,[58,62,65]),(44,[56,60,63])], 2, .30, .40),
 'sad':     (72,  [(53,[57,60,65]),(48,[55,60,64]),(50,[57,62,65]),(45,[57,60,64])], 1, .30, .75),
 'epic':    (90,  [(45,[57,64,69]),(41,[53,60,65]),(48,[55,60,67]),(43,[55,62,67])], 1, .22, .90),
 'space':   (70,  [(45,[57,64,69,72]),(41,[53,60,65,69])], 0, .20, .90),
 'dark':    (60,  [(33,[45,52]),(33,[45,51])], 0, 0, 1.0),
}
def music_section(mood, dur):
    bpm, prog, dens, pg, padg = MOODS[mood]; beat = 60 / bpm; out = np.zeros(int(dur * SR) + SR)
    t = 0.0; ci = 0
    while t < dur:
        root, ch = prog[ci % len(prog)]; bar = beat * 4; seg = min(bar, dur - t)
        if padg: put(out, pad([midi(m) for m in ch], seg + 0.5), t, padg)
        if mood == 'dark':
            put(out, lp(pad([midi(root), midi(root + 7)], seg + 0.5), 500), t, 1.2)
        else:
            put(out, bass(midi(root - 12), beat * 1.8), t, 0.9); put(out, bass(midi(root - 12), beat * 1.8), t + beat * 2, 0.7)
        if dens:
            arp = [ch[0]+12, ch[1]+12, ch[2]+12, ch[1]+12, ch[0]+24, ch[2]+12, ch[1]+12, ch[2]+12]
            step = beat / dens
            for k in range(int(4 * dens)):
                tt = t + k * step
                if tt < dur - 0.05: put(out, pluck(midi(arp[k % 8]), 0.6), tt, pg if k % 2 == 0 else pg * .7)
        t += bar; ci += 1
    return out[:int(dur * SR)]
def music_bed(sections, total):
    """sections: [(start_sec, mood), ...] sorted. Crossfades 0.6 s between sections."""
    out = np.zeros(int(total * SR)); xf = 0.6
    for i, (st, mood) in enumerate(sections):
        en = sections[i + 1][0] if i + 1 < len(sections) else total
        seg = music_section(mood, en - st + xf)
        n = len(seg); t = np.arange(n) / SR
        seg *= np.minimum(1, t / xf) if i else 1; seg *= np.minimum(1, (n / SR - t) / xf)
        put(out, seg, max(0, st - (xf / 2 if i else 0)))
    return reverb(out, 1.3, 0.22)

# ---------- SFX (each returns a mono array; durations in seconds) ----------
def whoosh(d=0.35, lo=300, hi=3000, g=0.5):
    n = int(d * SR); x = noise(d + 0.1); out = np.zeros(n); blk = 512
    for i in range(0, n, blk):
        f = lo * (hi / lo) ** (i / n); seg = x[max(0, i - 2048):i + blk]
        y = bp(seg, max(50, f * 0.6), min(SR / 2 - 100, f * 1.4))[-min(blk, n - i):]; out[i:i + len(y)] = y
    return out * np.sin(np.pi * np.arange(n) / n) ** 2 * g
def whoosh_down(d=0.3, g=0.5): return whoosh(d, 2000, 300, g)
def thud(g=0.8, f=70):
    d = 0.5; n = int(d*SR); t = np.arange(n)/SR; ff = f + 90*np.exp(-t*25)
    return (np.sin(2*np.pi*np.cumsum(ff)/SR)*np.exp(-t*7) + lp(noise(d), 400)*np.exp(-t*25)*0.5) * g
def boom(g=1.0): return lp(thud(1.0, 38), 300) * g + reverb(thud(0.5, 50), 2.0, 0.6) * g * .5
def pop(g=0.5):
    d = 0.12; n = int(d*SR); t = np.arange(n)/SR; f = 900*np.exp(-t*30) + 200
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*40) * g
def ding(f=1320, g=0.4):
    d = 1.0; n = int(d*SR); t = np.arange(n)/SR
    x = sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t*k) for a, r, k in [(1, 1, 5), (.5, 2.76, 9), (.3, 5.4, 14)])
    return x * np.minimum(1, t/0.002) * g
def shimmer(g=0.3):
    out = np.zeros(int(0.8*SR))
    for k in range(7): put(out, ding(2000 + k*260, 1.0)[:int(0.5*SR)], k*0.06, 0.3)
    return out * g * np.linspace(1, 0.3, len(out))
def metal(f0=420, d=1.2, g=0.5, decay=4):
    n = int(d*SR); t = np.arange(n)/SR; ratios = [1, 1.47, 2.09, 2.56, 3.34, 4.1, 5.2]
    x = sum(np.sin(2*np.pi*f0*r*t + rng.random()*6)*np.exp(-t*decay*(1+0.4*i))/(1+0.3*i) for i, r in enumerate(ratios))
    return (x + hp(noise(d), 2000)*np.exp(-t*60)*0.8) * g
def clang(g=0.5):
    x = reverb(metal(180, 2.0, 0.5, 2.5), 1.8, 0.45); put(x, thud(0.6, 50), 0); return x * g
def clink(g=0.4): return metal(1150, 0.7, 0.3, 7) * g
def sizzle(d=1.0, g=0.5, grow=False):
    x = hp(noise(d), 2500) * 0.4; cr = np.zeros(len(x)); idx = rng.integers(0, len(x), int(d*260)); cr[idx] = rng.standard_normal(len(idx))*3
    x += hp(cr, 1500); t = np.arange(len(x))/SR; e = np.minimum(1, t/0.15) * np.minimum(1, (d - t)/0.3)
    if grow: e *= 0.4 + 0.6*t/d
    return x * e * g
def sting_down(g=0.5):  # comedic "wah-wah"
    d = 0.9; n = int(d*SR); t = np.arange(n)/SR; f = midi(62) * 2 ** (-t*4/12/d*3); ph = 2*np.pi*np.cumsum(f)/SR
    x = np.sign(np.sin(ph))*0.3 + np.sin(ph) + 0.5*np.sin(2*ph)
    return lp(x, 1500) * (0.6 + 0.4*np.sin(2*np.pi*6*t)) * np.minimum(1, t/0.02) * np.minimum(1, (d-t)/0.2) * g
def sting_up(g=0.5): return sting_down(g)[::-1] * 0.8
def phone(g=0.3):
    out = np.zeros(int(0.6*SR))
    for k, (a, b) in enumerate([(697, 1209), (770, 1336), (852, 1477)]):
        n = int(0.12*SR); t = np.arange(n)/SR; put(out, (np.sin(2*np.pi*a*t) + np.sin(2*np.pi*b*t))*np.minimum(1, np.minimum(t, 0.12-t)/0.005), k*0.17)
    return out * g
def siren(d=2.0, g=0.35):
    n = int(d*SR); t = np.arange(n)/SR; f = 950 + 350*np.sin(2*np.pi*1.6*t); ph = 2*np.pi*np.cumsum(f)/SR
    return lp(np.sin(ph) + 0.4*np.sin(2*ph) + 0.2*np.sin(3*ph), 3500) * np.minimum(1, t/0.15) * np.minimum(1, (d - t)/0.5) * g
def powerdown(g=0.5):
    d = 1.1; n = int(d*SR); t = np.arange(n)/SR; f = 420*np.exp(-t*2.6) + 30; ph = 2*np.pi*np.cumsum(f)/SR
    return lp(2*((ph/(2*np.pi)) % 1) - 1, 1200) * np.minimum(1, t/0.01) * np.minimum(1, (d-t)/0.3) * g
def powerup(g=0.5): return powerdown(g)[::-1]
def crickets(d=2.0, g=0.08):
    n = int(d*SR); t = np.arange(n)/SR; am = (np.sin(2*np.pi*30*t) > 0.3) * (np.sin(2*np.pi*1.4*t) > 0.0)
    return np.sin(2*np.pi*4300*t)*am*np.minimum(1, t/0.4)*np.minimum(1, (d-t)/0.4)*g
def waves(d=6.0, g=0.25):
    x = lp(noise(d), 700, 2); t = np.arange(len(x))/SR
    return x * (0.45 + 0.55*(0.5 + 0.5*np.sin(2*np.pi*0.22*t - 1.2))**2) * np.minimum(1, t/0.5) * np.minimum(1, (d-t)/0.5) * g
def gull(g=0.2):
    out = []
    for k in range(3):
        d = 0.16 + 0.05*k; n = int(d*SR); t = np.arange(n)/SR; f = 1800 + 900*np.sin(np.pi*t/d) - 500*t/d; ph = 2*np.pi*np.cumsum(f)/SR
        out += [(np.sin(ph) + 0.3*np.sin(2*ph)) * np.sin(np.pi*t/d)**1.5, np.zeros(int(0.06*SR))]
    return bp(np.concatenate(out), 900, 5000) * g
def wind(d=2.0, g=0.3):
    x = bp(noise(d), 200, 1400); t = np.arange(len(x))/SR
    return x*(0.6 + 0.4*np.sin(2*np.pi*0.7*t))*np.minimum(1, t/0.2)*np.minimum(1, (d-t)/0.2)*g
def rise(d=1.4, g=0.3):
    n = int(d*SR); t = np.arange(n)/SR; f = 300*2**(t/d*2)
    return (np.sin(2*np.pi*np.cumsum(f)/SR) + 0.5*np.sin(2*np.pi*np.cumsum(f*1.5)/SR)) * np.sin(np.pi*t/d) * g
def whistle_down(d=1.2, g=0.3):
    n = int(d*SR); t = np.arange(n)/SR; f = 1900*np.exp(-t/d*1.5) + 300
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.minimum(1, t/0.1) * g
def plop(g=0.3):
    d = 0.09; n = int(d*SR); t = np.arange(n)/SR; f = 500 + 1400*t/d
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*45)*g
def bubbles(d=1.2, g=0.3):
    out = np.zeros(int(d*SR))
    for i in range(int(d*14)): put(out, plop(1.0), rng.random()*d*0.95, 0.5 + rng.random()*0.5)
    return out * g
def moo(g=0.5):
    d = 1.1; n = int(d*SR); t = np.arange(n)/SR; f = 150 - 40*t/d + 8*np.sin(2*np.pi*5*t); ph = 2*np.pi*np.cumsum(f)/SR
    x = sum(np.sin(h*ph)/h for h in range(1, 25)); x = bp(x, 300, 900)*0.6 + bp(x, 120, 400)
    return x*np.minimum(1, t/0.12)*np.minimum(1, (d-t)/0.25)*g
def horn(g=0.4):
    d = 0.5; n = int(d*SR); t = np.arange(n)/SR; x = np.zeros(n)
    for f in (420, 530): ph = 2*np.pi*f*t; x += np.sign(np.sin(ph))*.5 + np.sin(ph)
    return lp(x, 2500)*np.minimum(1, t/0.01)*np.minimum(1, (d-t)/0.05)*g
def rustle(g=0.3):
    d = 0.35; x = hp(noise(d), 1500); am = np.convolve((rng.random(len(x)) > 0.6)*1.0, np.ones(300)/300, 'same')
    return x*am*np.sin(np.pi*np.arange(len(x))/len(x))*g
def engine(d=2.0, g=0.3):
    t = np.arange(int(d*SR))/SR; f = 55 + 10*np.sin(2*np.pi*0.5*t)
    return lp(np.sign(np.sin(2*np.pi*np.cumsum(f)/SR)), 400) * np.minimum(1, t/0.3) * np.minimum(1, (d-t)/0.4) * g
def click(g=0.3): return hp(noise(0.02), 3000) * np.exp(-np.arange(int(0.02*SR))/SR*300) * g
def tick_tock(d=2.0, g=0.3):
    out = np.zeros(int(d*SR))
    for k in range(int(d*2)): put(out, bp(click(1.0), 1500 if k % 2 else 900, 5000), k*0.5)
    return out * g
def heartbeat(d=3.0, g=0.6):
    out = np.zeros(int(d*SR))
    for k in range(int(d/0.85)): put(out, thud(0.9, 50), k*0.85); put(out, thud(0.6, 55), k*0.85 + 0.22)
    return lp(out, 200) * g
def crowd_gasp(g=0.4):
    d = 0.9; x = bp(noise(d), 400, 2500); t = np.arange(len(x))/SR
    return x * np.minimum(1, t/0.05) * np.exp(-t*3) * g
def glitch(g=0.4):
    out = np.zeros(int(0.4*SR))
    for k in range(8): put(out, np.sign(np.sin(2*np.pi*(200 + rng.random()*2000)*np.arange(int(0.03*SR))/SR)), k*0.045, 0.5)
    return out * g

SFX = {k: v for k, v in globals().items() if callable(v) and k not in (
    'bp', 'lp', 'hp', 'env', 'noise', 'midi', 'put', 'reverb', 'fades', 'pluck', 'pad', 'bass', 'music_section', 'music_bed', 'butter', 'sosfilt', 'fftconvolve')}

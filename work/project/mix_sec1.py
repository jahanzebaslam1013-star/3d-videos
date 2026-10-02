"""Full Section 1 mix (0 - 123.09 s). 0-33 s = the approved test cues unchanged; the rest extends them."""
import json, numpy as np, sfxkit as A
LT = json.load(open('lt1.json'))
L = lambda i: LT[i][0]
F = lambda i, f: LT[i][0] + (LT[i][1] - LT[i][0]) * f
S = lambda i: LT[i][0] - 0.18          # shot start (engine lead)
DUR = 121.39 + 1.7
m = A.Mix(DUR)

# ===================== 0 - 33 s : approved test (unchanged) =====================
m.music(A.norm(A.pad([A.mtof(38), A.mtof(45), A.mtof(50)], 32.0, 700)), 0, -16)
m.music(A.norm(A.pad([A.mtof(62), A.mtof(65)], 20, 1800, 0.4)), 10.5, -26)
for k, n in enumerate([62, 65, 69, 67, 62, 60, 62, 65, 69, 72, 70, 69]):
    m.music(A.verb(A.pluck(A.mtof(n), 1.6), .5), 2.5 + k * 2.4, -22)
t = 19.0
while t < 31.5: m.music(A.boom(0.25, 70, 45, 16), t, -17); t += 1.0
m.music(A.norm(A.pad([A.mtof(74), A.mtof(75), A.mtof(80)], 4.0, 3000)), 28.0, -24)
n = int(33.5 * A.SR); w = A.lp(A.rng.standard_normal(n), 500)
w *= (0.6 + 0.4 * np.sin(np.arange(n) / A.SR * 2 * np.pi / 5.5) ** 2) * A.env(n, 0.01, 1.2)
m.sfx(A.norm(w), 0, -20); m.sfx(A.norm(A.bp(A.rng.standard_normal(n), 900, 3500)) * 0.4 * A.env(n, 0.01, 1.2), 0, -30)
eng_end = LT[2][0] + 1.0; t = 0.2
while t < eng_end:
    m.sfx(A.boom(0.12, 90, 50, 30), t, -16 + 4 * (t > eng_end - 2)); t += 0.24 + 0.1 * max(0, t - eng_end + 2.5)
m.sfx(A.sfx_power_down(), eng_end - 0.2, -12)
m.sfx(A.sfx_tick(), 0.3, -14); m.sfx(A.sfx_pop(), 0.3, -16)
m.sfx(A.sfx_pop(), F(3, .28) - 0.17, -12); m.sfx(A.sfx_stamp(), F(3, .28), -12)
m.sfx(A.sfx_pop(), F(3, .55), -12)
m.sfx(A.sfx_stamp(), F(3, .85), -8)
m.sfx(A.whoosh(0.6), 18.9, -12)
m.sfx(A.sfx_pop(), F(4, .42), -12); m.sfx(A.sfx_pop(), F(4, .78), -12); m.sfx(A.sfx_ding(), F(4, .8), -22)
m.sfx(A.sfx_pop(), LT[5][0] + 0.1, -14)
m.sfx(A.sfx_heartbeat(), 30.4, -10); m.sfx(A.sfx_heartbeat(), 31.1, -10)
fr = LT[6][1] + 0.1
m.sfx(A.sfx_hit(), fr, -4); m.sfx(A.sfx_tape_stop(), fr - 0.05, -12)
m.sfx(A.sfx_stamp(), fr + 0.6, -8)

# ===================== 33 s - end : extension =====================
# rewind into "8 months earlier"
m.sfx(A.whoosh(1.0, rev=True), S(8) - 0.9, -10)
m.sfx(A.sfx_pop(), L(8) + 0.1, -12)

# --- village theme (warm, light): 37.5 -> 78 s ---
v0, v1 = S(8), S(16)
m.music(A.norm(A.pad([A.mtof(50), A.mtof(57), A.mtof(62)], v1 - v0 + 2, 1600)), v0, -20)
mel = [62, 66, 69, 66, 64, 62, 64, 66, 69, 71, 69, 66]
k = 0; t = v0 + 0.6
while t < v1 - 1.0:
    m.music(A.verb(A.pluck(A.mtof(mel[k % len(mel)]), 1.2, 1.4), .4), t, -23); k += 1; t += 1.2
nv = int((v1 - v0) * A.SR)                                   # soft daytime air + a few birds
m.sfx(A.norm(A.lp(A.rng.standard_normal(nv), 700)) * A.env(nv, 1.0, 1.5), v0, -30)
for b in np.arange(v0 + 1.3, S(12), 3.7):
    for j in range(3): m.sfx(A.tone(2600 + 400 * j, 0.06, 30), b + j * 0.09, -32, pan=0.5)

m.sfx(A.sfx_pop(), L(9) + 0.2, -12); m.sfx(A.sfx_pop(), F(9, .55), -15)
m.sfx(A.whoosh(0.4), S(10), -16)
m.sfx(A.sfx_stamp(), F(10, .62), -8)
for i in range(30): m.sfx(A.whoosh(0.18), S(11) + i / 9, -28 - (i % 3) * 2, pan=0.4)   # CVs flying
m.sfx(A.sfx_hit(), F(11, .68), -10); m.sfx(A.sfx_pop(), F(11, .68), -12)
t0 = F(12, .45)
for i in range(14): m.sfx(A.sfx_tick(), t0 + i / 6 + 0.3, -14, pan=0.3)            # bills landing
m.sfx(A.sfx_pop(), t0 + 0.4, -12)

# phone buzz
bz = L(13) + 1.0
for j in range(3):
    m.sfx(A.norm(A.tone(150, 0.45, 0) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 30 * A.t_(0.45))))), bz + j * 0.7, -12)
# Instagram post
m.sfx(A.whoosh(0.5), S(14), -14); m.sfx(A.sfx_ding(), L(14) + 0.3, -16)
m.sfx(A.sfx_pop(), F(15, 0.0), -12); m.sfx(A.sfx_pop(), F(15, .25), -12)

# --- longing / tension: stare -> split -> dhaba ---
m.music(A.norm(A.pad([A.mtof(50), A.mtof(53), A.mtof(57)], S(20) - S(16) + 1.5, 1200)), S(16) - 0.5, -18)
for k, nn in enumerate([69, 65, 62, 64, 65, 64, 62, 60, 62, 65, 64, 62]):
    if S(16) + 0.4 + k * 1.8 < S(20) - 0.5:
        m.music(A.verb(A.pluck(A.mtof(nn), 1.6), .5), S(16) + 0.4 + k * 1.8, -23)
m.sfx(A.whoosh(0.6), S(17) - 0.3, -12)
m.sfx(A.sfx_pop(), L(17) + 0.1, -12); m.sfx(A.sfx_pop(), L(17) + 0.5, -12)
m.sfx(A.whoosh(0.6), S(18) - 0.3, -12)
m.sfx(A.sfx_ding(), L(19) + 0.3, -16)                                              # gold glint
m.sfx(A.sfx_pop(), L(19) + 0.15, -14)

# --- the price: dark ---
m.sfx(A.sfx_pop(), L(20), -12)
m.music(A.norm(A.pad([A.mtof(38), A.mtof(41), A.mtof(45)], S(23) - F(21, .05) + 1.0, 800)), F(21, .05), -15)
m.sfx(A.sfx_hit(), F(21, .05), -5)
m.sfx(A.sfx_pop(), F(21, .35), -12)
m.sfx(A.sfx_stamp(), F(21, .62), -7)
m.sfx(A.sfx_hit(), S(22), -6); m.sfx(A.whoosh(0.5), S(22) - 0.3, -12)
for j in range(5): m.sfx(A.sfx_heartbeat(), S(22) + 0.8 + j * 0.75, -9)

# --- night courtyard: crickets + sad plucks, fade ---
n0 = S(23); nn_ = int((DUR - n0) * A.SR)
cr = A.bp(A.rng.standard_normal(nn_), 4200, 5200) * (np.sin(2 * np.pi * 14 * np.arange(nn_) / A.SR) > 0.3) \
     * (0.5 + 0.5 * (np.sin(2 * np.pi * 0.6 * np.arange(nn_) / A.SR) > 0))
m.sfx(A.norm(cr) * A.env(nn_, 0.8, 1.5), n0, -32, pan=-0.3)
m.music(A.norm(A.pad([A.mtof(45), A.mtof(52), A.mtof(57)], DUR - n0, 900)), n0, -20)
for k, nn in enumerate([69, 67, 65, 64, 62, 64]):
    m.music(A.verb(A.pluck(A.mtof(nn), 2.0), .6), n0 + 0.8 + k * 1.9, -22)
m.sfx(A.sfx_pop(), L(25) + 0.7, -14)
m.music(A.verb(A.pluck(A.mtof(50), 3.0), .7), L(25) + 1.4, -18)

m.render('vo1.wav', 'mix_sec1.wav', fade=1.4)
print('ok', DUR)

import json, numpy as np, sfxkit as A, mixlib as X
j = json.load(open('part2.json')); LT = j['lt']
L = lambda i: LT[i][0]
F = lambda i, f: LT[i][0] + (LT[i][1] - LT[i][0]) * f
S = lambda i: LT[i][0] - 0.18 if i else 0.0
DUR = j['dur'] + 0.6
m = A.Mix(DUR)

# ---- music ----
X.pad(m, [45, 52, 57], 0, S(2) + 0.5, -19, 900)                                   # night: sad
X.plucks(m, [69, 67, 65, 64, 62, 64], 0.6, 1.9, -22, 2.0)
X.pad(m, [50, 57, 62, 66], S(2), S(4) + 0.4, -21, 1500)                            # airport: bittersweet
X.plucks(m, [62, 66, 69, 66, 64, 62], S(2) + 0.3, 1.6, -24, 1.4)
X.pad(m, [50, 57, 62], S(4), S(7) + 0.3, -21, 1700)                                # journey: moving pulse
t = S(4)
while t < S(7): m.music(A.boom(0.2, 70, 50, 18), t, -22); t += 0.6
X.plucks(m, [62, 64, 66, 69, 71, 69, 66, 64], S(4) + 0.3, 0.6, -25, 0.8, until=S(7))
X.pad(m, [38, 41, 45], S(7), S(18) + 0.5, -16, 750)                                # Libya / warehouse: dark
X.plucks(m, [65, 64, 62, 60, 62, 57], S(13) + 0.5, 2.2, -24, 2.0, until=S(18))
X.pad(m, [38, 44, 50], S(18), DUR, -16, 800)                                       # tension
t = S(19)
while t < DUR: m.music(A.boom(0.25, 70, 45, 16), t, -16); t += 0.9

# ---- ambience ----
m.sfx(X.crickets(S(2)), 0, -32, pan=-0.3)
m.sfx(X.bed(S(4) - S(2), 200, 1200, 0.5), S(2), -32)                               # airport hall
m.sfx(X.bed(DUR - S(9), 60, 300, 1.0, 0.3, 0.1), S(9), -26)                        # warehouse room tone

# ---- cues ----
m.sfx(A.sfx_ding(), S(0) + 1.9, -14); m.sfx(A.sfx_pop(), 0.9, -14)
m.sfx(A.sfx_stamp(), F(1, .62), -7)
m.sfx(A.whoosh(0.6), S(2) - 0.3, -12)
m.sfx(A.norm(A.lp(A.rng.standard_normal(int(4.5 * A.SR)), 900)) * A.env(int(4.5 * A.SR), 1.5, 2), S(2) + 0.3, -20)   # jet pass
m.sfx(A.sfx_pop(), F(2, .55), -13)
m.sfx(A.whoosh(0.5), S(3) - 0.2, -13)
for f in (0.15, 0.35, 0.6): m.sfx(A.sfx_pop(), F(3, f), -13)
m.sfx(A.whoosh(0.7), S(4) - 0.3, -12)
for tt in (L(4) - 0.1 + 0.7, F(4, .45) + 0.7, F(5, .35) + 0.7, F(5, .75) + 0.7, L(7) + 0.8): m.sfx(A.sfx_pop(), tt, -13)
for tt in (F(4, .45), F(5, .35), F(5, .75), L(7) + 0.1): m.sfx(A.whoosh(0.9), tt, -18)
m.sfx(A.sfx_pop(), F(4, .3), -13); m.sfx(A.sfx_pop(), F(4, .65), -14); m.sfx(A.sfx_ding(), F(4, .6), -22)
for tt in (F(4, .45) + .9, F(5, .35) + .9, F(5, .75) + .9): m.sfx(A.sfx_pop(), tt, -15)
for tt in (F(6, .55), F(6, .72), F(6, .88)): m.sfx(A.sfx_pop(), tt, -12)
m.sfx(A.sfx_pop(), F(5, .6), -14)
m.sfx(A.sfx_hit(), L(7) + 0.2, -10)
m.sfx(A.sfx_stamp(), S(8) + 0.2, -8)
m.sfx(A.sfx_hit(), F(8, .55), -6); m.sfx(A.nh(0.4, 400, 4000, 10), F(8, .55), -10)
m.sfx(A.whoosh(0.6), F(8, .55) + 0.35, -12)
m.sfx(A.sfx_pop(), F(8, .55) + 0.65, -13)
for k in range(10): m.sfx(A.boom(0.1, 90, 60, 30), S(9) + 0.1 + k * 0.28, -22)                          # footsteps
m.sfx(A.sfx_pop(), F(9, .3), -13)
m.sfx(A.mix(A.sfx_hit(), A.nh(0.6, 200, 3000, 8)), F(9, .75), -3)                                        # shutter slam
for f in (0.05, 0.38, 0.7): m.sfx(A.sfx_stamp(), F(10, f), -11)
m.sfx(A.whoosh(0.35), F(11, .45), -9); m.sfx(A.sfx_pop(), F(11, .45) + 0.5, -13)
m.sfx(A.sfx_pop(), F(12, .1), -13); m.sfx(A.whoosh(0.5, rev=True), F(12, .65), -16); m.sfx(A.sfx_pop(), F(12, .65) + 0.2, -13)
m.sfx(A.sfx_pop(), F(13, .3), -13); m.sfx(A.sfx_pop(), F(13, .55), -16); m.sfx(A.sfx_pop(), F(13, .8), -16)
m.sfx(A.sfx_stamp(), F(14, .5), -8)
m.sfx(A.sfx_pop(), L(15) + 0.1, -15); m.sfx(A.sfx_pop(), L(16) + 0.05, -15); m.sfx(A.sfx_pop(), F(17, .25), -15)
for k in range(21): m.sfx(A.sfx_tick(), S(18) + 0.2 + k / 14, -16)
m.sfx(A.sfx_stamp(), F(18, .4), -10)
for k in range(6): m.sfx(A.boom(0.12, 90, 55, 25), S(19) + 0.1 + k * 0.26, -16)                           # agent steps
t0 = F(19, .7); m.sfx(A.sfx_pop(), t0, -12); m.sfx(A.sfx_pop(), F(19, .8), -13)
t = t0 + 1
while t < DUR: m.sfx(A.sfx_tick(), t, -18); t += 1.0
m.sfx(A.sfx_pop(), L(20) + 0.05, -13); m.sfx(A.sfx_hit(), F(20, .45), -8); m.sfx(A.sfx_pop(), F(20, .75), -14)
m.sfx(A.whoosh(0.5), S(21) - 0.2, -12)
for k in range(3): m.sfx(X.ring(), S(21) + 0.4 + k * 1.1, -16, pan=0.4)

m.render('vo2.wav', 'mix_sec2.wav', fade=0.05)
print('ok', DUR)

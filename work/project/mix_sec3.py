import json, numpy as np, sfxkit as A, mixlib as X
j = json.load(open('part3.json')); LT = j['lt']
L = lambda i: LT[i][0]
F = lambda i, f: LT[i][0] + (LT[i][1] - LT[i][0]) * f
S = lambda i: LT[i][0] - 0.18 if i else 0.0
DUR = j['dur'] + 0.6
m = A.Mix(DUR)
tc = F(15, 0.8)                       # match cut to the cold open

# ---- music ----
X.pad(m, [38, 44, 50], 0, S(1) + 0.3, -16, 800)                                   # tension from the call
t = 0.2
while t < S(1): m.music(A.boom(0.25, 70, 45, 16), t, -16); t += 0.9
X.pad(m, [45, 52], S(1), S(4), -22, 600)                                         # the silence
m.music(A.verb(A.pluck(A.mtof(57), 3.0), .7), F(2, .3), -18)
X.plucks(m, [65, 64, 62, 57], S(3) + 0.3, 1.0, -22, 1.8)
X.pad(m, [38, 41, 45], S(4), S(12) - 0.3, -15, 750)                              # night move, boat
t = S(5)
while t < S(7): m.music(A.boom(0.2, 70, 48, 18), t, -17); t += 0.55
m.music(A.norm(A.pad([A.mtof(74), A.mtof(75), A.mtof(80)], 5.0, 3000)), S(7), -24)  # dread swell
X.pad(m, [50, 57, 62, 66], S(12), S(13), -20, 1800)                               # day 1: brief hope
X.plucks(m, [62, 66, 69, 71, 69, 66, 69, 74], S(12) + 0.2, 0.5, -22, 0.7, until=S(13))
X.pad(m, [45, 48, 52], S(13), tc, -17, 900)                                       # days 2-3: falling
X.plucks(m, [64, 62, 60, 59, 57], S(13) + 0.4, 1.5, -23, 1.6, until=tc - 0.5)
X.pad(m, [38, 45, 50], tc, S(20), -16, 700)                                        # back at 3 AM
X.plucks(m, [62, 65, 69, 67, 62, 60, 62, 65, 69, 72], tc + 0.5, 2.4, -22, 1.6, until=S(20))
X.pad(m, [50, 57, 62, 69], S(20), DUR, -15, 2200)                                  # the ship: hope swell
X.plucks(m, [62, 66, 69, 74, 73, 69, 66, 69], S(20) + 0.5, 0.8, -21, 1.0, until=DUR)

# ---- ambience ----
m.sfx(X.bed(S(5), 60, 300, 1.0, 0.3, 0.1), 0, -27)                                 # warehouse tone
m.sfx(X.waves(S(10) - F(6, .62)), F(6, .62), -20)                                   # shore
m.sfx(X.bed(S(12) - S(10), 50, 220, 1.0, 0.5, 0.3), S(10), -20)                     # hold creak/drone
m.sfx(X.waves(tc - S(12)), S(12), -24)
m.sfx(X.waves(DUR - tc), tc, -20); m.sfx(X.bed(DUR - tc, 900, 3500, 1.0), tc, -32)

# ---- cues ----
t = 1.0
while t < L(4) + 0.3: m.sfx(A.sfx_tick(), t, -19); t += 1.0
m.sfx(A.sfx_pop(), 0.3, -14)
m.sfx(A.sfx_pop(), L(2) + 0.05, -15)
m.sfx(A.whoosh(0.5), S(3) - 0.2, -12)
for k in range(5): m.sfx(A.sfx_tick(), F(3, .3) + 0.4 + k * 0.09, -14)                          # keys jingle
m.sfx(A.sfx_stamp(), F(3, .62), -6); m.sfx(A.sfx_pop(), F(3, .5), -14)
m.sfx(X.beep(1200, 0.5), L(4) + 0.3, -14)
m.sfx(A.whoosh(0.35), F(4, .55), -9); m.sfx(A.sfx_pop(), F(4, .55) + 0.3, -13)
m.sfx(A.sfx_pop(), 0.3 + S(5), -15)
m.sfx(A.sfx_hit(), F(5, .35), -8); m.sfx(X.crowd(S(6) - F(5, .35)), F(5, .35), -22)
m.sfx(A.sfx_pop(), F(5, .78), -12)
m.sfx(X.engine(F(6, .32) - S(6) + 0.3), S(6), -12)
m.sfx(A.sfx_hit(), F(6, .32), -10); m.sfx(A.whoosh(0.6), F(6, .62) - 0.3, -12)
for k, f in enumerate((0.15, 0.4, 0.65)): m.sfx(A.sfx_pop(), [S(6) + 0.15, F(6, .32) + 0.15, F(6, .62) + 0.15][k], -14)
for f in (0.05, 0.3, 0.6): m.sfx(A.sfx_pop(), F(8, f), -13)
m.sfx(X.crowd(S(10) - S(9)), S(9), -18); m.sfx(A.sfx_hit(), F(9, .55), -8)
m.sfx(A.whoosh(0.6), S(10) - 0.2, -12)
for f in (0.15, 0.6, 0.85): m.sfx(A.sfx_pop(), F(10, f), -13)
m.sfx(A.sfx_heartbeat(), F(10, .5), -10); m.sfx(A.sfx_heartbeat(), F(10, .5) + 0.8, -10)
m.sfx(A.whoosh(0.4), S(11), -16)
m.sfx(A.sfx_pop(), S(12) + 0.1, -12); m.sfx(X.crowd(S(13) - S(12)), S(12), -20); m.sfx(A.sfx_pop(), F(12, .55), -13)
m.sfx(A.sfx_pop(), S(13) + 0.1, -12); m.sfx(A.sfx_pop(), F(13, .5), -13)
for f in (0.1, 0.4, 0.7): m.sfx(A.sfx_pop(), F(14, f), -12)
m.sfx(X.crowd(S(15) - S(14)), S(14), -21)
m.sfx(A.sfx_pop(), S(15) + 0.1, -12)
t = S(15) + 0.1; end = F(15, .45)
while t < end: m.sfx(A.boom(0.12, 90, 50, 30), t, -16); t += 0.24 + 0.12 * max(0, t - end + 1.5)
m.sfx(A.sfx_power_down(), end, -10); m.sfx(A.sfx_stamp(), F(15, .5), -8)
m.sfx(A.sfx_hit(), tc, -4); m.sfx(A.sfx_tape_stop(), tc - 0.05, -12)
m.sfx(A.whoosh(1.0, rev=True), S(16), -12); m.sfx(A.sfx_pop(), F(16, .3), -13)
for f in (0.0, 0.35, 0.7): m.sfx(A.sfx_pop(), F(17, f), -13)
m.sfx(A.sfx_pop(), F(18, .45), -16)
m.sfx(A.sfx_pop(), F(19, .65), -14)
m.sfx(X.horn(3.0), S(20) + 0.8, -14, pan=0.5); m.sfx(A.sfx_pop(), F(20, .6), -13)
m.sfx(X.crowd(DUR - S(21)), S(21), -12); m.sfx(A.sfx_hit(), S(21) + 0.1, -10)

m.render('vo3.wav', 'mix_sec3.wav', fade=0.05)
print('ok', DUR)

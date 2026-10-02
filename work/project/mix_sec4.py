import json, numpy as np, sfxkit as A, mixlib as X
j = json.load(open('part4.json')); LT = j['lt']
L = lambda i: LT[i][0]
F = lambda i, f: LT[i][0] + (LT[i][1] - LT[i][0]) * f
S = lambda i: LT[i][0] - 0.18 if i else 0.0
DUR = j['dur'] + 3.6
m = A.Mix(DUR)
blk = S(4)                                     # cut to black: everything stops
tc = F(26, 0.75)                               # camera click
lg = LT[33][1] + 0.6                           # channel card

# ---- music ----
X.pad(m, [50, 57, 62, 69], 0, 1.4, -18, 2000)                                     # hope... cut
X.pad(m, [38, 41, 44], S(2), blk, -14, 700)                                        # storm dread
t = S(2)
while t < blk: m.music(A.boom(0.25, 65, 42, 14), t, -15); t += 0.75 - 0.25 * (t - S(2)) / (blk - S(2))
X.pad(m, [57, 64, 69], S(5), S(11), -22, 1500)                                     # waking, camp: fragile
X.plucks(m, [69, 67, 65, 64, 62], S(9) + 0.3, 2.0, -22, 2.4)
X.pad(m, [45, 52, 57], S(11), S(15), -18, 1100)                                    # the call
X.plucks(m, [69, 67, 65, 64, 62, 64, 65, 64, 62, 60, 62], S(12) + 0.4, 1.9, -20, 2.2, until=S(15))
X.pad(m, [43, 50, 55], S(15), S(17), -20, 900)
X.pad(m, [38, 44, 50], S(17), S(23), -16, 800)                                     # twist
X.pad(m, [45, 52, 57], S(23), tc, -19, 1000)                                       # night, the phone
X.plucks(m, [64, 62, 60, 57, 60, 62], S(23) + 0.5, 2.0, -22, 2.2, until=tc)
X.pad(m, [50, 57, 62, 66], tc, S(30), -19, 1700)                                   # the photo travels home (bitter irony)
X.plucks(m, [62, 66, 69, 66, 64, 62, 64, 66], tc + 0.6, 1.2, -23, 1.2, until=S(30))
X.pad(m, [38, 41, 45], S(30), S(31), -15, 800)                                     # agent again
X.pad(m, [45, 52, 57], S(31), DUR, -20, 800)                                       # fact card + close
X.plucks(m, [69, 67, 65, 64, 62, 57], S(32), 2.2, -21, 2.6, until=lg)

# ---- ambience ----
m.sfx(X.waves(S(2)), 0, -20)
m.sfx(X.waves(blk - S(2) + 0.05, 0.05) , S(2), -12); m.sfx(X.rain(blk - S(2) + 0.05, 0.05), S(2), -20)
m.sfx(X.bed(blk - S(2) + 0.05, 200, 900, 0.05, 0.6, 0.35), S(2), -16)                # wind
m.sfx(X.bed(S(10) - S(6), 150, 900, 1.0), S(6), -34)                                 # tent / camp air
m.sfx(X.bed(S(23) - S(11), 150, 900, 1.0), S(11), -32)
m.sfx(X.crickets(tc - S(23)), S(23), -30, pan=-0.3)
m.sfx(X.bed(S(31) - S(27), 150, 900, 1.0), S(27), -34)

# ---- cues ----
m.sfx(X.horn(3.5), 0.2, -16, pan=0.6)
for k in range(5): m.sfx(A.sfx_hit(), S(2) + 0.6 + k * 1.9, -12 + 2 * (k % 2))                    # thunder / waves
m.sfx(A.sfx_pop(), F(2, .25), -14); m.sfx(A.sfx_pop(), F(2, .7), -14)
m.sfx(A.boom(1.2, 60, 30, 2), F(3, .55), -8)                                                      # hull lurch
m.sfx(A.sfx_heartbeat(), F(4, .1), -10)
# blk -> S(5): silence
m.sfx(A.whoosh(1.2, rev=True), S(5) - 0.6, -18); m.sfx(A.sfx_ding(), F(5, .45), -24)
for f in (0.0, 0.25): m.sfx(A.sfx_pop(), F(6, f), -14)
m.sfx(A.sfx_pop(), F(6, .6), -14)
m.sfx(A.sfx_stamp(), F(7, .2), -6)
m.sfx(A.sfx_pop(), F(8, .55), -15)
m.sfx(A.sfx_pop(), 0.2 + S(10), -15); m.sfx(A.sfx_pop(), F(10, .75), -14)
m.sfx(A.sfx_pop(), F(11, .4), -14)
m.sfx(A.whoosh(0.5), S(12) - 0.2, -12)
for k in range(2): m.sfx(X.ring(), S(12) + 0.2 + k * 1.1, -17, pan=0.4)
m.sfx(A.sfx_pop(), F(13, .65), -15)
m.sfx(A.sfx_pop(), F(14, .02), -15); m.sfx(A.sfx_pop(), F(14, .55), -15)
m.sfx(A.sfx_pop(), F(15, .55), -15)
m.sfx(A.sfx_heartbeat(), F(16, .3), -9); m.sfx(A.sfx_heartbeat(), F(16, .3) + 0.7, -9)
m.sfx(A.sfx_hit(), S(17), -3); m.sfx(A.sfx_tape_stop(), S(17) - 0.05, -14)
m.sfx(A.whoosh(0.6), S(18) - 0.2, -12); m.sfx(A.sfx_stamp(), F(18, .45), -7); m.sfx(A.sfx_pop(), F(18, .6), -14)
m.sfx(X.bed(S(20) - S(19), 1500, 6000, 0.3, 0.5, 1.5), S(19), -26)                                 # water / scrubbing
m.sfx(A.sfx_pop(), F(19, .25), -14); m.sfx(A.sfx_pop(), F(19, .75), -14)
m.sfx(A.sfx_pop(), L(20) + 0.1, -15)
m.sfx(A.sfx_tape_stop(), S(21) - 0.1, -14); m.sfx(A.sfx_pop(), F(21, .45), -15); m.sfx(A.sfx_pop(), F(21, .7), -15)
m.sfx(A.sfx_pop(), L(22) + 0.1, -16)
m.sfx(A.sfx_pop(), F(24, .45), -16)
m.sfx(A.whoosh(1.4), S(25) + 0.2, -14)                                                              # car passes
m.sfx(X.shutter(), tc - 0.02, -6); m.sfx(A.sfx_ding(), tc + 0.05, -20)
m.sfx(A.whoosh(1.0), S(27), -14); m.sfx(A.sfx_pop(), S(27) + 0.3, -14)
m.sfx(A.sfx_pop(), F(29, .05), -13)
m.sfx(A.sfx_hit(), S(30) + 0.1, -8); m.sfx(A.sfx_ding(), F(30, .6), -14)
m.sfx(A.sfx_hit(), F(31, .55), -12)
m.sfx(A.sfx_hit(), lg, -8)

m.render('vo4.wav', 'mix_sec4.wav', fade=1.2)
print('ok', DUR)

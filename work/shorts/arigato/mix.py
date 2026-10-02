import json, numpy as np
import sfxkit as A
import short

lt = json.load(open('lt.json')); L = lambda i: lt[i][0]
END = short.END
m = A.Mix(END)

def cricket():
    out = np.zeros(int(0.5 * A.SR))
    for k in range(3):
        c = A.tone(4300, 0.035, 60) * (0.6 + 0.4 * np.sin(2 * np.pi * 60 * A.t_(0.035)))
        i = int(k * 0.055 * A.SR); out[i:i + len(c)] += c
    return A.norm(out)

def wah_wah():                       # sad trombone
    o = []
    for n, d in ((58, 0.35), (57, 0.35), (56, 0.35), (55, 1.1)):
        tt = A.t_(d); f = A.mtof(n) * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * tt) * (tt > 0.3))
        x = sum(np.sin(2 * np.pi * np.cumsum(f) / A.SR * k) / k for k in range(1, 7))
        o.append(A.lp(x, 1800) * A.env(len(tt), 0.03, 0.12))
    return A.norm(A.verb(np.concatenate(o), 0.25))

# 1) comedy pizzicato (hook -> boss walks in)
scale = [60, 64, 67, 64, 62, 65, 69, 65]
t, k = 0.3, 0
while t < L(4) - 0.3:
    m.music(A.pluck(A.mtof(scale[k % 8]), 0.4), t, -14)
    if k % 2 == 0: m.music(A.pluck(A.mtof(scale[k % 8] - 24), 0.5, 0.6), t, -14)
    t += 0.25; k += 1

# 2) tension: low drone + accelerating pulse (deal -> thinking)
tstop = L(9) - 0.75
m.music(A.norm(A.pad([A.mtof(38), A.mtof(45)], tstop - L(4) + 0.3, 600)), L(4) - 0.2, -17)
m.music(A.norm(A.pad([A.mtof(74), A.mtof(75), A.mtof(80)], tstop - L(8), 2500)), L(8) - 0.1, -26)
t = L(4)
while t < tstop:
    bpm = 100 + 70 * (t - L(4)) / (tstop - L(4))
    m.music(A.boom(0.22, 90, 55, 18), t, -13); t += 60 / bpm
m.sfx(A.sfx_tape_stop(), tstop - 0.1, -12)          # music dies before the word

# SFX
m.sfx(A.sfx_hit(), 0.75, -9)                         # title slam
m.sfx(A.sfx_pop(), 0.35, -16)
sh = {fn.__name__: a for a, b, fn in short.timeline()}
sc = short.Sc(sh['s_resume'])
for j in range(8): m.sfx(A.nh(0.05, 2000, 6000, 40), sh['s_resume'] + sc.at(1, 'fluent') - 0.15 + j * 0.1, -24)   # pen scribble
m.sfx(A.sfx_pop(), sh['s_resume'] + sc.at(1, 'fluent') + 0.9, -15)                                                   # flag pop
m.sfx(A.sfx_pop(), sh['s_hired'] + 0.05, -16); m.sfx(A.sfx_ding(), sh['s_hired'] + 0.35, -17)
m.sfx(A.sfx_stamp(), sh['s_hired'] + 0.65, -9)
for j in range(6): m.sfx(A.sfx_step(), sh['s_boss'] + 0.1 + j * 0.3, -18)
m.sfx(A.mix(np.zeros(1), A.nh(0.3, 200, 1200, 10)), sh['s_boss'], -20)   # door
m.sfx(A.sfx_pop(), sh['s_boss'] + 0.4, -16)
sc = short.Sc(sh['s_deal'])
tb = sh['s_deal'] + sc.at(5, 'billion')
m.sfx(A.sfx_hit(), tb, -10); m.sfx(A.sfx_ding(), tb + 0.05, -15); m.sfx(A.sfx_stamp(), tb + 0.6, -10)
m.sfx(A.whoosh(0.4), sh['s_bow'] - 0.1, -18)
sc = short.Sc(sh['s_bow'])
m.sfx(A.whoosh(0.35), sh['s_bow'] + sc.at(6, 'bows') - 0.15, -14); m.sfx(A.sfx_pop(), sh['s_bow'] + sc.at(6, 'bows'), -17)
m.sfx(A.whoosh(0.35), sh['s_bow'] + sc.at(7, 'bow') - 0.15, -14); m.sfx(A.sfx_pop(), sh['s_bow'] + sc.at(7, 'bow'), -17)
for j in range(3):                                   # thoughts pop + strike
    m.sfx(A.sfx_pop(), sh['s_word'] + 0.1 + j * 0.45, -15)
    m.sfx(A.whoosh(0.15), sh['s_word'] + 0.35 + j * 0.45, -17)
m.sfx(A.sfx_heartbeat(), sh['s_word'] + 0.2, -10); m.sfx(A.sfx_heartbeat(), sh['s_word'] + 0.9, -10)
m.sfx(A.sfx_heartbeat(), sh['s_word'] + 1.5, -9)
ta = sh['s_arigato']
m.sfx(A.sfx_hit(), ta + 0.1, -10)                    # ARIGATO slam
for j in range(7): m.sfx(cricket(), ta + 1.8 + j * 0.42, -20, pan=0.3)   # awkward silence
m.sfx(A.sfx_stamp(), ta + 1.7 + 0.5, -12)            # LOADING stamp
m.sfx(wah_wah(), ta + 3.05, -11)                     # frozen smile
m.render('vo_rt.wav', 'mix.wav')
print('ok')

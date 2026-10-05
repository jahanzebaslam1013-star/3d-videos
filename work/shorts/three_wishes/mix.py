import numpy as np, sfxkit as A, scenekit as K, short
END = K.END; L = lambda i: K.LT[i][0]
m = A.Mix(END + 4)
TL = {n: a for a, b, n in K.timeline_of(short.SHOTS)}
N = int(round(END / 0.25 / 8)) * 8; beat = END / N
ARAB = [64, 65, 68, 69, 71, 72, 74, 76]          # E phrygian dominant
def sec(t):
    if t < TL['s_genie'] or t >= TL['s_back'] - 0.1: return 'street'
    if t < TL['s_tax']: return 'magic'
    if t < TL['s_broke']: return 'trouble'
    if t < TL['s_famous']: return 'sad'
    if t < TL['s_onewish']: return 'magic'
    if t < TL['s_poof']: return 'tense'
    return 'none'
pat = [0, 2, 4, 3, 2, 1, 2, 0]
for k in range(N):
    t = k * beat; s = sec(t)
    if s == 'street':
        if k % 2 == 0: m.music(A.pluck(A.mtof([57, 60, 64, 67][(k // 2) % 4]), 0.6, 0.7), t, -17)
        if k % 8 == 0: m.music(A.pluck(A.mtof(45), 1.0, 0.5), t, -14)
    elif s == 'magic':
        m.music(A.pluck(A.mtof(ARAB[pat[k % 8] + (2 if (k // 8) % 2 else 0)]), 0.35), t, -15)
        if k % 2 == 0: m.music(A.pluck(A.mtof(40), 0.4, 0.6), t, -13)
        if k % 4 == 2: m.sfx(A.nh(0.05, 3000, 9000, 60), t, -26)
    elif s == 'trouble':
        m.music(A.pluck(A.mtof([52, 55, 58, 55][k % 4]), 0.3, 0.6), t, -15)
        if k % 2 == 0: m.music(A.boom(0.2, 90, 55, 18), t, -14)
m.music(A.norm(A.pad([A.mtof(40), A.mtof(47)], TL['s_poof'] - TL['s_onewish'] + 0.3, 700)), TL['s_onewish'] - 0.1, -17)
m.music(A.norm(A.pad([A.mtof(71), A.mtof(72)], TL['s_poof'] - TL['s_lastwish'], 2500)), TL['s_lastwish'], -25)
for j in range(int((TL['s_lastwish'] - TL['s_think']) / 0.5)): m.sfx(A.sfx_tick(), TL['s_think'] + j * 0.5, -14)
# sad trombone for broke
def wah():
    o = []
    for n, d in ((58, 0.3), (57, 0.3), (56, 0.3), (55, 0.9)):
        tt = A.t_(d); f = A.mtof(n) * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * tt) * (tt > 0.3))
        o.append(A.lp(sum(np.sin(2 * np.pi * np.cumsum(f) / A.SR * k) / k for k in range(1, 7)), 1800) * A.env(len(tt), 0.03, 0.1))
    return A.norm(A.verb(np.concatenate(o), 0.25))
m.sfx(wah(), TL['s_broke'] + 0.3, -12)
# SFX
S = lambda n: short.Sc(TL[n])
m.sfx(A.mix(A.boom(0.15, 300, 200, 30), A.nh(0.2, 2000, 8000, 25)), 0.32, -9)      # clank kick
m.sfx(A.sfx_hit(), 0.55, -13); m.sfx(A.sfx_pop(), 1.1, -17)
tp = TL['s_genie'] + S('s_genie').at(1, 'Poof')
for j in range(8): m.sfx(A.nh(0.06, 2000, 7000, 50), TL['s_genie'] + 0.1 + j * 0.1, -22)          # rubbing
m.sfx(A.sfx_hit(), tp, -9); m.sfx(A.whoosh(0.8, rev=True), tp - 0.7, -13); m.sfx(A.sfx_ding(), tp + 0.1, -13)
m.sfx(A.sfx_pop(), TL['s_genie'] + S('s_genie').L(2)[0] + 0.2, -15)
for n, w, li in (('s_rich', 'Make', 3), ('s_famous', 'Make', 8)):
    tt = TL[n] + S(n).at(li, w); m.sfx(A.sfx_pop(), TL[n] + 0.05, -15); m.sfx(A.sfx_ding(), tt, -12)
    m.sfx(A.mix(A.nh(0.04, 1500, 6000, 80)), tt + 1.0, -12)                                          # snap
l4 = TL['s_rich'] + S('s_rich').L(4)[0]
for j in range(10): m.sfx(A.tone(1800 + 120 * j, 0.06, 30), l4 + j * 0.15, -20)                  # counter
m.sfx(A.mix(A.tone(2400, 0.1, 20), A.tone(3200, 0.15, 15)), l4 + 1.6, -12); m.sfx(A.sfx_stamp(), l4 + 1.6, -10)
st = S('s_tax'); tc = TL['s_tax'] + st.at(5, 'calls') - 0.1
ring = A.mix(*[np.concatenate([np.zeros(int(i * 0.09 * A.SR)), A.tone(1400, 0.05, 20) + A.tone(1750, 0.05, 20)]) for i in range(8)])
m.sfx(ring, tc, -16); m.sfx(ring, tc + 0.9, -18)
th = TL['s_tax'] + st.at(5, 'half'); m.sfx(A.whoosh(0.3), th - 0.1, -12); m.sfx(A.sfx_stamp(), th + 0.2, -9)
for j in range(14): m.sfx(A.sfx_pop(), TL['s_cousins'] + 0.05 + j * 0.12, -22, pan=((j % 5) - 2) * 0.3)
m.sfx(A.verb(A.nh(1.5, 400, 3000, 1.2), 0.3), TL['s_cousins'] + 0.3, -22)                         # crowd murmur
m.sfx(A.sfx_stamp(), TL['s_broke'] + 0.5, -10)
l9 = TL['s_famous'] + S('s_famous').L(9)[0]
for j in range(3): m.sfx(A.sfx_pop(), l9 + j * 0.35, -14)
shutter = lambda: A.mix(A.nh(0.03, 2000, 8000, 150), 0.6 * np.concatenate([np.zeros(int(0.05 * A.SR)), A.nh(0.03, 1500, 6000, 150)]))
for j in range(6): m.sfx(shutter(), l9 + j * 0.5, -14)
for j in range(14): m.sfx(shutter(), TL['s_paps'] + j * 0.12 + (j % 3) * 0.03, -15, pan=((j % 5) - 2) * 0.35)
tf = TL['s_paps'] + S('s_paps').at(10, 'Fans') - 0.1
m.sfx(A.sfx_tape_stop(), tf - 0.05, -14); m.sfx(A.sfx_pop(), tf + 0.25, -13)
for j in range(8): m.sfx(shutter(), TL['s_milk'] + j * 0.3, -15, pan=((j % 3) - 1) * 0.6)
m.sfx(A.sfx_pop(), TL['s_milk'] + 0.2, -16); m.sfx(A.sfx_pop(), TL['s_milk'] + 0.6, -16)
to = TL['s_onewish'] + S('s_onewish').at(12, 'One'); m.sfx(A.sfx_ding(), to, -12); m.sfx(A.sfx_hit(), to, -14)
m.sfx(A.sfx_heartbeat(), TL['s_lastwish'] + 0.4, -11); m.sfx(A.sfx_heartbeat(), TL['s_lastwish'] + 1.4, -11)
m.sfx(A.whoosh(1.0, rev=True), TL['s_poof'] - 1.0, -11)
m.sfx(A.sfx_hit(), TL['s_poof'], -6); m.sfx(A.verb(A.nh(1.2, 300, 4000, 2.5), 0.5), TL['s_poof'], -10)
ta = TL['s_back'] + short.Sc(TL['s_back']).at(16, 'And then')
m.sfx(A.sfx_ding(), ta, -14)
for j in range(8): m.sfx(A.sfx_step(), TL['s_back'] + 0.2 + j * 0.31, -24)
for j in range(3): m.sfx(A.sfx_step(), j * 0.31, -24)
K.render_loop(m, 'vo_rt.wav', 'mix.wav'); print('ok')

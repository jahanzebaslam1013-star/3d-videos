import numpy as np, sfxkit as A, scenekit as K, short
END = K.END
m = A.Mix(END + 4)
TL = {n: a for a, b, n in K.timeline_of(short.SHOTS)}
S = lambda n: short.Sc(TL[n])
N = int(round(END / 0.28 / 12)) * 12; beat = END / N          # 3/4 grid that divides the loop
def sec(t):
    if TL['s_never'] <= t < TL['s_ninety']: return 'sneak'
    if TL['s_drawer'] <= t < TL['s_wink']: return 'reveal'
    return 'cozy'
CH = [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]]
for k in range(N):
    t = k * beat; s = sec(t); ch = CH[(k // 12) % 4]
    if s == 'cozy':
        m.music(A.pluck(A.mtof(ch[[0, 1, 2][k % 3]] + 12), 0.6, 1.2), t, -18)            # music-box
        if k % 3 == 0: m.music(A.pluck(A.mtof(ch[0] - 12), 0.8, 0.5), t, -14)
    elif s == 'sneak':
        if k % 2 == 0: m.music(A.pluck(A.mtof([45, 48, 47, 50, 48, 47][(k // 2) % 6]), 0.25, 0.6), t, -12)
        if k % 6 == 3: m.sfx(A.nh(0.04, 3000, 8000, 80), t, -24)
m.music(A.norm(A.pad([A.mtof(50), A.mtof(57), A.mtof(62)], TL['s_wink'] - TL['s_drawer'] + 0.3, 1500)), TL['s_drawer'] - 0.1, -18)
# SFX
m.sfx(A.verb(A.nh(0.6, 2000, 7000, 6), 0.4), 0.1, -26)                                   # whisper hiss
m.sfx(A.sfx_pop(), 0.35, -17); m.sfx(A.sfx_pop(), 0.6, -17)
m.sfx(A.sfx_pop(), TL['s_beg'] + 0.05, -16)
for j in range(10): m.sfx(A.tone(1500 + 80 * j, 0.05, 30), TL['s_beg'] + j * 0.18, -22)
m.sfx(A.verb(A.nh(1.6, 400, 3000, 1.2), 0.3), TL['s_beg'] + 0.6, -22)
for w in ('Neighbors', 'Cousins', 'mayor'): m.sfx(A.sfx_pop(), TL['s_who'] + S('s_who').at(2, w) - 0.1, -15)
m.sfx(A.mix(*[np.concatenate([np.zeros(int(i * 0.04 * A.SR)), A.nh(0.03, 2000, 6000, 100)]) for i in range(10)]), TL['s_never'], -15)   # zip
m.sfx(A.sfx_stamp(), TL['s_never'] + 0.45, -9)
m.sfx(A.sfx_pop(), TL['s_offers'] + 0.2, -15); m.sfx(A.sfx_ding(), TL['s_offers'] + 0.35, -15)
m.sfx(A.sfx_stamp(), TL['s_offers'] + S('s_offers').at(4, 'no'), -9)
for j in range(5): m.sfx(A.mix(A.nh(0.15, 300, 2500, 15), A.boom(0.1, 150, 80, 30) * 0.5), TL['s_spy'] + 0.3 + j * 0.45, -16)
m.sfx(A.sfx_tape_stop(), TL['s_spy'] + S('s_spy').at(5, 'Nothing') - 0.2, -14); m.sfx(A.sfx_stamp(), TL['s_spy'] + S('s_spy').at(5, 'Nothing'), -9)
m.sfx(A.sfx_pop(), TL['s_ninety'] + 0.1, -16); m.sfx(A.sfx_ding(), TL['s_ninety'] + S('s_ninety').at(6, 'you'), -13)
m.sfx(A.sfx_pop(), TL['s_promise'] + 0.05, -16); m.sfx(A.sfx_ding(), TL['s_promise'] + S('s_promise').L(8)[0], -14)
to = TL['s_drawer'] + S('s_drawer').at(9, 'opens')
m.sfx(A.mix(A.nh(0.6, 200, 1500, 4), 0.4 * A.tone(90, 0.5, 4)), to, -12)                  # drawer slide
m.sfx(A.verb(A.mix(A.tone(1318, 2.0, 1.5), A.tone(1568, 2.0, 1.6), A.tone(1976, 2.0, 1.7)), 0.5), to + 0.2, -13)   # angelic reveal
ti = TL['s_drawer'] + S('s_drawer').L(10)[0]
for j in range(9): m.sfx(A.sfx_pop(), ti + j * 0.22, -18)
m.sfx(A.sfx_tape_stop(), TL['s_store'] - 0.15, -11); m.sfx(A.sfx_hit(), TL['s_store'] + 0.05, -7); m.sfx(A.sfx_stamp(), TL['s_store'] + 0.05, -9)
m.sfx(A.mix(A.nh(0.1, 1500, 5000, 30), A.boom(0.12, 200, 120, 30)), TL['s_store'] + 0.75, -16)   # cookie hits floor
tw = TL['s_wink'] + S('s_wink').at(12, 'winks') + 0.1
m.sfx(A.mix(A.tone(2600, 0.25, 12), A.tone(3900, 0.2, 14)), tw, -12)                        # *ting* wink
for j in range(12): m.sfx(A.nh(0.05, 2500, 7000, 60), TL['s_years'] + j * 0.28, -23, pan=((j % 3) - 1) * 0.5)   # pages
m.sfx(A.whoosh(1.5), TL['s_years'] + 0.2, -16)
m.sfx(A.mix(*[np.concatenate([np.zeros(int(i * 0.04 * A.SR)), A.nh(0.03, 2000, 6000, 100)]) for i in range(10)]), TL['s_never2'], -15)
m.sfx(A.sfx_stamp(), TL['s_never2'] + 0.45, -9); m.sfx(A.mix(A.tone(2600, 0.25, 12), A.tone(3900, 0.2, 14)), TL['s_never2'] + 0.7, -13)
for j in range(5): m.sfx(A.sfx_step(), TL['s_grandkid'] + j * 0.32, -20)
m.sfx(A.sfx_pop(), TL['s_grandkid'] + S('s_grandkid').at(15, 'grandkid'), -16)
m.sfx(A.verb(A.nh(0.6, 2000, 7000, 6), 0.4), END - 0.7, -26)                               # whisper -> wraps to start
K.render_loop(m, 'vo_rt.wav', 'mix.wav'); print('ok')

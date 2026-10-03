import numpy as np, sfxkit as A, scenekit as K, short
END = K.END; L = lambda i: K.LT[i][0]
m = A.Mix(END + 4)
TL = {n: a for a, b, n in K.timeline_of(short.SHOTS)}
N = int(round(END / 0.26 / 8)) * 8; beat = END / N          # beat grid divides the loop exactly
prog = {'C': [60, 64, 67, 72], 'Am': [57, 60, 64, 69], 'F': [53, 57, 60, 65], 'G': [55, 59, 62, 67], 'Dm': [50, 53, 57, 62]}
for k in range(N):
    t = k * beat
    tense = L(4) - 0.2 <= t < L(5) - 0.2
    if tense: continue
    ch = ['C', 'Am', 'F', 'G'][(k // 8) % 4] if t < L(4) or t >= L(6) - 0.2 else ['F', 'G', 'C', 'C'][(k // 8) % 4]
    notes = prog[ch]
    m.music(A.pluck(A.mtof(notes[[0, 2, 1, 3, 2, 1, 3, 2][k % 8]]), 0.4), t, -15)
    if k % 2 == 0: m.music(A.pluck(A.mtof(notes[0] - 24), 0.5, 0.6), t, -13)
# tension under the boss
m.music(A.norm(A.pad([A.mtof(38), A.mtof(45)], L(5) - L(4) + 0.4, 600)), L(4) - 0.3, -16)
t = L(4)
while t < L(5) - 0.3: m.music(A.boom(0.22, 90, 55, 18), t, -12); t += 60 / 130
# SFX
m.sfx(A.sfx_pop(), 0.05, -18)
for j in range(14): m.sfx(A.mix(A.nh(0.03, 2000, 6000, 120), 0.3 * A.tone(1800, 0.02, 80)), TL['s_typing'] + short.Sc(TL['s_typing']).at(1, 'This') - 0.1 + j * 0.12, -20)
tc = TL['s_click'] + short.Sc(TL['s_click']).at(2, 'Reply') + 0.1
m.sfx(A.mix(A.nh(0.02, 1500, 5000, 200), 0.5 * A.tone(2200, 0.03, 90)), tc, -10); m.sfx(A.sfx_hit(), tc + 0.05, -12)
for j in range(12): m.sfx(A.sfx_pop(), TL['s_inbox'] + 0.05 + j * 0.12, -21, pan=(j % 3 - 1) * 0.5)
td = TL['s_inbox'] + short.Sc(TL['s_inbox']).at(3, 'Ding')
m.sfx(A.sfx_ding(), td, -9); m.sfx(A.sfx_ding(), td + 0.05, -13, pan=-0.6); m.sfx(A.sfx_ding(), td + 0.1, -13, pan=0.6)
sb = short.Sc(TL['s_boss'])
m.sfx(A.sfx_pop(), TL['s_boss'] + 0.05, -16); m.sfx(A.sfx_hit(), TL['s_boss'] + sb.at(4, 'My'), -11); m.sfx(A.sfx_stamp(), TL['s_boss'] + sb.at(4, 'My') + 0.9, -10)
sc = short.Sc(TL['s_ceo'])
m.sfx(A.sfx_pop(), TL['s_ceo'] + 0.05, -16); m.sfx(A.sfx_ding(), TL['s_ceo'] + sc.at(5, 'Agreed'), -14); m.sfx(A.sfx_stamp(), TL['s_ceo'] + sc.at(5, 'Cancel') + 0.2, -9)
tl = TL['s_legend'] + short.Sc(TL['s_legend']).at(6, 'legend') - 0.1
m.sfx(A.sfx_hit(), tl, -11); m.sfx(A.verb(A.nh(1.6, 800, 6000, 1.5), 0.3), tl, -20)   # crowd-ish cheer wash
sp = short.Sc(TL['s_promo'])
for w in ('Promoted', 'Corner', 'team'): m.sfx(A.sfx_pop(), TL['s_promo'] + sp.at(7, w), -15)
m.sfx(A.sfx_ding(), TL['s_promo'] + sp.at(7, 'Promoted'), -16)
for j in range(16): m.sfx(A.nh(0.06, 1500, 5000, 50), TL['s_rule_end'] + 0.45 + j * 0.15, -22)   # marker squeaks
K.render_loop(m, 'vo_rt.wav', 'mix.wav'); print('ok')

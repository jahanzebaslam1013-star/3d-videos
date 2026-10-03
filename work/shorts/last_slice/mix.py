import numpy as np, sfxkit as A, scenekit as K, short
END = K.END; L = lambda i: K.LT[i][0]
m = A.Mix(END + 4)
TL = {n: a for a, b, n in K.timeline_of(short.SHOTS)}
N = int(round(END / 0.3 / 8)) * 8; beat = END / N
melody = [64, 67, 71, 67, 62, 66, 69, 66]
for k in range(N):
    t = k * beat
    if L(5) - 0.3 <= t < L(8) - 0.2: continue                 # Bruno + pain: no cute music
    m.music(A.pluck(A.mtof(melody[k % 8]), 0.5, 0.8), t, -16)
    if k % 4 == 0: m.music(A.pluck(A.mtof(melody[k % 8] - 24), 0.8, 0.5), t, -14)
# dreamy night pad that crosses the loop seam (end -> start wraps)
m.music(A.norm(A.pad([A.mtof(52), A.mtof(59), A.mtof(64)], 4.5, 1200)), L(8) - 0.3, -19)
# Bruno: low drone + slow heavy steps
m.music(A.norm(A.pad([A.mtof(33), A.mtof(40)], L(8) - L(5) + 0.4, 500)), L(5) - 0.3, -15)
t = L(5)
while t < L(7) - 0.3: m.music(A.boom(0.3, 70, 40, 12), t, -11); t += 60 / 80
# sad slow notes for "everything hurts"
for i, n in enumerate((64, 62, 60, 59)): m.music(A.verb(A.pluck(A.mtof(n), 1.2, 0.5), 0.4), L(7) + i * 0.55, -14)
# SFX
m.sfx(A.verb(A.nh(0.4, 1500, 5000, 8), 0.2), 0.95, -22)        # paper rustle (note out of pocket)
m.sfx(A.sfx_pop(), 1.35 + 0, -18)
sn = short.Sc(TL['s_note']); m.sfx(A.sfx_pop(), TL['s_note'] + 0.05, -17)
for j in range(10): m.sfx(A.nh(0.05, 2000, 6000, 40), TL['s_note'] + sn.at(1, "Don't") + j * 0.15, -24)
m.sfx(A.sfx_stamp(), TL['s_hand'] + 0.25, -10)
se = short.Sc(TL['s_eat']); te = TL['s_eat'] + se.at(3, 'eat') - 0.1
m.sfx(A.sfx_pop(), TL['s_eat'] + se.at(3, 'laugh'), -16)
m.sfx(A.mix(A.boom(0.12, 200, 120, 30), A.nh(0.15, 1500, 5000, 30)), te + 0.5, -10)   # chomp
m.sfx(A.mix(A.boom(0.12, 200, 120, 30), A.nh(0.15, 1500, 5000, 30)), te + 0.8, -13)
m.sfx(A.sfx_tape_stop(), TL['s_sticky'] - 0.05, -12); m.sfx(A.sfx_hit(), TL['s_sticky'] + 0.15, -11)
for j in range(4): m.sfx(A.sfx_step(), TL['s_bruno'] + j * 0.33, -8)
sb = short.Sc(TL['s_bruno'])
m.sfx(A.sfx_pop(), TL['s_bruno'] + sb.at(5, 'six') + 0.2, -15); m.sfx(A.sfx_stamp(), TL['s_bruno'] + sb.at(5, 'body'), -9)
ss = short.Sc(TL['s_stare']); tc = TL['s_stare'] + ss.at(6, 'cracks')
crack = lambda: A.norm(A.mix(A.nh(0.06, 1500, 7000, 60), 0.6 * A.boom(0.08, 300, 150, 50)))
m.sfx(crack(), tc, -7); m.sfx(crack(), tc + 0.45, -7); m.sfx(A.sfx_heartbeat(), TL['s_stare'] + 0.5, -11); m.sfx(A.sfx_heartbeat(), TL['s_stare'] + 1.6, -11)
m.sfx(A.sfx_hit(), TL['s_hurts'], -6); m.sfx(A.boom(0.6, 120, 40, 6), TL['s_hurts'], -8)
for j in range(4): m.sfx(A.sfx_ding(), TL['s_hurts'] + 0.4 + j * 0.45, -24, pan=(-1) ** j * 0.5)  # tweety stars
sw = short.Sc(TL['s_write'])
for j in range(12): m.sfx(A.nh(0.05, 2000, 6000, 40), TL['s_write'] + sw.at(8, 'write') - 0.2 + j * 0.13, -22)
s9 = short.Sc(TL['s_end'])
m.sfx(A.verb(A.nh(0.3, 1500, 5000, 10), 0.2), TL['s_end'] + s9.at(9, 'slip') + 0.3, -22)
m.sfx(A.sfx_ding(), TL['s_end'] + s9.at(9, 'asleep'), -18)      # time-reset sparkle
K.render_loop(m, 'vo_rt.wav', 'mix.wav'); print('ok')

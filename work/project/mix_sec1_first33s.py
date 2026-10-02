import numpy as np, sfxkit as A
LT = [[0, 2.262], [3.221, 6.116], [7.098, 9.539], [10.512, 18.051], [19.046, 25.245], [26.232, 28.623], [30.297, 31.724], [33.443, 36.5]]
F = lambda i, f: LT[i][0] + (LT[i][1] - LT[i][0]) * f
DUR = 33.25
m = A.Mix(DUR)
# BGM: dark sea drone + slow sad plucks, swell into the freeze
m.music(A.norm(A.pad([A.mtof(38), A.mtof(45), A.mtof(50)], 32.0, 700)), 0, -16)
m.music(A.norm(A.pad([A.mtof(62), A.mtof(65)], 20, 1800, 0.4)), 10.5, -26)
for k, n in enumerate([62, 65, 69, 67, 62, 60, 62, 65, 69, 72, 70, 69]):
    m.music(A.verb(A.pluck(A.mtof(n), 1.6), .5), 2.5 + k * 2.4, -22)
t = 19.0
while t < 31.5: m.music(A.boom(0.25, 70, 45, 16), t, -17); t += 1.0     # heartbeat-like pulse
m.music(A.norm(A.pad([A.mtof(74), A.mtof(75), A.mtof(80)], 4.0, 3000)), 28.0, -24)   # dread swell
# ambience: waves + wind
n = int(DUR * A.SR); w = A.lp(A.rng.standard_normal(n), 500)
w *= 0.6 + 0.4 * np.sin(np.arange(n) / A.SR * 2 * np.pi / 5.5) ** 2
m.sfx(A.norm(w), 0, -20); m.sfx(A.norm(A.bp(A.rng.standard_normal(n), 900, 3500)) * 0.4, 0, -30)
# engine putt-putt until it dies
eng_end = LT[2][0] + 1.0; t = 0.2
while t < eng_end:
    m.sfx(A.boom(0.12, 90, 50, 30), t, -16 + 4 * (t > eng_end - 2)); t += 0.24 + 0.1 * max(0, t - eng_end + 2.5)
m.sfx(A.sfx_power_down(), eng_end - 0.2, -12)
# hits
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
m.render('vo1.wav', 'mix30.wav', fade=0.6)
print('ok')

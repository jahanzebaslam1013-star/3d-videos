"""The Last Slice — looping stickman reel. Ends asleep in bed = the first frame."""
import sys, math
sys.path.insert(0, '.')
from scenekit import *

INKBLUE = hexc('1d3a8a')
NOTE = "Don't eat the last slice."

def you(ctx, x, y, s, band=0.0, **kw):
    kw.setdefault('outfit', 'hoodie')
    hero(ctx, x, y, s, **kw)
    if band > 0.01:
        ctx.save(); ctx.translate(x, y); ctx.rotate(kw.get('rot', 0)); ctx.scale(s, s)
        shape(ctx, [(-63, -134), (63, -138), (65, -112), (-61, -108)], (0.97, 0.97, 0.95), 3, 6000, alpha=band)
        rough(ctx, [(-40, -128), (-38, -114)], 2, 6001, hexc('c9c3b5'), alpha=band)
        shape(ctx, [(62, -128), (88, -142), (84, -120)], (0.97, 0.97, 0.95), 2.5, 6002, alpha=band)
        ctx.save(); ctx.translate(32, -56); ctx.rotate(-0.4)
        shape(ctx, rect(-20, -8, 20, 8), hexc('e8c9a0'), 2.5, 6003, alpha=band)
        rough(ctx, [(-6, -8), (-6, 8)], 1.5, 6004, alpha=band); rough(ctx, [(6, -8), (6, 8)], 1.5, 6005, alpha=band)
        ctx.restore(); ctx.restore()

BRUNO_ARMS = {
    'down': [((-68, 44), (-185, 130), (-160, 225)), ((68, 44), (185, 130), (160, 225))],
    'clasp': [((-68, 44), (-190, 150), (-24, 160)), ((68, 44), (190, 150), (24, 160))],
}
def bruno(ctx, x, y, s, arms='down', **kw):
    A = BRUNO_ARMS[arms]; wd = 1.9
    person3(ctx, x, y, s, 'tee', 'crew', hexc('2a2622'), seed=3100, width=wd, color=hexc('34373d'), arms=A, **kw)
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for (sh, el, ha) in A:
        sx, sy = sh[0] * wd, sh[1]
        cx, cy = (sx + el[0]) / 2, (sy + el[1]) / 2
        ang = math.atan2(el[1] - sy, el[0] - sx)
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(ang)
        shape(ctx, ell(0, 0, 46, 24, 24), SKIN, 4, 3150 + int(sx))
        ctx.restore()
        ctx.save(); ctx.translate((el[0] + ha[0]) / 2, (el[1] + ha[1]) / 2); ctx.rotate(math.atan2(ha[1] - el[1], ha[0] - el[0]))
        shape(ctx, ell(0, 0, 38, 18, 20), SKIN, 4, 3160 + int(sx))
        ctx.restore()
    ctx.restore()

def note_paper(ctx, x, y, w, rot, txt_alpha=1.0, n=None, size=None):
    h = w * 0.62
    paper(ctx, x, y, w, h, rot, 6100, col=hexc('fbf6e2'))
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    size = size or w * 0.13
    s = NOTE if n is None else NOTE[:n]
    a, b = "Don't eat", " the last slice."
    l1 = s[:len(a)]; l2 = s[len(a):].strip()
    text(ctx, l1, -w * 0.4, -h * 0.08, size, color=INKBLUE, alpha=txt_alpha)
    text(ctx, l2, -w * 0.4, h * 0.22, size, color=INKBLUE, alpha=txt_alpha)
    ctx.restore()

# ---------------- bedroom (first + last shot) ----------------
PIV = (680, 1010); BS = 1.5
def bedroom(ctx, light):
    wall = tint(hexc('2b3550'), hexc('e2cfa8'), light); fl = tint(hexc('1f2433'), hexc('9a7a58'), light)
    room(ctx, wall, fl, 1330)
    shape(ctx, rect(110, 300, 470, 720), tint(hexc('1a2340'), hexc('a9d3ec'), light), 5, 6200)
    if light < 0.99: shape(ctx, ell(340, 430, 50, 50, 24), hexc('f1ecd0'), 3, 6201, alpha=1 - light)
    if light > 0.01: shape(ctx, ell(250, 450, 60, 60, 24), hexc('f6d36a'), 3, 6202, alpha=light)
    rough(ctx, [(290, 300), (290, 720)], 5, 6203); rough(ctx, [(110, 510), (470, 510)], 5, 6204)
    # bed
    shape(ctx, rect(110, 860, 170, 1300), hexc('6b4a35'), 5, 6210)
    shape(ctx, rect(120, 1160, 990, 1250), hexc('7a573d'), 5, 6211)
    for lx in (150, 960): shape(ctx, rect(lx - 14, 1250, lx + 14, 1320), hexc('5a3d2a'), 4, 6212 + lx)
    shape(ctx, rect(140, 1110, 985, 1165), (0.95, 0.95, 0.93), 4, 6215)
    shape(ctx, ell(270, 1080, 115, 42, 30), (0.97, 0.97, 0.97), 4, 6216)

def blanket(ctx):
    pts = [(560, 1150), (560, 990)] + [(600 + k * 40, 975 + 12 * math.sin(k * 1.3)) for k in range(10)] + [(990, 990), (995, 1175)]
    shape(ctx, pts, hexc('4f79b8'), 5, 6220)
    for k in range(3): rough(ctx, [(620 + k * 120, 1000), (650 + k * 120, 1150)], 2.5, 6221 + k, hexc('3a5f96'))

def bed_scene(ctx, light, r, expr, band=0.0, arms='down', note_at=None, dim=None):
    bedroom(ctx, light)
    s = BS
    ctx.save(); ctx.translate(*PIV); ctx.rotate(r)
    you(ctx, 0, -200 * s, s, band=band, expr=expr, arms=arms, legs=None)
    ctx.restore()
    blanket(ctx)
    if note_at is not None: note_paper(ctx, note_at[0], note_at[1], 170, -0.1, size=24)
    dark(ctx, 0.38 * (1 - light) if dim is None else dim, (0.02, 0.03, 0.08))

LIE = -math.pi / 2
HOLD = [((-68, 44), (-130, 120), (-70, 30)), ((68, 44), (90, 128), (86, 206))]
POCKET = [((-68, 44), (-100, 130), (-80, 196)), ((68, 44), (90, 128), (86, 206))]
def lerp_arms(A, B, u):
    return [tuple((lerp(p[0], q[0], u), lerp(p[1], q[1], u)) for p, q in zip(a, b)) for a, b in zip(A, B)]
def hand_world(arms, r):
    hx, hy = arms[0][2]; s = BS
    lx, ly = hx * s, -200 * s + hy * s
    return (PIV[0] + lx * math.cos(r) - ly * math.sin(r), PIV[1] + lx * math.sin(r) + ly * math.cos(r))

def s_wake(ctx, t, d, S):
    light = ease_io((t - 0.15) / 0.55)
    r = LIE * (1 - ease_io((t - 0.35) / 0.5))
    expr = 'closed' if t < 0.25 else ('neutral' if t < 1.1 else 'worried')
    DOWN = ARMS['down']
    if t < 0.9: arms = DOWN
    elif t < 1.05: arms = lerp_arms(DOWN, POCKET, (t - 0.9) / 0.15)
    else: arms = lerp_arms(POCKET, HOLD, ease_out((t - 1.05) / 0.3))
    note = hand_world(arms, r) if t > 1.05 else None
    bed_scene(ctx, light, r, expr, arms=arms, note_at=note)
    if t > 1.35: glow_text(ctx, '?', 840, 560, 160, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 1.35))

def s_end(ctx, t, d, S):
    ts = S.at(9, 'slip') ; tf = S.at(9, 'fall'); ta = S.at(9, 'asleep')
    if t < ts + 0.2: arms = HOLD
    elif t < ts + 0.6: arms = lerp_arms(HOLD, POCKET, ease_io((t - ts - 0.2) / 0.4))
    else: arms = lerp_arms(POCKET, ARMS['down'], ease_io((t - ts - 0.6) / 0.3))
    note = hand_world(arms, 0) if t < ts + 0.6 else None
    r = LIE * ease_io((t - tf + 0.15) / 0.6)
    expr = 'worried' if t < tf else ('blank' if t < ta else 'closed')
    band = 1 - ease_io((t - ta - 0.05) / 0.5)
    bed_scene(ctx, 0.0, r, expr, band=band, arms=arms, note_at=note)
    if 0 < t - ta < 0.75:                                          # time-reset sparkle
        hx, hy = PIV[0] - 295 * BS, PIV[1]
        for k in range(5):
            a = k * 1.256 + t * 3; rr = 90 + 40 * (t - ta)
            star(ctx, hx + rr * math.cos(a), hy - 40 + rr * 0.6 * math.sin(a), 18, alpha=max(0, 1 - (t - ta) / 0.75), seed=6300 + k)

# ---------------- story ----------------
def s_note(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('cdb894')); ctx.paint(); ctx.new_path()
    radial(ctx, 540, 850, 800, (1, 0.95, 0.8), 0.4)
    ctx.save(); cam(ctx, 540, 850, 1.0 + 0.08 * ease_io(t / d))
    tn = S.at(1, "Don't") - 0.1
    n = int(len(NOTE) * min(1, max(0, (t - tn) / 1.5)))
    note_paper(ctx, 540, 850, 860, -0.04, n=n, size=118)
    for hx, hy in ((150, 1080), (930, 1040)):
        shape(ctx, ell(hx, hy, 46, 40, 20), SKIN, 4, 6400 + hx)
    if n >= len(NOTE):
        rough(ctx, [(220, 1010), (lerp(220, 860, min(1, (t - tn - 1.5) / 0.3)), 990)], 7, 6410, hexc('c0322a'))
    ctx.restore()
    glow_text(ctx, 'A NOTE...', 540, 300, 130, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.05))

def s_hand(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('d7c4a0')); ctx.paint(); ctx.new_path()
    note_paper(ctx, 300, 560, 380, -0.08, size=52)
    paper(ctx, 790, 560, 340, 300, 0.07, 6450, col=hexc('fbf6e2'))
    ctx.save(); ctx.translate(790, 560); ctx.rotate(0.07)
    text(ctx, 'Signed:', -130, -40, 52, color=INKBLUE)
    text(ctx, '~ You', -110, 50, 80, color=INKBLUE)
    ctx.restore()
    stamp(ctx, '100% MATCH', 540, 820, 0.25, t, 100, -0.08)
    you(ctx, 540, 1460, 2.3, legs=None, expr='worried', look=(0, -6), arms='tense')
    for k, (qx, qy) in enumerate(((250, 1010), (830, 980))):
        glow_text(ctx, '?', qx, qy, 140, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.35 + k * 0.2))

def kitchen(ctx):
    room(ctx, hexc('bcd2c0'), hexc('8f7a62'), 1330)
    for k in range(4): shape(ctx, rect(60 + k * 250, 200, 290 + k * 250, 470), hexc('e9e1cf'), 4, 6500 + k)
    for k in range(4): shape(ctx, ell(270 + k * 250, 440, 8, 8, 10), hexc('8a8478'), 2, 6510 + k)
    shape(ctx, rect(820, 560, 1040, 1330), (0.93, 0.94, 0.95), 5, 6520)
    rough(ctx, [(820, 820), (1040, 820)], 4, 6521); rough(ctx, [(850, 620), (850, 760)], 6, 6522)

def slice_(ctx, x, y, s=1.0, rot=0, seed=6600):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    shape(ctx, [(-70, -20), (70, -20), (0, 120)], hexc('f2c35a'), 4, seed)
    shape(ctx, [(-76, -30), (76, -30), (72, -8), (-72, -8)], hexc('c78a3e'), 4, seed + 1)
    for k, (px, py) in enumerate(((-25, 15), (22, 25), (0, 62))):
        shape(ctx, ell(px, py, 13, 13, 12), hexc('b8322a'), 2, seed + 2 + k)
    ctx.restore()

def pizza_box(ctx, has_slice, sticky=0.0):
    shape(ctx, rect(290, 1020, 790, 1110), hexc('c9a06a'), 5, 6700)          # lid (inside)
    shape(ctx, [(270, 1110), (810, 1110), (840, 1185), (240, 1185)], hexc('b58a55'), 5, 6701)
    shape(ctx, [(320, 1120), (760, 1120), (780, 1170), (300, 1170)], hexc('e8d2a6'), 3, 6702)
    if has_slice: slice_(ctx, 540, 1150, 0.8, -math.pi / 2 + 0.2)
    if sticky > 0.01:
        ctx.save(); ctx.translate(540, 1062); ctx.rotate(0.05); ctx.scale(sticky * 0.55, sticky * 0.55)
        shape(ctx, rect(-110, -70, 110, 70), hexc('f6e46a'), 3, 6710)
        text(ctx, "BRUNO'S", 0, 0, 56, 'Bebas Neue', INK, anchor='c')
        text(ctx, 'TOUCH = DIE', 0, 52, 40, 'Bebas Neue', hexc('c0322a'), anchor='c')
        ctx.restore()

def s_eat(ctx, t, d, S):
    kitchen(ctx)
    tl = S.at(3, 'laugh'); te = S.at(3, 'eat') - 0.1
    desk(ctx, 140, 960, 1180, col=hexc('b38b5e'))
    u = 0.5 - 0.5 * math.cos(min(1, max(0, (t - te) / 0.5)) * math.pi)
    arms = eat_arms(u * math.pi) if t > te else 'table'
    you(ctx, 540, 820, 1.35, legs=None, expr='smile' if t < te + 0.6 else 'closed', look=(0, 6), arms=arms)
    pizza_box(ctx, t < te)
    if te < t < te + 0.7:
        hx, hy = 540 + lerp(90, 20, u) * 1.35, 820 + lerp(170, -30, u) * 1.35
        slice_(ctx, hx, hy, 0.8, -0.4 - 1.0 * u)
    glow_text(ctx, 'HA HA', 300, 420, 120, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, tl), rot=-0.1)
    glow_text(ctx, 'CHOMP', 760, 560, 140, 'Bebas Neue', GOLD, None, pop=pop(t, te + 0.55), rot=0.08)

def s_sticky(ctx, t, d, S):
    kitchen(ctx)
    ctx.save(); cam(ctx, 540, 1062, 3.2 + 0.15 * t / d)
    desk(ctx, 140, 960, 1180, col=hexc('b38b5e'))
    pizza_box(ctx, False, sticky=pop(t, 0.15, 0.25))
    ctx.restore()
    you(ctx, 540, 1560, 1.9, legs=None, expr='shock', arms='tense')
    for k in range(2):
        tt = (t * 1.4 + k * 0.5) % 1
        sweat(ctx, 700 + k * 18, 1250 + tt * 150, 1.5, alpha=1 - tt)

def s_bruno(ctx, t, d, S):
    kitchen(ctx)
    shape(ctx, rect(40, 480, 520, 1330), hexc('3b2e26'), 5, 6800)
    tsx, tb = S.at(5, 'six'), S.at(5, 'body')
    u = ease_out(min(1, t / 1.3))
    bruno(ctx, lerp(-200, 330, u), stand(1.85), 1.85, expr='blank', look=(6, 2), walk=t * 8 if t < 1.3 else None, headrot=0.08 if t < 1.0 else 0)
    you(ctx, 860, stand(0.95), 0.95, expr='shock', arms='tense', look=(-6, -4))
    if t > tsx - 0.1:
        k = ease_out((t - tsx + 0.1) / 0.4); top = stand(1.85) - 180 * 1.85
        rough(ctx, [(640, FLOOR), (640, lerp(FLOOR, top, k))], 5, 6810, GOLD)
        rough(ctx, [(615, top), (665, top)], 5, 6811, GOLD, alpha=k)
        glow_text(ctx, '6\'5"', 740, 520, 150, 'Bebas Neue', GOLD, (0.9, 0.7, 0.1), pop=pop(t, tsx + 0.2))
    stamp(ctx, 'BODYBUILDER', 540, 300, tb, t, 110, -0.08)

def s_stare(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('2a2a30')); ctx.paint(); ctx.new_path()
    radial(ctx, 540, 1000, 800, (0.9, 0.4, 0.3), 0.25)
    tc = S.at(6, 'cracks')
    z = 1.0 + 0.15 * ease_io(min(1, t / tc))
    ctx.save(); cam(ctx, 540, 1000, z)
    if t > tc: ctx.translate(10 * math.sin(t * 70) * max(0, 1 - ((t - tc) % 0.45) * 5), 0)
    bruno(ctx, 540, 1240, 2.6, arms='clasp' if t > tc - 0.3 else 'down', expr='blank', look=(0, 4), legs=None)
    ctx.restore()
    glow_text(ctx, "HE DOESN'T YELL.", 540, 300, 110, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.05))
    glow_text(ctx, 'CRACK!', 280, 560, 150, 'Bebas Neue', GOLD, None, pop=pop(t, tc), rot=-0.15)
    glow_text(ctx, 'CRACK!', 800, 720, 150, 'Bebas Neue', GOLD, None, pop=pop(t, tc + 0.45), rot=0.12)

def s_hurts(ctx, t, d, S):
    if t < 0.22:
        ctx.set_source_rgb(1, 1, 1); ctx.paint(); ctx.new_path()
        glow_text(ctx, 'POW!', 540, 900, 300, 'Bebas Neue', hexc('c0322a'), None, pop=1.0, rot=-0.1)
        return
    kitchen(ctx); dark(ctx, 0.25)
    you(ctx, 540, 1300, 2.2, band=1.0, legs=None, expr='sad', tear=(t - 0.4) / 1.2, arms='tense')
    for k in range(3):
        a = t * 4 + k * 2.09
        star(ctx, 540 + 230 * math.cos(a), 860 + 50 * math.sin(a), 30, seed=6900 + k, rot=t * 3)
    glow_text(ctx, 'EVERYTHING', 540, 280, 140, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.4))
    glow_text(ctx, 'HURTS', 540, 440, 170, 'Bebas Neue', hexc('c0322a'), (0.8, 0.1, 0.1), pop=pop(t, S.at(7, 'hurts')))

def s_write(ctx, t, d, S):
    room(ctx, hexc('2b3550'), hexc('1f2433'), 1330)
    desk(ctx, 140, 940, 1150, col=hexc('6b4a35'))
    tw = S.at(8, 'write') - 0.2
    wig = [((-68, 44), (-110, 150), (-30 + 18 * math.sin(t * 20), 196)), ((68, 44), (110, 150), (90, 185))]
    you(ctx, 540, 900, 1.35, band=1.0, legs=None, expr='worried', look=(0, 8), arms=wig if t > tw else 'table')
    n = int(len(NOTE) * min(1, max(0, (t - tw) / 1.6)))
    note_paper(ctx, 470, 1110, 300, 0.02, n=n, size=40)
    # lamp
    shape(ctx, [(820, 1150), (840, 960), (860, 1150)], hexc('3a3a3a'), 4, 6950)
    shape(ctx, [(760, 960), (920, 960), (880, 870), (800, 870)], hexc('e8c85a'), 4, 6951)
    dark(ctx, 0.3, (0.02, 0.03, 0.08))
    radial(ctx, 840, 1000, 550, (1, 0.85, 0.5), 0.35)
    glow_text(ctx, 'NOTE TO SELF', 540, 320, 120, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, S.at(8, 'pen')))

SHOTS = [(0, s_wake), (1, s_note), (2, s_hand), (3, s_eat), (4, s_sticky), (5, s_bruno), (6, s_stare), (7, s_hurts), (8, s_write), (9, s_end)]

if __name__ == '__main__':
    run(SHOTS)

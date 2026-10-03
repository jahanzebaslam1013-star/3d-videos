"""Reply All — looping stickman reel. The last shot ends on the exact first frame."""
import sys, math
sys.path.insert(0, '.')
from scenekit import *

HOOD_MAN = dict(outfit='hoodie')
TEAM = [(170, nerd, {}), (420, woman, {}), (670, lambda c, x, y, s, **k: person3(c, x, y, s, 'tee', 'short', hexc('6a4a30'), seed=2600, color=hexc('c77b3a'), **k), {})]

def team_backs(ctx, rise=1.0):
    for x, fn, kw in TEAM:
        fn(ctx, x, 1530 + (1 - rise) * 500, 1.0, legs=None, back=True, arms='down', **kw)

# ---- the rule (first shot AND last shot) ----
BOARD = [('RULE #1:', 430, 90, INK), ('ALWAYS HIT', 610, 190, hexc('1d3a8a')), ('REPLY ALL', 840, 230, hexc('c0322a'))]
POINT = [((-68, 44), (-170, 20), (-260, -10)), ((68, 44), (90, 128), (86, 206))]

def rule_scene(ctx, t, prog, arms, zoom):
    ctx.save(); cam(ctx, 540, 900, zoom)
    room(ctx, hexc('b9c4cc'), hexc('6c7775'), 1330)
    shape(ctx, rect(60, 320, 1020, 970), hexc('d8d2c4'), 6, 4000)
    shape(ctx, rect(85, 345, 995, 945), (0.98, 0.98, 0.97), 3, 4001)
    total = sum(len(s) for s, *_ in BOARD); n = int(total * prog)
    for s, y, size, col in BOARD:
        k = min(len(s), max(0, n)); n -= len(s)
        if k > 0: _partial(ctx, s, k, y, size, col)
    if prog >= 1:
        rough(ctx, [(250, 880), (830, 872)], 8, 4010, hexc('c0322a'))
    me(ctx, 880, stand(1.05), 1.05, outfit='suit', expr='smile', look=(-6, 0), arms=arms)
    team_backs(ctx)
    ctx.restore()

def _partial(ctx, s, k, y, size, col):
    ctx.select_font_face('Bebas Neue'); ctx.set_font_size(size); e = ctx.text_extents(s)
    x0 = 540 - e.width / 2 - e.x_bearing
    text(ctx, s[:k], x0, y, size, 'Bebas Neue', col)

def s_rule_hook(ctx, t, d, S):
    rule_scene(ctx, t, 1.0, POINT, 1.0 + 0.05 * ease_io(t / d))

def s_rule_end(ctx, t, d, S):
    tw0 = 0.45; tw1 = d - 0.75
    prog = 0 if t < tw0 else min(1, (t - tw0) / (tw1 - tw0))
    write = [((-68, 44), (-150, -40), (-215 + 25 * math.sin(t * 22), -140 + 12 * math.cos(t * 17))), ((68, 44), (90, 128), (86, 206))]
    if t < tw0 - 0.3:
        u = 0
    elif t < tw1:
        u = min(1, (t - tw0 + 0.3) / 0.3)
    else:
        u = 1 - ease_io((t - tw1) / 0.45)
    arms = [tuple((lerp(p[0], q[0], u), lerp(p[1], q[1], u)) for p, q in zip(a, b)) for a, b in zip(POINT, write)]
    zoom = 1.05 - 0.05 * ease_io(min(1, t / (d - 0.2)))
    rule_scene(ctx, t, prog, arms, zoom)

# ---- story ----
def screen(ctx, x0=80, y0=300, x1=1000, y1=1080):
    shape(ctx, rect(x0, y0, x1, y1), hexc('2a2d33'), 6, 4100)
    shape(ctx, rect(x0 + 30, y0 + 30, x1 - 30, y1 - 30), (0.98, 0.98, 0.98), 3, 4101)
    shape(ctx, rect(x0 + 30, y0 + 30, x1 - 30, y0 + 110), hexc('e3e6ea'), 3, 4102)

def s_typing(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('9aa6ad')); ctx.paint(); ctx.new_path()
    ctx.save(); cam(ctx, 540, 700, 1.0 + 0.05 * t / d)
    screen(ctx)
    text(ctx, 'New Message', 140, 395, 52)
    text(ctx, 'To:   dave', 140, 500, 60, color=hexc('555a60')); rough(ctx, [(140, 525), (940, 525)], 2, 4110, hexc('c3c6ca'))
    text(ctx, 'Subject:  lol', 140, 600, 60, color=hexc('555a60')); rough(ctx, [(140, 625), (940, 625)], 2, 4111, hexc('c3c6ca'))
    u = (t - S.at(1, 'This') + 0.1) / 1.7
    b1, b2 = '"This meeting could\'ve', 'been an email."'
    full = b1 + b2; s = reveal(full, u)
    text(ctx, s[:len(b1)], 140, 740, 66); text(ctx, s[len(b1):], 140, 820, 66)
    if int(t * 3) % 2 == 0 and u < 1.05:
        cx = 140 + (len(s[len(b1):]) * 28 if len(s) > len(b1) else len(s) * 28)
        rough(ctx, [(cx + 6, 690 if len(s) <= len(b1) else 770), (cx + 6, 750 if len(s) <= len(b1) else 830)], 4, 4112)
    ctx.restore()
    me(ctx, 230, 1340, 1.25, legs=None, expr='smile', look=(4, -6), arms='table', **HOOD_MAN)
    glow_text(ctx, 'TO: YOUR FRIEND', 700, 1200, 70, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, 0.15))

def s_click(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('9aa6ad')); ctx.paint(); ctx.new_path()
    tc = S.at(2, 'Reply') + 0.1
    ctx.save(); cam(ctx, 760, 820, 1.05 + 0.12 * ease_io(t / d))
    if t > tc: ctx.translate(6 * math.sin(t * 60) * max(0, 1 - (t - tc) * 3), 0)
    screen(ctx)
    for (x0, x1, lab) in ((150, 500, 'REPLY'), (580, 940, 'REPLY ALL')):
        hit = lab == 'REPLY ALL' and t > tc
        shape(ctx, rect(x0, 740, x1, 880), hexc('c0322a') if hit else hexc('e3e6ea'), 5, 4200 + x0)
        text(ctx, lab, (x0 + x1) / 2, 840, 90, 'Bebas Neue', (1, 1, 1) if hit else INK, anchor='c')
    if t > tc:
        text(ctx, 'To:  ALL STAFF (5,000)', 540, 560, 70, 'Bebas Neue', hexc('c0322a'), anchor='c', alpha=min(1, (t - tc) * 6))
    # cursor: hovers REPLY, slides to REPLY ALL
    u = ease_io(min(1, t / max(tc, 0.1)))
    cx = lerp(330, 760, ease_io(min(1, max(0, (t - tc * 0.45) / (tc * 0.55))))) if tc > 0 else 760
    cy = lerp(1020, 820, u)
    cs = 0.85 if abs(t - tc) < 0.08 else 1.0
    shape(ctx, [(cx, cy), (cx, cy + 90 * cs), (cx + 24 * cs, cy + 68 * cs), (cx + 44 * cs, cy + 106 * cs), (cx + 58 * cs, cy + 98 * cs),
                (cx + 38 * cs, cy + 62 * cs), (cx + 68 * cs, cy + 60 * cs)], (1, 1, 1), 5, 4210)
    if 0 < t - tc < 0.4:
        r = 30 + 200 * (t - tc); rough(ctx, ell(cx, cy, r, r, 30), 5, 4211, hexc('c0322a'), closed=True, alpha=1 - (t - tc) / 0.4)
    ctx.restore()

def s_inbox(ctx, t, d, S):
    ctx.set_source_rgb(*hexc('1d2228')); ctx.paint(); ctx.new_path()
    td = S.at(3, 'Ding')
    flash = t > td
    for r in range(6):
        for c in range(5):
            x = 110 + c * 215; y = 420 + r * 175
            delay = 0.05 + (r + c) * 0.07
            on = t > delay
            shape(ctx, rect(x - 85, y - 60, x + 85, y + 50), hexc('fff3c4') if flash and int(t * 8) % 2 == 0 else (hexc('dfe6ee') if on else hexc('3a4048')), 4, 4300 + r * 5 + c)
            rough(ctx, [(x, y + 50), (x, y + 75)], 5, 4330 + r * 5 + c)
            if on:
                p = pop(t, delay, 0.2)
                if p > 0.01:
                    ctx.save(); ctx.translate(x, y - 5); ctx.scale(p, p)
                    shape(ctx, rect(-40, -26, 40, 26), (1, 1, 1), 3, 4360 + r * 5 + c)
                    rough(ctx, [(-40, -26), (0, 6), (40, -26)], 3, 4390 + r * 5 + c)
                    shape(ctx, ell(38, -26, 14, 14, 12), hexc('c0322a'), 2, 4420 + r * 5 + c)
                    ctx.restore()
    n = int(5000 * min(1, t / max(td, 0.3)))
    glow_text(ctx, f'{n:,} INBOXES', 540, 260, 130, 'Bebas Neue', GOLD, (0.9, 0.7, 0.1), pop=pop(t, 0.0))
    glow_text(ctx, 'DING!', 540, 1000, 300, 'Bebas Neue', (1, 1, 1), (1, 0.8, 0.2), pop=pop(t, td, 0.25), rot=-0.06)

def s_boss(ctx, t, d, S):
    office(ctx)
    tm = S.at(4, 'My')
    ctx.save(); cam(ctx, 760, 1250, 1.0 + 0.08 * ease_io(t / d))
    boss(ctx, 290, 1360, 1.8, legs=None, expr='stern', look=(8, 0), arms='pointR')
    me(ctx, 820, 1360, 1.8, legs=None, expr='shock' if t > tm else 'worried', look=(-6, 0), arms='tense', **HOOD_MAN)
    if t > tm:
        for k in range(3):
            tt = (t * 1.3 + k * 0.33) % 1
            sweat(ctx, 930 + k * 16, 1050 + tt * 140, 1.4, alpha=1 - tt)
    ctx.restore()
    p = pop(t, 0.05)
    if p > 0.01:
        ctx.save(); ctx.translate(540, 420); ctx.scale(p, p)
        shape(ctx, rect(-440, -150, 440, 150), (1, 1, 1), 5, 4500)
        shape(ctx, ell(-350, -60, 50, 50, 24), hexc('8d8a84'), 3, 4501)
        text(ctx, 'From: BOSS', -270, -40, 70, 'Bebas Neue', INK)
        if t > tm: text(ctx, '"My office. Now."', -390, 90, 80, 'Patrick Hand', hexc('c0322a'))
        ctx.restore()
    stamp(ctx, 'FIRED?', 540, 770, tm + 0.9, t, 90, 0.12)

def s_ceo(ctx, t, d, S):
    room(ctx, hexc('5a2e30'), hexc('3b2a22'), 1330)
    for k in range(5): rough(ctx, [(k * 260, -100), (k * 260, 1330)], 6, 4600 + k, hexc('4a2426'))
    ta = S.at(5, 'Agreed'); tc = S.at(5, 'Cancel')
    radial(ctx, 540, 1100, 700, (1, 0.85, 0.4), 0.2)
    ctx.save(); cam(ctx, 540, 1200, 1.0 + 0.05 * t / d)
    ceo(ctx, 540, 1420, 2.0, legs=None, expr='smile' if t > ta else 'neutral', arms='clasp')
    ctx.restore()
    p = pop(t, 0.05)
    if p > 0.01:
        ctx.save(); ctx.translate(540, 420); ctx.scale(p, p)
        shape(ctx, rect(-440, -150, 440, 150), (1, 1, 1), 5, 4610)
        text(ctx, 'From: THE CEO', -400, -40, 70, 'Bebas Neue', hexc('8a6a1a'))
        if t > ta: text(ctx, '"Agreed. Cancel all meetings."', -400, 90, 62, 'Patrick Hand', INK)
        ctx.restore()
    stamp(ctx, 'MEETINGS CANCELLED', 540, 780, tc + 0.2, t, 90, -0.1)

def s_legend(ctx, t, d, S):
    office(ctx)
    radial(ctx, 540, 600, 700, (1, 0.85, 0.3), 0.25)
    bob = 30 * math.sin(t * 9)
    for i, (x, fn, kw) in enumerate(TEAM):
        fn(ctx, x + 70, stand(1.0) + 6 * math.sin(t * 9 + i), 1.0, expr='smile', arms='up', **kw)
    me(ctx, 540, 640 + bob, 1.0, expr='smile', arms='up', **HOOD_MAN)
    confetti(ctx, t)
    glow_text(ctx, 'LEGEND', 540, 290, 230, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=pop(t, S.at(6, 'legend') - 0.1), rot=-0.05)

def s_promo(ctx, t, d, S):
    office(ctx, wall=hexc('b9c4cc'), floor=hexc('6c7775'))
    tp, tc, tt = S.at(7, 'Promoted'), S.at(7, 'Corner'), S.at(7, 'team')
    desk(ctx, 200, 880, 1180)
    me(ctx, 540, 960, 1.2, legs=None, outfit='suit', expr='smile', arms='table')
    p = pop(t, tp)
    if p > 0.01:
        ctx.save(); ctx.translate(540, 1150); ctx.scale(p, p)
        shape(ctx, [(-160, -30), (160, -30), (180, 30), (-180, 30)], GOLD, 4, 4700)
        text(ctx, 'MANAGER', 0, 18, 60, 'Bebas Neue', INK, anchor='c')
        ctx.restore()
    glow_text(ctx, 'PROMOTED', 330, 300, 140, 'Bebas Neue', GOLD, (0.9, 0.7, 0.1), pop=pop(t, tp), rot=-0.06)
    if t > tc:
        glow_text(ctx, 'CORNER OFFICE', 800, 860, 70, 'Bebas Neue', (1, 1, 1), None, pop=pop(t, tc))
    if t > tt - 0.2:
        team_backs(ctx, ease_out((t - tt + 0.2) / 0.4))

SHOTS = [(0, s_rule_hook), (1, s_typing), (2, s_click), (3, s_inbox), (4, s_boss), (5, s_ceo), (6, s_legend), (7, s_promo), (8, s_rule_end)]

if __name__ == '__main__':
    run(SHOTS)

---
name: "stickman-pov-shorts"
description: "Make vertical 1080x1920 hand-drawn stickman story reels (20-60 s) for TikTok, Facebook Reels and YouTube Shorts: writes the script (POV or any strong hook, usually a seamless perfect loop), ElevenLabs voiceover, pycairo scenes, captions, music and SFX, then delivers the MP4 plus a TikTok/Reels title and hashtags."
---

# Stickman POV Shorts / Loop Reels

Makes vertical (1080x1920, 24 fps) reels in the hand-drawn stickman style: rough boiling black outlines, flat muted
colours, stick limbs + big anime-style heads, film grain, vignette, bold pop-in text, red stamps, speech bubbles,
white outlined captions, procedural music + SFX, narrator voiceover. Everything is drawn in code (pycairo): no
Higgsfield, no image generation. Long-form 16:9 videos are handled elsewhere; this skill is for vertical reels only.

Videos made so far with this skill (code in repo `jahanzebaslam1013-star/3d-videos`, `work/shorts/<slug>/`):
`arigato` (24 s, classic POV with fade-out), and four seamless loops: `reply_all` (28 s), `last_slice` (27 s),
`three_wishes` (52 s), `secret_recipe` (51 s). Reuse their scene code and props freely (see "Prop library").

## Talking to the user
- Reply in short, plain English. The user writes in Roman Urdu / casual English; end every reply with a one-line
  **English fix** of their message.
- Before EVERY voice generation, state the model, voice and cost (e.g. "Eleven v4, Russ, ~620 credits"), then go
  ahead (no need to wait for a yes).
- Never spend Higgsfield credits.
- Send each finished video with `SendUserFile` (display `render`) as soon as it's done; don't batch.
- When asked for "another one", write a fresh script yourself. The user likes being surprised; just say the
  title and the one-line premise before generating the voice.

## Formats
| Ask | Length | Ending |
|---|---|---|
| default / "for Facebook reel" / "TikTok" | 20-30 s (best for loops + rewatches) | **perfect loop** |
| "almost 1 minute" | 50-60 s (~115-130 words + pauses) | **perfect loop** |
| user gives a POV script with a punchline | whatever the script gives | emotional close-up + fade to black (classic) |

Default to a **perfect loop** unless the user's own script clearly ends on a punchline that needs a fade.
The hook doesn't have to be "POV:"; use whatever stops the scroll (a rule, a contradiction, a whisper, a mystery).

## Writing a perfect-loop script (the most important part)
Rules that made the four loop videos work:
1. **The last line flows grammatically into the first line.** Read them aloud joined:
   - "...you give them one piece of advice: / Always hit Reply All on a company email."
   - "...slip it in your pocket... and fall asleep. / You wake up with a note in your pocket."
   - "...walking home. And then... / You kick an old, dusty lamp."
   - "...You lean in close and whisper... / 'The secret ingredient...' Grandpa whispers."
2. **The first line is also a strong standalone hook** (it's what new viewers hear first).
3. **The last shot ends on the exact first frame**: same scene, same character positions/poses, same camera zoom.
   Animate the last shot *into* the opening composition (text being written onto a whiteboard, lying back down in
   bed, walking into the spot, leaning into the whisper).
4. Great loop shapes: a time loop (note to self), a generational loop (grandpa is the old you, drawn identically:
   same hair shape in grey), a reset (wish/poof back to the start), an ironic rule/advice that IS the hook.
5. Anything that changes during the story (bandages, grey hair, lights) must be undone by the last frame (e.g. the
   bandage fades with a sparkle as he falls asleep).
6. No fade-out, no music fade, no on-screen text in frame 0 (titles pop in from t≈0.3 s, so frame 0 is clean
   and matches the clean last frame).
7. Structure: hook (0-3 s) → escalating beats every 2-4 s → twist ~70% in → the reset line.
   ~2.3 words/s with Russ; 60-70 words ≈ 28 s, 115-125 words + pauses ≈ 51 s.

## Workflow

### 0. Setup (once per container, ~1 min)
```bash
pip install --break-system-packages -q pycairo pillow soundfile scipy
mkdir -p ~/.fonts && cd ~/.fonts
for f in ofl/creepster/Creepster-Regular.ttf ofl/patrickhand/PatrickHand-Regular.ttf ofl/bebasneue/BebasNeue-Regular.ttf; do
  curl -sSL -o $(basename $f) https://raw.githubusercontent.com/google/fonts/main/$f; done
fc-cache -f
```
(If the repo is cloned, the fonts are also in `work/project/fonts/`; the kit files are in any `work/shorts/<slug>/`.)
Create `work/shorts/<slug>/` and write `stickkit.py`, `sfxkit.py`, `scenekit.py`, `prep_vo.py` from the code
blocks at the bottom of this file **verbatim**, plus a `.gitignore`:
`p*.mp4 video.mp4 l.txt *.log *.wav test_*.png __pycache__/` (the repo root already ignores `*.mp4`/`*.mp3`).

### 1. Script
- Use the user's script, or write one (see the loop rules above). One narration line per row in `script.txt`
  (short sentences; each row becomes one caption). Strip stage directions but use them as shot ideas.

### 2. Voiceover (ElevenLabs)
- Voice **Russ – Deep American Narrator**, voice_id `t0eCaS57KWbQQc1wRkah`, model `eleven_v4`,
  `generations_count=1`, lines separated by blank lines. Cost ≈ 1 credit per character; say it first.
- Poll `creative_get_flow_run_status`; when done, the result has `media[0].url` (a signed storage.googleapis.com
  URL). In the cloud workspace you can **download it directly**: `curl -sS -o vo.mp3 '<url>'`.
  (Only if that's blocked: ask the user to download it from the flow link into their Stickman claude folder.)
- Fallback without ElevenLabs: Kokoro TTS (`kokoro-onnx`, voice `am_michael`, speed 0.95).

### 3. Timings + pauses + trim (`prep_vo.py`)
```bash
python3 prep_vo.py vo.mp3 "3:0.3,7:0.4,14:0.6,15:0.6"          # loop
python3 prep_vo.py vo.mp3 "0:0.3,6:0.3,9:0.9" --tail 3.4         # classic ending with a 3.4 s reaction tail
```
It prints the aligned table (check each line's duration looks right), inserts silence before the given line
indices (dramatic beats: before the twist, before "Poof", before the punchline word), trims the start to 0.06 s
before the first word and the end to `--tail` after the last word (default 0.38 s, so the loop gap is a natural
~0.45 s breath), and writes `vo_rt.wav` + `lt.json`. **Video length = `vo_rt.wav` length** (scenekit.END).

### 4. Plan shots
- One shot per 1-3 lines; a new visual every 2-4 s. Every shot moves: slow `cam` push-in, `pop()` text,
  stamps, walk cycles, bobbing, shake on impacts, sweat drops, flashes.
- Visualise the words literally and comically ("five thousand inboxes" → grid of 30 monitors with envelope badges
  and a rolling counter; "six-foot-five bodybuilder" → a gold height bar + BODYBUILDER stamp).
- Keep one main "you" character recognisable all video (hero, spiky hair). Outfit can change with the story
  (hoodie employee → suit manager), which helps the arc read.

### 5. Build `short.py` (template below)
Layout: faces between y≈300-1400; captions sit at y≈1640 so keep the bottom 350 px free of key visuals; big title
text at y≈250-650. Standing: `y = stand(s)` (feet on FLOOR=1450) or `stand(s, floor)`. Bust/close-up:
`legs=None`, scale 1.8-3.4, y ≈ 1300-1550. Seated behind a table: `legs=None`, y so the torso bottom
(`y + 200*s`) sits just below the table top.

**Characters** (`stickkit`): `hero` ("YOU"; `outfit='hoodie'|'suit'|'vest'|'tee'|'cardi'`, `color=`), `suit_man`
(sunglasses agent/spy), `doctor`, `officer`, `leader`, `old_man`, `old_woman`, `kid`, `nerd`, `woman`, or
`person3(...)` for anything custom. `scenekit` adds `me` (hero in light-blue shirt + tie), `boss` (bald, moustache),
`ceo` (white hair, full beard, gold tie).
Common kwargs: `expr` = neutral/smile/shock/worried/sad/stern/blank/closed (blank = half-lidded menacing stare);
`look=(dx,dy)`; `arms` = down/table/grip/clasp/reachR/reachL/holster/up/shrug/pointR/pointL/wave/tense or custom
`[(shoulder),(elbow),(hand)]*2` in local coords (shoulders at (±68,44), mouth ≈ (0,-40), eyes at (±24,-80));
`legs='stand'|None`; `walk=phase`; `rot`; `headrot`; `tear=0..1.2`; `glasses='sun'|'round'`; `beard='mous'|'full'`;
`wrinkles`; `cap=`; `back=True` (seen from behind: great for an audience/team in the foreground); `skin=` (blue
genie: `hexc('6aa5e0')`); `width=` (1.9 = bodybuilder); `flip`; `extra='bald'|'bun'|'scar'`.
Hair styles: spiky, spiky_s, short, slick, bob, crew, none.

**Animation tricks that worked**
- Pose blends: `lerp_arms(A, B, u)` between two arm lists (whisper lean, pointing→writing, hold→pocket).
- Pivot rotation for bowing / lying down / sitting up: `ctx.translate(hip); ctx.rotate(a);` then draw the person at
  `(0, -200*s)` with `legs=None` (legs drawn separately if needed). Lying in bed = rotate −π/2 about the hip.
- Text being written: reveal characters with `prog` and draw each line left-aligned from where its centred
  version would start (so letters don't slide).
- Walk loop that matches at the seam: `walk = 2π * round(END*1.6) * (S.t0 + t) / END`.
- Overlays drawn in the character's local frame (bandage, zipped lips, wink): `ctx.translate(x,y); ctx.rotate(rot);
  ctx.scale(s,s)` then draw at head coords (head centre (0,-95), radius ≈ 60x70).
- Muscles: skin-coloured ellipses along upper arm / forearm, drawn after the body.
- Day/night: `tint(night, day, light)` for wall/sky + `dark(ctx, 0.38*(1-light))` overlay.

**Helpers**: stickkit `shape`, `rough`, `ell`, `rect`, `bez`, `text`, `glow_text`, `stamp`, `say`, `bubble`, `sweat`,
`radial`, `dark`, `vignette`, `cam`, `room`, `sky`, `pine`, `bush`, `hills`, `van`, `clock`, `tally`, `price_tag`,
`rec_frame`, `grayscale_surface`, `eat_arms(phase)`, easing `ease_out_back/ease_out/ease_io/lerp`, `tint`;
scenekit `pop(t,t0)`, `office`, `desk`, `paper`, `star`, `confetti`, `strike`, `reveal`, `arm_to`, `stand`.
Colours: `INK, SKIN, HAIR, HOOD, SUIT, BURG, GOLD, RED, GREEN, PAPER`, `hexc('rrggbb')`.
Fonts: 'Bebas Neue' (titles/labels/stamps), 'Creepster' (horror), 'Patrick Hand' (captions/handwriting/bubbles).

### 6. Check before rendering
`python3 short.py --tl` prints the shot timeline. Render one frame per shot
(`python3 short.py 0 1.5 4.5 ... <END-0.02>` → `test_*.png`), paste into a contact sheet with PIL, and LOOK at it.
Fix: heads cut off, bubbles/text covering faces, props covering faces (a pizza-box lid hid the hero, a cookie plate
covered grandpa, a NO PRESSURE stamp covered a face), characters bumping heads when bowing, text appearing too late
(start a "being written" animation right at the line start, not at a later word), anything nonsense (a "bathrobe"
must not use the general's `white` outfit with medals; use `tee` in white). Then re-render only the fixed frames.

### 7. Render
Two parts for ≤30 s, three parts for ~50 s, in the background:
```bash
N=$(python3 -c "import scenekit as s; print(int(round(s.END*24)))"); A=$((N/3)); B=$((2*N/3))
for r in "0 $A p0.mp4" "$A $B p1.mp4" "$B $N p2.mp4"; do set -- $r; nohup python3 short.py --range $1 $2 $3 > r_$3.log 2>&1 & done
# write mix.py while it renders; then wait with a poll loop (sleep 10 until no "short.py --range" processes)
printf "file 'p0.mp4'\nfile 'p1.mp4'\nfile 'p2.mp4'\n" > l.txt && ffmpeg -y -f concat -safe 0 -i l.txt -c copy video.mp4
```

### 8. Music + SFX (`mix.py`)
```python
import numpy as np, sfxkit as A, scenekit as K, short
END = K.END; m = A.Mix(END + 4)                       # +4 s so sounds past the end survive to be wrapped
TL = {n: a for a, b, n in K.timeline_of(short.SHOTS)}  # shot name -> global start time
S = lambda n: short.Sc(TL[n])                          # S('s_boss').at(4, 'My') = local time of a word
N = int(round(END / 0.26 / 8)) * 8; beat = END / N     # beat grid that divides the loop exactly
for k in range(N): ...                                 # per-section plucks/bass (cozy, tense, magic, sneaky...)
m.sfx(A.sfx_stamp(), TL['s_boss'] + S('s_boss').at(4, 'My') + 0.9, -10)
K.render_loop(m, 'vo_rt.wav', 'mix.wav')               # LOOP: wraps overflow onto the start, no fade
# classic (non-loop) videos: m = A.Mix(END) ... m.render('vo_rt.wav', 'mix.wav')  (ducks + fades out)
```
- Mood palette: comedy = `pluck` pizzicato arpeggio + bass on every other beat; tension = low `pad` drone +
  `boom` pulse (accelerate toward the twist); magic/genie = E phrygian-dominant plucks `[64,65,68,69,71,72,74,76]`;
  cozy/family = music-box plucks on a 3/4 grid (multiple of 12); sneaky = staccato low plucks; dread = detuned
  high cluster; sad = slow `pluck` + `verb`, or a sad-trombone (four falling sawtooth notes 58-57-56-55, last with vibrato).
- Cut the music before a punchline with `sfx_tape_stop()`, then leave silence (crickets, a stare) for the beat.
- SFX on every pop-in, stamp, cut and impact: `sfx_pop`, `sfx_stamp`, `sfx_hit`, `sfx_ding`, `whoosh`, `sfx_step`,
  `sfx_heartbeat`, `sfx_tick`, `sfx_tape_stop`, `sfx_power_down`. Recipes made from primitives: typing (short `nh`
  clicks every 0.12 s), mouse click, phone ring (alternating 1400/1750 Hz beeps), camera shutter, knuckle crack,
  chomp, crickets (4.3 kHz chirp triplets), zipper (10 tiny `nh` ticks), paper rustle, whisper hiss, crowd murmur
  (`verb(nh(1.5, 400, 3000, 1.2))`). Use `A.mix(a, b)` for arrays of different lengths (never `a + b`).
- For loops, put a sound that crosses the seam (a whisper, a pad, footsteps) so the join feels continuous.
- Target ≈ -14 to -16 LUFS integrated (`ffmpeg -i mix.wav -af ebur128 -f null - 2>&1 | grep "I:"`).

### 9. Encode, verify, deliver
```bash
ffmpeg -y -i video.mp4 -i mix.wav -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest <Title>_loop_reel.mp4
```
- crf 23 for ≤30 s (~17 MB); crf 25 for ~50 s (~20-22 MB).
- ffprobe: 1080x1920, 24 fps, duration ≈ END.
- **Loop seam check** (loops): grab the last and first frames
  (`ffmpeg -sseof -0.05 -i video.mp4 -frames:v 1 last.png`, `-i video.mp4 -frames:v 1 first.png`), put them
  side by side and LOOK. Only line boil, grain and the caption may differ.
- `SendUserFile` the MP4 (display `render`), then commit the project folder (code, script, timings, mix) and push
  to the session branch. MP4/MP3 stay out of git (root `.gitignore`), so the user saves the video from the file card.
- On a Mac/Cowork setup instead: copy to `/Users/mbp/Documents/Stickman claude/Shorts/<title>.mp4` via
  `device_commit_files` (must be under 20 MB; raise crf if needed).

### 10. Reply + upload package
Reply with: the script as a one-line flow (→ arrows, ↺ for the loop), what the loop trick is, length/specs,
voice credits used, where the code is, then the **English fix**. If the user asks for upload text, give per video:
- **TikTok caption** = hook line + emoji + `#fyp` (TikTok shows the caption as the title), e.g.
  "Accidentally hit Reply All… best mistake of my career 📧😂 #fyp"
- **Hashtags**: `#fyp #foryou` + 2-3 topic tags + 2-3 format tags (`#stickman #animation #loop #storytime
  #plottwist #funny`); 5-8 total is best.
- Tips: pin a comment like "Did you notice it loops? 👀" (rewatches boost reach); put the hook as on-screen text in
  the first second; for Facebook/Instagram swap `#fyp #foryou` for `#reels #reelsviral`.

## Prop library (copy from past videos in `work/shorts/`)
- `reply_all/short.py`: whiteboard with hand-written text reveal, email/laptop screen UI with typing + cursor,
  REPLY / REPLY ALL buttons + mouse cursor click ripple, grid of inbox monitors with badges, email notification card,
  team seen from behind, legend lift + confetti, corner office + MANAGER nameplate.
- `last_slice/short.py`: bedroom with bed/pillow/blanket + day↔night, lying/sitting-up pivot, note paper with
  handwriting reveal, kitchen (cabinets, fridge), pizza box + slice + `eat_arms`, sticky note, bodybuilder roommate
  (`width=1.9` + muscles), height bar, POW flash, bandages, circling stars, desk lamp glow.
- `three_wishes/short.py`: magic lamp, genie with smoke tail, smoke puffs, purple starry bg, dusk city street with lit
  windows + streetlamp, phone bank app with counter, money rain, money bag split in half, crowd of cousins, calendar,
  empty wallet + moth, magazine/TV/billboard, house with paparazzi flashes, bathroom + shower curtain, store shelves.
- `secret_recipe/short.py`: warm kitchen with hanging lamp, table + cookie plate, old-you grandpa, wink overlay,
  zipped lips, bakery boxes, drawer with glow, briefcase of cash, spy head-first in a trash can, birthday cake.
- `arigato/short.py`: résumé paper, Japanese flag, HIRED stamp, bowing (`bower`), thought cloud with struck-out words.

## Gotchas (learned the hard way)
- Always `ctx.new_path()` after `ctx.paint()` following a `ctx.rectangle(...)`, otherwise the next `shape()` fills
  the whole canvas.
- Set `K.W, K.H` before `grain_layers()` / any drawing (scenekit does this).
- `K.BOIL = frame // 2` every frame (scenekit's runner does it).
- `glow_text(..., pop=...)` returns nothing when pop <= 0.01, so compute pop from local time with `pop(t, t0)`.
- `sfxkit.Mix(dur)` only keeps 1 s past `dur`; for loops create it with `END + 4` and use `render_loop`.
- Long renders: always `nohup ... &` in parallel parts and poll; never block one tool call > 10 min.
- `prep_vo.py` always starts again from `vo.mp3`, so re-running it with different pauses is safe.
- Avoid real brand names on screen (use "TOWN BAKERY", "STAR WEEKLY", "MY BANK").

## Code — write these files verbatim

### stickkit.py
```python
"""stickkit — hand-drawn stickman story kit (pycairo). Self-contained."""
import math, random, cairo, numpy as np

W, H, FPS = 1080, 1920, 24  # override for 16:9

def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

INK = hexc('17171a'); SKIN = hexc('f1dcc4'); HAIR = hexc('1f1f24'); HOOD = hexc('5f6e45')
HOOD_D = hexc('4a5735'); PAPER = hexc('f3efe4'); SKY1 = hexc('aeb6ae'); SKY2 = hexc('d9dbd1')
SUIT = hexc('1e2024'); COAT = hexc('eef0ee'); UNIF = hexc('4f5d6b')
SUITC = hexc('1e2024'); WHITEJ = hexc('efece2'); OLIVE = hexc('5c6446'); CARDI = hexc('8a6a4a'); TEE = hexc('4f79b8')
VEST = hexc('7d8288'); BURG = hexc('6e2a2e'); GOLD = hexc('c9a24a'); RED = hexc('c0322a'); GREEN = hexc('2f9e4f')
BOIL = 0  # set to frame//2 each frame for line boil

def ease_out_back(x, s=1.8):
    x = min(max(x, 0), 1); x -= 1
    return x * x * ((s + 1) * x + s) + 1

def ease_out(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def ease_io(x):
    x = min(max(x, 0), 1); return x * x * (3 - 2 * x)

def lerp(a, b, u): return a + (b - a) * u

def jit_pts(pts, seed, amp, step=16):
    rng = random.Random(seed)
    out = []
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]; x1, y1 = pts[i + 1]
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        for k in range(n):
            u = k / n; out.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u))
    out.append(pts[-1])
    offs = [(rng.uniform(-amp, amp), rng.uniform(-amp, amp)) for _ in out]
    n = len(out)
    res = []
    for i, (x, y) in enumerate(out):
        a = offs[max(i - 1, 0)]; b = offs[i]; c = offs[min(i + 1, n - 1)]
        res.append((x + (a[0] + 2 * b[0] + c[0]) / 4, y + (a[1] + 2 * b[1] + c[1]) / 4))
    return res

def poly(ctx, pts, close=True):
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    if close: ctx.close_path()

def rough(ctx, pts, w=4, seed=1, color=INK, closed=False, amp=1.4, alpha=1.0):
    if closed: pts = list(pts) + [pts[0]]
    rng = random.Random(seed * 13 + BOIL * 7919)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for i, (wm, a) in enumerate(((1.0, 1.0), (0.5, 0.65))):
        p = jit_pts(pts, seed * 97 + BOIL * 131 + i * 17, amp)
        poly(ctx, p, close=False)
        ctx.set_source_rgba(*color, a * alpha)
        ctx.set_line_width(max(0.6, w * wm * rng.uniform(0.85, 1.15)))
        ctx.stroke()

def shape(ctx, pts, fill, w=4, seed=1, ink=INK, amp=1.4, alpha=1.0):
    poly(ctx, pts); ctx.set_source_rgba(*fill, alpha); ctx.fill()
    if w > 0: rough(ctx, pts, w, seed, ink, closed=True, amp=amp, alpha=alpha)

def ell(cx, cy, rx, ry, n=40, a0=0, a1=2 * math.pi):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / n), cy + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + (0 if a1 - a0 >= 6.28 else 1))]

def bez(p0, p1, p2, p3, n=24):
    out = []
    for i in range(n + 1):
        u = i / n; v = 1 - u
        out.append((v**3 * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u**3 * p3[0],
                    v**3 * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u**3 * p3[1]))
    return out

def text(ctx, s, x, y, size, font='Patrick Hand', color=INK, anchor='l', alpha=1.0):
    ctx.select_font_face(font); ctx.set_font_size(size)
    ext = ctx.text_extents(s)
    if anchor == 'c': x -= ext.width / 2 + ext.x_bearing
    ctx.move_to(x, y); ctx.set_source_rgba(*color, alpha); ctx.show_text(s)

def sweat(ctx, x, y, s=1.0, alpha=1.0):
    pts = [(x, y - 16 * s)] + bez((x, y - 16 * s), (x + 12 * s, y), (x + 8 * s, y + 10 * s), (x, y + 10 * s), 8)[1:] + \
          bez((x, y + 10 * s), (x - 8 * s, y + 10 * s), (x - 12 * s, y), (x, y - 16 * s), 8)[1:]
    shape(ctx, pts, hexc('8fd0f2'), 2.6, 77, alpha=alpha)

def sky(ctx, top=SKY1, bot=SKY2, h=None):
    h = h or H
    g = cairo.LinearGradient(0, 0, 0, h); g.add_color_stop_rgb(0, *top); g.add_color_stop_rgb(1, *bot)
    ctx.rectangle(-400, -400, W + 800, H + 800); ctx.set_source(g); ctx.fill()

def pine(ctx, x, base, h, col, seed, w=3, dark=None):
    rng = random.Random(seed)
    rough(ctx, [(x, base), (x, base - h * 0.25)], w + 2, seed, hexc('3a3128'))
    tiers = 3
    for i in range(tiers):
        tb = base - h * 0.18 - i * h * 0.24
        tw = h * (0.34 - i * 0.08)
        tt = tb - h * 0.42
        pts = [(x - tw, tb)]
        for k in range(1, 4):
            pts.append((x - tw + tw * 0.33 * k, tb - rng.uniform(4, 12)))
        pts += [(x + tw, tb), (x + tw * 0.25, tt + h * 0.12), (x + tw * 0.45, tt + h * 0.14), (x, tt),
                (x - tw * 0.45, tt + h * 0.14), (x - tw * 0.25, tt + h * 0.12)]
        shape(ctx, pts, col, w, seed + i * 3)

def bush(ctx, x, base, r, col, seed, w=3):
    rng = random.Random(seed)
    pts = []
    n = 14
    for i in range(n + 1):
        a = math.pi + math.pi * i / n
        rr = r * rng.uniform(0.8, 1.1)
        pts.append((x + rr * 1.3 * math.cos(a), base + rr * math.sin(a)))
    shape(ctx, pts, col, w, seed)

def hills(ctx, y, amp, col, seed, off=0, w=3):
    rng = random.Random(seed)
    pts = [(-300, H + 50)]
    xs = list(range(-300, W + 400, 160))
    hs = [rng.uniform(0, amp) for _ in xs]
    for i, xx in enumerate(xs):
        pts.append((xx - off % 160, y - hs[i]))
    pts.append((W + 400, H + 50))
    shape(ctx, pts, col, w, seed, amp=2)

def van(ctx, x, y, s, dist, seed=900):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    shape(ctx, ell(0, 4, 300, 16, 24), (0, 0, 0), 0, 0, alpha=0.25)
    body = [(-262, -42), (-262, -196), (-234, -226), (104, -226), (168, -160), (248, -132), (262, -96), (262, -42)]
    shape(ctx, body, hexc('26292e'), 5, seed, ink=hexc('0b0b0c'))
    shape(ctx, [(114, -212), (160, -162), (114, -162)], hexc('56616c'), 3, seed + 1, ink=hexc('0b0b0c'))
    shape(ctx, [(-230, -206), (-40, -206), (-40, -160), (-230, -160)], hexc('3d454e'), 3, seed + 2, ink=hexc('0b0b0c'))
    shape(ctx, [(-20, -206), (96, -206), (96, -160), (-20, -160)], hexc('3d454e'), 3, seed + 3, ink=hexc('0b0b0c'))
    rough(ctx, [(-200, -200), (-160, -166)], 3, seed + 4, hexc('8a95a0'))
    rough(ctx, [(100, -150), (100, -50)], 3, seed + 5, hexc('0b0b0c'))
    rough(ctx, [(-262, -100), (262, -100)], 2.5, seed + 6, hexc('3c4046'))
    shape(ctx, ell(250, -116, 10, 8, 10), hexc('f3e3a0'), 2, seed + 7)
    for wx in (-160, 168):
        shape(ctx, ell(wx, -40, 48, 48, 28), hexc('0f0f10'), 4, seed + wx)
        shape(ctx, ell(wx, -40, 19, 19, 16), hexc('80868d'), 3, seed + wx + 1)
        a0 = dist / 48
        for k in range(4):
            a = a0 + k * math.pi / 2
            rough(ctx, [(wx, -40), (wx + 16 * math.cos(a), -40 + 16 * math.sin(a))], 2.5, seed + wx + 2 + k, hexc('2c2f33'))
    ctx.restore()

def grain_layers():
    rng = np.random.default_rng(3); outs = []
    for i in range(4):
        n = rng.random((H, W)); a = np.zeros((H, W, 4), np.uint8)
        alpha = np.zeros((H, W)); val = np.zeros((H, W))
        alpha[n < 0.10] = 26; alpha[n > 0.93] = 18; val[n > 0.93] = 255
        a[..., 3] = alpha.astype(np.uint8); pm = (val * alpha / 255).astype(np.uint8)
        a[..., 0] = pm; a[..., 1] = pm; a[..., 2] = pm
        outs.append(cairo.ImageSurface.create_for_data(bytearray(a.tobytes()), cairo.FORMAT_ARGB32, W, H, W * 4))
    return outs

def vignette(ctx, strength=0.45, col=(0, 0, 0)):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.05)
    g.add_color_stop_rgba(0, *col, 0); g.add_color_stop_rgba(1, *col, strength)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()

def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

HAIRS = {
 'spiky': [(-66, -78), (-80, -118), (-62, -120), (-70, -160), (-42, -150), (-34, -188), (-8, -162), (10, -194), (26, -160),
           (54, -182), (50, -146), (80, -142), (64, -114), (78, -84), (58, -104), (44, -122), (30, -112), (16, -126), (0, -112),
           (-14, -128), (-28, -112), (-44, -124), (-56, -100)],
 'short': [(-64, -86), (-68, -128), (-50, -160), (-20, -172), (20, -172), (50, -160), (68, -128), (64, -86), (54, -114),
           (30, -128), (0, -122), (-30, -130), (-56, -110)],
 'slick': [(-63, -92), (-66, -134), (-44, -166), (0, -174), (44, -166), (66, -134), (63, -92), (56, -118), (20, -140),
           (-20, -136), (-56, -118)],
 'bob': [(-70, -36), (-76, -120), (-52, -166), (0, -178), (52, -166), (76, -120), (70, -36), (54, -40), (56, -110),
         (30, -132), (-10, -126), (-50, -112), (-54, -40)],
}

HAIRS['crew'] = [(-62, -96), (-64, -140), (-50, -160), (50, -160), (64, -140), (62, -96), (52, -126), (-52, -126)]

HAIRS['spiky_s'] = [(-64, -84), (-72, -120), (-56, -122), (-60, -152), (-36, -144), (-26, -172), (-4, -150), (12, -176),
                      (26, -150), (48, -166), (46, -138), (70, -132), (58, -110), (66, -86), (52, -104), (30, -116), (0, -110),
                      (-30, -116), (-54, -100)]

def head2(ctx, hair='spiky', hcol=HAIR, expr='neutral', look=(0, 0), glasses=None, beard=None, wrinkles=False,
          cap=None, back=False, tear=None, seed=100):
    for sx in (-1, 1):
        shape(ctx, ell(sx * 60, -88, 12, 16, 16), SKIN, 3.5, seed + sx)
    if back:
        shape(ctx, ell(0, -95, 60, 70), hcol if cap is None else hexc('d9c3a9'), 4.5, seed + 3)
        if cap is not None:
            shape(ctx, [(-62, -118), (-58, -168), (58, -168), (62, -118)], cap, 4, seed + 60)
        return
    shape(ctx, ell(0, -95, 60, 70), SKIN, 4.5, seed + 3)
    if expr == 'shock':
        for i in range(5):
            rough(ctx, [(-40 + i * 9, -118), (-40 + i * 9, -104)], 2.2, seed + 40 + i, hexc('5a74a8'))
    if wrinkles:
        for k in range(2):
            rough(ctx, [(-26, -136 + k * 9), (-6, -139 + k * 9), (14, -136 + k * 9)], 2, seed + 45 + k, hexc('a88a70'))
        for sx in (-1, 1):
            rough(ctx, [(sx * 34, -58), (sx * 42, -64)], 2, seed + 47 + sx, hexc('a88a70'))
    for sx in (-1, 1):
        ex, ey = sx * 24, -80; lx, ly = look
        if glasses == 'sun':
            continue
        if expr == 'closed':
            rough(ctx, bez((ex - 12, ey), (ex - 4, ey + 7), (ex + 4, ey + 7), (ex + 12, ey), 8), 3.2, seed + 10 + sx)
        else:
            shape(ctx, ell(ex, ey, 14, 18, 24), (1, 1, 1), 3.2, seed + 10 + sx)
            if expr == 'shock':
                shape(ctx, ell(ex + lx, ey + ly, 3.5, 4.5, 12), INK, 0, 0)
            else:
                shape(ctx, ell(ex + lx, ey + 2 + ly, 9, 12, 20), INK, 0, 0)
                shape(ctx, ell(ex + lx - 3, ey - 3 + ly, 3.4, 3.4, 10), (1, 1, 1), 0, 0)
            if expr in ('blank', 'sad'):
                lid = [(ex - 15, ey - 2), (ex - 15, ey - 20), (ex + 15, ey - 20), (ex + 15, ey - 2)] if expr == 'blank' else \
                      [(ex - 15, ey - 6 - (sx * 5)), (ex - 15, ey - 20), (ex + 15, ey - 20), (ex + 15, ey - 6 + sx * 5)]
                shape(ctx, lid, SKIN, 0, 0)
                rough(ctx, [lid[0], lid[3]], 3, seed + 12 + sx)
        if expr == 'shock':
            rough(ctx, [(ex - 12, ey - 34), (ex + 12, ey - 36)], 3.5, seed + 20 + sx)
        elif expr in ('worried', 'sad'):
            rough(ctx, [(ex - sx * 13, ey - 34), (ex + sx * 11, ey - 24)], 3.5, seed + 20 + sx)
        elif expr == 'stern':
            rough(ctx, [(ex - sx * 13, ey - 30), (ex + sx * 11, ey - 24)], 3.5, seed + 20 + sx)
        else:
            rough(ctx, [(ex - 11, ey - 27), (ex + 11, ey - 28)], 3.5, seed + 20 + sx)
    if glasses == 'sun':
        for sx in (-1, 1):
            shape(ctx, [(sx * 6, -92), (sx * 40, -94), (sx * 38, -70), (sx * 10, -70)], hexc('0d0d10'), 3, seed + 14 + sx)
            rough(ctx, [(sx * 14, -88), (sx * 22, -82)], 2, seed + 16 + sx, hexc('6c737c'))
        rough(ctx, [(-6, -88), (6, -88)], 3, seed + 18)
        rough(ctx, [(-10, -130), (-30, -126)], 3.5, seed + 19); rough(ctx, [(10, -130), (30, -126)], 3.5, seed + 19)
    elif glasses == 'round':
        for sx in (-1, 1):
            rough(ctx, ell(sx * 24, -80, 20, 20, 20), 2.5, seed + 14 + sx, closed=True)
        rough(ctx, [(-4, -82), (4, -82)], 2.5, seed + 18)
    rough(ctx, [(2, -64), (-2, -54), (3, -53)], 2.4, seed + 30)
    if beard == 'full':
        shape(ctx, [(-58, -80), (-52, -40), (-26, -12), (0, -6), (26, -12), (52, -40), (58, -80), (40, -60), (20, -48),
                    (-20, -48), (-40, -60)], hcol, 3, seed + 32)
    if expr == 'shock':
        shape(ctx, ell(0, -36, 9, 12, 18), hexc('4a1f1f'), 3.2, seed + 31)
    elif expr in ('sad', 'worried'):
        rough(ctx, bez((-13, -34), (-5, -42), (5, -42), (13, -34), 8), 3, seed + 31)
    elif expr == 'stern' or glasses == 'sun':
        rough(ctx, [(-13, -38), (13, -38)], 3.2, seed + 31)
    elif expr == 'smile':
        rough(ctx, bez((-16, -42), (-6, -32), (6, -32), (16, -42), 8), 3, seed + 31)
    else:
        rough(ctx, bez((-12, -40), (-4, -37), (5, -37), (12, -40), 8), 3, seed + 31)
    if beard in ('mous', 'full'):
        shape(ctx, [(-24, -46), (-4, -54), (4, -54), (24, -46), (14, -44), (0, -48), (-14, -44)], hcol, 2.5, seed + 33)
    if cap is not None:
        for sx in (-1, 1):
            shape(ctx, [(sx * 58, -84), (sx * 66, -122), (sx * 50, -122), (sx * 48, -96)], hcol, 2.5, seed + 55 + sx)
        shape(ctx, [(-62, -118), (-58, -172), (58, -172), (62, -118)], cap, 4, seed + 60)
        shape(ctx, [(-70, -116), (70, -116), (60, -104), (-60, -104)], hexc('15181b'), 3, seed + 61)
        shape(ctx, ell(0, -145, 10, 12, 12), hexc('e3c24a'), 2.5, seed + 62)
    elif hair in HAIRS:
        shape(ctx, HAIRS[hair], hcol, 3.5, seed + 50)
    if tear is not None and tear > 0:
        ty = -72 + 70 * min(tear, 1)
        sweat(ctx, -30, ty, 0.55, alpha=min(1, tear * 5) * (1 - max(0, tear - 1.2) * 3))

def glow_text(ctx, s, x, y, size, font, fill, glow, pop=1.0, rot=0, alpha=1.0, outline=hexc('111111')):
    if pop <= 0.01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(pop, pop)
    ctx.select_font_face(font); ctx.set_font_size(size); e = ctx.text_extents(s)
    x0 = -e.width / 2 - e.x_bearing; y0 = e.height / 2
    ctx.move_to(x0 + 10, y0 + 12); ctx.text_path(s); ctx.set_source_rgba(0, 0, 0, 0.5 * alpha); ctx.fill()
    if glow:
        for lw, a in ((40, 0.07), (26, 0.12), (14, 0.22)):
            ctx.move_to(x0, y0); ctx.text_path(s); ctx.set_source_rgba(*glow, a * alpha); ctx.set_line_width(lw)
            ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
    ctx.move_to(x0, y0); ctx.text_path(s); ctx.set_source_rgba(*fill, alpha); ctx.fill_preserve()
    ctx.set_source_rgba(*outline, alpha); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()

def cam(ctx, cx, cy, s):
    ctx.translate(cx, cy); ctx.scale(s, s); ctx.translate(-cx, -cy)

def dark(ctx, a, col=(0.02, 0.03, 0.05)):
    ctx.rectangle(-500, -500, W + 1000, H + 1000); ctx.set_source_rgba(*col, a); ctx.fill()

def radial(ctx, x, y, r, col, a):
    g = cairo.RadialGradient(x, y, 1, x, y, r); g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
    ctx.arc(x, y, r, 0, 7); ctx.set_source(g); ctx.fill()

def stamp(ctx, s, x, y, t0, t, size=120, rot=-0.18):
    if t < t0: return
    sc = lerp(1.8, 1.0, ease_out((t - t0) / 0.12))
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc)
    ctx.select_font_face('Bebas Neue'); ctx.set_font_size(size); e = ctx.text_extents(s)
    red = hexc('c0322a'); a = min(1, (t - t0) / 0.08) * 0.92
    pad = 26
    rough(ctx, rect(-e.width / 2 - pad, -e.height / 2 - pad, e.width / 2 + pad, e.height / 2 + pad), 9, 999, red, closed=True, alpha=a)
    ctx.move_to(-e.width / 2 - e.x_bearing, e.height / 2); ctx.set_source_rgba(*red, a); ctx.show_text(s)
    ctx.restore()

def tally(ctx, x, y, n, seed, col=hexc('3a3d3a'), h=60, w=2.5):
    for g in range(n):
        gx = x + (g % 6) * 70; gy = y + (g // 6) * 80
        for k in range(4): rough(ctx, [(gx + k * 12, gy), (gx + k * 12 + 2, gy + h)], w, seed + g * 5 + k, col)
        rough(ctx, [(gx - 6, gy + h - 8), (gx + 44, gy + 8)], w, seed + g * 5 + 4, col)

def body3(ctx, outfit, arms, legs, walk, seed, width=1.0, tie=None, tie_off=0.0, color=None, shrug=0.0):
    col = color or {'suit': SUITC, 'white': WHITEJ, 'olive': OLIVE, 'cardi': CARDI, 'tee': TEE, 'vest': VEST,
                    'dress': hexc('7a2c3e'), 'hoodie': HOOD}[outfit]
    if legs == 'stand':
        for i, sx in enumerate((-1, 1)):
            lift = 0; fx = sx * 34 * width
            if walk is not None:
                ph = walk + i * math.pi
                lift = 22 * max(0, math.sin(ph)); fx += sx * 6 * math.cos(ph)
            lc = hexc('1a1a1d') if outfit in ('suit', 'olive', 'white') else INK
            if outfit == 'white': lc = hexc('2a2d44')
            rough(ctx, [(sx * 28 * width, 196), (sx * 32 * width, 262 - lift * .5), (fx, 330 - lift)], 7, seed + 5 + sx, lc)
            shape(ctx, ell(fx + sx * 8, 334 - lift, 22, 9, 16), hexc('151518'), 3, seed + 8 + sx)
    wd = width; sy = -shrug
    if outfit == 'dress':
        torso = [(-46 * wd, 10 + sy), (-66 * wd, 38 + sy), (-70 * wd, 120), (-96 * wd, 210), (96 * wd, 210), (70 * wd, 120), (66 * wd, 38 + sy), (46 * wd, 10 + sy)]
    else:
        torso = [(-48 * wd, 10 + sy), (-70 * wd, 38 + sy), (-78 * wd, 200), (78 * wd, 200), (70 * wd, 38 + sy), (48 * wd, 10 + sy)]
    shape(ctx, torso, col, 4.5, seed + 1)
    if outfit == 'suit':
        shape(ctx, [(-24, 10), (24, 10), (0, 92)], (0.96, 0.96, 0.96), 3, seed + 2)
        tc = tie or hexc('7a1d22')
        ctx.save(); ctx.translate(0, 16); ctx.rotate(tie_off); ctx.translate(0, -16)
        shape(ctx, [(-7, 16), (7, 16), (9, 78), (0, 92), (-9, 78)], tc, 2.5, seed + 3)
        ctx.restore()
        for sx in (-1, 1): rough(ctx, [(sx * 24, 10), (sx * 36 * wd, 62), (0, 112)], 3, seed + 4 + sx, hexc('3c4048'))
    elif outfit == 'white':
        rough(ctx, [(0, 12), (0, 198)], 3, seed + 2, hexc('b9b4a6'))
        for k in range(4): shape(ctx, ell(10, 40 + k * 38, 5, 5, 8), GOLD, 1.5, seed + 30 + k)
        shape(ctx, [(-60 * wd, 26), (-38 * wd, 22), (70 * wd, 176), (56 * wd, 196)], hexc('a8262c'), 3, seed + 3)
        for k, c in enumerate(('c0322a', '2f5fa8', 'e3c24a', '2f9e4f')):
            shape(ctx, rect(-58 * wd + k * 13, 64, -48 * wd + k * 13, 80), hexc(c), 1.5, seed + 40 + k)
        for k in range(3): shape(ctx, ell(-52 * wd + k * 14, 94, 6, 6, 8), GOLD, 1.5, seed + 50 + k)
        for sx in (-1, 1): shape(ctx, [(sx * 46 * wd, 12), (sx * 76 * wd, 30), (sx * 72 * wd, 46), (sx * 44 * wd, 26)], GOLD, 2.5, seed + 55 + sx)
    elif outfit == 'olive':
        rough(ctx, [(0, 12), (0, 198)], 3, seed + 2, hexc('3e4430'))
        shape(ctx, rect(-78 * wd, 150, 78 * wd, 166), hexc('2b2a24'), 2.5, seed + 3)
        for sx in (-1, 1):
            shape(ctx, rect(sx * 14 - 8, 14, sx * 14 + 8, 30), hexc('a8262c'), 1.5, seed + 4 + sx)
            shape(ctx, rect(sx * 44 - 20, 70, sx * 44 + 20, 104), hexc('525a3e'), 2.5, seed + 6 + sx)
        for k, c in enumerate(('c0322a', 'e3c24a', '2f5fa8')): shape(ctx, rect(-62 + k * 12, 52, -52 + k * 12, 62), hexc(c), 1, seed + 9 + k)
    elif outfit == 'cardi':
        shape(ctx, [(-20, 10), (20, 10), (6, 110), (-6, 110)], hexc('e8e2d0'), 2.5, seed + 2)
        for sx in (-1, 1): rough(ctx, [(sx * 20, 10), (sx * 8, 110), (sx * 8, 200)], 3, seed + 3 + sx, hexc('6b5139'))
        for k in range(4): shape(ctx, ell(-16, 120 + k * 20, 4, 4, 8), hexc('4a3a2a'), 1, seed + 10 + k)
    elif outfit == 'vest':
        shape(ctx, [(-20, 10), (20, 10), (0, 40)], (0.96, 0.96, 0.96), 2.5, seed + 2)
        shape(ctx, [(-5, 20), (5, 20), (6, 70), (0, 78), (-6, 70)], hexc('2f5fa8'), 2, seed + 3)
    elif outfit == 'tee':
        rough(ctx, [(-20, 12), (0, 30), (20, 12)], 3, seed + 2, hexc('3a5f96'))
    elif outfit == 'hoodie':
        for sx in (-1, 1): rough(ctx, [(sx * 12, 16), (sx * 14, 64)], 2.5, seed + 3 + sx, hexc('e8e2d0'))
    rough(ctx, [(0, 8), (0, -30)], 7, seed + 4)
    sleeve = {'suit': hexc('1e2024'), 'white': WHITEJ, 'olive': OLIVE}.get(outfit)
    for (sh, el, ha) in arms:
        sh = (sh[0] * wd, sh[1] + sy)
        if sleeve is not None:
            rough(ctx, [sh, el, ha], 13, seed + int(sh[0]) + 1, sleeve)
            rough(ctx, [sh, el, ha], 3, seed + int(sh[0]) + 2, INK, alpha=0.9)
        else:
            rough(ctx, [sh, el, ha], 6.5, seed + int(sh[0]))
        shape(ctx, ell(ha[0], ha[1], 12, 12, 14), SKIN, 3, seed + int(ha[0]) + 3)

ARMS = {
 'down': [((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (90, 128), (86, 206))],
 'table': [((-68, 44), (-120, 150), (-90, 185)), ((68, 44), (120, 150), (90, 185))],
 'grip': [((-68, 44), (-130, 140), (-150, 190)), ((68, 44), (130, 140), (150, 190))],
 'clasp': [((-68, 44), (-80, 130), (-10, 160)), ((68, 44), (80, 130), (10, 160))],
 'reachR': [((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (150, 80), (240, 70))],
 'reachL': [((-68, 44), (-150, 80), (-240, 70)), ((68, 44), (90, 128), (86, 206))],
 'holster': [((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (104, 120), (70, 170))],
 'up': [((-68, 44), (-120, -20), (-110, -110)), ((68, 44), (120, -20), (110, -110))],
 'shrug': [((-68, 44), (-120, 90), (-150, 30)), ((68, 44), (120, 90), (150, 30))],
 'pointR': [((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (170, 20), (260, -10))],
 'pointL': [((-68, 44), (-170, 20), (-260, -10)), ((68, 44), (90, 128), (86, 206))],
 'wave': [((-68, 44), (-90, 128), (-86, 206)), ((68, 44), (130, -10), (120, -100))],
 'tense': [((-68, 30), (-78, 124), (-70, 200)), ((68, 30), (78, 124), (70, 200))],
}

def eat_arms(ph):
    u = 0.5 - 0.5 * math.cos(ph)
    hand = (lerp(90, 20, u), lerp(170, -30, u))
    return [((-68, 44), (-120, 150), (-90, 185)), ((68, 44), (120, lerp(150, 90, u)), hand)]

def person3(ctx, x, y, s, outfit='suit', hair='spiky', hcol=None, expr='neutral', look=(0, 0), arms='down', legs='stand',
            walk=None, glasses=None, beard=None, wrinkles=False, cap=None, back=False, tear=None, rot=0, seed=300,
            headrot=0, width=1.0, skin=None, earpiece=False, tie=None, tie_off=0.0, extra=None, shrug=0.0, flip=False, color=None):
    global SKIN
    hcol = hcol or HAIR
    if isinstance(arms, str): arms = ARMS[arms]
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(-s if flip else s, s)
    old = SKIN
    if skin is not None: SKIN = skin
    body3(ctx, outfit, arms, legs, walk, seed, width, tie, tie_off, color=color, shrug=shrug)
    ctx.save(); ctx.translate(0, -shrug * 0.6); ctx.rotate(headrot)
    if extra == 'bald':
        head2(ctx, 'none', hcol, expr, look, glasses, beard, wrinkles, cap, back, tear, seed + 50)
        for sx in (-1, 1): shape(ctx, [(sx * 58, -76), (sx * 66, -118), (sx * 50, -112), (sx * 48, -84)], hcol, 2.5, seed + 90 + sx)
    else:
        head2(ctx, hair, hcol, expr, look, glasses, beard, wrinkles, cap, back, tear, seed + 50)
    if extra == 'bun':
        shape(ctx, ell(0, -182, 26, 20, 16), hcol, 3, seed + 95)
    if extra == 'scar':
        rough(ctx, [(34, -104), (46, -72)], 2.5, seed + 96, hexc('a06a5a'))
    if earpiece:
        rough(ctx, [(62, -84), (70, -50), (58, -30), (64, -10), (54, 6)], 2, seed + 97, hexc('d8d8d8'))
    ctx.restore()
    SKIN = old
    ctx.restore()

def price_tag(ctx, x, y, s, label, pop, col=(1, 1, 1), rot=-0.12):
    if pop <= 0.01: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(pop, pop)
    shape(ctx, [(-10, -44), (170, -44), (170, 44), (-10, 44), (-50, 0)], hexc('f3e6c4'), 4, 2000 + len(label))
    shape(ctx, ell(-22, 0, 8, 8, 10), hexc('7d6b52'), 2, 2010)
    text(ctx, label, 80, 18, 54 * s, 'Bebas Neue', INK, anchor='c')
    ctx.restore()

def bubble(ctx, x0, y0, x1, y1, tail, alpha=1.0, seed=2100):
    pts = [(x0, y0), (x1, y0), (x1, y1), ((x0 + x1) / 2 + 40, y1), tail, ((x0 + x1) / 2 - 20, y1), (x0, y1)]
    shape(ctx, pts, (1, 1, 1), 5, seed, alpha=alpha)

def grayscale_surface(surf):
    surf.flush()
    a = np.ndarray((H, W, 4), np.uint8, surf.get_data())
    g = (a[..., 0] * 0.11 + a[..., 1] * 0.59 + a[..., 2] * 0.30).astype(np.uint8)
    b = a.copy(); b[..., 0] = g; b[..., 1] = g; b[..., 2] = g
    return cairo.ImageSurface.create_for_data(bytearray(b.tobytes()), cairo.FORMAT_ARGB32, W, H, W * 4)

# ---------------- cast (reuse across videos; recolour via color=/hcol=) ----------------
def hero(ctx, x, y, s, **kw):
    """Main 'YOU' character: spiky black hair. Default outfit = green hoodie; pass outfit='suit' etc."""
    outfit = kw.pop('outfit', 'hoodie')
    person3(ctx, x, y, s, outfit, 'spiky', HAIR, **kw)
def suit_man(ctx, x, y, s, seed=1600, **kw):   # agents / guards
    person3(ctx, x, y, s, 'suit', 'slick', hexc('14161a'), glasses='sun', seed=seed, **kw)
def doctor(ctx, x, y, s, seed=410, **kw):
    person3(ctx, x, y, s, 'vest', 'short', hexc('5a3d2a'), glasses='round', seed=seed, color=hexc('eef0ee'), **kw)
def officer(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'olive', 'crew', hexc('9a968e'), wrinkles=True, extra='scar', seed=1500, **kw)
def leader(ctx, x, y, s, **kw):
    kw.setdefault('width', 1.22)
    person3(ctx, x, y, s, 'white', 'slick', hexc('cfcac0'), beard='mous', wrinkles=True, seed=1400, **kw)
def old_man(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'cardi', 'none', hexc('b9b4aa'), extra='bald', wrinkles=True, beard='mous', seed=1700, **kw)
def old_woman(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'cardi', 'short', hexc('9d978c'), extra='bun', wrinkles=True, seed=1750, color=hexc('7a5a7a'), **kw)
def kid(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'dress', 'bob', hexc('4a2e1e'), seed=1900, color=hexc('e07a9a'), **kw)
def nerd(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'tee', 'spiky_s', HAIR, glasses='round', seed=1800, **kw)
def woman(ctx, x, y, s, **kw):
    person3(ctx, x, y, s, 'dress', 'bob', hexc('a07040'), seed=2530, color=hexc('2c5f5a'), **kw)

def tint(c1, c2, u): return tuple(lerp(a, b, min(max(u, 0), 1)) for a, b in zip(c1, c2))

def room(ctx, wall=hexc('c9b89a'), floor=hexc('8a7058'), y=None):
    y = y or int(H * 0.7)
    shape(ctx, rect(-300, -300, W + 300, y), wall, 0, 1)
    for k in range(-2, W // 140 + 3): rough(ctx, [(k * 140, -300), (k * 140 + 3, y)], 2, 800 + k, tint(wall, (0, 0, 0), 0.1))
    shape(ctx, rect(-300, y, W + 300, H + 300), floor, 4, 802)

def clock(ctx, x, y, r, t, speed=1.0, seed=3010):
    shape(ctx, ell(x, y, r, r, 30), (0.96, 0.95, 0.9), 5, seed)
    a = t * speed; b = a / 12
    rough(ctx, [(x, y), (x + r * 0.8 * math.sin(a), y - r * 0.8 * math.cos(a))], 4, seed + 1)
    rough(ctx, [(x, y), (x + r * 0.5 * math.sin(b), y - r * 0.5 * math.cos(b))], 6, seed + 2)

def say(ctx, s, x0, y0, x1, y1, tail, t0, t, size=56):
    """Speech bubble that fades in at t0. Use '\n' for line breaks."""
    if t < t0: return
    a = min(1, (t - t0) * 5)
    bubble(ctx, x0, y0, x1, y1, tail, alpha=a)
    ls = s.split('\n')
    for i, ln in enumerate(ls):
        text(ctx, ln, (x0 + x1) / 2, (y0 + y1) / 2 + 18 + (i - (len(ls) - 1) / 2) * size * 1.1, size, anchor='c', alpha=a)

def caption(ctx, s, y=None, size=None, maxw=None):
    """Bottom caption, white with thick black outline (Patrick Hand)."""
    size = size or (74 if H > W else 64); maxw = maxw or W - 180
    y = y or (int(H * 0.855) if H > W else H - 110)
    ctx.select_font_face('Patrick Hand'); ctx.set_font_size(size)
    words = s.split(); lines = []; cur = ''
    for w_ in words:
        test = (cur + ' ' + w_).strip()
        if ctx.text_extents(test).width > maxw and cur: lines.append(cur); cur = w_
        else: cur = test
    lines.append(cur)
    y0 = y - (len(lines) - 1) * size * 0.55
    for i, ln in enumerate(lines):
        e = ctx.text_extents(ln); x = W / 2 - e.width / 2 - e.x_bearing; yy = y0 + i * size * 1.13
        ctx.move_to(x, yy); ctx.text_path(ln)
        ctx.set_source_rgba(0, 0, 0, 0.9); ctx.set_line_width(12); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
        ctx.move_to(x, yy); ctx.set_source_rgb(1, 1, 1); ctx.show_text(ln)

def rec_frame(ctx, x0, y0, x1, y1, t, a=1.0, L=70):
    for (cx, cy, dx, dy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        rough(ctx, [(cx + dx * L, cy), (cx, cy), (cx, cy + dy * L)], 6, 700 + int(cx + cy), hexc('e0e0e0'), alpha=a)
    if int(t * 2.5) % 2 == 0: shape(ctx, ell(x0 + 40, y0 + 50, 12, 12, 12), hexc('e8312a'), 0, 0, alpha=a)
    text(ctx, 'REC', x0 + 64, y0 + 64, 44, 'Bebas Neue', (0.9, 0.9, 0.9), alpha=a)
```

### sfxkit.py
```python
"""sfxkit — procedural score + SFX + VO mixing (numpy/scipy). Self-contained."""
import math, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve, resample_poly
SR = 48000
rng = np.random.default_rng(11)
def t_(d): return np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def db(x): return 10 ** (x / 20)
def norm(x): return x / (np.max(np.abs(x)) + 1e-9)
def env(n, a, r):
    e = np.ones(n); na = max(1, int(a * SR)); e[:na] = np.linspace(0, 1, na)
    nr = min(n, max(1, int(r * SR))); e[-nr:] *= np.linspace(1, 0, nr); return e
def mix(*xs):
    n = max(len(x) for x in xs); o = np.zeros(n)
    for x in xs: o[:len(x)] += x
    return o
_IR = lp(rng.standard_normal(int(1.8 * SR)) * np.exp(-np.arange(int(1.8 * SR)) / SR * 3.5), 5000)
def verb(x, m=0.3):
    y = np.concatenate([x, np.zeros(len(_IR))]); w = fftconvolve(y, _IR)[:len(y)]
    return y * (1 - m) + norm(w) * np.max(np.abs(x)) * m
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def tone(f, d, dec=0, a=0.005, r=0.03):
    tt = t_(d); return np.sin(2 * np.pi * f * tt) * np.exp(-tt * dec) * env(len(tt), a, r)
def boom(d, f0, f1, dec):
    tt = t_(d); f = f1 + (f0 - f1) * np.exp(-tt * 6)
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * dec))
def nh(d, lo, hi, dec): return norm(bp(rng.standard_normal(int(d * SR)), lo, hi) * np.exp(-t_(d) * dec))
def whoosh(d, rev=False):
    n = int(d * SR); x = rng.standard_normal(n); o = np.zeros(n); seg = 1200
    for i in range(0, n, seg):
        f = 300 + 3000 * (i / n); o[i:i + seg] = bp(x[i:i + seg], f, f * 2.2, 1)
    e = np.sin(np.linspace(0, np.pi, n)) ** 2 if not rev else np.linspace(0, 1, n) ** 3
    return norm(lp(o, 6000) * e)
def pluck(f, d=0.5, bright=1.0):
    tt = t_(d)
    x = sum(np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * (6 + k * 3 / bright)) / k for k in range(1, 7))
    return x * env(len(tt), 0.002, 0.05)
def pad(freqs, d, cutoff=1400, det=0.25):
    tt = t_(d); x = np.zeros(len(tt))
    for f in freqs:
        for dd in (-det, 0, det):
            ph = 2 * np.pi * (f + dd) * tt; x += sum(np.sin(k * ph) / k for k in range(1, 8))
    return lp(x, cutoff) * env(len(tt), min(0.8, d / 3), min(1.0, d / 3))
# ready-made SFX
def sfx_hit(): return norm(verb(mix(boom(1.4, 80, 35, 2.5), 0.4 * nh(0.5, 150, 1500, 6)), .4))       # dramatic boom
def sfx_stamp(): return norm(verb(mix(boom(0.7, 110, 50, 10), 0.7 * nh(0.2, 300, 3000, 25)), .2))    # stamp / impact
def sfx_pop(): return mix(whoosh(0.15), tone(900, 0.08, 25))                                          # text pop-in
def sfx_ding(): return norm(verb(sum(tone(f, 1.4, k) for f, k in ((1318, 3), (1661, 3.5), (1976, 4))), .4))  # sparkle
def sfx_tick(): return mix(nh(0.03, 2500, 7000, 200), 0.4 * tone(2800, 0.02, 100))                  # clock tick
def sfx_step(): return mix(boom(0.18, 120, 60, 30) * 0.8, nh(0.08, 1500, 6000, 60) * 0.5)          # footstep
def sfx_heartbeat(): return mix(boom(0.22, 60, 40, 20), np.concatenate([np.zeros(int(.15 * SR)), 0.7 * boom(0.22, 55, 38, 20)]))
def sfx_tape_stop():
    tt = t_(0.7); f = mtof(62) * np.exp(-tt * 4)
    return norm(lp(np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * rng.standard_normal(len(tt)), 2000)) * env(len(tt), .005, .2)
def sfx_power_down():
    tt = t_(1.6); f = 220 * np.exp(-tt * 2.2) + 25
    return norm(verb(lp(sum(np.sin(k * 2 * np.pi * np.cumsum(f) / SR) / k for k in range(1, 6)) * np.exp(-tt * 1.2), 1500), .4))

class Mix:
    def __init__(self, dur):
        self.N = int(dur * SR) + SR; self.dur = dur
        self.M = np.zeros((self.N, 2)); self.S = np.zeros((self.N, 2))
    def _put(self, buf, sig, at, g, pan):
        i = int(max(at, 0) * SR); sig = np.asarray(sig) * db(g); n = min(len(sig), self.N - i)
        if n <= 0: return
        gl = math.cos((pan + 1) * math.pi / 4) * 1.414; gr = math.sin((pan + 1) * math.pi / 4) * 1.414
        buf[i:i + n, 0] += sig[:n] * gl; buf[i:i + n, 1] += sig[:n] * gr
    def music(self, sig, at, g=-20, pan=0.0): self._put(self.M, sig, at, g, pan)
    def sfx(self, sig, at, g=-16, pan=0.0): self._put(self.S, sig, at, g, pan)
    def render(self, vo_path, out_path, fade=1.0):
        vo, sr = sf.read(vo_path)
        if vo.ndim > 1: vo = vo.mean(1)
        if sr != SR: vo = resample_poly(vo, SR, sr)
        vo = hp(vo, 60); vo = norm(vo) * db(-2.5)
        V = np.zeros(self.N); V[:len(vo)] = vo[:self.N]
        e = lp(np.abs(V), 6, 1); e = e / (e.max() + 1e-9)
        duck = 1 - 0.55 * np.clip(e * 4, 0, 1)
        out = self.M * duck[:, None] * db(-2) + self.S * (1 - 0.3 * np.clip(e * 4, 0, 1))[:, None] + V[:, None]
        f = np.interp(np.arange(self.N) / SR, [0, self.dur - fade, self.dur], [1, 1, 0]); out *= f[:, None]
        out = np.tanh(out * 1.05) / np.tanh(1.05); out = out / np.max(np.abs(out)) * db(-1)
        sf.write(out_path, out[:int(self.dur * SR)], SR, subtype='PCM_24')

def align_lines(vo_wav, lines, noise='-38dB', min_sil=0.22):
    """Return [(start,end)] per script line by matching silence gaps (ffmpeg silencedetect + DP)."""
    import subprocess, re
    r = subprocess.run(['ffmpeg', '-i', vo_wav, '-af', f'silencedetect=noise={noise}:d={min_sil}', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    ev = re.findall(r'silence_(start|end): ([0-9.]+)', r)
    sil = []; cur = None
    for k, v in ev:
        v = float(v)
        if k == 'start': cur = v
        else: sil.append((cur or 0, v)); cur = None
    total = sf.info(vo_wav).duration
    segs = []; t = 0
    for a, b in sil:
        if a > t + 0.05: segs.append((t, a))
        t = b
    if t < total - 0.05: segs.append((t, total))
    n, m = len(lines), len(segs); ch = [len(l) for l in lines]
    rate = sum(b - a for a, b in segs) / sum(ch)
    INF = 1e18; dp = [[INF] * (m + 1) for _ in range(n + 1)]; bk = [[0] * (m + 1) for _ in range(n + 1)]; dp[0][0] = 0
    for i in range(1, n + 1):
        for j in range(i, m + 1):
            for k in range(max(i - 1, j - 5), j):
                if dp[i - 1][k] >= INF: continue
                dur = segs[j - 1][1] - segs[k][0]; exp = ch[i - 1] * rate
                c = dp[i - 1][k] + ((dur - exp) / (exp + 0.5)) ** 2
                if c < dp[i][j]: dp[i][j] = c; bk[i][j] = k
    j = m; out = []
    for i in range(n, 0, -1):
        k = bk[i][j]; out.append((segs[k][0], segs[j - 1][1])); j = k
    return out[::-1]

def add_pauses(vo_wav, lt, pauses, out_wav):
    """Insert silence (sec) before given line indices: pauses={idx: sec}. Returns new timings."""
    x, sr = sf.read(vo_wav)
    if x.ndim > 1: x = x.mean(1)
    o = []; new = []; shift = 0.0; prev = 0
    for i, (a, b) in enumerate(lt):
        if i in pauses:
            cut = 0 if i == 0 else int((lt[i - 1][1] + 0.12) * sr)
            o.append(x[prev:cut]); o.append(np.zeros(int(pauses[i] * sr))); prev = cut; shift += pauses[i]
        new.append((a + shift, b + shift))
    o.append(x[prev:]); sf.write(out_wav, np.concatenate(o), sr)
    return new
```

### scenekit.py
```python
"""scenekit — shared props + loop-ready runner for stickman reels (stickman-pov-shorts skill)."""
import sys, json, math, subprocess
import numpy as np, cairo, soundfile as sf
import stickkit as K
from stickkit import *
K.W, K.H = 1080, 1920
W, H = K.W, K.H
LINES = [l.strip() for l in open('script.txt') if l.strip()]
LT = json.load(open('lt.json'))
END = sf.info('vo_rt.wav').duration          # loop: video length == VO length, no tail

class Sc:
    def __init__(self, t0): self.t0 = t0
    def L(self, i): return (LT[i][0] - self.t0, LT[i][1] - self.t0)
    def at(self, i, sub):
        k = LINES[i].find(sub); f = max(k, 0) / max(len(LINES[i]), 1); s, e = self.L(i); return s + (e - s) * f

FLOOR = 1450
def stand(s, floor=FLOOR): return floor - 334 * s
def pop(t, t0, d=0.3): return ease_out_back((t - t0) / d)

SHIRT = hexc('dce6f0'); WALL = hexc('cfd6d4'); CARPET = hexc('7c8784')

def me(ctx, x, y, s, **kw):
    kw.setdefault('outfit', 'vest'); kw.setdefault('color', SHIRT)
    hero(ctx, x, y, s, **kw)

def boss(ctx, x, y, s, **kw):
    kw.setdefault('width', 1.18)
    person3(ctx, x, y, s, 'suit', 'none', hexc('8d8a84'), extra='bald', beard='mous', wrinkles=True, seed=2700,
            color=hexc('3a3f4a'), tie=hexc('b0262c'), **kw)

def ceo(ctx, x, y, s, **kw):
    kw.setdefault('width', 1.1)
    person3(ctx, x, y, s, 'suit', 'slick', hexc('e4e1da'), glasses='round', beard='full', wrinkles=True, seed=2900,
            color=hexc('1c2030'), tie=GOLD, **kw)

def office(ctx, wall=WALL, floor=CARPET, y=1330, window=True, plant=True):
    room(ctx, wall, floor, y)
    if window:
        shape(ctx, rect(620, 260, 980, 760), hexc('a9c4d6'), 5, 3100)
        for bx, bw, bh in ((640, 70, 260), (720, 90, 380), (820, 60, 200), (890, 80, 320)):
            shape(ctx, rect(bx, 760 - bh, bx + bw, 760), hexc('8399a8'), 2.5, 3110 + bx)
        rough(ctx, [(800, 260), (800, 760)], 5, 3120); rough(ctx, [(620, 510), (980, 510)], 5, 3121)
    if plant:
        shape(ctx, [(110, y), (90, y - 110), (190, y - 110), (170, y)], hexc('9a5b3a'), 4, 3130)
        for k, (dx, dy) in enumerate(((-60, -250), (0, -300), (60, -240), (-30, -200), (40, -190))):
            shape(ctx, [(140, y - 110), (140 + dx * 0.5 - 18, y - 110 + dy * 0.6), (140 + dx, y - 110 + dy), (140 + dx * 0.5 + 18, y - 110 + dy * 0.6)],
                  hexc('4f7a45'), 3, 3140 + k)

def desk(ctx, x0, x1, y, seed=3200, col=hexc('8a6446')):
    shape(ctx, rect(x0, y, x1, y + 40), col, 5, seed)
    shape(ctx, rect(x0 + 20, y + 40, x1 - 20, y + 420), tint(col, (0, 0, 0), 0.15), 5, seed + 1)

def paper(ctx, x, y, w, h, rot=0, seed=3300, col=PAPER):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    shape(ctx, rect(-w / 2 + 12, -h / 2 + 14, w / 2 + 12, h / 2 + 14), (0, 0, 0), 0, 0, alpha=0.25)
    shape(ctx, rect(-w / 2, -h / 2, w / 2, h / 2), col, 5, seed)
    ctx.restore()

def star(ctx, x, y, r, col=hexc('f2d04a'), seed=3700, rot=0, alpha=1.0):
    pts = []
    for i in range(10):
        a = rot - math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    shape(ctx, pts, col, 3, seed, alpha=alpha)

def confetti(ctx, t, n=40, seed=5):
    import random
    rng = random.Random(seed)
    cols = [hexc('c0322a'), GOLD, hexc('2f9e4f'), hexc('2f5fa8'), hexc('e07a9a')]
    for i in range(n):
        x0 = rng.uniform(0, W); sp = rng.uniform(250, 450); ph = rng.uniform(0, 6)
        y = -50 + ((t * sp + rng.uniform(0, H)) % (H * 0.9))
        x = x0 + 30 * math.sin(t * 3 + ph)
        ctx.save(); ctx.translate(x, y); ctx.rotate(t * 4 + ph)
        shape(ctx, rect(-10, -5, 10, 5), cols[i % 5], 1.5, 5000 + i)
        ctx.restore()

def strike(ctx, x0, x1, y, u, seed):
    if u <= 0: return
    rough(ctx, [(x0, y), (lerp(x0, x1, min(u, 1)), y - 10)], 9, seed, hexc('c0322a'))

def reveal(s, u):
    return s[:int(len(s) * min(1, max(0, u)))]

def arm_to(hand, s=1.0, side=-1, bend=1.0):
    """Arm list with one hand placed at a local target; other arm down."""
    sh = (side * 68, 44); hx, hy = hand
    mx, my = (sh[0] + hx) / 2, (sh[1] + hy) / 2
    dx, dy = hx - sh[0], hy - sh[1]; L = math.hypot(dx, dy) + 1e-6
    px, py = -dy / L, dx / L
    if py < 0: px, py = -px, -py
    el = (mx + px * 40 * bend, my + py * 40 * bend)
    other = ((-side * 68, 44), (-side * 90, 128), (-side * 86, 206))
    a = (sh, el, (hx, hy))
    return [a, other] if side < 0 else [other, a]

def lerp_arms(A, B, u):
    """Blend two arm lists (pose A -> pose B) by u in [0,1]."""
    A = ARMS[A] if isinstance(A, str) else A; B = ARMS[B] if isinstance(B, str) else B
    return [tuple((lerp(p[0], q[0], u), lerp(p[1], q[1], u)) for p, q in zip(a, b)) for a, b in zip(A, B)]

# ---------------- runner ----------------
def run(SHOTS):
    def timeline():
        out = []
        for i, (li, fn) in enumerate(SHOTS):
            st = 0.0 if i == 0 else LT[li][0] - 0.18
            en = END if i == len(SHOTS) - 1 else LT[SHOTS[i + 1][0]][0] - 0.18
            out.append((st, en, fn))
        return out
    TL = timeline()
    if len(sys.argv) > 1 and sys.argv[1] == '--tl':
        for a, b, fn in TL: print(f'{a:6.2f} {b:6.2f} {fn.__name__}')
        return TL
    rng_mode = len(sys.argv) > 1 and sys.argv[1] == '--range'
    only = [] if rng_mode else [float(a) for a in sys.argv[1:]]
    grains = grain_layers()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    NF = int(round(END * 24)); ff = None
    if not only:
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                               '-r', '24', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
                               '-pix_fmt', 'yuv420p', sys.argv[4] if rng_mode else 'video.mp4'], stdin=subprocess.PIPE)
    frames = [min(NF - 1, int(x * 24)) for x in only] if only else (range(int(sys.argv[2]), min(NF, int(sys.argv[3]))) if rng_mode else range(NF))
    for f in frames:
        t = f / 24; K.BOIL = f // 2
        ctx = cairo.Context(surf)
        ctx.set_operator(cairo.OPERATOR_SOURCE); ctx.set_source_rgb(0, 0, 0); ctx.paint(); ctx.set_operator(cairo.OPERATOR_OVER); ctx.new_path()
        for a, b, fn in TL:
            if a <= t < b: ctx.save(); fn(ctx, t - a, b - a, Sc(a)); ctx.restore(); break
        ctx.set_source_surface(grains[K.BOIL % 4], 0, 0); ctx.paint(); vignette(ctx, 0.35)
        for (st, en), s in zip(LT, LINES):
            if st - 0.05 <= t < en + 0.25: caption(ctx, s); break
        surf.flush()
        if ff: ff.stdin.write(bytes(surf.get_data()))
        else: surf.write_to_png(f'test_{f:05d}.png')
    if ff: ff.stdin.close(); ff.wait()
    return TL

def timeline_of(SHOTS):
    out = []
    for i, (li, fn) in enumerate(SHOTS):
        st = 0.0 if i == 0 else LT[li][0] - 0.18
        en = END if i == len(SHOTS) - 1 else LT[SHOTS[i + 1][0]][0] - 0.18
        out.append((st, en, fn.__name__))
    return out

# ---------------- seamless loop mix ----------------
def render_loop(mix, vo_path, out_path):
    """Like sfxkit.Mix.render, but no fade-out: anything past END wraps onto the start so the loop is seamless."""
    import sfxkit as A
    n = int(round(END * A.SR))
    def wrap(buf):
        o = buf[:n].copy(); rest = buf[n:]
        k = 0
        while len(rest) > 0:
            m = min(len(rest), n); o[:m] += rest[:m]; rest = rest[m:]
        return o
    M = wrap(mix.M); S = wrap(mix.S)
    vo, sr = sf.read(vo_path)
    if vo.ndim > 1: vo = vo.mean(1)
    vo = A.hp(vo, 60); vo = A.norm(vo) * A.db(-2.5)
    V = np.zeros(n); V[:min(n, len(vo))] = vo[:n]
    e = A.lp(np.abs(np.concatenate([V[-4800:], V])), 6, 1)[4800:]; e = e / (e.max() + 1e-9)
    duck = 1 - 0.55 * np.clip(e * 4, 0, 1)
    out = M * duck[:, None] * A.db(-2) + S * (1 - 0.3 * np.clip(e * 4, 0, 1))[:, None] + V[:, None]
    out = np.tanh(out * 1.05) / np.tanh(1.05); out = out / np.max(np.abs(out)) * A.db(-1)
    sf.write(out_path, out, A.SR, subtype='PCM_24')
```

### prep_vo.py
```python
"""prep_vo — mp3 -> vo.wav -> aligned line timings -> dramatic pauses -> trimmed vo_rt.wav + lt.json.
Usage:  python3 prep_vo.py vo.mp3 "3:0.3,7:0.4,15:0.6"          # loop (default): VO ends 0.38 s after last word
        python3 prep_vo.py vo.mp3 "9:0.9" --tail 3.0             # non-loop: keep 3 s of silence for an ending beat
Pause keys are line indices (0-based) in script.txt; value = seconds of silence inserted BEFORE that line."""
import sys, json, subprocess
import numpy as np, soundfile as sf
import sfxkit as A

src = sys.argv[1]
pauses = {int(k): float(v) for k, v in (p.split(':') for p in sys.argv[2].split(',') if p)} if len(sys.argv) > 2 else {}
tail = float(sys.argv[sys.argv.index('--tail') + 1]) if '--tail' in sys.argv else 0.38
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-ar', '48000', '-ac', '1', 'vo.wav'], check=True)
lines = [l.strip() for l in open('script.txt') if l.strip()]
lt = A.align_lines('vo.wav', lines)
for i, ((a, b), l) in enumerate(zip(lt, lines)): print(f'{i:2d} {a:6.2f} {b:6.2f} {b - a:5.2f}  {l}')
lt2 = A.add_pauses('vo.wav', lt, pauses, 'vo_p.wav') if pauses else lt
x, sr = sf.read('vo_p.wav' if pauses else 'vo.wav')
if x.ndim > 1: x = x.mean(1)
idx = np.where(np.abs(x) > 10 ** (-40 / 20))[0]; a, b = idx[0] / sr, idx[-1] / sr
s0 = max(0, int((a - 0.06) * sr)); s1 = int((b + tail) * sr); y = x[s0:s1]
if len(y) < s1 - s0: y = np.concatenate([y, np.zeros(s1 - s0 - len(y))])
f = int(0.01 * sr); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
sf.write('vo_rt.wav', y, sr)
off = s0 / sr
lt2 = [(max(0.0, p - off), min(len(y) / sr, q - off)) for p, q in lt2]; lt2[0] = (0.0, lt2[0][1])
json.dump(lt, open('lt_raw.json', 'w')); json.dump(lt2, open('lt.json', 'w'))
print('final duration', round(len(y) / sr, 2), 's')
```

### short.py (loop template)
```python
"""<Title> — looping stickman reel. The last shot animates INTO the first frame."""
import sys, math, random
sys.path.insert(0, '.')
from scenekit import *

def you(ctx, x, y, s, **kw):                       # the main "YOU" character
    kw.setdefault('outfit', 'hoodie'); hero(ctx, x, y, s, **kw)

# ---- the loop composition: used by the FIRST and the LAST shot ----
POSE_A = 'down'                                    # pose at frame 0 (and at the very last frame)
def loop_scene(ctx, u, zoom):
    """u = 1 -> exact opening composition. The last shot animates u: 0 -> 1."""
    ctx.save(); cam(ctx, 540, 950, zoom)
    office(ctx)
    you(ctx, 540, stand(1.2), 1.2, expr='neutral', arms=lerp_arms('wave', POSE_A, u))
    ctx.restore()

def s_hook(ctx, t, d, S):                          # line 0: hook. Frame 0 must have no overlay text.
    loop_scene(ctx, 1.0, 1.0 + 0.05 * ease_io(t / d))
    glow_text(ctx, 'HOOK TITLE', 540, 300, 150, 'Bebas Neue', GOLD, (1, 0.75, 0.2), pop=pop(t, 0.35), rot=-0.04)

def s_story(ctx, t, d, S):                         # one shot per 1-3 lines; time things to words with S.at()
    office(ctx)
    you(ctx, 540, stand(1.2), 1.2, expr='shock' if t > S.at(1, 'word') else 'neutral')
    stamp(ctx, 'STAMP', 540, 500, S.at(1, 'word'), t, 120, -0.1)

def s_end(ctx, t, d, S):                           # last line: ends EXACTLY on frame 0
    u = ease_io((t - 0.15) / (d - 0.55))
    loop_scene(ctx, u, 1.05 - 0.05 * ease_io(min(1, t / (d - 0.15))))

SHOTS = [(0, s_hook), (1, s_story), (2, s_end)]    # (first line index, shot fn)

if __name__ == '__main__':
    run(SHOTS)
```

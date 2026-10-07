---
name: hegemon-shorts
description: "Hegemon Shorts: make the Hegemon channel's 30–35 s vertical (1080x1920) real-knowledge 3D Shorts for YouTube + Facebook — human body, survival, 'what happens if…' science — from a topic or a YouTube-AI suggestion. Writes and fact-checks the script, voices it with ElevenLabs (Liam, eleven_v4) and sends the voiceover for approval first, builds clean Zack-D-style 3D animation (rounded boy, x-ray cutaways, glow studios, screen-pinned titles that never leave the frame), renders with captions/music/SFX, then makes the thumbnail, YouTube SRT and upload package (vidIQ title/tags). Use for any Hegemon video, Short, voiceover, thumbnail, SRT or upload metadata request. No Blender or Higgsfield."
---

# Hegemon Shorts

Hegemon is a **real-knowledge** Shorts channel (it grew out of a funny "what-if" channel; the look and pipeline are the same, the content is true). Proven formats: "What Happens If You Don't Sleep for 11 Days? 😳" and "What Happens If You Drink ONLY Coffee for 3 Days?". Viewers respond to **high-stakes physiological "what happens when…" scenarios explained step by step** (day 1 → day 2 → day 3, stage by stage).

Everything is built as code: three.js scenes rendered headless → MP4, ElevenLabs voice, procedural music/SFX, burned-in captions. The `kit/` folder holds every file; `examples/coffee_shots.js` is a complete, working 17-shot video to copy patterns from.

## Hard rules
- **Never use Blender or Higgsfield.** Never spend ElevenLabs/vidIQ credits the user did not ask for; state the model and cost of every paid generation.
- **Send the voiceover to the user and wait for approval before animating.**
- **Facts must be true.** Fact-check every line (also YouTube-AI suggested scripts). If a line is wrong or overstated, fix it with the smallest change, keep the rest verbatim, and tell the user exactly what changed and why (e.g. coffee is ~98 % water, so "severe dehydration" → "massive caffeine overload").
- **Everything must stay inside the frame, especially text** (user's explicit request). Keep scenes zoomed out; all titles are HUD text pinned to the screen (see *Look*). Check a contact sheet before every full render.
- Keep chat replies short, in English. The user writes in Roman Urdu or English: end every reply with one line `**English fix:** <corrected version of his message>`.
- Commit and push project files (not audio/video) to the session branch when done.

## 1. Script (30–35 s, ~80–90 words)
- **Title shape:** "What Happens If You ___ for N Days?" / "What Happens to Your Body If ___".
- **Hook (0–4 s):** the premise as an action already happening, visible on frame 0 with a bold title (e.g. "ONLY COFFEE / FOR 72 HOURS?"). Never fade in.
- **Body:** 3–5 real facts in escalating stages ("At first… / By day two… / By day three…"). One mechanism name per stage (adenosine, dopamine, microsleeps, glymphatic waste) — viewers love a named mechanism.
- **Ending — pick one:** (a) **question CTA** ("How many cups do you drink a day? Let me know below.") and **cut cleanly right after it** — no dead tail; or (b) a **loop** where the last line runs into the first ("…nobody should end up like…" → "This boy hasn't slept in eleven days.") and the last frame matches frame 0.
- `script.txt`: one sentence per line, **display form** (digits ok, no em-dashes — use commas). For the voice, spell numbers out ("nineteen sixty-four").
- Show the script (and any fact fixes) to the user.

## 2. Voice (ElevenLabs) — send for approval
- Voice **Liam – Energetic, Social Media Creator** `TX3LPaxmHKxFdv7VOQHJ`; model **`eleven_v4`** (user's choice; reported 0 credits). Backup voices: Alex `yl2ZDV1MzN4HbQJbMihG` (faster, upbeat), Russ `t0eCaS57KWbQQc1wRkah` (deep, deadpan).
- One take: `creative_generate_speech(generations_count=1, model_id="eleven_v4")`, reuse one flow. v4 audio tags sparingly where the tone turns: `[excited]` on the payoff word, `[nervous]` for danger, `[curious]` on the closing question. CAPS for one emphasis word.
- Poll `creative_get_flow_run_status`, then download the `media[].url` with `curl -sS -o vo_raw.mp3 "<url>"` (works from the container).
- Tighten: `python3 tighten.py vo_raw.mp3 0.2` → `voiceover.wav` (every pause ≤ 0.2 s, head/tail trimmed). If still > 35 s: `ffmpeg -i voiceover.wav -af atempo=1.07 v.wav && mv v.wav voiceover.wav` (≤ 1.08, pitch preserved).
- Export an mp3 to the repo root and **SendUserFile it**; report length, cost and any script fixes; wait for OK.

## 3. Setup and timing
```bash
bash .claude/skills/hegemon-shorts/kit/setup.sh <topic>-short     # copies kit, npm three+montserrat, pip deps
cd <topic>-short && python3 align.py script.txt voiceover.wav timing.json
```
If the display script has digits the voice spoke as words, align a `script_spoken.txt` instead and map the words back (see sleep project: "1964" ↔ "nineteen sixty-four").
Chromium: `render.py` auto-uses the preinstalled `/opt/pw-browsers/chromium_headless_shell-*` (never `playwright install`).

## 4. Look (the Hegemon style)
- **Clean, rounded, Zack-D-like 3D**: MeshStandard rounded characters, dark gradient studios with blue/pink (or themed) rim lights, glow sprites, bold 3D props. Recurring hero: **the boy** (`kid()`): blue tee, big eyes with real eyelids, `tired()` dark circles + bloodshot eyes, `xray()` transparent head with a glowing brain.
- **Shots 1.5–3 s, hard cut on every line or key word** (`wordT`), slow 5–10 % camera push in each, a shake (`camS` hit times) on impact words, an SFX on every visible action.
- **Framing (zoomed out):** portrait half-width visible at distance d is `d·tan(fov/2)·0.5625`; keep every subject inside ±75 % of that. Typical: full body fov 40 at d 5–6; x-ray head fov 30 at d 3.2–3.5; props fov 40 at d 4.5–7. Keep faces above the caption band (caption ≈ 29 % from bottom).
- **Titles = HUD** (`hud(text,{yf,wf,fg,bg,stroke,size})` + `hpop(m,t0,t)`): pinned to the screen, `yf` 0.79–0.88 (top band, under YouTube's top icons), `wf` ≤ 0.84. They can never leave the frame. Use 1–3 words, yellow `#ffd23a` / white / red badge `bg:'#d8423a', stroke:null`. Two stacked titles: `yf .86` and `.79`.
- **Captions:** Montserrat ExtraBold white, black outline, yellow keywords, 2–3 words, pop-in, `captions.py … --hl word1,word2`.
- **Music moods** (`cues.json`): playful / mystery / tense / dark / space; change at story turns. SFX library: `python3 -c "import sfxlib;print(sorted(sfxlib.SFX))"` (heartbeat, tick_tock, boom, pop, shimmer, sizzle, bubbles, glitch, powerdown, siren, whoosh, thud, clink, ding…).

## 5. Writing `shots.js`
Copy the header of `examples/coffee_shots.js`, then one `shot(start, build)` per beat:
```js
import {THREE,camera,cam,clamp,ease,back,lerp,V,grp,RB,SPH,sm,cyl,setSeed,rnd} from './engine.js';
import * as K from './lib.js';
await K.initTimeline({t0:0.15, tail:0.25});      // tail: 0.25 for a CTA ending, ~0.06 for a loop
const {shot,hud,hpop,L,E,wordT,studio2,kid,xrayScene,updPulses,brainPt,glow,txt,dynTex,camS,sstep,bedroom,wallClock,mug,monitor,heart,stomach,molecule,hand,shadowMan,kitchen,steam,COF}=K;
shot(0,()=>{const s=studio2('#173049','#04080f');const k=kid(s);k.root.position.set(0,.95,0);
  const h=hud('ONLY COFFEE',{yf:.86,wf:.8});
  return{s,u(t){hpop(h,0,t);cam(40,[0,1.7,lerp(5.4,5,ease(t/2.5))],[0,1.5,0])}}});
K.go();
```
- `u(t)` must depend only on `t`. Start shots at `L(i)-0.1` or `wordT(i,'word')-0.05`.
- **lib.js API:** scenes `studio2(top,bot,{floor,key,rimA,rimB,hemi})`, `bedroom()`→`{s,clk,bed,blanket}`, `kitchen()`, `xrayScene('normal'|'toxic')`→`{s,k,B,M,pulses,tox}` + `updPulses(P,t,speed,on)`; characters `kid(p,{tee,pants,skin,hair})`→`{root,torso,head,legs,arms[{sh,el,s}],face(m),lid(0..1),tired(0..1),look(x,y),xray(on),brain}` (standing `root.y=.95`; lying face-up `root.rotation.x=-PI/2`), `shadowMan`, `hand`; props `mug(p,{h,r,fill,col})`+`setFill`, `steam`, `monitor(p,w)`+`setECG(t,bpm)`, `heart`, `stomach`, `molecule(p,col)`, `wallClock(p,r)`+`setTime(h)`, `brain`; FX `glow(p,col,size,op)`, `txt(p,text,{w,fg,bg,stroke,size})` (3D text — only inside props, e.g. a book page), `dynTex(w,h,draw)` (live counters), `camS(fov,pos,look,t,hits,amt)` (camera with shake), `face2cam(m)` (billboard after camera), `pop(m,t0,t)`, `hudMesh(mesh,{yf,wf})` (custom/dynamic HUD, e.g. a cup counter). Engine (`engine.js`): `RB SPH sm cyl grp box mat lerp ease eout back clamp V setSeed rnd lamp carSimple faceEyes paintTex`.
- Syntax check: `cp shots.js /tmp/x.mjs && node --check /tmp/x.mjs` (a syntax error otherwise shows only as a READY timeout).

## 6. Test → render → assemble
```bash
python3 render.py test 0.1,2.5,5.0,...        # one time per shot, then:
python3 sheet.py contact.jpg                  # red line = caption height; LOOK at it
```
Check: every HUD/caption fully inside, subjects inside the frame, faces above the caption line, nothing important clipped. Fix, re-test only changed shots, **send the sheet to the user**, then:
```bash
rm -rf chunks; nohup python3 render.py full > render.log 2>&1 &     # ~0.5 s/frame; resumable chunks
python3 captions.py timing.json captions.ass --hl key,words,here
# cues.json: {"total":END,"vo_offset":0.15,"music":[[0,"playful"],[13.5,"tense"]],"music_level":0.2,"cuts":[shot starts],"sfx":[{"t":..,"name":"boom","g":.6}]}
python3 mix.py cues.json voiceover.wav mix.wav
ffmpeg -y -i video.mp4 -i mix.wav -vf "ass=captions.ass:fontsdir=fonts" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest -movflags +faststart final.mp4
```
Wait for the render with a background `until grep -q DONE render.log; do sleep 5; done`. Re-check 8 frames of `final.mp4` (and ~-14 LUFS), copy it to the repo root with a descriptive name, **SendUserFile** it. A late fix only needs its chunk deleted (`chunks/c001.mp4`) and `render.py full` again.

## 7. Package (only when asked, or offer in one line)
- **Title:** use vidIQ `vidiq_score_title(type="short")` on 3–4 options; prefer one that also contains the top search phrase. Keyword data: `vidiq_keyword_research` (research + matching_terms), proof of demand: `vidiq_outliers(contentType="short")`.
- **What matters on Shorts:** title, 1-line description, 2–3 hashtags, pinned question comment. Tags barely matter (paste a ≤500-char list only if asked). Post **every 48 h**, same niche, same schedule on Facebook Reels.
- **Thumbnail 1080×1920:** `python3 thumbnail.py final.mp4 thumb.jpg --main <emotional face time> --line1 "11 DAYS" --line2 "NO SLEEP" [--inset <detail time> --arrow x0,y0,x1,y1]`; view it, fix arrow/crop, send.
- **YouTube SRT:** `python3 srt.py timing.json captions.srt`, then read it and hand-fix any awkward phrase break (never split "zero deep / sleep"). Upload: Studio → Subtitles → Add → Upload file → *With timing*.

## Lessons learned
- 3D labels near the camera or inside the head get clipped/hidden — use HUD titles; 3D text only on props.
- Billboards must face the camera **after** the camera moves (lib does this for `face2cam` and HUD).
- The narrow portrait frame is the #1 problem: when in doubt, pull the camera back.
- `rm -rf` with a relative glob after `cd` is blocked; use absolute paths or overwrite files.
- Stop hook wants untracked files committed: `git add <project> && git commit && git push -u origin <branch>`.

---
name: sued-loop-shorts
description: Make the user's "He Sued X" series — 30–35 s vertical (1080x1920) low-poly 3D comedy Shorts where a sunburned/sleepless/angry guy takes an absurd thing to court (Time, Sleep, the Sun, Gravity, Mondays…), told by the ElevenLabs voice "Alex" on eleven_v4 with emotion tags, ending in a PERFECT LOOP (last line + last frame flow straight back into the first). Covers script writing, voiceover only, the full video (three.js, no Blender), frame-safe on-screen text, subtitles, background music, SFX, and the title / description / pinned comment. Use this skill whenever the user asks for a new "he sued …" / "lawsuit against …" / absurd courtroom short, a looping low-poly short, "just the voiceover" for one of these, a 32-second loop script, or titles/descriptions for these videos — even if they don't say "skill" or name the series.
---

# "He Sued X" — low-poly loop shorts

The user runs a YouTube/TikTok channel of absurd courtroom shorts in the Zack-D-style low-poly look. Past episodes:
- **He Sued Time** — weekends too short.
- **He Sued Sleep** — never there in bed, attacks you in meetings.
- **He Sued the Sun** — sunburn → the Sun is ordered twice as far away → snow in July.

The user writes in Roman Urdu / casual English.
- Keep replies short and plain.
- End every reply with a one-line **English fix:** giving the corrected version of their message. It helps them practise.

Everything you need is in `scripts/`. `references/example_shots_sued_sun.js` is a complete, working episode: copy its structure.

## What the user cares about (learned the hard way)
1. **Script first, voiceover before video.** When they say "just the voiceover", send only the audio and stop. Don't render until they say go.
2. **Use their script word for word** when they give one, including numbers like "3:00 AM" and "12-hour".
   - eleven_v4 reads digits fine, so don't spell them out.
   - Don't "fix" their wording without saying so.
3. **Voice: "Alex – Upbeat, Energetic and Clear"** (`yl2ZDV1MzN4HbQJbMihG`, from `creative_list_voices`), model **eleven_v4**, `generations_count: 1`.
   - Add emotion tags such as `[curious]`, `[dramatically]`, `[sarcastic]`, `[nervous]`, `[gasps]`, `[mischievously] [slowly]`, and change them only where the mood changes.
   - v4 has been costing 0 credits. Check `estimate_only` first; if it's not free, state the cost before generating.
   - Older episodes used eleven_multilingual_v2, which can't use tags.
4. **Perfect loop.** The last spoken words must run grammatically into the first line ("…which is exactly why…" → "This man just sued the Sun."). The last video frame must equal frame 0, there's no silence at either end, and the music keeps going across the loop point.
5. **Text and framing.** The user explicitly complained about text being cut off and things being zoomed in too much. Every sign must be fully inside the frame and above the subtitle band, and no subject should fill the frame (see *Framing rules*).
6. **Music and subtitles** are on by default. They once asked for "no BGM, no subtitle"; follow whatever the latest request says.
7. Keep unrelated projects (e.g. a Blender voiceover) in their own folder and don't mix them in.

## Script formula (≈85–92 words → 30–33 s with Alex v4)
- **Line 1 is the hook and the loop target:** "This man just sued the Sun." / "At 3:00 AM on a Tuesday, a sleep-deprived guy officially filed a lawsuit against Sleep."
- **Escalate:** the reason → one real fact → the defendant shows up in court and does something absurd → a quick double gag ("The jury needed sunglasses. The stenographer got a tan.") → the judge's compromise → the compromise backfires.
- **Comment trigger:** "Would you take that deal? Yes or no?"
- **Loop line:** ends mid-sentence and leads into line 1, e.g. "He got frostbite… which is exactly why…", "He panicked so hard… that precisely…", "He hated the compromise so much, so…".
- Write `script.txt` as one spoken line per row with **no tags**; the tags go only in the TTS prompt.
- Show the script as a table (line / emotion / visual) before voicing, unless the user already said "make it".

## Pipeline
```bash
bash <skill>/scripts/setup.sh work/sued-<topic>      # copies the kit, npm/pip, caption font
cd work/sued-<topic>
```
1. **Voice:** `creative_generate_speech` (Alex, eleven_v4, tags) → poll `creative_get_flow_run_status` → `curl` the `content_url` to `raw.mp3`.
   - Reuse one flow (`creative_create_flow` once) so later transcriptions can connect to it.
2. **Trim for the loop:** `python3 trim_voice.py raw.mp3 voiceover.wav [--target 32]` prints `OFFSET` and `TEMPO`.
   - Use `--target` only if the user asked for an exact length, and keep the stretch within ±8 %.
   - Send the user the trimmed voiceover as an mp3 (`ffmpeg -i voiceover.wav -b:a 192k X_voiceover.mp3`).
3. **Exact word times (free):** `creative_transcribe_audio` with `connect_from:[<speech node_id>]`, model `eleven_scribe_v1`.
   - Save its `words` list to `words.json`, then run `python3 build_timing.py words.json script.txt timing.json --offset <OFFSET> --tempo <TEMPO>`.
   - Don't use `align.py`/pause guessing; it mis-split lines that had no pause between them.
   - Hugging Face is blocked here, so local Whisper won't work.
4. **Shots:** write `shots.js`, copying `references/example_shots_sued_sun.js`:
   - one shot per line, two for long lines, hard cuts;
   - gags timed to `wordT(line,'word')`;
   - `END` = voiceover length.
5. **Test stills before the full render:**
   - Run `python3 render.py test 0.0,0.5,…,END-0.02` (one time per shot plus frame 0 and the last frame), then `python3 sheet.py`, and Read `test/sheet.jpg`.
   - Fix framing and repeat, then send the user the sheet if they're around.
   - Frame 0 and the last frame must look identical.
6. **Full render in the background:** `nohup python3 render.py full > render.log 2>&1 &`.
   - About 0.6 s per frame, so a 32 s video takes ~10 min.
   - Wait with `timeout 590 bash -c 'until grep -q "DONE\|Error" render.log; do sleep 15; done'`.
   - If one shot crashes, delete only the affected `chunks/cNNN.mp4` and rerun.
7. **Subtitles:** `python3 captions.py timing.json captions.ass --size 92 --hl word1,word2,…`.
   - Highlight words are normalised: "forty-eight" → `fortyeight`, "3:00" → `300`.
8. **Audio:**
   - Write `cues.json` with `"loop":true` (folds the music tail onto the start), music moods by story beat (start and end on the same mood, e.g. `playful`), `cuts` from the render log's `shots` list, and an SFX on every visible action.
   - For no music, use `"music":[]`.
   - Run `python3 mix.py cues.json voiceover.wav mix.wav`, aiming for about −14 LUFS.
9. **Assemble:** `ffmpeg -y -i video.mp4 -i mix.wav -vf "ass=captions.ass:fontsdir=fonts" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -c:a aac -b:a 256k -shortest -movflags +faststart Final.mp4` (drop `-vf` if there are no subtitles).
   - Grab ~15 frames with `ffmpeg -ss`, check them on a sheet, then send the MP4 with `SendUserFile` (display `render`).
10. **Package:** send the title, description, TikTok caption, pinned comment and tags (format below), then commit and push the project folder.

## Framing rules (why text used to get cut off)
- **Route every sign, label, bubble and stamp through `face(obj)`.** In `shots.js` it rotates the object to face the camera *after* the camera has moved, then calls `fitToFrame(obj, .07, camera, CAP_Y)`.
  - `fitToFrame` (in `engine.js`) shrinks anything too big for the frame and slides anything past an edge back inside.
  - `CAP_Y = -0.27` keeps signs above the subtitle band.
  - Setting `lookAt` before `cam()` was the old bug: the sign faced the previous camera and vanished in single-frame tests.
- `fitToFrame` only shrinks, it never enlarges. Give signs a sensible base size (0.8–2.2 units) close to the subject, not far in the background.
- Draw text into canvases with `fitFont()` so it never overflows its own sign.
- Portrait is narrow: the visible half-width is `d·tan(fov/2)·0.5625`.
  - Keep the subject's face in the **upper 2/3** of the frame.
  - The subject should be about 40–60 % of the frame height. If something is cut off, pull the camera back; don't zoom in.
- Characters must face the camera.
  - If you see someone's back, rotate their group by `PI` (jury box, stenographer).
  - When the camera looks toward +z, world +x appears on the **left** of the screen.
- Use one `court()` world per shot with flags (`judge`, `man`, `sun`/defendant, `jury`, `steno`).
- The split screen (two scenes in one frame) is in the Sleep episode pattern: render both halves with your own cameras and scissor regions inside `u(t)`, and call `fitToFrame(o,.08,thatCamera)` for each half.

## The loop, concretely
- **Shot 0** starts mid-action at `t=0`: the man holds the folder overhead (`holdOverhead(man,f,-2.7)`) and slams it at `t≈0.15`, with screen shake and the kinetic hook text popping on the slam.
- **The last shot** has him storm in through the courtroom doors with a fresh folder, ending exactly on shot 0's `t=0` pose and camera (`C0`). The last ~0.1 s holds that pose.
- Check this with test frames at `0.0` and `END-0.02`.

## Upload package format
```
Title: He Sued the Sun ☀️⚖️ (And Instantly Regretted It)   (+2 alternatives)
Description: 2–3 punchy lines retelling the gag, 1 real fact, "Would you take that deal? YES or NO? 👇", hashtags (#shorts #animation #funny #whatif #<topic> #lawsuit #comedy #3danimation)
TikTok caption: <hook> <emoji> #animation #funny #whatif #<topic> #fyp
Pinned comment: the A/B question, e.g. "Sun twice as far away… but snow in July. YES or NO? ☀️❄️👇"
Tags: comma list (he sued the <x>, what if, funny animation, 3d animation, lawsuit, court, zack d films style …)
```

## Engine cheat-sheet (`scripts/engine.js`)
- **Characters:** `makeMan(p,{suit,cop})` (`.face(mood)`, `.arms[i].sh/el`, `.skinM`, `flail(m,t)`), `pajamaMan`, `poolGuy`.
- **Personified things:** `sunFace`, `sunHappy`, `moonChar`, `earthChar`, `cloudChar`, `gravity`.
- **Worlds and props:** `beachWorld`, `stairsWorld`, `room`, `deskSet`, `nightSky`, `skyScene`, `lounger`, `umbrella`, `palm`, `tree`, `cloud`, `carSimple`, `policeCar`, `label`, `bubble`, `picket`, `canvasTex`, `paintTex`, `textTex`, `RB`/`SPH`/`sm` (rounded parts), `confetti`, `rainLines`, `speedLines`.
- **Helpers in the example episode:** `court()`, `judgeMan()` (exposes `gHead` for gavel gags), `holdOverhead`, `folder`, `stamp`, `sign`, `bub`, `hookText`, `snow`, `sunburnt`, `shades`.
- **Lessons:**
  - Run `node --check` on a `.mjs` copy when you see "READY timeout".
  - A local variable named `face` shadows the helper and crashes the render.
  - In bash `while read` loops use `ffmpeg -nostdin`.
  - If Chromium doesn't match the playwright version, `render.py` uses `/opt/pw-browsers/chromium`, or `$CHROME`.

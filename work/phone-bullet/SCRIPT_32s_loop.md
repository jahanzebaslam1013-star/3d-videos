# "This Guy's Phone Just Stopped a Bullet" — 32 s perfect-loop short

**Voiceover:** `Phone_Bullet_loop_32s.wav` / `.mp3` (Alex, eleven_v4, emotion tags). Exactly **32.00 s**, 1080×1920 @ 30 fps = **960 frames**.
**Loop:** the last word *"…and"* (31.5 s) runs straight into the first line *"This guy's phone just stopped a bullet."*

## Script, shots and on-screen text (times are exact, from the voiceover)

| # | Time (s) | Frames | Voiceover (emotion) | Shot | On-screen text (pops on) |
|---|---|---|---|---|---|
| 1 | 0.00–2.60 | 0–78 | *[curious]* "This guy's phone just stopped a bullet." | Slow-mo: bullet squashed flat against the phone in his chest pocket, red impact rings. Low push-in. | **STOPPED A BULLET?!** @ 0.0 |
| 2 | 2.60–5.88 | 78–176 | *[dramatic]* "A pistol round hits at around 800 miles per hour." | Bullet leaves the pistol in slow motion, camera orbits the bullet. | **800 MPH** @ 3.9 |
| 3 | 5.88–8.36 | 176–251 | *[curious]* "But a phone isn't one solid block… it's layers." | Phone turns slowly in a studio void and starts to separate. | **LAYERS** @ 8.4 |
| 4 | 8.36–12.62 | 251–379 | "Tempered glass, an aluminum frame, and a dense battery." | Exploded view: glass, frame and battery float apart in layers. | **GLASS** @ 9.3 · **FRAME** @ 10.2 · **BATTERY** @ 11.8 |
| 5 | 12.62–15.12 | 379–454 | "Each layer slows the bullet down a little more." | Bullet pushes through each layer, slowing down. | speed counter **800 → 300 → 90 MPH** |
| 6 | 15.12–18.46 | 454–554 | *[excited]* "And against a slow handgun round — that can be just enough." | Slow-mo impact on the pocket: bullet flattens, he flinches (Mixamo hit reaction). | **STOPPED ✓** @ 17.8 |
| 7 | 18.46–22.26 | 554–668 | *[nervous]* "But a rifle round? Almost three times faster." | Rifle fires, slow-mo round with heat shimmer. | **3× FASTER** @ 20.2 |
| 8 | 22.26–24.94 | 668–748 | *[gasps]* "It rips through a WHOLE stack of phones like paper." | Rifle round tears through a stack of phones on a stand, glass shards flying. | *(no text — let the shot breathe)* |
| 9 | 24.94–28.45 | 748–854 | *[sarcastic]* "So… would your phone save you? Probably not." | Close-up: he looks down at the phone and shrugs. | **PROBABLY NOT.** @ 27.2 |
| 10 | 28.45–32.00 | 854–960 | *[mischievous, slow]* "Unless it's one very lucky Tuesday… and" | Calendar flips to TUESDAY, then the camera moves back to the exact frame-1 position as the slow-mo bullet arrives at the pocket. | **TUESDAY** @ 30.4 |

## Making the loop perfect in Blender
1. **Last frame = first frame.** Copy the camera's keyframe on frame 0 and paste it onto frame 959. Do the same for the character's pose, the phone and the bullet.
2. Use **linear** interpolation (or ease-out only) into the final key, so the motion is still moving at the cut instead of coming to a stop.
3. Set the render range to **0–959** (960 frames). Don't render frame 960, or the matching frame plays twice and the loop stutters.
4. The voiceover is already trimmed to the frame: no silence at the start or end.

## Fixing "text cut off / things too zoomed in"
The cause is putting text into the 3D scene, where the camera moves it around and crops it. The fix:

**Text**
- **Don't** make on-screen text as 3D objects in the scene. Add it **in post** as screen-space text: use the Video Sequencer → *Add → Text* strip, or After Effects/CapCut. It then can never leave the frame.
- If you must use 3D text, **parent it to the camera** (*Child Of* constraint, about 2 m in front of the lens) so it moves with the camera.
- **Safe zone for 1080×1920:** keep text between **x 90–990 px** and **y 300–1250 px** from the top.
  - The top 250 px is covered by the TikTok/Shorts UI.
  - The bottom ~650 px is covered by the caption, buttons and description.
- Max **80 % frame width** (≈860 px), **≤ 3 words per line**, 2 lines max, 100–140 px bold font with a thick black outline.
- Turn on **Camera → Viewport Display → Safe Areas** and set *Title Safe* to 0.10 / 0.15. Keep every text and key object inside that box.

**Zoom / framing**
- For a 9:16 frame use a **35–50 mm** lens for character shots and **85–100 mm** for macro shots (bullet, phone layers).
- The hero object should fill **40–60 %** of the frame height, never more than ~70 % of the width.
- Keep the subject's centre in the **middle third** horizontally. Portrait frames are narrow, so if the object is wide, pull the camera back instead of zooming in.
- **Before the full render**, do *View → Viewport Render Image* at the first frame of each shot (10 stills) and check them side by side. If anything touches an edge, pull the camera back.

> I added the same rule to my own animation engine (`fitToFrame` in `work/*/engine.js`). Every sign and label now automatically shrinks or slides back inside an 8 % safe margin each frame, so text can no longer go off-screen in the videos I render.

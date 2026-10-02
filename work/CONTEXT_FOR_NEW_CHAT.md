# Context: my Urdu stickman YouTube channel (paste this into a new chat)

## Who I am
- I'm Jahanzeb, a video editor in Pakistan. I write in Roman Urdu / casual English; please reply in short, clear English.
- I already have an English YouTube channel called **Doodle POV**: second-person ("POV: You're…") story videos, drawn in a hand-drawn stickman style.
- I'm now starting an **Urdu version for a Pakistani audience**. **It has no name and no logo yet** — that's what I need help with first.

## What the new channel makes
- **Format:** "POV / Farz karein aap…" second-person stories. Long-form 16:9 (about 8–9 min, 4 sections) plus 9:16 Shorts later.
- **Language:** Urdu voiceover (I generate it myself with ElevenLabs, a Pakistani-sounding male narrator). On-screen text is **Roman Urdu**. **No subtitles.** Background music and sound effects throughout.
- **Look:** rough "boiling" black outlines, flat muted colours, stick limbs, big expressive anime-style heads, film grain, slow camera push-ins. Pakistani details: shalwar kameez, topi, dupatta, charpai, chai dhaba, village, PKR in lakh.
- **Text styles:** Bebas Neue for titles, numbers and red rubber stamps (e.g. "NO WAY BACK", "FULL GUARANTEE"); Patrick Hand for speech bubbles and labels.
- **Recurring cast:** Hamza (spiky hair, light-blue kameez = "you"), Abba ji (bald, white topi, grey beard, brown waistcoat), Ammi (plum kameez, pink dupatta), Bilal (cousin, slick hair, sunglasses), Agent bhai (moustache, white kameez, black waistcoat, gold watch), Saleem chacha (grey beard).
- **Topics:** real Pakistani life and trending issues told as human stories: dunki / illegal migration, Gulf labour, freelancing, load-shedding, bills, rishta, joint family, MDCAT/CSS, floods, K2, Partition, Mughal history, cricket as human stories, Pakistani what-ifs.
- **Tone and red lines:** emotional, ironic endings, a twist. Respectful of religion and family. No sectarian content, no defamation of real people, nothing that could fall under PECA. Real tragedies are handled respectfully: no gore, cut to black, and cite sources on a closing fact card.
- **How each video gets made:** I give the topic and voiceover. Claude writes the Roman-Urdu script, then the Urdu TTS script, builds every scene in code (Python + cairo), mixes music and SFX, renders 1080p, and makes the thumbnail. I review frames first, then a 30 s test, then full sections.

## Video #1 — finished: "POV: DUNKI"
- **Subtitle:** "POV: You're taking the illegal route to Europe". 8:29, 1080p, 24 fps, −15 LUFS.
- **Story:** Hamza, 24, BA pass, no job, sees cousin Bilal's "Life set hai yaar" photo from Italy → Agent bhai at a chai dhaba asks Rs 25 lakh "full guarantee" → Abba sells the land, Ammi her dowry gold → Dubai → Libya warehouse (80 people, phone taken, Saleem chacha on his 3rd try) → 5 lakh more, Hamza lies to Abba, Abba mortgages the shop → overloaded boat, 3 days, engine dies → a ship passes by → storm, black → Hamza survives in a camp, Saleem doesn't → Abba: "zameen gayi, dukaan gayi… bas wapas aa ja" → twist: Bilal is in the same camp and never reached Italy; the red car was a customer's → Hamza sends home the same kind of fake smiling photo → a village boy thinks "Hamza bhai ki to life set hai" → Agent bhai smiling → fact card.
- **Fact card:** FIA via ProPakistani (July 2026): at least 335 Pakistanis died on this route between June 2023 and April 2026.
- **Closing line:** "Har photo ke peeche ek kahani hoti hai… aur kuch kahaniyan kabhi post nahi hotin."
- **Thumbnail:** "POV: DUNKI" + yellow banner "25 LAKH KA SAFAR" + "FULL GUARANTEE?" stamp, overloaded boat, shocked Hamza, red/black.
- **Ending card:** for now the video ends on a plain "DOODLE POV" text placeholder. **It will be replaced once I pick the new channel's name and logo** (only the last few seconds need re-rendering).

## Where things are
- **Video files:** I have the full 1080p video as 9 clips to join in Premiere, a 720p preview, and the thumbnail. My Mac is also rendering the full-quality master with `build_mac.sh`.
- **Code:** GitHub `jahanzebaslam1013-star/3d-videos`, branch `claude/magical-thompson-51tel9`, folder `work/project/`. It contains `sec1–sec4.py` (scenes), `mix_sec*.py` (audio), the finished audio, the fonts, `thumb.py` and `build_mac.sh`.
- **Mac folder:** `Documents/Main Channels/Urdu Stickman/Dunky Video/`.

## What I need help with now (in the new chat)
1. **Channel name** for the Urdu channel. It should:
   - work for Pakistanis (Urdu or Roman Urdu or a mix, easy to say and spell)
   - fit second-person POV stories with a stickman look
   - ideally be available as a YouTube handle
   - possibly relate to "Doodle POV" (same family) — or not; give options both ways
   - **For each idea:** the name, its meaning, the @handle, why it works, and any risk
2. **Logo and branding:** logo concept (something I can draw in the same rough black-outline stickman style), colours (current palette: black ink, warm paper beige, red stamp #c0322a, gold #ffd66a), profile picture, banner text, and a short end-card/intro sting idea.
3. **Channel setup:** description (Urdu + English), keywords/tags, playlists, upload schedule, Shorts strategy, and title and thumbnail style rules.
4. **Launch plan for "POV: DUNKI":** title options (Urdu/Roman Urdu/English mix), description with source link, tags, pinned comment, and 3–5 Shorts cut from it.
5. **Next 5 video ideas** for Pakistan, each with: Urdu title + English meaning, a 3-second hook, why now (with sources), Short/Long/both, risk (green/yellow/red), and a score out of 10.

## After that (back in the video workflow)
- Replace the "DOODLE POV" placeholder at the end of DUNKI with the new name/logo and re-render the last section.
- Start video #2 from the chosen idea: script → my voiceover (`1.mp3 … 4.mp3`) → frames review → 30 s test → full sections → final video and thumbnail.

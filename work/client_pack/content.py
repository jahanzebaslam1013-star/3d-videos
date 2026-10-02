"""All text for the client pitch pack. build.py turns this into PDF + DOCX."""

TITLE = "Animated Video Services"
SUBTITLE = "Client pitch pack for Upwork, Fiverr and LinkedIn"
OWNER = "Jahanzeb Aslam"
PREPARED_FOR = "Prepared for the profile and sales manager"
DATE = "October 2026"

INTRO = [
    "This pack has everything you need to sell my animation services: the niche names, keywords for "
    "gigs and profiles, sample frames, short client hooks, and prices.",
    "We offer three styles. Stickman POV animation comes as Shorts or long-form YouTube videos, and "
    "there are also low-poly 3D what-if Shorts. All three are produced with our own in-house animation "
    "pipeline: the script, voiceover, every scene, captions, music and sound effects. That keeps them "
    "fast and affordable. On top of that, we offer a premium Blender service for clients who want the "
    "cinematic, viral 3D Shorts look.",
    "Every project follows the same steps. The client approves the script, then sees sample frames "
    "(a storyboard) before the full render. This keeps revisions low, so tell clients about it.",
]

PROOF = [
    ("102% retention", "“Gravity Got Fired”, a low-poly 3D what-if Short from my own channel. Viewers watched it to the end and replayed it."),
    ("8:45 long-form POV story", "“POV: You're a Dictator's Personal Bodyguard”, a full stickman POV story in 4 sections with music, SFX, a thumbnail and a Premiere timeline."),
    ("Own channels in this format", "Doodle POV, our English stickman POV story channel. We make this content for ourselves, not just for clients."),
    ("English + Urdu", "Professional AI narration in English (deep American narrator) and Urdu. Other languages are available on request."),
]

# ---- the four niches -------------------------------------------------------
NICHES = [
    {
        "id": "stickman",
        "group": "Part 1 · Stickman POV Animation · Section 1 of 2: Shorts",
        "num": "01",
        "name": "Stickman POV Animated Shorts",
        "tagline": "Hand-drawn stickman “POV” Shorts for TikTok, YouTube Shorts and Reels (9:16, 30–90 s)",
        "images": ["stickman_short_1.jpg", "stickman_short_2.jpg", "stickman_short_3.jpg"],
        "image_layout": "row3",
        "caption": "Real frames from our stickman Shorts pipeline (1080×1920), shown with captions on.",
        "description": (
            "Vertical 30–90 second Shorts in a hand-drawn stickman style. They have rough “boiling” black "
            "outlines, flat muted colours and big expressive anime-style heads. Bold text pops in, along with red "
            "rubber stamps (FIRED, APPROVED, NO WAY BACK), speech bubbles, film grain and slow camera "
            "push-ins. Each one has a deep narrator voiceover, word-timed captions, a music bed and a sound "
            "effect on every action. Stories are told as “POV: You…” so the viewer is the main character, "
            "which is why people watch to the end. This is ideal for faceless channels that need a steady "
            "supply of Shorts."
        ),
        "main_keyword": "stickman animation",
        "tags5": ["stickman animation", "animated shorts", "pov animation", "youtube shorts", "faceless youtube"],
        "keywords": [
            "stickman animation", "stick figure animation", "POV animation", "POV shorts", "animated YouTube Shorts",
            "TikTok animation", "Instagram Reels animation", "faceless YouTube shorts", "faceless channel content",
            "YouTube automation", "cash cow shorts", "2D animated shorts", "doodle animation", "hand-drawn animation",
            "cartoon story shorts", "animated storytelling", "story time animation", "viral shorts animation",
            "relatable animation", "motivational animation", "what would you do shorts", "explainer shorts",
            "vertical video animation", "9:16 animation", "short-form video content", "animated captions video",
        ],
        "clients": [
            "Faceless YouTube / TikTok channel owners and YouTube automation agencies",
            "Story, motivation, “life lessons” and psychology-fact channels",
            "Coaches, apps and brands that want relatable Shorts for social media",
            "Podcasters who want a story moment turned into an animated clip",
        ],
        "hook_short": (
            "Faceless channel stuck at low views? I make hand-drawn stickman “POV” Shorts that people "
            "watch to the end. You get the script, voiceover, captions, music and SFX, all done for you. A "
            "Short costs $35–45 per minute and arrives in 48 hours. Want a free sample frame of your first "
            "scene?"
        ),
        "hook_long": (
            "Hi [Name], I saw your channel [channel]. Your topics would work really well as stickman "
            "“POV: You…” Shorts, because putting the viewer in the story keeps retention high. I make "
            "these end-to-end: script polish, a deep narrator voiceover, animated scenes, word-timed captions, "
            "music and sound effects. You approve sample frames before the full render, so there are no "
            "surprises. If you send me one topic, I'll make a free sample frame so you can see the style on "
            "your own idea."
        ),
        "gig_titles": [
            "I will create stickman POV animated shorts for YouTube, TikTok and Reels",
            "I will make faceless stickman story shorts with voiceover and captions",
        ],
        "upwork_title": "Stickman POV Animation | Faceless YouTube Shorts & TikTok Story Videos",
        "packages": [
            ("Basic", "$35/min", "Your script & voiceover · animation, captions, music & SFX · 1 revision · 2 days"),
            ("Standard", "$40/min", "Script polish + AI narrator · captions, music & SFX · 2 revisions · 2 days"),
            ("Premium", "$45/min", "Script written from your topic · premium narrator · cover image · 3 revisions · 3 days"),
        ],
        "bulk": "Priced per finished minute. For monthly volume deals, ask Jahanzeb for a quote.",
        "range": "$35 – $45 per minute",
        "delivery": "1–3 days",
    },
    {
        "id": "longform",
        "group": "Part 1 · Stickman POV Animation · Section 2 of 2: Long-form",
        "num": "02",
        "name": "Long-Form Stickman POV Animated Videos",
        "tagline": "Long-form 16:9 YouTube story videos (5–12 min) in the hand-drawn stickman style, plus Shorts cut-downs",
        "images": ["longform_thumbnail.jpg", "longform_scenes.jpg"],
        "image_layout": "row2",
        "caption": "From our long-form video “POV: You're a Dictator's Personal Bodyguard”: the thumbnail and four scenes (banquet, freeze frame, rule card, TV news).",
        "description": (
            "Full YouTube POV videos told from the viewer's point of view in the present tense (“You step forward.”), "
            "the format used by big story-animation channels. A cold-open hook drops the viewer into the most dangerous "
            "moment. Then a “3 years earlier…” rewind tells the story in order, with a twist and an ironic "
            "ending. The visuals use the same rough stickman style with mood-based colour palettes, maps, "
            "documents, stamps, freeze frames, rewind effects, counters and title cards. The music and Foley "
            "are cut to every beat. The client gets the video in sections, a thumbnail, and an optional "
            "Premiere Pro timeline file."
        ),
        "main_keyword": "animated story video",
        "tags5": ["animated story video", "youtube automation", "stickman animation", "2d animation", "faceless youtube"],
        "keywords": [
            "long-form POV videos", "POV story animation", "POV you're videos", "animated story videos",
            "faceless YouTube channel", "YouTube automation videos", "cash cow YouTube", "2D story animation",
            "stickman story animation", "animated documentary", "edutainment animation", "history animation",
            "hypothetical scenario videos", "what if story videos", "true story animation", "crime story animation",
            "survival story animation", "job POV videos", "animated narration video", "script to animated video",
            "long-form YouTube animation", "2D explainer video", "YouTube channel animation", "Urdu animation",
            "animated storytelling for YouTube", "faceless content creator",
        ],
        "clients": [
            "Faceless / YouTube automation channel owners (story, history, crime, “what if”, careers)",
            "Edutainment and history creators who want a consistent weekly animated format",
            "NGOs and awareness campaigns (migration, health, safety) that want an emotional story video",
            "Channels in any niche that want English or Urdu narration",
        ],
        "hook_short": (
            "I turn your script into an 8-minute “POV: You're…” animated story video in the hand-drawn "
            "stickman style that big story channels use, for $30 per minute ($240 for 8 minutes). You get full "
            "scenes, voiceover, music, SFX and a thumbnail in 5–10 days. Your channel gets a consistent weekly look without hiring an animation team."
        ),
        "hook_long": (
            "Hi [Name], I produce long-form POV animated story videos (“POV: You're a…”) end to end. I can "
            "write the script with a cold-open hook, a rewind and a twist ending, voice it, animate every scene "
            "and cut music and sound effects to each beat. You review it section by section. You also see "
            "frames before anything is fully rendered. I just finished an 8:45 video this way, “POV: You're a "
            "Dictator's Personal Bodyguard”, and can share it. Are you looking for one video, or a weekly upload partner?"
        ),
        "gig_titles": [
            "I will create a long form POV animated story video for your YouTube channel",
            "I will make long form stickman story animation for faceless YouTube channels",
        ],
        "upwork_title": "Animated Story Videos for YouTube | 2D Stickman “POV” Long-Form & Faceless Channels",
        "packages": [
            ("Rate", "$30/min", "Any length, billed per finished minute · full animation, AI narrator, music & SFX · thumbnail"),
            ("8-min video", "$240", "Our standard length · full package as above · 2 revisions · 5–10 days"),
            ("Examples", "", "5 min = $150 · 10 min = $300 · 12 min = $360"),
        ],
        "bulk": "Weekly upload partner: 4 videos a month at the same $30 per minute (4 × 8 min = $960).",
        "range": "$30 per minute (8 min = $240)",
        "delivery": "5–10 days",
    },
    {
        "id": "lowpoly",
        "group": "Part 2 · 3D Animation",
        "num": "03",
        "name": "3D Low-Poly “What If” Story Shorts",
        "tagline": "Funny 3D animated what-if Shorts with talking planets, objects and characters (9:16, 20–60 s)",
        "images": ["lowpoly_short_1.jpg", "lowpoly_short_2.jpg", "lowpoly_short_3.jpg", "lowpoly_short_4.jpg"],
        "image_layout": "row4",
        "caption": "Real frames from our low-poly 3D Shorts pipeline (1080×1920). Captions are off here.",
        "description": (
            "Viral-style vertical 3D Shorts built around an absurd “what if” premise. A natural thing becomes "
            "a person with a job or feelings: gravity gets fired, the moon goes on strike, the Earth gets "
            "dizzy. The look is flat-shaded, low-poly 3D with soft shadows, warm colours and painterly "
            "skies. A recurring cast of characters makes it feel like a series. Every Short opens on action "
            "in frame 1, escalates line by line, includes one real science fact so people share it, and ends "
            "on a loop or a twist. Each one comes with a deadpan narrator, bold word-by-word captions, a "
            "music bed and SFX on every gag. Our best one so far reached 102% retention (viewers "
            "watched to the end and replayed it)."
        ),
        "main_keyword": "3d animated shorts",
        "tags5": ["3d animation", "animated shorts", "youtube shorts", "what if", "explainer video"],
        "keywords": [
            "3D animated shorts", "3D cartoon shorts", "low poly animation", "low poly 3D", "what if animation",
            "what if shorts", "science shorts animation", "educational shorts", "edutainment shorts",
            "viral 3D shorts", "TikTok 3D animation", "YouTube Shorts 3D", "funny 3D animation",
            "3D story animation", "3D explainer", "talking objects animation", "personified planets animation",
            "fun facts animation", "kids educational animation", "brand mascot animation",
            "brand storytelling shorts", "looping shorts", "animated captions", "faceless 3D channel",
        ],
        "clients": [
            "Science, fun-facts and “what if” channels (YouTube Shorts, TikTok, Instagram)",
            "EdTech apps, schools and kids' brands that want fun explainers",
            "Brands that want a mascot or product to “come alive” in viral-style Shorts",
            "Faceless channel owners who want a 3D look without 3D-studio prices",
        ],
        "hook_short": (
            "“What if the moon went on strike?” That kind of 3D Short reached 102% retention on my own "
            "channel, so viewers watched it to the end and replayed it. I make low-poly 3D what-if Shorts end "
            "to end, from script and narration to animation, captions and sound. $50 per Short, delivered in 3 days."
        ),
        "hook_long": (
            "Hi [Name], your audience would love a 3D “what if” series built on your topics. I make "
            "low-poly animated Shorts where everyday things come alive (planets, clouds, objects, even your "
            "mascot). Every one has a hook in the first frame, escalating gags, one real fact and a loop "
            "ending that drives rewatches. One of mine reached 102% retention. "
            "Should I pitch you 3 episode ideas for your channel?"
        ),
        "gig_titles": [
            "I will create viral 3D what if animated shorts for YouTube and TikTok",
            "I will make funny low poly 3D story shorts with narration and captions",
        ],
        "upwork_title": "3D Animated Shorts | Viral “What If” Low-Poly Stories for YouTube Shorts & TikTok",
        "packages": [
            ("Per Short", "$50", "Up to 60 s · script + narrator · 3D animation · captions, music & SFX · 2 revisions · 2–4 days"),
        ],
        "bulk": "Monthly series: $50 per Short. Recurring characters stay consistent across the series. Custom mascots or brand characters: ask Jahanzeb for a quote.",
        "range": "$50 per Short",
        "delivery": "2–4 days",
    },
    {
        "id": "blender",
        "group": "Part 3 · Premium Blender 3D",
        "num": "04",
        "name": "Premium 3D Blender Shorts (Zack D. Films style)",
        "tagline": "Cinematic, custom-built Blender scenes and characters for viral 3D Shorts (9:16, 20–60 s)",
        "images": [],
        "image_layout": "none",
        "caption": "",
        "description": (
            "This is our top tier. Every Short is a one-off mini film made in Blender, with custom-modelled "
            "sets and characters, cinematic lighting, detailed textures and character animation. It is the "
            "polished 3D look of the biggest viral Shorts channels: “how it works” and “what happens "
            "if” stories, body and medical explainers, satisfying physics and dramatic mini-stories. "
            "These take far more hours per second than our in-house pipelines, so they are priced as premium. "
            "We still deliver the full package: script, narration, captions, music and sound design."
        ),
        "main_keyword": "blender 3d animation",
        "tags5": ["blender animation", "3d animation", "3d animated shorts", "3d character animation", "cgi shorts"],
        "keywords": [
            "Blender animation", "Blender 3D animation", "3D character animation", "Zack D Films style",
            "3D animated shorts", "3D storytelling shorts", "CGI shorts", "cinematic 3D shorts",
            "3D medical animation", "human body 3D animation", "how it works 3D animation",
            "3D science animation", "satisfying 3D animation", "3D product animation", "3D explainer video",
            "viral 3D shorts", "3D cartoon character", "custom 3D character", "3D scene design",
        ],
        "clients": [
            "Established Shorts channels (science, health, “what happens if”) that want a premium look",
            "Health, medical and fitness brands that need clear 3D body explainers",
            "Product brands and startups that want a cinematic 3D story ad",
            "Agencies that outsource 3D Shorts production",
        ],
        "hook_short": (
            "Want the cinematic 3D look of the biggest viral Shorts channels? We build custom Blender scenes "
            "and characters, so every Short is a one-off mini film, with script, narration, captions and "
            "sound included. $100–200 per Short, delivered in 5–10 days."
        ),
        "hook_long": (
            "Hi [Name], we produce premium 3D Shorts in Blender in the style of the top viral science and "
            "“what happens if” channels. Custom sets, characters and cinematic lighting, with script, "
            "narration and sound design included. If you want to test it, we can start with one Short and "
            "then move to a monthly series. What topic would you like to see first?"
        ),
        "gig_titles": [
            "I will create cinematic Blender 3D animated shorts in viral storytelling style",
            "I will make 3D character animation shorts in Blender for YouTube and TikTok",
        ],
        "upwork_title": "Blender 3D Animated Shorts | Cinematic Viral-Style Stories, Science & Product Explainers",
        "packages": [
            ("Basic", "$100", "Up to 30 s · simple set · library characters · narration, captions, music & SFX · 1 revision · 5 days"),
            ("Standard", "$150", "45–60 s · custom scene · 1 custom character · full sound design · 2 revisions · 7 days"),
            ("Premium", "$200+", "Up to 60 s · several custom characters or realistic / medical style · 3 revisions · 7–10 days · quote higher for complex work"),
        ],
        "bulk": "Series pricing: quote per project. Offer about 10% off when a client books 4 or more Blender Shorts a month.",
        "range": "$100 – $200+ per Short",
        "delivery": "5–10 days",
        "note": (
            "Naming tip: “Zack D. Films” is a real creator's name. Use it only as a search keyword in "
            "descriptions or proposals (“in the style of…”). Never put it in gig titles, tags or thumbnails, "
            "and never copy their characters. Fiverr and Upwork can flag other people's names in titles."
        ),
        "sample_note": "Blender sample renders: ask Jahanzeb for the latest portfolio clips before pitching this tier.",
    },
]

ADDONS = [
    ("Rush delivery (24–48 h)", "+30%"),
    ("Script writing from a topic", "+$15 per Short · +$60 per long video"),
    ("Urdu (or 2nd language) version", "+$20 per Short · +$80 per long video"),
    ("Custom thumbnail / cover", "+$15"),
    ("Extra revision", "+$10 each"),
    ("Shorts cut-downs from a long video", "+$25 each"),
    ("Captions off / custom caption style", "Free"),
    ("Commercial use rights", "Included"),
]

PROCESS = [
    ("Brief", "The client sends a topic or script, the target platform, length, language and 1–2 reference videos."),
    ("Script", "We write or polish the script (hook, escalation, twist), and the client approves it."),
    ("Voice", "AI narrator (English or Urdu) or the client's own voiceover. The client approves a sample."),
    ("Frames", "We send a storyboard of real frames before the full render, so fixes are cheap here."),
    ("Render", "Full animation, captions, music and SFX, loudness-matched for YouTube and TikTok."),
    ("Deliver", "MP4 (1080×1920 or 1920×1080), plus a thumbnail and project files if they were in the package."),
]

NEED_FROM_CLIENT = [
    "Topic or finished script (we can write it)",
    "Platform and length (Shorts, TikTok, Reels or long-form YouTube)",
    "Language and voice preference (or their own voiceover file)",
    "1–2 reference videos they like",
    "Brand colours, logo or mascot (if any)",
    "Deadline and how many videos per month",
]

RULES = [
    "No copyrighted characters or logos (no Disney, Marvel, anime characters and so on). Everything is drawn original.",
    "No real politicians or real people shown in a defamatory way. Fictional countries and leaders are fine.",
    "Violence is implied, never graphic, and content stays advertiser-friendly. No adult content.",
    "Long-form and Blender jobs taken off-platform (LinkedIn or direct): 50% upfront, 50% on delivery.",
    "Always confirm the script and voice before quoting a delivery date. Delivery time starts after approval.",
    "Platform fees: Fiverr keeps 20%, and Upwork's fee varies (about 0–15%). The prices here are list prices, so keep them.",
]

LINKEDIN_IDEAS = [
    "Before/after post: a client's plain script → 3 finished frames → “this became a 60-second Short”.",
    "Results post: “This 3D Short hit 102% retention. Here's why it worked” (hook, escalation, loop).",
    "Behind-the-scenes carousel: script → storyboard frames → final video for a POV story.",
    "Offer post to faceless-channel owners: “I'll animate your next story as a stickman POV Short. A free sample frame is on me.”",
]

LINKS = [
    ("Doodle POV (YouTube channel)", "[add link]"),
    ("“Gravity Got Fired” (3D low-poly Short)", "[add link]"),
    ("“POV: You're a Dictator's Personal Bodyguard” (long-form POV video)", "[add link]"),
    ("Blender portfolio clips", "[add link]"),
]

PROFILE_HEADLINES = [
    ("Upwork headline", "Animated Story Videos & Shorts | Stickman POV · 3D What-If · Blender 3D"),
    ("Fiverr seller tagline", "I animate faceless YouTube stories, Shorts and 3D what-ifs that people watch to the end"),
    ("LinkedIn headline", "Animator & Video Producer | Faceless YouTube Stories, Viral Shorts & 3D Animation | English + Urdu"),
]

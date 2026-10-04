#!/usr/bin/env python3
"""timing.json -> captions.ass (burned in by ffmpeg at assembly).
  python3 captions.py timing.json captions.ass --hl word1,word2 [--words 3] [--size 74] [--margin 560]
Chunks each line into groups of <= N words (breaking after punctuation), shows each
group from its first word's start until the next group, with a quick pop-in.
Highlight words (--hl) are drawn in the accent colour (#ff5b3a)."""
import json, sys, re, argparse
ap = argparse.ArgumentParser()
ap.add_argument("timing"); ap.add_argument("out")
ap.add_argument("--hl", default=""); ap.add_argument("--words", type=int, default=3)
ap.add_argument("--size", type=int, default=74); ap.add_argument("--margin", type=int, default=560)
ap.add_argument("--w", type=int, default=1080); ap.add_argument("--h", type=int, default=1920)
a = ap.parse_args()
HL = {w.strip().lower() for w in a.hl.split(",") if w.strip()}
T = json.load(open(a.timing))
def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {a.w}
PlayResY: {a.h}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,ZkitCaption,{a.size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H78000000,0,0,0,0,100,100,1,0,1,5,3,2,70,70,{a.margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
for li, line in enumerate(T):
    words = line["words"]; groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= a.words or re.search(r"[.,!?;:…]$", w["w"]): groups.append(cur); cur = []
    if cur: groups.append(cur)
    for gi, g in enumerate(groups):
        st = g[0]["start"] - 0.04
        en = groups[gi + 1][0]["start"] - 0.04 if gi + 1 < len(groups) else line["end"] + 0.12
        txt = " ".join(("{\\c&H3A5BFF&}" + w["w"] + "{\\c&HFFFFFF&}") if re.sub(r"[^a-z']", "", w["w"].lower()) in HL else w["w"] for w in g)
        ev.append(f"Dialogue: 0,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\fscx82\\fscy82\\t(0,120,\\fscx104\\fscy104)\\t(120,180,\\fscx100\\fscy100)}}{txt}")
open(a.out, "w", encoding="utf-8").write(hdr + "\n".join(ev) + "\n")
print(len(ev), "caption events ->", a.out)

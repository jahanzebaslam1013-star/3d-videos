#!/usr/bin/env python3
"""Exact per-word timing.json from an ElevenLabs transcript (creative_transcribe_audio, eleven_scribe_v1, free).
  python3 build_timing.py words.json script.txt timing.json --offset 0.08 [--tempo 1.0]
words.json : the transcript's "words" list  [{"text":"This","start":0.16,"end":0.32}, ...]  (raw take times)
script.txt : one spoken line per row, WITHOUT audio tags.  [tags] in the transcript are skipped.
--offset/--tempo come from trim_voice.py, so times line up with the trimmed voiceover.wav."""
import sys, json, re, argparse
ap = argparse.ArgumentParser(); ap.add_argument("words"); ap.add_argument("script"); ap.add_argument("out")
ap.add_argument("--offset", type=float, default=0.0); ap.add_argument("--tempo", type=float, default=1.0)
a = ap.parse_args()
W = json.load(open(a.words)); W = W.get("words", W) if isinstance(W, dict) else W
W = [w for w in W if w.get("type", "word") == "word" and not re.fullmatch(r"\[.*\]", w["text"].strip()) and re.search(r"\w", w["text"])]
f = lambda t: round(max(0.0, (t - a.offset) / a.tempo), 3)
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
lines = [l.strip() for l in open(a.script, encoding="utf-8") if l.strip()]
out, i = [], 0
for l in lines:
    toks = l.split(); ws = []
    for tk in toks:
        if i >= len(W): sys.exit(f"ran out of transcript words at line: {l}")
        if norm(W[i]["text"]) != norm(tk): print(f"warn: script '{tk}' vs transcript '{W[i]['text']}'", file=sys.stderr)
        ws.append({"w": tk, "start": f(W[i]["start"]), "end": f(W[i]["end"])}); i += 1
    out.append({"text": l, "start": ws[0]["start"], "end": ws[-1]["end"], "words": ws})
if i != len(W): print(f"warn: {len(W) - i} transcript words left over", file=sys.stderr)
json.dump(out, open(a.out, "w"), indent=1)
for k, r in enumerate(out): print(f"{k:2d} {r['start']:6.2f} {r['end']:6.2f}  {r['text']}")

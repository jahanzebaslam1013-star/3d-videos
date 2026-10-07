#!/usr/bin/env python3
"""YouTube SRT from timing.json (word times) -> phrase-sized cues.
  python3 srt.py timing.json out.srt [--t0 0.15] [--max 6]
Breaks after punctuation, never leaves a 1-2 word orphan, max N words per cue."""
import json, re, argparse
ap = argparse.ArgumentParser(); ap.add_argument('timing'); ap.add_argument('out'); ap.add_argument('--t0', type=float, default=.15); ap.add_argument('--max', type=int, default=6)
a = ap.parse_args(); T = json.load(open(a.timing))
def ts(t):
    ms = int(round(max(0, t) * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000); return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
cues = []
for line in T:
    ws = line['words']; i = 0
    while i < len(ws):
        j = i; best = None
        while j < len(ws) and j - i < a.max:
            if re.search(r'[.,?!;:]$', ws[j]['w']): best = j; break
            j += 1
        end = best if best is not None else min(len(ws) - 1, i + a.max - 1)
        if best is None:
            for k in range(end + 1, min(len(ws), end + 4)):
                if re.search(r'[.,?!;:]$', ws[k]['w']): end = k; break
        if len(ws) - 1 - end <= 2 and len(ws) - i <= a.max + 2: end = len(ws) - 1   # avoid orphans
        cues.append(ws[i:end + 1]); i = end + 1
out = []
for k, g in enumerate(cues):
    st = g[0]['start'] + a.t0; en = g[-1]['end'] + a.t0 + .15
    if k + 1 < len(cues): en = min(en, cues[k + 1][0]['start'] + a.t0 - .02)
    out.append(f"{k+1}\n{ts(st)} --> {ts(en)}\n{' '.join(w['w'] for w in g)}\n")
open(a.out, 'w').write('\n'.join(out)); print(len(out), 'cues ->', a.out)

"""Build Urdu + English .srt for DUNKI from the voice line timings (partN.json)."""
import json, re, os
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
ENDS = {1: 121.39 + 1.7}            # section lengths = secN.END (matches audio/secN.m4a)
times = []; off = 0.0
for n in range(1, 5):
    j = json.load(open(os.path.join(P, f'part{n}.json')))
    times += [(a + off, b + off) for a, b in j['lt']]
    off += ENDS.get(n, j['dur'] + (3.6 if n == 4 else 0.6))
ur = [re.sub(r'\s*\[[^\]]+\]\s*', ' ', l).strip() for l in open(os.path.join(P, 'all.txt'), encoding='utf-8').read().splitlines()]
en = open(os.path.join(HERE, 'en_lines.txt'), encoding='utf-8').read().splitlines()
assert len(ur) == len(en) == len(times) == 104

def chunks(s, maxc):
    if len(s) <= maxc: return [s]
    parts = [p.strip() for p in re.split(r'(?<=[۔?!.])\s+', s) if p.strip()]
    out, cur = [], ''
    for p in parts:
        if cur and len(cur) + 1 + len(p) > maxc: out.append(cur); cur = p
        else: cur = (cur + ' ' + p).strip()
    out.append(cur); return out

def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def write(lines, name, maxc):
    cues = []
    for (a, b), s in zip(times, lines):
        cs = chunks(s, maxc); tot = sum(len(c) for c in cs); t = a
        for c in cs:
            d = (b - a) * len(c) / tot; cues.append((t, t + d, c)); t += d
    with open(os.path.join(HERE, name), 'w', encoding='utf-8') as f:
        for i, (a, b, c) in enumerate(cues, 1):
            nxt = cues[i][0] if i < len(cues) else b + 1
            f.write(f'{i}\n{ts(a)} --> {ts(min(b + 0.25, nxt - 0.02))}\n{c}\n\n')
    print(name, len(cues), 'cues, last ends', ts(cues[-1][1]))

write(ur, 'Dunki_ur.srt', 60)
write(en, 'Dunki_en.srt', 80)

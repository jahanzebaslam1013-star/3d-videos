#!/usr/bin/env python3
"""Offline script-to-voiceover aligner (no speech model needed).
Usage: python3 align.py script.txt voiceover.(wav|mp3) timing.json
script.txt: one sentence (or caption-sized line) per line, in spoken order.
Finds pauses in the voiceover, then picks the pause set that best matches each
line's expected length (by character count) with dynamic programming.
Word times inside a line are spread over its voiced frames by word length."""
import sys, json, subprocess, numpy as np

def load(path, sr=16000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32), sr

def main(script, audio, out):
    lines = [l.strip() for l in open(script, encoding="utf-8") if l.strip()]
    x, sr = load(audio)
    hop = int(sr * 0.01)
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop * 3) / (hop * 3), "same")[::hop] + 1e-12)
    db = 20 * np.log10(rms / (np.percentile(rms, 99) + 1e-9))
    floor = np.percentile(db, 5)
    thr = max(-40.0, floor + 0.3 * (-floor))  # adapts to background noise
    voiced = db > thr
    # pauses = runs of unvoiced frames >= 0.09s
    pauses, i, n = [], 0, len(voiced)
    while i < n:
        if not voiced[i]:
            j = i
            while j < n and not voiced[j]: j += 1
            if j - i >= 9: pauses.append((i, j))
            i = j
        else: i += 1
    vi = np.where(voiced)[0]
    s0, s1 = vi[0], vi[-1] + 1
    cand = [(a, b) for a, b in pauses if a > s0 and b < s1]  # interior pauses (frames)
    cum_voiced = np.concatenate([[0], np.cumsum(voiced)])
    w = np.array([max(3, len(l)) + 6 for l in lines], float)  # expected weight per line
    K = len(lines)
    if K == 1: bounds = []
    else:
        total_v = cum_voiced[s1] - cum_voiced[s0]
        exp_len = w / w.sum() * total_v
        exp_cum = np.cumsum(exp_len)[:-1]
        P = len(cand); cpos = np.array([(a + b) / 2 for a, b in cand]); clen = np.array([b - a for a, b in cand])
        vc = np.array([cum_voiced[int(c)] - cum_voiced[s0] for c in cpos])
        INF = 1e18
        # dp[k][p]: best cost with boundary k at pause p
        dp = np.full((K - 1, P), INF); bk = np.zeros((K - 1, P), int)
        def seg_cost(v_len, e): return ((v_len - e) / (e + 20)) ** 2 * 100
        bonus = -np.log1p(clen / 10.0) * 2.5
        for p in range(P):
            dp[0, p] = seg_cost(vc[p], exp_len[0]) + bonus[p]
        for k in range(1, K - 1):
            win = max(300, exp_cum[k] * 0.25)
            for p in range(P):
                if abs(vc[p] - exp_cum[k]) > win: continue
                prev = dp[k - 1, :p] + seg_cost(vc[p] - vc[:p], exp_len[k]) if p else np.array([])
                if len(prev):
                    q = int(np.argmin(prev)); dp[k, p] = prev[q] + bonus[p]; bk[k, p] = q
        last = dp[K - 2] + seg_cost((cum_voiced[s1] - cum_voiced[s0]) - vc, exp_len[-1])
        p = int(np.argmin(last)); bounds = [p]
        for k in range(K - 2, 0, -1): p = bk[k, p]; bounds.append(p)
        bounds = bounds[::-1]
    edges = [s0] + [x for p in bounds for x in cand[p]] + [s1]
    res = []
    for k, l in enumerate(lines):
        a, b = edges[2 * k], edges[2 * k + 1]
        words = l.split(); ww = np.array([len(q) + 1 for q in words], float)
        vf = np.where(voiced[a:b])[0] + a
        if len(vf) == 0: vf = np.arange(a, b)
        cw = np.concatenate([[0], np.cumsum(ww)]) / ww.sum() * (len(vf) - 1)
        wt = [{"w": q, "start": round(vf[int(cw[j])] / 100, 3), "end": round(vf[int(cw[j + 1])] / 100 + .01, 3)} for j, q in enumerate(words)]
        res.append({"text": l, "start": round(a / 100, 3), "end": round(b / 100, 3), "words": wt})
    json.dump(res, open(out, "w"), indent=1)
    for r in res: print(f"{r['start']:7.2f} {r['end']:7.2f}  {r['text']}")

if __name__ == "__main__":
    main(*sys.argv[1:4])

#!/usr/bin/env python3
"""Shrink every pause longer than MAXP to MAXP seconds and trim the head/tail -> voiceover.wav"""
import subprocess, sys, numpy as np, soundfile as sf
src = sys.argv[1]; MAXP = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2
sr = 44100
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
hop = int(sr * .01); rms = np.sqrt(np.convolve(x**2, np.ones(hop*3)/(hop*3), 'same')[::hop] + 1e-12)
v = 20*np.log10(rms/np.percentile(rms, 99)) > -38
vi = np.where(v)[0]; s0, s1 = max(0, vi[0]-3), min(len(v), vi[-1]+6)
keep = np.ones(len(v), bool); keep[:s0] = False; keep[s1:] = False
i = s0
while i < s1:
    if not v[i]:
        j = i
        while j < s1 and not v[j]: j += 1
        L = j - i; m = int(MAXP*100)
        if L > m: keep[i + m//2: j - (m - m//2)] = False
        i = j
    else: i += 1
segs = []; i = 0
while i < len(keep):
    if keep[i]:
        j = i
        while j < len(keep) and keep[j]: j += 1
        seg = x[i*hop:j*hop].copy(); f = min(len(seg)//2, int(.008*sr))
        seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f); segs.append(seg); i = j
    else: i += 1
y = np.concatenate(segs); sf.write("voiceover.wav", y, sr); print(f"{len(x)/sr:.2f}s -> {len(y)/sr:.2f}s")

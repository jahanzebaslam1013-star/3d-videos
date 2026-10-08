#!/usr/bin/env python3
"""Trim an ElevenLabs take for a seamless loop: cut the silence before the first word and after the last.
  python3 trim_voice.py raw.mp3 voiceover.wav [--target 32.0]
--target speeds the take up/down (atempo) so it lasts exactly that long (keep within ±8 %).
Prints  OFFSET=<s> TEMPO=<x> DUR=<s>  -> pass OFFSET/TEMPO to build_timing.py."""
import sys, subprocess, argparse, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("raw"); ap.add_argument("out"); ap.add_argument("--target", type=float); ap.add_argument("--pad", type=float, default=0.03)
a = ap.parse_args(); SR = 44100
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", a.raw, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
h = SR // 100; db = 20 * np.log10(np.array([np.sqrt(np.mean(x[i:i + h] ** 2)) for i in range(0, len(x) - h, h)]) + 1e-9)
v = np.where(db > -40)[0]; s0 = max(0, v[0] / 100 - a.pad); s1 = min(len(x) / SR, v[-1] / 100 + a.pad * 2)
tempo = 1.0; filt = f"atrim={s0:.3f}:{s1:.3f},asetpts=PTS-STARTPTS"
if a.target:
    tempo = (s1 - s0) / a.target; filt += f",atempo={tempo:.5f}"
d = (s1 - s0) / tempo
filt += f",afade=t=in:d=0.01,afade=t=out:st={max(0, d - 0.04):.3f}:d=0.04"
if a.target: filt += f",apad=whole_dur={a.target},atrim=0:{a.target}"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.raw, "-af", filt, "-ar", str(SR), a.out], check=True)
print(f"OFFSET={s0:.3f} TEMPO={tempo:.5f} DUR={a.target or d:.3f}")

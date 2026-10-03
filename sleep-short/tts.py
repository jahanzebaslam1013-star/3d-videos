#!/usr/bin/env python3
"""Free local narrator (Kokoro TTS, voice am_michael) -> voiceover.wav + timing.json
  python3 tts.py script.txt [--voice am_michael] [--speed 1.1]
script.txt: one sentence per line. A line ending in '...' gets a longer dramatic pause.
Model files are downloaded once into ./tts_models (from GitHub releases)."""
import sys, os, json, argparse, subprocess, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("script"); ap.add_argument("--voice", default="am_michael"); ap.add_argument("--speed", type=float, default=1.1)
a = ap.parse_args()
D = "tts_models"; os.makedirs(D, exist_ok=True)
U = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
for f, n in [("kokoro.onnx", "kokoro-v1.0.onnx"), ("voices.bin", "voices-v1.0.bin")]:
    if not os.path.exists(f"{D}/{f}") or os.path.getsize(f"{D}/{f}") < 1_000_000:
        subprocess.run(["curl", "-sSL", "-o", f"{D}/{f}", U + n], check=True)
from kokoro_onnx import Kokoro
import soundfile as sf
k = Kokoro(f"{D}/kokoro.onnx", f"{D}/voices.bin")
lines = [l.strip() for l in open(a.script, encoding="utf-8") if l.strip()]
out, tim, t, sr = [], [], 0.0, 24000
for l in lines:
    spoken = l.replace("VoxMaps", "Vox Maps")
    x, sr = k.create(spoken, voice=a.voice, speed=a.speed, lang="en-us")
    idx = np.where(np.abs(x) > 0.01)[0]; x = x[max(0, idx[0] - 200): idx[-1] + 400]
    d = len(x) / sr; gap = 0.5 if l.endswith("...") else 0.18 if l.endswith(",") else 0.3
    ws = l.split(); tot = sum(len(w) + 2 for w in ws); acc = 0; words = []
    for w in ws:
        words.append({"w": w, "start": round(t + acc / tot * d, 3), "end": round(t + (acc + len(w) + 2) / tot * d, 3)}); acc += len(w) + 2
    tim.append({"text": l, "start": round(t, 3), "end": round(t + d, 3), "words": words})
    out += [x, np.zeros(int(gap * sr), np.float32)]; t += d + gap
sf.write("voiceover.wav", np.concatenate(out), sr); json.dump(tim, open("timing.json", "w"), indent=1)
for i, r in enumerate(tim): print(f"{i:2d} {r['start']:6.2f} {r['end']:6.2f}  {r['text']}")
print(f"total {t:.2f}s")

#!/usr/bin/env python3
"""Build the final audio: the user's voiceover + generated music bed (ducked) + SFX cues.
  python3 mix.py cues.json voiceover.wav mix.wav
cues.json:
{
  "total": 612.4,                      # seconds (defaults to voiceover length + 1.5)
  "vo_offset": 0.0,                    # shift voiceover (sec)
  "music": [[0,"playful"],[95.2,"mystery"],[240,"tense"]],   # moods: playful mystery tense sad epic space dark
  "music_level": 0.22,                 # peak level of music before ducking
  "cuts": [3.1, 7.9, ...],             # shot starts -> soft whoosh on each cut (optional)
  "sfx": [{"t":12.3,"name":"thud","g":0.8}, {"t":20,"name":"siren","d":2.5}, ...]
}
SFX names: see sfxlib.SFX (python3 -c "import sfxlib;print(sorted(sfxlib.SFX))").
Optional per-cue keys: g (gain), d (duration for sustained sfx), f (pitch for thud/ding/metal)."""
import json, sys, inspect, subprocess, numpy as np
import sfxlib as S
cues = json.load(open(sys.argv[1])); vo_path = sys.argv[2]; out = sys.argv[3]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vo_path, "-ac", "1", "-ar", str(S.SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
vo = np.frombuffer(raw, np.float32).astype(np.float64)
total = cues.get("total") or len(vo) / S.SR + 1.5
N = int(total * S.SR)
v = np.zeros(N); S.put(v, vo, cues.get("vo_offset", 0.0))
v = S.hp(v, 70); v = v / (np.max(np.abs(v)) + 1e-9) * 0.9
mus = S.music_bed([tuple(x) for x in cues.get("music", [[0, "mystery"]])], total)[:N]
mus = np.pad(mus, (0, N - len(mus)))
e = np.abs(v); k = int(0.12 * S.SR); e = np.convolve(e, np.ones(k) / k, "same"); e /= e.max() + 1e-9
mus = mus / (np.max(np.abs(mus)) + 1e-9) * cues.get("music_level", 0.22) * (1 - 0.55 * np.clip(e * 3, 0, 1))
fx = np.zeros(N)
for c in cues.get("cuts", []): S.put(fx, S.whoosh(0.3, 400, 2500, 0.22), c - 0.18)
for c in cues.get("sfx", []):
    fn = S.SFX[c["name"]]; params = inspect.signature(fn).parameters; kw = {}
    if "g" in c and "g" in params: kw["g"] = c["g"]
    if "d" in c and "d" in params: kw["d"] = c["d"]
    if "f" in c:
        for key in ("f", "f0"):
            if key in params: kw[key] = c["f"]
    S.put(fx, fn(**kw), c["t"])
pk = np.max(np.abs(fx))
if pk > 0: fx = fx / pk * min(0.7, pk)   # tame only if too hot
mix = np.tanh((v + mus + fx) * 1.05)
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.95
tmp = out + ".raw.wav"
import wave
with wave.open(tmp, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(S.SR)
    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16); w.writeframes(np.repeat(pcm, 2).tobytes())
# loudness-normalise to -14 LUFS (YouTube/TikTok target)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(S.SR), out], check=True)
import os; os.remove(tmp)
print("wrote", out, f"{total:.1f}s")

"""minimal soundfile shim on scipy.io.wavfile"""
import numpy as np, scipy.io.wavfile as wf
def read(p):
    sr, x = wf.read(p)
    if x.dtype.kind == 'i': x = x.astype(np.float64) / np.iinfo(x.dtype).max
    return x.astype(np.float64), sr
def write(p, x, sr, subtype=None):
    wf.write(p, sr, (np.clip(x, -1, 1) * 32767).astype(np.int16))
class _I:
    def __init__(s, d): s.duration = d
def info(p):
    sr, x = wf.read(p); return _I(len(x) / sr)

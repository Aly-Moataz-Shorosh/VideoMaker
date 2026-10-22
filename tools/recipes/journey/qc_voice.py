"""Check a piecewise voice map: build his clean voice over [t0, t1] with jy_audio.take() and compare its loudness envelope with the
published chapter in 1.5 s windows; prints the windows that do not match (wrong piece = wrong words). python work/scripts/qc_voice.py 34 0 165"""
import subprocess, sys
import numpy as np
from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent))
import jy_audio as A
ep, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
SR = A.SR
v = A.take(ep, t0, int((t1 - t0) * SR))
src = A._pcm(A.src(ep))[int(t0 * SR):int(t1 * SR)]
def env(x):
    h = SR // 100; n = len(x) // h
    return np.log(np.sqrt((x[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-4)
a, b = env(src), env(v)
bad = []
for s in range(0, min(len(a), len(b)) - 150, 75):
    x, y = a[s:s + 150], b[s:s + 150]
    if y.std() < 0.3:
        continue
    c = np.corrcoef(x, y)[0, 1]
    if c < 0.55:
        bad.append((round(t0 + s / 100, 1), round(float(c), 2)))
print(ep, 'windows bad:', len(bad), bad[:30])

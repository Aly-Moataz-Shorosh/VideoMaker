"""Piecewise map of his raw Oz recording (eN orginal v1.mp3) onto the published chapter — the method that worked for chapter 2:
3 s windows, whole-file search per window (normalised correlation), runs of the same offset; each change cut at the quietest 10 ms
between the last window of the old offset and the first of the new one. Prints the map + every window for checking.
python work/scripts/align_oz.py 32 e1 [t0 t1]"""
import glob, subprocess, sys
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parents[2]
ep, e = sys.argv[1], sys.argv[2]
t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0; t1 = float(sys.argv[4]) if len(sys.argv) > 4 else 9999


def env(f, sr=8000):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32)
    h = sr // 100; n = len(a) // h
    return np.log(np.sqrt((a[:n * h].reshape(n, h) ** 2).mean(1)) + 1)


a = env(glob.glob(str(P / 'input' / f'{ep}_*.mp4'))[0]); b = env(P / 'assets' / 'his' / 'oz_audio' / f'{e} orginal v1.mp3')
W = 300
cs = np.convolve(b, np.ones(W), 'valid'); cs2 = np.convolve(b ** 2, np.ones(W), 'valid')
sd = np.sqrt(np.maximum(cs2 / W - (cs / W) ** 2, 1e-6)); mu = cs / W
rows = []
for t in np.arange(max(0, t0), min(len(a) / 100 - 3, t1), 1.5):
    s = int(t * 100); seg = a[s:s + W]
    if seg.std() < 0.2:
        continue
    sg = (seg - seg.mean()) / seg.std()
    c = (np.correlate(b, sg, 'valid') / W) / sd  # == corr since sg has mean 0
    k = int(np.argmax(c)); rows.append((round(float(t), 1), round(k / 100 - t, 2), round(float(c[k]), 2)))
runs = []
for t, o, q in rows:
    if q < 0.8:
        continue
    if runs and abs(runs[-1][1] - o) <= 0.15:
        runs[-1][2] = t; runs[-1][3] += 1; continue
    runs.append([t, o, t, 1])
runs = [r for r in runs if r[3] >= 2]
m = []
for i, (ta, o, tb, n) in enumerate(runs):
    if not m:
        m.append((0.0, o)); continue
    lo, hi = int((runs[i - 1][2] + 3.0) * 100), int((ta + 0.3) * 100)
    lo = min(lo, hi - 1)
    cut = (lo + int(np.argmin(a[lo:hi]))) / 100
    m.append((round(cut, 2), o))
print('MAP', ep, e, m)
for r in rows:
    print('  ', r)

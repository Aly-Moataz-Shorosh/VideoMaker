"""Karim's face track (source px) for the speaker circle over the Karim-alone boards (143-178 s). Meet changed layouts there
(Karim big -> Aly pinned big + Karim small on the right -> letterboxed -> Karim big again), so a fixed point inside a tile showed
the wall (Aly 2026-10-27: "حصل فجأة زوم بعيد… الصورة المفروض تفضل على الضيف"). Haar face per 0.25 s, Karim = the largest face,
except while Aly is pinned big (149.25-157.5): the face right of x 1400. Median-smoothed, gaps interpolated.
-> work/karim_track.json [[t, cx, cy, h], ...]"""
import json, subprocess, sys
import numpy as np, cv2
from pathlib import Path
W = Path(__file__).resolve().parents[1]
V = str(W.parent / 'input' / '2026-10-27 16-06-01.mp4')
T0, T1, FPS = 143.0, 178.5, 4
raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(T0), '-t', str(T1 - T0), '-i', V, '-vf', f'fps={FPS},scale=960:540,format=gray', '-f', 'rawvideo', '-'],
                     capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 540, 960)
fc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
pts = []
for i, g in enumerate(fr):
    t = T0 + i / FPS
    fs = fc.detectMultiScale(g, 1.1, 5, minSize=(30, 30))
    fs = [f for f in fs if (f[0] + f[2] / 2) * 2 > 1400] if 149.25 <= t < 157.5 else list(fs)
    if not fs: pts.append([t, None, None, None]); continue
    x, y, w, h = max(fs, key=lambda f: f[2])
    pts.append([t, (x + w / 2) * 2, (y + h / 2) * 2, h * 2])
a = np.array([[p[0], np.nan if p[1] is None else p[1], np.nan if p[2] is None else p[2], np.nan if p[3] is None else p[3]] for p in pts], float)
for c in (1, 2, 3):
    ok = ~np.isnan(a[:, c]); a[:, c] = np.interp(a[:, 0], a[ok, 0], a[ok, c])
    k = 5; pad = np.pad(a[:, c], k, mode='edge'); a[:, c] = [np.median(pad[i:i + 2 * k + 1]) for i in range(len(a))]
json.dump([[round(v, 2) for v in r] for r in a.tolist()], open(W / 'karim_track.json', 'w'))
print(len(a), 'points; face h range', round(a[:, 3].min()), round(a[:, 3].max()), '; missing', int(sum(p[1] is None for p in pts)))

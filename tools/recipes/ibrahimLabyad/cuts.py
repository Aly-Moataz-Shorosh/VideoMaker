"""Per-frame difference -> candidate cuts not in shots.json."""
import cv2, json, numpy as np
from pathlib import Path
W = Path(__file__).resolve().parents[1]
shots = json.load(open(W / 'prototype/shots.json'))
known = [s['s'] for s in shots[1:]]
cap = cv2.VideoCapture(str(W / 'src720_crop-ready.mp4')); fps = cap.get(5)
prev = None; d = []; hd = []
while True:
    ok, f = cap.read()
    if not ok: break
    g = cv2.resize(f[88:620, 28:1248], (244, 106))
    hsv = cv2.cvtColor(g, cv2.COLOR_BGR2HSV)
    h = cv2.calcHist([hsv], [0, 1, 2], None, [8, 4, 4], [0, 180, 0, 256, 0, 256]); h = cv2.normalize(h, h).flatten()
    if prev is not None:
        d.append(float(np.mean(np.abs(g.astype(int) - prev[0].astype(int)))))
        hd.append(float(cv2.compareHist(prev[1], h, cv2.HISTCMP_BHATTACHARYYA)))
    else:
        d.append(0); hd.append(0)
    prev = (g, h)
d = np.array(d); hd = np.array(hd)
np.save(W / 'framediff.npy', np.stack([d, hd]))
# score = ratio to local median
for i in range(2, len(d) - 2):
    loc = np.median(np.r_[d[max(0, i - 8):i - 1], d[i + 2:i + 9]]) + 1
    r = d[i] / loc
    if (r > 3.0 and d[i] > 8) or hd[i] > 0.35:
        t = i / fps
        near = min(abs(t - k) for k in known)
        flag = 'known' if near < 0.1 else 'NEW'
        print(f'{t:8.3f}  d={d[i]:6.1f} r={r:5.1f} hd={hd[i]:.2f}  {flag} ({near:.2f})')

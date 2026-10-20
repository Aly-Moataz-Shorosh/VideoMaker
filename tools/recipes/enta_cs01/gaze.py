"""Which way is each person looking (per pip window)? Eyes centre vs face-box centre (haar) on 8 frames per window.
x offset < 0 = eyes shifted to the viewer's LEFT = he looks towards the left of the screen -> circle goes on the RIGHT (Aly 2026-10-20).
Usage: python gaze.py <video> <plan.json> -> prints [at, who, offset] and writes work/gaze.json"""
import json, subprocess, sys
import numpy as np, cv2
from pathlib import Path
video, plan = sys.argv[1], json.load(open(sys.argv[2], encoding='utf8'))
W = Path(sys.argv[2]).parent
fc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
ec = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
pr = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
out = []
for c in [c for c in plan['cues'] if c['t'] == 'pip']:
    t = plan['meet'][c['props']['who']]
    offs = []
    for k in range(8):
        ts = c['src'] + (k + 0.5) * c['dur'] / 8
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{ts:.2f}', '-i', video, '-frames:v', '1', '-vf', f'crop={t[2]}:{t[3]}:{t[0]}:{t[1]},format=gray',
                              '-f', 'rawvideo', '-'], capture_output=True).stdout
        g = np.frombuffer(raw, np.uint8).reshape(t[3], t[2])
        fs = fc.detectMultiScale(g, 1.1, 5, minSize=(80, 80))
        if len(fs):
            x, y, w, h = max(fs, key=lambda f: f[2])
            es = ec.detectMultiScale(g[y:y + h // 2, x:x + w], 1.1, 5, minSize=(w // 10, w // 10))
            if len(es) >= 2:
                es = sorted(es, key=lambda e: -e[2])[:2]
                ex = np.mean([e[0] + e[2] / 2 for e in es])
                offs.append((ex - w / 2) / w); continue
        # turned too far for the frontal detector: profile cascade (left-facing) on the image and its mirror
        if len(pr.detectMultiScale(g, 1.1, 5, minSize=(80, 80))): offs.append(-0.2)
        elif len(pr.detectMultiScale(cv2.flip(g, 1), 1.1, 5, minSize=(80, 80))): offs.append(0.2)
    o = float(np.median(offs)) if offs else 0.0
    out.append([c['src'], c['props']['who'], round(o, 3), len(offs)])
    print(out[-1], flush=True)
json.dump(out, open(W / 'gaze.json', 'w'), indent=0)

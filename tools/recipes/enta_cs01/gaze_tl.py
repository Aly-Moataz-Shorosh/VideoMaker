"""Gaze timeline: which way each person looks, every 2 s over the whole episode (one ffmpeg pass on the tile strip).
offset < 0 = looks towards the LEFT of the screen. Writes work/gaze_tl.json {"G": [[t, o|null], ...], "A": [...]}.
Aly 2026-10-20: he looks left -> his circle / his video goes RIGHT (content on the side he looks at), and the other way round."""
import json, subprocess, sys
import numpy as np, cv2
from pathlib import Path
video, plan = sys.argv[1], json.load(open(sys.argv[2], encoding='utf8'))
W = Path(sys.argv[2]).parent
T = plan['meet']; x0, y0 = T['G'][0], T['G'][1]; sw, sh = T['A'][0] + T['A'][2] - x0, T['G'][3]
sw += sw % 2  # yuv420 crops snap to even widths -> keep the raw stride right
fc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
ec = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
pr = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', video, '-vf', f'fps=0.5,crop={sw}:{sh}:{x0}:{y0},format=gray', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)


def off(g):
    fs = fc.detectMultiScale(g, 1.1, 5, minSize=(80, 80))
    if len(fs):
        x, y, w, h = max(fs, key=lambda f: f[2])
        es = ec.detectMultiScale(g[y:y + h // 2, x:x + w], 1.1, 5, minSize=(w // 10, w // 10))
        if len(es) >= 2:
            es = sorted(es, key=lambda e: -e[2])[:2]
            return float((np.mean([e[0] + e[2] / 2 for e in es]) - w / 2) / w)
    if len(pr.detectMultiScale(g, 1.1, 5, minSize=(80, 80))): return -0.2
    if len(pr.detectMultiScale(cv2.flip(g, 1), 1.1, 5, minSize=(80, 80))): return 0.2
    return None


out, i = {'G': [], 'A': []}, 0
while True:
    b = p.stdout.read(sw * sh)
    if len(b) < sw * sh: break
    fr = np.frombuffer(b, np.uint8).reshape(sh, sw)
    for who in ('G', 'A'):
        tx = T[who][0] - x0
        out[who].append([i * 2.0, off(np.ascontiguousarray(fr[:, tx:tx + T[who][2]]))])
    i += 1
json.dump(out, open(W / 'gaze_tl.json', 'w'))
for who in out:
    v = [o for t, o in out[who] if o is not None]
    print(who, len(out[who]), 'samples,', len(v), 'found; left', sum(o < -0.05 for o in v), 'front', sum(abs(o) <= 0.05 for o in v), 'right', sum(o > 0.05 for o in v))

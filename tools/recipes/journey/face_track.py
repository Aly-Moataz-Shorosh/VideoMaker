"""Where is his face in his Oz chapter, over time? (the circle must stay centred on his face — Aly v3 review)
OpenCV frontal-face cascade every 0.5 s on the published chapter, largest face, smoothed (median of 5), held through misses.
python work/scripts/face_track.py 32 34 35 36 -> work/face_<ep>.json [{t, cx, cy, r}] in 1920x1080 pixels"""
import glob, json, subprocess, sys
from pathlib import Path
import cv2
import numpy as np
P = Path(__file__).resolve().parents[2]
casc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
for ep in sys.argv[1:]:
    src = glob.glob(str(P / 'input' / f'{ep}_*.mp4'))[0]
    W, H, STEP = 960, 540, 0.5
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'fps={1 / STEP},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
    pts = []
    for i, g in enumerate(fr):
        f = casc.detectMultiScale(g, 1.1, 6, minSize=(40, 40))
        if len(f):
            x, y, w, h = max(f, key=lambda r: r[2] * r[3])
            pts.append([i * STEP, (x + w / 2) * 2, (y + h / 2) * 2, h * 2])
        else:
            pts.append([i * STEP, None, None, None])
    # hold through misses, then median-smooth
    last = None
    for p in pts:
        if p[1] is None and last:
            p[1:] = last
        elif p[1] is not None:
            last = p[1:]
    first = next((p[1:] for p in pts if p[1] is not None), [960, 600, 300])
    for p in pts:
        if p[1] is None:
            p[1:] = first
    arr = np.array([p[1:] for p in pts], float)
    sm = np.array([np.median(arr[max(0, i - 2):i + 3], axis=0) for i in range(len(arr))])
    out = [{'t': round(pts[i][0], 2), 'cx': round(sm[i][0]), 'cy': round(sm[i][1] + sm[i][2] * 0.12), 'r': round(max(180, sm[i][2] * 1.05))} for i in range(len(pts))]
    json.dump(out, open(P / 'work' / f'face_{ep}.json', 'w'), indent=0)
    miss = sum(1 for p in pts if p[3] is None)
    print(ep, len(out), 'points; r range', min(o['r'] for o in out), max(o['r'] for o in out))

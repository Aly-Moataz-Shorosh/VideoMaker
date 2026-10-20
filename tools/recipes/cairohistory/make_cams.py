"""Round 'webcam' bubbles: in his screen recording Aly sits small in the bottom-right corner (already keyed over the map).
For each window (source seconds) find his face (haar, mid-window) and cut a square clip around it -> public cam_<a>.mp4 (480 px).
Output work/cams.json {"a-b": {"file", "src"}}. Usage: python work/scripts/make_cams.py"""
import json, subprocess, sys
from pathlib import Path
import cv2
W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
SRC = P / 'input' / 'Vd0NUtDsUfk.mp4'
PUB = ROOT / 'motion-library/public/projects' / P.name
WINS = [(551.25, 554.85), (1337.66, 1344.7), (409.98, 413.7), (325.86, 332.04), (250.97, 255.25), (1288.06, 1292.24), (707.77, 713.13), (1043.84, 1047.04), (1164.36, 1166.88), (1252.08, 1256.42), (912.77, 916.35), (589.0, 593.8)]
PAD = 0.4
casc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
out = {}
for a, b in WINS:
    faces = []
    for t in (a + (b - a) * k for k in (0.25, 0.5, 0.75)):
        cap = cv2.VideoCapture(str(SRC)); cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, fr = cap.read()
        fs = [f for f in casc.detectMultiScale(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY), 1.1, 5, minSize=(60, 60)) if f[0] > 1300 and f[1] > 600]
        if fs: faces.append(max(fs, key=lambda f: f[2]))
    if not faces:
        print('no face', a, b); continue
    x = sum(f[0] + f[2] / 2 for f in faces) / len(faces); y = sum(f[1] + f[3] / 2 for f in faces) / len(faces); w = max(f[2] for f in faces)
    side = int(min(560, w * 3.6)); x0 = int(min(1920 - side, max(0, x - side / 2 + 40))); y0 = int(min(1080 - side, max(0, y - side * 0.42)))
    name = f'cam_{int(a)}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a - PAD:.2f}', '-i', str(SRC), '-t', f'{b - a + 2 * PAD:.2f}', '-vf', f'crop={side}:{side}:{x0}:{y0},scale=480:480',
                    '-c:v', 'libx264', '-crf', '17', '-an', str(PUB / name)], check=True)
    out[f'{a}-{b}'] = {'file': f'projects/{P.name}/{name}', 'src': a - PAD}
    print(a, b, 'face', int(x), int(y), w, 'crop', side, x0, y0)
json.dump(out, open(W / 'cams.json', 'w'), indent=1)

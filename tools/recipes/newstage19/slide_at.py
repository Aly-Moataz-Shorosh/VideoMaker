"""Which slide was on the projector? The RAW camera is static: crop the projector, compare (normalized correlation on 96x54
grey + edges) with all 133 exported slides, every 1 s. Writes work/slide_timeline.json [[main_sec, slide, score], ...].
Usage: python slide_at.py            (build)
       python slide_at.py 1162 1600  (print the slide at those Main-new seconds)"""
import json, subprocess, sys
from pathlib import Path
import cv2
import numpy as np
P = Path(__file__).resolve().parents[2]
OUT = P / 'work' / 'slide_timeline.json'
OFF = -88.01
CROP = (550, 10, 505, 285)  # x, y, w, h of the projected slide in the raw frame


def feat(g):
    g = cv2.resize(g, (96, 54), interpolation=cv2.INTER_AREA).astype(np.float32)
    e = cv2.Laplacian(g, cv2.CV_32F)
    v = np.concatenate([g.ravel(), e.ravel() * 2])
    v -= v.mean()
    return v / (np.linalg.norm(v) + 1e-6)


def build():
    slides = []
    for n in range(1, 134):
        im = cv2.imread(str(P / 'work' / 'slides' / f'slide_{n:03d}.png'), cv2.IMREAD_GRAYSCALE)
        slides.append(feat(im))
    S = np.stack(slides)
    x, y, w, h = CROP
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(P / 'input' / '20260908_103633.mp4'), '-vf', f'fps=1,crop={w}:{h}:{x}:{y},scale=192:108,format=gray',
                          '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    res, i = [], 0
    while True:
        b = p.stdout.read(192 * 108)
        if len(b) < 192 * 108: break
        g = np.frombuffer(b, np.uint8).reshape(108, 192)
        sc = S @ feat(g)
        k = int(np.argmax(sc))
        res.append([round(i - OFF, 1), k + 1, round(float(sc[k]), 3)])
        i += 1
    json.dump(res, open(OUT, 'w'))
    print(len(res), 'seconds')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        build()
    else:
        tl = json.load(open(OUT))
        for a in sys.argv[1:]:
            t = float(a)
            near = [r for r in tl if abs(r[0] - t) <= 3]
            print(a, [(r[0], r[1], r[2]) for r in near])

# His webcam square in the course recording moves/changes size between parts (Aly review 2026-11-07: "صورتي مقصوصة / مش في النص /
# في مساحة فاضية"). Per source second: find the webcam box (bottom-right, strong left + top edges) and his face inside it, return a square
# crop (1280x720 proxy px) centred on his face, as tight as the box allows, NEVER outside the box.   python webcam.py 3100 790 ...
import json, subprocess, sys
from pathlib import Path
import numpy as np
import cv2

PROJ = Path(__file__).resolve().parents[2]
SRC = PROJ.parents[1] / 'motion-library/public/projects/filmcourse/course.mp4'
CACHE = PROJ / 'work/shorts/webcam_cache.json'
_c = json.load(open(CACHE)) if CACHE.exists() else {}
FACE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
PROF = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')


def frame(t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', str(SRC), '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(720, 1280).astype(np.int16)


def box(g):
    """the webcam overlay is 16:9 glued to the bottom-right corner: find its TOP edge (the row where most pixels change sharply over
    the right part), the left edge follows from 16:9 (558 -> 992, 590 -> 1049, 617 -> 1097 measured by eye 2026-11-07)."""
    dy = np.abs(np.diff(g, axis=0)) > 22
    rows = [(dy[y - 1, 1190:1272].mean(), y) for y in range(480, 680)]
    top = max(rows)[1]
    return int(round(1280 - (720 - top) * 16 / 9)), top


def crop(t):
    k = f'{t:.1f}'
    if k in _c: return _c[k]
    faces, lt = [], []
    for dt in (0.0, 0.7, 1.4):
        g = frame(t + dt)
        L, T = box(g)
        lt.append((L, T))
        sub = np.clip(g[T:720, L:1280], 0, 255).astype(np.uint8)
        big = cv2.resize(sub, None, fx=3, fy=3)
        f = list(FACE.detectMultiScale(big, 1.1, 5, minSize=(60, 60))) or list(PROF.detectMultiScale(big, 1.1, 5, minSize=(60, 60)))
        if f:
            x, y, w, h = max(f, key=lambda r: r[2])
            fx, fy, fw = L + (x + w / 2) / 3, T + (y + h / 2) / 3, w / 3
            if fw > 0.22 * (720 - T) and fx > L + 10: faces.append((fx, fy, fw))  # a real face, not a bit of the room
    L, T = int(np.median([a for a, _ in lt])), int(np.median([b for _, b in lt]))
    bw, bh = 1280 - L, 720 - T
    if faces:
        cx, cy, fs = (float(np.median([f[i] for f in faces])) for i in range(3))
        s = min(bh, bw, max(2.4 * fs, 0.62 * bh))  # face ~40% of the circle (Aly: "كبرها")
    else:
        cx, cy, s = L + bw * 0.55, T + bh * 0.45, min(bh, bw) * 0.8
    sx = min(max(cx - s / 2, L), 1280 - s); sy = min(max(cy - s / 2 + 0.06 * s, T), 720 - s)
    r = dict(sx=round(sx, 1), sy=round(sy, 1), s=round(s, 1), box=[L, T], face=bool(faces))
    _c[k] = r
    json.dump(_c, open(CACHE, 'w'), indent=0)
    return r


if __name__ == '__main__':
    for t in map(float, sys.argv[1:]): print(t, crop(t))

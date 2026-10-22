"""Where is HIS motion in the frame? (هو ايه episodes: small animated pictures on a plain grey vignette.)
Every 0.25 s: pixels that differ from the plain background (episode's own empty frame, median of the quiet frames) -> bounding box.
Prints runs of similar boxes -> crop boxes for `jy_clip` (his own motion shown big in the 9:16 stage).
python work/scripts/content_boxes.py 08 6.5 83"""
import glob, subprocess, sys
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parents[2]
ep, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
src = glob.glob(str(P / 'input' / f'{ep}_*.mp4'))[0]
W, H, STEP = 480, 270, 0.25
raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t0), '-t', str(t1 - t0), '-i', src, '-vf', f'fps={1 / STEP},scale={W}:{H}',
                      '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.int16)
bg = np.median(fr, axis=0)  # the grey vignette is there most of the time
boxes = []
for i, f in enumerate(fr):
    m = np.abs(f - bg).sum(2) > 45
    m[:int(H * 0.09)] = False; m[int(H * 0.91):] = False  # his letterbox bars + credits
    ys, xs = np.where(m)
    if len(xs) < 60:
        boxes.append(None); continue
    x0, x1 = np.percentile(xs, [1, 99]); y0, y1 = np.percentile(ys, [1, 99])
    boxes.append([int(x0 * 4), int(y0 * 4), int(x1 * 4), int(y1 * 4)])
# runs
cur, start = None, 0
def same(a, b):
    return a is None and b is None or (a is not None and b is not None and max(abs(p - q) for p, q in zip(a, b)) < 60)
for i, b in enumerate(boxes + ['END']):
    if b == 'END' or not same(b, cur):
        if i > start:
            print(f'{t0 + start * STEP:6.2f}-{t0 + i * STEP:6.2f}  {cur}')
        cur, start = (None if b == 'END' else b), i

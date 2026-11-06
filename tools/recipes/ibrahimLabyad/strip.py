"""strip.py out.jpg t1 t2 ... : row per time, frames at -0.1 -0.033 0 +0.033 +0.1 s (frame i = diff index i => cut between i-1 and i)."""
import cv2, sys, numpy as np
from pathlib import Path
W = Path(__file__).resolve().parents[1]
cap = cv2.VideoCapture(str(W / 'src720_crop-ready.mp4')); fps = cap.get(5)
def fr(i):
    cap.set(1, i); ok, f = cap.read(); return cv2.resize(f[88:620, 28:1248], (280, 122))
rows = []
for t in map(float, sys.argv[2:]):
    i = int(round(t * fps))
    tiles = [fr(j) for j in (i - 3, i - 1, i, i + 1, i + 3)]
    row = np.hstack([np.pad(x, ((2, 2), (2, 2), (0, 0))) for x in tiles])
    lab = np.zeros((20, row.shape[1], 3), np.uint8)
    cv2.putText(lab, f'{t:.3f}  frames {i-3} {i-1} | {i} {i+1} {i+3}', (5, 15), 0, .5, (0, 255, 255), 1)
    rows.append(np.vstack([lab, row]))
cv2.imwrite(sys.argv[1], np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])

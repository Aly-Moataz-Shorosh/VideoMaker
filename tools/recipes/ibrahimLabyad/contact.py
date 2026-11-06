"""Contact sheets: 6 shots per sheet, 5 frames per shot (start, 25, 50, 75 %, end)."""
import cv2, json, sys, numpy as np
from pathlib import Path
W = Path(__file__).resolve().parents[1]
shots = json.load(open(W / 'prototype/shots.json'))
cap = cv2.VideoCapture(str(W / 'src720_crop-ready.mp4'))
fps = cap.get(cv2.CAP_PROP_FPS)
out = W / 'contact'; out.mkdir(exist_ok=True)
TW, TH = 300, 131
def frame(t):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps)))
    ok, f = cap.read()
    f = f[88:88 + 532, 28:28 + 1220]
    return cv2.resize(f, (TW, TH))
per = 6
for i in range(0, len(shots), per):
    rows = []
    for s in shots[i:i + per]:
        a, b = s['s'], s['e']
        ts = [a + 0.04, a + (b - a) * .25, a + (b - a) * .5, a + (b - a) * .75, b - 0.07]
        tiles = [frame(t) for t in ts]
        row = np.hstack([np.pad(t, ((2, 2), (2, 2), (0, 0))) for t in tiles])
        lab = np.zeros((22, row.shape[1], 3), np.uint8)
        cv2.putText(lab, f"SHOT {s['n']}  {a:.2f}-{b:.2f}  ({b-a:.2f}s)", (6, 16), cv2.FONT_HERSHEY_SIMPLEX, .55, (0, 255, 255), 1)
        rows.append(np.vstack([lab, row]))
    cv2.imwrite(str(out / f'sheet_{i//per+1:02d}.jpg'), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
print('done')

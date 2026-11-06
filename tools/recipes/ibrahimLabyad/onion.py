"""onion.py N1 N2 ... : per shot first frame (RED) over last frame (CYAN) + middle frame. Grey = did not move."""
import cv2, json, sys, numpy as np
from pathlib import Path
W = Path(__file__).resolve().parents[1]
shots = {s['n']: s for s in json.load(open(W / 'shots_v4.json'))}
bm = {r['n']: r for r in json.load(open(W / 'bgmotion.json'))}
cap = cv2.VideoCapture(str(W / 'src720_crop-ready.mp4'))
def get(i):
    cap.set(1, i); ok, f = cap.read(); return cv2.resize(f[88:620, 28:1248], (440, 192))
ns = [int(x) for x in sys.argv[2:]]
tiles = []
for n in ns:
    s = shots[n]; a, b = s['f0'] + 1, s['f1'] - 2
    A = cv2.cvtColor(get(a), cv2.COLOR_BGR2GRAY); B = cv2.cvtColor(get(b), cv2.COLOR_BGR2GRAY); M = get((a + b) // 2)
    A = cv2.equalizeHist(A); B = cv2.equalizeHist(B)
    on = np.dstack([B, B, A])            # BGR: last = cyan, first = red
    for g in range(1, 8): cv2.line(on, (g * 55, 0), (g * 55, 192), (255, 255, 255), 1)
    for g in range(1, 4): cv2.line(on, (0, g * 48), (440, g * 48), (255, 255, 255), 1)
    r = bm[n]
    t = np.hstack([on, np.zeros((192, 4, 3), np.uint8), M])
    lab = np.zeros((22, t.shape[1], 3), np.uint8)
    cv2.putText(lab, f"SHOT {n} ({r.get('d')}s)  x{r.get('panx')} y{r.get('pany')} z{r.get('scale')} jit{r.get('jit')} par{r.get('par')}", (5, 16), 0, .5, (0, 255, 255), 1)
    tiles.append(np.vstack([lab, t]))
cv2.imwrite(sys.argv[1], np.vstack(tiles), [cv2.IMWRITE_JPEG_QUALITY, 85])

"""Motion sheets: per shot = first frame with feature TRACKS (green->red over time) | last frame | camera path graph.
Metrics: cumulative pan dx/dy (median flow), scale, parallax (flow spread after a similarity fit), jitter."""
import cv2, json, numpy as np
from pathlib import Path
W = Path(__file__).resolve().parents[1]
shots = json.load(open(W / 'shots_v4.json'))
cap = cv2.VideoCapture(str(W / 'src720_crop-ready.mp4'))
def get(i):
    cap.set(1, i); ok, f = cap.read(); return f[88:620, 28:1248]
TW, TH = 420, 183
out = W / 'tracks'; out.mkdir(exist_ok=True)
met = []
rows = []
for s in shots:
    f0, f1 = s['f0'] + 1, s['f1'] - 2
    idx = list(range(f0, max(f0 + 1, f1), 1))
    frames = [get(i) for i in idx]
    grays = [cv2.cvtColor(cv2.resize(f, (610, 266)), cv2.COLOR_BGR2GRAY) for f in frames]
    p = cv2.goodFeaturesToTrack(grays[0], 250, 0.01, 8) if len(grays) > 1 else None
    tracks = [] if p is None else [[tuple(q.ravel())] for q in p]
    alive = list(range(len(tracks)))
    steps = []
    for a, b in zip(grays, grays[1:]):
        if not alive: break
        pa = np.float32([tracks[k][-1] for k in alive]).reshape(-1, 1, 2)
        pb, st, _ = cv2.calcOpticalFlowPyrLK(a, b, pa, None, winSize=(21, 21), maxLevel=3)
        back, st2, _ = cv2.calcOpticalFlowPyrLK(b, a, pb, None, winSize=(21, 21), maxLevel=3)
        good = (st.ravel() == 1) & (st2.ravel() == 1) & (np.linalg.norm((back - pa).reshape(-1, 2), axis=1) < 1.0)
        d = (pb - pa).reshape(-1, 2)[good]
        if len(d) >= 8:
            M, inl = cv2.estimateAffinePartial2D(pa[good], pb[good], ransacReprojThreshold=1.5)
            sc = float(np.hypot(M[0, 0], M[1, 0])) if M is not None else 1
            pred = (pa[good].reshape(-1, 2) @ M[:, :2].T + M[:, 2]) if M is not None else pa[good].reshape(-1, 2)
            par = float(np.median(np.linalg.norm(pb[good].reshape(-1, 2) - pred, axis=1)))
            steps.append((float(np.median(d[:, 0])), float(np.median(d[:, 1])), sc, par, float(inl.mean()) if inl is not None else 0))
        else:
            steps.append((0, 0, 1, 0, 0))
        na = []
        for k, g, q in zip(alive, good, pb.reshape(-1, 2)):
            if g: tracks[k].append(tuple(q)); na.append(k)
        alive = na
    st = np.array(steps) if steps else np.zeros((1, 5))
    dx, dy = st[:, 0], st[:, 1]
    cx, cy = -np.cumsum(dx), -np.cumsum(dy)          # camera direction: + = right / down
    hf = np.sqrt(np.mean((dx - cv2.blur(dx.reshape(-1, 1), (1, 7)).ravel()) ** 2 + (dy - cv2.blur(dy.reshape(-1, 1), (1, 7)).ravel()) ** 2)) if len(dx) > 7 else 0
    m = dict(n=s['n'], d=round(s['e'] - s['s'], 2), panx=round(float(cx[-1]), 1), pany=round(float(cy[-1]), 1),
             scale=round(float(np.prod(st[:, 2])), 3), parallax=round(float(np.mean(st[:, 3])), 2), jitter=round(float(hf), 2),
             inl=round(float(np.mean(st[:, 4])), 2))
    met.append(m)
    # draw
    k = TW / 610
    A = cv2.resize(frames[0], (TW, TH)); B = cv2.resize(frames[-1], (TW, TH))
    A = (A * 0.6).astype(np.uint8)
    for tr in tracks:
        if len(tr) < max(3, len(grays) * 0.5): continue
        pts = np.array(tr) * k
        for j in range(len(pts) - 1):
            c = j / max(1, len(pts) - 1)
            cv2.line(A, tuple(map(int, pts[j])), tuple(map(int, pts[j + 1])), (0, int(255 * (1 - c)), int(255 * c)), 1, cv2.LINE_AA)
        cv2.circle(A, tuple(map(int, pts[-1])), 2, (0, 0, 255), -1)
    G = np.zeros((TH, TH, 3), np.uint8); G[:] = 25
    cv2.line(G, (TH // 2, 0), (TH // 2, TH), (70, 70, 70), 1); cv2.line(G, (0, TH // 2), (TH, TH // 2), (70, 70, 70), 1)
    sc_ = (TH * 0.42) / max(20, np.abs(np.r_[cx, cy]).max())
    pts = np.c_[TH // 2 + cx * sc_, TH // 2 + cy * sc_].astype(int)
    for j in range(len(pts) - 1): cv2.line(G, tuple(pts[j]), tuple(pts[j + 1]), (0, 220, 255), 2)
    cv2.putText(G, f"x{m['panx']:.0f} y{m['pany']:.0f}", (4, 14), 0, .42, (255, 255, 255), 1)
    cv2.putText(G, f"z{m['scale']:.2f} par{m['parallax']:.2f}", (4, 30), 0, .42, (255, 255, 255), 1)
    cv2.putText(G, f"jit{m['jitter']:.2f}", (4, 46), 0, .42, (255, 255, 255), 1)
    row = np.hstack([A, np.full((TH, 4, 3), 0, np.uint8), B, np.full((TH, 4, 3), 0, np.uint8), G])
    lab = np.zeros((20, row.shape[1], 3), np.uint8)
    cv2.putText(lab, f"SHOT {s['n']}  {s['s']:.2f}-{s['e']:.2f} ({m['d']}s)", (5, 15), 0, .5, (0, 255, 255), 1)
    rows.append(np.vstack([lab, row]))
for i in range(0, len(rows), 6):
    cv2.imwrite(str(out / f'tr_{i // 6 + 1:02d}.jpg'), np.vstack(rows[i:i + 6]), [cv2.IMWRITE_JPEG_QUALITY, 85])
json.dump(met, open(W / 'motion_v5.json', 'w'), indent=0)
print('sheets', (len(rows) + 5) // 6)

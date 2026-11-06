"""Camera motion from the BACKGROUND only: people masked with DeepLabV3 (torchvision), LK flow on the rest.
Per shot: pan x/y (% of frame), scale, roll, parallax (spread of bg motion after similarity fit), jitter (shake)."""
import cv2, json, numpy as np, torch, torchvision
from pathlib import Path
W = Path(__file__).resolve().parents[1]
shots = json.load(open(W / 'shots_v4.json'))
net = torchvision.models.segmentation.deeplabv3_mobilenet_v3_large(weights='DEFAULT').eval()
MEAN = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1); STD = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
cap = cv2.VideoCapture(str(W / 'src720_crop-ready.mp4'))
FW, FH = 610, 266
def get(i):
    cap.set(1, i); ok, f = cap.read(); return cv2.resize(f[88:620, 28:1248], (FW, FH))
@torch.no_grad()
def person(f):
    x = torch.from_numpy(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).permute(2, 0, 1).float() / 255
    o = net(((x - MEAN) / STD)[None])['out'][0].argmax(0).numpy()
    m = (o == 15).astype(np.uint8)
    return cv2.dilate(m, np.ones((15, 15), np.uint8))
res = []
for s in shots:
    idx = list(range(s['f0'] + 1, s['f1'] - 1, 2))
    if len(idx) < 3: idx = list(range(s['f0'], s['f1']))
    fr = [get(i) for i in idx]
    g = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in fr]
    steps = []
    for k in range(len(g) - 1):
        bg = (1 - person(fr[k])) * 255
        p = cv2.goodFeaturesToTrack(g[k], 300, 0.005, 6, mask=bg.astype(np.uint8))
        if p is None or len(p) < 10: steps.append(None); continue
        q, st, _ = cv2.calcOpticalFlowPyrLK(g[k], g[k + 1], p, None, winSize=(21, 21), maxLevel=3)
        b, st2, _ = cv2.calcOpticalFlowPyrLK(g[k + 1], g[k], q, None, winSize=(21, 21), maxLevel=3)
        ok = (st.ravel() == 1) & (st2.ravel() == 1) & (np.linalg.norm((b - p).reshape(-1, 2), axis=1) < 0.8)
        if ok.sum() < 10: steps.append(None); continue
        P, Q = p[ok].reshape(-1, 2), q[ok].reshape(-1, 2)
        M, inl = cv2.estimateAffinePartial2D(P, Q, ransacReprojThreshold=1.0)
        if M is None: steps.append(None); continue
        sc = float(np.hypot(M[0, 0], M[1, 0])); rot = float(np.degrees(np.arctan2(M[1, 0], M[0, 0])))
        # translation of the frame centre
        c = np.array([FW / 2, FH / 2]); tc = M[:, :2] @ c + M[:, 2] - c
        resid = np.linalg.norm(Q - (P @ M[:, :2].T + M[:, 2]), axis=1)
        steps.append((tc[0], tc[1], sc, rot, float(np.percentile(resid, 75)), float(inl.mean()), int(ok.sum())))
    v = [x for x in steps if x is not None]
    if not v:
        res.append(dict(n=s['n'], ok=0)); continue
    a = np.array(v)
    dx, dy = -a[:, 0], -a[:, 1]          # camera: + = right / down
    sm = lambda z: np.convolve(z, np.ones(5) / 5, 'same') if len(z) >= 5 else z
    jit = float(np.sqrt(np.mean((dx - sm(dx)) ** 2 + (dy - sm(dy)) ** 2)))
    res.append(dict(n=s['n'], ok=round(len(v) / max(1, len(steps)), 2), d=round(s['e'] - s['s'], 2),
                    panx=round(float(dx.sum()) / FW * 100, 1), pany=round(float(dy.sum()) / FH * 100, 1),
                    scale=round(float(np.prod(a[:, 2])), 3), roll=round(float(a[:, 3].sum()), 2),
                    rollsd=round(float(a[:, 3].std()), 3), par=round(float(a[:, 4].mean()), 2), jit=round(jit, 2),
                    inl=round(float(a[:, 5].mean()), 2), npts=int(a[:, 6].mean()),
                    pathx=[round(float(z), 1) for z in np.cumsum(dx) / FW * 100][::2], pathy=[round(float(z), 1) for z in np.cumsum(dy) / FH * 100][::2]))
    r = res[-1]; print(r['n'], r['panx'], r['pany'], r['scale'], r['roll'], r['par'], r['jit'], r['npts'], flush=True)
json.dump(res, open(W / 'bgmotion.json', 'w'))

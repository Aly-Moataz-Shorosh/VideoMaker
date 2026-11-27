"""Put a REAL aerial photo of Giza under Aly in the start keyframe (Aly note 15: «عايزه واقعي»).

Usage: python real_ground.py <keyframe.png> <aerial.jpg> <out.png> [--horizon 0.36] [--debug]
Foreground (kept from the keyframe) = RVM person matte (body, legs, hands) + the held print (saturated blue/gold
area + its white curled corners) + the banner and the whole sky above the horizon line.
Ground = the aerial photo, cropped/scaled to cover everything below the horizon, its own sky cut off by a soft
gradient so it blends into the keyframe's haze; colour matched (mean/std per channel) to the old ground.
"""
import sys
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort

kf_p, ae_p, out_p = sys.argv[1:4]
arg = lambda k, d: float(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
hz = arg('--horizon', 0.36)
rd = lambda p: cv2.imdecode(np.fromfile(p, np.uint8), 1)
kf, ae = rd(kf_p), rd(ae_p)
H, W = kf.shape[:2]

# 1) person matte (RVM, single frame)
MODELS = Path(__file__).resolve().parents[6] / 'tools' / 'models'
sess = ort.InferenceSession(str(MODELS / 'rvm_resnet50_fp32.onnx'), providers=['CPUExecutionProvider'])
x = (cv2.cvtColor(kf, cv2.COLOR_BGR2RGB).astype(np.float32) / 255).transpose(2, 0, 1)[None]
rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
for _ in range(3):   # a few passes so the recurrent state settles on a still image
    fgr, pha, *rec = sess.run(None, {'src': x, 'r1i': rec[0], 'r2i': rec[1], 'r3i': rec[2], 'r4i': rec[3],
                                     'downsample_ratio': np.array([0.25], np.float32)})
person = pha[0, 0]

# 2) the held print: saturated region in the middle band + its white curls (bright, low-sat, touching it)
hsv = cv2.cvtColor(kf, cv2.COLOR_BGR2HSV)
# the print's deep-blue background only (sand is yellow and would leak in), then its convex hull
sat = ((hsv[..., 0] > 95) & (hsv[..., 0] < 130) & (hsv[..., 1] > 140) & (hsv[..., 2] > 40)).astype(np.uint8)
sat[: int(H * 0.45)] = 0; sat[int(H * 0.85):] = 0
sat = cv2.morphologyEx(sat, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.morphologyEx(sat, cv2.MORPH_CLOSE, np.ones((61, 61), np.uint8)))
pr = np.zeros((H, W), np.uint8)
if n > 1:
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    ys_, xs_ = np.nonzero((lab == i) & (sat > 0))
    hull = cv2.convexHull(np.column_stack([xs_, ys_]).astype(np.int32))
    cv2.fillConvexPoly(pr, hull, 1)
    x0, y0, w0, h0 = cv2.boundingRect(hull)
    # white curled corners: very bright + almost no colour (desert sand is yellow -> excluded), small blobs that
    # touch the print only
    b, g, r = [kf[..., c].astype(np.int16) for c in range(3)]
    white = ((hsv[..., 2] > 200) & (hsv[..., 1] < 30) & (np.abs(b - r) < 18)).astype(np.uint8)
    zone = np.zeros_like(white); zone[y0 - 30:y0 + h0 + 60, x0 - 40:x0 + w0 + 40] = 1
    white *= zone
    near = cv2.dilate(pr, np.ones((15, 15), np.uint8))
    nw, lw, sw, _ = cv2.connectedComponentsWithStats(white)
    for j in range(1, nw):
        if sw[j, cv2.CC_STAT_AREA] < 0.02 * w0 * h0 * 4 and (near[lw == j] > 0).any():
            pr[lw == j] = 1
    pr = cv2.morphologyEx(pr, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
fg = np.maximum(person, cv2.GaussianBlur(pr.astype(np.float32), (0, 0), 2))

# 3) ground plate from the aerial photo. --top: where the photo's top edge sits (lower = pyramids land below the
# paper); the band between the horizon and that edge keeps the keyframe's own hazy city (seam hidden by his body).
top = arg('--top', hz)
if top > hz or '--scale' in sys.argv:
    s = W * arg('--scale', 1.1) / ae.shape[1]
    aes = cv2.resize(ae, (int(ae.shape[1] * s) + 1, int(ae.shape[0] * s) + 1), interpolation=cv2.INTER_AREA)
    gh = H - int(H * top)
    if aes.shape[0] < gh:
        s2 = gh / aes.shape[0]; aes = cv2.resize(aes, (int(aes.shape[1] * s2) + 1, gh + 1), interpolation=cv2.INTER_AREA)
    cx = (aes.shape[1] - W) // 2
    plate = aes[:gh, cx:cx + W]
    hz = top
else:
    gh = int(H * (1 - hz)) + 80
    s = max(W / ae.shape[1], gh / ae.shape[0] * 1.0)
    aes = cv2.resize(ae, (int(ae.shape[1] * s) + 1, int(ae.shape[0] * s) + 1), interpolation=cv2.INTER_AREA)
    cx = (aes.shape[1] - W) // 2
    plate = aes[aes.shape[0] - gh:, cx:cx + W]
# the photo keeps its OWN colours (a per-channel match tinted the city blue -> the video model made it water);
# only brightness is matched to the old ground
old = kf[int(H * hz):]
gl = cv2.cvtColor(old, cv2.COLOR_BGR2GRAY).mean() / max(1, cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY).mean())
plate = plate.astype(np.float32) * (0.5 + 0.5 * gl)
# the photo's hazy top is blue/violet (shot through a plane window): neutralise per ROW band (gray world), then a
# light warm Cairo-haze grade, so nothing reads as water
for y in range(0, plate.shape[0], 16):
    band = plate[y:y + 16]
    m = band.reshape(-1, 3).mean(0); g = m.mean()
    band *= (g / np.maximum(m, 1))[None, None] * 0.6 + 0.4
plate = np.clip(plate * np.array([0.93, 1.0, 1.06], np.float32), 0, 255).astype(np.uint8)
ground = kf.copy()
y0g = H - gh
ground[y0g:] = plate
# soft blend into the keyframe's hazy horizon
ramp = np.clip((np.arange(H) - (H * hz)) / (H * 0.10), 0, 1).astype(np.float32)[:, None]
gmask = np.repeat(ramp, W, 1)
gmask *= (1 - fg)
a3 = gmask[..., None]
out = np.clip(kf * (1 - a3) + ground * a3, 0, 255).astype(np.uint8)
cv2.imencode('.png', out)[1].tofile(out_p)
if '--debug' in sys.argv:
    cv2.imencode('.jpg', (fg * 255).astype(np.uint8))[1].tofile(out_p.replace('.png', '_fg.jpg'))
print('ok', out_p)

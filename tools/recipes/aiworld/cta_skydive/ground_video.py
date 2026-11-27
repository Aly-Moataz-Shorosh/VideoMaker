"""Replace the generated ground in the skydive clip with a REAL aerial photo, every frame (Aly note 15).

Usage: python ground_video.py <in.mp4> <aerial.jpg> <out_silent.mp4> [--top 0.55] [--blend 0.08] [--drift 6] [--debug]
Camera is locked, so the ground is a still photo (tiny upward drift = falling). Kept from the clip per frame:
RVM person matte (recurrent, video) + the held print (deep-blue hull + white curls next to it) + everything above
the 'top' line (sky, banner, the hazy far ground), blended over --blend of the height so there is no seam.
The photo keeps its own colours; only its brightness is matched to the clip's ground.
"""
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort

src, ae_p, out = sys.argv[1:4]
arg = lambda k, d: float(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
top, blend, drift = arg('--top', 0.55), arg('--blend', 0.08), arg('--drift', 6)

cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
frames = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    frames.append(f)
H, W = frames[0].shape[:2]

ae = cv2.imdecode(np.fromfile(ae_p, np.uint8), 1)
s = W * 1.12 / ae.shape[1]
gh = H - int(H * top) + int(H * blend) + int(drift * H / 854) + 4
if ae.shape[0] * s < gh:
    s = gh / ae.shape[0]
aes = cv2.resize(ae, (int(ae.shape[1] * s) + 1, int(ae.shape[0] * s) + 1), interpolation=cv2.INTER_AREA)
cx = (aes.shape[1] - W) // 2
y_top = int(H * (top - blend))
# brightness only: match the photo's mean luminance to the clip's ground (frame 0)
g_clip = cv2.cvtColor(frames[0][int(H * top):], cv2.COLOR_BGR2GRAY).mean()
g_ph = cv2.cvtColor(aes[: H - int(H * top)], cv2.COLOR_BGR2GRAY).mean()
aes = np.clip(aes.astype(np.float32) * (0.5 + 0.5 * g_clip / max(g_ph, 1)), 0, 255)

ramp = np.clip((np.arange(H) - y_top) / max(1, H * blend), 0, 1).astype(np.float32)[:, None]

MODELS = Path(__file__).resolve().parents[6] / 'tools' / 'models'
sess = ort.InferenceSession(str(MODELS / 'rvm_resnet50_fp32.onnx'), providers=['CPUExecutionProvider'])
rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
ratio = np.array([0.25 if H > 1000 else 0.5], np.float32)


def held_print(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    sat = ((hsv[..., 0] > 95) & (hsv[..., 0] < 130) & (hsv[..., 1] > 140) & (hsv[..., 2] > 40)).astype(np.uint8)
    sat[: int(H * 0.45)] = 0; sat[int(H * 0.85):] = 0
    sat = cv2.morphologyEx(sat, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.morphologyEx(sat, cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8)))
    pr = np.zeros((H, W), np.uint8)
    if n < 2:
        return pr
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    ys, xs = np.nonzero((lab == i) & (sat > 0))
    hull = cv2.convexHull(np.column_stack([xs, ys]).astype(np.int32)); cv2.fillConvexPoly(pr, hull, 1)
    x0, y0, w0, h0 = cv2.boundingRect(hull)
    b, r = f[..., 0].astype(np.int16), f[..., 2].astype(np.int16)
    white = ((hsv[..., 2] > 185) & (hsv[..., 1] < 35) & (np.abs(b - r) < 20)).astype(np.uint8)
    zone = np.zeros_like(white); zone[max(0, y0 - 20):y0 + h0 + int(0.06 * H), max(0, x0 - 30):x0 + w0 + 30] = 1
    white *= zone
    near = cv2.dilate(pr, np.ones((9, 9), np.uint8))
    nw, lw, sw, _ = cv2.connectedComponentsWithStats(white)
    for j in range(1, nw):
        if sw[j, cv2.CC_STAT_AREA] < 0.15 * w0 * h0 and (near[lw == j] > 0).any():
            pr[lw == j] = 1
    return cv2.morphologyEx(pr, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))


ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(fps),
                       '-i', '-', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
nf = len(frames)
for k, f in enumerate(frames):
    x = (cv2.cvtColor(f, cv2.COLOR_BGR2RGB).astype(np.float32) / 255).transpose(2, 0, 1)[None]
    _, pha, *rec = sess.run(None, {'src': x, 'r1i': rec[0], 'r2i': rec[1], 'r3i': rec[2], 'r4i': rec[3], 'downsample_ratio': ratio})
    person = pha[0, 0]
    fg = np.maximum(person, cv2.GaussianBlur(held_print(f).astype(np.float32), (0, 0), 1.2))
    dy = int(round(drift * H / 854 * k / max(1, nf - 1)))
    plate = np.zeros_like(f, dtype=np.float32)
    seg = aes[dy: dy + (H - y_top), cx:cx + W]
    plate[y_top:y_top + seg.shape[0]] = seg
    a = (ramp * (1 - fg))[..., None]
    o = np.clip(f * (1 - a) + plate * a, 0, 255).astype(np.uint8)
    if '--debug' in sys.argv and k % 24 == 0:
        cv2.imencode('.jpg', (fg * 255).astype(np.uint8))[1].tofile(out.replace('.mp4', f'_fg{k:03d}.jpg'))
    ff.stdin.write(o.tobytes())
ff.stdin.close(); ff.wait()
print('done', nf, 'frames ->', out)

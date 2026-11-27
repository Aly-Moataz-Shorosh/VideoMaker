"""Keep the printed thumbnail STATIC on a moving/bending paper (Aly note 11: only his real face moves).

Usage: python freeze_print.py <in.mp4> <out_silent.mp4> [--ref ref.png] [--box x0 y0 x1 y1] [--debug]
- ref = the clean print (default: frame 0 of the video, or a keyframe image resized to the video).
- The paper region in frame 0 = the saturated blue/gold print area (auto) or --box.
- Every frame: dense optical flow (DIS, ultrafast->medium) from frame t back to frame 0 inside a dilated paper mask,
  then cv2.remap pulls the CLEAN print from frame 0 -> follows every bend/flutter of the paper, but the printed
  content (his printed face) stays the frame-0 picture. Light/folds kept: low-frequency luminance ratio t/0.
- The mask edge is feathered so paper edges and fingers on top come from the original frame.
"""
import subprocess
import sys

import cv2
import numpy as np

src, out = sys.argv[1:3]
debug = '--debug' in sys.argv
box = None
if '--box' in sys.argv:
    i = sys.argv.index('--box'); box = [int(v) for v in sys.argv[i + 1:i + 5]]

cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
frames = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    frames.append(f)
H, W = frames[0].shape[:2]
f0 = frames[0]
if '--ref' in sys.argv:
    r = cv2.imdecode(np.fromfile(sys.argv[sys.argv.index('--ref') + 1], np.uint8), 1)
    f0 = cv2.resize(r, (W, H), interpolation=cv2.INTER_AREA)


def print_mask(img):
    """Print = saturated area (deep blue bg + gold + red pill) in the lower-middle of the frame."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 1] > 90) & (hsv[..., 2] > 40)).astype(np.uint8) * 255
    m[: int(H * 0.40)] = 0; m[int(H * 0.85):] = 0          # sky banner (top) and the ground are out
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n < 2:
        return None
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h = st[i, :4]
    rect = np.zeros_like(m); cv2.rectangle(rect, (x, y), (x + w, y + h), 255, -1)
    return rect


if '--mask' in sys.argv:   # exact visible-print mask from fit_thumb.py (skips the curled corners)
    m0 = cv2.imdecode(np.fromfile(sys.argv[sys.argv.index('--mask') + 1], np.uint8), 0)
    m0 = (m0 > 127).astype(np.uint8) * 255
elif box:
    m0 = np.zeros((H, W), np.uint8); cv2.rectangle(m0, tuple(box[:2]), tuple(box[2:]), 255, -1)
else:
    m0 = print_mask(frames[0])
x, y, w, h = cv2.boundingRect(m0)
pad = int(max(w, h) * 0.35)
X0, Y0, X1, Y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
print('print box', (x, y, w, h), 'work box', (X0, Y0, X1, Y1))

dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
g0 = cv2.cvtColor(frames[0][Y0:Y1, X0:X1], cv2.COLOR_BGR2GRAY)
ref = f0[Y0:Y1, X0:X1].astype(np.float32)
mref = m0[Y0:Y1, X0:X1]
lum0 = cv2.GaussianBlur(cv2.cvtColor(frames[0][Y0:Y1, X0:X1], cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 9) + 1
hh, ww = g0.shape
gx, gy = np.meshgrid(np.arange(ww, dtype=np.float32), np.arange(hh, dtype=np.float32))

ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(fps),
                       '-i', '-', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
for k, f in enumerate(frames):
    o = f.copy()
    gt = cv2.cvtColor(f[Y0:Y1, X0:X1], cv2.COLOR_BGR2GRAY)
    flow = dis.calc(gt, g0, None)                        # for each pixel of frame t -> where it was in frame 0
    # paper motion only: fit a homography to the flow sampled on the print (RANSAC drops the moving printed mouth),
    # then add back a very smooth residual for the gentle bend. A small blur alone follows the printed face -> it "talks".
    ys_, xs_ = np.nonzero(cv2.erode(mref, np.ones((15, 15), np.uint8)))
    sel = np.random.default_rng(k).choice(len(xs_), min(3000, len(xs_)), replace=False)
    p_t = np.float32(np.column_stack([xs_[sel], ys_[sel]]))      # frame-t pixel grid points
    p_0 = p_t + flow[ys_[sel], xs_[sel]]
    Hm, _ = cv2.findHomography(p_t, p_0, cv2.RANSAC, 2.0)
    hx = (Hm[0, 0] * gx + Hm[0, 1] * gy + Hm[0, 2]) / (Hm[2, 0] * gx + Hm[2, 1] * gy + Hm[2, 2])
    hy = (Hm[1, 0] * gx + Hm[1, 1] * gy + Hm[1, 2]) / (Hm[2, 0] * gx + Hm[2, 1] * gy + Hm[2, 2])
    res = np.dstack([gx + flow[..., 0] - hx, gy + flow[..., 1] - hy])
    sig = max(W, H) * 0.03
    res = cv2.GaussianBlur(res, (0, 0), sig)
    flow = (np.dstack([hx - gx, hy - gy]) + res).astype(np.float32)
    mx, my = gx + flow[..., 0], gy + flow[..., 1]
    warped = cv2.remap(ref, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    wm = cv2.remap(mref, mx, my, cv2.INTER_NEAREST, borderValue=0)
    wm = cv2.erode(wm, np.ones((7, 7), np.uint8))
    lumt = cv2.GaussianBlur(gt.astype(np.float32), (0, 0), 9) + 1
    lum0w = cv2.remap(lum0, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    shade = np.clip(lumt / lum0w, 0.6, 1.4)[..., None]
    a = (cv2.GaussianBlur(wm.astype(np.float32), (0, 0), 3) / 255.0)[..., None]
    roi = o[Y0:Y1, X0:X1].astype(np.float32)
    o[Y0:Y1, X0:X1] = np.clip(roi * (1 - a) + warped * shade * a, 0, 255).astype(np.uint8)
    if debug and k % 24 == 0:
        cv2.rectangle(o, (X0, Y0), (X1, Y1), (0, 0, 255), 1)
    ff.stdin.write(o.tobytes())
ff.stdin.close(); ff.wait()
print('done', len(frames), 'frames ->', out)

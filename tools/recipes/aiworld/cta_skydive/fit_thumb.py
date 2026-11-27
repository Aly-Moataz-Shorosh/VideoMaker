"""Fit the REAL thumbnail onto the printed paper in frame 0 (SIFT homography) -> clean reference frame for freeze_print.

Usage: python fit_thumb.py <clip.mp4> <thumbnail.jpg> <ref_out.png> [--region x0 y0 x1 y1]
Prints the fitted quad and a --box (inset) to pass to freeze_print.py.
"""
import sys

import cv2
import numpy as np

clip, th_p, out = sys.argv[1:4]
cap = cv2.VideoCapture(clip); ok, f0 = cap.read()
H, W = f0.shape[:2]
th = cv2.imdecode(np.fromfile(th_p, np.uint8), 1)
reg = [int(v) for v in sys.argv[sys.argv.index('--region') + 1:sys.argv.index('--region') + 5]] if '--region' in sys.argv \
    else [0, int(H * 0.45), W, int(H * 0.85)]
g0 = cv2.cvtColor(f0, cv2.COLOR_BGR2GRAY); m = np.zeros_like(g0); m[reg[1]:reg[3], reg[0]:reg[2]] = 255
sift = cv2.SIFT_create(5000)
k1, d1 = sift.detectAndCompute(cv2.cvtColor(th, cv2.COLOR_BGR2GRAY), None)
k2, d2 = sift.detectAndCompute(g0, m)
good = [a for a, b in cv2.BFMatcher().knnMatch(d1, d2, k=2) if a.distance < 0.75 * b.distance]
src = np.float32([k1[a.queryIdx].pt for a in good]); dst = np.float32([k2[a.trainIdx].pt for a in good])
Hm, inl = cv2.findHomography(src, dst, cv2.RANSAC, 3.0)
print('matches', len(good), 'inliers', int(inl.sum()))
h, w = th.shape[:2]
c = cv2.perspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]])[None], Hm)[0]
print('quad', c.round(1).tolist())
wp = cv2.warpPerspective(th, Hm, (W, H), flags=cv2.INTER_AREA)
mk = cv2.erode(cv2.warpPerspective(np.full((h, w), 255, np.uint8), Hm, (W, H)), np.ones((3, 3), np.uint8))
# only where the PRINT is really visible in frame 0: colourful or dark pixels (not the white curled-back corners,
# not the pale ground seen behind them), holes filled -> also written as the freeze mask
hsv = cv2.cvtColor(f0, cv2.COLOR_BGR2HSV)
vis = (((hsv[..., 1] > 70) | (hsv[..., 2] < 95)) & (mk > 0)).astype(np.uint8) * 255
vis = cv2.morphologyEx(vis, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
cnts, _ = cv2.findContours(vis, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
vis = np.zeros_like(vis)
if cnts:
    cv2.drawContours(vis, [max(cnts, key=cv2.contourArea)], -1, 255, -1)
vis = cv2.morphologyEx(vis, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
mk = cv2.erode(vis, np.ones((5, 5), np.uint8))
cv2.imencode('.png', mk)[1].tofile(out.replace('.png', '_mask.png'))
l0 = cv2.GaussianBlur(g0.astype(np.float32), (0, 0), 12)
lw = cv2.GaussianBlur(cv2.cvtColor(wp, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 12) + 1
shade = np.clip(l0 / lw, 0.75, 1.25)[..., None]
a = (cv2.GaussianBlur(mk.astype(np.float32), (0, 0), 1.2) / 255)[..., None]
ref = np.clip(f0 * (1 - a) + wp * shade * a, 0, 255).astype(np.uint8)
cv2.imencode('.png', ref)[1].tofile(out)
x0, y0 = c[:, 0].min(), c[:, 1].min(); x1, y1 = c[:, 0].max(), c[:, 1].max()
ins = 0.05 * (x1 - x0)
print('box', int(x0 + ins), int(y0 + ins), int(x1 - ins), int(y1 - ins))
cv2.imencode('.jpg', np.hstack([f0[int(y0):int(y1), int(x0):int(x1)], ref[int(y0):int(y1), int(x0):int(x1)]]))[1].tofile(out.replace('.png', '_check.jpg'))

"""Static printed thumbnail for clips with BIG camera/body motion (Grok): find the real thumbnail in EVERY frame
(SIFT + RANSAC homography, thumbnail -> frame), smooth the homographies over time, paste the real thumbnail there.
Only where the print is visible in that frame (colourful/dark pixels inside the quad), so curled white corners,
fingers in front and the ground behind a curl stay from the clip. Light/shadows of the clip are kept.

Usage: python freeze_sift.py <in.mp4> <thumbnail.jpg> <out_silent.mp4> [--debug]
"""
import subprocess
import sys

import cv2
import numpy as np

src, th_p, out = sys.argv[1:4]
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
frames = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    frames.append(f)
H, W = frames[0].shape[:2]
th = cv2.imdecode(np.fromfile(th_p, np.uint8), 1)
th = cv2.resize(th, (960, int(960 * th.shape[0] / th.shape[1])), interpolation=cv2.INTER_AREA)
h, w = th.shape[:2]
corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]])[None]
sift = cv2.SIFT_create(4000)
k1, d1 = sift.detectAndCompute(cv2.cvtColor(th, cv2.COLOR_BGR2GRAY), None)
bf = cv2.BFMatcher()

# 1) homography per frame (thumbnail -> frame); search the lower 2/3 where the paper is
Hs, ok_ = [], []
reg = np.zeros((H, W), np.uint8); reg[int(H * 0.35):int(H * 0.92)] = 255
for f in frames:
    k2, d2 = sift.detectAndCompute(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), reg)
    Hm = None
    if d2 is not None and len(k2) > 20:
        good = [a for a, b in bf.knnMatch(d1, d2, k=2) if a.distance < 0.72 * b.distance]
        if len(good) >= 25:
            s_ = np.float32([k1[a.queryIdx].pt for a in good]); d_ = np.float32([k2[a.trainIdx].pt for a in good])
            Hm, inl = cv2.findHomography(s_, d_, cv2.RANSAC, 3.0)
            if Hm is None or inl.sum() < 20:
                Hm = None
    Hs.append(Hm)
# 2) fill gaps + smooth: work on the 4 projected corners, then back to homographies
C = []
for Hm in Hs:
    C.append(None if Hm is None else cv2.perspectiveTransform(corners, Hm)[0])
idx = [i for i, c in enumerate(C) if c is not None]
print('found in', len(idx), 'of', len(C), 'frames')
arr = np.zeros((len(C), 4, 2), np.float32)
for i in range(len(C)):
    if C[i] is not None:
        arr[i] = C[i]
    else:   # nearest found frame
        j = min(idx, key=lambda j: abs(j - i)); arr[i] = C[j]
sm = arr.copy()
for i in range(len(C)):   # small temporal blur (5 frames) against jitter
    a, b = max(0, i - 2), min(len(C), i + 3); sm[i] = arr[a:b].mean(0)
# 3) render
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(fps),
                       '-i', '-', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
for k, f in enumerate(frames):
    Hk = cv2.getPerspectiveTransform(corners[0], sm[k])
    wp = cv2.warpPerspective(th, Hk, (W, H), flags=cv2.INTER_AREA).astype(np.float32)
    quad = cv2.warpPerspective(np.full((h, w), 255, np.uint8), Hk, (W, H))
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    # print pixels = where the clip LOOKS LIKE the thumbnail placed there (blurred colour distance), so the dark city
    # seen behind a curled corner or the white back of the paper is never covered (Grok's print is a close copy)
    dist = cv2.GaussianBlur(np.abs(f.astype(np.float32) - wp).mean(2), (0, 0), 5)
    vis = ((dist < 48) & (quad > 0)).astype(np.uint8) * 255
    vis = cv2.morphologyEx(vis, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
    cnts, _ = cv2.findContours(vis, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    vm = np.zeros_like(vis)
    if cnts:
        cv2.drawContours(vm, [max(cnts, key=cv2.contourArea)], -1, 255, -1)
    vm = cv2.erode(cv2.morphologyEx(vm, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8)), np.ones((5, 5), np.uint8))
    # his FINGERS grip the paper's left/right edges and must stay in front (Aly: «حطيت الصورة على ايدي»):
    # skin-coloured pixels inside the outer 16% bands of the sheet are taken from the clip, not the print
    band = np.zeros((h, w), np.uint8); bw = int(w * 0.16); band[:, :bw] = 255; band[:, w - bw:] = 255
    bandw = cv2.warpPerspective(band, Hk, (W, H))
    ycc = cv2.cvtColor(f, cv2.COLOR_BGR2YCrCb)
    skin = ((ycc[..., 1] > 135) & (ycc[..., 1] < 180) & (ycc[..., 2] > 80) & (ycc[..., 2] < 130) & (ycc[..., 0] > 60)).astype(np.uint8)
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    skin = cv2.dilate(skin, np.ones((7, 7), np.uint8)) * (bandw > 0)
    vm[skin > 0] = 0
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
    shade = np.clip(cv2.GaussianBlur(g, (0, 0), 14) / (cv2.GaussianBlur(cv2.cvtColor(wp.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 14) + 1), 0.7, 1.3)[..., None]
    a = (cv2.GaussianBlur(vm.astype(np.float32), (0, 0), 1.5) / 255)[..., None]
    o = np.clip(f * (1 - a) + wp * shade * a, 0, 255).astype(np.uint8)
    ff.stdin.write(o.tobytes())
ff.stdin.close(); ff.wait()
print('done', len(frames), '->', out)

"""Replace the AI-printed (unscannable) QR on the paper with the REAL QR, tracked so it moves/tilts with the paper.

Usage: python qr_track_replace.py <in.mp4> <qr.png> <out_silent.mp4> [--debug]
1. Frame 0: printed QR = biggest cluster of dark pixels inside the white paper -> its 4 corners (minAreaRect).
2. Every frame: track feature points of the printed pattern (Lucas-Kanade, frame to frame), homography from
   frame 0 with RANSAC; re-detect corners from scratch when tracking gets weak.
3. Draw the real QR into the tracked quad. Paper shading (folds, light) is kept: QR white = paper brightness
   (dark modules removed by a max-filter, then blurred), QR black = that brightness * 0.12.
"""
import sys

import cv2
import numpy as np

src, qr_path, out = sys.argv[1:4]
debug = "--debug" in sys.argv
qr = cv2.imread(qr_path, cv2.IMREAD_GRAYSCALE)
qh, qw = qr.shape
qr_corners = np.float32([[0, 0], [qw, 0], [qw, qh], [0, qh]])


def order(pts):
    s, d = pts.sum(1), np.diff(pts, axis=1).ravel()
    return np.float32([pts[np.argmin(s)], pts[np.argmin(d)], pts[np.argmax(s)], pts[np.argmax(d)]])


def detect_quad(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    b, r = frame[..., 0].astype(np.int16), frame[..., 2].astype(np.int16)
    paper = ((hsv[..., 2] > 150) & (hsv[..., 1] < 50) & (np.abs(b - r) < 30)).astype(np.uint8) * 255
    paper = cv2.morphologyEx(paper, cv2.MORPH_CLOSE, np.ones((41, 41), np.uint8))  # fill the printed modules
    n, lab, st, _ = cv2.connectedComponentsWithStats(paper)
    if n < 2:
        return None
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    region = (lab == i).astype(np.uint8)
    region = cv2.erode(region, np.ones((9, 9), np.uint8))
    dark = ((hsv[..., 2] < 120) & (region > 0)).astype(np.uint8) * 255
    dark = cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    ys, xs = np.nonzero(dark)
    if len(xs) < frame.shape[0] * frame.shape[1] * 0.004:
        return None
    pts = np.column_stack([xs, ys]).astype(np.float32)
    # drop stray dark pixels far from the pattern's centre (edges of fingers, folds)
    c = np.median(pts, 0)
    d = np.linalg.norm(pts - c, axis=1)
    pts = pts[d < np.percentile(d, 98) * 1.05]
    return order(cv2.boxPoints(cv2.minAreaRect(pts)))


def paper_light(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    light = cv2.dilate(gray, np.ones((25, 25), np.uint8))  # removes the dark printed modules
    return cv2.GaussianBlur(light, (0, 0), 9).astype(np.float32)


cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
det = cv2.QRCodeDetector()
prev_gray, pts, quad, smooth, total, decoded, redetects = None, None, None, None, 0, 0, 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    total += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if pts is not None and len(pts) >= 12:
        nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, pts, None, winSize=(31, 31), maxLevel=4)
        good_old, good_new = pts[st.ravel() == 1], nxt[st.ravel() == 1]
        if len(good_new) >= 12:
            H, inl = cv2.findHomography(good_old, good_new, cv2.RANSAC, 4.0)
            if H is not None and inl.sum() >= 10:
                quad = cv2.perspectiveTransform(quad.reshape(-1, 1, 2), H).reshape(4, 2)
                pts = good_new[inl.ravel() == 1].reshape(-1, 1, 2)
            else:
                pts = None
        else:
            pts = None
    if pts is None or len(pts) < 40 or total % 8 == 0:  # (re)detect the printed QR, re-seed points inside it
        q = detect_quad(frame)
        if q is not None and quad is not None and np.abs(q - quad).max() > 0.25 * np.linalg.norm(quad[0] - quad[2]):
            q = None  # detection jumped (hand/fold) -> keep tracking
        if q is not None:
            quad = q if quad is None else quad * 0.5 + q * 0.5
            m = np.zeros_like(gray)
            cv2.fillConvexPoly(m, quad.astype(np.int32), 255)
            pts = cv2.goodFeaturesToTrack(gray, 400, 0.01, 6, mask=m)
            redetects += 1
    prev_gray = gray
    if quad is not None:
        smooth = quad if smooth is None else smooth * 0.4 + quad * 0.6
        # grow 6% so the real QR fully covers the AI-printed pattern
        c = smooth.mean(0)
        dst = (c + (smooth - c) * 1.08).astype(np.float32)
        M = cv2.getPerspectiveTransform(qr_corners, dst)
        warped = cv2.warpPerspective(qr, M, (w, h), flags=cv2.INTER_AREA, borderValue=0, borderMode=cv2.BORDER_CONSTANT)
        area = cv2.warpPerspective(np.full_like(qr, 255), M, (w, h), flags=cv2.INTER_AREA)
        a = (area.astype(np.float32) / 255.0)[..., None]
        light = paper_light(frame)
        tone = np.where(warped > 127, 1.0, 0.12).astype(np.float32) * light
        tint = frame.astype(np.float32).mean((0, 1)) * 0 + np.array([1.0, 1.0, 1.0], np.float32)
        qr_rgb = tone[..., None] * tint
        frame = (frame.astype(np.float32) * (1 - a) + qr_rgb * a).clip(0, 255).astype(np.uint8)
        if det.detectAndDecode(frame)[0]:
            decoded += 1
        if debug:
            cv2.polylines(frame, [smooth.astype(np.int32)], True, (0, 0, 255), 2)
    writer.write(frame)
writer.release()
print(f"frames {total}, QR decoded in {decoded} ({decoded * 100 // max(total, 1)}%), re-detections {redetects}")

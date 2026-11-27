"""CTA finish: the video's THUMBNAIL printed on the paper (tracked, moves/bends with it) + the REAL QR as a clean card
in the sky (top right) from the moment he says "scan" + mix: his voice over the clip's own wind sound.

Usage: python paper_thumb.py <in.mp4> <thumb.jpg> <qr.png> <voice> <wind_src.mp4> <out.mp4> [--qr-at 2.9] [--qr-size 0.18] [--qr-y 0.025] [--no-paper] [--debug]
Tracking = qr_track_replace.py: the AI-printed pattern on the paper gives the feature points (LK + RANSAC
homography, re-detect every 8 frames). The paper's corners are stored once in the pattern's own coordinates, so
the thumbnail follows the paper with the same homography.
"""
import subprocess
import sys

import cv2
import numpy as np



def order(pts):
    s, d = pts.sum(1), np.diff(pts, axis=1).ravel()
    return np.float32([pts[np.argmin(s)], pts[np.argmin(d)], pts[np.argmax(s)], pts[np.argmax(d)]])


_QR_DETECTORS = [cv2.QRCodeDetectorAruco(), cv2.QRCodeDetector()]


def detect_quad(frame):
    """The AI-printed QR: OpenCV finds its 3 finder squares (it can't decode it, but the corners are right), and
    returns the corners in the code's own order, so orientation never flips. Fallback: dark-pattern blob."""
    for d in _QR_DETECTORS:
        ok, p = d.detect(frame)
        if ok and p is not None:
            q = p.reshape(-1, 2)[:4].astype(np.float32)
            if len(q) == 4 and cv2.isContourConvex(q) and area(q) > frame.shape[0] * frame.shape[1] * 0.01:
                return q
    return None


def detect_quad_blob(frame):
    """(unused fallback) The AI-printed pattern on the paper: dark pixels inside the white sheet -> min-area rectangle."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    b, r = frame[..., 0].astype(np.int16), frame[..., 2].astype(np.int16)
    paper = ((hsv[..., 2] > 150) & (hsv[..., 1] < 50) & (np.abs(b - r) < 30)).astype(np.uint8) * 255
    paper = cv2.morphologyEx(paper, cv2.MORPH_CLOSE, np.ones((41, 41), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(paper)
    if n < 2:
        return None
    # the sheet = the white blob with the densest dark pattern (the banner is white too, but its print is sparse)
    darkpx = hsv[..., 2] < 120
    best, best_score = None, 0.0
    for i in 1 + np.argsort(st[1:, cv2.CC_STAT_AREA])[::-1][:4]:
        if st[i, cv2.CC_STAT_AREA] < frame.shape[0] * frame.shape[1] * 0.01:
            continue
        reg = cv2.erode((lab == i).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
        score = darkpx[reg].mean() if reg.any() else 0
        if score > best_score:
            best, best_score = reg, score
    if best is None or best_score < 0.18:
        return None
    region = best.astype(np.uint8)
    dark = (darkpx & (region > 0)).astype(np.uint8) * 255
    dark = cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    ys, xs = np.nonzero(dark)
    if len(xs) < frame.shape[0] * frame.shape[1] * 0.004:
        return None
    pts = np.column_stack([xs, ys]).astype(np.float32)
    c = np.median(pts, 0)
    d = np.linalg.norm(pts - c, axis=1)
    pts = pts[d < np.percentile(d, 98) * 1.05]
    return order(cv2.boxPoints(cv2.minAreaRect(pts)))


def paper_light(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    light = cv2.dilate(gray, np.ones((25, 25), np.uint8))  # removes the dark printed modules
    return cv2.GaussianBlur(light, (0, 0), 9).astype(np.float32)

args = [a for a in sys.argv[1:] if not a.startswith("--")]
src, thumb_path, qr_path, voice, wind_src, out = args[:6]
debug = "--debug" in sys.argv
no_paper = "--no-paper" in sys.argv  # v3: thumbnail is already held in the clip -> only QR card + footer + audio
qr_at = float(sys.argv[sys.argv.index("--qr-at") + 1]) if "--qr-at" in sys.argv else 2.9
tmp = out.replace(".mp4", "_silent.mp4")

thumb = cv2.imread(thumb_path)
th, tw = thumb.shape[:2]
qr = cv2.imread(qr_path, cv2.IMREAD_GRAYSCALE)
UNIT = np.float32([[0, 0], [1, 0], [1, 1], [0, 1]])


def paper_mask(frame, quad):
    """This frame's sheet: the white blob that CONTAINS the printed pattern (the banner is white too, often bigger)."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    b, r = frame[..., 0].astype(np.int16), frame[..., 2].astype(np.int16)
    m = ((hsv[..., 2] > 140) & (hsv[..., 1] < 55) & (np.abs(b - r) < 32)).astype(np.uint8) * 255
    cv2.fillConvexPoly(m, quad.astype(np.int32), 255)  # the printed pattern itself is part of the sheet
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((21, 21), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    cx, cy = np.clip(quad.mean(0).astype(int), 0, [frame.shape[1] - 1, frame.shape[0] - 1])
    if lab[cy, cx] == 0:
        return None
    sheet = (lab == lab[cy, cx]).astype(np.uint8)
    # never let it grow into the banner: keep it within 1.9x the pattern's size around the pattern
    hull = np.zeros_like(sheet)
    c = quad.mean(0)
    u = ((quad[1] - quad[0]) + (quad[2] - quad[3])) / 4
    v = ((quad[3] - quad[0]) + (quad[2] - quad[1])) / 4
    lim = np.float32([c - 1.55 * u - 1.3 * v, c + 1.55 * u - 1.3 * v, c + 1.55 * u + 1.3 * v, c - 1.55 * u + 1.3 * v])
    cv2.fillConvexPoly(hull, lim.astype(np.int32), 1)  # the sheet is only a bit bigger than its print (clouds!)
    return sheet * hull


def upright(q):
    """Start orientation: top edge as horizontal as possible, going left→right."""
    return max((np.roll(q, k, 0) for k in range(4)),
               key=lambda r: (r[1][0] - r[0][0]) / (np.linalg.norm(r[1] - r[0]) + 1e-6))


def match_order(q, ref):
    """Same corner order as ref (detections can come back rotated by 90°)."""
    best = min(range(4), key=lambda k: np.abs(np.roll(q, k, 0) - ref).sum())
    return np.roll(q, best, 0)


def area(q):
    return abs(cv2.contourArea(q.astype(np.float32)))


def qr_card(size):
    pad = size // 14
    card = np.full((size, size, 3), 255, np.uint8)
    q = cv2.resize(qr, (size - 2 * pad, size - 2 * pad), interpolation=cv2.INTER_NEAREST)
    card[pad:size - pad, pad:size - pad] = cv2.cvtColor(q, cv2.COLOR_GRAY2BGR)
    mask = np.zeros((size, size), np.uint8)
    rad = size // 10
    cv2.rectangle(mask, (rad, 0), (size - rad, size), 255, -1)
    cv2.rectangle(mask, (0, rad), (size, size - rad), 255, -1)
    for c in [(rad, rad), (size - rad, rad), (rad, size - rad), (size - rad, size - rad)]:
        cv2.circle(mask, c, rad, 255, -1, cv2.LINE_AA)
    return card, mask


cap = cv2.VideoCapture(src)
fps = cap.get(cv2.CAP_PROP_FPS)
w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter(tmp, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
qr_size = float(sys.argv[sys.argv.index("--qr-size") + 1]) if "--qr-size" in sys.argv else 0.18  # of width
qr_y = float(sys.argv[sys.argv.index("--qr-y") + 1]) if "--qr-y" in sys.argv else 0.025  # top, of height
card_size = int(w * qr_size)
card, card_mask = qr_card(card_size)
cx0, cy0 = w - card_size - int(w * 0.04), int(h * qr_y)  # small, up in the empty sky (Aly, note 5)
footer = cv2.imread("footer_follow.png", cv2.IMREAD_UNCHANGED)  # make_footer.py (style 26 handles + "Follow")
if footer is not None and footer.shape[1] != w:
    footer = cv2.resize(footer, (w, int(footer.shape[0] * w / footer.shape[1])), interpolation=cv2.INTER_AREA)
det = cv2.QRCodeDetector()

prev_gray, pts, quad, smooth, total, decoded = None, None, None, None, 0, 0
while True:
    ok, frame = cap.read()
    if not ok:
        break
    total += 1
    t = (total - 1) / fps
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if pts is not None and len(pts) >= 12:
        nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, pts, None, winSize=(31, 31), maxLevel=4)
        go, gn = pts[st.ravel() == 1], nxt[st.ravel() == 1]
        pts = None
        if len(gn) >= 12:
            H, inl = cv2.findHomography(go, gn, cv2.RANSAC, 4.0)
            if H is not None and inl.sum() >= 10:
                nq = cv2.perspectiveTransform(quad.reshape(-1, 1, 2), H).reshape(4, 2)
                if 0.7 < area(nq) / max(area(quad), 1) < 1.4 and cv2.isContourConvex(nq.astype(np.float32)):
                    quad = nq
                    pts = gn[inl.ravel() == 1].reshape(-1, 1, 2)
    if not no_paper and (pts is None or len(pts) < 40 or total % 8 == 0):
        q = detect_quad(frame)
        if q is not None and quad is not None:
            q = match_order(q, quad)
            if np.abs(q - quad).max() > 0.25 * np.linalg.norm(quad[0] - quad[2]):
                q = None
        if q is not None:
            quad = upright(q) if quad is None else quad * 0.5 + q * 0.5
            m = np.zeros_like(gray)
            cv2.fillConvexPoly(m, quad.astype(np.int32), 255)
            pts = cv2.goodFeaturesToTrack(gray, 400, 0.01, 6, mask=m)
    prev_gray = gray

    sheet = paper_mask(frame, quad) if quad is not None else None
    if quad is not None and sheet is not None:
        smooth = quad if smooth is None else smooth * 0.4 + match_order(quad, smooth) * 0.6
        # thumbnail centred on the printed pattern, along the pattern's own axes, 16:9, a bit wider than it
        c = smooth.mean(0)
        u = ((smooth[1] - smooth[0]) + (smooth[2] - smooth[3])) / 4  # half-width vector
        v = ((smooth[3] - smooth[0]) + (smooth[2] - smooth[1])) / 4  # half-height vector
        u = u * 1.32
        v = v / np.linalg.norm(v) * np.linalg.norm(u) * th / tw
        dst = np.float32([c - u - v, c + u - v, c + u + v, c - u + v])
        src_c = np.float32([[0, 0], [tw, 0], [tw, th], [0, th]])
        M = cv2.getPerspectiveTransform(src_c, dst)
        warped = cv2.warpPerspective(thumb, M, (w, h), flags=cv2.INTER_AREA)
        a = cv2.warpPerspective(np.full((th, tw), 255, np.uint8), M, (w, h), flags=cv2.INTER_AREA)
        a = (a.astype(np.float32) * sheet).astype(np.uint8)  # only on the sheet, never over his fingers
        # whole sheet white first, so none of the AI pattern peeks out around the thumbnail
        pa = cv2.GaussianBlur(sheet.astype(np.float32) * 255, (0, 0), 1.5)[..., None] / 255
        paper = dst
        light = paper_light(frame)
        ref = np.percentile(light[pa[..., 0] > 0.5], 90) if (pa > 0.5).any() else 230.0
        shade = np.clip(light / ref, 0.55, 1.08)[..., None]
        white = np.full_like(frame, 245, dtype=np.float32) * shade
        frame = (frame.astype(np.float32) * (1 - pa) + white * pa)
        af = a.astype(np.float32)[..., None] / 255
        frame = (frame * (1 - af) + warped.astype(np.float32) * shade * af).clip(0, 255).astype(np.uint8)
        if debug:
            cv2.polylines(frame, [paper.astype(np.int32)], True, (0, 0, 255), 2)

    if t >= qr_at:  # QR card in the sky, top right: quick pop then still, soft shadow
        k = min(1.0, (t - qr_at) / 0.25)
        s = 0.6 + 0.4 * (1 - (1 - k) ** 3) + 0.06 * np.sin(np.pi * k)
        sz = max(8, int(card_size * s))
        c_img, c_m = cv2.resize(card, (sz, sz)), cv2.resize(card_mask, (sz, sz))
        x = cx0 + (card_size - sz) // 2
        y = cy0 + (card_size - sz) // 2
        sh = cv2.GaussianBlur(c_m, (0, 0), sz / 25).astype(np.float32) / 255 * 0.45 * k
        sx, sy = x + sz // 30, y + sz // 20
        roi = frame[sy:sy + sz, sx:sx + sz].astype(np.float32)
        frame[sy:sy + sz, sx:sx + sz] = (roi * (1 - sh[..., None])).astype(np.uint8)
        m = c_m.astype(np.float32)[..., None] / 255 * k
        roi = frame[y:y + sz, x:x + sz].astype(np.float32)
        frame[y:y + sz, x:x + sz] = (roi * (1 - m) + c_img * m).astype(np.uint8)
        if det.detectAndDecode(frame)[0]:
            decoded += 1
    if footer is not None:  # handles footer, whole clip
        fh = footer.shape[0]
        y = h - fh - int(h * 0.045)
        fa = footer[..., 3:].astype(np.float32) / 255
        roi = frame[y:y + fh].astype(np.float32)
        frame[y:y + fh] = (roi * (1 - fa) + footer[..., :3].astype(np.float32) * fa).astype(np.uint8)
    writer.write(frame)
writer.release()
print(f"frames {total}, QR decoded in {decoded} of the frames after {qr_at}s")

dur = total / fps
subprocess.run([
    "ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-i", voice, "-i", wind_src,
    "-filter_complex",
    "[2:a]volume=0.9[wind];[1:a]highpass=f=90,volume=1.5[vo];"
    "[vo][wind]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]",
    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac",
    "-b:a", "192k", "-t", f"{dur:.2f}", out], check=True)
print("wrote", out)

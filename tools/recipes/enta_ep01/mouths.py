"""Who talks when (visual): mouth motion of the LEFT person (Aly) and the RIGHT person (guest), 10 fps.
Faces found with a haar cascade every 0.5 s per half of the frame; mouth = lower 40% of the face box.
Writes work/mouths.npy  rows = [t, mouthL, mouthR, faceL_x, faceL_y, faceR_x, faceR_y] (x,y as 0..1 of the frame)."""
import subprocess, sys, numpy as np, cv2
from pathlib import Path
W = Path(__file__).resolve().parents[1]
video = str(W.parent / 'input' / 'A1f.mp4')
w, h, fps = 960, 540, 10
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', video, '-vf', f'fps={fps},scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                     stdout=subprocess.PIPE)
cas = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face = {0: (160, 110, 105), 1: (680, 110, 90)}  # x, y, size (top-left) per side
prev = None; rows = []; i = 0
while True:
    b = p.stdout.read(w * h)
    if len(b) < w * h: break
    g = np.frombuffer(b, np.uint8).reshape(h, w)
    if i % 5 == 0:
        for side in (0, 1):
            x0 = 0 if side == 0 else w // 2
            fs = cas.detectMultiScale(g[:, x0:x0 + w // 2], 1.1, 5, minSize=(60, 60))
            if side == 0: continue  # Aly turns to the guest (profile) -> haar misses him; fixed box from frame 300
            if len(fs):
                fx, fy, fw, fh = max(fs, key=lambda f: f[2])
                face[side] = (x0 + fx, fy, fw)
    m = []
    for side in (0, 1):
        x, y, s = face[side]
        y0, y1, x1 = y + int(s * 0.62), y + int(s * 1.05), x + s
        if prev is None: m.append(0.0); continue
        d = np.abs(g[y0:y1, x + s // 5:x1 - s // 5].astype(np.int16) - prev[y0:y1, x + s // 5:x1 - s // 5]).mean()
        dd = np.abs(g[y:y + s // 2, x:x1].astype(np.int16) - prev[y:y + s // 2, x:x1]).mean()  # upper face = head motion
        m.append(float(d - 0.8 * dd))
    rows.append([i / fps, *m, (face[0][0] + face[0][2] / 2) / w, (face[0][1] + face[0][2] / 2) / h,
                 (face[1][0] + face[1][2] / 2) / w, (face[1][1] + face[1][2] / 2) / h])
    prev = g; i += 1
np.save(W / 'mouths.npy', np.array(rows, np.float32))
print('frames', i)

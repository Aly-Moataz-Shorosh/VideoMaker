"""QC of his camera (Aly 2026-10-19: "الكاميرا في النص مبقتش بصالي"): sample cam_NN.mp4 at 2 fps, find the person on the stage
with the RVM people matte, and report every stretch where he is near the frame edge or missing.
python qc_cam.py 7 9 12 ...   -> prints 'OK' or the bad seconds per short"""
import subprocess, sys
from pathlib import Path
import cv2
import numpy as np
import onnxruntime as ort
P = Path(__file__).resolve().parents[2]
RVM = ort.InferenceSession(str(P.parents[1] / 'tools' / 'models' / 'rvm_mobilenetv3_fp32.onnx'), providers=['CPUExecutionProvider'])
W, H = 270, 480


def check(n):
    f = P / 'work' / 'cam' / f'cam_{n:02d}.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(f), '-vf', f'fps=2,scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
    bad, i = [], 0
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        x = (np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32) / 255).transpose(2, 0, 1)[None].copy()
        _, pha, *rec = RVM.run(None, {'src': x, 'r1i': rec[0], 'r2i': rec[1], 'r3i': rec[2], 'r4i': rec[3], 'downsample_ratio': np.array([1.0], np.float32)})
        al = pha[0, 0] > 0.5
        # him = a blob in the stage part of the frame (his head ~y 0.22, feet ~y 0.6 of the short)
        n_, lab, st, cen = cv2.connectedComponentsWithStats(al[int(H * 0.12):int(H * 0.68)].astype(np.uint8))
        cands = [cen[k][0] / W for k in range(1, n_) if st[k][cv2.CC_STAT_HEIGHT] > H * 0.25 and st[k][cv2.CC_STAT_AREA] > 300]
        cx = min(cands, key=lambda v: abs(v - 0.5)) if cands else None
        if cx is None or cx < 0.22 or cx > 0.78:
            bad.append((i / 2, None if cx is None else round(cx, 2)))
        i += 1
    p.wait()
    # group into stretches (>= 1 s)
    out, cur = [], None
    for t, cx in bad:
        if cur and t - cur[1] <= 0.6:
            cur[1] = t
        else:
            if cur and cur[1] - cur[0] >= 1: out.append(cur)
            cur = [t, t]
    if cur and cur[1] - cur[0] >= 1: out.append(cur)
    print(f'short {n}:', 'OK' if not out else ' '.join(f'{a:.0f}-{b:.0f}s' for a, b in out), flush=True)


for n in map(int, sys.argv[1:]):
    check(n)

"""PICTURE gate before rendering (Aly 2026-10-21: picture must match the voice): for every piece of short N, frames of
cam_N.mp4 at its timeline vs the SOURCE frames around the same source second (±0.5 s) -> best offset must be 0 (one frame max).
python qc_cam.py 6 3 5 2 7"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
SRC = P / 'input' / 'Uc47QvWaocs.mp4'
PUB = ROOT / 'motion-library' / 'public' / 'projects' / P.name


def grab(f, ss, t):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{ss:.3f}', '-i', str(f), '-t', f'{t:.3f}', '-vf', 'fps=30,scale=96:54,format=gray',
                        '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, 54, 96).astype(np.float32)


bad = 0
for n in map(int, sys.argv[1:]):
    segs = json.load(open(W / f'segs_{n}.json'))
    worst = 0.0
    for s in segs:
        L = s['n'] / 30
        a0 = round(s['src'] * 30) / 30  # the frame the piece was cut at
        for k in ([L / 2] if L < 2 else [0.5, L / 2, L - 0.5]):
            k = round(k * 30) / 30
            c = grab(PUB / f'cam_{n}.mp4', s['tl'] + k, 0.3)[:6]
            r = grab(SRC, a0 + k - 0.5, 1.3)
            if len(c) < 6 or len(r) < 36:
                continue
            d = [((r[j:j + 6] - c) ** 2).mean() for j in range(0, len(r) - 6)]
            j = int(np.argmin(d)); off = (j - 15) / 30
            if np.max(np.abs(np.diff(c, axis=0))) < 1.0 and min(d) < 4:  # still picture: any offset matches
                off = 0.0
            worst = max(worst, abs(off))
            if abs(off) > 0.034:
                print(f'  short {n} piece src {a0:.2f} +{k:.1f}s: picture off {off:+.3f}s')
    ok = worst <= 0.034
    bad += not ok
    print(f'short {n}: worst picture offset {worst:.3f}s ->', 'OK' if ok else 'FAIL')
sys.exit(1 if bad else 0)

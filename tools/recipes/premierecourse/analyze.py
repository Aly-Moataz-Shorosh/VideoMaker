# Per episode, from the 720p recording (one pass, 4 fps, 320 px wide):
#   cursor: his yellow cursor highlight (x, y in source px, or null) -> smart zoom targets
#   diff:   how much the screen changed since the last sample (0..255) -> still screen detection
#   rms:    audio level per 0.1 s in dB -> quiet spots (chapter edges) and silent waits (fast-forward candidates)
# Writes work/ep<N>/analysis.json.   python analyze.py 1 2 3
import json, subprocess, sys
from pathlib import Path
import numpy as np

PROJ = Path(__file__).resolve().parents[2]
W, H, FPS = 320, 180, 4
SX = 1276 / W


def video(ep):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(PROJ / f'input/ep{ep}.mp4'), '-vf', f'fps={FPS},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         stdout=subprocess.PIPE)
    prev, cur, dif = None, [], []
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        a = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.int16)
        r, g, bl = a[..., 0], a[..., 1], a[..., 2]
        m = (r > 100) & (g > 90) & (bl < r * 0.4) & (np.abs(r - g) < 35)  # his yellow cursor highlight (semi-transparent: ~(138,130,5) over black)
        m[H - 9:, :] = False  # taskbar icons
        ys, xs = np.nonzero(m)
        cur.append([round(float(xs.mean()) * SX), round(float(ys.mean()) * SX)] if 6 <= len(xs) <= 260 else None)
        g8 = a.mean(2)
        dif.append(round(float(np.abs(g8 - prev).mean()), 2) if prev is not None else 0)
        prev = g8
    return cur, dif


def audio(ep):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(PROJ / f'input/ep{ep}.mp4'), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    n = len(a) // 1600
    rms = np.sqrt((a[: n * 1600].reshape(n, 1600) ** 2).mean(1))
    return [round(float(v), 1) for v in 20 * np.log10(rms + 1e-9)]


for ep in map(int, sys.argv[1:]):
    cur, dif = video(ep)
    rms = audio(ep)
    out = PROJ / f'work/ep{ep}/analysis.json'
    json.dump(dict(fps=FPS, cursor=cur, diff=dif, rms_step=0.1, rms=rms), open(out, 'w'))
    seen = sum(c is not None for c in cur)
    print(ep, len(cur), 'samples, cursor found', round(100 * seen / max(1, len(cur))), '%', out, flush=True)

"""Piecewise alignment of his clean voice to an EDITED episode (his edit cut / moved parts of the recording).
Every 1 s window of the episode -> best voice offset (whole-file search) -> runs of the same offset -> map [(video_from, off), ...]
(cut points snapped to the quietest 10 ms near each change). Updates work/huwa_voice.json with 'map'.
python work/scripts/align_pieces.py 02 03 05 ..."""
import glob, json, subprocess, sys
from pathlib import Path
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
P = Path(__file__).resolve().parents[2]
J = P / 'work' / 'huwa_voice.json'
cfg = json.load(open(J, encoding='utf8'))


def env(f, sr=8000):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(np.float32)
    h = sr // 100; n = len(a) // h
    return np.log(np.sqrt((a[:n * h].reshape(n, h) ** 2).mean(1)) + 1)


for ep in sys.argv[1:]:
    a = env(glob.glob(str(P / 'input' / f'{ep}_*.mp4'))[0]); b = env(P / cfg[ep]['file'])
    bn = (b - b.mean()) / b.std()
    # sliding normalised correlation of a 1.5 s window against the whole voice (FFT)
    W = 150; rows = []
    for t in np.arange(0, len(a) / 100 - 1.5, 0.5):
        s = int(t * 100); seg = a[s:s + W]
        if seg.std() < 0.25:
            rows.append((t, None, 0)); continue
        sg = (seg - seg.mean()) / seg.std()
        c = np.correlate(bn, sg, 'valid') / W
        # local normalisation of b windows
        cs = np.convolve(bn, np.ones(W), 'valid'); cs2 = np.convolve(bn ** 2, np.ones(W), 'valid')
        sd = np.sqrt(np.maximum(cs2 / W - (cs / W) ** 2, 1e-6))
        cn = c / sd
        k = int(np.argmax(cn)); rows.append((t, round(k / 100 - t, 2), float(cn[k])))
    # runs: keep confident windows, smooth by majority over neighbours
    good = [(t, o) for t, o, q in rows if o is not None and q > 0.75]
    pieces = []
    for t, o in good:
        if pieces and abs(pieces[-1][1] - o) <= 0.08:
            pieces[-1][2] = t; continue
        pieces.append([t, o, t])
    pieces = [p for p in pieces if p[2] - p[0] >= 1.0 or len(pieces) == 1]
    m = []
    for i, (t0, o, t1) in enumerate(pieces):
        if not m:
            m.append((0.0, o)); continue
        lo, hi = int(pieces[i - 1][2] * 100) + 100, int(t0 * 100) + 150  # change happens between the two runs
        cut = (lo + int(np.argmin(a[lo:max(lo + 1, hi)]))) / 100 if hi > lo else t0
        if abs(o - m[-1][1]) > 0.08:
            m.append((round(cut, 2), o))
    cfg[ep]['map'] = m
    print(ep, m)
json.dump(cfg, open(J, 'w', encoding='utf8'), ensure_ascii=False, indent=1)

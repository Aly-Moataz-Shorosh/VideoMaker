"""Map Main new.mp4 time -> raw camera time (input/20260908_103633.mp4, HLG 10-bit, no intro, no face blur).
His edit cut bits out of the raw, so the offset changes along the lecture: every 10 s of the edit, a 6 s audio chunk is located
in the raw (normalized cross-correlation around the expected offset). Writes work/sync.json [[main_t, raw_t, score], ...].
Usage: python sync.py ; then from sync import to_raw; to_raw(main_sec) -> raw_sec"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parents[2]
SR = 8000
OUT = P / 'work' / 'sync.json'


def audio(f, cache):
    c = P / 'work' / cache
    if c.exists():
        return np.load(c)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    np.save(c, a)
    return a


def locate(m, r, t, guess, span=40.0, L=6.0):
    x = m[int(t * SR):int((t + L) * SR)]
    a0 = max(0, int((t + guess - span) * SR)); a1 = min(len(r), int((t + guess + span + L) * SR))
    y = r[a0:a1]
    if len(y) < len(x) or x.std() < 1e-3:
        return None, 0
    n = 1 << int(np.ceil(np.log2(len(y) + len(x))))
    c = np.fft.irfft(np.fft.rfft(y, n) * np.conj(np.fft.rfft(x, n)), n)[:len(y) - len(x)]
    cs = np.concatenate([[0], np.cumsum(y.astype(np.float64) ** 2)])  # window energy via cumulative sum (convolve took minutes)
    e = np.sqrt(np.maximum(cs[len(x):len(x) + len(c)] - cs[:len(c)], 0)) + 1e-9
    nc = c / e / (np.linalg.norm(x) + 1e-9)
    k = int(np.argmax(nc))
    return (a0 + k) / SR, float(nc[k])


def build():
    m = audio(P / 'input' / 'Main new.mp4', 'main8k.npy')
    r = audio(P / 'input' / '20260908_103633.mp4', 'raw8k.npy')
    # first anchor: search widely (intro ~2 min is not in the raw)
    best = (None, 0, 0)
    for t in (130, 160, 200):
        rt, s = locate(m, r, t, guess=-100, span=200)
        if s > best[1]:
            best = (rt, s, t)
    guess = best[0] - best[2]
    pts = []
    t = 125.0
    while t < len(m) / SR - 8:
        rt, s = locate(m, r, t, guess)
        if rt is None or s < 0.5:
            rt2, s2 = locate(m, r, t, guess, span=200)
            if s2 > s:
                rt, s = rt2, s2
        if rt is not None and s >= 0.5:
            pts.append([round(t, 2), round(rt, 3), round(s, 3)])
            guess = rt - t
        t += 10
    json.dump(pts, open(OUT, 'w'))
    offs = [p[1] - p[0] for p in pts]
    print(len(pts), 'anchors; offset from', round(min(offs), 2), 'to', round(max(offs), 2))
    jumps = [(pts[i][0], round(offs[i] - offs[i - 1], 2)) for i in range(1, len(pts)) if abs(offs[i] - offs[i - 1]) > 0.08]
    print('offset changes (cuts in his edit):', jumps)


_pts = json.load(open(OUT)) if OUT.exists() else []


def to_raw(t):
    """main sec -> raw sec, using the nearest anchor at or before t (a cut between anchors is checked by make_short)."""
    best = None
    for p in _pts:
        if p[0] <= t + 5:
            best = p
    best = best or _pts[0]
    return t + best[1] - best[0]


if __name__ == '__main__':
    build()

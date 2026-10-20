"""Range edges from the audio WAVEFORM, never inside a word (Aly 2026-10-09: "ادي الكلام حقه متقطعش عليا… اتأكد من الـ wave form").
For every rough range [a, b] (seconds in the source):
  start = in the quiet just before the speech blob of the first word (onset - 60 ms), never inside the previous word;
  end   = after the last word's sound has really died (150 ms below the speech threshold) + 80 ms, never into the next word.
Speech threshold = local noise floor (15th percentile of 10 ms RMS over ±3 s) + 12 dB, at least -45 dB.
Usage: from edges import fit; fit(a, b) -> (start, end, report).  Run directly to check: python edges.py 797.5 799.4"""
import sys
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(P.parents[1] / 'tools'))
from transcribe import load_audio

SR, HOP = 16000, 160  # 10 ms
_a = load_audio(str(P / 'input' / 'cdkvUAgSoKc.mp4'))
_db = 20 * np.log10(np.sqrt(np.convolve(_a ** 2, np.ones(HOP) / HOP, 'same')[::HOP]) + 1e-9)  # one value per 10 ms


def thr_at(t):
    i = int(t * 100)
    loc = _db[max(0, i - 300):i + 300]
    return max(-45.0, float(np.percentile(loc, 15)) + 12)


def speech(i, th):
    return _db[i] > th


def fit(a, b, prev=None, nxt=None):
    """a = first word start, b = last word end (Whisper, rough); prev = previous word end, nxt = next word start (if any)."""
    th_a, th_b = thr_at(a), thr_at(b)
    # start: walk left from the first word's start while it is speech (Whisper starts words late), stop on quiet,
    # never further than 0.6 s nor into the previous word; no quiet at all -> deepest dip in that window
    i = int(a * 100)
    lo = int(max(a - 0.6, (prev - 0.1) if prev else 0) * 100)
    while i > lo and speech(i - 1, th_a):
        i -= 1
    if i == lo and speech(lo, th_a):
        i = lo + int(np.argmin(_db[lo:int(a * 100) + 1]))
        start = i / 100
    else:
        start = max(lo, i - 6) / 100
    # end: walk right until 150 ms in a row are quiet (+80 ms tail). Tight jump cut (no such quiet before the next
    # word) -> the deepest dip between the last word and the next one.
    j = int(b * 100); quiet = 0
    hi = int(min(b + 1.2, (nxt + 0.3) if nxt else b + 1.2) * 100)
    while j < hi and quiet < 15:
        quiet = quiet + 1 if not speech(j, th_b) else 0
        j += 1
    if quiet >= 15:
        end = min(hi, j - quiet + 8) / 100
    else:
        k0 = int((b - 0.05) * 100)
        end = (k0 + int(np.argmin(_db[k0:hi]))) / 100
    rep = f'[{a:.2f}->{start:.2f} {_db[int(start * 100)]:.0f}dB | {b:.2f}->{end:.2f} {_db[int(end * 100)]:.0f}dB thr {th_b:.0f}{" DIP" if quiet < 15 else ""}]'
    return round(start, 2), round(end, 2), rep


def profile(t0, t1):
    return ' '.join(f'{t / 100:.2f}:{_db[t]:.0f}' for t in range(int(t0 * 100), int(t1 * 100), 2))


if __name__ == '__main__':
    a, b = float(sys.argv[1]), float(sys.argv[2])
    print(fit(a, b)[2]); print(profile(b - 0.3, b + 1.0))

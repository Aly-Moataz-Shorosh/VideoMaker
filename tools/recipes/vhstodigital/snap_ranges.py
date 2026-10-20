"""Snap each short's rough ranges onto real audio dips (50 ms RMS) -> work/ranges.json. Prints edge loudness."""
import json, sys, glob
from pathlib import Path
import numpy as np
W = Path(__file__).resolve().parents[1]; P = W.parent
sys.path.insert(0, str(P.parents[1] / 'tools'))
from transcribe import load_audio
sys.stdout.reconfigure(encoding='utf-8')
ROUGH = {
    1: [[797.5, 799.35], [836.0, 840.8], [94.35, 116.7], [485.65, 497.7], [542.15, 559.3], [584.35, 596.0], [686.85, 692.65], [775.45, 781.1]],
    2: [[805.35, 809.4], [25.05, 36.5], [811.9, 818.15], [41.2, 43.5], [702.8, 708.2]],
    4: [[148.85, 153.2], [153.45, 163.9], [329.3, 337.6], [351.5, 354.6], [478.2, 485.65], [584.35, 596.0], [686.85, 692.65], [761.3, 769.4]],
    8: [[1.4, 21.2], [75.7, 81.05], [138.05, 142.3], [790.0, 794.45], [901.35, 903.6]],
}
video = str(P / 'input' / 'vSaO0bRnfz8.mp4')
a = load_audio(video); SR = 16000; HOP = 800
rms = np.sqrt(np.convolve(a ** 2, np.ones(HOP) / HOP, 'same'))
def snap(t, win=0.2):
    i0, i1 = int((t - win) * SR), int((t + win) * SR)
    seg = rms[i0:i1:80]; k = int(np.argmin(seg)); nt = i0 / SR + k * 80 / SR
    return round(nt, 2), round(20 * np.log10(seg[k] + 1e-9), 1)
out = {}
for n, rs in ROUGH.items():
    out[n] = []
    for x, y in rs:
        (sx, dx), (sy, dy) = snap(x), snap(y)
        out[n].append([sx, sy]); print(n, f'{x}->{sx} ({dx} dB)  {y}->{sy} ({dy} dB)')
    print('  len', round(sum(b - a for a, b in out[n]), 1))
json.dump(out, open(W / 'ranges.json', 'w'), indent=1)

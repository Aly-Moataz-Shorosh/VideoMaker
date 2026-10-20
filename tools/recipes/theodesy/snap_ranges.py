"""Snap each short's rough ranges onto real audio dips (50 ms RMS) -> work/ranges.json. Prints edge loudness."""
import json, sys, glob
from pathlib import Path
import numpy as np
W = Path(__file__).resolve().parents[1]; P = W.parent
sys.path.insert(0, str(P.parents[1] / 'tools'))
from transcribe import load_audio
sys.stdout.reconfigure(encoding='utf-8')
ROUGH = {
    1: [[46.6, 56.85], [555.05, 580.6], [587.3, 622.25]],
    2: [[81.1, 126.65]],
    3: [[126.75, 186.75]],
    4: [[187.4, 256.3]],
    5: [[256.4, 327.75], [333.4, 341.75]],
    6: [[341.8, 389.85]],
    7: [[389.85, 459.95]],
    8: [[460.2, 546.25], [550.6, 553.45]],
    9: [[623.3, 699.5]],
    10: [[716.5, 789.95]],
}
video = glob.glob(str(P / 'input' / '*Odesy' / 'final.mp4'))[0]
a = load_audio(video); SR = 16000; HOP = 800
rms = np.sqrt(np.convolve(a ** 2, np.ones(HOP) / HOP, 'same'))
def snap(t, win=0.35):
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

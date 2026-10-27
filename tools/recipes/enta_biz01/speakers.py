"""Who speaks each word: voice clusters (MFCC + pitch, GMM 2 clusters on 0.5 s windows; voiceclust.npz) -> word labels
A (Aly, left, higher pitch ~186 Hz) / G (guest, right, ~147 Hz), smoothed. Writes work/speakers.json:
{"words": [[start, end, word, "A"|"G"], ...], "turns": [[start, end, "A"|"G"], ...]}"""
import json, numpy as np
from pathlib import Path
W = Path(__file__).resolve().parents[1]
z = np.load(W / 'voiceclust.npz'); T, lab = z['T'], z['lab']
f0 = z['X'][:, -1] * 50
aly = 1 if np.median(f0[lab == 1]) > np.median(f0[lab == 0]) else 0
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
words = [w for s in tr['sentences'] for w in s['words'] if w["start"] >= 17.2 and w["start"] < 2685.9]
out = []
for w in words:
    m = (T + 0.5 > w['start']) & (T < w['end'])
    if not m.any(): m = np.abs(T + 0.25 - (w['start'] + w['end']) / 2) < 0.75
    v = (lab[m] == aly).mean() if m.any() else 0.5
    out.append([w['start'], w['end'], w['w'], v])
# smooth: average with neighbours (3 words each side), then threshold
v = np.array([o[3] for o in out]); vs = np.convolve(np.pad(v, 2, mode='edge'), np.ones(5) / 5, 'valid')
for o, x in zip(out, vs): o[3] = 'A' if x > 0.5 else 'G'
turns = []
for s, e, w, sp in out:
    if turns and turns[-1][2] == sp and s - turns[-1][1] < 1.2: turns[-1][1] = e
    else: turns.append([s, e, sp])
json.dump({'words': out, 'turns': turns}, open(W / 'speakers.json', 'w', encoding='utf8'), ensure_ascii=False)
print(len(turns), 'turns; A words', sum(o[3] == 'A' for o in out), 'G words', sum(o[3] == 'G' for o in out))

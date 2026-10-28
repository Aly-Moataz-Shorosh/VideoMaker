"""Lip-sync + length QC for the delivered shorts: audio of every piece vs the source (offset must stay ~0 and constant),
and the short's length vs its timeline.   python qc_sync.py 1 2 ..."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parents[2]
SRC = P / 'input' / '2026-10-27 16-06-01.mp4'


def aud(src, ss, t):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{ss:.3f}', '-t', f'{t:.3f}', '-i', str(src), '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.int16).astype(np.float32)


BAD = False
for n in map(int, sys.argv[1:]):
    tl = json.load(open(P / 'work' / 'shorts' / f'tl_{n:02d}.json'))
    vid = next((P / 'output' / 'shorts').glob(f'{n:02d}_*.mp4'))
    offs = []
    for s in tl['segs']:
        if s['b'] - s['a'] < 3:
            continue
        for k in (0.5, s['b'] - s['a'] - 2.5):
            o = aud(vid, s['st'] + k, 2.0); r = aud(SRC, s['a'] + k - 0.5, 3.0)
            offs.append(int(np.argmax(np.correlate(r, o, 'valid'))) / 8000 - 0.5)
    L = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(vid)]))
    bad = max(abs(x) for x in offs) > 0.06 or abs(L - tl['dur']) > 0.15
    if bad:
        BAD = True
    print(f'short {n}: drift ' + ' '.join(f'{x:+.2f}' for x in offs) + f' | len {L:.2f}/{tl["dur"]:.2f}' + (' <-- CHECK' if bad else ' ok'), flush=True)
sys.exit(1 if BAD else 0)

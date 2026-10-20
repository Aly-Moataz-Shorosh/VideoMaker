"""Lip-sync QC: for every piece of short N, where is its audio relative to the raw camera time? (should stay ~0)
python qc_sync.py 1 2 ...  -> max drift per short"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
P = Path(__file__).resolve().parents[2]
def aud(src, ss, t):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{ss:.3f}', '-t', f'{t:.3f}', '-i', str(src), '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.int16).astype(np.float32)
for n in map(int, sys.argv[1:]):
    tl = json.load(open(P / 'work' / 'shorts' / f'tl_{n:02d}.json'))
    vid = next((P / 'output' / 'v3').glob(f'{n:02d}_*.mp4'))
    offs = []
    for s in tl['segs']:
        if s['kind'] != 'seg' or s['b'] - s['a'] < 3: continue
        o = aud(vid, s['st'] + 0.5, 2.0); r = aud(P / 'input' / '20260908_103633.mp4', s['a'] - 88.01, 3.0)
        offs.append(int(np.argmax(np.correlate(r, o, 'valid'))) / 8000 - 0.5)
    print(f'short {n}: drift ' + ' '.join(f'{x:+.2f}' for x in offs), flush=True)

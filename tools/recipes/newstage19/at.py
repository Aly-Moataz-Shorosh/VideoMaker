"""Where is second S of short N?  python at.py N S [S2 ...]  (S = 33 or 1:07)
Prints the piece, the source second in Main new.mp4 (+ raw second), the words around it and the cue on screen."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P = Path(__file__).resolve().parents[2]
n = int(sys.argv[1])
tl = json.load(open(P / 'work' / 'shorts' / f'tl_{n:02d}.json'))
pr = json.load(open(P / 'work' / 'shorts' / f'props_{n:02d}.json', encoding='utf8'))
for a in sys.argv[2:]:
    t = sum(float(x) * 60 ** i for i, x in enumerate(reversed(a.split(':'))))
    seg = next((s for s in tl['segs'] if s['st'] <= t < s['st'] + (s.get('d') or (s['b'] - s['a']))), None)
    if seg and seg['kind'] == 'seg':
        src = seg['a'] + t - seg['st']
        where = f"piece {seg['a']:.2f}-{seg['b']:.2f} -> src {src:.2f} (raw {src - 88.01:.2f})"
    else:
        where = f"{seg['kind'] if seg else 'end'}"
    words = ' '.join(w['w'] for w in pr['words'] if t - 1.5 <= w['start'] <= t + 1.5)
    cue = [f"{c['k']}@{c['t']}" for c in pr['cues'] if c['t'] <= t < c['t'] + c['d']]
    print(f'{a}: {where} | cue {cue} | {words}')

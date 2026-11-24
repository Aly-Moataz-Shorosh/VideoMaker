"""Snap every short's pieces to Whisper word edges (v11 time) and print the text, so each piece starts/ends on whole words.
Writes work/shorts/cuts.json = [{n, slug, pieces:[[a,b],...], text:[...]}]."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shorts_data import SHORTS
W = sorted(json.load(open('words_v11_real.json', encoding='utf-8')), key=lambda w: w['a'])
PAD_A, PAD_B = 0.10, 0.18
def snap(a, b):
    ws = [w for w in W if w['a'] >= a - 0.25 and w['b'] <= b + 0.25]
    if not ws: return a, b, ''
    A = max(ws[0]['a'] - PAD_A, (max([w['b'] for w in W if w['b'] <= ws[0]['a']] or [0])) + 0.02)
    nxt = [w['a'] for w in W if w['a'] >= ws[-1]['b']]
    B = min(ws[-1]['b'] + PAD_B, (nxt[0] - 0.02) if nxt else 1e9)
    return round(A, 3), round(B, 3), ' '.join(w['w'] for w in ws)
out = []
for s in SHORTS:
    ps, tx = [], []
    for pc in s['pieces']:
        a, b = pc[0], pc[1]
        A, B, t = snap(a, b)
        if len(pc) > 2 and pc[2] == 'raw': A, B = (A if t and A > a - 0.3 else a), b   # keep holds / music / results whole
        ps.append([A, B]); tx.append(t)
    tot = sum(b - a for a, b in ps)
    out.append(dict(n=s['n'], slug=s['slug'], pieces=ps, text=tx, dur=round(tot, 2)))
    print(f"\n#{s['n']} {s['slug']} {tot:.1f}s")
    for (A, B), t in zip(ps, tx): print(f"  [{A:8.2f}-{B:8.2f}] {t}")
os.makedirs('shorts', exist_ok=True)
json.dump(out, open('shorts/cuts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

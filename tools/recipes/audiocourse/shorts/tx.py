# Session transcript in a range, one line per sentence with start seconds:  python tx.py 0 330
import json, sys
a, b = float(sys.argv[1]), float(sys.argv[2])
from pathlib import Path
t = json.load(open(Path(__file__).resolve().parents[1] / 'transcript.json', encoding='utf-8'))
for s in t['sentences']:
    ws = [w for w in s['words'] if a <= w['start'] < b]
    if ws: print(f"{ws[0]['start']:.1f}-{ws[-1]['end']:.1f} " + ' '.join(w['w'] for w in ws))

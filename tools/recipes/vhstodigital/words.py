"""Print words with times: python work/scripts/words.py S001 S002-S010"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
W = Path(__file__).resolve().parents[1]
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
ids = set()
for a in sys.argv[1:]:
    x, _, y = a.partition('-'); y = y or x
    ids |= {f'S{i:03d}' for i in range(int(x[1:]), int(y[1:]) + 1)}
for s in tr['sentences']:
    if s['id'] in ids:
        print(s['id'], ' '.join(f"{w['w']}|{w['start']:.2f}" for w in s['words']))

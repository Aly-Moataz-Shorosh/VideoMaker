# Word times around given seconds:  python wt.py 16 2060 ...  (prints the words within ±3 s)
import json, sys
from pathlib import Path
t = json.load(open(Path(__file__).resolve().parents[1] / 'transcript.json', encoding='utf-8'))
W = [(w['start'], w['end'], w['w']) for s in t['sentences'] for w in s['words']]
for x in map(float, sys.argv[1:]):
    print(f'@{x}: ' + ' '.join(f'{a:.2f}:{w}' for a, b, w in W if x - 3 <= a <= x + 3))

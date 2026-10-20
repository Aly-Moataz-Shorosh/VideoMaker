"""Print transcript words with times in a source range: python words.py <a_sec|m:ss> <b_sec|m:ss>"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
def sec(x): return sum(float(p) * 60 ** i for i, p in enumerate(reversed(x.split(':'))))
a, b = sec(sys.argv[1]), sec(sys.argv[2])
d = json.load(open(Path(__file__).parent.parent / 'transcript.json', encoding='utf8'))
line = []
for s in d['sentences']:
    for w in s['words']:
        if a <= w['start'] <= b:
            line.append(f"{w['w']}[{w['start']:.1f}]")
print(' '.join(line))

"""Words with times + speaker in a source range: python words.py <a> <b> [a b ...]"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open(Path(__file__).parent.parent / 'speakers.json', encoding='utf8'))['words']
args = [float(x) for x in sys.argv[1:]]
for a, b in zip(args[::2], args[1::2]):
    out, sp = [], None
    for s, e, w, k in d:
        if a <= s <= b:
            if k != sp: out.append(f'\n[{k}]'); sp = k
            out.append(f'{w}[{s:.1f}]')
    print(f'--- {a}-{b}', ' '.join(out))

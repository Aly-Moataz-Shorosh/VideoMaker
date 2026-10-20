# Dump the timed sentences of chapters (for writing shorts): python chapter_text.py out.txt 35 31 ...
import json, sys
from pathlib import Path
W = Path(__file__).resolve().parents[1]
ch = [c for c in json.load(open(W / 'chapters.json', encoding='utf-8')) if 'ep' in c]
out = []
for n in map(int, sys.argv[2:]):
    i = [c['n'] for c in ch].index(n); c = ch[i]
    nx = ch[i + 1] if i + 1 < len(ch) else None
    end = nx['src'] if nx and nx['ep'] == c['ep'] else 1e9
    out.append(f"===== ch {n} {c['ar']} ep{c['ep']} {c['src']} {end}")
    for s in json.load(open(W / f"ep{c['ep']}/transcript.json", encoding='utf-8'))['sentences']:
        if c['src'] - 1 <= s['start'] < end: out.append(f"{s['id']} {s['start']:.1f}-{s['end']:.1f} {s['text']}")
open(sys.argv[1], 'w', encoding='utf-8').write('\n'.join(out))

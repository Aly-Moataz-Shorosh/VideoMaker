"""Which parts of the episode changed between the rendered edit and the new one (Aly 2026-10-28: "متعيدش الفيديو كله… عيد بس الموشن
للحتت دي و بعدين جمع الفيديو"). Diff of the cues (everything but sfx: sound is re-mixed whole, his voice untouched), a changed
'shot' counts until the next shot, + boards whose title holds Latin letters / digits / a leading-trailing "…" (the RTL title fix)
and photo collages with captions (captions now above all photos). Output: work/redo_parts.json = [[from_frame, to_frame], ...].
Usage: python -X utf8 redo_parts.py <old edit json> <new edit json>"""
import json, re, sys
from pathlib import Path

old, new = (json.load(open(a, encoding='utf8')) for a in sys.argv[1:3])
FPS = new['fps']
TOTAL = round(new['duration'] * FPS)


def key(c):  # props that only got a new name for the same look are dropped (term defAt 9 = the old fixed 0.3 s)
    c = dict(c, props={k: v for k, v in c['props'].items() if not (k == 'defAt' and v == 9)})
    return json.dumps(c, sort_keys=True, ensure_ascii=False)


def spans(ed, keys):
    out = []
    shots = sorted([c for c in ed['cues'] if c['t'] == 'shot'], key=lambda c: c['at'])
    for i, c in enumerate(shots):
        if key(c) in keys:
            nxt = shots[i + 1]['at'] if i + 1 < len(shots) else c['at'] + c['dur']
            out.append((c['at'] - 0.2, max(c['at'] + c['dur'], nxt) + 0.8))   # + the blend into the next shot
    for c in ed['cues']:
        if c['t'] in ('sfx', 'shot') or key(c) not in keys: continue
        out.append((c['at'] - 0.3, c['at'] + c['dur'] + 0.3))
    return out


ko = {key(c) for c in old['cues']}
kn = {key(c) for c in new['cues']}
rng = spans(old, ko - kn) + spans(new, kn - ko)
for c in new['cues']:
    tt = c['props'].get('title', '')   # only MIXED titles changed with RTL (pure English or pure Arabic look the same)
    if c['t'] == 'biz_free' and ((re.search(r'[A-Za-z0-9]', tt) and re.search(r'[؀-ۿ]', tt)) or re.search(r'^\*?…|…\*?$', tt)):
        rng.append((c['at'] - 0.3, c['at'] + c['dur'] + 0.3))
    if c['t'] == 'enta_photos' and len(c['props']['items']) > 1 and any(it.get('caption') for it in c['props']['items']):
        rng.append((c['at'] - 0.3, c['at'] + c['dur'] + 0.3))
fr = sorted((max(0, round(a * FPS)), min(TOTAL - 1, round(b * FPS))) for a, b in rng)
merged = []
for a, b in fr:
    if merged and a <= merged[-1][1] + 3 * FPS: merged[-1][1] = max(merged[-1][1], b)   # gaps < 3 s: render through
    else: merged.append([a, b])
tot = sum(b - a + 1 for a, b in merged)
out = Path(sys.argv[2]).parents[3] / 'projects' / 'انت بتشتغل ايه' / '2026-10-27 ep01 biz karim tamer' / 'work' / 'redo_parts.json' if len(sys.argv) < 4 else Path(sys.argv[3])
json.dump(merged, open(out, 'w'), indent=0)
print(len(merged), 'parts,', round(tot / FPS / 60, 1), 'min of', round(TOTAL / FPS / 60, 1), '->', out)
for a, b in merged: print(f'  {int(a / FPS // 60)}:{a / FPS % 60:04.1f} - {int(b / FPS // 60)}:{b / FPS % 60:04.1f}  ({(b - a) / FPS:.1f} s)')

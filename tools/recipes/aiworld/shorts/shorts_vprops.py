"""NATIVE VERTICAL props for comp ai-world-vshort (Aly 2026-11-24: «مش عايز إطار horizontal جوه الـ vertical… عيد التنسيق»).
Every board of v11 is RE-LAID OUT on a 1080x1920 stage (no crop, no 16:9 frame inside the 9:16):
- a horizontal flow (right -> left) becomes a vertical flow (top -> bottom); rows become columns (first row = right column);
  arrows (edge pts) move with their cards;
- bar charts stay bars: squeezed into the width instead;
- boards narrow enough are only re-centred;
- then the GENERAL OVERLAP LAW resolver (v11_resolve.resolve_all) runs with the vertical content zone, + a final count that must be 0.
Pieces that touch a tree separator (SEP) are trimmed before it. Talking circles live in the title band (Short component).
Full-frame generated clips use their 9:16 regeneration from vertical_clips.json when it exists (else a placeholder crop, flagged).
Run from work/:  python scripts/shorts_vprops.py [N ...]   -> shorts/vprops_NN.json"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shorts_data import SHORTS
import v11_resolve
from v5_boxes import inter

FPS = 25
ZONE = (70, 380, 1010, 1400)          # content zone on the 1080x1920 stage (title band above, captions below)
v11_resolve.SAFE = (60, 370, 1020, 1410)
P = json.load(open('props_v11.json', encoding='utf-8'))
CUTS = {c['n']: c for c in json.load(open('shorts/cuts.json', encoding='utf-8'))}
W = sorted(json.load(open('words_v11_real.json', encoding='utf-8')), key=lambda w: w['a'])
VCLIPS = json.load(open('shorts/vertical_clips.json', encoding='utf-8')) if os.path.exists('shorts/vertical_clips.json') else {}
SKIPK = {'titleAt', 'line', 'brand', 'subscribe', 'sep', 'edge', 'split', 'diff', 'page', 'circle', 'puppet'}
SEPS = sorted(s['start'] for s in P['scenes'] if s['k'] == 'SEP')

def trim_seps(pieces):
    out = []
    for a, b in pieces:
        for s in P['scenes']:
            if s['k'] == 'SEP' and a < s['start'] < b: b = s['start'] - 0.04
            if s['k'] == 'SEP' and s['start'] <= a < s['start'] + s['dur']: a = s['start'] + s['dur']
        if b - a > 0.4: out.append((a, b))
    return out

def item_boxes(s):
    end = int(s['dur'] * FPS); bs = []
    for d in s['items']:
        if d.get('k') in SKIPK or d.get('x') is None: continue
        try: b = v11_resolve._bx(d, end)
        except Exception: b = None
        if b: bs.append(b)
    return bs

GAPX, GAPY = 30, 58
BIG = 2.2
def _bb(items, end):
    bs = [v11_resolve._bx(d, end) for d in items]
    bs = [b for b in bs if b]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)) if bs else None

def _shift(items, dx, dy):
    for d in items:
        d['x'] = round(d['x'] + dx)
        if d.get('k') == 'bar': d['base'] = round(d['base'] + dy)
        elif d.get('y') is not None: d['y'] = round(d['y'] + dy)

def _shrink(items, k):
    pos = [d for d in items if d.get('x') is not None and d.get('y') is not None]
    if len(pos) > 1:   # a group (grid) grows/shrinks as ONE picture: the distances between its cards scale too
        mx = sum(d['x'] for d in pos) / len(pos); my = sum(d['y'] for d in pos) / len(pos)
        for d in pos: d['x'] = round(mx + (d['x'] - mx) * k); d['y'] = round(my + (d['y'] - my) * k)
    bars = [d for d in items if d.get('k') == 'bar']
    if len(bars) > 1:   # bar charts: the bars come closer / spread too, and the bars get shorter / taller
        mx = sum(d['x'] for d in bars) / len(bars)
        for d in bars: d['x'] = round(mx + (d['x'] - mx) * k); d['h'] = round(d.get('h', 300) * k)
    for d in items:
        if d.get('k') == 'node':
            if d.get('w'): d['w'] = round(d['w'] * k)
            if d.get('s'): d['s'] = round(d['s'] * k)
            d['size'] = round(d.get('size', 30) * k, 1)
        elif d.get('k') in ('typed', 'wave', 'scan'):
            if d.get('w'): d['w'] = round(d['w'] * k)
            if d.get('k') == 'typed': d['size'] = round(d.get('size', 24) * k, 1)
        else: d['scale'] = round(d.get('scale', 0.8) * k, 3)

def relayout(s):
    """VERTICAL PACKER: blocks (an item, a grid, a bar chart) in speaking order -> rows (side by side only when they were side by side
    AND entered together AND fit) -> each row goes to the first free vertical gap among the rows still on screen; if nothing is free,
    the oldest rows leave just before (a hand-over). Arrows are redrawn between the new boxes. No overlap by construction."""
    end = int(s['dur'] * FPS)
    its = [d for d in s['items'] if d.get('k') not in SKIPK and d.get('x') is not None and ('y' in d or d.get('k') == 'bar')]
    if not its: return 'empty'
    for d in its: d.setdefault('at', 0)
    groups = {}
    for d in its:
        key = ('grid', d['grid']) if d.get('grid') else ('bars',) if d.get('k') == 'bar' else ('one', id(d))
        groups.setdefault(key, []).append(d)
    blocks = []
    Wz = ZONE[2] - ZONE[0]
    for g in groups.values():
        bb = _bb(g, end)
        if not bb: continue
        grow = min(BIG, Wz * 0.92 / max(1, bb[2] - bb[0]), (ZONE[3] - ZONE[1]) * 0.55 / max(1, bb[3] - bb[1]))
        if grow > 1.05: _shrink(g, grow); bb = _bb(g, end)   # phone size: cards made for 1920 are enlarged for the 1080-wide frame
        for _ in range(3):
            if bb[2] - bb[0] <= Wz: break
            _shrink(g, Wz / (bb[2] - bb[0]) * 0.97); bb = _bb(g, end)
        blocks.append(dict(items=g, box=bb, orig=bb, at=min(d['at'] for d in g), out=max(min(d.get('out', end), end) for d in g)))
    blocks.sort(key=lambda b: b['at'])
    rows = []
    for b in blocks:
        w = b['box'][2] - b['box'][0]
        r = rows[-1] if rows else None
        together = r and len(r['bl']) < 3 and b['at'] - r['at'] <= 25          # entered (almost) together -> share a row
        side = r and len(r['bl']) < 3 and abs((b['orig'][1] + b['orig'][3]) / 2 - r['cy']) < 70 and b['at'] - r['at'] <= 50             and abs(b['orig'][0] - r['bl'][-1]['orig'][0]) > 60
        if (together or side) and r['w'] + GAPX + w > Wz:
            k = (Wz - GAPX * len(r['bl'])) / (r['w'] - GAPX * (len(r['bl']) - 1) + w)
            if k >= 0.5:
                for q in r['bl'] + [b]:
                    _shrink(q['items'], k); q['box'] = _bb(q['items'], end)
                w = b['box'][2] - b['box'][0]
                r['w'] = sum(q['box'][2] - q['box'][0] for q in r['bl']) + GAPX * (len(r['bl']) - 1)
                r['h'] = max(q['box'][3] - q['box'][1] for q in r['bl'])
        if (together or side) and r['w'] + GAPX + w <= Wz + 1:
            r['bl'].append(b); r['w'] += GAPX + w; r['h'] = max(r['h'], b['box'][3] - b['box'][1]); r['out'] = max(r['out'], b['out'])
        else:
            rows.append(dict(bl=[b], w=w, h=b['box'][3] - b['box'][1], at=b['at'], out=b['out'], cy=(b['orig'][1] + b['orig'][3]) / 2))
    placed = []
    for r in rows:
        r['bl'].sort(key=lambda b: -b['orig'][0])   # reading order inside a row: originally right first
        while True:
            vis = sorted([q for q in placed if q['out'] > r['at'] + 8], key=lambda q: q['y'])
            y, ok = ZONE[1], False
            for cy_ in sorted([ZONE[1]] + [q['y'] + q['h'] + GAPY for q in vis]):
                if cy_ + r['h'] > ZONE[3]: continue
                if all(cy_ + r['h'] + GAPY <= q['y'] or cy_ >= q['y'] + q['h'] + GAPY for q in vis): y, ok = cy_, True; break
            if ok or not vis: break
            old = min(vis, key=lambda q: q['at'])   # hand-over: the oldest row leaves just before this one enters
            if old['at'] + 12 > r['at'] - 2:   # entered together: nothing can leave -> make this row smaller, else give up (counted)
                tries = r.get('tries', 0)
                if tries >= 3:   # last resort: the old row leaves anyway (a fast hand-over beats an overlap)
                    old['out'] = max(old['at'] + 1, r['at'] - 2)
                    for b in old['bl']:
                        b['out'] = min(b['out'], old['out'])
                        for d in b['items']: d['out'] = min(d.get('out', end), old['out'])
                    continue
                r['tries'] = tries + 1
                for b in r['bl']:
                    _shrink(b['items'], 0.82); b['box'] = _bb(b['items'], end)
                r['h'] = max(b['box'][3] - b['box'][1] for b in r['bl']); r['w'] = sum(b['box'][2] - b['box'][0] for b in r['bl']) + GAPX * (len(r['bl']) - 1)
                continue
            old['out'] = max(old['at'] + 12, r['at'] - 2)
            for b in old['bl']:
                b['out'] = min(b['out'], old['out'])
                for d in b['items']: d['out'] = min(d.get('out', end), old['out'])
        r['y'] = y
        x = (ZONE[0] + ZONE[2]) / 2 + r['w'] / 2
        for b in r['bl']:
            bw, bh = b['box'][2] - b['box'][0], b['box'][3] - b['box'][1]
            nx0, ny0 = x - bw, y + (r['h'] - bh) / 2
            _shift(b['items'], nx0 - b['box'][0], ny0 - b['box'][1])
            b['box'] = (nx0, ny0, nx0 + bw, ny0 + bh); x -= bw + GAPX
        placed.append(r)
    top = min(r['y'] for r in placed); bot = max(r['y'] + r['h'] for r in placed)
    dy = max(0, ((ZONE[1] + ZONE[3]) / 2) - (top + bot) / 2)
    for r in placed:
        r['y'] += dy
        for b in r['bl']:
            _shift(b['items'], 0, dy); b['box'] = (b['box'][0], b['box'][1] + dy, b['box'][2], b['box'][3] + dy)
    # safety net (overlap law): any two cards still on screen together and touching -> the earlier one leaves before the later enters
    flat = sorted([d for b in [b for r in placed for b in r['bl']] for d in b['items']], key=lambda d: d['at'])
    for i, a in enumerate(flat):
        ba = v11_resolve._bx(a, end)
        for c in flat[i + 1:]:
            bc = v11_resolve._bx(c, end)
            if ba and bc and min(a.get('out', end), c.get('out', end)) - max(a['at'], c['at']) >= 8 and v11_resolve._hit(ba, bc):
                a['out'] = max(a['at'] + 1, c['at'] - 2)
    for r in placed:
        for b in r['bl']: b['out'] = max(min(d.get('out', end), end) for d in b['items'])
    allb = [b for r in placed for b in r['bl']]
    rowof = {id(b): r for r in placed for b in r['bl']}
    def near(x, y):
        def dist(b):
            o = b['orig']; dx = max(o[0] - x, 0, x - o[2]); dy2 = max(o[1] - y, 0, y - o[3]); return dx * dx + dy2 * dy2
        return min(allb, key=dist)
    keep = []
    for d in s['items']:
        if d.get('k') != 'edge' or not d.get('pts'): keep.append(d); continue
        p = d['pts']; A, B = near(p[0], p[1]), near(p[2], p[3])
        if A is B: continue
        a, b = A['box'], B['box']
        if rowof[id(A)] is rowof[id(B)]:
            ym = (a[1] + a[3]) / 2
            d['pts'] = [round(a[0] - 6), round(ym), round(b[2] + 6), round(ym)] if a[0] > b[0] else [round(a[2] + 6), round(ym), round(b[0] - 6), round(ym)]
        elif a[1] < b[1]: d['pts'] = [round((a[0] + a[2]) / 2), round(a[3] + 6), round((b[0] + b[2]) / 2), round(b[1] - 6)]
        else: d['pts'] = [round((a[0] + a[2]) / 2), round(a[1] - 6), round((b[0] + b[2]) / 2), round(b[3] + 6)]
        d['bend'] = 0
        d['out'] = min(d.get('out', end), A['out'], B['out'])
        keep.append(d)
    s['items'] = keep
    return 'packed'

def overlaps(s):
    end = int(s['dur'] * FPS); n = 0
    its = [d for d in s['items'] if d.get('k') not in SKIPK and d.get('x') is not None and 'at' in d]
    for i, a in enumerate(its):
        ba = v11_resolve._bx(a, end)
        if not ba: continue
        for b in its[i + 1:]:
            bb = v11_resolve._bx(b, end)
            if not bb: continue
            t = min(a.get('out', end), b.get('out', end)) - max(a['at'], b['at'])
            if t >= 8 and v11_resolve._hit(ba, bb): n += 1
    return n

def build(sd):
    raw = CUTS[sd['n']]['pieces']
    pcs = trim_seps(raw)
    pieces, o = [], 0.0
    for a, b in pcs: pieces.append(dict(a=round(a, 3), b=round(b, 3), o=round(o, 3))); o += b - a
    dur = o
    scenes = [copy.deepcopy(s) for s in P['scenes'] if any(s['start'] < pc['b'] and s['start'] + s['dur'] > pc['a'] for pc in pieces)]
    modes, flagged = [], []
    for s in scenes:
        s['title'] = None
        if s['k'] in ('BOARD', 'AV', 'CLIP', 'WEB'): modes.append(relayout(s))
        for c in s.get('clips', []):
            if c['src'] in VCLIPS: c['src'] = VCLIPS[c['src']]; c['vertical'] = True
            elif s['k'] in ('AV', 'CLIP', 'LYR'): flagged.append(c['src'].split('/')[-1])
    left = []
    nov = sum(overlaps(s) for s in scenes)
    end = None
    if sd.get('endcard'):
        end = {'from': round(dur, 2), 'thumb': 'projects/aiworld/shorts/thumb_v11.jpg', 'line1': 'الفيديو الكامل على قناتي', 'line2': 'عالم الـ AI كله في فيديو واحد'}
        dur += 4.5
    words = []
    lyr = [s for s in P['scenes'] if s['k'] == 'LYR'][0]
    for pc in pieces:
        if lyr['start'] <= pc['a'] < lyr['start'] + lyr['dur']:
            lw = sorted(lyr['words'], key=lambda w: w['t'])
            for i, w in enumerate(lw):
                if pc['a'] <= w['t'] < pc['b']:
                    b = min(lw[i + 1]['t'] if i + 1 < len(lw) else w['t'] + 0.5, w['t'] + 0.9)
                    words.append(dict(a=round(pc['o'] + w['t'] - pc['a'], 3), b=round(pc['o'] + b - pc['a'], 3), w=w['w']))
            continue
        for w in W:
            if w['a'] >= pc['a'] - 0.05 and w['b'] <= pc['b'] + 0.1:
                words.append(dict(a=round(pc['o'] + w['a'] - pc['a'], 3), b=round(pc['o'] + w['b'] - pc['a'], 3), w=w['w']))
    faces = [f for f in P['faces'] if f.get('circle') and any(f['from'] < pc['b'] and f['from'] + f['dur'] > pc['a'] for pc in pieces)]
    props = dict(fps=FPS, duration=round(dur, 3), scenes=scenes, faces=faces, pieces=pieces, title=sd['title'], hook=sd.get('hook_text', ''),
                 cta=sd.get('cta', ''), ctaFrom=round((end['from'] if end else dur) - 3.0, 2), words=words, series=sd.get('series', ''))
    if end: props['end'] = end
    return props, modes, left, nov, flagged

if __name__ == '__main__':
    want = [int(x) for x in sys.argv[1:]] or [s['n'] for s in SHORTS]
    for sd in SHORTS:
        if sd['n'] not in want: continue
        p, modes, left, nov, flagged = build(sd)
        json.dump(p, open(f"shorts/vprops_{sd['n']:02d}.json", 'w', encoding='utf-8'), ensure_ascii=False)
        from collections import Counter
        print(f"#{sd['n']:02d} {sd['slug']}: {p['duration']:.1f}s layouts {dict(Counter(modes))} | unresolved {len(left)} | overlaps {nov} | crop-placeholders {len(set(flagged))}")

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
# Aly «حاول تبسطها»: long board lines are rewritten SHORT for the phone (big line + small line under it)
SIMPLE = {
 'استخدمت 444 كريدت من 600 في HeyGen ـ اشتراك Creator بـ 29$ في الشهر': ('444 كريدت من 600', 'اشتراك Creator ـ 29$ في الشهر'),
 'استخدمت حوالي 1088 كريدت في Higgsfield ـ اشتراك Ultra': ('حوالي 1088 كريدت', 'اشتراك Ultra'),
 'استخدمت 9197 حرف في ElevenLabs ـ اشتراك Starter بـ 6$ في الشهر': ('9197 حرف', 'اشتراك Starter ـ 6$ في الشهر'),
 'استخدمت 40 كريدت في Suno = 8 نسخ للأغنية ـ اشتراك Pro بـ 10$ في الشهر': ('40 كريدت = 8 نسخ للأغنية', 'اشتراك Pro ـ 10$ في الشهر'),
 'الاشتراك الشهري في Claude ـ الخطط بتبدأ من 20$': ('اشتراك شهري', 'الخطط من 20$'),
 'كله جوه الاشتراكات الشهرية.. ومفيش ولا دولار زيادة': ('كله جوه الاشتراكات.. ولا دولار زيادة', None),
 'ببلاش على جهازك: Whisper · Blender · Remotion · HyperFrames · ffmpeg · ComfyUI': ('ببلاش على جهازك', 'Whisper · Blender · Remotion · ffmpeg · ComfyUI'),
 'Higgsfield: بالكريدت حسب الخطة': ('Higgsfield', 'بالكريدت حسب الخطة'),
}
SEPS = sorted(s['start'] for s in P['scenes'] if s['k'] == 'SEP')

def _bxv(d, end):
    """v11 box + the real place of a text card WITH a sub line: Node centres the whole column (pill + sub) on y"""
    if d.get('k') == 'node' and d.get('label') and d.get('sub') and not d.get('src') and not d.get('logo') and d.get('y') is not None:
        sz = d.get('size', 30); ph = 1.55 * sz + 22; sh = sz * 0.72 * 1.5 + 6; tot = ph + sh
        w = max(len(str(d['label'])) * sz * 0.6 + 48, len(str(d['sub'])) * sz * 0.72 * 0.6 + 20)
        return (d['x'] - w / 2, d['y'] - tot / 2 - 4, d['x'] + w / 2, d['y'] + tot / 2 + 4)
    return v11_resolve._bx(d, end)

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
        try: b = _bxv(d, end)
        except Exception: b = None
        if b: bs.append(b)
    return bs

GAPX, GAPY = 30, 58
BIG = 3.0
def _bb(items, end):
    bs = [_bxv(d, end) for d in items]
    bs = [b for b in bs if b]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)) if bs else None

def _fit_size(d, want):
    n = len(str(d.get('label') or '')); extra = 1.4 if d.get('emo') else 0
    return min(want, (ZONE[2] - ZONE[0] - 60) / max(1.0, n * 0.6 + extra)) if n else want

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
    # Aly 2026-11-24: 3+ pictures that come together = ONE clean matrix of 2 columns, same size (never a small one on top of another)
    for gk in {d['grid'] for d in its if d.get('grid')}:   # an old grid of pictures becomes a clean matrix too
        g0 = [d for d in its if d.get('grid') == gk and d.get('k') == 'node' and d.get('src')]
        if len(g0) >= 3:
            for d in g0: d.pop('grid'); d['at0'] = d['at']; d['at'] = min(q['at'] for q in g0)   # one block (each still pops on its own word below)
    pics = sorted([d for d in its if d.get('k') == 'node' and d.get('src') and not d.get('grid')], key=lambda d: d['at'])
    mi = 0
    while pics:
        g = [q for q in pics if q['at'] - pics[0]['at'] <= 25]
        pics = [q for q in pics if q not in g]
        if len(g) < 3: continue
        g.sort(key=lambda d: (round(d['y'] / 60), -d['x']))   # reading order: top row first, right to left
        ar = g[0].get('ar', 16 / 9); lab = 80 if any(d.get('label') for d in g) else 0
        best = None
        for cols in (2, 3, 4, 5):   # the biggest pictures that fit: full width and at most ~75% of the board height
            rows = -(-len(g) // cols)
            w_ = min(470, (ZONE[2] - ZONE[0] - 30 * (cols - 1)) / cols, ((ZONE[3] - ZONE[1]) * 0.75 / rows - 30 - lab) * ar)
            if best is None or w_ > best[1]: best = (cols, w_)
        cols, w = best[0], round(best[1]); h = w / ar + lab
        for i, d in enumerate(g):
            c = i % cols
            d['w'] = w; d['x'] = round(960 + ((cols - 1) / 2 - c) * (w + 30)); d['y'] = round(300 + (i // cols) * (h + 30)); d['grid'] = f'mx{mi}'
            d['size'] = max(d.get('size', 30), 34)
            if d.get('at0') is not None: d['at'] = d.pop('at0')
        mi += 1
    groups = {}
    for d in its:
        key = ('grid', d['grid']) if d.get('grid') else ('bars',) if d.get('k') == 'bar' else ('one', id(d))
        groups.setdefault(key, []).append(d)
    blocks = []
    Wz = ZONE[2] - ZONE[0]
    for g in groups.values():
        bb = _bb(g, end)
        if not bb: continue
        grow = min(BIG, Wz * 0.92 / max(1, bb[2] - bb[0]), (ZONE[3] - ZONE[1]) * 0.7 / max(1, bb[3] - bb[1]))
        if grow > 1.05: _shrink(g, grow); bb = _bb(g, end)   # phone size: cards made for 1920 are enlarged for the 1080-wide frame
        for d in g:   # Aly «كبر شوية»: no small text on a phone — pills >= 46 px, labels under pictures >= 36 px, typed >= 32 px
            if d.get('k') == 'node': d['size'] = round(_fit_size(d, max(d.get('size', 30), 36 if (d.get('src') or d.get('logo')) else 46)), 1)
            elif d.get('k') == 'typed': d['size'] = max(d.get('size', 24), 32)
        bb = _bb(g, end)
        for _ in range(3):
            if bb[2] - bb[0] <= Wz: break
            _shrink(g, Wz / (bb[2] - bb[0]) * 0.97); bb = _bb(g, end)
        blocks.append(dict(items=g, box=bb, orig=bb, at=min(d['at'] for d in g), out=max(min(d.get('out', end), end) for d in g)))
    blocks.sort(key=lambda b: b['at'])
    merged = []
    for b in blocks:   # a bare logo and the line that comes right after it on the same height = one block (logo on top)
        a0 = merged[-1] if merged else None
        if a0 and len(a0['items']) == 1 and a0['items'][0].get('logo') and not a0['items'][0].get('label')                 and b['at'] - a0['at'] <= 25 and abs((b['orig'][1] + b['orig'][3]) / 2 - (a0['orig'][1] + a0['orig'][3]) / 2) < 60:
            ab, bb2 = a0['box'], b['box']
            _shift(b['items'], (ab[0] + ab[2]) / 2 - (bb2[0] + bb2[2]) / 2, ab[3] + 10 - bb2[1])
            a0['items'] = a0['items'] + b['items']; a0['box'] = _bb(a0['items'], end); a0['out'] = max(a0['out'], b['out'])
            continue
        merged.append(b)
    blocks = merged
    rows = []
    for b in blocks:
        w = b['box'][2] - b['box'][0]
        r = rows[-1] if rows else None
        small = w <= Wz * 0.5 and r and r['w'] <= Wz * 0.5
        together = r and small and len(r['bl']) < 3 and b['at'] - r['at'] <= 25          # small things entering together share a row
        side = r and len(r['bl']) < 3 and abs((b['orig'][1] + b['orig'][3]) / 2 - r['cy']) < 70 and b['at'] - r['at'] <= 50             and abs(b['orig'][0] - r['bl'][-1]['orig'][0]) > 60
        if (together or side) and r['w'] + GAPX + w > Wz:
            k = (Wz - GAPX * len(r['bl'])) / (r['w'] - GAPX * (len(r['bl']) - 1) + w)
            if k >= 0.5:
                for q in r['bl'] + [b]:
                    _shrink(q['items'], k); q['box'] = _bb(q['items'], end)
                w = b['box'][2] - b['box'][0]
                r['w'] = sum(q['box'][2] - q['box'][0] for q in r['bl']) + GAPX * (len(r['bl']) - 1)
                r['h'] = max(q['box'][3] - q['box'][1] for q in r['bl'])
        if side and r['w'] + GAPX + w > Wz + 1 and len(r['bl']) == 1:
            # a table row (logo + its line) that can't sit side by side: stack them as ONE block (logo on top, line under it)
            a0 = r['bl'][0]; ab, bb2 = a0['box'], b['box']
            _shift(b['items'], (ab[0] + ab[2]) / 2 - (bb2[0] + bb2[2]) / 2, ab[3] + 10 - bb2[1])
            a0['items'] = a0['items'] + b['items']; a0['box'] = _bb(a0['items'], end); a0['out'] = max(a0['out'], b['out'])
            r['w'] = a0['box'][2] - a0['box'][0]; r['h'] = a0['box'][3] - a0['box'][1]; r['out'] = max(r['out'], b['out'])
            continue
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
                if not r.get('lifted'):   # first: rows that came WITH this one move up into free space left by rows that already left
                    r['lifted'] = True; moved = False
                    for q in vis:
                        others = [o for o in vis if o is not q]
                        for ny in sorted([ZONE[1]] + [o['y'] + o['h'] + GAPY for o in others]):
                            if ny >= q['y']: break
                            if all(ny + q['h'] + GAPY <= o['y'] or ny >= o['y'] + o['h'] + GAPY for o in others):
                                for b in q['bl']:
                                    _shift(b['items'], 0, ny - q['y']); b['box'] = (b['box'][0], b['box'][1] + ny - q['y'], b['box'][2], b['box'][3] + ny - q['y'])
                                q['y'] = ny; moved = True; break
                    if moved: continue
                tries = r.get('tries', 0)
                if tries >= 3:   # last resort: the old row leaves anyway (a fast hand-over beats an overlap)
                    old['out'] = max(old['at'] + 1, r['at'] - 2)
                    for b in old['bl']:
                        b['out'] = min(b['out'], old['out'])
                        for d in b['items']: d['out'] = min(d.get('out', end), old['out'])
                    continue
                r['tries'] = tries + 1
                avail = ZONE[3] - (max(q['y'] + q['h'] for q in vis) + GAPY)   # shrink exactly to the free space under what stays
                kk = max(0.6, min(0.95, avail / max(1, r['h'])))
                for b in r['bl']:
                    _shrink(b['items'], kk); b['box'] = _bb(b['items'], end)
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
    for d in [d for r in placed for b in r['bl'] for d in b['items']]:   # «كبر شوية»: text never ends up tiny after a row squeeze
        if d.get('k') == 'node': d['size'] = round(_fit_size(d, max(d.get('size', 30), 32 if (d.get('src') or d.get('logo')) else 40)), 1)
    for r in placed:   # logo-on-top blocks: the line sits under the logo again after the text got bigger
        for b in r['bl']:
            it = b['items']
            if len(it) > 1 and it[0].get('logo') and not it[0].get('label'):
                lb = _bxv(it[0], end); ob = _bb(it[1:], end)
                if lb and ob: _shift(it[1:], (lb[0] + lb[2]) / 2 - (ob[0] + ob[2]) / 2, lb[3] + 10 - ob[1])
    # safety net (overlap law): any two cards still on screen together and touching -> the earlier one leaves before the later enters
    flat = sorted([d for b in [b for r in placed for b in r['bl']] for d in b['items']], key=lambda d: d['at'])
    for i, a in enumerate(flat):
        ba = _bxv(a, end)
        for c in flat[i + 1:]:
            bc = _bxv(c, end)
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
        ba = _bxv(a, end)
        if not ba: continue
        for b in its[i + 1:]:
            bb = _bxv(b, end)
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
        for d in s['items']:
            if d.get('label') in SIMPLE:
                d['label'], sub = SIMPLE[d['label']]
                if sub: d['sub'] = sub
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

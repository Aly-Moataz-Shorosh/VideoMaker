"""Props for comp ai-world-short (vertical shorts from v11): pieces on the output timeline, an automatic CAMERA per output frame
(follows the boxes of everything visible on the v11 stage: v11_resolve.boxes = the measured box model), word captions, title band.
Run from work/:  python scripts/shorts_props.py [N ...]   -> shorts/props_NN.json"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shorts_data import SHORTS
import v11_resolve

FPS = 25
VW, VH = 1080, 1100            # the window (Short11.tsx VIEW)
ZMIN, ZMAX = 0.56, 1.25
PAD = 40
P = json.load(open('props_v11.json', encoding='utf-8'))
CUTS = {c['n']: c for c in json.load(open('shorts/cuts.json', encoding='utf-8'))}
W = sorted(json.load(open('words_v11_real.json', encoding='utf-8')), key=lambda w: w['a'])
SKIPK = {'titleAt', 'line', 'brand', 'subscribe', 'sep', 'edge', 'split', 'diff', 'page', 'circle', 'puppet'}

def union(bs):
    bs = [b for b in bs if b]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)) if bs else None

def scene_at(t):
    c = [s for s in P['scenes'] if s['start'] <= t < s['start'] + s['dur']]
    return c[-1] if c else None

def target(t):
    """(cx, cy, z, key) for v11 second t"""
    face = [c for c in P['faces'] if c['from'] <= t < c['from'] + c['dur']]
    full = [c for c in face if not c.get('circle')]
    s = scene_at(t)
    key = (s['start'] if s else -1, bool(full))
    if full:   # his face fills the frame -> frame his face
        fx = full[0].get('fx', 0.5) * 1920
        return fx, 540, 1.0, key
    if not s: return 960, 540, ZMIN, key
    fs = (t - s['start']) * FPS; end = s['dur'] * FPS; k = s['k']
    bs = []
    if k == 'SEP': bs.append((200, 120, 1720, 920))
    elif k == 'MAP6': bs.append((380, 300, 1540, 840))
    elif k == 'SPLIT': bs.append((210, 330, 1710, 800))
    elif k == 'LYR': bs.append((420, 0, 1500, 1080))
    elif k in ('AV', 'CLIP') and not [d for d in s['items'] if d.get('k') not in SKIPK]: bs.append((420, 0, 1500, 1080))
    if s.get('fx') == 'diffusion': bs.append((460, 260, 1460, 860))
    if k == 'WEB':
        pg = [d for d in s['items'] if d.get('k') == 'page' and d.get('at', 0) <= fs]
        if pg:
            d = pg[-1]; w = d.get('w', 1180); h = w * 0.56 + 44; x, y = d.get('x', 960), d.get('y', 560)
            bs.append((x - w / 2, y - h / 2, x + w / 2, y + h / 2))
    for d in s['items']:
        if d.get('k') in SKIPK or 'x' not in d: continue
        a, o = d.get('at', 0), d.get('out', end)
        if not (a <= fs < o + 6): continue
        try: bs.append(v11_resolve._bx({**d}, end))
        except Exception: pass
    for c in face:   # talking circles over boards
        q = c['circle']; bs.append((q['x'] - q['r'], q['y'] - q['r'], q['x'] + q['r'], q['y'] + q['r']))
    for d in s['items']:
        if d.get('k') == 'circle' and d.get('at', 0) <= fs:
            r = d.get('r', 150); bs.append((d['x'] - r, d['y'] - r, d['x'] + r, d['y'] + r))
    b = union(bs)
    if not b: return 960, 540, ZMIN, key
    w, h = b[2] - b[0] + 2 * PAD, b[3] - b[1] + 2 * PAD
    z = max(ZMIN, min(ZMAX, VW / w, VH / h))
    return (b[0] + b[2]) / 2, (b[1] + b[3]) / 2, z, key

def fit(cx, cy, z):
    ww, wh = VW / z, VH / z
    cx = 960 if ww >= 1920 else min(max(cx, ww / 2), 1920 - ww / 2)
    cy = 540 if wh >= 1080 else min(max(cy, wh / 2), 1080 - wh / 2)
    return cx, cy

def build(sd):
    cut = CUTS[sd['n']]
    pieces, o = [], 0.0
    for a, b in cut['pieces']:
        pieces.append(dict(a=round(a, 3), b=round(b, 3), o=round(o, 3))); o += b - a
    dur = o
    end = None
    if sd.get('endcard'):
        end = dict(from_=round(dur, 2), thumb='projects/aiworld/shorts/thumb_v11.jpg', line1='الفيديو الكامل على قناتي', line2='عالم الـ AI كله في فيديو واحد')
        dur += 4.5
    nF = int(round(dur * FPS))
    cam, prev, pkey = [], None, None
    starts = {int(round(pc['o'] * FPS)) for pc in pieces}
    for f in range(nF):
        t_out = f / FPS
        pc = [pc for pc in pieces if pc['o'] <= t_out][-1]
        ts = min(pc['b'] - 0.01, pc['a'] + (t_out - pc['o']))
        cx, cy, z, key = target(ts)
        cx, cy = fit(cx, cy, z)
        if prev is None or f in starts or key != pkey: cur = [cx, cy, z]
        else:
            k = 0.10
            lz = math.log(prev[2]) + (math.log(z) - math.log(prev[2])) * k
            zz = math.exp(lz); px, py = prev[0] + (cx - prev[0]) * k, prev[1] + (cy - prev[1]) * k
            px, py = fit(px, py, zz); cur = [px, py, zz]
        cam.append([round(cur[0], 1), round(cur[1], 1), round(cur[2], 4)]); prev, pkey = cur, key
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
    props = dict(fps=FPS, duration=round(dur, 3), outW=1080, scenes=P['scenes'], subs=P['subs'], hud=[], caps=[], faces=P['faces'],
                 families=P.get('families') or ['التوليد', 'الـ LLMs والـ agents', 'السكريبتات', 'الـ MCP', 'الـ skills', 'الإنسان'],
                 pieces=pieces, cam=cam, title=sd['title'], hook=sd.get('hook_text', ''), cta=sd.get('cta', ''),
                 ctaFrom=round((end['from_'] if end else dur) - 3.0, 2), words=words, series=sd.get('series', ''))
    if end: props['end'] = {'from': end['from_'], 'thumb': end['thumb'], 'line1': end['line1'], 'line2': end['line2']}
    props.pop('families') if not P.get('families') else None
    return props

if __name__ == '__main__':
    want = [int(x) for x in sys.argv[1:]] or [s['n'] for s in SHORTS]
    os.makedirs('shorts', exist_ok=True)
    for sd in SHORTS:
        if sd['n'] not in want: continue
        p = build(sd)
        json.dump(p, open(f"shorts/props_{sd['n']:02d}.json", 'w', encoding='utf-8'), ensure_ascii=False)
        zs = [c[2] for c in p['cam']]
        print(f"#{sd['n']:02d} {sd['slug']}: {p['duration']:.1f}s, {len(p['pieces'])} pieces, words {len(p['words'])}, zoom {min(zs):.2f}-{max(zs):.2f}")

# Whole course video -> work/props_full.json (+ work/chapters.json, work/cues_report.txt).
#   python make_full.py
# Uses make_course.py (opening, chapter list, separators) + course_data.py (glossary, shortcuts, cards, fast-forward).
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_course as MC
import course_data as D

PROJ, PUB, FPS, SEP = MC.PROJ, MC.PUB, MC.FPS, MC.SEP
EP_LEN = MC.EP_LEN
AN = {ep: json.load(open(PROJ / f'work/ep{ep}/analysis.json')) for ep in (1, 2, 3)}
WORDS = {}
for ep in (1, 2, 3):
    t = json.load(open(PROJ / f'work/ep{ep}/transcript.json', encoding='utf-8'))
    WORDS[ep] = [(w['w'].strip(), w['start']) for s in t['sentences'] for w in s['words'] if w['w'].strip()]
report = []


def quiet_near(ep, t, back=2.0, fwd=1.0):
    """Quietest 150 ms point near t (chapter edges never on a word)."""
    if t <= 0: return 0.0
    r = np.array(AN[ep]['rms'])
    a, b = int((t - back) * 10), int((t + fwd) * 10)
    best, bt = 0, t
    for i in range(max(1, a), min(len(r) - 2, b)):
        v = r[i:i + 2].max()
        score = -v - abs(i / 10 - t) * 3
        if v < -38 and score > best: best, bt = score, i / 10 + 0.05
    return round(bt, 2)


# ---------- chapters with snapped edges ----------
chs = MC.chapter_ranges()
for c in chs:
    c['src'] = quiet_near(c['ep'], c['src']) if c['src'] > 0 else 0.0
for i, c in enumerate(chs):
    nxt = chs[i + 1] if i + 1 < len(chs) and chs[i + 1]['ep'] == c['ep'] else None
    c['end'] = nxt['src'] if nxt else EP_LEN[c['ep']]


def ff_in(ep, a, b):
    return [(max(a, x), min(b, y), n) for x, y, n in D.FF.get(ep, []) if min(b, y) > max(a, x)]


def pieces(c):
    """Source pieces of a chapter: (from, to, rate, note)."""
    out, t = [], c['src']
    for x, y, n in ff_in(c['ep'], c['src'], c['end']):
        if x > t: out.append((t, x, 1, None))
        out.append((x, y, 4, n)); t = y
    if t < c['end']: out.append((t, c['end'], 1, None))
    return out


# ---------- timeline ----------
open_len = sum(d for _, d, _ in MC.OPEN) + MC.STAMP_SEC * 3
t = open_len
for c in chs:
    c['sep'] = t; c['t'] = t + SEP
    c['pieces'] = []
    tt = c['t']
    for a, b, r, n in pieces(c):
        c['pieces'].append(dict(at=tt, frm=a, to=b, rate=r, note=n)); tt += (b - a) / r
    c['tend'] = tt
    t = tt
END_COURSE = t
EXTRA_LEN = 52.0
TOTAL_LEN = END_COURSE + SEP + EXTRA_LEN + 2.0


def tl(c, s):
    """Timeline second of source second s inside chapter c."""
    for p in c['pieces']:
        if p['frm'] <= s <= p['to']:
            return p['at'] + (s - p['frm']) / p['rate']
    return None


def in_ff(c, s):
    return any(p['rate'] > 1 and p['frm'] <= s <= p['to'] for p in c['pieces'])


def words_of(c):
    return [(w, s) for w, s in WORDS[c['ep']] if c['src'] <= s < c['end']]


def find(c, pat, after=None):
    ws = words_of(c)
    text, idx = '', []
    for w, s in ws:
        idx.append((len(text), s)); text += w + ' '
    m = re.search(pat, text, re.I)
    if not m: return None
    pos = m.start()
    best = ws[0][1] if ws else c['src']
    for p0, s in idx:
        if p0 <= pos: best = s
        else: break
    return best


cues, keys, scenes, huds, music, sfx, parts = [], [], [], [], [], [], []
LEFT = {'Def', 'Fig', 'New26'} | set(['ResGrid', 'ResLadder', 'TimelineAnim', 'KeyAnim', 'NestAnim', 'SlowMath', 'InsOver', 'RippleRoll', 'SlipSlide', 'InterpAnim', 'BlendAnim', 'AdjAnim', 'Agenda', 'Flip', 'FpsRace', 'PerSecond'])
side_iv = []  # (t0, t1) timeline intervals that need the left column (side mode)
zoom_pts = []  # (timeline t, ep, source s)


def add(t, d, k, p, ep=None, s=None):
    cues.append(dict(t=round(t, 3), d=d, k=k, p=p))
    if k in LEFT: side_iv.append((t, t + d))


# ---------- opening + timestamps (same as the approved chapter-1 review) ----------
tt = 0.0
for k, d, p in MC.OPEN:
    scenes.append(dict(t=tt, d=d, k=k, p=p)); tt += d
for ep in (1, 2, 3):
    items = [dict(time=MC.fmt(c['sep']), ar=c['ar'], ico=c['ico']) for c in chs if c['ep'] == ep]
    nums = [c['n'] for c in chs if c['ep'] == ep]
    if ep == 3:
        items.append(dict(time=MC.fmt(END_COURSE), ar=MC.EXTRA[0], ico=MC.EXTRA[2])); nums.append(MC.TOTAL)
    scenes.append(dict(t=tt, d=MC.STAMP_SEC, k='OStamps', p=dict(range=f'الفصول {nums[0]} – {nums[-1]}', title=MC.EP_TITLE[ep], items=items))); tt += MC.STAMP_SEC
music.append(dict(t=0, d=tt + 0.3, file=PUB + 'music/lofi_coffee_shop.mp3', from_=0, vol=0.14, fade=1.2))


def sep(n, ep, title, en, ico, at, thumb):
    scenes.append(dict(t=at, d=SEP, k='Sep', p=dict(n=n, total=MC.TOTAL, ep=ep, title=title, en=en, ico=ico, thumb=thumb)))
    music.append(dict(t=at, d=SEP + 0.3, file=PUB + 'music/lofi_coffee_shop.mp3', from_=8 + (n * 7) % 90, vol=0.14, fade=0.8))
    sfx.append(dict(t=at + 0.05, file='sfx/whoosh_2.wav', vol=0.18))


# ---------- chapters ----------
for c in chs:
    ep, n = c['ep'], c['n']
    sep(n, ep, c['ar'], c['en'], c['ico'], c['sep'], MC.thumb(ep, c['src'], f'ch{n:02d}.jpg'))
    for p in c['pieces']:
        parts.append(dict(at=round(p['at'], 3), from_=p['frm'], to=p['to'], rate=p['rate'], file=PUB + f'ep{ep}.mp4'))
        if p['rate'] > 1:
            d = (p['to'] - p['frm']) / p['rate']
            add(p['at'], d, 'Chip', dict(kind='ff', text=f'×4 — {p["note"]}', y=90))
            music.append(dict(t=p['at'], d=d, file=PUB + 'music/lofi_coffee_shop.mp3', from_=30 + n % 60, vol=0.10, fade=0.6))
    huds.append(dict(t=c['t'], d=c['tend'] - c['t'], ep=ep, n=n, total=MC.TOTAL, title=c['ar']))
    if n == 1:
        continue  # chapter 1 cues come from the approved review (make_course.py), added below
    # auto: English words (first time in the chapter), at most one every 4 s
    seen, last = {}, -9
    for w, s in words_of(c):
        for pat, en, ar in D.GLOSS:
            if re.search(pat, w, re.I) and s - seen.get(en, -999) > 180:
                tt2 = tl(c, s)
                if tt2 is None or in_ff(c, s) or tt2 - last < 4: break
                seen[en] = s; last = tt2
                add(tt2, 3.2, 'Kw', dict(en=en, ar=ar))
                break
    # auto: spoken shortcuts / clicks
    ws = words_of(c)
    lastk = {}
    for i in range(len(ws)):
        win = ' '.join(w for w, _ in ws[i:i + 3])
        for pat, kk, ar in D.KEYS:
            if re.match(pat, win, re.I):
                s = ws[i][1]; tt2 = tl(c, s)
                key = '+'.join(kk)
                if tt2 is None or in_ff(c, s) or tt2 - lastk.get(key, -99) < 10: continue
                lastk[key] = tt2
                add(tt2, 4.0, 'Key', dict(keys=kk, ar=ar))
                zoom_pts.append((tt2, ep, s))
    # manual cards
    for anchor, kind, d, p in D.M.get(n, []):
        s = anchor if isinstance(anchor, (int, float)) else find(c, anchor)
        if s is None:
            report.append(f'ch{n}: anchor not found: {anchor} ({kind})'); continue
        tt2 = tl(c, s)
        if tt2 is None: continue
        if kind == 'New':
            q = dict(D.NEW[p['n']])
            vid = q.pop('vid', None)
            if vid: q['thumb'], q['qr'] = D.V(vid)
            add(tt2, d, 'New26', q)
        elif kind == 'Key':
            add(tt2, d, 'Key', p); zoom_pts.append((tt2, ep, s))
        else:
            add(tt2, d, kind, p)

# ---------- chapter 1 = the approved review content ----------
c1 = chs[0]
T1 = c1['t']
src_cues = json.load(open(PROJ / 'work/props_ch1.json', encoding='utf-8'))
off = T1 - [s for s in src_cues['scenes'] if s['k'] == 'Sep'][0]['t'] - SEP
for q in src_cues['cues']:
    q = dict(q); q['t'] = round(q['t'] + off, 3); cues.append(q)
    if q['k'] in LEFT: side_iv.append((q['t'], q['t'] + q['d']))
ch1_keys = [dict(k) for k in src_cues['keys'] if k['t'] + off < c1['tend'] - 0.5]
for k in ch1_keys: k['t'] = round(k['t'] + off, 3)


# ---------- layout keys ----------
def cursor_at(ep, s):
    a = AN[ep]; f = a['fps']; cur = a['cursor']
    i = int(s * f)
    for d in range(0, 6):
        for j in (i - d, i + d):
            if 0 <= j < len(cur) and cur[j]: return cur[j]
    return None


def in_side(t):
    return any(a - 0.4 <= t <= b + 0.4 for a, b in side_iv)


def side_now(t):
    return any(a <= t < b for a, b in side_iv)


def slide_boxes(c):
    """Slides on black (chapters 2-5): crop to each slide's content."""
    a = AN[c['ep']]; f = a['fps']; dif = a['diff']
    i0, i1 = int(c['src'] * f), int(c['end'] * f)
    changes = [c['src'] + 0.3] + [i / f for i in range(i0 + 1, i1) if dif[i] > 6 and all(dif[j] <= 6 for j in range(max(i0, i - 8), i))]
    out = []
    for s in changes:
        png = PROJ / f'work/slides/{c["ep"]}_{int(s * 10)}.png'
        png.parent.mkdir(parents=True, exist_ok=True)
        if not png.exists():
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s + 0.8), '-i', str(PROJ / f'input/ep{c["ep"]}.mp4'), '-frames:v', '1', str(png)], check=True)
        from PIL import Image
        g = np.asarray(Image.open(png).convert('L'))[20:690, :1100]
        ys, xs = np.where(g > 40)
        if len(xs) < 50: out.append((s, None)); continue
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min() + 20, ys.max() + 20
        w = min(1276, max(x1 - x0 + 80, (y1 - y0 + 80) * 16 / 9, 640))
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        sx = int(min(max(0, cx - w / 2), 1276 - w)); sy = int(min(max(0, cy - w * 9 / 32), 720 - w * 9 / 16))
        out.append((s, (sx, sy, int(w))))
    return out


def busy(ep, s, sx, sy, sw, sh):
    """Zoom only where there is something to read (not an empty black area)."""
    from PIL import Image
    png = PROJ / f'work/zoomchk/{ep}_{int(s * 10)}.png'
    png.parent.mkdir(parents=True, exist_ok=True)
    if not png.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(s), '-i', str(PROJ / f'input/ep{ep}.mp4'), '-frames:v', '1', '-vf', 'scale=638:360', str(png)], check=True)
    g = np.asarray(Image.open(png).convert('L')).astype(float)[int(sy / 2):int((sy + sh) / 2), int(sx / 2):int((sx + sw) / 2)]
    edges = np.abs(np.diff(g, axis=1)).mean()
    return g.std() > 15 and edges > 2.2


def clicks(c):
    a = AN[c['ep']]; f = a['fps']; cur = a['cursor']; dif = a['diff']
    out = []
    for i in range(int(c['src'] * f) + 4, int(c['end'] * f) - 4):
        win = cur[i - 4:i]
        if any(w is None for w in win): continue
        if max(abs(w[0] - win[0][0]) + abs(w[1] - win[0][1]) for w in win) > 18: continue
        if max(dif[i:i + 4]) > 2.5 and max(dif[i - 4:i]) < 1.5:
            out.append(((i - 2) / f, win[-1]))
    return out


for c in chs[1:]:
    if c['n'] in D.SLIDES: continue
    for s_, cu in clicks(c):
        tt2 = tl(c, s_)
        if tt2 is not None and not in_ff(c, s_): zoom_pts.append((tt2, c['ep'], s_))

for c in chs[1:]:
    keys.append(dict(t=round(c['sep'] - 0.01, 3), m='side'))
    if c['n'] in D.SLIDES:
        for s, bx in slide_boxes(c):
            tt2 = tl(c, s)
            if tt2 is None: continue
            keys.append(dict(t=round(max(tt2, c['t']), 3), m='side', **(dict(sx=bx[0], sy=bx[1], sw=bx[2]) if bx else {})))
        continue
    # UI chapters: full screen; side while a left-column card is up; zoom on his cursor at shortcuts (>= 8 s apart)
    t0, t1 = c['t'], c['tend']
    ev = sorted([(a, 'side') for a, b in side_iv if t0 <= a < t1] + [(b, 'full') for a, b in side_iv if t0 <= b < t1])
    keys.append(dict(t=round(t0, 3), m='side' if side_now(t0) else 'full'))
    for a, m in ev:
        keys.append(dict(t=round(a, 3), m='side' if side_now(a + 0.01) else 'full'))
    lastz = -99
    for tz, ep, s in sorted(zoom_pts):
        if not (t0 + 1 <= tz < t1 - 4) or tz - lastz < 12 or in_side(tz) or in_side(tz + 4): continue
        cu = cursor_at(ep, s)
        if not cu: continue
        sw = 900; sh = sw * 9 / 16
        sx = int(min(max(0, cu[0] - sw / 2), 1276 - sw)); sy = int(min(max(0, cu[1] - sh / 2), 720 - sh))
        if not busy(ep, s, sx, sy, sw, sh): continue
        keys.append(dict(t=round(tz - 0.4, 3), m='full', sx=sx, sy=sy, sw=sw))
        keys.append(dict(t=round(tz + 3.6, 3), m='full'))
        lastz = tz
keys = ch1_keys + [dict(t=0, m='full')] + keys
keys.sort(key=lambda k: k['t'])
# drop keys closer than 0.7 s to the next one (keep the later)
clean = []
for k in keys:
    if clean and k['t'] - clean[-1]['t'] < 0.7: clean[-1] = k
    else: clean.append(k)
keys = clean

# ---------- chapter 47 (Claude): what to learn next ----------
t47 = END_COURSE
sep(MC.TOTAL, 3, MC.EXTRA[0], MC.EXTRA[1], MC.EXTRA[2], t47, None)
scenes.append(dict(t=t47 + SEP, d=EXTRA_LEN, k='ONext', p={}))
music.append(dict(t=t47 + SEP, d=EXTRA_LEN + 2, file=PUB + 'music/lofi_coffee_shop.mp3', from_=40, vol=0.12, fade=1.5))

for p in parts: p['from'] = p.pop('from_')
for m in music: m['from'] = m.pop('from_')
props = dict(fps=FPS, duration=round(TOTAL_LEN, 3), parts=parts, keys=keys, cues=sorted(cues, key=lambda q: q['t']), scenes=scenes, huds=huds, music=music, sfx=sfx)
json.dump(props, open(PROJ / 'work/props_full.json', 'w', encoding='utf-8'), ensure_ascii=False)
json.dump([dict(n=c['n'], time=MC.fmt(c['sep']), ar=c['ar'], en=c['en'], ep=c['ep'], src=c['src']) for c in chs] + [dict(n=MC.TOTAL, time=MC.fmt(END_COURSE), ar=MC.EXTRA[0], en=MC.EXTRA[1])],
          open(PROJ / 'work/chapters.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
kinds = {}
for q in cues: kinds[q['k']] = kinds.get(q['k'], 0) + 1
open(PROJ / 'work/cues_report.txt', 'w', encoding='utf-8').write('\n'.join(report))
print('length', MC.fmt(TOTAL_LEN), '| cues', len(cues), kinds, '| keys', len(keys), '| parts', len(parts), '| missing anchors', len(report))

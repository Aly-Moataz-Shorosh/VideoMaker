# Shorts series from the course (Aly 2026-10-18) -> work/shorts/props_<NN>.json   python make_shorts.py 1 2 ...
# Pieces = his sentences (source seconds) fitted on the waveform (never inside a word), pauses removed (0.12 s gap),
# per-piece gain to one voice level. Each piece says what fills the stage: his screen ('screen', zoom on his cursor, gold box on
# his clicks) or an animation / big line. Posting order = most impressive first (shorts_data.ORDER).
import json, subprocess, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shorts_data as SD

PROJ = Path(__file__).resolve().parents[2]
PUB = 'projects/premiere/'
FPS, GAP = 30, 0.12
AN = {ep: json.load(open(PROJ / f'work/ep{ep}/analysis.json')) for ep in (1, 2, 3)}
EPW = {}
for _ep in (1, 2, 3):
    _t = json.load(open(PROJ / f'work/ep{_ep}/transcript.json', encoding='utf-8'))
    EPW[_ep] = [(w['w'].strip(), w['start'], w['end']) for s_ in _t['sentences'] for w in s_['words'] if w['w'].strip()]
CARD_W, CARD_H = 1016, 840  # screen card in Short.tsx
import re as _re
BAD = _re.compile(r'اشتركوا|القناة|ترجمة|نانسي|قنقر|المترجم|شكرا للمشاهدة')
DUAL_H = (840 - 12) / 2
CH = {c['n']: c for c in json.load(open(PROJ / 'work/chapters.json', encoding='utf-8'))}
_db = {}


def db10(ep):
    """10 ms RMS dB of the episode (cached as .npy)."""
    if ep not in _db:
        f = PROJ / f'work/ep{ep}/db10.npy'
        if not f.exists():
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(PROJ / f'input/ep{ep}.mp4'), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
            a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
            n = len(a) // 160
            np.save(f, (20 * np.log10(np.sqrt((a[: n * 160].reshape(n, 160) ** 2).mean(1)) + 1e-9)).astype(np.float32))
        _db[ep] = np.load(f)
    return _db[ep]


def fit(ep, a, b):
    """Edges on the waveform: start just before the first sound, end after the sound has died (150 ms quiet)."""
    d = db10(ep)
    i, j = int(a * 100), int(b * 100)
    loc = d[max(0, i - 300):j + 300]
    th = max(-45.0, float(np.percentile(loc, 15)) + 12)
    s = i
    while s > i - 60 and d[s - 1] > th: s -= 1  # walk back while still speech (word started earlier than Whisper said)
    while s < j and d[s] <= th: s += 1  # skip leading quiet
    s = max(0, s - 6)
    e, q = j, 0
    while e < j + 120 and q < 15:
        q = q + 1 if d[e] <= th else 0
        e += 1
    e = e - 15 + 8
    prev_end = max([w[2] for w in EPW[ep] if w[2] <= a + 0.05] or [0])
    # the last word that STARTS inside the piece is always kept whole (Aly 2026-10-18: "Scale" / "Animation" were cut —
    # a word starting just before b used to count as the next word)
    inside = [w for w in EPW[ep] if a - 0.05 <= w[1] < b - 0.08]  # a word starting in the last 0.08 s belongs to the next sentence (edges are snapped to words in edge_fixes.json)
    last_end = max([w[2] for w in inside] or [b])
    nxt = min([w[1] for w in EPW[ep] if w[1] >= max(b, last_end - 0.02) and w[1] > a + 0.3] or [1e9])
    s = max(s, int((prev_end + 0.02) * 100))
    e = max(e, int((last_end + 0.12) * 100))
    e = min(e, int((nxt - 0.03) * 100))
    # never more than a breath outside his own words (Aly 2026-10-18: "شوية كلام زيادة بيتحط أول وبعد" = edges caught
    # bits of the neighbouring sentences)
    first_start = min([w[1] for w in inside] or [a])
    s = max(s, int((first_start - 0.15) * 100))
    e = min(e, int((last_end + 0.30) * 100))
    return round(s / 100, 2), round(e / 100, 2)


def level(ep, a, b):
    d = db10(ep)[int(a * 100):int(b * 100)]
    sp = d[d > np.percentile(d, 40)]
    return float(10 * np.log10(np.mean(10 ** (sp / 10)))) if len(sp) else -30.0


def cursor(ep, s):
    a = AN[ep]; cur = a['cursor']; i = int(s * a['fps'])
    for k in range(0, 8):
        for j in (i - k, i + k):
            if 0 <= j < len(cur) and cur[j]: return cur[j]
    return None


def clicks(ep, a, b):
    an = AN[ep]; f = an['fps']; cur = an['cursor']; dif = an['diff']; out = []
    for i in range(int(a * f) + 4, int(b * f) - 2):
        win = cur[i - 4:i]
        if any(w is None for w in win): continue
        if max(abs(w[0] - win[0][0]) + abs(w[1] - win[0][1]) for w in win) > 18: continue
        if max(dif[i:i + 4]) > 2.5 and max(dif[i - 4:i]) < 1.5 and (not out or i / f - out[-1][0] > 1.5):
            out.append((i / f, win[-1]))
    return out


def crop_at(c, sw=640):
    sh = sw * CARD_H / CARD_W
    return dict(sx=int(min(max(0, c[0] - sw / 2), 1276 - sw)), sy=int(min(max(0, c[1] - sh / 2), 720 - sh)), sw=sw)


def build(n):
    spec = SD.SHORTS[n]
    ep = spec['ep']
    voice, screens, cues, sfx = [], [], [], []
    t = 0.3
    levels = []
    plan = []
    for pc in spec['pieces']:
        ep = pc.get('ep', spec['ep'])  # a piece may come from another episode (short 44: shortcuts of the whole course)
        a, b = fit(ep, pc['a'], pc['b'])
        plan.append((pc, a, b)); levels.append(level(ep, a, b))
    target = float(np.median(levels))
    words = []
    caps = SD.CAP.get(n, [])
    wf = PROJ / f'work/shorts/words_{n:02d}.json'
    AUTOW = json.load(open(wf, encoding='utf-8')) if wf.exists() else []
    # drop Whisper's classic hallucinations (never said by Aly) and a whole run of them
    AUTOW = [w for w in AUTOW if not BAD.search(w['w'])]
    step = 0
    nsteps = sum(1 for pc, _, _ in plan if pc.get('step'))
    env = []
    for (pc, a, b), lv in zip(plan, levels):
        ep = pc.get('ep', spec['ep'])
        d = b - a
        gain = round(float(10 ** ((target - lv) / 20)), 3)
        voice.append(dict(file=PUB + f'ep{ep}.mp4', **{'from': a}, to=b, at=round(t, 3), gain=min(1.25, max(0.5, gain))))
        cap = caps[len(voice) - 1] if len(caps) >= len(voice) else None
        ew = [w for w in EPW[ep] if a - 0.05 <= w[1] < b]
        if not cap and AUTOW:  # no hand-corrected caption: re-transcribed words of this piece (hallucinations removed)
            for w in AUTOW:
                if t - 0.05 <= w['start'] < t + (b - a) and not BAD.search(w['w']):
                    words.append(dict(w=w['w'], start=w['start'], end=w['end']))
        if cap and ew:
            toks = cap.replace('_', ' ').split()
            span0, span1 = ew[0][1], ew[-1][2]
            for k_, tok in enumerate(toks):  # spread the corrected words over his real speech span (by word index)
                u0 = k_ / len(toks); u1 = (k_ + 1) / len(toks)
                i0 = min(len(ew) - 1, int(u0 * len(ew))); i1 = min(len(ew) - 1, int(u1 * len(ew) - 1e-6))
                ws0 = ew[i0][1] + (u0 * len(ew) - i0) * (ew[i0][2] - ew[i0][1])
                ws1 = ew[i1][1] + (u1 * len(ew) - i1) * (ew[i1][2] - ew[i1][1])
                words.append(dict(w=tok, start=round(t + max(0, ws0 - a), 2), end=round(t + max(0, min(b, ws1) - a), 2)))
        show = pc.get('show', 'screen')
        dd = db10(ep)[int(a * 100):int(b * 100)]
        env += [float(np.clip((np.max(dd[int(k * 100 / FPS):int((k + 1) * 100 / FPS)] if len(dd[int(k * 100 / FPS):int((k + 1) * 100 / FPS)]) else [-60]) + 45) / 30, 0, 1)) for k in range(int(round(d * FPS)))]
        env += [0.0] * int(round(GAP * FPS))
        if pc.get('hook'):
            hk = pc['hook']
            cues.append(dict(t=round(t, 3), d=round(d, 3), k='BeforeAfter', p=dict(file=PUB + f'ep{ep}.mp4', before=hk['before'], after=hk['after'], crop=hk['crop'], cropB=hk.get('cropB'), y=760)))
            show = 'none'
        if show == 'screen':
            src = pc.get('src', a)  # footage to show (default = the same moment he says it)
            keys = []
            if 'crop' in pc:
                keys.append(dict(t=0, **pc['crop']))
            else:
                c0 = cursor(ep, src + 0.3) or (638, 360)
                keys.append(dict(t=0, **crop_at(c0)))
                cl = clicks(ep, src, src + d)
                pts = [(ts - src - 0.4, xy, 520) for ts, xy in cl]
                for s2 in np.arange(src + 2.5, src + d - 0.5, 2.5):  # follow his cursor calmly between clicks
                    if all(abs((s2 - src) - p[0]) > 1.2 for p in pts):
                        c2 = cursor(ep, s2)
                        if c2: pts.append((s2 - src, c2, 640))
                for tk, xy, sw in sorted(pts):
                    if tk > 0.2: keys.append(dict(t=round(tk, 2), **crop_at(xy, sw)))
            marks = [dict(t=round(ts - src, 2), d=1.4, x=xy[0], y=xy[1], r=34, label='') for ts, xy in clicks(ep, src, src + d)] if pc.get('marks', True) else []
            # clicks the detector misses (e.g. the eyedropper): (abs time, x, y) in 1276x720 space
            marks += [dict(t=round(ts - src, 2), d=1.4, x=x, y=y, r=34, label='') for ts, x, y in pc.get('clicks', [])]
            marks.sort(key=lambda m: m['t'])
            dual = None
            if pc.get('dual'):
                top, bot = pc['dual']
                if top == 'auto':  # the panel around his cursor
                    c0 = cursor(ep, src + 0.5) or (280, 200)
                    sw = 560; sh = sw * DUAL_H / CARD_W
                    top = dict(sx=int(min(max(0, c0[0] - sw / 2), 1276 - sw)), sy=int(min(max(0, c0[1] - sh / 2), 720 - sh)), sw=sw)
                dual = dict(top=top, bottom=bot)  # marks are kept: drawn in whichever pane shows the click
            screens.append(dict(t=round(t, 3), d=round(d, 3), file=PUB + f'ep{ep}.mp4', **{'from': src}, keys=keys, marks=marks, y=pc.get('y', 740), dual=dual))
            for m in marks: sfx.append(dict(t=round(t + m['t'], 3), file='sfx/click.wav', vol=0.25))
        elif show == 'none':
            pass
        elif show.startswith('big:'):
            txt, _, sub = show[4:].partition('|')
            cues.append(dict(t=round(t, 3), d=round(d, 3), k='Big', p=dict(text=txt, sub=sub or None, ico=pc.get('ico'))))
        else:
            an = dict(pc.get('anim', {}))
            if pc.get('under'):  # animation small on top + his real screen under it (Aly: "حط سكرين ريكورد تحته علشان افهم")
                an['mini'] = True
                c = pc['under'] if pc['under'] != 'auto' else crop_at(cursor(ep, a + 0.3) or (638, 360), 560)
                screens.append(dict(t=round(t, 3), d=round(d, 3), file=PUB + f'ep{ep}.mp4', **{'from': pc.get('under_src', a)}, keys=[], marks=[], y=740,
                                    dual=dict(top=c, bottom=c), under=True))
            cues.append(dict(t=round(t, 3), d=round(max(d, 3.0), 3), k=show, p=an))
        if pc.get('step'):
            step += 1
            cues.append(dict(t=round(t + 0.1, 3), d=round(d - 0.1, 3), k='Step', p=dict(n=step, total=nsteps, text=pc['step'])))

        for pat, txt in pc.get('labels', []):
            hit = [w for w in EPW[ep] if a <= w[1] < b and pat in w[0]]
            if hit: cues.append(dict(t=round(t + hit[0][1] - a, 3), d=1.6, k='Label', p=dict(text=txt)))
        if pc.get('fix'):
            fx = pc['fix']
            cues.append(dict(t=round(t + fx.get('at', 0.3), 3), d=fx.get('d', round(d - 0.3, 2)), k='Fix', p=dict(text=fx['text'], src=fx['src'])))
        for kw in pc.get('kw', []):
            cues.append(dict(t=round(t + kw[2], 3), d=3.0, k='Kw', p=dict(en=kw[0], ar=kw[1])))
        if pc.get('key'):
            cues.append(dict(t=round(t + pc['key'][2], 3), d=round(min(3.5, d - pc['key'][2]), 3), k='Key', p=dict(keys=pc['key'][0], ar=pc['key'][1])))
        if pc.get('def'):
            cues.append(dict(t=round(t + 0.2, 3), d=round(d - 0.2, 3), k='Def', p=pc['def']))
        sfx.append(dict(t=round(t, 3), file='sfx/whoosh_1.wav', vol=0.12))
        t += d + GAP
    music = []
    if spec.get('new'):
        q = dict(SD.NEW[spec['new']]); vid = q.pop('vid', None)
        if vid: q['thumb'], q['qr'] = PUB + f'vids/{vid}.jpg', PUB + f'qr/{vid}.png'
        cues.append(dict(t=round(t, 3), d=6.5, k='New26', p=q))
        music.append(dict(t=round(t - 0.3, 3), d=7.0, file=PUB + 'music/lofi_coffee_shop.mp3', **{'from': 20}, vol=0.12))
        env += [0.0] * int(round(6.5 * FPS))
        t += 6.5
    cta_at = round(t + 0.1, 3)
    ch = CH[spec['chapter']]
    cta_d = SD.CTA_DUR
    props = dict(fps=FPS, duration=round(cta_at + cta_d, 3), look=spec['look'],
                 series=dict(no=spec['no'], total=SD.TOTAL, title=spec['title'].replace('*', '').replace('_', ' '), at=ch['time'], chap=spec['chapter']),
                 voice=voice, screens=screens, cues=cues, cta=dict(file=PUB + SD.CTA_FILE, at=cta_at, d=cta_d, qr=PUB + 'qr/course_full.png', vol=SD.CTA_VOL),
                 music=music, sfx=sfx, env=[round(v, 2) for v in env], words=words)
    out = PROJ / f'work/shorts/props_{spec["no"]:02d}.json'
    out.parent.mkdir(exist_ok=True)
    json.dump(props, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{spec["no"]:02d}', spec['title'], '| length', round(props['duration'], 1), 's | pieces', len(voice), '| voice level', round(target, 1), 'dB')


if __name__ == '__main__':
    for n in map(int, sys.argv[1:]): build(n)

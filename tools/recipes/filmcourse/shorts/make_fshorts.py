# Film-making course shorts -> work/shorts/props_NN.json      python make_fshorts.py 5 15 20
# Same recipe as the audio-course series (tools/recipes/audiocourse/shorts/make_shorts.py): his sentences fitted on the waveform (never
# inside a word), 0.12 s gaps, one voice level, composition `course-short` (look 'film', clapper logo). New here: hook piece + '⏪' label,
# scene props in SOURCE seconds (moved to each piece), `under` = scene on top + the film clip pane under it, one card across pieces.
import json, subprocess, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fs_data as SD

PROJ = Path(__file__).resolve().parents[2]
PUB = 'projects/filmcourse/'
SRC = PROJ / 'input/2026-11-06 14-39-41.mp4'
FPS, GAP = 30, 0.12
_t = json.load(open(PROJ / 'work/transcript.json', encoding='utf-8'))
EPW = [(w['w'].strip(), w['start'], w['end']) for s_ in _t['sentences'] for w in s_['words'] if w['w'].strip()]
CHS = [c for c in json.load(open(PROJ / 'work/chapters.json', encoding='utf-8'))['chapters'] if c.get('src') is not None]
import re as _re
BAD = _re.compile(r'اشتركوا|القناة|ترجمة|نانسي|المترجم|شكرا للمشاهدة')
_db = []


def full_at(s):
    """source second -> m:ss / h:mm:ss in the PUBLISHED full video (teaser + pages + separators before it)."""
    ch = [c for c in CHS if c['src'] <= s + 0.01][-1]
    t = int(ch['sep'] + 4 + (s - ch['src']))
    return f'{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}' if t >= 3600 else f'{t // 60}:{t % 60:02d}'


def db10():
    if not _db:
        f = PROJ / 'work/db10.npy'
        if not f.exists():
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(SRC), '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
            a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
            n = len(a) // 160
            np.save(f, (20 * np.log10(np.sqrt((a[: n * 160].reshape(n, 160) ** 2).mean(1)) + 1e-9)).astype(np.float32))
        _db.append(np.load(f))
    return _db[0]


def fit(a, b):
    """Edges on the waveform: start just before the first sound, end after the sound died; never more than a breath outside his words."""
    d = db10()
    i, j = int(a * 100), int(b * 100)
    loc = d[max(0, i - 300):j + 300]
    th = max(-45.0, float(np.percentile(loc, 15)) + 12)
    s = i
    while s > i - 60 and d[s - 1] > th: s -= 1
    while s < j and d[s] <= th: s += 1
    s = max(0, s - 6)
    e, q = j, 0
    while e < j + 120 and q < 15:
        q = q + 1 if d[e] <= th else 0
        e += 1
    e = e - 15 + 8
    prev_end = max([w[2] for w in EPW if w[2] <= a + 0.05] or [0])
    inside = [w for w in EPW if a - 0.05 <= w[1] < b - 0.08]
    last_end = max([w[2] for w in inside] or [b])
    nxt = min([w[1] for w in EPW if w[1] >= max(b, last_end - 0.02) and w[1] > a + 0.3] or [1e9])
    s = max(s, int((prev_end + 0.02) * 100))
    e = max(e, int((last_end + 0.12) * 100))
    e = min(e, int((nxt - 0.03) * 100))
    first_start = min([w[1] for w in inside] or [a])
    s = max(s, int((first_start - 0.15) * 100))
    e = min(e, int((max(last_end, b) + 0.30) * 100))
    return round(s / 100, 2), round(e / 100, 2)


def level(a, b):
    d = db10()[int(a * 100):int(b * 100)]
    sp = d[d > np.percentile(d, 40)]
    return float(10 * np.log10(np.mean(10 ** (sp / 10)))) if len(sp) else -30.0


def shift(anim, a):
    """scene props written in SOURCE seconds -> seconds from the start of this piece (values < 100 are already relative)."""
    o = json.loads(json.dumps(anim))
    mv = lambda t: round(t - a, 3) if t > 100 else t
    for k in ('modes', 'steps'):
        if k in o: o[k] = [[mv(x[0]), *x[1:]] for x in o[k]]
    for k in ('tags',):
        if k in o: o[k] = [dict(x, t=mv(x['t'])) for x in o[k]]
    if 'outB' in o: o['outB'] = mv(o['outB'])
    return o


def build(n):
    spec = SD.SHORTS[n]
    voice, screens, cues, sfx, env, words, cam = [], [], [], [], [], [], []
    t = 0.3
    plan = [(pc, *fit(pc['a'], pc['b'])) for pc in spec['pieces']]
    levels = [level(a, b) for _, a, b in plan]
    target = float(np.median(levels))
    caps = SD.CAP.get(n, [])
    wf = PROJ / f'work/shorts/words_{n:02d}.json'
    AUTOW = [w for w in (json.load(open(wf, encoding='utf-8')) if wf.exists() else []) if not BAD.search(w['w'])]
    kind = lambda q: ('none' if not 0 <= q < len(plan) else plan[q][0].get('show', 'under' if plan[q][0].get('under') else 'screen'))
    for k, ((pc, a, b), lv) in enumerate(zip(plan, levels)):
        d = b - a
        gain = round(float(10 ** ((target - lv) / 20)), 3)
        voice.append(dict(file=PUB + 'course.mp4', **{'from': a}, to=b, at=round(t, 3), gain=min(1.25, max(0.5, gain))))
        cam.append(dict(t=round(t, 3), d=round(d + GAP, 3), file=PUB + 'course.mp4', **{'from': a}, **SD.webcam(a)))  # Aly: his webcam square -> small round circle
        cap = caps[k] if k < len(caps) else None
        ew = [w for w in EPW if a - 0.05 <= w[1] < b]
        if cap == '':
            pass
        elif cap and ew:
            toks = cap.replace('_', ' ').split()
            if toks and toks[-1][-1] not in '.!?؟،': toks[-1] += '..'
            for k_, tok in enumerate(toks):
                u0 = k_ / len(toks); u1 = (k_ + 1) / len(toks)
                i0 = min(len(ew) - 1, int(u0 * len(ew))); i1 = min(len(ew) - 1, int(u1 * len(ew) - 1e-6))
                ws0 = ew[i0][1] + (u0 * len(ew) - i0) * (ew[i0][2] - ew[i0][1])
                ws1 = ew[i1][1] + (u1 * len(ew) - i1) * (ew[i1][2] - ew[i1][1])
                words.append(dict(w=tok, start=round(t + max(0, ws0 - a), 2), end=round(t + max(0, min(b, ws1) - a), 2)))
        else:
            for w in AUTOW:
                if t - 0.05 <= w['start'] < t + d: words.append(dict(w=w['w'], start=w['start'], end=w['end']))
        dd = db10()[int(a * 100):int(b * 100)]
        for q in range(int(round(d * FPS))):
            seg = dd[int(q * 100 / FPS):int((q + 1) * 100 / FPS)]
            env.append(float(np.clip(((np.max(seg) if len(seg) else -60) + 45) / 30, 0, 1)))
        env += [0.0] * int(round(GAP * FPS))
        show = kind(k)
        # one card across consecutive pieces of the same kind (never after the hook: the rewind is a new start)
        cin = kind(k - 1) == show and not pc.get('rew') and k > 0
        cout = kind(k + 1) == show and not plan[k + 1][0].get('rew') if k + 1 < len(plan) else False
        if show in ('screen', 'under'):
            src = pc.get('src', a)
            keys = [dict(t=0, **pc['crop'])] + [dict(t=round(zt - src, 2), **zc) for zt, zc in pc.get('zoom', [])]
            if cin and show == 'screen':
                prev = plan[k - 1][0]; pz = prev.get('zoom', [])
                keys = [dict(t=0, **(pz[-1][1] if pz else prev['crop'])), dict(t=0.45, **pc['crop'])] + keys[1:]
            dual = dict(top=pc['crop'], bottom=pc['crop']) if show == 'under' else None
            screens.append(dict(t=round(t, 3), d=round(d + (GAP if cout else 0), 3), file=PUB + 'course.mp4', **{'from': src}, keys=keys, marks=[], y=740,
                                dual=dual, under=show == 'under', cin=cin, cout=cout))
            if show == 'under' and pc.get('anim'):
                cues.append(dict(t=round(t, 3), d=round(d + (GAP if cout else 0), 3), k='PowerStairs', p=dict(shift(pc['anim'], a), under=True, cin=cin, cout=cout)))
        elif show.startswith('big:'):
            txt, _, sub = show[4:].partition('|')
            cues.append(dict(t=round(t, 3), d=round(d, 3), k='Big', p=dict(text=txt, sub=sub or None, ico=pc.get('ico'))))
        else:
            cin2 = cin or pc.get('cin', False)
            cues.append(dict(t=round(t, 3), d=round(max(d, 3.0) + (GAP if cout else 0), 3), k=show, p=dict(shift(pc.get('anim', {}), a), cin=cin2, cout=cout)))
        if pc.get('film'):
            cues.append(dict(t=round(t + 0.3, 3), d=round(min(d - 0.3, 5.0), 3), k='FilmTag', p=dict(pc['film'], x=40, y=1405 if show == 'under' else 1395)))
        if pc.get('rew'):
            cues.append(dict(t=round(t, 3), d=1.3, k='Label', p=dict(text='⏪ من الأول', img=None)))
        for lb in pc.get('labels', []):
            hit = [w for w in EPW if a <= w[1] < b and lb[0] in w[0]]
            if hit: cues.append(dict(t=round(t + hit[0][1] - a, 3), d=1.6, k='Label', p=dict(text=lb[1], img=lb[2] if len(lb) > 2 else None)))
        for off, txt, img, dd_ in pc.get('lab', []):
            cues.append(dict(t=round(t + off, 3), d=dd_, k='Label', p=dict(text=txt, img=img)))
        for kw in pc.get('kw', []):
            cues.append(dict(t=round(t + kw[2], 3), d=3.0, k='Kw', p=dict(en=kw[0], ar=kw[1])))
        if not cin: sfx.append(dict(t=round(t, 3), file='sfx/whoosh_1.wav', vol=0.12))
        t += d + GAP
    labs = sorted([c for c in cues if c['k'] == 'Label'], key=lambda c: c['t'])
    for c, n_ in zip(labs, labs[1:]):
        c['d'] = round(max(0.5, min(c['d'], n_['t'] - c['t'] - 0.05)), 3)
    end_at = round(t + 0.1, 3)
    end = dict(at=end_at, d=SD.END_D, thumb=PUB + 'pics/film_course_thumb.jpg', qr=PUB + 'qr/film_course.png', title='الكورس الكامل على القناة')
    dur = end_at + SD.END_D
    body = [pc for pc in spec['pieces'] if pc.get('rew')] or spec['pieces']
    props = dict(fps=FPS, duration=round(dur, 3), look='film', brand=dict(logo='film', name='كورس Film making'), src=dict(w=1280, h=720),
                 footer=dict(face=PUB + 'pics/ch_face.png', name=PUB + 'pics/ch_name.png'),
                 series=dict(no=spec['no'], total=SD.TOTAL, title=spec['title'].replace('*', '').replace('_', ' '), at=full_at(body[0]['a']), chap=spec['chapter']),
                 voice=voice, cam=cam, screens=screens, cues=cues, cta=None, end=end, music=[], sfx=sfx, env=[round(v, 2) for v in env], words=words)
    out = PROJ / f'work/shorts/props_{n:02d}.json'
    out.parent.mkdir(exist_ok=True)
    json.dump(props, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{n:02d}', spec['title'], '| length', round(props['duration'], 1), 's | at', props['series']['at'], '| voice', round(target, 1), 'dB')
    for (pc, a, b) in plan:
        print('   ', pc['a'], pc['b'], '->', a, b, '|', ' '.join(w[0] for w in EPW if a - 0.05 <= w[1] < b)[:140])


if __name__ == '__main__':
    for n in map(int, sys.argv[1:]): build(n)

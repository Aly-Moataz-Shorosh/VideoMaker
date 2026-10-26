# Shorts series from the audio course (Aly 2026-10-26) -> work/shorts/props_<NN>.json   python make_shorts.py 1 2 ...
# Same recipe as the Premiere series (tools/recipes/premierecourse/shorts): pieces = his sentences fitted on the waveform (never inside a
# word), 0.12 s gaps, one voice level per short, composition `course-short`. Differences: ONE source (the 1280x720 session), no cursor
# detector (crops + clicks by hand from frame_sheet.py), end card = course thumbnail + QR (his new CTA clip goes after it when it comes).
import json, subprocess, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shorts_data as SD

PROJ = Path(__file__).resolve().parents[2]
PUB = 'projects/audio/'
SRC = PROJ / 'input/2021-03-28 20-26-18_1.mp4'
FPS, GAP = 30, 0.12
_t = json.load(open(PROJ / 'work/transcript.json', encoding='utf-8'))
EPW = [(w['w'].strip(), w['start'], w['end']) for s_ in _t['sentences'] for w in s_['words'] if w['w'].strip()]
CH = {c['n']: c for c in json.load(open(PROJ / 'work/chapters.json', encoding='utf-8'))}
import re as _re
BAD = _re.compile(r'اشتركوا|القناة|ترجمة|نانسي|المترجم|شكرا للمشاهدة')
_db = []


def db10():
    """10 ms RMS dB of the session (cached as .npy)."""
    if not _db:
        f = PROJ / 'work/db10.npy'
        if not f.exists():
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(SRC), '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout
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
    e = min(e, int((max(last_end, b) + 0.30) * 100))  # b may sit after his words on purpose (a sound demo plays)
    return round(s / 100, 2), round(e / 100, 2)


def level(a, b):
    d = db10()[int(a * 100):int(b * 100)]
    sp = d[d > np.percentile(d, 40)]
    return float(10 * np.log10(np.mean(10 ** (sp / 10)))) if len(sp) else -30.0


def build(n):
    spec = SD.SHORTS[n]
    voice, screens, cues, sfx, env, words = [], [], [], [], [], []
    t = 0.3
    plan = [(pc, *((pc['a'], pc['b']) if pc.get('raw') else fit(pc['a'], pc['b']))) for pc in spec['pieces']]  # raw = exact edges (a sound demo before his words)
    levels = [level(a, b) for _, a, b in plan]
    target = float(np.median([lv for (pc, _, _), lv in zip(plan, levels) if not pc.get('raw')] or levels))  # a raw demo (noise / silence) never sets the voice level
    caps = SD.CAP.get(n, SD.CAP.get(spec['no'], []))
    wf = PROJ / f'work/shorts/words_{spec["no"]:02d}.json'
    AUTOW = [w for w in (json.load(open(wf, encoding='utf-8')) if wf.exists() else []) if not BAD.search(w['w'])]
    step, nsteps = 0, sum(1 for pc, _, _ in plan if pc.get('step'))
    for k, ((pc, a, b), lv) in enumerate(zip(plan, levels)):
        d = b - a
        gain = 1.0 if pc.get('raw') else round(float(10 ** ((target - lv) / 20)), 3)  # the demo plays as it was in the session
        voice.append(dict(file=PUB + 'course.mp4', **{'from': a}, to=b, at=round(t, 3), gain=min(1.25, max(0.5, gain))))
        cap = caps[k] if k < len(caps) else None
        ew = [w for w in EPW if a - 0.05 <= w[1] < b]
        if cap == '':  # a sound demo plays, nothing to caption
            pass
        elif cap and ew:  # corrected words spread over his real speech span
            toks = cap.replace('_', ' ').split()
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
        show = pc.get('show', 'screen')
        isscr = lambda q: 0 <= q < len(plan) and plan[q][0].get('show', 'screen') == 'screen'
        cin, cout = isscr(k - 1), isscr(k + 1)  # one continuous card through screen pieces (Aly: one video, not separate shots)
        if show == 'screen':
            src = pc.get('src', a)
            keys = [dict(t=0, **pc['crop'])] + [dict(t=round(zt - src, 2), **zc) for zt, zc in pc.get('zoom', [])]
            if cin:  # glide from where the last piece ended to this crop
                prev = plan[k - 1][0]; pz = prev.get('zoom', [])
                keys = [dict(t=0, **(pz[-1][1] if pz else prev['crop'])), dict(t=0.45, **pc['crop'])] + keys[1:]
            marks = sorted([dict(t=round(c[0] - src, 2), d=1.4, x=c[1], y=c[2], r=26, w=(c[3] if len(c) > 3 else 0), h=(c[4] if len(c) > 4 else 0), label='') for c in pc.get('clicks', [])], key=lambda m: m['t'])  # (t, x, y[, w, h]) w/h = size of the clicked word
            screens.append(dict(t=round(t, 3), d=round(d + (GAP if cout else 0), 3), file=PUB + 'course.mp4', **{'from': src}, keys=keys, marks=marks, y=740, dual=None, cin=cin, cout=cout))
            for m in marks: sfx.append(dict(t=round(t + m['t'], 3), file='sfx/click.wav', vol=0.25))
        elif show.startswith('big:'):
            txt, _, sub = show[4:].partition('|')
            cues.append(dict(t=round(t, 3), d=round(d, 3), k='Big', p=dict(text=txt, sub=sub or None, ico=pc.get('ico'))))
        else:
            cues.append(dict(t=round(t, 3), d=round(max(d, 3.0), 3), k=show, p=dict(pc.get('anim', {}))))
        if pc.get('bars'):
            cues.append(dict(t=round(t, 3), d=round(d, 3), k='Bars', p={}))
        if pc.get('step'):
            step += 1
            cues.append(dict(t=round(t + 0.1, 3), d=round(d - 0.1, 3), k='Step', p=dict(n=step, total=nsteps, text=pc['step'])))
        for lb in pc.get('labels', []):  # (word, text[, fluent picture]) shown when he says the word
            hit = [w for w in EPW if a <= w[1] < b and lb[0] in w[0]]
            if hit: cues.append(dict(t=round(t + hit[0][1] - a, 3), d=1.6, k='Label', p=dict(text=lb[1], img=lb[2] if len(lb) > 2 else None)))
        for off, txt, img, dd in pc.get('lab', []):  # (offset, text, fluent picture, seconds) at a fixed moment (a demo plays, no words)
            cues.append(dict(t=round(t + off, 3), d=dd, k='Label', p=dict(text=txt, img=img)))
        for kw in pc.get('kw', []):
            cues.append(dict(t=round(t + kw[2], 3), d=3.0, k='Kw', p=dict(en=kw[0], ar=kw[1])))
        if pc.get('key'):
            cues.append(dict(t=round(t + pc['key'][2], 3), d=round(min(3.5, d - pc['key'][2]), 3), k='Key', p=dict(keys=pc['key'][0], ar=pc['key'][1])))
        if not (show == 'screen' and cin): sfx.append(dict(t=round(t, 3), file='sfx/whoosh_1.wav', vol=0.12))
        t += d + GAP
    labs = sorted([c for c in cues if c['k'] == 'Label'], key=lambda c: c['t'])
    for c, n_ in zip(labs, labs[1:]):  # big labels never on top of each other: each one is gone before the next one comes (reel 29 overlap)
        c['d'] = round(max(0.5, min(c['d'], n_['t'] - c['t'] - 0.05)), 3)
    end_at = round(t + 0.1, 3)
    end = dict(at=end_at, d=SD.END_D, thumb=PUB + 'pics/audio_course_thumb.jpg', qr=PUB + 'qr/audio_course.png', title='الكورس الكامل على القناة')
    dur = end_at + SD.END_D
    cta = None
    if SD.CTA_FILE:
        cta = dict(file=PUB + SD.CTA_FILE, at=round(dur, 3), d=SD.CTA_DUR, qr=PUB + 'qr/audio_course.png', thumb=PUB + 'pics/audio_course_thumb.jpg', word=SD.CTA_WORD, vol=1.0)
        dur += SD.CTA_DUR
    props = dict(fps=FPS, duration=round(dur, 3), look='sound', brand=dict(logo='wave', name='أسرار الصوت'), src=dict(w=1280, h=720),
                 footer=dict(face=PUB + 'pics/ch_face.png', name=PUB + 'pics/ch_name.png'),
                 series=dict(no=spec['no'], total=SD.TOTAL, title=spec['title'].replace('*', '').replace('_', ' '), at=spec.get('at', CH[spec['chapter']]['time']), chap=spec['chapter']),
                 voice=voice, screens=screens, cues=cues, cta=cta, end=end, music=[], sfx=sfx, env=[round(v, 2) for v in env], words=words)
    out = PROJ / f'work/shorts/props_{spec.get("tag", "%02d" % spec["no"])}.json'
    out.parent.mkdir(exist_ok=True)
    json.dump(props, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{spec["no"]:02d}', spec['title'], '| length', round(props['duration'], 1), 's | pieces', len(voice), '| voice level', round(target, 1), 'dB')
    for (pc, a, b) in plan:
        print('   ', pc['a'], pc['b'], '->', a, b, '|', ' '.join(w[0] for w in EPW if a - 0.05 <= w[1] < b)[:150])


if __name__ == '__main__':
    for n in map(int, sys.argv[1:]): build(n)

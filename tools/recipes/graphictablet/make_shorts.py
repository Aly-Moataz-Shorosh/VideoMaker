"""Graphic tablet shorts (2026-10-21, style 10 glass-face, end = QR of the full video like style 11). Aly picked 6, 3, 5, 2, 7.
Run: python work/scripts/make_shorts.py 6 3 5 2 7 [--nocam]
 -> motion-library/public/projects/<code>/short_N.json, cam_N.mp4 (his frames of the kept pieces, frame-exact), voice_N.wav, qr.png
Voice = his original audio, GAIN ONLY (per sentence to one level, raw music pieces at a fixed -8 dB), never cleaned.
After building: the PICTURE gate (cam_N.mp4 frames vs the source at every piece) must pass before rendering."""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8')

W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
CODE = P.name
PJ = f'projects/{CODE}/'
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
SRC = P / 'input' / 'Uc47QvWaocs.mp4'
FPS = 30
TAIL = 3.0  # end card (QR) after his last word
from shorts_data import SHORTS, FIX, PIP, URL
from edges import fit
import level_voice as LV

# ---------- words: Whisper transcript, with the unboxing part (music under him) re-transcribed (unbox.txt) ----------
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
WORDS = []
for s in tr['sentences']:
    for i, w in enumerate(s['words']):
        if not (494.0 <= w['start'] < 664.0):
            WORDS.append({**w, 'sid': s['id'], 'i': i})
U = {'U1': (494.0, 606.0), 'U2': (616.0, 633.0)}
lines = open(W / 'unbox.txt', encoding='utf8').read().splitlines()
for ln in lines:
    if '@' not in ln:
        continue
    toks = [t.rsplit('@', 1) for t in ln.split()]
    t0 = float(toks[0][1])
    sid = next(k for k, (a, b) in U.items() if a <= t0 < b)
    for i, (w, t) in enumerate(toks):
        WORDS.append({'w': w, 'start': float(t), 'end': float(t) + 0.3, 'sid': sid, 'i': i})
WORDS.sort(key=lambda w: w['start'])
for k in range(len(WORDS) - 1):  # unboxing words have no end time: up to the next word (max 0.5 s)
    if WORDS[k]['sid'].startswith('U'):
        WORDS[k]['end'] = min(WORDS[k]['start'] + 0.5, WORDS[k + 1]['start'])
LV._bounds = sorted({w['start'] for w in WORDS if w['i'] == 0})
SENT = {}
for w in WORDS:
    SENT.setdefault(w['sid'], []).append(w)


def caption_text(w):
    """his real word for Whisper word w ('' = hide)"""
    fx = FIX.get(w['sid'])
    if fx is None:
        return w['w']
    new = fx.split()
    if len(new) != len(SENT[w['sid']]):
        return None  # spread later
    x = new[w['i']]
    return '' if x == '--' else x


def span(t0, t1, a_force=None, b_force=None):
    i = min(range(len(WORDS)), key=lambda k: abs(WORDS[k]['start'] - t0))
    j = min(range(len(WORDS)), key=lambda k: abs(WORDS[k]['start'] - t1))
    prev = WORDS[i - 1]['end'] if i > 0 else None
    nxt = WORDS[j + 1]['start'] if j + 1 < len(WORDS) else None
    a, b, rep = fit(WORDS[i]['start'], WORDS[j]['end'], prev, nxt)
    if a_force: a = a_force; rep += f' START FORCED {a_force}'
    if b_force: b = b_force; rep += f' END FORCED {b_force}'
    print('   ', WORDS[i]['w'], '…', WORDS[j]['w'], rep)
    return [a, b], WORDS[i:j + 1]


def frames_exact(segs):
    """round every piece to whole frames on the timeline (no drift between picture and voice)"""
    tl = 0
    for s in segs:
        s['src'] = round(s['src'] * FPS) / FPS  # start on the same frame the camera is cut at
        n = max(1, round(s['len'] * FPS))
        s['tl'] = tl / FPS; s['n'] = n; s['len'] = n / FPS; tl += n
    return tl / FPS


def build(n):
    S = SHORTS[n]
    print(f'== short {n} ({S["slug"]})')
    segs, kept = [], []
    for p in S['pieces']:
        if p[0] == 'raw':
            segs.append({'src': p[1], 'len': p[2] - p[1], 'raw': True, 'tag': 'raw'}); kept.append([]); print('    RAW', p[1], p[2])
        else:
            (a, b), ws = span(*p[1:])
            segs.append({'src': a, 'len': b - a, 'raw': False, 'tag': p[0]}); kept.append(ws)
    main_len = frames_exact(segs)
    dur = round(main_len + TAIL, 3)

    def to_tl(t, lo=0.0):
        """source second -> timeline second, first piece at/after timeline `lo` that holds it (a hook may repeat a range)"""
        best = None
        for s in segs:
            if s['tl'] + s['len'] < lo - 0.01:
                continue
            if s['src'] - 0.02 <= t <= s['src'] + s['len'] + 0.02:
                return max(lo, s['tl'] + min(max(t - s['src'], 0), s['len']))
            for e, v in ((abs(t - s['src']), s['tl']), (abs(t - s['src'] - s['len']), s['tl'] + s['len'])):
                if best is None or e < best[0]:
                    best = (e, max(lo, v))
        if best and best[0] <= 6.0:  # a time inside a cut gap snaps to the nearest kept edge
            return best[1]
        raise ValueError(f'{t} outside the pieces of short {n}')

    # ---------- scenes ----------
    chain = [sc for sc in S['scenes'] if not sc.get('over')]
    scenes, cams, lo = [], [], 0.0
    starts = {}
    for sc in S['scenes']:
        if sc.get('over'):
            continue
        a = to_tl(sc['at'], lo) if starts else 0.0; lo = a; starts[id(sc)] = a
    for sc in S['scenes']:
        if sc.get('over'):
            # overlay: search from the scene it sits on (the last chained scene that starts before it in the list)
            idx = S['scenes'].index(sc)
            base = max([starts[id(x)] for x in S['scenes'][:idx] if id(x) in starts] + [0.0])
            a = to_tl(sc['at'], base)
            b = to_tl(sc['to'], a)
        else:
            a = starts[id(sc)]
            k = chain.index(sc)
            b = starts[id(chain[k + 1])] if k + 1 < len(chain) else main_len
        props = {kk: v for kk, v in sc.items() if kk not in ('t', 'at', 'to', 'over', 'cam', 'camk', 'items', 'tiles')}
        fr = lambda t: max(0, round((to_tl(t, a) - a) * FPS))
        for key in ('a', 'b', 'cheap', 'kb', 'pen', 'free', 'decide', 'regret', 'mouse', 'sense', 'lines', 'map'):
            if key in props:
                props[key] = fr(props[key])
        for key in ('strokes', 'pins'):
            if key in props:
                props[key] = [fr(t) for t in props[key]]
        if 'tiles' in sc:
            props['tiles'] = [{**t, 'at': fr(t['at'])} for t in sc['tiles']]
        if 'items' in sc:
            items = []
            for itm in sc['items']:
                d = {kk: v for kk, v in itm.items() if kk not in ('t', 'until')}
                d['at'] = fr(itm['t'])
                if 'until' in itm:
                    d['out'] = fr(itm['until'])
                items.append(d)
            props['items'] = items
        if sc['t'] == 'tb_clip':
            props['cam'] = PJ + f'cam_{n}.mp4'; props['camAt'] = round(a * FPS)
        scenes.append({'t': sc['t'], 'at': round(a, 3), 'dur': round(b - a, 3), 'layer': 'front', 'props': props})
        if 'cam' in sc:
            cams.append((a, sc['cam']))
        for t, m in sc.get('camk', []):
            cams.append((to_tl(t, a), m))
    # his picture-in-picture inserts push him right -> 'tlowr' while they are on (only where the mode is 'tlow')
    for pa, pb in PIP:
        for s in segs:
            x0, x1 = max(pa, s['src']), min(pb, s['src'] + s['len'])
            if x1 - x0 > 0.3:
                cams.append((s['tl'] + x0 - s['src'], 'PIP+')); cams.append((s['tl'] + x1 - s['src'], 'PIP-'))
    cams.sort(key=lambda c: c[0])
    keys, base, pip = [], 'tlow', 0
    for t, m in cams:
        if m == 'PIP+': pip += 1
        elif m == 'PIP-': pip -= 1
        else: base = m
        mode = 'tlowr' if pip > 0 and base == 'tlow' else base
        if not keys or keys[-1]['m'] != mode:
            keys.append({'t': round(t, 3), 'm': mode})
    keys.append({'t': round(main_len, 3), 'm': 'hide'})
    if keys[0]['t'] > 0:
        keys.insert(0, {'t': 0, 'm': 'tlow'})
    # end card (QR) over the last second of his talk + the tail
    scenes.append({'t': 'tb_end', 'at': round(main_len - 0.6, 3), 'dur': round(TAIL + 0.6, 3), 'layer': 'front', 'props': {'qr': PJ + 'qr.png', 'thumb': PJ + 'thumb.jpg'}})

    # ---------- captions (his real words) ----------
    words = []
    for s, ws in zip(segs, kept):
        if not ws:
            continue
        a, b = s['src'], s['src'] + s['len']
        by = {}
        for w in ws:
            by.setdefault(w['sid'], []).append(w)
        for sid, group in by.items():
            texts = [caption_text(w) for w in group]
            if None in texts:  # different word count: spread his words over the kept part (only whole sentences here)
                new = [x for x in FIX[sid].split() if x != '--']
                if len(group) != len(SENT[sid]):
                    print('  !! partial sentence with a word-count fix', sid)
                a0, b0 = group[0]['start'], group[-1]['end']
                tot = sum(len(x) + 1 for x in new); t = a0
                for x in new:
                    d = (b0 - a0) * (len(x) + 1) / tot
                    words.append({'w': x, 'start': round(s['tl'] + max(0, t - a), 3), 'end': round(s['tl'] + min(b - a, t + d - a), 3)}); t += d
                continue
            for w, x in zip(group, texts):
                if x:
                    words.append({'w': x, 'start': round(s['tl'] + max(0, w['start'] - a), 3), 'end': round(s['tl'] + min(b - a, max(0.05, w['end'] - a)), 3)})
    words.sort(key=lambda w: w['start'])

    # ---------- sound effects: whoosh on scene changes, pop on every pill/card, special sounds ----------
    L = 'sfx/'
    sfx = []
    for i, s in enumerate(scenes):
        if s['at'] > 0.3 and s['t'] != 'tb_end':
            sfx.append({'file': L + f'whoosh_{i % 3 + 1}.wav', 'at': round(max(0, s['at'] - 0.1), 3), 'vol': 0.35})
        p = s['props']
        for j, itm in enumerate(p.get('items', [])):
            if itm['k'] in ('pill', 'card', 'mark', 'logo', 'word', 'emoji', 'tablet', 'monitor', 'pen') and itm['at'] < s['dur'] * FPS:
                snd = 'buzz_wrong' if itm['k'] == 'mark' and not itm.get('ok') else 'pop_%d' % (j % 3 + 1)
                sfx.append({'file': L + snd + '.wav', 'at': round(s['at'] + itm['at'] / FPS, 3), 'vol': 0.3})
        for t in p.get('tiles', []):
            sfx.append({'file': L + 'tick.wav', 'at': round(s['at'] + t['at'] / FPS, 3), 'vol': 0.4})
        if s['t'] == 'tb_check' and p.get('decide', 99999) < s['dur'] * FPS:
            sfx.append({'file': L + 'ding.wav', 'at': round(s['at'] + p['decide'] / FPS, 3), 'vol': 0.4})
        if s['t'] == 'tb_math':
            sfx.append({'file': L + 'typing.wav', 'at': round(s['at'] + 0.2, 3), 'vol': 0.4, 'dur': 1.8})
            if p.get('pen', 99999) < s['dur'] * FPS:
                sfx.append({'file': L + 'magic.wav', 'at': round(s['at'] + p['pen'] / FPS, 3), 'vol': 0.35})
        if s['t'] == 'tb_rewind':
            sfx.append({'file': L + 'tape.wav', 'at': s['at'], 'vol': 0.45, 'dur': 0.9})
        if s['t'] == 'tb_end':
            sfx.append({'file': L + 'magic.wav', 'at': round(s['at'] + 0.6, 3), 'vol': 0.4})
    for k in keys[1:]:  # the frame itself moves (cadre change) -> soft swish (Aly: whoosh only on cadre moves)
        sfx.append({'file': L + 'swish.wav', 'at': k['t'], 'vol': 0.22})

    # ---------- voice: his original audio, gain only ----------
    if LV._src is None:
        LV._src = LV.rd(SRC)
    SR = LV.SR; parts, log = [], []
    for s in segs:
        a = s['src']
        x = LV._src[int(a * SR):int(a * SR) + int(round(s['len'] * SR))].copy()
        if s['raw']:
            y = x * 10 ** (-8 / 20); fade = int(0.2 * SR); log.append('raw')
        else:
            y, gs = LV.level(x, [int((t - a) * SR) for t in LV._bounds if a < t < a + s['len']]); fade = int(0.012 * SR); log.append(gs)
        y[:fade] *= np.linspace(0, 1, fade); y[-fade:] *= np.linspace(1, 0, fade)
        parts.append(y)
    parts.append(np.zeros(int(TAIL * SR), np.float32))
    PUB.mkdir(parents=True, exist_ok=True)
    out = PUB / f'voice_{n}.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-c:a', 'pcm_s16le', str(out)],
                   input=np.concatenate(parts).astype(np.float32).tobytes(), check=True)
    print('  voice gains:', log)

    # ---------- camera: his frames of the kept pieces, frame-exact (select by frame number, never -ss/-t drift) ----------
    cam = PUB / f'cam_{n}.mp4'
    if '--nocam' not in sys.argv:
        # one decode, split per piece, trim by FRAME number, concat in the short's order (a hook may come from later in his video)
        k = len(segs)
        fc = f'[0:v]split={k}' + ''.join(f'[i{j}]' for j in range(k)) + ';'
        fc += ''.join(f'[i{j}]trim=start_frame={round(s["src"] * FPS)}:end_frame={round(s["src"] * FPS) + s["n"]},setpts=PTS-STARTPTS[v{j}];' for j, s in enumerate(segs))
        fc += ''.join(f'[v{j}]' for j in range(k)) + f'concat=n={k}:v=1:a=0,settb=1/{FPS},setpts=N[v]'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(SRC), '-filter_complex', fc, '-map', '[v]', '-an', '-r', str(FPS),
                        '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-g', '15', '-pix_fmt', 'yuv420p', str(cam)], check=True)
    nb = int(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets',
                             '-of', 'csv=p=0', str(cam)], capture_output=True, text=True).stdout.strip())
    want = sum(s['n'] for s in segs)
    print(f'  cam_{n}.mp4 {nb} frames (pieces {want})' + ('' if nb == want else '  !! LENGTH MISMATCH'))

    props = {'fps': FPS, 'duration': dur, 'voice': PJ + f'voice_{n}.wav', 'segs': [{'src': 0, 'tl': 0, 'len': dur}], 'words': words, 'aly': [],
             'scenes': scenes, 'sfx': sfx, 'look': 'glass', 'capBottom': 0.07, 'sfxGain': 1.0,
             'cam': {'file': PJ + f'cam_{n}.mp4', 'keys': keys}}
    json.dump(props, open(PUB / f'short_{n}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    json.dump([{'src': s['src'], 'tl': s['tl'], 'n': s['n'], 'raw': s['raw']} for s in segs], open(W / f'segs_{n}.json', 'w'), indent=1)
    print(f'  short {n}: {main_len:.1f}s + end {TAIL}s = {dur:.1f}s ({int(dur // 60)}:{dur % 60:04.1f}) | {len(segs)} pieces, {len(scenes)} scenes, {len(words)} words')
    for s in scenes:
        print(f"     {s['t']:9s} {s['at']:6.2f} +{s['dur']:5.2f}")
    print('  cam keys:', ' '.join(f"{k['t']:.1f}:{k['m']}" for k in keys))
    assert dur < 180, 'a short must stay under 3:00'


if __name__ == '__main__':
    import qrcode
    PUB.mkdir(parents=True, exist_ok=True)
    qrcode.make(URL, border=2).save(PUB / 'qr.png')
    for a in sys.argv[1:]:
        if a.isdigit():
            build(int(a))

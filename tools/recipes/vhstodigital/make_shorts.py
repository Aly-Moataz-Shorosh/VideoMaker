"""4 faceless-first vertical shorts (look 'vhs') from Aly's 'VHS لـ Digital' video (2026-10-09, shorts 1, 2, 4, 8 of my list).
Aly: the whole short is smart motion graphics / animated infographics (real footage only when showing how a real thing
looks), his cut-out appears only at a few moments, every short ends with his comment-keyword CTA.
Inputs : work/ranges.json (snap_ranges.py), work/faces.json (faces.py), work/transcript.json, work/fix.json, voice.m4a
Output : motion-library/public/projects/<code>/short_<n>.json  (composition 'film-short', src/film/*)
Run    : python work/scripts/make_shorts.py [n ...]
Render : cd motion-library && npx remotion render out/bundle film-short ../projects/<code>/output/short_<n>.mp4 --props=...
Scene tuple: (scene id, src start, src end, layer, props, beats{name: src second}) — beats become seconds from scene start."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
CODE = P.name
PJ = f'projects/{CODE}/'
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
FACES = {int(k): v for k, v in json.load(open(W / 'faces.json', encoding='utf8')).items()} if (W / 'faces.json').exists() else {}
FIX = json.load(open(W / 'fix.json', encoding='utf8'))
from edges import fit
from level_voice import build as build_voice
_words = [w for s in tr['sentences'] for w in s['words']]
KEEP = set()  # ids of the words inside the spans of the short being built (captions = exactly these words)


def span(t0, t1):
    """Range from the word starting at t0 to the word starting at t1 (Whisper starts), edges fitted on the waveform."""
    i = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t0))
    j = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t1))
    prev = _words[i - 1]['end'] if i > 0 else None
    nxt = _words[j + 1]['start'] if j + 1 < len(_words) else None
    a, b, rep = fit(_words[i]['start'], _words[j]['end'], prev, nxt)
    KEEP.update(id(w) for w in _words[i:j + 1])
    print('   ', _words[i]['w'], '…', _words[j]['w'], rep)
    return [a, b]


# Ranges = word spans (first word start, last word start). Edges are fitted on the audio waveform (work/scripts/edges.py).
SPANS = {
    1: [(797.65, 798.95), (94.46, 116.32), (818.27, 835.43), (835.65, 862.37), (686.99, 692.31), (775.55, 780.87)],
    2: [(805.49, 809.01), (25.16, 36.08), (811.99, 817.91), (41.28, 43.14), (702.91, 707.89)],
    4: [(148.98, 163.66), (329.45, 337.41), (351.61, 354.23), (478.32, 485.54), (584.42, 595.74), (686.99, 692.31), (761.39, 769.15)],
    8: [(1.54, 20.77), (75.80, 80.86), (138.16, 142.02), (790.07, 794.19), (901.43, 903.17)],
}
CTA_KEEP = (0.0, 7.6)
CTA_FIX = {'بتحول': 'بتتحوّل', 'وهبعث': 'وهبعتلك', 'لك': '', 'ان': 'إن'}
CHAIN = {'vcr': 586.5, 'av': 588.34, 'conv': 589.92, 'hdmi': 591.22, 'cap': 592.26, 'usb': 594.04, 'pc': 595.26}

SHORTS = {
    1: {  # both ways, from his summary at the end of the video (Aly review 1)
        'scenes': [
            ('vt', 797.6, 799.7, 'back', {'title': 'عايز تحوّل شرايطك لـ *ديجيتال*؟'}, {}),
            ('v1_idea', 94.4, 105.9, 'front', {}, {'cam': 99.76, 'pc': 104.44}),
            ('v1_hours', 105.9, 116.8, 'front', {}, {'n': 110.06, 'copy': 114.9}),
            ('v4_easy', 818.2, 829.9, 'front', {'tag': 'الطريقة 1 (الأشهر): إيزي كاب'}, {'famous': 819.33, 'usb': 829.41}),
            ('v1_soft', 829.9, 835.6, 'front', {}, {'obs': 832.75, 'dvd': 833.53}),
            ('vt', 835.6, 840.9, 'back', {'title': 'الطريقة 2: *طريقتي أنا*', 'stamp': 'أحسن مليون مرة'}, {'stamp': 840.35}),
            ('v1_result', 840.9, 843.6, 'front', {'tag': 'الجودة أحسن بكتير ✓'}, {'color': 841.55, 'hd': 99}),
            ('v1_convert', 843.6, 850.75, 'front', {'clip': 12}, {'rca': 847.57, 'box': 848.65, 'hdmi': 850.13}),
            ('v1_chain', 850.75, 862.9, 'front', {}, {'vcr': 850.8, 'av': 851.0, 'conv': 851.2, 'hdmi': 854.39, 'cap': 856.71, 'usb': 857.99, 'pc': 858.43}),
            ('v4_versus', 686.9, 693.4, 'front', {}, {'x': 689.0, 'win': 690.65}),
            ('v8_save', 775.4, 781.5, 'front', {'tag': 'أي شريط فيديو عندك', 'icons': False, 'label': 'VHS'}, {'dig': 777.5}),
        ],
        'aly': [(797.6, 799.5, 'big'), (835.9, 840.9, 'big')],
        'partial': {'S201': 'انتوا واخدين بالكم دلوقتي', 'S273': ''},
    },
    2: {  # 30 -> 300 EGP; many tapes = costly; privacy -> at home
        'scenes': [
            ('vt', 805.3, 809.8, 'back', {'title': 'زمان كان بـ *30 جنيه*… دلوقتي؟', 'stamp': '300 جنيه!'}, {'stamp': 809.01}),
            ('v2_shop', 24.9, 36.7, 'front', {}, {'give': 27.84, 'done': 34.6, 'costly': 35.78}),
            ('v2_price', 811.8, 814.5, 'front', {}, {'many': 811.9}),
            ('v2_privacy', 814.5, 818.4, 'front', {}, {'eyes': 814.85, 'lock': 817.57}),
            ('vt', 41.1, 43.7, 'back', {'title': 'يبقى الحل التاني *هو الأفضل*'}, {}),
            ('v2_home', 702.7, 708.4, 'front', {}, {'vcr': 703.6, 'pc': 704.5, 'best': 707.25}),
        ],
        'aly': [(805.3, 809.5, 'big'), (41.1, 43.6, 'big')],
        'partial': {'S001': 'الحل الأسهل والأول هو إن انت تاخد الشريط والفلوس بتاعتك وتنزل لأول واحد بتاع تصوير وتقوله',
                    'S002': 'أنا عايز أحوّل الشريط بتاعي لنسخة ديجيتال. أول ما هتعمل الحركة دي انت كده خلّصت اللي عليك. ده الحل المكلّف. يبقى الحل التاني هو الأفضل اللي هنعمله.'},
    },
    4: {  # EasyCap (the famous way) vs his way
        'scenes': [
            ('vt', 148.8, 153.62, 'back', {'title': 'الطريقة الأشهر… _مش الأحسن_ جودة'}, {}),
            ('v4_easy', 153.62, 164.4, 'front', {}, {'famous': 154.5, 'usb': 163.28}),
            ('v4_problem', 329.2, 354.8, 'front', {}, {'bw': 331.69, 'cut': 353.67}),
            ('v4_mine', 478.1, 485.9, 'front', {}, {'go': 480.98}),
            ('v1_chain', 584.2, 596.2, 'front', {}, CHAIN),
            ('v4_versus', 686.9, 766.2, 'front', {}, {'x': 690.65, 'win': 762.6}),
            ('v4_end', 766.2, 769.8, 'front', {}, {'n': 767.65}),
        ],
        'aly': [(148.8, 153.62, 'big')],
        'partial': {'S067': 'انت خدت بالك إن الشريط بيدّي أبيض وأسود أحيانًا وده مش في الأصل بتاع الشريط', 'S201': 'انتوا واخدين بالكم دلوقتي',
                    'S183': 'الـ USB. الـ USB دلوقتي هوصّله بالكمبيوتر.', 'S030': ''},
    },
    8: {  # nostalgia
        'scenes': [
            ('v8_real', 0.8, 13.8, 'front', {'clip': 0.8, 'title': 'أغلبنا عنده *شرايط فيديو* قديمة'}, {}),
            ('v8_box', 13.8, 17.7, 'front', {}, {'copy': 13.9, 'hi8': 17.65}),
            ('v8_save', 17.7, 21.5, 'front', {'tag': 'لازم نحوّلها ديجيتال', 'icons': False, 'label': 'فرح ١٩٩٨'}, {'dig': 19.8}),
            ('v1_end', 75.6, 81.3, 'back', {'title': 'نبعته لأهلنا… أو نحطّه على *فلاشة*',
                                            'items': [['النت', '🌐', '#33E1FF'], ['فلاشة', '💾', '#FFD21F'], ['تخزين', '🗄️', '#ECECE4']]},
             {'i0': 77.24, 'i1': 78.8, 'i2': 79.24}),
            ('v8_play', 137.9, 142.6, 'front', {'title': 'جرّبنا على شريط *بكار* قديم 📼'}, {'relic': 139.62}),
            ('v8_end', 789.9, 794.8, 'front', {}, {}),
            ('v8_pray', 901.1, 903.9, 'back', {}, {}),
        ],
        'aly': [(75.7, 81.1, 'big'), (901.3, 903.7, 'big')],
        'partial': {'S001': 'أغلبنا عنده شرايط فيديو قديمة كتير سواء شرايط VHS الكبيرة زي دي أو شرايط صغيرة اللي كانت بتتحط في الكاميرات ده مثلًا شريط Hi8 اللي كان بيتحط في الكاميرات السوني. مش قلتلك هيقعوا؟ لو وقعوا وراحوا مالهمش نسخ تانية ودي شرايط قديمة وعايزين نشوف شكلنا القديم فيها فدي آثار وعايزين نحتفظ بيها ولازم نحوّلها لنسخة ديجيتال.',
                    'S008': 'عشان', 'S288': 'وياريت بقى ما تنساش تدعيلي وانت بتتفرج على ذكرياتك'},
    },
}


def alpha_pos(file, at):
    """Head position in the cut-out square (from its alpha, haar misses him in the car): [x, y] of the face centre and the
    head width, all as fractions of the square. Cached in work/alpha_pos.json."""
    import subprocess, numpy as np
    cache = W / 'alpha_pos.json'
    c = json.load(open(cache)) if cache.exists() else {}
    key = f'{file}@{at:.2f}'
    if key not in c:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-c:v', 'libvpx-vp9', '-ss', f'{at:.2f}', '-i', str(ROOT / 'motion-library/public' / file), '-frames:v', '1',
                              '-vf', 'scale=270:270', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], capture_output=True).stdout
        a = np.frombuffer(raw, np.uint8).reshape(270, 270, 4)[..., 3] > 128
        rows = np.where(a.any(1))[0]
        y0 = rows[0]; band = a[y0:y0 + 50]
        xs = np.where(band.any(0))[0]
        cx = np.where(band)[1].mean()
        c[key] = [round(cx / 270, 3), round((y0 + 32) / 270, 3), round((xs[-1] - xs[0]) / 270, 3)]
        json.dump(c, open(cache, 'w'), indent=1)
    return c[key]


def build(n):
    S = SHORTS[n]
    print(f'short {n} edges:')
    KEEP.clear()
    ranges = [span(a, b) for a, b in SPANS[n]]
    segs, tl = [], 0.0
    for a, b in ranges:
        segs.append({'src': a, 'tl': round(tl, 3), 'len': round(b - a, 3)}); tl += b - a
    main = tl

    def to_tl(t):
        for s in segs:
            if s['src'] - 0.01 <= t <= s['src'] + s['len'] + 0.01:
                return s['tl'] + max(0.0, min(t - s['src'], s['len']))
        # scene edges are given a little outside the waveform-fitted ranges -> snap to the nearest range edge (<= 0.7 s)
        best = min([(abs(t - s['src']), s['tl']) for s in segs] + [(abs(t - s['src'] - s['len']), s['tl'] + s['len']) for s in segs])
        if best[0] <= 0.7:
            return best[1]
        raise ValueError(f'short {n}: {t} outside ranges')

    # captions: kept words + spelling fixes (whole-sentence fix only when the whole sentence is kept)
    words = []
    partial = S.get('partial', {})
    for snt in tr['sentences']:
        kept = [w for w in snt['words'] if id(w) in KEEP]
        if not kept:
            continue
        if partial.get(snt['id']) == '':  # Whisper put a word of the next part inside the range (timing off) -> drop
            continue
        txt = partial.get(snt['id']) if len(kept) < len(snt['words']) else FIX.get(snt['id'])
        if len(kept) < len(snt['words']) and snt['id'] not in partial:
            print(f'  !! partial {snt["id"]}: ' + ' '.join(w['w'] for w in kept))
        if txt:
            new = txt.split(); a0, b0 = kept[0]['start'], kept[-1]['end']
            if len(new) == len(kept):
                kept = [{**w, 'w': x} for w, x in zip(kept, new)]
            else:
                tot = sum(len(x) + 1 for x in new); t = a0; kk = []
                for x in new:
                    d = (b0 - a0) * (len(x) + 1) / tot; kk.append({'w': x, 'start': t, 'end': t + d}); t += d
                kept = kk
        for w in kept:
            ra, rb = min(ranges, key=lambda r: 0 if r[0] - 0.05 <= w['start'] < r[1] else min(abs(w['start'] - r[0]), abs(w['start'] - r[1])))  # a word never crosses its range edges
            words.append({'w': w['w'], 'start': round(to_tl(max(w['start'], ra)), 3), 'end': round(to_tl(max(ra, min(w['end'], rb))), 3)})
    # CTA clip words (his vertical phone clip, cleaned voice: work/cta/transcript.json)
    ct = json.load(open(W / 'cta' / 'transcript.json', encoding='utf8'))
    for w in [w for s_ in ct['sentences'] for w in s_['words'] if CTA_KEEP[0] - 0.05 <= w['start'] < CTA_KEEP[1] - 0.05]:
        x = CTA_FIX.get(w['w'], w['w'])
        if x:
            words.append({'w': x, 'start': round(main + w['start'] - CTA_KEEP[0], 3), 'end': round(main + w['end'] - CTA_KEEP[0], 3)})
    scenes = []
    for t, a, b, layer, props, beats in S['scenes']:
        at = to_tl(a)
        dur = to_tl(b) - at
        pr = dict(props)
        pr['b'] = {k: round(to_tl(v) - at, 3) for k, v in beats.items()}
        scenes.append({'t': t, 'at': round(at, 3), 'dur': round(dur, 3), 'layer': layer, 'props': pr})
    sc = sorted(scenes, key=lambda x: x['at'])  # close tiny holes (< 0.6 s) between scenes left by the waveform edges
    for x, y in zip(sc, sc[1:]):
        gap = y['at'] - (x['at'] + x['dur'])
        if 0 < gap < 0.6:
            x['dur'] = round(x['dur'] + gap, 3)
    aly = []
    for a, b, mode in S['aly']:
        win = next((x for x in FACES.get(n, []) if x['src'] - 0.05 <= a and b <= x['end'] + 0.05), None)
        if not win:
            print(f'  !! no cut-out for {a}-{b} (faces.py not done?)'); continue
        if win.get('faceW'):  # haar found the face (crop is centred on it): reliable; alpha is fooled by raised hands
            fx, fy, hw = win['face'][0], win['face'][1], round(win['faceW'] * 1.05, 3)
        else:
            fx, fy, hw = alpha_pos(win['file'], (a + b) / 2 - win['src'])
        aly.append({'file': win['file'], 'at': round(to_tl(a), 3), 'dur': round(to_tl(b) - to_tl(a), 3), 'from': round(a - win['src'], 3),
                    'mode': mode, 'face': [fx, fy, hw]})
    # sound design (scripts/sfx_plan.py): scene specials on beats + generic whoosh / swish / pop / impact / CTA sounds
    from sfx_plan import SFX
    L = 'sfx/'
    sfx = [{'file': L + 'impact.wav', 'at': 0.05, 'vol': 0.5}]
    k = 0
    for s in scenes:
        pr = s['props']['b']; spec = SFX.get(s['t'], [])
        if s['at'] > 0.3:
            if s['layer'] == 'front':
                k += 1; sfx.append({'file': L + f'whoosh_{k % 3 + 1}.wav', 'at': round(max(0, s['at'] - 0.12), 3), 'vol': 0.5})
            else:
                sfx.append({'file': L + 'swish.wav', 'at': s['at'], 'vol': 0.4})
        used = {x[0] for x in spec if isinstance(x[0], str)}
        for j, (bn, bt) in enumerate(pr.items()):
            if bn not in used and 0 <= bt < s['dur']:
                sfx.append({'file': L + f'pop_{j % 3 + 1}.wav', 'at': round(s['at'] + bt, 3), 'vol': 0.4})
        for it in spec:
            off = pr.get(it[0]) if isinstance(it[0], str) else it[0]
            if off is None or off >= s['dur']:
                continue
            dur = min(it[3] if len(it) > 3 else 3.0, s['dur'] - off + 0.4)
            sfx.append({'file': L + it[1] + '.wav', 'at': round(s['at'] + off, 3), 'vol': it[2], 'dur': round(dur, 3), 'loop': bool(len(it) > 4 and it[4])})
    sfx += [{'file': L + 'whoosh_2.wav', 'at': round(a['at'], 3), 'vol': 0.35} for a in aly if a['at'] > 0.5]
    c0 = main + 3.4 - CTA_KEEP[0]  # comment card: typing, post pop, DM ding (frames 49 / 80 / 105 of the card)
    sfx += [{'file': L + 'whoosh_1.wav', 'at': round(main - 0.1, 3), 'vol': 0.45}, {'file': L + 'typing.wav', 'at': round(c0 + 34 / 30, 3), 'vol': 0.45, 'dur': 0.9},
            {'file': L + 'pop_2.wav', 'at': round(c0 + 62 / 30, 3), 'vol': 0.55}, {'file': L + 'ding.wav', 'at': round(c0 + 84 / 30, 3), 'vol': 0.5}]
    vlog, vI = build_voice(segs, (PJ + 'cta.mp4', CTA_KEEP[0], CTA_KEEP[1] - CTA_KEEP[0]), PUB / f'voice_{n}.wav')
    print('  voice gains dB per piece:', vlog, f'(before final gain {vI:.1f} LUFS)')
    dur = round(main + CTA_KEEP[1] - CTA_KEEP[0], 3)
    props = {'fps': 30, 'duration': dur, 'voice': PJ + f'voice_{n}.wav', 'segs': [{'src': 0, 'tl': 0, 'len': dur}], 'words': words,
             'aly': aly, 'scenes': scenes, 'sfx': sfx, 'tint': S.get('tint', '#1F33E8'), 'look': 'vhs', 'capBottom': 0.12,
             'ctaVol': 0.0, 'sfxGain': 1.0, 'cta': {'file': PJ + 'cta.mp4', 'tl': round(main, 3), 'len': round(CTA_KEEP[1] - CTA_KEEP[0], 3), 'src': CTA_KEEP[0]},
             'ctaCue': {'at': round(3.4 - CTA_KEEP[0], 3), 'dur': round(CTA_KEEP[1] - 3.4, 3), 'props': {
                 'title': 'اكتب في *كومنت*', 'keyword': 'VHS', 'dm': 'ده لينك الفيديو كامل 📼', 'typeAt': 34, 'sendAt': 62, 'dmAt': 84, 'top': 0.02}}}
    json.dump(props, open(PUB / f'short_{n}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    holes = []
    cover = sorted([(s['at'], s['at'] + s['dur']) for s in scenes] + [(x['at'], x['at'] + x['dur']) for x in aly])
    end = 0
    for a, b in cover:
        if a - end > 0.3: holes.append((round(end, 2), round(a, 2)))
        end = max(end, b)
    if main - end > 0.3: holes.append((round(end, 2), round(main, 2)))
    print(f'short {n}: {main:.1f}s + CTA {CTA_KEEP[1] - CTA_KEEP[0]:.2f}s | {len(scenes)} scenes, {len(aly)} Aly | uncovered: {holes}')


for n in [int(x) for x in sys.argv[1:]] or sorted(SHORTS):
    build(n)

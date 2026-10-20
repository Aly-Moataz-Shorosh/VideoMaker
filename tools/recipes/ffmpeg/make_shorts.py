"""Faceless vertical shorts (look 'pop', new style from his 5 Behance refs) from Aly's 2021 FFmpeg tutorial (2026-10-14).
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


def span(t0, t1, a_force=None, b_force=None):
    """Range from the word starting at t0 to the word starting at t1 (Whisper starts), edges fitted on the waveform."""
    i = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t0))
    j = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t1))
    prev = _words[i - 1]['end'] if i > 0 else None
    nxt = _words[j + 1]['start'] if j + 1 < len(_words) else None
    a, b, rep = fit(_words[i]['start'], _words[j]['end'], prev, nxt)
    if a_force:  # start measured by hand on the 20 ms dB profile (edges.profile): Whisper start sat on the previous word's tail
        a = a_force; rep += f' START FORCED {a_force}'
    if b_force:
        b = b_force; rep += f' END FORCED {b_force}'
    KEEP.update(id(w) for w in _words[i:j + 1])
    print('   ', _words[i]['w'], '…', _words[j]['w'], rep)
    return [a, b]


# Ranges = word spans (first word start, last word start). Edges are fitted on the audio waveform (work/scripts/edges.py).
SPANS = {
    1: [(321.12, 329.76, 321.15, 330.08), (16.2, 19.33), (27.56, 29.02), (36.68, 39.13, 36.57), (77.13, 84.31), (84.99, 92.01), (117.32, 122.84),
        (179.74, 189.8), (228.30, 231.44, 228.43), (274.30, 280.94), (305.27, 306.97), (330.14, 333.78, 330.08)],
    2: [(92.25, 105.09), (108.37, 115.60, 108.10), (161.21, 164.97, 161.21), (255.56, 257.28, 255.53)],
    3: [(117.32, 138.10)],
    # v2 (Aly 2026-10-14): ONE short with the WHOLE tutorial, < 3:00
    4: [(321.12, 329.76, 321.15, 330.08), (16.2, 19.33), (27.56, 39.13), (41.25, 46.15), (49.11, 51.33), (61.18, 63.88), (66.89, 67.99),
        (70.72, 92.01), (92.25, 105.09), (108.37, 122.84, 108.10), (140.24, 147.83), (155.65, 156.73), (161.21, 164.97, 161.21),
        (179.74, 189.8), (223.04, 231.44), (261.76, 265.90), (267.82, 269.70), (274.30, 282.26), (294.80, 298.68), (301.85, 304.97),
        (305.27, 306.97), (317.74, 320.94, None, 321.13), (330.14, 333.78, 330.08)],
}
CTA_KEEP = (7.0, 11.95)  # brand/clips/cta_comment_youtube_9x16.mp4: "لو عايز نسخة الفيديو على اليوتيوب اكتب في كومنت يوتيوب..."
CTA_FIX = {'بعطلك': 'هبعتلك', 'طول.': 'طول'}

SHORTS = {
    1: {  # condensed tutorial: compress any video with one ffmpeg line
        'scenes': [
            ('f1_hook', 321.0, 330.06, 'front', {}, {'kb': 324.63, 'diff': 327.32, 'sky': 328.36}),
            ('f1_google', 16.1, 20.9, 'front', {}, {'type': 18.85, 'ff': 19.4}),
            ('f1_site', 27.4, 39.3, 'front', {'pics': PJ + 'pics/'}, {'dl': 29.02, 'want': 36.68, 'win': 38.82}),
            ('f1_bin', 77.0, 84.95, 'front', {'pics': PJ + 'pics/'}, {'all': 79.89, 'exe': 82.87}),
            ('f1_what', 84.95, 92.3, 'front', {}, {'press': 85.91, 'conv': 87.79, 'easy': 91.65}),
            ('f1_cmd', 117.2, 123.2, 'front', {}, {'search': 119.66, 'type': 121.46, 'enter': 122.84}),
            ('f1_line', 179.6, 190.4, 'front', {'pics': PJ + 'pics/'}, {'name': 181.64, 'space': 183.64, 'space2': 184.98, 'dash': 185.46, 'minus': 188.06, 'i': 188.66}),
            ('f1_in', 228.2, 232.0, 'front', {}, {'drop': 229.4, 'fmt': 231.28}),
            ('f1_trick', 274.2, 281.4, 'front', {}, {'trick': 275.52, 'mov': 278.12, 'mp4': 280.14}),
            ('f1_enter', 305.1, 307.5, 'front', {}, {'enter': 306.97}),
            ('f1_end', 330.1, 334.6, 'front', {}, {'kb': 330.72, 'mb': 332.1, 'diff': 333.12}),
        ],
        'aly': [],
        'partial': {
            'S115': 'لو وقفنا على ده هنلاقيه خمسة ميجا', 'S116': 'لو وقفنا على ده تسعين كيلو بايت', 'S117': 'شايفين الفرق؟', 'S118': 'يعني من السما للأرض',
            'S001c': 'المبدأ كده هنخش على جوجل', 'S001d': 'وهنكتب FFmpeg', 'S001g': 'فهنخش على الموقع ده وهندوس Download',
            'S002': 'أنا مش عايز… أنا عايز البرنامج نفسه', 'S003': 'فهاجي أدوس على علامة الويندوز',
            'S021': 'هفتح الفولدر اللي اسمه bin', 'S022': 'هلاقي البرامج دي كلها', 'S023': 'البرنامج هو ده', 'S024': 'ffmpeg.exe',
            'S025': 'ده بيعمل ايه؟ ده بيضغط الفيديو', 'S026': 'وبيعمل convert لأي نسخة', 'S027': 'موجودة عندي', 'S028': 'يقدر يضغطها بسهولة جدًا',
            'S036': 'الموضوع ببساطة هفتح الفولدر ده', 'S037': 'واكتب في السيرش هنا', 'S038': 'CMD وأدوس Enter',
            'S066': 'دلوقتي هكتب تاني اسم البرنامج', 'S067': 'والمرة دي هدوس space مهمة قوي دي space dash الشرطة اللي هي minus دي i و i small',
            'S076': 'اللينك بتاع الفيديو بتاعي اسم الفيديو dot format',
            'S091': 'بس بقى المهم التريكة كلها اللي محور كله', 'S092': 'إنه ما يبقاش dot mov', 'S093': 'أسميه dot mp4',
            'S107': 'فنخش بقى تاني وندوس Enter', 'S119': 'ده تسعين كيلو بايت', 'S120': 'وده ستة ميجا', 'S121': 'فرق شاسع',
        },
    },
    2: {  # why ffmpeg.exe opens and closes: a console program that waits for an input
        'scenes': [
            ('f2_flash', 92.1, 96.9, 'front', {}, {'dbl': 93.29, 'open': 95.53, 'close': 95.85}),
            ('f2_why', 96.9, 100.9, 'front', {}, {'no': 98.47, 'btn': 99.35, 'con': 100.47}),
            ('f2_console', 100.9, 105.4, 'front', {}, {'black': 102.29, 'cmd': 104.31}),
            ('f2_input', 108.2, 115.9, 'front', {}, {'why': 109.29, 'input': 111.13, 'none': 112.18, 'close': 115.32}),
            ('f2_give', 161.1, 165.4, 'front', {}, {'no': 162.77, 'give': 164.67}),
            ('f2_i', 255.4, 257.8, 'front', {}, {'i': 256.24, 'in': 257.28}),
        ],
        'aly': [],
        'partial': {
            'S029': 'فهروح دايس عليه double click', 'S030': 'هلاقيه فتح وقفل بسرعة',
            'S031': 'ليه الكلام ده؟ لإن ده مش برنامج بتاع زراير، ده برنامج كونسول',
            'S032': 'كونسول يعني ايه؟ يعني بيشتغل على الشاشة السودا وبكتبله commands وكلام زي ده',
            'S034': 'بس هو قفل بسرعة ليه؟ لإنه برنامج بدّه input يشتغل عليه', 'S035': 'مفيش، فهو أول ما دوست عليه بيفتحه ويقفله بسرعة',
            'S059': 'بس فتحهولي وقفلهولي، أنا مش عايز كده', 'S060': 'أنا عايز بقى أديله input',
            'S081': 'بعد كده dash input يعني هدخّل input',
        },
    },
    3: {  # 3 ways to open CMD
        'scenes': [
            ('f3_hook', 117.2, 118.6, 'front', {}, {}),
            ('f3_way1', 118.6, 124.95, 'front', {}, {'search': 119.66, 'type': 121.46, 'enter': 122.84}),
            ('f3_way2', 124.95, 129.15, 'front', {}, {'type': 127.10, 'enter': 127.92}),
            ('f3_way3', 129.15, 134.95, 'front', {}, {'win': 130.48, 'r': 132.46, 'type': 133.82, 'enter': 134.66}),
            ('f3_end', 134.95, 138.7, 'front', {}, {'cmd': 136.60, 'write': 137.84}),
        ],
        'aly': [],
        'partial': {
            'S036': 'الموضوع ببساطة هفتح الفولدر ده', 'S037': 'وأكتب في السيرش هنا', 'S038': 'CMD وأدوس Enter', 'S039': 'هيفتحلي الشاشة دي',
            'S040': 'أو أجي هنا في السيرش وأكتب CMD', 'S041': 'وأدوس Enter', 'S042': 'هيطلعلي هنا',
            'S043': 'أو هدوس علامة الويندوز', 'S044': 'وأفضل دايس وأدوس R', 'S045': 'وأكتب CMD وأدوس Enter',
            'S046': 'فالمهم إني أوصل للـ CMD', 'S047': 'اللي هي المكان اللي هكتب فيه',
        },
    },
    4: {  # v2: the whole tutorial in one short
        'scenes': [
            ('f1_hook', 321.16, 330.06, 'front', {}, {'kb': 324.63, 'diff': 327.32, 'sky': 328.36}),
            ('f1_google', 16.1, 20.9, 'front', {}, {'type': 18.85, 'ff': 19.4}),
            ('f1_site', 27.4, 39.8, 'front', {'pics': PJ + 'pics/'}, {'dl': 29.02, 'want': 30.54, 'win': 38.82}),
            ('f4_github', 41.1, 51.6, 'front', {}, {'gh': 45.87, 'any': 50.47}),
            ('f4_zip', 61.0, 68.6, 'front', {}, {'first': 63.50, 'dl': 67.99}),
            ('f4_folder', 70.6, 77.05, 'front', {}, {'open': 74.45, 'find': 76.35}),
            ('f1_bin', 77.05, 84.95, 'front', {'pics': PJ + 'pics/'}, {'all': 79.89, 'exe': 82.87}),
            ('f1_what', 84.95, 92.2, 'front', {}, {'press': 85.91, 'conv': 87.79, 'easy': 91.65}),
            ('f2_flash', 92.2, 96.9, 'front', {}, {'dbl': 93.29, 'open': 95.53, 'close': 95.85}),
            ('f2_why', 96.9, 100.9, 'front', {}, {'no': 98.47, 'btn': 99.35, 'con': 100.47}),
            ('f2_console', 100.9, 105.4, 'front', {}, {'black': 102.29, 'cmd': 104.31}),
            ('f2_input', 108.0, 115.85, 'front', {}, {'why': 109.29, 'input': 111.13, 'none': 112.18, 'close': 115.32}),
            ('f1_cmd', 115.85, 123.3, 'front', {'ways': True}, {'search': 119.66, 'type': 121.46, 'enter': 122.84}),
            ('f4_dragexe', 140.1, 148.3, 'front', {}, {'drag': 144.82, 'drop': 146.15}),
            ('f2_give', 155.5, 165.4, 'front', {}, {'no': 162.77, 'give': 164.67}),
            ('f1_line', 179.6, 190.4, 'front', {}, {'name': 181.64, 'space': 183.64, 'space2': 184.98, 'dash': 185.46, 'minus': 188.06, 'i': 188.66}),
            ('f1_in', 222.9, 232.3, 'front', {}, {'drop': 225.10, 'fmt': 231.28}),
            ('f4_anatomy', 261.6, 266.4, 'front', {}, {'prog': 261.8, 'i': 262.15, 'vid': 262.5, 'inn': 262.82, 'out': 263.20, 'same': 264.54}),
            ('f4_rename', 267.7, 271.2, 'front', {}, {'ren': 268.80, 'ff': 269.70}),
            ('f1_trick', 274.2, 282.5, 'front', {}, {'trick': 275.52, 'mov': 278.12, 'mp4': 280.14}),
            ('f4_big', 294.7, 305.15, 'front', {}, {'five': 297.94, 'hund': 303.51}),
            ('f1_enter', 305.15, 307.4, 'front', {}, {'enter': 306.97}),
            ('f4_new', 317.6, 321.0, 'front', {}, {'name': 319.38}),
            ('f1_end', 330.1, 334.6, 'front', {}, {'kb': 330.72, 'mb': 332.1, 'diff': 333.12}),
        ],
        'aly': [],
        'partial': {
            'S001h': 'وبعد كده مش عايز download source code لإن ده برنامج open source معناه إن البرنامج ده الكود',
            'S002': 'اللي بيشغّله موجود على النت. أنا مش عايز… أنا عايز البرنامج نفسه',
            'S005': 'الحتة اللي هي دي هدوس على', 'S006': 'اللينك التاني وهيفتح', 'S007': 'لي موقع GitHub',
            'S009': 'بس أنا هاخد بقى أي لينك من دول', 'S010': 'هنزّله', 'S014': 'هنزّل أي حاجة من دول', 'S015': 'هندوس على أول واحد',
            'S017': 'فهندوس Download', 'S018': 'هو ده الفولدر بتاعنا لما نفتحه وننزّله', 'S019': 'هنفتحه تاني', 'S020': 'هنلاقي فيه الفولدرات دي',
            'S049': 'أنا عايز أقوله أنا عايز أشغّل البرنامج ده', 'S050': 'فهقوم أقوله', 'S051': 'ده هدوس عليه وأشدّه', 'S052': 'وأحطه هنا',
            'S053': 'بدل ما أكتب اللينك بتاعه', 'S056': 'هيفتحهولي ويقفلهولي برضو',
            'S068': 'فدلوقتي يعني هدخّله input هقوم دايس بقى space تاني',
            'S074': 'هعمل ايه بقى؟ أمسك الفايل بتاعي وأشدّه وأحطه', 'S075': 'فكده عامل space double quotations',
            'S080': 'فأنا كده عملت ايه؟ الإنبوت بتاعي اللي هو ده البرنامج، اللي هو اللينك الطويل ده البرنامج',
            'S081': 'بعد كده dash input يعني هدخّل input', 'S082': 'وبعد كده اسم الفيديو بتاعي اللي هو dot', 'S083': 'dot',
            'S084': 'بعد كده ده الإنبوت', 'S085': 'الأوتبوت بقى هيكون نفس المكان بالظبط بنفس الاسم',
            'S088': 'أنا عايزه بقى ايه؟', 'S089': 'أغيّره وأكتب FFMPEG', 'S094': 'ده هيضغطه بشكل حلو',
            'S102': 'طبعًا احنا مش هنلاحظ قوي إنه صغر هنا عشان ده أصلًا', 'S103': 'فيديو خمسة ميجا',
            'S105': 'فمش هنحس قوي، بس في الفيديوهات اللي بتبقى مية ميجا', 'S106': 'وكده هنحس قوي',
            'S109': 'خلص عشان هو خمسة ميجا فخلص بسرعة', 'S113': 'ده الفيديو الجديد بتاعنا', 'S114': 'اسمه bee circle dot mp4'},
    },
}
SHORTS[4]['partial'] = {**SHORTS[1]['partial'], **SHORTS[2]['partial'], **SHORTS[3]['partial'], **SHORTS[4]['partial']}


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
    ranges = [span(*x) for x in SPANS[n]]
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
        txt = partial.get(snt['id']) or FIX.get(snt['id'])
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
    c0 = main + 0.6  # comment card: typing, post pop, DM ding (frames 49 / 80 / 105 of the card)
    sfx += [{'file': L + 'whoosh_1.wav', 'at': round(main - 0.1, 3), 'vol': 0.45}, {'file': L + 'typing.wav', 'at': round(c0 + 34 / 30, 3), 'vol': 0.45, 'dur': 0.9},
            {'file': L + 'pop_2.wav', 'at': round(c0 + 62 / 30, 3), 'vol': 0.55}, {'file': L + 'ding.wav', 'at': round(c0 + 84 / 30, 3), 'vol': 0.5}]
    vlog, vI = build_voice(segs, (PJ + 'cta.mp4', CTA_KEEP[0], CTA_KEEP[1] - CTA_KEEP[0]), PUB / f'voice_{n}.wav')
    print('  voice gains dB per piece:', vlog, f'(before final gain {vI:.1f} LUFS)')
    dur = round(main + CTA_KEEP[1] - CTA_KEEP[0], 3)
    props = {'fps': 30, 'duration': dur, 'voice': PJ + f'voice_{n}.wav', 'segs': [{'src': 0, 'tl': 0, 'len': dur}], 'words': words,
             'aly': aly, 'scenes': scenes, 'sfx': sfx, 'tint': S.get('tint', '#1F33E8'), 'look': 'pop', 'capBottom': 0.12,
             'ctaVol': 0.0, 'sfxGain': 1.0, 'cta': {'file': PJ + 'cta.mp4', 'tl': round(main, 3), 'len': round(CTA_KEEP[1] - CTA_KEEP[0], 3), 'src': CTA_KEEP[0]},
             'ctaCue': {'at': 0.6, 'dur': round(CTA_KEEP[1] - CTA_KEEP[0] - 0.6, 3), 'props': {
                 'title': 'اكتب في *كومنت*', 'keyword': 'يوتيوب', 'dm': 'ده لينك الفيديو كامل 🎬', 'typeAt': 34, 'sendAt': 62, 'dmAt': 84, 'top': 0.02}}}
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

"""10 faceless-first vertical shorts from Aly's 'حكاية الفيلم - The Odyssey' video (2026-10-08).
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
R = {int(k): v for k, v in json.load(open(W / 'ranges.json')).items()}
R[1][2][1] = 622.28  # end right after 'عادية' (snap moved it onto 'تاني')
R[3][0][1] = 187.3   # keep the last word 'الصور'
R[4][0][1] = R[5][0][0] = 256.42  # 'طيب' belongs to short 5
R[9][0][0] = 622.28  # start on 'تاني حاجة' (right where short 1 ends)
FACES = {int(k): v for k, v in json.load(open(W / 'faces.json', encoding='utf8')).items()} if (W / 'faces.json').exists() else {}
FIX = json.load(open(W / 'fix.json', encoding='utf8'))
CTA_KEEP = (7.06, 12.01)
CTA_TEXT = 'لو عايز نسخة الفيديو على اليوتيوب اكتب في كومنت يوتيوب وهو هيبعتلك اللينك على طول'

SHORTS = {
    1: {
        'scenes': [
            ('s1_hook', 46.55, 50.6, 'back', {'title': 'ليه نولان بيقولك: ما تشوفش *الأوديسة* غير في _IMAX_ ؟'}, {}),
            ('s1_nolan', 50.6, 56.88, 'front', {}, {'say': 51.1, 'mm': 54.1, 'all': 55.6}),
            ('s1_why', 555.28, 561.5, 'front', {}, {'colors': 559.4, 'strip': 560.7}),
            ('s1_projector', 561.5, 569.0, 'front', {}, {'proj': 562.5, 'huge': 564.1, 'special': 566.2}),
            ('s1_map', 569.0, 580.84, 'front', {}, {'n41': 570.7, 'na': 574.1, 'uk': 575.8, 'eu': 576.6, 'au': 577.7, 'none': 578.2,
                                                   'africa': 579.0, 'asia': 580.3}),
            ('s1_beam', 587.5, 595.9, 'front', {}, {'raw': 589.5, 'proj': 592.0}),
            ('s1_egypt', 595.9, 600.4, 'back', {}, {'egypt': 596.9, 'digital': 599.9}),
            ('s1_compare', 600.4, 610.5, 'front', {}, {'raw': 602.9, 'digital': 603.7, 'zoom': 605.1, 'notsame': 605.9}),
            ('s1_aspect', 610.5, 622.28, 'back', {}, {'cut1': 615.6, 'cut2': 619.7}),
            ('s1_end', 620.4, 622.28, 'front', {}, {'stamp': 620.8}),
        ],
        'aly': [(46.55, 50.6, 'bottom'), (595.9, 600.4, 'bottom'), (619.95, 621.85, 'right')],
        'partial': {'S145': '', 'S146': 'اللي بتعرض آي ماكس خام سبعين مللي بتعرضه وتعمله البروجكشن', 'S153': 'يعني متدخلش الفيلم ده في قاعة سينما عادية'},
    },
    2: {
        'scenes': [
            ('s2_hook', 81.27, 85.3, 'back', {}, {}),
            ('s2_emission', 85.3, 87.2, 'front', {}, {'rays': 85.9, 'no': 86.6}),
            ('s2_haytham', 87.2, 89.2, 'front', {}, {'no': 88.5}),
            ('s2_light', 89.2, 100.6, 'front', {}, {'hit': 90.1, 'bounce': 93.6, 'brain': 97.0, 'pic': 99.9}),
            ('s2_name', 100.6, 103.0, 'back', {}, {'name': 102.4}),
            ('s2_obscura', 103.0, 114.8, 'front', {}, {'box': 104.0, 'room': 106.6, 'hole': 108.5, 'light': 109.2, 'draw': 111.3}),
            ('s2_first', 114.8, 122.0, 'front', {}, {'year': 116.2, 'proj': 119.8}),
            ('s2_wall', 122.0, 126.86, 'back', {}, {}),
        ],
        'aly': [(81.27, 85.3, 'bottom'), (100.6, 103.0, 'bottom'), (122.0, 126.86, 'bottom')],
    },
    3: {
        'scenes': [
            ('s3_hook', 126.86, 131.0, 'back', {}, {}),
            ('s3_swap', 131.0, 144.8, 'front', {}, {'plate': 131.1, 'chem': 133.5, 'sens': 136.9, 'hit': 138.9, 'change': 139.9, 'stay': 142.0}),
            ('s3_keep', 144.8, 157.8, 'front', {}, {'proj': 147.7, 'photo': 150.8, 'save': 153.7, 'any': 157.0}),
            ('s3_gens', 157.8, 165.4, 'front', {}, {'ancestors': 162.4, 'kids': 164.7}),
            ('s3_miracle', 165.4, 167.7, 'back', {}, {'word': 166.2}),
            ('s3_develop', 167.7, 182.9, 'front', {}, {'sheet': 175.4, 'ghost': 178.8}),
            ('s3_born', 182.9, 187.3, 'back', {}, {'word': 184.1, 'year': 184.6}),
        ],
        'aly': [(126.86, 131.0, 'bottom'), (165.4, 167.7, 'bottom'), (182.9, 186.52, 'bottom')],
    },
    4: {
        'scenes': [
            ('s4_hook', 187.39, 191.5, 'back', {}, {}),
            ('s4_silver', 191.5, 203.8, 'front', {}, {'name': 192.1, 'hit': 197.8, 'bw': 201.0}),
            ('s4_film', 203.8, 219.4, 'front', {}, {'film': 213.7, 'sens': 218.5}),
            ('s4_camera', 219.4, 226.7, 'front', {}, {}),
            ('s4_burn', 226.7, 234.3, 'back', {}, {'burn': 228.9, 'dev': 233.6}),
            ('s4_develop', 234.3, 243.1, 'front', {}, {'fix': 236.9, 'copies': 239.9}),
            ('s4_color', 243.1, 252.8, 'front', {}, {'layers': 244.8, 'color': 250.3}),
            ('s4_past', 252.8, 256.42, 'back', {}, {}),
        ],
        'aly': [(187.39, 191.5, 'bottom'), (231.0, 233.5, 'left'), (252.8, 256.42, 'bottom')],
    },
    5: {
        'scenes': [
            ('s5_hook', 256.42, 262.5, 'back', {}, {}),
            ('s5_count', 262.5, 274.6, 'front', {}, {'two': 267.6, 'three': 268.2, 'ten': 269.0, 'many': 269.7, 'video': 272.8}),
            ('s5_camera', 274.6, 282.1, 'front', {}, {'many': 280.9}),
            ('s5_fps', 282.1, 291.0, 'front', {}, {'f16': 283.0, 'f12': 285.1, 'f24': 286.3, 'f30': 287.4, 'move': 290.3}),
            ('s5_silent', 291.0, 305.9, 'front', {}, {'silent': 295.9, 'seq': 297.2}),
            ('s5_band', 305.9, 315.8, 'front', {}, {'band': 310.4}),
            ('s5_mic', 315.8, 320.0, 'back', {}, {}),
            ('s5_sound', 320.0, 341.87, 'back', {}, {'rec': 322.9, 'wave': 336.6, 'side': 339.0}),
        ],
        'aly': [(256.59, 262.5, 'bottom'), (315.8, 320.0, 'bottom'), (338.5, 341.87, 'right')],
        'partial': {'S081': 'إن احنا هنقدر نسجل الصوت لأن الصوت عبارة عن موجة'},
    },
    6: {
        'scenes': [
            ('s6_hook', 341.87, 345.8, 'back', {}, {}),
            ('s6_gauge', 345.8, 357.5, 'front', {}, {'mm': 349.1, 'frame': 353.2}),
            ('s6_names', 357.5, 364.4, 'back', {}, {'cinema': 359.8, 'raw': 361.4}),
            ('s6_shoot', 364.4, 372.8, 'front', {}, {'many': 371.6}),
            ('s6_bigger', 372.8, 386.2, 'front', {}, {'m35': 379.3, 'detail': 384.9}),
            ('s6_clean', 386.2, 389.81, 'back', {}, {}),
        ],
        'aly': [(341.87, 345.8, 'bottom'), (360.0, 363.6, 'bottom'), (386.2, 389.81, 'bottom')],
    },
    7: {
        'scenes': [
            ('s7_hook', 389.81, 395.0, 'back', {}, {}),
            ('s7_digital', 395.0, 407.9, 'front', {}, {'digital': 395.6, 'cam': 398.5, 'years': 404.0, 'movie': 406.1}),
            ('s7_shock', 407.9, 413.0, 'back', {}, {'what': 412.0}),
            ('s7_colors', 413.0, 428.2, 'front', {}, {'sat': 416.2, 'back': 423.1, 'normal': 427.1}),
            ('s7_soul', 428.2, 439.3, 'front', {}, {'old': 430.6, 'soul': 438.2}),
            ('s7_grain', 439.3, 455.0, 'front', {}, {'grain': 440.1, 'pixels': 446.0, 'atoms': 450.3}),
            ('s7_better', 455.0, 460.0, 'back', {}, {}),
        ],
        'aly': [(389.81, 395.0, 'bottom'), (407.9, 413.0, 'bottom'), (455.0, 460.0, 'bottom')],
        'partial': {'S109': 'بيبقى أحسن من الديجيتال'},
    },
    8: {
        'scenes': [
            ('s8_hook', 460.0, 464.5, 'back', {}, {}),
            ('s8_gauges', 464.5, 481.9, 'front', {}, {'m70': 465.1, 'side': 474.7, 'area': 477.4, 'name': 479.1}),
            ('s8_biggest', 481.9, 494.8, 'front', {}, {'cost': 492.9}),
            ('s8_scenes', 494.8, 509.9, 'front', {}, {'dialog': 500.8, 'big': 503.1}),
            ('s8_noise', 509.9, 522.6, 'front', {}, {'film': 512.3, 'loud': 514.0}),
            ('s8_nolan', 522.6, 527.5, 'back', {}, {}),
            ('s8_blimp', 527.5, 537.0, 'front', {}, {'all': 527.8, 'box': 532.9, 'quiet': 536.2}),
            ('s8_mirror', 537.0, 546.51, 'front', {}, {'block': 540.4, 'mirror': 544.7}),
            ('s8_first', 550.27, 553.52, 'back', {}, {'first': 550.6}),
        ],
        'aly': [(460.0, 464.5, 'bottom'), (522.6, 527.5, 'bottom'), (550.27, 553.52, 'bottom')],
        'partial': {'S109': 'يعني فاللي حصل إيه بقى إن فيه أعلى من 35 مللي وهو', 'S129': ''},
    },
    9: {
        'scenes': [
            ('s9_hook', 622.28, 627.5, 'back', {}, {}),
            ('s9_old', 627.5, 642.3, 'front', {}, {'cut': 634.4, 'glue': 637.2}),
            ('s9_how', 642.3, 655.5, 'front', {}, {'digital': 648.8, 'pc': 650.6, 'nums': 653.6}),
            ('s9_robot', 655.5, 662.2, 'back', {}, {'no': 660.8}),
            ('s9_hand', 662.2, 669.8, 'front', {}, {'scissors': 667.1, 'glue': 668.3}),
            ('s9_prep', 669.8, 694.5, 'front', {}, {'cost': 675.5, 'prep': 680.7, 'digital': 682.9, 'improv': 686.6, 'edit': 690.5}),
            ('s9_ready', 694.5, 699.61, 'back', {}, {}),
        ],
        'aly': [(623.09, 627.5, 'bottom'), (658.5, 662.2, 'bottom'), (694.5, 699.61, 'bottom')],
        'partial': {'S153': 'تاني حاجة الفيلم ده'},
    },
    10: {
        'scenes': [
            ('s10_hook', 716.55, 721.5, 'back', {}, {}),
            ('s10_super8', 721.5, 741.5, 'front', {}, {'pricey': 722.7, 'cam': 724.2, 'quality': 727.4, 'p1': 734.0, 'p2': 739.0}),
            ('s10_16', 741.5, 754.5, 'front', {}, {'rent': 746.3, 'film': 752.3}),
            ('s10_35', 754.5, 765.0, 'front', {}, {'one': 758.6, 'price': 763.4}),
            ('s10_day', 765.0, 768.5, 'back', {}, {'n': 766.5}),
            ('s10_minute', 768.5, 777.0, 'front', {}, {'min': 771.7}),
            ('s10_receipt', 777.0, 785.0, 'front', {}, {'rent': 777.3, 'lens': 778.5, 'crew': 779.6, 'actors': 780.8, 'all': 781.8, 'pricey': 783.2}),
            ('s10_digital', 785.0, 790.15, 'back', {}, {}),
        ],
        'aly': [(716.55, 721.5, 'bottom'), (765.0, 768.5, 'bottom'), (785.0, 790.15, 'bottom')],
        'partial': {'S195': 'امسح وعيد وامسح وعيد وعيش حياتك براحتك خالص'},
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
    ranges = R[n]
    segs, tl = [], 0.0
    for a, b in ranges:
        segs.append({'src': a, 'tl': round(tl, 3), 'len': round(b - a, 3)}); tl += b - a
    main = tl

    def to_tl(t):
        for s in segs:
            if s['src'] - 0.01 <= t <= s['src'] + s['len'] + 0.01:
                return s['tl'] + max(0.0, min(t - s['src'], s['len']))
        raise ValueError(f'short {n}: {t} outside ranges')

    # captions: kept words + spelling fixes (whole-sentence fix only when the whole sentence is kept)
    words = []
    partial = S.get('partial', {})
    for snt in tr['sentences']:
        kept = [w for w in snt['words'] if any(a - 0.05 <= w['start'] < b - 0.05 for a, b in ranges)]
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
            rb = next(b for a, b in ranges if a - 0.05 <= w['start'] < b)  # word end never crosses its range end
            words.append({'w': w['w'], 'start': round(to_tl(max(w['start'], rb - 999)), 3), 'end': round(to_tl(min(w['end'], rb)), 3)})
    # CTA clip words
    ct = json.load(open(ROOT / 'brand/clips/cta_comment_youtube_9x16.transcript.json', encoding='utf8'))
    cw = [w for s in ct['sentences'] for w in s['words'] if CTA_KEEP[0] - 0.05 <= w['start'] < CTA_KEEP[1] - 0.05]
    new = CTA_TEXT.split()
    for w, x in zip(cw, new if len(new) == len(cw) else [w['w'] for w in cw]):
        words.append({'w': x, 'start': round(main + w['start'] - CTA_KEEP[0], 3), 'end': round(main + w['end'] - CTA_KEEP[0], 3)})

    scenes = []
    for t, a, b, layer, props, beats in S['scenes']:
        at = to_tl(a)
        dur = to_tl(b) - at
        pr = dict(props)
        pr['b'] = {k: round(to_tl(v) - at, 3) for k, v in beats.items()}
        scenes.append({'t': t, 'at': round(at, 3), 'dur': round(dur, 3), 'layer': layer, 'props': pr})
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
    c0 = main + 7.19 - CTA_KEEP[0]  # comment card: typing, post pop, DM ding (frames 49 / 80 / 105 of the card)
    sfx += [{'file': L + 'whoosh_1.wav', 'at': round(main - 0.1, 3), 'vol': 0.45}, {'file': L + 'typing.wav', 'at': round(c0 + 49 / 30, 3), 'vol': 0.45, 'dur': 0.9},
            {'file': L + 'pop_2.wav', 'at': round(c0 + 80 / 30, 3), 'vol': 0.55}, {'file': L + 'ding.wav', 'at': round(c0 + 105 / 30, 3), 'vol': 0.5}]
    props = {'fps': 30, 'duration': round(main + CTA_KEEP[1] - CTA_KEEP[0], 3), 'voice': PJ + 'voice.m4a', 'segs': segs, 'words': words,
             'aly': aly, 'scenes': scenes, 'sfx': sfx, 'tint': S.get('tint', '#E5232B'), 'capBottom': 0.12,
             'ctaVol': 1.0, 'sfxGain': 1.6, 'cta': {'file': PJ + 'cta_podcast.mp4', 'tl': round(main, 3), 'len': round(CTA_KEEP[1] - CTA_KEEP[0], 3), 'src': CTA_KEEP[0]},
             'ctaCue': {'at': round(7.19 - CTA_KEEP[0], 3), 'dur': 4.82, 'props': {
                 'title': 'اكتب في *كومنت*', 'keyword': 'يوتيوب', 'dm': 'ده لينك الفيديو كامل 🎬', 'typeAt': 49, 'sendAt': 80, 'dmAt': 105, 'top': 0.02}}}
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

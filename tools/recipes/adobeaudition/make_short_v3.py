"""ONE full Adobe Audition short (2026-10-15, style 10 glass-face; CTA with a QR of the full video). Based on the lighting short (Aly 2026-10-14: "شورت واحد كامل"; new look 'glass' from his Behance ref in his channel colours).
His face is on screen the WHOLE short (the video is about light: the viewer must SEE the effect) -> composition film-short,
look 'glass', prop `cam` = one continuous mp4 of the kept pieces (work/cam.mp4 -> public) + layout keys per chapter.
Run: python work/scripts/make_short.py  -> public/projects/<code>/short_1.json, cam.mp4, voice_1.wav
Piece = (chapter, first word start, last word start[, a_force, b_force]) fitted on the waveform, or ('raw', a, b) = a silent
moment of his video where a light switches on (his music is under it -> fixed -8 dB, no levelling)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))

W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
CODE = P.name
PJ = f'projects/{CODE}/'
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
SRC = P / 'input' / 'IjVlRDHEBSY.mp4'
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
from edges import fit
import level_voice as LV
_words = [w for s in tr['sentences'] for w in s['words']]
KEEP = set()

# v2 (Aly review 2026-10-15): it's a SHORT -> hook first (hear before -> after, same sentence), then straight to the steps;
# more motion (screen card follows every click), less of him (small round webcam), his voice enhanced except before/after.
PIECES = [
    # v3 (Aly: "خد اللي اتعرض"): the REAL before/after he played in the video (1:53 green = before, 1:59 white = processed)
    ('hook', 113.66, 116.70, 113.45, 116.80), ('hook', 119.20, 121.88, 119.02, 122.28),
    ('tool', 88.05, 90.49),
    ('noise', 301.98, 306.14), ('noise', 312.37, 314.49), ('noise', 314.81, 316.59), ('noise', 323.77, 328.27),
    ('noise', 337.57, 340.97), ('noise', 351.11, 355.56), ('noise', 358.73, 361.15), ('noise', 374.26, 377.18), ('noise', 390.90, 392.34),
    ('norm', 403.22, 408.64), ('norm', 410.55, 412.17),
    ('ve', 427.10, 430.30), ('ve', 432.88, 434.56), ('ve', 436.28, 437.98),
    ('master', 439.76, 443.90), ('master', 446.79, 449.11), ('master', 451.53, 452.23),
    ('eq', 458.34, 463.02), ('eq', 465.80, 468.52), ('eq', 470.83, 471.43),
    ('end', 516.53, 519.67),
]
RAWVOICE = {'hook'}  # before/after demo = his recording exactly as it is
TXT = {
    'S025': 'السلام عليكم كتير جدًا بيشوفوا إن الجرافيكس عبارة عن', 'S026': 'بشوف ودايمًا بقولها إن الجرافيكس أو بالآخر في الفيديو بروداكشن',
    'S004': 'الصوت عنصر مهم جدًا في أي فيديو', 'S006': 'كل ده 50% من جودة الفيديو، والـ 50%', 'S007': 'التانية أوديو',
    'S010': 'لكن لو الصوت وحش ومجلجل وصعب إنه', 'S011': 'يتسمع ويجيب لك صداع غالبًا مش هتكمّل الفيديو حتى لو متصوّر HD',
    'S019': 'بس أنا هنا بستعمل برنامج Adobe Audition', 'S028': 'فاللي هيحصل إن أنا هسجّلك الفيديو بمايك اللابتوب',
    'S029': 'علشان يكون الموضوع متوفر عند كل الناس', 'S039': 'فأول حاجة هنعمل File New Audio File',
    'S061': 'أنا اسمي علي معتز والفيديو ده بنسجّله لليوتيوب',
    'S064': 'أول حاجة عايزين نخلي الدوشة اللي في الخلفية دي تتشال', 'S067': 'إن أنا أختار مكان أنا كنت ساكت فيه مفهوش كلام',
    'S068': 'عشان الدوشة دي هي اللي اسمها الـ Noise', 'S072': 'وهعلّم عليها وأدوس رايت كليك', 'S073': 'وبعد رايت كليك هقوله Capture Noise Print',
    'S076': 'وبعد كده هدوس Ctrl A', 'S077': 'فأنا كده علّمت على الأوديو كامل', 'S082': 'هدوس Effects من فوق', 'S083': 'وهنزل تحت هدوس على',
    'S084': 'Noise Reduction', 'S086': 'عند Noise Reduction Process', 'S092': 'وهنا خلاص خلي الـ Settings زي ما هي كده', 'S093': 'ودوس Apply',
    'S095': 'السلام عليكم أنا اسمي علي معتز', 'S096': 'والفيديو ده بنسجّله لليوتيوب', 'S098': 'مفيش نقطة Noise واحدة',
    'S102': 'في الـ Effects هننزل تحت هندوس على Amplitude والكلمة اللي بعدها', 'S103': 'بعد كده هندوس Normalize', 'S104': 'بعد كده هندوس Apply وهيكون 93.6',
    'S108': 'هدوس Effects وهدوس Special', 'S109': 'بعد كده هدوس Vocal Enhancer', 'S110': 'انت هتختار Male ولا Female',
    'S112': 'انت لو ولد اختار Male ودوس Apply', 'S113': 'وبعد كده دوس Effects تاني', 'S114': 'وبعد كده دوس Special', 'S115': 'وبعد كده دوس Mastering',
    'S117': 'اختار Make Room For Vocals', 'S119': 'ودوس Apply', 'S121': 'وبعد كده اختار Filters', 'S122': 'وبعد كده Parametric Equalizer',
    'S123': 'اختار', 'S124': 'Vocal Enhancer من هنا', 'S126': 'ودوس Apply', 'S128': 'أنا اسمي علي معتز', 'S129': 'والفيديو ده بنسجّله لليوتيوب',
    'S142': 'بس هي دي الإفكتات اللي بستخدمها لما أكون مستعجل في أي فيديو',
}
RED, GREEN = '#FF5A5F', '#35D07F'
STEP = lambda n, en, ar, done, steps: {'n': n, 'en': en, 'ar': ar, 'done': done, 'steps': steps}
# chapter -> (scene id, beats in source seconds, extra props)
SCENES = {
    'hook': ('au_hook2', {'two': 119.2, 'how': 121.0}, {}),
    'tool': ('au_tool', {'au': 88.3}, {}),
    'new': ('au_new', {}, {}),
    'before': ('au_check', {}, {'label': 'قبل · مايك اللابتوب', 'noise': 0.32, 'color': RED, 'title': 'اسمع الصوت *قبل*'}),
    'noise': ('au_step', {'s1': 312.57, 's2': 327.45, 's3': 338.59, 's4': 351.75, 's5': 376.68, 'tip': 390.90},
              {**STEP('01', 'Noise Reduction', 'شيل الدوشة', 0, ['علّم على حتة ساكتة', 'Capture Noise Print', 'Ctrl + A = الأوديو كله', 'Effects ‹ Noise Reduction', 'Apply']), 'tip': 'مفيش نقطة Noise واحدة ✓'}),
    'after': ('au_check', {'ok': 390.90}, {'label': 'بعد Noise Reduction', 'noise': 0.0, 'color': GREEN, 'title': 'وبعد *Noise_Reduction*'}),
    'norm': ('au_step', {'s1': 403.54, 's2': 408.64, 's3': 411.15},
             STEP('02', 'Normalize', 'علّي الصوت', 1, ['Effects ‹ Amplitude', 'Normalize', 'Apply · 93.6%'])),
    've': ('au_step', {'s1': 427.54, 's2': 429.74, 's3': 433.84, 's4': 437.98},
           STEP('03', 'Vocal Enhancer', 'حسّن الصوت', 2, ['Effects ‹ Special', 'Vocal Enhancer', 'Male ولا Female', 'Apply'])),
    'master': ('au_step', {'s1': 441.0, 's2': 443.90, 's3': 447.91, 's4': 452.23},
               STEP('04', 'Mastering', 'ماسترينج', 3, ['Effects ‹ Special', 'Mastering', 'Make Room For Vocals', 'Apply'])),
    'eq': ('au_step', {'s1': 460.52, 's2': 462.40, 's3': 466.14, 's4': 471.43},
           STEP('05', 'Parametric EQ', 'إكولايزر', 4, ['Effects ‹ Filter and EQ', 'Parametric Equalizer', 'Preset: Vocal Enhancer', 'Apply'])),
    'final': ('au_check', {'two': 478.9}, {'label': 'قبل', 'noise': 0.32, 'color': RED, 'title': 'قبل و*بعد*', 'label2': 'بعد الـ 5 إفكتات'}),
    'end': ('au_end', {'fast': 518.53}, {}),
}
# real screen: crop keys (src s, sx, sy, sw) + click boxes (src s, dur, x, y, w, h[, label]) in 1920x1080 source px
EFX = (175, 9, 38, 19)
SCREEN = {
    'new': ([(171.0, 0, 0, 900)], [(172.4, 0.6, 2, 6, 36, 22), (172.9, 0.6, 192, 180, 352, 18), (173.5, 1.4, 576, 202, 224, 18, 'Audio File')]),
    'noise': ([(301.0, 330, 60, 1200), (323.5, 330, 150, 700), (337.0, 330, 60, 1200), (350.8, 0, 0, 900), (362.0, 560, 240, 1100)],
              [(312.4, 2.2, 464, 165, 475, 685), (326.8, 1.6, 730, 468, 170, 21, 'Capture Noise Print'), (338.8, 2.0, 340, 170, 1090, 680, 'Ctrl + A'),
               (351.6, 1.0, *EFX), (354.6, 1.4, 167, 360, 286, 20), (359.4, 1.8, 456, 383, 317, 19), (376.6, 1.0, 1060, 914, 80, 18, 'Apply')]),
    'norm': ([(403.0, 0, 0, 900), (409.4, 640, 300, 640)],
             [(403.5, 0.8, *EFX), (405.3, 1.6, 170, 251, 284, 19), (408.3, 1.2, 481, 450, 216, 18), (410.9, 0.6, 912, 556, 88, 22, 'Apply'), (411.6, 1.0, 900, 458, 60, 16, '93.6')]),
    've': ([(427.0, 0, 0, 900), (431.4, 500, 320, 600)],
           [(427.5, 0.6, *EFX), (428.2, 1.0, 171, 405, 288, 19), (429.7, 1.4, 458, 514, 224, 19), (433.6, 1.8, 613, 480, 43, 13, 'Male'), (437.8, 0.6, 816, 529, 79, 19, 'Apply')]),
    'master': ([(439.7, 0, 0, 900), (444.4, 600, 150, 860)],
               [(441.0, 0.6, *EFX), (442.6, 0.8, 171, 405, 288, 19), (443.8, 0.8, 456, 470, 225, 20), (446.8, 2.6, 694, 236, 200, 18, 'Make Room For Vocals'), (452.0, 0.5, 1234, 632, 76, 20, 'Apply')]),
    'eq': ([(458.3, 0, 0, 900), (464.0, 740, 220, 900)],
           [(458.4, 0.5, *EFX), (460.4, 1.0, 170, 316, 284, 19), (462.4, 1.2, 481, 425, 216, 19), (466.0, 2.4, 824, 556, 166, 20, 'Vocal Enhancer')]),
}
# camera layout (source second, mode): talking head at the start, then the webcam corner of his screen recording
CAM = [(113.45, 'hide'), (88.05, 'mini'), (301.98, 'cmini')]
CTA_KEEP = (7.0, 12.75)
CTA_FIX = {'بعطلك': 'هبعتلك', 'طول.': 'طول'}
SFX = {  # (beat | seconds from scene start, sfx, volume[, dur])
    'au_hook': [(0, 'impact', 0.45), ('half', 'pop_1', 0.4), ('audio', 'pop_2', 0.45), ('bad', 'buzz_wrong', 0.35), ('hd', 'pop_3', 0.4)],
    'au_tool': [('au', 'magic', 0.45), ('lap', 'swoop_up', 0.4), ('all', 'ding', 0.4)],
    'au_new': [(0.3, 'click', 0.6)],
    'au_check': [(0.2, 'tick', 0.4), ('ok', 'ding', 0.45)],
    'au_step': [('s1', 'click', 0.6), ('s2', 'click', 0.6), ('s3', 'click', 0.6), ('s4', 'click', 0.6), ('s5', 'click', 0.6)],
    'au_end': [(0.3, 'swish', 0.4), (0.27, 'pop_1', 0.4), (0.47, 'pop_2', 0.4), (0.67, 'pop_3', 0.4), ('fast', 'magic', 0.4)],
}


def zoom_on(m, aspect=1020 / 880):
    w = min(1400, max(560, m[4] * 1.7)); h = w / aspect
    x = min(1920 - w, max(0, m[2] + m[4] / 2 - w / 2)); y = min(1080 - h, max(0, m[3] + m[5] / 2 - h / 2))
    return round(x), round(y), round(w)


def span(t0, t1, a_force=None, b_force=None):
    i = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t0))
    j = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t1))
    prev = _words[i - 1]['end'] if i > 0 else None
    nxt = _words[j + 1]['start'] if j + 1 < len(_words) else None
    a, b, rep = fit(_words[i]['start'], _words[j]['end'], prev, nxt)
    if a_force: a = a_force; rep += f' START FORCED {a_force}'
    if b_force: b = b_force; rep += f' END FORCED {b_force}'
    KEEP.update(id(w) for w in _words[i:j + 1])
    print('   ', _words[i]['w'], '…', _words[j]['w'], rep)
    return [a, b]


def main():
    ranges, chap = [], []
    for p in PIECES:
        if p[0] == 'raw':
            ranges.append([p[1], p[2]]); print('    RAW', p[1], p[2])
        else:
            ranges.append(span(*p[1:]))
        chap.append(p[0])
    segs, tl = [], 0.0
    for (a, b), c in zip(ranges, chap):
        segs.append({'src': a, 'tl': round(tl, 3), 'len': round(b - a, 3), 'raw': c == 'raw', 'chap': c}); tl += b - a
    main_len = tl

    def to_tl(t):
        for s in segs:
            if s['src'] - 0.01 <= t <= s['src'] + s['len'] + 0.01:
                return s['tl'] + max(0.0, min(t - s['src'], s['len']))
        best = min([(abs(t - s['src']), s['tl']) for s in segs] + [(abs(t - s['src'] - s['len']), s['tl'] + s['len']) for s in segs])
        if best[0] <= 0.7:
            return best[1]
        raise ValueError(f'{t} outside ranges')

    global ENV
    if LV._src is None:
        LV._src = LV.rd(SRC)
    ENV = {}
    hk = [s for s, c in zip(segs, chap) if c == 'hook']
    for c0, s0 in (('before', hk[0]), ('final', hk[1])):
        x = LV._src[int(s0['src'] * LV.SR):int((s0['src'] + s0['len']) * LV.SR)]
        n = max(20, min(150, int(s0['len'] * 30) - 12)); hop = len(x) // n
        ENV[c0] = [float(np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean())) for i in range(n)]
    mx = max(max(v) for v in ENV.values())
    ENV = {k: [round(min(1, (v / mx) ** 0.6), 3) for v in vs] for k, vs in ENV.items()}

    # captions
    words = []
    for snt in tr['sentences']:
        kept = [w for w in snt['words'] if id(w) in KEEP]
        if not kept:
            continue
        txt = TXT.get(snt['id'])
        if txt is None:
            print('  !! no caption text for', snt['id'], ' '.join(w['w'] for w in kept))
        else:
            new = txt.split()
            if len(new) == len(kept):
                kept = [{**w, 'w': x} for w, x in zip(kept, new)]
            else:
                # different count: spread inside each kept RANGE separately is not possible -> only allowed for one-range sentences
                rs = {min(range(len(ranges)), key=lambda r: 0 if ranges[r][0] - 0.05 <= w['start'] < ranges[r][1] else 9) for w in kept}
                if len(rs) > 1:
                    print('  !! word count mismatch across ranges', snt['id'], len(new), len(kept))
                a0, b0 = kept[0]['start'], kept[-1]['end']
                tot = sum(len(x) + 1 for x in new); t = a0; kk = []
                for x in new:
                    d = (b0 - a0) * (len(x) + 1) / tot; kk.append({'w': x, 'start': t, 'end': t + d}); t += d
                kept = kk
        for w in kept:
            ra, rb = min(ranges, key=lambda r: 0 if r[0] - 0.05 <= w['start'] < r[1] else min(abs(w['start'] - r[0]), abs(w['start'] - r[1])))
            words.append({'w': w['w'], 'start': round(to_tl(max(w['start'], ra)), 3), 'end': round(to_tl(max(ra, min(w['end'], rb))), 3)})
    ct = json.load(open(W / 'cta' / 'transcript.json', encoding='utf8'))
    for w in [w for s_ in ct['sentences'] for w in s_['words'] if CTA_KEEP[0] - 0.05 <= w['start'] < CTA_KEEP[1] - 0.05]:
        x = CTA_FIX.get(w['w'], w['w'])
        if x:
            words.append({'w': x, 'start': round(main_len + w['start'] - CTA_KEEP[0], 3), 'end': round(main_len + w['end'] - CTA_KEEP[0], 3)})

    # scenes: one per chapter, from its first piece to the next chapter
    order = []
    for (a, b), c, s in zip(ranges, chap, segs):
        c2 = c if c != 'raw' else order[-1][0]
        if not order or order[-1][0] != c2:
            order.append([c2, s['tl'], s['tl'] + s['len']])
        else:
            order[-1][2] = s['tl'] + s['len']
    scenes = []
    for k, (c, a, b) in enumerate(order):
        t, beats, extra = SCENES[c]
        b2 = order[k + 1][1] if k + 1 < len(order) else main_len
        props = {'b': {n: round(to_tl(v) - a, 3) for n, v in beats.items()}, **extra}
        def rel(t):  # source second -> frames from scene start (a time inside a cut gap snaps to the nearest kept edge)
            try:
                v = to_tl(t)
            except ValueError:
                v = min([(abs(t - g['src']), g['tl']) for g in segs] + [(abs(t - g['src'] - g['len']), g['tl'] + g['len']) for g in segs])[1]
            return round((v - a) * 30)
        if c in SCREEN:
            ks, ms = SCREEN[c]
            ks = sorted(list(ks) + [(m[0] - 0.35, *zoom_on(m)) for m in ms])
            props.update(cam=PJ + 'cam_v3.mp4', camAt=round(a * 30),
                         keys=[{'t': max(0, rel(t0)), 'sx': x, 'sy': y, 'sw': w} for t0, x, y, w in ks],
                         marks=[{'t': rel(m[0]), 'd': round(m[1] * 30), 'x': m[2], 'y': m[3], 'w': m[4], 'h': m[5], **({'label': m[6]} if len(m) > 6 else {})} for m in ms])
        if c == 'hook':
            props['env'], props['env2'] = ENV['before'], ENV['final']
        if c == 'end':
            props['qr'] = PJ + 'qr.png'
        scenes.append({'t': t, 'at': round(a, 3), 'dur': round(b2 - a, 3), 'layer': 'front', 'props': props})
    keys = sorted([{'t': round(to_tl(s), 3) if abs(s - PIECES[0][1]) > 1 and s != 113.45 else 0, 'm': m} for s, m in CAM], key=lambda k: k['t'])

    # sfx
    L = 'sfx/'
    sfx = []
    for i, s in enumerate(scenes):
        if s['at'] > 0.3:
            sfx.append({'file': L + f'whoosh_{i % 3 + 1}.wav', 'at': round(max(0, s['at'] - 0.12), 3), 'vol': 0.4})
        for it in SFX.get(s['t'], []):
            off = s['props']['b'].get(it[0]) if isinstance(it[0], str) else it[0]
            if off is None or off >= s['dur']:
                continue
            sfx.append({'file': L + it[1] + '.wav', 'at': round(s['at'] + off, 3), 'vol': it[2], 'dur': round(it[3] if len(it) > 3 else 3.0, 3)})
    for k in keys[1:]:
        sfx.append({'file': L + 'swish.wav', 'at': k['t'], 'vol': 0.25})
    c0 = main_len + 0.6
    sfx += [{'file': L + 'whoosh_1.wav', 'at': round(main_len - 0.1, 3), 'vol': 0.45}, {'file': L + 'typing.wav', 'at': round(c0 + 30 / 30, 3), 'vol': 0.45, 'dur': 0.9},
            {'file': L + 'pop_2.wav', 'at': round(c0 + 54 / 30, 3), 'vol': 0.55}, {'file': L + 'ding.wav', 'at': round(c0 + 70 / 30, 3), 'vol': 0.5}, {'file': L + 'pop_3.wav', 'at': round(c0 + 92 / 30, 3), 'vol': 0.55}]

    # voice: speech pieces levelled (gain only); raw pieces = his music at a fixed -8 dB with soft fades
    if LV._src is None:
        LV._src = LV.rd(SRC)
    SR = LV.SR; parts, log = [], []
    enh = W / 'voice_enh.wav'
    if not enh.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(SRC), '-vn', '-ac', '1', '-ar', str(SR), '-af',
                        'highpass=f=80,afftdn=nf=-28:nr=14:tn=1,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3,'
                        'equalizer=f=9000:t=h:w=0.7:g=2,acompressor=threshold=-22dB:ratio=3:attack=8:release=120:makeup=3', str(enh)], check=True)
    ENH = LV.rd(enh)
    for s in segs:
        a, b = s['src'], s['src'] + s['len']
        x = LV._src[int(a * SR):int(b * SR)].copy()
        if ENH is not None and s['chap'] not in RAWVOICE:
            x = ENH[int(a * SR):int(b * SR)].copy()
        if s['raw']:
            y = x * 10 ** (-8 / 20); fade = int(0.25 * SR); log.append('raw')
        else:
            y, gs = LV.level(x, [int((t - a) * SR) for t in LV._bounds if a < t < b]); fade = int(0.012 * SR); log.append(gs)
        y[:fade] *= np.linspace(0, 1, fade); y[-fade:] *= np.linspace(1, 0, fade)
        parts.append(y)
    c = LV.rd(ROOT / 'motion-library' / 'public' / (PJ + 'cta.mp4'))[int(CTA_KEEP[0] * SR):int(CTA_KEEP[1] * SR)]
    cy, _ = LV.level(c, []); parts.append(cy)
    out = PUB / 'voice_1_v3.wav'; raw = out.with_suffix('.raw.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', str(raw)], input=np.concatenate(parts).astype(np.float32).tobytes(), check=True)
    m = subprocess.run(['ffmpeg', '-i', str(raw), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(m.split('Integrated loudness:')[1].split('I:')[1].split('LUFS')[0])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', f'volume={-15 - I:.2f}dB,alimiter=limit=0.89:level=false', '-c:a', 'pcm_s16le', str(out)], check=True)
    raw.unlink()
    print('  voice gains:', log)

    # cam.mp4 = the kept pieces of his video, in order (no audio), keyframe every 15 frames for fast seeking
    cam = PUB / 'cam_v3.mp4'
    if '--nocam' not in sys.argv:
        args = ['ffmpeg', '-v', 'error', '-y']
        for s in segs:
            args += ['-ss', f'{s["src"]:.3f}', '-t', f'{s["len"] + 0.2:.3f}', '-i', str(SRC)]
        # exact frame count per piece (= the frames of its range on the 30 fps timeline) -> no drift against the voice
        nf = [round((s['tl'] + s['len']) * 30) - round(s['tl'] * 30) for s in segs]
        fc = ''.join(f'[{i}:v]fps=30,trim=end_frame={nf[i]},setpts=PTS-STARTPTS,settb=1/30[v{i}];' for i in range(len(segs)))
        fc += ''.join(f'[v{i}]' for i in range(len(segs))) + f'concat=n={len(segs)}:v=1:a=0[v]'
        args += ['-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-g', '15', '-pix_fmt', 'yuv420p', str(cam)]
        subprocess.run(args, check=True)
        d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(cam)], capture_output=True, text=True).stdout)
        print(f'  cam.mp4 {d:.2f}s (main {main_len:.2f}s)')

    dur = round(main_len + CTA_KEEP[1] - CTA_KEEP[0], 3)
    props = {'fps': 30, 'duration': dur, 'voice': PJ + 'voice_1_v3.wav', 'segs': [{'src': 0, 'tl': 0, 'len': dur}], 'words': words, 'aly': [],
             'scenes': scenes, 'sfx': sfx, 'look': 'glass', 'capBottom': 0.07, 'ctaVol': 0.0, 'sfxGain': 1.0,
             'cam': {'file': PJ + 'cam_v3.mp4', 'keys': keys},
             'cta': {'file': PJ + 'cta.mp4', 'tl': round(main_len, 3), 'len': round(CTA_KEEP[1] - CTA_KEEP[0], 3), 'src': CTA_KEEP[0]},
             'ctaCue': {'at': 0.6, 'dur': round(CTA_KEEP[1] - CTA_KEEP[0] - 0.6, 3), 'props': {
                 'title': 'اكتب في *كومنت*', 'keyword': 'يوتيوب', 'dm': 'ده لينك الفيديو كامل 🎬', 'typeAt': 30, 'sendAt': 54, 'dmAt': 70, 'top': 0.02, 'qr': PJ + 'qr.png', 'qrAt': 92}}}
    json.dump(props, open(PUB / 'short_1_v3.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'short: {main_len:.1f}s + CTA = {dur:.1f}s ({int(dur // 60)}:{dur % 60:04.1f}) | {len(segs)} pieces, {len(scenes)} scenes')
    for s in scenes:
        print(f"   {s['t']:12s} {s['at']:7.2f} +{s['dur']:5.2f}  {s['props']['b']}")


main()

"""ONE full short 'After Effects -> code' (2026-10-16). Notes: style '2 and 6 and 10' -> mixed look 'lottie':
grainy two-blue background (02), glass cards (10), light VHS touches PLAY/PAUSE OSD + scanlines (06). Structure = style 11
(hook first, then the steps at once). His face = small round webcam from the corner of his screen recording (big webcam only
in the opening, 0-26 s of his video). Code is rebuilt as a clean vector editor (his 720p recording is too small to read);
his real screen (AE panel clicks, browser result, smileys test) big in a glass card with a gold box on every click.
Run: python work/scripts/make_short.py [--nocam]  -> public/projects/<code>/short_1.json, cam.mp4, voice_1.wav"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))

W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
CODE = P.name
PJ = f'projects/{CODE}/'
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
SRC = P / 'input' / '5C4KNFiJFjA.mp4'
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
from edges import fit
import level_voice as LV
_words = [w for s in tr['sentences'] for w in s['words']]
KEEP = set()

# (chapter, first word start, last word start) in source seconds
PIECES = [  # v2 (Aly: "طويل على الفاضي… ابسط واسرع"): hook, after effects, download, json, code, result, vector + compare, summary
    ('hook', 1534.52, 1537.47),
    ('ae', 15.90, 24.50),  # v3: keep the end of the sentence (Android app / website) = the point of the hook
    ('plugin', 139.06, 144.08),
    ('aelook', 27.63, 30.25),  # v3: his animation inside After Effects BEFORE the extension
    ('export', 474.40, 477.16), ('export', 538.92, 543.14),
    ('code', 889.41, 895.64),
    ('run', 1072.50, 1077.16),
    ('use', 1541.97, 1546.55), ('use', 1548.89, 1556.90),  # v3: he presses PLAY / PAUSE + what you can build with it
    ('scale', 1174.15, 1177.07),
    ('eff', 2097.06, 2099.94), ('eff', 2177.10, 2181.22),
    ('end', 2267.57, 2277.10),
]
# caption text per sentence (Whisper spelling fixed; same word count -> word times kept, else spread inside the sentence)
TXT = {
    'S351': 'أنا أعمل ريفرش أدوس Play اشتغل أدوس Pause وقف فدلوقتي أنا عملت',
    'S352': 'الأنيميشن بتاعي أقدر أتحكم فيه بسهولة جدًا وأدوس Play وشغّل',
    'S001': 'السلام عليكم ورحمة الله وبركاته. إزايكم عاملين إيه الأخبار. تمام؟ إن شاء الله ده أول فيديو توتوريال أعمله وإن شاء الله هرفعه على القناة. وفي الفيديو ده هنعرف إزاي نعمل الأنيميشن على الـ After Effects ونحوّله لكود عشان نقدر نستخدمه بعد كده زي ما احنا عايزين سواء في Android Application أو في ويب سايت احنا بنعمله مثلًا. تعالوا بقى نشوف هنعمل الكلام ده إزاي. الأنيميشن اللي انتو شايفينه ده أنا عملته على After Effects أول حاجة أنا عملته إزاي كده الأول مرة جربت',
    'S009': 'فلما جيت حوّلتها بقى لكود بعد كده', 'S010': 'لقيت إن هو الإفكت ده ولا حطه في أي اعتبار',
    'S011': 'وكان الأنيميشن معمول عادي خالص كخط مستقيم',
    'S016': 'مسحت اللير دي', 'S017': 'وفي الآخر عملت', 'S018': 'لير تانية عادية خالص', 'S019': 'وعملتها بشكل الموجة دي',
    'S037': 'البلجن اللي احنا هنستخدمه هو بلجن Open Source وببلاش', 'S038': 'اسمه Bodymovin هتلاقوه على GitHub',
    'S054': 'مش لازم تدفع الـ 20 دولار دول وتدوس Add to Cart', 'S087': 'وغيّرته من ZXP لـ ZIP',
    'S111': 'هتخش في E وتخش على Adobe After Effects', 'S112': 'وبعد كده في Support Files', 'S113': 'هتلاقي فيها فايلات كتير جدًا',
    'S114': 'هتلاقي فيها بقى Extensions',
    'S117': 'وبعد كده لما تعمله هتخش بقى على الحتة دي تعمل وتخش على After Effects وتخش على Edit',
    'S118': 'Preferences بعد كده هتقوم تشوف يعني إيه لك وتعمله وهو هيشتغل عندك زي الفل',
    'S133': 'من Window Extensions هلاقي حاجة اسمها', 'S134': 'Bodymovin ده',
    'S142': 'فهدوس Selected فهيقوم معلّملي عليه', 'S143': 'وبعد كده هقوم أقول له أنا عايز أحطه فين',
    'S151': 'وبعد كده هقوم', 'S152': 'أدوس Render', 'S153': 'كده خلّصهولي ببساطة شديدة',
    'S030': 'الكود ده هو الأنيميشن بتاعنا',
    'S191': 'أو Bodymovin Player هو ده اللي بيشغّل', 'S192': 'الأنيميشن بتاعتك نقول Get the Player',
    'S196': 'فايل جديد اسمه player.js ده فايل الجافاسكريبت بتاعهم',
    'S202': 'انت مش هينفع ترن على فايل HTML وخلاص انت لازم ترن من سيرفر', 'S212': 'فهنا هفتح XAMPP',
    'S237': 'سكريبت ده عشان تقدر تاخد الأنيميشن بتاعك انت محتاج تنادي',
    'S238': 'على فنكشن في كلاس اسمه bodymovin اسمها loadAnimation',
    'S245': 'الأنيميشن بتاعي مكانه فين؟ الفايل .json بتاعي فين؟',
    'S257': 'وأسميه مثلًا animeHERE',
    'S260': 'الـ container ده هديله الـ id بتاعي',
    'S261': 'بتاعه وكذا. اه صح كده. مش هديله اسم الـ id كده وخلاص. أنا لازم',
    'S262': 'أقول له document dot get Element By Id. اه هقول له اللي هو كده أنا إديت له',
    'S272': 'ماشي أدي الأنيميشن بتاعي', 'S273': 'جيت شغلته عادي خالص الموضوع طلع زي', 'S274': 'الفل وعشرة على العشرة طب لو انتو',
    'S275': 'أخدتوا بالكم إن الأنيميشن بتاعي', 'S276': 'اشتغل مرة واحدة', 'S277': 'بس وقف طب إيه المشكلة في كده لو عملت',
    'S279': 'وقف. ده ليه علشان فيه attribute اسمها loop. الـ default بتاعها إنها هي',
    'S280': 'false. أنا هقوم دخلتها. وعملت loop. وقلت لها إنها true. وبعد كده أجي',
    'S281': 'أعمل refresh. أعمل animation. وهتلاقيه بقى عمّال يعيد وكده. طب أهو زي',
    'S288': 'بتاعي ببساطة جدًا عارف لو ده فيديو ممكن يبكسل معاك أكتر من كده', 'S289': 'أو يرخم معاك. علشان تفضل تصغر وتكبر بسهولة وكده. هنا انت بقى',
    'S290': 'تكبر وتصغر بسهولة ما هو مفيش بكسلة أصلًا يعني. تعالوا بقى',
    'S307': 'فاحنا أول حاجة فيه attribute اسمه autoplay', 'S308': 'هعمله false. ونعمل هنا الكوما أول ما عملت الأنيميشن بتاعي',
    'S322': 'عايزين ناخده في variable فهنعمل variable نسميه اسمه animation مثلًا',
    'S353': 'الفيديو بتاعي وأدوس Pause وشغّل الفيديو بتاعي هنا بقى في مجال',
    'S354': 'إبداع كبير جدًا يعني انت ممكن مثلًا تعمل أكتر من شكل أنيميشن',
    'S355': 'وتخلّي كل حاجة لوحدها بزراير معينة انت ممكن تعمل الجيم أصلًا',
    'S348': 'أدوس Play تمام اشتغل الأنيميشن بتاعي زي الفل دلوقتي أنا عايز بقى لما',
    'S350': 'فنكشن اه ما لقيتهاش فيه بس إنه أكيد هيكون فيه Pause فجربتها',
    'S418': 'وكل اللي حصل بس إن أنا عملت event listener', 'S419': 'بحيث إن أول ما انت تشوف الماوس يا معلم داخل في الـ container بتاعي',
    'S420': 'اه Play وأول ما يخرج Stop',
    'S473': 'إن أفضل حاجة الـ Shape Layer الصراحة',
    'S476': 'الـ PNG لو خدتوا بالكم إنه هو بصوا فيه هنا شوية بكسلة مش عارف ظاهرة لكم',
    'S496': 'فرقهم بسيط بس عاجبني أكتر الـ Shape Layer تعالوا نشوف مين أكتر efficient وبياخد مساحة أقل',
    'S497': 'عندي الـ shape ده الفايل بتاع الـ shape نقف عليه هو أربعة كيلو بايت بس',
    'S508': 'المهم هو ده كان إزاي تعمل تحوّل الأنيميشن بتاعك', 'S509': 'لكود عشان تعرف تستخدمه زي ما انت عايز باستخدام بلجن اسمه Bodymovin',
}
# chapter -> (scene id, beats in source seconds, extra props)
SCENES = {
    'hook': ('lt_hook', {'play': 1535.26, 'pause': 1537.07}, {}),
    'ae': ('lt_intro', {'ae': 17.76, 'code': 19.04, 'android': 21.98, 'web': 23.50}, {}),
    'aelook': ('lt_aelook', {}, {}),
    'use': ('lt_use', {'play': 1542.4, 'pause': 1545.5, 'shapes': 1551.44, 'btns': 1554.44, 'game': 1556.54}, {'n': '05'}),
    'plugin': ('lt_plugin', {'free': 139.06, 'name': 142.44, 'gh': 143.78}, {}),
    'export': ('lt_export', {'s1': 474.40, 's2': 538.92, 's3': 542.16, 'json': 542.16},
               {'n': '02', 'steps': ['Window ‹ Extensions ‹ Bodymovin', 'Render', 'النتيجة: ملف json'], 'stepKeys': ['s1', 's2', 's3']}),
    'code': ('lt_code', {'load': 889.41}, {'n': '03'}),
    'run': ('lt_run', {}, {'n': '04'}),
    'scale': ('lt_scale', {'px': 1174.15, 'vec': 1175.15}, {}),
    'eff': ('lt_eff', {'best': 2098.64, 'png': 2099.9, 'kb': 2180.26}, {'n': '06', 'inside': True}),
    'end': ('lt_end', {}, {}),
}
# real screen: crop keys (src s, sx, sy, sw) + click boxes (src s, dur, x, y, w, h[, label]) in 1920x1080 source px
SCREEN = {
    'export': ([(474.0, 0, 0, 960), (538.5, 560, 150, 960)],
               [(474.4, 0.5, 349, 23, 48, 19), (474.9, 1.0, 346, 113, 368, 19), (476.2, 1.0, 726, 136, 188, 19, 'Bodymovin'),
                (538.9, 1.4, 699, 276, 81, 29, 'Render')]),
    'run': ([(1072.0, 300, 80, 1300)], []),
    'aelook': ([(27.5, 460, 60, 1060)], []),
    'use': ([(1541.9, 0, 0, 900)], [(1542.4, 1.0, 16, 540, 97, 42, 'PLAY'), (1545.5, 1.0, 122, 534, 119, 42, 'PAUSE')]),
    'eff': ([(2097.0, 0, 330, 1920), (2177.0, 0, 0, 1250)], [(2098.6, 1.2, 1560, 610, 300, 300, 'Shape Layer'), (2177.6, 3.4, 870, 190, 210, 55, '4 KB')]),
}
# camera: big webcam corner in the opening (his video 0-26 s), small round webcam after
NOZOOM = {'use'}  # keep the whole circle + buttons in view while he clicks
CAM = [(1534.52, 'lmini'), (15.90, 'lbig'), (139.06, 'lmini')]
CTA_KEEP = (7.0, 12.75)
CTA_FIX = {'بعطلك': 'هبعتلك', 'طول.': 'طول'}
SFX = {  # (beat | seconds from scene start, sfx, volume[, dur])
    'lt_hook': [('play', 'click', 0.6), ('play', 'swoop_up', 0.35), ('pause', 'click', 0.6), ('ctl', 'magic', 0.4)],
    'lt_intro': [('ae', 'pop_1', 0.45), ('code', 'typing', 0.4, 0.8), ('android', 'pop_2', 0.45), ('web', 'pop_3', 0.45)],
    'lt_tip': [('fx', 'buzz_wrong', 0.35), ('new', 'swish', 0.4), ('wave', 'ding', 0.4)],
    'lt_plugin': [('free', 'cash', 0.4), ('name', 'magic', 0.4), ('gh', 'pop_2', 0.4)],
    'lt_install': [('cart', 'click', 0.6), ('zip', 'typing', 0.4, 0.7), ('path', 'pop_1', 0.4), ('p2', 'pop_2', 0.4), ('p3', 'pop_3', 0.4), ('p4', 'ding', 0.4)],
    'lt_use': [('play', 'click', 0.6), ('pause', 'click', 0.6), ('shapes', 'pop_1', 0.45), ('btns', 'pop_2', 0.45), ('game', 'magic', 0.45)],
    'lt_aelook': [(0.3, 'pop_1', 0.4)],
    'lt_export': [('s1', 'click', 0.6), ('s2', 'click', 0.6), ('s3', 'click', 0.6), ('s4', 'click', 0.6), ('json', 'magic', 0.45)],
    'lt_player': [('gp', 'click', 0.6), ('js', 'pop_2', 0.45)],
    'lt_server': [('no', 'buzz_wrong', 0.35), ('yes', 'ding', 0.4), ('xampp', 'click', 0.6)],
    'lt_code': [('load', 'typing', 0.4, 1.2), ('path', 'typing', 0.4, 1.0), ('id', 'typing', 0.4, 0.8), ('cont', 'typing', 0.4, 0.8), ('get', 'typing', 0.4, 1.2)],
    'lt_run': [(0.3, 'ding', 0.4), ('once', 'tick', 0.4), ('loop', 'typing', 0.4, 0.8), ('again', 'swoop_up', 0.35)],
    'lt_scale': [('px', 'glitch', 0.3), ('vec', 'swoop_up', 0.4)],
    'lt_control': [('auto', 'typing', 0.4, 0.8), ('var', 'typing', 0.4, 0.8), ('play', 'click', 0.6), ('pause', 'click', 0.6)],
    'lt_hover': [('ev', 'typing', 0.4, 1.0), ('in', 'swoop_up', 0.35), ('stop', 'tick', 0.4)],
    'lt_eff': [(0.3, 'pop_1', 0.4), ('best', 'ding', 0.4), ('png', 'glitch', 0.3), ('kb', 'cash', 0.4)],
    'lt_end': [(0.3, 'swish', 0.4), (0.6, 'pop_1', 0.4), (1.0, 'pop_2', 0.4), (1.4, 'pop_3', 0.4), (1.8, 'ding', 0.4)],
}


def zoom_on(m, aspect=1020 / 880):
    w = min(1400, max(560, m[4] * 1.7)); h = w / aspect
    x = min(1920 - w, max(0, m[2] + m[4] / 2 - w / 2)); y = min(1080 - h, max(0, m[3] + m[5] / 2 - h / 2))
    return round(x), round(y), round(w)


def span(t0, t1):
    i = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t0))
    j = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t1))
    prev = _words[i - 1]['end'] if i > 0 else None
    nxt = _words[j + 1]['start'] if j + 1 < len(_words) else None
    a, b, rep = fit(_words[i]['start'], _words[j]['end'], prev, nxt)
    KEEP.update(id(w) for w in _words[i:j + 1])
    print('   ', _words[i]['w'], '…', _words[j]['w'], rep)
    return [a, b]


def main():
    ranges = [span(*p[1:]) for p in PIECES]
    chap = [p[0] for p in PIECES]
    segs, tl = [], 0.0
    for (a, b), c in zip(ranges, chap):
        segs.append({'src': a, 'tl': round(tl, 3), 'len': round(b - a, 3), 'chap': c}); tl += b - a
    main_len = tl

    def to_tl(t, near=None):
        cands = [s for s in segs if s['src'] - 0.01 <= t <= s['src'] + s['len'] + 0.01]
        if cands:
            s = cands[0] if near is None else min(cands, key=lambda s: abs(s['tl'] - near))
            return s['tl'] + max(0.0, min(t - s['src'], s['len']))
        pool = segs if near is None else [s for s in segs if abs(s['tl'] - near) < 60]
        best = min([(abs(t - s['src']), s['tl']) for s in pool] + [(abs(t - s['src'] - s['len']), s['tl'] + s['len']) for s in pool])
        if best[0] <= 0.9:
            return best[1]
        raise ValueError(f'{t} outside ranges')

    # captions (words kept inside each range)
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
            full = snt['words']
            if len(new) == len(full):
                m = {id(w): x for w, x in zip(full, new)}
                kept = [{**w, 'w': m[id(w)]} for w in kept]
            else:
                print('  !! word count', snt['id'], len(new), len(full), '-> spread')
                a0, b0 = kept[0]['start'], kept[-1]['end']
                tot = sum(len(x) + 1 for x in new); t = a0; kk = []
                for x in new:
                    d = (b0 - a0) * (len(x) + 1) / tot; kk.append({'w': x, 'start': t, 'end': t + d}); t += d
                kept = kk
        for w in kept:
            ra, rb = min(ranges, key=lambda r: 0 if r[0] - 0.05 <= w['start'] < r[1] else min(abs(w['start'] - r[0]), abs(w['start'] - r[1])))
            s0 = to_tl(max(w['start'], ra))
            words.append({'w': w['w'], 'start': round(s0, 3), 'end': round(to_tl(max(ra, min(w['end'], rb)), s0), 3)})
    words.sort(key=lambda w: w['start'])
    ct = json.load(open(W / 'cta' / 'transcript.json', encoding='utf8'))
    for w in [w for s_ in ct['sentences'] for w in s_['words'] if CTA_KEEP[0] - 0.05 <= w['start'] < CTA_KEEP[1] - 0.05]:
        x = CTA_FIX.get(w['w'], w['w'])
        if x:
            words.append({'w': x, 'start': round(main_len + w['start'] - CTA_KEEP[0], 3), 'end': round(main_len + w['end'] - CTA_KEEP[0], 3)})

    # scenes: one per chapter
    order = []
    for c, s in zip(chap, segs):
        if not order or order[-1][0] != c:
            order.append([c, s['tl'], s['tl'] + s['len']])
        else:
            order[-1][2] = s['tl'] + s['len']
    scenes = []
    for k, (c, a, b) in enumerate(order):
        t, beats, extra = SCENES[c]
        b2 = order[k + 1][1] if k + 1 < len(order) else main_len
        mid = (a + b2) / 2
        props = {'b': {n: round(to_tl(v, mid) - a, 3) for n, v in beats.items()}, **extra}

        def rel(t):
            return round((to_tl(t, mid) - a) * 30)
        if c in SCREEN:
            ks, ms = SCREEN[c]
            ks = sorted(list(ks) + ([] if c in NOZOOM else [(m[0] - 0.35, *zoom_on(m)) for m in ms]), key=lambda k_: rel(k_[0]))
            props.update(cam=PJ + 'cam_v3.mp4', camAt=round(a * 30),
                         keys=[{'t': max(0, rel(t0)), 'sx': x, 'sy': y, 'sw': w} for t0, x, y, w in ks],
                         marks=[{'t': rel(m[0]), 'd': round(m[1] * 30), 'x': m[2], 'y': m[3], 'w': m[4], 'h': m[5], **({'label': m[6]} if len(m) > 6 else {})} for m in ms])
        if c == 'end':
            props['qr'] = PJ + 'qr.png'
        scenes.append({'t': t, 'at': round(a, 3), 'dur': round(b2 - a, 3), 'layer': 'front', 'props': props})
    keys = [{'t': 0 if i == 0 else round(to_tl(s), 3), 'm': m} for i, (s, m) in enumerate(CAM)]

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
    c0 = main_len + 0.6
    sfx += [{'file': L + 'whoosh_1.wav', 'at': round(main_len - 0.1, 3), 'vol': 0.45}, {'file': L + 'typing.wav', 'at': round(c0 + 1, 3), 'vol': 0.45, 'dur': 0.9},
            {'file': L + 'pop_2.wav', 'at': round(c0 + 54 / 30, 3), 'vol': 0.55}, {'file': L + 'ding.wav', 'at': round(c0 + 70 / 30, 3), 'vol': 0.5}, {'file': L + 'pop_3.wav', 'at': round(c0 + 92 / 30, 3), 'vol': 0.55}]
    missing = sorted({x['file'] for x in sfx if not (ROOT / 'motion-library' / 'public' / x['file']).exists()})
    if missing:
        print('  !! missing sfx', missing)

    # voice: his ORIGINAL audio, gain only (per sentence to one level), then -15 LUFS
    LV._src = LV.rd(SRC)
    SR = LV.SR; parts, log = [], []
    for s in segs:
        a, b = s['src'], s['src'] + s['len']
        x = LV._src[int(a * SR):int(b * SR)].copy()
        y, gs = LV.level(x, [int((t - a) * SR) for t in LV._bounds if a < t < b]); fade = int(0.012 * SR); log.append(gs)
        y[:fade] *= np.linspace(0, 1, fade); y[-fade:] *= np.linspace(1, 0, fade)
        parts.append(y)
    c = LV.rd(PUB / 'cta.mp4')[int(CTA_KEEP[0] * SR):int(CTA_KEEP[1] * SR)]
    cy, _ = LV.level(c, []); parts.append(cy)
    out = PUB / 'voice_1_v3.wav'; raw = out.with_suffix('.raw.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', str(raw)], input=np.concatenate(parts).astype(np.float32).tobytes(), check=True)
    m = subprocess.run(['ffmpeg', '-i', str(raw), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(m.split('Integrated loudness:')[1].split('I:')[1].split('LUFS')[0])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', f'volume={-15 - I:.2f}dB,alimiter=limit=0.89:level=false', '-c:a', 'pcm_s16le', str(out)], check=True)
    raw.unlink()

    # cam.mp4 = the kept pieces of his video in order (no audio), upscaled to 1920x1080 (Screen/Cam work in 1080p px)
    cam = PUB / 'cam_v3.mp4'
    if '--nocam' not in sys.argv:
        args = ['ffmpeg', '-v', 'error', '-y']
        for s in segs:
            args += ['-ss', f'{s["src"]:.3f}', '-t', f'{s["len"] + 0.2:.3f}', '-i', str(SRC)]
        nf = [round((s['tl'] + s['len']) * 30) - round(s['tl'] * 30) for s in segs]
        fc = ''.join(f'[{i}:v]fps=30,trim=end_frame={nf[i]},setpts=PTS-STARTPTS,settb=1/30,scale=1920:1080:flags=lanczos[v{i}];' for i in range(len(segs)))
        fc += ''.join(f'[v{i}]' for i in range(len(segs))) + f'concat=n={len(segs)}:v=1:a=0[v]'
        args += ['-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-g', '15', '-pix_fmt', 'yuv420p', str(cam)]
        subprocess.run(args, check=True)
        d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(cam)], capture_output=True, text=True).stdout)
        print(f'  cam.mp4 {d:.2f}s (main {main_len:.2f}s)')

    dur = round(main_len + CTA_KEEP[1] - CTA_KEEP[0], 3)
    props = {'fps': 30, 'duration': dur, 'voice': PJ + 'voice_1_v3.wav', 'segs': [{'src': 0, 'tl': 0, 'len': dur}], 'words': words, 'aly': [],
             'scenes': scenes, 'sfx': sfx, 'look': 'lottie', 'capBottom': 0.06, 'ctaVol': 0.0, 'sfxGain': 1.0,
             'cam': {'file': PJ + 'cam_v3.mp4', 'keys': keys},
             'cta': {'file': PJ + 'cta.mp4', 'tl': round(main_len, 3), 'len': round(CTA_KEEP[1] - CTA_KEEP[0], 3), 'src': CTA_KEEP[0]},
             'ctaCue': {'at': 0.6, 'dur': round(CTA_KEEP[1] - CTA_KEEP[0] - 0.6, 3), 'props': {
                 'title': 'اكتب في *كومنت*', 'keyword': 'يوتيوب', 'dm': 'ده لينك الفيديو كامل 🎬', 'typeAt': 30, 'sendAt': 54, 'dmAt': 70, 'top': 0.02, 'qr': PJ + 'qr.png', 'qrAt': 92}}}
    json.dump(props, open(PUB / 'short_1_v3.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'short: {main_len:.1f}s + CTA = {dur:.1f}s ({int(dur // 60)}:{dur % 60:04.1f}) | {len(segs)} pieces, {len(scenes)} scenes')
    for s in scenes:
        print(f"   {s['t']:11s} {s['at']:7.2f} +{s['dur']:5.2f}  {s['props']['b']}")


main()

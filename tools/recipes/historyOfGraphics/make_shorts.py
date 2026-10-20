"""Vertical shorts (look 'hist') from Aly's video "تاريخ الجرافيكس" (cdkvUAgSoKc, 12:25, 2026-10-10).
Aly's brief: the whole short = ONE continuous motion-graphics shot along a TIMELINE (old on the left, new on the right); the camera
walks left -> right while he explains, slows / stops on an era for effects, zooms in / out, then walks on. His face: BIG cut-out
in the opening only, then a small round webcam to the end, never covering motion. Real photos / his video inserts = small circles
next to the drawing. Music + sound effects. Drawing style from his references (Egyptian kit, Egyptian Stories opener, Mazepa, Tamim).
Ideas (my list, he asked for the best first): 3 fear of death invented writing, 4 dead sciences / pyramids, 5 stone -> paper -> print,
7 the main skill of every era, 9 the whole history in one minute.
Inputs : work/transcript.json, work/cta/transcript.json, public/projects/<code>/{cta.mp4, roto_*.webm, clips/, pics/, music/}
Output : motion-library/public/projects/<code>/short_<n>.json  (composition 'film-short', scene 'hworld' = src/hist/world.tsx)
Run    : python work/scripts/make_shorts.py [n ...]   then  sh work/scripts/check.sh <n>  /  sh work/scripts/render.sh <n...>
All times below are SOURCE seconds (his video); they are mapped to the short's timeline."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
CODE = P.name
PJ = f'projects/{CODE}/'
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
SRC = P / 'input' / 'cdkvUAgSoKc.mp4'
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
from edges import fit
from level_voice import build as build_voice
_words = [w for s in tr['sentences'] for w in s['words']]

# caption spelling (Whisper misheard)
WFIX = {'الخضرات': 'الحضارات', 'حضرات': 'حضارات', 'الحضرات': 'الحضارات', 'بصنات': 'بصمات', 'الهيلوغرفية': 'الهيروغليفية', 'وعالحطان': 'وعالحيطان',
        'وينحطوها': 'وينحتوها', 'المنطوك': 'المنطوق', 'المبزول': 'المبذول', 'فحشان': 'فعشان', 'اتعاملت': 'اتعملت', 'توديل': 'توديه', 'سابت': 'ثابت',
        'وبأصبح': 'وأصبح', 'تغيره': 'اتغيرت', 'الصرعة': 'السرعة', 'الآلب': 'القالب', 'آلب': 'قالب', 'تتقلب': 'تتقولب', 'اللغريفي': 'الهيروغليفي',
        'تدر': 'تقدر', 'ورد': 'Word', 'قل': 'الأقل', 'وتخلت': 'وتخلّد', 'هتحرك': 'هيتحرك', 'كنت': 'كانت', 'نازم': 'لازم', 'Graphics؟': 'الجرافيكس؟',
        'بال': '', 'سمع': 'السلام', 'أسلب': 'باحاول', 'محاول': '', 'وبيت': 'وبقت', 'بيت': 'بقت', 'تعلقوا': 'تعلقها', 'المحور': 'الحيطة', 'دمكت': 'دمجت',
        'لنبس': 'لأني', 'معك': 'بتكلم معاك', 'عايش': 'عايز', 'سقوله': 'تقوله', 'هيباليها': 'هيبقى ليها', 'جدوة': 'جدوى', 'بعرفتش': 'معرفتش',
        'فعمل': 'فعامل', 'الواحده': 'الواحد', 'زكي': 'ذكي', 'تكيفا': 'تكيّفًا', 'أسعى': 'أسرع', 'راح': 'واحد', 'تسهله': 'تسهّل له', 'البناء': 'بني',
        'ادمين': 'آدم', 'عيزة': 'عبرة', 'كرة': 'كده', 'حلطيته': 'حطيته', 'أصد': 'قصاد', 'عنت': 'عالنت', 'متدائم': 'متضايق', 'رخيم': 'رخم',
        'بيتحك': 'بيضحك', 'منتاج': 'مونتاج', 'كورسي': 'كورس', 'وهيزبقك': 'وهيسبقك', 'محتاجنا': 'محتاجين', 'تقلب': 'تقلبها', 'مبزول': 'مبذول'}
WFIX_AT = {236.48: 'علّى', 349.78: 'قلّ', 551.88: 'الأقل', 210.08: 'كنت'}  # same word, different fix by position

SPANS = {
    3: [(190.50, 259.70)],
    4: [(283.66, 288.74), (260.14, 283.14), (289.04, 319.06)],
    5: [(319.52, 355.06), (358.64, 379.24)],
    7: [(540.30, 547.02), (547.44, 562.48), (519.88, 539.90), (651.72, 656.84)],
    1: [(25.45, 86.72)],
    2: [(109.24, 160.78), (172.52, 183.36)],
    6: [(446.80, 464.50), (469.90, 512.22)],
    8: [(626.92, 651.40), (595.08, 625.44)],
    9: [(0.84, 6.90), (87.30, 94.44), (203.80, 213.48), (217.66, 221.20), (319.52, 321.10), (324.28, 326.04), (359.86, 364.16), (379.74, 382.10),
        (419.38, 423.02), (536.02, 539.90), (651.72, 656.84)],
}
BIG = {3: (190.0, 197.4), 4: (283.0, 288.74), 5: (319.0, 326.04), 7: (539.8, 547.02), 9: (0.3, 6.9), 1: (25.0, 32.6), 2: (109.0, 115.6), 6: (446.5, 450.62), 8: (626.6, 634.6)}  # opening = big round webcam until this source second
MUSIC = {3: ('atlas_egypt', 0.0, 0.11), 4: ('atlas_egypt', 40.0, 0.11), 5: ('curious_minds', 20.0, 0.12), 7: ('curious_minds', 60.0, 0.11), 9: ('curious_minds', 0.0, 0.13), 1: ('curious_mind', 0.0, 0.1), 2: ('travel_egypt', 20.0, 0.07), 6: ('curious_minds', 90.0, 0.11), 8: ('curious_mind', 30.0, 0.1)}
CTA_KEEP = (0.0, 6.0)
CTA_FIX = {'علي': 'على', 'وهو': 'وهبعتهولك', 'اعطولك': '', 'طول.': 'طول'}
X = {'speech': 600, 'village': 1450, 'cave': 2350, 'sumer': 3450, 'egypt': 4550, 'pyramids': 5650, 'china': 6750, 'rome': 7800, 'paper': 8900,
     'baghdad': 10050, 'press': 11250, 'computer': 12400, 'now': 13600, 'weak': -700, 'future': 14900}
STONE, SPEECH, PAPER, PRINT, PC, GFX = [0.05, 0.65, 0.9], [0.2, 0.1, 0.2], [0.75, 0.3, 0.55], [0.9, 0.25, 0.85], [0.95, 0.2, 0.9], [1.0, 0.05, 1.0]
C = lambda n: PJ + f'clips/{n}.mp4'
I = lambda n: PJ + f'pics/{n}.jpg'
CLEN = {'cave_panel': 2.7, 'rockart': 1.7, 'hands': 2.7, 'horse': 0.8, 'lions': 0.8, 'tablet': 3.7, 'hiero': 1.8, 'chinese': 0.8, 'latin': 1.8, 'karnak': 0.8,
        'ceiling': 1.8, 'pyramids': 2.9, 'towers': 1.8, 'ramp1': 1.7, 'ramp2': 1.8, 'water': 2.7, 'paper': 3.8, 'letters': 3.7, 'abubakr': 4.7,
        'gutenberg': 1.8, 'press': 3.8, 'bible': 7.8, 'posters': 9.7, 'propaganda': 4.8, 'tv': 4.8}


def pic(at, out, name, st, dx=0, y=760, label=None, img=False, d=None, pos=None):
    p = {'at': at, 'out': out, 'src': I(name) if img else C(name), 'x': X[st] + dx, 'y': y}
    if not img:
        p.update(video=True, len=CLEN[name])
    if label: p['label'] = label
    if d: p['d'] = d
    if pos: p['pos'] = pos
    return p


def cam(*k):  # (t, station or x, z[, dx])
    out = []
    for e in k:
        t, s, z = e[0], e[1], e[2]
        x = (X[s] if isinstance(s, str) else s) + (e[3] if len(e) > 3 else 0)
        out.append({'t': t, 'x': x, 'z': z})
    return out


def ev(*k):  # (station, action, at[, out])
    return [dict(s=e[0], k=e[1], at=e[2], **({'out': e[3]} if len(e) > 3 else {})) for e in k]


def wd(at, out, text, y=0.25, size=96, color=None):
    w = {'at': at, 'out': out, 'text': text, 'y': y, 'size': size}
    if color: w['color'] = color
    return w


def burst(at, st, y=900, dx=0, c=None):
    b = {'at': at, 'x': X[st] + dx, 'y': y}
    if c: b['c'] = c
    return b


PLAN = {
    # ---------------- 3: fear of death invented writing ----------------
    3: dict(
        cam=cam((190.5, 'cave', 0.62, -900), (191.5, 'cave', 0.62, -700), (192.2, 'now', 0.62), (193.0, 'now', 0.62), (194.2, 7000, 0.37),
                (195.0, 'cave', 0.62, -700), (195.9, 'cave', 0.62, -600), (196.7, 'now', 0.62), (197.6, 'now', 0.62), (198.8, 7000, 0.37),
                (200.3, 'egypt', 0.95), (203.4, 'egypt', 1.0, 80), (205.0, 'cave', 1.0), (207.6, 'cave', 1.05, 60), (209.2, 'cave', 1.45, -260),
                (210.6, 'cave', 1.4, -200), (213.3, 'sumer', 1.0), (216.4, 'sumer', 1.15, -150), (217.9, 4000, 0.6), (219.9, 4000, 0.6), (220.7, 7275, 0.6),
                (226.8, 7300, 0.62), (229.8, 'egypt', 0.95), (233.4, 'egypt', 1.1, -100), (235.5, 'egypt', 1.0), (241.5, 'egypt', 0.9, 60),
                (244.9, 'egypt', 1.0, -100), (248.7, 'egypt', 1.6, -330), (255.0, 'egypt', 1.65, -300), (256.6, 'egypt', 0.8, 300), (259.7, 'egypt', 0.75, 700)),
        ev=ev(('speech', 'talk', 190.5), ('now', 'video', 192.0), ('now', 'icons', 192.3), ('egypt', 'hiero', 200.5), ('cave', 'paint', 206.1),
              ('cave', 'hands', 208.2), ('sumer', 'cune', 215.8), ('egypt', 'hiero', 218.3), ('sumer', 'cune', 219.6), ('china', 'bamboo', 220.6),
              ('rome', 'latin', 221.2), ('egypt', 'carve', 230.9, 236.0)),
        era=[{'at': 190.5, 'st': 'speech'}, {'at': 192.0, 'st': 'now'}, {'at': 200.4, 'st': 'egypt'}, {'at': 204.8, 'st': 'cave'}, {'at': 212.7, 'st': 'sumer'},
             {'at': 218.3, 'st': 'egypt'}, {'at': 219.6, 'st': 'sumer'}, {'at': 220.6, 'st': 'china'}, {'at': 221.2, 'st': 'rome'}, {'at': 230.0, 'st': 'egypt'}],
        meters=[{'at': 227.2, 'v': SPEECH}, {'at': 229.4, 'v': [0.2, 0.1, 0.9]}, {'at': 238.6, 'v': [0.2, 0.1, 0.95]}, {'at': 243.2, 'v': [0.05, 0.1, 0.95]},
                {'at': 248.0, 'v': [0.05, 0.65, 0.95]}],
        words=[wd(190.5, 191.5, 'زمان'), wd(191.64, 192.8, 'دلوقتي'), wd(192.9, 194.2, 'وبعدين؟'), wd(195.2, 199.2, 'الخوف من الموت', size=104),
               wd(200.7, 203.6, 'يخلّدوا اسمهم', y=0.27), wd(201.74, 203.6, 'وعلمهم', y=0.32, size=80), wd(202.66, 203.6, 'وأخبارهم', y=0.39, size=80),
               wd(209.6, 210.8, 'أنا كنت هنا!', size=104), wd(216.2, 217.6, 'رموز', size=110), wd(229.4, 231.0, 'بقاء أعلى ▲', color='#8EE59B'),
               wd(243.2, 244.8, 'مش بيتحرك من مكانه', size=84), wd(252.2, 255.3, 'نفك الرموز؟', size=96), wd(256.6, 259.6, 'الكتابة = بقاء', size=104)],
        pics=[pic(206.3, 209.0, 'horse', 'cave', 330, 640, 'كهف لاسكو'), pic(208.6, 211.0, 'hands', 'cave', -350, 620, 'كهف الأيادي'),
              pic(215.9, 219.0, 'tablet', 'sumer', 300, 620, 'لوح مسماري'), pic(218.3, 223.6, 'hiero', 'egypt', 0, 520, 'هيروغليفي', d=200),
              pic(219.6, 223.8, 'cuneiform', 'sumer', 0, 520, 'سومري', img=True, d=200), pic(220.6, 224.0, 'chinese', 'china', 0, 520, 'صيني', d=200),
              pic(221.2, 224.2, 'latin', 'rome', -200, 520, 'لاتيني', d=200), pic(232.2, 234.0, 'karnak', 'egypt', 330, 600, 'معابد'),
              pic(233.9, 236.0, 'ceiling', 'egypt', -330, 600, 'جدران المعابد'), pic(249.6, 255.3, 'rosetta', 'egypt', 200, 600, 'حجر رشيد', img=True)],
        bursts=[burst(200.6, 'egypt', 850), burst(208.2, 'cave', 900), burst(218.3, 'egypt', 900, c='#F2B531'), burst(219.6, 'sumer', 900, c='#F2B531'),
                burst(220.6, 'china', 900, c='#F2B531'), burst(221.2, 'rome', 900, c='#F2B531'), burst(256.6, 'egypt', 850)],
    ),
    # ---------------- 4: dead sciences / pyramids ----------------
    4: dict(
        cam=cam((283.66, 'pyramids', 0.75, 250), (285.9, 'pyramids', 0.95), (288.0, 'pyramids', 1.2, -150), (260.14, 'village', 0.7, -400),
                (262.9, 'speech', 0.95, 300), (266.0, 'village', 1.0, -100), (269.5, 'village', 1.05), (274.0, 'village', 1.1, 40), (280.0, 'village', 0.9, 120),
                (283.1, 'village', 0.8, 400), (289.3, 'pyramids', 0.9, 500), (291.5, 'pyramids', 0.95, 400), (293.6, 'pyramids', 0.95, -150),
                (298.0, 'pyramids', 1.0, -200), (300.5, 'pyramids', 0.9), (304.9, 'pyramids', 0.85, 100), (307.7, 'pyramids', 0.7, 300), (309.6, 4000, 0.6),
                (310.9, 4000, 0.6), (311.7, 7275, 0.6), (316.0, 7300, 0.62), (319.06, 7400, 0.6)),
        ev=ev(('pyramids', 'q', 287.4), ('village', 'talk', 263.0), ('speech', 'talk', 263.4), ('village', 'fade', 275.2), ('pyramids', 'crane', 290.2),
              ('pyramids', 'ramp1', 293.6), ('pyramids', 'ramp2', 295.5), ('pyramids', 'x1', 298.6), ('pyramids', 'x2', 299.4), ('pyramids', 'q', 300.5),
              ('egypt', 'hiero', 310.6), ('sumer', 'cune', 310.6), ('china', 'bamboo', 311.7), ('rome', 'latin', 312.0)),
        era=[{'at': 285.9, 'st': 'pyramids'}, {'at': 262.9, 'st': 'village'}, {'at': 289.3, 'st': 'pyramids'}, {'at': 311.26, 'st': 'egypt'}],
        words=[wd(287.8, 288.7, 'اتعملت إزاي؟!', size=104), wd(261.0, 262.6, 'مش كل الحضارات اتكتبت', size=80), wd(264.0, 266.4, 'قبل الكتابة', size=96),
               wd(268.4, 269.4, 'ماتت', size=110, color='#FF8A6A'), wd(273.3, 274.0, 'إفريقيا', size=96), wd(279.6, 280.5, 'هتموت', size=110, color='#FF8A6A'),
               wd(282.6, 283.1, 'علوم ماتت', size=104, color='#FF8A6A'), wd(290.2, 292.2, 'نقدر نبنيها دلوقتي', size=84),
               wd(293.6, 297.5, 'نظريات', size=104), wd(302.7, 304.5, 'ولا طريقة تانية خالص؟', size=84), wd(306.5, 308.0, 'علم مات', size=110, color='#FF8A6A'),
               wd(311.26, 313.8, 'اللي كتبت تاريخها عاشت', size=84), wd(315.1, 316.9, 'الخوف من الموت', y=0.25, size=80),
               wd(317.46, 319.06, 'نشر العلم', y=0.32, size=80), wd(318.74, 319.06, 'الأخبار', y=0.39, size=80)],
        pics=[pic(285.9, 288.7, 'pyramids', 'pyramids', 330, 560, 'أهرامات الجيزة'), pic(270.0, 274.0, 'rockart', 'village', 330, 600, 'رسومات منطوقة؟'),
              pic(290.3, 292.5, 'towers', 'pyramids', 350, 560, 'علوم النهاردة'), pic(293.8, 295.9, 'ramp1', 'pyramids', 330, 560, 'نظرية'),
              pic(295.9, 298.0, 'ramp2', 'pyramids', 330, 560, 'نظرية تانية'), pic(300.9, 304.5, 'water', 'pyramids', 330, 560, 'ولا دي؟'),
              pic(310.4, 311.6, 'papyrus', 'egypt', 0, 520, 'بردية', img=True, d=200), pic(310.6, 311.6, 'tablet', 'sumer', 0, 520, 'سومري', d=200),
              pic(311.7, 314.5, 'bamboo', 'china', 0, 520, 'صيني', img=True, d=200), pic(312.0, 314.5, 'trajan', 'rome', -200, 520, 'روماني', img=True, d=200)],
        bursts=[burst(287.4, 'pyramids', 800), burst(310.6, 'egypt', 900, c='#F2B531'), burst(310.6, 'sumer', 900, c='#F2B531'),
                burst(311.7, 'china', 900, c='#F2B531'), burst(312.0, 'rome', 900, c='#F2B531')],
    ),
    # ---------------- 5: stone -> paper -> printing press ----------------
    5: dict(
        cam=cam((319.52, 'rome', 0.8, -300), (321.1, 'paper', 0.95), (323.6, 'paper', 0.95, -60), (326.4, 'paper', 1.0, 60), (330.0, 'paper', 1.05, -50),
                (332.4, 'paper', 0.9, 80), (334.4, 'paper', 0.82), (337.5, 'paper', 0.9, 100), (343.3, 'paper', 1.2, -40), (346.9, 'paper', 0.95),
                (350.3, 'paper', 0.9, -80), (355.0, 'paper', 0.9, 200), (358.64, 'baghdad', 0.85, -300), (359.3, 'baghdad', 0.95), (360.6, 'baghdad', 1.0, 60),
                (362.2, 'press', 0.95), (363.7, 'press', 1.15, -60), (366.5, 'press', 1.0), (369.2, 'press', 0.95, 150), (372.8, 'press', 0.8, 450),
                (375.4, 'press', 0.7, 500), (379.2, 11900, 0.62)),
        ev=ev(('rome', 'latin', 319.5), ('paper', 'book', 321.1), ('paper', 'sheets', 330.4), ('paper', 'ship', 335.4), ('paper', 'pigeon', 336.5),
              ('baghdad', 'lib', 358.64), ('baghdad', 'burn', 359.6), ('baghdad', 'ink', 360.4), ('press', 'press', 362.3), ('press', 'copies', 370.8)),
        era=[{'at': 321.1, 'st': 'paper'}, {'at': 358.9, 'st': 'baghdad'}, {'at': 361.7, 'st': 'press'}],
        meters=[{'at': 321.9, 'v': STONE}, {'at': 325.5, 'v': [0.75, 0.65, 0.9]}, {'at': 343.3, 'v': [0.75, 0.3, 0.9]}, {'at': 349.8, 'v': PAPER},
                {'at': 368.4, 'v': [0.9, 0.3, 0.55]}, {'at': 374.9, 'v': [0.9, 0.3, 0.85]}],
        words=[wd(320.5, 321.4, 'الورق', size=110), wd(327.5, 328.6, 'معبد ثابت', size=96), wd(331.5, 332.4, 'أي حتة في العالم', size=84),
               wd(333.2, 334.4, 'أسرع من الكلام!', size=96), wd(345.2, 346.9, 'حروف ← كلمات', size=96), wd(358.64, 359.9, 'مكتبة بغداد', size=96),
               wd(363.6, 364.6, 'طفرة!', size=120), wd(370.4, 372.9, 'نسخ… نسخ… نسخ', size=90), wd(378.0, 379.2, 'بقاء أعلى ▲', color='#8EE59B')],
        pics=[pic(321.2, 325.5, 'paper', 'paper', 330, 600, 'صناعة الورق'), pic(327.3, 328.8, 'karnak_wall', 'paper', -330, 600, 'الكتابة على المعابد', img=True),
              pic(330.0, 332.4, 'gbible', 'paper', 330, 600, 'كتاب', img=True), pic(336.0, 338.2, 'ship', 'paper', 330, 600, 'مركب', img=True),
              pic(336.8, 339.0, 'pigeon', 'paper', -330, 560, 'حمام زاجل', img=True), pic(344.5, 347.0, 'letters', 'paper', 330, 600, 'الحروف'),
              pic(350.9, 353.4, 'trajan', 'paper', -330, 600, 'حفر في الصخر', img=True), pic(353.5, 355.0, 'gbible', 'paper', 330, 600, 'كتاب', img=True),
              pic(359.2, 361.6, 'baghdad1258', 'baghdad', 330, 560, 'سقوط بغداد 1258', img=True), pic(363.0, 365.0, 'gutenberg', 'press', 330, 560, 'جوتنبرج'),
              pic(365.0, 368.8, 'press', 'press', 330, 560, 'مطبعة جوتنبرج'), pic(369.5, 373.0, 'bible', 'press', 330, 560, 'أول كتاب مطبوع')],
        bursts=[burst(321.1, 'paper', 900), burst(363.6, 'press', 850), burst(375.4, 'press', 850, 300, c='#8EE59B')],
    ),
    # ---------------- 7: the main skill of every era ----------------
    7: dict(
        cam=cam((540.3, 'speech', 0.95), (542.8, 'speech', 1.05, 60), (544.7, 'egypt', 0.95), (545.3, 'egypt', 0.95, 60), (547.0, 'computer', 1.0),
                (548.7, 'now', 1.0), (550.9, 'now', 1.05, 60), (553.2, 'now', 1.0, -40), (557.7, 'now', 0.9), (559.5, 7000, 0.37), (562.48, 7100, 0.37),
                (519.88, 'now', 0.95), (522.5, 'now', 1.0), (526.0, 'now', 0.9, -40), (531.5, 'now', 0.88, 40), (535.5, 'now', 0.95), (539.9, 'now', 1.1, 60),
                (651.72, 'now', 1.2), (656.84, 'now', 0.85, -100)),
        ev=ev(('speech', 'talk', 541.0), ('speech', 'chain', 542.0), ('egypt', 'hiero', 544.5), ('computer', 'type', 546.5), ('now', 'video', 550.9),
              ('now', 'icons', 553.2), ('cave', 'hands', 559.0), ('now', 'video', 519.9), ('now', 'icons', 535.5), ('now', 'world', 652.0)),
        era=[{'at': 540.3, 'st': 'speech'}, {'at': 544.5, 'st': 'egypt'}, {'at': 546.6, 'st': 'computer'}, {'at': 548.6, 'st': 'now'}],
        meters=[{'at': 535.9, 'v': [0.5, 0.5, 0.5]}, {'at': 537.04, 'v': [0.5, 0.5, 1.0]}, {'at': 538.28, 'v': [1.0, 0.5, 1.0]}, {'at': 539.9, 'v': GFX}],
        words=[wd(542.5, 543.2, 'تتكلم', size=110), wd(544.5, 545.3, 'تكتب', size=110), wd(546.8, 547.4, 'Word', size=110),
               wd(550.9, 552.2, 'فيديو', size=110), wd(553.2, 554.2, 'ديزاين', size=110), wd(555.0, 557.6, 'معلومتك', y=0.25, size=80),
               wd(556.2, 557.6, 'خبرتك', y=0.32, size=80), wd(557.0, 557.6, 'قصتك', y=0.39, size=80), wd(560.8, 562.48, 'تخلّد اسمك', size=110),
               wd(520.5, 523.0, 'أي قالب', size=104), wd(534.9, 535.9, 'ده جرافيكس!', size=104), wd(655.8, 656.84, 'الجرافيكس والفيديو', size=90)],
        pics=[pic(560.4, 562.48, 'hands', 'rome', -800, 600, 'أنا كنت هنا'), pic(523.6, 535.2, 'ibmpc', 'now', -340, 640, 'فيديو على هارد', img=True, d=210),
              pic(526.0, 535.2, 'unclesam', 'now', 340, 640, 'مطبوع', img=True, d=210, pos='50% 20%'), pic(528.2, 535.2, 'posters', 'now', -340, 1000, 'على الحيطة', d=210),
              pic(531.5, 535.2, 'hiero', 'now', 340, 1000, 'منحوت في الصخر', d=210), pic(651.8, 655.0, 'tv', 'now', 330, 560, 'فيديو')],
        bursts=[burst(523.6, 'now', 700, -340, c='#F2B531'), burst(526.0, 'now', 700, 340, c='#F2B531'), burst(528.2, 'now', 1000, -340, c='#F2B531'),
                burst(531.5, 'now', 1000, 340, c='#F2B531'), burst(559.5, 'cave', 900), burst(537.0, 'now', 850)],
    ),
    # ---------------- 9: the whole history in one minute ----------------
    9: dict(
        cam=cam((0.84, 7000, 0.36), (2.0, 'egypt', 0.6), (2.6, 'egypt', 0.62), (3.5, 'cave', 0.6), (4.3, 'now', 0.6), (5.3, 7000, 0.36), (6.9, 7100, 0.36),
                (87.3, 'speech', 0.9, -200), (88.5, 'speech', 1.0), (94.4, 'speech', 1.05, 120), (203.8, 'cave', 0.9, -200), (205.4, 'cave', 1.0),
                (208.2, 'cave', 1.3, -250), (210.6, 'cave', 1.2, -150), (213.4, 'egypt', 0.95), (217.66, 'egypt', 1.0, 100), (218.6, 4000, 0.6),
                (219.9, 4000, 0.6), (220.7, 7275, 0.6), (221.2, 7300, 0.6), (319.52, 'rome', 0.85), (321.1, 'paper', 0.95), (326.0, 'paper', 1.0, 80), (359.86, 'baghdad', 0.85), (362.2, 'press', 0.95),
                (364.1, 'press', 1.1, -40), (379.74, 'press', 0.9, 500), (381.4, 'computer', 1.0), (382.1, 'computer', 1.05, 40), (419.38, 'computer', 0.9, 500),
                (420.8, 'now', 1.0), (423.0, 'now', 1.05), (536.0, 'now', 1.0), (539.9, 'now', 1.1), (651.72, 'now', 0.9), (654.0, 7400, 0.37), (656.84, 7300, 0.36)),
        ev=ev(('egypt', 'hiero', 2.4), ('cave', 'paint', 3.5), ('now', 'video', 4.3), ('speech', 'chain', 89.7), ('cave', 'paint', 205.4), ('cave', 'hands', 208.2),
              ('egypt', 'hiero', 213.0), ('sumer', 'cune', 219.6), ('china', 'bamboo', 220.6), ('rome', 'latin', 221.2), ('paper', 'book', 321.0),
              ('paper', 'pigeon', 324.4), ('press', 'press', 362.2), ('computer', 'type', 381.5), ('now', 'video', 420.8), ('now', 'icons', 421.6),
              ('now', 'world', 651.8)),
        era=[{'at': 87.6, 'st': 'speech'}, {'at': 204.8, 'st': 'cave'}, {'at': 213.0, 'st': 'egypt'}, {'at': 219.6, 'st': 'sumer'}, {'at': 220.6, 'st': 'china'},
             {'at': 221.2, 'st': 'rome'}, {'at': 321.0, 'st': 'paper'}, {'at': 361.9, 'st': 'press'}, {'at': 381.4, 'st': 'computer'}, {'at': 420.8, 'st': 'now'}],
        meters=[{'at': 92.7, 'v': SPEECH}, {'at': 218.3, 'v': STONE}, {'at': 325.0, 'v': PAPER}, {'at': 363.7, 'v': PRINT}, {'at': 381.8, 'v': PC},
                {'at': 537.0, 'v': [0.95, 0.2, 1.0]}, {'at': 538.28, 'v': [1.0, 0.2, 1.0]}, {'at': 539.9, 'v': GFX}],
        words=[wd(2.4, 3.4, 'الفراعنة', size=96), wd(3.5, 4.2, 'إنسان الكهف', size=96), wd(4.3, 5.2, 'النهاردة', size=96),
               wd(5.3, 6.9, 'وعلاقتهم بالجرافيكس؟', size=90), wd(93.4, 94.4, 'لغة', size=110), wd(209.6, 210.8, 'أنا كنت هنا!', size=100),
               wd(212.6, 213.48, 'الكتابة', size=110), wd(320.5, 321.1, 'الورق', size=110), wd(363.6, 364.16, 'طفرة!', size=120),
               wd(381.6, 382.1, 'كمبيوتر', size=110), wd(421.8, 423.0, 'الجرافيكس', size=110), wd(655.8, 656.84, 'الجرافيكس والفيديو', size=90)],
        pics=[pic(205.6, 208.4, 'lascaux', 'cave', 330, 640, 'كهف لاسكو', img=True), pic(208.6, 211.0, 'hands', 'cave', -350, 620, 'كهف الأيادي'),
              pic(217.9, 221.2, 'hiero', 'egypt', 0, 520, 'هيروغليفي', d=200), pic(219.6, 221.2, 'cuneiform', 'sumer', 0, 520, 'سومري', img=True, d=200),
              pic(220.6, 221.2, 'chinese', 'china', 0, 520, 'صيني', d=200), pic(321.0, 326.0, 'paper', 'paper', 330, 600, 'صناعة الورق'),
              pic(362.4, 364.16, 'press', 'press', 330, 560, 'مطبعة جوتنبرج'), pic(381.0, 382.1, 'ibmpc', 'computer', 330, 560, 'IBM PC 1981', img=True),
              pic(421.0, 423.0, 'posters', 'now', 330, 560, 'جرافيك ديزاين'), pic(536.2, 539.9, 'tv', 'now', 330, 560, 'فيديو')],
        bursts=[burst(2.4, 'egypt', 900, c='#F2B531'), burst(3.5, 'cave', 900, c='#F2B531'), burst(4.3, 'now', 900, c='#F2B531'), burst(208.2, 'cave', 900),
                burst(219.6, 'sumer', 900, c='#F2B531'), burst(220.6, 'china', 900, c='#F2B531'), burst(221.2, 'rome', 900, c='#F2B531'),
                burst(363.6, 'press', 850), burst(537.0, 'now', 850), burst(654.0, 'now', 900, c='#F2B531')],
    ),
    # ---------------- 1: the weakest creature won with the mind + communication ----------------
    1: dict(
        cam=cam((25.45, 'weak', 0.9), (32.6, 'weak', 0.95), (39.3, 'weak', 0.95, -40), (41.9, 'weak', 1.25, 30), (45.0, 'weak', 1.15, 60),
                (49.37, 'weak', 0.95, 200), (53.3, 'speech', 0.95), (57.8, 'speech', 0.9, 300), (60.0, 'speech', 0.85, 500), (63.3, 'speech', 1.0),
                (68.6, 'speech', 1.05, 60), (73.8, 'speech', 0.95, 40), (75.5, 300, 0.5), (81.8, 400, 0.52), (83.0, 'speech', 0.9), (86.72, 'speech', 1.05, 60)),
        ev=ev(('weak', 'lion', 30.7), ('weak', 'cheetah', 34.4), ('weak', 'bear', 37.6), ('weak', 'camel', 38.9), ('weak', 'brain', 41.9), ('weak', 'tools', 47.3),
              ('speech', 'gens', 57.8), ('speech', 'chain', 65.7), ('weak', 'team', 74.6), ('speech', 'talk', 84.6), ('village', 'talk', 76.0)),
        era=[{'at': 25.6, 'st': 'weak'}, {'at': 52.8, 'st': 'speech'}],
        words=[wd(27.3, 29.0, 'مخلوق ضعيف', size=104), wd(32.1, 32.8, 'هيخسر!', size=110, color='#FF8A6A'), wd(41.9, 43.0, 'العقل', size=120),
               wd(43.8, 45.6, 'يسخّر البيئة', size=96), wd(52.2, 53.6, 'التواصل', size=110), wd(57.8, 59.9, 'وولاده؟', size=104),
               wd(62.0, 63.2, 'كل المشاكل؟', size=96), wd(68.6, 73.6, 'العلم', y=0.25, size=80), wd(70.5, 73.6, 'الخبرات', y=0.32, size=80),
               wd(71.8, 73.6, 'القصص', y=0.39, size=80), wd(75.1, 77.0, 'التعاون', size=110), wd(80.9, 81.9, 'يسخّروا الدنيا', size=96),
               wd(83.3, 84.5, 'بيحصل إزاي؟', size=104), wd(86.3, 86.72, 'وسائل التواصل', size=96)],
        pics=[],
        bursts=[burst(41.9, 'weak', 1000), burst(75.5, 'weak', 900), burst(86.2, 'speech', 900, c='#F2B531')],
    ),
    # ---------------- 2: the 3 criteria (speed, effort, survival) measured on speech ----------------
    2: dict(
        cam=cam((109.24, 'speech', 0.8), (116.0, 'speech', 0.95), (121.2, 'speech', 0.9, 150), (124.8, 'speech', 0.9, 250), (127.7, 'speech', 1.0),
                (132.9, 'speech', 1.3, -230), (138.5, 'speech', 1.25, -200), (143.6, 'speech', 0.95), (146.6, 'speech', 1.3, 0), (150.2, 'speech', 0.85, 600),
                (154.6, 'speech', 0.9, 450), (157.7, 'speech', 0.95, 250), (160.8, 'speech', 0.95, 300), (172.52, 'speech', 0.95, 500), (174.5, 'village', 0.95),
                (183.36, 'village', 1.05, 60)),
        ev=ev(('speech', 'talk', 110.0), ('speech', 'chain', 121.6), ('speech', 'chain', 130.0), ('speech', 'talk', 138.0), ('speech', 'gens', 150.2),
              ('speech', 'out', 152.2), ('village', 'talk', 172.6), ('village', 'fade', 181.3)),
        era=[{'at': 109.4, 'st': 'speech'}, {'at': 174.0, 'st': 'village'}],
        meters=[{'at': 117.3, 'v': [0.2, 0.0, 0.0]}, {'at': 136.9, 'v': [0.2, 0.1, 0.0]}, {'at': 160.3, 'v': SPEECH}],
        words=[wd(111.3, 112.9, '3 مقاييس', size=110), wd(116.9, 118.4, 'سرعة الانتشار', size=96, color='#7FD8D2'), wd(120.7, 121.6, 'بطيئة', size=110, color='#FF8A6A'),
               wd(128.7, 130.0, 'الجهد', size=110, color='#FFB08A'), wd(136.6, 137.7, 'تقريبًا مفيش', size=96, color='#8EE59B'),
               wd(144.8, 145.9, 'البقاء', size=110, color='#FFD65A'), wd(150.3, 151.3, 'أحفاد أحفادك', size=96),
               wd(153.5, 154.9, 'نسيوا النار!', size=104, color='#FF8A6A'), wd(160.3, 160.9, 'ضعيف', size=110, color='#FF8A6A'),
               wd(175.0, 176.6, 'الناس الأمينة؟', size=96), wd(181.5, 183.36, 'هيختفي', size=110, color='#FF8A6A')],
        pics=[pic(181.4, 183.36, 'rockart', 'village', 330, 600, 'علوم ضاعت')],
        bursts=[burst(116.9, 'speech', 900, c='#7FD8D2'), burst(128.7, 'speech', 900, c='#FFB08A'), burst(144.8, 'speech', 900, c='#FFD65A'), burst(147.3, 'speech', 1150)],
    ),
    # ---------------- 6: a picture is worth a thousand words ----------------
    6: dict(
        cam=cam((446.8, 'now', 0.8, -200), (450.6, 'now', 0.95), (455.6, 'now', 1.0, 60), (459.5, 'now', 0.95), (461.5, 'now', 1.1, 60), (464.5, 'now', 1.0),
                (469.9, 'now', 0.95, -60), (474.2, 'now', 0.9), (480.3, 'now', 0.85, 150), (486.5, 'now', 1.05, 380), (492.9, 'now', 0.95, 200),
                (497.0, 'now', 0.85), (499.7, 'now', 0.9), (504.2, 'now', 1.0), (507.2, 'now', 1.05, -60), (512.22, 'now', 0.95)),
        ev=ev(('now', 'video', 461.5), ('now', 'icons', 452.2), ('now', 'board', 480.6), ('now', 'world', 497.3), ('now', 'hearts', 508.6)),
        era=[{'at': 446.9, 'st': 'now'}],
        meters=[{'at': 449.4, 'v': [0.5, 0.5, 0.5]}, {'at': 455.6, 'v': [1.0, 0.5, 1.0]}, {'at': 478.8, 'v': GFX}],
        words=[wd(450.4, 451.0, 'حاجة رهيبة', size=104), wd(453.5, 454.6, 'أي قالب', size=104), wd(458.5, 460.0, 'سرعة غير طبيعية', size=90),
               wd(462.5, 464.4, 'ويوصلك!', size=104), wd(473.4, 474.1, 'في كل حتة', size=104), wd(478.8, 480.2, 'أقل جهد', size=110, color='#8EE59B'),
               wd(486.5, 488.9, 'صورة واحدة', size=104), wd(491.2, 492.5, 'ولا كلمة!', size=110), wd(497.3, 498.9, 'الصين · أمريكا · مصر', size=84),
               wd(499.7, 502.0, 'الصورة بألف كلمة', size=96), wd(504.7, 507.1, 'المعنى', y=0.25, size=80), wd(505.6, 507.1, 'المعلومة', y=0.32, size=80),
               wd(506.6, 507.1, 'الخبرة', y=0.39, size=80), wd(508.6, 510.9, 'المشاعر ❤', size=110)],
        pics=[pic(461.6, 464.4, 'tv', 'now', 330, 560, 'فيديو'), pic(486.6, 490.5, 'lascaux', 'now', -330, 560, 'صورة من 17,000 سنة', img=True),
              pic(497.4, 499.6, 'unclesam', 'now', -330, 560, 'مفهومة لأي حد', img=True, pos='50% 20%'), pic(510.9, 512.22, 'posters', 'now', 330, 560, 'صور')],
        bursts=[burst(455.6, 'now', 850), burst(499.7, 'now', 850, c='#F2B531'), burst(486.5, 'now', 800, 560)],
    ),
    # ---------------- 8: 82% of the internet is video + teach your kids ----------------
    8: dict(
        cam=cam((626.92, 'now', 0.95), (628.6, 'now', 1.0, -60), (634.7, 'now', 0.95), (639.8, 'now', 0.9, 60), (644.7, 'now', 1.05, -200), (651.4, 'now', 1.0, -100),
                (595.08, 'now', 0.9, 100), (600.0, 'now', 0.95, 200), (603.6, 'now', 0.9, 400), (606.9, 'future', 1.1), (611.0, 'future', 1.15),
                (613.2, 'future', 1.55, -420), (614.8, 'future', 1.55, 0), (616.9, 'future', 1.55, 420), (618.2, 'future', 1.05), (621.7, 'future', 1.2),
                (625.44, 'future', 1.25, 60)),
        ev=ev(('now', 'pct', 627.0, 639.6), ('now', 'video', 633.9), ('now', 'icons', 639.8), ('now', 'emoji', 648.8), ('now', 'video', 597.9),
              ('future', 'ps', 613.2), ('future', 'edit', 614.8), ('future', 'motion', 616.9), ('future', 'job', 621.7)),
        era=[{'at': 627.0, 'st': 'now'}, {'at': 606.5, 'st': 'future'}],
        words=[wd(633.9, 634.7, 'فيديوهات!', size=110), wd(639.3, 641.9, 'أيقونات وصور وجرافيك', size=84), wd(643.0, 644.6, 'أسهل وسيلة', size=104),
               wd(648.8, 651.4, 'وش بيضحك 😄', size=96), wd(598.0, 599.9, 'فيديو · فوتوشوب', size=96), wd(602.9, 603.6, 'غيرك هيسبقك!', size=104, color='#FF8A6A'),
               wd(606.4, 607.6, 'علّمها لولادك', size=104), wd(609.4, 610.9, 'استيعابهم عالي', size=96), wd(613.2, 614.6, 'فوتوشوب', size=110),
               wd(614.8, 616.4, 'مونتاج', size=110), wd(616.9, 618.0, 'موشن جرافيك', size=104), wd(623.4, 625.44, 'شغلانة', size=110)],
        pics=[pic(640.4, 643.0, 'posters', 'now', 330, 560, 'جرافيك ديزاين')],
        bursts=[burst(627.0, 'now', 600, -60, c='#F2B531'), burst(606.9, 'future', 850), burst(621.7, 'future', 650, c='#F2B531')],
    ),
}

# ---------------- sound design ----------------
L = 'sfx/'
EV_SND = {'paint': ('swish', 0.35), 'hands': ('stamp', 0.4), 'cune': ('click', 0.4), 'hiero': ('magic', 0.3), 'carve': ('click', 0.45), 'burn': ('crackle', 0.45),
          'ink': ('pour', 0.35), 'press': ('door_slam', 0.4), 'copies': ('paper', 0.5), 'pigeon': ('swoop_up', 0.4), 'ship': ('wind', 0.3), 'type': ('typing', 0.45),
          'video': ('ding', 0.4), 'icons': ('pop_2', 0.4), 'world': ('strings', 0.35), 'q': ('tick', 0.45), 'ramp1': ('swish', 0.4), 'ramp2': ('swish', 0.4),
          'x1': ('buzz_wrong', 0.4), 'x2': ('buzz_wrong', 0.4), 'crane': ('riser', 0.35), 'fade': ('wind', 0.4), 'chain': ('pop_1', 0.35), 'talk': ('pop_3', 0.25),
          'bamboo': ('rustle', 0.4), 'latin': ('click', 0.4), 'book': ('paper', 0.45), 'sheets': ('rustle', 0.45), 'lib': ('pop_1', 0.3),
          'lion': ('impact', 0.35), 'cheetah': ('whoosh_3', 0.45), 'bear': ('wind', 0.35), 'camel': ('swoop_down', 0.3), 'brain': ('magic', 0.45), 'tools': ('click', 0.45),
          'team': ('strings', 0.35), 'gens': ('swish', 0.35), 'out': ('wind', 0.45), 'board': ('swoop_up', 0.35), 'hearts': ('ding', 0.35), 'pct': ('riser', 0.4),
          'emoji': ('pop_2', 0.45), 'ps': ('ding', 0.4), 'edit': ('ding', 0.4), 'motion': ('ding', 0.4), 'job': ('cash', 0.45)}


def build_sfx(mp, aly, main):
    sfx = [{'file': L + 'impact.wav', 'at': 0.05, 'vol': 0.4}]
    for e in mp['ev']:
        if e['k'] in EV_SND and e['at'] < main - 0.3:
            s = EV_SND[e['k']]
            sfx.append({'file': L + s[0] + '.wav', 'at': e['at'], 'vol': s[1], 'dur': 2.5})
            if e['k'] == 'press':  # every press cycle (1.8 s) thumps
                for k in range(1, 6):
                    if e['at'] + k * 1.82 < main - 0.3:
                        sfx.append({'file': L + 'stamp.wav', 'at': round(e['at'] + k * 1.82 + 0.4, 3), 'vol': 0.3})
    for x in mp.get('era', []):
        sfx.append({'file': L + 'whoosh_1.wav', 'at': max(0, x['at'] - 0.15), 'vol': 0.3})
    for i, w in enumerate(mp.get('words', [])):
        sfx.append({'file': L + f'pop_{i % 3 + 1}.wav', 'at': w['at'], 'vol': 0.35})
    for p in mp.get('pics', []):
        sfx.append({'file': L + 'swoop_up.wav', 'at': p['at'], 'vol': 0.25})
    for b in mp.get('bursts', []):
        sfx.append({'file': L + 'magic.wav', 'at': b['at'], 'vol': 0.3})
    for m in mp.get('meters', []):
        sfx.append({'file': L + 'tick.wav', 'at': m['at'], 'vol': 0.35})
    cams = mp['cam']
    for a, b in zip(cams, cams[1:]):  # fast travel / big zoom = whoosh
        if b['t'] - a['t'] < 3 and (abs(b['x'] - a['x']) > 1500 or abs(b['z'] / a['z'] - 1) > 0.8):
            sfx.append({'file': L + 'whoosh_2.wav', 'at': a['t'], 'vol': 0.4})
    sfx += [{'file': L + 'whoosh_2.wav', 'at': a['at'], 'vol': 0.3} for a in aly if a['at'] > 0.5 and a.get('ain', True)]
    c0 = main + 2.9
    sfx += [{'file': L + 'whoosh_1.wav', 'at': round(main - 0.1, 3), 'vol': 0.45}, {'file': L + 'typing.wav', 'at': round(c0 + 34 / 30, 3), 'vol': 0.45, 'dur': 0.9},
            {'file': L + 'pop_2.wav', 'at': round(c0 + 62 / 30, 3), 'vol': 0.55}, {'file': L + 'ding.wav', 'at': round(c0 + 84 / 30, 3), 'vol': 0.5}]
    sfx.sort(key=lambda s: s['at'])
    out = []  # never stack more than 3 sounds inside 0.15 s
    for s in sfx:
        if sum(1 for o in out if abs(o['at'] - s['at']) < 0.15) < 3:
            out.append(s)
    return out


def cam_clip(a, b):
    """round webcam = plain crop around his face (no roto), one clip per kept range -> (file, src start)"""
    a0, d = a - 0.6, b - a + 1.2
    name = f'cam_{a0:.2f}.mp4'
    if not (PUB / name).exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a0:.2f}', '-i', str(SRC), '-t', f'{d:.2f}', '-vf', 'crop=600:600:610:100,scale=480:480',
                        '-c:v', 'libx264', '-crf', '18', '-an', str(PUB / name)], check=True)
    return PJ + name, a0


KEEP = set()


def span(t0, t1):
    i = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t0))
    j = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t1) if _words[k]['start'] <= t1 + 0.05 else 1e9)
    j = max(j, i)
    prev = _words[i - 1]['end'] if i > 0 else None
    nxt = _words[j + 1]['start'] if j + 1 < len(_words) else None
    a, b, rep = fit(_words[i]['start'], _words[j]['end'], prev, nxt)
    KEEP.update(id(w) for w in _words[i:j + 1])
    print('   ', _words[i]['w'], '…', _words[j]['w'], rep)
    return [a, b]


def build(n):
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
                return round(s['tl'] + max(0.0, min(t - s['src'], s['len'])), 3)
        best = min([(abs(t - s['src']), s['tl']) for s in segs] + [(abs(t - s['src'] - s['len']), s['tl'] + s['len']) for s in segs])
        if best[0] > 2.5:
            print(f'  !! short {n}: {t} is {best[0]:.1f}s outside the ranges')
        return round(best[1], 3)

    words = []
    for w in _words:
        if id(w) not in KEEP:
            continue
        x = WFIX_AT.get(round(w['start'], 2), WFIX.get(w['w'], w['w']))
        if not x:
            continue
        ra = next((r for r in ranges if r[0] - 0.05 <= w['start'] < r[1]), None)
        if ra is None:
            continue
        words.append({'w': x, 'start': to_tl(max(w['start'], ra[0])), 'end': to_tl(max(ra[0], min(w['end'], ra[1])))})
    for i in range(len(words) - 1, 0, -1):  # '82' + '%' -> one caption word
        if words[i]['w'] in ('%', '٪'):
            words[i - 1]['w'] += '%'; words[i - 1]['end'] = words[i]['end']; del words[i]
    ct = json.load(open(W / 'cta' / 'transcript.json', encoding='utf8'))
    for i, w in enumerate([w for s_ in ct['sentences'] for w in s_['words']]):
        x = CTA_FIX.get(w['w'], w['w'])
        if i > 7 and w['w'] == 'اليوتيوب':
            x = 'يوتيوب'
        if x and w['start'] < CTA_KEEP[1]:
            words.append({'w': x, 'start': round(main + w['start'], 3), 'end': round(main + min(w['end'], CTA_KEEP[1]), 3)})

    mp = json.loads(json.dumps(PLAN[n]))
    for key in ('cam', 'ev', 'era', 'meters', 'words', 'pics', 'bursts'):
        for e in mp.get(key, []):
            for tk in (('t',) if key == 'cam' else ('at', 'out')):
                if tk in e:
                    e[tk] = to_tl(e[tk])
        if key == 'cam':
            for a_, b_ in zip(mp[key], mp[key][1:]):  # equal times after mapping -> keep order, nudge
                if b_['t'] <= a_['t']:
                    b_['t'] = round(a_['t'] + 0.05, 3)
        elif key in mp:
            mp[key].sort(key=lambda e: e['at'])
    scenes = [{'t': 'hworld', 'at': 0, 'dur': round(main, 3), 'layer': 'back', 'props': mp}]

    # his face (Aly: "المقدمة بس اللي دايرة كبيرة"): BIG round webcam in the opening that shrinks into the small bottom-left circle,
    # then the small circle to the very end (one clip per kept range, windows touch -> no pop)
    aly = []
    big_end = to_tl(BIG[n][1])
    for sg in segs:
        f_, a0 = cam_clip(sg['src'], sg['src'] + sg['len'])
        e_tl = sg['tl'] + sg['len']
        if sg['tl'] < big_end:
            aly.append({'file': f_, 'at': sg['tl'], 'dur': round(min(e_tl, big_end) - sg['tl'], 3), 'from': round(sg['src'] - a0, 3), 'mode': 'bubble-big', 'face': [0.5, 0.4, 0.3]})
        a_tl = max(sg['tl'], big_end)
        if e_tl - a_tl < 0.1:
            continue
        aly.append({'file': f_, 'at': round(a_tl, 3), 'dur': round(e_tl - a_tl, 3), 'from': round(sg['src'] + (a_tl - sg['tl']) - a0, 3), 'mode': 'bubble-s',
                    'face': [0.5, 0.4, 0.3]})
    ws = sorted(aly, key=lambda x: x['at'])
    for x, y in zip(ws, ws[1:]):
        if abs(y['at'] - (x['at'] + x['dur'])) < 0.08 and y['mode'] == 'bubble-s':
            x['aout'] = False; y['ain'] = False

    sfx = build_sfx(mp, aly, main)
    sfx = [s for s in sfx if s['at'] < main + CTA_KEEP[1]]
    vlog, vI = build_voice(segs, (PJ + 'cta.mp4', CTA_KEEP[0], CTA_KEEP[1] - CTA_KEEP[0]), PUB / f'voice_{n}.wav')
    print('  voice gains dB per piece:', vlog, f'(before final gain {vI:.1f} LUFS)')
    dur = round(main + CTA_KEEP[1] - CTA_KEEP[0], 3)
    mu = MUSIC[n]
    props = {'fps': 30, 'duration': dur, 'voice': PJ + f'voice_{n}.wav', 'segs': [{'src': 0, 'tl': 0, 'len': dur}], 'words': words,
             'aly': aly, 'scenes': scenes, 'sfx': sfx, 'tint': '#B4512F', 'look': 'hist', 'capBottom': 0.175,
             'music': {'file': PJ + f'music/{mu[0]}.mp3', 'from': mu[1], 'vol': mu[2]},
             'ctaVol': 0.0, 'sfxGain': 1.0, 'cta': {'file': PJ + 'cta.mp4', 'tl': round(main, 3), 'len': round(CTA_KEEP[1] - CTA_KEEP[0], 3), 'src': CTA_KEEP[0]},
             'ctaCue': {'at': 2.9, 'dur': round(CTA_KEEP[1] - 2.9, 3), 'props': {
                 'title': 'اكتب في *كومنت*', 'keyword': 'يوتيوب', 'dm': 'ده لينك الفيديو كامل 🎨', 'typeAt': 34, 'sendAt': 62, 'dmAt': 84, 'top': 0.02}}}
    json.dump(props, open(PUB / f'short_{n}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'short {n}: {main:.1f}s + CTA {CTA_KEEP[1] - CTA_KEEP[0]:.1f}s | {len(aly)} Aly, {len(words)} words, {len(sfx)} sfx')


for n in [int(x) for x in sys.argv[1:]] or sorted(SPANS):
    build(n)

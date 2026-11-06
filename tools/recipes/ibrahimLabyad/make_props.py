"""Props for composition 'scene-analysis' (Ibrahim El Abyad, scene 55/56). Writes work/props.json.
All times = seconds from the start of the OBS recording (film TC ~ 1:16:00 + t).
Shots: work/shots_v4.json (98 shots, frame-exact cuts). Lines: Whisper word times, checked on the audio level.
PDF rects in points (page 595 x 842), page images rendered at 3 px/pt."""
import json
from pathlib import Path
W = Path(__file__).resolve().parents[1]
FPS = 30
cuts = json.load(open(W / 'shots_v4.json'))

# n: (place, size, movement, extra)   place codes -> scene
S = {
 1: ('PRE', 'ELS', 'Slow Push-in', ''), 2: ('PRE', 'MLS', 'Slow Push-in', ''),
 3: ('TI', 'CU → MCU', 'Camera Move (Reveal)', ''), 4: ('TF', 'LS', 'Truck Right (Reveal)', 'OTS · Dirty Frame'),
 5: ('TI', 'MCU', 'Handheld · Pan Left', ''), 6: ('TF', 'MS', 'Static', ''), 7: ('TI', 'MS', 'Pull-out + Tilt Up', ''),
 8: ('TW', 'WS', 'Truck Right', 'Dirty Frame'), 9: ('TI', 'CU', 'Handheld', ''), 10: ('TF', 'MS', 'Static', ''),
 11: ('TI', 'CU → Insert', 'Pan Right', ''), 12: ('TI', 'MS', 'Pan Right (Follow)', ''),
 13: ('TF', 'MS → MCU', 'Static (actor leans in)', ''), 14: ('TI', 'MS', 'Pull-out + Tilt Up', ''),
 15: ('TF', 'OTS → MS', 'Arc Shot', 'Dirty Frame'), 16: ('TI', 'CU', 'Pan Right → Darkness', ''),
 17: ('A', 'LS → MLS', 'Push-in (through laundry)', ''), 18: ('A', 'Insert → MCU', 'Tilt Up + Pan Right', ''),
 19: ('TI', 'CU', 'Handheld', ''), 20: ('A', 'LS', 'Handheld', ''), 21: ('TF', 'MS', 'Static', ''),
 22: ('A', 'LS', 'Handheld · Pan Right', ''), 23: ('P', 'MS', 'Handheld (Whip)', ''), 24: ('TF', 'MS', 'Static', ''),
 25: ('A', 'MLS', 'Handheld · Push-in', ''), 26: ('TI', 'CU', 'Handheld', ''), 27: ('P', 'MS', 'Handheld · Pan Right', ''),
 28: ('A', 'MS', 'Handheld', ''), 29: ('TF', 'MS', 'Static', ''), 30: ('TI', 'CU', 'Handheld · Pull-out', ''),
 31: ('TW', 'WS', 'Slow Push-in', 'Dirty Frame'), 32: ('TI', 'CU', 'Handheld', ''), 33: ('A', 'LS', 'Static', 'Frame within a Frame'),
 34: ('TW', 'WS', 'Static', ''), 35: ('A', 'LS', 'Static', ''), 36: ('TF', 'MS', 'Static', ''), 37: ('TI', 'CU', 'Handheld', ''),
 38: ('A', 'LS', 'Static', ''), 39: ('P', 'MS', 'Handheld (Whip)', ''), 40: ('TF', 'MCU', 'Static', ''),
 41: ('A', 'Insert', 'Handheld', ''), 42: ('TI', 'CU', 'Static', ''), 43: ('TF', 'MS', 'Static', ''), 44: ('A', 'MS', 'Handheld', ''),
 45: ('P', 'MS', 'Handheld', ''), 46: ('A', 'MCU', 'Handheld', ''), 47: ('A', 'MLS', 'Handheld', ''), 48: ('P', 'MCU', 'Static', ''),
 49: ('A', 'MS', 'Handheld', ''), 50: ('A', 'MS', 'Handheld', ''), 51: ('TF', 'MS', 'Static', ''), 52: ('P', 'CU', 'Slow Push-in', ''),
 53: ('TF', 'MCU', 'Static', ''), 54: ('A', 'MS', 'Handheld', ''), 55: ('A', 'MS', 'Handheld', ''),
 56: ('N', 'MS', 'Static', 'Frame within a Frame'), 57: ('A', 'MS', 'Handheld', ''), 58: ('P', 'MS', 'Handheld', ''),
 59: ('A', 'MCU', 'Handheld', ''), 60: ('N', 'MS', 'Tilt Up (Follow)', ''), 61: ('P', 'MCU', 'Handheld', ''),
 62: ('N', 'MCU', 'Static', ''), 63: ('P', 'MCU', 'Handheld', ''), 64: ('TW', 'WS', 'Static', 'Dirty Frame'),
 65: ('K', 'LS', 'Slow Push-in', ''), 66: ('K', 'CU', 'Handheld', ''), 67: ('P', 'MCU', 'Handheld', ''), 68: ('P', 'MCU', 'Handheld', ''),
 69: ('P', 'MCU', 'Whip Tilt', ''), 70: ('A', 'MCU', 'Handheld', ''), 71: ('P', 'MCU', 'Handheld', 'Flash Cut 0.2 s'),
 72: ('P', 'MCU', 'Whip Tilt', ''), 73: ('TF', 'MS', 'Static', ''), 74: ('P', 'MCU', 'Handheld', ''),
 75: ('K', 'MCU', 'Handheld · Tilt Down', ''), 76: ('TW', 'WS', 'Static', ''), 77: ('TI', 'CU', 'Static', ''),
 78: ('K', 'LS', 'Static', 'Low Angle'), 79: ('K', 'Insert', 'Handheld', ''), 80: ('K', 'MLS', 'Static', 'Low Angle'),
 81: ('K', 'Insert', 'Handheld', ''), 82: ('TF', 'MS', 'Static', ''), 83: ('TI', 'CU', 'Handheld · Pull-out', ''),
 84: ('K', 'Insert', 'Whip Pan', ''), 85: ('TI', 'CU', 'Handheld', ''), 86: ('K', 'MLS', 'Static', 'Low Angle'),
 87: ('TI', 'CU', 'Handheld', ''), 88: ('TI', 'CU', 'Handheld', ''), 89: ('K', 'Insert', 'Handheld', ''),
 90: ('TT', 'Insert', 'Static', ''), 91: ('TT', 'MS → MCU', 'Tilt Up + Push-in', ''), 92: ('TF', 'MCU', 'Static', ''),
 93: ('R', 'ELS', 'Crane Up + Pan Right', ''), 94: ('M', 'MS', 'Slow Push-in', 'Top Shot'), 95: ('M', 'MS', 'Static', 'Top Shot'),
 96: ('M', 'MS', 'Static', 'Top Shot'), 97: ('M', 'MS', 'Static', 'Top Shot'), 98: ('MB', 'MS', 'Tracking (Leading)', ''),
}
SCENE = {'PRE': 'x', 'TI': '55', 'TF': '55', 'TW': '55', 'TT': '55', 'A': '56', 'P': '56', 'N': '56', 'R': '56', 'M': '56', 'MB': '56', 'K': 'add'}
WHO = {'PRE': 'Ibrahim · rooftop', 'TI': 'Ibrahim', 'TF': 'Fares', 'TW': 'Table (wide)', 'TT': 'Tongue', 'A': 'Alley attack',
       'P': 'Drink & pills', 'N': 'Narges', 'R': 'Rooftop', 'M': 'Money hole', 'MB': 'Ashry', 'K': 'Tongue (street)'}
shots = []
for c in cuts:
    pl, size, mv, ex = S[c['n']]
    shots.append({'n': c['n'], 's': c['s'], 'e': c['e'], 'place': pl, 'scene': SCENE[pl], 'size': size, 'move': mv, 'extra': ex, 'who': WHO[pl]})

# ---------- SOUND window: what is heard -> its line in the script ----------
# r = [page, x0, y0, x1, y1] (pt). diff = how the film differs (Arabic). spk = speaker.
D = [210, 395]   # dialogue column x range (pt)
V = [300, 545]   # V.O. column on p.99-100
L = []
def ln(t0, t1, spk, page, y0, y1, diff='', col=D, scene='55', echo=False):
    L.append({'t0': t0, 't1': t1, 'spk': spk, 'r': [page, col[0], y0, col[1], y1], 'diff': diff, 'scene': scene, 'echo': echo})
ln(7.40, 10.80, 'FARES', 97, 304, 353)
ln(10.80, 16.86, 'FARES', 97, 328, 402)
ln(16.86, 21.72, 'FARES', 97, 377, 426, 'في الفيلم من غير «يا سيد ابراهيم»')
ln(22.56, 25.30, 'FARES', 97, 426, 476, 'في الفيلم: «الراجل» بدل «الزول»')
ln(25.45, 26.55, 'IBRAHIM', 97, 494, 541)
ln(27.40, 29.42, 'FARES', 97, 584, 631)
ln(29.42, 32.32, 'IBRAHIM', 97, 678, 725, 'في الفيلم: «ماليش سيد» مرتين ورا بعض')
ln(32.32, 35.56, 'FARES', 98, 58, 129)
ln(35.56, 39.42, 'FARES', 98, 104, 129, 'في الفيلم: «ضغط عليك أكتر»')
ln(39.42, 44.68, 'FARES', 98, 104, 154, 'في الفيلم: «أهم حاجة يكون السر بيناتنا»')
ln(46.00, 47.20, 'FARES', 98, 340, 387, 'في الفيلم: «ليا شرطين» بس — جملة «اللي يجلجني…دوغري» اتشالت')
ln(48.00, 50.72, 'FARES', 98, 363, 410)
ln(50.72, 57.58, 'FARES', 98, 386, 433, '«فول إستوب… تخصك لوحدك» اتشالت من الفيلم')
ln(59.40, 61.00, 'FARES', 98, 478, 502)
ln(61.00, 68.44, 'FARES', 98, 547, 571)
ln(69.00, 74.36, 'FARES', 98, 547, 594)
ln(75.90, 81.80, 'FARES', 98, 593, 663)
ln(83.70, 86.42, 'FARES', 98, 639, 663)
ln(87.88, 90.62, 'FARES', 98, 662, 686)
ln(91.98, 94.38, 'FARES', 98, 616, 663, 'نفس الجملة بتتكرر', echo=True)
ln(96.30, 105.38, 'FARES', 98, 639, 686, 'نفس الجملة بتتكرر', echo=True)
ln(105.38, 108.38, 'FARES', 98, 662, 709)
ln(110.30, 111.90, 'FARES', 98, 685, 709)
ln(118.06, 121.40, 'FARES', 98, 685, 732)
ln(122.00, 128.80, 'FARES', 98, 708, 755)
ln(129.87, 131.10, 'FARES', 98, 708, 732, '«دحلاب وسخ» بتتكرر', echo=True)
ln(132.00, 134.08, 'FARES', 98, 731, 778)
ln(134.08, 138.16, 'FARES', 98, 754, 778)
ln(138.16, 143.64, 'FARES', 99, 35, 82)
ln(143.64, 145.86, 'FARES', 99, 58, 82)
ln(147.30, 159.22, 'FARES', 99, 58, 82, '«ويورث هو الملك» بتتكرر', echo=True)
ln(167.72, 174.06, 'FARES', 99, 58, 105)
ln(178.00, 181.50, 'FARES', 99, 81, 128, 'في الفيلم: «تفتكر يعمل إيه» بدل «فكرك»')
ln(198.56, 207.84, 'ASHRY V.O.', 0, 0, 0, 'مش مكتوبة في السيناريو: «وعملها صاحبنا… خرج من عند عزرائيل ودخل عند ملك الموت»', scene='56')
ln(207.84, 213.90, 'ASHRY V.O.', 100, 40, 108, '«عمره ما بيشرب حشيش…» اتشالت', col=V, scene='56')
ln(213.90, 218.30, 'ASHRY V.O.', 100, 249, 297, '«وناس من الدرب الأحمر…» اتشالت', col=V, scene='56')
ln(218.30, 219.76, 'ASHRY V.O.', 100, 342, 388, col=V, scene='56')
ln(219.76, 223.94, 'ASHRY V.O.', 100, 510, 559, col=V, scene='56')
ln(234.58, 240.44, 'ASHRY V.O.', 99, 510, 578, 'في السيناريو دي أول جملة في المونتاج — الفيلم أخّرها للآخر', col=V, scene='56')

# ---------- PICTURE window: what we see -> its line in the script ----------
A_ = [40, 285]
PIC = {
 'PRE': None,
 'TI': {'r': [97, 35, 90, 556, 186], 'scene': '55'},
 'TF': {'r': [97, 35, 209, 556, 258], 'scene': '55'},
 'TW': {'r': [97, 35, 209, 556, 258], 'scene': '55'},
 'A': {'r': [100, 40, 319, 285, 367], 'scene': '56'},
 'P': {'r': [100, 40, 582, 285, 631], 'scene': '56'},
 'N': {'r': [99, 40, 611, 285, 659], 'scene': '56'},
 'K': {'r': [99, 300, 241, 556, 266], 'scene': 'add'},
 'TT': {'r': [99, 300, 217, 556, 266], 'scene': '55'},
 'R': {'r': [99, 40, 659, 285, 731], 'scene': '56'},
 'M': {'r': [100, 40, 462, 285, 511], 'scene': '56'},
 'MB': {'r': [101, 40, 376, 285, 424], 'scene': '56'},
}
pics = []
for s in shots:
    p = PIC[s['place']]
    pics.append({'t0': s['s'], 't1': s['e'], 'place': s['place'], 'r': p['r'] if p else None, 'scene': p['scene'] if p else 'x'})

# ---------- cards (3 kinds only: edit / sound / camera) ----------
C = []
def card(t0, t1, kind, term, ar, anim, **k):
    C.append({'t0': t0, 't1': t1, 'kind': kind, 'term': term, 'ar': ar, 'anim': anim, **k})
card(7.6, 15.2, 'edit', 'J-Cut', 'صوت المشهد الجاي بيبدأ قبل صورته — الصوت سبق الصورة بـ 3.7 ثانية', 'jcut', lead=3.67)
card(17.6, 24.2, 'camera', 'Dirty Frame', 'حاجة في المقدمة (Foreground) بتغطي جزء من الكادر وبتخلينا نبص من ورا', 'dirty')
card(24.8, 32.0, 'edit', 'Shot / Reverse Shot', 'القطع بين الاتنين: فارس ↔ إبراهيم، كل واحد في كادره', 'srs')
card(39.5, 46.0, 'edit', 'Reaction Shot', 'فارس هو اللي بيتكلم، بس المونتير ساب الصورة على إبراهيم وهو بيسمع', 'react')
card(50.8, 57.6, 'camera', 'Insert Shot', 'لقطة قريبة لحاجة مهمة: الكاميرا بتعمل Pan من وش إبراهيم للإزازة', 'insert')
card(59.2, 66.4, 'camera', 'Static Shot · Blocking', 'الكاميرا ثابتة — فارس هو اللي بيقرّب (السيناريو: «يقترب وجهه»)', 'static')
card(75.4, 80.6, 'camera', 'Arc Shot', 'الكاميرا بتلف حوالين فارس: المقدمة والخلفية بيتحركوا عكس بعض', 'arc')
card(80.6, 88.0, 'sound', 'Sound Bridge', 'الموسيقى الجديدة بدأت عند 1:20 — الصورة اتقطعت للحارة بعد 12.6 ثانية', 'bridge', lead=12.6)
card(88.2, 95.4, 'edit', 'Hidden Cut', 'الكاميرا بتعمل Pan للضلمة… والقطع للحارة استخبى جوه الضلمة', 'hidden')
card(95.6, 103.4, 'edit', 'Cross-Cutting', 'الصوت من مشهد 55 (فارس)، والصورة من مشهد 56 (الحارة) — مشهدين في وقت واحد', 'cross')
card(104.0, 110.6, 'sound', 'Dialogue Echo', 'جمل فارس بتتكرر وبتتشوّه — زي ما هي بترن في دماغ إبراهيم', 'echo')
card(120.0, 128.0, 'edit', 'Pacing · ASL (Average Shot Length)', 'متوسط طول الشوت: في الحوار ~5.8 ثانية ← في الذروة ~1.3 ثانية', 'asl')
card(165.2, 172.0, 'edit', 'Jump Cut', 'نفس المكان ونفس الكادر تقريبا، بس فيه قفزة في الوقت', 'jump')
card(188.6, 194.6, 'sound', 'Fade to Silence', 'الصوت كله بيختفي من 3:11 لحد الصمت مع القطع على إبراهيم', 'fade')
card(194.8, 200.6, 'sound', 'SFX (Sound Effect) · Water Drips', 'في الصمت: صوت نقط مية بتنقط — زي الدم', 'drips')
card(203.9, 211.0, 'edit', 'Montage + V.O. (Voice-Over)', 'صور سريعة من أيام كتير، وتحتها صوت عشري بيحكي — مشهد 56', 'montage')
card(211.2, 218.8, 'camera', 'Crane Shot', 'الكاميرا بتطلع لفوق (Crane Up) وبتلف يمين على السطوح (من شكل الصورة)', 'crane')
card(219.8, 225.6, 'camera', 'Top Shot', 'الكاميرا فوق دماغهم بالظبط وباصة لتحت على الحفرة', 'top')
card(225.8, 230.8, 'edit', 'Jump Cuts (Time Passing)', 'نفس الـ Top Shot بس الفلوس بتزيد — 3 قطعات = الوقت بيعدي', 'jump2')
card(231.2, 238.6, 'camera', 'Tracking Shot', 'الكاميرا ماشية قدام عشري وهو سايق الموتوسيكل', 'track')

# small notes (Lighting / Acting only = one line)
NOTES = [
 (27.0, 30.8, 'LIGHTING', 'Low-key — نص وش فارس في الضل'),
 (45.6, 50.4, 'ACTING', 'إيد فارس بتعد الشروط'),
 (108.2, 112.4, 'LIGHTING', 'Practical Light — النار هي مصدر النور'),
 (195.0, 200.6, 'ACTING', 'إبراهيم ساكت وباصص — الصمت هو الأداء'),
]
notes = [{'t0': a, 't1': b, 'k': k, 'txt': t} for a, b, k, t in NOTES]

# marks drawn ON the film (x0,y0,x1,y1 in 0..1 of the video)
marks = [
 {'t0': 18.2, 't1': 23.8, 'term': 'DIRTY FRAME', 'box': [0.06, 0.04, 0.66, 0.80], 'icon': 'dirty'},
 {'t0': 27.0, 't1': 30.6, 'term': 'NEGATIVE SPACE', 'box': [0.42, 0.06, 0.97, 0.80], 'icon': 'neg'},
 {'t0': 53.3, 't1': 55.1, 'term': 'INSERT SHOT', 'box': None, 'icon': 'insert'},
 {'t0': 75.6, 't1': 80.4, 'term': 'ARC SHOT', 'box': None, 'icon': 'arc', 'arrow': 'arc'},
 {'t0': 100.2, 't1': 103.8, 'term': 'TILT UP + PAN RIGHT', 'box': None, 'icon': 'tilt', 'arrow': 'upright'},
 {'t0': 125.6, 't1': 126.3, 'term': 'FRAME WITHIN A FRAME', 'box': [0.25, 0.08, 0.76, 0.80], 'icon': 'fwf'},
 {'t0': 190.9, 't1': 193.1, 'term': 'INSERT SHOT', 'box': None, 'icon': 'insert'},
 {'t0': 219.8, 't1': 222.6, 'term': 'TOP SHOT', 'box': None, 'icon': 'top'},
]

# timeline markers (name at a time; span = lead-in bracket)
markers = [
 {'t': 7.40, 'name': 'J-Cut', 'kind': 'edit', 'span': [7.40, 11.067]},
 {'t': 24.60, 'name': 'Shot / Reverse Shot', 'kind': 'edit'},
 {'t': 39.40, 'name': 'Reaction Shot', 'kind': 'edit'},
 {'t': 80.00, 'name': 'Sound Bridge', 'kind': 'sound', 'span': [80.0, 92.6]},
 {'t': 88.07, 'name': 'Pan → Darkness', 'kind': 'camera'},
 {'t': 92.60, 'name': 'Hidden Cut → Cross-Cutting', 'kind': 'edit', 'region': [92.6, 190.767]},
 {'t': 96.30, 'name': 'Echo', 'kind': 'sound'},
 {'t': 159.80, 'name': 'Film Addition', 'kind': 'edit'},
 {'t': 165.033, 'name': 'Jump Cut', 'kind': 'edit'},
 {'t': 191.00, 'name': 'Fade to Silence', 'kind': 'sound', 'span': [191.0, 193.233]},
 {'t': 193.233, 'name': 'SFX: Water Drips', 'kind': 'sound'},
 {'t': 203.733, 'name': 'Montage', 'kind': 'edit'},
 {'t': 223.80, 'name': 'Jump Cuts', 'kind': 'edit'},
]

# audio clips (A1 dialogue by speaker, A2 music/drone, A3 sfx)
a1 = []
for l in L:
    if a1 and a1[-1]['name'] == l['spk'] and l['t0'] - a1[-1]['e'] < 1.6 and a1[-1]['echo'] == l['echo']:
        a1[-1]['e'] = l['t1']
    else:
        a1.append({'s': l['t0'], 'e': l['t1'], 'name': l['spk'], 'echo': l['echo']})
a2 = [{'s': 0, 'e': 80.0, 'name': 'DRONE'}, {'s': 80.0, 'e': 193.233, 'name': 'MUSIC (new cue)', 'fadeOut': 191.0},
      {'s': 203.733, 'e': 242.03, 'name': 'MUSIC (montage)'}]
a3 = [{'s': 193.233, 'e': 198.5, 'name': 'SFX: WATER DRIPS'}]

props = {'duration': round(len(open(W / 'shots_v4.json').read()) * 0 + cuts[-1]['e'], 3), 'tc0': 76 * 60,
         'shots': shots, 'lines': L, 'pics': pics, 'cards': C, 'notes': notes, 'marks': marks, 'markers': markers,
         'a1': a1, 'a2': a2, 'a3': a3}
json.dump(props, open(W / 'props.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('shots', len(shots), 'lines', len(L), 'cards', len(C), 'dur', props['duration'])

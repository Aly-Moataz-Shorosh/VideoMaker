"""4 vertical shorts (look 'cairo') from Aly's video "خريطة القاهرة" (Vd0NUtDsUfk, 2026-10-09; my list: 1 summary, 3 Port Said street
was a canal, 2 Zamalek didn't exist, 9 the seat of power moved 7 times).
Aly: the map must be EXACTLY his drawing (his KMZ -> src/cairo/data.json), creative motion, his face sometimes shown, sometimes not.
The whole short = ONE map scene ('cmap', back layer) whose camera / layers / labels are timed on his words; overlays on top.
Inputs : work/transcript.json, work/cams.json (make_cams.py), work/cta/transcript.json, public/projects/<code>/{cta.mp4, aly_hook.webm}
Output : motion-library/public/projects/<code>/short_<n>.json  (composition 'film-short')
Run    : python work/scripts/make_shorts.py [n ...]   then  sh work/scripts/check.sh <n>  /  sh work/scripts/render.sh <n...>
All times below are SOURCE seconds (his video); they are mapped to the short's timeline."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

W = Path(__file__).resolve().parents[1]; P = W.parent; ROOT = P.parents[1]
sys.stdout.reconfigure(encoding='utf-8')
CODE = P.name
PJ = f'projects/{CODE}/'
PUB = ROOT / 'motion-library' / 'public' / 'projects' / CODE
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
CAMS = json.load(open(W / 'cams.json', encoding='utf8'))
from edges import fit
from level_voice import build as build_voice
_words = [w for s in tr['sentences'] for w in s['words']]

# caption spelling (Whisper heard Egyptian names wrong)
WFIX = {'عبر': 'عمرو', 'العصد': 'العاص', 'العص': 'العاص', 'الكاهرة': 'القاهرة', 'الفستات': 'الفسطاط', 'للفستات': 'للفسطاط', 'السكلي': 'الصقلي',
        'المانيا': 'المنيل', 'المانيال': 'المنيل', 'زيسوستريس': 'سيزوستريس', 'الفرانية': 'الفرعونية', 'الزقزيق': 'الزقازيق', 'البحارات': 'البحيرات',
        'برسعيد': 'بورسعيد', 'بروسعيد': 'بورسعيد', 'كذيرت': 'جزيرة', 'الرودة': 'الروضة', 'بالحجب': 'بالحجم', 'الزرق': 'الزرقا', 'وصل': 'واصلة',
        'المصر': 'لمصر', 'الولاء': 'ولاية', 'دقوا': 'ضاقوا', 'ودقوا': 'وضاقوا', 'ومن': 'والدنيا', 'دنيا': '', 'بر': 'برة', 'وسماء': 'وسمّاها', 'وسقاها': 'وسمّاها',
        'جيه': 'جه', 'هيتتعمل': 'هتتعمل', 'وقاهرة': 'والقاهرة', 'أصوار': 'أسوار', 'اصوار': 'أسوار', 'صور': 'سور', 'المسلس': 'المثلث',
        'لقيمني': 'لأن', 'المباريج': 'المماليك', 'اتمالت': 'اتملت', 'اخيرها': 'آخرها', 'وقلعت': 'وقلعة', 'ديني': 'الدين', 'لأيوبي': 'الأيوبي',
        'تحكيل': 'تعديلات', 'عبدين': 'عابدين', 'القب': 'القبة', 'العلوية': 'العلوية', 'فشارع': 'فشارع', 'دوت': 'ده', 'ديت': 'دي', 'تتهمل': 'تتهمل',
        'تفضلت': 'فضلت', 'بيتخرج': 'بتخرج', 'ومشي': 'وماشية', 'وتسمت': 'واتسمّت', 'بي': 'بـ', 'مكافينا': 'مكفّينا', 'وإينا': 'وإحنا', 'اتردم': 'اتردم',
        'فيك': 'فيه', 'برسمة': 'برسم', 'زوء': 'ذات', 'مغطيها': 'مغطّيها', 'متغطية': 'متغطّية', 'كذيرة': 'جزيرة', 'فمبدائيا': 'فمبدئيًا',
        'الحدث': 'الحتة', 'نهري': 'نهر', 'للحد': 'لحد', 'فهم': 'فم', 'الاسرع': 'أسوار', 'اسر': 'قصر', 'الابة': 'عابدين', 'تبهدلت': 'اتبهدلت',
        'المؤطم': 'المقطم', 'العصد.': 'العاص'}

SPANS = {
    1: [(46.92, 58.02), (442.80, 450.74), (551.25, 554.85), (560.69, 569.85), (662.45, 675.19), (802.21, 805.61), (829.35, 839.17),
        (994.46, 998.90), (1032.36, 1040.70), (1258.96, 1265.02), (1302.50, 1304.38), (1305.86, 1308.52), (1337.66, 1344.70)],
    3: [(409.98, 417.80), (283.92, 286.88), (290.98, 307.20), (307.66, 318.08), (320.78, 337.12), (337.48, 365.18), (1349.66, 1353.44)],
    2: [(198.02, 201.68), (190.22, 197.68), (202.10, 212.60), (234.46, 250.39), (250.97, 255.25), (1017.46, 1023.68)],
    9: [(551.25, 554.85), (560.69, 565.21), (568.79, 569.85), (675.97, 680.55), (682.61, 684.19), (805.95, 816.61), (1285.02, 1302.18),
        (1302.50, 1304.38), (1305.86, 1308.52), (1315.40, 1317.08)],
    4: [(442.80, 450.74), (551.25, 559.05), (560.69, 572.69), (588.87, 596.93), (600.21, 611.19), (662.45, 681.99), (707.77, 713.13)],
    5: [(802.21, 805.61), (805.95, 816.61), (824.17, 846.21), (846.85, 854.19), (886.55, 912.19), (912.77, 926.26)],
    6: [(994.46, 1004.16), (1007.60, 1011.04), (1032.36, 1061.40), (1064.22, 1080.98), (1099.84, 1104.98)],
    7: [(1164.36, 1166.88), (466.56, 473.62), (475.88, 488.49), (489.19, 492.51), (1167.24, 1190.57), (1195.15, 1199.89)],
    8: [(1252.08, 1258.70), (1233.16, 1248.86), (1258.96, 1284.02)],
}
CTA_KEEP = (0.0, 6.0)
CTA_FIX = {'علي': 'على', 'وهو': 'وهبعتهولك', 'اعطولك': '', 'طول.': 'طول'}
OLD = (500, -2400)  # old-Cairo overview centre (metres)
C_ = lambda n: n  # place name passthrough (readability)

# ---------------- map plans (source seconds) ----------------
MAP = {
    1: {
        'cam': [{'t': 46.9, 'x': 62000, 'y': 20000, 's': 0.0045, 'tilt': 20}, {'t': 50.6, 'at': 'القاهرة', 's': 0.012, 'tilt': 30},
                {'t': 57.0, 'x': OLD[0], 'y': OLD[1], 's': 0.15, 'tilt': 38},
                {'t': 442.8, 'x': -700, 'y': -4300, 's': 0.24, 'tilt': 42}, {'t': 450.7, 'x': -800, 'y': -4700, 's': 0.33, 'tilt': 46, 'rot': -6},
                {'t': 554.8, 'x': -600, 'y': -4200, 's': 0.22, 'tilt': 42}, {'t': 562, 'x': -300, 'y': -3500, 's': 0.3, 'tilt': 44},
                {'t': 569.8, 'x': -200, 'y': -3400, 's': 0.3, 'tilt': 44, 'rot': 4}, {'t': 663.5, 'x': 0, 'y': -3200, 's': 0.22, 'tilt': 42},
                {'t': 671.2, 'x': 500, 'y': -2500, 's': 0.3, 'tilt': 45}, {'t': 675.2, 'x': 600, 'y': -2300, 's': 0.33, 'tilt': 46, 'rot': -5},
                {'t': 803.0, 'x': 1200, 'y': -900, 's': 0.22, 'tilt': 42}, {'t': 829.4, 'x': 1650, 'y': -500, 's': 0.33, 'tilt': 46},
                {'t': 839.2, 'x': 1650, 'y': -400, 's': 0.38, 'tilt': 48, 'rot': 6}, {'t': 994.5, 'x': OLD[0], 'y': OLD[1], 's': 0.15, 'tilt': 38},
                {'t': 1040.7, 'x': OLD[0], 'y': OLD[1] + 200, 's': 0.16, 'tilt': 40, 'rot': -4}, {'t': 1259.5, 'x': 1300, 'y': -1300, 's': 0.2, 'tilt': 42},
                {'t': 1265.0, 'x': 1300, 'y': -1100, 's': 0.22, 'tilt': 44, 'rot': 4}, {'t': 1303, 'x': 500, 'y': -900, 's': 0.25, 'tilt': 44},
                {'t': 1308.5, 'x': 350, 'y': -850, 's': 0.3, 'tilt': 46}, {'t': 1338.5, 'x': 300, 'y': -1500, 's': 0.11, 'tilt': 40},
                {'t': 1344.7, 'x': 0, 'y': -800, 's': 0.06, 'tilt': 36}],
        'ev': [{'l': 'canal_amr', 'at': 46.9, 'out': 50.0}, {'l': 'fields', 'at': 46.9}, {'l': 'oldnile', 'at': 46.9, 'out': 1032.4},
               {'l': 'khalij', 'at': 446.0}, {'l': 'fustat', 'at': 450.1}, {'l': 'focus_fustat', 'at': 551.5, 'out': 554.6},
               {'l': 'askar', 'at': 566.0}, {'l': 'qatai', 'at': 671.2}, {'l': 'fatimid', 'at': 829.4}, {'l': 'fwall', 'at': 836.0},
               {'l': 'swall', 'at': 1034.4}, {'l': 'citadel', 'at': 1035.5}, {'l': 'aqueduct', 'at': 1036.0},
               {'l': 'focus_fustat', 'at': 1038.0, 'out': 1041}, {'l': 'focus_askar', 'at': 1038.86, 'out': 1041}, {'l': 'focus_qatai', 'at': 1039.42, 'out': 1041},
               {'l': 'focus_fatimid', 'at': 1040.18, 'out': 1041.2}, {'l': 'mamluk', 'at': 1263.0}, {'l': 'modern', 'at': 1338.8, 'd': 5.5},
               {'l': 'roads', 'at': 1340.0}],
        'labels': [{'n': 'حصن بابليون', 'at': 444.7, 'out': 448.5, 'red': True}, {'n': 'مسجد عمرو بن العاص', 'at': 448.6, 'red': True, 'out': 554.0},
                   {'n': 'فوم الخليج', 'at': 446.0, 'out': 450.0, 'text': 'الخليج'},
                   {'n': 'مسجد بن طولون', 'at': 678.0, 'red': True, 'text': 'مسجد ابن طولون', 'out': 805},
                   {'n': 'الجامع الأزهر', 'at': 831.5, 'red': True, 'out': 838.5}, {'n': 'قلعة صلاح الدين', 'at': 1036.0, 'red': True, 'out': 1040.4},
                   {'n': 'مسجد السلطان حسن', 'at': 1259.8, 'red': True, 'out': 1264.5}, {'n': 'مسجد الظاهر بيبرس', 'at': 1260.6, 'red': True, 'out': 1265},
                   {'n': 'قصر عابدين', 'at': 1307.8, 'red': True, 'out': 1340.5}],
        'icons': [{'n': 'حصن بابليون', 'i': 'fort', 'at': 444.7}, {'n': 'مسجد عمرو بن العاص', 'i': 'mosque', 'at': 448.6},
                  {'n': 'مسجد بن طولون', 'i': 'spiral', 'at': 671.5}, {'n': 'الجامع الأزهر', 'i': 'mosque', 'at': 831.4},
                  {'n': 'باب الفتوح', 'i': 'gate', 'at': 838.3, 's': 0.6}, {'n': 'باب زويلة', 'i': 'gate', 'at': 838.6, 's': 0.6},
                  {'n': 'قلعة صلاح الدين', 'i': 'citadel', 'at': 1035.6}, {'n': 'مسجد السلطان حسن', 'i': 'mosque', 'at': 1259.8, 's': 0.6},
                  {'n': 'مسجد الظاهر بيبرس', 'i': 'mosque', 'at': 1260.6, 's': 0.6}, {'n': 'قصر عابدين', 'i': 'palace', 'at': 1307.8}],
        'years': [{'at': 442.8, 'y': 641, 'era': 'الفتح الإسلامي'}, {'at': 560.7, 'y': 750, 'era': 'العباسيين'}, {'at': 662.45, 'y': 870, 'era': 'ابن طولون'},
                  {'at': 802.2, 'y': 969, 'era': 'الفاطميين'}, {'at': 994.46, 'y': 1176, 'era': 'صلاح الدين الأيوبي'}, {'at': 1258.96, 'y': 1250, 'era': 'المماليك'},
                  {'at': 1302.5, 'y': 1874, 'era': 'الخديوي إسماعيل'}, {'at': 1337.66, 'y': 2025, 'era': 'القاهرة النهاردة'}],
        'balls': [{'c': 'fustat', 'at': 450.7, 'out': 554.0, 'name': 'الفسطاط'}, {'c': 'askar', 'at': 569.85, 'out': 663.0, 'name': 'العسكر'},
                  {'c': 'fustat', 'at': 664.5, 'out': 669.5, 'mood': 'squeeze'}, {'c': 'askar', 'at': 664.6, 'out': 669.5, 'mood': 'squeeze'},
                  {'c': 'qatai', 'at': 675.2, 'out': 805.0, 'name': 'القطائع'}, {'c': 'fatimid', 'at': 831.9, 'out': 997, 'name': 'القاهرة الفاطمية'},
                  {'c': 'mamluk', 'at': 1263.6, 'out': 1303, 'x': 2500, 'y': -500, 'name': 'المماليك'}],
    },
    3: {
        'cam': [{'t': 409.9, 'x': 900, 'y': -300, 's': 0.3, 'tilt': 46, 'rot': -14}, {'t': 417.8, 'x': 400, 'y': -1500, 's': 0.17, 'tilt': 40, 'rot': -8},
                {'t': 284.0, 'x': -900, 'y': -2700, 's': 0.26, 'tilt': 44}, {'t': 286.9, 'x': -600, 'y': -1900, 's': 0.2, 'tilt': 42},
                {'t': 293.7, 'x': 30000, 'y': 15000, 's': 0.0055, 'tilt': 24}, {'t': 303.0, 'x': 70000, 'y': 15000, 's': 0.0055, 'tilt': 26},
                {'t': 315.0, 'x': 60000, 'y': 15000, 's': 0.0058, 'tilt': 26}, {'t': 325.3, 'x': 12000, 'y': 15000, 's': 0.011, 'tilt': 30},
                {'t': 337.0, 'x': 14000, 'y': 18000, 's': 0.0105, 'tilt': 30}, {'t': 345.5, 'x': 40000, 'y': 15000, 's': 0.0055, 'tilt': 24},
                {'t': 356.5, 'x': -1200, 'y': -2600, 's': 0.06, 'tilt': 34}, {'t': 358.8, 'x': 30000, 'y': 15000, 's': 0.0055, 'tilt': 24},
                {'t': 365.2, 'x': 50000, 'y': 15000, 's': 0.0055, 'tilt': 26}, {'t': 1349.7, 'x': 400, 'y': -1200, 's': 0.17, 'tilt': 40},
                {'t': 1351.9, 'x': 400, 'y': -1200, 's': 0.17, 'tilt': 40}, {'t': 1353.5, 'x': 14000, 'y': 15000, 's': 0.012, 'tilt': 30}],
        'ev': [{'l': 'modern', 'at': 409.9, 'd': 0.05, 'out': 284.2}, {'l': 'roads', 'at': 409.9, 'd': 0.05, 'out': 284.2}, {'l': 'khalij', 'at': 414.4, 'd': 3.2},
               {'l': 'fields', 'at': 283.9}, {'l': 'oldnile', 'at': 283.9},
               {'l': 'canal_sesostris', 'at': 297.0, 'd': 5.0, 'out': 340.6}, {'l': 'boat_sesostris', 'at': 303.4, 'd': 4.5},
               {'l': 'canal_roman', 'at': 325.3, 'd': 5.0, 'out': 340.6}, {'l': 'canal_amr', 'at': 357.2, 'd': 3.5}, {'l': 'canal_sesostris', 'at': 359.7, 'd': 3.4},
               {'l': 'boat_amr', 'at': 360.0, 'd': 3.0}, {'l': 'modern', 'at': 1349.66, 'd': 0.05}, {'l': 'roads', 'at': 1349.66, 'd': 0.05},
               {'l': 'ismailia', 'at': 1353.0}],
        'labels': [{'n': 'شارع بورسعيد', 'at': 411.6, 'out': 417.6, 'red': True}, {'n': 'فوم الخليج', 'at': 284.5, 'out': 287.0, 'text': 'الخليج', 'red': True},
                   {'n': 'الزقازيق', 'at': 297.6, 'out': 318}, {'n': 'البحيرات المرة', 'at': 299.6, 'out': 318}, {'n': 'البحر الأحمر', 'at': 302.6, 'out': 318, 'dy': 20},
                   {'n': 'القاهرة', 'at': 293.7, 'out': 365.2, 'red': True}, {'n': 'فوم الخليج', 'at': 357.2, 'out': 358.6, 'text': 'فم الخليج', 'red': True},
                   {'n': 'الإسماعيلية', 'at': 1353.2, 'text': 'ترعة الإسماعيلية', 'red': True}],
        'years': [{'at': 290.98, 'y': 1850, 'era': 'الفراعنة', 'suf': 'ق.م'}, {'at': 314.48, 'y': 112, 'era': 'الرومان', 'suf': 'م'},
                  {'at': 342.06, 'y': 641, 'era': 'الفتح الإسلامي', 'suf': 'م'}],
    },
    2: {
        'cam': [{'t': 198.0, 'x': -2000, 'y': 200, 's': 0.3, 'tilt': 46}, {'t': 200.9, 'x': -2000, 'y': -1800, 's': 0.22, 'tilt': 44},
                {'t': 190.2, 'x': -1000, 'y': -1200, 's': 0.13, 'tilt': 38}, {'t': 197.7, 'x': -900, 'y': -1000, 's': 0.14, 'tilt': 40, 'rot': -4},
                {'t': 202.1, 'x': -1800, 'y': -1500, 's': 0.2, 'tilt': 42}, {'t': 205.7, 'x': 300, 'y': -300, 's': 0.22, 'tilt': 42},
                {'t': 210.6, 'x': -1300, 'y': -2900, 's': 0.28, 'tilt': 46}, {'t': 234.4, 'x': -1800, 'y': -1600, 's': 0.16, 'tilt': 40},
                {'t': 250.9, 'x': -1800, 'y': -1600, 's': 0.16, 'tilt': 40}, {'t': 255.2, 'x': -1500, 'y': -1500, 's': 0.15, 'tilt': 40},
                {'t': 1017.5, 'x': -1300, 'y': -1200, 's': 0.15, 'tilt': 40}, {'t': 1023.6, 'x': -1500, 'y': -1300, 's': 0.13, 'tilt': 38, 'rot': -5}],
        'ev': [{'l': 'modern', 'at': 198.0, 'd': 0.05, 'out': 199.4}, {'l': 'roads', 'at': 198.0, 'd': 0.05, 'out': 199.6},
               {'l': 'oldnile', 'at': 199.9, 'd': 1.4, 'out': 1020.4}, {'l': 'fields', 'at': 199.9, 'out': 1021.5}, {'l': 'focus_oldnile', 'at': 193.6, 'out': 197.5},
               {'l': 'khalij', 'at': 210.6}, {'l': 'modern', 'at': 1021.0, 'd': 2.6}, {'l': 'roads', 'at': 1021.5}],
        'labels': [{'n': 'جزيرة الزمالك', 'at': 198.7, 'out': 201.0}, {'n': 'جزيرة المنيل', 'at': 200.9, 'out': 201.7, 'text': 'جزيرة الروضة'},
                   {'n': 'ميدان المساحة - الدقي', 'at': 203.5, 'out': 212.6, 'text': 'الدقي'}, {'n': 'شارع بورسعيد', 'at': 205.7, 'out': 212.6},
                   {'n': 'فوم الخليج', 'at': 210.6, 'out': 212.6, 'text': 'فم الخليج', 'red': True},
                   {'n': 'جزيرة الزمالك', 'at': 1021.6, 'text': 'جزيرة الزمالك'}],
        'years': [{'at': 190.22, 'y': 641, 'era': 'الفتح الإسلامي'}, {'at': 1017.46, 'y': 1176, 'era': 'الأيوبيين'}],
    },
    9: {
        'cam': [{'t': 551.2, 'x': -500, 'y': -4300, 's': 0.24, 'tilt': 42}, {'t': 560.7, 'x': -300, 'y': -3700, 's': 0.24, 'tilt': 42},
                {'t': 569.8, 'x': 0, 'y': -3200, 's': 0.22, 'tilt': 42}, {'t': 677.0, 'x': 400, 'y': -2700, 's': 0.24, 'tilt': 42},
                {'t': 806.0, 'x': 1000, 'y': -1500, 's': 0.19, 'tilt': 40}, {'t': 816.6, 'x': 1300, 'y': -1100, 's': 0.2, 'tilt': 40},
                {'t': 1285.0, 'x': 1200, 'y': -2000, 's': 0.22, 'tilt': 42}, {'t': 1302.2, 'x': 1200, 'y': -1900, 's': 0.24, 'tilt': 44, 'rot': 6},
                {'t': 1305.9, 'x': 600, 'y': -1100, 's': 0.2, 'tilt': 42}, {'t': 1315.4, 'x': 1600, 'y': 800, 's': 0.11, 'tilt': 38},
                {'t': 1317.1, 'x': 1300, 'y': 0, 's': 0.085, 'tilt': 36, 'rot': -6}],
        'ev': [{'l': 'fields', 'at': 551.2}, {'l': 'oldnile', 'at': 551.2, 'out': 1285.0}, {'l': 'khalij', 'at': 551.2, 'd': 0.05},
               {'l': 'fustat', 'at': 551.3, 'd': 1.6}, {'l': 'askar', 'at': 561.0, 'd': 1.8}, {'l': 'qatai', 'at': 676.0, 'd': 1.8},
               {'l': 'fatimid', 'at': 806.5, 'd': 2.0}, {'l': 'fwall', 'at': 808.0}, {'l': 'swall', 'at': 1285.2}, {'l': 'citadel', 'at': 1285.6},
               {'l': 'mamluk', 'at': 1292.2, 'd': 2}, {'l': 'modern', 'at': 1303.0, 'd': 6}, {'l': 'roads', 'at': 1304.0}],
        'seats': [{'at': 551.6, 'n': 'الفسطاط#pt', 'k': 1, 'name': 'الفسطاط'}, {'at': 560.7, 'n': 'العسكر', 'k': 2, 'name': 'العسكر'},
                  {'at': 677.3, 'n': 'مسجد بن طولون', 'k': 3, 'name': 'القطائع'}, {'at': 811.7, 'n': 'القاهرة الفاطمية#pt', 'k': 4, 'name': 'القاهرة الفاطمية'},
                  {'at': 1288.7, 'n': 'قلعة صلاح الدين', 'k': 5, 'name': 'القلعة'}, {'at': 1307.8, 'n': 'قصر عابدين', 'k': 6, 'name': 'قصر عابدين'},
                  {'at': 1316.6, 'n': 'قصر القبة', 'k': 7, 'name': 'قصر القبة'}],
        'labels': [{'n': 'الفسطاط#pt', 'at': 552.0, 'out': 559.5, 'red': True, 'dy': 110}, {'n': 'العسكر', 'at': 561.0, 'out': 676, 'red': True, 'dy': 110},
                   {'n': 'مسجد بن طولون', 'at': 677.6, 'out': 806, 'red': True, 'text': 'القطائع', 'dy': 110},
                   {'n': 'القاهرة الفاطمية#pt', 'at': 812.0, 'out': 1286, 'red': True, 'text': 'القاهرة الفاطمية', 'dy': 110},
                   {'n': 'قلعة صلاح الدين', 'at': 1289.0, 'out': 1306, 'red': True, 'text': 'قلعة صلاح الدين', 'dy': 110},
                   {'n': 'قصر عابدين', 'at': 1308.2, 'red': True, 'dy': 110}, {'n': 'قصر القبة', 'at': 1316.8, 'red': True, 'dy': 110}],
        'icons': [{'n': 'مسجد عمرو بن العاص', 'i': 'mosque', 'at': 551.4, 's': 0.6}, {'n': 'مسجد بن طولون', 'i': 'spiral', 'at': 676.2, 's': 0.6},
                  {'n': 'قلعة صلاح الدين', 'i': 'citadel', 'at': 1285.6}, {'n': 'قصر عابدين', 'i': 'palace', 'at': 1307.8}, {'n': 'قصر القبة', 'i': 'palace', 'at': 1316.6}],
        'years': [{'at': 551.25, 'y': 641, 'era': 'الفسطاط'}, {'at': 560.69, 'y': 750, 'era': 'العسكر'}, {'at': 675.97, 'y': 870, 'era': 'القطائع'},
                  {'at': 805.95, 'y': 969, 'era': 'القاهرة الفاطمية'}, {'at': 1290.74, 'y': 1176, 'era': 'الأيوبيين'}, {'at': 1292.24, 'y': 1250, 'era': 'المماليك'},
                  {'at': 1293.66, 'y': 1517, 'era': 'العثمانيين'}, {'at': 1298.18, 'y': 1805, 'era': 'محمد علي'}, {'at': 1302.5, 'y': 1874, 'era': 'الخديوي إسماعيل'}],
    },
}
# overlay scenes: (id, src start, src end, props, beats{name: src sec})
FRONT = {
    1: [('ct', 46.9, 51.4, {'title': 'القاهرة اتبنت *إزاي*؟', 'sub': 'من خريطتي أنا على جوجل إيرث', 'top': 0.22}, {}),
        ('cchip', 553.8, 554.85, {'text': 'أول عاصمة لمصر الإسلامية', 'ok': True, 'top': 0.33}, {})],
    3: [('ct', 409.9, 413.6, {'title': 'شارع بورسعيد… *كان نهر!*', 'top': 0.32}, {}),
        ('cpaper', 290.9, 296.0, {'src': PJ + 'map_pharaoh_canal.jpg', 'ratio': 920 / 856, 'w': 820, 'top': 0.45, 'mark': [24, 38, 18, 9], 'tag': 'قناة سيزوستريس'},
         {'mark': 293.7}),
        ('cchip', 363.4, 365.2, {'text': 'خليج أمير المؤمنين', 'ok': True, 'top': 0.34}, {}),
        ('cchip', 1350.6, 1352.0, {'text': 'اتردم ✗', 'top': 0.34}, {})],
    2: [('ct', 198.0, 199.9, {'title': 'جزيرة الزمالك… *ما كانتش موجودة!*', 'top': 0.33, 'size': 84}, {}),
        ('cpaper', 234.4, 245.2, {'src': PJ + 'map_roda.jpg', 'ratio': 920 / 780, 'w': 800, 'top': 0.44, 'mark': [10, 83, 9, 13], 'tag': 'الروضة بس… فين الزمالك؟'},
         {'mark': 240.2}),
        ('cchip', 242.7, 245.0, {'text': 'الزمالك؟ ✗', 'top': 0.7}, {}),
        ('cpaper', 245.2, 250.4, {'src': PJ + 'map_nile_bw.jpg', 'ratio': 920 / 1100, 'w': 860, 'top': 0.44, 'mark': [38, 82, 10, 12], 'from': 'left'}, {'mark': 247.0})],
    9: [('ct', 551.2, 554.8, {'title': 'مركز الحكم في مصر *اتنقل 7 مرات!*', 'top': 0.33, 'size': 84}, {})],
}

def base(T, upto='qatai', nile_out=None, nile=True):
    """the city as it already was at time T (layers appear instantly)"""
    order = ['fustat', 'askar', 'qatai', 'fatimid', 'fwall', 'swall', 'citadel', 'aqueduct', 'mamluk']
    ev = [{'l': 'fields', 'at': T, 'd': 0.05}, {'l': 'khalij', 'at': T, 'd': 0.05}]
    ev += [{'l': k, 'at': T, 'd': 0.05} for k in order[:order.index(upto) + 1]]
    if nile:  # the wide Nile only until the Ayyubids (Aly: it shrank in the Ayyubid era)
        ev.append({'l': 'oldnile', 'at': T, 'd': 0.05, **({'out': nile_out} if nile_out else {})})
    return ev


MAP.update({
    4: {
        'cam': [{'t': 442.8, 'x': -700, 'y': -4300, 's': 0.24, 'tilt': 42}, {'t': 450.7, 'x': -800, 'y': -4700, 's': 0.33, 'tilt': 46, 'rot': -6},
                {'t': 551.2, 'x': -700, 'y': -4500, 's': 0.28, 'tilt': 44}, {'t': 559.0, 'x': -600, 'y': -4300, 's': 0.26, 'tilt': 42},
                {'t': 560.7, 'x': -300, 'y': -3700, 's': 0.24, 'tilt': 42}, {'t': 572.7, 'x': -150, 'y': -3400, 's': 0.3, 'tilt': 44, 'rot': 4},
                {'t': 588.9, 'x': -150, 'y': -3300, 's': 0.3, 'tilt': 44}, {'t': 596.9, 'x': -200, 'y': -3500, 's': 0.28, 'tilt': 44},
                {'t': 600.2, 'x': -300, 'y': -3900, 's': 0.2, 'tilt': 42}, {'t': 611.2, 'x': -400, 'y': -4100, 's': 0.19, 'tilt': 42},
                {'t': 662.45, 'x': 0, 'y': -3300, 's': 0.2, 'tilt': 42}, {'t': 671.2, 'x': 500, 'y': -2500, 's': 0.3, 'tilt': 45},
                {'t': 681.9, 'x': 450, 'y': -2400, 's': 0.34, 'tilt': 46, 'rot': -5}, {'t': 707.8, 'x': 0, 'y': -3300, 's': 0.15, 'tilt': 40},
                {'t': 713.1, 'x': 0, 'y': -3200, 's': 0.155, 'tilt': 40, 'rot': -4}],
        'ev': [{'l': 'fields', 'at': 442.8}, {'l': 'oldnile', 'at': 442.8}, {'l': 'khalij', 'at': 446.0}, {'l': 'fustat', 'at': 450.1},
               {'l': 'focus_fustat', 'at': 556.9, 'out': 559.0}, {'l': 'outline_askar', 'at': 566.0}, {'l': 'askar', 'at': 605.6, 'd': 3.5},
               {'l': 'focus_askar', 'at': 608.9, 'out': 611.2}, {'l': 'focus_fustat', 'at': 610.8, 'out': 611.2},
               {'l': 'qatai', 'at': 671.2}, {'l': 'focus_fustat', 'at': 708.7, 'out': 713.2}, {'l': 'focus_askar', 'at': 708.4, 'out': 713.2},
               {'l': 'focus_qatai', 'at': 710.6, 'out': 713.2}],
        'labels': [{'n': 'حصن بابليون', 'at': 444.7, 'out': 448.5, 'red': True}, {'n': 'مسجد عمرو بن العاص', 'at': 448.6, 'out': 559.0, 'red': True},
                   {'n': 'مسجد بن طولون', 'at': 678.2, 'red': True, 'text': 'مسجد ابن طولون', 'out': 707.7}],
        'icons': [{'n': 'حصن بابليون', 'i': 'fort', 'at': 444.7}, {'n': 'مسجد عمرو بن العاص', 'i': 'mosque', 'at': 448.6},
                  {'n': 'مسجد بن طولون', 'i': 'spiral', 'at': 678.2}, {'n': '@900,-2000', 'i': 'palace', 'at': 680.5, 's': 0.6}],
        'years': [{'at': 442.8, 'y': 641, 'era': 'الفسطاط'}, {'at': 560.69, 'y': 750, 'era': 'العسكر'}, {'at': 662.45, 'y': 870, 'era': 'القطائع'}],
        'balls': [{'c': 'fustat', 'at': 450.7, 'out': 664.4, 'name': 'الفسطاط'}, {'c': 'askar', 'at': 569.85, 'out': 590.6, 'name': 'العسكر'},
                  {'c': 'askar', 'at': 590.9, 'out': 600.0, 'x': -500, 'y': -3000, 'mood': 'angry'}, {'c': 'askar', 'at': 591.2, 'out': 600.0, 'x': 200, 'y': -3200, 'mood': 'angry'},
                  {'c': 'askar', 'at': 591.5, 'out': 600.0, 'x': -150, 'y': -3700, 'mood': 'angry'}, {'c': 'askar', 'at': 600.3, 'out': 664.4, 'name': 'العسكر'},
                  {'c': 'fustat', 'at': 664.5, 'out': 669.6, 'mood': 'squeeze'}, {'c': 'askar', 'at': 664.6, 'out': 669.6, 'mood': 'squeeze'},
                  {'c': 'qatai', 'at': 675.2, 'out': 707.6, 'name': 'القطائع'},
                  {'c': 'fustat', 'at': 707.9, 'name': 'الفسطاط'}, {'c': 'askar', 'at': 708.4, 'name': 'العسكر'}, {'c': 'qatai', 'at': 710.6, 'name': 'القطائع'}],
    },
    5: {
        'cam': [{'t': 802.2, 'x': 500, 'y': -2000, 's': 0.15, 'tilt': 40}, {'t': 816.6, 'x': 700, 'y': -1600, 's': 0.16, 'tilt': 40},
                {'t': 824.2, 'x': 1000, 'y': -1500, 's': 0.2, 'tilt': 42}, {'t': 829.4, 'x': 1650, 'y': -500, 's': 0.3, 'tilt': 45},
                {'t': 839.2, 'x': 1650, 'y': -400, 's': 0.36, 'tilt': 47, 'rot': 6}, {'t': 846.9, 'x': 1700, 'y': -200, 's': 0.4, 'tilt': 48},
                {'t': 854.2, 'x': 1700, 'y': -150, 's': 0.44, 'tilt': 48, 'rot': -4}, {'t': 886.6, 'x': 1700, 'y': -200, 's': 0.3, 'tilt': 45},
                {'t': 893.8, 'x': 1750, 'y': 150, 's': 0.38, 'tilt': 47}, {'t': 897.3, 'x': 1350, 'y': -100, 's': 0.38, 'tilt': 47},
                {'t': 900.6, 'x': 1600, 'y': -650, 's': 0.38, 'tilt': 47}, {'t': 908.0, 'x': 2050, 'y': -250, 's': 0.38, 'tilt': 47},
                {'t': 912.2, 'x': 1700, 'y': -200, 's': 0.28, 'tilt': 44}, {'t': 926.3, 'x': 1700, 'y': -200, 's': 0.3, 'tilt': 46, 'rot': 8}],
        'ev': base(802.2) + [{'l': 'fatimid', 'at': 829.4, 'd': 3}, {'l': 'fwall', 'at': 838.3, 'd': 2.5}, {'l': 'focus_fatimid', 'at': 912.8, 'out': 926.3}],
        'labels': [{'n': 'القطائع#pt', 'at': 824.9, 'out': 829.2, 'red': True}, {'n': 'الجامع الأزهر', 'at': 849.4, 'red': True, 'out': 886.5},
                   {'n': 'باب الفتوح', 'at': 893.8, 'red': True, 'out': 912.6}, {'n': 'باب القنطرة', 'at': 897.3, 'red': True, 'out': 912.6},
                   {'n': 'باب زويلة', 'at': 900.6, 'red': True, 'out': 912.6}, {'n': 'باب البرقية', 'at': 908.0, 'red': True, 'out': 912.6}],
        'icons': [{'n': 'الجامع الأزهر', 'i': 'mosque', 'at': 849.4}, {'n': 'باب الفتوح', 'i': 'gate', 'at': 893.8, 's': 0.7},
                  {'n': 'باب القنطرة', 'i': 'gate', 'at': 897.3, 's': 0.7}, {'n': 'باب زويلة', 'i': 'gate', 'at': 900.6, 's': 0.7},
                  {'n': 'باب البرقية', 'i': 'gate', 'at': 908.0, 's': 0.7}],
        'years': [{'at': 802.21, 'y': 969, 'era': 'الفاطميين'}],
        'balls': [{'c': 'fatimid', 'at': 811.7, 'out': 828.9, 'name': 'مركز الخلافة'}, {'c': 'fatimid', 'at': 831.9, 'out': 886.4, 'name': 'القاهرة الفاطمية'}],
    },
    6: {
        'cam': [{'t': 994.5, 'x': 1500, 'y': -600, 's': 0.28, 'tilt': 44}, {'t': 1004.1, 'x': 1500, 'y': -500, 's': 0.3, 'tilt': 45, 'rot': 5},
                {'t': 1007.6, 'x': 800, 'y': -1800, 's': 0.16, 'tilt': 40}, {'t': 1011.0, 'x': 600, 'y': -2200, 's': 0.15, 'tilt': 40},
                {'t': 1032.4, 'x': 500, 'y': -2400, 's': 0.15, 'tilt': 40}, {'t': 1047.2, 'x': 400, 'y': -2300, 's': 0.16, 'tilt': 40, 'rot': -4},
                {'t': 1051.5, 'x': 1300, 'y': -2200, 's': 0.32, 'tilt': 46}, {'t': 1056.0, 'x': 1400, 'y': -2100, 's': 0.34, 'tilt': 47, 'rot': 6},
                {'t': 1061.0, 'x': 1700, 'y': -1500, 's': 0.2, 'tilt': 42}, {'t': 1064.2, 'x': -700, 'y': -3000, 's': 0.28, 'tilt': 44},
                {'t': 1072.0, 'x': 200, 'y': -2700, 's': 0.26, 'tilt': 44}, {'t': 1078.0, 'x': 1100, 'y': -2500, 's': 0.3, 'tilt': 45},
                {'t': 1081.0, 'x': 1300, 'y': -2300, 's': 0.32, 'tilt': 46}, {'t': 1099.8, 'x': 500, 'y': -2400, 's': 0.15, 'tilt': 40},
                {'t': 1105.0, 'x': 500, 'y': -2300, 's': 0.16, 'tilt': 40}],
        'ev': base(994.4, 'fatimid', 1032.4) + [{'l': 'fwall', 'at': 1001.5, 'd': 2.5}, {'l': 'mamluk', 'at': 1010.4, 'd': 2.0},
               {'l': 'swall', 'at': 1034.4, 'd': 4}, {'l': 'focus_fustat', 'at': 1038.0, 'out': 1042}, {'l': 'focus_askar', 'at': 1038.86, 'out': 1042},
               {'l': 'focus_qatai', 'at': 1039.42, 'out': 1042}, {'l': 'focus_fatimid', 'at': 1040.18, 'out': 1042.2},
               {'l': 'citadel', 'at': 1052.5, 'd': 2}, {'l': 'aqueduct', 'at': 1066.4, 'd': 14}],
        'labels': [{'n': 'قلعة صلاح الدين', 'at': 1053.5, 'red': True, 'out': 1064.0}, {'n': 'سور مجرى العيون', 'at': 1066.8, 'red': True, 'out': 1081},
                   {'n': 'فوم الخليج', 'at': 1067.8, 'text': 'فم الخليج', 'out': 1081}, {'n': 'باب القرافة', 'at': 1078.0, 'red': True, 'out': 1081}],
        'icons': [{'n': 'قلعة صلاح الدين', 'i': 'citadel', 'at': 1052.5}],
        'years': [{'at': 994.46, 'y': 1176, 'era': 'صلاح الدين الأيوبي'}],
    },
    7: {
        'cam': [{'t': 1164.3, 'x': 600, 'y': -2300, 's': 0.15, 'tilt': 40}, {'t': 466.5, 'x': 600, 'y': -2300, 's': 0.15, 'tilt': 40},
                {'t': 492.5, 'x': 600, 'y': -2200, 's': 0.16, 'tilt': 40}, {'t': 1167.2, 'x': -600, 'y': -3000, 's': 0.26, 'tilt': 44},
                {'t': 1174.0, 'x': 800, 'y': -2600, 's': 0.24, 'tilt': 44}, {'t': 1184.3, 'x': 1200, 'y': -2300, 's': 0.2, 'tilt': 42},
                {'t': 1190.5, 'x': 1500, 'y': -2400, 's': 0.22, 'tilt': 42}, {'t': 1195.1, 'x': 300, 'y': -2700, 's': 0.2, 'tilt': 42},
                {'t': 1199.9, 'x': 700, 'y': -2500, 's': 0.21, 'tilt': 43, 'rot': 5}],
        'ev': base(466.5, 'mamluk', nile=False) + base(1164.3, 'mamluk', nile=False) + [{'l': 'aqueduct', 'at': 1172.1, 'd': 2.2}, {'l': 'focus_fatimid', 'at': 1177.0, 'out': 1180.0}],
        'labels': [{'n': 'فوم الخليج', 'at': 1169.5, 'text': 'فم الخليج', 'red': True}, {'n': 'قلعة صلاح الدين', 'at': 1174.1, 'red': True},
                   {'n': 'القاهرة الفاطمية#pt', 'at': 1177.5, 'text': 'القاهرة'}, {'n': 'مدينة المقطم', 'at': 1181.9, 'text': 'جبل المقطم'},
                   {'n': '@-900,-1500', 'at': 1176.4, 'text': '⬅ الغرب', 'out': 1199.9}, {'n': '@2500,-1700', 'at': 1178.9, 'text': 'الشرق ➡', 'red': True}],
        'icons': [{'n': 'قلعة صلاح الدين', 'i': 'citadel', 'at': 1174.1}],
        'years': [{'at': 466.56, 'y': 1525, 'era': 'بيري ريس'}],
    },
    8: {
        'cam': [{'t': 1252.0, 'x': 1700, 'y': 1150, 's': 0.32, 'tilt': 46}, {'t': 1254.6, 'x': 1500, 'y': 600, 's': 0.22, 'tilt': 44},
                {'t': 1258.7, 'x': 1500, 'y': 500, 's': 0.2, 'tilt': 43}, {'t': 1233.1, 'x': 900, 'y': -1200, 's': 0.15, 'tilt': 40},
                {'t': 1243.9, 'x': 900, 'y': -1200, 's': 0.16, 'tilt': 40}, {'t': 1246.4, 'x': 1350, 'y': -1900, 's': 0.3, 'tilt': 46},
                {'t': 1248.8, 'x': 1400, 'y': -1900, 's': 0.32, 'tilt': 46, 'rot': 5}, {'t': 1258.96, 'x': 1300, 'y': -600, 's': 0.17, 'tilt': 42},
                {'t': 1266.0, 'x': 1300, 'y': -600, 's': 0.17, 'tilt': 42}, {'t': 1272.0, 'x': 1000, 'y': -300, 's': 0.22, 'tilt': 44},
                {'t': 1281.5, 'x': 900, 'y': -1000, 's': 0.14, 'tilt': 40, 'rot': -5}, {'t': 1284.0, 'x': 900, 'y': -1000, 's': 0.135, 'tilt': 40}],
        'ev': base(1252.0, 'aqueduct', nile=False) + base(1233.1, 'aqueduct', nile=False) + [{'l': 'mamluk', 'at': 1263.66, 'd': 4}, {'l': 'focus_fatimid', 'at': 1254.5, 'out': 1258.7}],
        'labels': [{'n': 'مسجد الظاهر بيبرس', 'at': 1253.5, 'red': True, 'out': 1258.8}, {'n': 'مسجد السلطان حسن', 'at': 1246.4, 'red': True, 'out': 1249},
                   {'n': 'مسجد الظاهر بيبرس', 'at': 1266.3, 'red': True}],
        'icons': [{'n': 'مسجد الظاهر بيبرس', 'i': 'mosque', 'at': 1252.1, 's': 0.8}, {'n': 'مسجد السلطان حسن', 'i': 'mosque', 'at': 1246.4, 's': 0.8},
                  {'n': 'قلعة صلاح الدين', 'i': 'citadel', 'at': 1233.1}],
        'years': [{'at': 1233.16, 'y': 1250, 'era': 'المماليك'}],
        'balls': [{'c': 'mamluk', 'at': 1264.0, 'x': 2700, 'y': -200, 'name': 'برة السور'}],
    },
})
FRONT_MORE = {
    4: [('ct', 442.8, 445.5, {'title': 'أول 3 عواصم *قبل القاهرة*', 'top': 0.33}, {}),
        ('cchip', 711.6, 713.13, {'text': 'كأنها مدينة واحدة ✓', 'ok': True, 'top': 0.34}, {})],
    5: [('ct', 802.2, 805.6, {'title': 'أول مدينة *بسور* في مصر الإسلامية', 'top': 0.33, 'size': 84}, {}),
        ('cpaper', 851.3, 854.19, {'src': PJ + 'map_muizz.jpg', 'ratio': 820 / 630, 'w': 640, 'top': 0.43, 'mark': [57, 32, 9, 15], 'tag': 'شارع المعز'}, {'mark': 852.7}),
        ('cpaper', 886.55, 893.6, {'src': PJ + 'map_gates.jpg', 'ratio': 820 / 630, 'w': 660, 'top': 0.43, 'tag': 'أبواب القاهرة الفاطمية', 'from': 'left'}, {}),
        ('cchip', 918.8, 926.26, {'text': 'لسه موجودة لحد النهاردة ✓', 'ok': True, 'top': 0.34}, {})],
    6: [('ct', 994.5, 997.8, {'title': 'صلاح الدين *قفل على القاهرة كلها*', 'top': 0.33, 'size': 84}, {}),
        ('cpaper', 1099.84, 1104.98, {'src': PJ + 'map_salah_walls.jpg', 'ratio': 960 / 1140, 'w': 920, 'top': 0.44, 'tag': 'أسوار صلاح الدين (بول كازانوفا)'}, {})],
    7: [('ct', 1164.36, 1166.88, {'title': 'لغز في خريطة *عمرها 500 سنة*', 'top': 0.33}, {}),
        ('cpaper', 466.5, 473.7, {'src': PJ + 'map_piri.jpg', 'ratio': 920 / 1240, 'w': 960, 'top': 0.45, 'tag': 'خريطة بيري ريس — الدولة العثمانية'}, {}),
        ('cpaper', 475.88, 488.49, {'src': PJ + 'map_piri.jpg', 'ratio': 920 / 1240, 'w': 960, 'top': 0.45, 'flip': True, 'tag': 'الخريطة مقلوبة!'}, {'spin': 480.3}),
        ('cchip', 489.19, 492.51, {'text': 'زمان كتير من الخرايط كانت بتترسم كده', 'ok': True, 'top': 0.34}, {}),
        ('cpaper', 1175.0, 1184.2, {'src': PJ + 'map_piri.jpg', 'ratio': 920 / 1240, 'w': 960, 'top': 0.45, 'tag': 'القلعة في الغرب؟!', 'mark': [55, 30, 14, 10]}, {'mark': 1176.4}),
        ('cchip', 1184.3, 1186.4, {'text': 'عشان الخريطة مقلوبة!', 'top': 0.34}, {}),
        ('cchip', 1197.2, 1199.89, {'text': 'القلعة شرق القاهرة ✓', 'ok': True, 'top': 0.34}, {})],
    8: [('ct', 1252.08, 1254.5, {'title': 'ليه جامع بيبرس *برة السور؟*', 'top': 0.33}, {}),
        ('cchip', 1237.6, 1240.0, {'text': 'العصر الذهبي للقاهرة ✓', 'ok': True, 'top': 0.34}, {}),
        ('cpaper', 1271.82, 1279.2, {'src': PJ + 'map_braun.jpg', 'ratio': 920 / 1500, 'w': 980, 'top': 0.42, 'tag': 'بيوت قدام أسوار القاهرة'}, {})],
}
FRONT.update(FRONT_MORE)

# his face: 'big' = cut-out from the green-screen intro (aly_hook.webm starts at src 46.0); 'bubble'/'bubble-r' = webcam corner clip
ALY = {
    1: [(46.92, 58.3, 'big'), (551.25, 554.85, 'bubble'), (1337.66, 1344.7, 'bubble')],
    3: [(409.98, 413.7, 'bubble'), (325.86, 332.04, 'bubble-r')],
    2: [(250.97, 255.25, 'bubble')],
    9: [(1288.06, 1292.24, 'bubble')],
}
HOOK = {'file': PJ + 'aly_hook.webm', 'src': 46.0, 'face': [0.5, 0.4, 0.28]}
import os
V = os.environ.get('V', '')  # V=v2 -> props short_<n>_v2.json (Aly: keep the old versions, make new ones)
ROTO = sorted(float(f.stem[5:]) for f in PUB.glob('roto_*.webm'))
HIDE = {1: [0], 3: [], 2: [], 9: [], 4: [], 5: [], 6: [], 7: [], 8: []}  # range indexes WITHOUT his cut-out (1: hook = green-screen cut-out)


def roto_for(a, b):
    """cut-out file covering source range [a, b] -> (file, src start); ranges merged exactly like roto_all.py"""
    rng = sorted({(x, y) for v in SPANS.values() for x, y in v if x > 80})
    merged = []
    for x, y in rng:
        if merged and x <= merged[-1][1] + 1.0:
            merged[-1][1] = max(merged[-1][1], y)
        else:
            merged.append([x, y])
    for x, y in merged:
        if x <= a and b <= y:
            r0 = x - 1.0
            if (PUB / f'roto_{r0:.2f}.webm').exists():
                return PJ + f'roto_{r0:.2f}.webm', r0
    print(f'  !! no cut-out yet for {a}-{b}')
    return None, None


KEEP = set()


def alpha_pos(file, at):
    """[face x, face y, head width] in the cut-out square, from its alpha (top of the head + 32 px of 270). Cached."""
    import subprocess, numpy as np
    cache = W / 'alpha_pos.json'
    c = json.load(open(cache)) if cache.exists() else {}
    key = f'{file}@{at:.2f}'
    if key not in c:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-c:v', 'libvpx-vp9', '-ss', f'{at:.2f}', '-i', str(ROOT / 'motion-library/public' / file), '-frames:v', '1',
                              '-vf', 'scale=270:270', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], capture_output=True).stdout
        a = np.frombuffer(raw, np.uint8).reshape(270, 270, 4)[..., 3] > 128
        a[:, :60] = False  # ignore the mouse hand on the left
        rows = np.where(a.any(1))[0]
        y0 = rows[0]; band = a[y0:y0 + 50]
        xs = np.where(band.any(0))[0]
        c[key] = [round(np.where(band)[1].mean() / 270, 3), round((y0 + 32) / 270, 3), round((xs[-1] - xs[0]) / 270, 3)]
        json.dump(c, open(cache, 'w'), indent=1)
    return c[key]


def span(t0, t1):
    i = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t0))
    j = min(range(len(_words)), key=lambda k: abs(_words[k]['start'] - t1))
    prev = _words[i - 1]['end'] if i > 0 else None
    nxt = _words[j + 1]['start'] if j + 1 < len(_words) else None
    a, b, rep = fit(_words[i]['start'], _words[j]['end'], prev, nxt)
    KEEP.update(id(w) for w in _words[i:j + 1])
    print('   ', _words[i]['w'], '…', _words[j]['w'], rep)
    return [a, b]


def build(n):
    global BUBBLE_V2
    print(f'short {n} edges:')
    KEEP.clear()
    ranges = [span(a, b) for a, b in SPANS[n]]
    segs, tl = [], 0.0
    for a, b in ranges:
        segs.append({'src': a, 'tl': round(tl, 3), 'len': round(b - a, 3)}); tl += b - a
    main = tl

    def to_tl(t):  # source second -> timeline second (nearest range edge if t falls in a cut)
        for s in segs:
            if s['src'] - 0.01 <= t <= s['src'] + s['len'] + 0.01:
                return round(s['tl'] + max(0.0, min(t - s['src'], s['len'])), 3)
        best = min([(abs(t - s['src']), s['tl']) for s in segs] + [(abs(t - s['src'] - s['len']), s['tl'] + s['len']) for s in segs])
        if best[0] > 2.5:
            print(f'  !! short {n}: {t} is {best[0]:.1f}s outside the ranges')
        return round(best[1], 3)

    # captions = exactly the kept words, word spelling fixed
    words = []
    for w in _words:
        if id(w) not in KEEP:
            continue
        x = WFIX.get(w['w'], w['w'])
        if not x:
            continue
        ra = next((r for r in ranges if r[0] - 0.05 <= w['start'] < r[1]), None)
        if ra is None:
            continue
        words.append({'w': x, 'start': to_tl(max(w['start'], ra[0])), 'end': to_tl(max(ra[0], min(w['end'], ra[1])))})
    ct = json.load(open(W / 'cta' / 'transcript.json', encoding='utf8'))
    cw = [w for s_ in ct['sentences'] for w in s_['words']]
    for i, w in enumerate(cw):
        x = CTA_FIX.get(w['w'], w['w'])
        if i > 7 and w['w'] == 'اليوتيوب':
            x = 'يوتيوب'
        if x and w['start'] < CTA_KEEP[1]:
            words.append({'w': x, 'start': round(main + w['start'], 3), 'end': round(main + min(w['end'], CTA_KEEP[1]), 3)})

    # map scene (whole main part) with every time converted
    mp = json.loads(json.dumps(MAP[n]))
    for key in ('cam', 'ev', 'labels', 'years', 'balls', 'seats', 'icons'):
        for e in mp.get(key, []):
            for tk in (('t',) if key == 'cam' else ('at', 'out')):
                if tk in e:
                    e[tk] = to_tl(e[tk])
        if key == 'cam':
            mp[key].sort(key=lambda c: c['t'])
            for a_, b_ in zip(mp[key], mp[key][1:]):  # equal times after mapping -> keep order, nudge
                if b_['t'] <= a_['t']:
                    b_['t'] = round(a_['t'] + 0.05, 3)
    if (V == 'v2' or n in (4, 5, 6, 7, 8)) and not (V == 'v2' and n in (4, 5, 6)):
        mp['cx'], mp['cy'] = 0.4, 0.52  # Aly stands bottom-right -> the map's action moves left/up
    if V == 'v2' and n in (4, 5, 6):
        mp['cx'], mp['cy'] = 0.6, 0.5  # round webcam bottom-left -> map action right/up
    scenes = [{'t': 'cmap', 'at': 0, 'dur': round(main, 3), 'layer': 'back', 'props': mp}]
    for t, a, b, props, beats in FRONT.get(n, []):
        at = to_tl(a); dur = to_tl(b) - at
        pr = dict(props); pr['b'] = {k: round(to_tl(v) - at, 3) for k, v in beats.items()}
        scenes.append({'t': t, 'at': at, 'dur': round(dur, 3), 'layer': 'front', 'props': pr})
    aly = []
    aly_v2 = V == 'v2' or n in (4, 5, 6, 7, 8)
    BUBBLE_V2 = V == 'v2' and n in (4, 5, 6)  # Aly 2026-10-09: big in the opening only, round webcam after
    if aly_v2:
        ALY[n] = [x for x in ALY.get(n, []) if x[2] == 'big']
        for i, (a, b) in enumerate(SPANS[n]):
            if i in HIDE.get(n, []) or a < 80:
                continue
            fl, r0 = roto_for(a, b)
            if fl:
                fx, fy, hw = alpha_pos(fl, (a + b) / 2 - r0)
                sg = segs[i]  # the whole fitted piece -> windows touch each other exactly
                if BUBBLE_V2 and i > 0:  # v2 of 4/5/6: big only in the opening, then the small round webcam (no roto)
                    aly.append({'file': fl.replace('roto_', 'camr_').replace('.webm', '.mp4'), 'at': sg['tl'], 'dur': sg['len'],
                                'from': round(sg['src'] - r0, 3), 'mode': 'bubble', 'face': [0.5, 0.4, 0.3]})
                    continue
                aly.append({'file': fl, 'at': sg['tl'], 'dur': sg['len'], 'from': round(sg['src'] - r0, 3), 'mode': 'anchor',
                            'face': [fx, fy, hw], 'clipL': 0.3})
    # consecutive cut-out windows (touching on the timeline) continue each other: no pop-out / pop-in between pieces
    ws = sorted(aly, key=lambda x: x['at'])
    for x, y in zip(ws, ws[1:]):
        if abs(y['at'] - (x['at'] + x['dur'])) < 0.08 and x['mode'] == y['mode']:
            x['aout'] = False; y['ain'] = False
    for a, b, mode in ALY.get(n, []):
        if mode == 'big':
            aly.append({'file': HOOK['file'], 'at': to_tl(a), 'dur': round(to_tl(b) - to_tl(a), 3), 'from': round(a - HOOK['src'], 3), 'mode': 'big', 'face': HOOK['face']})
        else:
            c = CAMS[f'{a}-{b}']
            aly.append({'file': c['file'], 'at': to_tl(a), 'dur': round(to_tl(b) - to_tl(a), 3), 'from': round(a - c['src'], 3), 'mode': mode, 'face': [0.5, 0.4, 0.3]})

    # sound design: map events get their own sounds
    L = 'sfx/'
    sfx = [{'file': L + 'impact.wav', 'at': 0.05, 'vol': 0.45}]
    SND = {'fustat': ('magic', 0.35), 'askar': ('magic', 0.35), 'qatai': ('magic', 0.35), 'fatimid': ('magic', 0.4), 'mamluk': ('magic', 0.35),
           'modern': ('riser', 0.35), 'oldnile': ('pour', 0.35), 'khalij': ('pour', 0.4), 'fwall': ('stamp', 0.4), 'swall': ('stamp', 0.45),
           'citadel': ('impact', 0.35), 'canal_sesostris': ('pour', 0.35), 'canal_roman': ('pour', 0.35), 'canal_amr': ('pour', 0.4)}
    for e in mp['ev']:
        if e['l'] in SND and e.get('d', 1) > 0.1 and e['at'] < main - 0.3:
            sfx.append({'file': L + SND[e['l']][0] + '.wav', 'at': e['at'], 'vol': SND[e['l']][1], 'dur': 2.5})
    for i, y in enumerate(mp.get('years', [])):
        sfx.append({'file': L + 'tick.wav', 'at': y['at'], 'vol': 0.4}); sfx.append({'file': L + 'stamp.wav', 'at': round(y['at'] + 0.85, 3), 'vol': 0.35})
    for i, l_ in enumerate(mp.get('labels', [])):
        sfx.append({'file': L + f'pop_{i % 3 + 1}.wav', 'at': l_['at'], 'vol': 0.3})
    for b_ in mp.get('balls', []):
        sfx.append({'file': L + 'swoop_up.wav', 'at': b_['at'], 'vol': 0.35})
    for s_ in mp.get('seats', []):
        sfx += [{'file': L + 'swoop_up.wav', 'at': s_['at'], 'vol': 0.4}, {'file': L + 'ding.wav', 'at': round(s_['at'] + 0.75, 3), 'vol': 0.4}]
    cams = mp['cam']
    for a_, b_ in zip(cams, cams[1:]):  # big camera jumps
        if abs(a_['s'] / b_['s'] - 1) > 0.8 and b_['t'] - a_['t'] < 3:
            sfx.append({'file': L + 'whoosh_2.wav', 'at': a_['t'], 'vol': 0.4})
    for s in scenes[1:]:
        snd = {'ct': ('impact', 0.45), 'cpaper': ('paper', 0.55), 'cchip': ('buzz_wrong' if not s['props'].get('ok') else 'ding', 0.4)}[s['t']]
        sfx.append({'file': L + snd[0] + '.wav', 'at': s['at'], 'vol': snd[1]})
    sfx += [{'file': L + 'whoosh_2.wav', 'at': a['at'], 'vol': 0.3} for a in aly if a['at'] > 0.5]
    c0 = main + 2.9
    sfx += [{'file': L + 'whoosh_1.wav', 'at': round(main - 0.1, 3), 'vol': 0.45}, {'file': L + 'typing.wav', 'at': round(c0 + 34 / 30, 3), 'vol': 0.45, 'dur': 0.9},
            {'file': L + 'pop_2.wav', 'at': round(c0 + 62 / 30, 3), 'vol': 0.55}, {'file': L + 'ding.wav', 'at': round(c0 + 84 / 30, 3), 'vol': 0.5}]
    sfx = [s for s in sfx if s['at'] < main + CTA_KEEP[1]]
    vlog, vI = build_voice(segs, (PJ + 'cta.mp4', CTA_KEEP[0], CTA_KEEP[1] - CTA_KEEP[0]), PUB / f'voice_{n}.wav')
    print('  voice gains dB per piece:', vlog, f'(before final gain {vI:.1f} LUFS)')
    dur = round(main + CTA_KEEP[1] - CTA_KEEP[0], 3)
    props = {'fps': 30, 'duration': dur, 'voice': PJ + f'voice_{n}.wav', 'segs': [{'src': 0, 'tl': 0, 'len': dur}], 'words': words,
             'aly': aly, 'scenes': scenes, 'sfx': sfx, 'tint': '#C3241C', 'look': 'cairo', 'capBottom': 0.1 if (not aly_v2 or BUBBLE_V2) else 0.05,
             'ctaVol': 0.0, 'sfxGain': 1.0, 'cta': {'file': PJ + 'cta.mp4', 'tl': round(main, 3), 'len': round(CTA_KEEP[1] - CTA_KEEP[0], 3), 'src': CTA_KEEP[0]},
             'ctaCue': {'at': 2.9, 'dur': round(CTA_KEEP[1] - 2.9, 3), 'props': {
                 'title': 'اكتب في *كومنت*', 'keyword': 'يوتيوب', 'dm': 'ده لينك الفيديو كامل 🗺️', 'typeAt': 34, 'sendAt': 62, 'dmAt': 84, 'top': 0.02}}}
    json.dump(props, open(PUB / f'short_{n}{"_" + V if V else ""}.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print(f'short {n}: {main:.1f}s + CTA {CTA_KEEP[1] - CTA_KEEP[0]:.1f}s | {len(scenes)} scenes, {len(aly)} Aly, {len(words)} words, {len(sfx)} sfx')


for n in [int(x) for x in sys.argv[1:]] or sorted(SPANS):
    build(n)

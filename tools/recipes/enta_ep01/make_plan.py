"""انت بتشتغل ايه — ep01 fnon (Ahmed Moataz, BIM / Technical Design). Motion pass on Aly's finished edit (17:44, 1080p60).
Nothing cut. His intro 0-17.0 and the intro again at the end 1046.7-end: no motion, no captions (plan.quiet).
One wide camera: Aly LEFT (x~0.2), guest RIGHT (x~0.76). Virtual camera = 'cut' zooms on whoever talks (speakers.json),
cards always on the side opposite the person in shot (wide shot -> centre). Show look = enta kit (docs/22).
Run: python work/scripts/make_plan.py -> work/plan.json"""
import json, random
from pathlib import Path

W = Path(__file__).resolve().parents[1]
P = 'projects/enta01/'
QUIET = [[0.0, 17.05], [1046.7, 1064.1]]
A0, A1 = 17.05, 1046.6
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
SENT = {s['id']: s for s in tr['sentences']}
spk = json.load(open(W / 'speakers.json', encoding='utf8'))
random.seed(7)


def T(sid, sub, k=0):
    """start of the k-th word in sentence sid that contains sub (raw Whisper text)."""
    hits = [w['start'] for w in SENT[sid]['words'] if sub in w['w']]
    assert len(hits) > k, (sid, sub)
    return hits[k]


def who(a, b):
    ws = [x for x in spk['words'] if a <= x[0] < b]
    if not ws: return 'W'
    g = sum(x[3] == 'G' for x in ws)
    return 'G' if g >= len(ws) / 2 else 'A'


cues, locks, boards = [], [], []


def add(t, at, dur, **props):
    cues.append({'t': t, 'src': round(at, 2), 'dur': round(dur, 2), 'props': props})


def sfx(at, name, vol=0.4):
    add('sfx', at, 2.0, name=name, volume=vol)


SIDE_X = {'right': 0.76, 'left': 0.24, 'center': 0.5}


def lock(at, dur, shot=None):
    s = shot or who(at, at + dur)
    locks.append((at - 0.15, at + dur, s))
    return {'A': 'right', 'G': 'left', 'W': 'center'}[s]


def term(at, dur, term, defn='', example='', exAt=None, en='', sticker='', accent='orange', paper='cream', pic='', shot=None):
    side = lock(at, dur, shot)
    add('enta_term', at, dur, term=term, defn=defn, example=example, exampleAt=int(((exAt or at + 1.5) - at) * 30), en=en,
        sticker=sticker, accent=accent, paper=paper, pic=pic, side=side, top=0.1 if side != 'center' else 0.08)
    cues[-1]['props']['def'] = cues[-1]['props'].pop('defn')
    sfx(at, 'swish', 0.35); sfx(at + 0.17, 'tape', 0.3)
    if example and exAt: sfx(exAt, 'pop_2', 0.3)


def photo(at, dur, src, caption='', sepia=False, pos='50% 40%', fit='cover', sticker='', w=560, h=0, shot=None, y=0.36, rot=-3):
    side = lock(at, dur, shot)
    add('enta_photos', at, dur, items=[dict(src=src, x=SIDE_X[side], y=y, w=w, h=h, at=0, rot=rot if side != 'left' else -rot,
                                            caption=caption, sepia=sepia, pos=pos, fit=fit, sticker=sticker)])
    sfx(at, 'shutter', 0.35)


def stick(at, items, dur=1.8):
    add('enta_stickers', at, dur, items=[dict(name=n, x=x, y=y, size=s, at=int(d * 30), rot=r) for n, x, y, s, d, r in items])
    for k, it in enumerate(items): sfx(at + it[4], ['pop_1', 'pop_2', 'pop_3'][k % 3], 0.3)


def bubble(at, dur, text, speaker='A'):
    side = lock(at, dur, speaker)
    x = 0.42 if speaker == 'A' else 0.58  # next to the head, inside the close-up
    add('enta_bubble', at, dur, text=text, x=x, y=0.13, tail='left' if speaker == 'A' else 'right', w=560)
    sfx(at, 'pop_3', 0.4)


def board(t, a, b, **props):
    boards.append((a - 0.3, b + 0.3))
    add(t, a, b - a, **props)
    add('enta_glitch', a - 0.1, 0.3, seed=int(a)); sfx(a - 0.1, 'glitch', 0.3); sfx(a, 'whoosh_2', 0.4)
    add('enta_glitch', b - 0.2, 0.3, seed=int(b)); sfx(b - 0.2, 'whoosh_1', 0.3)


def punch(at, dur=1.2, to=1.12):
    add('zoom', at, dur, style='punch', to=to)


F = lambda base, t: int(round((t - base) * 30))  # seconds -> frame inside a cue

# ---------------- opening: guest intro ----------------
a = T('S002', 'انا')
add('enta_name', a, 6.0, name='أحمد معتز شُرُش', role='مهندس معماري · *Technical Design*', side='right', accent='orange')
locks.append((a - 0.2, a + 6.0, 'W')); sfx(a, 'swoop_up', 0.45); sfx(a + 0.45, 'stamp', 0.3)
add('enta_leak', a - 0.3, 1.6, kind='leak_warm', x=0.85, y=0.5)
stick(T('S002', 'اسمي'), [('star_y', 0.33, 0.14, 120, 0, 10), ('spark_o', 0.42, 0.22, 90, 0.15, -8), ('spark_b', 0.27, 0.27, 80, 0.3, 0)])
punch(T('S002', 'اسمي'), 1.4)
term(T('S003', 'فنون'), 5.2, 'خريج *فنون جميلة*', 'قسم *عمارة*', sticker='brush', accent='mustard')
a = T('S003', 'خبرتي')
term(a, T('S004', 'وحالين') - a - 0.2, '*سنتين* خبرة', 'مكتب *استشاري* معماري', 'ديزاين ← بعدين *تكنيكال*', exAt=T('S003', 'تزاين'), accent='blue')
a = T('S004', 'بي')
term(a, 9.0, '*BIM* Architect', 'قسم الـ*Technical Design*', 'يعني *Technical Architect*', exAt=T('S005', 'تكنيكال'), en='Building Information Modeling',
     sticker='star8_b', accent='orange')
# "explain it like the old woman of our intro is asking" -> her picture from his intro + her question
a = T('S006', 'بتطلع')
photo(a, T('S008', 'اللي') - a, P + 'woman.jpg', 'الست بتاعة *المقدمة*', sepia=True, pos='30% 40%', sticker='qmark', w=480, h=400, shot='A')
add('enta_bubble', T('S008', 'بتسألك'), 3.0, text='يعني إيه *BIM*؟', x=0.6, y=0.12, tail='right', w=480); sfx(T('S008', 'بتسألك'), 'pop_3', 0.4)

# ---------------- the building pipeline (full-screen board) ----------------
a = T('S011', 'ديزاين') - 0.4; b = T('S016', 'للمقاول') + 0.9
board('enta_pipeline', a, b, title='المبنى بيعدّي على *مين*؟', hi=1, hiAt=F(a, T('S015', 'بتشغل')), hiText='هنا شغل *أحمد*',
      steps=[dict(pic=P + 'gem_facade.jpg', label='الديزاين', sub='شكل المبنى', at=F(a, T('S011', 'ديزاين'))),
             dict(pic=P + 'revit_ui.png', label='التكنيكال', sub='رسومات تنفيذية', at=F(a, T('S011', 'الرسمات'))),
             dict(pic=P + 'blueprint.jpg', label='المقاول', sub='بيستلم اللوح', at=F(a, T('S014', 'للمقاول'))),
             dict(pic=P + 'site.jpg', label='الموقع', sub='التنفيذ', at=F(a, T('S015', 'موقع')))],
      chips=[dict(text='كهربا', at=F(a, T('S012', 'كهربا'))), dict(text='ميكانيكا', at=F(a, T('S012', 'وميكانيكا'))),
             dict(text='HVAC', at=F(a, T('S012', 'واتشفاك'))), dict(text='خرسانة', at=F(a, T('S013', 'وخراسانة')))])
for s, k in (('S011', 'ديزاين'), ('S011', 'الرسمات'), ('S014', 'للمقاول'), ('S015', 'موقع')): sfx(T(s, k), 'pop_1', 0.35)
for s, k in (('S012', 'كهربا'), ('S012', 'وميكانيكا'), ('S012', 'واتشفاك'), ('S013', 'وخراسانة')): sfx(T(s, k), 'click', 0.35)
sfx(T('S015', 'بتشغل'), 'ding', 0.35)

a = T('S017', 'رسومات')
term(a, 8.5, 'رسومات *تنفيذية*', 'بتقول كل حاجة *فين* وتتعمل *إزاي*', 'الحيطان · المواسير · الواجهة', exAt=T('S018', 'مواسير'),
     en='Working Drawings', pic=P + 'blueprint.jpg', accent='blue')
# ---------------- facade ----------------
a = T('S021', 'فساد')
term(a, 8.0, '*Facade*', '= *الواجهة* ومعالجتها', 'تتركّب *إزاي* على المبنى؟', exAt=T('S022', 'معالجة'), en='Facade', sticker='spark_y', accent='olive')
stick(T('S024', 'فاهم'), [('qmark', 0.33, 0.12, 150, 0, 8)], 1.6); punch(T('S024', 'فاهم'), 1.3)
photo(T('S025', 'كرتنول'), 5.0, P + 'curtain.jpg', 'Curtain Wall = واجهة *إزاز*', pos='50% 30%', w=420, h=520, y=0.42)
a = T('S026', 'قلود')
photo(a, 3.0, 'logos/claude.svg', 'أهلًا 👋 أنا *Claude*', fit='contain', sticker='spark_o', w=300, h=300, rot=6, shot='A')
add('enta_glitch', a - 0.05, 0.25, seed=3, strength=0.7); sfx(a, 'magic', 0.35)
# ---------------- Grand Egyptian Museum ----------------
a = T('S033', 'المتحف')
photo(a, T('S036', 'الشكل', 1) - a - 0.2, P + 'gem_facade.jpg', 'المتحف المصري *الكبير*', w=620, h=420)
a = T('S036', 'الشكل', 1)
photo(a, 7.0, P + 'gem_wide.jpg', 'المثلثات دي هتتركّب *إزاي*؟', pos='40% 50%', w=620, h=420, rot=3)
a = T('S038', 'قابلة')
term(a, T('S043', 'العواميد') - a - 0.3, 'قابل *للتنفيذ*؟', 'رسمة حلوة ≠ مبنى *يتبني*', 'كل مسمار · كل قطعة · كل عمود', exAt=T('S042', 'مصمار'),
     sticker='burst', accent='orange')
photo(T('S043', 'كسمة'), 6.0, P + 'rebar.jpg', 'القسم *الإنشائي*', pos='50% 40%')
stick(T('S047', 'العمود'), [('qmark', 0.7, 0.12, 140, 0, 6), ('burst', 0.62, 0.2, 110, 0.2, -10)], 2.0); punch(T('S047', 'العمود'), 1.4)
stick(T('S050', 'يختلف', 1), [('spark_o', 0.68, 0.15, 100, 0, 0), ('star_y', 0.84, 0.12, 110, 0.15, 12)], 1.6)
# ---------------- departments ----------------
a = T('S056', 'ديزاين', 1)
term(a, T('S059', 'كوردينيت') - a - 0.3, 'الديزاين *خلص*؟', 'يروح للتكنيكال: معماري · إنشائي · ميكانيكا · كهربا', 'كل واحد *ماسك حتته*',
     exAt=T('S058', 'بيمسك'), accent='blue', paper='blue')
a = T('S059', 'كوردينيت')
term(a, 5.0, '*Coordination*', 'كل الأقسام *تتفق* مع بعض', en='Coordination', sticker='arrow_wave', accent='olive')
a = T('S061', 'الكهرباء')
term(a, T('S066', 'وكوردنيشن') - a, 'كل قسم *عايز مكان*', 'الكهربا: أوضة هنا · الميكانيكا: أوضة *موتور* في البيزمنت',
     'نشيل *كام ركنة* 🚗', exAt=T('S066', 'كاميراكنا'), accent='mustard')
a = T('S072', 'جمالي')
term(a, 8.0, 'المعماري مسؤول عن *إيه*؟', 'شكل *جمالي* + المبنى *شغّال*', sticker='spark_g', accent='orange')
a = T('S076', 'كود')
term(a, T('S080', 'داد') - a - 0.8, '*الكود*', 'قوانين لازم المبنى يمشي عليها', 'زي كود *الحريق* 🔥', exAt=T('S079', 'الحريق'),
     en='Building Code', accent='orange', paper='blue')
a = T('S080', 'داد') - 0.3; b = T('S085', 'اصلا') + 0.4
board('enta_deadend', a, b, title='كود الحريق: *Dead End*', walkAt=F(a, T('S081', 'تجري')), wallAt=F(a, T('S081', 'حيطة')),
      ruleAt=F(a, T('S082', 'تسعة')), stampAt=F(a, T('S084', 'رخصة')), rule='مايزيدش عن *9 متر*', stamp='مفيش رخصة')
sfx(T('S081', 'تجري'), 'swish', 0.3); sfx(T('S081', 'حيطة'), 'impact', 0.45); sfx(T('S082', 'تسعة'), 'tick', 0.35)
sfx(T('S084', 'رخصة'), 'stamp', 0.5)
a = T('S087', 'الصورة')
term(a, 8.0, 'الصورة *الكبيرة*', 'المعماري بيربط: الأقسام + الديزاين + *الأكواد*', sticker='spark_y', accent='mustard')
a = T('S093', 'بيبدأ')
stick(a, [('arrow_y', 0.72, 0.18, 150, 0, 0), ('arrow_b', 0.86, 0.3, 130, 0.6, 10)], 2.4)
a = T('S097', 'مكتب')
term(a, 9.0, 'مكتب *استشاري*', 'فيه كل الأقسام', 'ميكانيكا · كهربا · إنشائي · معماري', exAt=T('S099', 'ميكانيكا'), accent='blue')
# ---------------- a day at work: restaurants below, offices above -> exhaust duct clash ----------------
a = T('S102', 'مبدأ')
term(a, T('S104', 'مدخانة') - a - 0.3, 'مثال: *مبنى*', 'تحت *مطاعم* · فوق *مكاتب / سكني*', sticker='floppy' if False else 'star_line', accent='olive')
a = T('S104', 'مدخانة')
term(a, T('S107', 'داقطات') - a - 0.2, '*Shaft*', 'فتحة طالعة لفوق تشفط *الهوا*', 'زي مدخنة / ملقف هوا', exAt=T('S106', 'ملقى'), en='Shaft', accent='orange')
photo(T('S107', 'داقطات'), 4.6, P + 'ducts.jpg', '*Ducts*: مجاري الهوا', pos='50% 40%')
a = T('S108', 'ميكانيكي') - 0.3; b = T('S114', 'مشاكل') + 0.5
board('enta_clash', a, b, title='*تعارض* بين الأقسام', ductAt=F(a, T('S108', 'هحتاج')), clashAt=F(a, T('S109', 'هيكلش')),
      fixAt=F(a, T('S111', 'امسك')), floors=['مكاتب / سكني', 'مكاتب / سكني', 'مطاعم', 'بيزمنت'],
      clashText='الدكت طالع *في نص الفراغ*!', fixText='نمشّيه في سقف *الكوريدور*')
sfx(T('S109', 'هيكلش'), 'buzz_wrong', 0.4); sfx(T('S111', 'امسك'), 'swoop_up', 0.35); sfx(T('S112', 'كوريدور'), 'ding', 0.35)
photo(T('S115', 'سلالم'), 6.0, P + 'blueprint.jpg', 'لوح *السلالم* والأسانسيرات', pos='50% 30%', w=440, h=520, y=0.42)
stick(T('S118', 'علامة'), [('arrow_wave', 0.74, 0.2, 170, 0, 0)], 2.0)
photo(T('S121', 'الهندريل'), 6.5, P + 'handrail_dwg.jpg', 'تفصيلة الـ*Handrail*', sepia=True, pos='50% 45%', w=440, h=520, y=0.42)
a = T('S123', 'بريفرنس')
term(a, 6.0, 'رقم *Reference*', 'العلامة بتوديك على لوحة *التفصيلة*', en='Detail Reference', sticker='arrow_g', accent='blue')
# ---------------- engineering or fine arts? ----------------
bubble(T('S127', 'هندسة'), 3.0, 'هندسة ولا *فنون*؟')
stick(T('S129', 'ابعد', 1), [('masks', 0.3, 0.14, 170, 0, -6), ('brush', 0.42, 0.2, 120, 0.3, 10)], 2.2)
a = T('S136', 'احسن')
term(a, 6.0, 'فنون جميلة *عمارة*', 'من أحسن الكليات اللي *بتعلّم*', sticker='masks', accent='mustard')
a = T('S138', 'ووركينج')
term(a, 7.0, 'مادة *Working*', 'بنطلّع الرسومات التنفيذية *من الكلية*', 'السلم · الكود · التفاصيل', exAt=T('S140', 'والسلم'), accent='olive')
# ---------------- AI ----------------
bubble(T('S142', 'اوي'), 3.0, 'الـ*AI* دخل شغلك؟')
stick(T('S142', 'جدا'), [('spark_y', 0.66, 0.12, 110, 0, 0), ('star8_b', 0.8, 0.2, 100, 0.15, 0)], 1.6)
a = T('S145', 'حل')
term(a, T('S148', 'مفوش') - a, 'الـ*AI* في التكنيكال', 'معلومات + *حل مشاكل*', 'لسه مش بأعلى *كواليتي*', exAt=T('S147', 'كواليتي'), sticker='spark_b', accent='blue')
a = T('S157', 'سكيتشي') - 0.8; b = T('S163', 'دولت')
board('enta_render', a, b, title='رندر بالـ*AI*', sketch=P + 'sketch.jpg', color=P + 'sketch_color.jpg', render=P + 'render.jpg',
      colorAt=F(a, T('S158', 'احمر')), renderAt=F(a, T('S160', 'رندر')), nightAt=F(a, T('S161', 'نايت')), vsAt=F(a, T('S162', 'سبع')),
      prompts=[dict(text='Render this sketch', at=F(a, T('S160', 'يطلع'))), dict(text='Change the wall material', at=F(a, T('S160', 'المتريل'))),
               dict(text='Night shot', at=F(a, T('S161', 'نايت')))], before='7-8 *ساعات*', after='*ثواني*')
sfx(T('S158', 'احمر'), 'paper', 0.35); sfx(T('S160', 'يطلع'), 'typing', 0.3); sfx(T('S160', 'رندر'), 'magic', 0.35)
sfx(T('S160', 'المتريل'), 'typing', 0.3); sfx(T('S161', 'نايت'), 'swoop_down', 0.35); sfx(T('S162', 'سبع'), 'clock', 0.3)
a = T('S165', 'اسبوعين')
term(a, 5.0, 'شغل *أسبوعين*', 'واحد بالـAI يخلّصه في *يوم*', sticker='spark_o', accent='olive')
bubble(T('S166', 'يوصل'), 3.0, 'توصلها *إزاي*؟')
a = T('S168', 'هندسة')
term(a, 7.0, 'تدخلها *إزاي*؟', 'هندسة عمارة *أو* فنون عمارة', sticker='qmark', accent='orange')
a = T('S173', 'روح')
term(a, 4.5, 'قدّم *على طول* ✔', 'مش محتاج تذاكر حاجة زيادة', accent='olive')
stick(T('S175', 'لا'), [('qmark', 0.7, 0.13, 140, 0, -6)], 1.6); punch(T('S175', 'لا'), 1.3)
# ---------------- BIM ----------------
photo(T('S183', 'الموقع'), 5.0, P + 'site.jpg', 'المشكلة تظهر في *الموقع* 😬', pos='50% 50%')
stick(T('S184', 'كارسية'), [('burst', 0.3, 0.16, 150, 0, 0), ('qmark', 0.4, 0.1, 120, 0.15, 10)], 1.8)
punch(T('S184', 'كارسية'), 1.4, 1.15)
a = T('S186', 'مودلت') - 0.3; b = T('S190', 'الواقع') + 0.3
board('enta_merge', a, b, title='*BIM*: كل قسم عامل موديل على *Revit*',
      models=[dict(label='معماري', at=F(a, T('S186', 'عامل'))), dict(label='ميكانيكا', at=F(a, T('S187', 'والميكانيك'))),
              dict(label='إنشائي', at=F(a, T('S187', 'والاستروكش')))],
      mergeAt=F(a, T('S188', 'فبندخل')), reportAt=F(a, T('S189', 'تلاش')))
for s, k in (('S186', 'عامل'), ('S187', 'والميكانيك'), ('S187', 'والاستروكش')): sfx(T(s, k), 'swish', 0.3)
sfx(T('S188', 'فبندخل'), 'impact', 0.4); sfx(T('S188', 'فبندخل') + 1.0, 'buzz_wrong', 0.3); sfx(T('S189', 'تلاش'), 'printer', 0.3)
photo(T('S190', 'الواقع'), 3.0, 'logos/autodeskrevit.svg', '*Revit*', fit='contain', w=260, h=260, rot=5)
a = T('S191', 'ابعاد')
term(a, T('S196', 'بتتفق') - a, 'أبعاد الـ*BIM*', 'من أول المشروع لحد ما *يتسلّم*', 'مفيش حاجة *تفاجئك* في الموقع', exAt=T('S195', 'هتتفاجئ'),
     sticker='star8_b', accent='blue', paper='blue')
# ---------------- future ----------------
bubble(T('S202', 'مستقبلها'), 3.2, 'هتتغيّر بالـ*AI*؟')
stick(T('S203', 'طبعا'), [('burst', 0.68, 0.14, 140, 0, 0)], 1.4)
a = T('S210', 'بلان')
term(a, T('S213', 'الديزاينر') - a - 0.3, 'من *Plan* ← *Model*', 'الـAI بيطلّعه لوحده', '(لسه فيه *غلطات* كتير)', exAt=T('S212', 'غرضات'), accent='olive')
a = T('S213', 'الديزاينر')
term(a, T('S216', 'زي') - a, 'كمان *سنتين*؟', 'الـAI يصمم: الأرض + الكود + الـConstraints', 'وإحنا *نتفرّج* 🍿', exAt=T('S216', 'نتفرج'),
     sticker='spark_o', accent='orange')
a = T('S216', 'شكرا')
stick(a, [('star_y', 0.3, 0.12, 130, 0, 10), ('onair', 0.5, 0.08, 220, 0.2, -6), ('star8_b', 0.7, 0.13, 110, 0.4, 0)], 3.0)
add('enta_leak', a, 2.0, kind='leak_warm', x=0.5, y=0.3)
a = T('S217', 'اول')
photo(a, 4.0, P + 'logo_fnon.png', 'أول *حلقة* 🎬', fit='contain', w=520, h=300, shot='W', y=0.34)

# ---------------- virtual camera ----------------
CLOSE, MED, LOCK = 1.6, 1.3, 1.45
ORIG = {'A': (0.0, 0.3), 'G': (1.0, 0.33)}
grid = []  # 0.1 s cells: shot letter
t = A0
turns = [tt for tt in spk['turns'] if tt[1] > A0 and tt[0] < A1]
while t < A1:
    grid.append(None); t += 0.1
def cell(x): return int(round((x - A0) * 10))
# 1) speaker turns
for s, e, sp in turns:
    for i in range(max(0, cell(s + 0.15)), min(len(grid), cell(e + 0.3))):
        grid[i] = sp
# 2) short turns (< 1.6 s) -> wide
i = 0
while i < len(grid):
    j = i
    while j < len(grid) and grid[j] == grid[i]: j += 1
    if (j - i) < 16 and grid[i] in ('A', 'G'):
        for k in range(i, j): grid[k] = 'W'
    i = j
# 3) build shots, long ones split into close / medium / wide / close (pacing ~1 change every 2-4 s)
shots, i = [], 0
while i < len(grid):
    j = i
    while j < len(grid) and grid[j] == grid[i]: j += 1
    shots.append([A0 + i / 10, A0 + j / 10, grid[i] or 'W']); i = j
out = []
for s, e, sp in shots:
    if e - s < 4.5:
        out.append([s, e, sp, CLOSE if sp != 'W' else 1.0]); continue
    pat = [CLOSE, MED, 1.0, CLOSE, MED] if sp != 'W' else [1.0, 'A', 1.0, 'G']  # wide stretches: peek at each person
    x, k = s, 0
    while x < e - 0.1:
        seg = min(e, x + random.uniform(2.2, 3.4))
        if e - seg < 2.0: seg = e
        z = pat[k % len(pat)]
        out.append([x, seg, z, MED] if isinstance(z, str) else [x, seg, sp, z]); x = seg; k += 1
# 4) locks (cards opposite the person) override; boards -> wide
def apply(a, b, sp, z):
    res = []
    for s, e, p, zz in out:
        if e <= a or s >= b: res.append([s, e, p, zz]); continue
        if s < a: res.append([s, a, p, zz])
        if e > b: res.append([b, e, p, zz])
    res.append([a, b, sp, z]); res.sort(key=lambda x: x[0]); return res
for a, b, sp in locks: out = apply(max(A0, a), min(A1, b), sp, LOCK if sp != 'W' else 1.0)
for a, b in boards: out = apply(a, b, 'W', 1.0)
# 5) merge same + absorb tiny shots
merged = []
for s, e, p, z in out:
    if e - s < 0.05: continue
    if merged and merged[-1][2] == p and merged[-1][3] == z and s - merged[-1][1] < 0.05: merged[-1][1] = e
    elif merged and e - s < 1.2: merged[-1][1] = e
    else: merged.append([s, e, p, z])
n_cut = 0
for k, (s, e, p, z) in enumerate(merged):
    if p != 'W' and z > 1.01:
        ox, oy = ORIG[p]
        add('zoom', s, e - s, style='cut', to=z, x=ox, y=oy)
    if k and not any(a - 0.5 < s < b + 0.5 for a, b in boards):
        n_cut += 1
        if n_cut % 7 == 0: add('enta_glitch', s - 0.08, 0.25, seed=k, strength=0.6); sfx(s - 0.08, 'glitch', 0.2)

# fillers: no stretch > 4 s without a card on screen or a camera change -> slow push
def holes():
    ev = sorted([c['src'] for c in cues if c['t'] == 'zoom'] + [m[0] for m in merged])
    cov = sorted((c['src'], c['src'] + c['dur']) for c in cues if c['t'] not in ('sfx', 'zoom', 'enta_glitch', 'enta_leak'))
    pts = sorted(set(ev + [x for ab in cov for x in ab] + [A0, A1]))
    res = []
    for a, b in zip(pts, pts[1:]):
        mid = (a + b) / 2
        if b - a > 4 and not any(x <= mid < y for x, y in cov): res.append((a, b))
    return res
for a, b in holes():
    x = a + 1.5
    while x < b - 1.5:
        add('zoom', x, 2.2, style='push', to=1.08); x += 3.5
cues.sort(key=lambda c: c['src'])
plan = {'cut': False, 'pack': 'charcoal', 'quiet': QUIET, 'fix': json.load(open(W / 'fix.json', encoding='utf8')), 'cues': cues}
json.dump(plan, open(W / 'plan.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
gaps = [(round(a, 1), round(b - a, 1)) for a, b in holes()]
print(len(cues), 'cues;', len(merged), 'shots; avg shot', round((A1 - A0) / len(merged), 2), 's; gaps > 5 s:', gaps)

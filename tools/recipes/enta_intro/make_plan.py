"""انت بتشتغل ايه — show intro video (Aly alone on the couch, 4:23, 1080p60, 2026-10-16). Motion pass on his video:
nothing cut, no intro/outro added, no captions (long video) -> bottom notes. Show look = enta kit (docs/22), shared stickers only.
Aly's asks: the files screenshot (dates 2023) when he says he made the intro back then; when he names the CS ("graphics")
and the fnon intros -> the intros as muted pictures on the side, a teaser only (not the whole intro).
Run: python work/scripts/make_plan.py -> work/plan.json ; build with the project code 'enta00' (junction, see docs/22)."""
import json, random
from pathlib import Path

W = Path(__file__).resolve().parents[1]
P = 'projects/enta00/'
A0, A1 = 0.0, 263.5
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
SENT = {s['id']: s for s in tr['sentences']}
random.seed(5)


def T(sid, sub, k=0):
    hits = [w['start'] for w in SENT[sid]['words'] if sub in w['w']]
    assert len(hits) > k, (sid, sub)
    return hits[k]


cues, locks, boards = [], [], []
F = lambda base, t: int(round((t - base) * 30))


def add(t, at, dur, **props):
    cues.append({'t': t, 'src': round(at, 2), 'dur': round(dur, 2), 'props': props})


def sfx(at, name, vol=0.4):
    add('sfx', at, 2.0, name=name, volume=vol)


def lock(at, dur, shot='R'):  # R = Aly pushed left (card on the right), W = wide
    locks.append((at - 0.15, at + dur, shot))


def term(at, dur, term, defn='', example='', exAt=None, en='', sticker='', accent='orange', paper='cream'):
    lock(at, dur)
    add('enta_term', at, dur, term=term, example=example, exampleAt=int(((exAt or at + 1.5) - at) * 30), en=en,
        sticker=sticker, accent=accent, paper=paper, pic='', side='right', top=0.1)
    cues[-1]['props']['def'] = defn
    sfx(at, 'swish', 0.35); sfx(at + 0.17, 'tape', 0.3)
    if example and exAt: sfx(exAt, 'pop_2', 0.3)


def photos(at, dur, items, shot='R', snd='shutter'):
    lock(at, dur, shot)
    add('enta_photos', at, dur, items=[dict(dict(x=0.76, y=0.36, w=520, h=0, at=0, rot=-3, caption='', sepia=False, pos='50% 40%',
                                                 fit='cover', sticker='', start=0, bare=False), **it) for it in items])
    for it in items: sfx(at + it.get('at', 0) / 30, snd, 0.35)


def stick(at, items, dur=1.8):
    add('enta_stickers', at, dur, items=[dict(name=n, x=x, y=y, size=s, at=int(d * 30), rot=r) for n, x, y, s, d, r in items])
    for k, it in enumerate(items): sfx(at + it[4], ['pop_1', 'pop_2', 'pop_3'][k % 3], 0.3)


def bubble(at, dur, text):
    lock(at, dur, 'M')
    add('enta_bubble', at, dur, text=text, x=0.67, y=0.12, tail='left', w=520)
    sfx(at, 'pop_3', 0.4)


def board(t, a, b, **props):
    boards.append((a - 0.3, b + 0.3))
    add(t, a, b - a, **props)
    add('enta_glitch', a - 0.1, 0.3, seed=int(a)); sfx(a - 0.1, 'glitch', 0.3); sfx(a, 'whoosh_2', 0.4)
    add('enta_glitch', b - 0.2, 0.3, seed=int(b)); sfx(b - 0.2, 'whoosh_1', 0.3)


def note(at, text, sticker='', d=4.5, accent='orange'):
    add('enta_note', at, d, text=text, sticker=sticker, side='center', accent=accent); sfx(at, 'paper', 0.3)


def punch(at, dur=1.2, to=1.1):
    add('zoom', at, dur, style='punch', to=to, x=0.45, y=0.3)


# ---------------- hello ----------------
a = T('S001', 'عاملين')
add('enta_name', a - 0.3, 3.2, name='علي معتز شُرُش', role='مقدّم *انت بتشتغل ايه*', side='right', accent='orange')
lock(a - 0.3, 3.2, 'W'); sfx(a - 0.3, 'swoop_up', 0.45); sfx(a + 0.15, 'stamp', 0.3)
note(T('S002', 'ارتجال'), 'فيديو *ارتجال* · من غير مونتاج', accent='mustard')
stick(T('S002', 'يلا'), [('spark_o', 0.62, 0.16, 100, 0, 0), ('star_y', 0.7, 0.26, 80, 0.15, 10)], 1.6)
# new show + its two logos
a = T('S003', 'برنامج')
photos(a, T('S004', 'اول') - a - 0.1, [dict(src=P + 'logo_cs_trim.png', x=0.68, y=0.36, w=330, h=333, fit='contain', bare=True, rot=-4),
                                       dict(src=P + 'logo_fnon_trim.png', x=0.87, y=0.42, w=330, h=333, fit='contain', bare=True, rot=4, at=12)], snd='pop_1')
sfx(a, 'swoop_up', 0.35)
a = T('S004', 'اول')
term(a, T('S004', 'وما') - a, 'أول حلقة: *النهاردة*', 'الساعة *4* إن شاء الله', sticker='onair', accent='orange')
note(T('S004', 'صورتش'), 'صوّرت *حلقة واحدة* بس', accent='blue')
a = T('S005', 'البرنامج')
term(a, T('S007', 'والبرنامج') - a - 0.1, 'الفكرة من *4 سنين*', 'وكنت عامل *الانترو* كمان', exAt=T('S006', 'الانترو'), sticker='star8_b', accent='mustard')
# ---------------- name + 3 flavours ----------------
a = T('S007', 'انت')
bubble(a - 0.2, T('S007', 'الفليفر') - a + 0.1, 'انت بتشتغل *ايه*؟')
a = T('S007', 'الاولاني')
term(a, T('S008', 'من') - a + 0.9, 'الحلقة = *انترفيو*', 'مع ضيف *من مجاله*', sticker='qmark', accent='blue', paper='blue')
a = T('S008', 'مجال') - 0.3; b = T('S010', 'كان', 1) + 1.0
board('enta_flavours', a, b, title='انت بتشتغل ايه؟ *3 أنواع* ضيوف',
      items=[dict(pic=P + 'logo_cs_trim.png', label='حاسبات', sub='Computer Science', at=F(a, T('S008', 'الكمبيوتر')), fit='contain', accent='blue', chips=[]),
             dict(pic=P + 'logo_fnon_trim.png', label='فنون', sub='مجالات الفن', at=F(a, T('S009', 'الفنون')), fit='contain', accent='orange', chips=[]),
             dict(pic=P + 'workshop.jpg', label='أصحاب أعمال', sub='', at=F(a, T('S009', 'اصحاب')), fit='cover', accent='olive',
                  chips=[dict(text='شركة', at=F(a, T('S010', 'شركة'))), dict(text='ورشة', at=F(a, T('S010', 'ورشة'))), dict(text='مصنع', at=F(a, T('S010', 'مصنع')))])])
for s, k in (('S008', 'الكمبيوتر'), ('S009', 'الفنون'), ('S009', 'اصحاب')): sfx(T(s, k), 'pop_1', 0.4)
for k in ('شركة', 'ورشة', 'مصنع'): sfx(T('S010', k), 'click', 0.35)
# ---------------- 2023: the files screenshot (dates) ----------------
a = T('S010', 'تقريبا')
photos(a, T('S012', 'الانترو') - a - 0.2, items=[dict(src=P + 'files_2023.png', x=0.765, y=0.36, w=706, h=318, rot=-2, pos='50% 50%',
                                                 caption='ملفات البرنامج: *2023*', sticker='star_y')])
note(T('S011', 'ثلاثة'), 'من حوالي *3 سنين ونص*', accent='olive')
# ---------------- his two intros: teasers on both sides, muted ----------------
a = T('S012', 'الانترو') - 0.1; b = T('S015', 'الانترو') - 0.2
photos(a, b - a, [dict(src=P + 'intro_cs.mp4', x=0.145, y=0.37, w=470, h=264, rot=-3, start=0.8, caption='انترو *حاسبات*', pos='50% 50%'),
                  dict(src=P + 'intro_fnon.mp4', x=0.855, y=0.37, w=470, h=264, rot=3, start=0.0, at=F(a, T('S013', 'الفنون')), caption='انترو *فنون*', pos='50% 50%')],
       shot='W', snd='projector')
note(T('S014', 'للناس'), 'خدت *رأي* القريبين مني', accent='blue')
a = T('S015', 'الانترو')
photos(a, T('S015', 'فهو') - a, [dict(src=P + 'intro_cs.mp4', x=0.75, y=0.36, w=560, h=315, rot=-3, start=7.4, caption='كنت *بتفرج عليها* كتير', sticker='spark_o', pos='50% 50%')],
       snd='projector')
# ---------------- 4 years, why ----------------
a = T('S016', 'تخرج')
term(a, T('S018', 'ليه') - a - 0.1, 'عمر البرنامج: *4 سنين*', 'وعدد الحلقات… *0*', exAt=T('S018', 'وكم'), sticker='qmark', accent='orange')
punch(T('S017', 'لزيز'), 1.1)
bubble(T('S018', 'ليه'), 0.85, '*ليه*؟')
a = T('S018', 'اول')
term(a, T('S019', 'اعمل') - a - 0.1, 'السبب *الأول*', 'مفيش *وقت* خالص', sticker='spark_y', accent='mustard')
a = T('S019', 'اعمل')
photos(a, T('S019', 'وبما') - a - 0.1, [dict(src=P + 'camera.jpg', x=0.67, y=0.33, w=330, h=250, rot=-4, caption='تصوير', pos='50% 50%'),
                                        dict(src=P + 'premiere-pro-official.png', x=0.82, y=0.31, w=190, h=190, fit='contain', bare=True, rot=4, at=F(a, T('S019', 'ومنتجه')), caption='مونتاج'),
                                        dict(src=P + 'youtube-icon.svg', x=0.935, y=0.33, w=180, h=180, fit='contain', bare=True, rot=-3, at=F(a, T('S019', 'وارفع')), caption='رفع')])
note(T('S019', 'مرهق'), 'كل ده لوحدي = *مرهق جدًا*', sticker='burst', accent='orange')
punch(T('S019', 'مرهق'), 1.3, 1.12)
a = T('S019', 'وبما') + 0.7  # 'في كلود' (Whisper: 'في' only)
photos(a, T('S020', 'والمشكلة') - a - 0.1, [dict(src=P + 'claude.svg', x=0.76, y=0.34, w=300, h=300, fit='contain', bare=True, rot=5, caption='دلوقتي فيه *Claude*', sticker='spark_o')], snd='pop_1')
sfx(a, 'magic', 0.35)
a = T('S020', 'والمشكلة')
term(a, T('S022', 'لو') - a - 0.1, 'السبب *التاني*', 'مش أنا بس… *الضيوف* كمان', sticker='star_line', accent='blue', paper='blue')
bubble(T('S022', 'لو'), T('S023', 'وفي') - T('S022', 'لو'), 'لو حصلت *مشكلة*؟')
sfx(T('S022', 'المونتاج'), 'buzz_wrong', 0.25)
stick(T('S023', 'متضايق'), [('qmark', 0.62, 0.14, 120, 0, 8)], 1.4)
note(T('S023', 'لان'), 'كنت عايز فيديوهات *حلوة*', accent='olive')
a = T('S024', 'لان')
term(a, T('S026', 'بس') - a - 0.1, 'أعرف ناس *كتير*', 'في كل الأنواع', 'حاسبات · فنون · شركات · *العيلة*', exAt=T('S025', 'كاصحاب'), sticker='star_y', accent='olive')
bubble(T('S026', 'ما'), T('S027', 'فقلت') - T('S026', 'ما') - 0.1, 'معنديش *الجرأة*')
punch(T('S027', 'الجرأة'), 1.2, 1.1)
a = T('S027', 'فقلت')
term(a, T('S029', 'اه') - a - 0.1, 'أبدأ *خفيف*', 'ولو اتشجعت: ناس *أكتر*', 'وناس *أكبر*', exAt=T('S029', 'اكبر'), sticker='spark_g', accent='mustard')
# ---------------- the drawer: 2023 -> today ----------------
a = T('S029', 'فعلى') - 0.3; b = T('S033', 'اه') + 0.4
board('enta_drawer', a, b, items=[P + 'logo_cs_trim.png', P + 'logo_fnon_trim.png'], hero=P + 'logo_fnon_trim.png',
      closeAt=F(a, T('S029', 'مركونا')), years=[dict(y=2023, at=0), dict(y=2024, at=F(a, T('S030', 'تلات'))), dict(y=2025, at=F(a, T('S030', 'اربع'))),
                                               dict(y=2026, at=F(a, T('S030', 'هبتدي')))],
      openAt=F(a, T('S030', 'اول')), jumpAt=F(a, T('S031', 'النهاردة')),
      text1='اللوجو + الانترو *جاهزين*', text2='في *الدرج*… 3-4 سنين', text3='أول حلقة *النهاردة*', text4='الفكرة *طلعت من الدرج*', t4At=F(a, T('S032', 'الفكرة')))
sfx(T('S029', 'مركونا'), 'door_slam', 0.3)
for k in ('تلات', 'اربع'): sfx(T('S030', k), 'tick', 0.35)
sfx(T('S030', 'هبتدي'), 'tock', 0.35); sfx(T('S030', 'اول'), 'rustle', 0.35); sfx(T('S031', 'النهاردة'), 'swoop_up', 0.45); sfx(T('S031', 'النهاردة') + 0.35, 'ding', 0.35)
# ---------------- proof of concept + intro again ----------------
a = T('S033', 'البروف')
term(a, T('S033', 'والانترو', 1) - a - 0.1, '*Proof of Concept*', 'تجربة أولى تثبت إن الفكرة *تنفع*', en='Proof of Concept', sticker='star8_b', accent='blue')
a = T('S033', 'والانترو', 1)
photos(a, T('S034', 'برنامج') - a - 0.2, [dict(src=P + 'intro_fnon.mp4', x=0.75, y=0.36, w=560, h=315, rot=3, start=5.0, caption='الانترو *ظهرت*', sticker='star_y', pos='50% 50%')],
       snd='projector')
a = T('S034', 'برنامج')
photos(a, T('S035', 'بس') - a, [dict(src=P + 'logo_fnon_trim.png', x=0.76, y=0.36, w=380, h=384, fit='contain', bare=True, rot=-3, caption='أول حلقة: *فنون*')], snd='pop_1')
stick(T('S035', 'الفنون'), [('onair', 0.6, 0.12, 180, 0, -6)], 2.0)
note(T('S035', 'حلقة', 0) + 0.4, 'الحلقة الجاية *أحسن وأحسن*', accent='mustard')
stick(T('S036', 'واحسن', 1), [('star_y', 0.64, 0.14, 90, 0, 0), ('spark_b', 0.72, 0.22, 80, 0.15, 0), ('star8_b', 0.8, 0.14, 80, 0.3, 0)], 2.0)
note(T('S036', 'برضو', 1), 'من *3 سنين*: شكل الفيديو', accent='blue')
# ---------------- the old look (2023 designs) + intro/logo unchanged ----------------
a = T('S037', 'ديزاين')
photos(a, T('S038', 'الانترو') - a - 0.1, [dict(src=P + 'design_2023a.jpg', x=0.72, y=0.3, w=520, h=292, rot=-4, caption='', pos='50% 50%'),
                                            dict(src=P + 'design_2023b.jpg', x=0.8, y=0.62, w=520, h=292, rot=4, at=F(a, T('S037', 'الفيديو')), caption='ديزاين *2023*', pos='50% 50%')])
a = T('S038', 'الانترو')
photos(a, T('S039', 'وما') - a - 0.1, [dict(src=P + 'intro_cs.mp4', x=0.72, y=0.33, w=500, h=281, rot=-3, start=9.6, caption='الانترو *زي ما هي*', pos='50% 50%'),
                                        dict(src=P + 'logo_fnon_trim.png', x=0.88, y=0.66, w=250, h=253, fit='contain', bare=True, rot=5, at=F(a, T('S039', 'واللوجو')))])
# ---------------- before the AI era: all by hand ----------------
a = T('S039', 'قبل')
term(a, T('S040', 'المونتاج') - a - 0.1, 'قبل عصر *الـAI*', 'كله كان *بإيدي*', sticker='spark_o', accent='orange')
a = T('S040', 'المونتاج')
photos(a, T('S041', 'الحاجات') - a - 0.1, [dict(src=P + 'premiere-pro-official.png', x=0.62, y=0.34, w=210, h=210, fit='contain', bare=True, rot=-4, caption='مونتاج'),
                                            dict(src=P + 'after_effects.png', x=0.77, y=0.34, w=210, h=205, fit='contain', bare=True, rot=4, at=F(a, T('S040', 'والموشن')), caption='موشن'),
                                            dict(src=P + 'illustrator.png', x=0.91, y=0.34, w=200, h=200, fit='contain', bare=True, rot=-3, at=F(a, T('S041', 'والاستريتور')), caption='لوجو')],
       snd='pop_1')
note(T('S040', 'اليدوي'), 'موشن ولوجو *يدوي*', accent='mustard')
bubble(T('S041', 'الحاجات'), T('S041', 'فحبيت') - T('S041', 'الحاجات'), 'الحاجات دي *وحشاني*')
a = T('S041', 'فحبيت')
term(a, T('S042', 'حتى') - a, '*توثيق* للحظة دي', 'فيديو قبل أول حلقة', sticker='onair', accent='blue', paper='blue')
note(T('S043', 'بحلقة') - 0.2, 'حتى لو *حلقة · حلقتين · تلاتة*', accent='olive')
stick(T('S043', 'نكمل'), [('star_y', 0.64, 0.14, 100, 0, 0), ('spark_o', 0.74, 0.22, 90, 0.2, 0)], 1.8)
# ---------------- thanks ----------------
a = T('S044', 'وشكرا')
note(a + 0.6, 'جمعة *مباركة*', sticker='star8_b', accent='mustard')
add('enta_leak', a, 2.0, kind='leak_warm', x=0.5, y=0.3)
a = T('S044', 'والسلام')
photos(a, A1 - a - 0.05, [dict(src=P + 'logo_cs_trim.png', x=0.68, y=0.36, w=300, h=303, fit='contain', bare=True, rot=-4),
                          dict(src=P + 'logo_fnon_trim.png', x=0.86, y=0.42, w=300, h=303, fit='contain', bare=True, rot=4, at=8)], snd='pop_1')

# ---------------- virtual camera (single person, calm; ep01 lessons: less zoom, never the same zoom twice in a row) ----------------
MED, CLOSE = 1.25, 1.4
FREE = (0.45, 0.3)   # zoom on his face, he stays in the middle
PUSH = (0.95, 0.3)   # card on the right: he moves to ~0.33
shots, t, k = [], 2.0, 0
pat = [1.0, MED, 1.0, CLOSE]
while t < A1:
    e = min(A1, t + random.uniform(3.4, 5.2) * (1.3 if t < 40 else 1.0))
    if A1 - e < 2.5: e = A1
    z = pat[k % 4] if t > 12 else (1.0 if k % 2 == 0 else MED)
    shots.append([t, e, 'F', z]); t = e; k += 1
shots.insert(0, [0.0, 2.0, 'F', 1.0])


def apply(a, b, p, z):
    res = []
    for s, e, pp, zz in shots:
        if e <= a or s >= b: res.append([s, e, pp, zz]); continue
        if s < a: res.append([s, a, pp, zz])
        if e > b: res.append([b, e, pp, zz])
    res.append([a, b, p, z]); res.sort(key=lambda x: x[0]); return res


for a, b, s in sorted(locks):
    shots = apply(max(0, a), min(A1, b), {'R': 'P', 'W': 'F', 'M': 'F'}[s], {'R': MED, 'W': 1.0, 'M': MED}[s])
for a, b in boards: shots = apply(a, b, 'F', 1.0)
merged = []
for s, e, p, z in shots:
    if e - s < 0.05: continue
    if merged and merged[-1][2] == p and merged[-1][3] == z and s - merged[-1][1] < 0.05: merged[-1][1] = e
    elif merged and e - s < 1.2: merged[-1][1] = e
    else: merged.append([s, e, p, z])
n_cut = 0
for i, (s, e, p, z) in enumerate(merged):
    if z > 1.01:
        ox, oy = PUSH if p == 'P' else FREE
        add('zoom', s, e - s, style='cut', to=z, x=ox, y=oy)
    if i and not any(a - 0.5 < s < b + 0.5 for a, b in boards):
        n_cut += 1
        if n_cut % 8 == 0: add('enta_glitch', s - 0.08, 0.25, seed=i, strength=0.5); sfx(s - 0.08, 'glitch', 0.18)

cues.sort(key=lambda c: c['src'])
plan = {'cut': False, 'captions': False, 'pack': 'charcoal', 'cues': cues}
json.dump(plan, open(W / 'plan.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
cards = sorted((c['src'], c['src'] + c['dur']) for c in cues if c['t'].startswith('enta_') and c['t'] not in ('enta_glitch', 'enta_leak'))
gaps, prev = [], 2.0
for a, b in cards:
    if a - prev > 5: gaps.append((round(prev, 1), round(a, 1)))
    prev = max(prev, b)
print(len(cues), 'cues;', len(merged), 'shots; avg', round(A1 / len(merged), 2), 's; no-graphic stretches > 5 s:', gaps)

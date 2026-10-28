"""Aly's review 1 of output/review_01.mp4 (2026-10-28, 31 notes in work/review1_notes.md) applied to make_plan.py (one-off patch,
each replacement asserted). Run once: python -X utf8 work/scripts/patch_review1.py"""
from pathlib import Path

p = Path(__file__).with_name('make_plan.py')
s = p.read_text(encoding='utf8')


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:90])
    s = s.replace(a, b)


# ---------------------------------------------------------------- helpers: term per-line timing, Arabic subtitle, both circles, keyframes
rep("""def term(at, dur, term, defn='', example='', exAt=None, en='', sticker='', accent='orange', paper='cream', w=None, exLabel=''):
    dur = min(dur, 9.0)
    if exAt and exAt > at + dur - 2.0: exAt = at + min(dur - 2.0, max(1.5, dur * 0.5))
    sp = side(at, dur, w)
    add('enta_term', at, dur, term=term, example=example, exampleAt=int(((exAt or at + 1.5) - at) * 30), en=en,""",
"""# English name = the term itself -> an Arabic name under it instead (Aly 2026-10-28: "Accountability / Accountability")
AR = {'accountability': 'المساءلة', 'storytelling': 'الحكي', 'small business': 'مشروع صغير', 'passive income': 'دخل سلبي',
      'potential': 'إمكانية النمو', 'pivot': 'تغيير الاتجاه', 'exponential': 'أُسّي', 'curriculum': 'المنهج'}


def term(at, dur, term, defn='', example='', exAt=None, en='', sticker='', accent='orange', paper='cream', w=None, exLabel='', defAt=None, cap=9.0):
    # every line on its own word (Aly 2026-10-28: the cards came before the words): defAt / exAt = absolute seconds
    dur = min(dur, cap)
    if exAt and exAt > at + dur - 2.0: dur = min(cap + 6, exAt - at + 2.5)
    if en and en.lower() == term.replace('*', '').strip().lower(): en = AR.get(en.lower(), en)
    sp = side(at, dur, w)
    add('enta_term', at, dur, term=term, example=example, exampleAt=int(((exAt or at + 1.5) - at) * 30), en=en,
        defAt=int(((defAt or at + 0.3) - at) * 30),""")
rep("""        sticker=sticker, accent=accent, paper=paper, pic='', side='left' if sp == 'G' else 'right', top=0.1, exLabel=exLabel)""",
    """sticker=sticker, accent=accent, paper=paper, pic='', side='left' if sp == 'G' else 'right', top=0.1, exLabel=exLabel)""")
rep("""def board(a, b, title, items, snd=True):
    \"\"\"biz_free board from a to b (seconds); item 'at'/'out'/'grey' in ABSOLUTE seconds -> frames from the board start.\"\"\"
    boards.append((a - 0.3, b + 0.3))
    its = []
    for it in items:
        it = dict(it)
        for key in ('at', 'out', 'grey'):
            if key in it: it[key] = F(a, it[key])""",
"""BOTH = []   # boards where BOTH people stay in their circles (Aly 2026-10-28: 12:30 / 13:35 — the other one listens)


def board(a, b, title, items, snd=True, both=False):
    \"\"\"biz_free board from a to b (seconds); item 'at'/'out'/'grey'/'ceiling'/'cut'/'move' and the first value of every key in
    moves/poses/faces/grow/shake/pop in ABSOLUTE seconds -> frames from the board start.\"\"\"
    boards.append((a - 0.3, b + 0.3))
    if both: BOTH.append(round(a, 2))
    its = []
    for it in items:
        it = dict(it)
        for key in ('at', 'out', 'grey', 'ceiling', 'cut', 'move'):
            if key in it: it[key] = F(a, it[key])
        for key in ('moves', 'poses', 'faces', 'grow', 'shake'):
            if key in it: it[key] = [[F(a, q[0])] + list(q[1:]) for q in it[key]]
        if 'pop' in it: it['pop'] = [dict(q, **{k: F(a, q[k]) for k in ('at', 'grey') if k in q}) for q in it['pop']]""")
rep("""for c in [c for c in cues if c['t'] == 'biz_free' and c['dur'] > 5 and c['src'] > CUT]:
    a, b = c['src'] + 0.8, c['src'] + c['dur'] - 0.3""",
"""for c in [c for c in cues if c['t'] == 'biz_free' and c['dur'] > 5 and c['src'] > CUT]:
    a, b = c['src'] + 0.8, c['src'] + c['dur'] - 0.3
    if round(c['src'], 2) in BOTH:
        add('pip', a, b - a, who='A', zx=FACE['A'][0], zy=FACE['A'][1], side='L'); add('pip', a, b - a, who='G', zx=FACE['G'][0], zy=FACE['G'][1], side='R')
        continue""")

KF = "P + 'pics/karim_face_"

# ---------------------------------------------------------------- 1) business lane: 7 of 8 years, then the 1-year gap, then on again
rep("""    i('path', pts=[[330, 820], [895, 820]], color='mustard', w=12, at=S('S055'), dur=round((T('S057', 'سنة') - S('S055')) * 30)),
    i('walker', n='rocket', pts=[[330, 820], [895, 820]], s=140, at=S('S055'), dur=round((T('S057', 'سنة') - S('S055')) * 30)),""",
"""    # Aly 2026-10-28: the business line reaches much further (it stopped only 1 of the 8 years) -> 7/8 of the Full Time line
    i('path', pts=[[330, 820], [1459, 820]], color='mustard', w=12, at=S('S055'), dur=round((T('S057', 'سنة') - S('S055')) * 30)),
    i('walker', n='rocket', pts=[[330, 820], [1459, 820]], s=140, at=S('S055'), dur=round((T('S057', 'سنة') - S('S055')) * 30)),""")
rep("""    i('chip', text='سنة واحدة *بس* وقف', x=975, y=930, bg='orange', size=30, at=T('S057', 'سنة')),
    i('path', pts=[[1056, 820], [1620, 820]], color='mustard', w=12, at=S('S058'), dur=round((b - S('S058') - 0.5) * 30)),
    i('walker', n='rocket', pts=[[1056, 820], [1620, 820]], s=140, at=S('S058'), dur=round((b - S('S058') - 0.5) * 30)),""",
"""    i('chip', text='سنة واحدة *بس* وقف', x=1540, y=930, bg='orange', size=30, at=T('S057', 'سنة')),
    i('path', pts=[[1620, 820], [1780, 820]], color='mustard', w=12, at=S('S058'), dur=round((b - S('S058') - 0.5) * 30)),
    i('walker', n='rocket', pts=[[1620, 820], [1780, 820]], s=140, at=S('S058'), dur=round((b - S('S058') - 0.5) * 30)),""")

# ---------------------------------------------------------------- 3) "روحت استوديوهات وصورت… جبت ناس كتير": 3 of their instructors in the studio
rep("""photos(S('S077'), E('S080') - S('S077') + 0.3, [""", """photos(S('S077'), S('S080') - S('S077'), [""")
rep("""bubble(T('S074', 'تقفلو'), 3.5,""", """photos(S('S080'), E('S081') - S('S080') + 0.3, [dict(src=P + 'web/courzerve/campaign_1.mp4', start=105, x=0.78, y=0.26, w=400, h=225, rot=-3),
    dict(src=P + 'web/courzerve/campaign_2.mp4', start=30, x=0.82, y=0.5, w=400, h=225, rot=2, at=30),
    dict(src=P + 'web/courzerve/campaign_3.mp4', start=3, x=0.76, y=0.74, w=400, h=225, rot=-2, at=60, caption='مدرّسين في *ستوديو* Courzerve')], w='A')
bubble(T('S074', 'تقفلو'), 3.5,""")

# ---------------------------------------------------------------- 4) Breadfast board: two separate halves, each with its own sentence
a0 = s.index("board(a, b, 'نفس *الفكرة*… في نفس *الوقت*', [")
a1 = s.index("photos(S('S096')")
s = s[:a0] + """board(a, b, 'نفس *الفكرة*… في نفس *الوقت*', [
    # Aly 2026-10-28: no arrow joining them (two separate companies); each sentence on its own side; brand name Early Breakfast
    i('path', pts=[[960, 230], [960, 1010]], color='mustard', w=6, dash=True, at=a + 0.3, dur=20),
    # right = Karim's startup (said first: Early Breakfast)
    i('emo', n='sunrise', x=1440, y=300, s=130, at=T('S090', 'Early') if True else a, float=True),
    i('text', text='Early Breakfast', x=1440, y=440, size=56, paper=True, at=T('S090', 'Early') + 0.2),
    i('chip', text='الستارتب اللي كريم *اشتغل فيها*', x=1440, y=550, bg='orange', size=30, at=T('S090', 'Early') + 0.6),
    i('emo', n='cityscape', x=1640, y=780, s=170, at=S('S094') + 1.0), i('emo', n='round_pushpin', x=1640, y=660, s=90, at=S('S094') + 1.4),
    i('walker', n='motor_scooter', pts=[[1180, 820], [1520, 820]], s=150, at=S('S094') + 0.4, dur=50),
    i('emo', n='bread', x=1180, y=700, s=90, at=S('S094') + 0.4),
    i('chip', text='نفس الحاجة… *أكبر شوية* · في *دبي*', x=1440, y=960, bg='blue', size=32, at=S('S094') + 1.2),
    # left = Breadfast (Egypt)
    i('logo', src=P + 'pics/breadfast_brand.svg', x=480, y=380, s=230, pad=0.1, at=S('S091') + 0.4),
    i('emo', n='alarm_clock', x=250, y=640, s=110, at=S('S093'), float=True),
    i('walker', n='motor_scooter', pts=[[180, 820], [560, 820]], s=150, at=S('S093') + 0.3, dur=50),
    i('emo', n='bread', x=180, y=700, s=90, at=S('S093') + 0.3),
    i('emo', n='house', x=720, y=780, s=170, at=S('S093') + 0.8), i('emo', n='round_pushpin', x=720, y=660, s=90, at=S('S093') + 1.2),
    i('chip', text='*التجمع* · كل يوم *الصبح*', x=480, y=960, bg='mustard', size=34, at=S('S093') + 0.6),
])
""" + s[a1:]

# ---------------------------------------------------------------- 5) courses board: the 4th part = Marketing (Whisper wrote المحتوى x5)
rep("""    i('emo', n='books', x=1540, y=470, s=180, at=S('S136')), i('chip', text='*المحتوى*', x=1540, y=640, bg='mustard', at=S('S136') + 0.2),""",
    """    i('emo', n='megaphone', x=1540, y=470, s=180, at=S('S136')), i('chip', text='*Marketing*', x=1540, y=640, bg='mustard', at=S('S136') + 0.2),""")

# ---------------------------------------------------------------- 6) marketing = tries: several posters, videos one by one, + After Effects
rep("""    i('pic', src=P + 'web/courzerve/cz_android.jpg', x=470, y=520, w=420, rot=-4, cap='الأول: *صور*', at=S('S160') + 0.6),
    i('arrow', pts=[[720, 520], [860, 520]], color='mustard', at=S('S160') + 3.0),
    i('pic', src=P + 'web/courzerve/campaign_2.mp4', x=1230, y=500, w=720, ar=16 / 9, rot=2, cap='بعدين: *فيديو*', at=S('S160') + 3.4, **{'from': 30 * 20}),
    i('emo', n='clapper_board', x=420, y=880, s=120, at=S('S161') + 0.6), i('emo', n='camera_with_flash', x=600, y=880, s=120, at=S('S162')),
    i('logo', src='logos/premiere-pro-official.png', x=780, y=880, s=110, pad=0.08, at=T('S162', 'منتاج')), i('emo', n='framed_picture', x=960, y=880, s=120, at=S('S163')),
    i('chip', text='*الكوست* كبيرة', x=690, y=1010, bg='orange', size=34, at=S('S164')),
    i('chip', text='لحد ما تلاقي *الوصفة* اللي تنفع', x=1300, y=900, bg='mustard', size=38, emo='man_cook', at=S('S167')),""",
"""    # Aly 2026-10-28: several posters side by side (small overlap); the videos one by one: motion examples, then studio shots
    i('pic', src=P + 'web/courzerve/cz_android.jpg', x=300, y=500, w=280, rot=-7, at=T('S160', 'صور') - 0.3),
    i('pic', src=P + 'web/courzerve/cz_instructors.jpg', x=470, y=530, w=280, rot=2, at=T('S160', 'صور') + 0.1),
    i('pic', src=P + 'web/courzerve/cz_head.jpg', x=640, y=500, w=280, rot=7, at=T('S160', 'بس'), cap='الأول: *صور*'),
    i('arrow', pts=[[800, 520], [880, 520]], color='mustard', at=T('S160', 'وبعد')),
    i('pic', src=P + 'web/courzerve/campaign_2.mp4', x=1310, y=480, w=720, ar=16 / 9, rot=2, cap='بعدين: *موشن*', at=T('S160', 'عملنا'), out=T('S160', 'الانستروكترز') - 0.3, **{'from': 30 * 36}),
    i('pic', src=P + 'web/courzerve/campaign_1.mp4', x=1310, y=480, w=720, ar=16 / 9, rot=-2, cap='و*موشن* كمان', at=T('S160', 'الانستروكترز'), out=T('S160', 'ستوديوز') - 0.3, **{'from': 30 * 6}),
    i('pic', src=P + 'web/courzerve/campaign_1.mp4', x=1310, y=480, w=720, ar=16 / 9, rot=2, cap='و*تصوير* في ستوديو', at=T('S160', 'ستوديوز'), out=T('S160', 'ادتنج') - 0.3, **{'from': 30 * 105}),
    i('pic', src=P + 'web/courzerve/campaign_3.mp4', x=1310, y=480, w=720, ar=16 / 9, rot=-2, cap='و*تصوير* في ستوديو', at=T('S160', 'ادتنج'), **{'from': 30 * 125}),
    i('emo', n='clapper_board', x=360, y=880, s=120, at=S('S161') + 0.6), i('emo', n='camera_with_flash', x=540, y=880, s=120, at=S('S162')),
    i('logo', src='logos/premiere-pro-official.png', x=720, y=880, s=110, pad=0.08, at=T('S162', 'منتاج')),
    i('logo', src='logos/after-effects.png', x=880, y=880, s=110, pad=0.08, at=T('S162', 'منتاج') + 0.4),
    i('emo', n='framed_picture', x=1040, y=880, s=120, at=S('S163')),
    i('chip', text='*الكوست* كبيرة', x=700, y=1010, bg='orange', size=34, at=S('S164')),
    i('chip', text='لحد ما تلاقي *الوصفة* اللي تنفع', x=1460, y=1000, bg='mustard', size=36, emo='man_cook', at=S('S167')),""")

# ---------------------------------------------------------------- 7) McDonald's: other restaurants = icons, the % no longer covers the logo; then the worlds
rep("""a, b = S('S228'), E('S234') + 0.4
board(a, b, 'أحسن واحد *بيلمّ الليلة*', [
    i('logo', src='logos/mcdonalds.svg', x=520, y=420, s=200, at=S('S230') + 2.0),
    i('bar', x=520, y=900, w=230, h=380, color='mustard', label='60–70%؟', at=S('S232'), dur=24),
    i('logo', src='logos/kfc.svg', x=1180, y=420, s=150, at=S('S229') + 1.5), i('logo', src='logos/burgerking.svg', x=1380, y=420, s=150, at=S('S229') + 2.5),
    i('emo', n='fork_and_knife_with_plate', x=1580, y=430, s=140, at=S('S233')),
    i('bar', x=1380, y=900, w=520, h=150, color='blue', label='*3000* مطعم… في الباقي', at=S('S233'), dur=24),""",
"""a, b = S('S228'), S('S234') - 0.2
board(a, b, 'أحسن واحد *بيلمّ الليلة*', [
    i('logo', src='logos/mcdonalds.svg', x=520, y=300, s=180, at=S('S230') + 2.0),
    i('bar', x=520, y=900, w=230, h=380, color='mustard', label='60–70%؟', at=S('S232'), dur=24),
    # Aly 2026-10-28: the 3000 = restaurants with no name -> icons, no KFC / Burger King
    *[i('emo', n=['hamburger', 'pizza', 'taco', 'hot_dog', 'sushi', 'burrito', 'fork_and_knife_with_plate'][k % 7], x=1150 + (k % 6) * 92 + (k // 6 % 2) * 46, y=440 + (k // 6) * 92,
        s=78, at=S('S233') + 0.08 * k) for k in range(18)],
    i('bar', x=1380, y=900, w=520, h=150, color='blue', label='*3000* مطعم… في الباقي', at=S('S233'), dur=24),""")
rep("""note(S('S240'), 'ماينفعش *تحارب* العالم بتاعك… لازم يكون *محتاجك*', d=4.5, accent='olive')
""", """# 12) "العالم بتاعك" (Aly 2026-10-28): every business type = a small world with its players; Karim = a character with his real face
a, b = S('S234') - 0.2, E('S243') + 0.4
board(a, b, 'كل بيزنس = *عالم* لوحده', [
    i('planet', x=520, y=560, r=150, color='orange', logo='logos/mcdonalds.svg', label='عالم *الفاست فود*', at=T('S234', 'ماكدولنز'), out=T('S234', 'تحدد') - 0.3,
      pop=[dict(n='hamburger', ang=-55, s=70, at=T('S234', 'البرجر')), dict(n='french_fries', ang=55, s=70, at=T('S234', 'الفاست'))]),
    i('planet', x=1400, y=560, r=150, color='olive', icon='man_cook', label='عالم *البرجر الجورميه*', at=T('S234', 'الجورميه'), out=T('S234', 'تحدد') - 0.3),
    i('text', text='*مش* في نفس العالم', x=960, y=330, size=44, paper=True, at=T('S234', 'نفس'), out=T('S234', 'تحدد') - 0.3),
    i('planet', x=960, y=610, r=200, color='blue', icon='graduation_cap', label='عالم *كورسات Software*', at=T('S234', 'تحدد'),
      shake=[[T('S236', 'Software')], [T('S236', 'موسقة')], [T('S236', 'هيفيدك')]],
      pop=[dict(n='school', ang=-150 + k * 25, s=64, at=T('S234', 'الكورسز') + 1.2 + 0.12 * k) for k in range(13)]),
    i('char', s=200, at=T('S234', 'العالم', 3),
      moves=[[T('S234', 'العالم', 3), 960, 410], [T('S236', 'وأنا'), 960, 410], [T('S236', 'Software') - 0.2, 700, 760], [S('S240'), 700, 760],
             [T('S240', 'أحارب') + 0.3, 520, 820], [S('S241'), 520, 820], [T('S241', 'يحتاج') + 0.6, 960, 410]],
      poses=[[T('S234', 'العالم', 3), 'stand'], [T('S236', 'وأنا'), 'walk'], [T('S236', 'Software'), 'push'], [T('S240', 'أحارب'), 'sad'],
             [S('S241'), 'walk'], [T('S241', 'يحتاج') + 0.6, 'cheer'], [S('S243'), 'stand']],
      faces=[[T('S234', 'العالم', 3), KF + 'neutral.png'], [S('S235'), KF + 'sad.png'], [T('S241', 'يحتاج'), KF + 'happy.png'], [S('S243'), KF + 'neutral.png']]),
    i('chip', text='*10–15* منافس', x=1500, y=330, bg='blue', size=34, at=T('S234', 'الكورسز') + 2.0, out=S('S235') + 2.0),
    i('emo', n='scroll', x=1520, y=420, s=120, at=T('S235', 'شهادات')),
    i('chip', text='العملاء عايزين *شهادات معتمدة*', x=1500, y=560, bg='blue', size=32, at=T('S235', 'شهادات') + 0.2),
    i('chip', text='وهو مقتنع: *مش هتفرق*', x=1500, y=660, bg='orange', size=32, at=T('S236', 'Software')),
    i('mark', ok=False, x=420, y=640, s=100, at=T('S240', 'أحارب')), i('chip', text='*تحارب* عالمك', x=420, y=960, bg='orange', size=34, at=T('S240', 'أحارب') + 0.2),
    i('mark', ok=True, x=1240, y=300, s=100, at=T('S241', 'يحتاج')), i('chip', text='عالمك يبقى *محتاجك*', x=1500, y=960, bg='olive', size=34, at=T('S241', 'يحتاج') + 0.2),
    i('text', text='هتبقى *أحسن واحد* في عالمك؟', x=960, y=1000, size=36, paper=True, at=S('S243')),
], both=True)
""")
# remove the old term card + notes the worlds/cake boards replace
rep("""term(S('S235'), E('S236') - S('S235'), 'شهادات *معتمدة*', 'عملاء Courzerve كانوا عايزين *شهادات* من جهات معينة', 'وكريم مقتنع إنها في الـ*Software* مش هتفرق', exAt=S('S236'),
     sticker='star_y', accent='blue', paper='blue', w='G')
note(S('S253'), 'مش لازم تبقى *الأول*… لو المكسب *كويس* يكفي', d=5.0, accent='olive')
note(S('S258') + 0.3, 'مبيعاتك كويسة؟ *العالم كبير* ويكفي', d=4.0, accent='mustard')
""", """# 9) 13:35 Aly's cake example — Karim stays visible (both circles) while Aly explains
a, b = S('S251') - 0.3, E('S254') + 0.3
board(a, b, 'قد إيه من *التورتة*؟', [
    i('cake', x=560, y=560, r=120, frac=0.5, at=S('S251') - 0.1, cut=T('S251', 'قد'), move=T('S251', 'هتاخده'), slide=[0, 300]),
    i('chip', text='تورتة *صغيرة* · حتة *كبيرة* (50%)', x=560, y=360, bg='orange', size=30, at=S('S251') + 0.1),
    i('cake', x=1360, y=520, r=300, frac=0.12, at=S('S251') + 0.4, cut=T('S251', 'هتاخده'), move=T('S251', 'الترطة'), slide=[0, 340]),
    i('chip', text='تورتة *كبيرة* · حتة *صغيرة* (12%)', x=1360, y=290, bg='blue', size=30, at=S('S251') + 0.6),
    i('emo', n='balance_scale', x=960, y=860, s=150, at=S('S252')),
    i('mark', ok=True, x=1600, y=820, s=100, at=T('S253', 'كويس')),
    i('text', text='مش فارق تاخد *قد إيه*… فارق *حجم التورتة*', x=960, y=1010, size=38, paper=True, at=T('S252', 'الترطة'), out=S('S254') - 0.2),
    i('text', text='مش لازم تبقى *الأول*… لو المكسب *كويس*', x=960, y=1010, size=38, paper=True, at=S('S254')),
], both=True)
# S258-S260 "العالم كبير… التاني ولا التالت ولا العاشر يكفي": the same world grows, Karim a little figure on it
a, b = S('S258') + 0.3, E('S260') + 0.2
board(a, b, 'العالم *كبير*', [
    i('planet', x=960, y=640, r=170, color='blue', icon='graduation_cap', label='عالمك', at=a + 0.2, grow=[[a + 0.4, 1.0], [T('S260', 'كبير'), 1.35]]),
    i('char', s=150, at=a + 0.4, moves=[[a + 0.4, 960, 470], [T('S260', 'كبير'), 960, 410]], poses=[[a, 'stand'], [T('S260', 'فيكفي'), 'cheer']],
      faces=[[a, KF + 'neutral.png'], [T('S260', 'فيكفي'), KF + 'happy.png']]),
    i('chip', text='*التاني*', x=1460, y=420, bg='olive', size=34, at=T('S259', 'الثاني')),
    i('chip', text='*التالت*', x=1520, y=560, bg='olive', size=34, at=T('S259', 'الثلاثة')),
    i('chip', text='*العاشر*', x=1460, y=700, bg='olive', size=34, at=T('S259', 'العشر')),
    i('text', text='ولو مبيعاتك *كويسة*… *يكفي*', x=960, y=1000, size=38, paper=True, at=T('S260', 'فيكفي') - 0.4),
])
""")

# ---------------------------------------------------------------- 13) arrows inside Arabic text point LEFT
rep("""i('chip', text="*Kiko's* · 11 الصبح → 2 الفجر",""", """i('chip', text="*Kiko's* · 11 الصبح ← 2 الفجر",""")
rep("""note(S('S272'), 'Courzerve: *2019* → *2021* · قرب سنتين'""", """note(S('S272'), 'Courzerve: *2019* ← *2021* · قرب سنتين'""")

# ---------------------------------------------------------------- 14) 4 h vs 14 h: time = blue both sides, money = mustard both sides + legend
rep("""    i('bar', x=1290, y=920, w=140, h=360, color='orange', label='*14* ساعة', at=S('S431') - 1.5, dur=26),""",
    """    i('bar', x=1290, y=920, w=140, h=360, color='blue', label='*14* ساعة', at=S('S431') - 1.5, dur=26),""")
rep("""    i('emo', n='alarm_clock', x=960, y=640, s=150, at=S('S429') + 1.0, float=True),
])""", """    i('emo', n='alarm_clock', x=960, y=640, s=150, at=S('S429') + 1.0, float=True),
    i('chip', text='الوقت', x=880, y=1010, bg='blue', size=30, emo='alarm_clock', at=S('S428') + 0.5),
    i('chip', text='الفلوس', x=1060, y=1010, bg='mustard', size=30, emo='money_bag', at=S('S428') + 0.7),
])""")

# ---------------------------------------------------------------- 12b) "عالم جديد": Karim jumps from the crowded world and makes his own
a0 = s.index("board(a, b, 'عالم *جديد*… مفيش فيه منافسة', [")
a1 = s.index("note(T('S376', 'الجيش')")
s = s[:a0] + """board(a, b, 'عالم *جديد*… مفيش فيه منافسة', [
    i('planet', x=500, y=620, r=150, color='blue', icon='graduation_cap', label='عالم *الكورسات*', at=a + 0.2,
      pop=[dict(n='school', ang=-150 + k * 30, s=56, at=a + 0.4 + 0.08 * k) for k in range(11)]),
    i('char', s=180, at=a + 0.5,
      moves=[[a + 0.5, 500, 470], [T('S373', 'هعمل'), 500, 470], [T('S373', 'عالم') + 0.2, 930, 240], [T('S373', 'جديد') + 0.6, 1360, 430]],
      poses=[[a, 'sad'], [T('S373', 'هعمل'), 'jump'], [T('S373', 'جديد') + 0.6, 'stand'], [T('S374', 'منافسة'), 'cheer']],
      faces=[[a, KF + 'sad.png'], [T('S373', 'هعمل'), KF + 'neutral.png'], [T('S374', 'منافسة'), KF + 'happy.png']]),
    i('planet', x=1360, y=620, r=190, color='orange', icon='popcorn', label='سناكس *السينما* للبيت', at=T('S373', 'عالم'),
      pop=[dict(n='house', ang=60, s=90, at=T('S373', 'للبيت')), dict(n='clapper_board', ang=-60, s=80, at=T('S373', 'السينما'))]),
    i('emo', n='crown', x=1360, y=230, s=110, at=T('S374', 'منافسة') + 0.4, rot=-8),
    i('text', text='مفيش منافسة… يبقى أنا *الأحسن* في العالم ده', x=960, y=1000, size=40, paper=True, at=T('S374', 'منافسة')),
    i('pic', src=P + 'web/kikos/p03.jpg', x=1740, y=860, w=240, rot=6, at=S('S375') + 1.0),
])
""" + s[a1:]

# ---------------------------------------------------------------- 15/17) photo captions: on top (code) + more room; Highlights on the app
rep("""photos(S('S487'), 6.0, [dict(src=P + 'web/fpl/p07.jpg', w=380, rot=-3, caption='Highlights على *الويبسايت*'), dict(src=P + 'web/fpl/p11.jpg', x=0.84, y=0.66, w=330, rot=4, at=14)], w='G')""",
    """photos(S('S487'), 6.0, [dict(src=P + 'web/fpl/p07.jpg', y=0.36, w=380, rot=-3, caption='Highlights على *الأبليكيشن*'), dict(src=P + 'web/fpl/p11.jpg', x=0.84, y=0.74, w=330, rot=4, at=14)], w='G')""")

# ---------------------------------------------------------------- 12c) S507 "سقف العالم بتاعي": the FPL world has a ceiling he hits
rep("""note(S('S505'), 'مع سرعة *AI*… فيه *Gap* في السوق لازم يستغله', d=4.5, accent='blue')""",
"""note(S('S505'), 'مع سرعة *AI*… فيه *Gap* في السوق لازم يستغله', d=4.5, accent='blue')
a, b = S('S507'), E('S508') + 0.3
board(a, b, '*سقف* العالم بتاعه', [
    i('planet', x=960, y=660, r=200, color='olive', icon='soccer_ball', label='عالم *الـFantasy*', at=a + 0.2, ceiling=T('S507', 'سقف'), ceilR=2.4,
      pop=[dict(n='mobile_phone', ang=-140 + k * 40, s=70, at=a + 0.6 + 0.1 * k) for k in range(8)]),
    i('char', s=180, at=a + 0.6,
      moves=[[a + 0.6, 960, 460], [T('S507', 'العالم'), 960, 460], [T('S507', 'العالم') + 0.35, 960, 330], [T('S507', 'العالم') + 0.8, 960, 460]],
      poses=[[a, 'stand'], [T('S507', 'العالم'), 'jump'], [T('S507', 'العالم') + 0.8, 'sad']],
      faces=[[a, KF + 'neutral.png'], [T('S507', 'العالم') + 0.6, KF + 'sad.png']]),
    i('text', text='المنافسين *سبقوه*… والـAI هيخليهم يسبقوا *أكتر*', x=960, y=1010, size=36, paper=True, at=S('S508')),
])""")
rep("""note(S('S508'), 'المنافسين *سبقوه*… والـAI هيخليهم يسبقوا *أكتر*', d=5.0, accent='orange')
""", "")

# ---------------------------------------------------------------- 16) new project card: no link
rep("""term(S('S517'), 7.0, 'المشروع *الجديد*', 'تتخيّل *بيتك* وتفرشه قبل ما تشتري', 'اللينك *في الوصف*', exAt=S('S524'), sticker='shop', accent='olive', w='G')""",
    """term(S('S517'), 7.0, 'المشروع *الجديد*', 'تتخيّل *بيتك* وتفرشه قبل ما تشتري', '', sticker='shop', accent='olive', w='G')""")
rep("""note(S('S527'), 'لينك الأبلكيشن الجديد *في الوصف*', d=4.0, accent='mustard')
""", "")

# ---------------------------------------------------------------- 18) Barrier to Entry (Aly said "barrier for entry" at 26:41)
rep("""bubble(S('S528'), 5.0, 'في عصر *AI*… إيه *الـEdge* اللي يخليك تنجح؟', w='A')""",
"""term(T('S528', 'البرير'), E('S530') - T('S528', 'البرير'), '*Barrier to Entry*', 'اللي بيصعّب على حد *جديد* يدخل نفس البيزنس',
     'والـAI خلّاه *أقل* بكتير… فالمنافسين *أكتر*', exAt=S('S529'), en='عائق الدخول', sticker='briefcase', accent='blue', w='A')
bubble(S('S533'), 4.5, 'في عصر *AI*… إيه *الـEdge* اللي يخليك تنجح؟', w='A')""")

# ---------------------------------------------------------------- 19) 5 pillars (2nd board): each sentence above ITS pillar, at its time
rep("""its += [i('chip', text='الفكرة = *بتاعتك*… رأيك و*ذوقك*', x=960, y=270, bg='mustard', size=34, at=S('S589'), out=S('S592')),
        i('chip', text='والتوقيت: الناس *محتاجاه دلوقتي*؟', x=960, y=270, bg='blue', size=34, at=S('S592')),
        i('text', text='بدل *5 عواميد*… محتاج *3* بس', x=960, y=260, size=46, paper=True, at=S('S600'))]
its[-2]['out'] = S('S600') - 0.2""",
"""its += [i('text', text='*بتاعتك*:\\nرأيك و*ذوقك*', x=360, y=280, size=30, paper=True, at=T('S591', 'الأوبينيون'), out=S('S600') - 0.2),
        i('text', text='على حسب\\n*رؤيتك*', x=660, y=280, size=30, paper=True, at=T('S591', 'التنفيذ'), out=S('S600') - 0.2),
        i('text', text='الناس *محتاجاه*\\nدلوقتي؟', x=1560, y=280, size=30, paper='blue', at=S('S592'), out=S('S600') - 0.2),
        i('text', text='بدل *5 عواميد*… محتاج *3* بس', x=960, y=260, size=46, paper=True, at=S('S600'))]""")

# ---------------------------------------------------------------- 20/21/22) cards on their words
rep("""term(S('S631'), E('S640') - S('S631'), 'هدف كريم', 'يصحى يحس *بالفخر*', 'إن *البيزنس بتاعه* هو اللي معيّشه', exAt=S('S638'), sticker='star_y', accent='mustard', w='G')""",
    """term(T('S638', 'احس') - 0.2, E('S640') - T('S638', 'احس') + 0.2, 'هدف كريم', 'يصحى يحس *بالفخر*', 'إن *البيزنس بتاعه* هو اللي معيّشه', exAt=T('S639', 'البيزنس'), sticker='star_y', accent='mustard', w='G', cap=12.0)""")
rep("""term(S('S695'), E('S700') - S('S695'), 'ولا حتى *عشان الفلوس*', 'الوظيفة = دخل *ثابت* على طول', 'البيزنس… عبال ما يوصل لدخلك *حرقت وقت*', exAt=S('S698'), sticker='coin', accent='orange', w='A')""",
    """term(T('S694', 'عشان') - 0.1, E('S699') - T('S694', 'عشان') + 0.8, 'ولا حتى *عشان الفلوس*', 'الوظيفة = دخل *ثابت* على طول', 'البيزنس… عبال ما يوصل لدخلك *حرقت وقت*',
     defAt=T('S696', 'ثابت') - 0.6, exAt=T('S699', 'حرقت'), sticker='coin', accent='orange', w='A', cap=19.0)""")
rep("""term(S('S753'), E('S755') - S('S753'), '*Storytelling*', 'تحكي *قصة* بتفيد الناس… مش إعلان بحت', 'بيشرح بشكل *مبسط*… والناس تستفيد', exAt=S('S754'), en='Storytelling', sticker='star_y', accent='mustard', w='G')""",
    """term(T('S753', 'storytelling'), 9.0, '*Storytelling*', 'تحكي *قصة*… وتنزّل *Content*', 'بيشرح بشكل *مبسط*… والناس تستفيد', defAt=T('S753', 'content'), exAt=S('S754') + 1.0,
     en='Storytelling', sticker='star_y', accent='mustard', w='G')
note(T('S756', 'مايبقاش'), 'مش مادة *إعلانية* بحتة', d=2.2, accent='mustard')""")

# ---------------------------------------------------------------- 11) Accountability = المساءلة (via AR) + "بيسألك ويتابعك"
rep("""'*Accountability*', 'حد *يحاسبك*: دفعت فلوس… ومواعيد في الأسبوع'""", """'*Accountability*', 'حد *بيسألك* ويتابعك: دفعت فلوس… ومواعيد في الأسبوع'""")

# ---------------------------------------------------------------- 23) don't stubborn-push: glove beside "إمتى تقاوح؟", chips centred
rep("""    i('emo', n='boxing_glove', x=560, y=520, s=220, at=S('S764'), rot=-10),
    i('chip', text='إمتى *تتعلم*؟', x=1180, y=400, bg='blue', size=38, emo='books', at=S('S767')),
    i('chip', text='إمتى *تقاوح*؟', x=1180, y=520, bg='olive', size=38, emo='flexed_biceps', at=T('S767', 'تقوح')),
    i('chip', text='وإمتى *ترمي المنديل*… أو تغيّر؟', x=1180, y=640, bg='orange', size=36, emo='white_flag', at=S('S768')),""",
"""    i('chip', text='إمتى *تتعلم*؟', x=960, y=380, bg='blue', size=38, emo='books', at=S('S767')),
    i('chip', text='إمتى *تقاوح*؟', x=960, y=510, bg='olive', size=38, emo='flexed_biceps', at=T('S767', 'تقوح')),
    i('emo', n='boxing_glove', x=1250, y=505, s=150, at=T('S767', 'تقوح') + 0.2, rot=-14),
    i('chip', text='وإمتى *ترمي المنديل*… أو تغيّر؟', x=960, y=640, bg='orange', size=36, emo='white_flag', at=S('S768')),""")

# ---------------------------------------------------------------- 26) AI pyramid: the source on the side (36Kr, numbers = Karpathy's napkin math)
rep("""    i('text', text='رقم تقريبي من صورة علي شافها · مش إحصائية', x=960, y=1020, size=26, at=S('S821') + 0.5),""",
"""    i('pic', src=P + 'pics/ai_pyramid_36kr.jpg', x=1640, y=700, w=420, rot=3, at=S('S824') + 0.5, cap='المصدر: *36Kr*', capSize=26),
    i('text', text='التقدير: *Andrej Karpathy* (بوست على X · أكتوبر 2026) · أرقام *تقريبية*', x=960, y=1030, size=26, at=S('S821') + 0.5),""")

# ---------------------------------------------------------------- 27/28) "الـAI بيتغلغل واحدة واحدة" + the architect episode card
rep("""board(a, b, 'الـAI *بيتغلغل*… واحدة واحدة', [""", """board(a, b, 'الـAI *بيتغلغل* واحدة واحدة', [""")
rep("""    i('emo', n='classical_building', x=960, y=520, s=180, at=S('S866') + 10.0), i('chip', text='*المعماري*', x=960, y=680, bg='olive', at=S('S866') + 10.2),""",
"""    i('emo', n='classical_building', x=960, y=520, s=180, at=S('S866') + 10.0), i('chip', text='*المعماري*', x=960, y=680, bg='olive', at=S('S866') + 10.2),
    # Aly 2026-10-28: our architect episode = thumbnail + its exact YouTube title + QR (never a QR without the thumbnail)
    i('panel', x=1460, y=330, w=600, h=300, bg='dark', at=S('S866') + 10.6, out=S('S868') - 0.3),
    i('pic', src=P + 'pics/arch_ep_thumb.jpg', x=1380, y=300, w=300, ar=16 / 9, tape=False, at=S('S866') + 10.8, out=S('S868') - 0.3),
    i('pic', src=P + 'pics/qr_arch_ep.png', x=1650, y=300, w=150, tape=False, at=S('S866') + 11.0, out=S('S868') - 0.3),
    i('text', text='من رسمة حلوة لمبنى حقيقي:\\nشغل الـ*Technical Design*', x=1460, y=430, size=24, at=S('S866') + 11.0, out=S('S868') - 0.3),""")

# ---------------------------------------------------------------- 29) "عزة النفس بتلعبه كوتشينة": the joke as a tiny scene
rep("""note(S('S887'), 'لو متمسك بيها… الناس *هتسبقك* جامد', d=4.5, accent='orange')""",
"""note(S('S887'), 'لو متمسك بيها… الناس *هتسبقك* جامد', d=3.4, accent='orange')
a, b = S('S889') - 0.2, S('S889') + 4.4
board(a, b, '*عزة النفس*… بتلعب كوتشينة', [
    i('poly', pts=[[460, 700], [1460, 700], [1640, 990], [280, 990]], fill='#2f6b4f', stroke='#e9e4dc', sw=8, at=a + 0.1, dur=8),
    i('emo', n='smirking_face', x=960, y=480, s=250, at=a + 0.2), i('emo', n='crown', x=960, y=300, s=130, rot=-12, at=a + 0.4),
    i('chip', text='*عزة النفس*', x=960, y=650, bg='orange', size=34, at=a + 0.5),
    i('card', face='K♥', from_=[960, 560], to=[760, 850], rot=-14, at=T('S889', 'كوتشينة') - 0.3, dur=12),
    i('card', face='A♠', from_=[960, 560], to=[960, 870], rot=4, at=T('S889', 'كوتشينة'), dur=12),
    i('card', face='Q♦', from_=[960, 560], to=[1160, 850], rot=16, at=T('S889', 'كوتشينة') + 0.3, dur=12),
    i('emo', n='rolling_on_the_floor_laughing', x=1560, y=520, s=150, at=T('S889', 'معرفش')),
])
for c in cues:   # 'from' is a Python keyword -> from_ in the item, the card reads 'from'
    if c['t'] == 'biz_free':
        for it in c['props']['items']:
            if it.get('k') == 'card' and 'from_' in it: it['from'] = it.pop('from_')""")

# ---------------------------------------------------------------- 31) his 4 accounts (TikTok too)
rep("""photos(S('S941'), 6.0, [dict(src='logos/instagram.svg', w=150, rot=-6, bare=True), dict(src='logos/facebook.svg', x=0.71, y=0.5, w=150, rot=5, at=8, bare=True),
                        dict(src='logos/youtube-icon.svg', x=0.86, y=0.42, w=160, rot=-3, at=16, bare=True)], w='A')
note(S('S941') + 6.2, 'ريل *كل يوم*: Instagram · Facebook · YouTube', d=4.0, accent='orange')""",
"""photos(S('S941') + 1.0, 7.0, [dict(src='logos/instagram.svg', x=0.66, y=0.27, w=130, h=130, rot=-4, bare=True, caption='@alyshorosh'),
                        dict(src='logos/facebook.svg', x=0.86, y=0.27, w=130, h=130, rot=4, at=8, bare=True, caption='aly.shorosh'),
                        dict(src='logos/youtube-icon.svg', x=0.66, y=0.62, w=130, h=130, rot=3, at=16, bare=True, caption='@AlyShorosh'),
                        dict(src='logos/tiktok.svg', x=0.86, y=0.62, w=130, h=130, rot=-3, at=24, bare=True, caption='@alyshorosh')], w='A')
note(S('S941') + 8.2, 'ريل *كل يوم*: Instagram · Facebook · YouTube · TikTok', d=4.0, accent='orange')""")

# ---------------------------------------------------------------- 2) name tag علي شُرُش (+ old text kept for the width) and Meet's speaking dots hidden
PT = "json.load(open(W / 'patches.json'))"
rep("""dict(who='A', box=[978, 776, 110, 26], tag='علي معتز'),""", """dict(who='A', box=[978, 776, 110, 26], tag='علي شُرُش', keep='علي معتز', fix=True),
                                        dict(who='G', box=[908, 290, 44, 44], patch=PATCH['G2'], fix=True),""")
rep("""                 'masks': [dict(who='G', box=[186, 912, 150, 30], tag='كريم تامر')],""",
    """                 'masks': [dict(who='G', box=[186, 912, 150, 30], tag='كريم تامر'), dict(who='G', box=[1705, 152, 44, 44], patch=PATCH['Gbig'], fix=True)],""")
rep("""                                 masks=[dict(who='G', box=[186, 912, 150, 30], tag='كريم تامر')]),""",
    """                                 masks=[dict(who='G', box=[186, 912, 150, 30], tag='كريم تامر'), dict(who='G', box=[1705, 152, 44, 44], patch=PATCH['Gbig'], fix=True)]),""")
rep("""cues.sort(key=lambda c: c['src'])
plan = {""", """cues.sort(key=lambda c: c['src'])
PATCH = """ + PT + """   # clean crops of the spot where Meet drew the speaking dots (work/indicator_scan.npz)
plan = {""")

p.write_text(s, encoding='utf8', newline='\n')
print('patched', p)

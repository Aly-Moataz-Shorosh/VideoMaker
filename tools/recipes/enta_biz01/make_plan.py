"""انت بتشتغل ايه — رواد الأعمال ep01 (guest Karim Tamer: Courzerve -> Kiko's Snacks -> FPL Champ), 2026-10-27.
Input = his Premiere export of a Google Meet SCREEN RECORDING (45:03): his biz intro 0-17.12 and again 2686.0-end.
Two Meet layouts (found by numbers, work/scripts notes in docs/22):
  17.12-187.53  Karim BIG (tile 169,151 1582x800) + Aly's tiny self-view (1658,808 139x104) inside Karim's tile corner
  187.53-2686   side by side (Karim 18,288 936x526 · Aly 966,288 936x526) — his own cut at 187.53 is the switch
Aly's asks (2026-10-27): 0:17-2:03 = HIS intro with a tiny camera -> enlarge only "enough" + a LOT of motion + Blender (biz_open,
his picture the whole time, Karim behind a curtain that opens); then Karim alone; then the usual style 14 (cadres + calm zoom),
Aly LEFT / Karim RIGHT (he looks right). No crop of the tiles the whole video (Meet labels covered by our name tags).
Run: python -X utf8 work/scripts/make_plan.py -> work/plan.json ; build: sh work/scripts/build.sh review_01 (code 'entabiz01')."""
import json, random
from pathlib import Path

W = Path(__file__).resolve().parents[1]
P = 'projects/entabiz01/'
A0, CUT, A1 = 17.12, 187.53, 2686.0
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
SENT = {s['id']: s for s in tr['sentences']}
SPK = json.load(open(W / 'speakers.json', encoding='utf8'))
random.seed(11)


def T(sid, sub, k=0):  # time of the k-th word containing sub in sentence sid (falls back to the sentence start)
    hits = [w['start'] for w in SENT[sid]['words'] if sub in w['w']]
    if len(hits) <= k:
        print('  ! anchor not found', sid, sub); return SENT[sid]['words'][0]['start']
    return hits[k]


def S(sid): return SENT[sid]['words'][0]['start']
def E(sid): return SENT[sid]['words'][-1]['end']


def who(t):
    best = min(SPK['words'], key=lambda w: abs((w[0] + w[1]) / 2 - t))
    return best[3]


cues, locks, boards = [], [], []
FACE = {'G': (0.49, 0.48), 'A': (0.49, 0.44)}      # face centre inside each side-by-side tile
F = lambda base, t: int(round((t - base) * 30))


def add(t, at, dur, **props):
    cues.append({'t': t, 'src': round(at, 2), 'dur': round(dur, 2), 'props': props})


def sfx(at, name, vol=0.4):
    add('sfx', at, 2.0, name=name, volume=vol)


def lock(at, dur, shot):
    locks.append((at - 0.2, at + dur, shot))


def side(at, dur, w=None):
    sp = w or who(at + min(1.0, dur / 2))
    lock(at, dur, sp + 'P')
    return sp


def term(at, dur, term, defn='', example='', exAt=None, en='', sticker='', accent='orange', paper='cream', w=None, exLabel=''):
    dur = min(dur, 9.0)
    if exAt and exAt > at + dur - 2.0: exAt = at + min(dur - 2.0, max(1.5, dur * 0.5))
    sp = side(at, dur, w)
    add('enta_term', at, dur, term=term, example=example, exampleAt=int(((exAt or at + 1.5) - at) * 30), en=en,
        sticker=sticker, accent=accent, paper=paper, pic='', side='left' if sp == 'G' else 'right', top=0.1, exLabel=exLabel)
    cues[-1]['props']['def'] = defn
    sfx(at, 'swish', 0.35); sfx(at + 0.17, 'tape', 0.3)
    if example and exAt: sfx(exAt, 'pop_2', 0.3)


def photos(at, dur, items, snd='pop_1', w=None):
    dur = min(dur, 8.0)
    sp = side(at, dur, w)
    its = [dict(dict(x=0.79, y=0.42, w=420, h=0, at=0, rot=-3, caption='', sepia=False, pos='50% 50%',
                     fit='contain', sticker='', start=0, bare=False), **it) for it in items]
    if sp == 'G':  # guest on the right -> pictures on the left
        for it in its: it['x'] = round(1 - it['x'], 3)
    add('enta_photos', at, dur, items=its)
    for it in items: sfx(at + it.get('at', 0) / 30, snd, 0.35)


def stick(at, items, dur=1.8):
    add('enta_stickers', at, dur, items=[dict(name=n, x=x, y=y, size=s, at=int(d * 30), rot=r) for n, x, y, s, d, r in items])
    for k, it in enumerate(items): sfx(at + it[4], ['pop_1', 'pop_2', 'pop_3'][k % 3], 0.3)


def bubble(at, dur, text, w=None):
    sp = w or who(at + 0.3)
    dur = min(dur, 5.0)
    lock(at, dur, 'two')
    add('enta_bubble', at, dur, text=text, x=0.75 if sp == 'G' else 0.25, y=0.11, tail='right' if sp == 'G' else 'left', w=560)
    sfx(at, 'pop_3', 0.4)


def note(at, text, sticker='', d=4.5, accent='orange'):
    add('enta_note', at, d, text=text, sticker=sticker, side='center', accent=accent); sfx(at, 'paper', 0.3)


def board(a, b, title, items, snd=True):
    """biz_free board from a to b (seconds); item 'at'/'out'/'grey' in ABSOLUTE seconds -> frames from the board start."""
    boards.append((a - 0.3, b + 0.3))
    its = []
    for it in items:
        it = dict(it)
        for key in ('at', 'out', 'grey'):
            if key in it: it[key] = F(a, it[key])
        it.setdefault('at', 8)
        its.append(it)
        if snd and it.get('k') in ('emo', 'pic', 'logo', 'chip', 'sticker'):
            sfx(a + it['at'] / 30, ['pop_1', 'pop_2', 'pop_3'][len(its) % 3], 0.3)
        if snd and it.get('k') == 'mark': sfx(a + it['at'] / 30, 'stamp' if not it.get('ok') else 'pop_2', 0.35)
    add('biz_free', a, b - a, title=title, items=its)
    add('enta_glitch', a - 0.1, 0.3, seed=int(a)); sfx(a - 0.1, 'glitch', 0.25); sfx(a, 'whoosh_2', 0.4)
    add('enta_glitch', b - 0.2, 0.3, seed=int(b)); sfx(b - 0.2, 'whoosh_1', 0.3)


def i(k, **kw): return dict(k=k, **kw)


# ======================================================================= OPENING (Aly, tiny camera) — biz_open
O = lambda t: F(A0, t)
ob = []
def L(k, a, b, **kw): ob.append(dict(k=k, at=O(a), dur=round((b - a) * 30), **kw))
# 17-21 greeting (Aly big, centre): 3rd episode of the show
L('head', 18.4, 21.2, text='الحلقة *التالتة* من انت بتشتغل ايه', x=960, y=150, size=58)
# 21.1-27.6 "أول حلقة من الفليفر بتاع رواد الأعمال": the show's 3 flavours (logos from the intros), رواد الأعمال selected (Aly 2026-10-27)
L('flavours', 21.4, 27.6, items=[dict(src=P + 'pics/flavour_cs.png', ring=[50.6, 10.1, 17, 7.1]), dict(src=P + 'pics/flavour_fnon.png', ring=[50.7, 10.5, 13, 7]),
         dict(src=P + 'pics/flavour_biz.png', ring=[51.8, 10.0, 20.6, 7])],   # ring = measured name box in each logo (+ margin)
  sel=2, selAt=round((23.6 - 21.4) * 30), x=1180, y=560)
L('head', 21.8, 27.6, text='الحلقة *الأولى* في رواد الأعمال', x=1060, y=150, size=50)
sfx(21.4, 'pop_1', 0.35); sfx(21.65, 'pop_2', 0.35); sfx(21.9, 'pop_3', 0.35); sfx(23.6, 'stamp', 0.45)
# 27.9-31.4 "بس الأول عايز أكلمكم على حاجة": biz stickers around one chip, nothing overlaps (Aly left, guest corner top-right)
L('chips', 28.0, 31.4, items=[dict(text='بس الأول… *حاجة مهمة*', emo='index_pointing_up', at=0)], x=1180, y=500)
for n, x, y, sz, d, r in [('bulb', 800, 330, 150, 28.2, -8), ('shop', 1200, 300, 140, 28.35, 8), ('rocket', 1580, 470, 160, 28.5, -6),
                          ('chart_up', 800, 760, 150, 28.65, 6), ('coin', 1100, 790, 130, 28.8, 10), ('briefcase', 1420, 790, 140, 28.95, -10)]:
    L('stk', d, 31.4, name=n, x=x, y=y, size=sz, rot=r); sfx(d, 'pop_2', 0.3)
# 31.4-34 most podcasts host a FAMOUS guest -> Blender podcast studio, push onto the guest's crown -> 34-43 the gold tower
# ONE continuous Blender shot (Aly: the studio is in an apartment; we leave the building and find ourselves in the city): studio
# inside (host pawn + gold queen) -> back out through the window -> over the night city -> the gold tower climbs, coin on 'ملايين'
L('clip', 31.4, 43.2, file=P + 'b3d/b_podcity.webm')
L('head', 31.6, 34.6, text='أغلب *البودكاستات* بتستضيف… ضيف *مشهور*', x=1020, y=120, size=44)
L('big', 38.8, 42.9, text='$ 1,000,000,000', sub='*ملايين* · أرقام كبيرة جدًا', x=1120, y=200, size=90)
sfx(31.4, 'whoosh_2', 0.4); sfx(33.6, 'whoosh_3', 0.35); sfx(35.4, 'riser', 0.3); sfx(36.1, 'impact', 0.35); sfx(38.8, 'cash', 0.45)
# 42.9-53.6 a MIX: starters + people who reached a level, closed and started something else -> Blender road
L('clip', 43.6, 53.9, file=P + 'b3d/b_road.webm')
L('head', 42.9, 45.0, text='الأفضل؟ *ميكس*', x=1100, y=130, size=56)
L('chips', 45.0, 53.6, items=[dict(text='اللي لسه *بيبدأ*', emo='rocket', at=0), dict(text='وصل *لليفل* معين', emo='chart_increasing', at=round((48.5 - 45.0) * 30)),
                              dict(text='*قفل*… ودخل حاجة *تانية*', emo='door', at=round((50.3 - 45.0) * 30))], x=1120, y=110)
sfx(45.2, 'whoosh_1', 0.35); sfx(50.3, 'stamp', 0.35)
# 53-56.9 learn from their experience
L('head', 53.6, 57.2, text='هنتعلم من *تجاربهم* أكتر بكتير', x=1060, y=150, size=52)
# 56.9-67.9 the extreme stories = ~a quarter percent -> Blender crowd (dolly zoom on the golden one, then the many light up)
L('clip', 56.9, 68.4, file=P + 'b3d/b_crowd.webm')
L('chips', 57.6, 59.6, items=[dict(text='التجارب *الإكستريم*', emo='crown', at=0)], x=1120, y=150)
L('big', 59.8, 63.4, text='0.25%', sub='*ربع في المية* من الناس (مثلًا)', x=1120, y=210, size=120)
L('chips', 63.5, 68.4, items=[dict(text='قصص *استثنائية*', emo='glowing_star', at=0), dict(text='ومش كتير من *دوايرنا* وصلها', emo='busts_in_silhouette', at=round((65.5 - 63.5) * 30))], x=1080, y=110)
sfx(57.9, 'stamp', 0.3); sfx(59.8, 'pop_3', 0.4)
# 68.4-74 the guest: curtain opens on "كريم" (big), then he goes to the corner
sfx(71.5, 'whoosh_2', 0.45); sfx(71.6, 'magic', 0.3)
# 74.4-84 GUC in New Cairo: map dive Egypt -> Cairo -> pin on GUC ("جيو سي" 76.8), the real road sign + campus (Commons)
L('map', 74.4, 84.2, zoomAt=24, pinAt=round((76.7 - 74.4) * 30))
sfx(74.4, 'whoosh_1', 0.35); sfx(75.2, 'swoop_up', 0.35); sfx(76.7, 'stamp', 0.45)
L('pics', 76.9, 84.2, items=[dict(src=P + 'pics/guc_logo.jpg', x=1640, y=150, w=300, rot=5, at=0),
                             dict(src=P + 'pics/new_cairo.jpg', x=1560, y=835, w=420, rot=-3, cap='لافتة في التجمع: *GUC*', at=round((78.0 - 76.9) * 30)),
                             dict(src=P + 'pics/guc_desert.jpg', x=1110, y=850, w=380, rot=3, cap='من جوّه *الجامعة*', at=round((79.2 - 76.9) * 30))])
L('chips', 76.3, 84.2, items=[dict(text='خريج *هندسة*', emo='graduation_cap', at=0), dict(text='وحاليًا *شغال*', emo='laptop', at=round((78.6 - 76.3) * 30))], x=320, y=880)
# 80.9-90 the most excited to open his own startup
L('chips', 84.4, 90.6, items=[dict(text='من *أكتر* الناس اللي أعرفها', emo='fire', at=0), dict(text='*متحمس* جدًا يفتح الستارتب بتاعه', emo='rocket', at=round((86.4 - 84.4) * 30))], x=1000, y=820)
L('stk', 86.4, 90.6, name='rocket', x=1600, y=780, size=200, rot=-12)
# 90.8-102.6 three projects one after another -> Blender cards on a timeline
L('clip', 92.4, 102.8, file=P + 'b3d/b_three.webm')
L('head', 96.0, 102.6, text='ليه *تلاتة*؟ · وإيه اللي حصل *بينهم*؟', x=1020, y=120, size=46)
sfx(93.4, 'pop_1', 0.4); sfx(94.6, 'pop_2', 0.4); sfx(95.5, 'pop_3', 0.4)
# 103-122 his projects are different: real pictures of all three
L('head', 104.3, 109.2, text='مشاريعه *مختلفة*', x=1100, y=120, size=56)
L('phone', 105.5, 122.0, items=[dict(src=P + 'web/kikos/p04.jpg'), dict(src=P + 'web/kikos/p06.jpg'), dict(src=P + 'web/kikos/p03.jpg'), dict(src=P + 'web/kikos/p02.jpg')],
  text="kikos.snacks", x=1660, y=600, size=330, rot=5)
# Courzerve (Aly 2026-10-27): first their instructor explaining at a desk in the studio, then the screen recording of their website
L('pics', 107.0, 122.0, items=[dict(src=P + 'web/courzerve/campaign_1.mp4', **{'from': 30 * 108}, x=1160, y=430, w=600, rot=-3, cap='Courzerve · الكورسات', at=0, out=round(6.5 * 30)),
                              dict(src=P + 'web/courzerve/campaign_1.mp4', **{'from': 30 * 82}, x=1160, y=430, w=600, rot=-3, cap='Courzerve · الويبسايت', at=round(6.5 * 30), cut=True),
                              dict(src=P + 'web/fpl/p05.jpg', x=1150, y=830, w=330, rot=3, cap='FPL Champ', at=round((112.5 - 107.0) * 30))])
L('chips', 114.5, 122.0, items=[dict(text='حاجات *بتبيع*', emo='shopping_cart', at=0), dict(text='وحاجات مش بتحصل غير في *شركات كبيرة*', emo='office_building', at=round((117.5 - 114.5) * 30))], x=760, y=880)
# 122.2-124.3 we'll learn all that together
L('head', 122.2, 124.4, text='يلا *نبدأ*!', x=960, y=150, size=72)
cam = [dict(at=0, m='hero'), dict(at=O(21.0), m='left'), dict(at=O(122.0), m='hero')]
guest = dict(src=P + 'karim_open.mp4', label='ضيف الحلقة', name='كريم تامر', openAt=O(71.5),
             pos=[dict(at=O(25.9), m='corner'), dict(at=O(68.4), m='big'), dict(at=O(74.2), m='corner'), dict(at=O(84.3), m='side'), dict(at=O(90.6), m='corner'), dict(at=O(121.8), m='off')])
add('biz_open', A0, 124.3 - A0, cam=cam, guest=guest, layers=ob)
# karim_open.mp4 = his full Meet tile (no crop) from source 17.12 = the cue start -> plays in sync with from 0
sfx(18.4, 'swoop_up', 0.4); sfx(28.0, 'paper', 0.3); sfx(104.3, 'swish', 0.3); sfx(122.2, 'stamp', 0.35)

# ======================================================================= KARIM ALONE (124.3-187.5): his big tile, cards beside him
add('enta_name', S('S048'), 4.0, name='كريم تامر', role='*Software* Engineer', side='left', accent='orange'); sfx(S('S048'), 'swoop_up', 0.45)
lock(S('S048'), 4.0, 'GP')
# 143.3-165.2 Full Time + his own business IN PARALLEL (Aly: the arrow didn't say "على جنب") — two lanes moving together; the
# one year he stopped = a gap in the business lane. Karim in a circle (his face only, never the corner where Meet's menus were).
a, b = 143.3, 165.2
board(a, b, '*Full Time*… و*بيزنس خاص*', [
    i('path', pts=[[330, 520], [1620, 520]], color='blue', w=12, at=a + 0.3, dur=round((b - a - 1.0) * 30)),
    i('walker', n='laptop', pts=[[330, 520], [1620, 520]], s=150, at=a + 0.3, dur=round((b - a - 1.0) * 30), dy=0),
    i('chip', text='*Full Time* · Software Engineer', x=560, y=290, bg='blue', size=34, at=a + 0.5),
    i('num', x=980, y=290, size=72, to=8, suffix=' سنين', at=a + 0.8, dur=14),
    i('path', pts=[[330, 820], [895, 820]], color='mustard', w=12, at=S('S055'), dur=round((T('S057', 'سنة') - S('S055')) * 30)),
    i('walker', n='rocket', pts=[[330, 820], [895, 820]], s=140, at=S('S055'), dur=round((T('S057', 'سنة') - S('S055')) * 30)),
    i('chip', text='و*بيزنس خاص* على جنب', x=560, y=930, bg='mustard', size=34, at=S('S055') + 0.3),
    i('chip', text='سنة واحدة *بس* وقف', x=975, y=930, bg='orange', size=30, at=T('S057', 'سنة')),
    i('path', pts=[[1056, 820], [1620, 820]], color='mustard', w=12, at=S('S058'), dur=round((b - S('S058') - 0.5) * 30)),
    i('walker', n='rocket', pts=[[1056, 820], [1620, 820]], s=140, at=S('S058'), dur=round((b - S('S058') - 0.5) * 30)),
    i('text', text='دايمًا لازم يبقى عنده *حاجة على جنب*', x=1180, y=605, size=34, paper=True, at=S('S058')),
])
KTR = json.load(open(W / 'karim_track.json'))   # Karim's face in source px (work/scripts/karim_track.py) -> the circle never loses him
add('pip', 143.6, 164.9 - 143.6, who='G', side='R', track=KTR)
# 171.4-177.3 "نبقى من القصص الاستثنائية اللي انت بتقول عليها" -> callback to the opening's golden figure
a, b = T('S060', 'القصص') - 0.6, E('S061') + 0.4
board(a, b, 'نبقى من القصص *الاستثنائية*', [
    i('pic', src=P + 'b3d/b_crowd.webm', x=960, y=600, w=1300, ar=16 / 9, bare=True, at=a + 0.2, **{'from': 150}),
    i('chip', text='زي ما علي قال في *الأول*', x=960, y=960, bg='mustard', size=34, at=a + 1.0),
])
add('pip', a + 0.6, b - a - 1.0, who='G', side='R', track=KTR)
note(S('S066'), 'الهدف: *البيزنس الخاص* بيه', sticker='rocket', d=3.5, accent='olive')

# ======================================================================= COURZERVE
note(T('S071', 'كورزيرف') if True else 0, 'المشروع الأول: *Courzerve*', d=4.0, accent='blue')
photos(T('S071', 'كورزيرف'), 4.0, [dict(src=P + 'web/courzerve/logo.jpg', w=260, rot=-4, caption='Courzerve'),
                                    dict(src=P + 'web/courzerve/cz_instructors.jpg', x=0.83, y=0.62, w=420, rot=3, at=10)], w='A')
bubble(T('S074', 'تقفلو'), 3.5, 'الصفحات *اتقفلت*… بس لقيت الماركتنج على Behance', w='A')
photos(S('S077'), E('S080') - S('S077') + 0.3, [dict(src=P + 'web/courzerve/cz_banner.jpg', x=0.8, y=0.34, w=560, rot=-2, caption='الويبسايت'),
                                               dict(src=P + 'web/courzerve/cz_preview.jpg', x=0.84, y=0.7, w=330, rot=4, at=24, caption='Instagram · Facebook')], w='A')
term(S('S089'), 5.0, 'بدأ *في الجامعة*', 'تالتة جامعة… قبل ما يتخرج', '', sticker='star_y', accent='olive', w='G')
# Breadfast story
a, b = S('S091'), S('S095') + 1.0
board(a, b, 'نفس *الفكرة*… في نفس *الوقت*', [
    i('emo', n='sunrise', x=960, y=330, s=200, at=a + 0.3, float=True, out=S('S094')),  # the chip takes its place (no overlap)
    i('text', text='التجمع · كل يوم *الصبح*', x=960, y=470, size=40, at=a + 0.6),
    i('emo', n='motor_scooter', x=560, y=640, s=230, at=a + 0.8), i('emo', n='bread', x=520, y=520, s=120, at=a + 1.0),
    i('chip', text='الستارتب اللي كريم *اشتغل فيها*', x=560, y=820, bg='orange', size=34, at=a + 1.2),
    i('emo', n='motor_scooter', x=1360, y=640, s=230, flip=True, at=T('S091', 'Breakfast') if False else a + 2.4),
    i('logo', src=P + 'pics/breadfast_brand.svg', x=1360, y=470, s=230, pad=0.1, at=a + 2.4),
    i('chip', text='*Breadfast*', x=1360, y=820, bg='mustard', size=40, at=a + 2.6),
    i('arrow', pts=[[560, 900], [960, 960], [1360, 900]], color='mustard', at=S('S092'), dur=18),
    i('text', text='الاتنين *بيوصّلوا العيش*', x=960, y=1000, size=40, at=S('S092') + 0.3),
    i('chip', text='وإحنا بنعمل نفس الحاجة… *أكبر شوية*', x=960, y=330, bg='blue', size=36, at=S('S094'), out=b),
])
photos(S('S096'), 6.0, [dict(src=P + 'pics/breadfast_app.png', x=0.8, y=0.42, w=460, rot=-3, caption='*Breadfast* النهاردة: سوبرماركت في جيبك')], w='G')
term(T('S097', 'روح') if True else S('S097'), 6.5, 'روح *ريادة الأعمال*', 'أي *Vision* عند الفاوندر… بيحاول يطبقه على أرض الواقع', '', sticker='bulb', accent='mustard', w='G')
term(S('S103'), E('S106') - S('S103'), 'أول *غلطة*', 'كان عايز يفتح بيزنس… *من غير* ما يشوف مشكلة يحلها', '', sticker='qmark', accent='orange', w='G')
# Courzerve journey (pivots)
a, b = S('S107'), E('S117') + 0.5
board(a, b, 'رحلة *Courzerve*', [
    i('emo', n='office_building', x=330 + 60, y=540, s=200, at=S('S108')), i('chip', text='حجز *Working Spaces*', x=390, y=700, bg='blue', size=34, at=S('S108') + 0.3),
    i('emo', n='spiral_calendar', x=470, y=420, s=110, at=S('S108') + 0.8, rot=10),
    i('arrow', pts=[[560, 560], [700, 470], [840, 560]], color='orange', at=S('S113'), dur=14),
    i('chip', text='*Pivot* · غيّرنا الاتجاه', x=700, y=380, bg='orange', size=32, at=S('S113') + 0.3),
    i('emo', n='man_teacher', x=960, y=540, s=210, at=T('S114', 'software')), i('chip', text='كورسات *Software Engineering*', x=960, y=720, bg='mustard', size=32, at=T('S114', 'software') + 0.3),
    i('arrow', pts=[[1090, 560], [1230, 470], [1370, 560]], color='orange', at=S('S116'), dur=14),
    i('emo', n='laptop', x=1500, y=540, s=200, at=S('S116') + 0.8), i('logo', src='logos/zoom.svg', x=1600, y=430, s=110, at=S('S116') + 1.2),
    i('chip', text='*أونلاين*', x=1500, y=720, bg='olive', size=36, at=S('S116') + 1.0),
    i('text', text='وفي النص… كذا *Pivot*', x=960, y=900, size=40, at=S('S113') + 1.2),
])
term(T('S113', 'بوب') if False else S('S113'), 3.0, '*Pivot*', 'تغيير *اتجاه* المشروع لما الفكرة الأولانية ماتمشيش', '', en='Pivot', sticker='arrow_y', accent='blue', paper='blue', w='G') if False else None
bubble(S('S118'), E('S125') - S('S118') if E('S125') - S('S118') < 5 else 5.0, 'بقى *يكسب* إمتى؟ وعملت كل ده *إزاي*؟', w='A')
note(S('S122') + 0.2, 'بالبودجت؟ بالعلاقات؟ ولا *بنفسك*؟', d=4.0, accent='mustard')
# what a courses business needs
a, b = S('S129'), E('S139') + 0.4
board(a, b, 'كورسات *Software* = كذا *شِق*', [
    i('emo', n='globe_with_meridians', x=390, y=470, s=180, at=S('S131')), i('chip', text='*Website*', x=390, y=640, bg='blue', at=S('S131') + 0.2),
    i('logo', src='logos/zoom.svg', x=760, y=470, s=170, at=S('S133')), i('chip', text='الكورس على *Zoom*', x=760, y=640, bg='blue', size=32, at=S('S133') + 0.2),
    i('emo', n='handshake', x=1170, y=470, s=180, at=S('S135')), i('chip', text='اتفاقات *الـInstructors*', x=1170, y=640, bg='olive', size=32, at=S('S135') + 0.2),
    i('emo', n='books', x=1540, y=470, s=180, at=S('S136')), i('chip', text='*المحتوى*', x=1540, y=640, bg='mustard', at=S('S136') + 0.2),
    i('mark', ok=True, x=450, y=380, s=100, at=S('S139')),
    i('text', text='أسهل حاجة لينا… *الويبسايت*', x=960, y=860, size=46, at=S('S139') + 0.2),
])
term(S('S141'), E('S144') - S('S141'), 'خليك *صريح* مع نفسك', 'إيه اللي انت *شاطر* فيه… وإيه اللي *لأ*', 'وماتستخبّاش في الـ*Comfort Zone*', exAt=S('S144'),
     sticker='check', accent='olive', w='G')
a, b = S('S146'), E('S158') + 0.4
board(a, b, 'إحنا كنا *Software Engineers*', [
    i('panel', x=700, y=600, w=760, h=520, bg='dark', label='*Comfort Zone*', at=S('S146')),
    i('emo', n='laptop', x=520, y=520, s=150, at=S('S147')), i('chip', text='نكتب *Code*', x=520, y=660, bg='olive', size=34, at=S('S147') + 0.2),
    i('mark', ok=True, x=610, y=430, s=80, at=S('S147') + 0.5),
    i('emo', n='globe_with_meridians', x=860, y=520, s=150, at=T('S147', 'website')), i('chip', text='نعمل *Website*', x=860, y=660, bg='olive', size=34, at=T('S147', 'website') + 0.2),
    i('mark', ok=True, x=950, y=430, s=80, at=T('S147', 'website') + 0.5),
    i('emo', n='megaphone', x=1330, y=430, s=150, at=S('S148')), i('chip', text='*Marketing*', x=1330, y=560, bg='orange', size=34, at=S('S148') + 0.2),
    i('mark', ok=False, x=1430, y=360, s=90, at=S('S149') - 0.2),
    i('emo', n='telephone_receiver', x=1550, y=740, s=140, at=S('S149') + 0.6), i('chip', text='*Sales*', x=1550, y=860, bg='orange', size=34, at=S('S149') + 0.8),
    i('mark', ok=False, x=1650, y=680, s=90, at=S('S149') + 1.6),
    i('text', text='Follow up · مكالمة · *تشرح وتبيع*', x=1120, y=990, size=38, at=S('S152')),
    i('text', text='بنركز في اللي إحنا *أقوية* فيه… ونبعد عن *الضعيف*', x=960, y=250, size=40, at=S('S157'), paper=True),
])
# marketing experiments: his real campaign videos (Behance)
a, b = S('S160'), E('S168') + 0.4
board(a, b, 'الماركتنج = *تجارب*', [
    i('pic', src=P + 'web/courzerve/cz_android.jpg', x=470, y=520, w=420, rot=-4, cap='الأول: *صور*', at=S('S160') + 0.6),
    i('arrow', pts=[[720, 520], [860, 520]], color='mustard', at=S('S160') + 3.0),
    i('pic', src=P + 'web/courzerve/campaign_2.mp4', x=1230, y=500, w=720, ar=16 / 9, rot=2, cap='بعدين: *فيديو*', at=S('S160') + 3.4, **{'from': 30 * 20}),
    i('emo', n='clapper_board', x=420, y=880, s=120, at=S('S161') + 0.6), i('emo', n='camera_with_flash', x=600, y=880, s=120, at=S('S162')),
    i('logo', src='logos/premiere-pro-official.png', x=780, y=880, s=110, pad=0.08, at=T('S162', 'منتاج')), i('emo', n='framed_picture', x=960, y=880, s=120, at=S('S163')),
    i('chip', text='*الكوست* كبيرة', x=690, y=1010, bg='orange', size=34, at=S('S164')),
    i('chip', text='لحد ما تلاقي *الوصفة* اللي تنفع', x=1300, y=900, bg='mustard', size=38, emo='man_cook', at=S('S167')),
])
# founders' roles
a, b = S('S178'), E('S183') + 0.6
board(a, b, 'Courzerve = كذا *Founder*', [
    i('emo', n='man_technologist', x=540, y=500, s=210, at=S('S178') + 0.8), i('chip', text='*Development*', x=540, y=680, bg='blue', at=S('S178') + 1.0),
    i('emo', n='megaphone', x=960, y=500, s=210, at=S('S179')), i('chip', text='*Marketing*', x=960, y=680, bg='orange', at=S('S179') + 0.2),
    i('emo', n='man_office_worker', x=1380, y=500, s=210, at=S('S180')), i('chip', text='كريم: *بيشرف* + Programming', x=1380, y=680, bg='mustard', size=34, at=S('S180') + 0.2),
    i('arrow', pts=[[1380, 760], [960, 860], [540, 760]], color='olive', at=S('S183'), dur=18), i('text', text='أكتر حاجة بتاخد وقت: *ننسّق* بين الناس', x=960, y=930, size=40, at=S('S183') + 0.3),
])
term(S('S193'), E('S199') - S('S193'), 'الـ*Curriculum*', 'المنهج: الكورس بيشرح *إيه* وبالترتيب ده *ليه*', 'المجال بيتطور بسرعة… لازم يكون *مفيد* فعلًا', exAt=S('S198'),
     en='Curriculum', sticker='star_y', accent='blue', paper='blue', w='G')
bubble(S('S201'), 4.5, 'قفلت Courzerve *ليه*؟ وكنت *بتكسب*؟', w='A')
a, b = S('S212'), E('S215') + 0.5
board(a, b, 'كسب… خسارة… *كسب*', [
    i('path', pts=[[260, 600], [480, 420], [700, 760], [920, 400], [1140, 780], [1360, 460], [1580, 700], [1700, 620]], color='mustard', w=12, at=S('S212') + 1.0, dur=60),
    i('chip', text='أكسب في *كورس*', x=480, y=330, bg='olive', size=34, at=S('S213')), i('chip', text='أخسر في *اللي بعده*', x=700, y=860, bg='orange', size=34, at=S('S213') + 1.8),
    i('emo', n='face_with_spiral_eyes', x=1500, y=300, s=180, at=S('S215')), i('text', text='مرهق و*Stressful*… مش *متحمس*', x=1160, y=960, size=42, at=S('S215') + 0.3),
])
photos(S('S216'), 4.2, [dict(src='fluent/studio_microphone.png', w=200, rot=-6, caption='البودكاستات: "*عافر*!"', bare=True)], w='G')
# The Dip
a, b = S('S220'), E('S228') + 0.4
dip = [[300, 420], [520, 470], [700, 600], [860, 820], [980, 870], [1110, 820], [1300, 600], [1500, 430], [1640, 380]]
board(a, b, '*The Dip* · Seth Godin', [
    i('pic', src=P + 'pics/the_dip.jpg', x=330, y=640, w=260, rot=-5, at=S('S220') + 0.4),
    i('path', pts=dip, color='blue', w=14, at=S('S221'), dur=40),
    i('walker', n='person_walking', pts=dip[:5], s=110, at=S('S222'), dur=70),
    i('chip', text='*الحفرة*: النقطة اللي بتنزل فيها *تحت قوي*', x=980, y=990, bg='orange', size=34, at=S('S222') + 0.4),
    i('chip', text='تكمّل؟', x=1400, y=470, bg='olive', size=40, emo='flexed_biceps', at=S('S223') + 2.5),
    i('chip', text='ولا *تقف*؟', x=1400, y=600, bg='orange', size=40, emo='stop_sign', at=S('S223') + 3.5),
    i('text', text='هتبقى *أحسن واحد* في العالم بتاعك؟', x=1000, y=300, size=46, paper=True, at=S('S226') + 1.5),
])
a, b = S('S228'), E('S234') + 0.4
board(a, b, 'أحسن واحد *بيلمّ الليلة*', [
    i('logo', src='logos/mcdonalds.svg', x=520, y=420, s=200, at=S('S230') + 2.0),
    i('bar', x=520, y=900, w=230, h=380, color='mustard', label='60–70%؟', at=S('S232'), dur=24),
    i('logo', src='logos/kfc.svg', x=1180, y=420, s=150, at=S('S229') + 1.5), i('logo', src='logos/burgerking.svg', x=1380, y=420, s=150, at=S('S229') + 2.5),
    i('emo', n='fork_and_knife_with_plate', x=1580, y=430, s=140, at=S('S233')),
    i('bar', x=1380, y=900, w=520, h=150, color='blue', label='*3000* مطعم… في الباقي', at=S('S233'), dur=24),
    i('text', text='مثال كريم · الأرقام *تقريبية*', x=960, y=1000, size=30, at=S('S232') + 0.5),
])
note(S('S240'), 'ماينفعش *تحارب* العالم بتاعك… لازم يكون *محتاجك*', d=4.5, accent='olive')
term(S('S261'), E('S268') - S('S261') + 0.5, 'لو انت *تحت*', 'ومفيش *علامات إيجابية* تكمل عشانها', 'يبقى لازم *تفوق*… وتقفل', exAt=S('S265'), sticker='qmark', accent='orange', w='G')
note(S('S272'), 'Courzerve: *2019* → *2021* · قرب سنتين', d=4.0, accent='blue')
# the 4-month system nobody asked for — comic strip
a, b = S('S278'), E('S296') + 0.5
board(a, b, '*4 شهور* شغل… راحوا في كده', [
    i('panel', x=500, y=480, w=760, h=380, label='1', at=S('S279')),
    i('emo', n='man_office_worker', x=330, y=490, s=170, at=S('S279')), i('emo', n='speech_balloon', x=470, y=380, s=110, at=S('S279') + 0.5),
    i('text', text='محتاج *سيستم*\nللـWorking Space والحجوزات', x=650, y=505, size=32, paper=True, at=S('S280')),
    i('panel', x=1420, y=480, w=760, h=380, label='2', at=S('S282')),
    i('emo', n='man_technologist', x=1180, y=490, s=140, at=S('S282')), i('emo', n='man_technologist', x=1330, y=490, s=140, at=S('S282') + 0.3),
    i('emo', n='man_technologist', x=1480, y=490, s=140, at=S('S282') + 0.6),
    i('num', from_=0, to=4, x=1660, y=400, size=80, suffix=' شهور', at=S('S283'), dur=30, **{'from': 0}),
    i('chip', text='*4 ساعات* كل يوم بعد الجامعة', x=1420, y=615, bg='mustard', size=30, at=S('S284')),
    i('panel', x=500, y=905, w=760, h=320, label='3', at=S('S286')),
    i('emo', n='spiral_calendar', x=380, y=910, s=160, at=S('S286')), i('chip', text='شبه *Google Calendar*', x=640, y=915, bg='blue', size=32, at=S('S286') + 0.3),
    i('emo', n='trophy', x=820, y=835, s=100, at=S('S287')),
    i('panel', x=1420, y=905, w=760, h=320, label='4', at=S('S287') + 1.5),
    i('emo', n='door', x=1170, y=905, s=150, at=S('S288')), i('emo', n='sleeping_face', x=1360, y=900, s=150, at=S('S289')),
    i('emo', n='pouting_face', x=1360, y=900, s=150, at=S('S290')),
    i('text', text='"*انتو مين*؟!"', x=1610, y=865, size=40, paper=True, at=S('S291')),
    i('text', text='"لا… *مش عايز*"', x=1610, y=960, size=36, paper='blue', at=S('S292')),
    i('mark', ok=False, x=1680, y=790, s=100, at=S('S296')),
], snd=True)
cues[[k for k, c in enumerate(cues) if c['t'] == 'biz_free'][-1]]['props']['items'] = [dict(it, **({'from': 0} if it.get('k') == 'num' else {})) for it in cues[[k for k, c in enumerate(cues) if c['t'] == 'biz_free'][-1]]['props']['items']]
sfx(S('S289'), 'pop_3', 0.35); sfx(S('S290'), 'buzz_wrong', 0.25)
term(S('S303'), E('S315') - S('S303'), 'الحماس *مش* ضمان', 'إنك متحمس لفكرة… مش معناه إن الناس *هتدفع*', 'الضمان الوحيد: الناس *تدفع فعلًا*', exAt=S('S312'),
     sticker='coin', accent='mustard', w='G')
bubble(S('S317'), 4.0, 'لو رجع بيك الزمن… *ومعاك AI*… تفتحه تاني؟', w='A')
note(S('S323'), '"معتقدش… *لا خالص*"', d=3.0, accent='orange')
a, b = S('S330'), E('S337') + 0.4
board(a, b, '*Learn by Doing*', [
    i('emo', n='robot', x=560, y=520, s=240, at=S('S332')), i('chip', text='الـ*AI* = مدرس خصوصي', x=560, y=720, bg='blue', size=36, at=S('S336')),
    i('emo', n='memo', x=1000, y=480, s=150, at=S('S336') + 0.8), i('chip', text='بيعمل لك *امتحانات*', x=1000, y=640, bg='mustard', size=32, at=S('S336') + 1.0),
    i('emo', n='hammer_and_wrench', x=1400, y=500, s=180, at=S('S330') + 0.5), i('chip', text='تتعلم *وانت بتطبّق*', x=1400, y=680, bg='olive', size=34, at=S('S331')),
])
# ======================================================================= KIKO'S SNACKS
note(S('S349'), 'المشروع التاني: *Kiko\'s Snacks*', d=4.0, accent='orange')
photos(S('S349'), 6.0, [dict(src=P + 'web/kikos/profile.jpg', w=200, rot=-4, round=True), dict(src=P + 'web/kikos/p07.jpg', x=0.82, y=0.62, w=420, rot=3, at=12, caption="*Kiko's* Snacks")], w='A')
term(S('S351'), E('S353') - S('S351') + 0.4, '*Small Business*', 'بيزنس صغير… أوقع من كلمة *Startup*', '', en='Small Business', sticker='shop', accent='olive', w='G')
note(S('S364'), 'وعمل *نفس الغلطة* تاني 🔁', d=3.6, accent='orange')
a, b = S('S372'), E('S375') + 1.0
board(a, b, 'عالم *جديد*… مفيش فيه منافسة', [
    i('emo', n='clapper_board', x=420, y=520, s=200, at=S('S373')), i('chip', text='سناكس *السينما*', x=420, y=700, bg='orange', size=34, at=S('S373') + 0.3),
    i('emo', n='popcorn', x=820, y=500, s=170, at=S('S373') + 1.4, float=True),
    i('arrow', pts=[[560, 520], [760, 420], [1060, 420], [1260, 520]], color='mustard', at=S('S373') + 1.6, dur=24),
    i('emo', n='motor_scooter', x=960, y=540, s=150, at=S('S373') + 2.2),
    i('emo', n='house', x=1400, y=520, s=200, at=S('S373') + 2.8), i('chip', text='لحد *البيت*', x=1400, y=700, bg='blue', size=34, at=S('S373') + 3.0),
    i('emo', n='crown', x=1400, y=330, s=150, at=S('S374') + 1.0, rot=-8),
    i('text', text='مفيش منافسة… يبقى أنا *الأحسن* في العالم ده', x=960, y=900, size=42, paper=True, at=S('S374') + 1.2),
    i('pic', src=P + 'web/kikos/p03.jpg', x=1700, y=790, w=280, rot=6, at=S('S375')),
])
note(T('S376', 'الجيش'), 'وكان فيه كمان *فترة الجيش*', d=3.5, accent='olive')
photos(S('S377'), 6.0, [dict(src=P + 'web/kikos/p02.jpg', w=360, rot=-3, caption='*ريسيبيز* + موردين'), dict(src=P + 'web/kikos/p09.jpg', x=0.84, y=0.66, w=320, rot=4, at=14)], w='G')
note(S('S384'), 'Courzerve خلص أول *2021* · Kiko\'s بدأ نص *2021*', d=4.5, accent='blue')
term(S('S392'), 7.0, 'بيزنس *أكل*', 'الأكل لو ما اتباعش… ممكن *يبوظ*', 'ومحتاج *Investment* (فلوس تتحط) في الأول', exAt=S('S396'), en='Investment', sticker='coin', accent='orange', w='G')
a, b = S('S427'), E('S433') + 0.4
board(a, b, '*4 ساعات* ولا *14 ساعة*؟', [
    i('logo', src='logos/vscode.svg', x=520, y=250, s=110, at=S('S427')), i('chip', text='الوظيفة: *Software*', x=520, y=370, bg='blue', size=34, at=S('S427') + 0.2),
    i('bar', x=430, y=920, w=140, h=110, color='blue', label='*4* ساعات', at=S('S427') + 0.8),
    i('bar', x=610, y=920, w=140, h=360, color='mustard', label='فلوس ×*أضعاف*', at=S('S428'), dur=26),
    i('emo', n='popcorn', x=1380, y=250, s=110, at=S('S428') + 1.5), i('chip', text="*Kiko's* · 11 الصبح → 2 الفجر", x=1380, y=370, bg='orange', size=32, at=S('S429')),
    i('bar', x=1290, y=920, w=140, h=360, color='orange', label='*14* ساعة', at=S('S431') - 1.5, dur=26),
    i('bar', x=1470, y=920, w=140, h=90, color='mustard', label='فلوس', at=S('S431')),
    i('emo', n='alarm_clock', x=960, y=640, s=150, at=S('S429') + 1.0, float=True),
])
a, b = S('S434'), E('S444') + 0.5
board(a, b, 'عشان يكمل… لازم *يضاعف السعر*', [
    i('emo', n='popcorn', x=640, y=520, s=260, at=S('S438')),
    i('num', x=1180, y=480, size=150, to=90, suffix=' جنيه', at=S('S439'), dur=20, color='olive', out=S('S442')),
    i('num', x=1180, y=480, size=150, to=200, suffix=' جنيه', at=S('S442'), dur=24, color='orange', **{'from_': 0}),
    i('chip', text='العلبة كانت *90*… هتبقى *200*؟', x=960, y=760, bg='mustard', size=38, at=S('S442') + 0.6),
    i('text', text='وهي أصلًا حاجة *رفاهية*', x=960, y=900, size=44, paper=True, at=S('S444')),
])
for c in cues:  # 'num' items: 'from' is the start value (default 0); the 90 -> 200 one counts up from 90
    if c['t'] == 'biz_free':
        for it in c['props']['items']:
            if it.get('k') == 'num':
                it.pop('from_', None); it.setdefault('from', 0)
cues[-6 if False else len(cues) - 1]
for c in cues:
    if c['t'] == 'biz_free' and c['props']['title'].startswith('عشان يكمل'):
        c['props']['items'][2]['from'] = 90
term(S('S447'), E('S450') - S('S447') + 0.4, 'الـ*Need* في السوق', 'ماتبصش بس على الفكرة اللي *بتحبها*', 'بُص على اللي الناس *محتاجاه فعلًا*', exAt=S('S450'), en='Market Need', sticker='check', accent='olive', w='A')
# ======================================================================= FPL CHAMP
note(S('S462'), 'المشروع التالت: *FPL Champ* · أقرب لمجاله', d=4.5, accent='olive')
a, b = S('S469'), E('S486') + 0.4
board(a, b, '*Fantasy* Premier League', [
    i('emo', n='soccer_ball', x=430, y=470, s=200, at=S('S470'), float=True), i('chip', text='لعبة مربوطة *بالدوري الإنجليزي*', x=430, y=650, bg='olive', size=32, at=S('S470') + 0.3),
    i('chip', text='اللي بيحصل *في الواقع*… بيحصل في اللعبة', x=960, y=300, bg='blue', size=34, at=S('S475')),
    i('emo', n='goal_net', x=900, y=520, s=170, at=S('S477')), i('chip', text='جون = *نقط*', x=900, y=680, bg='mustard', size=34, at=S('S477') + 0.3),
    i('emo', n='handshake', x=1220, y=520, s=150, at=S('S478')), i('chip', text='أسيست = *نقط*', x=1220, y=680, bg='mustard', size=34, at=S('S478') + 0.3),
    i('emo', n='trophy', x=1560, y=500, s=190, at=S('S479')), i('chip', text='أكتر نقط = *تكسب صحابك*', x=1560, y=680, bg='orange', size=32, at=S('S479') + 0.3),
    i('text', text='شرح *مبسط جدًا*', x=960, y=880, size=34, at=S('S480')),
    i('pic', src=P + 'web/fpl/p05.jpg', x=640, y=880, w=280, rot=-5, at=S('S484')), i('pic', src=P + 'web/fpl/p09.jpg', x=1300, y=880, w=280, rot=5, at=S('S486')),
], snd=True)
photos(S('S487'), 6.0, [dict(src=P + 'web/fpl/p07.jpg', w=380, rot=-3, caption='Highlights على *الويبسايت*'), dict(src=P + 'web/fpl/p11.jpg', x=0.84, y=0.66, w=330, rot=4, at=14)], w='G')
term(S('S491'), E('S496') - S('S491') + 0.4, '*Passive Income*', 'دخل بييجي *لوحده* تقريبًا من غير شغل يومي', 'هنا: *اشتراك شهري* (Subscription)', exAt=S('S495'), en='Passive Income', sticker='coin', accent='mustard', w='G')
note(S('S505'), 'مع سرعة *AI*… فيه *Gap* في السوق لازم يستغله', d=4.5, accent='blue')
term(S('S517'), 7.0, 'المشروع *الجديد*', 'تتخيّل *بيتك* وتفرشه قبل ما تشتري', 'اللينك *في الوصف*', exAt=S('S524'), sticker='shop', accent='olive', w='G')
# ======================================================================= AI + the 5 pillars
bubble(S('S528'), 5.0, 'في عصر *AI*… إيه *الـEdge* اللي يخليك تنجح؟', w='A')
cols = [('الفكرة', 'light_bulb', 'mustard', 'S542'), ('التنفيذ', 'hammer_and_wrench', 'olive', 'S543'), ('الفريق', 'busts_in_silhouette', 'blue', 'S544'),
        ('الفلوس', 'money_bag', 'orange', 'S545'), ('التوقيت', 'alarm_clock', 'blue', 'S546')]
a, b = S('S540'), E('S563') + 0.5
its = []
for k, (nm, em, c, sid) in enumerate(cols):
    x = 360 + k * 300
    its += [i('bar', x=x, y=900, w=170, h=360, color=c, at=S(sid), dur=16), i('emo', n=em, x=x, y=420, s=130, at=S(sid) + 0.2),
            i('chip', text=nm, x=x, y=980, bg=c, size=34, at=S(sid))]
its[2 * 3 + 0]['grey'] = S('S559'); its[3 * 3 + 0]['grey'] = S('S559')
its += [i('emo', n='robot', x=1500, y=280, s=170, at=S('S554'), float=True), i('chip', text='بقوا على *AI*', x=1250, y=260, bg='blue', size=36, at=S('S554') + 0.3),
        i('text', text='*خمس* عوامل أساسية لأي بيزنس', x=960, y=300, size=40, at=S('S541'), out=S('S554') - 0.2)]
board(a, b, 'عشان أي بيزنس *ينجح*', its)
a, b = S('S566'), E('S588') + 0.4
board(a, b, 'زمان كنت *محتاج*…', [
    i('emo', n='artist', x=420, y=480, s=170, at=S('S568')), i('chip', text='*Graphic* Designer', x=420, y=640, bg='olive', size=30, at=S('S568') + 0.2),
    i('emo', n='man_technologist', x=780, y=480, s=170, at=S('S569')), i('chip', text='*Developers*', x=780, y=640, bg='blue', size=30, at=S('S569') + 0.2),
    i('emo', n='telephone_receiver', x=1140, y=480, s=170, at=S('S570')), i('chip', text='*Sales*', x=1140, y=640, bg='orange', size=30, at=S('S570') + 0.2),
    i('emo', n='megaphone', x=1500, y=480, s=170, at=S('S570') + 0.8), i('chip', text='*Marketing*', x=1500, y=640, bg='mustard', size=30, at=S('S570') + 1.0),
    i('strike', x=960, y=560, w=1350, at=S('S573')),
    i('text', text='دلوقتي… *مش محتاج* حد منهم', x=960, y=780, size=46, paper=True, at=S('S573') + 0.3),
    i('emo', n='robot', x=700, y=930, s=130, at=S('S583')), i('chip', text='اشتراك *AI*… بدل *فريق كامل*', x=1080, y=930, bg='blue', size=34, at=S('S583') + 0.3),
])
a, b = S('S588'), E('S602') + 0.5
its = []
for k, (nm, em, c, sid) in enumerate(cols):
    x = 360 + k * 300
    gone = nm in ('الفريق', 'الفلوس')
    its += [i('bar', x=x, y=900, w=170, h=360, color=c, at=a + 0.3 + k * 0.15, dur=10, **({'grey': a + 1.5} if gone else {})),
            i('emo', n=em, x=x, y=420, s=130, at=a + 0.4 + k * 0.15, **({'grey': a + 1.5} if gone else {})), i('chip', text=nm, x=x, y=980, bg=c, size=34, at=a + 0.4 + k * 0.15)]
its += [i('chip', text='الفكرة = *بتاعتك*… رأيك و*ذوقك*', x=960, y=270, bg='mustard', size=34, at=S('S589'), out=S('S592')),
        i('chip', text='والتوقيت: الناس *محتاجاه دلوقتي*؟', x=960, y=270, bg='blue', size=34, at=S('S592')),
        i('text', text='بدل *5 عواميد*… محتاج *3* بس', x=960, y=260, size=46, paper=True, at=S('S600'))]
its[-2]['out'] = S('S600') - 0.2
board(a, b, '', its)
term(S('S607'), E('S619') - S('S607'), 'الشراكة', 'على حسب *الشريك*: حد تقدر *تختلف* معاه من غير ما تخاف', 'مالقيتش ده؟ الأحسن *تكمّل لوحدك*', exAt=S('S618'), sticker='briefcase', accent='blue', paper='blue', w='G')
bubble(S('S624'), 5.0, 'البيزنس عشان *دخل جانبي*… ولا *تسيب الوظيفة*؟', w='A')
term(S('S631'), E('S640') - S('S631'), 'هدف كريم', 'يصحى يحس *بالفخر*', 'إن *البيزنس بتاعه* هو اللي معيّشه', exAt=S('S638'), sticker='star_y', accent='mustard', w='G')
a, b = S('S643'), E('S646') + 0.5
board(a, b, 'عمره ما فكر في *الفلوس* الأول', [
    i('emo', n='person_raising_hand', x=640, y=520, s=200, at=S('S645')), i('chip', text='أول *زبون*', x=640, y=700, bg='olive', size=36, at=S('S645') + 0.2),
    i('arrow', pts=[[780, 520], [1080, 520]], color='mustard', at=S('S645') + 0.8),
    i('num', x=1300, y=520, size=150, to=10, prefix='×', at=S('S645') + 1.0, dur=20, **{'from': 1}), i('chip', text='عايز *عشرة*!', x=1300, y=700, bg='orange', size=36, at=S('S645') + 1.2),
    i('text', text='وبعدها… أصلّح الحتة اللي *بخسر* فيها', x=960, y=880, size=40, at=S('S646')),
])
# comfort myth: the iceberg
a, b = S('S671'), E('S690') + 0.5
berg = [[960, 360], [1080, 470], [1150, 560], [1220, 640], [700, 640], [780, 540], [860, 430]]
under = [[700, 640], [1220, 640], [1380, 790], [1300, 960], [960, 1040], [600, 950], [520, 790]]
board(a, b, 'البيزنس *المريح*؟', [
    i('text', text='هدفك *الراحة*؟ … دي *أسوأ* حاجة', x=960, y=250, size=44, paper=True, at=S('S672'), out=S('S678')),
    i('chip', text='9 لـ 5', x=420, y=420, bg='blue', size=36, at=S('S678')), i('chip', text='جمعة وسبت *أجازة*', x=420, y=520, bg='blue', size=32, at=S('S679')),
    i('chip', text='21 يوم *أجازة*', x=420, y=620, bg='blue', size=34, at=S('S680')), i('mark', ok=False, x=560, y=520, s=120, at=S('S682')),
    i('poly', pts=under, fill='rgba(70,110,160,.55)', at=S('S686'), grow=False, dur=20),
    i('poly', pts=berg, fill='#EFE6D2', at=S('S683'), dur=18),
    i('wave', y=640, amp=10, fill='rgba(60,100,150,.35)', at=S('S683'), speed=14),
    i('emo', n='beach_with_umbrella', x=960, y=330, s=150, at=S('S684')), i('chip', text='60 سنة · شركة · *بيصيّف*', x=1450, y=360, bg='mustard', size=32, at=S('S684') + 0.3),
    i('emo', n='man_technologist', x=820, y=760, s=120, at=S('S686')), i('emo', n='crescent_moon', x=1000, y=730, s=110, at=S('S686') + 0.4),
    i('emo', n='alarm_clock', x=1130, y=850, s=110, at=S('S686') + 0.8), i('emo', n='chart_decreasing', x=880, y=920, s=110, at=S('S687')),
    i('chip', text='اللي *تحت المية*: كان بيعمل إيه عشان يوصل', x=1450, y=860, bg='blue', size=30, at=S('S687')),
])
term(S('S695'), E('S700') - S('S695'), 'ولا حتى *عشان الفلوس*', 'الوظيفة = دخل *ثابت* على طول', 'البيزنس… عبال ما يوصل لدخلك *حرقت وقت*', exAt=S('S698'), sticker='coin', accent='orange', w='A')
term(S('S704'), E('S712') - S('S704'), '*سقف* الدخل', 'لو قربت توصل *لسقف* مجالك (Senior / Manager)', 'ساعتها تفكر في بيزنس *تعدّي* بيه السقف', exAt=S('S711'), sticker='chart_up', accent='blue', paper='blue', w='A')
bubble(S('S715'), 5.0, 'بتجيب *أول عميل* إزاي؟', w='A')
note(S('S724'), 'اعرف هتوصل *لعملائك* إزاي… *قبل* ما تبدأ', d=5.0, accent='mustard')
# how each project reached its customers
a, b = S('S731'), E('S752') + 0.4
board(a, b, 'كل بيزنس *وصل لعملاؤه* إزاي؟', [
    # panels start at y 330 so the speaker circle (top right) never covers the 'FPL Champ' label
    i('panel', x=380, y=650, w=560, h=640, bg='dark', label='Courzerve', at=S('S731')),
    i('pic', src=P + 'web/courzerve/campaign_3.mp4', x=380, y=560, w=480, ar=16 / 9, rot=-2, at=S('S732'), **{'from': 30 * 30}),
    i('logo', src='logos/youtube-icon.svg', x=290, y=770, s=110, at=S('S733')), i('logo', src='logos/instagram.svg', x=460, y=770, s=110, at=S('S733') + 0.4),
    i('chip', text='*Video Ads*', x=380, y=915, bg='blue', size=34, at=S('S732') + 0.3),
    i('panel', x=960, y=650, w=560, h=640, bg='dark', label="Kiko's", at=S('S735')),
    i('pic', src=P + 'web/kikos/p06.jpg', x=960, y=545, w=330, rot=2, at=S('S736')),
    i('emo', n='woman_cook', x=1175, y=700, s=100, at=S('S738')), i('chip', text='*Food Bloggers*', x=960, y=915, bg='orange', size=34, at=S('S738') + 0.3),
    i('text', text='سنتين… من غير ما يدفع\nتقريبًا في *الإعلانات*', x=960, y=790, size=28, at=S('S743')),
    i('panel', x=1540, y=650, w=560, h=640, bg='dark', label='FPL Champ', at=S('S747')),
    i('pic', src=P + 'web/fpl/p01.jpg', x=1540, y=585, w=300, rot=-2, at=S('S747') + 0.4),
    i('emo', n='speech_balloon', x=1440, y=820, s=90, at=S('S749')), i('chip', text='مجتمع *Reddit*', x=1600, y=820, bg='olive', size=30, at=S('S750')),
    i('chip', text='*Paid Collab* مع Influencers', x=1540, y=915, bg='mustard', size=28, at=S('S752')),
])
term(S('S753'), E('S755') - S('S753'), '*Storytelling*', 'تحكي *قصة* بتفيد الناس… مش إعلان بحت', 'بيشرح بشكل *مبسط*… والناس تستفيد', exAt=S('S754'), en='Storytelling', sticker='star_y', accent='mustard', w='G')
bubble(S('S756') + 2.0, 5.0, 'لو رجعت لكريم *2019*… تنصحه بإيه؟', w='A')
# advice: don't stubborn-push, know when to throw in the towel
a, b = S('S763'), E('S779') + 0.4
board(a, b, '*ماتقاوحش* كتير', [
    i('emo', n='boxing_glove', x=560, y=520, s=220, at=S('S764'), rot=-10),
    i('chip', text='إمتى *تتعلم*؟', x=1180, y=400, bg='blue', size=38, emo='books', at=S('S767')),
    i('chip', text='إمتى *تقاوح*؟', x=1180, y=520, bg='olive', size=38, emo='flexed_biceps', at=T('S767', 'تقوح')),
    i('chip', text='وإمتى *ترمي المنديل*… أو تغيّر؟', x=1180, y=640, bg='orange', size=36, emo='white_flag', at=S('S768')),
    i('text', text='حط لنفسك *Targets* من الأول:\nلو ما حققتش كذا… *هغيّر*', x=960, y=860, size=38, paper=True, at=S('S775')),
])
note(S('S783'), 'كتير من الناس *جربوا* حاجة… وفرقت معاهم *جدًا*', d=4.5, accent='olive')
a, b = S('S797'), E('S811') + 0.4
board(a, b, 'فيه *Gap* دلوقتي', [
    i('panel', x=480, y=620, w=640, h=520, bg='blue', label='فاهمين *AI*', at=S('S801')),
    i('emo', n='rocket', x=480, y=600, s=200, at=S('S803') - 1.0, float=True),
    i('panel', x=1440, y=620, w=640, h=520, bg='dark', label='لسه *مش فاهمين*', at=S('S803')),
    i('emo', n='thinking_face', x=1440, y=600, s=180, at=S('S803') + 0.3),
    i('arrow', pts=[[1180, 860], [960, 950], [760, 860]], color='mustard', at=S('S807'), dur=20),
    i('chip', text='*Sooner or later* هييجوا', x=960, y=990, bg='mustard', size=32, at=S('S807') + 0.3),
    i('text', text='يبقى عندك *فرصة* تمشي بسرعة', x=960, y=270, size=44, paper=True, at=S('S805')),
])
term(S('S816'), 5.5, '*MVP*', 'أول نسخة *بسيطة* من المنتج… الناس تجرّبها وتحبها', '', en='Minimum Viable Product', sticker='rocket', accent='orange', w='G')
# Aly: the AI pyramid + exponential
a, b = S('S820'), E('S839') + 0.4
pyr = [[960, 330], [1460, 960], [460, 960]]
board(a, b, 'هرم *AI*', [
    i('poly', pts=pyr, fill='rgba(92,139,192,.35)', at=S('S820') + 0.5, dur=18),
    i('poly', pts=[[960, 330], [1040, 430], [880, 430]], fill='#E8B54A', at=S('S821'), grow=False, dur=12),
    i('chip', text='~*20 مليون* · بيدفعوا ويستخدموه *صح*', x=1340, y=380, bg='mustard', size=30, at=S('S821') + 0.3),
    i('text', text='والباقي… بيستخدموه *Free* أو مش بيستخدموه', x=960, y=820, size=34, at=S('S824')),
    i('chip', text='20 مليون', x=420, y=560, bg='olive', size=34, at=S('S836')), i('chip', text='100 مليون', x=420, y=680, bg='blue', size=36, at=S('S837')),
    i('chip', text='*1 بليون*', x=420, y=800, bg='orange', size=40, at=S('S839')), i('emo', n='chart_increasing', x=420, y=420, s=130, at=S('S834')),
    i('text', text='رقم تقريبي من صورة علي شافها · مش إحصائية', x=960, y=1020, size=26, at=S('S821') + 0.5),
])
term(S('S834'), 3.0, '*Exponential*', 'بيكبر *أضعاف* مش بالجمع', '', en='Exponential', sticker='chart_up', accent='blue', paper='blue', w='A') if False else None
bubble(S('S853'), 5.0, 'لو *AI* قدر ياخد *شغلانتك*… تعمل إيه؟', w='A')
term(S('S876'), E('S885') - S('S876'), '*عزة النفس* في الـSkill', 'اتعلمت حرفة سنين… وفجأة *زرار* يعملها', 'لازم *تتخلى* عنها… وإلا الناس هتسبقك', exAt=S('S885'), sticker='qmark', accent='orange', w='G')
photos(S('S903'), 5.0, [dict(src='fluent/video_game.png', w=200, rot=-8, caption='مش *5 ساعات* PlayStation 😄', bare=True)], w='G')
a, b = S('S906'), E('S915') + 0.4
board(a, b, '*موجة* الـAI', [
    i('wave', y=700, amp=55, at=S('S906'), speed=8),
    i('walker', n='person_surfing', pts=[[300, 0], [1500, 0]], s=230, at=S('S908'), dur=round((E('S913') - S('S908')) * 30), wave=dict(y=700, amp=55, speed=8, at=0), dy=-40),
    i('text', text='*اركبها*… وشوف رايحة فين', x=960, y=300, size=48, paper=True, at=S('S908')),
    i('chip', text='ماتتمسّكش *أوي* بأفكارك', x=960, y=440, bg='orange', size=36, at=S('S914')),
])
for c in cues:  # walker riding the wave: its wave 'at' = board start (frames)
    if c['t'] == 'biz_free' and c['props']['title'] == '*موجة* الـAI':
        for it in c['props']['items']:
            if it.get('k') == 'walker': it['wave']['at'] = it['at'] - F(a, S('S908')) if False else 0
photos(S('S921'), 5.5, [dict(src='logos/claude.svg', w=200, rot=-5, caption='الحلقة دي اتعمل موشن بـ*Claude*', bare=True)], w='A')
note(S('S924'), 'علي اتعلم *موشن جرافيك* وعمل فيه كورسات… ودلوقتي AI بيعمله', d=5.0, accent='olive')
photos(S('S941'), 6.0, [dict(src='logos/instagram.svg', w=150, rot=-6, bare=True), dict(src='logos/facebook.svg', x=0.71, y=0.5, w=150, rot=5, at=8, bare=True),
                        dict(src='logos/youtube-icon.svg', x=0.86, y=0.42, w=160, rot=-3, at=16, bare=True)], w='A')
note(S('S941') + 6.2, 'ريل *كل يوم*: Instagram · Facebook · YouTube', d=4.0, accent='orange')
note(S('S950'), 'مفيش وقت *تقعد تفكر*… حاول *تتصرف*', d=4.5, accent='orange')
note(S('S966'), 'لينك مشروع كريم الجديد *في الوصف*', d=5.0, accent='mustard')
stick(S('S970'), [('star_y', 0.43, 0.12, 110, 0, -10), ('spark_o', 0.5, 0.09, 90, 0.15, 0), ('star8_b', 0.57, 0.12, 100, 0.3, 10)], 2.4)

# ======================================================================= fillers in the long empty stretches (each on what is said)
bubble(S('S169'), 4.5, 'إيه المهام اللي كانت بتاخد *أكتر وقت*؟', w='A')
note(S('S188'), 'أول ما الناس *جت*… الشغل بقى *إشراف*', d=4.5, accent='blue')
note(S('S191'), 'اتفاقات الـ*Instructors* · والحسابات', d=4.0, accent='olive')
term(S('S235'), E('S236') - S('S235'), 'شهادات *معتمدة*', 'عملاء Courzerve كانوا عايزين *شهادات* من جهات معينة', 'وكريم مقتنع إنها في الـ*Software* مش هتفرق', exAt=S('S236'),
     sticker='star_y', accent='blue', paper='blue', w='G')
note(S('S253'), 'مش لازم تبقى *الأول*… لو المكسب *كويس* يكفي', d=5.0, accent='olive')
note(S('S258') + 0.3, 'مبيعاتك كويسة؟ *العالم كبير* ويكفي', d=4.0, accent='mustard')
term(S('S338'), E('S339') - S('S338'), '*Accountability*', 'حد *يحاسبك*: دفعت فلوس… ومواعيد في الأسبوع', 'عشان كده الكورسات لسه بتفيد ناس', exAt=S('S339'), en='Accountability',
     sticker='check', accent='mustard', w='G')
note(S('S367'), 'شريك جديد: حد اتعامل معاه في *Courzerve*', d=4.5, accent='blue')
photos(S('S392') + 6.0, 6.5, [dict(src=P + 'web/kikos/p08.jpg', w=360, rot=-3, caption='*الأكل* نفسه'), dict(src=P + 'web/kikos/p09.jpg', x=0.84, y=0.66, w=320, rot=4, at=14)], w='G')
note(S('S392') + 14.0, 'وكمان *إيجار المكان* وتجهيزه', d=4.5, accent='orange')
note(S('S399'), 'وده *Risk* أي بيزنس', d=3.0, accent='orange')
term(S('S402'), 4.5, '*Potential*', 'إن الربح الصغير ده ممكن *يكبر*', '', en='Potential', sticker='chart_up', accent='olive', w='G')
note(S('S424'), 'الدخل مكانش *بيعيّشه* شهريًا… فرجع يدور على شغل *Software*', d=5.5, accent='blue')
a, b = S('S461'), S('S461') + 18.0
board(a, b, 'أي بيزنس = كذا *زاوية*', [
    i('emo', n='man_technologist', x=460, y=470, s=190, at=T('S461', 'development')), i('chip', text='*Development*', x=460, y=640, bg='blue', at=T('S461', 'development') + 0.2),
    i('emo', n='megaphone', x=960, y=470, s=190, at=T('S461', 'marketing')), i('chip', text='*Marketing*', x=960, y=640, bg='orange', at=T('S461', 'marketing') + 0.2),
    i('emo', n='telephone_receiver', x=1460, y=470, s=190, at=T('S461', 'sales')), i('chip', text='*Sales*', x=1460, y=640, bg='mustard', at=T('S461', 'sales') + 0.2),
    i('text', text='هتبقى *قوي* في حاجات… و*ضعيف* في حاجات\nمفيش مشاكل', x=960, y=860, size=40, paper=True, at=S('S461') + 12.0),
])
note(S('S508'), 'المنافسين *سبقوه*… والـAI هيخليهم يسبقوا *أكتر*', d=5.0, accent='orange')
note(S('S509'), '*ركنه على جنب*… واستغل سرعة الـAI', d=4.5, accent='olive')
note(S('S527'), 'لينك الأبلكيشن الجديد *في الوصف*', d=4.0, accent='mustard')
note(S('S531'), 'البداية بقت *أسهل* بكتير… بس المنافسة *رهيبة*', d=5.0, accent='blue')
note(S('S608'), 'معظم الناس بتنصح: *ماتشاركش صحابك*', d=4.5, accent='orange')
note(S('S612'), 'شريك طريقة تفكيره *قريبة* منك… مش لازم *زيك*', d=5.0, accent='olive')
note(S('S621'), "ساب Kiko's… والوظيفة كانت بتجيب *أكتر بكتير*", d=4.5, accent='blue')
note(S('S653'), 'الربح *مش* هو اللي بيحركه', d=4.0, accent='mustard')
note(S('S657'), 'أغلب الناس: بيزنس *جانبي*… عشان *يرتاحوا*', d=4.5, accent='orange')
bubble(S('S667'), 5.0, 'فيه دافع *صح*… ودافع *غلط*؟', w='A')
a, b = S('S866') + 1.0, E('S872') + 0.4
board(a, b, 'الـAI *بيتغلغل*… واحدة واحدة', [
    i('wave', y=860, amp=26, at=S('S866') + 1.5, speed=11, fill='rgba(92,139,192,.45)'),
    i('emo', n='laptop', x=460, y=520, s=180, at=S('S866') + 2.0), i('chip', text='*Software*', x=460, y=680, bg='blue', at=S('S866') + 2.2),
    i('emo', n='classical_building', x=960, y=520, s=180, at=S('S866') + 10.0), i('chip', text='*المعماري*', x=960, y=680, bg='olive', at=S('S866') + 10.2),
    i('emo', n='money_bag', x=1460, y=520, s=180, at=S('S868')), i('chip', text='*Finance*', x=1460, y=680, bg='mustard', at=S('S868') + 0.2),
    i('emo', n='robot', x=960, y=300, s=150, at=S('S871'), float=True),
    i('text', text='مع الوقت… هيدخل في *مجالك*', x=960, y=950, size=40, paper=True, at=S('S871')),
])
note(S('S887'), 'لو متمسك بيها… الناس *هتسبقك* جامد', d=4.5, accent='orange')
note(S('S894'), 'خلال *2 – 5 سنين* (توقّع كريم)', d=4.5, accent='blue')
bubble(S('S899'), 4.0, 'انت *مستعد*؟', w='G')
note(S('S943'), '"علي بينزّل ريل *كل يوم*… وأنا *كل أسبوع*؟"', d=4.5, accent='mustard')
note(S('S946'), 'الدنيا بتتغير *بالسرعة دي*', d=4.0, accent='olive')

# ======================================================================= shots ("كادرات")
turns = [[s, e, sp] for s, e, sp in SPK['turns'] if e > CUT and s < A1]
merged = []
for s, e, sp in turns:
    if merged and merged[-1][2] == sp and s - merged[-1][1] < 2.0: merged[-1][1] = e
    else: merged.append([s, e, sp])
shots, lastz = [], {'G': 1.0, 'A': 1.0}
t = CUT
for s, e, sp in merged:
    s = max(s - 0.25, t)
    if s - t > 0.5 and shots: shots[-1][1] = s
    if e - s < 4.0:
        shots.append([s, e, 'two', 1.0]); t = e; continue
    k, cur = 0, s
    while cur < e - 0.5:
        ln = random.uniform(4.0, 6.5)
        end = min(e, cur + ln)
        if e - end < 3.0: end = e
        if k % 3 == 1: shots.append([cur, end, 'two', 1.0])
        else:
            z = 1.08 if lastz[sp] == 1.0 and k else 1.0
            lastz[sp] = z
            shots.append([cur, end, sp, z])
        cur = end; k += 1
    t = e
if shots: shots[0][0] = CUT; shots[-1][1] = A1


def apply(a, b, m, z=1.0):
    global shots
    res = []
    for s, e, mm, zz in shots:
        if e <= a or s >= b: res.append([s, e, mm, zz]); continue
        if s < a: res.append([s, a, mm, zz])
        if e > b: res.append([b, e, mm, zz])
    res.append([a, b, m, z]); res.sort(key=lambda x: x[0]); shots = res


for a, b, m in sorted(locks):
    if b > CUT: apply(max(CUT, a), min(A1, b), m)
for a, b in boards: apply(max(CUT, a), min(A1, b), 'two')
fixed = []
for s, e, m, z in shots:
    if e - s < 0.3:
        if fixed: fixed[-1][1] = e
        continue
    if fixed and fixed[-1][2] == m and abs(fixed[-1][3] - z) < 0.01: fixed[-1][1] = e
    elif fixed and e - s < 1.4: fixed[-1][1] = e
    else: fixed.append([s, e, m, z])
add('shot', 0.0, A0, m='full')
add('enta_glitch', A0 - 0.12, 0.3, seed=17); sfx(A0 - 0.12, 'glitch', 0.25)
add('shot', A0, 124.0 - A0, m='G')                           # under biz_open (covered)
# Karim alone 124-187.5: his whole tile big (no crop), a calm zoom inside only on long stretches; GP (beside a card) from locks
kshots = [[124.0, 139.0, 'G', 1.0], [139.0, 151.5, 'G', 1.06], [151.5, 161.0, 'G', 1.0], [161.0, 171.0, 'G', 1.06], [171.0, CUT, 'G', 1.0]]
for a, b, m in sorted(locks):
    if a < CUT:
        for ks in list(kshots):
            pass
for s, e, m, z in kshots:
    add('shot', s, e - s, m=m, **({'z': z, 'zx': 0.42, 'zy': 0.46} if z > 1 else {}))
for a, b, m in sorted(locks):  # GP cadres while a card is up (Karim on his side, card on the other)
    if a < CUT: add('shot', a, b - a, m=m); add('shot', b, 0.01, m='G')
add('enta_glitch', CUT - 0.1, 0.3, seed=187); sfx(CUT - 0.1, 'glitch', 0.3); sfx(CUT, 'whoosh_2', 0.35)
for s, e, m, z in fixed:
    sp = m[0] if m != 'two' else None
    props = {'m': m}
    if sp and z > 1.0 and m in ('G', 'A'): props.update(z=z, zx=FACE[sp][0], zy=FACE[sp][1])
    add('shot', max(CUT, s), e - max(CUT, s), **props)
add('enta_glitch', A1 - 0.15, 0.3, seed=18)
add('shot', A1, 2703.0 - A1, m='full')

# ======================================================================= speaker circle over boards > 5 s
for c in [c for c in cues if c['t'] == 'biz_free' and c['dur'] > 5 and c['src'] > CUT]:
    a, b = c['src'] + 0.8, c['src'] + c['dur'] - 0.3
    ts = [a + k * 0.25 for k in range(int((b - a) / 0.25) + 1)]
    lab = [who(x) for x in ts]
    lab = [max('AG', key=lambda q: lab[max(0, n - 6):n + 7].count(q)) for n in range(len(lab))]
    segs = []
    for x, sp in zip(ts, lab):
        if segs and segs[-1][2] == sp: segs[-1][1] = x + 0.25
        else: segs.append([x, x + 0.25, sp])
    k = 0
    while k < len(segs):
        if segs[k][1] - segs[k][0] < 2.5 and len(segs) > 1:
            if k: segs[k - 1][1] = segs[k][1]
            else: segs[1][0] = segs[0][0]
            segs.pop(k)
            m = [segs[0]]
            for x in segs[1:]:
                if x[2] == m[-1][2]: m[-1][1] = x[1]
                else: m.append(x)
            segs, k = m, 0
            continue
        k += 1
    segs[-1][1] = b
    for s0, s1, sp in segs:
        add('pip', s0, s1 - s0, who=sp, zx=FACE[sp][0], zy=FACE[sp][1], side='R' if sp == 'G' else 'L')

cues.sort(key=lambda c: c['src'])
plan = {'cut': False, 'captions': False, 'pack': 'charcoal', 'video': 'input/2026-10-27 16-06-01.mp4', 'quiet': [[0.0, A0], [A1, 2703.0]],
        'meet': {'G': [169, 151, 1582, 800], 'A': [1688, 808, 160, 102], 'left': 'A', 'self': [1652, 800, 240, 138],
                 'masks': [dict(who='G', box=[186, 912, 150, 30], tag='كريم تامر')],
                 'phases': [dict(**{'from': 149.25}, G=[1412, 222, 492, 658], A=[18, 164, 1376, 772]),   # Aly pinned big (covered by a board)
                            dict(**{'from': 157.5}, G=[169, 151, 1582, 800], A=[1688, 808, 160, 102], self=[1652, 800, 240, 138],
                                 masks=[dict(who='G', box=[186, 912, 150, 30], tag='كريم تامر')]),
                            dict(**{'from': CUT}, G=[18, 288, 936, 526], A=[966, 288, 936, 526],
                                 masks=[dict(who='G', box=[30, 776, 110, 26], tag='كريم تامر'), dict(who='A', box=[978, 776, 110, 26], tag='علي معتز'),
                                        dict(who='A', box=[1858, 772, 40, 36])])]},
        'cues': cues}
json.dump(plan, open(W / 'plan.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
cards = sorted((c['src'], c['src'] + c['dur']) for c in cues if c['t'].startswith(('enta_', 'biz_')) and c['t'] not in ('enta_glitch', 'enta_leak'))
gaps, prev = [], A0
for a, b in cards:
    if a - prev > 12: gaps.append((round(prev, 1), round(a, 1)))
    prev = max(prev, b)
lens = [e - s for s, e, m, z in fixed]
print(len(cues), 'cues;', len(fixed), 'shots; avg', round(sum(lens) / len(lens), 2), 's; boards', len(boards), '; cards', len(cards))
print('no-graphic stretches > 12 s:', gaps)
# every picture must exist (a missing Fluent name stopped the first render: people_holding_hands, chef)
import re as _re, os as _os
_pub = W.parents[3] / 'motion-library' / 'public'
_s = json.dumps(plan, ensure_ascii=False)
_miss = [e for e in sorted(set(_re.findall(r'"(?:emo|n)": "([a-z0-9_]+)"', _s))) if not (_pub / 'fluent' / f'{e}.png').exists()]
_miss += [x for x in sorted(set(_re.findall(r'"(?:src|file|aly)": "([^"]+)"', _s))) if not (_pub / x).exists()]
if _miss: raise SystemExit('MISSING assets: ' + ', '.join(_miss))
_ms = sorted({c['props']['name'] for c in cues if c['t'] == 'sfx' and not (_pub / 'sfx' / f"{c['props']['name']}.wav").exists()})
if _ms: raise SystemExit('MISSING sfx: ' + ', '.join(_ms))

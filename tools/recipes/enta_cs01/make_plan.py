"""انت بتشتغل ايه — حاسبات ep01 (guest Aiman Ismail, Senior Software QA Engineer), 2026-10-20.
Input = Google Meet SCREEN RECORDING (guest tile LEFT, Aly tile RIGHT, 30:23, his intro 0-17.13 and again 1806.5-end).
Aly: hide the Meet UI, simple calm frame, change between "كادرات" instead of zoom; zoom only INSIDE the tile and only a little.
-> Edit 'meet' layout (motion-library/src/enta/Meet.tsx): shots two / G / A / GP / AP (P = person on the left, card on the right).
Nothing cut, no captions (long video) -> bottom notes. Stickers: cs + shared only (vector now). Boards: src/enta/BoardQA.tsx.
Run: python -X utf8 work/scripts/make_plan.py -> work/plan.json ; build: sh work/scripts/build.sh review_01 (code 'entacs01')."""
import json, random
from pathlib import Path

W = Path(__file__).resolve().parents[1]
P = 'projects/entacs01/'
A0, A1 = 17.2, 1806.4          # after his intro / before his intro at the end
tr = json.load(open(W / 'transcript.json', encoding='utf8'))
SENT = {s['id']: s for s in tr['sentences']}
SPK = json.load(open(W / 'speakers.json', encoding='utf8'))
random.seed(7)


def T(sid, sub, k=0):
    hits = [w['start'] for w in SENT[sid]['words'] if sub in w['w']]
    assert len(hits) > k, (sid, sub, [w['w'] for w in SENT[sid]['words']])
    return hits[k]


def S(sid):  # sentence start / end
    return SENT[sid]['words'][0]['start']


def E(sid):
    return SENT[sid]['words'][-1]['end']


def who(t):  # who talks at t (word labels from speakers.py)
    best = min(SPK['words'], key=lambda w: abs((w[0] + w[1]) / 2 - t))
    return best[3]


cues, locks, boards = [], [], []
F = lambda base, t: int(round((t - base) * 30))


def add(t, at, dur, **props):
    cues.append({'t': t, 'src': round(at, 2), 'dur': round(dur, 2), 'props': props})


def sfx(at, name, vol=0.4):
    add('sfx', at, 2.0, name=name, volume=vol)


def lock(at, dur, shot):
    locks.append((at - 0.2, at + dur, shot))


def side(at, dur, w=None):  # the speaker big on the LEFT, card on the right
    lock(at, dur, (w or who(at + min(1.0, dur / 2))) + 'P')


def term(at, dur, term, defn='', example='', exAt=None, en='', sticker='', accent='orange', paper='cream', w=None):
    dur = min(dur, 9.0)  # a card never stays longer than ~9 s
    if exAt and exAt > at + dur - 2.0: exAt = at + min(dur - 2.0, max(1.5, dur * 0.5))
    side(at, dur, w)
    add('enta_term', at, dur, term=term, example=example, exampleAt=int(((exAt or at + 1.5) - at) * 30), en=en,
        sticker=sticker, accent=accent, paper=paper, pic='', side='right', top=0.1)
    cues[-1]['props']['def'] = defn
    sfx(at, 'swish', 0.35); sfx(at + 0.17, 'tape', 0.3)
    if example and exAt: sfx(exAt, 'pop_2', 0.3)


def photos(at, dur, items, snd='pop_1', w=None):
    dur = min(dur, 8.0)
    side(at, dur, w)
    add('enta_photos', at, dur, items=[dict(dict(x=0.79, y=0.4, w=420, h=0, at=0, rot=-3, caption='', sepia=False, pos='50% 50%',
                                                 fit='contain', sticker='', start=0, bare=True), **it) for it in items])
    for it in items: sfx(at + it.get('at', 0) / 30, snd, 0.35)


def stick(at, items, dur=1.8):  # top band (clear in the two-shot)
    add('enta_stickers', at, dur, items=[dict(name=n, x=x, y=y, size=s, at=int(d * 30), rot=r) for n, x, y, s, d, r in items])
    for k, it in enumerate(items): sfx(at + it[4], ['pop_1', 'pop_2', 'pop_3'][k % 3], 0.3)


def bubble(at, dur, text, w=None):  # speech bubble above the speaker's tile in the two-shot
    sp = w or who(at + 0.3)
    dur = min(dur, 5.0)
    lock(at, dur, 'two')
    add('enta_bubble', at, dur, text=text, x=0.25 if sp == 'G' else 0.75, y=0.11, tail='left' if sp == 'G' else 'right', w=560)
    sfx(at, 'pop_3', 0.4)


def board(t, a, b, **props):
    boards.append((a - 0.3, b + 0.3))
    add(t, a, b - a, **props)
    add('enta_glitch', a - 0.1, 0.3, seed=int(a)); sfx(a - 0.1, 'glitch', 0.3); sfx(a, 'whoosh_2', 0.4)
    add('enta_glitch', b - 0.2, 0.3, seed=int(b)); sfx(b - 0.2, 'whoosh_1', 0.3)


def note(at, text, sticker='', d=4.5, accent='orange'):
    add('enta_note', at, d, text=text, sticker=sticker, side='center', accent=accent); sfx(at, 'paper', 0.3)


# ================= opening: Aly + the guest =================
a = T('S001', 'عليكم')
add('enta_name', a, 3.4, name='علي معتز شُرُش', role='مقدّم *انت بتشتغل ايه*', side='right', accent='orange')
side(a, 3.4, 'A'); sfx(a, 'swoop_up', 0.45); sfx(a + 0.45, 'stamp', 0.3)
a = T('S001', 'الحاسبات')
photos(a - 0.2, T('S001', 'فضيف') - a + 0.1, [dict(src=P + 'logo_cs_trim.png', w=380, h=384, rot=-4, caption='أول حلقة *حاسبات*')], w='A')
note(T('S001', 'الحلقة'), 'الحلقة *التانية* · وأول حلقة *حاسبات*', accent='blue', d=4.0)
a = S('S002')
add('enta_name', a, 4.6, name='أيمن إسماعيل', role='Senior Software *QA Engineer*', side='right', accent='blue')
side(a, 4.6, 'G'); sfx(a, 'swoop_up', 0.45); sfx(a + 0.45, 'stamp', 0.3)
note(T('S002', 'الكفاح'), 'صاحبي *وزميل شغل* من سنين', accent='olive', d=3.6)
a = T('S004', 'Testing')
term(a, T('S006', 'فأنا') - a, '*Testing* · *QA* · *QC*', 'أسامي كتير… *لنفس المجال*', 'Quality Assurance · Quality *Control*',
     exAt=T('S005', 'QA'), en='Software Testing', sticker='bug', accent='blue', paper='blue', w='A')
note(S('S006') + 0.3, 'وعلي كمان *Tester*', sticker='bug', accent='mustard', d=3.5)
stick(T('S007', 'اشتغلنا'), [('brace_l', 0.44, 0.1, 90, 0, -8), ('brace_r', 0.56, 0.1, 90, 0.12, 8)], 1.8)
note(T('S016', 'فروفرشنال') - 0.6, 'دردشة *خفيفة*… مش بروفيشنال', accent='olive', d=3.6)
bubble(S('S018'), E('S019') - S('S018'), 'عرّفنا *بيك*؟', w='A')
# ================= who is Aiman =================
a = S('S020')
term(a, E('S023') - a + 0.6, 'أيمن · دفعة *2021*', 'شغال *QA*', 'بقاله قرب *5 سنين*', exAt=T('S023', 'خمس'), sticker='star_y', accent='mustard', w='G')
a = S('S027') + 0.3
photos(a, E('S031') - a + 1.6, [dict(src='fluent/mobile_phone.png', w=230, h=230, rot=-6, caption='قبلها: *Mobile Dev*')], w='A')
a = T('S035', 'جربت')
term(a, E('S038') - a + 0.3, 'جرّب *حاجات كتير*', 'Front End · Back End', 'Graphic Design · *Motion*', exAt=T('S037', 'الجرافيك'),
     sticker='spark_o', accent='orange', w='G')
note(T('S041', 'وخترته'), 'اختار التستنج *عن شغف*', sticker='star_y', accent='mustard', d=4.0)
stick(T('S045', 'شغف'), [('spark_o', 0.62, 0.1, 80, 0, 0), ('star_y', 0.7, 0.16, 70, 0.15, 10)], 1.6)
note(T('S048', 'الجرافيكس'), 'علي كمان: *جرافيكس* و *Development*… واختار التستنج', accent='blue', d=4.6)
bubble(T('S050', 'بتظن'), E('S050') - T('S050', 'بتظن') + 0.4, 'التستنج *محدش* بيدخله بمزاجه؟', w='A')
bubble(S('S053'), E('S056') - S('S053'), 'اشرحها لحد *برّه المجال*', w='A')
# ================= the myth: boring? =================
a = S('S062')
term(a, E('S066') - a + 0.3, 'تصوّر *غلط*', 'ممل؟ روتيني؟ *مفيش كود*؟', 'هنصححه *في الأسئلة*', exAt=S('S066'), sticker='qmark', accent='orange', w='G')
stick(T('S065', 'كودنج'), [('brace_l', 0.62, 0.12, 80, 0, -6), ('cross', 0.7, 0.12, 80, 0.15, 6)], 1.6)
note(T('S069', 'تيم'), 'أول *Team Lead*: "ممكن تزهق"', accent='mustard', d=3.6)
note(T('S071', 'مالقتش'), 'ومن ساعتها… *مزهقش*', sticker='star_y', accent='olive', d=3.4)
a = S('S080')
term(a, E('S098') - a + 0.4, 'ممل *ولا لأ*؟', 'حسب *المكان* والـ*Challenges*', 'وحسبك: تنفّذ التاسك وبس… ولا *تتعلم Tools جديدة*؟',
     exAt=T('S093', 'مهتمل'), sticker='qmark', accent='blue', paper='blue', w='G')
# ================= Testing = ? =================
a = S('S101') + 0.8; b = E('S111') + 0.5
board('qa_what', a, b, appAt=F(a, T('S103', 'software')), bugsAt=F(a, T('S107', 'مشاكل')), reqAt=F(a, T('S109', 'requirements')),
      req=[dict(text='اللي *الـClient* طلبه', at=F(a, T('S110', 'client'))), dict(text='بالظبط *زي ما اتطلب*', at=F(a, T('S111', 'validate')))])
sfx(T('S103', 'software'), 'pop_1', 0.4); sfx(T('S107', 'مشاكل'), 'buzz_wrong', 0.25); sfx(T('S109', 'requirements'), 'paper', 0.35)
bubble(S('S113'), E('S114') - S('S113'), 'على *أساس* إيه؟', w='A')
note(T('S118', 'كريتيريا'), 'فيه *Criteria* تقيس عليها الصح والغلط', accent='blue', d=4.2)
a = S('S121')
term(a, E('S130') - a - 2.0, '*Requirements*', 'اللي الـClient *كتبه*: 1، 2، 3', 'و*الخبرة*: حاجات محدش طلبها', exAt=T('S127', 'يطلبهاش'),
     en='Requirements', sticker='floppy', accent='olive', w='G')
note(T('S131', 'سوفتوير'), 'أي *Software*: أبلكيشن · ويبسايت · أي حاجة', accent='mustard', d=4.0)
a = T('S134', 'فانكشناليتيز')
term(a, E('S138') - a + 0.3, 'Functional و *Non-Functional*', 'شغال صح؟ + بطيء؟ *Security*؟ *Performance*؟', 'و*UI/UX* اللي الناس متعودة عليه',
     exAt=T('S138', 'اليوزرز'), sticker='spark_b', accent='blue', paper='blue', w='A')
note(T('S139', 'جاهز'), 'جاهز *ينزل للناس*؟', sticker='check', accent='olive', d=4.2)
bubble(T('S147', 'محتاجك'), E('S151') - T('S147', 'محتاجك'), 'فيه *Developers* شطار… *محتاجينك* ليه؟', w='A')
# ================= developer eye vs tester eye =================
a = S('S160'); b = E('S168') + 0.3
board('qa_eyes', a, b, devAt=F(a, T('S161', 'بيفكر')), testAt=F(a, T('S161', 'بفكر')), anglesAt=F(a, T('S165', 'زاوية')))
sfx(T('S161', 'بيفكر'), 'pop_1', 0.35); sfx(T('S161', 'بفكر'), 'pop_2', 0.35); sfx(T('S165', 'زاوية'), 'whoosh_1', 0.3)
bubble(T('S170', 'إشوز'), E('S173') - T('S170', 'إشوز') - 1.5, 'مع الـ*AI*… لسه فيه *Bugs*؟', w='A')
photos(T('S173', 'الاي'), 3.0, [dict(src='logos/claude.svg', x=0.72, w=170, h=170, rot=-5), dict(src='logos/chatgpt.svg', x=0.85, w=170, h=170, rot=5, at=8)], w='G')
a = T('S176', 'بالريكويرمنت'); b = E('S180') + 0.4
board('qa_req', a, b, req='عايز زرار *حفظ*',
      people=[dict(emo='man_office_worker', label='اللي *كتبه*', shape='circle', at=F(a, T('S177', 'حد'))),
              dict(emo='man_technologist', label='*Developer*', shape='square', at=F(a, T('S178', 'ببريفها'))),
              dict(emo='woman_technologist', label='*Tester*', shape='tri', at=F(a, T('S178', 'والتيستي')))],
      bugAt=F(a, T('S180', 'بقز')))
sfx(T('S180', 'بقز'), 'buzz_wrong', 0.25)
note(T('S183', 'بقز'), 'علي: الـBugs *زي ما هي*', accent='blue', d=3.8)
note(T('S186', 'قل'), 'أيمن: *قلّت شوية*', accent='orange', d=3.4)
a = T('S190', 'الاي')
term(a, T('S192', 'حلو') - a, '*AI* Testing', 'الـAI بيعمل *Test*', 'بس محتاج *عقل بشري*', exAt=T('S191', 'عقل'), sticker='qmark', accent='mustard', w='G')
a = T('S195', 'البوج')
term(a, 4.4, 'يعني إيه *Bug*؟', 'حاجة *بايظة* · مشكلة · Issue', '', sticker='bug', accent='orange', w='A')
a = T('S199', 'الستوري')
term(a, E('S202') - a + 0.5, '*Story* (فيتشر)', 'حاجة عايزين *نعملها*', 'الـBug: ما خدش باله إنها *بتأثر* في حتة بعيدة', exAt=T('S202', 'بيأفكت'),
     en='User Story', sticker='floppy', accent='blue', paper='blue', w='A')
note(T('S204', 'ببرامتر'), 'وBug تانية: *Parameter* ضخم محدش *هندله*', sticker='bug', accent='mustard', d=4.4)
# ================= production? =================
a = T('S209', 'production')
term(a, 4.0, '*Production*', 'النسخة اللي *الناس* بتستخدمها', '', en='Production', sticker='onair', accent='orange', w='A')
bubble(T('S217', 'يتصلح'), E('S225') - T('S217', 'يتصلح') + 0.3, 'ننزّلها… والناس *تبلّغ* عن الـBugs؟', w='A')
a = T('S231', 'payment'); b = E('S269') + 0.3
board('qa_prod', a, b, usersAt=10, refundAt=F(a, T('S243', 'ريفوند')), moneyAt=F(a, T('S254', 'فلوس')), repAt=F(a, T('S265', 'سمعة')),
      bankAt=F(a, T('S269', 'بانكي')))
sfx(T('S243', 'ريفوند'), 'click', 0.4); sfx(T('S254', 'فلوس'), 'cash', 0.4); sfx(T('S265', 'سمعة'), 'buzz_wrong', 0.25)
# ================= how you test: types =================
bubble(T('S271', 'تطبق'), T('S274', 'طيب') - T('S271', 'تطبق'), 'بتعمل *Testing* إزاي؟ وإيه *أنواعه*؟', w='A')
note(T('S276', 'تشن'), 'السؤال ده *عايز حلقة لوحده*', sticker='qmark', accent='mustard', d=3.8)
a = T('S278', 'الانواع'); b = T('S287', 'تولز') - 0.3
board('qa_types', a, b, funcAt=F(a, T('S279', 'فنكشنال')), nonAt=F(a, T('S284', 'والنون')),
      func=[dict(emo='backhand_index_pointing_up', label='Manual', sub='تجرب *بإيدك*', at=F(a, T('S281', 'منول'))),
            dict(emo='robot', label='Automation', sub='*Script* بيجرب', at=F(a, T('S282', 'سكريبت')))],
      non=[dict(emo='high_voltage', label='Performance', at=F(a, T('S284', 'والنون')) + 20),
           dict(emo='shield', label='Security', at=F(a, T('S284', 'والنون')) + 35),
           dict(emo='thumbs_up', label='Usability', at=F(a, T('S286', 'اليوزابيليتي')))])
sfx(T('S281', 'منول'), 'pop_1', 0.35); sfx(T('S282', 'سكريبت'), 'pop_2', 0.35); sfx(T('S286', 'اليوزابيليتي'), 'pop_3', 0.35)
a = T('S289', 'الاي')
photos(a, T('S291', 'لان') - a, [dict(src='logos/claude.svg', x=0.7, w=160, h=160, rot=-5), dict(src='logos/chatgpt.svg', x=0.82, w=160, h=160, rot=4, at=6),
                                 dict(src='logos/googlegemini.svg', x=0.93, w=150, h=150, rot=-3, at=12, caption='')], w='G')
note(a + 0.3, 'أغلب الشغل دلوقتي *بالـAI*', accent='orange', d=4.0)
note(T('S292', 'بالاوتوميشن'), 'منول *+* أوتوميشن', accent='olive', d=3.2)
# ================= the login example =================
a = T('S302', 'بداية'); b = E('S330') + 0.6
board('qa_login', a, b, manualAt=F(a, T('S308', 'منوال')),
      cases=[dict(email='aly@mail.com', pass_='x', ok=True, msg='Welcome ✓', at=F(a, T('S315', 'سليم'))),
             dict(email='aly@mail.com', pass_='x', ok=False, msg='Wrong password', at=F(a, T('S316', 'غلط'))),
             dict(email='', pass_='', ok=False, msg='Email is required', at=F(a, T('S318', 'مسلا'))),
             dict(email='old@mail.com', pass_='x', ok=False, msg='Account not active', at=F(a, T('S319', 'اكتف')))],
      autoAt=F(a, T('S321', 'الاوتوميشن')),
      code=['driver.get("myapp.com/login")', 'type(email, data.email)', 'type(password, data.pass)', 'click(loginButton)', 'assert(message == data.expected)'],
      repeatAt=F(a, T('S323', 'اكتر')), reportAt=F(a, T('S329', 'ريكورت')))
for k in ('سليم', ): sfx(T('S315', k), 'click', 0.35)
sfx(T('S316', 'غلط'), 'buzz_wrong', 0.2); sfx(T('S319', 'اكتف'), 'buzz_wrong', 0.2); sfx(T('S321', 'الاوتوميشن'), 'magic', 0.35)
sfx(T('S323', 'اكتر'), 'tick', 0.3); sfx(T('S329', 'ريكورت'), 'ding', 0.35)
for c in cues[-12:]:  # 'pass' is a python word; the schema key is pass
    if c['t'] == 'qa_login':
        for k in c['props']['cases']: k['pass'] = k.pop('pass_')
# ================= API, security, performance =================
a = S('S331'); b = E('S341') + 0.4
board('qa_api', a, b, uiAt=F(a, T('S332', 'البراوزر')), selAt=F(a, T('S338', 'شلينيوم')), apiAt=F(a, T('S333', 'end')) - 40,
      postmanAt=F(a, T('S334', 'Postman')), autoAt=F(a, T('S335', 'Automation')), libAt=F(a, T('S339', 'رسط')))
sfx(T('S334', 'Postman'), 'pop_1', 0.4); sfx(T('S338', 'شلينيوم'), 'pop_2', 0.35)
a = S('S342'); b = E('S345') + 0.3
board('qa_perf', a, b, secAt=F(a, T('S342', 'Security')), perfAt=F(a, T('S344', 'performance')))
sfx(T('S344', 'performance'), 'whoosh_1', 0.35)
note(S('S346'), 'والأدوات… *بسيطة*', accent='olive', d=3.0)
# ================= what you need =================
bubble(T('S348', 'توصل'), T('S351', 'خريج') - T('S348', 'توصل') - 0.1, 'عشان توصل للشغلانة دي… *محتاج إيه*؟', w='A')
bubble(T('S351', 'خريج'), E('S356') - T('S351', 'خريج'), 'لازم تكون خريج *Computer Science*؟', w='A')
note(T('S358', 'ربنا'), 'الرزق *بتاع ربنا*… وانت عليك *تسعى*', sticker='star_y', accent='mustard', d=5.0)
a = T('S366', 'يفهم')
term(a, T('S373', 'موضوع') - a - 0.2, 'افهم *Software* كويس', 'جرّب *تبني* وتكتب بإيدك', 'ومادة عن الـ*Software Industry*', exAt=T('S370', 'مادة'),
     sticker='brace_l', accent='blue', paper='blue', w='G')
note(T('S373', 'اختفت') - 0.4, 'كاميرا علي *فصلت* ثواني', sticker='qmark', accent='orange', d=3.6)
a = T('S374', 'كمبيوتر')
term(a, E('S380') - a, 'لازم *Computer Science*؟', '*لأ*… فيه ناس من برّه المجال', 'المهم *تذاكر وتفهم*', exAt=T('S379', 'يذاكر'),
     sticker='qmark', accent='orange', w='G')
a = S('S382'); b = E('S403') + 0.5
board('qa_road', a, b, steps=[
    dict(emo='laptop', label='افهم *Software*', sub='جرّب وابني بإيدك', at=F(a, T('S383', 'فهم'))),
    dict(pic=P + 'istqb-ctfl-4-logo.jpg', label='ISTQB *Foundation*', sub='المنهج بتاعنا', at=F(a, T('S384', 'ISTQP'))),
    dict(emo='lady_beetle', label='*Manual*', sub='طلّع Bugs واعمل *Report*', at=F(a, T('S387', 'ويبسايت'))),
    dict(logo=['logos/openjdk_c.svg', 'logos/javascript_c.svg', 'logos/python_c.svg'], label='*Automation*', sub='بأي لغة', at=F(a, T('S389', 'automation'))),
    dict(emo='briefcase', label='*قدّم* على شغل', sub='بإذن الله', at=F(a, T('S403', 'يقدم')))])
for s_, k in (('S383', 'فهم'), ('S384', 'ISTQP'), ('S387', 'ويبسايت'), ('S389', 'automation'), ('S403', 'يقدم')): sfx(T(s_, k), 'pop_1', 0.35)
# ================= tester = joker =================
a = T('S406', 'جوكر') - 0.4; b = T('S423', 'الباك') + 2.6
board('qa_joker', a, b, skills=[
    dict(emo='speaking_head', text='يكلّم *Business*', at=F(a, T('S407', 'تتكلم'))),
    dict(emo='brain', text='تفكير *نقدي*', at=F(a, T('S408', 'تفكير'))),
    dict(emo='handshake', text='يتعامل مع *Developers*', at=F(a, T('S411', 'الديبلبرز'))),
    dict(emo='artist_palette', text='عين *فنية*', at=F(a, T('S413', 'فنية'))),
    dict(emo='globe_with_meridians', text='*Front End*', at=F(a, T('S418', 'الفرونت'))),
    dict(emo='file_cabinet', text='*Back End* · API', at=F(a, T('S423', 'الباك')))])
for s_, k in (('S407', 'تتكلم'), ('S408', 'تفكير'), ('S411', 'الديبلبرز'), ('S413', 'فنية'), ('S418', 'الفرونت'), ('S423', 'الباك')): sfx(T(s_, k), 'pop_2', 0.3)
a = T('S425', 'الاتابيسيز')
term(a, E('S426') - a + 0.3, '*Database*', 'تعمل *Query* وتشوف الداتا', 'تتأكد إن الـRecord *اتسيف صح*', exAt=T('S426', 'تتسايف'),
     en='SQL', sticker='floppy', accent='blue', paper='blue', w='A')
note(T('S427', 'سكينزي'), 'ومهارات *Soft Skills* كتير', sticker='star_y', accent='mustard', d=4.0)
note(T('S440', 'تجربة'), 'للمبتدئ: *متتخضّش*… هتتعلمها مع الوقت', accent='olive', d=4.6)
note(T('S446', 'بدأت'), 'ناس بدأت *من الصفر*… وبقالها سنين', accent='blue', d=4.2)
a = T('S456', 'تبريدكت')
term(a, T('S466', 'بسم') - a, '*تتوقّع* الـBug', 'لو عارف الحاجة *اتبنت إزاي*', 'تروح *عليها* على طول', exAt=T('S462', 'هروح'),
     sticker='bug', accent='orange', w='G')
stick(T('S467', 'شاطر'), [('star_y', 0.62, 0.1, 80, 0, 0), ('spark_y', 0.7, 0.16, 70, 0.12, 0), ('star8_b', 0.78, 0.1, 70, 0.24, 0)], 1.8)
# ================= ISTQB =================
a = T('S473', 'الايستي'); b = E('S489') + 1.2
board('qa_istqb', a, b, logo=P + 'logo-for-header.svg',
      certs=[dict(pic=P + 'istqb-ctfl-4-logo.jpg', name='Foundation', at=F(a, T('S476', 'فاونديشن')), his=True),
             dict(name='Agile', at=F(a, T('S477', 'واجايل'))),
             dict(pic=P + 'istqb-mobile-app-testing-logo.jpg', name='Mobile', at=F(a, T('S477', 'وموبايل')), his=True),
             dict(pic=P + 'istqb-test-automation-engineering-logo.jpg', name='Automation', at=F(a, T('S489', 'والاوتوميشن')), his=True)],
      stampAt=F(a, T('S489', 'اخدت')), stampText='أيمن *أخد* الـ3 دول',
      chips=[dict(text='المنهج: *أنواع التستنج والتكنيكس*', at=F(a, T('S481', 'انواع'))), dict(text='مش *كل* الشركات بتطلبها', at=F(a, T('S483', 'كل')))])
sfx(T('S489', 'اخدت'), 'stamp', 0.4)
note(T('S492', 'هادة'), 'علي: *معندوش* الشهادة', accent='orange', d=3.6)
note(T('S497', 'الانترفيو'), 'بس الإنترفيوهات *بتسأل عليها*', accent='blue', d=4.4)
a = T('S510', 'السنيني')
term(a, E('S511') - a + 0.4, '*Senior*', 'بعدد *سنين الخبرة*', 'وبالـ*مسؤوليات* في الشغل', exAt=T('S511', 'والمسؤولات'), sticker='star8_b', accent='mustard', w='A')
# ================= AI =================
a = S('S520'); b = E('S533') + 0.3
board('qa_ai', a, b, aiAt=8, meAt=F(a, T('S532', 'شاشتين')),
      tasks=[dict(text='*Manual* Testing', at=F(a, T('S522', 'manual'))), dict(text='يكتب *Test Cases*', at=F(a, T('S523', 'تيستي'))),
             dict(text='*Demo* Video', at=F(a, T('S524', 'الديمو'))), dict(text='يرفع الشغل', at=F(a, T('S525', 'ويرفعه')))],
      qAt=F(a, T('S525', 'بيستبدلنا')), aAt=F(a, T('S530', 'بيستبدلنا')), qEnd=F(a, T('S532', 'شاشتين')) - 6)
sfx(T('S525', 'بيستبدلنا'), 'glitch', 0.25); sfx(T('S530', 'بيستبدلنا'), 'ding', 0.35)
note(T('S536', 'كتول'), 'الـAI = *Tool* بتسرّع الشغل', sticker='spark_o', accent='olive', d=4.0)
note(T('S541', 'نركز'), 'بيوفّر *شغل رهيب*… ونركز في *حاجات تانية*', accent='blue', d=4.4)
a = T('S547', 'الطلب'); b = E('S550') + 0.3
board('qa_demand', a, b, seniorAt=F(a, T('S547', 'السينيورز')), juniorAt=F(a, T('S548', 'الجونيورز')),
      more=[dict(text='تفاصيل *أكتر بكتير*', at=F(a, T('S549', 'تفاصيل'))), dict(text='البسيط… *الـAI بيعمله*', at=F(a, T('S550', 'بيعملها')))])
note(T('S557', 'اغلب'), 'أغلب الشركات *لسه فيها* Testers', sticker='check', accent='olive', d=4.0)
# ================= advice + contact =================
a = T('S568', 'يذاكر')
term(a, E('S573') - a + 0.4, 'النصيحة', '*ذاكر* واجتهد', 'واكب *الـAI*… وذاكر بالطرق الجديدة', exAt=T('S572', 'نواكب'), sticker='star_y', accent='olive', w='G')
note(T('S570', 'نريزست'), 'مش هنرجع لعصر *ما قبل الـAI*', accent='orange', d=3.6)
a = T('S581', 'لينكات')
photos(a, E('S586') - a + 0.3, [dict(src='logos/linkedin_c.svg', w=200, h=200, rot=-4, caption='linkedin.com/in/*aimanismail07*')], w='A')
note(T('S584', 'لينك'), 'اللينك *في الوصف*', accent='blue', d=3.4)
a = S('S587')
stick(a, [('star_y', 0.6, 0.1, 90, 0, 0), ('spark_o', 0.7, 0.16, 80, 0.15, 0), ('star8_b', 0.8, 0.1, 80, 0.3, 0)], 2.0)
add('enta_leak', a, 2.0, kind='leak_warm', x=0.5, y=0.3)

# ================= fillers: short point notes / bubbles where nothing explained the talk for > 8 s =================
note(T('S013', 'المجال'), 'نعرف أكتر عن *مجال التستنج*', accent='blue', d=3.6)
note(T('S014', 'الاسئلة'), 'وندخل في *الأسئلة*', sticker='qmark', accent='mustard', d=3.4)
note(T('S032', 'الكلية'), 'Mobile *أيام الكلية*', accent='olive', d=3.6)
note(T('S034', 'بيثبتش'), 'مكانش *بيثبت على حاجة*', sticker='spark_o', accent='orange', d=3.6)
note(T('S047', 'شغف'), 'ودخل الكلية *عن شغف* برضو', accent='olive', d=3.6)
stick(T('S058', 'كتير'), [('qmark', 0.12, 0.1, 90, 0, -8)], 1.6)
bubble(T('S100', 'اقول'), E('S101') - T('S100', 'اقول') - 3.0, 'لو حد سألك: *انت بتشتغل ايه*؟', w='A')
note(T('S116', 'العميل'), 'تعرف منين *العميل عايز إيه*؟', accent='blue', d=4.0)
note(T('S133', 'الجودة'), 'وتتأكد إنه *محقق الجودة*', sticker='check', accent='olive', d=4.0)
stick(T('S142', 'بالضبط'), [('check', 0.12, 0.1, 90, 0, -6)], 1.5)
note(T('S155', 'developer'), 'مش موضوع الـDeveloper *شاطر ولا لأ*', accent='mustard', d=4.4)
note(T('S182', 'بصراحة'), 'علي عنده *رأي تاني*', sticker='qmark', accent='blue', d=3.4)
note(T('S188', 'تفاصيل'), 'الـAI لسه موصلش *لأدق التفاصيل*', accent='orange', d=4.4)
note(T('S192', 'اغير'), 'علي: *غيّرت رأيي*', sticker='spark_y', accent='olive', d=3.6)
note(T('S197', 'زمان'), 'الـBugs دلوقتي *مش زي زمان*', sticker='bug', accent='blue', d=4.4)
note(T('S206', 'فلوس'), 'الشركة بتدفع *للـTesters*… ليه؟', accent='mustard', d=3.8)
stick(T('S275', 'طويل'), [('qmark', 0.12, 0.1, 90, 0, -6)], 1.5)
note(T('S296', 'اللخص'), 'علي *هيلخّص* بمثال', accent='olive', d=3.6)
note(T('S361', 'الاخصى'), 'اعمل *أقصى* حاجة تقدر عليها', accent='olive', d=4.0)
note(T('S424', 'تبريدكت'), 'تتوقع الـ*Bug* هتطلع فين', sticker='bug', accent='orange', d=3.8)
note(T('S427', 'جوكر'), 'الـTester = *جوكر*', accent='mustard', d=3.6)
note(T('S428', 'مليون'), 'متفق *مليون في المية*', sticker='check', accent='olive', d=3.4)
note(T('S431', 'ونه'), 'بس المبتدئ هيقول: *إيه كل ده*؟!', sticker='qmark', accent='orange', d=4.0)
note(T('S438', 'جربنا'), 'إحنا *بنحب نجرّب*', accent='blue', d=3.6)
note(T('S443', 'سايبر'), '*Cyber Security* محتاج أكتر كمان', accent='mustard', d=3.8)
note(T('S453', 'الناوليج'), 'كل المعرفة دي *هتساعدك*', accent='olive', d=3.6)
note(T('S495', 'انترفيو'), 'أول إنترفيو: *محدش سأل* عليها', accent='mustard', d=4.0)
note(T('S500', 'سمعة'), 'بقى عنده *خبرة وسمعة*', accent='olive', d=3.6)
note(T('S503', 'الوحيد'), 'الوحيد اللي يعرفهم *من غير شهادة*', accent='orange', d=4.0)
bubble(S('S506'), E('S507') - S('S506') + 0.2, 'إحنا الاتنين *Senior*؟', w='A')
bubble(T('S517', 'تدخل') - 1.0, 2.9, 'الـ*AI* بيدخل في شغلك؟', w='A')
note(S('S518'), 'الـAI *في كل شغلنا*', sticker='spark_o', accent='blue', d=3.6)
note(T('S535', 'برل'), 'شغال *حاجتين* في نفس الوقت', accent='olive', d=3.6)
note(T('S538', 'الوتينية'), 'الحاجات *الروتينية* = الـAI', accent='mustard', d=4.0)
note(T('S543', 'جاود'), 'بنطلّع *جودة أحسن*', sticker='check', accent='olive', d=3.6)
note(T('S546', 'بتتطور'), 'الدنيا *بتتطور* بسرعة… والله أعلم', accent='blue', d=4.2)
note(T('S551', 'مطلوب'), 'الشغل *لسه مطلوب*', accent='olive', d=3.6)
bubble(T('S561', 'تنصح'), E('S562') - T('S561', 'تنصح'), 'عايز *تنصح* بحاجة؟', w='A')
note(T('S567', 'بيخوفنا'), 'الـAI *مخوّفنا كلنا*', accent='orange', d=3.8)
bubble(T('S577', 'حابب'), E('S580') - T('S577', 'حابب'), 'الناس *توصلّك* إزاي؟', w='A')

note(T('S097', 'تولز'), 'بتتعلم *Tools جديدة*؟', accent='blue', d=3.8)
note(T('S125', 'والجزئات'), 'و*الجزء التاني*: الخبرة', accent='olive', d=4.0)
note(T('S128', 'اكشن'), 'لازم يحصل *Action* معيّن', accent='mustard', d=4.0)
note(T('S153', 'نظري'), 'رأي أيمن *الشخصي*', accent='blue', d=3.4)
note(T('S272', 'انواعه'), 'وإيه *أنواع* التستنج؟', sticker='qmark', accent='mustard', d=3.8)
note(T('S275', 'الأدوات'), 'والـ*Tools* اللي بيستخدمها', accent='olive', d=3.6)
note(T('S368', 'يحتك'), 'يحتك *بالـSoftware* كتير', accent='blue', d=3.8)
note(T('S377', 'عرف'), 'ناس *مش خريجين CS* شغالين عادي', accent='olive', d=4.2)
note(T('S381', 'يذاكر'), 'بس *لازم تذاكر*', sticker='star_y', accent='mustard', d=3.4)
note(T('S465', 'الستوري'), 'ستوري معيّنة = *Bug متوقّعة*', sticker='bug', accent='orange', d=4.0)

# ================= shots ("كادرات") =================
# Calm: hold a framing >= 3.5 s; short exchanges = both; long turns = the speaker alone, then both, then alone again with a
# gentle zoom INSIDE his tile (1.08, never twice in a row on the same person). Aly's camera dropped ~1126.5-1133 -> guest only.
FACE = {'G': (0.47, 0.36), 'A': (0.49, 0.55)}
turns = [[s, e, sp] for s, e, sp in SPK['turns'] if e > A0 and s < A1]
merged = []
for s, e, sp in turns:
    if merged and merged[-1][2] == sp and s - merged[-1][1] < 2.0: merged[-1][1] = e
    else: merged.append([s, e, sp])
shots, lastz = [], {'G': 1.0, 'A': 1.0}
t = A0
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
if shots: shots[-1][1] = A1


def apply(a, b, m, z=1.0):
    global shots
    res = []
    for s, e, mm, zz in shots:
        if e <= a or s >= b: res.append([s, e, mm, zz]); continue
        if s < a: res.append([s, a, mm, zz])
        if e > b: res.append([b, e, mm, zz])
    res.append([a, b, m, z]); res.sort(key=lambda x: x[0]); shots = res


for a, b, m in sorted(locks): apply(max(A0, a), min(A1, b), m)
for a, b in boards: apply(a, b, 'two')
apply(1126.0, 1133.5, 'G')
fixed = []
for s, e, m, z in shots:
    if e - s < 0.3:
        if fixed: fixed[-1][1] = e
        continue
    if fixed and fixed[-1][2] == m and abs(fixed[-1][3] - z) < 0.01: fixed[-1][1] = e
    elif fixed and e - s < 1.4: fixed[-1][1] = e   # too short to read -> stay
    else: fixed.append([s, e, m, z])
add('shot', 0.0, 17.13, m='full')
add('enta_glitch', 17.0, 0.3, seed=17); sfx(17.0, 'glitch', 0.25)
add('enta_glitch', 1806.35, 0.3, seed=18)
for s, e, m, z in fixed:
    sp = m[0] if m != 'two' else None
    props = {'m': m}
    if sp and z > 1.0 and m in ('G', 'A'): props.update(z=z, zx=FACE[sp][0], zy=FACE[sp][1])
    add('shot', max(17.13, s), e - max(17.13, s), **props)
add('shot', 1806.5, 1823.7 - 1806.5, m='full')

cues.sort(key=lambda c: c['src'])
plan = {'cut': False, 'captions': False, 'pack': 'charcoal', 'video': 'input/main video.mp4', 'quiet': [[0.0, 17.13], [1806.5, 1823.7]],
        'meet': {'G': [36, 290, 910, 470], 'A': [985, 290, 910, 470], 'left': 'G'}, 'cues': cues}
json.dump(plan, open(W / 'plan.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
cards = sorted((c['src'], c['src'] + c['dur']) for c in cues if c['t'].startswith(('enta_', 'qa_')) and c['t'] not in ('enta_glitch', 'enta_leak'))
gaps, prev = [], A0
for a, b in cards:
    if a - prev > 8: gaps.append((round(prev, 1), round(a, 1)))
    prev = max(prev, b)
if A1 - prev > 8: gaps.append((round(prev, 1), A1))
lens = [e - s for s, e, m, z in fixed]
print(len(cues), 'cues;', len(fixed), 'shots; avg', round(sum(lens) / len(lens), 2), 's; min', round(min(lens), 2), '; boards', len(boards))
print('no-graphic stretches > 8 s:', gaps)

"""Oz chapters 1, 3, 4, 5 -> shorts 32, 34, 35, 36, 37, 38, 39, 40 (playlist order). Same approved recipe as short 33.
Times = seconds in his chapter video. Field scenes (his whole frame + the field's motion) get clip='cam' (the short's own camera file)."""
from shorts_data import SHORTS as _S

OZ_FIX = dict(_S[33]['WFIX'])
OZ_FIX.update({'دورسي': 'دورثي', 'برشي': 'دورثي', 'قوس': 'أوز', 'قص': 'أوز', 'بوس': 'أوز', 'المقاتة': 'المآتة', 'ماتة': 'مآتة', 'المقات': 'المآتة',
               'المئاتة': 'المآتة', 'السحر': 'الساحر', 'سريدي': '3D', 'السريدي': 'الـ3D', 'الفيكس': 'إفكتس', 'افكتس': 'إفكتس', 'كومبوزوتينج': 'كمبوزيتنج',
               'وبكسفه.': '--', 'الاداعة': 'الإبداع', 'والابتهاد': 'والاجتهاد', 'واتعم': 'واتعلّم', 'ترفحها': 'ترفعها', 'بيكوي': 'بيقوّي', 'بهانسي': 'Behance',
               'بيهانس': 'Behance', 'جغل': 'شغل', 'حاليات': 'حاجات', 'بحرل': 'بحر', 'المثائقية': 'الوثائقية', 'سينانية': 'سينمائية', 'بازيت': 'بسيط',
               'الموار': '--', 'أسجار': 'أشجار', 'وأخصانها': 'وأغصانها', 'الممتقة': 'المنطقة', 'الوسعة': 'الواسعة', 'مربعبين': 'مرعوبين', 'وتلع': 'وطلع',
               'بورتوفوليو': 'بورتفوليو', 'سيحة': '--', 'فلقصت': 'فالأسد', 'عايقش': 'عايش', 'كرافك': 'جرافيك', 'دأخرهم': 'وأخّرهم', 'الاسفل': 'الأصفر',
               'زغال': 'وشغل', 'أجابة': '--', 'ويورروا': 'ويورّوا', 'لضاقة': 'الإضاءة', 'قلني': 'قولّي', 'احترد': 'محتار', 'بيجاتي': '--', 'مجالي': 'مجال',
               'كوحي': '--', 'الأبنيات': 'الأمنيات', 'تطلو': 'تطلب', 'هروح': '--', 'عشر': '--', 'وماية': '--', 'واجه': 'وآجي', 'دائم': '--', 'عليكم': 'على ايه',
               'مستدن': 'مستني', 'مقفك': 'موقّفك', 'تخيب': 'تجيب', 'وتوضع': 'واتواضع', 'نقل': 'لو', 'وبتبع': 'وبتطلع', 'مكسبك': 'مكسبك', 'الصغر': 'الصور',
               'والسري': 'والـ3D', 'دي': 'دي', 'شداتك': 'شدّتك', 'بازن': 'بإذن', 'انككملت': 'إنك كمّلت', 'بيتولد': 'بيتولد', 'فاكة': 'فاكر', 'أصر': 'قصر', 'الأصر': 'القصر', 'الحجر': 'الحجري'})
F3 = ['f3_arch', 'f3_interior', 'f3_game', 'f3_pics', 'f3_cgi', 'f3_film', 'f3_ads']
F4 = ['f4_edit', 'f4_film', 'f4_vfx', 'f4_trad', 'f4_2d', 'f4_3d', 'f4_mg', 'f4_stop', 'f4_jobs']
HIDE = {k: (900, 1390, 220, 1) for k in F3 + F4 + ['jy_clip']}  # his whole frame is up: no circle (he is inside it)
CENTER = dict(face_center=[955, 745], face_r=265)
F3L = [dict(e='🏛️', ar='عمارة'), dict(e='🛋️', ar='ديكور'), dict(e='🎮', ar='ألعاب'), dict(e='🖼️', ar='صور'), dict(e='🎬', ar='CGI'), dict(e='🧸', ar='أفلام 3D'), dict(e='📺', ar='إعلانات')]
F4L = [dict(e='✂️', ar='مونتاج'), dict(e='🎥', ar='صناعة الأفلام'), dict(e='✨', ar='VFX'), dict(e='✏️', ar='أنيميشن'), dict(e='🔷', ar='موشن جرافيك'), dict(e='🧸', ar='ستوب موشن')]
ALL4 = ['scarecrow', 'tin', 'lion']


def oz(n, ep, label, vt, slug, pieces, scenes, **kw):
    d = dict(ep=ep, sec='oz', label=label, vid_title=f'المجالات و ساحر مدينة أوز | {vt}', slug=slug, pieces=pieces, scenes=scenes, WFIX=OZ_FIX, real=[],
             face=f'src_{ep}.mp4', face_pos={**HIDE, 'oz_many': (935, 300, 170)}, cam=True, **CENTER)
    d.update(kw)
    if d.get('face_shape') == 'rect':  # Aly 2026-10-23 (37-40): his face bigger, a rectangle showing the room; lessons make room on the right
        RECT = (810, 1360, 330, 0)
        d['face_pos'] = {**d['face_pos'], **{s['t']: RECT for s in scenes if s['t'] not in d['face_pos']}}
        # scenes whose characters fill the bottom right: above the wizard / in the sky, or hidden in the short title + castle shots
        d['face_pos'].update({'oz_walk': (810, 1360, 330, 1), 'c5_castle': (810, 1360, 330, 1), 'c5_reveal': (540, 790, 300, 0), 'oz_road': (810, 1360, 330, 0)})
        for s in scenes:
            if s['t'] in ('c5_lesson', 'c5_sites', 'oz_road'):
                s['room'] = True
    return n, d


def lesson(at, who, head, lines, **beats):
    b = {k: t for k, t, *_ in lines}; b.update(beats)
    return dict(t='c5_lesson', at=at, who=who, head=head, lines=[[k, txt] + list(rest) for k, t, txt, *rest in [(l[0], l[1], l[2], *l[3:]) for l in lines]], b=b)


OZ = dict([
    oz(32, '32', 'الفصل 1 من 5', 'الفصل الأول "المقدمة"', 'oz_intro', [(5.1, 11.8), (23.9, 91.3)], [
        dict(t='jy_clip', at=5.0, src='cam', box=[0, 0, 1920, 1080], title='المجالات و ساحر أوز', chips=[dict(t=25.1, text='📺 خلّصت "هو ايه"'), dict(t=28.4, text='🤔 محتار تتخصص في ايه؟')]),
        dict(t='c1_book', at=32.2, b=dict(dorothy=35.8, oz=38.6)),
        dict(t='c1_lost', at=47.0, b=dict(signs=50.5)),
        dict(t='c1_city', at=54.6, b=dict(wizard=60.8)),
        dict(t='c1_princess', at=66.1, b=dict(road=71.5, end=75.6)),
        dict(t='oz_walk', at=79.6, chap='الفصل الأول:', chapB='المقدمة', b=dict(city=81.1)),
        dict(t='oz_road', at=84.3, chars=[], next='الفصل الجاي: الصور 🖼️ وخيال المآتة', b=dict(road=88.1)),
    ], face_track='face_32_clean.json'),
    oz(34, '34', 'الفصل 3 من 5', 'الفصل الثالث "3D"', 'tinman_3d', [(1.6, 4.1), (14.0, 163.2)], [
        dict(t='oz_walk', at=1.4, chap='الفصل التالت:', chapB='3D', chars=['scarecrow'], b=dict(city=16.1)),
        dict(t='c3_land', at=17.0, b=dict(work=23.0)),
        dict(t='c3_tin', at=27.6, b=dict(oil=31.5, move=35.0, ask=37.5)),
        dict(t='oz_many', at=41.0, list=F3L, title='مجالات', titleEn='3D', sub='داخل في مجالات كتير جدًا', some='تعالي أقولك 👇', b=dict(some=43.5)),
        dict(t='f3_arch', at=44.4, clip='cam'), dict(t='f3_interior', at=55.4, clip='cam'), dict(t='f3_game', at=60.8, clip='cam'),
        dict(t='f3_pics', at=76.4, clip='cam'), dict(t='f3_cgi', at=87.7, clip='cam'), dict(t='f3_film', at=101.5, clip='cam'), dict(t='f3_ads', at=106.5, clip='cam'),
        dict(t='c3_principles', at=116.4),
        dict(t='c3_wish', at=130.6, b=dict(heart=143.3)),
        dict(t='oz_road', at=145.6, chars=['scarecrow', 'tin'], next='الفصل الجاي: الأسد 🦁 والفيديو', b=dict(road=160.4)),
    ]),
    # Aly 2026-10-23: 35 + 36 merged into ONE short under 3:00 (whole chapter 4); only repeats/asides left out:
    # extra VFX details 115.7-136.4, part of the motion-graphics uses 170.9-182.7, part of the roles 190.1-199.8, the sleep + joke 216.3-229.4
    oz(35, '35', 'الفصل 4 من 5', 'الفصل الرابع "فيديو"', 'lion_video', [(0.2, 1.6), (11.7, 115.5), (136.4, 139.5), (139.8, 170.7), (182.7, 189.9),
                                                                         (199.8, 204.0), (204.8, 215.5), (229.4, 233.2)], [
        dict(t='oz_walk', at=0.0, chap='الفصل الرابع:', chapB='فيديو', chars=['scarecrow', 'tin'], b=dict(city=1.0)),
        dict(t='c4_forest', at=12.9, b=dict(video=23.2)),
        dict(t='c4_lion', at=27.5, b=dict(roar=32.0, stop=39.0, scared=43.0)),
        dict(t='c4_fear', at=44.4, b=dict(upload=46.5, portfolio=50.0, people=54.6)),
        dict(t='c4_invite', at=62.0, b=dict(yes=70.1)),
        dict(t='oz_many', at=77.7, list=F4L, title='مجالات', titleEn='Video', sub='الفيديو كبير جدًا وجميل', some='تعالي أقولك 👇', b=dict(some=80.0)),
        dict(t='f4_edit', at=81.0, clip='cam'), dict(t='f4_film', at=97.0, clip='cam'), dict(t='f4_vfx', at=107.3, clip='cam'),
        dict(t='c4_intro2', at=139.6),
        dict(t='f4_trad', at=143.8, clip='cam'), dict(t='f4_2d', at=149.3, clip='cam'), dict(t='f4_3d', at=156.8, clip='cam'), dict(t='f4_mg', at=161.3, clip='cam'),
        dict(t='f4_stop', at=182.6, clip='cam'), dict(t='f4_jobs', at=186.0, clip='cam'),
        dict(t='oz_road', at=204.7, chars=ALL4, next='الفصل الأخير: الساحر ✨', b=dict(road=229.5), room=True),
    ], face_pos={**HIDE, 'oz_many': (935, 300, 170), 'c4_intro2': (920, 770, 200, 1)}),
    oz(36, '35', 'الفصل 4 من 5 · جزء 2', 'الفصل الرابع "فيديو"', 'lion_animation', [(139.8, 232.8)], [
        dict(t='c4_intro2', at=139.6),
        dict(t='f4_trad', at=143.8, clip='cam'), dict(t='f4_2d', at=149.3, clip='cam'), dict(t='f4_3d', at=156.8, clip='cam'), dict(t='f4_mg', at=161.3, clip='cam'),
        dict(t='f4_stop', at=182.0, clip='cam'), dict(t='f4_jobs', at=186.0, clip='cam'),
        dict(t='c4_sleep', at=202.7, b=dict(sleep=218.8, focus=222.0)),
        dict(t='oz_road', at=229.4, chars=ALL4, next='الفصل الأخير: الساحر ✨', b=dict(road=230.1)),
    ]),
    oz(37, '36', 'الفصل 5 من 5 · جزء 1', 'الفصل الخامس و الأخير "الختام"', 'wizard_scarecrow', [(0.4, 1.3), (11.5, 127.1)], [
        dict(t='oz_walk', at=0.2, chap='الفصل الخامس:', chapB='الختام', chars=ALL4, b=dict(city=1.0)),
        dict(t='c5_castle', at=11.5, b=dict(meet=19.7)),
        dict(t='c5_reveal', at=21.8, b=dict(man=23.0, sad=28.4, good=33.0, help=44.2)),
        lesson(50.3, 'scarecrow', 'الساحر لخيال المآتة 🧠', [('l1', 51.9, 'مشكلتك مش في العقل'), ('l2', 54.6, 'واقف مستني المعلومة تيجي لك ⏳', 'red'), ('l3', 63.9, 'أي حد يقدر يتعلم أي حاجة 💪', 'gold')]),
        dict(t='c5_search', at=64.8, b=dict(results=74.0, visual=81.9, solve=89.7)),
        lesson(96.4, 'scarecrow', 'إزاي تكمّل؟', [('a', 98.4, 'اتعلم الأصول 📚'), ('b', 102.1, 'كورسات أونلاين وأوفلاين 🎓'), ('c', 104.4, 'مبادئ التصميم ✏️'),
                                                  ('d', 108.0, 'البرامج اللي محتاجها 🖥️'), ('e', 110.0, 'اسأل كتير 🙋'), ('f', 112.5, 'طبّق كتير جدًا 🔁', 'gold'),
                                                  ('g', 124.5, 'الصبر والاجتهاد ⏳💪', 'gold')]),
    ], face_shape='rect'),
    oz(38, '36', 'الفصل 5 من 5 · جزء 2', 'الفصل الخامس و الأخير "الختام"', 'wizard_lion', [(127.8, 170.3)], [
        lesson(127.6, 'lion', 'الساحر للأسد 🦁', [('a', 130.0, 'ما تخافش.. ارفع شغلك ☁️'), ('b', 132.5, 'كلنا بنتعلم ونتطوّر 🌱'), ('c', 140.0, 'قلّد شغل معمول أو لشركة وهمية 🏢'),
                                                  ('d', 148.5, 'الرفض نفسه خبرة 👍', 'gold'), ('e', 152.0, 'بعد سنين هتشوف تطوّرك 📈'), ('f', 167.4, 'العزيمة والإصرار 🔥', 'gold')], brave=165.0),
    ], face_shape='rect'),
    oz(39, '36', 'الفصل 5 من 5 · جزء 3', 'الفصل الخامس و الأخير "الختام"', 'wizard_tinman', [(171.4, 224.3)], [
        lesson(171.2, 'tin', 'الساحر للراجل الحديدي ❤️', [('a', 175.0, 'الناس مش بتتولد مبدعة', 'red'), ('b', 182.0, 'الإبداع صفة بتنمّيها 🌱', 'gold'), ('c', 194.3, 'شغف وحب للي بتعمله ❤️')], heart=194.3),
        dict(t='c5_sites', at=197.5, b=dict(sites=198.9, groups=207.7)),
        lesson(212.7, 'tin', 'الإبداع ييجي منين؟', [('a', 212.9, 'اتفرّج كتير 👀'), ('b', 218.0, 'مش إنك فنان..'), ('c', 221.3, 'إنك مجتهد 💪', 'gold')], heart=212.8),
    ], face_shape='rect'),
    oz(40, '36', 'الفصل 5 من 5 · جزء 4', 'الفصل الخامس و الأخير "الختام"', 'wizard_dorothy', [(224.7, 280.0)], [
        lesson(224.5, 'dorothy', 'الساحر لدورثي 👧', [('a', 231.5, 'مكسبك كان في الطريق الأصفر 🟨', 'gold'), ('b', 234.0, 'عرفتي مجالات كتير: صور • فيديو • 3D'),
                                                     ('c', 240.2, 'افتحي Behance وقلّبي 🔍'), ('d', 247.6, 'اعرفي اسم اللي شدّك ودوّري فيه'),
                                                     ('e', 251.2, 'تحت كل شغل مكتوب البرامج 🖥️'), ('f', 257.4, 'جرّبي مجالات كتير 🧪', 'gold')]),
        dict(t='oz_road', at=266.7, chars=ALL4, line='شكرًا إنك كمّلت الطريق لحد الآخر 🟨', next='شوف البلايليست كاملة 👇', b=dict(road=274.9)),
    ], face_shape='rect'),
])

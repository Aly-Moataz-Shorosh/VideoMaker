# Shorts 04..20 of the film-making course (Aly 2026-11-07: "اعمل باقي الفيديوهات و عايزك تبدع", order = most exciting first,
# every short complete on its own). Same piece format as fs_data.py. Crops in the 1280x720 proxy; the stage is 1016x760
# (crop height = 0.748 x sw, sw <= 962 for the whole height).
FULL = dict(sx=160, sy=0, sw=960)
L = lambda sx, sy, sw: dict(sx=sx, sy=sy, sw=sw)
FT = lambda title, year, note='المشهد اللي عرضه في الكورس': dict(title=title, year=year, note=note)
T = lambda t, text, c=None: dict(t=t, text=text, **({'c': c} if c else {}))
PIPE = [dict(name='Discovery', ar='الاكتشاف: الفكرة والهدف', img='light_bulb', at=0.1), dict(name='Pre-production', ar='التحضير: سكريبت وتخطيط', img='scroll', at=0.3),
        dict(name='Production', ar='التصوير والصوت', img='movie_camera', at=0.5), dict(name='Post-production', ar='المونتاج والموشن والصوت', img='film_frames', at=0.7),
        dict(name='Distribution', ar='التوزيع: يوتيوب والمنصات', img='globe_with_meridians', at=0.9)]

SHORTS = {
    # 04 split diopter: the info he had wrong for years
    4: dict(no=4, chapter=25, title='المعلومة اللي كنت *فاهمها غلط*', pieces=[
        dict(a=3429.4, b=3437.7, crop=FULL, film=FT('الجزيرة', '2007'), lab=[(0.3, 'Split diopter', None, 2.4)]),
        dict(a=3396.9, b=3409.8, crop=L(200, 60, 870), rew=True, kw=[('Split diopter', 'عدسة بتخلي القريب والبعيد واضحين', 3.6)]),
        dict(a=3409.8, b=3421.7, show='FocusScene', anim=dict(keys=[[3409.8, 'fake']], tags=[T(3413.2, 'فيديو قديم ليّا.. على معلومة غلط', '#E5232B')])),
        dict(a=3421.7, b=3429.4, crop=L(220, 60, 860), src=3424.5, lab=[(1.5, 'عدسة.. نصها بس', None, 2.2)]),
        dict(a=3429.4, b=3437.7, show='FocusScene', anim=dict(keys=[[3429.4, 'shallow'], [3432.7, 'split']], tags=[T(3433.4, 'القريب واضح.. والبعيد واضح'), T(3435.6, 'والنص مغبّش')])),
    ]),
    # 05 the cut has a meaning (Kuleshov idea in his words)
    5: dict(no=5, chapter=16, title='القطع *ليه معنى*', pieces=[
        dict(a=1620.5, b=1628.3, show='CutMeaning', anim=dict(bAt=0.3, resultAt=0.62)),
        dict(a=1595.0, b=1607.3, crop=FULL, src=1590.5, rew=True, film=FT('Se7en', '1995'), lab=[(4.6, 'نخش جوه دماغه', None, 2.2)]),
        dict(a=1608.7, b=1617.1, crop=FULL, src=1598, lab=[(0.3, 'جزء من ثانية', None, 1.8)], kw=[('Cut', 'القطع = رسالة', 3.4)]),
        dict(a=1617.1, b=1628.3, show='CutMeaning', anim=dict(bAt=0.5, resultAt=0.78)),
        dict(a=1658.3, b=1667.0, show='CutMeaning', anim=dict(mode='music', bAt=0.45, result='= إحساس بالأزمة', resultAt=0.7)),
    ]),
    # 06 camera moves with a tripod + dolly zoom
    6: dict(no=6, chapter=26, title='حركة الكاميرا و *Dolly zoom*', pieces=[
        dict(a=3626.2, b=3634.8, show='MoveScene', anim=dict(keys=[[3626.2, 'dolly']], tags=[T(3630.8, 'زوم عكس الحركة')])),
        dict(a=3474.3, b=3484.8, show='MoveScene', anim=dict(keys=[[3474.3, 'intro']]), rew=True),
        dict(a=3493.3, b=3512.1, show='MoveScene', anim=dict(keys=[[3493.3, 'static']], tags=[T(3500.0, 'ترايبود = الكاميرا ثابتة')])),
        dict(a=3523.6, b=3548.1, show='MoveScene', anim=dict(keys=[[3523.6, 'tilt']], tags=[T(3528.2, 'الدراع: فوق وتحت')]), kw=[('Tilt', 'الكاميرا بتبص لفوق ولتحت', 6.0)]),
        dict(a=3548.1, b=3562.8, show='MoveScene', anim=dict(keys=[[3548.1, 'pan']]), kw=[('Pan', 'يمين وشمال', 2.0)]),
        dict(a=3562.8, b=3576.6, crop=L(200, 60, 870), src=3584, film=FT('Once Upon a Time in Hollywood', '2019')),
        dict(a=3606.1, b=3614.3, show='MoveScene', anim=dict(keys=[[3606.1, 'push'], [3610.5, 'dolly']])),
        dict(a=3626.2, b=3634.8, show='MoveScene', anim=dict(keys=[[3626.2, 'dolly']], tags=[T(3626.8, 'تزق الترايبود لورا'), T(3630.8, 'وتعمل زوم عكس الحركة')])),
    ]),
    # 07 focus sends a message
    7: dict(no=7, chapter=25, title='الفوكس *بيوصل رسالة*', pieces=[
        dict(a=3368.5, b=3378.0, crop=FULL, src=3357, kw=[('Focus puller', 'شغلانته يغيّر الفوكس طول المشهد', 1.6)]),
        dict(a=3225.2, b=3240.8, crop=L(300, 0, 700), src=3237, rew=True, lab=[(9.0, 'الفوكس بيوصل رسالة', None, 2.4)]),
        dict(a=3243.0, b=3254.5, show='FocusScene', anim=dict(keys=[[3243.0, 'shallow'], [3249.3, 'deep']]), kw=[('Depth of field', 'المسافة اللي باينة واضحة', 0.4)]),
        dict(a=3256.0, b=3262.9, show='FocusScene', anim=dict(keys=[[3256.0, 'shallow'], [3261.4, 'deep']], tags=[T(3259.8, 'قطة بس؟'), T(3261.4, 'ولا المسافة كلها؟')])),
        dict(a=3265.2, b=3282.2, show='FocusScene', anim=dict(keys=[[3265.2, 'deep'], [3273.3, 'shallow']], tags=[T(3269.0, 'رجل فضاء وكوكب: الاتنين واضحين'), T(3273.3, 'ولو عايز حاجة واحدة بس')]), kw=[('Deep focus', 'كله واضح', 1.0)]),
        dict(a=3311.8, b=3313.7, show='FocusScene', anim=dict(keys=[[3311.8, 'shallow'], [3312.4, 'far']]), kw=[('Rack focus', 'الفوكس بيتنقل جوه اللقطة', 0.1)]),  # only his words (an English video talks before)
        dict(a=3354.6, b=3378.0, crop=FULL, src=3352),
    ]),
    # 08 video is a language: form + content (الكيف / الفيل الأزرق)
    8: dict(no=8, chapter=2, title='الفيديو *لغة*: شكل ومحتوى', pieces=[
        dict(a=207.8, b=222.0, crop=L(30, 200, 680), src=189, lab=[(0.5, 'كلغة سينمائية.. الاتنين عباقرة', None, 2.6)]),
        dict(a=93.3, b=117.0, crop=FULL, src=105, rew=True, lab=[(4.0, 'صور ورا بعض + صوت', None, 2.4), (17.0, 'وسيلة تواصل = لغة', None, 2.6)]),
        dict(a=136.9, b=150.1, show='big:الفيديو لغة|ليها شكل.. وليها محتوى', ico='film'),
        dict(a=150.8, b=180.4, crop=L(520, 180, 740), src=165, labels=[('الشكل', 'الشكل = طريقة الكتابة'), ('والمحتوى', 'المحتوى = المعنى')]),
        dict(a=180.7, b=192.1, crop=L(30, 200, 680), src=189, labels=[('الكيف', 'الكيف'), ('اللازرق', 'الفيل الأزرق')]),
        dict(a=222.0, b=239.4, show='big:مش بالأدوات بس|اللغة السينمائية معتمدة على البلاغة', ico='film'),
        dict(a=243.0, b=251.7, show='big:جمال في الشكل.. وجمال في المضمون', ico='film'),
    ]),
    # 09 shot sizes
    9: dict(no=9, chapter=20, title='أحجام *اللقطات*', pieces=[
        dict(a=2509.0, b=2526.4, crop=L(300, 60, 700), src=2508, kw=[('Establishing shot', 'تعرف انت فين من غير ما حد يقولك', 1.0)]),
        dict(a=2393.6, b=2402.1, crop=L(400, 100, 500), src=2400, rew=True, kw=[('Shot size', 'حجم اللقطة', 1.0)]),
        dict(a=2421.1, b=2445.3, crop=FULL, src=2428, zoom=[(2436, L(160, 0, 960))], labels=[('عينين', 'Extreme close up'), ('الكتاف', 'Close up / Medium'), ('كله', 'Full shot')]),
        dict(a=2445.3, b=2465.9, crop=L(20, 40, 640), src=2450, zoom=[(2455, L(620, 40, 640))], kw=[('Wide / Full / Medium', 'كل حجم بيقول حاجة', 6.0)]),
        dict(a=2509.0, b=2530.6, crop=L(300, 60, 700), src=2508, kw=[("Show, don't tell", 'ورّي.. متحكيش', 17.0)]),
    ]),
    # 10 the script describes everything before shooting
    10: dict(no=10, chapter=18, title='السكريبت *بيوصف كل حاجة*', pieces=[
        dict(a=2292.6, b=2304.5, crop=L(320, 60, 700), src=2296, lab=[(0.4, 'قبل التصوير', None, 2.0)]),
        dict(a=2131.5, b=2140.5, crop=L(300, 0, 720), src=2134, rew=True, lab=[(0.5, 'سكريبت إبراهيم الأبيض', None, 2.4)]),
        dict(a=2154.7, b=2165.9, crop=L(160, 0, 960), src=2164, kw=[('Sequence · Scene · Shot', 'تتابع · مشهد · لقطة', 2.0)]),
        dict(a=2224.6, b=2244.1, crop=L(320, 60, 700), src=2234, zoom=[(2238, L(400, 120, 560))]),
        dict(a=2253.7, b=2271.3, crop=L(320, 60, 700), src=2256, lab=[(14.0, 'ومش كل ده جه في المشهد', None, 2.4)]),
        dict(a=2292.6, b=2304.5, crop=L(320, 60, 700), src=2296),
        dict(a=2320.8, b=2344.1, show='Pipeline', anim=dict(items=PIPE[1:4], hi=[[2320.8, 0], [2335.2, 0], [2338.7, 1], [2340.5, 2]], tags=[T(2342.3, 'إدّي لكل خطوة حقها')])),
    ]),
    # 11 sequence / scene / shot with Ibrahim El Abyad
    11: dict(no=11, chapter=17, title='تتابع ومشهد *ولقطة*', pieces=[
        dict(a=2068.1, b=2081.6, crop=FULL, src=2047, film=FT('إبراهيم الأبيض', '2009')),
        dict(a=1977.5, b=1994.4, show='TreeScene', anim=dict(seqAt=6.0, sceneAt=10.0, shotAt=12.2), rew=True),
        dict(a=2058.0, b=2068.1, crop=FULL, src=2060, film=FT('إبراهيم الأبيض', '2009')),
        dict(a=2068.1, b=2088.6, crop=FULL, src=2071),
        dict(a=2089.1, b=2108.0, crop=FULL, src=2095),
        dict(a=2108.0, b=2114.2, show='TreeScene', anim=dict(film='إبراهيم الأبيض', seqAt=0.4, sceneAt=2.4, shotAt=4.6, tags=[T(2109.3, 'ده تتابع كامل')])),
    ]),
    # 12 framing + the 180 rule (his own camera demo in the middle: the webcam fills the card, so no circle there)
    12: dict(no=12, chapter=21, title='أنواع الـ *Framing*', pieces=[
        dict(a=2566.6, b=2583.2, crop=L(200, 0, 880), src=2570, nocam=True, kw=[('Dirty single', 'ظهر حد تاني باين في الكادر', 1.0)]),
        dict(a=2531.6, b=2551.4, crop=L(430, 100, 420), src=2540, rew=True, kw=[('POV', 'الكاميرا = عين الشخصية', 4.0)], lab=[(13.5, 'الكاميرا مكان الكورة', None, 2.4)]),
        dict(a=2552.0, b=2566.6, crop=L(430, 100, 420), src=2555, kw=[('Insert · Single clean', 'تفصيلة.. أو أنا بس في الكادر', 1.0)]),
        dict(a=2566.6, b=2583.2, crop=L(200, 0, 880), src=2570, nocam=True),
        dict(a=2584.0, b=2606.4, crop=L(120, 40, 900), src=2590, kw=[('Two shot · OTS', 'اتنين.. أو من ورا الكتف', 2.0)]),
        dict(a=2606.4, b=2613.7, show='big:قاعدة الـ 180 درجة|ما تعديش الخط اللي بين الاتنين', ico='cam'),
    ]),
    # 13 the process: fix it while shooting, not in post
    13: dict(no=13, chapter=10, title='صلّحها وانت *بتصوّر*', pieces=[
        dict(a=994.4, b=1002.3, show='Pipeline', anim=dict(items=PIPE[1:4], hi=[[994.4, 1]], tags=[T(994.4, 'المكتب اللي ورا ظهرك؟ شيله دلوقتي', '#E5232B')])),
        dict(a=894.7, b=905.6, show='Pipeline', anim=dict(items=PIPE[1:4], hi=[[894.7, -1]]), rew=True),
        dict(a=905.6, b=930.0, crop=L(380, 60, 520), src=908, kw=[('Production', 'التصوير: قلل الارتجال', 4.0)]),
        dict(a=955.7, b=970.5, crop=L(700, 60, 560), src=960, kw=[('Post-production', 'مونتاج، موشن، صوت، ألوان', 3.0)]),
        dict(a=979.2, b=1002.3, show='Pipeline', anim=dict(items=PIPE[1:4], hi=[[979.2, 2], [981.5, 1]], tags=[T(987.0, 'صوت مزعج؟ شيله وانت بتصور'), T(994.4, 'متقولش هشيله في البوست', '#E5232B')])),
        dict(a=1023.2, b=1047.0, show='Pipeline', anim=dict(items=PIPE, hi=[[1023.2, 0], [1038.5, 4]])),
    ]),
    # 14 the five animation types
    14: dict(no=14, chapter=6, title='أنواع *الأنيميشن الخمسة*', pieces=[
        dict(a=641.1, b=658.4, crop=L(150, 0, 960), src=643, kw=[('Stop motion', 'تصور وتحرك خطوة', 2.0)]),
        dict(a=573.2, b=584.5, crop=L(150, 0, 960), src=583, rew=True, kw=[('Traditional', 'بيترسم فريم فريم', 6.0)]),
        dict(a=585.5, b=603.2, crop=L(150, 0, 960), src=592, kw=[('2D animation', 'الكاركتر بيترسم مرة ويتحرك', 3.0)]),
        dict(a=606.0, b=611.6, crop=L(150, 0, 960), src=611, kw=[('3D / CG', 'موديل 3D بيتحرك', 0.6)]),
        dict(a=617.6, b=636.9, crop=L(150, 0, 960), src=622, kw=[('Motion graphics', 'إعلانات وشرح', 6.0)]),
        dict(a=636.9, b=658.4, crop=L(150, 0, 960), src=645, lab=[(5.0, 'الأنبياء المرسلون', None, 2.4)]),
    ]),
    # 15 visual literacy
    15: dict(no=15, chapter=16, title='محو *الأمية البصرية*', pieces=[
        dict(a=1735.4, b=1744.1, show='LiteracyScene', anim=dict(rows=[dict(img='musical_notes', a='كلنا بنسمع أغاني', b='مش كلنا بنكتبها', at=0.1), dict(img='scroll', a='كلنا بنستمتع بالزخارف', b='مش كلنا بنقراها', at=2.4)])),
        dict(a=1465.5, b=1487.0, crop=FULL, src=1440, rew=True, lab=[(0.4, 'Martin Scorsese', None, 2.2)], kw=[('Visual literacy', 'إنك تقرا الصورة وتكتبها', 6.0)]),
        dict(a=1732.5, b=1744.1, show='LiteracyScene', anim=dict(rows=[dict(img='musical_notes', a='كلنا بنسمع أغاني', b='مش كلنا بنكتبها', at=1.0), dict(img='scroll', a='كلنا بنستمتع بالزخارف', b='مش كلنا بنقراها', at=4.7)])),
        dict(a=1744.9, b=1761.7, show='LiteracyScene', anim=dict(rows=[dict(img='cinema', a='كلنا بنحب الأفلام', b='مش كلنا بنقرا حروفها', at=0.2)],
             letters=['Shot size', 'Angle', 'Framing', 'Focus', 'Movement', 'Cut'], lettersAt=8.0)),
    ]),
    # 16 rule of thirds
    16: dict(no=16, chapter=23, title='قاعدة *الأثلاث*', pieces=[
        dict(a=2888.4, b=2897.9, crop=FULL, src=2890, lab=[(4.0, 'حط الشخصية على التقاطع', None, 2.4)]),
        dict(a=2864.5, b=2872.6, crop=L(400, 0, 500), src=2866, rew=True, kw=[('Composition', 'قواعد تكوين الصورة', 1.0)]),
        dict(a=2875.3, b=2887.0, crop=FULL, src=2880, lab=[(2.0, 'Steve McCurry', None, 2.2)]),
        dict(a=2888.4, b=2906.4, crop=FULL, src=2892, zoom=[(2897.5, FULL)], kw=[('Rule of thirds', 'الكادر 3 × 3', 1.0)]),
    ]),
    # 17 what a good film maker needs
    17: dict(no=17, chapter=3, title='الفيلم ميكر *الشاطر*', pieces=[
        dict(a=298.2, b=306.4, crop=L(160, 0, 960), src=290, lab=[(1.8, 'لازم تكون شاعر', None, 2.4)]),
        dict(a=260.6, b=285.1, crop=L(160, 0, 960), src=272, rew=True, labels=[('بتبيع', 'تبيع'), ('تعرفها', 'تعرّف'), ('فسلية', 'تسلّي'), ('قصة', 'تحكي قصة')]),
        dict(a=285.1, b=310.6, crop=L(160, 0, 960), src=290, labels=[('ستوري', 'Storyteller'), ('سولفر', 'Problem solver'), ('قرارات', 'Decision maker'), ('صبور', 'صبور')]),
        dict(a=347.1, b=370.8, crop=L(160, 0, 960), src=345, lab=[(8.5, 'الكاميرا مكان الكورة', None, 2.4)]),
        dict(a=414.6, b=437.5, crop=L(160, 0, 960), src=400, film=FT('BBC Sport · World Cup 2018', 'trailer', 'الفيديو اللي عرضه في الكورس')),
        dict(a=437.5, b=457.4, show='big:فكّر قبل ما تصوّر|علشان توصل الفكرة بأبلغ وأجمل طريقة', ico='film'),
    ]),
    # 18 aspect ratio: decide before you shoot
    18: dict(no=18, chapter=13, title='الـ *Aspect ratio*', pieces=[
        dict(a=1196.7, b=1203.6, show='AspectScene', anim=dict(keys=[[1196.7, '4:3', 'الأفلام القديمة'], [1201.7, '16:9', 'الأفلام الحديثة']])),
        dict(a=1131.2, b=1153.7, crop=L(0, 150, 640), src=1134, zoom=[(1139.7, L(330, 150, 640)), (1149.4, L(640, 150, 640))], rew=True),
        dict(a=1157.5, b=1163.7, crop=L(0, 100, 800), src=1153, kw=[('Frames', 'الفيديو = صور ورا بعض', 1.0)]),
        dict(a=1171.8, b=1196.7, show='AspectScene', anim=dict(keys=[[1171.8, '4:3', 'التلفزيون'], [1173.7, '16:9', 'يوتيوب'], [1189.0, '9:16', 'ريلز وموبايل'], [1191.5, '1:1', 'إنستجرام']])),
        dict(a=1196.7, b=1203.6, show='AspectScene', anim=dict(keys=[[1196.7, '4:3', 'الأفلام القديمة'], [1201.7, '16:9', 'الأفلام الحديثة']])),
    ]),
    # 19 still vs moving pictures: the line from animation to film
    19: dict(no=19, chapter=5, title='رسوم متحركة ولا *صور متحركة*؟', pieces=[
        dict(a=542.7, b=553.6, crop=L(560, 120, 720), src=509, lab=[(0.4, 'Stop motion: في النص', None, 2.4)]),
        dict(a=488.8, b=500.5, crop=L(160, 0, 960), src=470, rew=True, labels=[('متحرك', 'المتحرك'), ('صور', 'صور متحركة'), ('رسوم', 'رسوم متحركة')]),
        dict(a=500.7, b=535.8, crop=L(0, 120, 720), src=509, zoom=[(522.0, L(280, 120, 720))], kw=[('2D · 3D', 'أقرب للرسوم', 8.0)]),
        dict(a=535.9, b=570.4, crop=L(560, 120, 720), src=509, kw=[('VFX · Film', 'أقرب للصور', 22.0)]),
    ]),
    # 20 camera gear
    20: dict(no=20, chapter=27, title='أدوات *الكاميرا*', pieces=[
        dict(a=3850.5, b=3859.9, crop=L(240, 60, 800), src=3852, kw=[('Gimbal', 'حركة هاند هيلد ثابتة', 1.0)]),
        dict(a=3830.1, b=3840.8, crop=L(300, 0, 700), src=3838, rew=True, kw=[('Tripod', 'حتى للموبايل', 6.6)]),
        dict(a=3843.4, b=3850.5, crop=L(300, 0, 700), src=3846, kw=[('Track / Dolly', 'تحرك الكاميرا يمين وشمال', 3.0)]),
        dict(a=3867.9, b=3878.7, crop=L(300, 0, 700), src=3866, kw=[('Waterproof case', 'الكاميرا تحت المية', 1.0)]),
    ]),
}
CAP = {}

# caption fixes on the re-transcribed words (words he said, spelled right)
FIX = {'trybud': 'ترايبود', 'trybud.': 'ترايبود.', 'ترايبوت': 'ترايبود', 'دولة': 'دولي', 'المجزيرة': 'الجزيرة', 'diopeter': 'diopter', 'established': 'Establishing',
       'white': 'wide', 'الestablishing': 'الـ Establishing', 'فالsequence': 'فالـ Sequence', 'الcharacters': 'الـ characters', 'شرط': 'شوت', 'سايدز': 'سايز',
       'سايدز،': 'سايز،', 'مفمت': 'موفمنت', 'بتزوء': 'بتزق', 'تزوء': 'تزق', 'كيف': 'الكيف', 'الكرداري': 'للجريد', 'الجردالي': 'للجريد', 'الجرداري': 'للجريد'}
CAP[8] = ['لكن بقى كلغة سينمائية.. الاتنين عباقرة.. وفيلم الكيف كلغة سينمائية عبقري عبقري.. لأنه مش بس بيتكلم على المخدرات.. وبيتكلم على اللغة.. فيلم عبقري سينمائيا']

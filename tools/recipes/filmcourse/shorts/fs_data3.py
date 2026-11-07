# Aly's review 1 of the 20 film-course shorts (2026-11-07, work/review_shorts_1.md) -> the shorts that change. Overrides fs_data/fs_data2.
# New piece keys: raw (a clip he played: exact edges + its own sound), file (another public file: ibrahim720.mp4 = the analysed
# Ibrahim El Abyad scene padded to 1280x720, wc06.mp4 = his webcam at native size during the tripod demo), seq (several shots in one card).
from fs_data2 import FULL, L, FT, T, PIPE

IB = 'ibrahim720.mp4'
IBC, IBL, IBR = L(268, 81, 745), L(60, 81, 745), L(535, 81, 745)
NOWC = L(150, 30, 840)          # course screen without his webcam corner (x <= 990, y <= 658)
SH = lambda *xs: [list(x) for x in xs]
IBF = FT('إبراهيم الأبيض', '2009', 'المشهد اللي حللناه في الفيديو التاني')

SHORTS = {
    # 04: hook = the الجزيرة split-diopter clip he played (no tilt shift), his second الجزيرة example in, edges on word gaps
    4: dict(no=4, chapter=25, title='المعلومة اللي كنت *فاهمها غلط*', pieces=[
        dict(a=3429.4, b=3435.4, crop=L(40, 60, 1000), src=3466.0, film=FT('الجزيرة', '2007'), lab=[(0.3, 'Split diopter', None, 2.4)]),
        dict(a=3396.9, b=3409.8, crop=L(200, 60, 870), rew=True, kw=[('Split diopter', 'عدسة بتخلي القريب والبعيد واضحين', 3.6)]),
        dict(a=3409.8, b=3421.7, show='FocusScene', anim=dict(keys=[[3409.8, 'fake']], tags=[T(3413.2, 'فيديو قديم ليّا.. على معلومة غلط', '#E5232B')])),
        dict(a=3421.7, b=3429.4, crop=L(220, 60, 860), lab=[(1.5, 'عدسة.. نصها بس', None, 2.2)]),
        dict(a=3429.4, b=3435.4, crop=L(200, 60, 870), film=FT('الجزيرة', '2007')),
        dict(a=3458.3, b=3474.4, raw=True, crop=L(40, 60, 1000), film=FT('الجزيرة', '2007', 'المثال التاني اللي عرضه')),
        dict(a=3429.4, b=3435.4, show='FocusScene', anim=dict(keys=[[3429.4, 'shallow'], [3431.0, 'split']], tags=[T(3431.3, 'القريب واضح.. والبعيد واضح'), T(3433.6, 'والنص مغبّش')])),
    ]),
    # 05: the train in perspective (scene), the caption at 0:17, WHEN the cut-for-meaning idea appeared (source), the scene he comments on
    5: dict(no=5, chapter=16, title='القطع *ليه معنى*', pieces=[
        dict(a=1620.5, b=1628.3, show='CutMeaning', anim=dict(bAt=0.3, resultAt=0.62)),
        dict(a=1595.0, b=1607.3, crop=NOWC, src=1590.5, rew=True, film=FT('Se7en', '1995')),
        dict(a=1608.7, b=1614.3, crop=NOWC, src=1598, lab=[(0.3, 'جزء من ثانية', None, 1.8)], kw=[('Cut', 'القطع = رسالة', 3.0)]),
        dict(a=1614.4, b=1620.5, show='FactCard', anim=dict(title='إمتى ظهرت الفكرة دي؟', text='تجربة المخرج الروسي ليف كوليشوف حوالي 1918 (المصادر مختلفة على السنة): نفس الوش + لقطة مختلفة = إحساس مختلف',
             src='University of Leeds · Facing the Mind: The Kuleshov effect')),
        dict(a=1620.5, b=1628.3, show='CutMeaning', anim=dict(bAt=0.5, resultAt=0.78)),
        dict(a=1644.0, b=1657.9, raw=True, crop=NOWC, film=FT('Misery', '1990', 'المشهد اللي بيعلّق عليه')),
        dict(a=1658.3, b=1667.0, show='CutMeaning', anim=dict(mode='music', bAt=0.45, result='= إحساس بالأزمة', resultAt=0.7)),
    ]),
    # 06: real dolly-zoom example (Raging Bull), his webcam as a big rectangle while he shows the tripod, no "after the course" sentence
    6: dict(no=6, chapter=26, title='حركة الكاميرا و *Dolly zoom*', pieces=[
        dict(a=3626.2, b=3634.8, crop=L(40, 60, 1000), src=3796.0, film=FT('Raging Bull', '1980', 'مثال Dolly zoom'), lab=[(0.3, 'Dolly zoom', None, 2.2)]),
        dict(a=3474.3, b=3484.8, show='MoveScene', anim=dict(keys=[[3474.3, 'intro']]), rew=True),
        dict(a=3493.3, b=3512.1, file='wc06.mp4', src=3493.3 - 3480, crop=L(128, 0, 1024), nocam=True, kw=[('Static', 'الكاميرا ثابتة', 8.0)]),
        dict(a=3523.6, b=3548.1, file='wc06.mp4', src=3523.6 - 3480, crop=L(128, 0, 1024), nocam=True, kw=[('Tilt', 'فوق وتحت', 6.0)]),
        dict(a=3548.1, b=3562.8, file='wc06.mp4', src=3548.1 - 3480, crop=L(128, 0, 1024), nocam=True, kw=[('Pan', 'يمين وشمال', 2.0)]),
        dict(a=3569.4, b=3576.6, crop=L(150, 30, 840), src=3584, film=FT('Once Upon a Time in Hollywood', '2019')),
        dict(a=3606.1, b=3614.3, show='MoveScene', anim=dict(keys=[[3606.1, 'push'], [3610.5, 'dolly']])),
        dict(a=3626.2, b=3634.8, show='MoveScene', anim=dict(keys=[[3626.2, 'dolly']], tags=[T(3626.8, 'تزق الترايبود لورا'), T(3630.8, 'وتعمل زوم عكس الحركة')])),
        dict(a=3626.2, b=3634.8, crop=L(40, 60, 1000), src=3802.0, film=FT('Raging Bull', '1980', 'شوف الخلفية بتتمط')),
    ]),
    # 07: from the middle on: the real pictures/clips on his screen while he explains
    7: dict(no=7, chapter=25, title='الفوكس *بيوصل رسالة*', pieces=[
        dict(a=3368.5, b=3378.0, crop=NOWC, kw=[('Focus puller', 'شغلانته يغيّر الفوكس طول المشهد', 1.6)]),
        dict(a=3225.2, b=3240.8, crop=L(300, 0, 700), rew=True, lab=[(9.0, 'الفوكس بيوصل رسالة', None, 2.4)]),
        dict(a=3243.0, b=3254.5, crop=L(280, 0, 720), kw=[('Depth of field', 'المسافة اللي باينة واضحة', 0.4)]),
        dict(a=3256.0, b=3262.9, show='FocusScene', anim=dict(keys=[[3256.0, 'shallow'], [3261.4, 'deep']], tags=[T(3259.8, 'قطة بس؟'), T(3261.4, 'ولا المسافة كلها؟')])),
        dict(a=3265.2, b=3282.2, crop=L(330, 150, 620), kw=[('Deep focus', 'كله واضح', 2.0)]),
        dict(a=3285.4, b=3302.6, crop=NOWC, kw=[('Soft focus', 'إحساس الحلم', 9.0)]),
        dict(a=3311.8, b=3313.7, crop=NOWC, src=3316, kw=[('Rack focus', 'الفوكس بيتنقل جوه اللقطة', 0.1)]),
        dict(a=3354.6, b=3378.0, crop=NOWC),
    ]),
    # 10: hook = a film moment; every script description shown with the matching shot of the scene we analysed
    10: dict(no=10, chapter=18, title='السكريبت *بيوصف كل حاجة*', more=[dict(thumb='projects/filmcourse/pics/yt_NWtPI7aiefw.jpg', qr='projects/filmcourse/qr/yt_NWtPI7aiefw.png', title='تحليل المشهد كامل')], pieces=[
        dict(a=2193.4, b=2215.6, file=IB, crop=IBC, seq=SH((0, 11.0, IBR), (4.3, 31.0, IBC), (9.0, 104.0, IBR), (13.0, 114.0, IBR), (17.5, 120.0, IBR)), film=IBF),
        dict(a=2131.5, b=2140.5, crop=L(300, 0, 720), rew=True, lab=[(0.5, 'سكريبت إبراهيم الأبيض', None, 2.4)]),
        dict(a=2154.7, b=2165.9, crop=L(160, 0, 960), kw=[('Sequence · Scene · Shot', 'تتابع · مشهد · لقطة', 2.0)]),
        dict(a=2193.4, b=2215.6, file=IB, crop=IBC, seq=SH((0, 11.0, IBR), (4.3, 31.0, IBC), (9.0, 104.0, IBR), (13.0, 114.0, IBR), (17.5, 120.0, IBR)), film=IBF),
        dict(a=2224.6, b=2244.1, crop=L(320, 60, 700), zoom=[(2238, L(400, 120, 560))], lab=[(1.0, 'السكريبت بيوصف المكان', None, 2.2)]),
        dict(a=2253.7, b=2285.0, file=IB, crop=IBR, seq=SH((0, 51.0, IBC), (7.0, 135.0, IBC), (14.0, 125.0, IBC), (21.0, 51.5, IBC)), lab=[(8.0, 'عيون زجاجية.. مغيّب', None, 2.4)]),
        dict(a=2285.5, b=2304.5, file=IB, crop=IBL, seq=SH((0, 59.0, IBL), (6.0, 107.0, IBL), (12.0, 142.0, IBL)), lab=[(7.0, 'قطع للحاج فارس', None, 2.2)]),
        dict(a=2327.2, b=2344.1, show='Pipeline', anim=dict(items=PIPE[1:4], hi=[[2327.2, 0], [2335.2, 0], [2338.7, 1], [2340.5, 2]], tags=[T(2342.3, 'إدّي لكل خطوة حقها')])),
    ]),
    # 11: matching film shots 0:30-1:10, caption "اقطع لسان جوز بنتي", end = course + analysis video
    11: dict(no=11, chapter=17, title='تتابع ومشهد *ولقطة*', more=[dict(thumb='projects/filmcourse/pics/yt_NWtPI7aiefw.jpg', qr='projects/filmcourse/qr/yt_NWtPI7aiefw.png', title='تحليل المشهد كامل')], pieces=[
        dict(a=2068.1, b=2081.6, file=IB, crop=IBL, seq=SH((0, 122.0, IBL), (5.0, 135.0, IBC), (9.0, 142.0, IBL)), film=IBF),
        dict(a=1977.5, b=1994.4, show='TreeScene', anim=dict(seqAt=6.0, sceneAt=10.0, shotAt=12.2), rew=True),
        dict(a=2058.0, b=2068.1, file=IB, crop=IBC, seq=SH((0, 11.0, IBR), (3.6, 27.0, IBL), (7.0, 31.0, IBC)), film=IBF),
        dict(a=2068.1, b=2088.6, file=IB, crop=IBL, seq=SH((0, 122.0, IBL), (5.0, 135.0, IBC), (9.0, 142.0, IBL), (14.0, 108.0, IBC), (17.0, 113.0, IBC))),
        dict(a=2089.1, b=2108.0, file=IB, crop=IBC, seq=SH((0, 175.0, IBC), (5.0, 186.0, IBC), (9.5, 204.0, IBC), (14.0, 224.0, IBC))),
        dict(a=2108.0, b=2114.2, show='TreeScene', anim=dict(film='إبراهيم الأبيض', seqAt=0.4, sceneAt=2.4, shotAt=4.6, tags=[T(2109.3, 'ده تتابع كامل')])),
    ]),
    # 12: sync (his face pieces from the same second), basketball POV, his shot examples, the 180-degree rule, Parasite
    12: dict(no=12, chapter=21, title='أنواع الـ *Framing*', pieces=[
        dict(a=2566.6, b=2583.2, crop=L(200, 0, 880), nocam=True, kw=[('Dirty single', 'ظهر حد تاني باين في الكادر', 1.0)]),
        dict(a=2531.6, b=2544.5, crop=L(430, 100, 420), rew=True, kw=[('POV', 'الكاميرا = عين الشخصية', 4.0)]),
        dict(a=2544.9, b=2551.4, crop=NOWC, src=336.0, lab=[(0.3, 'الكاميرا مكان الكورة', None, 2.6)]),
        dict(a=2552.0, b=2566.6, crop=L(430, 100, 420), kw=[('Insert · Single clean', 'تفصيلة.. أو أنا بس في الكادر', 1.0)]),
        dict(a=2566.6, b=2583.2, crop=L(200, 0, 880), nocam=True),
        dict(a=2584.0, b=2606.4, crop=L(120, 40, 860), kw=[('Single · Two · Three · Crowd', 'كام واحد في الكادر', 2.0), ('OTS', 'من ورا الكتف', 14.0)]),
        dict(a=2606.4, b=2620.4, show='Rule180', anim=dict(crossAt=2614.5, tags=[T(2608.5, 'الكاميرا تفضل في ناحية واحدة من الخط'), T(2614.5, 'لو عدّيت الخط.. الاتنين يبصوا لنفس الناحية', '#E5232B')])),
        dict(a=2783.0, b=2799.5, crop=NOWC, film=FT('Parasite', '2019')),
    ]),
    # 13: caption Post-production, the pre-production part, bigger pipeline, his PROCESS slide while he explains
    13: dict(no=13, chapter=10, title='صلّحها وانت *بتصوّر*', pieces=[
        dict(a=994.4, b=1002.3, show='Pipeline', anim=dict(items=PIPE[1:4], hi=[[994.4, 1]], tags=[T(994.4, 'المكتب اللي ورا ظهرك؟ شيله دلوقتي', '#E5232B')])),
        dict(a=894.7, b=905.6, show='Pipeline', anim=dict(items=PIPE[1:4], hi=[[894.7, -1]]), rew=True),
        dict(a=905.6, b=919.1, crop=L(380, 60, 520), kw=[('Production', 'التصوير: قلل الارتجال', 4.0)]),
        dict(a=919.1, b=934.9, crop=L(100, 60, 520), kw=[('Pre-production', 'اكتب وحضّر كل مشهد', 2.0)]),
        dict(a=955.7, b=970.5, crop=L(700, 60, 560), kw=[('Post-production', 'مونتاج، موشن، صوت، ألوان', 3.0)]),
        dict(a=979.2, b=1002.3, show='Pipeline', anim=dict(items=PIPE[1:4], hi=[[979.2, 2], [981.5, 1]], tags=[T(987.0, 'صوت مزعج؟ شيله وانت بتصور'), T(994.4, 'متقولش هشيله في الـ Post', '#E5232B')])),
        dict(a=1010.3, b=1021.3, crop=L(100, 60, 520), kw=[('Pre-production', 'ادّي التحضير حقه', 1.0)]),
        dict(a=1023.2, b=1047.0, show='Pipeline', anim=dict(items=PIPE, hi=[[1023.2, 0], [1038.5, 4]])),
    ]),
    # 14: the slide of the type he names, at that moment (src = a)
    14: dict(no=14, chapter=6, title='أنواع *الأنيميشن الخمسة*', pieces=[
        dict(a=641.1, b=658.4, crop=L(150, 0, 900), kw=[('Stop motion', 'تصور وتحرك خطوة', 2.0)]),
        dict(a=573.2, b=584.5, crop=L(150, 0, 900), rew=True, kw=[('Traditional', 'بيترسم فريم فريم', 6.0)]),
        dict(a=585.5, b=603.2, crop=L(150, 0, 900), kw=[('2D animation', 'الكاركتر بيترسم مرة ويتحرك', 3.0)]),
        dict(a=606.0, b=611.6, crop=L(150, 0, 900), kw=[('3D / CG', 'موديل 3D بيتحرك', 0.6)]),
        dict(a=617.6, b=636.9, crop=L(150, 0, 900), kw=[('Motion graphics', 'إعلانات وشرح', 6.0)]),
        dict(a=636.9, b=658.4, crop=L(150, 0, 900), lab=[(5.0, 'الأنبياء المرسلون', None, 2.4)]),
    ]),
    # 16: tighter + the other composition rules
    16: dict(no=16, chapter=23, title='قواعد *تكوين الكادر*', pieces=[
        dict(a=2888.4, b=2897.9, crop=NOWC, lab=[(4.0, 'حط الشخصية على التقاطع', None, 2.4)]),
        dict(a=2864.5, b=2872.6, crop=L(400, 0, 500), rew=True, kw=[('Composition', 'قواعد تكوين الصورة', 1.0)]),
        dict(a=2875.3, b=2887.0, show='ComposeRules', anim=dict(at=0.3, step=1.6)),
        dict(a=2888.4, b=2906.4, crop=NOWC, zoom=[(2897.5, NOWC)], kw=[('Rule of thirds', 'الكادر 3 × 3', 1.0)]),
    ]),
    # 17: the videos he comments on, shown first with their own sound
    17: dict(no=17, chapter=3, title='الفيلم ميكر *الشاطر*', pieces=[
        dict(a=298.2, b=306.4, crop=NOWC, src=290, lab=[(1.8, 'لازم تكون شاعر', None, 2.4)]),
        dict(a=260.6, b=285.1, crop=NOWC, src=272, rew=True, labels=[('بتبيع', 'تبيع'), ('تعرفها', 'تعرّف'), ('فسلية', 'تسلّي'), ('قصة', 'تحكي قصة')]),
        dict(a=285.1, b=310.6, crop=NOWC, labels=[('ستوري', 'Storyteller'), ('سولفر', 'Problem solver'), ('قرارات', 'Decision maker'), ('صبور', 'صبور')]),
        dict(a=331.3, b=346.9, raw=True, crop=NOWC, lab=[(0.3, 'الفيديو الأول', None, 2.0)]),
        dict(a=347.1, b=370.8, crop=NOWC, src=345, lab=[(8.5, 'الكاميرا مكان الكورة', None, 2.4)]),
        dict(a=372.0, b=386.0, raw=True, crop=NOWC, film=FT('BBC Sport · World Cup 2018', 'trailer', 'الفيديو التاني')),
        dict(a=414.6, b=437.5, crop=NOWC, src=400),
        dict(a=437.5, b=457.4, show='big:فكّر قبل ما تصوّر|علشان توصل الفكرة بأبلغ وأجمل طريقة', ico='film'),
    ]),
    # 18: not boring: one film frame cut live to each ratio
    18: dict(no=18, chapter=13, title='الـ *Aspect ratio*', pieces=[
        dict(a=1196.7, b=1203.6, show='AspectCut', anim=dict(img='projects/filmcourse/stills/aspect_ibrahim.jpg', credit='إبراهيم الأبيض (2009)', keys=[[1196.7, '4:3', 'الأفلام القديمة'], [1201.7, '16:9', 'الأفلام الحديثة']])),
        dict(a=1131.2, b=1153.7, crop=L(0, 150, 640), zoom=[(1139.7, L(330, 150, 640)), (1149.4, L(640, 150, 640))], rew=True),
        dict(a=1157.5, b=1163.7, crop=L(0, 100, 800), kw=[('Frames', 'الفيديو = صور ورا بعض', 1.0)]),
        dict(a=1171.8, b=1196.7, show='AspectCut', anim=dict(img='projects/filmcourse/stills/aspect_ibrahim.jpg', credit='إبراهيم الأبيض (2009)',
             keys=[[1171.8, '4:3', 'التلفزيون'], [1173.7, '16:9', 'يوتيوب'], [1189.0, '9:16', 'ريلز وموبايل.. بيضيع كتير'], [1191.5, '1:1', 'إنستجرام']])),
        dict(a=1196.7, b=1203.6, show='AspectCut', anim=dict(img='projects/filmcourse/stills/aspect_ibrahim.jpg', credit='إبراهيم الأبيض (2009)', keys=[[1196.7, '4:3', 'الأفلام القديمة'], [1201.7, '16:9', 'الأفلام الحديثة']])),
    ]),
    # 19: his drawing at that very moment + zoom onto each item he names
    19: dict(no=19, chapter=5, title='رسوم متحركة ولا *صور متحركة*؟', pieces=[
        dict(a=542.7, b=553.6, crop=L(560, 60, 520), lab=[(0.4, 'Stop motion: في النص', None, 2.4)]),
        dict(a=488.8, b=500.5, crop=L(160, 0, 960), rew=True, labels=[('متحرك', 'المتحرك'), ('صور', 'صور متحركة'), ('رسوم', 'رسوم متحركة')]),
        dict(a=500.7, b=535.8, crop=L(0, 40, 960), zoom=[(503.3, L(760, 40, 520)), (504.0, L(0, 40, 520)), (512.1, L(100, 40, 520)), (521.5, L(100, 40, 520)), (527.1, L(220, 40, 520))],
             kw=[('2D · 3D · Traditional', 'أقرب للرسوم', 12.0)]),
        dict(a=535.9, b=570.4, crop=L(380, 40, 520), zoom=[(542.7, L(560, 40, 520)), (554.5, L(700, 40, 520)), (558.5, L(760, 40, 520))], kw=[('VFX · Film', 'أقرب للصور', 22.0)]),
    ]),
    # 20: "Camera gear", nothing rushed, every item shown when he names it, drone sentence with its law
    20: dict(no=20, chapter=27, title='أدوات *الكاميرا*', pieces=[
        dict(a=3850.5, b=3859.9, crop=L(380, 150, 560), kw=[('Gimbal', 'حركة هاند هيلد ثابتة', 2.0)]),
        dict(a=3830.1, b=3840.8, crop=L(300, 0, 700), rew=True, kw=[('Tripod', 'حتى للموبايل', 6.6)]),
        dict(a=3843.4, b=3850.5, crop=L(300, 0, 700), kw=[('Remote · Track', 'تصور من بعيد.. وتحرك الكاميرا', 1.0)]),
        dict(a=3850.5, b=3859.9, crop=L(380, 150, 560)),
        dict(a=3864.1, b=3867.9, show='FactCard', anim=dict(title='الدرون في مصر', text='قانون 216 لسنة 2017: لازم تصريح من وزارة الدفاع (فيه استثناء لبعض الأنواع الخفيفة جدا)', src='Egypt Independent · مسار (Masaar)')),
        dict(a=3867.9, b=3878.7, crop=L(300, 0, 700), kw=[('Waterproof case', 'الكاميرا تحت المية', 2.0)]),
    ]),
}

# 08 rebuilt around what he wants to say (Aly 2026-11-07): beauty has two kinds, in writing and in video; tools of each.
# (His 2 new recordings 20261107_075021/075352 were not found on disk yet -> built from the course audio; swap in when they arrive.)
SHORTS[8] = dict(no=8, chapter=2, title='الجمال *نوعين*', pieces=[
    dict(a=136.9, b=150.1, show='big:الفيديو لغة|ليها شكل.. وليها محتوى', ico='film'),
    dict(a=93.3, b=117.0, crop=L(160, 0, 960), rew=True, lab=[(4.0, 'صور ورا بعض + صوت', None, 2.4), (17.0, 'وسيلة تواصل = لغة', None, 2.6)]),
    dict(a=150.8, b=180.4, show='TwoBeauty', anim=dict(mode='writing', leftAt=0.3, rightAt=7.0, step=1.2)),
    dict(a=180.7, b=192.1, crop=L(30, 200, 680), src=189, labels=[('الكيف', 'الكيف'), ('اللازرق', 'الفيل الأزرق')]),
    dict(a=207.8, b=222.0, crop=L(30, 200, 680), src=189, lab=[(0.5, 'كلغة سينمائية.. الاتنين عباقرة', None, 2.6)]),
    dict(a=222.0, b=251.7, show='TwoBeauty', anim=dict(mode='video', leftAt=0.3, rightAt=12.0, step=1.3)),
])

FIX_MORE = {'triboot.': 'ترايبود.', 'triboot': 'ترايبود', 'tripod': 'ترايبود', 'جوزبين': 'جوز بنتي', 'جوزبنتي': 'جوز بنتي', 'كير': 'Gear', 'البوست': 'الـ', 'النوش.': 'Post-production.', 'النوش': 'Post-production'}
N = None
CAP = {
    5: [None, 'خدتوا بالكم.. وممكن تقطع عشان نخش جوه دماغ حد.. الراجل هو ده.. فيلم سيفن.. اللقطة اللي فاتت.. مش عارف انتو عارفينه ولا لا'],
    11: ['فهيقول لك فزورة.. فزورة لو حليتها تكسب.. فزورة بالآخر بيقول له اقتل اللي قطع لسان جوز بنتي.. بس بيقولها له بفزورة'],
}
CAP[8] = [None, None, None, None, 'لكن بقى كلغة سينمائية.. الاتنين عباقرة.. وفيلم الكيف كلغة سينمائية عبقري عبقري.. لأنه مش بس بيتكلم على المخدرات.. وبيتكلم على اللغة.. فيلم عبقري سينمائيا']

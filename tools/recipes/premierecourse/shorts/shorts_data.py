# Shorts series data (premiere course). Key = posting number (most impressive first, Aly 2026-10-18).
# piece: a/b = his sentence (source seconds, fitted on the waveform later); show = 'screen' (his recording, zoom on his cursor or
# 'crop'), an animation name, or 'big:line|sub'; step = the step chip text; kw = [(EN, AR, offset)]; key = (keys, AR, offset).
TOTAL = 44
CTA_VOL = 1.0  # level is set after the render (CTA ~1.5 dB under the body: Aly 2026-10-18 'مش عايز صوتي في الـ CTA أعلى بكتير')
CTA_FILE = 'cta_course_full.mp4'  # Aly: the WHOLE CTA as he said it (comment "كورس" + what the course is)
CTA_DUR = 33.27

# crops in the 1276x720 recording
PROGRAM = dict(sx=560, sy=20, sw=700)        # Program monitor (top right)
PROGRAM_BIG = dict(sx=150, sy=20, sw=1100)   # Program monitor maximized
EFFCTRL = dict(sx=0, sy=20, sw=640)          # Effect Controls (top left)
EFFECTS = dict(sx=0, sy=330, sw=640)         # Effects panel (bottom left)
PROG_PANE = dict(sx=575, sy=25, sw=700)      # Program monitor for the lower half of a dual card (wide pane)
TL1 = dict(sx=520, sy=190, sw=640)          # ep1 timeline panel
TH1 = dict(sx=520, sy=330, sw=420)          # ep1 track headers (targeting / sync lock)
TLD = dict(sx=520, sy=380, sw=640)          # ep1 timeline TRACKS for a wide dual / under pane
SPEED_DLG = dict(sx=500, sy=40, sw=620)      # ep3: Clip Speed/Duration dialog + Program monitor in one view
DEMO3 = dict(sx=720, sy=40, sw=400)          # ep3 2020: the demo playing in the Program monitor, big

NEW = {
    'bgremove': dict(title='من غير Green screen', how='Object Mask يشيل الخلفية من غير ما تصوّر على أخضر', vid='bgremove', channel='Smertimba Graphics', src='Adobe helpx'),
    'mask': dict(title='Object Mask', how='دوسة واحدة.. والبرنامج يحدد الحاجة ويتتبعها لوحده', vid='mask', channel='Adobe Care', src='Adobe helpx'),
    'optflow': dict(title='Optical Flow', how='سلو موشن أنعم: البرنامج بيعمل فريمات جديدة بين الفريمات', vid='optflow', channel='Smertimba Graphics', src='Adobe helpx'),
    'genext': dict(title='Generative Extend', how='الكليب قصير؟ الـ AI يطوّله فريمات زيادة', vid='genext', channel='Adobe Video', src='Adobe helpx'),
    'colormode': dict(title='Color mode (beta)', how='مكان جديد للألوان معمول للي لسه بيبدأ', vid='colormode', channel='Adobe Video', src='Adobe helpx'),
}

SHORTS = {
    1: dict(no=1, chapter=45, ep=3, look='glass', title='Green_screen في *3_خطوات*', new='bgremove', pieces=[
        dict(a=2476.6, b=2481.4, hook=dict(before=2441, after=2479, crop=PROGRAM)),
        dict(a=2433.8, b=2445.6, step='Effects ← Keying ← Ultra Key', kw=[('Ultra Key', 'إفكت شيل الخلفية', 5.5)]),
        dict(a=2463.2, b=2465.3, step='اسحب Ultra Key على الكليب'),
        dict(a=2471.2, b=2476.1, step='بالقطارة اختار اللون الأخضر', dual=('auto', PROG_PANE), kw=[('Key Color', 'اللون اللي هيتشال', 0.5)]),
        dict(a=2481.4, b=2493.9, dual=('auto', PROG_PANE), kw=[('Highlight / Shadow', 'ظبّطهم لو فيه بواقي أخضر', 3.0)]),
        dict(a=2659.7, b=2666.4, show='screen', crop=PROGRAM, src=2662, marks=False),
    ]),
    2: dict(no=2, chapter=28, ep=2, look='film', title='دخان *من_غير* Green_screen', pieces=[
        dict(a=1202.5, b=1210.7, hook=dict(before=1225, after=1236, crop=PROGRAM_BIG)),
        dict(a=1188.5, b=1202.1, crop=PROGRAM, src=1194, marks=False, kw=[('Blend mode', 'طريقة دمج الطبقات', 9)]),
        dict(a=1074.5, b=1079.6, step='Effect Controls ← Opacity ← Blend Mode', crop=EFFCTRL),
        dict(a=1084.4, b=1090.7, show='BlendAnim'),
        dict(a=1214.4, b=1224.9, step='اختار طبقة الدخان ← Multiply', dual=(dict(sx=200, sy=150, sw=560), PROG_PANE)),
        dict(a=1226.0, b=1230.7, crop=PROGRAM_BIG, src=1236, marks=False),
        dict(a=1257.3, b=1261.7, show='big:ونفس الحيلة|تشويش التلفزيون على أي فيديو', ico='film'),
        dict(a=1305.6, b=1309.6, hook=dict(before=1300, after=1309.5, crop=PROGRAM)),
        dict(a=1344.3, b=1348.4, show='big:Blend_modes|في حاجات كتير جدا', ico='blend'),
    ]),
}

SHORTS.update({
    3: dict(no=3, chapter=43, ep=3, look='vhs', title='سريع ← بطيء ← *يقف*', new='genext', pieces=[
        dict(a=2019.1, b=2030.4, crop=DEMO3, marks=False, labels=[('سريع', '⏩ سريع'), ('بطيط', '🐢 بطيء'), ('وقف', '⏸ وقف'), ('اكتر', '🐢 أبطأ')]),
        dict(a=1853.3, b=1856.1, step='Right click على الكليب', key=(['Right', 'Click'], 'قايمة الاختيارات', 0.6)),
        dict(a=1873.0, b=1877.4, step='Speed/Duration ← 200%', crop=SPEED_DLG, marks=False, kw=[('Speed', 'السرعة', 1.0)]),
        dict(a=1886.7, b=1900.6, step='اقطع بـ C ورجّع الباقي 100%', key=(['C'], 'المقص', 1.0)),
        dict(a=1938.5, b=1946.2, step='Right click ← Frame Hold Options'),
        dict(a=1949.8, b=1958.1, crop=DEMO3, marks=False),
        dict(a=1973.9, b=1981.4, step='Speed/Duration ← 50%', crop=SPEED_DLG, marks=False),
        dict(a=2032.7, b=2042.2, show='SlowMath'),
    ]),
    4: dict(no=4, chapter=9, ep=1, look='pop', title='ليه الـ Slow_motion *بيقطّع؟*', new='optflow', pieces=[
        dict(a=1659.3, b=1670.6, show='FpsRace', anim=dict(note='فريمات بتترمي = حركة بتقطّع')),
        dict(a=1632.9, b=1647.5, show='big:30 على تايم لاين 24|مبتتقسمش.. فيه فريمات بتترمي', ico='timeline'),
        dict(a=1484.0, b=1489.9, step='صوّر بـ Frame rate عالي ونزّله لـ 24', show='big:صوّر أسرع|ونزّل لـ 24', ico='slow'),
        dict(a=1505.0, b=1521.0, crop=dict(sx=40, sy=9, sw=860), marks=False),
        dict(a=1556.8, b=1569.6, show='SlowMath'),
        dict(a=1698.6, b=1702.5, show='big:صوّر باللي كاميرتك|بتستحمله', ico='cam'),
    ]),
    5: dict(no=5, chapter=33, ep=2, look='lottie', title='ماسك *بيتحرك* مع الحاجة', new='mask', pieces=[
        dict(a=2751.0, b=2762.0, hook=dict(before=2384, after=2759, crop=dict(sx=190, sy=10, sw=850), cropB=dict(sx=740, sy=50, sw=360))),
        dict(a=2366.6, b=2377.4, show='big:Mask|تظهر جزء من الصورة والباقي يختفي', ico='mask', kw=[('Mask', 'تحديد جزء من الصورة', 1.0)]),
        dict(a=2387.2, b=2390.6),
        dict(a=2394.6, b=2399.0, step='Effect Controls ← Opacity ← Pen', crop=EFFCTRL),
        dict(a=2425.8, b=2428.4, step='ارسم حوالين الحاجة'),
        dict(a=2446.8, b=2453.0, crop=PROGRAM, marks=False),
        dict(a=2539.6, b=2557.3, step='Feather و Expansion و Invert', dual=('auto', dict(sx=740, sy=40, sw=420)), kw=[('Feather', 'تنعيم الحواف', 6.0), ('Invert', 'عكس التحديد', 9.5)]),
        dict(a=2587.1, b=2601.5, step='Mask Path = Keyframes', dual=('auto', dict(sx=740, sy=40, sw=420)), kw=[('Mask Path', 'شكل الماسك في كل فريم', 3.0)]),
        dict(a=2660.0, b=2664.1, show='big:فريم.. فريم|بس في 2026 فيه أسهل', ico='mask'),
    ]),
})

# Captions = what he actually says (re-transcribed per piece, then corrected by reading; never words he didn't say), one string per piece.
CAP = {
    1: ['اه اهي اتظبطت فجأة كده على طول.. بقى انت عامل جرين سكرين بس كده',
        'دي صورة مثلا أنا عايز أشيل الـ Green_Screen فيها.. فيها إيه بقى؟ تدوس عليها، فيه إفكت اسمه Ultra_Key.. من Video_Effects تحتها Keying',
        'تدوس على Ultra_Key وتحطها هنا',
        'تاخد دي تحطها على اللون الأخضر.. اهي حطها على اللون الأخضر',
        'الدنيا سهلة جدا.. ظبطها بقى هنا عشان فيه شوية غوشة.. خش بقى على الحاجات دي تظبط الدنيا.. مثلا الـ Highlight تقلله.. والـ Shadow تزوده شوية',
        'تشيل الـ Green_Screen وتلعب بقى في الفيديو عادي خالص.. اتشال الـ Green_Screen من الفيديو اهو'],
    2: ['فطبعا انت مش محتاج بقى Green_Screen وقصة دي كلها.. إنك تجيب دخان بالـ Green_Screen عشان تعرف تقصه.. لا، طالما هو خلفيته بيضا',
        'وأنا عايز مثلا أحط لها دخان.. فبصوا الفيديو ده بقى أنا جايبه من عالنت.. عبارة عن دخان بيطلع وليه خلفية بيضا.. تمام؟ تقدر تحطه على الفيديو بتاعك.. لأنه خلفيته بيضا وهو أسود',
        'وفيه في الإفكتات تحت الـ Scale والـ Position وكل ده.. فيه حاجة اسمها Blend_Mode.. تمام؟',
        'فمثلا دست Multiply.. المفروض طبعا الأبيض ده كله يتشال ويبان اللي في الخلفية',
        'دست بقى هنا جيت عند الدخان ده.. دلوقتي أنا دايس على الـ layer بتاعت الدخان.. وأنزل الـ Blending_Modes.. وأدوس Multiply',
        'بص الدخان بعد كده.. بص الفيديو بقى شكله إيه',
        'مثلا لو انت عايز تعمل كأن الفيديو اللي انت بتتفرج عليه ده في التلفزيون ويكون فيه تشويش',
        'أول ما أدوس Multiply.. الفيديو ظهر من وراها',
        'فطبعا تقدر تستخدم Blend_Mode في حاجات كتيرة جدا جدا جدا'],
}

CAP.update({
    3: ['سريع.. بطيء.. وقف.. بطيء أكتر',
        'هدوس على هنا.. Right Click على الفيديو',
        'أدوس على Speed and Duration.. هنخلي السرعة مثلا 200%',
        'فدست C قطعته.. بعد كده هدوس على الفيديو التاني اللي أنا عايزه ده.. Right Click، Speed and Duration، أخلي سرعته 100%.. بعد كده عايز في النص.. بصوا هيبقى سريع',
        'وأدوس Right Click، و Frame Hold Options.. أول ما أدوس Frame Hold Options',
        'جه عند الفريم اللي أنا واقف فيه.. وخلاه الكليب كله.. الكليب كله عبارة عن الصورة دي.. أدوس Play بس هو عبارة عن صورة ثابتة',
        'Speed Duration وخليه سرعة 50%.. اقلب بقى',
        'فده ممكن تستخدمه كتير برضو.. لما انت تكون صورت مثلا بكاميرا فيديو بستين فريم في الثانية'],
    4: ['فاللي هيحصل إن تقريبا فيه فريم بيترمي.. فلما بيترمي، الفيديو هيبقى فيه تقطيع.. كل ثانية والتانية فيه حاجة غريبة.. فدي مش حلوة',
        'لو انت مسكت الـ 30 فريم دول وقسمتهم على 24.. يعني انت دلوقتي عملت التايم لاين بتاعك.. آخره بيستوعب في الثانية 24 صورة.. وانت صورت 30 صورة في الثانية.. إيه اللي هيحصل؟ إن التلاتين فريم ما بتتقسمش على 24.. هيطلع لك كسر',
        'عايز تعمل Slow motion.. بتصور بفريم عالي وتنزله للـ 24 فريم',
        'فانت عندك 30 فريم في الثانية.. عايز تعمل Slow motion.. هتقلله بنسبة 80% بس.. فنضرب 30 في 0.8.. أربعة وعشرين فريم في الثانية',
        'تقدر تقلله من 100% لـ 40%.. ده Slow motion كويس.. لو هتصور بـ 120 فريم.. تقلله لـ 20%.. تقدر تقلله لـ 20%',
        'فغالبا يستحسن كل كاميرا تصور باللي هي بتستحمله'],
    5: ['فبصوا بقى دلوقتي.. الفيديو عبارة عن فيه شمسية وأنا بتفرج عليها.. طبعا لو عملت Selection بالفريم.. هتشوف شمسية بتتحرك لوحدها.. وطبعا وش الست معاها',
        'الماسك ده عامل زي اللي في الفوتوشوب بالظبط.. مش بالظبط يعني، فكرته هي اللي في فوتوشوب اللي احنا كنا عارفينها.. إنك بتظهر حاجة من الصورة والباقي يختفي',
        'أنا عايز آخد الشجرة دي من الفيديو',
        'وأجي عند الـ Effect tab.. وأدوس على علامة الـ Pen tool دي',
        'تبدأ بقى تعلم على الشجرة زي ما انت عايز',
        'كده أنا علمت الشجرة بس.. لو شغلت الفيديو هتلاقي الراجل بيعدي قصاد الشجرة دلوقتي',
        'هنا Mask 1 ده الشمسية تمام؟ عندك بقى هنا Path و Feather و Opacity و Expansion و Invert.. الـ Invert دي هتعكس لي الماسك كله.. هيعلم على كل حاجة إلا الشمسية.. بص كده.. الـ Expansion ده اللي هو بيكبر لك الماسك بالطريقة اللي انت شايفها دي',
        'Mask Path ده إيه؟ ده عبارة عن الـ Path اللي احنا عاملينه.. السيليكشن الأزرق ده اللي احنا عاملينه هو ده الـ Path.. فلو أنا عملت له هنا وقلت له احفظ لي الماسك ده.. فبالتالي أي تغيير هعمله، طالما أنا أول مرة عملت له، خلاص Keyframe',
        'المفروض تمشي فريم فريم.. تمشي فريم وتقوم ظابط معاها'],
})


NEW['props'] = dict(title='Properties panel', how='كل الإعدادات المهمة للكليب في مكان واحد', vid='props', channel='Adobe Video', src='Adobe helpx')

# ---------- batch 2 (posting 06-13) ----------
SHORTS.update({
    6: dict(no=6, chapter=40, ep=3, look='glass', title='لوّن الفيديو *كله* مرة واحدة', pieces=[
        dict(a=999.8, b=1011.0, hook=dict(before=995, after=1166, crop=PROGRAM)),
        dict(a=865.7, b=873.8, show='AdjAnim', kw=[('Adjustment Layer', 'طبقة بتأثر على اللي تحتها', 4.0)]),
        dict(a=888.8, b=892.5, step='New Item ← Adjustment Layer'),
        dict(a=905.4, b=909.0, step='اسحبها فوق الكليبات'),
        dict(a=918.4, b=921.9, show='big:طبقة مخفية|بتأثر على كل اللي تحتها', ico='layers'),
        dict(a=944.4, b=952.2, step='حط الإفكت عليها', dual=('auto', PROG_PANE)),
        dict(a=1123.2, b=1132.0, dual=('auto', PROG_PANE), kw=[('Grid', 'خطوط على الفيديو', 2.0)]),
        dict(a=1203.8, b=1214.9, show='big:غيّر مرة واحدة|بدل ما تغيّر كل كليب', ico='layers'),
    ]),
    7: dict(no=7, chapter=41, ep=3, look='film', title='لون *الفيلم* بـ Tint', new='colormode', pieces=[
        dict(a=1395.9, b=1413.0, hook=dict(before=1239, after=1385, crop=PROGRAM)),
        dict(a=1250.3, b=1268.7, show='big:Tint = إحساس|سقعة وخوف بدل الشمس', ico='drop', kw=[('Tint', 'صبغة لونين', 1.0)]),
        dict(a=1308.3, b=1313.1, step='Tint على Adjustment layer'),
        dict(a=1313.5, b=1327.1, step='Map Black To: لون الغامق', dual=('auto', PROG_PANE)),
        dict(a=1328.4, b=1338.6, step='Map White To: لون الفاتح', dual=('auto', PROG_PANE)),
        dict(a=1383.9, b=1392.3, crop=PROGRAM, marks=False),
        dict(a=1425.3, b=1432.4, show='big:لون واحد|للفيديو كله', ico='wheel'),
    ]),
    8: dict(no=8, chapter=44, ep=3, look='vhs', title='*Lens_Flare* على فيديوك', pieces=[
        dict(a=2307.6, b=2309.9, hook=dict(before=2296, after=2320, crop=PROGRAM)),
        dict(a=2250.7, b=2255.6, step='File ← New ← Black Video'),
        dict(a=2281.3, b=2292.5, show='big:ليه أسود؟|Lens_Flare مش بيشتغل على طبقة شفافة', ico='fx'),
        dict(a=2297.6, b=2307.1, step='Lens Flare على Black Video ← Screen', dual=('auto', PROG_PANE), kw=[('Screen', 'الأسود يختفي', 6.0)]),
        dict(a=2316.9, b=2328.4, crop=PROGRAM, marks=False),
    ]),
    9: dict(no=9, chapter=30, ep=2, look='pop', title='ترانزيشن في ثانية: *Ctrl_+_D*', pieces=[
        dict(a=1829.5, b=1836.2, crop=PROGRAM, marks=False, labels=[('بهدوء', '⤴ بتخش بهدوء'), ('وبتخرج', '⤵ وبتخرج بهدوء')]),
        dict(a=1552.5, b=1560.0, show='big:تختفي بالراحة|من غير Keyframes', ico='fade'),
        dict(a=1641.2, b=1646.4, step='Right click ← Apply Default Transitions', key=(['Right', 'Click'], 'قايمة الاختيارات', 1.5)),
        dict(a=1761.8, b=1768.1, crop=PROGRAM, marks=False),
        dict(a=1779.9, b=1782.2, step='Ctrl + D', key=(['Ctrl', 'D'], 'ترانزيشن على الكليب', 0.5)),
        dict(a=1815.8, b=1824.1, crop=PROGRAM, marks=False),
    ]),
    10: dict(no=10, chapter=27, ep=2, look='lottie', title='ليه حركتك شكلها *روبوت؟*', pieces=[
        dict(a=909.9, b=914.4, show='InterpAnim'),
        dict(a=521.8, b=534.8, show='big:Linear|كل فريم بيتغير بنفس القدر', ico='curve', kw=[('Linear', 'حركة بالتساوي', 1.0)]),
        dict(a=539.0, b=544.0, show='big:Hold|التغيير فجأة', ico='freeze', kw=[('Hold', 'تغيير فجأة', 1.0)]),
        dict(a=579.3, b=591.8, show='KeyAnim', anim=dict(ease=True), kw=[('Bezier', 'حركة ناعمة', 1.0)]),
        dict(a=798.4, b=803.6, step='افتح الجراف من السهم'),
        dict(a=702.9, b=706.4),
    ]),
    11: dict(no=11, chapter=29, ep=2, look='glass', title='حركة ناعمة بـ *Ease*', pieces=[
        dict(a=1363.7, b=1367.8, crop=PROGRAM, marks=False),
        dict(a=1375.5, b=1380.5, show='big:Bezier_=_Easy_Ease|نفس الفكرة في After_Effects', ico='curve'),
        dict(a=1388.8, b=1398.3, show='KeyAnim', anim=dict(ease=True)),
        dict(a=1399.9, b=1413.8, show='big:Ease_In_/_Ease_Out|تخش عادي وتخرج بهدوء.. تفرمل', ico='curve'),
        dict(a=1434.0, b=1447.5, step='Right click على الكيفريم ← Ease In', key=(['Right', 'Click'], 'على الكيفريم', 0.5)),
    ]),
    12: dict(no=12, chapter=26, ep=2, look='film', title='حرّك أي حاجة بـ *Keyframes*', new='props', pieces=[
        dict(a=470.0, b=474.7, crop=PROGRAM, marks=False),
        dict(a=209.9, b=216.6, show='KeyAnim', kw=[('Keyframe', 'نقطة بتحفظ الحالة', 2.0)]),
        dict(a=352.3, b=363.4, show='big:غيّرت ومفيش حركة؟|لازم تقوله إنك شغال Keyframes', ico='key'),
        dict(a=378.7, b=383.8, step='دوس على الساعة جنب Scale', dual=('auto', PROG_PANE), kw=[('Stopwatch', 'ابدأ Keyframes', 1.0)]),
        dict(a=405.7, b=416.1, dual=('auto', PROG_PANE)),
        dict(a=426.6, b=444.7, step='روح لفريم تاني وغيّر = Keyframe جديد', dual=('auto', PROG_PANE)),
    ]),
    13: dict(no=13, chapter=19, ep=1, look='vhs', title='*Ripple* ولا *Rolling؟*', pieces=[
        dict(a=3736.2, b=3754.7, show='RippleRoll', under=TLD, under_src=3511.3),
        dict(a=3497.9, b=3510.2, step='Ripple Edit: اسحب الطرف', dual=(TLD, PROG_PANE), kw=[('Ripple Edit', 'يقص ويقفل الفراغ', 8.0)]),
        dict(a=3511.3, b=3528.8, dual=(TLD, PROG_PANE)),
        dict(a=3544.0, b=3557.3, step='Rolling Edit', dual=(TLD, PROG_PANE), kw=[('Rolling Edit', 'يطوّل ده ويقصّر اللي جنبه', 1.5)]),
        dict(a=3557.4, b=3565.8, dual=(TLD, PROG_PANE)),
        dict(a=3574.7, b=3583.0, show='RippleRoll', under=TLD, under_src=3557.4),
    ]),
})


CAP.update({
    6: ['لو أنا بقى عايز أحط إفكت أو مثلا أعمل ألوان معينة أو Color_correction معين عليهم كلهم.. هحط الـ Adjustment_layer وأحط اللي أنا عايزه.. وكده بقى على كله',
        'دول كلهم على بعض اسمهم Adjustment_Layers.. وفي الـ After_Effects وفي الـ Premiere فيه حاجة اسمها Adjustment_Layer',
        'هدوس على New_Item.. وهدوس على Adjustment_Layer',
        'ندراج الـ Adjustment_layer.. نحطها ونخليها بحجم الفيديو',
        'الـ Adjustment_layer دي عاملة زي Layer مخفية',
        'عايز إفكت اسمه Levels.. حطيته على الـ Adjustment_layer.. فأنا لو حطيت مليون فيديو تحت هيتعامل عليهم كلهم',
        'الـ Blend_mode بتاعت الـ Layer نفسها.. بتاعت الـ Adjustment_layer نفسها.. وأعملها Multiply.. هنا بقى بقى فيه Grid على الفيديو بتاعي.. تمام؟',
        'فدلوقتي انت مثلا عايز تشيل الألوان أو تغيرها.. مش هتغيرها بقى في كل فيديو انت حاطه.. لا، احنا عندنا الـ Adjustment_layer.. تغير منها أو تخفيها وهو هيظبط كله'],
    7: ['تعالوا بقى نشوف قبله وبعده.. نشيل الـ Adjustment_layer.. ده كان المنظر.. وده هو المنظر بعد ما عملنا الصبغة اللي هي اسمها Tint.. وحطيناها على الـ Adjustment_layer.. ده قبل وده بعد',
        'بس يعني أنا حاسس نوعا ما فيه أحسن.. ممكن أغير الألوان عشان مثلا أحس بالسقعة أكتر.. لو فيلم مثلا مفروض يكون ده مشهد صاقع.. مبيكونش فيه شمس والإحساس بالطمأنينة.. أنا عايز أخلي فيه إحساس بالخوف مثلا.. وأحط شوية سقعة في المنظر',
        'أخش على الـ Adjustment_layer.. أنزل أعدّل الـ Scale والكلام ده.. أهو',
        'أنا مثلا عايز اللون الغامق يكون مثلا كده',
        'واللون الفاتح.. عايزه كده.. لا، نخليه كده',
        'دلوقتي المنظر أعتقد شوية بيوحي أكتر بالسقعة عشان الشمس بقت ضعيفة',
        'فده لما انت تكون بتعمل فيديو.. ألوان الفيديو ممكن تكون مختلفة شوية.. انت تحاول تخليها لون واحد'],
    8: ['عشان الـ Lens_Flare يبان زي مثلا كده',
        'البلاك فيديو بيبقى أسود.. ده ممكن تستخدمه إنك تحط عليه Lens_Flare',
        'ممكن تحط عليه إفكت Lens_Flare.. عشان الـ Lens_Flare ما بيشتغلش غير على حاجة.. ما ينفعش زي الـ Adjustment_layer أو الـ Transparent_layer.. مش هتتحط.. الاتنين دول مخفيين',
        'فالـ Lens_Flare بتحطها على الـ Black_Video.. وتدوس Multiply للـ Layer بتاعة الـ Black_Video دي.. أو Overlay.. أو Screen.. نخليها Screen',
        'وتيجي هنا.. Screen.. اللي هي بانت.. وممكن بقى تظبطها وحاجات زي كده بقى'],
    9: ['دلوقتي بقت الصورة بتخش بهدوء.. وبتخرج بهدوء',
        'وعايز تخليه مثلا في آخره الإضاءة تضعف كده.. اللي هو بالتدريج.. الفيديو ظهر لك ويختفي بالراحة',
        'هتيجي عند آخر الفيديو ده.. وتدوس Right_Click.. وتقول له Apply_Default_Transitions',
        'الصوت بيتداخل والصورة بتتداخل.. دي بقى عشان تعملها بالـ Keyframes هتاخد منك خمس دقايق.. وانت عملتها في ثانية',
        'لو دست عليه وعملت له Control_D',
        'زي مثلا صورة لوجو انت عايز تحطه.. هتدوس عليه.. ودست Control_D.. عملها لك من الناحيتين'],
    10: ['مثلا لو أنا عملت Hold على كل دول.. فجأة هتلاقيه نط للناحية التانية',
         'فالـ Linear ده اللي هو هيكبر بالتدريج.. مثلا لو انت قلت له عند Frame_10 انت حجمك 100.. وعند Frame_20 حجمك 200.. كل Frame هيكبر 10.. كل Frame هيكبر 10 بالترتيب بالظبط',
         'وقلت له إيه؟ لا أنا مش عايزك Linear.. أنا عايزك Hold.. Hold يعني أنا مش هشتغل غير لما تيجي',
         'دلوقتي هنشوف التاني.. الـ Bezier.. ممكن متلاحظوهاش هنا قوي.. بس لو عملنا Bezier هو بيعملها زي Graph.. بيخش بالهداوة وبعد كده يخرج بسرعة',
         'تقدر تفتح الجراف بتاع الـ Scale أو الـ Position من السهم ده.. تمام؟',
         'هيكبر بسرعة قوي.. ويكمل بالراحة'],
    11: ['عبارة عن إن فيه شوية كور كلهم بيمشوا مع بعض بالظبط',
         'الـ Bezier ده عامل زي حاجة في الـ After_Effects هتقابلوها اسمها Easy_Ease',
         'بس انت بقى الـ Bezier ده بيخلي الأنيميشن تخش بسلاسة.. بهدوء كده بنعومة.. وتخرج بنعومة',
         'انت عايزها تخش عادي زي الـ Linear.. كله بيكبر بنفس التدريج.. لكن في الآخر تخرج بهدوء كده.. تهدى يعني.. تفرمل',
         'هاجي عند الأولانية وأدوس Right_Click.. وأجي عند Temporal_Interpolation.. ما علينا يعني.. فأدوس Ease_In'],
    12: ['وهو عارف بقى إن في Frame_20 فيه Keyframe.. ده هيتغير.. فبيعملها بالتدريج',
         'هتتحرك من المكان A للمكان B.. وهو ده هيكون اسمه Animation',
         'انت غيرت في الـ Scale وكبرته ودست Play.. مفيش حاجة حصلت.. انت ما قلتلوش أنا عايز أشتغل على الـ Keyframes.. انت قلت له كبرلي الصورة دي.. وهتفضل كبيرة طول الوقت',
         'تدوس هنا على علامة الساعة دي اللي جنب الـ Scale',
         'فهو عند الفريم ده.. العاشر.. سيّف لي الـ Settings بتاعة الصورة دي.. تمام؟ هنا خلاص هو سيّفها.. عشان يبقى عارف المكان بتاعها',
         'تيجي هنا بقى وتكبّر الـ Scale.. هنا عمل إيه؟ عمل مربع تاني.. عمل Save_Settings كمان مرة.. طالما انت قلت له عايز أشتغل بالـ Keyframes.. أي تغيير هيعامله كـ Keyframe جديد'],
    13: ['ماشي.. بصوا الـ Ripple_Edit بيعمل إيه؟ إن هو بيقص.. ويشيل.. ويدليت.. ده الـ Ripple_Edit.. الـ Rolling_Edit بيعمل إيه؟ بيقص.. ويشيل.. ويجر.. ده الفرق',
         'فالـ Ripple_Edit دي.. بدل ما انت تقوم قاطع.. وتدوس هنا وDelete.. وبعد كده Delete وتيجي كده.. لا، فيه طريقة أسهل.. بتجيب الـ Ripple_Edit.. وتقوم دايس وتشد',
         'بتقصره وبتدليت.. كده اللي حصل إن انت قصّرت دي.. كأنك جبت الـ Move_tool ومسكت الفيديو ده قصّرته.. وبعد كده دست Delete.. بدل القصة دي بتجيب الـ Ripple_Edit.. بتعملها كده.. على طول',
         'فيه الـ Rolling_Edit.. دي عبارة عن إيه؟ أنا مثلا هنا.. قبل ما القرد ييجي يبصلنا بنكون جبنا التلج.. أنا مش عايز كده.. أنا عايز القرد يبصلنا الأول',
         'فبقوم دايس على الـ Layer بتاعة القرد.. وأقوم شادها.. وهو هنا بيجيب لي المنظرين',
         'هو اللي عمله إن هو زوّد فيديو القرد.. وخده من مساحة الفيديو بتاع التلج'],
})


# ---------- batch 3 (posting 14-17) ----------
import course_data as _CD
for _k, _v in _CD.NEW.items():
    NEW.setdefault(_k, {k: v for k, v in _v.items() if k != 'vtitle'})
SOURCE = dict(sx=0, sy=20, sw=490)          # ep1 Source monitor
LUM_PROG = dict(sx=520, sy=60, sw=520)      # ep3 colour workspace: program monitor
TITLE_PREV = dict(sx=290, sy=170, sw=460)   # ep2 legacy title window preview

SHORTS.update({
    14: dict(no=14, chapter=14, ep=1, look='pop', title='خد *الحتة* اللي عايزها بس: I و O', new='tbe', pieces=[
        dict(a=2626.3, b=2628.0, crop=SOURCE, marks=False, labels=[('المفاجأة', '🎯 الكلمة دي بس')]),
        dict(a=2602.6, b=2607.1, show='big:خد الحتة اللي عايزها|قبل ما تحطها في التايم لاين', ico='io'),
        dict(a=2678.1, b=2684.0, step='I = بداية الحتة', crop=SOURCE, key=(['I'], 'In = البداية', 1.0)),
        dict(a=2684.1, b=2692.2, step='O = نهاية الحتة', crop=SOURCE, key=(['O'], 'Out = النهاية', 0.5)),
        dict(a=2692.2, b=2703.7, show='InsOver', kw=[('Insert', 'يزق اللي بعده', 1.0), ('Overwrite', 'يكتب فوقه', 7.0)]),
        dict(a=2717.0, b=2726.1, step='Insert (,) يقسم ويزق', dual=(TLD, PROG_PANE), key=([','], 'Insert', 1.0)),
        dict(a=2808.5, b=2813.5, step='↑ ↓ أول وآخر الحتة', key=(['↑', '↓'], 'تنقّل بين الحتت', 0.5)),
    ]),
    15: dict(no=15, chapter=21, ep=1, look='lottie', title='*Slip* ولا *Slide؟*', pieces=[
        dict(a=3961.3, b=3966.4, show='SlipSlide', under=PROG_PANE, under_src=4003.5),
        dict(a=3872.5, b=3883.0, crop=PROGRAM, marks=False, labels=[('الارقام', '⏱ فيديو عدّاد')]),
        dict(a=3980.0, b=3992.6, step='Slip: نفس المكان.. محتوى تاني', crop=dict(sx=200, sy=60, sw=560), marks=False, kw=[('Slip', 'تحرّك اللي جوه الشباك', 1.0)]),
        dict(a=4002.8, b=4014.3, dual=(TLD, PROG_PANE)),
        dict(a=4128.9, b=4140.4, step='Slide: الكليب نفسه بيتحرك', dual=(TLD, PROG_PANE), kw=[('Slide', 'يقصّر ده ويطوّل ده', 4.0)]),
    ]),
    16: dict(no=16, chapter=42, ep=3, look='glass', title='*ألوان* الأفلام في Premiere', new='colormode', pieces=[
        dict(a=1576.3, b=1586.3, hook=dict(before=1505, after=1583, crop=LUM_PROG)),
        dict(a=1459.3, b=1467.5, step='Window ← Workspaces ← Color', crop=dict(sx=0, sy=20, sw=560), kw=[('Workspace', 'ترتيب شكل البرنامج', 4.0)]),
        dict(a=1484.5, b=1496.7, step='Shadow tint و Highlight tint', dual=('auto', LUM_PROG)),
        dict(a=1598.1, b=1617.7, step='Creative ← Look: ألوان جاهزة', dual=('auto', LUM_PROG), kw=[('Look', 'ألوان جاهزة', 2.0)]),
        dict(a=1621.0, b=1634.0, show='big:كل فيلم ليه لون|الفيديو لازم يبقى موحّد', ico='wheel'),
        dict(a=1647.9, b=1652.2, show='big:Harry_Potter|مزرّق وغامق جدا', ico='film'),
    ]),
    17: dict(no=17, chapter=34, ep=2, look='film', title='اكتب على الفيديو في *Premiere*', new='titles', pieces=[
        dict(a=2907.8, b=2918.7, hook=dict(before=2820, after=2985, crop=PROGRAM)),
        dict(a=2856.7, b=2865.2, step='Title: الحجم و Shadow', crop=TITLE_PREV,
             fix=dict(text='الـ Legacy Title ده اتشال من نسخة 23.0.. دلوقتي بأداة Type (T) تكتب على الشاشة على طول', src='Adobe blog + helpx')),
        dict(a=2879.9, b=2886.6, step='Background: خلفية غامقة', dual=('auto', TITLE_PREV)),
        dict(a=2886.6, b=2903.7, step='Outer Stroke ولون الكتابة', dual=('auto', TITLE_PREV), kw=[('Stroke', 'إطار حوالين الحروف', 1.0)]),
    ]),
})

CAP.update({
    14: ['أنا عايز كلمة المفاجأة بس',
         'ناخد الفوتيج اللي هنا نحطه في الـ Timeline بطريقة معينة',
         'فأدوس I.. In يعني.. I',
         'خدت كلمة استعدوا.. وبعدين أدوس O يعني Out.. فهي I و O.. بتدوس I بداية الفيديو اللي انت عايزه.. وO نهاية الفيديو اللي انت عايزه',
         'بعد كده بتدوس كوما أو دوت.. الكوما اللي هي Insert.. والدوت اللي هي Overwrite',
         'استعدوا هي هي عايز أحطها.. لو دست Insert أو دست كوما.. الـ Insert هيقسمهولي نصين.. ويجيب ده يمين وده شمال.. ويحط الفيديو بتاعه في النص',
         'هنا فيه السهم اللي فوق والسهم اللي تحت.. بيجيب لك أول وآخر المنطقة.. تدوس السهم اللي فوق يجيب لك هنا'],
    15: ['فالـ Slip_tool دي هيحصل إن احنا بنحرك اللي ورا ده.. وبنعمله كده',
         'نبدأه من أول ما تظهر الأرقام.. وعايزين نجيبه لآخر رقم.. نقص هنا.. نعلّم على دي ونشيلها',
         'وبنعمله كده.. هيعرض منه بدل رقم خمسة.. أو نعمل كده هيعرض رقم اتنين.. بس هي نفس المساحة اللي بتتعرض.. نفس المساحة الصغيرة دي',
         'بقى دلوقتي بيعرض لنا رقم أربعة وجزء من تلاتة.. تعالوا نشد بقى الناحية التانية.. على آخر الناحية هيعرض لنا خمسة',
         'أما بقى لو أنا مسكت الـ Slide_tool ودست عليه.. ودست هنا وعملت كده.. بيقصّر لك ده ويطوّل لك ده.. فده الفرق بينهم'],
    16: ['ده قبل وده بعد.. طبعا اللي بعد شكله أنضف.. ده حاسس إني ببص من إزاز طيارة.. لونه أزرق',
         'ندوس على Workspace.. نختار Color.. الـ Workspace ده بتنظيم شكل الـ Premiere بس.. تنظيم شكل البرنامج',
         'ممكن أزوّد الـ Shadow_Tint.. أزوّد الـ Highlight_Tint.. الـ Shadow_Tint والـ Highlight_Tint هما اللونين اللي كنا شغالين عليهم من شوية.. اللون الغامق واللون الفاتح',
         'يعني مثلا تدوس هنا.. لا مش عاجبني.. بالماوس بالـ Scroll تنزل كده وتجرب ألوان جاهزة هما عاملينها.. وتفضل تنزل.. نزل أكتر.. وهكذا',
         'والـ Color_correction ده مهم جدا.. لازم يكون الفيديو بتاعك موحّد.. ولو بتحب تتفرج على الأفلام هتاخد بالك إن كل فيلم تحس إن ليه لون معين',
         'ومثلا أفلام Harry_Potter مزرّقة وعلى غامق جدا'],
    17: ['أو تدوس X.. كل حاجة سيبها.. تدراج آند دروب.. وخلاص بقى الفيديو شغال وفيه الـ Title بتاعك.. وتقدر تحط عليه Transitions وهكذا',
         'تكبّره.. ممكن تحط شيب لو انت عايز.. بس مش عايزين.. أحط لها Shadow',
         'Background عشان عايز أغمّق الخلفية.. أدوس على الـ Background.. وأقلل الـ Opacity على الآخر.. حاجة بسيطة.. بقت الخلفية سودا',
         'عايز أحط Outer_Stroke.. مش عايز Inner_Stroke.. أحطه أبيض.. وأخلي الكتابة نفسها تكون زرقا مثلا.. وهكذا.. تمام؟'],
})


# ---------- batch 4 (posting 18-23) ----------
EFF2 = dict(sx=0, sy=190, sw=600)          # ep2 Effects panel (bottom left)
TL3 = dict(sx=480, sy=300, sw=520)          # ep3 timeline
AUTO_DLG = dict(sx=400, sy=90, sw=560)      # ep2 Automate To Sequence dialog
MIXER = dict(sx=0, sy=40, sw=330)           # ep3 Audio Clip Mixer
EC3 = dict(sx=0, sy=30, sw=560)             # ep3 Effect Controls (audio Level)
GAIN_DLG = dict(sx=470, sy=220, sw=340)     # ep3 Audio Gain dialog

SHORTS.update({
    18: dict(no=18, chapter=35, ep=2, look='vhs', title='*Slideshow* في ثواني', pieces=[
        dict(a=3084.9, b=3093.0, crop=PROGRAM, marks=False, labels=[('بينقل', '📸 Slideshow جاهز')]),
        dict(a=2992.1, b=2998.1, show='big:Slideshow في ثواني|من غير ما ترص الصور واحدة واحدة', ico='slides'),
        dict(a=3005.8, b=3009.9, step='حط الصور كلها في Bin'),
        dict(a=3024.0, b=3029.1, step='علّم عليهم ← Automate to Sequence', kw=[('Automate to Sequence', 'يرصّهم لوحده', 2.0)]),
        dict(a=3031.4, b=3035.0, step='Ordering: Selection Order', crop=AUTO_DLG),
        dict(a=3052.1, b=3055.9, step='Apply Default Video Transition', crop=AUTO_DLG),
        dict(a=3068.8, b=3080.9, step='Right click ← Set Selected as Default Transition', key=(['Right', 'Click'], 'على الترانزيشن', 3.0)),
        dict(a=3102.8, b=3111.5, show='big:بعدها زوّد حركة|Zoom وإضاءة ودخان', ico='slides'),
    ]),
    19: dict(no=19, chapter=31, ep=2, look='pop', title='*Transitions* صح', new='transitions', pieces=[
        dict(a=1872.5, b=1877.9, crop=PROGRAM, marks=False, labels=[('بعض', '✂ قطع ناشف')]),
        dict(a=1877.9, b=1894.9, step='Effects ← ابحث Transitions', crop=EFF2, kw=[('Effects', 'كل الإفكتات والترانزيشنز', 6.0)]),
        dict(a=1972.1, b=1988.8, step='مكانها: على الأول ولا في النص؟', dual=('auto', PROG_PANE)),
        dict(a=1999.7, b=2002.8, show='big:طول الترانزيشن|= الوقت اللي بياخده من كل فيديو', ico='trans'),
        dict(a=2053.3, b=2057.0, step='Video Transitions', crop=EFF2),
        dict(a=2076.0, b=2094.5, show='big:متعتمدش على الجاهز|غيّر الترانزيشن واشتغل Keyframes', ico='key'),
        dict(a=2100.8, b=2108.6, step='Right click ← Set Selected as Default Transition', key=(['Right', 'Click'], 'على الترانزيشن', 1.0)),
    ]),
    20: dict(no=20, chapter=32, ep=2, look='lottie', title='*Effects* جاهزة بسحبة', new='effects', pieces=[
        dict(a=2200.4, b=2208.4, crop=PROGRAM, marks=False, labels=[('بلور', '🌫 Blur في الأول')]),
        dict(a=2176.6, b=2187.0, step='Effects ← Presets ← Blurs', crop=EFF2, kw=[('Presets', 'إفكتات متظبطة جاهزة', 6.0)]),
        dict(a=2187.0, b=2190.5, step='اسحبه على الكليب', crop=EFF2),
        dict(a=2323.7, b=2337.8, step='Lumetri Presets ← Filmstocks', crop=EFF2, kw=[('Filmstocks', 'ألوان أفلام جاهزة', 2.0)]),
        dict(a=2358.1, b=2361.7, show='big:دعبس في الإفكتات|جرّب وشوف بنفسك', ico='fx'),
    ]),
    21: dict(no=21, chapter=37, ep=3, look='glass', title='الصوت يمين وشمال: *Pan*', new='speech', pieces=[
        dict(a=335.6, b=339.0, crop=MIXER, marks=False, labels=[('السماعة', '🎧 حط السماعة')]),
        dict(a=147.0, b=154.2, step='M = Mute', kw=[('Mute', 'اكتم صوت التراك', 4.0)]),
        dict(a=240.4, b=257.4, step='S = Solo', kw=[('Solo', 'اسمع التراك ده بس', 2.0)]),
        dict(a=257.4, b=262.6, step='Audio Clip Mixer'),
        dict(a=278.4, b=284.4, show='big:Pan|السماعة اليمين والشمال', ico='pan', kw=[('Pan', 'يمين ولا شمال', 1.0)]),
        dict(a=327.0, b=335.2, step='لف الـ Pan يمين على الآخر', crop=MIXER),
        dict(a=358.0, b=364.0, step='أو شمال على الآخر', crop=MIXER),
        dict(a=370.4, b=382.2, show='big:حد بيتكلم من اليمين؟|خلّي صوته من اليمين.. عمق', ico='pan'),
    ]),
    22: dict(no=22, chapter=38, ep=3, look='film', title='علّي ووطّي الصوت بـ *Keyframes*', pieces=[
        dict(a=436.6, b=441.9, show='big:Keyframes على الصوت|تعلّي وتوطّي في أي لحظة', ico='wave'),
        dict(a=478.1, b=496.2, step='Effect Controls ← Volume ← Level', crop=EC3, kw=[('Level', 'علو الصوت', 4.0)]),
        dict(a=497.2, b=517.6, step='Keyframe واطي.. وبعدين يعلى', crop=EC3),
        dict(a=526.4, b=537.6, show='big:Linear = بالتدريج|Hold = فجأة', ico='curve'),
        dict(a=640.9, b=659.2, step='أو على خط الصوت في التايم لاين', crop=TL3),
    ]),
    23: dict(no=23, chapter=39, ep=3, look='vhs', title='*Audio_Gain* في دوسة', pieces=[
        dict(a=781.4, b=791.3, step='Audio Gain: تعلّي (+) أو توطّي (-)', crop=GAIN_DLG, kw=[('Audio Gain', 'تعلية الصوت كله مرة واحدة', 2.0)]),
        dict(a=792.3, b=806.9, step='بالسالب = الصوت يوطى', crop=GAIN_DLG),
        dict(a=806.9, b=819.3, show='big:بيزوّد على اللي موجود|-42 وبعدين +42 = صفر', ico='knob'),
        dict(a=819.3, b=828.5),
    ]),
})

CAP.update({
    18: ['نشغّل الفيديو.. أهو بينقل بينهم.. بس كنت أصغّرها أكتر من كده',
         'نخش بقى في الـ Slideshow.. الـ Slideshow دي حاجة سهلة جدا.. لو انت مثلا عايز تعمل Slideshow ومكسّل',
         'هتعمل فولدر وتحط فيه كل صور الـ Slideshow اللي انت عايزها',
         'أنا عايز أعمل بيهم Slideshow.. أعلّم عليهم كلهم وأدوس Automate_to_Sequence',
         'بتقول بقى عايز ترتبهم بطريقة معينة إيه.. أنا أقول له Selection_order',
         'وهنا بقى بتقول له الترانزيشن اللي هيكون بين كل صورة وصورة',
         'زي ما عملنا قبل كده.. تخش في الإفكتات عند الترانزيشن.. وتدوس على الترانزيشن اللي انت عايزه.. Right_Click.. Set_as_Default_Transition.. تعال ندوسه كده.. بص حط لي كل الصور بتاعتي أهي',
         'تحطه على الـ After_Effects وتلعب بقى فيه.. تكبّر وتصغّر.. وتحط شوية دخان وشوية إضاءة.. بحيث تحس إن الـ Slideshow نضيف'],
    19: ['دلوقتي فيه صورتين ورا بعض.. بس بيتنقلوا بين بعض زي ما فيش حاجة',
         'أنا بقى لو جيت هنا في البانل دي.. ودست عند التاب اللي اسمها Effects.. هيجي لي إفكتات كتيرة جدا.. شبه اللي في الـ After_Effects.. وتقدر تعمل هنا سيرش',
         'نعمل زوم عشان تاخد بالك أحسن.. لو خدت بالك أنا واقف هنا.. قال لي هنا على الفيديو الأولاني بس.. ده معناه إن الفيديو الأولاني هيخرج بالطريقة دي.. بس الفيديو التاني مش هيخش بالطريقة دي',
         'هنا بس عشان المدة الزمنية.. تاخد المدة الزمنية من أنهي فيديو',
         'هتلاقيها أول ما تفتح الـ Effects.. هتلاقي Video_Transitions.. ندوس عليها',
         'متعملهمش كلهم بالطريقة دي.. ابدع.. حاول تغيّر الترانزيشن بشكل حلو.. اكبر بقى في الـ Keyframes.. تحط شوية إضاءة وهكذا.. أكيد مش حاجة أي حد يشوفها يعرف يعمل زيها',
         'انت لما تدوس على Transition معين.. عندك كلمة Set_Selected_as_Default_Transition.. تمام؟'],
    20: ['بصوا في أول الفيديو خالص.. الإفكت ده بيخلي الفيديو في الأول Blur.. وبعدين يبتدي الـ Blur يتشال ويبقى فيديو عادي خالص',
         'هتخش عند التاب اللي اسمها Effects.. تعالى نقفل كل اللي احنا فاتحينه.. هيجي لك المنظر ده.. خش مثلا على Presets.. Blurs',
         'انت عايز تعمله Blur.. هتعمل كده',
         'Filmstock.. مثلا نجرب ده.. يغيّر في الألوان.. مثلا نجرب ده.. Cinematic.. دي Color_Corrections جاهزة عموما',
         'يعني انتو دعبسوا بقى في الإفكتات دي وشوفوها'],
    21: ['لو انت حطيت السماعة هتسمع الصوت على الودن اليمين فقط',
         'مش عايز أسمع صوت الفيديو.. فهعمل إيه؟ ممكن أدوس Mute.. كده مش هسمع الفيديو',
         'مثلا عايز تسمع صوت واحد منهم.. هتدوس Solo على اللي انت عايزه.. مثلا هسمع الصوت الأولاني فقط.. وهكذا.. تمام؟',
         'هنا في التابات اللي فوق دي فيه تاب اسمها Audio_Clip_Mixer',
         'الـ R والـ L دول.. هما السماعة اليمين والسماعة الشمال.. Audio_1.. Audio_2.. Audio_3',
         'فأنا هاجي هنا عند Audio_3.. ومثلا هخلّيه Right على الآخر.. تمام؟',
         'مثلا لو أنا عملته بقى على الناحية التانية.. الشمال خالص.. كده السماعة الشمال بس اللي هتشغّل الصوت',
         'انت مثلا عايز الكلام تحس إن فيه حد بيتكلم من اليمين.. وعايز تقوّيها.. تخلي الصوت جاي من اليمين فقط.. عشان تحس بعمق الصوت'],
    22: ['فاكرين الـ Keyframes؟ بتاعة الصوت.. الأول تعالوا نشوفها في الـ Effect_Controls',
         'تيجي بقى عند الصوت.. هتلاقي عندك الـ Level.. الـ Level ده اللي كان هنا.. والـ Level معمول له Keyframe جاهز لو لاحظتم',
         'همشي مثلا أجي هنا.. وأقول له عايز Keyframe يبقى واطي.. ما يتسمعش.. وبعد كده ييجي هنا ويعلى.. يتسمع',
         'الـ Hold ما يشتغلش غير لما أوصل له.. يعني لو شغلته دلوقتي هتلاقيه بيقل بالتدريج وبيعلى بالتدريج.. لو قلت له Hold هيفضل واطي.. وفجأة يوصل للعلو اللي أنا عايزه',
         'بدل كده نقدر نتحرك بالطريقة دي.. هنا عند الأوديو.. نعمل هنا أي Keyframe ونمشي.. بس هنا مش هيبقى عندك ميزة الـ Linear والـ Bezier والـ Hold.. لكن ممكن نرجع لهم تاني'],
    23: ['فيه حاجة اسمها Audio_Gain.. الـ Audio_Gain دي لما تدوس بدل ما انت تلعب هنا.. ممكن تعمل لها بلس عشرين.. لو عملتها مثلا كده',
         'أو ممكن تعملها بالماينص.. لو عملتها بالماينص هتلاقي إنك مش سامع صوت.. أو صوت خفيف واطي',
         'أخليه بقى Audio_Gain تاني.. بص.. الـ Gain اللي كان موجود ماينص 42.. فأنا لو عملته دلوقتي 42.. مش هيبقى 42.. هيرجع زيرو.. والصوت هيتسمع',
         'طبعا دي غالبا مش هنستعملها قوي إلا لو انت عايز.. غالبا هتستعملها من هنا'],
})


# ---------- batch 5 (posting 24-29) ----------
EXP_R = dict(sx=700, sy=20, sw=560)         # ep1 Export Settings (right side)
MENU1 = dict(sx=0, sy=0, sw=480)            # ep1 File menu
RES_PX = dict(sx=330, sy=150, sw=620)       # ep1 pixel circles picture
RES_R = dict(sx=240, sy=40, sw=800)         # ep1 R squares picture
RES_UHD = dict(sx=240, sy=50, sw=800)       # ep1 SD/HD/4K/8K picture
SDHD = dict(sx=100, sy=0, sw=860)           # ep1 SD vs HD picture

SHORTS.update({
    24: dict(no=24, chapter=36, ep=2, look='lottie', title='رتّب الزحمة بـ *Nest*', pieces=[
        dict(a=3126.0, b=3136.8, show='NestAnim'),
        dict(a=3151.2, b=3161.3, step='علّم عليهم ← Right click ← Nest', key=(['Right', 'Click'], 'على الكليبات', 6.0), kw=[('Nest', 'كله في علبة واحدة', 8.0)]),
        dict(a=3162.9, b=3176.1, step='سمّيها.. وبقت Sequence واحدة'),
        dict(a=3176.2, b=3187.5, step='افتحها: كل حاجة جوه زي ما هي', dual=('auto', PROG_PANE)),
        dict(a=3187.5, b=3200.6, show='big:إفكت واحد على الكل|Keyframes وإفكتات مرة واحدة', ico='nest'),
    ]),
    25: dict(no=25, chapter=18, ep=1, look='glass', title='المقص: *Razor*', pieces=[
        dict(a=3337.4, b=3346.9, crop=PROG_PANE, marks=False, labels=[('اقص', '✂ الحتة دي تمشي')]),
        dict(a=3348.7, b=3357.5, step='C = Razor', dual=('auto', PROG_PANE), key=(['C'], 'Razor tool', 0.5), kw=[('Razor', 'المقص', 3.0)]),
        dict(a=3361.8, b=3370.4, step='V ← اختار الحتة ← Delete', dual=('auto', PROG_PANE), key=(['Delete'], 'شيلها', 5.5)),
        dict(a=3415.6, b=3424.0, dual=('auto', PROG_PANE)),
        dict(a=3427.2, b=3434.7, show='big:قص.. وشيل أو حرّك|اللي في النص', ico='razor'),
    ]),
    26: dict(no=26, chapter=22, ep=1, look='film', title='المغناطيس: *Snap*', pieces=[
        dict(a=4158.9, b=4162.4, show='big:Snap = مغناطيس|بيشد القص للمكان الصح', ico='magnet', kw=[('Snap', 'مغناطيس', 1.0)]),
        dict(a=4182.4, b=4198.3, step='Snap شغال: القص بيتشد للمؤشر'),
        dict(a=4199.3, b=4210.5, step='S = تقفل وتفتح المغناطيس', key=(['S'], 'Snap on / off', 1.0)),
        dict(a=4222.9, b=4239.4),
    ]),
    27: dict(no=27, chapter=20, ep=1, look='vhs', title='سرّع وبطّأ بسحبة: *Rate_Stretch*', new='optflow', pieces=[
        dict(a=3782.2, b=3787.1, show='big:Rate_Stretch|تسرّع وتبطّأ بالسحب', ico='rate', key=(['R'], 'Rate Stretch', 1.0)),
        dict(a=3793.8, b=3798.6, step='اسحب لجوه = أسرع', dual=('auto', PROG_PANE)),
        dict(a=3803.6, b=3808.3, step='اسحب لبره = أبطأ', dual=('auto', PROG_PANE)),
        dict(a=3827.2, b=3835.5, show='SlowMath'),
        dict(a=3835.5, b=3849.4, step='Right click ← Speed/Duration', key=(['Right', 'Click'], 'على الكليب', 0.5)),
    ]),
    28: dict(no=28, chapter=24, ep=1, look='pop', title='طلّع الفيديو: *Export*', new='export', pieces=[
        dict(a=4295.3, b=4298.7, show='big:Export|طلّع الفيديو فيديو عادي', ico='export'),
        dict(a=4300.2, b=4305.8, step='File ← Export ← Media', crop=MENU1, key=(['Ctrl', 'M'], 'نفس الحاجة', 2.5)),
        dict(a=4323.4, b=4332.8, step='Format: H.264', crop=EXP_R, kw=[('H.264', 'جودة حلوة وحجم صغير', 3.0)]),
        dict(a=4333.3, b=4341.9, step='Export Video / Export Audio', crop=EXP_R),
        dict(a=4342.6, b=4348.8, step='Output Name = مكان الحفظ', crop=EXP_R),
    ]),
    29: dict(no=29, chapter=2, ep=1, look='lottie', title='يعني إيه *Resolution*؟', pieces=[
        dict(a=252.8, b=258.3, crop=SDHD, marks=False),
        dict(a=145.2, b=161.1, crop=RES_PX, marks=False, kw=[('Pixel', 'أصغر نقطة في الصورة', 2.0)]),
        dict(a=161.1, b=171.0, show='ResGrid'),
        dict(a=172.1, b=184.8, crop=RES_R, marks=False),
        dict(a=191.8, b=199.8, show='ResLadder'),
        dict(a=199.8, b=208.6, crop=RES_UHD, marks=False, labels=[('1920', 'HD = 1920 × 1080')]),
    ]),
})

CAP.update({
    24: ['مثلا انت هنا شغال في Sequence اسمها Slideshow.. ومليانة بقى موسيقى وصور وفيديوهات.. وقصة طويلة وزحمة',
         'وعايز ألعب فيهم كلهم مرة واحدة.. مش هعمل إفكت هنا وإفكت هنا.. فأعمل إيه؟ أعلّم على كل دول.. وRight_Click.. Nest',
         'أقول له مثلا سمّيها لي.. السلايد بتاعنا.. بص هنا عمل إيه؟ عمل لي Sequence اسمها السلايد بتاعنا',
         'وهنا حوّل لي كل الصور لعبارة عن Sequence.. هتلاقي بقى اللي انت كنت عامله.. هتلاقي الصور والفيديوهات وكل حاجة',
         'كنت عاملها قبل كده بالترانزيشنز وكل حاجة.. فالـ Nest دي بتخليك الكركبة اللي عندك دي كلها تحطها في Sequence واحدة كده.. وتشتغل عليها.. وتعمل لها Keyframe لوحدها.. تحط إفكتات وهكذا'],
    25: ['أنا بقى عايز أقص الحتة دي.. تمام؟ عايزه ييجي القرد ياكل على طول.. فممكن أعملها إزاي؟',
         'أدوس C أو أختار المقص.. المقص أهو.. وأقف هنا.. وأدوس.. كده أنا قطعت',
         'أجيب بقى V عشان أجيب الأداة الأولانية.. وأدوس على الحتة دي وأدوس Delete.. بعد كده أدوس هنا وأدوس Delete',
         'هو بيقطع عشان بيرندر وهو بيشتغل.. أول ما خلصت جت على طول اللقطة بتاعة القرد وهو بياكل',
         'المقص بيقطع.. تدوس كده وكده.. وتقوم شايل اللي في النص مثلا.. أو ترفعها لفوق وتجيبها هنا.. بتقطع الفيديو اللي معاك'],
    26: ['آخر أداة بقى الـ Snap.. الـ Snap دي إيه يا باشا؟',
         'أنا هنا عايز أقطع عند الفريم ده.. أول ما آجي هنا وأدوس بقطعه.. فيه Snap.. زي المغناطيس كده.. بيشد المقص ده للمكان بتاعي',
         'أما بقى لو أنا دست هنا وشلت الـ Snap.. هيتشال المغناطيس.. مش عارف أوقفها بشكل كويس.. ممكن تقص على بعد ملّي.. تعالوا نعمل زوم على الآخر',
         'لكن لو انت مشغّل الـ Snap.. هي بتشدها.. بص أنا بعيد أهو ولسه هو معلّم على الأزرق.. أشيل المغناطيس.. أول ما أمشي من الأزرق هيقص في حتة تانية'],
    27: ['الأداة دي سهلة جدا وممتعة جدا.. دي بتحط المدة اللي بتقص.. بتسرّع وتبطّأ',
         'عايز تخليه فيديو سريع.. بتدوس وتشد.. بتقصّره كده',
         'انت بقى عايز تخليه بطيء.. بتدوس وتطوّل المدة بتاعته',
         'بس يستحسن ما تستخدمهاش كتير.. ولما تيجي تسرّع وتبطّأ.. تاخد بالك من الـ Frame_rate',
         'وتسرّع وتبطّأ زي ما احنا قلنا.. بتدوس Right_Click.. وبتدوس على Speed/Duration.. وهنا بقى تخليها تمانين في المية.. ولا أربعين في المية.. على حسب الـ Frame_rate'],
    28: ['ده الفيديو.. عايزين نعمل له Render عشان يبقى فيديو عادي خالص ونطلّعه',
         'هتدوس File.. Export.. Media',
         'الأفضل تدوس H.264.. دي بتطلّع لك الفيديو بكواليتي حلوة.. وفي نفس الوقت صغيرة.. تمام؟',
         'هنا تقدر تدوس لو عايز تخرّج الفيديو.. ولا يكون Audio بس.. أو لو عايز تخرّج الفيديو من غير صوت تعمل كده.. وهكذا',
         'هنا تدوس Output_Name.. تدوس هنا وتختار المكان اللي عايز تسيّف فيه'],
    29: ['زمان كان التصوير بالمنظر ده.. وبعد كده ده الـ HD.. الصورة أوضح',
         'عدد البيكسلز اللي في الفريم الواحد.. يعني انت عندك المربع ده قد المربع ده قد المربع ده.. تلاتة قد بعض بالظبط.. بس الأولاني فيه 10 بيكسل في العرض و10 بيكسل في الطول.. فتلاقيها مزغللة كده.. فلما تلاقيها 20 بيكسل في 20 بيكسل الصورة بتوضح',
         'كل ما تزوّد الطول في العرض بيكسلز وتضربهم في بعض.. كل ما الكواليتي بتبقى أوضح.. الـ Resolution بتبقى أنضف',
         'يعني هنا مثلا ده One_Frame.. المربع ده قد المربع ده بالظبط.. نفس الحجم.. بس الفرق عدد البيكسلز.. كل ما تزيد كل ما الصورة بتبقى أوضح',
         'ده كان الفيديو الـ Standard.. الحجم الطبيعي اللي بيتعمل.. كان صغير جدا.. بعد كده عملوا الـ Standard الجديد اللي هو الـ HD',
         'ده 1920 في 1080.. ده اللي غالبا هنشتغل عليه.. ده اللي في اليوتيوب هتلاقيه 1080p.. اللي تحته على طول 720'],
})


# ---------- batch 6 (posting 30-35) ----------
SHORTS.update({
    30: dict(no=30, chapter=1, ep=1, look='glass', title='يعني إيه *Frame_rate*؟', new='optflow', pieces=[
        dict(a=38.3, b=48.8, crop=dict(sx=240, sy=59, sw=800), marks=False, labels=[('صور', '🐎 صور جنب بعض')]),
        dict(a=82.5, b=91.3, crop=dict(sx=160, sy=0, sw=870), marks=False, kw=[('fps', 'صور في الثانية', 2.0)]),
        dict(a=93.3, b=103.1, crop=dict(sx=290, sy=120, sw=700), marks=False),
        dict(a=105.3, b=113.7, crop=dict(sx=330, sy=150, sw=620), marks=False),
        dict(a=121.8, b=128.9, show='FpsRace'),
    ]),
    31: dict(no=31, chapter=4, ep=1, look='film', title='يعني إيه *Keyframe*؟', pieces=[
        dict(a=465.9, b=469.7, crop=dict(sx=400, sy=150, sw=520), marks=False),
        dict(a=477.3, b=483.1, crop=dict(sx=400, sy=150, sw=520), marks=False, kw=[('Keyframe', 'نقطة بتحفظ الحالة', 2.5)]),
        dict(a=484.3, b=495.1, show='KeyAnim'),
        dict(a=495.5, b=508.9, show='big:Keyframe = بيحفظ المكان|والبرنامج يعمل الحركة اللي بينهم', ico='key'),
        dict(a=604.8, b=626.4, show='InterpGraph', anim=dict(kind='bezier')),
        dict(a=626.4, b=642.9, crop=dict(sx=100, sy=40, sw=860), marks=False, kw=[('Graph', 'سرعة الحركة', 3.0)]),
    ]),
    32: dict(no=32, chapter=3, ep=1, look='vhs', title='يعني إيه *Timeline*؟', pieces=[
        dict(a=271.8, b=277.4, show='big:Timeline = خط الزمن|حاجات بتحصل على مر الوقت', ico='timeline'),
        dict(a=300.6, b=315.2, crop=dict(sx=300, sy=140, sw=680), marks=False),
        dict(a=364.2, b=389.3, crop=dict(sx=0, sy=140, sw=700), marks=False, labels=[('15', '15 فريم = نص ثانية')]),
        dict(a=441.3, b=453.7, show='TimelineAnim'),
    ]),
    33: dict(no=33, chapter=5, ep=1, look='pop', title='يعني إيه *Sequence*؟', pieces=[
        dict(a=749.8, b=766.9, crop=dict(sx=330, sy=140, sw=620), marks=False),
        dict(a=767.4, b=780.2, crop=dict(sx=330, sy=140, sw=620), marks=False, kw=[('function', 'تكتبها مرة وتستخدمها كتير', 3.0)]),
        dict(a=802.6, b=809.4, show='big:Composition = Sequence|After_Effects · Premiere', ico='seq'),
        dict(a=809.4, b=833.5, show='NestAnim'),
        dict(a=913.0, b=934.4, crop=dict(sx=160, sy=0, sw=860), marks=False),
    ]),
    34: dict(no=34, chapter=11, ep=1, look='lottie', title='تشريح الـ *Timeline*', pieces=[
        dict(a=1890.0, b=1898.4, show='TimelineAnim'),
        dict(a=1967.9, b=1986.3, step='الفيديو فوق.. والأوديو تحت'),
        dict(a=2055.8, b=2066.0, step='العين = اخفي التراك', dual=('auto', PROG_PANE)),
        dict(a=2086.6, b=2090.5, step='M = Mute'),
        dict(a=4245.1, b=4263.5, step='Right click ← Add Tracks', crop=dict(sx=380, sy=120, sw=520), key=(['Right', 'Click'], 'جنب التراكات', 3.0)),
    ]),
    35: dict(no=35, chapter=12, ep=1, look='glass', title='سجّل صوتك جوه *Premiere*', new='speech', pieces=[
        dict(a=2184.5, b=2194.4, step='زرار المايك: Voice-over record', kw=[('Voice-over', 'تسجيل صوتك على الفيديو', 3.0)]),
        dict(a=2213.2, b=2226.0, step='اكتم الصوت التاني وسجّل', dual=('auto', PROG_PANE)),
        dict(a=2234.4, b=2244.1, show='big:الصدى ده ليه؟|السماعة جنب المايك = دايرة مقفولة', ico='mic'),
        dict(a=2244.1, b=2250.5),
    ]),
})


# ---------- 10 & 11 rebuilt after Aly's review (2026-10-18): Linear drawing was wrong, info not landing ----------
MENU_INT = dict(sx=300, sy=110, sw=520)     # ep2 Temporal Interpolation menu
SHORTS[10] = dict(no=10, chapter=27, ep=2, look='lottie', title='ليه حركتك شكلها *روبوت؟*', pieces=[
    dict(a=509.6, b=520.9, show='InterpGraph', anim=dict(kind='all')),
    dict(a=521.8, b=534.8, show='InterpGraph', anim=dict(kind='linear')),
    dict(a=553.3, b=567.0, show='InterpGraph', anim=dict(kind='hold')),
    dict(a=666.3, b=687.1, show='InterpGraph', anim=dict(kind='bezier')),
    dict(a=1399.9, b=1413.8, show='InterpGraph', anim=dict(kind='easeIn')),
    dict(a=1414.6, b=1419.0, show='InterpGraph', anim=dict(kind='easeOut')),
    dict(a=1435.0, b=1448.3, step='Right click على الكيفريم ← Temporal Interpolation', crop=MENU_INT, key=(['Right', 'Click'], 'على الكيفريم', 0.3)),
])
SHORTS[11] = dict(no=11, chapter=27, ep=2, look='glass', title='اتحكم في *سرعة* الحركة بالـ Graph', pieces=[
    dict(a=728.5, b=733.0, crop=PROG_PANE, marks=False, labels=[('بسرعة', '⚡ سريع.. وبعدين يهدى')]),
    dict(a=798.4, b=803.6, step='افتح الجراف من السهم جنب Scale', kw=[('Graph', 'شكل السرعة', 2.0)]),
    dict(a=623.6, b=633.2, show='big:الجراف ده = السرعة|مش القيمة نفسها', ico='curve'),
    dict(a=702.9, b=706.4, show='InterpGraph', anim=dict(kind='easeIn')),
    dict(a=710.1, b=726.9, step='ارفع الكيرف في الأول = يطلع بسرعة', dual=('auto', PROG_PANE)),
    dict(a=737.3, b=744.9, show='InterpGraph', anim=dict(kind='easeOut')),
    dict(a=765.0, b=772.0, step='نزّل الكيرف = يرجع لورا الأول', dual=('auto', PROG_PANE)),
])

CAP[10] = ['فيه حاجة في الـ After_Effects والـ Premiere اسمها الـ Keyframe.. ليها أنواع.. فيه Linear وHold وBezier.. وفيه حاجات كتير',
           'فالـ Linear ده اللي هو هيكبر بالتدريج.. مثلا لو انت قلت له عند Frame_10 انت حجمك 100.. وعند Frame_20 حجمك 200.. كل Frame هيكبر 10.. كل Frame هيكبر 10 بالترتيب بالظبط',
           'ده معناه إن أنا مش هشتغل غير لما تيجي عندي.. يعني مفيش حاجة اسمها تدريج.. كبر فجأة.. أول ما جه عند الكيفريم ده كبر فجأة.. فاهمين قصدي؟',
           'فيه كيرف ده.. اللي هو الأول بيكبر مثلا 2 سكيل في الفريم.. وبعد كده يبقى 10 سكيل في الفريم.. مثلا 20.. ويبتدي ينزل تاني لحد 2 سكيل في الفريم.. فده الـ Bezier.. وده لذيذ.. عشان ما يحسسكش إن شكلها مزعج',
           'انت عايزها تخش عادي زي الـ Linear.. 10 سكيل في الفريم.. كله بيكبر بنفس التدريج.. لكن في الآخر تخرج بهدوء كده.. تهدى يعني.. تفرمل',
           'أو عايزها تخش بهدوء.. فدي بقى ميزة الـ Ease_In أو Ease_Out',
           'وأدوس Right_Click.. وأجي عند Temporal_Interpolation.. فأدوس Ease_In']
CAP[11] = ['وهكذا.. طلع بسرعة.. وبعد كده هدي في الآخر',
           'تقدر تفتح الجراف بتاع الـ Scale أو الـ Position من السهم ده.. تمام؟',
           'الكيرف التاني ده بيوصف الحركة.. مش الـ Scale نفسه.. يعني كان بيقولك إن الحركة كانت ثابتة',
           'هيكبر بسرعة قوي.. ويكمل بالراحة',
           'يعني هو هنا عامل الكيرف إنه بيطلع بسرعة جدا.. وبعد كده ينزل الكيرف.. ده معناه إنه من السكيل ده لحد هنا هيطلّعه بسرعة أوي.. وبعد كده هنا هيبتدي يطلع بالراحة.. فبص المنظر',
           'فممكن أخليها العكس.. أخليه يكبر في الأول بالراحة.. وبعد كده يبقى سريع أوي في الآخر',
           'فاهمين قصدي؟ فالكيرف ده لما أنا نزّلته كده.. بقى بيصغّر.. وبعد كده يطلع لفوق بسرعة']

CAP.update({
    30: ['نبدأ.. أول حاجة.. الفيديو عبارة عن مجموعة صور بتتحط جنب بعض',
         'كل ما عدد الفريمز اللي في الثانية بيكتر.. كل ما انت تحس إن الفيديو فيه تفاصيل أكتر',
         'زي كده مثلا.. انت فيه هنا فريمز أكتر بكتير تحت أكتر من فوق.. فتحس إن اللي تحت فيه تفاصيل أكتر.. فاللي تحت ممكن يتعمل Slow_motion.. اللي فوق صعب',
         'ودي صورة برضه بتعبّر.. الثانية الواحدة فيها 60 صورة.. أو 45 صورة.. أو 30 صورة.. أو 15.. أو 10 بس',
         'بص.. فكرة الـ Frame_per_second دي مهمة جدا.. لو انت عندك 30 Frame_per_second.. يعني 30 صورة في الثانية'],
    31: ['الـ Timeline غالبا هتلاقي فيها مربعات كتيرة كده.. إيه المربعات دي؟',
         'فالوردة دي انت عايز تحركها من مكان لمكان.. فكل اللي بيحصل إن المربعات دي اسمها Keyframe',
         'الـ Keyframe ده يعني انت مثلا عند الفريم الفلاني خليت الوردة في مكان معين.. فبتدوس على حاجة تعمل لك Save.. إن في الفريم ده لازم الوردة تكون في المكان ده',
         'تمشي انت شوية وتحرك الوردة.. وتقول له في الفريم ده أنا عايز الوردة تكون في المكان ده.. فده Keyframe بيحفظ لك المكان.. وبيعمل لك هو لوحده الحركة اللي بينهم',
         'بس ده مش واقعي.. لما انت تشوط كورة.. في الأول الكورة بتبقى ماشية بالراحة.. تزيد سرعتها لحد ما توصل لسرعة ثابتة.. وبعد كده لما تيجي تقف هتهدى وتقف.. فانت عايز الكورة تمشي بالراحة.. بعد كده سرعتها تزيد.. وبعد كده تنزل',
         'فاهمني؟ ده هو الكيرف.. لو Keyframe عادي هتلاقي الخط ده كده مستقيم.. لكن انت جبت الجراف عشان تغيّر الاستقامة دي'],
    32: ['Timeline يعني خط الزمن.. انت بيبقى عندك حاجة بتحصل على مر الزمن',
         'فيه حدث بيحصل لوحده.. وبعد كده يحصل معاه حدث في نفس الوقت.. بعد ده يخلص الحدث ده.. وده يكمّل وهكذا.. فمهم إن انت يكون عندك خمس ست حاجات شغالين في Timeline واحد',
         'كل صورة مدّها لك على مدة زمنية.. كان هنا 15 فريم.. وهنا 1 ثانية.. وهنا 15 فريم تانيين.. ده كان 30 Frame_per_second.. 15 فريم هو النص.. 30 فريم انت كده عملت ثانية',
         'وده الـ Premiere.. ده اللي هنشتغل عليه إن شاء الله.. فبص.. انت عندك فوق عدد الثواني.. وتحت الـ Layers'],
    33: ['في البرمجة انت مثلا بتعمل إيه؟ فيه كود عندك.. والكود ده مفروض هيعمل Calculator.. ياخد رقمين يجمعهم مع بعض.. ماشي؟ انت بتعمل Function اسمها Add.. تاخد رقمين تجمعهم.. بدل ما تكتب الكود ده على طول هنا',
         'لكذا سبب.. أول سبب إنك هتحتاج تعيد الـ Function دي كذا مرة.. فانت مش هتعيد نفس الكود.. فبتعمل Function عشان تكتب اسمها بس بدل ما تعيد الكود كله',
         'فالموضوع ده في الـ After_Effects اسمه Composition.. في الـ Premiere اسمه Sequence',
         'هو عبارة عن إيه بقى؟ انت عندك فيديو.. بتحطه في Composition.. فيه كذا فيديو وصورة وأنيميشن وصوت.. تحطهم كلهم جوه Composition.. وتاخد الـ Composition ده تحطه جوه Composition تاني.. اللي هو الـ Main',
         'ودي Sequence.. اللي هي زي الـ Composition.. فيها فيديوهات كتيرة جدا.. ولو انت دست عليها هتلاقي جواها فيديوهات وصور وحاجات كتير.. هو لخّصهم في Sequence'],
    34: ['الـ Timeline فيه هنا عدد الثواني.. وهنا الـ Layers',
         'فوق دول فيديو.. لما حطيت فيديو خدتوا بالكم عمل إيه؟ اتقسم حاجتين.. صورة وصوت.. وانت طالع دي الصور.. وانت نازل دول الأوديو.. ومفصولين بحتة صغيرة كده',
         'عايز تخفيه.. زي الـ Photoshop بالظبط.. بتدوس هنا.. انت كده خليت كل الفيديوهات اللي في الـ Layer دي اختفت',
         'عند Mute تدوس هنا.. هيبقى كده لا صوت ولا صورة',
         'تزوّد عدد الـ Layers اللي في الفيديو أو في الأوديو.. بتدوس Right_Click.. Add_Tracks.. تزوّد Track فيديو أو Track أوديو.. مثلا خمس Tracks للفيديو.. وتراكين للأوديو'],
    35: ['أنا عايز أسجل صوتي.. أسجله على صوت الجيتار.. أدوس هنا',
         'اللي بيحصل إيه؟ بيخليني أتكلم Voice_over على الفيديو وهو شغال على الـ Timeline.. طب هو الفيديو شغال أصلا بيبقى فيه موسيقى شغالة.. أنا مش عايز كده.. أنا عايز أتكلم ومفيش حاجة معايا.. فأعمل كده',
         'إيه الصدى ده؟ ليه؟ عشان أنا مش بتكلم في مايك.. لو بتكلم في مايك هيبقى الوضع مختلف.. الفكرة إنه بيسمّعني وأنا بتكلم.. فبيبقى فيه دايرة مقفولة',
         'المهم انتو عرفتوا إزاي بسجل الصوت.. ده لو انت مثلا شغال على الفيديو.. وعايز كلمة تتقال دلوقتي.. فتعملها بالطريقة دي'],
})


# ---------- batch 7 (posting 36-44) ----------
TL1 = dict(sx=520, sy=190, sw=640)          # ep1 timeline panel
TH1 = dict(sx=520, sy=330, sw=420)          # ep1 track headers (targeting / sync lock)

SHORTS.update({
    36: dict(no=36, chapter=13, ep=1, look='vhs', title='الـ *Paste* هيتحط فين؟', pieces=[
        dict(a=2291.1, b=2296.4, show='big:V1 · A1 = مكان اللصق|الزرار الأزرق جنب التراك', ico='patch', kw=[('Track Targeting', 'التراك المتعلّم', 1.0)]),
        dict(a=2382.3, b=2399.8, step='Ctrl + V بيحط على أول تراك متعلّم', dual=(TH1, PROG_PANE)),
        dict(a=2399.8, b=2415.1, step='علّم V2 بس ← Ctrl + V = يتحط فوق', dual=(TH1, PROG_PANE), key=(['Ctrl', 'V'], 'Paste', 7.0)),
        dict(a=2425.9, b=2439.7, step='نفس الكلام في الصوت: A1 ← A2', crop=TL1),
        dict(a=2473.4, b=2480.8, step='من الـ Source: اسحب الفيلم = صورة بس', crop=SOURCE),
        dict(a=2481.0, b=2487.6, step='اسحب الموجة = صوت بس', crop=SOURCE),
    ]),
    37: dict(no=37, chapter=15, ep=1, look='pop', title='Insert من غير ما يقطع: *Sync_Lock*', pieces=[
        dict(a=2930.6, b=2939.5, crop=TL1, marks=False, labels=[('بيقطع', '✂ قطع اللي تحت')]),
        dict(a=2948.4, b=2954.7, step='اقفل Sync Lock على V1 · A1', crop=TH1, kw=[('Sync Lock', 'التراك يتحرك مع الـ Insert', 2.0)]),
        dict(a=2955.5, b=2965.7, step='Insert تاني = اللي تحت سليم', crop=TL1),
        dict(a=2982.0, b=2993.2, show='big:Sync_Lock مفتوح = يقطع|مقفول = سليم', ico='lock'),
    ]),
    38: dict(no=38, chapter=16, ep=1, look='lottie', title='حرّك الصوت لوحده + *Markers*', pieces=[
        dict(a=3119.5, b=3125.5, crop=TL1, marks=False, labels=[('مع', '🔗 لازقين في بعض')]),
        dict(a=3128.1, b=3137.8, step='اقفل Linked Selection', crop=TL1, kw=[('Linked Selection', 'الصوت والصورة مربوطين', 1.5)]),
        dict(a=3138.2, b=3159.0, step='حرّك الصوت لوحده', dual=(TLD, PROG_PANE)),
        dict(a=3170.3, b=3185.5, step='Add Marker = كومنت على التايم لاين', crop=TL1, key=(['M'], 'Add Marker', 6.0)),
        dict(a=3192.0, b=3204.5, step='Right click ← Clear Selected / All Markers', key=(['Right', 'Click'], 'على المسطرة', 0.3)),
    ]),
    39: dict(no=39, chapter=17, ep=1, look='glass', title='زُق كل الكليبات مرة واحدة: *A*', pieces=[
        dict(a=3207.8, b=3218.8, step='V = Selection: دوس وحرّك', crop=TL1, key=(['V'], 'Selection tool', 1.0)),
        dict(a=3243.2, b=3252.6, step='A = Track Select Forward', key=(['A'], 'يختار كل اللي بعده', 1.0)),
        dict(a=3258.6, b=3268.7, step='دوس بعد الكليب = يزق اللي بعده بس'),
        dict(a=3282.9, b=3298.0, step='Shift + A = كل اللي قبله', key=(['Shift', 'A'], 'Track Select Backward', 1.0)),
    ]),
})

CAP.update({
    36: ['الـ V1 والـ A1 دول مكان اللي انت هتحط فيه.. تمام؟ يعني إيه اللي بقوله ده؟',
         'إنك تحطهولي في.. لو أنا مثلا بعمل كوبي لتلات فيديوهات فوق بعض.. حط لي الأولاني في V1 والتاني في V2 وهكذا.. أنا بعمل كوبي لـ Layer واحدة.. من Timeline لـ Timeline.. فبقول له دلوقتي حطهولي بالأولوية',
         'في V1.. تمام؟ فهو بيحطه لي هنا.. أنا دلوقتي مش عايز ده.. أنا عايز الأولوية في V2.. فبعلّم على V2 بس.. فبدوس Ctrl_V.. حطه لي فوق.. طب أنا عايز V3.. حط الأولوية في V3',
         'حط لي الفيديو فوق عشان دي V3 هنا.. وA1 هنا.. فاهمني؟ طب أنا عايز أحط الأوديو في A2.. بشيل A1 وأسيب A2',
         'انت لو عايز تحط الفيديو بس.. بتقف على الفيديو وتجر.. كده حطيت الفيديو.. من غير الصوت',
         'عايز تحط الصوت بس.. بتمسك الأوديو وتجره وتحطه هنا.. كده حطيت الأوديو بس'],
    37: ['أنا عايز أحط الفيديو ده فوق ودست Insert.. بصوا بيحطه فوق بس بيقطع.. أنا مش عايزك تقطعه.. أنا عايزك تحطه فوق وخلاص.. فإيه اللي هيحصل؟',
         'أقول له Ctrl_Z.. عشان هنا أنا سايب دول.. أقول له هنا دول اثبتهم لي.. مش عايز يحصل لهم حاجة',
         'وبعد كده أجي هنا وأدوس Insert.. اللي حصل بقى.. بصوا.. سابهم لي عادي خالص.. وهو كمّل فوق',
         'لو سايب دول مفتوحين ودست Insert هيقطعهم.. لو قفلتهم مش هيقطعهم.. تمام؟'],
    38: ['مثلا هنا.. الفيديو والأوديو بيتحركوا مع بعض.. أنا عايز أحرك الأوديو لوحده',
         'فبدوس على دي.. Linked_Selection.. الـ Linked_Selection دي لو دست عليها.. هتقدر تتحكم في الفيديو لوحده.. والأوديو لوحده',
         'أدي الأوديو اتحرك لوحده.. هنا لو حركت مثلا الأوديو.. أدي الأوديو هو اللي سبق الفيديو بثانية.. مفيش صوت لحد ما يوصل للصوت.. والصوت هيبدأ معانا',
         'ودي عبارة عن كومنت.. انت بتدوس Add_Marker.. بيظهر لك العلامة الخضرا دي.. عشان انت عايز كومنت في الحتة دي.. وتكتب اسمه.. وتكتب اللي انت عايزه',
         'تدوس عليه Right_Click.. Clear_All_Markers.. أو تقول Clear_Selected_Marker.. كده انت بتحط Marker يعني كومنت.. عشان لو حد تاني هيشتغل من بعدك في الفيديو ده'],
    39: ['الأداة الأولانية.. بتدوس وتحرك.. كده كده.. بسيطة جدا.. انت عايز تحرك الفيديو بس كده',
         'الأداة دي عبارة عن إنك بتزق كل الفيديوهات مع بعض.. لو دست هنا هيزق لك كل الفيديوهات على الجنب شوية',
         'لكن مش عايز أزق الفيديو الأولاني ده.. فهاجي هنا من بعد الفيديو ده على طول.. كده هزق كل الفيديوهات اللي بعده.. تمام؟',
         'المفروض اللي يتشد الفيديو الأولاني بس.. عشان أنا معلّم عنده.. طب لو أنا عايز أشد كله.. أجي من هنا.. تمام؟'],
})

FILEMENU1 = dict(sx=0, sy=0, sw=600)        # ep1 File > New menu
NEWSEQ1 = dict(sx=330, sy=60, sw=680)       # ep1 New Sequence dialog
SHORTS.update({
    40: dict(no=40, chapter=8, ep=1, look='film', title='اعمل *Sequence* صح', pieces=[
        dict(a=1305.7, b=1314.2, show='big:التايم لاين فاضي؟|محتاج Sequence الأول', ico='seq'),
        dict(a=1315.8, b=1327.2, step='File ← New ← Sequence', crop=FILEMENU1, key=(['Ctrl', 'N'], 'Sequence جديدة', 7.0)),
        dict(a=1385.1, b=1404.8, step='اختار 1080 و 30 / 25 / 24 fps', crop=NEWSEQ1),
        dict(a=1737.8, b=1761.2, step='أو اسحب الفيديو على أيقونة New Item', kw=[('New Item', 'Sequence بنفس إعدادات الفيديو', 8.0)]),
    ]),
    41: dict(no=41, chapter=7, ep=1, look='vhs', title='دخّل ملفاتك في *Premiere*', pieces=[
        dict(a=1153.6, b=1165.6, show='big:Project = مكتبة|مش Layers زي Photoshop', ico='folder'),
        dict(a=1169.6, b=1188.6, src=1174.0, step='دبل كليك في الـ Project ← اختار الملف', key=(['Ctrl', 'I'], 'Import', 2.0)),
        dict(a=1189.6, b=1201.4, step='كبّر وصغّر الأيقونات'),
        dict(a=1215.0, b=1238.8, step='Import Folder = فولدر كامل'),
        dict(a=1253.8, b=1270.7, step='أو اسحب وارمي من الويندوز'),
    ]),
    42: dict(no=42, chapter=6, ep=1, look='pop', title='أول مرة تفتح *Premiere*', pieces=[
        dict(a=966.3, b=976.3, step='New Project', crop=dict(sx=200, sy=0, sw=860)),
        dict(a=978.6, b=997.0, step='اكتب الاسم واختار المكان', crop=dict(sx=340, sy=40, sw=600)),
        dict(a=1059.1, b=1080.6, step='كل مربع = Panel.. الأزرق = اللي شغال', kw=[('Panel', 'مربع من البرنامج', 4.0)]),
        dict(a=1835.6, b=1855.0, step='دبل كليك على اسم البانل = تكبر الشاشة كلها'),
    ]),
    43: dict(no=43, chapter=46, ep=3, look='lottie', title='رتّب شكل البرنامج: *Workspaces*', pieces=[
        dict(a=2697.8, b=2713.4, step='Editing للمونتاج · Color للألوان', kw=[('Workspace', 'ترتيب البانلز', 2.0)]),
        dict(a=2722.0, b=2738.6, step='اعمل الـ Workspace بتاعك', crop=dict(sx=0, sy=0, sw=870)),
        dict(a=1031.4, b=1043.1, ep=1, show='big:Workspace|زي اللي في Photoshop', ico='grid'),
    ]),
    44: dict(no=44, chapter=14, ep=1, look='glass', title='*اختصارات* الكورس كلها', pieces=[
        dict(a=1324.6, b=1327.2, step='Ctrl + N = Sequence', crop=FILEMENU1, key=(['Ctrl', 'N'], 'Sequence جديدة', 0.3)),
        dict(a=2305.1, b=2311.0, step='Ctrl + C / Ctrl + V', key=(['Ctrl', 'C'], 'Copy', 0.3)),
        dict(a=2678.1, b=2684.0, step='I = بداية الحتة', crop=SOURCE, key=(['I'], 'In', 0.3)),
        dict(a=2684.1, b=2688.5, step='O = نهاية الحتة', crop=SOURCE, key=(['O'], 'Out', 0.3)),
        dict(a=2698.3, b=2703.7, step=', = Insert · . = Overwrite', key=([','], 'Insert', 0.3)),
        dict(a=3207.8, b=3212.5, step='V = Selection', key=(['V'], 'Selection', 0.3)),
        dict(a=3348.7, b=3352.0, step='C = Razor', key=(['C'], 'المقص', 0.3)),
        dict(a=3243.2, b=3249.1, step='A = Track Select Forward', key=(['A'], 'زق اللي بعده', 0.3)),
        dict(a=1779.9, b=1782.2, ep=2, step='Ctrl + D = ترانزيشن', key=(['Ctrl', 'D'], 'Default transition', 0.3)),
        dict(a=2948.4, b=2950.6, step='Ctrl + Z = رجوع', key=(['Ctrl', 'Z'], 'Undo', 0.3)),
        dict(a=4301.3, b=4305.8, step='Ctrl + M = Export', crop=MENU1, key=(['Ctrl', 'M'], 'Export', 0.3)),
    ]),
})


# 12 rebuilt (Aly 2026-10-18: "مش حاسس ان الفيديو شارح نفسه"): result first, then every step with setting + result together
EFF2C = dict(sx=0, sy=20, sw=640)           # ep2 Effect Controls (top left)
SHORTS[12] = dict(no=12, chapter=26, ep=2, look='film', title='حرّك أي حاجة بـ *Keyframes*', new='props', pieces=[
    dict(a=465.4, b=474.7, crop=PROG_PANE, marks=False, labels=[('بالتدريج', '🎬 كبر لوحده')]),
    dict(a=209.9, b=216.6, show='KeyAnim', kw=[('Keyframe', 'نقطة بتحفظ الحالة', 2.0)]),
    dict(a=352.3, b=363.4, dual=(EFF2C, PROG_PANE), labels=[('حاجة', '❌ مفيش حركة')]),
    dict(a=375.4, b=383.8, step='دوس على الساعة جنب Scale', dual=(EFF2C, PROG_PANE), kw=[('Stopwatch', 'ابدأ Keyframes', 4.0)]),
    dict(a=405.7, b=416.1, step='أول Keyframe = حفظ الحجم هنا', dual=(EFF2C, PROG_PANE)),
    dict(a=426.6, b=444.7, step='فريم تاني + غيّر = Keyframe جديد', dual=(EFF2C, PROG_PANE)),
])
CAP[12] = ['أول ما يوصل للـ Keyframe.. وهو عارف بقى إن في Frame_20 فيه Keyframe.. ده هيتغير.. فبيعملها بالتدريج',
           'هتتحرك من المكان A للمكان B.. وهو ده هيكون اسمه Animation',
           'أنا غيّرت في الـ Scale وكبّرته ودست Play.. مفيش حاجة حصلت.. انت ما قلتلوش أنا عايز أشتغل على Keyframes.. انت قلت له كبّر لي الصورة دي.. وهتفضل كبيرة طول الوقت',
           'وقول له أنا عايز أبدأ أشتغل بالـ Keyframes على الـ Scale.. تدوس هنا على علامة الساعة دي اللي جنب الـ Scale',
           'فهو عند الفريم ده.. العاشر.. سيّف لي الـ Settings بتاعة الصورة دي.. تمام؟ هنا خلاص هو سيّفها.. عشان يبقى عارف المكان بتاعها',
           'تيجي هنا بقى وتكبّر الـ Scale.. لو خدتوا بالكم عمل إيه؟ عمل مربع تاني.. عمل Save_Settings كمان مرة.. طالما انت قلت له عايز أشتغل بالـ Keyframes.. أي تغيير هيعامله كـ Keyframe جديد']


# ---------- sentence-snapped edges (fix_edges.py + hand checks, 2026-10-18) ----------
import json as _json, os as _os
_fx = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../shorts/edge_fixes.json')
for _k, (_a, _b) in _json.load(open(_fx)).items():
    _n, _i = map(int, _k.split('.'))
    SHORTS[_n]['pieces'][_i]['a'], SHORTS[_n]['pieces'][_i]['b'] = _a, _b

# captions matching the snapped edges
CAP[4][2] = 'تعمل Slow_motion.. بتصور بفريم عالي.. وتنزّله للـ 24 فريم'
CAP[4][3] = CAP[4][3] + '.. فاهمني؟ ده المفروض يبقى Equal في الآخر'
CAP[15][2] = 'هيعرض منه بدل رقم خمسة.. أو نعمل كده هيعرض رقم اتنين.. بس هي نفس المساحة اللي بتتعرض.. نفس المساحة الصغيرة دي'
CAP[18][0] = 'نشغّل الفيديو.. أهو.. بينقل بينهم'
CAP[19][1] = CAP[19][1] + ' على Transitions.. هيجي لك Transitions'
CAP[24][3] = CAP[24][3] + ' اللي انت كنت عاملها قبل كده'
CAP[24][4] = 'فالـ Nest دي بتخليك الكركبة اللي عندك دي كلها تحطها في Sequence واحدة كده.. وتشتغل عليها.. وتعمل لها Keyframe لوحدها.. تحط إفكتات وهكذا'
CAP[26][1] = CAP[26][1] + ' عليه'
CAP[27][4] = 'بتدوس Right_Click.. وبتدوس على Speed/Duration.. وهنا بقى تخليها تمانين في المية.. ولا أربعين في المية.. على حسب.. زي ما قلنا في الـ Frame_rate'
CAP[36][1] = CAP[36][1] + ' في V1'
CAP[36][2] = 'فهو بيحطه لي هنا.. أنا دلوقتي مش عايز ده.. أنا عايز الأولوية في V2.. فبعلّم على V2 بس.. فبدوس Ctrl_V.. حطه لي فوق.. طب أنا عايز V3.. حط الأولوية في V3'
CAP.update({
    40: ['بس هو فاضي.. إزاي بقى تملاه وتبقى فيه Sequence تشتغل فيها.. يكون فيه Timeline تعمل فيديوهات عليه؟ في كذا طريقة',
         'ممكن تدوس File.. New.. Sequence.. أو ممكن تدوس Ctrl_N',
         'هنا بتختار الكواليتي بتاعة الفيديو بتاعك.. هنا عندك الـ 1080.. اللي هي 1920 في 1080.. 30 فريم.. أو 1080 25 فريم.. أو 1080 24 فريم',
         'إنك تمسك الفيديو اللي انت عايزه وتجره على المكان ده.. هو عمل لك إيه؟ عمل لك Sequence وTimeline بنفس الـ Properties بالظبط بتاعة الفيديو ده.. لو الفيديو ده 30 فريم هيعمل لك ده 30 فريم.. لو الفيديو ده HD هيعمل لك ده HD.. وهكذا'],
    41: ['في الـ Photoshop بتاخد صورة بتدخل على طول في الـ Layers.. هنا انت مش عايز كده.. هنا انت بتحط الصور على جنب.. في حاجة زي المكتبة كده.. وبتاخد منها تحطها في الفيديوهات',
         'فعشان تحط صور في البرنامج.. بتدوس Double_click في المكان ده في الـ Project.. وبتختار مثلا الفيديو ده.. كده انت حطيت الفيديو ده في الـ Project بتاعك.. عايز تحط صورة نفس الشيء.. دي صورة اتحطت في الـ Project بتاعك',
         'ومن هنا بتكبّر أو بتصغّر حجم الحاجات المعروضة عندك.. عشان لو حطيت حاجات كتير ما تبقاش زحمة وتفضل تعمل Scroll.. فهنا تكبّر وهنا تصغّر',
         'أو مثلا عايز تحط فولدر كامل.. ممكن تدوس Import.. وتختار مثلا فولدر Videos.. عايز تاخده كامل تحطه في الـ Project عندك.. هتدوس Import_Folder.. كده الفولدر',
         'أو ممكن أسهل من ده كله.. تدوس وتعمل Drag.. تمام؟ عايز خلاص.. دوس واسحب'],
    42: ['هيفتح لك البتاع ده.. هيقول لك عايز تعمل New_Project ولا Open_Project.. فأكيد هتدوس New_Project',
         'أول حاجة هيظهر لك الـ Name.. عايز تسميه إيه؟ هنسميه Training_180.. هنا بقى الـ Location.. عايز تحطه فين؟ أنا عايز أحطه في الـ Work.. Select_Folder',
         'أول حاجة نشرحها الـ Panels.. إيه الـ Panels دي؟ انت شايف دلوقتي حاجات مربعات.. كل مربع ده اسمه Panel.. تمام؟ لما تيجي تشتغل في Panel معينة بتدوس عليها.. حواليها كده أزرق.. تدوس هنا.. هتبقى دي زرقا.. يعني هي اللي عليها التركيز دلوقتي',
         'هو ده الـ Premiere والـ After_Effects والبرامج دي عموما.. لما انت تيجي تركز في مكان معين.. بتروح عند اسمه وتدوس Double_click.. يعني مثلا عايز دي تاخد المساحة كلها.. دوس Double_click.. يحصل كده'],
    43: ['يعني الـ Workspaces دي بتسهّل لك الشغل.. ممكن تدوس على Editing عشان تعمل Edit.. تدوس على الـ Workspace اللي اسمها Color عشان تلعب في الألوان.. وهكذا.. بتحط لك الحاجات اللي هتستخدمها أكتر.. وطبعا تقدر تعمل الـ Workspace اللي انت عايزها',
         'ده كان لما دست على الـ Workspace اللي اسمها All.. بحط لي الحاجات بالمنظر ده.. ودي الـ Workspaces اللي فوق.. ممكن أعمل Edit_Workspaces.. وأعمل الـ Workspace اللي أنا عايزها.. تمام؟ أنا بفضّل Editing وبرجع لها',
         'دي حاجة اسمها Workspace.. زي اللي في الـ Photoshop'],
    44: ['أو ممكن تدوس Ctrl_N',
         'Ctrl_C.. عملت Copy.. تمام؟ لو دست Ctrl_V',
         'فأدوس I.. In يعني.. I',
         'وبعدين أدوس O.. يعني Out.. فهي I وO',
         'الكوما اللي هي Insert.. والدوت اللي هي Overwrite',
         'الأداة الأولانية.. الشورت كت بتاعها V.. بتدوس وتحرك',
         'أدوس C.. أو أختار المقص',
         'الأداة دي عبارة عن إنك بتزق كل الفيديوهات مع بعض',
         'لو دست عليه وعملت له Ctrl_D',
         'أقول له Ctrl_Z',
         'هتدوس File.. Export.. Media'],
})


# ---------- Aly review 2 (2026-10-18): 1, 25, 30, 31, 34 ----------
EC3K = dict(sx=0, sy=140, sw=520)            # ep3 Effect Controls around Key Color (eyedropper)
TL25 = dict(sx=300, sy=380, sw=640)          # ep1 timeline tracks where he cuts (razor)
# 1: the eyedropper clicks shown (Effect Controls on top, the picture under it)
SHORTS[1]['pieces'][3].update(dual=(EC3K, PROG_PANE), src=2471.2, clicks=[(2474.6, 214, 231), (2475.4, 1028, 130)])
# 25: everything happens on the timeline -> the timeline is always on screen with the cut/select clicks
for _i in (0, 1, 2, 3):
    _p = SHORTS[25]['pieces'][_i]; _p.pop('crop', None); _p['dual'] = (TL25, PROG_PANE)
SHORTS[25]['pieces'][1]['clicks'] = [(3355.9, 516, 520)]
SHORTS[25]['pieces'][2]['clicks'] = [(3365.4, 500, 524), (3369.2, 502, 524)]
# 30: fast start — the idea first (animation), then his pictures
SHORTS[30]['pieces'] = [
    dict(a=121.8, b=128.9, show='FpsRace', kw=[('fps', 'صور في الثانية', 2.0)]),
    dict(a=38.3, b=48.4, crop=dict(sx=240, sy=59, sw=800), marks=False, labels=[('صور', '🐎 صور جنب بعض')]),
    dict(a=105.3, b=113.7, crop=dict(sx=330, sy=150, sw=620), marks=False, labels=[('60', '60 صورة في الثانية')]),
    dict(a=82.5, b=91.3, crop=dict(sx=160, sy=0, sw=870), marks=False, labels=[('تفاصيل', '✨ تفاصيل أكتر')]),
    dict(a=93.3, b=103.1, crop=dict(sx=290, sy=120, sw=700), marks=False, labels=[('slow', '🐢 Slow motion')]),
]
CAP[30] = [CAP[30][4], 'نبدأ.. أول حاجة.. الفيديو عبارة عن مجموعة صور بتتحط جنب بعض', CAP[30][3], CAP[30][1], CAP[30][2]]
# 31: his own example — the rose and "Save" — drawn
SHORTS[31]['pieces'][2] = dict(a=484.3, b=495.13, show='RoseKey', anim=dict(stage=1))
SHORTS[31]['pieces'][3] = dict(a=495.5, b=508.9, show='RoseKey', anim=dict(stage=2))
# 34: where he clicks
SHORTS[34]['pieces'][1]['crop'] = dict(sx=0, sy=330, sw=700)
SHORTS[34]['pieces'][2].update(dual=(dict(sx=400, sy=380, sw=600), PROG_PANE))
SHORTS[34]['pieces'][3].update(crop=dict(sx=400, sy=380, sw=600), clicks=[(2088.3, 654, 570)])
SHORTS[34]['pieces'][4]['crop'] = dict(sx=150, sy=60, sw=760)
SHORTS[34]['pieces'][1]['crop'] = dict(sx=0, sy=170, sw=760)

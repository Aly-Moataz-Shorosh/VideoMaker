# Aly 2026-10-27: "19 مش مفهوم كفاية و ممل و نفس الكلام 20.. 21.. 22 اغلب الفيديو بشرح حاجات انت مش مبينها.. 23 مش فاهم ايه اللي
# بيحصل كا متفرج". Cause: he talks about SOUND examples he played (tawashih, a video without music, the dialogue scene before/after,
# room tone) and the shorts never let the viewer HEAR them; 22's middle was an animation while he pointed at the Single/Double system
# drawing. -> the examples are raw pieces (heard as they played in the session), his pointing = zoom on that part, 23 = camera sound vs
# mic sound named clearly, the clap, then the Sync animation. These shorts replace the 19-23 data (incl. series_data7 for them).
FULL = dict(sx=220, sy=40, sw=760)
CLIP20 = dict(sx=290, sy=60, sw=690)          # 20: the small demo window (50 %)
ED21 = dict(sx=300, sy=60, sw=500)            # 21: the editor's player (the film shot) + top of its timeline
SLIDE22 = dict(sx=220, sy=60, sw=760)         # 22: "Sync Sound" slide (camera + recorder)
ALL22 = dict(sx=240, sy=120, sw=600)          # 22: Single / Double system drawing (normal view, 4190+)
SINGLE = dict(sx=250, sy=160, sw=320)
DOUBLE = dict(sx=520, sy=160, sw=320)
MON = dict(sx=760, sy=60, sw=420)             # 23: Premiere program monitor = his video
MONTL = dict(sx=480, sy=40, sw=780)
CLAP = dict(sx=700, sy=300, sw=420)

SHORTS = {
    19: dict(no=19, chapter=16, at='1:04:41', title='إحساس من غير *موسيقى*', pieces=[
        dict(a=3813.6, b=3824.0, raw=True, crop=FULL, bars=True, lab=[(0.3, 'تواشيح بدل الموسيقى', 'mosque', 3.0)]),
        dict(a=3801.54, b=3813.4, crop=FULL),
        dict(a=3836.9, b=3881.0, crop=FULL, labels=[('شعر', 'شعر وكلمات عربي', 'scroll'), ('اجنبية', 'حتى على حاجة أجنبية', 'globe_with_meridians'), ('الصليبية', 'فيلم جمع الاتنين', 'crossed_swords')]),
        dict(a=3881.54, b=3902.6, crop=FULL, labels=[('خبطات', 'صوت خبطات', 'drum')]),
        dict(a=3902.8, b=3913.0, raw=True, crop=FULL, bars=True, lab=[(0.3, 'من غير موسيقى: دقات بس', 'drum', 3.0)]),
    ]),
    20: dict(no=20, chapter=17, at='1:08:06', title='إزاي *تبدع* في الحوار', pieces=[
        dict(a=3963.4, b=3971.6, crop=CLIP20),
        dict(a=3979.0, b=3990.0, raw=True, crop=FULL, bars=True, lab=[(0.3, 'العادي: صوته زي ما اتسجل', 'speaking_head', 3.0)]),
        dict(a=4002.7, b=4028.6, crop=FULL, labels=[('متوتر', 'متوتر وخايف', 'anxious_face_with_sweat'), ('مكانه', 'خليني مكانه', 'ear')]),
        dict(a=4028.7, b=4046.0, raw=True, crop=FULL, bars=True, lab=[(0.3, 'الإبداع: الصوت بيقل.. زي ما هو سامع', 'ear', 3.4)]),
        dict(a=4053.7, b=4072.4, crop=dict(sx=80, sy=40, sw=760), labels=[('يقل', 'الصوت يقل', 'speaker_low_volume'), ('أوداني', 'كأن إيدي على وداني', 'ear')]),
    ]),
    21: dict(no=21, chapter=18, at='1:10:15', title='الصوت *المحيط* Ambience', pieces=[
        dict(a=4073.58, b=4080.6, src=4109.9, crop=ED21),
        dict(a=4086.0, b=4100.4, raw=True, crop=ED21, bars=True, lab=[(0.3, 'اسمع الخلفية', 'ear', 2.6)]),
        dict(a=4109.35, b=4141.9, crop=ED21, labels=[('غن', 'الشوت جن شال الخلفية', 'studio_microphone'), ('كاتمة', 'سكوت تام = غلط', 'cross_mark'),
                                                     ('سجل', 'سجّل الخلفية لوحدها', 'microphone'), ('وورا', 'وحطها تحت الكلام', 'level_slider')]),
    ]),
    22: dict(no=22, chapter=19, at='1:11:33', title='*Sync* الصوت مع الصورة', pieces=[
        dict(a=4155.27, b=4171.1, crop=SLIDE22, labels=[('سينك', 'Sync = تزامن', 'link')]),
        dict(a=4180.37, b=4221.6, src=4190.5, crop=ALL22,
             zoom=[(4193.1, SINGLE), (4196.0, DOUBLE), (4200.3, ALL22), (4205.6, SINGLE), (4214.1, ALL22)],
             labels=[('للكاميرا', 'Single: المايك في الكاميرا', 'video_camera'), ('بمسجل', 'Double: المايك في مسجل صوت', 'studio_microphone'),
                     ('جودة', 'الكاميرا بتقلل جودة الصوت', 'speaker_low_volume')]),
        dict(a=4222.5, b=4253.2, crop=ALL22, labels=[('مسجل', 'سجّل على مسجل أو موبايل', 'mobile_phone')]),
    ]),
    23: dict(no=23, chapter=20, at='1:15:49', title='صوت الكاميرا ولا *المايك*؟', pieces=[
        dict(a=4443.9, b=4451.2, raw=True, crop=MON, bars=True, lab=[(0.2, 'صوت كاميرا الموبايل', 'mobile_phone', 3.2)]),
        dict(a=4496.2, b=4508.4, raw=True, crop=MON, bars=True, lab=[(0.2, 'صوت المايك', 'studio_microphone', 3.2)]),
        dict(a=4454.66, b=4463.1, crop=MON, lab=[(0.3, 'الكاميرا: وش كتير وصوت واطي', 'speaker_low_volume', 3.0)]),
        dict(a=4508.53, b=4523.5, crop=MON, labels=[('المروحة', 'المايك: مفيش وش', 'check_mark_button'), ('الكمبيوتر', 'الصوت على الكمبيوتر', 'laptop'), ('الموبايل', 'والصورة على الموبايل', 'mobile_phone')],
             lab=[(12.0, 'بسقّف بإيدي', 'clapping_hands', 2.4)]),
        dict(a=4529.59, b=4554.5, crop=MONTL, zoom=[(4540.0, CLAP)], clicks=[(4544.6, 900, 560, 40, 90)], lab=[(15.5, 'التسقيفة = ويف عالية في الاتنين', 'clapping_hands', 2.6)]),
        dict(a=4560.72, b=4579.2, show='SyncAnim'),
    ]),
}

CAP = {
    19: ['',
         'بس هل كل الأفلام عشان أوصل إحساس لازم موسيقى تصويرية؟ مش لازم.. ممكن أستخدم أدان.. أو مش لازم أدان.. ممكن تواشيح أو أي حاجة زي كده',
         'انت مش لازم تصور حاجة إسلامية عشان تستخدم الحاجات دي.. فيه كلمات شعر كتير وكلمات عربي كتير وتواشيح كتير بتتكلم عن معاني مختلفة.. ممكن تحطها في أوقات مختلفة.. طب لو هتصور حاجة أجنبية؟ ينفع تحط حاجة عربي.. وهتلاقي فيه حاجات زي كده كتير في كل اللغات.. مش عندنا بس.. زي الأوبرا.. فيه فيلم مستخدم توشيح عربي على أجنبي.. عشان كان فيه الحروب الصليبية.. فكان جامع بين الاتنين بشكل حلو جدا',
         'ممكن تستخدم صوت خبطات أو حاجات زي كده.. انت تعمل الإحساس.. والموسيقى التصويرية.. زي الفيديو ده من غير موسيقى خالص.. فبصوا هتلاقوا الخلفية يا إما دقات.. يا إما ضرب.. يا إما تسقيف.. فدي الموسيقى التصويرية',
         ''],
    20: ['الديالوج مثلا.. انت إزاي هتبدع فيه؟ خلاص سجلت الراجل.. هتوصل إحساس أكتر من اللي هو عمله في التمثيل؟ لا.. ينفع تعمل كده',
         '',
         'راجل بيتكلم.. والراجل ده المفروض يكون متوتر وخايف ومرعوب.. بس انت هنا ما أبدعتش.. أخدت الصوت بتاع الراجل حطيته وخلاص.. طب إزاي تخليها توضح المعنى ده أكتر؟ بسيطة.. إنك توصل لشعور الراجل ده نفسه.. حاسس بإيه.. تخليني مكانه.. فمثلا هنخلينا مكانه.. وصوت الراجل من كتر تركيزه ما بقاش يسمع.. ومن كتر خوفه',
         '',
         'وهنا بقى خلى الصوت يقل.. كأني حطيت إيدي على وداني.. وبسمع الصوت بيقل معايا.. فهو ده.. انت ممكن برضو تمسك الصوت بتاع الراجل وتشتغل عليه.. مش لازم تمسك الحوار بس'],
    21: ['كده قلنا مؤثرات صوتية.. قلنا الحاجات دي كلها.. ناقص حاجة أخيرة.. الصوت المحيط.. فبصوا الفيديو ده',
         '',
         'اللي حصل إنه استخدم شوت جن عشان يسجل أصوات الممثلين.. فالشوت جن شال تقريبا أغلب الصوت اللي في الخلفية.. فبقى فيه صوت كاتم كده.. ما بقاش فيه صوت.. فده غلط.. لازم يكون فيه الصوت المحيط دايما.. عشان احنا مصورين حاجة في الواقع.. فهو سجل الخلفية عادي لوحدها.. وخد الأمبيانس ده.. الصوت المحيط.. وحطه بين السكتات.. وورا الكلام بس بصوت أقل.. بحيث إن ما يبقاش فيه سكوت تام'],
}

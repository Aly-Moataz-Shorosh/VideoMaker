# "أسرار الصوت" shorts 03 + 04 (chapter 3, film examples). Aly 2026-10-27: "اعمل 03 و 04 بمقاطع الأفلام زي الكورس" -> the film
# clips he played in the session are SHOWN and HEARD (raw pieces, exact edges, as they played), with the film name card (FilmTag)
# like the course. raw = exact edges where fit() clipped his first word (quiet start). Students' talk (720-733 / 816-834) and the Hazem film-making aside (897.6-904.1) are cut out.
MICKEY = dict(sx=0, sy=0, sw=834)      # Mickey, Donald, Goofy: Pete is on the left half
KOC = dict(sx=100, sy=0, sw=834)       # The King of Comedy: man at his desk / the laughing crowd
WRS = dict(sx=220, sy=0, sw=834)       # The Wrestler (letterboxed in the middle of his screen)
RB = dict(sx=220, sy=0, sw=834)        # Raging Bull: the boxer in the middle
F_MICKEY = dict(title='Mickey, Donald, Goofy: The Three Musketeers', year='2004', note='الموسيقى كنوع من الكوميديا')
F_KOC = dict(title='The King of Comedy', year='1982', note='الموسيقى بتوصل معنى')
F_WRS = dict(title='The Wrestler', year='2008', note='الصوت بيحكي اللي في دماغه')
F_RB = dict(title='Raging Bull', year='1980', note='بنسمع اللي هو سامعه بس')

SHORTS = {
    3: dict(no=3, chapter=3, at='9:12', title='الموسيقى *بتضحّكك*.. وبتخوّفك', pieces=[
        # hook: the opera joke itself (the same music every time he says "الأوبرا")
        dict(a=678.62, b=691.0, raw=True, crop=MICKEY, film=F_MICKEY, lab=[(6.6, 'نفس الموسيقى.. كل مرة', 'repeat_button', 3.0)]),
        dict(a=652.5, b=661.2, show='IdeaRows', anim=dict(rows=[
            dict(at=0.3, y=520, pics=['musical_note', 'face_with_tears_of_joy'], tag='الموسيقى ممكن تبقى كوميديا'),
            dict(at=5.6, y=880, pics=['clapper_board'], tag='زي فيلم ميكي وبطوط وبندق', c='#8B5CF6')])),
        dict(a=671.2, b=678.55, src=671.2, crop=MICKEY, labels=[('بتتعاد', 'بتتعاد كذا مرة', 'repeat_button'), ('أوبرا', 'كل ما يقول «أوبرا»', 'musical_note')]),
        dict(a=691.0, b=709.7, raw=True, crop=MICKEY),
        dict(a=709.7, b=713.6, raw=True, show='IdeaRows', anim=dict(rows=[
            dict(at=0.3, y=620, pics=['face_with_tears_of_joy', 'check_mark_button'], tag='الرسالة وصلت.. بالضحك')])),
        dict(a=738.1, b=748.0, show='IdeaRows', anim=dict(rows=[
            dict(at=0.3, y=480, pics=['musical_note', 'light_bulb'], tag='الموسيقى كمان بتوصل معنى'),
            dict(at=4.6, y=830, pics=['star', 'microphone'], tag='عايز يبقى كوميديان مشهور', c='#8B5CF6')])),
        dict(a=748.95, b=762.65, raw=True, crop=KOC, labels=[('دماغه', 'اللي في دماغه', 'thought_balloon'), ('صور', 'بيكلم صور', 'framed_picture'), ('ودانه', 'بنسمع اللي في ودانه', 'ear')]),
        dict(a=762.7, b=779.4, raw=True, crop=KOC, film=F_KOC, lab=[(7.0, 'الضحك اللي في دماغه', 'face_with_tears_of_joy', 3.0)]),
        dict(a=779.4, b=785.7, raw=True, show='IdeaRows', anim=dict(rows=[
            dict(at=0.3, y=500, pics=['fearful_face'], tag='ممكن تقلب رعب شوية', c='#FF6B5A'),
            dict(at=2.8, y=860, pics=['star', 'brain'], tag='بس بتقول: مهووس بالشهرة', c='#8B5CF6')])),
    ]),
    4: dict(no=4, chapter=3, at='14:24', title='الصوت *بيحكي* اللي في دماغه', pieces=[
        # hook: the music rises like he is walking into the ring.. and stops dead: it is the supermarket
        dict(a=846.0, b=861.8, raw=True, crop=WRS, film=F_WRS, lab=[(9.0, 'داخل الحلبة؟', 'boxing_glove', 2.6), (13.0, 'لا.. السوبر ماركت', 'shopping_cart', 2.6)]),
        dict(a=788.3, b=804.5, show='IdeaRows', anim=dict(rows=[
            dict(at=0.3, y=470, pics=['boxing_glove', 'cross_mark'], tag='مصارع بطّل المصارعة'),
            dict(at=6.8, y=780, pics=['shopping_cart'], tag='بقى شغال في سوبر ماركت', c='#8B5CF6'),
            dict(at=11.0, y=1090, pics=['thought_balloon', 'boxing_glove'], tag='ولسه المصارعة في دماغه', c='#FF6B5A')])),
        dict(a=804.5, b=816.25, raw=True, crop=WRS, labels=[('الموسل', 'وهو ماشي بضهره بس', 'eyes'), ('الساوند', 'Sound track', 'musical_note'), ('الحلبة', 'صوت الحلبة', 'loudspeaker')]),
        dict(a=861.9, b=880.8, show='IdeaRows', anim=dict(rows=[
            dict(at=0.3, y=470, pics=['musical_note', 'up_arrow'], tag='الموسيقى بتعلى.. كأنه داخل الحلبة'),
            dict(at=6.6, y=780, pics=['shopping_cart', 'muted_speaker'], tag='وتقف فجأة: ده السوبر ماركت', c='#FF6B5A'),
            dict(at=10.0, y=1090, pics=['performing_arts', 'cross_mark'], tag='من غير ما الممثل يمثل', c='#8B5CF6')])),
        dict(a=882.4, b=897.5, src=886.0, crop=RB, labels=[('المصارع', 'بيتبهدل وبيخسر', 'boxing_glove'), ('الكاميرا', 'الكاميرا مكانه', 'video_camera')]),
        dict(a=904.1, b=912.5, src=897.6, crop=RB, labels=[('يحسسني', 'شايف إيه؟', 'eyes'), ('سامع', 'وسامع إيه؟', 'ear')]),
        dict(a=912.5, b=919.1, raw=True, crop=RB, film=F_RB),
        dict(a=919.15, b=932.3, raw=True, crop=RB, labels=[('سكوت', 'سكوت تام', 'muted_speaker'), ('الجمهور', 'صوت الجمهور اختفى', 'speaker_high_volume')]),
        dict(a=932.3, b=946.3, raw=True, crop=RB, lab=[(1.0, 'اسمع اللي هو سامعه', 'ear', 3.0)]),
        dict(a=946.3, b=961.3, raw=True, crop=RB, labels=[('الفلاش', 'فلاش الكاميرا', 'camera_with_flash'), ('اللاكمات', 'صوت اللكمات', 'oncoming_fist'), ('المعلق', 'والمعلق.. اتشالوا', 'microphone')]),
    ]),
}

CAP = {
    3: ['',
        'الموسيقى ممكن تستخدم كنوع من الكوميديا.. زي مثلا في الفيلم ده.. اللي هو بتاع ميكي وبطوط وبندق',
        'هنا فيه مثلا نوع.. اللقطة موسيقى بتتعاد كذا مرة كنوع من الكوميديا.. كل ما يقول كلمة أوبرا',
        '',
        'فالرسالة هنا وصلت.. يعني هو خلاها كنوع من الكوميديا',
        'الموسيقى كمان ممكن توصل معنى.. زي مثلا اللقطة دي من فيلم.. المفروض إن الراجل ده هدفه إنه يبقى مشهور وكوميديان ومهتم قوي بالشهرة قوي',
        'فهنا بقى بيورينا بعض من التفكير اللي عنده في دماغه.. بيورينا هو بيفكر إزاي من جوه.. فبيورينا إنه في البيت بتاعه لوحده.. وبيكلم صور موجودة.. وبيخلينا بقى نسمع اللي هو سامعه في ودانه',
        '',
        'ممكن تقلب برعب شوية.. بس يعني هو هنا محسسنا بإنه مهووس قد إيه بالشهرة وبإنه يضحك الناس'],
    4: ['',
        'هنا الفيلم ده بيتكلم عن المصارع.. المصارع ده استقال وخلاص بطل المصارعة عشان يكسب فلوس.. فجايبنا بقى بيورينا إحساس إنه دلوقتي شغال في السوبر ماركت.. لسه في دماغه إنه حابب المصارعة.. عايز يروح للمصارعة ومتضايق إنه في السوبر ماركت',
        'كل ده حسيناه وهو ماشي بضهره بس.. عشان الموسيقى.. عشان وزّع الساوند تراك اللي شغال.. أو الساوند إفكتس اللي شغالة.. هنكون سامعين صوت الحلبة.. وبصوا',
        'سمعتوا؟ خدتوا بالكم التغيير اللي حصل؟ الموسيقى بتاعتها هتعلى هتعلى هتعلى.. كأنه داخل الحلبة.. وبعد كده وقفت فجأة إنه داخل السوبر ماركت.. فنقل لنا الإحساس بتاعه كله.. من غير ما الممثل يمثل.. وصل لنا كل المشاعر.. إنه دلوقتي متضايق ونفسه يرجع المصارعة',
        'وهنا برضو.. في الفيلم ده المشهور جدا.. الراجل عايز يورينا المصارع وهو بيتبهدل.. وهو خلاص بيخسر.. المنظور بتاعه.. فمش بس حط الكاميرا مكانه عشان يورينا المنظور بتاعه',
        'فهتلاقوا إنه استخدم برضه تكنيكس في الساوند إفكت.. عشان يحسسني مش بس الراجل ده شايف إيه.. الراجل ده سامع إيه.. فبصوا لما الراجل مثلا هنا',
        '',
        'سكوت تام.. هو مش سامع أي حاجة.. غير بس شوية حاجات.. كانت الدنيا دوشة في الأول.. وبعد كده لغى صوت الجمهور.. فحاسسك إنه مش مركز مع الجمهور أصلا',
        '',
        'كل اللي هو سامعه.. صوت الفلاش بتاع الكاميرا وهي بتصوره.. وصوت الناس وهي بتخضه.. صوت اللكمات.. فهنا بيحسسني أكتر باللي هو فيه.. بدل ما كان شغال بصوت الجمهور واحنا سامعينه عادي في الأول.. وصوت المعلق.. وقف الاتنين مع بعض'],
}

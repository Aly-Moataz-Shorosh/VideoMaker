# Shorts from the film-making course (plan: خطة_الشورتس.md, Aly 2026-11-06: every short complete on its own). Key = number in the
# plan = course order. Source = the 1280x720 30 fps proxy of the course (public projects/filmcourse/course.mp4), same timeline.
# piece: a/b = his sentence (source s, fitted on the waveform), show = 'screen' (crop + zoom keys in 1280x720 space) | scene name |
# 'big:line|sub'; scene props 'anim' (times in SOURCE seconds -> moved to the piece); under = scene on top + the clip pane under it;
# labels (word, text[, fluent]); lab (offset, text, fluent, dur); kw (EN, AR, offset); film = FilmTag; rew = '⏪' label (after the hook).
TOTAL = 20
URL = 'https://youtu.be/S-tSUtClTOg'
END_D = 4.5

# 05 — crops on his setup slides (slide 18 at 776-820, 19 at 821-830, 20 at 830-842, 21 at 842-)
ROOM = dict(sx=600, sy=80, sw=560)          # tall photo: the scarf hung on the bunk-bed ladder + the chair with the camera box
SCARF = dict(sx=700, sy=150, sw=330)        # the green scarf
CHAIR = dict(sx=780, sy=170, sw=380)        # chair + box + old camera
BUNK = dict(sx=60, sy=20, sw=540)           # under the upper bed (scarf behind)
RESULT = dict(sx=100, sy=300, sw=500)       # him in front of the green scarf (result)
ROOF = dict(sx=520, sy=0, sw=640)           # the green cloth on the roof
AE = dict(sx=640, sy=350, sw=440)           # the Harry Potter motion graphics video in After Effects
STUDIO_L = dict(sx=80, sy=120, sw=590)      # home studio photo 1
STUDIO_R = dict(sx=680, sy=40, sw=540)      # home studio photo 2
TABLET = dict(sx=120, sy=170, sw=560)       # with the tablet + ring light
# 15 — his angle notes + example sheets
NOTES = dict(sx=360, sy=120, sw=560)
NOTES_Z = dict(sx=360, sy=220, sw=300)      # eye level / dutch / low angle / high angle lines
GRID = dict(sx=10, sy=90, sw=860)
OVERHEAD = dict(sx=0, sy=330, sw=440)
DUTCH = dict(sx=690, sy=20, sw=590)
GROUND = dict(sx=840, sy=200, sw=430)
# 20 — the film clip window (Movies & TV player, 640x480 file shown at 213..1066 x 170..533)
HP = dict(sx=205, sy=175, sw=870)

# his webcam square in the recording (1280x720): bigger box in the slides part (until ~1500 s), smaller later; square around his face
def webcam(a):
    return dict(sx=1065, sy=558, s=160) if a < 1500 else dict(sx=1085, sy=590, s=130)

ST = lambda *k: [list(x) for x in k]
HP_STEPS = ST((4580, 0, 2), (4611.9, 0, 2), (4617.2, 3, 2), (4623.1, 3, 4), (4628.5, 5, 4), (4630.0, 4, 5), (4631.3, 5, 5), (4661.5, 5, 5),
              (4662.1, 5, 2), (4665.2, 5, 2), (4666.0, 5, 2))
HP_TAGS = [dict(t=4589.7, text='إزاي تنقل السلطة بالكاميرا؟'), dict(t=4611.9, text='الأطول = السلطة الأعلى'), dict(t=4617.2, text='طلعت سلمة.. السلطة معاها'),
           dict(t=4623.1, text='طلعت سلمة أعلى.. السلطة اتنقلت'), dict(t=4627.1, text='حرب.. رايحة جاية'), dict(t=4659.2, text='الكلمة القاضية', c='#E5232B'),
           dict(t=4662.0, text='نزلت سلمة..', c='#E5232B'), dict(t=4665.2, text='والسلطة بقت معاها'), dict(t=4670.1, text='Push in + Zoom'), dict(t=4673.3, text='والتانية خرجت من الكادر')]
HP_ANIM = dict(steps=HP_STEPS, tags=HP_TAGS, outB=4673.3)
HPF = dict(title='Harry Potter and the Order of the Phoenix', year='2007', note='المشهد اللي عرضه في الكورس')

SHORTS = {
    5: dict(no=5, chapter=8, title='كروما من *طرحة أمي*', pieces=[
        dict(a=814.0, b=820.2, crop=RESULT, lab=[(0.2, 'النتيجة', 'clapper_board', 2.4)]),
        dict(a=767.24, b=781.27, show='big:الأدوات بتساعدك بس|متبقاش مقيد بيها.. انت ممكن تعمل أي حاجة', ico='clap', rew=True),
        dict(a=781.77, b=794.41, crop=ROOM, zoom=[(785.2, SCARF)], labels=[('طرحة', 'طرحة أمي'), ('السلم', 'وراها طرحة تانية')]),
        dict(a=794.41, b=804.87, crop=BUNK, labels=[('السرير', 'سلم السرير اللي فوق')]),
        dict(a=804.92, b=813.6, crop=ROOM, zoom=[(808.2, CHAIR)], labels=[('كورسي', 'كرسي + علبة جزمة'), ('كاميرا', 'كاميرا قديمة جدا')]),
        dict(a=814.0, b=820.2, crop=RESULT, labels=[('كروب', 'Crop')]),
        dict(a=820.9, b=829.9, crop=ROOF, zoom=[(824.6, AE)], labels=[('هاري', 'فيديو هاري بوتر')]),
        dict(a=830.7, b=840.4, crop=STUDIO_L, zoom=[(834.9, STUDIO_R)], labels=[('استوديو', 'استوديو + مايك'), ('سنتر', 'Journey to the center')]),
        dict(a=840.4, b=845.73, crop=STUDIO_R, zoom=[(842.4, TABLET)], labels=[('التابلت', 'تابلت')]),
        dict(a=847.54, b=855.62, show='ToolsLadder', anim=dict(title='أدواتك بتتغير.. الغاية لأ', titleAt=4.6, items=[
            dict(img='projects/filmcourse/stills/setup_bunk.jpg', text='سلم السرير', at=0.1), dict(img='projects/filmcourse/stills/setup_result.jpg', text='طرحة أمي', at=0.6),
            dict(img='projects/filmcourse/stills/setup_roof.jpg', text='السطح', at=1.1), dict(img='projects/filmcourse/stills/setup_studio.jpg', text='استوديو', at=1.6),
            dict(img='projects/filmcourse/stills/setup_tablet.jpg', text='تابلت', at=2.1)])),
    ]),
    15: dict(no=15, chapter=24, title='زاوية الكاميرا بتغير *المعنى*', pieces=[
        dict(a=3111.01, b=3117.47, show='AngleScene', anim=dict(modes=[[3111.0, 0], [3112.6, -1]], tags=[dict(t=3112.8, text='هو فوق.. واحنا تحت', c='#E5232B'), dict(t=3114.3, text='= نظرة استعلاء', c='#E5232B')])),
        dict(a=3090.74, b=3102.58, crop=NOTES, zoom=[(3096.5, NOTES_Z)], kw=[('Camera angle', 'زاوية الكاميرا', 1.2)], rew=True),
        dict(a=3102.92, b=3110.68, show='AngleScene', anim=dict(modes=[[3102.9, 0], [3104.9, 1]], tags=[dict(t=3105.0, text='الكاميرا فوق.. بنبصله من فوق', c='#3BA9F5'), dict(t=3107.4, text='فمش بيحسسك إنه بيعلّمك من فوق', c='#3BA9F5')])),
        dict(a=3111.01, b=3120.2, show='AngleScene', anim=dict(modes=[[3111.0, 1], [3112.6, -1]], tags=[dict(t=3112.8, text='لو هو اللي بيبصلنا من فوق', c='#E5232B'), dict(t=3114.3, text='= نظرة استعلاء.. مش هنحبها', c='#E5232B')]), cin=True),
        dict(a=3123.07, b=3132.67, crop=GRID, zoom=[(3128.9, OVERHEAD)], kw=[('Overhead shot', 'من فوق خالص: بيورينا المكان', 6.0)]),
        dict(a=3133.92, b=3144.84, crop=DUTCH, kw=[('Dutch angle', 'كادر مايل: توهان وقلق', 1.2)]),
        dict(a=3144.84, b=3151.77, crop=GROUND, kw=[('Ground level', 'من الأرض: مين اللي جاي؟', 0.4)]),
        dict(a=3219.44, b=3224.72, show='big:الزاوية بتفرق في المعنى|كل زاوية بتديك إحساس', ico='cam'),
    ]),
    20: dict(no=20, chapter=30, title='نزلت سلمة.. *وطلعت سلمة*', pieces=[
        dict(a=4616.19, b=4625.93, crop=HP, under=True, anim=HP_ANIM, film=HPF),
        dict(a=4583.71, b=4600.02, crop=HP, under=True, anim=HP_ANIM, rew=True, film=HPF),
        dict(a=4603.92, b=4615.5, crop=HP, under=True, anim=HP_ANIM),
        dict(a=4616.19, b=4631.77, crop=HP, under=True, anim=HP_ANIM),
        dict(a=4659.23, b=4678.59, crop=HP, under=True, anim=HP_ANIM),
    ]),
}

CAP = {5: ['عشان أقدر أطلع الكواليتي دي.. عملت كروب وقصيت نفسي.. فما فيش عذر خالص للأدوات', 'انت اللي بتعمل الموفي.. والتولز دي هي بتساعدك.. فما تبقاش بتحاول تمسك التول قبل ما تفكر في حاجة.. وما تبقاش مقيد بالتول دي ممكن تعملك إيه.. لأن انت ممكن تعمل أي حاجة', 'أنا كانت عندي كروما مثلا وأنا صغير.. ولما كنت عايز أعمل فيديوهات جبت طرحة بتاعة أمي.. وهي طرحة أصلا شفافة بس خضرا شوية.. فجبتها والطرحة دي حطيت وراها طرحة تانية سودا', 'ده من كتير قوي.. مش عارف، 15 سنة مثلا.. وطلعت سلم السرير اللي فوق وسندت عليه', 'وعشان أقدر أعمل كروما صغيرة.. وما عنديش استاند.. فجبت كرسي.. وعليه علبة الجزمة.. وحطيت فيها كاميرا قديمة جدا بتصور', 'عشان أقدر أطلع الكواليتي دي.. عملت كروب وقصيت نفسي.. فما فيش عذر خالص للأدوات', 'بعد كده اتطورت شوية.. وقعدت أصور بيها.. وعملت فيديو الموشن جرافيك بتاع هاري بوتر.. اللي اتكلمت عليه في الفيديو بتاعه', 'بعد كده اتطورت شوية.. وعندي استوديو.. وبقيت أصور بمايك والحاجات دي كلها.. وده كان الفيديو اللي هو الانترودكشن لمشروع Journey_to_the_Center', 'بعد كده اتطورت أكتر.. ومثلا ده فيديو جه في التابلت.. الكواليتي بقت تتحسن', 'فأدواتك بتتغير.. ففي الفيلم ميكينج زمان أدواتهم كانت مختلفة.. ودلوقتي مختلفة.. فالمهم في الآخر الغاية اللي احنا عايزين نعملها'], 15: ['لو انت الدحيح.. وبرضه هو بيبص لنا من فوق واحنا تحت.. هنحس بنظرة استعلاء.. هنحس بنظرة مش هنحبها', 'كاميرا أنجل بقى.. زاوية الكاميرا برضه بتحكي قصة.. بتوصل معنى.. لما تكون بتبص لي في عيني مختلف.. عن لما تكون بتبص لي من تحت.. مختلف عن من فوق.. يعني مثلا الدحيح', 'لو خدت بالك الدحيح دايما.. احنا الأنجل اللي فوق.. بنبص له من فوق.. علشان ما يحسسكش إن أنا بديك معلومة وبعرّفك وبعلّمك', 'لو انت الدحيح.. وبرضه هو بيبص لنا من فوق واحنا تحت.. هنحس بنظرة استعلاء.. هنحس بنظرة مش هنحبها.. فمش هننبسط بالفيديو.. بس النظرة دي حلوة', 'فالزاوية بتفرق في المعنى.. خلينا نشوف أمثلة.. عندنا مثلا الـ Overhead_shot.. بتورينا شكل المكان', 'الـ Dutch_angle حسسنا بتوهان.. بقلق.. بتوتر.. الدنيا مش مريحة.. فكل Angle بيدي لنا إحساس', 'الـ Ground_level مثلا ده.. بيورينا مين الشخص اللي جاي ده.. وهكذا', 'فالزوايا بتخلينا نحس.. فدي تبقى التكوينة بتاعة الأنجلز'], 20: ['بعد كده دي طلعت سلمة.. فعرفنا إن دي سلطتها الأعلى دلوقتي.. وجايب لنا كادر تاني.. بعد كده دي طلعت سلمة أعلى.. ويورينا السلطة اتنقلت لدي', 'هنا الفيديو ده بيبين لنا حاجة جميلة قوي.. عايز يورينا بلغة السينما والفيجوال.. إزاي تنقل السلطة.. دي المفروض كانت ماسكة هوجورتس أكتر.. وبعد كده دي جت دلوقتي.. وبقت سلطتها أعلى.. فهيجي لنا المشهد ده إزاي', 'الناس كلها بتبص.. وجايب لنا هنا طبعا دي أطول.. فهي ليها السلطة الأعلى', 'بعد كده دي طلعت سلمة.. فعرفنا إن دي سلطتها الأعلى دلوقتي.. وجايب لنا كادر تاني.. بعد كده دي طلعت سلمة أعلى.. ويورينا السلطة اتنقلت لدي.. نقاش.. حرب رايحة جاية', 'بص بقى هنا الكلمة القاضية.. فدي اللي نزلت.. وبعد كده طلعت.. فالسلطة بقت معاها.. اعمل لي بقى يا باشا Push بالكاميرا وزوم.. وعلّي الموسيقى.. وشيل الست التانية من الكادر.. سينما بقى.. هي دي القوة']}  # hand-corrected captions per piece (after caption_words.py); empty = his re-transcribed words

"""Shorts 31–34 (Aly 2026-10-19: "اعمل الأفكار الأربعة كلها") — the lecture parts no other short used (no speech repeated).
31 CS jobs change vs engineering · 32 who I am (180 ten years ago, colourist) · 33 the 3 names: Digital Art / Graphics · 34 Q&A OpenAI."""

H = {'_hook': True}
CARD = {'n': 6, 'sx': 30, 'sy': 115, 'sw': 400, 'w': 560, 'h': 700}   # his card 1: BLACK & WHITE VIDEO COLORIST

NEW = {
    31: dict(
        slug='cs_jobs_change', head='شغلانتك مش مضمونة *السنة_الجاية*',
        hook=(309.7, 318.65),
        pieces=[(304.8, 339.2), (340.6, 357.2)],
        cues=[
            (309.7, 'big', {'text': 'ضامن شغلانتك *كمان_5_سنين*؟', 'top': 'hourglass_not_done', **H}, {}),
            (316.9, 'big', {'text': 'مش ضامنها *السنة_الجاية*', 'top': 'tear-off_calendar', **H}, {}),
            (304.8, 'slide', {'n': 4, 'sx': 0, 'sy': 0, 'sw': 1000, 'w': 940, 'h': 700, 'label': 'كل حاجة بتتغير'}, {}),
            (312.8, 'flow', {'items': [{'e': 'gear', 't': 'Back End'}, {'e': 'desktop_computer', 't': 'Front End'}, {'e': 'man_technologist', 't': 'أيًا كان'}]},
             {'s0': 313.4, 's1': 313.8, 's2': 314.4}),
            (316.9, 'big', {'text': 'مش ضامنها *السنة_الجاية*', 'top': 'tear-off_calendar'}, {}),
            (320.6, 'hero', {'e': 'robot', 't': 'طريقة الشغل بتتغير جدًا', 'sub': 'خاصة بعد الـ AI'}, {}),
            (325.7, 'vs', {'a': {'e': 'laptop', 't': 'حاسبات', 'sub': 'بتتغير كل سنة'}, 'b2': {'e': 'building_construction', 't': 'هندسة', 'sub': 'علم ثابت'}},
             {'a': 325.9, 'b': 326.6}),
            (328.9, 'flow', {'items': [{'e': 'gear', 't': 'ميكانيكا'}, {'e': 'classical_building', 't': 'عمارة'}]}, {'s0': 329.2, 's1': 334.7}),
            (337.6, 'big', {'text': 'علم *بقاله_سنين*', 'top': 'books'}, {}),
            (345.9, 'hero', {'e': 'construction_worker', 't': 'المهندس المدني = الجوكر', 'sub': 'أكتر حد بيعرف كل حاجة'}, {}),
            (353.5, 'big', {'text': 'اسأل أي حد باباه *مهندس*', 'top': 'man_construction_worker'}, {}),
        ],
    ),
    32: dict(
        slug='ten_years_180', head='من 10 سنين كنت *طالب* هنا',
        hook=(427.7, 436.35),
        pieces=[(391.1, 398.9), (402.2, 410.45), (422.5, 449.45)],
        cues=[
            (427.7, 'count', {'to': 10, 't': 'سنين من New Stage 9', 'to2': 8, 't2': 'سنين بقدّم السيشن دي', **H}, {'go': 429.0, 'go2': 431.8}),
            (433.5, 'big', {'text': 'فرقت في حياتي *جدًا_جدًا*', 'top': 'red_heart', **H}, {}),
            (391.1, 'hero', {'e': 'man_technologist', 't': 'عايز تبقى Back End؟', 'sub': 'تعرف موبايل وAI ومش عارف إيه؟'}, {}),
            (397.6, 'big', {'text': 'لأ.. *جرّب*', 'top': 'test_tube'}, {}),
            (402.2, 'flow', {'items': [{'e': 'gear', 't': 'Back End'}, {'e': 'desktop_computer', 't': 'Front End'}, {'e': 'sparkles', 't': 'كل حاجة'}]},
             {'s0': 404.3, 's1': 405.6, 's2': 408.2}),
            (409.0, 'big', {'text': 'أيام الكلية و*بعد* الكلية', 'top': 'graduation_cap'}, {}),
            (422.5, 'slide', {'n': 6, 'w': 1000, 'label': 'أنا مين؟'}, {}),
            (425.2, 'big', {'text': 'خريج *حاسبات* ومعلومات', 'top': 'graduation_cap'}, {}),
            (427.7, 'count', {'to': 10, 't': 'سنين من New Stage 9', 'to2': 8, 't2': 'سنين بقدّم السيشن دي'}, {'go': 429.0, 'go2': 431.8}),
            (433.5, 'big', {'text': 'فرقت في حياتي *جدًا_جدًا*', 'top': 'red_heart'}, {}),
            (437.2, 'list', {'title': 'اشتغلت في:', 'items': [{'e': 'artist_palette', 't': 'Graphic Design'}, {'e': 'film_frames', 't': 'Motion Graphics'},
                                                          {'e': 'video_camera', 't': 'Video'}]}, {'r0': 438.1, 'r1': 438.8, 'r2': 439.6}),
            (440.4, 'slide', {**CARD, 'label': 'تلوين الأبيض والأسود'}, {}),
            (444.7, 'big', {'text': 'جرّبت حاجات *كتير*', 'top': 'test_tube'}, {}),
            (446.4, 'big', {'text': 'فأقدر أقولكم عن الـ *Digital_Art*', 'top': 'artist_palette'}, {}),
        ],
    ),
    33: dict(
        slug='digital_art_graphics_names', head='يعني إيه *Digital_Art* و Graphics؟',
        hook=(202.2, 208.25),
        pieces=[(188.1, 209.3), (451.2, 454.4), (458.1, 471.2, 'x'), (471.25, 475.35, 'x'), (485.5, 491.1), (622.6, 630.0), (635.1, 657.95)],
        cues=[
            (202.2, 'slide', {'n': 2, 'w': 1000, 'label': 'تلات أسامي', **H}, {}),
            (188.1, 'flow', {'items': [{'e': 'artist_palette', 't': 'Digital Art'}, {'e': 'desktop_computer', 't': 'Computer Graphics'}, {'e': 'film_frames', 't': 'Multimedia'}]},
             {'s0': 189.3, 's1': 192.3, 's2': 193.5}),
            (194.1, 'big', {'text': 'أقسام ومواد *بالأسامي* دي', 'top': 'books'}, {}),
            (202.2, 'big', {'text': '*Digital_Art* = أشمل كلمة', 'top': 'bullseye'}, {}),
            (451.2, 'slide', {'n': 2, 'w': 1000, 'label': 'نعرفهم واحد واحد'}, {}),
            (458.1, 'big', {'text': '*Digital* = رقمي', 'top': 'input_numbers'}, {}),
            (464.4, 'hero', {'e': 'desktop_computer', 't': 'أي حاجة زي الكمبيوتر', 'sub': 'رقمية'}, {}),
            (471.3, 'slide', {'n': 8, 'w': 1000, 'label': 'يعني إيه Art؟'}, {}),
            (485.5, 'big', {'text': 'الفن = إزاي الإنسان *يعبّر* عن نفسه', 'top': 'artist_palette'}, {}),
            (622.6, 'big', {'text': 'يعني إيه *Graphics*؟', 'top': 'thinking_face'}, {}),
            (635.1, 'slide', {'n': 13, 'w': 1000, 'label': 'Graphics = رسومات'}, {}),
            (648.9, 'list', {'title': 'رسومات يعني:', 'items': [{'e': 'writing_hand', 't': 'مرسومة باليد'}, {'e': 'camera', 't': 'الصورة المتصورة'},
                                                              {'e': 'triangular_ruler', 't': 'الخطوط والأشكال'}]}, {'r0': 650.0, 'r1': 651.6, 'r2': 653.3}),
            (654.8, 'big', {'text': 'التعريف اللفظي: *رسومات*', 'top': 'open_book'}, {}),
        ],
    ),
    34: dict(
        slug='openai_egyptian_grad', head='إزاي مصري يشتغل في *OpenAI*؟',
        hook=(3104.3, 3109.25),
        pieces=[(3086.0, 3109.25)],
        cues=[
            (3104.3, 'big', {'text': 'من قال لا أعلم *فقد_أفتى*', 'top': 'open_book', **H}, {}),
            (3086.0, 'slide', {'n': 133, 'w': 1000, 'label': 'أسئلة؟'}, {}),
            (3087.3, 'flow', {'items': [{'e': 'logo:openai', 't': 'OpenAI'}, {'e': 'logo:claude', 't': 'Anthropic'}, {'e': 'graduation_cap', 't': 'خريج جامعة مصرية'}]},
             {'s0': 3088.7, 's1': 3089.4, 's2': 3090.8}),
            (3093.2, 'big', {'text': '*معرفش* صراحة', 'top': 'person_shrugging'}, {}),
            (3095.7, 'hero', {'e': 'thinking_face', 't': 'اللي يجاوبك = اللي وصل لكده', 'sub': 'أنا هجاوبك بتوقّع من خبرتي'}, {}),
            (3104.3, 'big', {'text': 'من قال لا أعلم *فقد_أفتى*', 'top': 'open_book'}, {}),
            (3108.7, 'big', {'text': 'بس أكيد فيه *طريقة*', 'top': 'rocket'}, {}),
        ],
    ),
}


def add(shorts):
    shorts.update(NEW)

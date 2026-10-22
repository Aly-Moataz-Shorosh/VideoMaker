"""The programs video (playlist 37) -> shorts 41, 42, 43, 45, 46, 47, 48 (44 = the hand-made 3D one).
HIS tree motion (the whole frame: his real program logos) + program names popping under it on his words; my branch scene opens
each category (as in the approved short 44). Times = seconds in his video."""
from shorts_data import SHORTS as _S

FULL = [0, 0, 1920, 1080]
FIX = dict(_S[44]['WFIX'])
FIX.update({'Homosexual': 'GIMP', 'Gameฮer': '--', 'Roe': 'RawTherapee', 'Serapy': '--', 'Creta': 'Krita', 'reci': 'Serif', 'celebrity': '--',
            'الحكومته': 'الكمبوزيتنج', 'الم': '--', 'Shaping': 'الكمبوزيتنج', 'ادوي': 'أدوبي', 'كاث': 'كاتيجوريز', 'hagورج': '--', 'معتازة': 'معتز',
            'اداسيتي': 'Audacity', 'اداستيه': 'Audacity', 'اوديشن': 'Audition', 'تماستر': 'تعمل ماستر', 'الليها': 'اللي', 'اكس': 'XD', 'دي': 'دي',
            'سكيتش': 'Sketch', 'سكريباس': 'Scribus', 'Ink': 'Inkscape', 'Space': '--', 'دافنجي': 'DaVinci', 'ريزولب': 'Resolve', 'بوزدينج': 'كمبوزيتنج',
            'فيوجين': 'Fusion', 'نيوك': 'Nuke', 'ناترون': 'Natron', 'توم': 'Toon', 'هارموني': 'Boom Harmony', 'موهو': 'Moho', 'وأوبنتونز': 'وOpenToonz',
            'وسكيتش': 'وSketchBook', 'لألترنتيفز': 'ليه Alternatives', 'موكا': 'Mocha', 'بهانس': 'Behance', 'ريدت': 'Reddit', 'مرجز': 'مركز',
            'المسروع': 'المشروع', 'تفنيت': 'تفنيد', 'مهتز': 'معتز', 'Rights': '--', 'dis': '--', 'skinny': '--', 'Aqua': '--', 'العموارة': 'العمارة',
            'علعاب': 'ألعاب', 'كلر': 'كلر', 'المكبس': 'الماك', 'منتاج': 'مونتاج', 'بالمنتاج': 'بالمونتاج', 'المنتاج': 'المونتاج', 'دوت': 'ده'})


def P(n, label, slug, pieces, scenes):
    return n, dict(ep='37', sec='prog', label=label, vid_title='كل برامج الجرافيكس و ازاي تختار البرنامج اللي محتاجوا', slug=slug, pieces=pieces,
                   scenes=scenes, WFIX=FIX, real=[])


def clip(at, title, chips):
    return dict(t='jy_clip', at=at, src='src_37.mp4', box=FULL, title=title, sec='prog', chips=[dict(t=t, text=x) for t, x in chips])


PROG = dict([
    P(41, 'أنواعها + الصوت', 'programs_audio', [(0.9, 77.5)], [
        clip(0.7, 'كل برامج الجرافيكس', [(4.1, '🧭 تختار البرنامج اللي محتاجه'), (18.2, '💻 Software Applications')]),
        clip(23.0, 'General ولا Special؟', [(25.5, '🧰 General Purpose = وظايف كتير'), (28.0, '🎯 Special Purpose = وظيفة معينة'), (36.5, '🆕 كل يوم برنامج جديد'), (41.0, '🗺️ خريطة لكل البرامج')]),
        dict(t='p3_branch', at=46.6, on=0, say='نبدأ بالصوت 🎧', b=dict(d3=55.5)),
        clip(56.4, 'برامج الصوت', [(60.2, '🎧 Adobe Audition'), (61.0, '🆓 Audacity = Open Source'), (68.5, '🎚️ ماستر للصوت'), (71.9, '✨ إفكتات على الصوت')]),
    ]),
    P(42, 'الصور Pixel', 'programs_pixel', [(78.1, 139.5)], [
        dict(t='p3_branch', at=78.0, on=1, say='نروح للصور 🖼️', b=dict(d3=78.4)),
        clip(80.0, 'Pixel Based ولا Vector Based؟', [(81.0, '🟥 Pixel Based'), (82.5, '✒️ Vector Based'), (91.3, '🧩 Compositing • ✂️ Editing • ✏️ Drawing')]),
        clip(107.0, 'برامج الـ Pixel', [(108.5, 'Adobe Photoshop'), (111.8, 'Affinity Photo'), (114.5, '🆓 GIMP = Open Source'), (120.6, 'Adobe Lightroom'),
                                        (123.0, '🆓 RawTherapee'), (131.0, '✏️ Paint • Krita')]),
    ]),
    P(43, 'الصور Vector', 'programs_vector', [(139.6, 198.4)], [
        clip(139.5, 'برامج الـ Vector', [(147.9, '🖥️ UI / UX'), (153.8, '📰 النشر واللياوت'), (155.5, '✒️ الإليستريشن')]),
        clip(158.5, 'UI / UX', [(159.4, 'Adobe XD'), (163.0, 'Sketch')]),
        clip(164.5, 'النشر واللياوت', [(167.8, 'Adobe InDesign'), (169.0, '🆓 Scribus'), (171.9, 'MS Publisher • Affinity Publisher'), (175.0, '📰 جرايد • 📚 كتب • 📄 PDF')]),
        clip(180.0, 'الإليستريشن', [(186.0, 'Adobe Illustrator'), (194.0, '🆓 Inkscape'), (196.5, 'Affinity Designer')]),
    ]),
    P(45, 'الفيديو', 'programs_video', [(271.3, 350.7)], [
        dict(t='p3_branch', at=271.1, on=3, say='ننقل للفيديو 🎬', b=dict(d3=272.3)),
        clip(274.0, 'برامج الفيديو', [(276.0, '✂️ مونتاج'), (278.5, '🧩 كمبوزيتنج وموشن'), (281.4, '🎬 أنيميشن')]),
        clip(282.5, 'المونتاج', [(286.0, 'Adobe Premiere Pro'), (291.0, 'DaVinci Resolve'), (294.0, '🎨 الأقوى في الألوان'), (303.1, 'Final Cut Pro (ماك)'),
                                 (307.3, 'Premiere Rush (بسيط)')]),
        clip(315.0, 'كمبوزيتنج وموشن جرافيك', [(319.4, 'Adobe After Effects'), (328.5, '⭐ الأفضل للموشن جرافيك'), (331.5, 'Fusion'), (336.5, 'Nuke'),
                                               (342.8, '🆓 Natron')]),
    ]),
    P(46, 'الأنيميشن والمتخصصة', 'programs_animation', [(350.8, 462.6)], [
        clip(350.7, 'برامج الأنيميشن', [(361.0, 'Adobe Animate (كان Flash)'), (372.1, 'Toon Boom Harmony'), (378.0, 'Moho'), (380.7, 'TV Paint • OpenToonz • SketchBook')]),
        clip(392.9, 'برامج متخصصة', [(406.0, 'Character Animator'), (414.3, 'Substance Designer & Painter'), (424.1, 'Adobe Media Encoder'), (433.0, 'Adobe Fuse'),
                                     (441.4, 'AutoCAD • SketchUp'), (457.0, 'Mocha Pro')]),
    ]),
    P(47, 'كل مجال وبرامجه', 'programs_by_field', [(462.6, 605.0)], [
        clip(462.4, 'كل مجال محتاج برامج ايه؟', [(479.3, '🔀 البرنامج الواحد في أكتر من مجال'), (502.7, '🎵 صوت • ✏️ رسم • 🎬 تحريك • 🧊 3D'), (510.8, '✨ VFX'),
                                                (518.9, '✏️ 2D Animation'), (523.6, '🧊 3D Animation'), (527.5, '🏷️ براندينج'), (536.6, '🎨 جرافيك ديزاين'),
                                                (545.7, '🏛️ عمارة'), (553.1, '🎮 ألعاب')]),
        clip(572.6, 'إزاي تعرف برامج مجالك؟', [(576.3, '🔍 Behance: البرامج تحت كل شغل'), (585.8, '👥 جروبات فيسبوك'), (594.2, '💬 Reddit'), (602.6, '🔎 Google • YouTube')]),
    ]),
    P(48, 'ختام الرحلة', 'journey_end', [(611.7, 720.8)], [
        clip(611.5, 'رحلة إلى مركز الجرافيكس', [(616.5, '🏁 خلصنا مرحلة البرامج'), (620.9, '🗺️ الصورة الكبيرة للجرافيكس'), (630.4, '🚶 تكمل لوحدك بعد كده')]),
        dict(t='p_map', at=638.1, b=dict(one=641.0, two=654.6, three=687.9, share=706.9)),
    ]),
])

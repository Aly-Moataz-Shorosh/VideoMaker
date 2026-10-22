"""Journey series shorts (2026-10-22). Pilot = 8 (هو ايه | vectors), 33 (خيال المآتة), 44 (برامج الـ 3D).
Times = seconds in HIS source video `ep`. pieces = (first word start, last word start) fitted on the waveform.
scenes: t = scene id (motion-library/src/journey/*), at = source second it starts, b = {beat: source second} -> scene frames.
WFIX = caption word fixes (Whisper word -> his word; '--' = hide an unsure word)."""

PLAYLIST = 'https://youtube.com/playlist?list=PL--cO7twoKgnrn0J1tzEAb8JPbFJCa8kv'
PL_NAME = 'رحلة إلى مركز الجرافيكس'

# ---- REAL pictures over the motion (Aly review 2026-10-22). t / until = source seconds of his video ----
def C(src, t, until, x, y, w, label=None, **kw):  # circle
    d = dict(src=src, t=t, until=until, x=x, y=y, w=w, shape='circle', **kw)
    if label: d['label'] = label
    return d


def K(src, t, until, x, y, w, h, label=None, **kw):  # card
    d = dict(src=src, t=t, until=until, x=x, y=y, w=w, h=h, shape='card', **kw)
    if label: d['label'] = label
    return d


REAL = {
    8: [C('his_photo_face.jpg', 8.8, 13.4, 120, 960, 230, 'صورة حقيقية'),
        C('his_photo_pix1.png', 10.7, 13.4, 960, 960, 230, 'مكبّرة: مربعات'),
        C('his_photo_pix2.png', 15.0, 18.0, 960, 1000, 250, 'كبّرتها أكتر'),
        K('c_billboard.jpg', 32.9, 37.3, 280, 1150, 430, 286, 'إعلان في الشارع'),
        K('his_tshirt.jpg', 34.6, 37.3, 800, 1150, 410, 286, 'تيشيرت من شغل علي'),
        C('his_cartoon.png', 50.8, 52.5, 870, 500, 210, 'Vector من شغل علي', fit='contain', bg='#fff'),
        K('his_manip.jpg', 62.7, 64.0, 540, 850, 780, 410, 'صورة فوتوغرافية من شغل علي'),
        C('his_cartoon_full.png', 67.6, 72.3, 870, 500, 210, 'رسمة Vector لعلي', fit='contain', bg='#fff')],
    33: [K('oz_ui.jpg', 48.1, 53.0, 540, 740, 940, 330, 'تصميم موقع'), K('his_grad_ui.jpg', 53.0, 58.3, 540, 760, 520, 406, 'من شغل علي: تطبيقات'),
         K('oz_brand1.jpg', 60.5, 66.5, 540, 740, 940, 330, 'ألوان البراند'), K('oz_brand2.jpg', 66.5, 71.3, 540, 740, 940, 330, 'اللوجو والاسم'),
         K('his_logo180.jpg', 71.3, 74.0, 540, 740, 900, 321, 'من شغل علي: لوجو'), K('his_social.jpg', 74.0, 77.7, 540, 760, 520, 406, 'من شغل علي: براند كامل'),
         K('oz_poster.jpg', 79.8, 84.0, 540, 740, 940, 330, 'بوستر مطبوع'), K('c_billboard.jpg', 84.0, 87.6, 540, 760, 600, 340, 'يافطة في الشارع'),
         K('oz_brochure.jpg', 87.7, 92.7, 540, 760, 600, 378, 'بروشور'),
         K('oz_pack.jpg', 93.8, 100.4, 540, 780, 320, 470, 'باكدجنج حقيقي'),
         K('oz_social1.jpg', 101.0, 104.6, 540, 740, 940, 365, 'تصميمات سوشيال'), K('his_social.jpg', 104.6, 106.4, 540, 760, 520, 406, 'من شغل علي'),
         K('oz_social2.jpg', 106.4, 108.0, 540, 740, 940, 330, 'بوستات'),
         K('his_photo_cover.jpg', 109.3, 113.6, 540, 760, 520, 406, 'من شغل علي: تصوير وتعديل'), K('his_manip.jpg', 113.6, 117.1, 540, 760, 720, 380, 'ريتاتش وكمبوزيتنج'),
         K('oz_illus.jpg', 118.3, 123.0, 540, 740, 940, 350, 'إليستريشن'), K('his_cartoon_full.png', 123.0, 127.5, 540, 780, 300, 470, 'من شغل علي', fit='contain', bg='#fff'),
         K('oz_paint.jpg', 129.3, 134.0, 540, 740, 940, 330, 'رسم ديجيتال'), K('c_paint.jpg', 134.0, 139.5, 540, 790, 340, 480, 'ديجيتال بينتنج', pos='50% 30%')],
    44: [C('c_arch.jpg', 229.6, 231.9, 860, 1120, 270, 'تصميم معماري'), C('c_interior.jpg', 231.9, 232.8, 860, 1120, 270, 'تصميم داخلي'),
         C('c_maya.jpg', 235.2, 240.9, 860, 600, 240, 'رندر بـ Maya'), C('c_bbb.jpg', 254.1, 262.0, 200, 760, 240, 'فيلم معمول بـ Blender', pos='40% 50%'),
         C('c_c4d.jpg', 266.0, 269.7, 860, 1150, 260, 'شغل Cinema 4D')],
}

SHORTS = {
    # ---------------- 8: هو ايه | vectors (playlist #08, his "7") ----------------
    8: dict(ep='08', sec='huwa', label='مصطلح 7 من 30', vid_title='هو ايه | vectors', slug='vectors',
        pieces=[(6.5, 82.2)],
        scenes=[
            dict(t='v8_raster', at=6.3, b=dict(sq=8.8, col=10.7, show=11.7)),
            dict(t='v8_scale', at=13.6, b=dict(bad=17.1)),
            dict(t='v8_addrm', at=18.2, b=dict(add=18.9, rm=21.1)),
            dict(t='v8_heavy', at=23.5, b=dict(pc=25.1, bad=29.1, file=29.9)),
            dict(t='v8_sizes', at=32.1, b=dict(logo=34.6)),
            dict(t='v8_alt', at=37.4, b=dict(list=38.3)),
            dict(t='v8_pen', at=45.5, b=dict(line=48.1, tri=48.6, color=49.6, render=50.8)),
            dict(t='v8_size', at=52.6),
            dict(t='v8_photo', at=55.4, b=dict(det=59.8, photo=62.7)),
            dict(t='v8_convert', at=64.0, b=dict(trace=67.6)),
            dict(t='v8_tools', at=72.4, b=dict(progs=75.8)),
            dict(t='huwa_outro', at=79.5, term='Vectors', next='Image Compositing', b=dict(next=80.6)),
        ],
        WFIX={'software': 'الصور', 'لي': 'ليه', 'وهتبوز.': 'وهتبوظ.', 'هيزاود': 'هيزوّد', 'مرضو': 'برضو', 'هيبكبير': 'هيبقى كبير',
              'يفوت': '--', 'بتبكبيرها': 'بتكبّرها', 'واللجوهات': 'واللوجوهات', 'بت': '--', 'الكوبيوتر': 'للكمبيوتر', 'بكسلية': 'بيكسلاية',
              'ومسلس': 'ومثلث', 'كشورة': 'كصورة', 'تعوز': 'تعوز', 'بسيغ': 'بصيغ', 'فيكتورس': 'Vectors', 'الفيكتورس': 'الفيكتورز',
              'raster': 'الراستر'}),

    # ---------------- 33: المجالات و ساحر مدينة أوز | الفصل التاني "صور" (playlist #33) — all drawn, no film ----------------
    33: dict(ep='33', sec='oz', label='الفصل 2 من 5', vid_title='المجالات و ساحر مدينة أوز | الفصل الثاني "صور"', slug='scarecrow',
        pieces=[(13.5, 165.7)],
        scenes=[
            dict(t='oz_walk', at=13.3, b=dict(city=17.4)),
            dict(t='oz_farm', at=19.4, b=dict(work=25.1)),
            dict(t='oz_meet', at=27.9, b=dict(years=31.3, ask=33.4, yes=39.0)),
            dict(t='oz_many', at=42.0, b=dict(some=45.4)),
            dict(t='f_uiux', at=47.0, b=dict(ux=49.0, web=54.9, android=56.5)),
            dict(t='f_brand', at=58.4, b=dict(colors=65.0, font=71.3, card=76.3)),
            dict(t='f_print', at=77.8, b=dict(rollup=83.3, banner=84.1, sign=84.8, layout=87.7, flyer=90.7, brochure=91.6)),
            dict(t='f_pack', at=92.8, b=dict(juice=97.6, chips=98.1, carton=98.8)),
            dict(t='f_social', at=100.5, b=dict(poster=105.8)),
            dict(t='f_photo', at=108.1, b=dict(shot=109.3, retouch=113.6)),
            dict(t='f_illus', at=117.2, b=dict(mag=123.1)),
            dict(t='f_paint', at=127.6, b=dict(paper=136.6)),
            dict(t='oz_wish', at=139.9, b=dict(years=145.2, brain=150.7)),
            dict(t='oz_together', at=153.1, b=dict(road=162.9)),
        ],
        WFIX={'مقاتة': 'مآتة', 'بإبعاء': 'بحكم', 'تكلمي': 'تكلمني', 'بقلك': 'بقالك', 'لتخصوصات': 'تخصصات', 'الصفر': 'الأصفر', 'ماشي': 'ماشية',
              'وتلقى': 'وتعمل', 'دية': 'دي', 'البرينتينجز': 'البرينتنج', 'الرولابس': 'الرول أب', 'والليوفة': 'واليافط', 'الليئاوتز': 'اللياوتس',
              'الباكتجينج': 'الباكدجنج', 'والكاراتين': 'والكراتين', 'بصرات': 'بوسترات', 'Victors': 'Vectors', 'حيات': 'حاجات', 'برانج': 'برامج',
              'وبيباليها': 'وبيبقى ليها', 'بألم': 'بقلم', 'تخديني': 'تاخديني', 'للسحر': 'للساحر', 'قوز': 'أوز', 'وفقت': 'وافقت', 'هيكمله': 'هيكملوا',
              'عالطريق': 'على الطريق', 'لساحر': 'لساحر', 'اوز': 'أوز'}),

    # ---------------- 44: البرامج | برامج الـ 3D (playlist #37, 3:20-4:31) ----------------
    44: dict(ep='37', sec='prog', label='برامج الـ 3D', vid_title='كل برامج الجرافيكس و ازاي تختار البرنامج اللي محتاجوا', slug='3d_programs',
        pieces=[(200.8, 270.6)],
        scenes=[
            dict(t='p3_branch', at=200.6, b=dict(d3=201.8)),
            dict(t='p3_fields', at=202.5, b=dict(many=205.4)),
            dict(t='p3_shared', at=206.6, b=dict(move=210.0)),
            dict(t='p3_huwa', at=213.6),
            dict(t='p3_list', at=216.4, b=dict(any=219.7, each=222.8)),
            dict(t='p3_max', at=226.8, b=dict(model=230.4, arch=229.6, interior=231.9)),
            dict(t='p3_maya', at=232.8, b=dict(anim=235.2, disney=238.9, diff=240.9, plugins=243.7, own=246.6)),
            dict(t='p3_blender', at=248.0, b=dict(free=250.2, general=251.9, d3=254.1, edit=256.4, anim2d=258.3, comp=260.2)),
            dict(t='p3_c4d', at=262.0, b=dict(opinion=264.5, easy=265.0, mg=269.7)),
        ],
        WFIX={'لل3D': 'للـ3D', 'بيخشف': 'بيدخل في', 'اخلق': 'أغلب', 'بيبسها': 'بسهولة', 'لتنقل': 'تنتقل', 'مبادئة': 'مبادئ', 'بمميز': 'مميز',
              'بلغانز': 'بلاجنز', 'صوفت': 'سوفت', 'ويرز': 'وير', 'يتقدر': 'تقدر', 'تعملي': 'تعمل', 'الكمبوزوتينج': 'الكمبوزيتنج'}),
}
for _n, _r in REAL.items():
    SHORTS[_n]['real'] = _r
SHORTS[33]['face'] = 'oz_face.webm'  # he tells the story from a circle (Aly review 2026-10-22)
SHORTS[33]['face_pos'] = {'oz_many': (935, 300, 170)}  # the 8 field tiles fill the stage -> small circle top-right

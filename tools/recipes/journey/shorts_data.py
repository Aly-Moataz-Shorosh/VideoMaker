"""Journey series shorts (2026-10-22). Pilot = 8 (هو ايه | vectors), 33 (خيال المآتة), 44 (برامج الـ 3D).
Times = seconds in HIS source video `ep`. pieces = (first word start, last word start) fitted on the waveform.
scenes: t = scene id (motion-library/src/journey/*), at = source second it starts, b = {beat: source second} -> scene frames.
WFIX = caption word fixes (Whisper word -> his word; '--' = hide an unsure word)."""

PLAYLIST = 'https://youtube.com/playlist?list=PL--cO7twoKgnrn0J1tzEAb8JPbFJCa8kv'
PL_NAME = 'رحلة إلى مركز الجرافيكس'

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
            dict(t='v8_alt', at=37.4, b=dict(list=39.5)),
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

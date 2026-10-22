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
    8: [K('c_billboard.jpg', 32.9, 37.3, 280, 1150, 430, 286, 'إعلان في الشارع'),
        K('his_tshirt.jpg', 34.6, 37.3, 790, 1150, 410, 286, 'تيشيرت من شغل علي', be=True)],
    33: [],  # v3: the fields show his WHOLE video frame while he scrolls (Field clip), not crops
    44: [],  # v3: fewer examples; Big Buck Bunny replaces the Blender ball inside the scene
}

SHORTS = {
    # ---------------- 8: هو ايه | vectors (playlist #08, his "7") ----------------
    8: dict(ep='08', sec='huwa', label='مصطلح 7 من 30', vid_title='هو ايه | vectors', slug='vectors',
        pieces=[(6.5, 82.2)],
        scenes=[  # v3 (Aly review 2026-10-22): his own motion is better -> jy_clip = his episode, the box where his animation is
            dict(t='jy_clip', at=6.3, src='src_08.mp4', box=[500, 260, 1380, 790], title='الصورة الراستر = مربعات',
                 chips=[dict(t=8.8, text='🟥 مربعات كتير'), dict(t=10.7, text='🎨 كل مربع ليه لونه'), dict(t=11.7, text='🖥️ الكمبيوتر بيعرضها')]),
            dict(t='jy_zoom', at=13.6, src='pyramids_photo.png', iw=1920, ih=1080, target=[791, 393], b=dict(zoom=14.8, bad=17.1)),
            dict(t='v8_addrm', at=18.2, b=dict(add=18.9, rm=21.1)),
            dict(t='jy_clip', at=23.5, src='src_08.mp4', box=[268, 300, 1530, 760], title='كاميرات أعلى وكمبيوترز أقوى',
                 chips=[dict(t=24.3, text='📷 كاميرات أعلى'), dict(t=25.1, text='💻 كمبيوترز أقوى'), dict(t=29.9, text='📁 الملف بيكبر', bad=True)]),
            dict(t='v8_sizes', at=32.1, b=dict(logo=34.6)),
            dict(t='v8_alt', at=37.4, b=dict(list=38.3)),
            dict(t='v8_pen', at=45.5, b=dict(line=48.1, tri=48.6, color=49.6, render=50.8)),
            dict(t='v8_size', at=52.6),
            dict(t='jy_clip', at=55.4, src='src_08.mp4', box=[60, 100, 1830, 950], title='الراستر فيه تفاصيل',
                 chips=[dict(t=57.4, text='🖼️ مش هنستغنى عن الراستر'), dict(t=59.8, text='🔍 فيه تفاصيل')]),
            dict(t='jy_clip', at=61.25, src='src_08.mp4', box=[120, 220, 1810, 880], title='Vector ← → Raster',
                 chips=[dict(t=62.7, text='📷 الصور الفوتوغرافية'), dict(t=65.2, text='Vector ⬅ كصورة ⬅ Raster'), dict(t=67.6, text='Raster ⬅ Vector')]),
            dict(t='jy_clip', at=68.6, src='src_08.mp4', box=[150, 220, 1670, 850], title='التفاصيل بتقل',
                 chips=[dict(t=70.0, text='✏️ الشكل بيتغير'), dict(t=71.1, text='➖ التفاصيل بتقل', bad=True)]),
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
            dict(t='f_uiux', at=47.0, clip='src_33.mp4', b=dict(ux=49.0, web=54.9, android=56.5)),
            dict(t='f_brand', at=58.4, clip='src_33.mp4', b=dict(colors=65.0, font=71.3, card=76.3)),
            dict(t='f_print', at=77.8, clip='src_33.mp4', b=dict(rollup=83.3, banner=84.1, sign=84.8, layout=87.7, flyer=90.7, brochure=91.6)),
            dict(t='f_pack', at=92.8, clip='src_33.mp4', b=dict(juice=97.6, chips=98.1, carton=98.8)),
            dict(t='f_social', at=100.5, clip='src_33.mp4', b=dict(poster=105.8)),
            dict(t='f_photo', at=108.1, clip='src_33.mp4', b=dict(shot=109.3, retouch=113.6)),
            dict(t='f_illus', at=117.2, clip='src_33.mp4', b=dict(mag=123.1)),
            dict(t='f_paint', at=127.6, clip='src_33.mp4', b=dict(paper=136.6)),
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
            dict(t='p3_blender', at=248.0, real='c_bbb.jpg', b=dict(free=250.2, general=251.9, d3=254.1, edit=256.4, anim2d=258.3, comp=260.2)),
            dict(t='p3_c4d', at=262.0, b=dict(opinion=264.5, easy=265.0, mg=269.7)),
        ],
        WFIX={'لل3D': 'للـ3D', 'بيخشف': 'بيدخل في', 'اخلق': 'أغلب', 'بيبسها': 'بسهولة', 'لتنقل': 'تنتقل', 'مبادئة': 'مبادئ', 'بمميز': 'مميز',
              'بلغانز': 'بلاجنز', 'صوفت': 'سوفت', 'ويرز': 'وير', 'يتقدر': 'تقدر', 'تعملي': 'تعمل', 'الكمبوزوتينج': 'الكمبوزيتنج'}),
}
for _n, _r in REAL.items():
    SHORTS[_n]['real'] = _r
SHORTS[33]['face'] = 'src_33.mp4'  # he tells the story from a circle (Aly review 2026-10-22)
SHORTS[33]['face_pos'] = {'oz_many': (935, 300, 170), **{k: (900, 1390, 220, 1) for k in ('f_uiux', 'f_brand', 'f_print', 'f_pack', 'f_social', 'f_photo', 'f_illus', 'f_paint')}}  # the 8 field tiles fill the stage -> small circle top-right

# هو ايه terms 1..30 (playlist 02..31, short number = playlist position) — generated the approved way (huwa_data.py).
# Short 8 (vectors) keeps its hand-made version above.
import json as _json, os as _os
_cache = _os.path.join(_os.path.dirname(__file__), '..', 'huwa_shorts.json')
if _os.path.exists(_cache):
    for _k, _v in _json.load(open(_cache, encoding='utf8')).items():
        if int(_k) != 8:
            SHORTS[int(_k)] = _v

# Aly's review 2 of the film-course shorts (2026-11-07, work/review_shorts_1.md "Review 2"). Overrides fs_data2/fs_data3.
import fs_data2 as _D2
from fs_data2 import FULL, L, FT, T, PIPE
from fs_data3 import IB, IBC, IBL, IBR, NOWC, SH, IBF

SHORTS, CAP = {}, {8: []}  # 08 = new recording: auto captions from it

# 04: "انت بوظته" -> back to the first version EXACTLY + the new الجزيرة scene (only addition; hook ends before the tilt-shift slide)
_p4 = [dict(x) for x in _D2.SHORTS[4]['pieces']]
_p4[0] = dict(_p4[0], b=3436.0)
SHORTS[4] = dict(_D2.SHORTS[4], pieces=_p4[:-1] + [dict(a=3458.3, b=3474.4, raw=True, crop=L(40, 60, 1000), film=FT('الجزيرة', '2007', 'المثال التاني اللي عرضه'))] + _p4[-1:])

# 05: the Kuleshov moment = an OLD film (the 1918 original is lost): Ivan Mozzhukhin — the very actor of the experiment — in
# "The Queen of Spades" (1916, public domain, Wikimedia Commons); fact card ON the picture.
from fs_data3 import SHORTS as _S3
_p5 = [dict(x) for x in _S3[5]['pieces']]
_p5[3] = dict(a=1614.4, b=1620.5, file='qs1916_720.mp4', src=0.0, crop=L(160, 0, 960),
              film=FT('The Queen of Spades', '1916', 'إيفان موجوخين: نفس ممثل تجربة كوليشوف'),
              fact=dict(title='إمتى ظهرت الفكرة دي؟', text='تجربة ليف كوليشوف حوالي 1918 (المصادر مختلفة): نفس وش الممثل ده + لقطة مختلفة = إحساس مختلف',
                        src='University of Leeds · Facing the Mind', at=0.4))
SHORTS[5] = dict(_S3[5], pieces=_p5)

# 06: his webcam INSIDE the motion (tripod visible), no "Once upon a time" words, the dolly sentence once, another dolly-zoom frame
SHORTS[6] = dict(no=6, chapter=26, title='حركة الكاميرا و *Dolly zoom*', pieces=[
    dict(a=3626.2, b=3634.8, crop=L(40, 60, 1000), src=3766.0, film=FT('Guardians of the Galaxy Vol. 2', '2017', 'مثال Dolly zoom'), lab=[(0.3, 'Dolly zoom', None, 2.2)]),
    dict(a=3474.3, b=3484.8, show='MoveScene', anim=dict(keys=[[3474.3, 'intro']]), rew=True),
    dict(a=3493.3, b=3512.1, show='MoveScene', nocam=True, anim=dict(keys=[[3493.3, 'static']], cam={'file': 'projects/filmcourse/wc06.mp4', 'from': round(3493.3 - 3480, 2)})),
    dict(a=3523.6, b=3548.1, show='MoveScene', nocam=True, anim=dict(keys=[[3523.6, 'tilt']], tk=[[3523.6, 0], [3531.2, 0], [3531.6, 1], [3532.1, -1], [3532.8, 0], [3539.2, 0], [3539.6, 1], [3541.2, 1], [3541.6, -1], [3542.6, 0]], cam={'file': 'projects/filmcourse/wc06.mp4', 'from': round(3523.6 - 3480, 2)})),
    dict(a=3548.1, b=3562.8, show='MoveScene', nocam=True, anim=dict(keys=[[3548.1, 'pan']], pk=[[3548.1, 0], [3555.2, 0], [3555.6, -1], [3557.2, -1], [3557.6, 1], [3558.6, 1], [3559.0, -1], [3560.0, 0]], cam={'file': 'projects/filmcourse/wc06.mp4', 'from': round(3548.1 - 3480, 2)})),
    dict(a=3573.0, b=3579.9, crop=L(150, 30, 840), src=3591.0, film=FT('La La Land', '2016'), kw=[('Whip pan', 'Pan سريع بين الاتنين', 5.2)]),
    dict(a=3606.1, b=3614.3, show='MoveScene', anim=dict(keys=[[3606.1, 'push'], [3610.5, 'dolly']])),
    dict(a=3626.2, b=3634.8, show='MoveScene', anim=dict(keys=[[3626.2, 'dolly']], clip={'file': 'projects/filmcourse/course.mp4', 'from': 3766.0})),
])

# 10: short hook; script (top) + the film shot (bottom) TOGETHER the whole time
_TOP = L(320, 60, 700)
_pair = lambda *seq: dict(top=_TOP, file=IB, seq=SH(*seq))
SHORTS[10] = dict(no=10, chapter=18, title='السكريبت *بيوصف كل حاجة*', more=[dict(thumb='projects/filmcourse/pics/yt_NWtPI7aiefw.jpg', qr='projects/filmcourse/qr/yt_NWtPI7aiefw.png', title='تحليل المشهد كامل')], pieces=[
    dict(a=2292.6, b=2298.0, crop=_TOP, pair=_pair((0, 59.0, IBL)), film=IBF),
    dict(a=2131.5, b=2140.5, crop=L(300, 0, 720), rew=True, lab=[(0.5, 'سكريبت إبراهيم الأبيض', None, 2.4)]),
    dict(a=2154.7, b=2165.9, crop=L(160, 0, 960), kw=[('Sequence · Scene · Shot', 'تتابع · مشهد · لقطة', 2.0)]),
    dict(a=2193.4, b=2215.6, crop=_TOP, pair=_pair((0, 11.0, IBR), (4.3, 31.0, IBC), (9.0, 104.0, IBR), (13.0, 114.0, IBR), (17.5, 120.0, IBR))),
    dict(a=2224.6, b=2244.1, crop=_TOP, pair=_pair((0, 11.0, IBC), (7.0, 39.0, IBR), (13.0, 3.0, IBC))),
    dict(a=2253.7, b=2285.0, crop=_TOP, pair=_pair((0, 51.0, IBC), (7.0, 135.0, IBC), (14.0, 125.0, IBC), (21.0, 51.5, IBC))),
    dict(a=2285.5, b=2304.5, crop=_TOP, pair=_pair((0, 59.0, IBL), (6.0, 107.0, IBL), (12.0, 142.0, IBL))),
    dict(a=2327.2, b=2344.1, show='Pipeline', anim=dict(items=PIPE[1:4], hi=[[2327.2, 0], [2335.2, 0], [2338.7, 1], [2340.5, 2]], tags=[T(2342.3, 'إدّي لكل خطوة حقها')])),
])

# 12 / 13 / 19: no hook — straight into the topic
SHORTS[12] = dict(_S3[12], pieces=[dict(x, rew=False) for x in _S3[12]['pieces'][1:]])
SHORTS[13] = dict(_S3[13], pieces=[dict(x, rew=False) for x in _S3[13]['pieces'][1:]])
_p19 = [dict(x) for x in _S3[19]['pieces'][1:]]
_p19[0] = dict(_p19[0], rew=False)
# measured on his drawing (gridded frame at 509 s, 1280x720): 2D/3D ~180, traditional ~330, motion graphics ~520, stop motion ~720, VFX ~880, film ~1060
_p19[1] = dict(_p19[1], zoom=[(503.3, L(800, 30, 480)), (504.0, L(0, 30, 480)), (512.1, L(60, 30, 480)), (521.5, L(60, 30, 480)), (527.1, L(160, 30, 480))])
_p19[2] = dict(_p19[2], crop=L(300, 30, 480), zoom=[(542.7, L(500, 30, 480)), (554.5, L(660, 30, 480)), (558.5, L(800, 30, 480))])
SHORTS[19] = dict(_S3[19], pieces=_p19)

# 15: Youssef Chahine talking (his own voice, the clip he played) + Martin Scorsese
_p15 = [dict(x) for x in _D2.SHORTS[15]['pieces']]
SHORTS[15] = dict(_D2.SHORTS[15], pieces=[_p15[0],
    dict(a=1382.3, b=1399.2, raw=True, crop=L(150, 30, 840), rew=True, film=FT('يوسف شاهين', 'Youssef Chahine', 'من الفيديو اللي عرضه')),
    dict(a=1417.6, b=1436.4, raw=True, crop=L(150, 30, 840), film=FT('Martin Scorsese', 'Visual literacy', 'من الفيديو اللي عرضه')),
    dict(_p15[1], rew=False)] + _p15[2:])

# 16: NEW reel instead of the composition one (Aly: "شيله خالص.. وزود مكانه ريل تاني"): scenes that talk without dialogue
SHORTS[16] = dict(no=16, chapter=28, title='المشهد بيتكلم *من غير كلام*', pieces=[
    dict(a=4454.4, b=4467.7, crop=L(150, 30, 840), film=FT('Léon: The Professional', '1994'), kw=[('Sound effects', 'صوت التلاجة.. صوت الساعة', 2.0)]),
    dict(a=4069.6, b=4089.3, crop=L(150, 30, 840), rew=True, film=FT('زي النهاردة', '2008')),
    dict(a=4137.1, b=4144.3, crop=L(150, 30, 840), kw=[('Jump cut · Over the shoulder', 'قطع سريع.. ومن ورا الكتف', 0.6)]),
    dict(a=4158.5, b=4163.8, crop=L(150, 30, 840), kw=[('Whip pan', 'Pan سريع جدا', 2.6)]),
    dict(a=4198.3, b=4201.4, crop=L(150, 30, 840), kw=[('Sound effects', 'أصوات خفيفة بتكمّل المشهد', 0.4)]),
    dict(a=4295.9, b=4311.5, crop=L(150, 30, 840), kw=[('Crowd shot', 'ناس كتير.. والكاميرا بتجري معاهم', 1.2)]),
    dict(a=4328.6, b=4334.4, crop=L(150, 30, 840), lab=[(1.0, 'الطبل وقف.. علشان نركز', None, 2.4)]),
    dict(a=4443.8, b=4467.7, crop=L(150, 30, 840), film=FT('Léon: The Professional', '1994'), lab=[(6.5, 'مفيش كلام', None, 2.0)]),
    dict(a=4420.9, b=4433.6, show='big:اتفرّج كتير|وحلّل المشاهد والشوتات', ico='film'),
])

# 18: ratios on his exact words
SHORTS[18] = dict(_S3[18])
_p18 = [dict(x) for x in _S3[18]['pieces']]
_p18[3] = dict(_p18[3], anim=dict(_p18[3]['anim'], keys=[[1171.8, '4:3', 'التلفزيون'], [1173.7, '16:9', 'الشاشات الحديثة'], [1186.2, '16:9', 'يوتيوب: Landscape'],
                                                         [1189.0, '9:16', 'تقلب الموبايل'], [1190.8, '1:1', 'إنستجرام: مربع'], [1193.0, '9:16', 'أو ريل طويل']]))
SHORTS[18] = dict(_S3[18], pieces=_p18)

# 20: the drone fact ON the drone picture he showed (never an empty stage)
_p20 = [dict(x) for x in _S3[20]['pieces']]
_p20[4] = dict(a=3864.1, b=3867.9, crop=L(440, 200, 420), src=3858.0,
               fact=dict(title='الدرون في مصر', text='قانون 216 لسنة 2017: لازم تصريح من وزارة الدفاع (فيه استثناء لبعض الأنواع الخفيفة جدا)', src='Egypt Independent · مسار (Masaar)', at=0.2))
SHORTS[20] = dict(_S3[20], pieces=_p20)

# 08: his phone recording 20261107_075352 (built by make_f08.py: voice + circle from that file), pictures instead of text
P = lambda t, img, label, credit=None: dict(t=t, img='projects/filmcourse/stills/' + img, label=label, **({'credit': credit} if credit else {}))
SHORTS[8] = dict(no=8, chapter=2, title='الجمال *نوعين*', at='2:40', chap=2, camfix=dict(sx=500, sy=225, s=310), pieces=[
    dict(a=0.6, b=29.4, show='PicBoard', anim=dict(title='الجمال نوعين', items=[P(7.0, 'f08_naskh.jpg', 'خط نسخ', 'Wikimedia Commons'), P(11.5, 'f08_thuluth.jpg', 'خط ثلث', 'Wikimedia Commons'),
        P(16.0, 'f08_hiero.jpg', 'الهيروغليفي', 'Wikimedia Commons'), P(20.0, 'f08_chinese.jpg', 'الخط الصيني', 'Wikimedia Commons')])),
    dict(a=47.7, b=60.0, show='PicBoard', anim=dict(title='جمال الشكل في السينما', items=[P(4.5, 'f08_fil.jpg', 'الفيل الأزرق', 'لقطة من الإعلان')])),
    dict(a=60.8, b=88.0, show='PicBoard', anim=dict(title='جمال المحتوى', items=[P(2.6, 'f08_keif.jpg', 'الكيف'), P(5.6, 'f08_aar.jpg', 'العار'), P(8.6, 'f08_avocato.jpg', 'الأفوكاتو'),
        P(13.0, 'f08_fil.jpg', 'الفيل الأزرق: الاتنين'), P(19.0, 'f08_keif.jpg', 'كل فيلم ركّز حسب هدفه')])),
    dict(a=119.4, b=159.9, show='PicBoard', anim=dict(title='بلاغة السينما', items=[P(0.5, 'ex_low_angle.jpg', 'زاوية الكاميرا'), P(18.0, 'aspect_ibrahim.jpg', 'الكادر: فيه كام شخص؟'),
        P(27.0, 'setup_studio.jpg', 'هتركز على إيه؟'), P(31.0, 'dahih_high1.jpg', 'ترتيب الكادرات.. والقطع'), P(37.5, 'f08_sett.jpg', 'والموسيقى')])),
    dict(a=159.9, b=176.4, show='PicBoard', anim=dict(title='أفلام جمعت الاتنين', items=[P(2.5, 'f08_fil.jpg', 'الفيل الأزرق'), P(4.0, 'f08_kira.jpg', 'كيرة والجن'),
        P(6.6, 'f08_sett.jpg', 'الست'), P(10.0, 'f08_kabab.jpg', 'الإرهاب والكباب')])),
])

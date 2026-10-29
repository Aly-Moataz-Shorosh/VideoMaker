# Aly's review 2026-10-29 (the rest "حلوة اوي"):
#  01: "في الثانية 28 كلمة نص الفيديو مظهرتش" -> the piece ended on "يعتبر تقريبا", now it runs to "في ناس تقول 50% في فيديو";
#      "لما جيت انقل للمثال بتاع الصوت محتاج اقول و في الصوت" -> the ear piece starts on "المهم الأوديو بقى";
#      "ال hook ممكن يكون كلمة الصمت مهم نفس اهمية الصوت" -> that sentence (3:58) is the hook, the last-but-one piece ends before it.
#  19: the Istabraq video he played without music (only beats/claps) runs longer (as it was in the session, gain 1), and the
#      "العار" (1982) example he played (someone talking over the film's opening music) is in, with his words before/after it.
#      (the clip ends at 3786.3, the quietest spot of the music, to keep 19 under 3:00)
from series_data import AUD_OUT
from series_data8 import FULL
AAR = dict(sx=260, sy=60, sw=760)        # the 4:3 player of the العار clip
F_AAR = dict(title='El Aar', year='1982', note='فيلم العار · الشرح من قناة CINEMATOLOGY')  # Latin title: Arabic + year flipped (bidi)
# Aly: the talk over العار is from the Egyptian channel CINEMATOLOGY (exact 2021 video not found: their العار episode is from 2024);
# the no-music video at the end is Hazem El Seddiq's Stabraq video (English subtitles; exact video not found on YouTube).
F_STAB = dict(title='Hazem El Seddiq', note='فيديو إستبرق · من غير موسيقى')

ONE = {  # piece start a -> new piece (None = drop)
    16.7: dict(a=16.7, b=33.84, crop=dict(sx=180, sy=90, sw=760), lab=[(2.2, 'الأوديو', 'speaker_high_volume', 2.0), (16.3, 'الصوت = نص الفيديو', 'speaker_high_volume', 2.6)]),
    188.1: dict(a=186.04, b=199.12, raw=True, crop=dict(sx=150, sy=430, sw=330), labels=[('هدانك', 'ودانك', 'ear'), ('الكرسي', 'تزييق الكرسي', 'chair')]),
    235.0: dict(a=235.0, b=238.9, raw=True, src=221.9, crop=AUD_OUT, lab=[(0.8, 'صوت + فراغ', 'speaker_high_volume', 2.6)]),
}
CAP1 = {
    16.7: 'بس عمليا فيه نقطة ناقصة.. وهي الأوديو.. لأن الأوديو دايما احنا بنتجاهله وبنهتم بالصورة بس وبننسى إن الصوت مهم.. والصوت قصدي يعتبر تقريبا.. فيه ناس تقول 50% في الفيديو',
    188.1: 'المهم الأوديو بقى.. انت بتستخدم ودانك.. بتغمض عينك.. ولازم تركز قوي في التفاصيل الصغيرة اللي في الهوا حوالينا.. صوت تزييق الكرسي',
    235.0: 'الأوتبوت هو تكوين بين الصوت والفراغ..',
}
HOOK1 = dict(a=238.9, b=242.84, raw=True, src=221.9, crop=AUD_OUT, lab=[(0.2, 'الصمت مهم زي الصوت', 'shushing_face', 3.4)])
HOOK1_CAP = 'الصمت في حد ذاته مهم زي أهمية الصوت..'  # '..' ends the caption line here

NINETEEN = [
    dict(a=3813.6, b=3824.0, raw=True, crop=FULL, bars=True, lab=[(0.3, 'تواشيح بدل الموسيقى', 'mosque', 3.0)]),
    dict(a=3751.94, b=3758.47, crop=AAR),
    dict(a=3758.5, b=3786.3, raw=True, crop=AAR, film=F_AAR),  # no bars: they cover the FilmTag
    dict(a=3797.54, b=3813.4, crop=FULL),
    dict(a=3836.9, b=3881.0, crop=FULL, labels=[('شعر', 'شعر وكلمات عربي', 'scroll'), ('اجنبية', 'حتى على حاجة أجنبية', 'globe_with_meridians'), ('الصليبية', 'فيلم جمع الاتنين', 'crossed_swords')]),
    dict(a=3881.54, b=3902.6, crop=FULL, labels=[('خبطات', 'صوت خبطات', 'drum')]),
    dict(a=3902.8, b=3942.3, raw=True, crop=FULL, bars=True, lab=[(0.3, 'من غير موسيقى: دقات بس', 'drum', 3.0)], film=F_STAB, film_at=3.4),
]
CAP19 = ['',
         'تعالوا بقى نروح للموسيقى التصويرية.. تعالوا نشوف الفيديو ده.. ده لفيلم العار.. واحد بيتكلم عنه',
         '',
         'فده مثلا موسيقى تصويرية جميلة جدا في الفيلم.. بس هل كل الأفلام عشان أوصل إحساس لازم موسيقى تصويرية؟ مش لازم.. ممكن أستخدم أدان.. أو مش لازم أدان.. ممكن تواشيح أو أي حاجة زي كده',
         None, None, '']


def patch(SHORTS, CAP):
    ps, cs = SHORTS[1]['pieces'], CAP[1]
    for a, new in ONE.items():
        k = next(i for i, p in enumerate(ps) if abs(p['a'] - a) < 0.05)
        ps[k] = new; cs[k] = CAP1[a]
    ps.insert(0, HOOK1); cs.insert(0, HOOK1_CAP)
    old = dict(zip((p['a'] for p in SHORTS[19]['pieces']), CAP[19]))
    SHORTS[19]['pieces'] = NINETEEN
    CAP[19] = [c if c is not None else old[p['a']] for p, c in zip(NINETEEN, CAP19)]

# Aly 2026-10-29: "متعملش الفيديوهات من الاول بس حاول تعمل فيديو جديد و ترقمه 5" -> the old 05 (general talk) stays archived and a NEW 05
# is made from the part no short used: at 7:54 he plays a whole video "اللي فيه اللعبة مع المونتاج والصوت" (desert, balloons, mosque,
# Nubian musicians.. heard as it played, 511.7-629.8; the Zoom "meeting ended" popup comes at 631) and after the restart a clip with
# tense music where he says "أحس إن فيه قلق.. الراجل ده هيعمل جريمة قتل" (636.6-649.0) = the hook. Out of course order (7:54, chapter 2):
# Aly asked for number 5 so the other 30 files and bands stay as they are.
TENSE = dict(sx=330, sy=60, sw=760)       # the clip with the young man in the hood (his face stays inside)
EGY = dict(sx=260, sy=60, sw=760)         # the played video, below the Zoom toolbar (source y 0-50)

SHORT5 = dict(no=5, chapter=2, at='7:54', title='المونتاج *والصوت* مع بعض', pieces=[
    dict(a=636.6, b=649.0, raw=True, crop=TENSE, lab=[(0.4, 'الموسيقى بتقولك: فيه قلق', 'anxious_face_with_sweat', 4.0)]),
    dict(a=479.1, b=483.15, crop=EGY),
    dict(a=511.7, b=629.8, raw=True, crop=EGY, bars=True, lab=[(0.4, 'اسمع الصوت مع كل قطعة', 'speaker_high_volume', 4.0)]),
])
CAP5 = ['أنا أحس مثلا إن فيه قلق.. الراجل ده هيعمل جريمة قتل على أي حاجة',
        'فالفيديو ده اللي فيه اللعبة مع المونتاج والصوت',
        '']


def patch(SHORTS, CAP):
    SHORTS[5] = SHORT5; CAP[5] = list(CAP5)

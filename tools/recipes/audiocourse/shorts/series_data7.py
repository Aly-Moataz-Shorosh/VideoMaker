# Aly 2026-10-27: "ال icons مش بتبقى كافية خالص للشرح نهائي" + "جيب انا بشرح بايه في الفيديو" -> every IdeaRows (icon rows) piece of
# the series is replaced by what he really showed on his screen at that moment (slides, film frames, photos, demo videos; checked with
# frame_sheet.py, sheets ir0..ir4), or by real material he refers to (31: the Zoom H5 photo "اللي وريتكم الصورة بتاعته", the course
# HeadMonitor animation). Applied on top of all the other series data: patch(SHORTS, CAP).
from series_data import AUD_MIC, AUD_OUT, IMP, IMP_INFO
from series_data2 import TUBE
from series_data6 import MICKEY, KOC, WRS
AU_WAVE = dict(sx=300, sy=40, sw=760)
FULL = dict(sx=260, sy=40, sw=760)        # a full-screen video / film he played (centre)
SHOT_CELL = dict(sx=930, sy=330, sw=320)  # polar patterns chart: the Shotgun cell
H5 = dict(sx=320, sy=100, sw=640)         # Zoom H5 recorder photo (22 / 31)

R = {  # (short, piece start a) -> new piece(s)
    (1, 256.4): [dict(a=256.4, b=270.2, crop=AUD_OUT, labels=[('وحشة', 'صورة وحشة.. تكمل', 'television'), ('بويز', 'صوت بايظ.. تقفل', 'cross_mark')])],
    (1, 188.1): [dict(a=188.1, b=199.12, raw=True, crop=AUD_MIC, labels=[('هدانك', 'ودانك', 'ear'), ('الكرسي', 'تزييق الكرسي', 'chair')])],
    (1, 272.35): [dict(a=272.35, b=281.45, raw=True, crop=AUD_MIC, labels=[('الكاميرا', 'أصعب من التصوير', 'video_camera'), ('المونتاج', 'أهم من المونتاج', 'clapper_board')])],
    (2, 341.2): [dict(a=341.2, b=356.6, crop=IMP, zoom=[(345.5, IMP_INFO)], labels=[('المسدس', 'تعمير مسدس', 'water_pistol'), ('انفجار', 'انفجار', 'collision'), ('حادثة', 'حادثة', 'automobile')])],
    (3, 652.5): [dict(a=652.5, b=661.2, crop=MICKEY)],
    (3, 709.7): [dict(a=709.7, b=713.6, raw=True, src=705.0, crop=MICKEY, labels=[('الكوميديا', 'الرسالة وصلت بالضحك', 'face_with_tears_of_joy')])],
    (3, 738.1): [dict(a=738.1, b=748.0, crop=KOC, labels=[('معنى', 'الموسيقى بتوصل معنى', 'musical_note'), ('مشهور', 'عايز يبقى مشهور', 'star')])],
    (3, 779.4): [dict(a=779.4, b=785.7, raw=True, crop=KOC, labels=[('برعب', 'ممكن تقلب رعب', 'fearful_face'), ('بالشهرة', 'مهووس بالشهرة', 'star')])],
    (4, 788.3): [dict(a=788.3, b=804.5, crop=WRS, labels=[('استقال', 'بطّل المصارعة', 'boxing_glove'), ('السوبر', 'شغال في سوبر ماركت', 'shopping_cart')])],
    (4, 861.9): [dict(a=861.9, b=880.8, crop=WRS, labels=[('هتعلى', 'الموسيقى بتعلى', 'up_arrow'), ('فجأة', 'وتقف فجأة', 'muted_speaker'), ('يمثل', 'من غير ما الممثل يمثل', 'performing_arts')])],
    (13, 2815.98): [dict(a=2815.98, b=2828.2, src=2577.0, crop=SHOT_CELL, labels=[('شوت', 'مش لازم Shotgun', 'cross_mark')])],
    (13, 2836.4): [dict(a=2836.4, b=2842.7, src=2589.2, crop=SHOT_CELL, labels=[('هتنفع', 'ولو Shotgun.. ينفع', 'check_mark_button')])],
    (14, 2969.48): [dict(a=2969.48, b=3008.5, crop=dict(sx=230, sy=40, sw=760), zoom=[(2988.0, dict(sx=380, sy=60, sw=560))])],
    (15, 3009.09): [dict(a=3009.09, b=3024.2, src=3013.5, crop=dict(sx=310, sy=60, sw=640))],
    (18, 3708.82): [dict(a=3708.82, b=3732.5, crop=FULL)],
    (19, 3801.54): [dict(a=3801.54, b=3813.4, crop=FULL)],
    (19, 3836.9): [dict(a=3836.9, b=3881.0, crop=FULL)],
    (19, 3881.54): [dict(a=3881.54, b=3902.5, crop=FULL)],
    (20, 3963.4): [dict(a=3963.4, b=3971.4, crop=dict(sx=290, sy=60, sw=690))],
    (20, 4002.7): [dict(a=4002.7, b=4028.6, crop=dict(sx=220, sy=40, sw=760))],
    (20, 4053.7): [dict(a=4053.7, b=4072.4, crop=dict(sx=80, sy=40, sw=760))],
    (21, 4073.58): [dict(a=4073.58, b=4080.0, src=4109.9, crop=dict(sx=220, sy=40, sw=760))],
    (21, 4109.35): [dict(a=4109.35, b=4141.9, crop=dict(sx=220, sy=40, sw=760))],
    (22, 4155.27): [dict(a=4155.27, b=4171.1, crop=dict(sx=220, sy=60, sw=760))],
    (22, 4222.5): [dict(a=4222.5, b=4253.2, crop=dict(sx=230, sy=80, sw=600), labels=[('سيستمز', 'Single / Double system', 'video_camera')])],
    (27, 5906.99): [dict(a=5906.99, b=5916.4, src=6330.0, crop=AU_WAVE, labels=[('ازبطه', 'صوت عايز أظبطه', 'level_slider')]),
                    dict(a=5916.4, b=5930.1, src=2972.0, crop=dict(sx=230, sy=40, sw=760), labels=[('بودكاست', 'أو أسجل عليه', 'studio_microphone')])],
    (31, 7203.31): [dict(a=7203.31, b=7214.0, src=4253.5, crop=H5, labels=[('زوم', 'مسجل صوت Zoom', 'studio_microphone')]),
                    dict(a=7214.0, b=7221.0, src=7220.0, crop=AU_WAVE, labels=[('اوديشن', 'أو اللابتوب: Audition', 'laptop')])],
    (31, 7240.26): [dict(a=7240.26, b=7282.6, show='HeadMonitor'),
                    dict(a=7282.8, b=7302.1, src=2680.6, crop=TUBE, labels=[('الشوت', 'ماسك الشوت جن', 'studio_microphone'), ('السماعة', 'لازم يلبس السماعة', 'headphone')])],
}
CAPSPLIT = {  # pieces split in two -> their caption split too: (short, piece start a) -> (first, second)
    (27, 5906.99): ('أنا باستخدمه لحاجتين.. يا إما إن أنا عندي صوت عايز أظبطه.. وأشيل اللي فيه صوت الخلفية والحاجات دي كلها',
                    'يا إما أنا هسجل عليه أصلا.. بس ده احتمال قليل.. إلا لو مثلا هصور بودكاست وهوصل المايك بلابتوب وأسجل على اللابتوب.. أو ممكن لو عندي صوت فيديو أشتغل عليه على طول'),
    (31, 7203.31): ('أنا بوصل المايك.. ده بيحصل في حالتين.. لو أنا موصل المايك مش للكاميرا.. موصل المايك لمسجل صوت.. زوم ده اللي وريتكم الصورة بتاعته',
                    'أو موصل المايك باللابتوب وبسجل على أدوبي أوديشن'),
    (31, 7240.26): ('كان فيه طريقة إني أشغل الصوت وأنا بتكلم.. فهو بيخلي إنه وهو بيتكلم يكون سامع صوته.. بيوصل السماعة للزوم أو للمسجل الصوت اللي بيسجل عليه.. أو يوصل السماعة للابتوب.. بحيث إنه وهو بيتكلم يسمع صوته.. إيه لازمة ده كله؟ إنه يبقى عارف صوته واضح ولا مش واضح.. عشان في الأغلب بيبقى مستخدم مايك حساس.. فمش عايز صوته مرة بعيد ومرة قريب.. عشان البودكاست في الأساس صوتية مش مرئية.. فهو بس بيسمع صوته عشان يبقى حاسس بنفسه',
                    'ونفس الكلام الراجل اللي ماسك الشوت جن في الأفلام.. الشوت جن ده يا دوب بيمسك خط من الصوت.. فلازم يلبس السماعة.. عشان هو بيمسك المايك وبينقله بين اللي بيتكلموا.. لازم يبقى سامع المايك سامع إيه.. فعشان كده بيلبس السماعة'),
}


def patch(SHORTS, CAP):
    for (n, a), new in R.items():
        ps = SHORTS[n]['pieces']
        k = next(i for i, p in enumerate(ps) if abs(p['a'] - a) < 0.02)
        ps[k:k + 1] = new
        if (n, a) in CAPSPLIT:
            CAP[n][k:k + 1] = list(CAPSPLIT[(n, a)])

"""Hand-written on-screen CONTENT per plan scene (key = 'at' sentence id or 'av<n>'), so nothing on screen is plan prose.
items: (anchor_word, {label, emoji, logo(name in LOGOS), num, img}) -> appears ON that word.  clips: (clip_id, anchor_word).
fx: 'diffusion' (noise -> picture).  Images are project paths."""
KF = "assets/ai/higgsfield/keyframes_final/"
KF1 = "assets/ai/higgsfield/keyframes_v1/"
C = {
 "av1": dict(),   # auto: الوش / الصوت / المكان on their words
 "S001.5": dict(title="الفيديو ده معمول بالـ AI بإشراف علي شُرُش", items=[
     ("والصوت", dict(emoji="🎙️", label="الصوت")), ("والمكان", dict(emoji="🏛️", label="المكان")), ("متولّد", dict(emoji="✨", label="كله متولّد")),
     ("الفيديو", dict(img="output/studio_look_v5_generated.jpg", label="الستوديو ده اتولّد: 6 تجارب")),
     ("بإشراف", dict(img="output/studio_look_v9_mashrabiya.jpg", label="واتعدّل لحد ما بقى كده"))]),
 "S002.1": dict(items=[("سنين", dict(num="3", label="سنين")), ("فيديو", dict(num="0", label="فيديو جديد"))]),
 "S002.2": dict(items=[("ثمانية", dict(num="28", label="فيديو في الأسبوع"))]),
 "av4": dict(items=[("منصات", dict(logo="YouTube", label="@AlyShorosh")), ("منصات", dict(logo="إنستجرام", label="@alyshorosh")),
     ("منصات", dict(logo="فيسبوك", label="aly.shorosh")), ("منصات", dict(logo="تيك توك", label="@alyshorosh")), ("إزاي", dict(emoji="❓", label="إزاي؟"))]),
 "S002.5": dict(clips=[(6, "النهارده"), (102, "عالم"), (903, "خطوة"), (186, "أغنية")],
     items=[("عالم", dict(label="عالم الـ AI كله")), ("خطوة", dict(label="خطوة بخطوة")), ("أغنية", dict(emoji="🎵", label="وفي الآخر.. أغنية"))]),
 "S003.1": dict(clips=[(6, None)], items=[("طيارة", dict(emoji="✈️", label="طيارة حربية"))]),
 "S003.2": dict(clips=[(901, None)], items=[("قطعة", dict(emoji="🧩", label="كل قطعة ليها شغلانة")), ("ناقصة", dict(emoji="⛔", label="قطعة ناقصة = مش هتطير"))]),
 "S004.7": dict(clips=[(9, None)], items=[("نفك", dict(emoji="🔧", label="نفك الطيارة قطعة قطعة"))]),
 "av12": dict(items=[("الموديل", dict(emoji="🧠", label="موديل")), ("الأداة", dict(emoji="🌐", label="≠ أداة")), ("workflow", dict(emoji="🔀", label="≠ workflow")),
     ("Seedance", dict(logo="Seedance", label="Seedance")), ("Kling", dict(logo="Kling", label="Kling")), ("Veo", dict(logo="Veo", label="Veo"))]),
 "S005.4": dict(title="الأداة = الموقع اللي بتكتب فيه", url="higgsfield.ai",
     items=[("Higgsfield", dict(img="research/evidence_shots_v1/hf_genjutsu_refs.png", label="Higgsfield")),
            ("HeyGen", dict(img="research/evidence_shots_v1/heygen_looks.png", label="HeyGen"))]),
 "S005.5": dict(title="الـ workflow = الترتيب", items=[("صورة", dict(img=KF + "kf_026_C02b.png", label="صورة")),
     ("فيديو", dict(img=KF + "kf_031_C02b.png", label="فيديو")), ("صوت", dict(emoji="🎙️", label="صوت"))]),
 "av15": dict(items=[("بيرسم", dict(emoji="🎨", label="بيرسم إزاي؟")), ("ملايين", dict(num="ملايين", label="مثال اتدرب عليها"))]),
 "S006.3": dict(fx="diffusion", items=[("دوشة", dict(img=KF + "kf_006_C01.png", label="بيبدأ من دوشة.. وكل خطوة بيشيل شوية"))]),
 "S006.4": dict(title="قبل ما تفتح أي موقع.. 3 أسئلة", items=[("الموديل", dict(emoji="🧠", label="إيه الموديل؟")),
     ("input", dict(emoji="📥", label="إيه الـ input؟")), ("workflow", dict(emoji="🔀", label="إيه الـ workflow؟"))]),
 "av18": dict(),  # VID auto (thumbnail + QR)
 "S007.1": dict(clips=[(19, None)], items=[("الصور", dict(emoji="🖼️", label="الصور"))]),
 "S007.2": dict(items=[("كلام", dict(img=KF + "kf_019_C02a.png", label="كلام مكتوب ← صورة", prompt="A cartoon version of the same man stands in the middle of a floating gallery: dozens of freshly generated pictures fly around him like birds, sparkles where each picture appears.")), ("وصورة", dict(img="assets/ai/higgsfield/keyframes_final/kf_019_C02a_EDIT_red_noBeard.png", before="assets/ai/higgsfield/keyframes_final/kf_019_C02a.png", label="نفس الصورة: جاكت أحمر ومن غير دقن"))]),
 "S007.4": dict(clips=[(25, None)], items=[("الخلفية", dict(emoji="✂️", label="غيّر الخلفية")), ("امسح", dict(emoji="🧽", label="امسح حاجة")),
     ("برا", dict(emoji="↔️", label="كمّل برا الكادر")), ("بستايل", dict(emoji="🎨", label="ستايل تاني"))]),
 "S007.5": dict(title="أمثلة"),
 "S008.1": dict(title="الشخصية تفضل هي هي", items=[("الشخصية", dict(img="output/keyframes_v2_test_compare.jpg", label="تجارب وش علي في الفيديو ده")),
     ("صورة", dict(img="output/keyframes_v6_test.jpg", label="لحد ما بقى مظبوط"))]),
}

from plan_v3_content2 import C2
C.update(C2)

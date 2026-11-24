"""v4 content changes (Aly's v3 notes) on top of plan_v3_content.C. Same format; extra keys:
  out_at = anchor word where the item LEAVES (a group ends before the next group), pos = (x, y) next to its object,
  text with *word* = that word highlighted inside the sentence (note 10), page = a real page shown in the browser."""
PD = "work/pdf_pages/"
PG = "research/pages_v4/"
KF = "assets/ai/higgsfield/keyframes_final/"
C4 = {
 "av4": dict(items=[("منصات", dict(img=PD + "p21.png", label="الوصول على كل منصة (من داشبورد كل منصة)")), ("إزاي", dict(emoji="❓", label="إزاي؟"))]),
 "S002.2": dict(items=[("ثمانية", dict(num="28", label="فيديو في الأسبوع")), ("منصات", dict(img=PD + "p13.png", label="متجدولين كل يوم 8 بالليل"))]),
 # note 6: two groups — the rule (on its words) leaves before the model logos (each on its own name)
 "av12": dict(items=[("الموديل", dict(emoji="🧠", label="الموديل", out_at="العقل")), ("الأداة", dict(emoji="🌐", label="الأداة", out_at="العقل")),
     ("workflow", dict(emoji="🔀", label="الـ workflow", out_at="العقل")), ("العقل", dict(text="الموديل = *العقل* اللي بيولّد")),
     ("Seedance", dict(logo="Seedance", label="Seedance", out_at="الأداة")), ("Kling", dict(logo="Kling", label="Kling", out_at="الأداة")), ("Veo", dict(logo="Veo", label="Veo", out_at="الأداة"))]),
 # notes 7, 8: Higgsfield's image page on its name; Magnific (the voice says it now) = its name + what it is known for (our picture upscaled)
 "S005.4": dict(items=[("الأداة", dict(text="الأداة = *الموقع* اللي بتكتب فيه", pos=(960, 110), out_at="Higgsfield")),
     ("Higgsfield", dict(page=PG + "higgsfield_image_crop.png", url="higgsfield.ai/ai-image")),
     ("Magnific", dict(img=KF + "kf_026_C02b.png", label="Magnific: تكبير بتفاصيل", pos=(1480, 560), w=640))], extend=1.8),  # both said at the very end -> hold 1.8 s into the next sentence
 "av15": dict(items=[("بيرسم", dict(emoji="🎨", label="بيرسم إزاي؟")), ("ملايين", dict(text="اتدرب على *ملايين* الأمثلة"))]),
 "S006.4": dict(title="قبل ما تفتح أي موقع.. 3 أسئلة", items=[("الموديل", dict(emoji="🧠", label="إيه الموديل؟")),
     ("input", dict(emoji="📥", label="إيه الـ input؟")), ("workflow", dict(emoji="🔀", label="إيه الـ workflow؟"))]),
 # note 14: each word ON its card (cards of clip 25 from right to left in reading: beach, eraser, frame, brush are LEFT->RIGHT on screen)
 "S007.4": dict(clips=[(25, None)], items=[("الخلفية", dict(emoji="✂️", label="غيّر الخلفية", pos=(205, 120))), ("امسح", dict(emoji="🧽", label="امسح حاجة", pos=(700, 120))),
     ("برا", dict(emoji="↔️", label="كمّل برا الكدر", pos=(1195, 120))), ("بستايل", dict(emoji="🎨", label="ستايل تاني", pos=(1690, 120)))]),
 # PDF proof pages (note 1 / v2 note 4)
 "av121": dict(items=[("video", dict(img=PD + "p06.png", label="video maker")), ("ستايل", dict(img=PD + "p09.png", label="20 ستايل برقم"))]),
 "S038.3": dict(items=[("skill", dict(img=PD + "p10.png", label="skill السكريبت")), ("publisher", dict(img=PD + "p12.png", label="28 فيديو في الأسبوع")),
     ("إنستجرام", dict(img=PD + "p17.png", label="كومنت ← اللينك في الرسايل"))]),
 "av125": dict(items=[("كورس", dict(img=PD + "p07.png", label="كورس ساعتين ← 31 شورت"))]),
 "S039.3": dict(items=[("أربعمية", dict(img=PD + "p21.png", label="474 ألف مشاهدة في آخر شهر")), ("ميتين", dict(img=PD + "p23.png", label="ريل واحد: 253 ألف على فيسبوك"))]),
 "S039.5": dict(items=[("كل", dict(img=PD + "p08.png", label="شورت كل يوم + فيديو كل أسبوع"))]),
 "S037.3": dict(items=[("سنين", dict(num="3", label="سنين من غير فيديو")), ("كورسات", dict(img=PD + "p26.png", label="3 كورسات على الرف")),
     ("الإنترو", dict(img=PD + "p27.png", label="إنترو «انت بتشتغل ايه» من 2023"))]),
 "S036.5": dict(items=[("skill", dict(img=PD + "p10.png", label="skill بتكتب السكريبت")), ("الريلز", dict(img=PD + "p12.png", label="skill بتنشر الريلز")),
     ("إنستجرام", dict(img=PD + "p18.png", label="skill بترد على الكومنتات"))], clips=[(117, None)]),
}

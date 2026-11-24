
# ======================= v8 PART A (v6 time): Aly's notes on rough cut v7 (review_rough_v7_notes.md) =======================
V8 = "assets/v8/"; LG = lg
def drop(title_or_label):
    s_ = findS(title_or_label); SPECS.remove(s_); return s_
# boards rebuilt from scratch in v8 time (PART B): camera moves, start/end frames, 3D, best trick, sites tour, free tools, N1,
# Claude, MCP (3 specs), skills N3, «made with» tree, real experience, step by step
for k_ in ("حركة الكاميرا بتختارها بالاسم", "أول صورة وآخر صورة", "الـ 3D", "أحسن تريك: الحركة من Blender.. والشكل من الـ AI", "جولة في المواقع",
           "على جهازك ببلاش", "LLM = موديل اتدرب على كلام كتير جداً", "claude_new_chat.jpg", "فيشة موحدة", "Claude بيقرا القايمة",
           "الفيديو ده نفسه: Claude متوصّل بالأربعة في نفس الوقت", "skill = كراسة خبرة", "الفيديو ده اتعمل من جوه Claude Code",
           "تجربة حقيقية بالأرقام", "الدروس", "خطوة بخطوة: ريل 30 ثانية"):
    try: drop(k_)
    except (KeyError, ValueError): print("v8: no spec for", k_)

# note 12: alternatives with their LOGOS (+ promoat); the round face centred (V8.tsx)
s = findS("avatar_section_circle.mp4")
alt = [it for it in s["items"] if str(it.get("label", "")).startswith("بدايل")]
if alt:
    t_alt = alt[0]["t"]; o_alt = alt[0].get("out_t")
    s["items"] = [it for it in s["items"] if not (str(it.get("label", "")).startswith("بدايل") or it.get("label") == "كل واحد ليه أفاتار بيتكلم")]
    names = [("synthesia.png", "Synthesia"), ("d-id.png", "D-ID"), ("hedra.png", "Hedra"), ("captions.png", "Captions"), ("promoat.png", "Promoat")]
    s["items"] += outs([N(t_alt, 560, 400, "alternatives: بدايل", size=24)] +
                       [N(t_alt + 0.2 + i * 0.15, 330 + (i % 3) * 230, 520 + (i // 3) * 170, logo=LG(f), label=n, size=18) for i, (f, n) in enumerate(names)], o_alt)
# note 13: Looks bigger, 2x2, the circle hidden while they play; note 14: lip sync = BEFORE (his real video) -> AFTER (same video, new words in sync)
circ = next(it for it in s["items"] if it.get("k") == "circle")
tl6 = T("looks", 201.4, 201.6); tls6 = T("lipsync", 206.2, 206.4); tsay = T("تاخد", 207.2, 207.4); tex6 = T("وجربنا", 210.8, 211.0)
s["items"] = [it for it in s["items"] if not (tl6 - 0.05 <= (it.get("t") or 0) < tex6 - 0.2)]
looks = [(GEN + "avatar_015_C02.mp4", "الستوديو"), (HG + "look_beach.mp4", "البحر"), (HG + "look_room_black.mp4", "أوضة تانية"), (HG + "look_presenter.mp4", "مقدم واقف")]
s["items"] += outs([N(tl6 + 0.1 * i, 1240 - (i % 2) * 560, 330 + (i // 2) * 330, nm, src=src, w=480, loop=3.6, size=22) for i, (src, nm) in enumerate(looks)], tls6 - 0.15)
s["items"] += outs([N(tls6, 960, 250, "lip sync: نفس الفيديو الحقيقي.. البق بس اللي بيتغير", size=26),
                    N(tls6 + 0.2, 1340, 560, "قبل: فيديو حقيقي ليّ", src=HG + "lipsync_src_realroom_a.mp4", w=560, loop=3.8, size=22),
                    E(tls6 + 0.6, 1040, 560, 880, 560),
                    N(tsay, 580, 560, "بعد: نفس الفيديو بيقول الكلام ده", src=HG + "lipsync_ex_realroom.mp4", w=560, size=22, good=True)], tex6 - 0.15)
circ["hide"] = [[tl6 - 0.1, tex6 - 0.1]]
# note 16: the consent chips come WITH «بموافقته» and stay (+ a 2 s hold in the timeline)
tq6 = T("بموافقته", 228.0, 230.0)
for it in s["items"]:
    if it.get("label") in ("HeyGen بيطلب فيديو موافقة", "من غير موافقة = مينفعش"): it["t"] = tq6 + (0.2 if "HeyGen" in it["label"] else 0.4)

# note 11: the Genjutsu REEL itself plays beside the dashboard + 253K
s = findS("ريل Genjutsu: داشبورد فيسبوك")
t0 = min(it["t"] for it in s["items"] if it.get("k") == "num")
for it in s["items"]:
    if it.get("label") == "ريل Genjutsu: داشبورد فيسبوك": it.update(x=1300, y=640, w=380)
    if it.get("k") == "num": it.update(x=1300, y=830)
s["items"] = [it for it in s["items"] if not (it.get("logo") or "").endswith("facebook.png")]
s["items"] += [N(t0 - 0.6, 560, 520, "الريل نفسه: اتعمل بـ Genjutsu", src=V8 + "genjutsu_reel.mp4", w=620, loop=12, size=22)]

# note 24: Video Agent = HeyGen's own page (my montage was not made in HeyGen); note 14 there: twin/looks keep v7
s = findS("Video Agent")
for it in s["items"]:
    if it.get("label") == "Video Agent": it.update(src=EV + "heygen_agent.png", sub="صفحة Video Agent الرسمية في HeyGen", loop=None); it.pop("loopDur", None); it.pop("loop", None)
# note 28: MCP said early -> «we explain MCP in detail later»
for key_, w_, a_ in (("Suno MCP · أكتوبر (تجريبي)", "MCP", 466.0), ("MCP: Claude يكلّم HeyGen", "MCP", 371.5)):
    try:
        s = findS(key_); tm_ = T(w_, a_ - 2, a_)
        s["items"] += [N(tm_ + 0.4, 960, 900, "الـ MCP.. هنشرحه بالتفصيل بعدين في الفيديو", emo="pushpin", size=20, bg="mustard")]
    except KeyError: pass
# note 25: the Higgsfield pricing video thumb bigger with its QR (and a 2.5 s hold in the timeline)
s = findS("فيديو تسعيرة Higgsfield")
for it in s["items"]:
    if it.get("label") == "فيديو تسعيرة Higgsfield": it.update(w=360, x=1500, y=560, label="عندي فيديو كامل عن تسعيرة Higgsfield")
    if "qr_10UXB0cT4Ss" in str(it.get("src", "")): it.update(x=1500, y=770, w=120)
# note 33: the agents chip lower, off the logo labels
s = findS("الـ agent مش بيرسم بنفسه.. بيكتب كود")
for it in s["items"]:
    if it.get("label") == "الـ agent مش بيرسم بنفسه.. بيكتب كود": it["y"] = 470
# note 34: HyperFrames is said -> add it; and the rest of the real stack as a small strip
for it in s["items"]:
    if it.get("label") in ("Remotion", "three.js", "ffmpeg", "Blender", "Whisper"): it["x"] = {"Remotion": 1620, "three.js": 1350, "ffmpeg": 1080, "Blender": 810, "Whisper": 270}[it["label"]]
tl_h = next(it["t"] for it in s["items"] if it.get("label") == "Remotion")
s["items"] += [N(tl_h + 0.5, 540, 620, logo=LG("hyperframes-site.svg"), label="HyperFrames", sub="HTML ← فيديو", size=20),
               N(tl_h + 3.5, 960, 840, "وكمان: OpenCV · NumPy · Pillow · onnxruntime · Playwright · yt-dlp", size=17)]
# note 36: the real Photoshop / After Effects icons; note 38: scripts we made -> «in the Human part»
s = findS("سكريبتات جوه برامجك")
for it in s["items"]:
    if it.get("label") == "Photoshop": it["logo"] = LG("photoshop.svg")
    if it.get("label") == "After Effects": it["logo"] = LG("after-effects.svg")
    if str(it.get("label", "")).startswith("سكريبتاتنا"): it.update(label="سكريبتات تانية عملناها (نشر الريلز، الرد على الكومنتات).. هنشوفها في قسم الإنسان", size=19, emo="pushpin")

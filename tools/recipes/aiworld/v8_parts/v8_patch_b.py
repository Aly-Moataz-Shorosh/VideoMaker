
# ======================= v8 PART B (v8 time = words_v8.json): boards rebuilt for Aly's v7 notes =======================
for sp_ in SPECS:   # circle hide windows were written in v6 time
    for it in sp_["items"]:
        if it.get("hide"): it["hide"] = [[M67(a_), M67(b_)] for a_, b_ in it["hide"]]
W8 = json.load(open("work/words_v8.json", encoding="utf-8"))
def T8(word, after, default=None, win=12):
    key = word.split()[0].lower()
    for w in W8:
        if w["a"] >= after - 0.4 and key in w["w"].lower():
            if w["a"] - after > win: break
            return round(w["a"], 3)
    MISS6.append(("v8:" + word, after)); return round(default if default is not None else after, 3)
T8P = json.load(open("work/timeline_v8.json", encoding="utf-8"))["pieces"]
def spec8(a, b, title=None, title_t=None, items=(), sfx=()):
    SPECS.append(dict(a=round(a, 3), b=round(b, 3), title=title, title_t=title_t, items=list(items), circle=False, sfx=list(sfx)))
CLv = CL; P6v = P6; LGv = lg

# note 8: start / end frame = clip 201 (the parts assemble: first frame ≠ last frame), the middle video plays, the board holds through the pause
ta = T8("وأقوى", 154.3); tf2 = T8("وend", 156.8); tmid = T8("وهو", 159.5)
spec8(ta - 0.1, T8("وفيه", 162.3) - 0.1, "أول صورة وآخر صورة", ta, [
    N(ta + 0.1, 1470, 400, "1. أول صورة", src=V8 + "f201_first.jpg", w=360, size=22),
    N(tf2, 450, 400, "2. آخر صورة", src=V8 + "f201_last.jpg", w=360, size=22),
    N(tmid, 960, 400, "3. الموديل بيعمل اللي في النص", src=CL + "clip_201_C11.mp4", w=360, size=22),
    E(tmid, 1280, 400, 1150, 400), E(tmid, 640, 400, 770, 400),
    SC(ta + 1.0, 960, 740, P6 + "hf_frames_slot.jpg", w=200, ar=466 / 604, boxes=[dict(x=36, y=46, w=28, h=9, label="Frames"), dict(x=3, y=58, w=94, h=40, label="هنا الصور")]),
    N(ta + 1.2, 1360, 740, "في Higgsfield: الصورة الأولى = البداية", size=20)])
# note 9: camera moves — each clip comes WITH its name on its word, then the board holds (+ 2.2 s pause)
tk = T8("حركة", 162.9); td = T8("dolly", 164.5); to_ = T8("orbit", 165.3); tc = T8("crane", 166.0)
spec8(tk - 0.15, T8("الموديلات", 168.9) - 0.1, "حركة الكاميرا بتختارها بالاسم", tk, [
    N(td, 1400, 400, "dolly: الكاميرا بتدخل", src=CL + "clip_006_C01.mp4", w=400, loop=4, size=24), E(td + 0.2, 1310, 650, 1490, 650),
    N(to_, 960, 400, "orbit: بتلف حواليه", src=CL + "clip_204_C11.mp4", w=400, loop=4, size=24), E(to_ + 0.2, 880, 660, 1040, 660, bend=-120),
    N(tc, 520, 400, "crane: بتطلع لفوق", src=CL + "clip_029_C02b.mp4", w=400, loop=4, size=24), E(tc + 0.2, 520, 690, 520, 630),
    N(tc + 0.7, 1080, 800, "حركات الكاميرا بالتفصيل: «لغة السينما»", src=CH + "thumb_S-tSUtClTOg.jpg", w=200, size=20),
    N(tc + 0.9, 850, 800, src=CH + "qr_S-tSUtClTOg.png", w=100, ar=1)])
# notes 19/21/22: 3D = generation only (image -> 3D model, Gaussian splats); «best trick» explained as steps Blender -> Higgsfield -> result
a3 = T8("3D", 308.2); tmod = T8("موديل", 313.0); tgs = T8("Gaussian", 316.0)
spec8(a3 - 0.2, T8("وأحسن", 319.8) - 0.1, "الـ 3D", a3, outs([
    N(T8("صورة", 310.2), 1400, 470, "صورة", src=KF + "kf_171_C09.png", w=420, size=22), E(tmod, 1170, 470, 1000, 470),
    N(tmod, 740, 470, "← موديل 3D تلف حواليه", src=HF6 + "jet_from_image_turntable.mp4", w=460, loop=6, sub="sam 3D في Higgsfield", size=22)], tgs - 0.15) + [
    N(tgs, 1200, 470, "Gaussian splats: صور كتير لمكان حقيقي", src=P5 + "splats_inria.png", w=560, size=22),
    E(tgs + 1.0, 900, 470, 760, 470), N(tgs + 1.1, 560, 470, "← مشهد 3D تلف فيه", emo="camera_with_flash", size=24)])
tb1 = T8("وأحسن", 319.8); tbl = T8("Blender،", 322.9); tgive = T8("نديها", 327.7); tsee = T8("وهتشوف", 332.9)
spec8(tb1 - 0.1, T8("الصوت", 335.0) - 0.15 if False else T8("دلوقتي", 334.3) + 0.9, "أحسن تريك: الحركة من Blender.. والشكل من الـ AI", tb1, outs([
    N(tbl, 1440, 430, "1. Blender: الحركة والكاميرا", src="output/blockouts_v6/bridge_static_blockout.mp4", w=420, loop=6, size=22),
    E(tgive - 0.2, 1200, 430, 1080, 430),
    N(tgive, 960, 400, "2. نديها لـ Higgsfield كريفرنس", logo=LG("higgsfield.png"), size=22),
    TY(tgive + 0.4, 960, 500, "«كوبري على النيل وقت الغروب»", w=330, rtl=True, head="✎", size=19, dur=14),
    E(tgive + 1.2, 840, 430, 720, 430),
    N(tgive + 1.4, 480, 430, "3. النتيجة: نفس الحركة.. شكل جديد", src=CL + "look_bridge.mp4", w=420, loop=6, size=22, good=True)], tsee - 0.1) + [
    N(tsee, 1250, 520, "قبل: Blender رمادي", src="output/blockouts_v6/bridge_static_blockout.mp4", w=600, loop=6, size=22),
    N(tsee, 670, 520, "بعد: التوليد", src=CL + "look_bridge.mp4", w=600, loop=6, size=22)])
# note 23: sites tour = generation sites only (no Claude / Codex) + Magnific
at_ = T8("دلوقتي", 338.0)
sites = [("heygen.ico", "HeyGen"), ("elevenlabs.png", "ElevenLabs"), ("higgsfield.png", "Higgsfield"), ("suno.png", "Suno")]
spec8(at_ - 0.1, T8("نبدأ", 347.5) + 1.0, "جولة في مواقع التوليد", at_ + 0.2,
      [N(at_ + 0.3 + i * 0.35, 1560 - i * 300, 470, logo=LG(f), label=n, size=22) for i, (f, n) in enumerate(sites)] +
      [N(at_ + 1.7, 360, 470, "Magnific", src=P6 + "magnific_home.jpg", w=300, ar=1008 / 326, size=22),
       N(T8("نوفمبر", 342.0), 960, 720, "لحد نوفمبر 2026", emo="calendar", size=28), N(T8("بتتغير", 344.5), 960, 830, "بتتغير كل شهر.. دي صورة لدلوقتي", size=22)])
# note 29: free on your PC — a clean grid, one Qwen, Luma logo
fa = T8("ComfyUI", 492.0, 492.0); ff = T8("Firefly", 511.8)
spec8(fa - 0.3, T8("قبل", 518.2) - 0.15, "على جهازك ببلاش", fa, [
    N(fa, 1450, 300, logo=LG("comfyui.png"), label="ComfyUI", size=22),
    N(fa + 0.8, 1640, 470, "وصف", size=20), E(fa + 0.9, 1585, 470, 1510, 470), N(fa + 1.0, 1450, 470, "موديل", size=20), E(fa + 1.1, 1390, 470, 1310, 470), N(fa + 1.2, 1250, 470, "فيديو", size=20),
    N(T8("LTX", 499.5), 1620, 640, logo=LG("ltx.png"), label="LTX 2.5: 4K + صوت", size=18),
    N(T8("وWan", 503.5), 1450, 640, logo=LG("wan.ico"), label="Wan", size=18),
    N(T8("وFlux", 504.2), 1300, 640, logo=LG("flux.png"), label="Flux: صور", size=18),
    N(T8("وQwen", 505.8), 1150, 640, logo=LG("qwen.png"), label="Qwen", size=18),
    N(T8("nodes", 507.0), 1400, 830, "nodes لـ HeyGen + Comfy Cloud لو جهازك ضعيف", logo=LG("heygen.ico"), size=17),
    N(ff, 780, 320, logo=LG("firefly.png"), label="Firefly", sub="توسيع وتعديل صور", size=20), N(T8("وRunway", ff), 450, 320, logo=LG("runway.png"), label="Runway", sub="فيديو", size=20),
    N(T8("وLuma", ff), 780, 620, logo=LG("luma.ico"), label="Luma", sub="فيديو + 3D", size=20), N(T8("وCapCut", ff), 450, 620, logo=LG("capcut.ico"), label="CapCut", sub="مونتاج + كابشن", size=20)])
# notes 30/31: what LLM / agent / Code are — 3 columns with REAL examples; the agent does not generate by itself: it OPENS the sites;
# + the audiobook example in the pause after N1
n1 = T8("قبل", 518.2); tag = T8("agent؟", 526.9); tdl = T8("بتكلّمه", 536.1); tgen = T8("حتى", 539.3); tsh = T8("الشات", 545.0); tco = T8("وCowork", 546.8); tcd = T8("وCode", 549.9); tvid = T8("والفيديو", 556.0)
hold_end = next(p["t"] + p["dur"] for p in T8P if p["kind"] == "hold" and abs(p["t"] - 560.5) < 3)
spec8(n1, hold_end - 0.05, None, None, outs([
    N(T8("LLM؟", 519.7), 1460, 270, "LLM = موديل اتدرب على كلام كتير جداً", emo="brain", size=24),
    N(T8("فبيفهم", 522.5), 1460, 360, "بيفهم · بيكتب · بيخطط", size=20),
    E(tag, 1200, 270, 1110, 270), N(tag, 880, 270, "agent = LLM ليه إيدين", emo="robot", size=24),
    N(T8("ملفات،", 529.5), 880, 360, "بيفتح ملفات · بيشغّل برامج · يشوف النتيجة", size=19),
    N(tdl, 960, 470, "بتكلّمه وتفكّروا سوا.. وهو اللي يشتغل", emo="speech_balloon", size=22, good=True),
    N(tgen, 960, 570, "بيفتح مواقع التوليد بنفسه ويولّد هناك.. ويديك النتيجة", size=20),
    *[N(tgen + 0.4 + i * 0.2, 640 + i * 210, 700, logo=LG(f), size=18) for i, f in enumerate(["elevenlabs.png", "higgsfield.png", "heygen.ico", "suno.png"])],
    N(tgen + 1.5, 960, 840, "إزاي يدخل على موقع؟ access للمتصفح أو MCP (هنشرحه في قسم الـ MCP)", emo="pushpin", size=18)], tsh - 0.2) +
    outs([N(tsh, 1460, 270, "1. الشات: كلام وتفكير", size=24), N(tsh + 0.3, 1460, 430, src=P6 + "claude_new_chat.jpg", w=420, ar=1120 / 380),
          *[N(tsh + 0.5 + i * 0.2, 1340 + i * 120, 600, logo=LG(f), size=16) for i, f in enumerate(["claude.svg", "chatgpt.png", "gemini.png"])],
          N(tco, 960, 270, "2. Cowork / agent: بيشتغل على ملفاتك وبرامجك", size=22), N(tco + 0.3, 960, 430, src=V8 + "claude_session_2x.mp4", w=420, ar=1280 / 1004, loop=8),
          N(tco + 0.6, 960, 640, "Claude Cowork · ChatGPT agent", size=18),
          N(tcd, 460, 270, "3. Code: بيكتب برنامج صغير ويشغّله", size=22),
          *[N(tcd + 0.3 + i * 0.2, 280 + i * 120, 420, logo=LG(f), size=16) for i, f in enumerate(["claude.svg", "openai-codex.png", "cursor.png", "antigravity.png"])],
          N(tcd + 1.2, 460, 560, "Claude Code · Codex · Cursor · Antigravity", size=17),
          N(T8("developer،", 553.1), 460, 680, "مش علشان تبقى developer.. علشان يخلّص شغلك", size=18),
          N(tvid, 960, 820, "الفيديو ده كله اتعمل من جوه Claude Code", logo=LG("claude.svg"), size=24, bg="mustard", good=True)], hold_end - 6.0) +
    [N(hold_end - 5.8, 960, 230, "مثال: حوّل كتاب لكتاب مسموع بـ Claude Code", emo="headphone", size=26, bg="mustard"),
     TY(hold_end - 5.5, 1450, 330, "«حوّل الكتاب ده لصوت، فصل فصل»", w=380, rtl=True, head="انت:", size=20, dur=12),
     E(hold_end - 4.6, 1450, 430, 1450, 480),
     TY(hold_end - 4.5, 1450, 500, "import pytesseract  # OCR\nfrom TTS import tts  # صوت", w=380, head="Python", size=18, dur=18),
     N(hold_end - 4.0, 960, 420, "1. OCR: صفحات الكتاب ← كلام", emo="page_facing_up", size=20),
     N(hold_end - 3.3, 960, 540, "2. الكلام ← صوت (library ببلاش أو ElevenLabs بالـ MCP)", logo=LG("elevenlabs.png"), size=18),
     W(hold_end - 2.4, 600, 470, w=420, h=110),
     N(hold_end - 2.2, 600, 590, "3. النتيجة: فصل 1.mp3 · فصل 2.mp3 …", emo="musical_notes", size=20, good=True)])
# note 32: the Claude products, each with a real picture / motion
c1 = T8("claude.ai", 590.4); cP = T8("Projects،", 591.9); cC = T8("Connectors", 592.8); cS = T8("Skills.", 595.4); cCh = T8("Chrome", 597.3); cCC = T8("وClaude", 598.7); cPl = T8("والخطط:", 600.8)
spec8(T8("Claude", 586.5, 587.0) - 0.1 if False else 589.9, T8("Codex", 605.0) - 0.15, "Claude", c1, outs([
    N(c1, 1500, 330, "claude.ai: الشات", src=P6 + "claude_new_chat.jpg", w=420, ar=1120 / 380, size=20),
    N(cP, 1500, 520, "Projects: فولدر لكل مشروع بملفاته وتعليماته", emo="file_folder", size=18),
    N(cC, 1500, 650, "Connectors: يتوصل بأي أداة (MCP)", src=V8 + "connectors_ui.mp4", w=300, ar=1020 / 794, size=18),
    N(cS, 960, 330, "Skills: كراسات خبرة بيقراها لما يحتاجها", src=P6 + "claude_skill_row.jpg", w=380, size=18),
    N(cCh, 960, 600, "Claude in Chrome: بيدوس ويكتب في الصفحة بنفسه", src=V8 + "claude_session_2x.mp4", w=360, ar=1280 / 1004, loop=8, size=18),
    N(cCC, 420, 420, "Claude Code: بيشتغل على ملفاتك وبيعمل الحاجة", logo=LG("claude.svg"), size=18),
    TY(cCC + 0.4, 420, 520, "«قص الصمت من الفيديو ده»\n✓ قرا الفيديو\n✓ قص 37 سكتة\n✓ حفظ video_cut.mp4", w=360, rtl=True, size=17, dur=20)], cPl - 0.15) + [
    B(cPl + 0.2, 1300, 820, 60, 20, "Pro", logo=LG("claude.svg")), B(T8("وMax", 603.0), 960, 820, 300, 100, "Max", logo=LG("claude.svg")),
    B(T8("وUltra", 604.2), 620, 820, 560, 200, "Ultra", logo=LG("claude.svg"))])
# notes 39/40/41/42: MCP explained step by step (no code), his real Claude session, his real connectors
m1 = T8("الـ", 702.8); mHow = T8("إزاي", 709.1); mMenu = T8("بيعرض", 710.6); mRead = T8("بيقرا", 716.6); mPick = T8("ويختار", 717.8); mSend = T8("ويبعتلها", 719.4); mRes = T8("والنتيجة", 720.5)
mSet = T8("تفتح", 723.7); mBl = T8("ولـ", 730.6); mDv = T8("ولبرامج", 740.5); mGp = T8("ونفس", 745.1); m4 = T8("HeyGen", 747.0); mBC = T8("وبعدين", 750.9); mTy = T8("يعني", 757.1); mThis = T8("والفيديو", 760.4); mFree = T8("المجاني", 766.1)
spec8(m1 - 0.1, mHow - 0.1, "الـ MCP = فيشة موحدة", m1, [
    N(m1 + 0.3, 1450, 470, "أي AI", logo=LG("claude.svg"), size=24), N(m1 + 0.8, 960, 470, "MCP", emo="electric_plug", size=34, bg="mustard"),
    N(m1 + 1.4, 470, 470, "أي برنامج", emo="desktop_computer", size=24), E(m1 + 0.9, 1330, 470, 1080, 470), E(m1 + 1.5, 840, 470, 590, 470),
    N(T8("كود", 707.8), 960, 680, "من غير كود ربط مخصوص لكل برنامج", size=22)])
spec8(mHow - 0.1, mSet - 0.1, "الـ MCP بيشتغل إزاي؟", mHow, [
    N(mMenu, 1500, 360, "1. HeyGen بيعرض «منيو» أدوات", logo=LG("heygen.ico"), size=20),
    TY(mMenu + 0.4, 1500, 470, "• اعمل فيديو أفاتار\n• ولّد صوت\n• هات الأصوات", w=330, rtl=True, head="المنيو", size=19, dur=14),
    E(mRead - 0.1, 1310, 520, 1110, 520), N(mRead, 960, 470, "2. Claude بيقرا المنيو", logo=LG("claude.svg"), size=20),
    N(mPick, 960, 620, "3. يختار: «اعمل فيديو أفاتار»", size=20),
    E(mSend - 0.1, 810, 520, 620, 520), N(mSend, 460, 360, "4. الطلب بيروح لـ HeyGen", emo="outbox_tray", size=20),
    N(mRes, 460, 540, "5. الفيديو بيرجع", src=GEN + "avatar_012_C02.mp4", w=320, loop=4, size=20, good=True)])
spec8(mSet - 0.1, mBl - 0.1, "توصّله من التطبيق.. من غير كود", mSet, [
    N(mSet, 1250, 520, "Settings ← Connectors ← Add custom connector ← Connect", src=V8 + "connectors_ui.mp4", w=620, ar=1020 / 794, loop=4.6, size=18),
    N(mSet + 1.0, 560, 470, "الـ connectors بتاعتي: ElevenLabs · HeyGen · Higgsfield · Suno", size=18),
    *[N(mSet + 1.3 + i * 0.2, 380 + i * 120, 600, logo=LG(f), size=16) for i, f in enumerate(["elevenlabs.png", "heygen.ico", "higgsfield.png", "suno.png"])]])
spec8(mBl - 0.1, m4 - 0.1, "برامج تانية بالـ MCP", mBl, outs([
    N(mBl, 1250, 460, "Blender MCP", src=P5 + "blender_mcp_repo.png", w=480, size=20),
    TY(T8("اعمل", 737.2), 1250, 650, "«اعمل كوبري على النيل»", w=360, rtl=True, size=20, dur=12),
    N(T8("فيبني", 739.4), 620, 460, "← بيبني المشهد", src="output/blockouts_v6/bridge_static_blockout.mp4", w=420, loop=6, size=20)], mDv - 0.15) + [
    N(mDv, 1250, 470, "DaVinci Resolve MCP: يقص ويرتب", src=P5 + "davinci_mcp.png", w=440, size=20),
    N(mGp, 600, 470, "نفس الفيشة مع ChatGPT", logo=LG("chatgpt.png"), sub="من Developer mode", size=22)])
four = [("HeyGen", "heygen.ico", 1560), ("وElevenLabs", "elevenlabs.png", 1200), ("وHiggsfield", "higgsfield.png", 840), ("وSuno", "suno.png", 480)]
spec8(m4 - 0.1, mFree - 0.6, None, None, outs(
    [N(T8(w_, m4 - 0.2), x, 360, logo=LG(f), label=w_.lstrip("و"), sub="عنده MCP", size=20) for w_, f, x in four], mBC - 0.15) + outs([
    N(mBC, 960, 270, "Blender بالكود (بالـ MCP)", logo=LG("blender.svg"), size=22),
    TY(mBC + 0.4, 1450, 340, "camera.location.z += 0.2\nsun.rotation_euler.x -= 0.02\npart.location = target", w=380, head="Python", size=17, dur=20),
    N(T8("الكاميرا", 753.2), 1250, 600, "الكاميرا بتطير", src=V8 + "b3d_camera_fly.mp4", w=360, loop=4, size=20),
    N(T8("والشمس", 754.4), 760, 600, "الشمس بتغرب", src=V8 + "b3d_sun_set.mp4", w=360, loop=4, size=20),
    N(T8("والقطع", 755.7), 960, 840, "القطع بتتركب", src=CL + "clip_201_C11.mp4", w=260, loop=4, size=18)], mTy - 0.15) + [
    N(mTy, 960, 300, "تكتب جملة.. وClaude يفتح الأداة ويشتغل", emo="speech_balloon", size=24),
    N(mThis, 960, 560, "الفيديو ده نفسه: من جوه Claude بس.. من غير ما أفتح أي برنامج تاني", src=V8 + "claude_session_2x.mp4", w=600, ar=1280 / 1004, loop=10, size=20, good=True)])
# note 44/45: «made with» tree at the end of MCP — right HyperFrames logo, more space, names under the MCP logos
lib = [("Whisper", "whisper.png"), ("وRemotion", "remotion.png"), ("وHyperFrames", "hyperframes-site.svg"), ("وthree.js", "threejs.ico"), ("وBlender", "blender.svg"), ("وffmpeg", "ffmpeg.ico")]
it = [N(mFree - 0.4, 960, 335, logo=LG("claude.svg"), label="Claude Code", size=24, bg="mustard"),   # v8 review: below the title
      N(mFree - 0.1, 520, 470, "MCPs", size=22), E(mFree - 0.1, 880, 400, 560, 445), N(mFree - 0.1, 1400, 470, "libraries ببلاش على الجهاز", size=22), E(mFree - 0.1, 1040, 400, 1360, 445)]
it += [N(mFree + 0.2 + i * 0.2, 260 + i * 170, 620, logo=LG(f), label=n, size=16) for i, (f, n) in enumerate([("heygen.ico", "HeyGen"), ("elevenlabs.png", "ElevenLabs"), ("higgsfield.png", "Higgsfield"), ("suno.png", "Suno")])]
aft = mFree + 1
for i, (w_, f) in enumerate(lib):
    t = T8(w_, aft, aft + 0.8); aft = t + 0.2
    it.append(dict(N(t, 1180 + (i % 3) * 220, 600 + (i // 3) * 170, logo=LG(f), label=w_.lstrip("و"), size=16), s=90))
it.append(N(T8("ببلاش", aft, aft + 1), 960, 900, "كل دول ببلاش وعلى الجهاز", size=22, good=True))
spec8(mFree - 0.5, T8("الجهاز.", aft) + 1.6, "الفيديو ده اتعمل من جوه Claude Code", mFree - 0.4, it)

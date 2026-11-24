"""v6 scenes for Aly's 50 notes on rough cut v5 (review_rough_v5_notes.md), written directly in v6 time (words_v6.json).
make_props_v8 uses SPECS from here = the v5 specs (already moved to v6 time, some patched below) + the new ones.
Item helpers come from v6_specs (N node, E edge, B price bar, W wave, TY typed, SC scan)."""
import json, glob
import v7_specs as base
from v7_specs import N, E, B, W, TY, SC, lg, KF, CL, EV, PD, GEN

WORDS = json.load(open("work/words_v6.json", encoding="utf-8"))
MISS6 = []
def T(word, after, default=None, win=20):
    key = word.split()[0].lower()
    for w in WORDS:
        if w["a"] >= after - 0.3 and key in w["w"].lower():
            if w["a"] - after > win: break
            return round(w["a"], 3)
    MISS6.append((word, after)); return round(default if default is not None else after, 3)

V6 = "assets/v6/"; HG = "assets/ai/heygen/v6/"; HF6 = "assets/ai/higgsfield/clips_v6/"; P6 = "research/pages_v6/"; P5 = "research/pages_v5/"
PI = "work/pdf_imgs/"; CH = "assets/channel/"
SPECS = []
def spec(a, b, title=None, title_t=None, items=(), circle=False, sfx=()):
    SPECS.append(dict(a=round(a, 3), b=round(b, 3), title=title, title_t=title_t, items=list(items), circle=circle, sfx=list(sfx)))
def outs(items, t):   # a group leaves TOGETHER (note 4)
    for it in items: it["out_t"] = round(t, 3)
    return items
def num(t, x, y, to, label, out=None, big=False):
    d = dict(k="num", t=t, x=x, y=y, to=to, label=label)
    if big: d["big"] = True
    if out is not None: d["out_t"] = out
    return d
def thumbqr(t, x, y, vid, label=None, w=330):
    return [N(t, x, y, label, src=CH + f"thumb_{vid}.jpg", w=w), N(t + 0.25, x, y + w * 0.28 + 75, src=CH + f"qr_{vid}.png", w=100, ar=1)]

# ======================= patches on the v5 specs (already in v6 time) =======================
def find(sub):
    for s in base.SPECS:
        for it in s["items"]:
            if sub in str(it.get("label", "")) or sub in str(it.get("src", "")) or sub in str(it.get("text", "")): return s
    return None
s = find("face_real.jpg")        # note 1: the GENERATED face, not the real one
if s:
    for it in s["items"]:
        if it.get("src", "").endswith("face_real.jpg"): it["src"] = V6 + "face_gen.jpg"; it["sub"] = "الوش المتولّد"; it["ar"] = 1
s = find("demo_refs.jpg")        # note 6: his character sheet beside the reference pictures
if s:
    for it in s["items"]:
        if it.get("src", "").endswith("demo_refs.jpg"): it["src"] = V6 + "refs_plus_sheet.jpg"; it["ar"] = 1802 / 600; it["label"] = "صور مرجع + الـ character sheet بتاعي"
s = find("bridge_blockout.mp4")  # note 22: the Blender bridge stays STILL like the generated one
if s:
    for it in s["items"]:
        if "bridge_blockout" in it.get("src", ""): it["src"] = "output/blockouts_v6/bridge_static_blockout.mp4"
s = find("ريلي اللي اتعمل بـ Genjutsu")   # note 12 + 42: no PDF page; the real insights graph + 253K in both languages
if s:
    s["items"] = [it for it in s["items"] if not str(it.get("src", "")).endswith("p23.png")]
    for it in s["items"]:
        if it.get("k") == "num": it["label"] = "253K · 253 ألف مشاهدة على فيسبوك"
    t0 = min(it["t"] for it in s["items"] if it.get("k") == "num")
    s["items"] += [N(t0 - 0.3, 640, 380, "ريل Genjutsu: داشبورد فيسبوك", src=PI + "p23_0.png", w=460, ar=798 / 412)]
s = find("looks: مكان ولبس جديد")         # replaced by the whole avatar section (note 14)
if s: base.SPECS.remove(s)
s = find("Avatar 6: twin")                # note 26: credits THIS video used on HeyGen
if s:
    tb = max(it["t"] for it in s["items"] if it.get("k") == "bar")
    s["items"] += [N(tb + 0.6, 1560, 690, "الفيديو ده صرف 209 كريدت HeyGen", sub="من 600 في الشهر", size=22, bg="mustard")]
s = find("Seedance 2.5 · 4K")             # notes 27/28: the roof STAYS + his Higgsfield pricing video (thumb + QR)
if s:
    for it in s["items"]:
        if it.get("k") == "edge" and it.get("arrow") is False: it.pop("out_t", None)
        if str(it.get("logo", "")).endswith("higgsfield.png") and it.get("size") == 22: it.pop("out_t", None)
    tb = max(it["t"] for it in s["items"] if it.get("k") == "bar")
    s["items"] += [N(tb + 0.8, 1560, 640, "فيديو تسعيرة Higgsfield", src=CH + "thumb_10UXB0cT4Ss.jpg", w=260), N(tb + 1.0, 1560, 800, src=CH + "qr_10UXB0cT4Ss.png", w=95, ar=1)]
s = find("حركة الكاميرا بتختارها")        # note 11: «لغة السينما» thumb + QR at the end of the camera moves
if s:
    s["items"] = [it for it in s["items"] if it.get("k") != "edge"]
    te = max(it["t"] for it in s["items"])
    pass
s = find("claude.ai")                     # note 47: Claude pictures from the APP, not the CLI
if s:
    for it in s["items"]:
        if it.get("k") == "typed" and it.get("head") == "claude.ai":
            t_ = it.get("t", s["a"] + 1); it.clear(); it.update(N(t_, 1470, 300, "claude.ai: الشات", src=P6 + "claude_new_chat.jpg", w=400, ar=1120 / 380))
        if it.get("label", "").startswith("Connectors"): it.update(dict(src=P6 + "claude_connectors.jpg", w=330, ar=1610 / 850, y=600)); it.pop("emo", None); it.pop("size", None)
        if it.get("label", "").startswith("Skills"): it["y"] = 790
s = find("lab_blockout.mp4")   # inside the numbered tricks now (trick 6)
if s: base.SPECS.remove(s)
for s_ in base.SPECS:
    for it in s_["items"]:
        if "t" not in it: it["t"] = s_["a"] + 0.5

# ======================= new scenes =======================
# note 5 (+ order): model ≠ tool ≠ workflow — logos on their words, the REAL Magnific page
a = T("أول", 62.8, 63.0); tm, tt_, tw = T("الموديل", 66.8, 67.0), T("الأداة", 71.3, 71.5), T("والـ", 75.0, 75.2)
spec(a, T("طب", 80.4, 80.6) - 0.1, "الموديل ≠ الأداة ≠ الـ workflow", a + 0.1, [
    N(tm, 1480, 290, "الموديل: العقل اللي بيولّد", emo="brain", size=24),
    N(T("Seedance", tm), 1600, 430, logo=lg("seedance.ico"), label="Seedance", size=20), N(T("Kling", tm), 1480, 540, logo=lg("kling.png"), label="Kling", size=20),
    N(T("Veo", tm), 1360, 430, logo=lg("veo.ico"), label="Veo", size=20),
    N(tt_, 960, 290, "الأداة: الموقع اللي بتكتب فيه", emo="globe_with_meridians", size=24),
    N(T("Higgsfield", tt_), 960, 420, logo=lg("higgsfield.png"), label="Higgsfield", size=20),
    N(T("Magnific", tt_), 960, 610, "Magnific", src=P6 + "magnific_home.jpg", w=420, ar=1008 / 326),
    N(tw, 440, 290, "الـ workflow: الترتيب", emo="footprints", size=24),
    N(T("صورة", tw), 440, 430, "1. صورة", src=KF + "kf_026_C02b.png", w=220), N(T("فيديو", tw + 1), 440, 590, "2. فيديو", src=CL + "clip_026_C02b.mp4", w=220, loop=4),
    E(T("فيديو", tw + 1), 440, 495, 440, 525), N(T("صوت", tw + 1.5), 440, 750, "3. صوت", emo="speaker_high_volume", size=22), E(T("صوت", tw + 1.5), 440, 665, 440, 715)])

# note 9: start frame + end frame in 3 steps, and WHERE they go in Higgsfield
a = T("frame", 150.4, 151.1)
spec(a - 0.1, T("وفيه", 155.5, 155.8) - 0.1, "أول صورة وآخر صورة", a, [
    N(a, 1470, 380, "1. أول صورة", src=V6 + "frame_start.jpg", w=340), N(T("وend", a), 450, 380, "2. آخر صورة", src=V6 + "frame_end.jpg", w=340),
    N(T("اللي", a + 1.5), 960, 380, "3. الموديل بيعمل اللي في النص", src=CL + "clip_026_C02b.mp4", w=340, loop=5),
    E(T("اللي", a + 1.5), 1290, 380, 1140, 380), E(T("اللي", a + 1.5), 630, 380, 780, 380),
    SC(a + 1.2, 960, 720, P6 + "hf_frames_slot.jpg", w=200, ar=466 / 604, boxes=[dict(x=36, y=46, w=28, h=9, label="Frames"), dict(x=3, y=58, w=94, h=40, label="هنا الصور")]),
    N(a + 1.4, 1330, 720, "في Higgsfield: أول صورة = البداية", size=20)])

# note 10/11: the models, each logo ON its name
a = T("الموديلات", 160.0, 160.2)
mods = [("Seedance", "seedance.ico"), ("وKling", "kling.png"), ("وVeo", "veo.ico"), ("وWan", "wan.ico"), ("وMiniMax", "minimax.ico")]
it = []; aft = a
for i, (w_, f) in enumerate(mods):
    t = T(w_, aft, aft + 0.6); aft = t + 0.1
    it.append(N(t, 1500 - i * 270, 520, logo=lg(f), label=w_.lstrip("و"), size=24))
it += [N(a + 0.3, 1100, 790, "حركات الكاميرا بالتفصيل: «لغة السينما»", src=CH + "thumb_S-tSUtClTOg.jpg", w=250), N(a + 0.5, 850, 790, src=CH + "qr_S-tSUtClTOg.png", w=100, ar=1)]
spec(a - 0.1, T("وفيه", 165.4, 165.6) - 0.1, "الموديلات المشهورة دلوقتي", a, it)

# note 14 (+ 15, 16, 24): the AVATAR section — big avatar, then a CIRCLE at the top while the examples play under it
a = T("HeyGen", 194.8, 195.0); SKIP0 = 193.25
tl, tls, tex, tdb, tq = T("looks", 201.4, 201.6), T("lipsync", 206.2, 206.4), T("وجربنا", 210.8, 211.0), T("دبلجة", 224.0, 224.6), T("والقاعدة", 229.0, 229.1)
g1 = outs([N(a, 1480, 420, logo=lg("heygen.ico"), label="HeyGen", size=24),
           N(T("نسخة", a + 1), 1480, 650, "digital twin = إنت نفسك", src=GEN + "avatar_012_C02.mp4", w=320, loop=4, sub="من فيديو حوالي 15 ث"),
           N(a + 1.0, 560, 520, "بدايل: Synthesia · D-ID · Hedra · Captions", size=22),
           N(a + 1.3, 560, 640, "كل واحد ليه أفاتار بيتكلم", size=18)], tl - 0.15)
looks = [(GEN + "avatar_015_C02.mp4", "الستوديو"), (HG + "look_beach.mp4", "البحر"), (HG + "look_room_black.mp4", "أوضة تانية"), (HG + "look_presenter.mp4", "مقدم واقف")]
g2 = outs([N(tl, 960, 430, "Looks: نفس الـ twin.. بلبس ومكان تاني", size=24)] +
          [N(T("لبس", tl) + 0.35 * i, 1440 - i * 320, 640, nm, src=src, w=290, loop=3.5) for i, (src, nm) in enumerate(looks)], tls - 0.15)
g3 = outs([N(tls, 960, 430, "lip sync: البق يمشي على كلام جديد", size=24),
           N(tls + 0.4, 1460, 640, "قبل: فيديو حقيقي", src=HG + "lipsync_src_realroom_a.mp4", w=290, loop=3.8),
           N(tls + 1.0, 1140, 640, "بعد: كلام جديد", src=HG + "lipsync_ex_realroom.mp4", w=290, loop=3.8), E(tls + 1.0, 1300, 640, 1290, 640, arrow=False),
           N(tls + 1.6, 780, 640, "قبل: الستوديو", src=HG + "lipsync_src_S4g_a.mp4", w=290, loop=3.8),
           N(tls + 2.2, 460, 640, "بعد: كلام جديد", src=HG + "lipsync_ex_S4g.mp4", w=290, loop=3.8)], tex - 0.15)
g4 = outs([N(tex, 960, 430, "جربنا التلاتة في الفيديو ده", size=24),
           N(T("صورة", tex), 1460, 640, "صورة واحدة: الحركة زيادة ✗", src="assets/ai/heygen/test_S001_avatar.mp4", w=320, loop=4),
           N(T("ومن", tex + 4), 960, 640, "lip sync: البق ظبط.. العين والجسم لأ ✗", src=HG + "lipsync_ex_realroom.mp4", w=320, loop=3.8),
           N(T("والـ", tex + 9), 460, 640, "الـ twin كان الأحسن ✓", src=GEN + "avatar_012_C02.mp4", w=320, loop=4, good=True)], tdb - 0.15)
g5 = outs([N(tdb, 1300, 560, "دبلجة: نفس الفيديو بلغة تانية", emo="globe_showing_europe-africa", size=26), W(tdb + 0.3, 700, 560, w=420, h=110),
           N(tdb + 1.5, 700, 700, "بنفس الصوت.. والبق ماشي معاها", size=20)], tq - 0.1)
g6 = [N(tq, 960, 430, "القاعدة", bg="mustard", size=30),
      N(T("بموافقته", tq), 960, 600, "وش أي حد وصوته.. بموافقته بس", emo="handshake", size=28, good=True),
      N(T("بموافقته", tq) + 0.6, 1440, 760, "HeyGen بيطلب فيديو موافقة", emo="video_camera", size=20),
      N(T("بموافقته", tq) + 0.9, 480, 760, "من غير موافقة = مينفعش", emo="no_entry", size=20)]
spec(a - 0.1, 232.6, None, None, [dict(k="circle", t=a, x=960, y=235, r=118, src=HG + "avatar_section_circle.mp4", skip=round(a - 0.1 - SKIP0, 3))] + g1 + g2 + g3 + g4 + g5 + g6)

# notes 20-22: 3D — a picture or a clip on EVERY word
a = T("3D", 291.8, 292.0); tb, tcam, tthree, tgs = T("Blender", 299.5, 299.8), T("الكاميرا", 300.9, 301.0), T("three.js", 305.5, 305.7), T("Gaussian", 308.2, 308.4)
spec(a - 0.25, T("وأحسن", 312.3, 312.5) - 0.1, "الـ 3D", a, outs([
    N(T("صورة", a), 1480, 430, "صورة", src=KF + "kf_171_C09.png", w=330),
    E(T("موديل", a + 2), 1300, 430, 1170, 430), N(T("موديل", a + 2), 960, 430, "← موديل 3D تلف حواليه", src=HF6 + "jet_from_image_turntable.mp4", w=380, loop=6, sub="sam 3D في Higgsfield"),
    TY(tb, 440, 430, "import bpy\ncam.location.z += 0.2\nsun.rotation_euler.x -= 0.02\npart.location = target", w=400, head="Blender · Python", size=19, dur=30),
    N(tcam, 1480, 740, "الكاميرا بتطير", src=CL + "clip_213_C11.mp4", w=300, loop=4),
    N(T("والشمس", tcam), 960, 740, "الشمس بتغرب", src=CL + "clip_032_C02b.mp4", w=300, loop=4),
    N(T("والقطع", tcam + 1), 440, 740, "القطع بتتركب", src=CL + "clip_201_C11.mp4", w=300, loop=4)], tthree - 0.15) + [
    N(tthree, 1330, 440, "three.js: 3D جوه الكود", src=P5 + "threejs_home.png", w=500),
    TY(tthree + 0.5, 1330, 730, "const mesh = new THREE.Mesh(geo, mat)\nscene.add(mesh)\nrenderer.render(scene, camera)", w=460, head="three.js", size=18, dur=30),
    N(tgs, 590, 440, "Gaussian splats: تصوير مكان ← مشهد 3D", src=P5 + "splats_inria.png", w=500),
    N(tgs + 1.2, 590, 720, "صور كتير لمكان حقيقي ← سحابة نقط بتتلف", emo="camera_with_flash", size=20)])

# note 29: the Suno SITE as a mind map
a = T("Suno", 449.3, 449.4)
k = [T("Simple", a), T("v6", a + 4.5), T("Voices", a + 8.5), T("وStems", a + 9.5, a + 10.5), T("Studio", a + 10.5, a + 12), T("Warner", a + 16, a + 18), T("MCP", a + 20, a + 22)]
c = (960, 520)
def br(t, x, y, *nodes):
    return [E(t - 0.1, c[0] + (x - c[0]) * 0.2, c[1] + (y - c[1]) * 0.2, x + (c[0] - x) * 0.25, y + (c[1] - y) * 0.25)] + list(nodes)
spec(a - 0.1, 475.4, None, None, [N(a, 960, 520, logo=lg("suno.png"), label="Suno", size=30, bg="mustard")] +
     br(k[0], 1460, 290, N(k[0], 1460, 290, "Create", sub="Simple: فكرة · Custom: كلمات + ستايل", size=24)) +
     br(k[1], 1560, 540, N(k[1], 1560, 540, "v6 · v6-mini · v6-wild", sub="النسخة السادسة", size=24)) +
     br(k[2], 1440, 800, N(k[2], 1440, 800, "Voices: تغني بصوتك", emo="microphone", size=22)) +
     br(k[3], 960, 840, N(k[3], 960, 840, "Stems: الفوكال لوحده والطبلة لوحدها", size=22)) +
     br(k[4], 480, 800, N(k[4], 480, 800, "Suno Studio 2.0", sub="مونتاج مزيكا في المتصفح", emo="level_slider", size=22)) +
     br(k[5], 400, 540, N(k[5], 400, 470, "اتعمل مع شركات مزيكا", size=20), N(k[5] + 0.2, 280, 580, logo=lg("warner.png"), size=20),
        N(T("BMG", k[5], k[5] + 0.6), 400, 600, logo=lg("bmg.ico"), size=20), N(T("Believe", k[5], k[5] + 1.0), 520, 580, logo=lg("believe.png"), size=20)) +
     br(k[6], 480, 290, N(k[6], 480, 290, "Suno MCP · أكتوبر (تجريبي)", logo=lg("claude.svg"), size=22)))

# note 34: free on your PC — an example under every tool
a = 475.5; tc = T("ComfyUI", a); to = T("Firefly", a + 15, a + 19)
spec(a - 0.1, T("قبل", 498.2, 500.0) - 0.15, "على جهازك ببلاش", a, [
    N(tc, 1460, 290, logo=lg("comfyui.png"), label="ComfyUI", size=24),
    N(tc + 0.8, 1660, 420, "وصف", size=20), N(tc + 1.1, 1460, 420, "موديل", size=20), N(tc + 1.4, 1260, 420, "فيديو", size=20),
    E(tc + 0.9, 1610, 420, 1515, 420), E(tc + 1.2, 1405, 420, 1315, 420),
    N(T("LTX", tc), 1660, 580, logo=lg("ltx.png"), label="LTX 2.5: 4K + صوت", size=18), N(T("وWan", tc + 4), 1460, 580, logo=lg("wan.ico"), label="Wan", size=18),
    N(T("وFlux", tc + 5), 1260, 580, logo=lg("flux.png"), label="Flux: صور", size=18), N(T("وQwen", tc + 5.5), 1460, 700, logo=lg("qwen.png"), label="Qwen", size=18),
    N(T("لـ", tc + 10, tc + 11.5), 1360, 830, "nodes لـ HeyGen + Comfy Cloud لو جهازك ضعيف", logo=lg("heygen.ico"), size=18),
    N(to, 760, 330, logo=lg("firefly.png"), label="Firefly", sub="توسيع وتعديل صور", size=20), N(T("وRunway", to), 440, 330, logo=lg("runway.png"), label="Runway", sub="فيديو وتعديل فيديو", size=20),
    N(T("وLuma", to), 760, 620, logo=lg("luma.ico"), label="Luma", sub="فيديو + 3D", size=20), N(T("وCapCut", to), 440, 620, logo=lg("capcut.ico"), label="CapCut", sub="مونتاج + كابشن", size=20)])

# notes 32/35: what an LLM and an agent are; chat / Cowork / Code; «made inside Claude Code»
a = 500.0; tag, tdl, tsh, tdev, tcc = T("agent", a + 8), T("بتكلّمه", a + 15), T("شات", a + 20), T("developer", a + 30), T("والفيديو", a + 34)
spec(a, 542.2, None, None, outs([
    N(T("LLM", a), 1460, 300, "LLM = موديل اتدرب على كلام كتير جداً", emo="brain", size=24),
    N(T("فبيفهم", a + 3), 1460, 430, "بيفهم · بيكتب · بيخطط", size=20),
    E(tag, 1300, 330, 1120, 330), N(tag, 960, 300, "agent = LLM ليه إيدين", emo="robot", size=24),
    N(T("ملفات", tag), 960, 430, "بيفتح ملفات", emo="open_file_folder", size=20), N(T("برامج", tag), 960, 520, "بيشغّل برامج", emo="gear", size=20),
    N(T("النتيجة", tag), 960, 610, "يشوف النتيجة ويصلّح", emo="eyes", size=20),
    E(tdl, 800, 330, 620, 330), N(tdl, 470, 300, "بتكلّمه وتفكّروا سوا.. وهو اللي يشتغل", emo="speech_balloon", size=22, good=True),
    N(T("التوليد", tdl + 3), 470, 470, "حتى التوليد بيعمله بنفسه", emo="sparkles", size=20)], tsh - 0.2) + [
    N(T("الشات", tsh), 1460, 400, "الشات: كلام وتفكير", src=P6 + "claude_new_chat.jpg", w=420, ar=1120 / 380),
    N(T("وCowork", tsh), 960, 400, "Cowork: بيشتغل على ملفاتك وبرامجك", emo="desktop_computer", size=22),
    TY(T("وCode", tsh), 460, 400, "> claude\n✓ كتب السكريبت\n✓ ولّد الصوت\n✓ رندر الفيديو", w=380, head="Claude Code", size=19, dur=28),
    N(tdev, 460, 600, "الكود مش علشان تبقى developer.. علشان يخلّص شغلك", size=19),
    N(tcc, 960, 780, "الفيديو ده كله اتعمل من جوه Claude Code", logo=lg("claude.svg"), size=28, bg="mustard", good=True)])

# note 31: Codex — desktop app, terminal, skills, local models; the Gemini CLI correction
a = max(580.0, T("Codex", 578.0, 580.0)); toss, tfix = T("--oss", a + 5, a + 6), T("وتصحيح", a + 10, a + 10.8)
spec(a - 0.1, 603.0, None, None, [N(a, 960, 240, logo=lg("openai-codex.png"), label="Codex من OpenAI", size=26)] + outs([
    N(T("تطبيق", a), 1460, 450, "تطبيق على الكمبيوتر", src=P5 + "codex_app.png", w=420),
    TY(T("التيرمينال", a), 960, 470, "> codex\n✓ قرا المشروع\n✓ عدّل 3 ملفات", w=360, head="Terminal", size=19, dur=25),
    N(T("الـ", a + 3), 470, 450, "skills بنفس المعيار المفتوح", emo="notebook", size=22),
    TY(toss, 1300, 730, "codex --oss", w=280, head="موديل على جهازك", size=22, dur=15),
    N(toss + 0.6, 900, 730, logo=lg("ollama.png"), label="Ollama", size=20), N(toss + 0.9, 640, 730, logo=lg("lmstudio.ico"), label="LM Studio", size=20)], tfix - 0.15) + [
    N(tfix + 0.4, 1400, 500, "Gemini CLI: وقف للأفراد 18 يونيو 2026", logo=lg("gemini.png"), size=22),
    E(tfix + 1.5, 1180, 500, 760, 500), N(tfix + 1.6, 540, 500, "Antigravity CLI", logo=lg("antigravity.png"), size=24),
    N(T("والـ", tfix + 5), 960, 720, "extensions ← اسمها بقى plugins", size=22)])

# Chinese models: every logo ON its name
a = 603.1
ch = [("Kimi", "kimi.ico", "Kimi K3.1"), ("وDeepSeek", "deepseek.ico", "DeepSeek V4.1"), ("وQwen", "qwen.png", "Qwen"), ("وGLM", "glm.png", "GLM"),
      ("وMiniMax", "minimax.ico", "MiniMax M3: كلام"), ("وMiniMax", "minimax.ico", "MiniMax H3: فيديو")]
it = []; aft = a + 1
for i, (w_, f, lab) in enumerate(ch):
    t = T(w_, aft, aft + 0.8); aft = t + 0.3
    it.append(N(t, 1640 - i * 265, 430, logo=lg(f), label=lab, size=20))
tv = T("وكتير", a + 11, a + 12.3)
it = outs(it, tv - 0.1) + [N(tv, 960, 330, "موديلات الفيديو اللي بنستخدمها.. صيني", size=24),
    N(T("Seedance", tv), 1360, 560, logo=lg("bytedance.png"), label="Seedance من ByteDance", size=22), N(T("وKling", tv), 960, 560, logo=lg("kling.png"), label="Kling", size=22),
    N(T("وWan", tv), 560, 560, logo=lg("wan.ico"), label="Wan", size=22)]
spec(a - 0.1, T("أمثلة", 623.0, 623.2) - 0.1, "الموديلات الصيني", a, it)

# agents: examples, libraries (each logo on its word), browser / computer / scheduled
a = T("أمثلة", 623.0, 623.2); tl_, tbr = T("libraries", a + 7, a + 8.2), T("agents", a + 18, a + 19)
spec(a - 0.1, T("الـ", 652.3, 652.5) - 0.15, "الـ agents بتشتغل إزاي", a, outs([
    N(T("Claude", a), 1500, 330, logo=lg("claude.svg"), label="Claude Code", size=22), N(T("وCodex", a), 1180, 330, logo=lg("openai-codex.png"), label="Codex", size=22),
    N(T("وAntigravity", a), 860, 330, logo=lg("antigravity.png"), label="Antigravity CLI", size=22), N(T("Qwen", a + 2), 540, 330, logo=lg("qwen.png"), label="Qwen Code", size=22)], tl_ - 0.15) +
    [N(T("مش", a + 5), 960, 460, "الـ agent مش بيرسم بنفسه.. بيكتب كود", emo="writing_hand", size=22)] + outs([
    N(T("Remotion", tl_), 1560, 620, logo=lg("remotion.png"), label="Remotion", sub="موشن", size=20),
    N(T("three.js", tl_), 1250, 620, logo=lg("threejs.ico"), label="three.js", sub="3D", size=20),
    N(T("وffmpeg", tl_), 960, 620, logo=lg("ffmpeg.ico"), label="ffmpeg", sub="قص وتجميع", size=20),
    N(T("وBlender", tl_), 670, 620, logo=lg("blender.svg"), label="Blender", sub="بالبايثون", size=20),
    N(T("وWhisper", tl_), 360, 620, logo=lg("whisper.png"), label="Whisper", sub="كلام ← نص", size=20)], tbr - 0.1) + [
    N(T("Chrome", tbr), 1400, 640, "Claude in Chrome: المتصفح", logo=lg("claude.svg"), size=22),
    N(T("الكمبيوتر", tbr + 2), 960, 780, "الكمبيوتر كله: ماوس وكيبورد", emo="computer_mouse", size=22),
    N(T("بتتجدول", tbr + 4), 520, 640, "مهام بتتجدول.. وإنت نايم", emo="alarm_clock", size=22)])

# notes 36/38: scripts — logos on their programs, his After Effects → code video, our own scripts
a = T("الـ", 652.3, 652.5)
spec(a - 0.1, 667.7, "سكريبتات جوه برامجك", a, [
    TY(a + 1.0, 1400, 320, "// After Effects expression\nwiggle(2, 30)", w=380, head="سكريبت", size=20, dur=20),
    N(T("After", a + 2), 1640, 540, logo=lg("adobe.png"), label="After Effects", size=20), N(T("وPremiere", a + 3), 1380, 540, logo=lg("premiere-pro-official.png"), label="Premiere", size=20),
    N(T("وPhotoshop", a + 3), 1120, 540, logo=lg("adobe.png"), label="Photoshop", size=20), N(T("وBlender", a + 3), 860, 540, logo=lg("blender.svg"), label="Blender", size=20),
    N(T("وDaVinci", a + 4), 600, 540, logo=lg("davinci-resolve.png"), label="DaVinci", size=20),
    N(T("أنيميشن", a + 6, a + 9.5), 1250, 760, "أنيميشن After Effects ← كود (فيديو على القناة)", src=CH + "thumb_5C4KNFiJFjA.jpg", w=280),
    N(T("أنيميشن", a + 6, a + 9.5) + 0.25, 1000, 790, src=CH + "qr_5C4KNFiJFjA.png", w=100, ar=1),
    N(a + 1.5, 520, 330, "سكريبتاتنا: publisher بيرفع الريلز · أوتوميشن كومنتات إنستجرام", size=19)])

# MCP = one standard plug: any AI <-> any program
a = 669.6
spec(a, 675.85, "الـ MCP", a + 0.1, [
    N(a + 0.2, 960, 420, "فيشة موحدة", emo="electric_plug", size=34, bg="mustard"),
    N(T("أي", a + 1.5), 1450, 420, "أي AI", logo=lg("claude.svg"), size=24), E(T("أي", a + 1.5) + 0.2, 1330, 420, 1110, 420),
    N(T("برنامج", a + 2.5), 470, 420, "أي برنامج", emo="desktop_computer", size=24), E(T("برنامج", a + 2.5) + 0.2, 810, 420, 590, 420),
    N(T("كود", a + 4), 960, 640, "من غير كود ربط مخصوص لكل برنامج", size=22)])

# note 39 (N2): how MCP works — tools list, connectors steps, mcp.json, Blender MCP, DaVinci MCP, ChatGPT
a = 675.9; tset, tbl, tdv, tgp = T("ولو", a + 12, a + 14), T("ولـ", a + 25, a + 27), T("ولبرامج", a + 32, a + 34), T("ونفس", a + 38, a + 40)
spec(a, 719.7, None, None, outs([
    TY(T("بيعرض", a), 1450, 380, "create_video\ncreate_speech\nlist_voices", w=360, head="HeyGen MCP tools", size=18, dur=30),
    E(T("بيقرا", a + 4), 1220, 380, 1080, 380), N(T("بيقرا", a + 4), 960, 380, logo=lg("claude.svg"), label="Claude بيقرا القايمة", size=22),
    N(T("ويختار", a + 5), 960, 520, "اختار: create_video", size=20),
    E(T("ويبعتلها", a + 6), 840, 380, 620, 380), N(T("ويبعتلها", a + 6), 470, 380, logo=lg("heygen.ico"), label="HeyGen", size=22),
    N(T("والنتيجة", a + 7), 470, 600, "النتيجة رجعت", src=GEN + "avatar_012_C02.mp4", w=300, loop=4)], tset - 0.15) + outs([
    N(T("Settings", tset), 1300, 470, "Settings ← Connectors", src=P6 + "claude_connectors.jpg", w=600, ar=1610 / 850),
    TY(T("Add", tset), 560, 380, "1. Settings\n2. Connectors\n3. Add custom connector\n4. MCP URL\n5. Connect", w=380, head="Claude", size=19, dur=30),
    TY(T("mcp.json", tset + 6, tset + 8), 560, 720, '{ "mcpServers": {\n  "heygen": { "url": "mcp.heygen.com" } } }\n> /mcp', w=420, head="Claude Code: .mcp.json", size=17, dur=25)], tbl - 0.15) + outs([
    N(tbl, 1380, 440, "Blender MCP", src=P5 + "blender_mcp_repo.png", w=500),
    TY(T("اعمل", tbl + 3), 1380, 720, "«اعمل كوبري على النيل»", w=380, rtl=True, size=22, dur=15),
    N(T("فيبني", tbl + 4), 960, 760, "← بيبني المشهد", src="output/blockouts_v6/bridge_static_blockout.mp4", w=300, loop=6),
    N(tdv, 540, 440, "DaVinci Resolve MCP: يقص ويرتب", src=P5 + "davinci_mcp.png", w=440)], tgp - 0.1) + [
    N(tgp, 960, 500, "نفس الفيشة مع ChatGPT", logo=lg("openai.png"), size=26), N(T("Developer", tgp), 960, 640, "من Developer mode", size=22)])

# MCP: the 4 tools have MCP — Claude connected to all 4 (the tree)
a = T("HeyGen", 719.6, 719.8)
four = [("HeyGen", "heygen.ico", 1560), ("وElevenLabs", "elevenlabs.png", 1200), ("وHiggsfield", "higgsfield.png", 760), ("وSuno", "suno.png", 400)]
it = []; aft = a - 0.2
for w_, f, x in four:
    t = T(w_, aft, aft + 0.7); aft = t + 0.2
    it += [N(t, x, 620, logo=lg(f), label=w_.lstrip("و"), size=22)]
tc = T("Claude", a + 4, a + 5)
it += [N(tc, 960, 330, logo=lg("claude.svg"), label="Claude", size=28, bg="mustard")] + [E(tc + 0.2 + i * 0.15, 960, 380, x, 560) for i, (_, _, x) in enumerate(four)]
it += [N(T("نفسه", a + 7, a + 8), 960, 800, "الفيديو ده نفسه: Claude متوصّل بالأربعة في نفس الوقت", size=22, good=True)]
spec(a - 0.1, 731.5, "الـ MCP", a, it)

# notes 40/41 (N3): skills explained simply
a = 733.3; tset = T("في", 753.5, 754.5); tvm = T("ومثال", a + 30, a + 32)
spec(a, 771.5, None, None, outs([
    N(a + 0.1, 960, 300, "skill = كراسة خبرة", emo="notebook", size=28, bg="mustard"),
    TY(T("SKILL.md", a + 1), 1430, 470, "---\nname: aly-video-motion\ndescription: motion the way Aly likes\n---\n1. read the style number\n2. never cut a word", w=440, head="SKILL.md", size=17, dur=35),
    N(T("سكريبتات", a + 4), 1430, 720, "+ سكريبتات وأمثلة", emo="page_facing_up", size=20),
    N(T("بتتبني", a + 7), 960, 470, "بتتبني إزاي؟", size=22),
    N(T("بتكتب", a + 8), 960, 580, "1. اللي بتعمله كل مرة بالترتيب", size=19), N(T("واللي", a + 10), 960, 670, "2. اللي اتعلمته من غلطاتك", size=19),
    N(T("وأهميتها", a + 12), 490, 470, "ليه مهمة؟", size=22),
    N(T("الصفر", a + 14), 490, 580, "مش بيبدأ من الصفر كل مرة", size=19), N(T("بأسلوبك", a + 15), 490, 670, "بيشتغل بأسلوبك", size=19),
    N(T("يحتاجها", a + 16), 490, 760, "بيقراها بس لما يحتاجها", size=19),
    N(T("واللي", a + 10) + 1.0, 960, 790, "خبرة فوق خبرة", emo="building_construction", size=20)], tset - 0.15) + outs([
    N(tset, 1400, 430, "في Claude: Skills", src=P6 + "claude_connectors.jpg", w=520, ar=1610 / 850),
    TY(T("اعملّي", tset + 2), 1400, 720, "«اعملّي skill»", w=300, rtl=True, size=22, dur=12),
    TY(T("Claude", tset + 5), 960, 760, ".claude/skills/aly-video-motion/SKILL.md", w=520, head="Claude Code", size=18, dur=20),
    N(T("ChatGPT", tset + 5), 470, 420, "ChatGPT و Codex: Skills بنفس الفكرة", logo=lg("openai.png"), size=20)], tvm - 0.15) + [
    N(tvm, 1300, 500, "الـ video maker بتاعنا", src=PI + "p06_4.png", w=260, ar=753 / 741, sub="skill فيها كل اللي عجب علي"),
    N(T("غلطة", tvm + 2), 700, 420, "كل غلطة اتسجلت.. متتكررش", emo="no_entry", size=20),
    N(T("وعشرين", tvm + 3), 700, 640, "عشرين ستايل برقم", src=PI + "p09_1.png", w=340)])

# skills = open standard (logos on words) + what the skills here are (note 41: reels/IG are SCRIPTS, not skills)
a = T("وده", 771.4, 771.6)
spec(a - 0.1, 783.5, None, None, [
    N(a, 960, 320, "معيار مفتوح", size=26),
    N(T("Claude", a + 1), 1400, 520, logo=lg("claude.svg"), label="Claude Code", size=22), N(T("وCodex", a + 1), 960, 520, logo=lg("openai-codex.png"), label="Codex", size=22),
    N(T("Antigravity", a + 2), 520, 520, logo=lg("antigravity.png"), label="Antigravity: جوه الـ plugins", size=22),
    N(T("أمثلة", a + 6), 960, 730, "skill بتكتب السكريبت بأسلوب صاحب القناة", src=PI + "p10_6.png", w=120, ar=753 / 741)])

# note 33: «made inside Claude Code» = a TREE: Claude Code → MCPs + free libraries
a = 783.6
lib = [("Whisper", "whisper.png"), ("وRemotion", "remotion.png"), ("وHyperFrames", "hyperframes.ico"), ("وthree.js", "threejs.ico"), ("وBlender", "blender.svg"), ("وffmpeg", "ffmpeg.ico")]
it = [N(a, 960, 260, logo=lg("claude.svg"), label="Claude Code", size=28, bg="mustard"),
      N(a + 0.4, 520, 400, "MCPs", size=22), E(a + 0.4, 900, 300, 560, 380), N(a + 0.4, 1400, 400, "libraries ببلاش على الجهاز", size=22), E(a + 0.4, 1020, 300, 1360, 380)]
it += [N(a + 0.7 + i * 0.25, 260 + i * 170, 580, logo=lg(f), size=20) for i, f in enumerate(["heygen.ico", "elevenlabs.png", "higgsfield.png", "suno.png"])]
aft = a + 2
for i, (w_, f) in enumerate(lib):
    t = T(w_, aft, aft + 0.8); aft = t + 0.2
    it.append(N(t, 1180 + (i % 3) * 210, 560 + (i // 3) * 170, logo=lg(f), label=w_.lstrip("و"), size=20))
it.append(N(T("ببلاش", a + 10, a + 11), 960, 860, "كل دول ببلاش وعلى الجهاز", size=22, good=True))
spec(a - 0.1, 796.7, "الفيديو ده اتعمل من جوه Claude Code", a, it)

# notes 42/36: the REAL experience — the PDF rebuilt as motion (its pictures, counters, logos), not page screenshots
a = 798.5; tb4, told, tres, tles = T("اللي", 814.8, 815.0), T("والفيديوهات", 838.4, 838.6), T("والنتيجة", 844.2, 844.4), T("والدروس", 858.3, 858.5)
plats = ["youtube.png", "instagram.ico", "facebook.png", "tiktok.png"]
spec(a, 872.5, "تجربة حقيقية بالأرقام", a + 0.2, outs([
    N(T("software", a + 2), 1460, 380, "software tester full-time", emo="technologist", size=22),
    N(T("وقت", a + 4), 1460, 500, "المونتاج والموشن: مفيش وقت", emo="hourglass_not_done", size=20),
    num(T("تلات", a + 7), 1460, 720, 3, "سنين من غير فيديو"),
    N(T("كورسات", a + 8), 960, 380, "3 كورسات على الرف", src=PI + "p26_1.png", w=300), N(T("كورسات", a + 8) + 0.3, 960, 560, src=PI + "p26_2.png", w=300),
    N(T("كورسات", a + 8) + 0.6, 960, 740, src=PI + "p26_3.png", w=300),
    N(T("الإنترو", a + 10), 470, 480, "إنترو «انت بتشتغل إيه؟» جاهز من 2023", src=PI + "p27_1.png", w=380)], tb4 - 0.15) + outs([
    N(tb4, 960, 260, "اللي اتبنى بـ Claude Code.. على الجهاز", logo=lg("claude.svg"), size=24),
    N(T("video", tb4 + 3), 1460, 470, "1. video maker: 20 ستايل برقم", src=PI + "p09_1.png", w=360),
    N(T("skill", tb4 + 9), 1460, 730, "2. skill السكريبت بنفس الأسلوب", src=PI + "p10_6.png", w=110, ar=753 / 741),
    num(T("publisher", tb4 + 12), 760, 450, 28, "فيديو في الأسبوع"),
    *[N(T("publisher", tb4 + 12) + 0.8 + i * 0.15, 600 + i * 105, 610, logo=lg(f), size=18) for i, f in enumerate(plats)],
    N(T("إنستجرام", tb4 + 17), 760, 760, "4. كومنت بكلمة ← اللينك في الرسايل", logo=lg("instagram.ico"), size=20)], told - 0.15) + outs([
    N(told, 1400, 480, "كورس واحد ساعتين", src=PI + "p26_3.png", w=420), E(told + 1.0, 1170, 480, 1000, 480),
    *[N(T("واحد", told + 2) + i * 0.2, 560 + (i % 3) * 120, 400 + (i // 3) * 220, src=PI + f, w=100, ar=9 / 16) for i, f in enumerate(["p07_2.png", "p07_7.png", "p07_9.png", "p07_10.png", "p07_13.png", "p07_14.png"])],
    num(T("شورت", told + 2), 680, 790, 31, "شورت")], tres - 0.15) + [
    num(T("أربعمية", tres), 1440, 430, 474, "ألف مشاهدة في آخر شهر"),
    *[N(tres + 1.0 + i * 0.15, 1290 + i * 105, 560, logo=lg(f), size=18) for i, f in enumerate(plats)],
    N(T("Genjutsu", tres + 4), 640, 400, "ريل واحد: 253K على فيسبوك", src=PI + "p23_0.png", w=460, ar=798 / 412),
    N(T("ميتين", tres + 4) + 0.5, 640, 680, src=PI + "p23_2.png", w=380, ar=680 / 337),
    N(T("وشورت", tres + 10), 1440, 760, "شورت كل يوم + فيديو يوتيوب كل أسبوع", emo="calendar", size=20)])
spec(tles - 0.1, 872.5, "الدروس", tles, [
    N(T("بتتكرر", tles), 1440, 450, "أي حاجة بتتكرر ← تتأتمت", emo="repeat_button", size=24),
    N(T("السكريبتات", tles + 2), 960, 600, "الـ AI يكتب السكريبت.. والسكريبت هو اللي يشتغل (أوفر)", emo="money_with_wings", size=22),
    N(T("ego", tles + 7), 480, 450, "مفيش مكان للـ ego", emo="person_bowing", size=24),
    N(T("فاركب", tles + 12), 960, 800, "اركب الموجة", emo="water_wave", size=30, bg="mustard")])

# notes 43/44: STEP BY STEP — a picture / motion for every step
st = [T("خطوة", 884.2 + d, 884.4 + d) for d in (0,)]
def step_t(n_word, after, d): return T(n_word, after, d)
s1, s2, s3, s4, s5, s6 = 884.4, 886.4, 895.2, 900.0, 916.9, 921.1
s7, s8, s9, s10, s11, s_end = 928.3, 933.2, 937.9, 949.7, 959.0, 964.3
s1, s2, s3, s4 = T("خطوة", 884.2, s1), T("خطوة", 886.2, s2), T("خطوة", 895.0, s3), T("خطوة", 899.8, s4)
s5, s6, s7, s8 = T("خطوة", 916.7, s5), T("خطوة", 920.9, s6), T("خطوة", 928.1, s7), T("خطوة", 933.0, s8)
s9, s10, s11 = T("خطوة", 937.7, s9), T("خطوة", 949.5, s10), T("خطوة", 958.8, s11)
def badge(t, n, out): return N(t, 1640, 230, f"خطوة {n}", size=26, bg="mustard", out=out)
a = T("تعالى", 874.1, 874.3)
goal = [(V6 + "face_gen.jpg", "وش", 1), (None, "صوت", None), ("assets/ai/higgsfield/studio_look_v2/plate_S4g_empty.png", "ستوديو", None),
        (CL + "clip_183_C11.mp4", "لقطة سينمائية", None), (None, "كابشن", None), (None, "مزيكا", None)]
gi = []
for i, (src, lab, ar) in enumerate(goal):
    t = T(lab[:3], 878.8 + i * 0.6, 879.3 + i * 0.8); x = 1560 - i * 240
    if src: gi.append(N(t, x, 560, lab, src=src, w=200, ar=ar, loop=4 if src.endswith(".mp4") else None))
    elif lab == "صوت": gi.append(W(t, x, 560, w=200, h=80))
    elif lab == "كابشن": gi.append(N(t, x, 560, "«أهلاً، أنا علي»", sub=lab, size=18))
    else: gi.append(N(t, x, 560, logo=lg("suno.png"), label=lab, size=18))
spec(a - 0.1, s_end, "خطوة بخطوة: ريل 30 ثانية", a, outs([N(a + 1.5, 960, 340, "النسخة الـ AI بتعرّف بنفسها", emo="clapper_board", size=26)] + gi, s1 - 0.15) +
    outs([badge(s1, 1, None), N(s1 + 0.6, 960, 480, "اشترك في Claude", logo=lg("claude.svg"), size=30), B(s1 + 0.9, 960, 820, 60, 20, "Pro", logo=lg("claude.svg"))], s2 - 0.15) +
    outs([badge(s2, 2, None), N(T("Claude", s2), 1250, 480, "Claude Desktop ← تبويب Code", src=P6 + "claude_new_chat.jpg", w=520, ar=1120 / 380),
          TY(T("PowerShell", s2 + 1), 560, 500, "PS> irm https://claude.ai/install.ps1 | iex\nPS> claude --version", w=520, head="PowerShell", size=18, dur=30)], s3 - 0.15) +
    outs([badge(s3, 3, None)] + [N(T(w_, s3) + 0.0, 1500 - i * 360, 520, logo=lg(f), label=w_.lstrip("و"), size=24) for i, (w_, f) in
          enumerate([("ElevenLabs", "elevenlabs.png"), ("وHeyGen", "heygen.ico"), ("وHiggsfield", "higgsfield.png"), ("وSuno", "suno.png")])], s4 - 0.15) +
    outs([badge(s4, 4, None), N(T("Settings", s4 + 2), 1250, 520, "Settings ← Connectors ← Add custom connector", src=P6 + "claude_connectors.jpg", w=620, ar=1610 / 850),
          TY(T("Claude", s4 + 10), 520, 520, '.mcp.json\n{ "mcpServers": { ... } }\n> /mcp', w=380, head="Claude Code", size=19, dur=20)], s5 - 0.15) +
    outs([badge(s5, 5, None), N(T("الـ", s5), 1200, 520, "digital twin: كليب قصير ليك", src=GEN + "avatar_012_C02.mp4", w=420, loop=4),
          N(T("موافقة", s5 + 1), 620, 520, "+ فيديو موافقة إن ده وشك", emo="handshake", size=24)], s6 - 0.15) +
    outs([badge(s6, 6, None), N(T("look", s6 + 1), 1250, 500, "look جوه الستوديو نفسه ✓", src=GEN + "avatar_015_C02.mp4", w=440, loop=4, good=True),
          N(T("مش", s6 + 3), 620, 500, "✗ أفاتار متركّب على صورة", src="assets/ai/higgsfield/studio_look_v2/plate_S4g_empty.png", w=360),
          N(T("الإضاءة", s6 + 4), 960, 790, "علشان الإضاءة تبقى واحدة", emo="light_bulb", size=20)], s7 - 0.15) +
    outs([badge(s7, 7, None), TY(T("فولدر", s7), 1250, 500, "my-reel/\n  CLAUDE.md\n  input/\n  output/", w=340, head="📁 المشروع", size=20, dur=18),
          TY(T("CLAUDE.md", s7 + 1), 620, 500, "- الكلام بالمصري\n- اسأل قبل أي توليد بفلوس\n- الريل 30 ث", w=400, head="CLAUDE.md", size=20, dur=25, rtl=True)], s8 - 0.15) +
    outs([badge(s8, 8, None), TY(T("البرومبت", s8), 960, 520, "عايز ريل 30 ثانية:\nالنسخة الـ AI بتعرّف بنفسها،\nستايل سينمائي، مزيكا هادية", w=620, head="البرومبت", size=24, dur=35, rtl=True)], s9 - 0.15) +
    outs([badge(s9, 9, None),
          N(T("الصوت", s9 + 1), 1560, 450, "الصوت", emo="speaker_high_volume", size=20), N(T("Whisper", s9 + 2), 1180, 450, logo=lg("whisper.png"), label="Whisper: التوقيت", size=20),
          N(T("الوش", s9 + 4), 800, 450, logo=lg("heygen.ico"), label="الوش", size=20), N(T("ولقطة", s9 + 5), 420, 450, logo=lg("higgsfield.png"), label="لقطة", size=20),
          N(T("Suno", s9 + 6), 1180, 700, logo=lg("suno.png"), label="المزيكا", size=20), N(T("Remotion", s9 + 7), 800, 700, logo=lg("remotion.png"), label="Remotion", size=20),
          N(T("وffmpeg", s9 + 7), 420, 700, logo=lg("ffmpeg.ico"), label="ffmpeg: يجمّع", size=20),
          E(T("Whisper", s9 + 2), 1460, 450, 1300, 450), E(T("الوش", s9 + 4), 1080, 450, 920, 450), E(T("ولقطة", s9 + 5), 700, 450, 540, 450),
          E(T("Suno", s9 + 6), 420, 520, 1100, 640), E(T("Remotion", s9 + 7), 1080, 700, 920, 700), E(T("وffmpeg", s9 + 7), 700, 700, 540, 700)], s10 - 0.15) +
    outs([badge(s10, 10, None), N(T("المراجعة", s10), 960, 360, "المراجعة", emo="magnifying_glass_tilted_left", size=28),
          N(T("الاسم", s10 + 3), 1400, 560, "الاسم اتنطق غلط ← اتصلح ✓", size=20), N(T("والصوت", s10 + 4), 960, 640, "الصوت ماكانش شبهه ← اتصلح ✓", size=20),
          N(T("والحركة", s10 + 5), 520, 560, "الحركة زيادة ← اتصلحت ✓", size=20)], s11 - 0.15) +
    [badge(s11, 11, None), N(T("export", s11), 1250, 500, "export", emo="film_frames", size=28),
     TY(T("تكلفة", s11 + 2), 620, 520, "تكلفة الريل:\nHeyGen 28 كريدت\nHiggsfield 45 كريدت", w=380, head="🧾", size=22, dur=20, rtl=True)])

# note 45: tricks NUMBERED with a visual each
a = T("شوية", 965.9, 966.1)
TR = [("واحد", 967.9), ("اتنين", 978.9), ("تلاتة", 991.3), ("أربعة", 995.6), ("خمسة", 1000.7), ("ستة", 1005.9), ("سبعة", 1008.9), ("تمانية", 1014.0),
      ("تسعة", 1020.0), ("عشرة", 1024.2), ("حداشر", 1028.2), ("اتناشر", 1033.4), ("تلاتاشر", 1039.2), ("أربعتاشر", 1046.1)]
tt = [T(w_, af, af + 0.2, win=4) for w_, af in TR] + [1054.8]
def trick(i, label, *vis):
    t, o = tt[i], tt[i + 1] - 0.15
    return outs([N(t, 1640, 240, str(i + 1) if i < 13 else "14 و 15", size=40, bg="mustard"), N(t + 0.2, 960, 340, label, size=26)] + list(vis), o)
spec(a - 0.1, 1054.8, "تريكات بتوفر وقت", a, [N(a, 960, 520, "15 تريك", emo="light_bulb", size=34, out=tt[0] - 0.1)] +
    trick(0, "الكابشن من توقيت كل كلمة", N(tt[0] + 1.5, 1350, 520, "Scribe", src=EV + "eleven_scribe.png", w=380), N(tt[0] + 3, 960, 520, logo=lg("whisper.png"), label="Whisper ببلاش", size=20),
          TY(tt[0] + 4, 560, 520, "1\n00:00:01,2 --> 00:00:02,0\nأهلاً، أنا علي", w=360, head="SRT", size=19, dur=20),
          N(tt[0] + 6, 760, 760, logo=lg("capcut.ico"), label="CapCut", size=18), N(tt[0] + 6.2, 1000, 760, logo=lg("premiere-pro-official.png"), label="Premiere", size=18)) +
    trick(1, "موشن بخلفية شفافة", N(tt[1] + 1, 1350, 520, logo=lg("remotion.png"), label="Remotion", size=24), TY(tt[1] + 3, 900, 520, "ProRes 4444 / WebM\n(شفاف)", w=300, size=22, dur=15),
          N(tt[1] + 6, 520, 520, "layer فوق الفيديو", logo=lg("premiere-pro-official.png"), size=20)) +
    trick(2, "الـ look جوه المكان", N(tt[2] + 0.6, 1250, 520, "✓ جوه المكان", src=GEN + "avatar_015_C02.mp4", w=380, loop=3, good=True),
          N(tt[2] + 1.2, 640, 520, "✗ متركّب على خلفية", src="assets/ai/higgsfield/studio_look_v2/plate_S4g_empty.png", w=340)) +
    trick(3, "كلمة بتتنطق غلط؟ غيّر الجملة", TY(tt[3] + 0.8, 1200, 520, "«نص» ← بيتقري غلط", w=340, rtl=True, size=24, dur=12),
          E(tt[3] + 2, 1000, 520, 900, 520), TY(tt[3] + 2.2, 660, 520, "«كلام مكتوب» ✓", w=320, rtl=True, size=24, dur=12)) +
    trick(4, "آخر فريم = أول فريم", N(tt[4] + 0.6, 1250, 520, "آخر فريم", src=V6 + "frame_end.jpg", w=380), E(tt[4] + 1.5, 1040, 520, 880, 520),
          N(tt[4] + 1.6, 660, 520, "أول فريم في اللي بعده", src=V6 + "frame_end.jpg", w=380)) +
    trick(5, "الحركة من Blender والشكل من التوليد", N(tt[5] + 0.4, 1250, 520, "Blender", src="output/blockouts_v6/bridge_static_blockout.mp4", w=420, loop=5),
          N(tt[5] + 0.8, 660, 520, "التوليد", src=CL + "look_bridge.mp4", w=420, loop=5)) +
    trick(6, "ثبّت الشخصية", N(tt[6] + 0.6, 1200, 520, "صور مرجع + character sheet", src=V6 + "refs_plus_sheet.jpg", w=560, ar=1802 / 600),
          TY(tt[6] + 2.5, 560, 520, "prompts.txt\n#01 الستوديو…\n#02 الكوبري…", w=320, size=19, dur=18)) +
    trick(7, "اسأل عن السعر قبل التوليد", B(tt[7] + 0.8, 1300, 800, 66, 16, "تجربة رخيصة", logo=lg("kling.png"), unit="كريدت"),
          B(tt[7] + 2.5, 900, 800, 330, 80, "4K في الآخر", logo=lg("seedance.ico"), unit="كريدت"), N(tt[7] + 1.5, 520, 520, "رخيص الأول.. الغالي في الآخر", emo="money_bag", size=22)) +
    trick(8, "قص الصمت + الشابترز", W(tt[8] + 0.5, 1250, 520, w=480, h=120, mode="clean", clean_t=tt[8] + 1.5),
          TY(tt[8] + 1.5, 620, 520, "0:00 البداية\n1:42 الصور\n3:13 الأفاتار", w=320, head="Whisper ← شابترز", size=20, dur=18)) +
    trick(9, "الـ stems: وطّي المزيكا تحت الكلام", W(tt[9] + 0.5, 1250, 500, w=420, h=110, color="#E0642E"), N(tt[9] + 0.7, 1250, 620, "الكلام", size=20),
          W(tt[9] + 1, 660, 500, w=420, h=60, color="#5FD3E6", gain=0.5), N(tt[9] + 1.2, 660, 620, "المزيكا أوطى", size=20)) +
    trick(10, "صوت يوتيوب: -14 LUFS", TY(tt[10] + 0.6, 960, 520, "ffmpeg -i in.mp4 -af loudnorm=I=-14 out.mp4", w=620, head="ffmpeg", size=20, dur=25)) +
    trick(11, "من الطويل للريلز: 9:16", N(tt[11] + 0.5, 1300, 520, "16:9", src=GEN + "avatar_015_C02.mp4", w=440, loop=3), E(tt[11] + 1.2, 1060, 520, 860, 520),
          N(tt[11] + 1.4, 700, 520, "9:16 + نفس الكابشن", src="assets/channel/shorts_frames/s_00.jpg", w=170, ar=9 / 16)) +
    trick(12, "مكتبة assets: كل لوجو بمصدره", *[N(tt[12] + 0.5 + i * 0.15, 1400 - i * 170, 520, logo=lg(f), size=20) for i, f in
          enumerate(["claude.svg", "heygen.ico", "elevenlabs.png", "higgsfield.png", "suno.png", "remotion.png"])],
          N(tt[12] + 2.5, 960, 700, "من الموقع الرسمي + اللينك", size=20)) +
    trick(13, "كارت لكل ستايل + جرّبه على 3 لقطات رخيصة", TY(tt[13] + 0.6, 1250, 520, "ستايل 16\nprompt: …\nmodel: Kling\nألوان: كحلي + دهبي", w=380, size=20, dur=25),
          *[N(tt[13] + 3 + i * 0.3, 760 - i * 180, 520 + (i % 2) * 40, src=KF + f, w=170) for i, f in enumerate(["kf_026_C02b.png", "kf_171_C09.png", "kf_026_C02b.png"][:2])]))

# note 46: the TOTAL cost invoice of this video (rows, each with its logo; till 22 Nov 2026)
a = T("وتكلفة", 1077.9, 1078.1)
rows = [("heygen.ico", "HeyGen: 209 كريدت (حوالي 10 دولار)"), ("higgsfield.png", "Higgsfield: 1072 كريدت"), ("suno.png", "Suno: 40 كريدت + تنزيل"),
        ("elevenlabs.png", "ElevenLabs: 0"), ("claude.svg", "Claude: اشتراك Pro بـ 20 دولار في الشهر"), (None, "الموشن والريندر على الجهاز: ببلاش")]
inv = []
for i, (f, lab) in enumerate(rows):
    t = a + 0.3 + i * 0.35; y = 300 + i * 100
    inv.append(N(t, 1230, y, logo=lg(f), size=20) if f else N(t, 1230, y, emo="desktop_computer", size=26))
    inv.append(N(t + 0.05, 880, y, lab, size=24, good=(f is None)))
spec(a - 0.1, T("الـ", 1085.0, 1085.2) - 0.15, "فاتورة الفيديو ده (لحد 22 نوفمبر 2026)", a, inv, sfx=[("cash", a + 2.5)])

# separators are TreeMap scenes now; the old SUBS list is not used
for sp in SPECS:   # a new scene never covers a separator: keep it inside its own section
    mid = sp["a"] + 0.5
    for a_, b_, g_ in base._SEC:
        if not g_ and a_ - 0.4 <= mid <= b_:
            sp["a"], sp["b"] = round(max(sp["a"], a_), 3), round(min(sp["b"], b_), 3); break
SPECS = base.SPECS + SPECS
MISS = base.MISS + MISS6

# ======================= v7: Aly's notes on rough cut v6 (review_rough_v6_notes.md, «نفذ»), written in v6 time, moved to v7 below =======================
V7 = "assets/v7/"
def findS(sub):
    for s in SPECS:
        if sub == s.get("title"): return s
        for it in s["items"]:
            if sub in str(it.get("label", "")) or sub in str(it.get("src", "")) or sub in str(it.get("text", "")): return s
    raise KeyError(sub)

# note 5: the workflow column — each picture with ITS label under it, nothing covers anything
s = findS("الـ workflow: الترتيب")
for it in s["items"]:
    lab = it.get("label")
    if lab == "1. صورة": it.update(y=395, w=180)
    elif lab == "2. فيديو": it.update(y=600, w=180)
    elif lab == "3. صوت": it.update(y=800)
    elif it.get("k") == "edge" and it["pts"][0] == 440 and it["pts"][1] == 495: it["pts"] = [440, 508, 440, 540]
    elif it.get("k") == "edge" and it["pts"][0] == 440 and it["pts"][1] == 665: it["pts"] = [440, 712, 440, 765]

# note 9: «كلام مكتوب يبقى فيديو، وصورة تبقى فيديو» — something on screen from the first word, held to the next board
s = findS("صورة تبقى فيديو")
s["a"], s["title_t"] = 146.95, 146.95
s["items"] = [
    TY(147.0, 1330, 300, "«سوق قديم في القاهرة.. والكاميرا طالعة لفوق»", w=440, rtl=True, head="✎", size=20, dur=14),
    E(147.6, 1080, 330, 900, 330), N(147.85, 640, 330, "كلام مكتوب ← فيديو", src=CL + "clip_029_C02b.mp4", w=360, loop=5),
    N(148.25, 1330, 650, "صورة البداية", src=KF + "kf_026_C02b.png", w=400),
    E(148.8, 1100, 650, 870, 650), N(148.85, 640, 650, "← نفس الصورة بقت فيديو", src=CL + "clip_026_C02b.mp4", w=400, loop=5)]

# note 9: start / end frame board — the middle clip comes on «وهو يعمل» (not on the last word) and stays (+ a hold in the timeline)
s = findS("أول صورة وآخر صورة")
tmid = T("وهو", 154.5, 154.7)
for it in s["items"]:
    if it.get("label") == "3. الموديل بيعمل اللي في النص": it["t"] = tmid
    elif it.get("k") == "edge" and it["pts"][1] == 380: it["t"] = tmid

# notes 10 + 11 (asked in v4 #15 and v5 #10-11): the 3 clips TOGETHER on «حركة كاميرا», each name + arrow under its clip ON its word,
# the named clip grows a bit; «لغة السينما» thumb + QR HERE (not on the models board); the board is held (hold in the timeline)
s = findS("حركة الكاميرا بتختارها بالاسم")
tk = T("حركة", 156.2, 156.4); td, to_, tc = T("dolly", 157.8, 158.0), T("orbit", 158.6, 158.8), T("crane", 159.3, 159.5)
s["a"], s["b"], s["title_t"] = round(tk - 0.15, 3), 160.1, tk
s["items"] = [
    N(tk + 0.05, 1400, 400, src=CL + "clip_006_C01.mp4", w=400, loop=4, act=(td, td + 1.2)),
    N(tk + 0.2, 960, 400, src=CL + "clip_204_C11.mp4", w=400, loop=4, act=(to_, to_ + 1.2)),
    N(tk + 0.35, 520, 400, src=CL + "clip_029_C02b.mp4", w=400, loop=4, act=(tc, tc + 1.2)),
    N(td, 1400, 580, "dolly: الكاميرا بتدخل", size=24), E(td + 0.15, 1310, 640, 1490, 640),
    N(to_, 960, 580, "orbit: بتلف حواليه", size=24), E(to_ + 0.15, 880, 650, 1040, 650, bend=-120),
    N(tc, 520, 580, "crane: بتطلع لفوق", size=24), E(tc + 0.15, 520, 680, 520, 625),
    N(tc + 0.5, 1080, 790, "حركات الكاميرا بالتفصيل: «لغة السينما»", src=CH + "thumb_S-tSUtClTOg.jpg", w=200, size=20),
    N(tc + 0.7, 850, 790, src=CH + "qr_S-tSUtClTOg.png", w=100, ar=1)]
s = findS("الموديلات المشهورة دلوقتي")
s["items"] = [it for it in s["items"] if "S-tSUtClTOg" not in str(it.get("src", ""))]

# note 12: 253K — the K beside the yellow number, the Arabic once under it
s = findS("ريل Genjutsu: داشبورد فيسبوك")
for it in s["items"]:
    if it.get("k") == "num": it["suffix"] = "K"; it["label"] = "253 ألف مشاهدة على فيسبوك"

# note 13 (= v5 #14 a + d): the avatar section opens with HIM full-frame, then the screen shrinks into the circle at the top;
# lip sync = two examples on the LEFT saying the SAME words he says at that moment (played once, in sync with the voice)
s = findS("avatar_section_circle.mp4")
s["a"] = 193.4
for it in s["items"]:
    if it.get("k") == "circle": it["t"] = 193.4; it["skip"] = round(193.4 - SKIP0, 3); it["grow_t"] = 194.95
    elif it.get("t") is not None and it["t"] < 195.5: it["t"] = 195.5
tls6 = T("lipsync", 206.2, 206.4); tsay = T("تاخد", 207.2, 207.4); tex6 = T("وجربنا", 210.8, 211.0)
s["items"] = [it for it in s["items"] if not (tls6 - 0.05 <= (it.get("t") or 0) < tex6 - 0.2)]
s["items"] += outs([N(tls6, 1400, 470, "lip sync", sub="البق بيمشي على كلام جديد.. نفس اللي بقوله دلوقتي", size=30),
                    N(tsay, 700, 420, "الستوديو ده.. لابس أسود", src=HG + "lipsync_ex_S4g.mp4", w=340),
                    N(tsay, 700, 710, "أوضتي الحقيقية", src=HG + "lipsync_ex_realroom.mp4", w=340)], tex6 - 0.15)

# note 14 (= v5 #24 + #25, never done on THIS board): twin = his real room take -> the same face saying new words; Looks = the twin
# in other places / clothes; Video Agent = cinematic shots MIXED with his avatar
s = findS("Avatar 6: twin")
_old = {it.get("label"): it["t"] for it in s["items"] if it.get("label") in ("Avatar 6: twin", "Looks", "Video Agent")}
k0, k1, k2 = _old["Avatar 6: twin"], _old["Looks"], _old["Video Agent"] - 1.1   # the times of the v6 branches (on their words)
g2o = next(it.get("out_t") for it in s["items"] if it.get("label") == "Avatar 6: twin")
drop = ("Avatar 6: twin", "Looks", "Video Agent")
s["items"] = [it for it in s["items"] if it.get("label") not in drop]
looks4 = [GEN + "avatar_015_C02.mp4", HG + "look_beach.mp4", HG + "look_room_black.mp4", HG + "look_presenter.mp4"]
s["items"] += outs([
    N(k0, 1500, 400, "Avatar 6: twin", src=V7 + "real_room_take_6s.mp4", w=250, loop=6, sub="كليب حقيقي ليّ ~15 ث", size=22),
    E(k0 + 0.8, 1500, 560, 1500, 590), N(k0 + 0.9, 1500, 680, "← نفس الوش بكلام جديد", src="assets/ai/heygen/avatar_clips_v1/avatar_001_C00.mp4", w=250, loop=5, size=20),
    *[N(k1 + 0.15 * i, 1065 + (i % 2) * 150, 440 + (i // 2) * 100, src=f, w=140, loop=3.5) for i, f in enumerate(looks4)],
    N(k1 + 0.6, 1140, 640, "Looks", sub="نفس الـ twin.. مكان ولبس تاني", size=22),
    N(k2 + 1.1, 780, 600, "Video Agent", src=V7 + "video_agent_mix.mp4", w=300, loop=6, sub="لقطات سينمائية + الأفاتار", size=22)], g2o)

# v6 review «الحاجات ظهرت متأخر»: in the numbered boards (step by step, tricks) the step's picture comes WITH its number, not a second later
for title_ in ("خطوة بخطوة: ريل 30 ثانية", "تريكات بتوفر وقت"):
    s = findS(title_)
    groups = {}
    for it in s["items"]:
        groups.setdefault(it.get("out_t"), []).append(it)
    for o_, its in groups.items():
        badge = next((it for it in its if str(it.get("label", "")).startswith("خطوة ") or (it.get("size") == 40 and it.get("bg") == "mustard")), None)
        if badge is None: continue
        rest = [it for it in its if it is not badge and it.get("t") is not None and not (it.get("size") == 26 and it.get("x") == 960 and it.get("y") == 340)]
        if not rest: continue
        lag = min(it["t"] for it in rest) - (badge["t"] + 0.3)
        if lag > 0.15:
            for it in rest: it["t"] = round(it["t"] - min(lag, 3.0), 3)

# v5 #29 (picture under the Suno branches, not done in v6): the real v6 page and the real edit page, small, beside their branches
s = findS("Suno Studio 2.0")
tv6 = next(it["t"] for it in s["items"] if str(it.get("label", "")).startswith("v6 ·")); tst = next(it["t"] for it in s["items"] if it.get("label") == "Suno Studio 2.0")
s["items"] += [N(tv6 + 0.4, 1560, 670, src=EV + "suno_v6.png", w=210), N(tst + 0.4, 720, 690, src=EV + "suno_edit.png", w=210)]


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
s["items"] = [it for it in s["items"] if it.get("label") != "ريل Genjutsu: داشبورد فيسبوك"]
for it in s["items"]:
    if str(it.get("src", "")).endswith("hf_genjutsu_len.png"): it.update(x=1350, y=380, w=440)
    if it.get("k") == "num": it.update(x=1350, y=720)
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

# ---------- v6 time -> v7 time (v7 = longer separators, two audio fixes, holds after S009.2 / S009.3 / S009.5) ----------
T6P = json.load(open("work/timeline_v6.json", encoding="utf-8"))["pieces"]; T7P = json.load(open("work/timeline_v8.json", encoding="utf-8"))["pieces"]
_L = lambda p: p["dur"] if p["kind"] in ("gap", "hold") else p["b"] - p["a"]
_G6 = [p for p in T6P if p["kind"] == "gap"]; _G7 = [p for p in T7P if p["kind"] == "gap"]
def M67(t6):
    if t6 is None: return None
    best = next((p for p in T6P if p["t"] - 1e-6 <= t6 <= p["t"] + _L(p) + 1e-6), None)
    if best is None:
        prev = max((p for p in T6P if p["t"] <= t6), key=lambda p: p["t"])
        return round(M67(prev["t"] + _L(prev)) + (t6 - prev["t"] - _L(prev)), 3)
    p, off = best, t6 - best["t"]
    if p["kind"] == "gap":
        q = _G7[_G6.index(p)]; return round(q["t"] + off * q["dur"] / p["dur"], 3)
    if p["kind"] == "file":
        q = next(q for q in T7P if q["kind"] == "file" and q["sids"] == p["sids"]); return round(q["t"] + off * _L(q) / max(0.01, _L(p)), 3)
    t2 = p["a"] + off
    for q in T7P:
        if q["kind"] == "v2" and q["a"] - 1e-3 <= t2 <= q["b"] + 1e-3: return round(q["t"] + t2 - q["a"], 3)
    q = min((q for q in T7P if q["kind"] == "v2"), key=lambda q: min(abs(t2 - q["a"]), abs(t2 - q["b"])))
    return round(q["t"] + min(max(t2, q["a"]), q["b"]) - q["a"], 3)
for sp_ in SPECS:
    sp_["a"], sp_["b"] = M67(sp_["a"]), M67(sp_["b"])
    if sp_["title_t"] is not None: sp_["title_t"] = M67(sp_["title_t"])
    for it in sp_["items"]:
        for k_ in ("t", "out_t", "clean_t", "dim_t", "grow_t"):
            if it.get(k_) is not None: it[k_] = M67(it[k_])
        if it.get("act_t"): it["act_t"] = [M67(it["act_t"][0]), M67(it["act_t"][1])]
    sp_["sfx"] = [(n, M67(t)) for n, t in sp_["sfx"]]


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
    N(ta + 0.1, 1470, 400, "1. أول صورة", src=V8 + "f032_first.jpg", w=360, size=22),
    N(tf2, 450, 400, "2. آخر صورة", src=V8 + "f032_last.jpg", w=360, size=22),
    N(tmid, 960, 400, "3. الموديل بيعمل اللي في النص", src=CL + "clip_032_C02b.mp4", w=360, loop=6, size=22),
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
          N(tco, 960, 270, "2. Cowork / agent: بيشتغل على ملفاتك وبرامجك", size=22), N(tco + 0.3, 960, 470, src=V8 + "claude_session_2x.mp4", w=290, ar=1280 / 1004, loop=8),
          N(tco + 0.6, 960, 660, "Claude Cowork · ChatGPT agent", size=18),
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
    N(cS, 960, 300, "Skills: كراسات خبرة بيقراها لما يحتاجها", emo="notebook", size=18),
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
    TY(T8("اعمل", mBl + 1.0), 1250, 650, "«اعمل كوبري على النيل»", w=360, rtl=True, size=20, dur=12),
    N(T8("فيبني", mBl + 1.5), 620, 460, "← بيبني المشهد", src="output/blockouts_v6/bridge_static_blockout.mp4", w=420, loop=6, size=20)], mDv - 0.15) + [
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
    N(mThis, 960, 610, "الفيديو ده نفسه: من جوه Claude بس.. من غير ما أفتح أي برنامج تاني", src=V8 + "claude_session_2x.mp4", w=500, ar=1280 / 1004, loop=10, size=20, good=True)])
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


# note 43: skills explained simply + «you don't write it yourself: tell Claude to turn the finished work into a skill»
k1 = T8("الـ", 781.4); kB = T8("بتتبني", 791.6); kW = T8("وأهميتها", 796.0); kIn = T8("في", 802.2); kEx = T8("ومثال:", 811.2); kOpen = T8("وده", 819.7); kEnd = T8("خليني", 833.2)
spec8(k1 - 0.1, kEnd - 0.15, "الـ skill = كراسة خبرة", k1, outs([
    N(T8("ملف", 783.0), 1400, 330, "ملف SKILL.md: الخطوات + القواعد + أمثلة", size=20), TY(T8("ملف", 783.0) + 0.3, 1400, 400, "---\nname: aly-video-motion\ndescription: الموشن بأسلوب علي\n---\n1. اقرا رقم الستايل\n2. متقصش كلمة", w=400, head="SKILL.md", size=16, dur=20),
    N(kB, 820, 360, "بتتبني إزاي؟", size=24),
    N(T8("بتكتب", 792.2), 820, 460, "اللي بتعمله كل مرة.. واللي اتعلمته من غلطاتك", size=19),
    N(kW, 820, 600, "ليه مهمة؟ مش بيبدأ من الصفر كل مرة", emo="light_bulb", size=20),
    N(T8("بأسلوبك،", 800.2), 820, 700, "بيشتغل بأسلوبك.. وبيقراها بس لما يحتاجها", size=18)], kIn - 0.15) + outs([
    N(kIn, 1450, 330, "مش لازم تكتبها بنفسك", emo="sparkles", size=24, bg="mustard"),
    TY(kIn + 0.4, 1450, 420, "«حوّل الشغل ده لـ skill واحفظ المعرفة»", w=420, rtl=True, head="بعد ما تخلص شات أو فيديو:", size=19, dur=16),
    E(kIn + 1.6, 1450, 560, 1450, 610),
    N(kIn + 1.8, 1450, 640, "الـ skill اتحفظت ✓", emo="check_mark_button", size=22, good=True),
    N(kIn + 2.6, 760, 520, "المرة الجاية بيبدأ من هنا", emo="repeat_button", size=22),
    N(T8("ChatGPT", 809.2), 760, 700, "ChatGPT و Codex: Skills بنفس الفكرة", logo=LG("chatgpt.png"), size=18)], kEx - 0.15) + outs([
    N(kEx, 1300, 470, "الـ video maker بتاعنا", src="../../styles/16 journey-series/cover.jpg", w=420, size=22, sub="skill فيها كل اللي عجب علي"),
    N(T8("غلطة", 817.2), 700, 400, "كل غلطة اتسجلت.. متتكررش", emo="no_entry", size=20),
    N(T8("وعشرين", 818.1), 700, 560, "20 ستايل برقم", emo="artist_palette", size=22)], kOpen - 0.15) + [
    N(kOpen, 960, 330, "معيار مفتوح", size=26),
    N(T8("Claude", 822.8), 1400, 520, logo=LG("claude.svg"), label="Claude Code", size=20), N(T8("وCodex،", 823.6), 960, 520, logo=LG("openai-codex.png"), label="Codex", size=20),
    N(T8("Antigravity", 824.4), 520, 520, logo=LG("antigravity.png"), label="Antigravity", size=20),
    N(T8("أمثلة:", 826.3), 960, 760, "skill بتكتب السكريبت بأسلوب صاحب القناة", emo="writing_hand", size=20)])
# notes 46/47: the real experience — no PDF crops: real course thumbs side by side, the styles wall, what the publisher / IG automation DO
import glob as _g, os
r1 = T8("خليني", 833.2); rBuilt = T8("اللي", 849.8); rVM = T8("video", 855.4); rSk = T8("skill", 861.1); rPub = T8("publisher", 864.2); rIG = T8("أوتوميشن", 869.3)
rOld = T8("والفيديوهات", 873.4); rRes = T8("والنتيجة", 879.2); rLes = T8("والدروس؟", 893.3); rEnd = T8("الموجة.", 906.8) + 1.0
covers = sorted(_g.glob("../../styles/[01]*/cover.jpg"))[:20]
plats = ["youtube.png", "instagram.ico", "facebook.png", "tiktok.png"]
spec8(r1 - 0.1, rLes - 0.1, "تجربة حقيقية بالأرقام", r1, outs([
    N(T8("software", 837.7), 1460, 330, "software tester full-time", emo="technologist", size=22),
    N(T8("وقت", 840.3), 1460, 430, "المونتاج والموشن: مفيش وقت", emo="hourglass_not_done", size=20),
    num(T8("تلات", 841.2), 1460, 650, 3, "سنين من غير فيديو"),
    *[N(T8("كورسات", 844.1) + i * 0.25, 1100 - i * 300, 360, None, src=PI + f, w=270) for i, f in enumerate(["p26_1.png", "p26_2.png", "p26_3.png"])],
    N(T8("كورسات", 844.1) + 0.8, 800, 500, "3 كورسات متسجلة على الرف", size=20),
    N(T8("الإنترو", 848.2), 800, 700, "إنترو «انت بتشتغل إيه؟» جاهز من 2023", src=PI + "p27_1.png", w=360, size=18)], rBuilt - 0.15) + outs([
    N(rBuilt, 960, 250, "اللي اتبنى بـ Claude Code.. على الجهاز", emo="laptop", size=22),
    *[N(rVM + 0.1 * i, 1640 - (i % 5) * 130, 380 + (i // 5) * 80, None, src=f, w=120) for i, f in enumerate(covers)],
    N(rVM + 0.4, 1380, 720, "1. video maker: 20 ستايل برقم", size=20)], rSk - 0.15) + outs([
    N(rSk, 1400, 330, "2. skill السكريبت بنفس الأسلوب", emo="writing_hand", size=20),
    N(rPub, 700, 300, "3. publisher: فيديو واحد ← يتجدول على 4 منصات", emo="calendar", size=20),
    *[N(rPub + 0.5 + i * 0.15, 520 + i * 120, 420, logo=LG(f), size=16) for i, f in enumerate(plats)],
    num(T8("تمنية", 865.4), 700, 560, 28, "فيديو في الأسبوع"),
    N(rIG, 1400, 680, "4. أوتوميشن إنستجرام", logo=LG("instagram.ico"), size=20),
    TY(rIG + 0.4, 1400, 770, "كومنت: «كلمة»  ←  رسالة فيها اللينك ✓", w=420, rtl=True, size=18, dur=14)], rOld - 0.15) + outs([
    N(rOld, 1400, 470, "كورس واحد ساعتين", src=CH + "thumb_2XVRSnTuZJQ.jpg" if os.path.exists(CH + "thumb_2XVRSnTuZJQ.jpg") else PI + "p26_3.png", w=420, size=20),
    E(rOld + 1.0, 1170, 470, 1000, 470),
    *[N(T8("واحد", rOld + 2) + i * 0.15, 560 + (i % 3) * 120, 400 + (i // 3) * 220, None, src=PI + f, w=100, ar=9 / 16) for i, f in enumerate(["p07_2.png", "p07_7.png", "p07_9.png", "p07_10.png", "p07_13.png", "p07_14.png"])],
    num(T8("شورت.", rOld + 3), 680, 820, 31, "شورت")], rRes - 0.15) + [
    num(T8("أربعمية", 883.4), 1440, 430, 474, "ألف مشاهدة في آخر شهر"),
    *[N(rRes + 1.0 + i * 0.15, 1290 + i * 105, 580, logo=LG(f), size=16) for i, f in enumerate(plats)],
    N(T8("Genjutsu", 887.0), 640, 470, "ريل واحد: 253K على فيسبوك", src=V8 + "genjutsu_reel.mp4", w=480, loop=10, size=20),
    N(T8("وشورت", 890.0), 1440, 760, "شورت كل يوم + فيديو يوتيوب كل أسبوع", emo="calendar", size=20)])
spec8(rLes - 0.1, rEnd, "الدروس", rLes, [
    N(T8("بتتكرر", 894.8), 1440, 450, "أي حاجة بتتكرر ← تتأتمت", emo="repeat_button", size=24),
    N(T8("السكريبتات،", 898.0), 960, 600, "الـ AI يكتب السكريبت.. والسكريبت هو اللي يشتغل (أوفر)", emo="money_with_wings", size=22),
    N(T8("ego:", 902.8), 480, 450, "مفيش مكان للـ ego", emo="person_bowing", size=24),
    N(T8("فاركب", 906.2), 960, 800, "اركب الموجة", emo="water_wave", size=30, bg="mustard")])
# notes 48/50: step by step SIMPLE — one big picture per step, «خطوة N من 11» + a progress bar, desktop app only (no PowerShell / no code)
sa = T8("تعالى", 910.3)
steps = [T8("خطوة", 920.5 + 0)]
for af in (922.5, 926.6, 931.4, 943.1, 947.4, 954.6, 959.5, 964.1, 976.0, 985.3): steps.append(T8("خطوة", af))
send = T8("بالظبط.", 989.8) + 1.4
def stepbar(i, t, o):
    return [N(t, 960, 285, f"خطوة {i} من 11", size=26, bg="mustard", out=o)] + \
           [N(t + 0.05, 1460 - j * 100, 350, str(j + 1) + (" ✓" if j < i - 1 else ""), size=16, out=o, bg=("mustard" if j == i - 1 else None), dim=(t + 0.3 if j > i - 1 else None)) for j in range(11)]
vis = [
    N(steps[0] + 0.2, 960, 560, "اشترك في Claude (Pro)", logo=LG("claude.svg"), size=30),
    N(steps[1] + 0.2, 960, 560, "نزّل Claude Desktop وافتح تبويب Code", src=P6 + "claude_new_chat.jpg", w=720, ar=1120 / 380, size=24),
    N(steps[2] + 0.2, 960, 560, "حسابات: ElevenLabs · HeyGen · Higgsfield · Suno", emo="key", size=26),
    N(steps[3] + 0.2, 960, 620, "Settings ← Connectors ← Add custom connector ← Connect", src=V8 + "connectors_ui.mp4", w=560, ar=1020 / 794, loop=4.6, size=20),
    N(steps[4] + 0.2, 960, 560, "الـ digital twin: كليب قصير ليك + فيديو موافقة", src=V7 + "real_room_take_6s.mp4", w=620, loop=6, size=22),
    N(steps[5] + 0.2, 960, 560, "look جوه الستوديو نفسه ✓", src=GEN + "avatar_015_C02.mp4", w=620, loop=4, size=22, good=True),
    N(steps[6] + 0.2, 960, 560, "فولدر للمشروع.. وجواه ملف بقواعدك", emo="file_folder", size=30),
    TY(steps[7] + 0.2, 960, 460, "عايز ريل 30 ثانية:\nالنسخة الـ AI بتعرّف بنفسها،\nستايل سينمائي، مزيكا هادية", w=640, head="البرومبت", size=26, dur=35, rtl=True),
    N(steps[8] + 0.2, 960, 560, "Claude بيولّد بالترتيب.. وانت بتتفرج", src=V8 + "claude_session_2x.mp4", w=640, ar=1280 / 1004, loop=10, size=22),
    N(steps[9] + 0.2, 960, 560, "المراجعة: الاسم · الصوت · الحركة ← اتصلحوا ✓", emo="magnifying_glass_tilted_left", size=26),
    N(steps[10] + 0.2, 960, 560, "export.. وتكلفة الريل على الشاشة", emo="film_frames", size=28)]
items = outs([N(sa + 1.0, 960, 420, "ريل 30 ثانية: النسخة الـ AI بتعرّف بنفسها", emo="clapper_board", size=28),
              *[N(T8(w_, 915.3 + i * 0.6), 1500 - i * 220, 620, w_.rstrip("،."), size=20) for i, w_ in enumerate(["وش،", "وصوت،", "وستوديو،", "ولقطة", "وكابشن،", "ومزيكا."])]], steps[0] - 0.15)
for i in range(11):
    o = (steps[i + 1] - 0.15) if i + 1 < 11 else None
    items += stepbar(i + 1, steps[i], o) + [dict(vis[i], **({"out_t": o} if o else {}))]
spec8(sa - 0.1, send, "خطوة بخطوة: ريل 30 ثانية", sa, items)

# generic (v7 notes 8a/16/25): a board whose end falls on a silent hold stays through the hold
for sp_ in SPECS:
    for p_ in T8P:
        if p_["kind"] == "hold" and p_["t"] - 0.8 <= sp_["b"] <= p_["t"] + 0.3: sp_["b"] = round(p_["t"] + p_["dur"] - 0.05, 3)

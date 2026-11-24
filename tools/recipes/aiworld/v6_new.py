"""v6 scenes for Aly's 50 notes on rough cut v5 (review_rough_v5_notes.md), written directly in v6 time (words_v6.json).
make_props_v6 uses SPECS from here = the v5 specs (already moved to v6 time, some patched below) + the new ones.
Item helpers come from v6_specs (N node, E edge, B price bar, W wave, TY typed, SC scan)."""
import json, glob
import v6_specs as base
from v6_specs import N, E, B, W, TY, SC, lg, KF, CL, EV, PD, GEN

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

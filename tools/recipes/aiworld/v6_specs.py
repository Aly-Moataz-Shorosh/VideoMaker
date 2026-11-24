"""v5 explaining scenes (Aly's v4 notes 2-33). Each SPEC replaces [a, b] of the timeline with ONE diagram board whose items enter on
their WORD (absolute times; make_props_v5.py turns them into frames). Safe area: x 140..1780, y 170..900 (note 24).
Item helpers: N = node (picture / looping clip / logo / chip + label), E = edge that draws itself, B = green price bar,
W = live voice wave, TY = typed text, SC = OCR scan / detection boxes."""
import json, re

WORDS = json.load(open("work/words_v5.json", encoding="utf-8"))
LOG = "../../brand/logos-tools/"
KF = "assets/ai/higgsfield/keyframes_final/"
CL = "assets/ai/higgsfield/clips_v1/"
EV = "research/evidence_shots_v1/"
PD = "work/pdf_pages/"
V5 = "assets/v5/"
GEN = "assets/ai/heygen/avatar_clips_v2_gen/"
MISS = []

def T(word, after, default=None):
    """first time `word` (its first token) is said at/after `after` (s)"""
    key = word.split()[0].lower()
    for w in WORDS:
        if w["a"] >= after - 0.3 and key in w["w"].lower():
            if w["a"] - after > 25: break
            return round(w["a"], 3)
    MISS.append((word, after)); return default if default is not None else after

def N(t, x, y, label=None, src=None, logo=None, emo=None, w=None, ar=None, out=None, loop=None, sub=None, bg=None, size=None, fit=None, good=False, act=None, dim=None):
    d = dict(k="node", t=t, x=x, y=y)
    for k, v in dict(label=label, src=src, logo=logo, emo=emo, w=w, ar=ar, out_t=out, loopDur=loop, sub=sub, bg=bg, size=size, fit=fit, act_t=act, dim_t=dim).items():
        if v is not None: d[k] = v
    if loop: d["loop"] = True
    if good: d["good"] = True
    return d
def E(t, x1, y1, x2, y2, out=None, bend=0, color=None, arrow=True, dur=14):
    d = dict(k="edge", t=t, pts=[x1, y1, x2, y2], bend=bend, arrow=arrow, dur=dur)
    if out is not None: d["out_t"] = out
    if color: d["color"] = color
    return d
def B(t, x, base, h, price, label, logo=None, sub=None, out=None, unit=None):
    d = dict(k="bar", t=t, x=x, base=base, h=h, price=price, label=label)
    if unit: d["unit"] = unit
    if logo: d["logo"] = logo
    if sub: d["sub"] = sub
    if out is not None: d["out_t"] = out
    return d
def W(t, x, y, w=620, h=130, out=None, mode=None, clean_t=None, color=None, gain=1.3):
    d = dict(k="wave", t=t, x=x, y=y, w=w, h=h, gain=gain)
    if out is not None: d["out_t"] = out
    if mode: d["mode"] = mode
    if clean_t is not None: d["clean_t"] = clean_t
    if color: d["color"] = color
    return d
def TY(t, x, y, text, w=520, head=None, rtl=False, dur=40, size=22, out=None):
    d = dict(k="typed", t=t, x=x, y=y, text=text, w=w, rtl=rtl, dur=dur, size=size)
    if head: d["head"] = head
    if out is not None: d["out_t"] = out
    return d
def SC(t, x, y, src, w=520, mode=None, boxes=None, text=None, ar=16 / 9, out=None):
    d = dict(k="scan", t=t, x=x, y=y, src=src, w=w, ar=ar)
    if mode: d["mode"] = mode
    if boxes: d["boxes"] = boxes
    if text: d["text"] = text
    if out is not None: d["out_t"] = out
    return d
def lg(name): return LOG + name

SPECS = []
def spec(a, b, title=None, title_t=None, items=(), circle=False, sfx=()):
    SPECS.append(dict(a=round(a, 3), b=round(b, 3), title=title, title_t=title_t, items=list(items), circle=circle, sfx=list(sfx)))

# ---------- note 2: «الوش ده، والصوت ده، والمكان ده.. كله متولّد» ----------
a = T("والصوت", 4.2) - 0.25; t_face = a + 0.05; t_v = T("والصوت", 4.2); t_p = T("والمكان", 4.5); t_all = T("متولّد", 5.5); t_ttl = T("الفيديو", 7.5)
spec(a, 11.25, "الفيديو ده معمول بالـ AI بإشراف علي شُرُش", t_ttl, [
    N(t_face, 1440, 420, "الوش", src=V5 + "face_real.jpg", w=380, sub="صورة وشي الحقيقية"),
    N(t_v, 960, 420, "الصوت", emo="studio_microphone", size=32), W(t_v, 960, 520, w=380, h=110),
    N(t_p, 480, 420, "المكان", src="assets/ai/higgsfield/studio_look_v2/plate_S4g_empty.png", w=380, sub="الستوديو من غيري"),
    N(t_all, 960, 760, "كله متولّد", emo="sparkles", size=40, bg="mustard"),
    E(t_all, 1440, 560, 1060, 735), E(t_all, 960, 600, 960, 720), E(t_all, 480, 560, 860, 735)])

# ---------- note 3: «تلات سنين من غير ولا فيديو» + his channel page ----------
spec(11.25, 14.6, None, None, [
    dict(k="num", t=11.4, x=1480, y=380, to=0, label="فيديو جديد"), dict(k="num", t=T("سنين", 11.3), x=1480, y=680, to=3, label="سنين"),
    N(11.6, 720, 540, "قناتي: آخر الفيديوهات من 3 و4 سنين", src="assets/channel/aly_channel_last_videos_3y_ago.webp", w=900, ar=1453 / 674)])

# ---------- note 4: 28 videos a week = many real shorts around the number (16 picked to look DIFFERENT) ----------
import glob, math
frames = json.load(open("assets/channel/shorts_frames/_varied16.json"))
t28 = T("ثمانية", 14.0); t4 = T("أربع", 15.5)
ring = []
for i, f in enumerate(frames):   # Aly: «الدايرة كانت حلوة» — the circle back (videos may touch each other)
    ang = -math.pi / 2 + i * 2 * math.pi / len(frames)
    ring.append(N(round(t28 + 0.12 * i, 3), round(960 + 660 * math.cos(ang)), round(530 + 270 * math.sin(ang)), src=f, w=96, ar=9 / 16))
spec(14.6, 18.55, None, None, [dict(k="num", t=t28, x=960, y=480, to=28, label="فيديو في الأسبوع", big=True)] + ring + [
    dict(N(t4 + i * 0.15, 840 + i * 80, 670, logo=lg(n)), s=64) for i, n in enumerate(["youtube.png", "instagram.ico", "facebook.png", "tiktok.png"])])

# ---------- notes 10 + 11: the problem (2 pictures) and 3 solutions, each with a REAL screenshot, held long enough ----------
a = T("وأهم", 121.0) - 0.1; t_p = T("الشخصية", 122.4)
t_soul, t_ref, t_lora = T("Soul", 125.5), T("مرجع", 127.0), T("LoRA", 128.0)
spec(a, t_lora + 3.2, "الشخصية تفضل هي هي", t_p, [
    N(t_p, 1160, 370, "تجارب وش علي في الفيديو ده", src="output/keyframes_v2_test_compare.jpg", w=360),
    N(t_p + 0.4, 760, 370, "لحد ما بقى مظبوط", src="output/keyframes_v6_test.jpg", w=360),
    E(t_soul - 0.2, 960, 500, 1420, 600), E(t_ref - 0.2, 960, 500, 960, 600), E(t_lora - 0.2, 960, 500, 500, 600),
    N(t_soul, 1420, 720, "Soul ID في Higgsfield", src="research/pages_v5/hf_character_crop.png", w=380, ar=1160 / 650),
    N(t_ref, 960, 720, "صور مرجع", src=V5 + "demo_refs.jpg", w=380),
    N(t_lora, 500, 720, "تدريب LoRA على وشك", src="research/pages_v5/hf_lora_crop.png", w=380, ar=1150 / 485)])

# ---------- note 12: every small tool WITH a picture example ----------
a2 = t_lora + 3.2; tt = [T("تكبير", 132.5), T("وشيل", 134.5), T("ولوجوهات", 136.0), T("وثمبنيلز", 137.5)]
spec(a2, tt[3] + 3.3, "أدوات صغيرة بتوفر يوم", a2 + 0.2, [
    N(tt[0], 1530, 540, "تكبير من غير ما تبوظ", src=V5 + "demo_upscale.jpg", w=360),
    N(tt[1], 1150, 540, "شيل الخلفية في ثانية", src=V5 + "demo_bg_remove.jpg", w=360),
    N(tt[2], 770, 540, "لوجوهات وفيكتور", src=V5 + "demo_logos.jpg", w=360, sub="من شغلي"),
    N(tt[3], 390, 540, "ثمبنيلز", src=V5 + "demo_thumbs.jpg", w=360, sub="ثمبنيلز قناتي")])

# ---------- note 14: start picture -> the same picture moving, held ----------
t_img = T("وصورة", 142.6)
spec(t_img - 0.4, t_img + 4.6, "صورة تبقى فيديو", t_img - 0.3, [
    N(t_img, 1260, 520, "صورة البداية", src=KF + "kf_026_C02b.png", w=560),
    E(t_img + 1.0, 960, 520, 980, 520, dur=8, arrow=False),
    N(t_img + 1.1, 660, 520, "← نفس الصورة بقت فيديو", src=CL + "clip_026_C02b.mp4", w=560, loop=5),
    E(t_img + 1.0, 990, 520, 950, 520)])

# ---------- notes 15 + 16: dolly / orbit / crane, each a looping clip under its word ----------
a = T("حركة", 150.6) - 0.2; td, to_, tc = T("dolly", 152.5), T("orbit", 153.0), T("crane", 153.6)
spec(a, tc + 4.0, "حركة الكاميرا بتختارها بالاسم", a + 0.2, [
    N(td, 1400, 480, "dolly: الكاميرا بتدخل", src=CL + "clip_006_C01.mp4", w=420, loop=4),
    E(td + 0.5, 1310, 760, 1490, 760),
    N(to_, 960, 480, "orbit: بتلف حواليه", src=CL + "clip_204_C11.mp4", w=420, loop=4),
    E(to_ + 0.5, 880, 770, 1040, 770, bend=-120),
    N(tc, 520, 480, "crane: بتطلع لفوق", src=CL + "clip_029_C02b.mp4", w=420, loop=4),
    E(tc + 0.5, 520, 800, 520, 720)])


# ---------- note 17: Genjutsu = the tool page + HIS reel made with it and its real views (his own dashboard, PDF p23) ----------
tg1 = T("Genjutsu", 167.5); tg2 = T("تدي", 169.5); tg3 = T("فينقل", 173.5)
spec(tg1 - 0.6, T("وفي", 176.8) - 0.1, "Genjutsu في Higgsfield", tg1 - 0.4, [
    N(tg1, 1250, 470, "تدي فيديو 4–30 ث + لحد 30 صورة مرجع", src=EV + "hf_genjutsu_len.png", w=520),
    N(tg3, 640, 420, "ريلي اللي اتعمل بـ Genjutsu", src=PD + "p23.png", w=220, ar=0.74, fit="contain"),
    dict(k="num", t=tg3 + 0.6, x=560, y=740, to=253, label="ألف مشاهدة على فيسبوك"),
    N(tg3 + 0.6, 800, 720, logo=lg("facebook.png"), size=22)], sfx=[("cash", tg3 + 0.6)])

# ---------- notes 17 + 19: Genjutsu reel + his YouTube videos (thumb + QR) ----------
tg = T("Genjutsu", 182.0); tf = T("وفيلم", 183.5)
spec(tg - 0.6, tf + 3.6, None, None, [
    N(tg, 1240, 470, "فيديو Genjutsu", src="assets/channel/thumb_8d4jkySoXe4.jpg", w=440),
    N(tg + 0.3, 1240, 760, src="assets/channel/qr_8d4jkySoXe4.png", w=150, ar=1),
    N(tf, 680, 470, "الفيلم القصير اللي اتعمل بالـ AI", src="assets/channel/thumb_PJTcdeSiDUI.jpg", w=440),
    N(tf + 0.3, 680, 760, src="assets/channel/qr_PJTcdeSiDUI.png", w=150, ar=1)])

# ---------- note 22: looks vs lip sync, side by side, each on its word ----------
tl, ts = T("looks", 195.0), T("lipsync", 199.5)
spec(tl - 0.3, ts + 3.6, None, None, [
    N(tl, 1250, 470, "looks: مكان ولبس جديد", src=GEN + "avatar_015_C02.mp4", w=560, loop=4, sub="الوش والمكان متولّدين"),
    N(ts, 670, 470, "lip sync: فيديو حقيقي", src="assets/ai/heygen/avatar_clips_v1/avatar_001_C00.mp4", w=560, loop=3, sub="البق بس اللي اتغير")])

# ---------- notes 25-27: the VOICE family = a mind map that builds on his words (+ live wave) ----------
a = T("الصوت", 226.5) - 0.1
br = [("text", "text to speech", "تكتب ← والموديل يقرا", 1480, 300), ("clone:", "voice clone", "سريعة: دقيقة–اتنين · احترافية: ½–3 ساعات", 1560, 560),
      ("changer", "voice changer", "صوتك ← صوت تاني", 1480, 820), ("design", "voice design", "توصف ← صوت جديد", 440, 820),
      ("مؤثرات", "مؤثرات من وصف", "«انفجار بعيد» ← صوت", 360, 560), ("وتنضيف", "تنضيف الدوشة", "دوشة ← صوت نضيف", 440, 300),
      ("وفصل", "فصل الصوت عن المزيكا", "غنا | مزيكا", 960, 220)]
items = [N(a + 0.1, 960, 470, "الصوت", emo="studio_microphone", size=44, bg="mustard")]
times = []
after = a
for key, name, sub, x, y in br:
    t = T(key, after); times.append(t); after = t + 0.2
for i, ((key, name, sub, x, y), t) in enumerate(zip(br, times)):
    nxt = times[i + 1] if i + 1 < len(times) else None
    items += [E(t - 0.15, 960 + (x - 960) * 0.22, 470 + (y - 470) * 0.22, x + (960 - x) * 0.18, y + (470 - y) * 0.18),
              N(t, x, y, name, sub=sub, size=28, act=(t, (nxt or t + 3) - 0.2), dim=(nxt or t + 4))]
t_clean = times[5]
items += [W(a + 0.1, 960, 600, w=460, h=120, out=t_clean - 0.6)]
items += [W(t_clean, 960, 600, w=460, h=120, mode="clean", clean_t=t_clean + 0.6, color="#5FD3E6", out=times[6] - 0.1)]
t_win = T("كسب", 255.0)
items += [N(T("جربنا", 254.0), 960, 800, "جربنا كذا صوت.. واللي بتسمعه ده هو اللي كسب ✓", size=26, bg="mustard", good=True)]
spec(a, T("Suno", 259.5) - 0.15, None, None, items)

# Suno = the same way
a = T("Suno", 259.5) - 0.1
t1, t2, t3, t4, t5 = T("الكلمات", 261.5), T("تعدل", 266.0), T("كورال", 270.0), T("cover", 271.8), T("stems", 274.0)
spec(a, T("الثري", 281.0) - 0.15, None, None, [
    N(a + 0.1, 960, 450, logo=lg("suno.png"), label="Suno: أغنية كاملة", size=30),
    E(t1 - 0.1, 880, 480, 520, 330), TY(t1, 520, 250, "كلمات + «عود وطبلة حديثة»", w=420, rtl=True, head="✎"), N(t1 + 1.2, 520, 430, "← أغنية بصوت ومزيكا", emo="musical_notes", size=24),
    E(t2 - 0.1, 1040, 480, 1400, 330), TY(t2, 1400, 250, "خلّي الكورس يتغنى كورال", w=420, rtl=True, head="✎"), N(t3, 1400, 430, "اتعدّل الجزء ده بس", emo="check_mark_button", size=24),
    E(t4 - 0.1, 960, 520, 960, 640), N(t4, 960, 690, "cover · extend · مزج أغنيتين", size=26),
    W(t5, 700, 820, w=360, h=90, color="#E0642E"), N(t5 + 0.2, 700, 900 - 20, "الفوكال لوحده", size=22),
    W(t5 + 0.5, 1220, 820, w=360, h=90, color="#5FD3E6", gain=0.8), N(t5 + 0.7, 1220, 880, "الطبلة لوحدها", size=22)])

# ---------- note 29: Blender grey motion and the generated look, SAME moment, both moving ----------
a = T("وأحسن", 301.5) - 0.1
spec(a, T("فيه", 316.8) - 0.2, "أحسن تريك: الحركة من Blender.. والشكل من الـ AI", a + 0.2, [
    N(a + 0.6, 1250, 500, "Blender رمادي: الحركة والكاميرا", src="output/blockouts_v1/bridge_blockout.mp4", w=600, loop=6),
    N(a + 0.6, 670, 500, "← بعد التوليد: الشكل", src=CL + "look_bridge.mp4", w=600, loop=6),
    E(a + 1.0, 955, 500, 975, 500, arrow=False)])
a = T("ستة", 877.0) - 0.1
spec(a, a + 4.4, "الحركة من Blender والشكل من التوليد", a + 0.2, [
    N(a + 0.3, 1250, 500, "Blender رمادي", src="output/blockouts_v1/lab_blockout.mp4", w=600, loop=5),
    N(a + 0.3, 670, 500, "← بعد التوليد", src=CL + "look_lab.mp4", w=600, loop=5)])

# ---------- note 31: the AI that UNDERSTANDS ----------
a = T("فيه", 316.8) - 0.1; tw = T("Whisper", 321.0); tcap = T("الكابشن", 324.5); tocr = T("OCR", 327.0); tdes = T("بتوصف", 329.0); tvid = T("وبتحلل", 330.5)
g = tocr - 0.25
spec(a, T("دلوقتي", 334.5) - 0.15, "الـ AI اللي بيفهم.. مش بيولّد", a + 0.2, [
    W(tw, 420, 380, w=340, h=100, out=g), E(tw + 0.4, 610, 380, 830, 380, out=g),
    N(tw + 0.5, 960, 380, logo=lg("whisper.png"), label="Whisper", size=26, out=g),
    E(tw + 1.0, 1090, 380, 1270, 380, out=g), TY(tw + 1.2, 1460, 320, "05.2 الموديل\n05.8 غير\n06.1 الأداة", w=330, rtl=True, dur=30, out=g),
    N(tcap, 1330, 600, "الكابشن", emo="memo", size=26, out=g), N(tcap + 0.4, 1590, 600, "الشابترز", emo="card_index_dividers", size=26, out=g),
    E(tcap, 1460, 470, 1340, 570, out=g), E(tcap + 0.4, 1460, 470, 1580, 570, out=g),
    N(tocr, 1440, 300, "OCR: بيقرا الكلام اللي في الصورة", size=24),
    SC(tocr, 1440, 590, PD + "p06.png", w=330, ar=0.9, mode="ocr", text="video maker · 20 style"),
    N(tdes, 960, 300, "بيوصف الصورة", size=24),
    SC(tdes, 960, 590, KF + "kf_026_C02b.png", w=400, boxes=[dict(x=38, y=18, w=24, h=70, label="راجل"), dict(x=72, y=40, w=24, h=30, label="عربية حنطور"), dict(x=4, y=8, w=30, h=40, label="مشربية")]),
    N(tvid, 480, 300, "بيحلل فيديو ثانية بثانية", size=24),
    N(tvid, 480, 540, src=CL + "clip_029_C02b.mp4", w=380, loop=4), TY(tvid + 0.3, 480, 680, "0:01 سوق قديم · 0:03 الكاميرا بتطلع · 0:05 مآذن", w=400, rtl=True, size=18)])

# tour of the sites
a = T("دلوقتي", 334.5) - 0.1; tmon = T("شهر", 340.5)
sites = [("heygen.ico", 1560), ("elevenlabs.png", 1290), ("higgsfield.png", 1020), ("suno.png", 750), ("claude.svg", 480), ("openai-codex.png", 210)]
names = ["HeyGen", "ElevenLabs", "Higgsfield", "Suno", "Claude", "Codex"]
it = [N(a + 0.3 + i * 0.35, x, 470 + (60 if i % 2 else -60), logo=lg(f), label=names[i], size=22) for i, (f, x) in enumerate(sites)]
it += [E(a + 0.45 + i * 0.35, sites[i][1] - 70, 470 + (60 if i % 2 else -60), sites[i + 1][1] + 70, 470 + (-60 if i % 2 else 60), bend=40) for i in range(len(sites) - 1)]
it += [N(a + 0.3, 960, 760, "لحد نوفمبر 2026", emo="calendar", size=30), N(tmon, 960, 860 - 10, "بتتغير كل شهر.. دي صورة لدلوقتي", size=22)]
spec(a, T("نبدأ", 343.5) + 1.0, "جولة في المواقع", a + 0.2, it)

# HeyGen = branches from its logo, each with its own little motion (Aly: «تعبر ب motion graphic تحت كل واحدة»), then price bars
a = T("HeyGen", 345.0) - 0.4
k = [T("Avatar", 346.0), T("Looks", 349.5), T("Agent", 353.0), T("ترجمة", 359.0), T("LiveAvatar", 362.5), T("HyperFrames", 366.0), T("MCP", 371.5), T("مجاني", 375.5), T("Creator", 376.5)]
g2 = k[4] - 0.2; g3 = k[7] - 0.3
X4 = [1500, 1140, 780, 420]
spec(a, T("ElevenLabs", 379.5) - 0.15, None, None, [
    N(a + 0.2, 960, 220, logo=lg("heygen.ico"), label="HeyGen", size=26),
    E(k[0], 1000, 290, X4[0], 360, out=g2), N(k[0], X4[0], 520, "Avatar 6: twin", src=GEN + "avatar_012_C02.mp4", w=300, loop=4, sub="من كليب 15 ث بس", out=g2),
    E(k[1], 980, 290, X4[1], 360, out=g2), N(k[1], X4[1], 520, "Looks", src="assets/ai/heygen/look_S4g/ex_generated.mp4", w=300, loop=4, sub="نفس الشخص.. مكان ولبس تاني", out=g2),
    E(k[2], 940, 290, X4[2], 360, out=g2), TY(k[2], X4[2], 380, "فكرة: طيارة فوق القاهرة", w=300, rtl=True, head="✎", out=g2, dur=25),
    E(k[2] + 1.0, X4[2], 450, X4[2], 500, out=g2), N(k[2] + 1.1, X4[2], 600, "Video Agent", src=CL + "clip_183_C11.mp4", w=300, loop=4, sub="لقطات + أفاتار", out=g2),
    E(k[3], 920, 290, X4[3], 360, out=g2), dict(k="num", t=k[3], x=X4[3], y=470, to=175, label="لغة", out_t=g2), W(k[3] + 0.5, X4[3], 690, w=280, h=80, out=g2),
    N(k[3] + 0.5, X4[3], 780, "ترجمة + lip sync", emo="globe_showing_europe-africa", size=22, out=g2),
    E(k[4], 1000, 290, 1440, 360, out=g3), N(k[4], 1440, 520, "LiveAvatar: بيرد في مكالمة", src=GEN + "avatar_015_C02.mp4", w=320, loop=4, out=g3),
    E(k[5], 960, 290, 960, 360, out=g3), TY(k[5], 960, 380, "<h1>أهلاً</h1>\nanimate(fadeIn)", w=320, head="HTML", out=g3, dur=25),
    E(k[5] + 1.0, 960, 470, 960, 530, out=g3), N(k[5] + 1.1, 960, 620, "HyperFrames ← فيديو", emo="film_frames", size=24, out=g3),
    E(k[6], 920, 290, 480, 360, out=g3), N(k[6], 400, 480, logo=lg("claude.svg"), size=24, out=g3), N(k[6] + 0.3, 580, 480, logo=lg("heygen.ico"), size=24, out=g3),
    E(k[6] + 0.5, 460, 480, 520, 480, out=g3), N(k[6] + 0.6, 490, 620, "MCP: Claude يكلّم HeyGen", size=24, out=g3),
    B(k[7], 760, 790, 20, 0, "مجاني"), B(k[8], 1160, 790, 330, 29, "Creator", sub="600 كريدت / شهر")], sfx=[("cash", k[8])])

# ElevenLabs = a tree of 3 departments, then tools, then price bars
a = T("ElevenLabs", 379.5) - 0.2
e = [T("ElevenCreative", 382.0), T("ElevenAgents", 384.5), T("ElevenAPI", 386.5), T("Library", 389.0), T("Studio", 393.0), T("Flows", 397.0), T("Music", 400.0), T("Scribe", 402.0), T("Starter", 405.5), T("وCreator", 407.0)]
g2, g3 = e[3] - 0.3, e[8] - 0.3
spec(a, T("Higgsfield", 411.5) - 0.15, None, None, [
    N(a + 0.2, 960, 240, logo=lg("elevenlabs.png"), label="ElevenLabs", size=26),
    E(e[0], 900, 290, 500, 420, out=g2), N(e[0], 500, 470, "ElevenCreative: صناعة المحتوى", emo="clapper_board", size=26, out=g2),
    E(e[1], 960, 290, 960, 560, out=g2), N(e[1], 960, 620, "ElevenAgents: مساعدين صوتيين", emo="telephone_receiver", size=26, out=g2),
    E(e[2], 1020, 290, 1420, 420, out=g2), N(e[2], 1420, 470, "ElevenAPI: للمبرمجين", emo="laptop", size=26, out=g2),
    N(e[3], 470, 500, "Voice Library + voice clone", src=EV + "eleven_creative.png", w=340, out=g3),
    N(e[4], 960, 500, "Studio Agent: أول نسخة", src=EV + "eleven_agent.png", w=340, out=g3),
    N(e[5], 1450, 420, "Flows: nodes بتتوصل", emo="gear", size=22, out=g3),
    N(e[5] + 0.3, 1330, 540, "صوت", size=20, out=g3), N(e[5] + 0.6, 1570, 540, "مزيكا", size=20, out=g3), N(e[5] + 0.9, 1450, 660, "فيديو", size=20, out=g3),
    E(e[5] + 0.4, 1360, 560, 1430, 640, out=g3), E(e[5] + 0.7, 1540, 560, 1470, 640, out=g3),
    N(e[6], 700, 760, "Music + Sound Effects", emo="musical_notes", size=22, out=g3),
    N(e[7], 1200, 760, "Scribe: كلام ← نص بتوقيت", src=EV + "eleven_scribe.png", w=300, out=g3),
    B(e[8], 760, 790, 70, 6, "Starter", logo=lg("elevenlabs.png")), B(e[9], 1160, 790, 255, 22, "Creator", sub="فيه voice clone الاحترافي", logo=lg("elevenlabs.png"))],
    sfx=[("cash", e[8]), ("cash", e[9])])

# Higgsfield = many models under ONE roof + cost per generation
a = T("Higgsfield", 411.5) - 0.2
h = [T("Seedance", 414.5), T("Kling", 416.0), T("MiniMax", 416.8), T("Wan", 417.5), T("Cinema", 420.5), T("Genjutsu", 429.0), T("Supercomputer", 430.5), T("MCP", 434.5), T("تمانين", 444.0), T("ستاشر", 447.0)]
g2, g3 = h[4] - 0.3, T("تكلفته", 436.5) - 0.3
roof = [E(a + 0.3, 520, 420, 960, 240, arrow=False, out=g2, dur=12), E(a + 0.3, 1400, 420, 960, 240, arrow=False, out=g2, dur=12)]
spec(a, T("Suno", 449.5) - 0.15, "موديلات كتير تحت سقف واحد", a + 0.2, roof + [
    N(a + 0.2, 960, 320, logo=lg("higgsfield.png"), size=22, out=g2),
    N(h[0], 600, 540, logo=lg("seedance.ico"), label="Seedance 2.5 · 4K", size=22, out=g2), N(h[1], 840, 540, logo=lg("kling.png"), label="Kling", size=22, out=g2),
    N(h[2], 1080, 540, logo=lg("minimax.ico"), label="MiniMax", size=22, out=g2), N(h[3], 1320, 540, logo=lg("wan.ico"), label="Wan", size=22, out=g2),
    N(h[4], 560, 520, "Cinema Studio 4.0", sub="كاميرا · عدسة · إضاءة · +30 حركة", emo="movie_camera", size=26, out=g3),
    N(h[5], 1000, 520, "Genjutsu", src=EV + "hf_genjutsu_len.png", w=320, out=g3),
    N(h[6], 1400, 450, "Supercomputer: agent بيشتغل خطوات", emo="robot", size=22, out=g3),
    N(h[7], 1400, 640, logo=lg("claude.svg"), label="MCP لـ Claude", size=22, out=g3),
    N(g3 + 0.3, 960, 260, "كل توليد بيقولك تكلفته قبل ما تدفع", emo="money_bag", size=28),
    B(h[8], 760, 790, 330, 80, "Seedance 2.5", sub="5 ث بجودة 1080", logo=lg("seedance.ico"), unit="كريدت"),
    B(h[9], 1160, 790, 66, 16, "Kling 4.0", sub="5 ث", logo=lg("kling.png"), unit="كريدت")], sfx=[("cash", h[8]), ("cash", h[9])])

# ---------- note 33: Claude = 3 screens that SHOW what each does, then the plans in green ----------
a = T("Claude:", 474.0) - 0.2
c = [T("claude.ai", 475.5), T("Projects", 476.5), T("Connectors", 477.8), T("Skills", 480.5), T("Chrome", 482.5), T("Code", 484.4), T("Pro", 486.5), T("وMax", 488.0), T("وUltra", 489.3)]
g3 = c[6] - 0.3
spec(a, T("Codex", 490.5) - 0.15, None, None, [
    N(a + 0.1, 960, 210, logo=lg("claude.svg"), label="Claude", size=26),
    TY(c[0], 1470, 300, "إنت: اكتبلي سكريبت الحلقة\nClaude: أكيد، دي أول نسخة…", w=400, rtl=True, head="claude.ai", out=g3),
    N(c[1], 1470, 500, "Projects: فولدر لكل مشروع", emo="file_folder", size=22, out=g3),
    N(c[2], 1470, 590, "Connectors: فيشة لأي أداة", emo="electric_plug", size=22, out=g3),
    N(c[3], 1470, 680, "Skills: كراسات خبرة", emo="notebook", size=22, out=g3),
    N(c[4], 960, 480, "Claude in Chrome: بيدوس ويكتب في الصفحة", src="research/pages_v4/higgsfield_image_crop.png", w=360, ar=1385 / 779, out=g3),
    TY(c[5], 450, 300, "> claude\n✓ make_props_v5.py اتعدّل\n✓ render_v5.sh اشتغل\n✓ rough_cut_v5.mp4", w=400, head="Claude Code", out=g3),
    N(c[5] + 0.6, 450, 560, "Claude Code: بيشتغل على ملفاتك", emo="technologist", size=22, out=g3),
    B(c[6], 640, 790, 40, 20, "Pro", logo=lg("claude.svg")), B(c[7], 960, 790, 165, 100, "Max", logo=lg("claude.svg")), B(c[8], 1280, 790, 330, 200, "Ultra", logo=lg("claude.svg"))],
    sfx=[("cash", c[6]), ("cash", c[7]), ("cash", c[8])])

# ---------- note 32: the price summary, all tools side by side ----------
a = T("بكام", 926.5) - 0.6
p = [T("Claude", 931.5), T("ElevenLabs", 933.5), T("HeyGen", 935.5), T("Suno", 937.5), T("وHiggsfield", 939.2), T("والمجاني", 941.0)]
spec(a, T("وتكلفة", 947.5) - 0.15, "كل ده بكام؟ (نوفمبر 2026)", a + 0.2, [
    B(p[0], 500, 790, 140, 20, "Claude Pro", logo=lg("claude.svg")), B(p[1], 720, 790, 42, 6, "ElevenLabs", logo=lg("elevenlabs.png")),
    B(p[2], 940, 790, 200, 29, "HeyGen", logo=lg("heygen.ico")), B(p[3], 1160, 790, 70, 10, "Suno Pro", logo=lg("suno.png")),
    N(p[4], 1480, 480, "Higgsfield: بالكريدت حسب الخطة", logo=lg("higgsfield.png"), size=22),
    N(p[5], 960, 300, "ببلاش على جهازك: Whisper · Blender · Remotion · HyperFrames · ffmpeg · ComfyUI", size=24, bg="olive")],
    sfx=[("cash", p[0]), ("cash", p[1]), ("cash", p[2]), ("cash", p[3])])


# ---------- the closing list of his videos: a 3 x 2 grid, every thumbnail WITH its QR under it, each on its title ----------
vids = [("H5oOZypINf0", "«عايز", 1239.5), ("PJTcdeSiDUI", "والفيلم", 1242.5), ("10UXB0cT4Ss", "و«إزاي", 1244.6),
        ("8d4jkySoXe4", "وفيديو", 1249.2), ("ZXQLSxYmLsw", "و«شيل", 1250.6), ("Ps7A-UXx-5g", "والـ", 1252.0)]
a = T("منها", 1237.3) - 0.1
grid = []
for i, (vid, w_, af) in enumerate(vids):
    t = T(w_, af); col, row = i % 3, i // 3; x = 1400 - col * 440; y = 340 + row * 320
    grid += [N(t, x, y, src=f"assets/channel/thumb_{vid}.jpg", w=330), N(t + 0.25, x, y + 175, src=f"assets/channel/qr_{vid}.png", w=100, ar=1)]
spec(a, T("دوّر", 1254.0) + 1.0, "منها حاجات موجودة على القناة", a + 0.2, grid)

# sub-categories (note 18): (start word, after, family index, name)
SUBS = [("الصور", 100.5, 0, "الصور"), ("الفيديو", 140.3, 0, "الفيديو"), ("هنا", 187.0, 0, "الأفاتار"), ("الصوت", 226.5, 0, "الصوت"),
        ("Suno", 259.5, 0, "المزيكا"), ("الثري", 281.0, 0, "3D"), ("فيه", 316.8, 0, "الـ AI اللي بيفهم"), ("دلوقتي", 334.5, 0, "جولة المواقع"),
        ("Claude:", 474.0, 1, "Claude"), ("Codex", 490.5, 1, "Codex"), ("والموديلات", 511.5, 1, "الموديلات الصيني"), ("ولو", 530.0, 0, "على جهازك ببلاش"),
        ("طب", 566.5, 1, "الـ LLM والـ agent"), ("الـ", 609.5, 2, "السكريبتات"), ("الـ", 628.5, 3, "الـ MCP"), ("الـ", 650.0, 4, "الـ skills"),
        ("خليني", 671.5, 5, "تجربة حقيقية"), ("تعالى", 746.5, 5, "خطوة بخطوة"), ("شوية", 837.0, 5, "تريكات"), ("طب", 926.5, 5, "الأسعار"),
        ("الـ", 954.0, 5, "دور الإنسان"), ("يوتيوب", 985.0, 5, "علامة الـ AI")]

# ======================= v6: every spec was written in v5 time -> moved to the v6 order (timeline_v6 pieces) =======================
T5_ = json.load(open("work/timeline_v5.json", encoding="utf-8")); T6_ = json.load(open("work/timeline_v6.json", encoding="utf-8"))
def C(t5):
    """a v5 second -> v6 (through the source second). Re-voiced sentences map linearly onto their new file piece."""
    d = 0.0; rep = None
    sp = 0.0
    for e in T5_["edits"]:
        st = e["v2_a"] + sp; en = st + (e["trim"][1] - e["trim"][0] if e["file"] else 0)
        if e["file"] and st - 1e-6 <= t5 <= en + 1e-6: rep = (e["v2_a"], e["v2_b"], (t5 - st) / max(0.01, en - st))
        sp += e["delta"]
    if rep is None:
        for e in T5_["edits"]:
            if t5 >= e["v2_b"] + d + e["delta"] - 1e-6: d += e["delta"]
        t2 = t5 - d
    else:
        t2 = rep[0] + rep[2] * (rep[1] - rep[0])
    for p in T6_["pieces"]:
        if p["kind"] == "v2" and p["a"] - 1e-6 <= t2 <= p["b"] + 1e-6: return round(p["t"] + t2 - p["a"], 3)
        if p["kind"] == "file" and p.get("rep") and p["rep"][0] - 1e-6 <= t2 <= p["rep"][1] + 1e-6:
            r0, r1 = p["rep"]; return round(p["t"] + (t2 - r0) / max(0.01, r1 - r0) * (p["b"] - p["a"]), 3)
    near = min((p for p in T6_["pieces"] if p["kind"] == "v2"), key=lambda p: min(abs(t2 - p["a"]), abs(t2 - p["b"])))
    return round(near["t"] + min(max(t2, near["a"]), near["b"]) - near["a"], 3)
for sp_ in SPECS:
    a5 = sp_["a"]; sp_["a"] = C(sp_["a"]); sp_["b"] = C(sp_["b"])
    if sp_["title_t"] is not None: sp_["title_t"] = C(sp_["title_t"])
    for it in sp_["items"]:
        for k in ("t", "out_t", "clean_t", "dim_t"):
            if it.get(k) is not None: it[k] = C(it[k])
        if it.get("act_t"): it["act_t"] = [C(it["act_t"][0]), C(it["act_t"][1])]
    sp_["sfx"] = [(n, C(t)) for n, t in sp_["sfx"]]
# a spec whose two ends landed in different pieces (the new order split them) is kept inside the piece where most of its items are
import collections as _c
# sections = runs of pieces between two separators (a spec may span pieces of ONE section, never a separator)
_SEC = []
for p in T6_["pieces"]:
    ln = p["dur"] if p["kind"] == "gap" else p["b"] - p["a"]
    if p["kind"] == "gap" or not _SEC or _SEC[-1][2]: _SEC.append([p["t"], p["t"] + ln, p["kind"] == "gap"])
    else: _SEC[-1][1] = p["t"] + ln
def _piece(t6):
    for i, (a_, b_, g_) in enumerate(_SEC):
        if a_ - 0.35 <= t6 <= b_ + 0.35 and not g_: return i
    return None
for sp_ in SPECS:
    ia, ib = _piece(sp_["a"]), _piece(sp_["b"])
    if ia != ib:
        votes = _c.Counter(_piece(it["t"]) for it in sp_["items"] if it.get("t") is not None)
        k = votes.most_common(1)[0][0] if votes else ia
        p0, p1 = _SEC[k][0], _SEC[k][1]
        sp_["a"] = max(sp_["a"], p0) if ia == k else p0
        sp_["b"] = min(sp_["b"], p1) if ib == k else p1
        sp_["items"] = [it for it in sp_["items"] if it.get("t") is None or p0 - 0.5 <= it["t"] <= p1 + 0.5]
SPECS = [s for s in SPECS if s["b"] - s["a"] > 0.5]

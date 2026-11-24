"""v11 scenes = every v10 spec (v10_new run straight in v11 time: AIW_TIMELINE / AIW_WORDS) + Aly's 16 notes on v10 (review_rough_v10_notes.md).
make_props_v11 imports SPECS + FACE_WINDOWS from here. Word times = REAL audio (words_v11_real.json, v10 note 7)."""
import os, json
os.environ.setdefault("AIW_TIMELINE", "work/timeline_v11.json"); os.environ.setdefault("AIW_WORDS", "work/words_v11_real.json")
import v10_new as V
from v10_new import N, E, TY, SC, lg, LG, A10, CH, P13, spec10, findS, drop_where, outs, sid_t, sid_end, T10, PIECE, pend, unclip_gaps
from v7_specs import W
from words_real_v11 import name_time

SPECS = V.SPECS; T11P = V.T10P; FACE_WINDOWS = list(V.FACE_WINDOWS)
A11 = "assets/v11/"; ST = "../../styles/"
UQ = json.load(open("work/pdf13/unique_v11.json"))          # the PDF pictures, duplicates removed (perceptual hash) — note 11
PDF = lambda i: UQ[i]["f"]
def nxt_piece(p): return T11P[T11P.index(p) + 1]
def drop_range(a, b, keep=lambda s: False):
    """make [a, b] free for new boards: an older board keeps the items that are OUTSIDE [a, b] (it starts later / ends earlier / is split in two)"""
    for s in list(SPECS):
        if s.get("v11") or keep(s) or s["b"] <= a or s["a"] >= b: continue
        its = s["items"]; tt = lambda it: it.get("t") if it.get("t") is not None else s["a"]
        bef = [it for it in its if tt(it) < a - 0.2 or it.get("k") == "circle"]; aft = [it for it in its if tt(it) >= b and it.get("k") != "circle"]
        if not [x for x in bef if x.get("k") != "circle"] and not aft: SPECS.remove(s); continue
        if [x for x in bef if x.get("k") != "circle"] and aft:
            tail = dict(s, a=round(b + 0.02, 3), items=aft, title_t=None); SPECS.append(tail)
        elif aft:
            s["a"] = round(max(s["a"], b + 0.02), 3); s["items"] = aft; continue
        s["b"] = round(min(s["b"], a - 0.02), 3); s["items"] = bef
        for it in s["items"]:
            if it.get("out_t") and it["out_t"] > s["b"]: it["out_t"] = s["b"]
def spec11(a, b, title=None, title_t=None, items=(), sfx=()):
    SPECS.append(dict(a=round(a, 3), b=round(b, 3), title=title, title_t=title_t, items=list(items), circle=False, sfx=list(sfx), v10=True, v11=True))
def W2(t, words, after=None, d=0.0):
    """time of the first word of `words` heard after `after` (real audio)"""
    return round(T10(words, (after if after is not None else t) - 0.3, t) + d, 3)

# ================= notes 3 + 4: libraries -> concepts -> the audiobook example step by step -> «تعالوا نسمع النتيجة» -> the RESULT =================
n1 = PIECE["N1"]; nb = {k: PIECE[k] for k in ("N1b_a", "N1b_b", "N1b_c", "N1b_d", "N1b_e", "N1b_f", "N1b_g", "N1b_h", "N1b_i")}
hold = nxt_piece(nb["N1b_i"]); assert hold["kind"] == "hold"
H0, H1 = hold["t"], hold["t"] + hold["dur"]
old = findS("مثال: حوّل كتاب لكتاب مسموع بـ Claude Code")
old["b"] = round(pend(n1) + 0.3, 3)                       # the LLM / agent board ends with N1 (its old audiobook items move out)
drop_where(old, lambda it: (it.get("t") or 0) >= pend(n1) - 0.05)
for it in old["items"]:
    if it.get("out_t") and it["out_t"] > old["b"]: it["out_t"] = old["b"]
ta = nb["N1b_a"]["t"]; tb = nb["N1b_b"]["t"]
spec11(ta - 0.1, pend(nb["N1b_b"]) + 0.2, "الـ AI libraries: زمان ودلوقتي", ta, [
    N(ta + 0.2, 1380, 300, "زمان", emo="hourglass_not_done", size=26, bg="mustard"),
    N(W2(ta, "المبرمجين"), 1380, 430, "المبرمجين بس", emo="technologist", size=22),
    N(W2(ta, "libraries"), 1380, 560, "AI libraries", emo="books", size=22),
    N(W2(ta, "المكتبات"), 1380, 690, "مكتبات مفتوحة بتعمل حاجات جاهزة", emo="package", size=19),
    N(tb + 0.1, 760, 300, "دلوقتي", emo="sparkles", size=26, bg="mustard"),
    E(tb + 0.2, 1180, 300, 900, 300, color="mustard"),
    N(W2(tb, "كمستخدم"), 760, 430, "إنت.. مستخدم عادي", emo="bust_in_silhouette", size=22),
    N(W2(tb, "Claude", tb + 2), 760, 580, "تقول لـ Claude Code", logo=LG("claude.svg"), size=20),
    N(W2(tb, "سطر"), 760, 760, "من غير ولا سطر كود منك ✓", size=21, good=True)])
tc = nb["N1b_c"]["t"]; td = nb["N1b_d"]["t"]
spec11(tc - 0.1, pend(nb["N1b_d"]) + 0.2, "برنامج على قد احتياجك", tc, [
    N(tc + 0.2, 1380, 300, "زمان: مستخدم لبرامج", emo="desktop_computer", size=22),
    N(W2(tc, "تدوّر"), 1500, 450, "مفيش وقت تدوّر على برنامج متخصص", emo="magnifying_glass_tilted_left", size=18),
    N(W2(tc, "حجمه"), 1500, 560, "البرنامج حجمه كبير", emo="floppy_disk", size=18),
    N(W2(tc, "بفلوس"), 1500, 670, "البرنامج بفلوس", emo="money_with_wings", size=18),
    N(td + 0.1, 760, 300, "دلوقتي: عصر الـ AI", emo="sparkles", size=22, bg="mustard"),
    E(td + 0.2, 1180, 560, 960, 560, color="mustard"),
    N(W2(td, "Claude"), 960 - 230, 450, logo=LG("claude.svg"), label="Claude Code", size=18),
    N(W2(td, "Codex"), 960 - 40, 450, logo=lg("openai-codex.png"), label="Codex", size=18),
    N(W2(td, "Cursor"), 960 + 150, 450, logo=LG("cursor.png"), label="Cursor", size=18),
    N(W2(td, "يكتبلك"), 760, 660, "يكتبلك برنامج على قد احتياجك بالظبط", emo="gear", size=19),
    N(W2(td, "بسيطة"), 760, 790, "حتى لو مهمة بسيطة أوي", emo="check_mark_button", size=20, good=True)])
te = nb["N1b_e"]["t"]; tf = nb["N1b_f"]["t"]
LIBS = [("pytesseract", "Python", "2019"), ("EasyOCR", "Python", "2021"), ("Tesseract.js", "JavaScript", "2023"), ("faster-whisper", "Python", "2024"), ("Kokoro", "Python", "2025")]
lib_items = []
for i, (nm, lang, yr) in enumerate(LIBS):   # library names come and go (year / language) — they are NOT what you keep
    t_ = te + 0.3 + i * 0.9   # Arabic words between the English ones: an all-English line reads backwards in the RTL layout
    lib_items.append(N(t_, 1440, 300 + (i % 3) * 110, f"مكتبة {nm} بلغة {lang} سنة {yr}", emo="package", size=17, out=t_ + 2.4))
spec11(te - 0.1, pend(nb["N1b_f"]) + 0.3, "متحفظش الأسامي.. افهم المفهوم", te, lib_items + [
    N(W2(te, "بتتغير"), 1440, 700, "الأسامي بتتغير: سنة بسنة، ولغة بلغة", emo="counterclockwise_arrows_button", size=18, out=tf - 0.1),
    N(W2(te, "المفاهيم"), 760, 300, "اللي يفضل: المفهوم", emo="light_bulb", size=24, bg="mustard"),
    N(W2(tf, "transcript"), 1440, 330, "Transcript", emo="studio_microphone", size=22),
    W(W2(tf, "transcript"), 1440, 450, w=360, h=70),
    N(W2(tf, "مكتوب"), 1440, 560, "كلام بيتقال ← كلام مكتوب", emo="memo", size=18),
    N(W2(tf, "OCR"), 960, 440, "OCR", emo="page_facing_up", size=22),
    SC(W2(tf, "OCR"), 960, 590, PDF(31), w=200, mode="ocr", ar=0.56),
    N(W2(tf, "لنص"), 960, 760, "صفحة فيها كلام ← نص", size=18),
    N(W2(tf, "TTS"), 520, 440, "TTS", emo="speaker_high_volume", size=22),
    TY(W2(tf, "TTS"), 520, 580, "«النص ده..»", w=240, rtl=True, size=18, dur=10),
    N(W2(tf, "لصوت"), 520, 720, "نص ← صوت", size=18)])
tg = nb["N1b_g"]["t"]; th = nb["N1b_h"]["t"]
spec11(tg - 0.1, pend(nb["N1b_h"]) + 0.2, "مثال: كتاب ← كتاب صوتي بـ Claude Code", tg, [
    N(W2(tg, "كتاب"), 1500, 300, "1. عندي كتاب", emo="closed_book", size=20),
    N(W2(tg, "السفرية"), 1500, 430, "عايز أسمعه في السفرية الجاية", emo="airplane", size=18),
    N(W2(tg, "فولدر"), 1500, 570, "2. أحطه في فولدر", emo="file_folder", size=20),
    TY(W2(tg, "حوّل"), 1440, 740, "«حوّل الكتاب ده لكتاب صوتي»", w=380, rtl=True, head="3. أقول لـ Claude Code:", size=18, dur=12),
    E(th, 1180, 560, 1080, 560, color="mustard"),
    TY(W2(th, "كود"), 900, 340, "import ocr_lib   # يقرا الصفحات\nimport tts_lib   # يحوّل لصوت\nfor ch in chapters: save(ch.mp3)", w=420, head="4. بيكتب كود", size=16, dur=22),
    N(W2(th, "مكتبات"), 900, 520, "5. بينزّل مكتبات مفتوحة", emo="inbox_tray", size=19),
    N(W2(th, "OCR"), 760, 620, "OCR: يقرا الصفحات", emo="page_facing_up", size=17),
    N(W2(th, "TTS"), 1040, 620, "TTS: كلام ← صوت", emo="speaker_high_volume", size=17),
    N(W2(th, "فصول"), 900, 740, "6. فصل 1.mp3 · فصل 2.mp3 · فصل 3.mp3", emo="headphone", size=18, good=True)])
ti = nb["N1b_i"]["t"]
spec11(ti - 0.05, H1 - 0.05, "تعالوا نسمع النتيجة", ti, [
    N(ti + 0.4, 960, 330, "النتيجة: الكتاب الصوتي اللي عمله Claude Code", emo="headphone", size=24, bg="mustard"),
    N(H0 + 0.3, 960, 470, "▶ فصل 1.mp3", emo="speaker_high_volume", size=22),
    W(H0 + 0.25, 960, 610, w=620, h=110),
    N(H0 + 0.8, 960, 770, "صوت معمول بـ library على الجهاز.. ببلاش", emo="laptop", size=19)])
FACE_WINDOWS.append((ta, pend(nb["N1b_i"])))                 # his talking twin (voice + picture) the whole explanation (note 4: «صوت و صورة»)
AUDIOBOOK_AT = round(H0 + 0.25, 3)                           # make_props: the result sound + its waveform start here

# ================= note 5: the Claude Code example — a REAL plain talk video, the loop (understand -> order -> wait), transparent motion =================
c = {k: PIECE[k] for k in ("N25a", "N25b", "N25c", "N25c2", "N25d", "N25e", "N25e2", "N25f", "N25g")}
SPECS.remove(findS("مثال: Claude Code من فولدر فاضي"))
a25 = c["N25a"]["t"]
spec11(a25 - 0.1, pend(c["N25c"]) + 0.15, "مثال: Claude Code من فولدر فاضي", a25, [
    N(a25 + 0.3, 1480, 300, "1. فولدر فاضي + فيديو بيشرح", emo="file_folder", size=20),
    N(W2(a25, "فيديو", a25 + 1), 1480, 470, "فيديو عادي.. من غير موشن", src=A11 + "plain_talk.mp4", w=340, loop=4.9, size=17),
    TY(c["N25b"]["t"], 960, 330, "«حط موشن على الفيديو ده»", w=360, rtl=True, head="2. بتكتب لـ Claude Code:", size=20, dur=14),
    N(W2(c["N25c"]["t"], "Whisper"), 520, 330, "3. بيفهم الفيديو", src=A10 + "web/faster_whisper_card.png", w=260, ar=2.0, size=18, sub="Whisper: الكلام + توقيت كل كلمة"),
    E(c["N25c"]["t"] + 0.3, 760, 330, 680, 330)])
t2 = c["N25c2"]["t"]   # the loop: Claude in the middle, an order goes out, a result comes back, it understands, the next order
spec11(t2 - 0.05, pend(c["N25c2"]) + 0.15, "ميزة الـ AI: يفهم ← يأمر ← يستنى ← يفهم", t2, [
    N(t2 + 0.2, 960, 560, "Claude Code", logo=LG("claude.svg"), size=22),
    N(W2(t2, "لكود"), 520, 360, "Whisper", src=A10 + "web/faster_whisper_card.png", w=220, ar=2.0, size=16),
    E(W2(t2, "أمر"), 860, 500, 640, 400, color="mustard"), N(W2(t2, "أمر"), 720, 470, "أمر", size=16, bg="mustard"),
    E(W2(t2, "النتيجة"), 640, 440, 860, 540, color="olive"), N(W2(t2, "ويفهمها"), 780, 610, "النتيجة: الكلام + التوقيت ✓", size=15),
    N(W2(t2, "تاني"), 1400, 360, "Remotion", logo=lg("remotion.png"), size=16),   # with its arrow (the name is said 0.3 s later)
    E(W2(t2, "تاني"), 1060, 500, 1300, 400, color="mustard"), N(W2(t2, "تاني"), 1210, 470, "أمر تاني", size=16, bg="mustard"),
    N(W2(t2, "لفّة"), 960, 790, "يفهم ← يأمر ← يستنى ← يفهم ← يأمر تاني..", emo="counterclockwise_arrows_button", size=20, bg="mustard"),
    N(W2(t2, "يخلص", t2 + 8), 960, 880, "لحد ما الشغل يخلص ✓", size=18, good=True)])
FACE_WINDOWS.append((t2, pend(c["N25c2"])))
t4 = c["N25d"]["t"]
spec11(t4 - 0.05, pend(c["N25g"]) + 1.1, "مثال: Claude Code من فولدر فاضي", t4, [
    TY(t4, 1480, 330, "جملة 1 ← كلمة على الشاشة\nجملة 2 ← صورة حقيقية\nجملة 3 ← رسمة بتشرح", w=360, rtl=True, head="4. خطة الموشن", size=17, dur=14),
    TY(W2(c["N25e"]["t"], "فولدرات", c["N25d"]["t"]), 960, 360, "src/\n  Video.tsx   ← الكود\npublic/\n  video.mp4\nimport {Composition} from 'remotion'", w=380, head="5. فولدرات + كود", size=16, dur=20),
    N(W2(c["N25e"]["t"], "Remotion", c["N25d"]["t"]), 960, 590, logo=lg("remotion.png"), label="library: Remotion", size=18),
    N(W2(c["N25e2"]["t"], "شفاف"), 520, 330, "الموشن لوحده: شفاف.. من غير خلفية", src=A10 + "checker_motion.mp4", w=340, loop=4.9, size=17),
    N(W2(c["N25e"]["t"], "ffmpeg"), 520, 620, logo=lg("ffmpeg.ico"), label="6–7. ffmpeg بيركّبه فوق الفيديو", size=17),
    N(c["N25g"]["t"], 1480, 650, "8. نفس الفيديو.. بالموشن ✓", src=A11 + "plain_talk_motion.mp4", w=340, loop=4.9, good=True, size=17)])
FACE_WINDOWS.append((c["N25e2"]["t"], pend(c["N25e2"])))

# ================= note 6 (general): what enters inside a group's time leaves WITH the group =================
for s in SPECS:
    its = [it for it in s["items"] if it.get("t") is not None and it.get("k") not in ("circle", "titleAt")]
    outs_ = {}
    for it in its:
        if it.get("out_t"): outs_.setdefault(round(it["out_t"], 2), []).append(it["t"])
    for o_, ts_ in outs_.items():
        if len(ts_) < 3: continue
        g0 = min(ts_)
        for it in its:
            if it.get("out_t") is None and g0 < it["t"] < o_ - 0.3: it["out_t"] = o_
# ================= note 7 (general): every logo / product card on the REAL moment its name is said =================
NAMEMAP = {"Premiere": "Premiere", "Photoshop": "Photoshop", "After Effects": "After Effects", "Blender": "Blender", "DaVinci": "DaVinci",
           "Claude Code": "Claude", "Codex": "Codex", "Cursor": "Cursor", "Antigravity": "Antigravity", "Remotion": "Remotion", "HeyGen": "HeyGen",
           "ElevenLabs": "ElevenLabs", "Higgsfield": "Higgsfield", "Suno": "Suno", "Kling": "Kling", "Veo": "Veo", "Seedance": "Seedance", "Luma": "Luma",
           "Magnific": "Magnific", "Runway": "Runway", "Firefly": "Firefly", "ComfyUI": "ComfyUI", "Meta": "Meta", "Genjutsu": "Genjutsu", "three.js": "three.js"}
SNAP = []
for s in SPECS:
    if s.get("v11"): continue
    for it in s["items"]:
        nm = NAMEMAP.get(str(it.get("label", "")).strip())
        if nm and it.get("t") is not None and (it.get("logo") or it.get("label") == nm):
            r = name_time(nm, it["t"])
            if r is not None and abs(r - it["t"]) > 0.25:
                SNAP.append((nm, it["t"], r)); it["t"] = r
                if it.get("out_t") and it["out_t"] < r + 1.0: it["out_t"] = round(r + 1.0, 3)
print("v11 logos moved to their REAL word:", len(SNAP), [(n, round(a, 1), round(b, 1)) for n, a, b in SNAP][:12])

# ================= note 8: the skill rule cards = one clean column (no stack), the folder box leaves first =================
s = findS("ممنوع overlap")
rules = [it for it in s["items"] if it.get("emo") == "check_mark_button" and it.get("size") == 17]
t_r = min(it["t"] for it in rules)
for i, it in enumerate(sorted(rules, key=lambda it: it["t"])): it.update(x=720, y=300 + 78 * i)
for it in s["items"]:
    if it.get("k") == "typed" and "aly-video-motion/" in str(it.get("text", "")): it["out_t"] = round(t_r - 0.1, 3)

# ================= note 9: HOW the football (Playmobil) script was made with the content skill =================
p37 = {k: PIECE[k] for k in ("N37a", "N37b", "N37c", "N37d")}
a37 = p37["N37a"]["t"]
drop_range(a37 - 0.05, pend(p37["N37d"]) + 1.2)
spec11(a37 - 0.05, pend(p37["N37d"]) + 1.15, "مثال حقيقي: سكريبت فيديو الماتش", a37, [
    N(a37 + 0.3, 1450, 330, "دورتموند × بايرن بستايل Playmobil", src=A10 + "playmobil_thumb.jpg", w=340, ar=16 / 9, size=17),
    N(p37["N37b"]["t"], 900, 330, "1. ادّيت الـ skill الفكرة.. كتبت السكريبت بأسلوبي", src=A10 + "skill_content.mp4", w=420, loop=13.4, size=16),
    N(p37["N37b"]["t"] + 0.8, 900, 610, "من الـ PDF صفحة 10: TOOL 2 · SCRIPT WRITER", src=P13 + "page10.png", w=260, ar=1.0, size=14),
    N(p37["N37c"]["t"], 1450, 640, "2. صوّرت أنا ← 3. الـ AI عمل Playmobil", src=A10 + "playmobil_short.mp4", w=200, ar=9 / 16, loop=8.9, size=16),
    N(W2(p37["N37d"]["t"], "مشاهدة"), 520, 560, "~31K مشاهدة على 4 منصات", src=P13 + "page22.png", w=260, ar=1.0, size=18, good=True)])

# ================= notes 11-14: «تجربة حقيقية» REBUILT — one clear idea per sentence, real pictures, no repeats, no random walls =================
g = {q["sep"][1]: q for q in T11P if q["kind"] == "gap"}
RA = g["تجربة حقيقية"]["t"] + g["تجربة حقيقية"]["dur"] + 0.02; RB = sid_end("S040.6") + 0.8
RB = min(RB, g["خطوة بخطوة"]["t"] - 0.02)
drop_range(RA, RB)
def sen(i): return sid_t(i)
t1 = sen("S037.1"); t2_ = sen("S037.2"); t3 = sen("S037.3"); r0 = PIECE["N43b_reason"]["t"]
spec11(t1 - 0.05, r0 - 0.05, "تجربة حقيقية بالأرقام", t1, [
    N(W2(t2_, "شغال"), 1450, 330, "software tester.. full-time", emo="briefcase", size=20),
    N(W2(t2_, "وقت"), 1450, 560, "المونتاج والموشن: محتاجين وقت مش موجود", emo="hourglass_not_done", size=17),
    {"k": "num", "t": W2(t3, "تلات"), "x": 760, "y": 320, "to": 3, "label": "سنين من غير فيديو جديد"},
    N(W2(t3, "كورسات"), 760, 520, "3 كورسات متسجلة.. على الرف", emo="books", size=18),
    N(W2(t3, "كورسات") + 0.3, 560, 670, src=PDF(12), w=190, ar=16 / 9), N(W2(t3, "كورسات") + 0.5, 760, 670, src=PDF(26), w=190, ar=16 / 9),
    N(W2(t3, "كورسات") + 0.7, 960, 670, src=PDF(13), w=190, ar=16 / 9),
    N(W2(t3, "الإنترو"), 1450, 760, "إنترو «انت بتشتغل إيه؟» جاهز من 2023", src=PDF(14), w=300, ar=16 / 9, size=16)])
spec11(r0 - 0.05, pend(PIECE["N43b_reason"]) + 0.3, "3 سنين.. ليه؟", r0, [
    N(r0 + 0.2, 1100, 290, "كل حاجة كانت بإيدي", emo="hourglass_not_done", size=22, bg="mustard"),
    N(W2(r0, "المونتاج"), 1500, 440, "مونتاج بإيدي", src=PDF(21), w=300, ar=16 / 9, size=17),
    N(W2(r0, "والكروما"), 1100, 440, "كروما بإيدي", src=PDF(4), w=300, ar=16 / 9, size=17),
    N(W2(r0, "VFX"), 700, 440, "VFX بإيدي", src=PDF(15), w=300, ar=16 / 9, size=17),
    N(W2(r0, "فريم"), 1300, 720, "موشن.. فريم فريم", src=PDF(17), w=300, ar=16 / 9, size=17),
    N(W2(r0, "full-time"), 860, 720, "+ شغل full-time", emo="briefcase", size=20, good=True)])
s1, s2, s3, s4, s5, s6 = (sen(x) for x in ("S038.1", "S038.2", "S038.3", "S038.4", "S038.5", "S038.6"))
covers = sorted(f for f in os.listdir("../../styles") if f[:2].isdigit() and os.path.exists(f"../../styles/{f}/cover.jpg"))[:20]
grid = [N(W2(s2, "عشرين") + 0.05 * i, 760 + (i % 5) * 160, 520 + (i // 5) * 95, src=f"{ST}{f}/cover.jpg", w=150, ar=16 / 9) for i, f in enumerate(covers)]
for gi in grid: gi["grid"] = "styles"                    # ONE block: the resolver never splits it (note 13)
spec11(s1 - 0.05, s3 - 0.05, "اللي اتبنى بـ Claude Code.. على الجهاز", s1, [
    N(s1 + 0.3, 1500, 300, "كله على الجهاز.. من غير سيرفر", logo=LG("claude.svg"), size=18),
    N(W2(s2, "video"), 1500, 520, "1. video maker: اتعلم من المشاريع القديمة", emo="clapper_board", size=17),
    N(W2(s2, "عشرين"), 1080, 330, "20 ستايل.. بيتختاروا برقم", emo="artist_palette", size=19)] + grid)
spec11(s3 - 0.05, s5 - 0.05, "اللي اتبنى بـ Claude Code.. على الجهاز", s3, [
    N(s3 + 0.1, 1450, 330, "2. skill بتكتب السكريبت بنفس الأسلوب", src=A10 + "skill_content.mp4", w=380, loop=13.4, size=16),
    N(W2(s4, "publisher"), 820, 330, "3. publisher: بيجدول وبيرفع", src=PDF(73), w=380, ar=16 / 9, fit="contain", size=16),
    {"k": "num", "t": W2(s4, "تمنية"), "x": 820, "y": 600, "to": 28, "label": "فيديو في الأسبوع"},
    *[N(W2(s4, "منصات") + 0.15 * i, 640 + i * 120, 760, logo=LG(f), size=14) for i, f in enumerate(["youtube.png", "instagram.ico", "facebook.png", "tiktok.png"])]])
spec11(s5 - 0.05, sen("S039.1") - 0.05, "اللي اتبنى بـ Claude Code.. على الجهاز", s5, [
    N(s5 + 0.1, 1450, 330, "4. أوتوميشن إنستجرام", logo=LG("instagram.ico"), size=18),
    N(W2(s6, "كلمة"), 900, 500, "بيرد على الكومنتات بنفسه", src=A10 + "script_rec_0.mp4", w=200, ar=9 / 16, size=16),
    TY(W2(s6, "يوصلك"), 1450, 560, "كومنت: «كلمة»  ←  رسالة فيها اللينك ✓", w=420, rtl=True, size=18, dur=14)])
u1, u2, u3, u4, u5 = (sen(x) for x in ("S039.1", "S039.2", "S039.3", "S039.4", "S039.5"))
spec11(u1 - 0.05, u3 - 0.05, "الفيديوهات القديمة.. حياة جديدة", u1, [
    N(W2(u2, "كورس"), 1450, 380, "كورس واحد.. ساعتين", src=PDF(26), w=380, ar=16 / 9, size=18),
    E(W2(u2, "طلع"), 1230, 380, 1080, 380, color="mustard"),
    {"k": "num", "t": W2(u2, "واحد", u2 + 1.5), "x": 860, "y": 300, "to": 31, "label": "شورت"},
    *[N(W2(u2, "شورت") + 0.12 * i, 600 + i * 130, 620, src=PDF(31 + i), w=110, ar=9 / 16) for i, _ in enumerate(range(6))]])
spec11(u3 - 0.05, u5 - 0.05, "النتيجة في آخر شهر", u3, [
    N(W2(u3, "داشبورد"), 1500, 330, "من داشبورد كل منصة", src=PDF(81), w=320, ar=16 / 9, fit="contain", size=16),
    N(W2(u3, "داشبورد") + 0.4, 1500, 560, src=PDF(0), w=320, ar=16 / 9, fit="contain"),
    {"k": "num", "t": W2(u4, "أربعمية"), "x": 940, "y": 300, "to": 474, "label": "ألف مشاهدة", "suffix": "K"},
    N(W2(u4, "Genjutsu"), 940, 560, "ريل واحد من فيديو Genjutsu", src=PDF(85), w=300, ar=16 / 9, size=16),
    N(W2(u4, "ميتين"), 560, 560, "253K على فيسبوك", src=PDF(79), w=260, ar=16 / 9, fit="contain", size=17, good=True)])
v1_, v2_, v3_, v4_, v5_, v6_ = (sen(x) for x in ("S040.1", "S040.2", "S040.3", "S040.4", "S040.5", "S040.6"))
spec11(u5 - 0.05, v1_ - 0.05, "ودلوقتي..", u5, [
    N(u5 + 0.1, 1300, 420, "شورت كل يوم", emo="mobile_phone", size=24, bg="mustard"),
    N(W2(u5, "يوتيوب"), 620, 420, "فيديو يوتيوب كل أسبوع", logo=LG("youtube.png"), size=22),
    N(W2(u5, "يوتيوب") + 0.5, 960, 650, src=PDF(23), w=520, ar=16 / 9, fit="contain")])
spec11(v1_ - 0.05, sid_end("S040.6") + 0.6, "والدروس؟", v1_, [
    N(W2(v2_, "بتتكرر"), 1450, 320, "أي حاجة بتتكرر.. تتأتمت", emo="repeat_button", size=20),
    N(W2(v3_, "يكتب"), 1450, 470, "الـ AI يكتب السكريبت", emo="robot", size=18),
    E(W2(v3_, "تشتغل"), 1220, 470, 1080, 470, color="mustard"),
    N(W2(v3_, "تشتغل"), 860, 470, "والسكريبت هو اللي يشتغل.. علشان توفّر", emo="money_bag", size=18),
    N(W2(v4_, "ego"), 1450, 650, "مفيش مكان للـ ego", emo="thinking_face", size=20),
    N(W2(v5_, "مهارات"), 860, 650, "مهارات سنين.. الـ AI بيعملها دلوقتي", src=PDF(17), w=260, ar=16 / 9, size=16),
    N(W2(v6_, "الموجة"), 1150, 830, "فاركب الموجة", emo="person_surfing", size=26, bg="mustard", good=True)])
# calibrated-checker leftovers (v10 note 8): two older boards placed by hand
s = findS("ترجمة + lip sync")
for it in s["items"]:
    if it.get("label") == "ترجمة + lip sync": it.update(x=1300, y=830)
    if it.get("k") == "wave" and abs((it.get("t") or 0) - min(x.get("t") or 9e9 for x in s["items"] if x.get("label") == "ترجمة + lip sync")) < 1.0: it.update(x=960, y=830, w=280, h=70)
s = findS("ProRes 4444")
for it in s["items"]:
    if str(it.get("label", "")).startswith("ProRes 4444"): it.update(y=895)
FACE_WINDOWS = [w for w in FACE_WINDOWS]
unclip_gaps()
MISS = [m for m in V.MISS6 if str(m[0]).startswith("v10:")]
print("v11 specs:", len(SPECS), "| face windows:", len(FACE_WINDOWS), "| words NOT found (fell back):", MISS)

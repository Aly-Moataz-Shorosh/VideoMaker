"""v10 scenes = every v9 spec (v9_new, v9 time) moved to v10 time through the SOURCE (M910) + Aly's 56 notes on v9 (review_rough_v9_notes.md).
make_props_v10 imports SPECS + FACE_WINDOWS from here."""
import json, os
import v9_new as base
TL = os.environ.get("AIW_TIMELINE", "work/timeline_v10.json"); WF = os.environ.get("AIW_WORDS", "work/words_v10.json")   # v11 builds on this in v11 time
from v7_specs import N, E, TY, SC, CL, lg

SPECS = base.SPECS; MISS6 = base.MISS6
T9P = json.load(open("work/timeline_v9.json", encoding="utf-8"))["pieces"]
T10P = json.load(open(TL, encoding="utf-8"))["pieces"]
_L = lambda p: p["dur"] if p["kind"] in ("gap", "hold") else p["b"] - p["a"]
_G9 = [p for p in T9P if p["kind"] == "gap"]; _G10 = [p for p in T10P if p["kind"] == "gap"]
assert len(_G9) == len(_G10)
def _hold10(p9):
    i = T9P.index(p9); last = T9P[i - 1]["sids"][-1]
    j = next(k for k, q in enumerate(T10P) if q.get("sids") and last in q["sids"])
    return next(q for q in T10P[j:] if q["kind"] == "hold")
def M910(t9):
    if t9 is None: return None
    best = next((p for p in T9P if p["t"] - 1e-6 <= t9 <= p["t"] + _L(p) + 1e-6), None)
    if best is None:
        prev = max((p for p in T9P if p["t"] <= t9), key=lambda p: p["t"])
        return round(M910(prev["t"] + _L(prev)) + (t9 - prev["t"] - _L(prev)), 3)
    p, off = best, t9 - best["t"]
    if p["kind"] == "gap":
        q = _G10[_G9.index(p)]; return round(q["t"] + off * q["dur"] / p["dur"], 3)
    if p["kind"] == "hold":
        q = _hold10(p); return round(q["t"] + min(off, q["dur"]), 3)
    if p["kind"] == "file":
        q = next((q for q in T10P if q["kind"] == "file" and q["sids"] == p["sids"]), None)
        if q is None:   # a re-voiced v2 piece in v10 (S028.2 / S055.4)
            q = next(q for q in T10P if q.get("sids") and q["sids"][0] == p["sids"][0])
        return round(q["t"] + off * _L(q) / max(0.01, _L(p)), 3)
    t2 = p["a"] + off
    for q in T10P:
        if q["kind"] == "v2" and q["a"] - 1e-3 <= t2 <= q["b"] + 1e-3: return round(q["t"] + t2 - q["a"], 3)
        if q["kind"] == "file" and q.get("rep") and q["rep"][0] - 1e-3 <= t2 <= q["rep"][1] + 1e-3:
            r0, r1 = q["rep"]; return round(q["t"] + (t2 - r0) / max(0.01, r1 - r0) * _L(q), 3)
    q = min((q for q in T10P if q["kind"] == "v2"), key=lambda q: min(abs(t2 - q["a"]), abs(t2 - q["b"])))
    return round(q["t"] + min(max(t2, q["a"]), q["b"]) - q["a"], 3)
for sp_ in SPECS:
    sp_["a"], sp_["b"] = M910(sp_["a"]), M910(sp_["b"])
    if sp_["title_t"] is not None: sp_["title_t"] = M910(sp_["title_t"])
    for it in sp_["items"]:
        for k_ in ("t", "out_t", "clean_t", "dim_t", "grow_t"):
            if it.get(k_) is not None: it[k_] = M910(it[k_])
        if it.get("act_t"): it["act_t"] = [M910(it["act_t"][0]), M910(it["act_t"][1])]
        if it.get("hide"): it["hide"] = [[M910(a_), M910(b_)] for a_, b_ in it["hide"]]
    sp_["sfx"] = [(n, M910(t)) for n, t in sp_["sfx"]]

W10 = json.load(open(WF, encoding="utf-8"))
def T10(word, after, default=None, win=12):
    key = word.split()[0].lower()
    for w in W10:
        if w["a"] >= after - 0.4 and key in w["w"].lower():
            if w["a"] - after > win: break
            return round(w["a"], 3)
    MISS6.append(("v10:" + word, after)); return round(default if default is not None else after, 3)
PIECE = {q["sids"][0]: q for q in T10P if q.get("sids")}
pend = lambda q: q["t"] + _L(q)
def V2T(t2):
    for q in T10P:
        if q["kind"] == "v2" and q["a"] - 1e-3 <= t2 <= q["b"] + 1e-3: return round(q["t"] + t2 - q["a"], 3)
    raise KeyError(t2)
SENT = {x["id"]: x for x in json.load(open("work/sentences_v3.json", encoding="utf-8"))}
def sid_t(sid):
    """the v10 time where SENTENCE sid starts (a v2 piece can hold many sentences)"""
    q = next(q for q in T10P if q.get("sids") and sid in q["sids"])
    if q["kind"] == "v2" and sid in SENT: return round(q["t"] + max(0.0, SENT[sid]["a"] - q["a"]), 3)
    return q["t"]
def sid_end(sid):
    q = next(q for q in T10P if q.get("sids") and sid in q["sids"])
    if q["kind"] == "v2" and sid in SENT: return round(q["t"] + min(q["b"], SENT[sid]["b"]) - q["a"], 3)
    return pend(q)
def spec10(a, b, title=None, title_t=None, items=(), sfx=()):
    SPECS.append(dict(a=round(a, 3), b=round(b, 3), title=title, title_t=title_t, items=list(items), circle=False, sfx=list(sfx), v10=True))
# boards whose range broke in an earlier mapping (end before start): rebuild the range from their own items, end at the next separator
for sp_ in SPECS:
    ts = [it["t"] for it in sp_["items"] if it.get("t") is not None]
    if ts and (sp_["b"] <= sp_["a"] + 0.5 or min(ts) > sp_["b"]):
        sp_["a"] = round(min(ts) - 0.15, 3)
        ends = [it["out_t"] for it in sp_["items"] if it.get("out_t")] + [max(ts) + 2.5]
        nxt = min([q["t"] for q in T10P if q["kind"] == "gap" and q["t"] > max(ts)] or [max(ends)])
        sp_["b"] = round(min(nxt - 0.02, max(ends) + 1.0), 3)
def findS(sub):
    for s in SPECS:
        if sub == s.get("title"): return s
        for it in s["items"]:
            if sub in str(it.get("label", "")) or sub in str(it.get("src", "")) or sub in str(it.get("text", "")): return s
    raise KeyError(sub)
def outs(items, t):
    for it in items: it["out_t"] = round(t, 3)
    return items
def drop_where(s, f): s["items"] = [it for it in s["items"] if not f(it)]
A10 = "assets/v10/"; H10 = "assets/ai/heygen/v10/"; CH = "assets/channel/"; P13 = "work/pdf13/"; LG = lambda f: "../../brand/logos-tools/" + f
SRC = lambda t: N(None, 0, 0, t)   # placeholder (unused)
def tag(t, x, y, text, out=None): return N(t, x, y, text, size=15, bg="olive", out=out)   # «المصدر: …» tag under a web clip

# ---------------- general: logos / clips that were WRONG everywhere ----------------
for sp_ in SPECS:
    for it in sp_["items"]:
        lg_ = str(it.get("logo", "")); src_ = str(it.get("src", ""))
        if lg_.endswith("luma.ico"): it["logo"] = LG("luma-card.png")                                    # note 16
        if "magnific_home" in src_: it.pop("src", None); it.pop("ar", None); it["logo"] = LG("magnific-mark.png"); it.pop("w", None)   # note 13
        if lg_.endswith("whisper.png"):                                                                   # notes 20 (+13:11)
            it["logo"] = None; it.pop("logo"); it["src"] = A10 + "web/faster_whisper_card.png"; it["w"] = 300; it["ar"] = 2.0
            it["label"] = "Whisper (OpenAI)"; it["sub"] = "على جهازي: faster-whisper"
        if src_.endswith("claude_session_2x.mp4") and "Chrome" in str(it.get("label", "")):              # note 21
            it.update(src=A10 + "claude_chrome_official.mp4", ar=16 / 9, w=420, sub="من صفحة Claude in Chrome الرسمية — claude.com/chrome", loop=True, loopDur=9.8)

# ---------------- note 3 / 17 / 32: separators are never covered by a board ----------------
GAPS = [(q["t"], q["t"] + q["dur"]) for q in T10P if q["kind"] == "gap"]
def unclip_gaps():
    for sp_ in SPECS:
        for ga, gb in GAPS:
            if sp_["a"] < ga < sp_["b"] and sp_["b"] <= gb + 30:
                if ga - sp_["a"] >= 1.0: sp_["b"] = round(ga - 0.02, 3)
            if ga - 0.05 <= sp_["a"] < gb: sp_["a"] = round(gb + 0.02, 3)

# ---------------- note 4: v2v — «والحركة زي ما هي» under the row, no overlap ----------------
s = findS("video to video: نفس الحركة.. حاجة واحدة بتتغير")
for it in s["items"]:
    if str(it.get("label", "")).startswith("والحركة زي ما هي"): it.update(y=912, size=20)
    if it.get("label") in ("غيّر الستايل", "غيّر الشخصية: فرعون", "غيّر المكان: شارع نيون"): it["y"] = 680
    if it.get("label") == "الفيديو الأصلي": it["y"] = 300

# ---------------- note 5: Genjutsu — the WHOLE reel on the word «Genjutsu», 253K under it, a real Genjutsu picture ----------------
s = findS("الريل نفسه: اتعمل بـ Genjutsu")
tg = T10("Genjutsu:", sid_t("S010.3"))
drop_where(s, lambda it: it.get("k") == "num" or str(it.get("src", "")).endswith(("hf_genjutsu_len.png", "genjutsu_reel.mp4")) or it.get("label") in ("253 ألف مشاهدة على فيسبوك",))
s["items"] += [N(tg, 600, 430, "الريل نفسه: اتعمل بـ Genjutsu", src=A10 + "genjutsu_reel_full.mp4", w=560, size=20),
               {"k": "num", "t": tg + 0.8, "x": 600, "y": 790, "to": 253, "label": "253 ألف مشاهدة على فيسبوك", "suffix": "K"},
               N(tg + 0.5, 1380, 430, "Genjutsu: تبدّل حاجة في الفيديو بصورة", src=A10 + "genjutsu_official.mp4", w=520, loop=8.8, size=20,
                 sub="من صفحة Genjutsu الرسمية — higgsfield.ai/genjutsu")]
s["b"] = max(s["b"], round(tg + 16.2, 3))   # the reel plays to its last frame
# note 6: the three words with a REAL explaining visual above each (on «تطويل / وتكبيره / الفريمات»)
t_ext = T10("تطويل", sid_t("S010.6")); t_up = T10("وتكبيره،", t_ext); t_fr = T10("الفريمات", t_up)
spec10(t_ext - 0.15, max(t_fr + 4.5, sid_end("S010.6")), None, None, [
    N(t_ext, 1430, 380, src=A10 + "extend_strip.jpg", w=440, ar=2.55), N(t_ext + 0.2, 1430, 560, "تطويل: نفس اللقطة بتكمل", emo="play_button", size=20),
    N(t_up, 960, 350, "قبل", src=A10 + "upscale_before.jpg", w=250), N(t_up + 0.5, 960, 560, "بعد: 4K", src=A10 + "upscale_after.jpg", w=250, good=True),
    N(t_fr, 490, 330, "5 فريم في الثانية: بيقطّع", src=A10 + "frames_choppy.mp4", w=300, loop=4),
    N(t_fr + 0.6, 490, 600, "بعد زيادة الفريمات: ناعم", src=A10 + "frames_smooth.mp4", w=300, loop=4, good=True)])

# ---------------- notes 8 / 9: looks — presenter WIDE, the top-left room -> a different studio ----------------
for it in findS("مقدم واقف")["items"]:
    if it.get("label") == "مقدم واقف": it["src"] = "assets/ai/heygen/v10/look10_presenter_wide.mp4"
    if it.get("label") == "أوضة تانية": it.update(src="assets/ai/heygen/v10/look10_podcast.mp4", label="ستوديو بودكاست")
# ---------------- note 10: lip sync — real room (new pair) + blue room (still photo -> lip-synced clip), both AFTER on the real voice second ----------------
s = findS("قبل: كليب من صورة واحدة (الأوضة الزرقا)")
t_say = V2T(202.50)   # the S011.7 audio the two lipsyncs were made from starts here
for it in s["items"]:
    lb = str(it.get("label", ""))
    if lb.startswith("قبل: فيديو حقيقي"): it.update(src=A10 + "realroom_before.mp4", loop=True, loopDur=3.7)
    if lb.startswith("بعد: نفس الفيديو"): it.update(src=A10 + "realroom_after.mp4", t=t_say); it.pop("loop", None); it.pop("loopDur", None)
    if lb.startswith("قبل: كليب من صورة"): it.update(src=A10 + "blueroom_photo.jpg", label="قبل: صورة واحدة بس (الأوضة الزرقا)"); it.pop("loop", None)
    if lb.startswith("بعد: نفس الكليب"): it.update(src=A10 + "blueroom_after.mp4", t=t_say, label="بعد: الصورة بتقول الكلام ده"); it.pop("loop", None)

# ---------------- note 11: Gaussian splats — a REAL example (official project video) + the board ends with its sentence ----------------
s = findS("← مشهد 3D تلف فيه")
tgs = next(it["t"] for it in s["items"] if it.get("label") == "← مشهد 3D تلف فيه")
drop_where(s, lambda it: it.get("label") == "← مشهد 3D تلف فيه")
s["items"] += [N(tgs, 560, 470, "صور كتير لمكان حقيقي ← مشهد 3D تلف فيه", src=A10 + "gsplat_garden.mp4", w=520, size=20),
               tag(tgs + 0.4, 560, 690, "المصدر: 3D Gaussian Splatting — Kerbl et al., SIGGRAPH 2023 (Inria)")]
nxt = T10("نعمل", tgs + 1, tgs + 6); s["b"] = min(s["b"], round(nxt - 0.6, 3)) if nxt > tgs + 2 else s["b"]
# ---------------- note 12: the best trick — the REAL prompt + no overlap ----------------
s = findS("2. نديها لـ Higgsfield كريفرنس")
for it in s["items"]:
    if it.get("label") == "2. نديها لـ Higgsfield كريفرنس": it.update(y=330)
    if it.get("k") == "typed" and "كوبري على النيل" in str(it.get("text", "")):
        it.update(y=420, w=520, rtl=False, size=15, head="البرومبت الحقيقي (Higgsfield · Kling video edit)",
                  text="Turn this grey blockout into a photorealistic\nQasr El Nil bridge over the Nile in Cairo at\ngolden hour: stone lion statues, arches above\nthe water, boats and city behind. Keep the exact\ncamera motion, timing and object positions.", dur=40)
# ---------------- note 14: Video Agent — HIS part is seen ----------------
for sp_ in SPECS:
    for it in sp_["items"]:
        if it.get("label") == "Video Agent" and "video_agent_cairo_jet" in str(it.get("src", "")): it.update(w=330, loopDur=6.4, **{"from": 200})

# ---------------- notes 18 / 30: Cowork = the real Cowork (official + Luke Byrne) + his browser that runs by itself (honest label) ----------------
s = findS("2. Cowork / agent: بيشتغل على ملفاتك وبرامجك")
tco = next(it["t"] for it in s["items"] if it.get("label") == "2. Cowork / agent: بيشتغل على ملفاتك وبرامجك")
o_co = next((it.get("out_t") for it in s["items"] if it.get("label") == "2. Cowork / agent: بيشتغل على ملفاتك وبرامجك"), None)
drop_where(s, lambda it: str(it.get("src", "")).endswith("claude_session_2x.mp4") and abs((it.get("t") or 0) - tco) < 1.5)
drop_where(s, lambda it: it.get("t") is not None and tco - 0.2 <= it["t"] < (o_co or 1e9) and it.get("label") != "2. Cowork / agent: بيشتغل على ملفاتك وبرامجك" and it.get("k") != "circle" and it.get("k") == "node" and not it.get("logo"))
s["items"] += outs([N(tco + 0.3, 1380, 520, "Claude Cowork", src=A10 + "cowork_official.mp4", w=380, loop=9.8, size=18, sub="claude.com/product/cowork"),
                    N(tco + 0.9, 900, 520, "Claude بيحرك الماوس", src=A10 + "cowork_luke.mp4", w=150, ar=9 / 16, loop=9.8, size=15, sub="YouTube — AI Luke"),
                    N(tco + 1.6, 560, 520, "متصفح بيشتغل لوحده", src=A10 + "browser_auto_0.mp4", w=150, ar=9 / 16, loop=12, size=15, sub="بسكريبت عمله Claude")], o_co)
# ---------------- note 19: the audiobook hold — the RESULT is heard (sound in make_sfx) + no overlap ----------------
s = findS("مثال: حوّل كتاب لكتاب مسموع بـ Claude Code")
for it in s["items"]:
    lb = str(it.get("label", ""))
    if lb.startswith("2. الكلام"): it.update(y=600, x=700)
    if lb.startswith("3. النتيجة"): it.update(y=760, x=700)
    if lb.startswith("1. OCR"): it.update(y=440, x=700)
    if it.get("k") == "wave": it.update(y=860, x=700, w=420, h=70)
# ---------------- notes 22 / 23: Codex = a normal Desktop app; alternatives = Cursor + Antigravity ----------------
s = findS("Gemini CLI: وقف للأفراد 18 يونيو 2026")
drop_where(s, lambda it: it.get("k") == "typed" and "codex" in str(it.get("text", "")).lower() or str(it.get("label", "")).startswith(("Gemini CLI", "extensions")))
tq = sid_t("S028.2")
s["items"] += [N(tq + 0.2, 1400, 470, "تطبيق Desktop عادي زي Claude", emo="desktop_computer", size=24)]
n23 = PIECE["N23_alt_tools"]; t23 = n23["t"]
spec10(t23 - 0.1, pend(n23) + 1.45, "أدوات زي Claude Code وCodex", t23, [
    N(T10("Claude", t23), 1500, 480, logo=lg("claude.svg"), label="Claude Code", size=22), N(T10("وCodex", t23), 1130, 480, logo=lg("openai-codex.png"), label="Codex", size=22),
    N(T10("Cursor", t23), 760, 480, logo=LG("cursor.png"), label="Cursor", size=22), N(T10("وAntigravity", t23), 400, 480, logo=lg("antigravity.png"), label="Antigravity", size=22)])
# ---------------- note 24: HyperFrames leaves WITH its group ----------------
s = findS("HyperFrames")
grp = [it for it in s["items"] if it.get("label") in ("Remotion", "three.js", "ffmpeg", "Blender", "Whisper (OpenAI)")]
if grp:
    o_ = max((it.get("out_t") or 0) for it in grp) or None
    for it in s["items"]:
        if it.get("label") == "HyperFrames" or str(it.get("label", "")).startswith("وكمان: OpenCV"): it["out_t"] = o_

# ---------------- note 25: Claude Code example — empty folder -> motion on a video, step by step ----------------
ns = [PIECE[k] for k in ("N25a", "N25b", "N25c", "N25d", "N25e", "N25f", "N25g")]
a25, b25 = ns[0]["t"], pend(ns[-1]) + 1.1
spec10(a25 - 0.1, b25, "مثال: Claude Code من فولدر فاضي", a25, [
    N(ns[0]["t"] + 0.3, 1480, 330, "1. فولدر فاضي + فيديو بيشرح", emo="file_folder", size=20),
    N(T10("فيديو", ns[0]["t"] + 1), 1480, 470, src=CL + "clip_026_C02b.mp4", w=260, loop=5),
    TY(ns[1]["t"], 960, 330, "«حط موشن على الفيديو ده»", w=360, rtl=True, head="2. بتكتب لـ Claude Code:", size=20, dur=14),
    N(T10("Whisper", ns[2]["t"]), 480, 330, "3. بيفهم الفيديو", src=A10 + "web/faster_whisper_card.png", w=260, ar=2.0, size=18, sub="الكلام + توقيت كل كلمة"),
    E(ns[2]["t"] + 0.3, 760, 330, 640, 330),
    TY(ns[3]["t"], 1480, 640, "جملة 1 ← كلمة على الشاشة\nجملة 2 ← صورة حقيقية\nجملة 3 ← رسمة بتشرح", w=360, rtl=True, head="4. خطة الموشن", size=17, dur=14),
    TY(T10("فولدرات", ns[4]["t"]), 960, 600, "src/\n  Video.tsx   ← الكود\npublic/\n  video.mp4\nimport {Composition} from 'remotion'", w=380, head="5. فولدرات + كود", size=16, dur=20),
    N(T10("Remotion", ns[4]["t"]), 960, 830, logo=lg("remotion.png"), label="library: Remotion", size=18),
    N(T10("ffmpeg", ns[5]["t"]), 480, 640, logo=lg("ffmpeg.ico"), label="6–7. رندر + تركيب بـ ffmpeg", size=18),
    N(ns[6]["t"], 480, 830, "8. الفيديو بالموشن ✓", src=CL + "clip_028_C02b.mp4", w=260, loop=5, good=True, size=18)])

# ---------------- note 26: every logo on ITS word (general) ----------------
NAMES_ = {"Photoshop": "وPhotoshop", "Premiere": "وPremiere", "After Effects": "After", "Blender": "وBlender", "DaVinci": "وDaVinci"}
s = findS("سكريبتات جوه برامجك")
for it in s["items"]:
    nm = it.get("label")
    if nm in NAMES_ and it.get("t") is not None:
        it["t"] = T10(NAMES_[nm], it["t"] - 4, it["t"], win=8)
# ---------------- note 27 / 28 / 29 / 31: MCP ----------------
for sp_ in SPECS:
    for it in sp_["items"]:
        if it.get("label") == "أي برنامج": it["label"] = "أي برنامج أو موقع"
s = findS("الـ MCP بيشتغل إزاي؟")
th = next(it["t"] for it in s["items"] if str(it.get("label", "")).startswith("1. HeyGen"))
o28 = s["b"]
s["items"] = [it for it in s["items"] if it.get("k") in ("circle",)]
step = max(1.6, (o28 - th - 1.0) / 5)
s["items"] += [N(th - 0.3, 1520, 330, "Claude", logo=lg("claude.svg"), size=22), N(th - 0.2, 400, 330, "HeyGen (موقع)", logo=lg("heygen.ico"), size=22),
               E(th, 1360, 300, 560, 300, color="mustard"), N(th + 0.1, 960, 250, "1. Claude بيكلّم الموقع", size=20),
               E(th + step, 560, 470, 1360, 470, color="olive"), TY(th + step, 960, 560, "• اعمل فيديو أفاتار\n• ولّد صوت\n• هات الأصوات", w=330, rtl=True, head="2. الموقع بيرجّعله المنيو", size=18, dur=14),
               N(th + 2 * step, 1520, 600, "3. Claude بيقرر: «اعمل فيديو أفاتار»", emo="thought_balloon", size=18),
               E(th + 3 * step, 1360, 760, 560, 760, color="mustard"), N(th + 3 * step, 960, 720, "4. بيقول للموقع يعمل كده", size=18),
               E(th + 4 * step, 560, 860, 1360, 860, color="olive"), N(th + 4 * step, 960, 820, "5. الموقع بيرجّعله النتيجة", size=18),
               N(th + 4 * step + 0.3, 400, 620, "الفيديو", src="assets/ai/heygen/v9/look9_studio.mp4", w=260, good=True, size=18)]
s = findS("DaVinci Resolve MCP: يقص ويرتب")
for it in s["items"]:
    if it.get("label") == "DaVinci Resolve MCP: يقص ويرتب":
        it.update(src=A10 + "davinci_mcp.mp4", w=440, loop=11.8, sub="المصدر: YouTube — Creator Magic «I Let GPT-6 Astra Edit In DaVinci Resolve MCP»")
tbm = T10("Blender", s["a"]) if s else None
s["items"] += [N(s["a"] + 1.2, 1400, 760, "Claude + Blender MCP: بيبني مودل من برومبت", src=A10 + "blender_mcp_build.mp4", w=380, loop=14.8, size=17,
                 sub="المصدر: YouTube — GaminGuruz")]
s = findS("Blender بالكود (بالـ MCP)")
tbc = next(it["t"] for it in s["items"] if it.get("label") == "Blender بالكود (بالـ MCP)")
s["items"] += [{"k": "puppet", "t": tbc + 0.2, "x": 960, "y": 520, "size": 1.0, "claude": lg("claude.svg"), "logo": lg("blender.svg")}]
for it in s["items"]:
    if it.get("label") == "Blender بالكود (بالـ MCP)": it.update(y=660); it.pop("logo", None)   # the Blender logo lives in the puppet's strings only
    if it.get("label") == "الشمس بتغرب": it.update(y=600, x=560)
    if it.get("label") == "القطع بتتركب": it.update(y=600, x=1360)
s["items"] += [N(tbc + 1.0, 1500, 820, "Blender MCP: مشهد كامل بيتبني", src=A10 + "blender_mcp_timelapse.mp4", w=300, loop=11.8, size=16, sub="المصدر: YouTube — Muska")]
o_bc = next((it.get("out_t") for it in s["items"] if it.get("label") == "Blender بالكود (بالـ MCP)"), None)
if o_bc:   # puppet + timelapse leave with their group (not 8 s later)
    for it in s["items"]:
        if it.get("k") == "puppet" or it.get("label") == "Blender MCP: مشهد كامل بيتبني": it["out_t"] = o_bc

# ---------------- note 33 / 35 / 37: skills — real skill folder + richer SKILL.md + rules + screenshots + the content skill ----------------
s = findS("الـ skill = كراسة خبرة")
for it in s["items"]:
    if it.get("k") == "typed" and "aly-video-motion" in str(it.get("text", "")):
        it.update(w=520, size=14, text="---\nname: aly-video-motion\ndescription: الموشن بأسلوب علي — اقراها في أي شغل\n  فيديو (ستايل، زوم، لوجوهات، موشن)\n---\n## 0. رقم الستايل الأول\n## اللي عجب علي (كرّره)\n- صورة حقيقية على كل كلمة\n## غلطات المراجعة (متكررهاش)\n- ممنوع overlap\n- كل ملاحظة تتنفذ قبل نسخة جديدة", dur=40)
s["items"] += [TY(s["a"] + 1.5, 560, 400, "aly-video-motion/\n  SKILL.md\n  references/\n  scripts/", w=300, head="فولدر الـ skill", size=16, dur=15)]
s = findS("الـ video maker بتاعنا")
tvm = next(it["t"] for it in s["items"] if it.get("label") == "الـ video maker بتاعنا")
o_vm = next((it.get("out_t") for it in s["items"] if it.get("label") == "الـ video maker بتاعنا"), None)
drop_where(s, lambda it: it.get("label") in ("20 ستايل برقم", "كل غلطة اتسجلت.. متتكررش"))
RULES = ["ممنوع overlap", "كل ملاحظة تتنفذ قبل نسخة جديدة", "لوجو حقيقي لكل أداة", "الوش في دايرة فوق اللوحة", "QR جنب الثمبنيل دايماً", "مزيكا هادية بس",
         "صوت علي مايتنضفش إلا لو طلب", "متقصش كلمة في النص"]
s["items"] += outs([N(tvm + 0.6 + 0.45 * i, 640, 300 + 70 * i, r_, emo="check_mark_button", size=17) for i, r_ in enumerate(RULES)] +
                   [N(tvm + 4.5, 1300, 760, "20 ستايل برقم", src="../../styles/styles_strip_v10.jpg", w=520, ar=4.0, size=18)], o_vm)
# the content-creation skill: his skill working -> the Playmobil short + its numbers (PDF p.10 / p.22)
t_sk = sid_t("S038.3")
spec10(t_sk - 0.1, max(t_sk + 3.5, sid_end("S038.3")), "skill بتكتب السكريبت بنفس الأسلوب", t_sk, [
    N(t_sk + 0.2, 1350, 470, "الـ skill شغالة: سكريبت الريل", src=A10 + "skill_content.mp4", w=520, size=18),
    N(t_sk + 1.2, 560, 430, "النتيجة: ريل Playmobil", src=A10 + "playmobil_short.mp4", w=200, ar=9 / 16, size=18),
    N(t_sk + 1.8, 560, 780, "~31K مشاهدة على 4 منصات", src=P13 + "page22.png", w=300, ar=1.0, size=16, sub="من الـ PDF صفحة 22")])

# ---------------- note 36: his script recordings (scripts section + the human part) ----------------
s = findS("سكريبتات جوه برامجك")
n38 = PIECE["N38"]
s["items"] += [N(n38["t"] + 0.2, 330, 760, "نشر الريلز", src=A10 + "script_rec_1.mp4", w=120, ar=9 / 16, size=14),
               N(n38["t"] + 0.8, 545, 760, "الرد على الكومنتات", src=A10 + "script_rec_0.mp4", w=120, ar=9 / 16, size=14)]

# ---------------- notes 40 / 43: the real experience — ALL the PDF pictures, his old photos, the hand work ----------------
PDF = json.load(open("work/pdf13/index.json"))
pics = lambda pg: [o["f"] for o in PDF if o["page"] == pg and not (o["w"] == 240 and o["h"] == 240)]
SLOTS = [(1440, 330), (960, 330), (1440, 640), (960, 640), (480, 640), (1440, 860)]
def wall(t0, t1, files, title=None):
    files = [f for f in files][:max(1, int((t1 - t0) / 0.7))]
    if not files: return
    dt = max(0.55, (t1 - t0 - 0.6) / len(files)); its = []
    for i, f in enumerate(files):
        x, y = SLOTS[i % len(SLOTS)]; ti = t0 + i * dt
        its.append(dict(N(ti, x, y, None, src=f, w=400, ar=16 / 9, fit="contain", out=round(min(t1 - 0.1, ti + dt * len(SLOTS) - 0.1), 3)), filler=True))   # filler: makes room for real cards
    spec10(t0 - 0.05, t1, title, t0 if title else None, its)
tS37 = sid_t("S037.1")
wall(tS37, sid_t("S037.3"), pics(3)[:5] + pics(1), "تجربة حقيقية بالأرقام")
wall(sid_t("S037.3"), PIECE["N43b_reason"]["t"], [P13 + "p03_5.png", P13 + "p03_7.png", P13 + "p03_8.png", P13 + "p03_9.png"] + pics(26) + pics(27)[:2])
n43b = PIECE["N43b_reason"]
wall(n43b["t"], pend(n43b) + 0.4, pics(2)[:1] + [P13 + "p02_1.png", P13 + "p02_2.png", P13 + "p02_4.png", P13 + "p02_5.png"] + pics(4))
wall(sid_t("S038.1"), sid_t("S038.3"), pics(6) + pics(7) + pics(9)[:6])
wall(sid_t("S038.4"), sid_t("S039.1"), pics(12) + pics(13) + pics(15) + pics(17) + pics(18))
wall(sid_t("S039.1"), sid_t("S039.3"), pics(7)[1:] + pics(8)[:6])
wall(sid_t("S039.3"), sid_t("S040.1"), pics(21) + pics(23) + pics(24) + pics(25) + pics(5)[:4] + pics(22))
wall(sid_t("S040.1"), sid_t("S040.6") + 1.2, pics(32) + pics(33) + pics(30) + pics(31) + pics(29))

# v10 still check: the older «video maker / publisher / numbers» board (range broken since v8: its cards run to ~948 s) overlapped the walls and
# both were lost -> ONE board per stretch: its explanation cards on their words + the PDF pictures as a wall around them
_old = next((sp_ for sp_ in SPECS if not sp_.get("v10") and any(str(it.get("label", "")).startswith("1. video maker") for it in sp_["items"])), None)
if _old:
    _walls = [sp_ for sp_ in SPECS if sp_.get("v10") and sp_["a"] >= sid_t("S038.1") - 0.2 and sp_["b"] <= sid_t("S040.6") + 1.5 and not sp_.get("title")]
    _pre = next(sp_ for sp_ in SPECS if sp_.get("v10") and abs(sp_["b"] - n43b["t"]) < 0.2)   # wall before the reason
    for it in list(_old["items"]):
        if (it.get("t") or 0) < n43b["t"]: _pre["items"].append(it); _old["items"].remove(it)   # «اللي اتبنى بـ Claude Code» stays on its word
    for it in _pre["items"]:
        if it.get("src") and "pdf13" in str(it.get("src")): it.update(w=280, out=round(min(it.get("out") or 9e9, it["t"] + 2.6), 3))
    for w_ in _walls:
        for it in w_["items"]: it.update(w=260, out=round(min(it.get("out") or 9e9, it["t"] + 2.6), 3))
        _old["items"] += w_["items"]; SPECS.remove(w_)
    ts_ = [it["t"] for it in _old["items"] if it.get("t") is not None]
    _old["a"] = round(min(w_["a"] for w_ in _walls), 3) if _walls else round(min(ts_) - 0.15, 3)
    _old["b"] = round(max([w_["b"] for w_ in _walls] + [max(ts_) + 3.0]), 3)
for it in (_old["items"] if _old else []):
    if str(it.get("label", "")).startswith("شورت كل يوم"): it.update(x=700, y=860)   # the stats column on the right is full at that moment
# note 43: the reason on its words (his old photos / hand work = the wall pictures of this stretch)
_r = next(sp_ for sp_ in SPECS if sp_.get("v10") and abs(sp_["a"] - (n43b["t"] - 0.05)) < 0.1)
for it in _r["items"]: it.update(w=320)
_r["items"] += [N(n43b["t"] + 0.2, 960, 200, "3 سنين من غير فيديوهات.. ليه؟", emo="hourglass_not_done", size=24, bg="mustard"),
                N(T10("المونتاج", n43b["t"]), 1500, 520, "مونتاج بإيدي", emo="scissors", size=19),
                N(T10("والكروما", n43b["t"]), 1500, 640, "كروما بإيدي", emo="green_square", size=19),
                N(T10("VFX", n43b["t"]), 1500, 760, "VFX بإيدي", emo="sparkles", size=19),
                N(T10("فريم", n43b["t"]), 1500, 880, "موشن.. فريم فريم", emo="film_frames", size=19),
                N(T10("full-time", n43b["t"]), 960, 880, "+ شغل full-time", emo="briefcase", size=19, good=True)]

# ---------------- notes 44 / 45: step 6 = a prompt to Claude through the MCP; step 11 = the reel itself (no price) ----------------
s = findS("خطوة بخطوة: ريل 30 ثانية")
for it in s["items"]:
    if it.get("label") == "look جوه الستوديو نفسه ✓":
        t6 = it["t"]
    if it.get("label") == "export.. وتكلفة الريل على الشاشة":
        it.update(label="export: الريل النهائي", src="assets/ai/heygen/avatar_clips_v1/avatar_001_C00.mp4", w=560, emo=None, size=22)
s["items"] += [TY(t6 + 0.8, 1500, 760, "«اعمل look ليّ جوه الستوديو ده»", w=380, rtl=True, head="برومبت لـ Claude:", size=17, dur=14),
               N(t6 + 1.6, 1500, 880, "Claude ← MCP ← HeyGen ← الـ look", size=16, bg="mustard")]
# ---------------- notes 46 / 47 / 48: tricks ----------------
s = findS("موشن بخلفية شفافة")
tl_ = next(it["t"] for it in s["items"] if it.get("label") == "موشن بخلفية شفافة" or "ProRes 4444" in str(it.get("text", "")))
drop_where(s, lambda it: "ProRes 4444" in str(it.get("text", "")))
s["items"] += [N(tl_ + 0.6, 1380, 470, "الموشن لوحده.. خلفيته شفافة", src="assets/v10/checker_motion.mp4", w=440, size=18),
               TY(tl_ + 2.0, 700, 430, "V2  موشن.webm  (شفاف)\nV1  الفيديو.mp4", w=420, head="التايملاين في البرنامج", size=18, dur=14),
               N(tl_ + 3.2, 700, 650, "النتيجة: الموشن فوق الفيديو", src=CL + "clip_026_C02b.mp4", w=360, loop=5, good=True, size=18),
               N(tl_ + 3.6, 1380, 760, "ProRes 4444 / WebM = بيحافظوا على الشفافية", size=16)]
n48 = PIECE["N48_davinci"]
findS("موشن بخلفية شفافة")["items"] += outs([
    N(T10("DaVinci", n48["t"]), 1350, 470, logo=LG("davinci-resolve.png"), label="DaVinci Resolve", size=24),
    N(T10("فيديو", n48["t"] + 1), 600, 430, "فيديو: شيل الصمت بضغطة في DaVinci", src=CH + "thumb_ZXQLSxYmLsw.jpg", w=380),
    N(T10("فيديو", n48["t"] + 1) + 0.25, 600, 680, src=CH + "qr_ZXQLSxYmLsw.png", w=110, ar=1)], pend(n48) + 0.5)
for it in findS("موشن بخلفية شفافة")["items"]:   # the layer-trick group leaves before the DaVinci tip
    if it.get("t") is not None and tl_ - 0.5 <= it["t"] < n48["t"] and (it.get("out_t") is None or it["out_t"] > n48["t"]): it["out_t"] = round(n48["t"] - 0.15, 3)
for sp_ in SPECS:
    for it in sp_["items"]:
        if "refs_plus_sheet" in str(it.get("src", "")) and (it.get("t") or 0) > 900: it.update(src="assets/v6/character_sheet_s.jpg", label="character sheet = نفس الشخصية من كل الزوايا", w=600, ar=2.0)

# ---------------- note 49: the bill — verified numbers, one total, aligned (built in make_bill_v10.py -> work/bill_v10.json) ----------------
BILL = json.load(open("work/bill_v10.json", encoding="utf-8"))
s = findS("فاتورة الفيديو ده (لحد 22 نوفمبر 2026)")
s["title"] = BILL["title"]
s["items"] = [it for it in s["items"] if it.get("k") == "circle"]
y0, dy = 275, 120   # rows far enough apart that each logo sits beside ITS line (v10 still: 105 pushed the logos down)
for i, (logo, text) in enumerate(BILL["rows"]):
    t_ = s["a"] + 0.6 + 0.55 * i
    s["items"] += [N(t_, 1560, y0 + dy * i, logo=LG(logo), size=16), N(t_ + 0.1, 960, y0 + dy * i, text, size=21)]
s["items"] += [N(s["a"] + 0.6 + 0.55 * len(BILL["rows"]) + 0.4, 960, y0 + dy * len(BILL["rows"]) + 10, BILL["total"], size=28, bg="mustard", good=True)]

# ---------------- note 53: the song's versions ----------------
n53 = PIECE["N53_song_versions"]
VERS = json.load(open("work/song_versions_v10.json", encoding="utf-8"))
its = [N(n53["t"] + 0.3, 960, 240, "نسخ الأغنية", logo=lg("suno.png"), size=22)]
for i, v in enumerate(VERS):
    x, y = 1500 - (i % 4) * 340, 470 + (i // 4) * 230
    its += [N(n53["t"] + 0.6 + 0.45 * i, x, y, v["label"], emo=("check_mark_button" if v.get("final") else "musical_note"), size=17, good=bool(v.get("final")))]
spec10(n53["t"] - 0.1, pend(n53) + 0.4, None, None, its)
# ---------------- notes 39 / 56: the ending part + the CTA ----------------
n39 = [PIECE[k] for k in ("N39a", "N39b", "N39c", "N39d", "N39e", "N39f")]
spec10(n39[0]["t"] - 0.1, pend(n39[-1]) + 0.9, "الـ AI مش ساحر", n39[0]["t"], [
    N(n39[1]["t"] + 0.5, 1450, 380, "5 أيام شغل مع الـ AI", emo="calendar", size=22),
    N(n39[2]["t"] + 0.3, 1450, 560, "skills متمرّنة في فيديوهات قبل كده", src="../../styles/styles_strip_v10.jpg", w=420, ar=4.0, size=18),
    N(n39[3]["t"] + 0.3, 1450, 760, "معرفة علي: بناء الحلقة + السكريبت", emo="light_bulb", size=20),
    N(n39[4]["t"] + 0.2, 560, 470, "أكتر من 10 نسخ", src="assets/v10/versions_strip.jpg", w=520, ar=2.2, size=20),
    N(n39[5]["t"] + 0.2, 560, 760, "مثابرة.. بس أسهل بكتير من الشغل اليدوي", emo="flexed_biceps", size=20, good=True)])
n56 = PIECE["N56_cta"]
spec10(n56["t"] - 0.1, pend(n56) + 0.3, None, None, [
    N(n56["t"] + 0.2, 560, 470, "ده أنا", src="assets/v6/face_gen.jpg", w=300, ar=1.0, size=22),
    N(T10("إنسان", n56["t"]), 1380, 470, "اللي ورا الفيديو ده إنسان", emo="red_heart", size=24),
    N(T10("بدعمكم", n56["t"]), 1380, 640, "لايك · اشتراك · كومنت", emo="thumbs_up", size=22, bg="mustard")])
for sp_ in SPECS:   # note 50: the Meta logo beside the TikTok page, never on it
    if any(it.get("k") == "page" for it in sp_["items"]):
        for it in sp_["items"]:
            if str(it.get("logo", "")).endswith("meta.png") or it.get("label") == "Meta": it.update(x=1730, y=640)
for sp_ in SPECS:
    for it in sp_["items"]:
        if str(it.get("label", "")).startswith("صور مرجع + الـ") and (it.get("t") or 0) < 900: it.update(w=360, x=960, label="صور مرجع + character sheet")
        if it.get("label") == "Soul ID في Higgsfield" and (it.get("t") or 0) < 900: it.update(x=1450, w=320)
        if it.get("label") == "تدريب LoRA على وشك" and (it.get("t") or 0) < 900: it.update(x=470, w=260)
for nw in [x for x in SPECS if x.get("v10")]:
    for old in [x for x in SPECS if not x.get("v10")]:
        if old["a"] < nw["a"] - 0.3 and old["b"] > nw["b"] + 0.8:
            tail = dict(old, a=round(nw["b"] + 0.02, 3), title=None, title_t=None, sfx=[],
                        items=[it for it in old["items"] if (it.get("t") or 0) >= nw["b"] - 0.3 or (it.get("out_t") or 1e9) > nw["b"] + 0.5 or it.get("k") == "circle"])
            old["b"] = round(nw["a"] - 0.02, 3); SPECS.append(tail)
for sp_ in SPECS:
    for it in sp_["items"]:
        if it.get("k") == "bar" and it.get("label") == "4K في الآخر": it["h"] = 280   # its top cleared the trick title (note 50 check)
unclip_gaps()

# face windows for the long talking circles (notes 34 / 41 / 48 / 55) — v10 time ranges (make_props_v10 fills them from the v10 avatar batch)
g = {q["sep"][1]: q for q in T10P if q["kind"] == "gap"}
FACE_WINDOWS = [(g["الـ skills"]["t"] + g["الـ skills"]["dur"], g["تجربة حقيقية"]["t"]), (g["تجربة حقيقية"]["t"] + g["تجربة حقيقية"]["dur"], g["الأغنية"]["t"]),
                (sid_t("S057.1"), json.load(open(TL, encoding="utf-8"))["total"])]
print("v10 specs:", len(SPECS), "| words not found:", [m for m in MISS6 if str(m[0]).startswith("v10:")])

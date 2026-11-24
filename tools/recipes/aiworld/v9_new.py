"""v9 scenes = all v8 SPECS (v8_new, written in v8 time) moved to v9 time through the SOURCE (M89), + Aly's v8 notes and the
open v7 items (review_rough_v8_notes.md): 6 lip-synced looks, blue-room lip sync, the real tests, the real Video Agent video,
video-to-video character / place, Higgsfield first/last frame page, boards over the new lines N25 / N38 / N43, the closing lines N55.
make_props_v9 imports SPECS from here."""
import json
import v8_new as base
from v7_specs import N, E, TY, SC, CL

SPECS = base.SPECS; MISS6 = base.MISS6
T8P = json.load(open("work/timeline_v8.json", encoding="utf-8"))["pieces"]
T9P = json.load(open("work/timeline_v9.json", encoding="utf-8"))["pieces"]
_L = lambda p: p["dur"] if p["kind"] in ("gap", "hold") else p["b"] - p["a"]
_G8 = [p for p in T8P if p["kind"] == "gap"]; _G9 = [p for p in T9P if p["kind"] == "gap" and p["sep"][1] != "OPEN"]
assert len(_G8) == len(_G9)

def _hold9(p8):
    i = T8P.index(p8); prev = T8P[i - 1]; last = prev["sids"][-1]
    j = next(k for k, q in enumerate(T9P) if q.get("sids") and last in q["sids"])
    return next(q for q in T9P[j:] if q["kind"] == "hold")

def M89(t8):
    """v8 time -> v9 time, through the same piece (gap by order, file by sentence id, hold after the same sentence, v2 by source second)"""
    if t8 is None: return None
    best = next((p for p in T8P if p["t"] - 1e-6 <= t8 <= p["t"] + _L(p) + 1e-6), None)
    if best is None:
        prev = max((p for p in T8P if p["t"] <= t8), key=lambda p: p["t"])
        return round(M89(prev["t"] + _L(prev)) + (t8 - prev["t"] - _L(prev)), 3)
    p, off = best, t8 - best["t"]
    if p["kind"] == "gap":
        q = _G9[_G8.index(p)]; return round(q["t"] + off * q["dur"] / p["dur"], 3)
    if p["kind"] == "hold":
        q = _hold9(p); return round(q["t"] + min(off, q["dur"]), 3)
    if p["kind"] == "file":
        q = next(q for q in T9P if q["kind"] == "file" and q["sids"] == p["sids"]); return round(q["t"] + off * _L(q) / max(0.01, _L(p)), 3)
    t2 = p["a"] + off
    for q in T9P:
        if q["kind"] == "v2" and q["a"] - 1e-3 <= t2 <= q["b"] + 1e-3: return round(q["t"] + t2 - q["a"], 3)
    q = min((q for q in T9P if q["kind"] == "v2"), key=lambda q: min(abs(t2 - q["a"]), abs(t2 - q["b"])))
    return round(q["t"] + min(max(t2, q["a"]), q["b"]) - q["a"], 3)

for sp_ in SPECS:
    sp_["a"], sp_["b"] = M89(sp_["a"]), M89(sp_["b"])
    if sp_["title_t"] is not None: sp_["title_t"] = M89(sp_["title_t"])
    for it in sp_["items"]:
        for k_ in ("t", "out_t", "clean_t", "dim_t", "grow_t"):
            if it.get(k_) is not None: it[k_] = M89(it[k_])
        if it.get("act_t"): it["act_t"] = [M89(it["act_t"][0]), M89(it["act_t"][1])]
        if it.get("hide"): it["hide"] = [[M89(a_), M89(b_)] for a_, b_ in it["hide"]]
    sp_["sfx"] = [(n, M89(t)) for n, t in sp_["sfx"]]

# ---------- helpers in v9 time ----------
W9 = json.load(open("work/words_v9.json", encoding="utf-8"))
def T9(word, after, default=None, win=12):
    key = word.split()[0].lower()
    for w in W9:
        if w["a"] >= after - 0.4 and key in w["w"].lower():
            if w["a"] - after > win: break
            return round(w["a"], 3)
    MISS6.append(("v9:" + word, after)); return round(default if default is not None else after, 3)
def V2T(t2):   # source (v2) second -> v9 time
    for q in T9P:
        if q["kind"] == "v2" and q["a"] - 1e-3 <= t2 <= q["b"] + 1e-3: return round(q["t"] + t2 - q["a"], 3)
    raise KeyError(t2)
PIECE = {q["sids"][0]: q for q in T9P if q.get("sids")}
pend = lambda q: q["t"] + _L(q)
def spec9(a, b, title=None, title_t=None, items=(), sfx=()):
    SPECS.append(dict(a=round(a, 3), b=round(b, 3), title=title, title_t=title_t, items=list(items), circle=False, sfx=list(sfx)))
def findS(sub):
    for s in SPECS:
        if sub == s.get("title"): return s
        for it in s["items"]:
            if sub in str(it.get("label", "")) or sub in str(it.get("src", "")) or sub in str(it.get("text", "")): return s
    raise KeyError(sub)
def outs(items, t):
    for it in items: it["out_t"] = round(t, 3)
    return items
V9 = "assets/ai/heygen/v9/"; HF9 = "assets/ai/higgsfield/v9/"

# boards that ended where a NEW line now follows (N25 / N38 / N43) stay through that line and its hold
for nid in ("N25", "N38", "N43"):
    q = PIECE[nid]; i = T9P.index(q); end = pend(q) + (T9P[i + 1]["dur"] if T9P[i + 1]["kind"] == "hold" else 0)
    for sp_ in SPECS:
        if abs(sp_["b"] - q["t"]) < 1.2 or (sp_["a"] < q["t"] < sp_["b"] and sp_["b"] < end):
            old = sp_["b"]; sp_["b"] = round(end - 0.05, 3)
            for it in sp_["items"]:
                if it.get("out_t") is not None and it["out_t"] >= old - 0.6: it["out_t"] = round(end - 0.1, 3)

# ---------- v8 note 5 (= v7 13a/b): SIX looks, all saying THIS sentence, lip-synced like clones; Burj = camera pulling back ----------
s = findS("مقدم واقف")
olds = [it for it in s["items"] if it.get("label") in ("الستوديو", "البحر", "أوضة تانية", "مقدم واقف")]
o_ = olds[0].get("out_t"); s["items"] = [it for it in s["items"] if it not in olds]
t0 = V2T(196.66)   # the looks clips were made from the voice from 196.66 (v2) -> they start on that exact second
L6 = [("الستوديو", "look9_studio.mp4"), ("البحر", "look9_beach.mp4"), ("أوضة تانية", "look9_room.mp4"),
      ("مقدم واقف", "look9_presenter_16x9.mp4"), ("في الغابة", "look9_jungle.mp4"), ("جلابية فوق برج خليفة", "look9_burj_pullback.mp4")]
s["items"] += outs([N(t0, [1420, 960, 500][i % 3], [370, 680][i // 3], nm, src=V9 + f, w=420, size=20) for i, (nm, f) in enumerate(L6)], o_)
for it in s["items"]:   # the group before the looks leaves BEFORE the clones start (no overlap)
    if it.get("t") is not None and it["t"] < t0 - 0.2 and it.get("out_t") is not None and t0 - 0.2 < it["out_t"] < t0 + 3: it["out_t"] = round(t0 - 0.15, 3)
for it in s["items"]:   # the board title above the grid
    if str(it.get("label", "")).startswith("Looks"): it.update(y=175, t=min(it["t"], t0))

# ---------- v7 14: lip sync = BEFORE -> AFTER twice: the real room + the blue room (made from one photo, Aly v8) ----------
tsay = T9("تاخد", t0 + 4)
for it in s["items"]:
    lb = str(it.get("label", ""))
    if lb.startswith("lip sync: نفس"): it.update(y=190)
    elif lb.startswith("قبل: فيديو حقيقي"): it.update(x=1340, y=400, w=400)
    elif lb.startswith("بعد: نفس الفيديو"): it.update(x=580, y=400, w=400)
    elif it.get("k") == "edge" and it.get("pts") == [1040, 560, 880, 560]: it["pts"] = [1110, 400, 810, 400]
lp = next(it for it in s["items"] if str(it.get("label", "")).startswith("قبل: فيديو حقيقي"))
s["items"] += outs([N(lp["t"] + 0.3, 1340, 710, "قبل: كليب من صورة واحدة (الأوضة الزرقا)", src=V9 + "blueroom_before.mp4", w=400, size=20),
                    E(lp["t"] + 0.7, 1110, 710, 810, 710),
                    N(tsay, 580, 710, "بعد: نفس الكليب بيقول الكلام ده", src=V9 + "blueroom_after.mp4", w=400, size=20, good=True)], lp.get("out_t"))

# ---------- v7 15: «جربنا التلاتة» = the REAL tests ----------
for sp_ in SPECS:
    for it in sp_["items"]:
        lb = str(it.get("label", ""))
        if lb.startswith("صورة واحدة: الحركة زيادة"): it.update(src=V9 + "blueroom_before.mp4", sub="تجربة 1: صورة الأوضة الزرقا"); it.pop("loop", None); it.pop("loopDur", None)
        if lb.startswith("lip sync: البق ظبط"): it.update(src=V9 + "test03_lipsync_16x9.mp4", sub="تجربة 3: فيديو حقيقي + بق جديد"); it.pop("loop", None); it.pop("loopDur", None)

# ---------- v7 24: a video REALLY made with HeyGen Video Agent (prompt «طيارة فوق القاهرة» + his look) ----------
for sp_ in SPECS:
    for it in sp_["items"]:
        if it.get("label") == "Video Agent" and it.get("src"):
            it.update(src=V9 + "video_agent_cairo_jet.mp4", sub="اتعمل فعلاً بـ HeyGen Video Agent: «طيارة فوق القاهرة»", loop=True, loopDur=9, **{"from": 50})

# ---------- v7 10: video to video = the original + style / character / place, each on its word ----------
tv = T9("video", 178.5); ts_ = T9("الستايل،", tv); tch = T9("شخصية،", ts_); tpl = T9("المكان،", tch); tend = T9("هي.", tpl, tpl + 2.2)
spec9(tv - 0.25, tend + 0.9, "video to video: نفس الحركة.. حاجة واحدة بتتغير", tv, [
    N(tv + 0.1, 960, 330, "الفيديو الأصلي", src=CL + "clip_026_C02b.mp4", w=400, loop=5, size=22),
    E(ts_, 860, 450, 520, 560), N(ts_, 500, 700, "غيّر الستايل", src=CL + "clip_028_C02b.mp4", w=380, loop=5, size=22),
    E(tch, 960, 470, 960, 560), N(tch, 960, 700, "غيّر الشخصية: فرعون", src=HF9 + "v2v_character.mp4", w=380, loop=5, size=22),
    E(tpl, 1060, 450, 1400, 560), N(tpl, 1420, 700, "غيّر المكان: شارع نيون", src=HF9 + "v2v_place.mp4", w=380, loop=5, size=22),
    N(tend, 960, 880, "والحركة زي ما هي", emo="check_mark_button", size=22, good=True)])

# ---------- v7 8c: the real Higgsfield page: first frame -> last frame (gold boxes on the two pictures) ----------
s = findS("أول صورة وآخر صورة")
s["items"] = [it for it in s["items"] if "hf_frames_slot" not in str(it.get("src", "")) and not str(it.get("label", "")).startswith("في Higgsfield: الصورة الأولى")]
tfa = min(it["t"] for it in s["items"] if it.get("t") is not None)
s["items"] += [SC(tfa + 1.0, 960, 735, "assets/v9/higgsfield_first_last_frame.png", w=600, ar=1600 / 620,
                  boxes=[dict(x=33, y=2, w=21, h=67, label="أول صورة"), dict(x=64, y=2, w=27, h=78, label="آخر صورة")]),
               N(tfa + 1.3, 960, 895, "من صفحة Higgsfield الرسمية: Start frame ← End frame", size=18)]

# ---------- v7 38 (N38): scripts we made -> «in the Human part», said now ----------
q = PIECE["N38"]; tn = q["t"]
s = findS("سكريبتات تانية عملناها")
for it in s["items"]:
    if str(it.get("label", "")).startswith("سكريبتات تانية عملناها"): it.update(t=tn + 0.1, label="سكريبتات تانية عملناها: نشر الريلز والرد على الكومنتات", sub="هنشوفها في: 6. الإنسان › تجربة حقيقية", size=18)


# ---------- v7 43 (N43): you don't write the skill yourself — step by step on his words ----------
q = PIECE["N43"]; tn = q["t"]; te = pend(q)
tq_ = T9("قول", tn + 3); tw_ = T9("يكتبها،", tq_); tnx = T9("والمرة", tw_)
spec9(tn - 0.1, te + 1.45, None, None, [N(tn + 0.05, 960, 230, "مش لازم تكتب الـ skill بنفسك", emo="sparkles", size=28, bg="mustard"),
                    N(T9("تخلّص", tn + 1), 1500, 470, "1. خلّصت شات أو فيديو", emo="speech_balloon", size=20),
                    E(tq_ - 0.1, 1330, 470, 1200, 470),
                    TY(tq_, 960, 470, "«حوّل ده لـ skill واحفظ المعرفة»", w=420, rtl=True, head="2. قول لـ Claude:", size=19, dur=12),
                    E(tw_ - 0.1, 720, 470, 600, 470),
                    N(tw_, 420, 470, "3. SKILL.md اتكتب واتحفظ ✓", emo="check_mark_button", size=20, good=True),
                    N(tnx, 960, 720, "4. المرة الجاية بيبدأ من هنا", emo="repeat_button", size=24)])

# ---------- v7 55 (N55a / N55b): the two closing lines, HIM saying them (lip-synced), + comment and poll chips ----------
qa, qb = PIECE["N55a"], PIECE["N55b"]
import subprocess
dur_a = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", V9 + "N55a_comment.wav"], capture_output=True, text=True).stdout)
sk_a, sk_b = qa["a"], dur_a + 0.4 + qb["a"]   # the avatar video = N55a wav + 0.4 s + N55b wav
FROM = lambda s_: int(round(s_ * 25))
tpb = T9("بتحبوا", qb["t"]); tor = T9("ولا", tpb)
spec9(qa["t"] - 0.1, pend(qb) + 0.5, "قولولي", qa["t"], [
    {**N(qa["t"] - 0.05, 640, 500, None, src=V9 + "closing9_N55.mp4", w=760), "from": FROM(sk_a - 0.05), "out_t": round(qb["t"] - 0.05, 3)},
    {**N(qb["t"] - 0.05, 640, 500, None, src=V9 + "closing9_N55.mp4", w=760), "from": FROM(sk_b - 0.05)},
    N(qa["t"] + 0.3, 1450, 360, "قولولي في الكومنت: عايزين فيديوهات إيه تاني؟", emo="speech_balloon", size=22),
    N(tpb, 1450, 560, "AI بالكامل", emo="robot", size=26),
    N(tor, 1450, 720, "ولا أنا بنفسي", emo="person_raising_hand", size=26)])
print("v9 specs:", len(SPECS), "| words not found:", [m for m in MISS6 if str(m[0]).startswith("v9:")])

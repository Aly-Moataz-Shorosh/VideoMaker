"""v10 note 7: the script words (work/words_v11.json, times GUESSED in script order) get the REAL times heard by Whisper
(work/whisper_words_v11.json) -> work/words_v11_real.json. Sequence alignment on normalised tokens; unmatched words are placed
between their matched neighbours. Also `name_time(name, t)` = the nearest REAL moment a product name is said (±4 s), used to put
every logo on its word (Premiere/Photoshop were swapped vs the script in v10).
Usage (project folder): python -X utf8 work/scripts/words_real_v11.py"""
import json, re, difflib

def norm(w):
    w = re.sub(r"[ً-ْـ«»\"'.,،؛:؟?!()\-…]", "", w.lower())
    w = w.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")
    for p in ("وال", "ال", "و", "بال", "لل"):
        if w.startswith(p) and len(w) > len(p) + 2: w = w[len(p):]; break
    return w

NAMES = {"Premiere": ["premiere", "بريمير", "بريميير", "البريمير"], "Photoshop": ["photoshop", "فوتوشوب"], "After Effects": ["after", "افتر"],
         "DaVinci": ["davinci", "دافنشي", "دافينشي", "دافنتشي"], "Blender": ["blender", "بلندر", "البلندر"], "Claude": ["claude", "كلود", "كلاود"],
         "Codex": ["codex", "كودكس", "كوديكس"], "Cursor": ["cursor", "كيرسر", "كرسر", "كورسر"], "Antigravity": ["antigravity", "انتي"],
         "Remotion": ["remotion", "ريموشن", "الموشن"], "ffmpeg": ["ffmpeg", "اف"], "Whisper": ["whisper", "ويسبر", "وسبر"],
         "HeyGen": ["heygen", "هايجن", "هيجن", "هاي"], "ElevenLabs": ["elevenlabs", "ايلفن", "اليفن", "ليفن"], "Higgsfield": ["higgsfield", "هيجز", "هيجزفيلد"],
         "Suno": ["suno", "سونو"], "Kling": ["kling", "كلينج"], "Veo": ["veo", "فيو"], "Seedance": ["seedance", "سيدانس"], "Luma": ["luma", "لوما"],
         "CapCut": ["capcut", "كاب"], "Runway": ["runway", "رانواي"], "Firefly": ["firefly", "فايرفلاي"], "ComfyUI": ["comfy", "كومفي"],
         "Magnific": ["magnific", "ماجنيفيك"], "Midjourney": ["midjourney", "ميدجيرني"], "ChatGPT": ["chatgpt", "شات"], "Gemini": ["gemini", "جيميني"],
         "three.js": ["three", "ثري"], "Python": ["python", "بايثون"], "Genjutsu": ["genjutsu", "جينجتسو", "جنجتسو"], "Meta": ["meta", "ميتا"],
         "TikTok": ["tiktok", "تيك"], "Instagram": ["instagram", "انستجرام"], "YouTube": ["youtube", "يوتيوب"], "Facebook": ["facebook", "فيسبوك"]}
_RAW = None
def _raw():
    global _RAW
    if _RAW is None: _RAW = json.load(open("work/whisper_words_v11.json", encoding="utf-8"))
    return _RAW
def name_time(name, t, win=4.0):
    keys = [norm(k) for k in NAMES.get(name, [name])]
    hits = [w["a"] for w in _raw() if abs(w["a"] - t) <= win and any(norm(w["w"]).startswith(k) or k in norm(w["w"]) for k in keys if len(k) >= 3)]
    return round(min(hits, key=lambda a: abs(a - t)), 3) if hits else None

if __name__ == "__main__":
    S = json.load(open("work/words_v11.json", encoding="utf-8")); R = _raw()
    a = [norm(w["w"]) for w in S]; b = [norm(w["w"]) for w in R]
    real = [None] * len(S)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            i, j = blk.a + k, blk.b + k
            if abs(R[j]["a"] - S[i]["a"]) < 6: real[i] = (R[j]["a"], R[j]["b"])
    n_m = sum(r is not None for r in real)
    out = []
    for i, w in enumerate(S):
        if real[i]: out.append({**w, "a": round(real[i][0], 3), "b": round(real[i][1], 3), "real": True}); continue
        p = next((k for k in range(i - 1, -1, -1) if real[k]), None); q = next((k for k in range(i + 1, len(S)) if real[k]), None)
        if p is not None and q is not None and S[q]["a"] > S[p]["a"]:
            f = (w["a"] - S[p]["a"]) / (S[q]["a"] - S[p]["a"]); ta = real[p][1] + f * (real[q][0] - real[p][1])
            out.append({**w, "a": round(ta, 3), "b": round(ta + (w["b"] - w["a"]), 3)})
        else: out.append(dict(w))
    out.sort(key=lambda w: w["a"])   # TIME order: the word search stops at the first far match (unsorted = items fell back to the board start)
    json.dump(out, open("work/words_v11_real.json", "w", encoding="utf-8"), ensure_ascii=False)
    sh = [0.0]
    print(f"{len(S)} script words, {n_m} matched to real audio ({100 * n_m / len(S):.0f} %), moved > 0.3 s: {sum(x > 0.3 for x in sh)}, max {max(sh):.2f} s")
    print("Premiere @", name_time("Premiere", 830), "| Photoshop @", name_time("Photoshop", 830))

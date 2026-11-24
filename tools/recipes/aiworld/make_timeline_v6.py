"""Timeline v6 (Aly's 50 notes on v5, «نفذ كله»): the video in a NEW ORDER (note 44), new narration N1–N3 (notes 32, 39, 40),
re-voiced sentences (3D ×5, قطعة ×4, القاعدة), cut phrases (notes 38, 41), and a real 1.6 s pause before every sub-category
(the tree-map separator, notes 3 + 37). Everything is built from the v2 voice (source) + new files, cut in silences, 10 ms fades.
Writes work/timeline_v6.json (pieces + v2→v6 map + seps), work/words_v6.json, output/audio_stems_v6/ (voice, song stems, mix).
Usage (project folder): python -X utf8 work/scripts/make_timeline_v6.py"""
import json, subprocess
from pathlib import Path
import numpy as np

SR = 48000
S = {s["id"]: s for s in json.load(open("work/sentences_v3.json", encoding="utf-8"))}
m2 = json.load(open("work/rough_v2_map.json", encoding="utf-8")); S0, EX = m2["song_start"], m2["extra"]
rm2 = lambda t: t if t <= S0 + 180 else t + EX
SA = lambda i: S[i]["a"]; SB = lambda i: S[i]["b"]   # sentences_v3 is already on the v2 (song-shifted) clock
V2 = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "output/audio_stems_v2/voice_full_timeline.wav", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                  capture_output=True).stdout, np.float32)
def rms(t, w=0.02):
    i = int(t * SR); s = V2[max(0, i - int(w * SR)): i + int(w * SR)]
    return float(np.sqrt((s ** 2).mean() + 1e-12))
def snap(t, back=0.35, fwd=0.35):
    """nearest quiet point (the quietest 40 ms window) around t"""
    cands = np.arange(t - back, t + fwd, 0.01)
    return float(min(cands, key=lambda x: (rms(x) > 0.004, abs(x - t) if rms(x) <= 0.004 else rms(x))))

# words in v2 time (from words_v5 through the inverse of the v5 edits)
T5 = json.load(open("work/timeline_v5.json", encoding="utf-8")); W5 = json.load(open("work/words_v5.json", encoding="utf-8"))
def inv5(t):
    d = 0.0
    for e in T5["edits"]:
        if t >= e["v2_b"] + d + e["delta"] - 1e-6: d += e["delta"]
    return t - d
v5_spans = []
d = 0.0
for e in T5["edits"]:
    st = e["v2_a"] + d; v5_spans.append((st, st + (e["trim"][1] - e["trim"][0] if e["file"] else 0), e)); d += e["delta"]
W2 = []
for w in W5:
    inside = next((sp for sp in v5_spans if sp[0] - 0.01 <= w["a"] < sp[1] - 0.01), None)
    if inside: W2.append({"w": w["w"], "a": inside[2]["v2_a"] + (w["a"] - inside[0]), "b": inside[2]["v2_a"] + (w["b"] - inside[0]), "file": inside[2]["file"]})
    else: W2.append({"w": w["w"], "a": inv5(w["a"]), "b": inv5(w["b"])})

F6 = "assets/ai/heygen/voice_fix_v6/"
REVOICE = {"S003.5": F6 + "S003.5_3d.wav", "S016.1": F6 + "S016.1_3d.wav", "S016.2": F6 + "S016.2_3d.wav", "S016.5": F6 + "S016.5_3d.wav",
           "S033.3": F6 + "S033.3_3d.wav", "S003.2": F6 + "S003.2_qeta.wav", "S003.3": F6 + "S003.3_qeta.wav", "S004.7": F6 + "S004.7_qeta.wav",
           "S016.4": F6 + "S016.4_qeta.wav", "S012.8": F6 + "S012.8_qaeda.wav",
           "S005.4": "assets/ai/heygen/voice_fix_v1/S005.4_magnific.wav", "S007.2": "assets/ai/heygen/voice_fix_v1/S007.2_kalam_maktoob.wav",
           "S009.2": "assets/ai/heygen/voice_fix_v1/S009.2_kalam_maktoob.wav"}
NEW = {"N1": F6 + "N1_llm_agent.wav", "N2": F6 + "N2_mcp.wav", "N3": F6 + "N3_skills.wav"}
KEEP = {"S034.4": (626.80, 629.42), "S036.6": (666.30, 669.02)}   # keep only «وتحويل أنيميشن After Effects لكود» / «skill بتكتب السكريبت بأسلوب صاحب القناة» (notes 38, 41)
DROP = {"S006.9", "S032.1", "S032.2", "S032.3", "S032.4", "S032.5", "S035.4", "S036.2"}   # removed / said better by N1–N3

def ids(a, b):
    keys = list(S.keys()); return keys[keys.index(a): keys.index(b) + 1]
SEP = lambda fam, name: ("SEP", fam, name)
ORDER = ([*ids("S001.1", "S006.9")]
         + [SEP(0, "الصور")] + ids("S007.1", "S008.5") + [SEP(0, "الفيديو")] + ids("S009.1", "S010.7")
         + [SEP(0, "الأفاتار")] + ids("S011.1", "S012.9") + [SEP(0, "الصوت")] + ids("S013.1", "S014.5")
         + [SEP(0, "المزيكا")] + ids("S015.1", "S015.7") + [SEP(0, "3D")] + ids("S016.1", "S017.4")
         + [SEP(0, "مواقع التوليد")] + ids("S019.1", "S019.3") + ids("S020.1", "S021.7") + [SEP(0, "ElevenLabs")] + ids("S022.1", "S023.2")
         + [SEP(0, "Higgsfield")] + ids("S024.1", "S025.5") + [SEP(0, "Suno")] + ids("S026.1", "S026.6")
         + [SEP(0, "على جهازك ببلاش")] + ids("S030.1", "S030.6")
         + [SEP(1, "يعني إيه LLM و agent")] + ["N1"] + [SEP(1, "الـ AI اللي بيفهم")] + ids("S018.1", "S018.4")
         + [SEP(1, "Claude")] + ids("S027.1", "S027.5") + [SEP(1, "Codex")] + ids("S028.1", "S028.5")
         + [SEP(1, "الموديلات الصيني")] + ids("S029.1", "S029.4") + [SEP(1, "الـ agents بتشتغل إزاي")] + ids("S032.1", "S033.4")
         + [SEP(2, "السكريبتات")] + ids("S034.1", "S034.4") + [SEP(3, "الـ MCP")] + ["S035.1", "S035.2", "N2"] + ids("S035.3", "S035.7")
         + [SEP(4, "الـ skills")] + ["S036.1", "N3"] + ids("S036.2", "S036.6")
         + [SEP(4, "الفيديو ده اتعمل بإيه")] + ids("S031.1", "S031.3")
         + [SEP(5, "تجربة حقيقية")] + ids("S037.1", "S040.6") + [SEP(5, "خطوة بخطوة")] + ids("S041.1", "S044.11")
         + [SEP(5, "تريكات")] + ids("S045.1", "S048.9") + [SEP(5, "الأسعار")] + ids("S049.1", "S050.3")
         + [SEP(5, "دور الإنسان")] + ids("S051.1", "S052.3") + [SEP(5, "علامة الـ AI")] + ids("S053.1", "S054.6")
         + [SEP(5, "الأغنية")] + ids("S055.1", "S055.5") + ["SONG"] + ids("S057.1", "S058.4"))
ORDER = [x for x in ORDER if not (isinstance(x, str) and x in DROP)]
used = {x for x in ORDER if isinstance(x, str)}
missing = [k for k in S if k not in used and k not in DROP]
assert not missing, missing

def file_span(f, pad=0.06):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    e = np.sqrt(np.convolve(a ** 2, np.ones(960) / 960, "same")); on = np.where(e > 0.01)[0]
    return max(0, on[0] / SR - pad), min(len(a) / SR, on[-1] / SR + pad)

# ---- pieces ----
pieces = []   # {kind: v2|file|gap|song, a, b (source), sid(s), ...}
for x in ORDER:
    if isinstance(x, tuple): pieces.append({"kind": "gap", "dur": 1.6, "sep": [x[1], x[2]]}); continue
    if x == "SONG":
        pieces.append({"kind": "v2", "a": SB("S055.5"), "b": SA("S057.1"), "sids": ["SONG"], "song": True}); continue
    if x in NEW:
        ta, tb = file_span(NEW[x]); pieces.append({"kind": "file", "f": NEW[x], "a": ta, "b": tb, "sids": [x], "new": True}); continue
    if x in REVOICE:
        ta, tb = file_span(REVOICE[x]); pieces.append({"kind": "file", "f": REVOICE[x], "a": ta, "b": tb, "sids": [x], "rep": [SA(x), SB(x)]}); continue
    a, b = SA(x), SB(x)
    if x in KEEP:
        pieces.append({"kind": "v2", "a": KEEP[x][0], "b": KEEP[x][1], "sids": [x], "fixed": True}); continue
    prev = pieces[-1] if pieces else None
    if prev and prev["kind"] == "v2" and not prev.get("song") and abs(prev["b"] - a) < 1.2 and prev["sids"][-1] != x:
        prev["b"] = b; prev["sids"].append(x)   # contiguous in the source: one piece (keeps the real pauses)
    else:
        pieces.append({"kind": "v2", "a": a, "b": b, "sids": [x]})
# cut points in silence, a short breath at every jump
for i, p in enumerate(pieces):
    if p["kind"] != "v2": continue
    p["a"] = snap(p["a"] - 0.08, 0.12 if p.get("fixed") else 0.3, 0.12); p["b"] = snap(p["b"] + 0.08, 0.12, 0.12 if p.get("fixed") else 0.35)
# pieces that touch in the SOURCE (e.g. split by a separator) get one shared cut point: no word heard twice
v2p = sorted([p for p in pieces if p["kind"] == "v2"], key=lambda p: p["a"])
for x, y in zip(v2p, v2p[1:]):
    if y["a"] < x["b"] + 0.05 and y["a"] > x["a"]:
        c = snap((x["b"] + y["a"]) / 2, 0.2, 0.2); x["b"] = c; y["a"] = c
t = 0.0; GAP = 0.3
for i, p in enumerate(pieces):
    if p["kind"] == "gap": p["t"] = round(t, 3); t += p["dur"]; continue
    if i > 0 and pieces[i - 1]["kind"] != "gap": t += GAP
    p["t"] = round(t, 3); t += p["b"] - p["a"]
TOTAL = round(t + 0.5, 3)

# ---- audio ----
O = Path("output/audio_stems_v6"); (O / "music").mkdir(parents=True, exist_ok=True)
F = 0.01
ins, fl, mix = ["-i", "output/audio_stems_v2/voice_full_timeline.wav"], [], []
files = {}
for p in pieces:
    if p["kind"] == "file" and p["f"] not in files: files[p["f"]] = len(files) + 1; ins += ["-i", p["f"]]
for k, p in enumerate(pieces):
    if p["kind"] == "gap": continue
    src = 0 if p["kind"] == "v2" else files[p["f"]]; d = p["b"] - p["a"]; ms = int(round(p["t"] * 1000))
    fl.append(f"[{src}]atrim={p['a']:.4f}:{p['b']:.4f},asetpts=N/SR/TB,aresample={SR},aformat=channel_layouts=mono,afade=t=in:d={F},"
              f"afade=t=out:st={max(0, d - F):.4f}:d={F},adelay={ms}|{ms}[p{k}]"); mix.append(f"[p{k}]")
fl.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0,apad,atrim=0:{TOTAL}[o]")
open("work/_tl6_filter.txt", "w").write(";".join(fl))
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex_script", "work/_tl6_filter.txt", "-map", "[o]", "-c:a", "pcm_s24le", str(O / "voice_full_timeline.wav")], check=True)
song = next(p for p in pieces if p.get("song")); s0 = round(song["t"] + (S0 - song["a"]), 3)
for nm in ("song_C1_full", "song_C1_vocals", "song_C1_music_only"):
    ms = int(round(s0 * 1000))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"output/audio_stems_v1/music/{nm}.wav", "-af", f"aresample={SR},adelay={ms}|{ms},apad,atrim=0:{TOTAL}",
                    "-c:a", "pcm_s24le", str(O / "music" / f"{nm}_timeline.wav")], check=True)

# ---- words + v2→v6 map ----
W6 = []
for p in pieces:
    if p["kind"] == "v2":
        for w in W2:
            if p["a"] - 0.02 <= w["a"] < p["b"] - 0.02 and not w.get("file"):
                W6.append({"w": w["w"], "a": round(p["t"] + w["a"] - p["a"], 3), "b": round(p["t"] + w["b"] - p["a"], 3)})
json.dump({"pieces": pieces, "total": TOTAL, "song_start_v6": s0}, open("work/timeline_v6.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(W6, open("work/_words_v6_v2part.json", "w", encoding="utf-8"), ensure_ascii=False)
print("pieces", len(pieces), "seps", sum(p["kind"] == "gap" for p in pieces), "total", TOTAL, "song at", s0)

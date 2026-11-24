"""Timeline v11 = v10 + Aly's v10 notes 3/4/5/9 (review_rough_v10_notes.md): new twin lines N1b_a..i (libraries + the audiobook example, then
«تعالوا نسمع النتيجة» and the RESULT in an 11.1 s hold), N25c2 (the understand->order->wait loop), N25e2 (transparent motion), N37a..d (the
Playmobil script). Rest as v10.
"""
"""Timeline v10 = v9 + Aly's v9 notes (review_rough_v9_notes.md): kids v10 (real group), S009.3 keeps «في النص» before its hold (note 3),
Codex = Desktop app (S028.2 re-voiced, S028.4/5 cut -> N23), Claude Code example N25a-g (note 25), the 3-year reason N43b (43), DaVinci tip N48 (48),
song versions N53 (53), ending N39a-f (39) + CTA N56 (56), «عُود» re-voiced (52), the reel price lines cut (45). Was: Timeline v9 = v8 + Aly's v8 notes (review_rough_v8_notes.md): S003.3 re-voiced (note 2), kids voices on every separator + the OPEN tree before S003.1 (note 4),
new twin lines N25/N38/N43/N55a/N55b (carried v7 notes 25, 38, 43, 55). Was: Timeline v8 = v7 + Aly's v7 notes 1, 7, 16, 20, 21, 25, 37, 41, 45, 48 (see review_rough_v7_notes.md). Was: Timeline v7 = v6 + Aly's v6 notes 1, 2, 7, 8 (حربية whole, «ست» once, longer tree separators: the first one rides on HIS «This is the Aly Show» sting).
Was: Timeline v6 (Aly's 50 notes on v5, «نفذ كله»): the video in a NEW ORDER (note 44), new narration N1–N3 (notes 32, 39, 40),
re-voiced sentences (3D ×5, قطعة ×4, القاعدة), cut phrases (notes 38, 41), and a real 1.6 s pause before every sub-category
(the tree-map separator, notes 3 + 37). Everything is built from the v2 voice (source) + new files, cut in silences, 10 ms fades.
Writes work/timeline_v10.json (pieces + v2→v6 map + seps), work/words_v8.json, output/audio_stems_v10/ (voice, song stems, mix).
Usage (project folder): python -X utf8 work/scripts/make_timeline_v7.py"""
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
REVOICE = {"S003.5": F6 + "S003.5_3d.wav", "S016.1": F6 + "S016.1_3d.wav", "S016.2": F6 + "S016.2_3d.wav", "S016.5": "assets/ai/heygen/voice_fix_v8/S016.5_gs.wav",
           "S033.3": F6 + "S033.3_3d.wav", "S003.2": F6 + "S003.2_qeta.wav", "S003.3": "assets/ai/heygen/v9/S003.3_v9.wav", "S028.2": "assets/ai/heygen/v10/S028.2_v10.wav", "S055.4": "assets/ai/heygen/v10/S055.4_oud.wav", "S004.7": F6 + "S004.7_qeta.wav",
           "S016.4": F6 + "S016.4_qeta.wav", "S012.8": F6 + "S012.8_qaeda.wav",
           "S005.4": "assets/ai/heygen/voice_fix_v1/S005.4_magnific.wav", "S007.2": "assets/ai/heygen/voice_fix_v1/S007.2_kalam_maktoob.wav",
           "S009.2": "assets/ai/heygen/voice_fix_v8/S009.2a.wav"}
TAIL = {"S009.2b": "assets/ai/heygen/voice_fix_v8/S009.2b.wav"}   # note 7: «وأقوى حاجة:» starts the NEXT part, after the hold
V9 = "assets/ai/heygen/v9/"; V10 = "assets/ai/heygen/v10/"; V11 = "assets/ai/heygen/v11/"
NEW = {"N1": F6 + "N1_llm_agent.wav", "N2": "assets/ai/heygen/voice_fix_v8/N2_v8.wav", "N3": F6 + "N3_skills.wav",
       "N25": V9 + "N25_higgs_video.wav", "N38": V9 + "N38_scripts.wav", "N43": V9 + "N43_skill.wav", "N55a": V9 + "N55a_comment.wav", "N55b": V9 + "N55b_opinion.wav",
       **{k: V10 + k + ".wav" for k in ["N23_alt_tools", "N25a", "N25b", "N25c", "N25d", "N25e", "N25f", "N25g", "N43b_reason", "N48_davinci", "N53_song_versions",
                                        "N39a", "N39b", "N39c", "N39d", "N39e", "N39f", "N56_cta"]},
       **{k: V11 + k + ".wav" for k in json.load(open(V11 + "lines_v11_text.json", encoding="utf-8"))}}
KIDS = json.load(open("assets/ai/elevenlabs/kids_v10/kids_index.json", encoding="utf-8"))
KID_LEN = dict(zip(KIDS["names"], KIDS["speech"]))   # note 4: the kids shout the name, the tree stays until they finish + the cheer
KEEP = {"S034.4": (627.53, 629.42), "S036.6": (666.30, 669.02), "S041.7": (761.50, 764.02), "S035.3": (636.40, 639.98), "S016.3": (289.50, 291.50), "S009.3": (146.97, 152.14)}   # v10 note 3: «النص» ends at 152.06, the silence at 152.14   # v8: 37 (no «ب و» before «تحويل»), 48 (no PowerShell)
EXACT = {"S034.4", "S041.7", "S035.3", "S016.3", "S009.3"}   # moved sentences: no «وفيه» / no double «الكاميرا»   # keep only «وتحويل أنيميشن After Effects لكود» / «skill بتكتب السكريبت بأسلوب صاحب القناة» (notes 38, 41)
DROP = {"S006.9", "S032.1", "S032.2", "S032.3", "S032.4", "S032.5", "S035.4", "S036.2", "S042.7", "S042.8", "S028.4", "S028.5", "S044.10", "S044.11"}   # v10 notes 23 (Gemini CLI info), 45 (no price line)   # v8 note 41: no .mcp.json / /mcp   # removed / said better by N1–N3

def ids(a, b):
    keys = list(S.keys()); return keys[keys.index(a): keys.index(b) + 1]
SEP = lambda fam, name: ("SEP", fam, name)
ORDER = ([*ids("S001.1", "S002.5")] + [SEP(-1, "OPEN")] + [*ids("S003.1", "S006.9")]
         + [SEP(0, "الصور")] + ids("S007.1", "S008.5") + [SEP(0, "الفيديو")] + ["S009.1", "S009.2", "S009.2b"] + ids("S009.3", "S010.7")
         + [SEP(0, "الأفاتار")] + ids("S011.1", "S012.9") + [SEP(0, "الصوت")] + ids("S013.1", "S014.5")
         + [SEP(0, "المزيكا")] + ids("S015.1", "S015.7") + [SEP(0, "3D")] + ["S016.1", "S016.2", "S016.5"] + ids("S017.1", "S017.4")
         + [SEP(0, "مواقع التوليد")] + ids("S019.1", "S019.3") + ids("S020.1", "S021.7") + [SEP(0, "ElevenLabs")] + ids("S022.1", "S023.2")
         + [SEP(0, "Higgsfield")] + ids("S024.1", "S025.5") + ["N25"] + [SEP(0, "Suno")] + ids("S026.1", "S026.6")
         + [SEP(0, "على جهازك ببلاش")] + ids("S030.1", "S030.6")
         + [SEP(1, "يعني إيه LLM والـ agent")] + ["N1", "N1b_a", "N1b_b", "N1b_c", "N1b_d", "N1b_e", "N1b_f", "N1b_g", "N1b_h", "N1b_i"] + [SEP(1, "الـ AI اللي بيفهم")] + ids("S018.1", "S018.4")
         + [SEP(1, "Claude")] + ids("S027.1", "S027.3") + ["N25a", "N25b", "N25c", "N25c2", "N25d", "N25e", "N25e2", "N25f", "N25g"] + ids("S027.4", "S027.5") + [SEP(1, "Codex")] + ids("S028.1", "S028.3") + ["N23_alt_tools"]
         + [SEP(1, "الموديلات الصيني")] + ids("S029.1", "S029.4") + [SEP(1, "الـ agents بتشتغل إزاي")] + ids("S032.1", "S033.4")
         + [SEP(2, "السكريبتات")] + ids("S034.1", "S034.4") + ["N38"] + [SEP(3, "الـ MCP")] + ["S035.1", "S035.2", "N2"] + ["S035.3", "S035.4", "S016.3", "S016.4"] + ids("S035.5", "S035.7") + ids("S031.1", "S031.3")
         + [SEP(4, "الـ skills")] + ["S036.1", "N3"] + ids("S036.2", "S036.6") + ["N37a", "N37b", "N37c", "N37d"] + ["N43"]
         
         + [SEP(5, "تجربة حقيقية")] + ids("S037.1", "S037.3") + ["N43b_reason"] + ids("S038.1", "S040.6") + [SEP(5, "خطوة بخطوة")] + ids("S041.1", "S044.11")
         + [SEP(5, "تريكات")] + ids("S045.1", "S045.6") + ["N48_davinci"] + ids("S046.1", "S048.9") + [SEP(5, "الأسعار")] + ids("S049.1", "S050.3")
         + [SEP(5, "دور الإنسان")] + ids("S051.1", "S052.3") + [SEP(5, "علامة الـ AI")] + ids("S053.1", "S054.6")
         + [SEP(5, "الأغنية")] + ids("S055.1", "S055.5") + ["N53_song_versions", "SONG"] + ids("S057.1", "S057.5") + ["N39a", "N39b", "N39c", "N39d", "N39e", "N39f"] + ids("S058.1", "S058.3") + ["N55a", "N55b", "N56_cta", "S058.4"])
ORDER = [x for x in ORDER if not (isinstance(x, str) and x in DROP)]
used = {x for x in ORDER if isinstance(x, str)}
missing = [k for k in S if k not in used and k not in DROP]   # (S009.2b is a tail piece, not a sentence id)
assert not missing, missing

def file_span(f, pad=0.06):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    e = np.sqrt(np.convolve(a ** 2, np.ones(960) / 960, "same")); on = np.where(e > 0.01)[0]
    return max(0, on[0] / SR - pad), min(len(a) / SR, on[-1] / SR + pad)

# ---- pieces ----
pieces = []   # {kind: v2|file|gap|song, a, b (source), sid(s), ...}
HOLD_AFTER = {"S009.2": 2.0, "S009.3": 1.8, "S009.5": 2.2, "S012.9": 2.0, "N25": 2.5, "N38": 1.5, "N43": 1.5, "N25g": 1.2, "N39f": 0.8, "N1b_i": 11.1, "N37d": 1.2, "N23_alt_tools": 1.5, "S050.3": 3.0}   # N1: the audiobook example (note 31) plays in this pause   # v8 notes 7, 8, 9, 16, 25   # «سيبه يظهر شوية» / «متنقلش بسرعة»
FIRST_SEP, SEP_DUR = 3.2, 3.0   # v8 note 3: the tree is already drawn, stays a bit longer (no sting)   # v6 note 7: the first tree stands still under his intro sting (4.43 s); note 8: every separator slower (was 1.6 s)
for x in ORDER:
    if pieces and pieces[-1]["kind"] in ("v2", "file") and pieces[-1]["sids"][-1] in HOLD_AFTER and pieces[-1]["sids"][-1] != x:
        pieces.append({"kind": "hold", "dur": HOLD_AFTER[pieces[-1]["sids"][-1]]})   # a silent hold so the board stays on screen (v6 9/10, v7 7/8/9/16/25)
    if isinstance(x, tuple):
        kl = KID_LEN.get(x[2], 1.0)   # the kids' shout starts 0.35 s in; the tree holds until it ends + 1.4 s of cheer
        pieces.append({"kind": "gap", "dur": round(max(SEP_DUR, 0.35 + kl + 1.4), 2), "sep": [x[1], x[2]]}); continue
    if x == "SONG":
        pieces.append({"kind": "v2", "a": SB("S055.5"), "b": SA("S057.1"), "sids": ["SONG"], "song": True}); continue
    if x in TAIL:
        ta, tb = file_span(TAIL[x]); pieces.append({"kind": "file", "f": TAIL[x], "a": ta, "b": tb, "sids": [x]}); continue
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
    if p["sids"][0] in EXACT: continue   # measured by hand on the waveform (v8 notes 37, 48)
    p["a"] = snap(p["a"] - 0.08, 0.12 if p.get("fixed") else 0.3, 0.12); p["b"] = snap(p["b"] + 0.08, 0.12, 0.12 if p.get("fixed") else 0.35)
FIXB = {"S003.1": 31.62}   # v6 note 1: «حربية» ends at 31.55 in the source (its soft «ـية» was cut at 31.39)
for p in pieces:
    if p["kind"] == "v2" and p["sids"][-1] in FIXB: p["b"] = FIXB[p["sids"][-1]]
# pieces that touch in the SOURCE (e.g. split by a separator) get one shared cut point: no word heard twice
v2p = sorted([p for p in pieces if p["kind"] == "v2"], key=lambda p: p["a"])
for x, y in zip(v2p, v2p[1:]):
    if y["a"] < x["b"] + 0.05 and y["a"] > x["a"]:
        c = snap((x["b"] + y["a"]) / 2, 0.2, 0.2); x["b"] = c; y["a"] = c
t = 0.0; GAP = 0.3
for i, p in enumerate(pieces):
    if p["kind"] in ("gap", "hold"): p["t"] = round(t, 3); t += p["dur"]; continue
    if i > 0 and pieces[i - 1]["kind"] not in ("gap", "hold"): t += GAP
    p["t"] = round(t, 3); t += p["b"] - p["a"]
TOTAL = round(t + 0.5, 3)
for i, p in enumerate(pieces):
    if p["kind"] == "hold" and i > 0 and i + 1 < len(pieces) and pieces[i + 1]["kind"] == "v2":
        prv = pieces[i - 1]; nx = pieces[i + 1]
        if prv["kind"] == "v2" and prv["sids"][-1] in S:
            assert nx["a"] >= SB(prv["sids"][-1]) - 0.05, ("a word of", prv["sids"][-1], "is after the hold", nx["a"], SB(prv["sids"][-1]))

# ---- audio ----
O = Path("output/audio_stems_v11"); (O / "music").mkdir(parents=True, exist_ok=True)
F = 0.01
ins, fl, mix = ["-i", "output/audio_stems_v2/voice_full_timeline.wav"], [], []
files = {}
for p in pieces:
    if p["kind"] == "file" and p["f"] not in files: files[p["f"]] = len(files) + 1; ins += ["-i", p["f"]]
for k, p in enumerate(pieces):
    if p["kind"] in ("gap", "hold"): continue
    src = 0 if p["kind"] == "v2" else files[p["f"]]; d = p["b"] - p["a"]; ms = int(round(p["t"] * 1000))
    fl.append(f"[{src}]atrim={p['a']:.4f}:{p['b']:.4f},asetpts=N/SR/TB,aresample={SR},aformat=channel_layouts=mono,afade=t=in:d={F},"
              f"afade=t=out:st={max(0, d - F):.4f}:d={F},adelay={ms}|{ms}[p{k}]"); mix.append(f"[p{k}]")
fl.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0,apad,atrim=0:{TOTAL}[o]")
open("work/_tl10_filter.txt", "w").write(";".join(fl))
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex_script", "work/_tl10_filter.txt", "-map", "[o]", "-c:a", "pcm_s24le", str(O / "voice_full_timeline.wav")], check=True)
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
env = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(O / "voice_full_timeline.wav"), "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
fr_ = 320; rr = np.sqrt(np.array([(env[i:i + fr_] ** 2).mean() for i in range(0, len(env) - fr_, fr_)]) + 1e-12); rr = np.clip(rr / np.percentile(rr, 99), 0, 1)
json.dump([round(float(v), 3) for v in rr], open("work/voice_env_v11.json", "w"))
json.dump({"pieces": pieces, "total": TOTAL, "song_start_v6": s0}, open("work/timeline_v11.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(W6, open("work/_words_v11_v2part.json", "w", encoding="utf-8"), ensure_ascii=False)
print("pieces", len(pieces), "seps", sum(p["kind"] == "gap" for p in pieces), "total", TOTAL, "song at", s0)

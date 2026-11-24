"""Timeline v4 (Aly's v3 notes): every voice edit in ONE place, in v2 time.
  replace S007.2 / S009.2 («كلام مكتوب»), replace S005.4 («زي Higgsfield أو Magnific», note 8), REMOVE S006.9 («عايز تبدأ تعمل فيديوهات AI؟», note 13).
Writes: work/timeline_v4.json (edits + v4(t) shifts), work/words_v4.json (script words on v4 times; English names re-timed from the
voice itself with Whisper + a prompt of the names, note 6), output/audio_stems_v4/ (voice, song stems, review mix) — every sound separate.
Usage (project folder): python -X utf8 work/scripts/make_timeline_v4.py"""
import json, re, subprocess
from pathlib import Path
import numpy as np

S = {s["id"]: s for s in json.load(open("work/sentences_v3.json", encoding="utf-8"))}
tl = json.load(open("work/timeline_v2.json", encoding="utf-8"))
m2 = json.load(open("work/rough_v2_map.json", encoding="utf-8"))
S0, EX = m2["song_start"], m2["extra"]
rm2 = lambda t: t if t <= S0 + 180 else t + EX
F = "assets/ai/heygen/voice_fix_v1/"
EDITS = [  # sid, new file (None = remove), trim a, b (s in the new file), new words [w, a, b] (file time)
    ("S005.4", F + "S005.4_magnific.wav", 0.249, 3.421, [["الأداة", .299, .725], ["هي", .768, .896], ["الموقع", .939, 1.237], ["اللي", 1.28, 1.451],
        ["بتكتب", 1.493, 1.707], ["فيه،", 1.749, 1.877], ["زي", 2.091, 2.261], ["Higgsfield", 2.347, 2.773], ["أو", 2.944, 3.072], ["Magnific.", 3.115, 3.371]]),
    ("S006.9", None, 0, 0, []),
    ("S007.2", F + "S007.2_kalam_maktoob.wav", 0.249, 3.293, [["كلام", 0.299, 0.597], ["مكتوب", 0.64, 1.024], ["يبقى", 1.237, 1.493], ["صورة،", 1.536, 1.835],
        ["وصورة", 2.048, 2.645], ["تبقى", 2.688, 2.944], ["صورة.", 2.987, 3.243]]),
    ("S009.2", F + "S009.2_kalam_maktoob.wav", 0.206, 3.634, [["كلام", 0.256, 0.597], ["مكتوب", 0.64, 0.896], ["يبقى", 0.939, 1.152], ["فيديو،", 1.195, 1.451],
        ["وصورة", 1.664, 2.091], ["تبقى", 2.133, 2.304], ["فيديو،", 2.347, 2.56], ["وأقوى", 2.773, 3.285], ["حاجة:", 3.328, 3.584]]),
]
ED = []
for sid, f, a, b, ws in EDITS:
    s = S[sid]; old = s["b"] - s["a"]; new = (b - a) if f else 0.0
    if not f:   # removing a sentence also removes the pause before it (the previous sentence's end -> the next sentence's start)
        prev = max((x for x in S.values() if x["b"] <= s["a"] + 0.01), key=lambda x: x["b"])
        old = s["b"] - prev["b"]; s = {**s, "a": prev["b"]}
    ED.append(dict(sid=sid, v2_a=s["a"], v2_b=s["b"], file=f, trim=[a, b], words=ws, delta=round(new - old, 3)))
ED.sort(key=lambda e: e["v2_a"])

def v4(t):   # v2 (song-remapped) time -> v4 time; times INSIDE a removed piece collapse to its start
    d = 0.0
    for e in ED:
        if t >= e["v2_b"] - 1e-6: d += e["delta"]
        elif e["file"] is None and t > e["v2_a"]: return round(e["v2_a"] + d, 3)
    return round(t + d, 3)
TOTAL = v4(m2["total"])

W = []
for c in tl["chapters"]:
    for seg in c["segments"]:
        for w, a, b in seg.get("word_times") or []:
            W.append({"w": w, "a": rm2(a), "b": rm2(b)})
for e in ED:   # drop the old words of every edited sentence, add the new ones
    W = [w for w in W if not (e["v2_a"] - 0.01 <= w["a"] < e["v2_b"] - 0.01)]
W = [{"w": w["w"], "a": v4(w["a"]), "b": v4(w["b"])} for w in W]
for e in ED:
    st = v4(e["v2_a"])
    W += [{"w": w, "a": round(st + x - e["trim"][0], 3), "b": round(st + y - e["trim"][0], 3)} for w, x, y in e["words"]]
W.sort(key=lambda w: w["a"])

# ---- audio v4 (every sound separate) ----
SR = 48000; O = Path("output/audio_stems_v4"); (O / "music").mkdir(parents=True, exist_ok=True)
run = lambda a: subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
ins, fl, cur, k, n = ["-i", "output/audio_stems_v2/voice_full_timeline.wav"], [], 0.0, 0, 1
for e in ED:
    fl.append(f"[0]atrim={cur}:{e['v2_a']},asetpts=N/SR/TB,aresample={SR}[p{k}]"); k += 1
    if e["file"]:
        ins += ["-i", e["file"]]
        fl.append(f"[{n}]atrim={e['trim'][0]}:{e['trim'][1]},asetpts=N/SR/TB,aresample={SR},aformat=channel_layouts=mono[p{k}]"); k += 1; n += 1
    cur = e["v2_b"]
fl.append(f"[0]atrim={cur},asetpts=N/SR/TB,aresample={SR}[p{k}]"); k += 1
fl.append("".join(f"[p{i}]" for i in range(k)) + f"concat=n={k}:v=0:a=1,apad,atrim=0:{TOTAL}[o]")
run(ins + ["-filter_complex", ";".join(fl), "-map", "[o]", "-c:a", "pcm_s24le", str(O / "voice_full_timeline.wav")])
s0 = v4(S0); ms = int(round(s0 * 1000))
for nm in ("song_C1_full", "song_C1_vocals", "song_C1_music_only"):
    run(["-i", f"output/audio_stems_v1/music/{nm}.wav", "-af", f"aresample={SR},adelay={ms}|{ms},apad,atrim=0:{TOTAL}", "-c:a", "pcm_s24le", str(O / "music" / f"{nm}_timeline.wav")])
run(["-i", str(O / "voice_full_timeline.wav"), "-i", str(O / "music/song_C1_full_timeline.wav"), "-filter_complex",
     "[0]pan=stereo|c0=c0|c1=c0[v];[1]volume=-3dB[s];[v][s]amix=inputs=2:normalize=0,alimiter=limit=0.95[o]", "-map", "[o]", "-c:a", "pcm_s16le", str(O / "mix_rough_v4.wav")])

# ---- English names: their real time from the voice (Whisper drops / misplaces Latin names, note 6) ----
from faster_whisper import WhisperModel
M = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
voice = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(O / "voice_full_timeline.wav"), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
lat = [i for i, w in enumerate(W) if re.search(r"[A-Za-z]{2,}", w["w"]) and W[i]["a"] < s0]
fixed = 0
for i in lat:
    name = re.sub(r"[^A-Za-z0-9.\- ]", "", W[i]["w"]).strip(".")
    if not name: continue
    a0 = max(0, W[i]["a"] - 2.5); seg = voice[int(a0 * 16000): int((W[i]["b"] + 2.5) * 16000)]
    segs, _ = M.transcribe(seg, language="ar", vad_filter=False, word_timestamps=True, initial_prompt=name)
    best = None
    for sg in segs:
        for wd in sg.words:
            if name.lower()[:4] in wd.word.lower():
                t = a0 + wd.start
                if best is None or abs(t - W[i]["a"]) < abs(best[0] - W[i]["a"]): best = (t, a0 + wd.end)
    if best and abs(best[0] - W[i]["a"]) > 0.15:
        W[i]["a"], W[i]["b"] = round(best[0], 3), round(best[1], 3); fixed += 1
json.dump(W, open("work/words_v4.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump({"edits": ED, "total": TOTAL, "song_start_v4": s0}, open("work/timeline_v4.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("total", TOTAL, "song at", s0, "edits", [(e["sid"], e["delta"]) for e in ED], "| English names", len(lat), "re-timed", fixed)

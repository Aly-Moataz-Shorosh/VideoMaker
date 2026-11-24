"""Timeline v5 (Aly's v4 note 8: «في صوت قطعة حاد»): the v4 edit points were Whisper sentence edges, some INSIDE speech
(S006.9 ended 0.2 s before the removed «AI؟» really ended -> its tail stayed = the harsh click). Here every edit point sits
in real silence (checked on the waveform) + 10 ms fades at every joint. Extra edits (e.g. the «3D» re-voices) go in EXTRA.
No Whisper run: words come from work/words_v4.json mapped through the new edits.
Writes work/timeline_v5.json, work/words_v5.json, output/audio_stems_v5/ (voice, song stems, review mix — every sound separate).
Usage (project folder): python -X utf8 work/scripts/make_timeline_v5.py"""
import json, subprocess
from pathlib import Path
import numpy as np

T4 = json.load(open("work/timeline_v4.json", encoding="utf-8")); W4 = json.load(open("work/words_v4.json", encoding="utf-8"))
m2 = json.load(open("work/rough_v2_map.json", encoding="utf-8"))
SNAP = {"S006.9": (101.40, 103.24), "S007.2": (106.23, 108.18), "S009.2": (143.86, 146.98), "S005.4": (70.57, 74.60)}   # measured silences (v2 time)
EXTRA = []   # (sid, file, trim_a, trim_b, words, v2_a, v2_b) — filled when new sentences are recorded

def mapper(ED):
    def f(t):
        d = 0.0
        for e in ED:
            if t >= e["v2_b"] - 1e-6: d += e["delta"]
            elif e["file"] is None and t > e["v2_a"]: return round(e["v2_a"] + d, 3)
        return round(t + d, 3)
    return f
def inverse(ED):   # v-time -> v2 time, outside edited pieces
    def g(t):
        d = 0.0
        for e in ED:
            if t >= e["v2_b"] + d + e["delta"] - 1e-6: d += e["delta"]
        return t - d
    return g
old_v, old_inv = mapper(T4["edits"]), inverse(T4["edits"])

ED = []
for e in T4["edits"]:
    a, b = SNAP.get(e["sid"], (e["v2_a"], e["v2_b"]))
    new = (e["trim"][1] - e["trim"][0]) if e["file"] else 0.0
    ED.append({**e, "v2_a": a, "v2_b": b, "delta": round(new - (b - a), 3)})
for sid, f, ta, tb, ws, a, b in EXTRA:
    ED.append(dict(sid=sid, v2_a=a, v2_b=b, file=f, trim=[ta, tb], words=ws, delta=round((tb - ta) - (b - a), 3)))
ED.sort(key=lambda e: e["v2_a"])
v5 = mapper(ED); TOTAL = v5(m2["total"])

# words: edited sentences re-placed from their files; every other word mapped v4 -> v2 -> v5
spans = [(old_v(e["v2_a"]), old_v(e["v2_a"]) + (e["trim"][1] - e["trim"][0] if e["file"] else 0)) for e in T4["edits"]]
spans += [(old_v(x[5]), old_v(x[6])) for x in EXTRA]
W = [{"w": w["w"], "a": v5(old_inv(w["a"])), "b": v5(old_inv(w["b"]))} for w in W4 if not any(a - 0.01 <= w["a"] < b - 0.01 for a, b in spans)]
for e in ED:
    st = v5(e["v2_a"])
    W += [{"w": w, "a": round(st + x - e["trim"][0], 3), "b": round(st + y - e["trim"][0], 3)} for w, x, y in e["words"]]
W.sort(key=lambda w: w["a"])

SR = 48000; O = Path("output/audio_stems_v5"); (O / "music").mkdir(parents=True, exist_ok=True)
run = lambda a: subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
F = 0.01   # 10 ms fade in/out at every joint
ins, fl, cur, k, n = ["-i", "output/audio_stems_v2/voice_full_timeline.wav"], [], 0.0, 0, 1
def piece(src, a, b, label, mono=False):
    d = b - a
    fades = (f",afade=t=in:d={F}" if a > 0 else "") + f",afade=t=out:st={max(0, d - F):.4f}:d={F}"
    return f"[{src}]atrim={a}:{b},asetpts=N/SR/TB,aresample={SR}{',aformat=channel_layouts=mono' if mono else ''}{fades}[{label}]"
for e in ED:
    fl.append(piece(0, cur, e["v2_a"], f"p{k}")); k += 1
    if e["file"]:
        ins += ["-i", e["file"]]; fl.append(piece(n, e["trim"][0], e["trim"][1], f"p{k}", True)); k += 1; n += 1
    cur = e["v2_b"]
fl.append(f"[0]atrim={cur},asetpts=N/SR/TB,aresample={SR},afade=t=in:d={F}[p{k}]"); k += 1
fl.append("".join(f"[p{i}]" for i in range(k)) + f"concat=n={k}:v=0:a=1,apad,atrim=0:{TOTAL}[o]")
run(ins + ["-filter_complex", ";".join(fl), "-map", "[o]", "-c:a", "pcm_s24le", str(O / "voice_full_timeline.wav")])
s0 = v5(m2["song_start"]); ms = int(round(s0 * 1000))
for nm in ("song_C1_full", "song_C1_vocals", "song_C1_music_only"):
    run(["-i", f"output/audio_stems_v1/music/{nm}.wav", "-af", f"aresample={SR},adelay={ms}|{ms},apad,atrim=0:{TOTAL}", "-c:a", "pcm_s24le", str(O / "music" / f"{nm}_timeline.wav")])
run(["-i", str(O / "voice_full_timeline.wav"), "-i", str(O / "music/song_C1_full_timeline.wav"), "-filter_complex",
     "[0]pan=stereo|c0=c0|c1=c0[v];[1]volume=-3dB[s];[v][s]amix=inputs=2:normalize=0,alimiter=limit=0.95[o]", "-map", "[o]", "-c:a", "pcm_s16le", str(O / "mix_rough_v5.wav")])
json.dump(W, open("work/words_v5.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump({"edits": ED, "total": TOTAL, "song_start_v4": s0}, open("work/timeline_v5.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("total", TOTAL, "song at", s0, [(e["sid"], e["delta"]) for e in ED])

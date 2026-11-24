"""Rough cut v2 = the REAL material on the v2 timeline (shotlist_v2 numbering kept).
- B shots  -> HeyGen avatar clips (assets/ai/heygen/avatar_clips_v1/avatar_<n>_<ch>.mp4)
- C shots  -> Higgsfield clips (assets/ai/higgsfield/clips_v1/clip_<n>_<ch>.mp4)
- D shots  -> Higgsfield "looks" of the Blender blockouts (901 jet / 902 lab / 903 bridge) where the chapter has one;
              in the song (C11) the D shots = a recap of the other worlds' clips (jet look first and last)
- E / F    -> the v1 placeholder card, but over the nearest real clip (blurred + dark) instead of a flat colour
The song (C1, 189.68 s) is 9.68 s longer than the [MUSIC 180] slot -> C11 shots are stretched, everything after
C11 is shifted by +9.68 s. Captions = the script words with their real Whisper times (shifted the same way);
during C11 = the song lines (Suno lyric alignment, work/song_C1_lines.json).
Media are hard-linked into motion-library/public/projects/aiworld/v2/ (no copy).
Writes work/props_rough_v2_720.json + work/rough_v2_map.json.  Usage (project folder): python -X utf8 work/scripts/make_props_v2.py"""
import json, os
from pathlib import Path

P = Path(__file__).resolve().parents[2]            # project folder
PUB = P.parents[1] / "motion-library" / "public" / "projects" / "aiworld" / "v2"
PUB.mkdir(parents=True, exist_ok=True)
tl = json.loads((P / "work/timeline_v2.json").read_text(encoding="utf-8"))
shots = json.loads((P / "work/shotlist_v2.json").read_text(encoding="utf-8"))
av = {x["n"]: x for x in json.loads((P / "assets/ai/heygen/avatar_clips_v1/avatar_clips_v1.json").read_text(encoding="utf-8"))}
hf = json.loads((P / "assets/ai/higgsfield/clips_v1/clips_v1.json").read_text(encoding="utf-8"))
lines = json.loads((P / "work/song_C1_lines.json").read_text(encoding="utf-8"))

SONG = 189.68
c11 = next(c for c in tl["chapters"] if c["id"] == "C11")
S0, S1 = c11["start"], c11["start"] + 180.0          # old music slot
EXTRA = round(SONG - 180.0, 3)
K = SONG / 180.0

def remap(t):                                        # old timeline time -> new
    if t <= S0: return t
    if t <= S1: return S0 + (t - S0) * K
    return t + EXTRA

def link(src: Path, name: str) -> str:
    dst = PUB / name
    if not dst.exists():
        os.link(src, dst)
    return f"projects/aiworld/v2/{name}"

def dur_of(n):
    return hf[str(n)]["dur"]

LOOK = {"C01": 901, "C05": 901, "C11": 901, "C02": 902, "C07": 902, "C02f": 903}
recap = [n for n in (6, 26, 99, 115, 162, 168, 192, 53, 117, 186) if str(n) in hf]   # other worlds, for the song
out, rmap, ri = [], [], 0
c11_d = [s["n"] for s in shots if s["chapter"] == "C11" and s["type"] == "D"]
for s in shots:
    a, b = remap(s["start"]), remap(s["start"] + s["dur"])
    s2 = {**s, "start": round(a, 3), "dur": round(b - a, 3), "cost": str(s["cost"])}
    src, clipdur, label = None, None, ""
    if s["type"] == "B":
        src = link(P / "assets/ai/heygen/avatar_clips_v1" / av[s["n"]]["file"], av[s["n"]]["file"]); clipdur = av[s["n"]]["dur"]; label = "HeyGen avatar"
    elif s["type"] == "C":
        f = hf[str(s["n"])]["file"]; src = link(P / "assets/ai/higgsfield/clips_v1" / f, f); clipdur = dur_of(s["n"]); label = hf[str(s["n"])]["model"]
    elif s["type"] == "D" and s["chapter"] == "C11":
        if s["n"] in (c11_d[0], c11_d[-1]): n = 901
        else: n = recap[ri % len(recap)]; ri += 1
        f = hf[str(n)]["file"]; src = link(P / "assets/ai/higgsfield/clips_v1" / f, f); clipdur = dur_of(n); label = "recap" if n != 901 else "Blender → look"
    elif s["type"] == "D" and s["chapter"] in LOOK:
        n = LOOK[s["chapter"]]; f = hf[str(n)]["file"]; src = link(P / "assets/ai/higgsfield/clips_v1" / f, f); clipdur = dur_of(n); label = "Blender → look"
    if src:
        s2["src"] = src; s2["label"] = label
        s2["rate"] = round(min(1.0, clipdur / s2["dur"]), 4) if clipdur else 1.0
    out.append(s2)
    rmap.append({"n": s["n"], "chapter": s["chapter"], "type": s["type"], "start": s2["start"], "dur": s2["dur"], "src": src, "label": label})

# the 0.6 s GAP between chapters has no shot (= black in the first render): each shot lasts until the next one starts
for x, nx in zip(out, out[1:]):
    old = x["dur"]; new = round(nx["start"] - x["start"], 3)
    if new > old:
        x["dur"] = new
        if x.get("rate"): x["rate"] = round(x["rate"] * old / new, 4)   # same clip fills the longer shot
# E/F (and D without a look): nearest real clip as a blurred background
real = [x for x in out if x.get("src") and x["type"] != "B"]
for x in out:
    if not x.get("src"):
        same = [r for r in real if r["chapter"] == x["chapter"]] or real
        r = min(same, key=lambda r: abs(r["start"] - x["start"]))
        x["bg"] = r["src"]

caps = []
for ch in tl["chapters"]:
    for seg in ch["segments"]:
        wt = seg.get("word_times") or []
        for i in range(0, len(wt), 6):
            g = wt[i:i + 6]
            caps.append({"a": round(remap(g[0][1]), 2), "b": round(remap(g[-1][2]), 2), "t": " ".join(w for w, _, _ in g)})
for ln in lines:
    caps.append({"a": round(S0 + ln["a"], 2), "b": round(S0 + ln["b"], 2), "t": ln["t"], "song": True})
caps.sort(key=lambda c: c["a"])
chs = []
for c in tl["chapters"]:
    st, en = remap(c["start"]), (S0 + SONG + 0.6 if c["id"] == "C11" else remap(c["end"]))
    chs.append({"id": c["id"], "title": c["title"], "start": round(st, 3), "end": round(en, 3)})
total = round(tl["total"] + EXTRA, 3)
last = out[-1]; old = last["dur"]; last["dur"] = round(total - last["start"], 3)   # last shot runs to the end
if last.get("rate"): last["rate"] = round(last["rate"] * old / last["dur"], 4)
props = {"fps": 25, "duration": total, "outW": 1280, "shots": out, "caps": caps, "chapters": chs}
(P / "work/props_rough_v2_720.json").write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
(P / "work/rough_v2_map.json").write_text(json.dumps({"song_start": S0, "extra": EXTRA, "total": total, "shots": rmap},
                                                      ensure_ascii=False, indent=1), encoding="utf-8")
print("shots", len(out), "real", sum(1 for x in out if x.get("src")), "caps", len(caps), "total", total, "extra", EXTRA)

"""v10 note 2: per avatar clip, measure the mouth vs the voice it was made from (tools/lipsync_lag.py, MediaPipe) and return a skip shift that brings
a clip whose sound clearly comes BEFORE the mouth (lag >= +120 ms, corr >= 0.3) back to the natural -80 ms. Cached in work/lipfix_v10.json."""
import json, os, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / "tools"))
PUB = pathlib.Path(__file__).resolve().parents[4] / "motion-library" / "public"
CACHE = "work/lipfix_v10.json"; _c = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
m2 = json.load(open("work/rough_v2_map.json", encoding="utf-8")); AVW = {x["n"]: x["start"] for x in m2["shots"] if x["type"] == "B"}
def shift(src):
    if src in _c: return _c[src]["shift"]
    m = re.search(r"avatar_(\d{3})_", src); sh = 0.0; info = {"lag": None}
    if m and int(m.group(1)) in AVW:
        from lipsync_lag import lag
        f = str(PUB / src)
        import subprocess
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout or 0)
        if d > 2.5:
            r = lag(f, 0.1, d - 0.2, "output/audio_stems_v2/voice_full_timeline.wav", AVW[int(m.group(1))] + 0.1)
            if r:
                info = {"lag": r[0], "corr": r[1]}
                if r[0] >= 120 and r[1] >= 0.3: sh = round((r[0] + 80) / 1000, 3)
    _c[src] = {**info, "shift": sh}; json.dump(_c, open(CACHE, "w"), indent=0)
    return sh

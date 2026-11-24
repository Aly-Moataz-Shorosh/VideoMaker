"""QA gates for rough cut v5: black frames, frozen picture (outside the song's held frames), and avatar lip-sync
(each avatar scene: the v4 voice under it vs the v2 voice the HeyGen clip was made from -> lag must be ~0).
Usage (project folder): python -X utf8 work/scripts/qa_v4.py"""
import json, re, subprocess
import numpy as np

V = "output/rough_cut_v5.mp4"
P = json.load(open("work/props_v5.json", encoding="utf-8")); T = json.load(open("work/timeline_v5.json", encoding="utf-8"))
def ff(args): return subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *args], capture_output=True, text=True, errors="ignore").stderr
log = ff(["-i", V, "-vf", "blackdetect=d=0.12:pix_th=0.06,freezedetect=n=0.002:d=0.8", "-an", "-f", "null", "-"])
black = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", log)
fs = re.findall(r"freeze_start: ([\d.]+)", log); fe = re.findall(r"freeze_end: ([\d.]+)", log)
print("black:", black or "none")
print("freeze >= 0.8 s:", list(zip(fs, fe)) or "none")

def wav(f):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
v4w, v2w = wav("output/audio_stems_v5/voice_full_timeline.wav"), wav("output/audio_stems_v2/voice_full_timeline.wav")
def to_v2(t):   # inverse of v4(): v4 time -> v2 time (outside removed pieces)
    d = 0.0
    for e in T["edits"]:
        if t >= e["v2_b"] + d + e["delta"] - 1e-6: d += e["delta"]
    return t - d
SR = 8000; worst = []
for s in P["scenes"]:
    if s["k"] != "AV" or not s["clips"] or "avatar_001" in s["clips"][0]["src"] or "look_S4g" in s["clips"][0]["src"]: continue
    a = s["start"] + 0.2; n = int(min(2.5, s["dur"] - 0.4) * SR)
    if n < SR: continue
    x = v4w[int(a * SR): int(a * SR) + n]; b0 = int(to_v2(a) * SR); best = (0, -1)
    for lag in range(-int(0.3 * SR), int(0.3 * SR) + 1, 8):
        y = v2w[b0 + lag: b0 + lag + n]
        if len(y) < n: continue
        c = float(np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-9))
        if c > best[1]: best = (lag, c)
    worst.append((round(s["start"], 1), round(best[0] / SR * 1000), round(best[1], 3)))
bad = [w for w in worst if abs(w[1]) > 40 or w[2] < 0.9]
print(f"lip-sync: {len(worst)} avatar scenes, lag ms max {max(abs(w[1]) for w in worst)}, bad {bad or 'none'}")

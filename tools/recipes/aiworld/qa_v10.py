"""QA gates for rough cut v10 (the delivered file itself): black frames, frozen picture, and LIP SYNC measured on the final picture
(MediaPipe mouth inside each talking circle / full-frame avatar vs the voice stem at the same seconds). Natural HeyGen = mouth ~80-120 ms
before the sound (negative). Flag: sound leads (lag > +40 ms) or mouth far ahead (< -200 ms).
Usage (project folder): python -X utf8 work/scripts/qa_v10.py"""
import json, re, subprocess, sys
sys.path.insert(0, "../../tools")
import lipsync_lag as LS

V = "output/rough_cut_v10.mp4"; VOICE = "output/audio_stems_v10/voice_full_timeline.wav"
P = json.load(open("work/props_v10.json", encoding="utf-8"))
log = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", V, "-vf", "blackdetect=d=0.12:pix_th=0.06,freezedetect=n=0.002:d=0.8", "-an", "-f", "null", "-"],
                     capture_output=True, text=True, errors="ignore").stderr
black = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", log)
fs = re.findall(r"freeze_start: ([\d.]+)", log); fe = re.findall(r"freeze_end: ([\d.]+)", log)
print("black:", black or "none")
print("freeze >= 0.8 s:", list(zip(fs, fe)) or "none")
# lip windows: every circle >= 6 s (crop the circle), every full-frame AV scene >= 6 s
wins = []
for f in P["faces"]:
    if f["dur"] < 6: continue
    c = f.get("circle")
    crop = f"{2 * c['r']}:{2 * c['r']}:{c['x'] - c['r']}:{c['y'] - c['r']}" if c else None
    wins.append((f["from"] + 0.5, min(f["dur"] - 1, 30), crop))
for s in P["scenes"]:
    if s["k"] == "AV" and s["dur"] >= 6: wins.append((s["start"] + 0.5, min(s["dur"] - 1, 30), None))
bad = []
for a, d, crop in sorted(wins):
    r = LS.lag(V, a, d, voice=VOICE, crop=crop)
    flag = "" if r is None or (-200 <= r[0] <= 40) or r[1] < 0.15 else "  <-- CHECK"
    if flag: bad.append((round(a, 1), r))
    print(f"{a:8.1f} {d:5.1f} {'circle' if crop else 'full  '} {r}{flag}")
print("lip windows:", len(wins), "| to check:", bad or "none")

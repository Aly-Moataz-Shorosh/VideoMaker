"""PICTURE vs SOUND lip-sync gate (Aly v9 note 2: «الصوت سابق الصورة» — qa_v9 only compared voice with voice).
For every place his face talks in the RENDERED video (AV scenes, face shots, circles, looks): find the face, take the mouth box, measure the mouth
motion per frame (frame difference) and cross-correlate it with the voice loudness of the final mix. lag > 0 = the mouth moves AFTER the sound.
Usage (project folder): python -X utf8 work/scripts/qa_lips_v10.py <video.mp4> <props.json> [voice.wav]"""
import json, subprocess, sys
import numpy as np, cv2
V, P = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8"))
VOICE = sys.argv[3] if len(sys.argv) > 3 else None
FPS = 25
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
def frames(a, d, box=None, scale=1.0):
    W, H = 960, 540
    vf = f"scale={W}:{H}"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", V, "-vf", vf, "-r", str(FPS), "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                         capture_output=True).stdout
    n = len(raw) // (W * H); return np.frombuffer(raw[: n * W * H], np.uint8).reshape(n, H, W)
def env(a, d):
    src = VOICE or V
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", src, "-ac", "1", "-ar", "8000", "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    hop = 8000 // FPS; e = np.array([np.sqrt((x[i:i + hop] ** 2).mean() + 1e-12) for i in range(0, len(x) - hop + 1, hop)])
    return np.diff(e, prepend=e[:1]).clip(0) + 0.3 * e   # onsets + level
def lag_of(a, d):
    F = frames(a, d)
    if len(F) < FPS * 2: return None
    faces = casc.detectMultiScale(F[len(F) // 2], 1.1, 5, minSize=(40, 40))
    if len(faces) == 0: return None
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    mb = F[:, y + int(h * 0.62): y + int(h * 0.95), x + int(w * 0.25): x + int(w * 0.75)].astype(np.float32)
    mot = np.abs(np.diff(mb, axis=0)).mean(axis=(1, 2)); mot = np.concatenate([[mot[0]], mot])
    e = env(a, d); n = min(len(e), len(mot)); e, mot = e[:n], mot[:n]
    e = (e - e.mean()) / (e.std() + 1e-9); mot = (mot - mot.mean()) / (mot.std() + 1e-9)
    best = (0, -9)
    for L in range(-12, 13):   # ±0.48 s
        if L >= 0: c = float(np.dot(e[: n - L], mot[L:]) / (n - L))
        else: c = float(np.dot(e[-L:], mot[: n + L]) / (n + L))
        if c > best[1]: best = (L, c)
    return round(best[0] * 1000 / FPS), round(best[1], 2)
out = []
for s in P["scenes"]:
    if s["k"] == "AV" and s["dur"] > 2.5: out.append(("AV", s["start"], min(8, s["dur"])))
for f in P.get("faces", []):
    if f["dur"] > 2.5: out.append(("face" + ("-circle" if f.get("circle") else ""), f["from"], f["dur"]))
res = []
for kind, a, d in out:
    r = lag_of(a + 0.2, d - 0.4)
    res.append((kind, round(a, 1), r)); print(kind, round(a, 1), r)
bad = [x for x in res if x[2] and x[2][1] > 0.15 and abs(x[2][0]) >= 80]
print("SUSPECT (|lag| >= 80 ms with a clear correlation):", bad)

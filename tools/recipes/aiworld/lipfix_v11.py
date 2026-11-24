"""v10 notes 1/2: lip sync of every avatar clip by its OWN SOUND. A HeyGen clip's audio track is exactly what its mouth says, so the clip is
in sync when its audio lines up with the video's voice at the same seconds. Cross-correlate the two loudness curves (10 ms steps) and return
the skip correction (v10's mouth-measure shifted avatar_015 by 0.48 s by mistake -> wrong lips at 1:25 + a frozen tail at 1:29).
Also `length(src)` for the general «never ask a clip past its end» check. Cache: work/lipfix_v11.json."""
import json, os, subprocess, pathlib
import numpy as np
PUB = pathlib.Path(__file__).resolve().parents[4] / "motion-library" / "public"
CACHE = "work/lipfix_v11.json"; _c = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
VOICE = "output/audio_stems_v11/voice_full_timeline.wav"
def _env(f, a, d):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, a):.3f}", "-t", f"{d:.3f}", "-i", str(f), "-ac", "1", "-ar", "8000", "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    return np.array([np.sqrt((x[i:i + 80] ** 2).mean() + 1e-12) for i in range(0, len(x) - 80 + 1, 80)])
def length(src):
    k = "len:" + src
    if k not in _c:
        _c[k] = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(PUB / src)], capture_output=True, text=True).stdout or 0)
        json.dump(_c, open(CACHE, "w"), indent=0)
    return _c[k]
def correction(src, skip, t_from, dur):
    """seconds to ADD to skip so the clip's own audio lines up with the video's voice (0 if the clip has no clear audio match)"""
    k = f"{src}|{skip:.3f}|{t_from:.3f}|{dur:.3f}"
    if k in _c: return _c[k]["fix"]
    a = _env(PUB / src, skip, dur); b = _env(VOICE, t_from, dur); n = min(len(a), len(b)); fix, c = 0.0, None
    if n > 100 and a[:n].std() > 1e-4:
        a, b = (a[:n] - a[:n].mean()) / a[:n].std(), (b[:n] - b[:n].mean()) / (b[:n].std() + 1e-9)
        best = max(range(-60, 61), key=lambda L: float(np.dot(a[max(0, L):n + min(0, L)], b[max(0, -L):n - max(0, L)])) / (n - abs(L)))
        c = float(np.dot(a[max(0, best):n + min(0, best)], b[max(0, -best):n - max(0, best)])) / (n - abs(best))
        if c >= 0.6 and best != 0: fix = round(best * 0.01, 3)   # clip sound at index i+L matches voice at i -> show the clip L later
    _c[k] = {"fix": fix, "corr": None if c is None else round(c, 2)}; json.dump(_c, open(CACHE, "w"), indent=0)
    return fix

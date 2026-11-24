"""v10 note 42: where is his face in a circle source? MediaPipe face landmarks on one frame -> (fx, fy) = face centre as a fraction of the 1920x1080 frame.
Cached in work/face_center_v10.json. Used by make_props_v10 so every circle shows his face in the middle."""
import json, os, subprocess, sys, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / "tools"))
PUB = pathlib.Path(__file__).resolve().parents[4] / "motion-library" / "public"
CACHE = "work/face_center_v10.json"; _c = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def center(src, skip=0.0):
    if src in _c: return tuple(_c[src])
    if not (PUB / src).exists(): return 0.5, 0.42   # not there yet: do not cache
    from lipsync_lag import _landmarker
    import mediapipe as mp
    W, H = 960, 540
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{skip + 0.5:.2f}", "-i", str(PUB / src), "-frames:v", "1", "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fx, fy = 0.5, 0.42
    if len(r) == W * H * 3:
        res = _landmarker().detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.frombuffer(r, np.uint8).reshape(H, W, 3).copy()))
        if res.face_landmarks:
            L = res.face_landmarks[0]; xs = [p.x for p in L]; ys = [p.y for p in L]
            fx, fy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2 + 0.03   # a bit below the eyes = the face middle incl. the chin
    _c[src] = [round(fx, 3), round(fy, 3)]; json.dump(_c, open(CACHE, "w"), indent=0)
    return fx, fy

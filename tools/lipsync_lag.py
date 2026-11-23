"""Measure lips vs sound (mouth opening from face landmarks vs voice loudness). lag > 0 = the mouth moves AFTER the sound (sound leads).
Usage: python tools/lipsync_lag.py <video> <start> <dur> [voice_audio_file]   (or import lag())
Model: ~/ai-models/face_landmarker.task (MediaPipe, official Google file)."""
import subprocess, sys, pathlib
import numpy as np, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
FPS, W, H = 25, 640, 360
_lm = None
def _landmarker():
    global _lm
    if _lm is None:
        opt = vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=str(pathlib.Path.home() / "ai-models" / "face_landmarker.task")),
                                           running_mode=vision.RunningMode.IMAGE, num_faces=1)
        _lm = vision.FaceLandmarker.create_from_options(opt)
    return _lm
def frames(v, a, d, crop=None):
    vf = (f"crop={crop}," if crop else "") + f"scale={W}:{H},fps={FPS}"
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a}", "-t", f"{d}", "-i", v, "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    k = len(r) // (W * H * 3); return np.frombuffer(r[: k * W * H * 3], np.uint8).reshape(k, H, W, 3)
def env(v, a, d):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a}", "-t", f"{d}", "-i", v, "-ac", "1", "-ar", "8000", "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    hop = 8000 // FPS; return np.array([np.sqrt((x[i:i + hop] ** 2).mean() + 1e-12) for i in range(0, len(x) - hop + 1, hop)])
def mouth(F):
    lm = _landmarker(); o = []
    for f in F:
        r = lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(f)))
        if not r.face_landmarks: o.append(np.nan); continue
        L = r.face_landmarks[0]; o.append(abs(L[13].y - L[14].y) / (abs(L[10].y - L[152].y) + 1e-6))
    o = np.array(o)
    if np.isnan(o).all(): return None
    o[np.isnan(o)] = np.nanmean(o); return o
def lag(v, a, d, voice=None, voice_a=None, crop=None):
    m = mouth(frames(v, a, d, crop))
    if m is None: return None
    e = env(voice or v, a if voice_a is None else voice_a, d); n = min(len(m), len(e)); m, e = m[:n], e[:n]
    m = (m - m.mean()) / (m.std() + 1e-9); e = (e - e.mean()) / (e.std() + 1e-9); best = (0, -9)
    for L in range(-10, 11):
        c = float(np.dot(e[: n - L], m[L:]) / (n - L)) if L >= 0 else float(np.dot(e[-L:], m[: n + L]) / (n + L))
        if c > best[1]: best = (L, c)
    return best[0] * 1000 // FPS, round(best[1], 2)
if __name__ == "__main__":
    print(lag(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else None))

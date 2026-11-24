"""3 short examples of Aly in studio S4g on the same 5.6 s line (Aly 2026-11-21):
  real = his real avatar pixels (RVM cut-out, low feather) + colours of HOW HE LOOKS in the generated S4g still
  mix  = his real pixels + the generated still's low-frequency LIGHT (light map), so the room's light is on his real face
(the 'generated' example = HeyGen look of S4g, rendered by HeyGen, downloaded separately)
Usage (project folder): python -X utf8 work/scripts/studio_examples.py"""
import glob, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "work/scripts")
from studio_comp import comp, load_plate, _blur, _lab_stats

L = "assets/ai/heygen/look_S4g/"
frames = sorted(glob.glob(L + "frames_rgba/*.png"))
f0 = np.asarray(Image.open(frames[0]).convert("RGBA")).astype(np.float32) / 255
H, W = f0.shape[:2]
plate = load_plate("assets/ai/higgsfield/studio_look_v2/plate_S4g_empty.png", W, H)
gen = np.asarray(Image.open("assets/ai/higgsfield/studio_look_v2/gen_S4g_nefertari_mashrabiya.png").convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.float32) / 255
src = np.asarray(Image.open("assets/ai/higgsfield/studio_look_v1/src_avatar001_2s.png").convert("RGB")).astype(np.float32) / 255
ref_a = np.asarray(Image.open("assets/ai/higgsfield/studio_look_v1/matte_avatar001_2s.png").convert("RGBA")).astype(np.float32)[..., 3] / 255
# how he looks in the generated room (his region of the generated still)
target = _lab_stats(gen, ref_a)
# light map: generated light / real light, low frequency only, inside him
lm = (_blur(gen * ref_a[..., None], 45) + 1e-3) / (_blur(src * ref_a[..., None], 45) + 1e-3)
lm = np.clip(lm, 0.55, 1.6)
# brightness of the generated light fully, its colour only 25% (a red lantern cast on one cheek looked wrong)
lum = lm.mean(-1, keepdims=True); lm = lum + (lm - lum) * 0.25
lm = lm * _blur(ref_a, 45)[..., None] + (1 - _blur(ref_a, 45)[..., None])   # fade to 1 outside him

def enc(name, fn):
    out = f"{L}ex_{name}.mp4"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "25", "-i", "-",
                          "-i", L + "voice_S001_0-5.59.wav", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac",
                          "-b:a", "192k", "-shortest", out], stdin=subprocess.PIPE)
    for i, f in enumerate(frames):
        fg = np.asarray(Image.open(f).convert("RGBA")).astype(np.float32) / 255
        p.stdin.write((fn(fg, i) * 255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait(); print("ok", out)

if "--mix-only" not in sys.argv: enc("real", lambda fg, i: comp(fg, plate, seed=i, feather=0.35, erode=0.35, wrap=0.12, rim=0.35, grade=0.7, target=target))
enc("mix", lambda fg, i: comp(fg, plate, seed=i, feather=0.35, erode=0.35, wrap=0.12, rim=0.25, grade=0.35, target=target, lightmap=lm, key_strength=0.0))

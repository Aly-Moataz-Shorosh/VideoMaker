"""Small assets for rough cut v7 (Aly's v6 notes 13, 14, 18): his face logo with the WHOLE chin, his REAL room take (what the twin was
made from), and a «Video Agent» style cut = cinematic shots + his avatar. Free (local ffmpeg / Pillow), nothing generated.
Usage (project folder): python -X utf8 work/scripts/prep_v7_assets.py"""
import subprocess
from pathlib import Path
from PIL import Image

O = Path("assets/v7"); O.mkdir(parents=True, exist_ok=True)
# note 18: face logo cut at 805 px (v6 cut at 783 = under the chin), transparent around it
pp = Image.open("assets/v6/logo_pp2.png").convert("RGBA")
pp.crop((250, 75, 810, 806)).save(O / "logo_face_full.png")

def ff(*a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
# note 14: the twin = made from a short REAL take of him in his room (training clip, 6 s, muted)
ff("-ss", "20", "-t", "6", "-i", "../2026-11-20 avatar avatarTest/input/avatar_training_150s.mp4", "-an", "-vf", "scale=960:-2,fps=25",
   "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", str(O / "real_room_take_6s.mp4"))
# note 14: Video Agent = an idea -> cinematic shots mixed with the avatar (jet over Cairo -> his avatar -> the market)
CL = "assets/ai/higgsfield/clips_v1/"
parts = [(CL + "clip_183_C11.mp4", 0.3, 2.0), ("assets/ai/heygen/avatar_clips_v2_gen/avatar_012_C02.mp4", 0.5, 2.2), (CL + "clip_029_C02b.mp4", 0.3, 2.0)]
ins, fl = [], []
for i, (f, s, d) in enumerate(parts):
    ins += ["-ss", str(s), "-t", str(d), "-i", f]
    fl.append(f"[{i}:v]scale=960:540:force_original_aspect_ratio=increase,crop=960:540,fps=25,setsar=1[v{i}]")
fl.append("".join(f"[v{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[o]")
ff(*ins, "-filter_complex", ";".join(fl), "-map", "[o]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", str(O / "video_agent_mix.mp4"))
print("ok", sorted(p.name for p in O.iterdir()))

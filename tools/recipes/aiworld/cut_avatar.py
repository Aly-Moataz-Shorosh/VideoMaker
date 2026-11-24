"""Cut the one long HeyGen avatar video (all B shots back-to-back, 0.4 s gaps) into one clip per shot.
Input : assets/ai/heygen/avatar_B_shots_v1.mp4 + avatar_B_shots_v1.json (avatar_in / dur per shot)
Output: assets/ai/heygen/avatar_clips_v1/avatar_<shot>_<chapter>.mp4 (1920x1080, 25 fps, with the voice) + index json.
Usage (project folder): python -X utf8 work/scripts/cut_avatar.py"""
import json, subprocess
from pathlib import Path

src = "assets/ai/heygen/avatar_B_shots_v1.mp4"
meta = json.load(open("assets/ai/heygen/avatar_B_shots_v1.json", encoding="utf-8"))
out = Path("assets/ai/heygen/avatar_clips_v1"); out.mkdir(parents=True, exist_ok=True)
idx = []
for p in meta["parts"]:
    f = out / f"avatar_{p['n']:03d}_{p['chapter']}.mp4"
    if not f.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{p['avatar_in']:.3f}", "-i", src, "-t", f"{p['dur']:.3f}",
                        "-vf", "scale=1920:1080,fps=25", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                        "-c:a", "aac", "-b:a", "192k", str(f)], check=True)
    idx.append({**p, "file": f.name})
json.dump(idx, open(out / "avatar_clips_v1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(idx), "clips")

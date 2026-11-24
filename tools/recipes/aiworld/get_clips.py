"""Download finished Higgsfield clips -> assets/ai/higgsfield/clips_v1/clip_<shot>_<chapter>.mp4 (+ clips_v1.json).
Usage (project folder): python -X utf8 work/scripts/get_clips.py <index>=<hf_stamp_jobid> ...   (adds to the json, skips existing files)"""
import json, subprocess, sys, urllib.request
from pathlib import Path

U = "https://d8j0ntlcm91z4.cloudfront.net/user_3IGG8sowIvVZvoQJxwgFTvKY4uu/hf_20261120_"
D = Path("assets/ai/higgsfield/clips_v1"); D.mkdir(parents=True, exist_ok=True)
J = D / "clips_v1.json"
meta = json.load(open(J, encoding="utf-8")) if J.exists() else {}
req = {r["index"]: r for r in json.load(open("work/clips_v1.json", encoding="utf-8"))["requests"]}
NAMES = {901: "look_jet", 902: "look_lab", 903: "look_bridge"}
for arg in sys.argv[1:]:
    i, stamp = arg.split("=", 1); i = int(i)
    name = f"clip_{i:03d}_{req[i]['chapter']}.mp4" if i in req else f"{NAMES[i]}.mp4"
    f = D / name
    if not f.exists():
        urllib.request.urlretrieve(U + stamp + ".mp4", f)
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                        "-show_entries", "format=duration", "-of", "json", str(f)], capture_output=True, text=True).stdout
    pr = json.loads(p)
    st = pr["streams"][0]
    meta[str(i)] = {"file": name, "url": U + stamp + ".mp4", "job_id": stamp.split("_", 1)[1],
                    "w": st["width"], "h": st["height"], "fps": st["r_frame_rate"], "dur": round(float(pr["format"]["duration"]), 3),
                    "model": req[i]["params"]["model"] if i in req else "kling_video_edit",
                    "cost": req[i]["cost"] if i in req else 12, "keyframe": req[i]["keyframe"] if i in req else None,
                    "shot_dur": req[i]["shot_dur"] if i in req else None, "prompt": req[i]["params"]["prompt"] if i in req else None}
json.dump(meta, open(J, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(meta), "clips;", round(sum(v["cost"] for v in meta.values()), 2), "credits")

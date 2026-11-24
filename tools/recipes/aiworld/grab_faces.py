"""Grab full-quality face frames of Aly from his recent public YouTube videos (stream, no download) + local CTA clip.
Writes assets/ai/higgsfield/refs/recent/<name>.jpg and one small check sheet work/recent_faces_sheet.jpg.
Usage (project folder): python -X utf8 work/scripts/grab_faces.py"""
import subprocess, sys
from pathlib import Path
from PIL import Image

OUT = Path("assets/ai/higgsfield/refs/recent"); OUT.mkdir(parents=True, exist_ok=True)
CTA = Path("../../brand/clips/cta_comment_youtube_9x16.mp4")
# (youtube id, [fractions of duration])  — close-up CTA endings + the Figma Make talk
YT = [("3tSeDjpQ2ko", [0.93, 0.965, 0.99]), ("Z_gxTH0KV-Y", [0.80, 0.88, 0.95]), ("wz-Z9F7lNYw", [0.25, 0.6, 0.97])]


def grab(src, t, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", "-q:v", "2", str(out)], check=True)


files = []
for vid, fr in YT:
    info = subprocess.run([sys.executable, "-m", "yt_dlp", "--js-runtimes", "node", "-f", "bv[height<=1920][ext=mp4]/bv/b", "-g",
                           "--print", "duration", f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True).stdout.split("\n")
    dur, url = float(info[0]), info[1]
    for i, f in enumerate(fr):
        p = OUT / f"{vid}_{i}.jpg"; grab(url, dur * f, p); files.append(p)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(CTA)],
                           capture_output=True, text=True).stdout)
for i, f in enumerate([0.15, 0.5, 0.85]):
    p = OUT / f"cta_{i}.jpg"; grab(str(CTA), dur * f, p); files.append(p)
ims = [Image.open(p).convert("RGB") for p in files]
th = []
for im in ims:
    im.thumbnail((200, 356)); c = Image.new("RGB", (200, 356)); c.paste(im, ((200 - im.width) // 2, (356 - im.height) // 2)); th.append(c)
g = Image.new("RGB", (200 * 6, 356 * 2))
for i, c in enumerate(th):
    g.paste(c, ((i % 6) * 200, (i // 6) * 356))
g.save("work/recent_faces_sheet.jpg", quality=85)
for p, im in zip(files, ims):
    print(p.name, im.size)

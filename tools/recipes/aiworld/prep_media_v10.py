"""Prepare every media file the v10 boards use (Aly's v9 notes) -> assets/v10/ . Usage (project folder): python -X utf8 work/scripts/prep_media_v10.py"""
import subprocess, os, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
O = Path("assets/v10"); O.mkdir(parents=True, exist_ok=True)
R = "D:/Temp/v10_refs/"; H9 = "assets/ai/heygen/v9/"; H10 = "assets/ai/heygen/v10/"; CL = "../../motion-library/public/projects/aiworld/v6/clips/"
def ff(*a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
def cut(src, a, d, out, vf=None, audio=False):
    ff("-ss", str(a), "-i", src, "-t", str(d), *(["-vf", vf] if vf else []), "-c:v", "libx264", "-crf", "19", "-preset", "fast", "-r", "25",
       *(["-c:a", "aac"] if audio else ["-an"]), str(O / out))
# note 18/29/37: reference clips from the web (muted, short, with their source shown on screen)
cut(R + "OWpr7jEFV68.mp4", 3, 10, "cowork_luke.mp4")
cut(R + "IUtt1DKrpQg.mp4", 76, 15, "blender_mcp_build.mp4")
cut(R + "rckZwwjdLRA.mp4", 40, 12, "blender_mcp_timelapse.mp4")
cut(R + "V7CtHz8JFWA.mp4", 596, 12, "davinci_mcp.mp4")
cut(R + "eThBPaL37Ac.mp4", 0, 9, "playmobil_short.mp4")
Image.open(R + "eThBPaL37Ac.jpg").convert("RGB").save(O / "playmobil_thumb.jpg")
cut("assets/v10/web/gsplat_garden.mp4", 0, 9, "gsplat_garden.mp4", "scale=1280:-2")
cut("assets/v10/web/genjutsu_hero.mp4", 0, 9, "genjutsu_official.mp4", "scale=1280:-2")
cut("assets/v10/web/claude_chrome_official.webm", 0, 10, "claude_chrome_official.mp4")
cut("assets/v10/web/cowork_official.webm", 0, 10, "cowork_official.mp4")
# note 37: his content-creation skill — crop away the left sidebar (private chat titles)
cut("input/skill content creation.mp4", 0, 13.5, "skill_content.mp4", "crop=1640:1080:280:0,scale=1280:-2")
# notes 30/36: his phone recordings (vertical, muted)
for k, f in enumerate(["input/WhatsApp Video 2026-11-23 at 7.09.03 PM.mp4", "input/WhatsApp Video 2026-11-23 at 7.09.17 PM.mp4"]):
    cut(f, 0, 20, f"browser_auto_{k}.mp4", "scale=478:850")
for k, f in enumerate(["input/scripts/WhatsApp Video 2026-11-23 at 7.11.54 PM.mp4", "input/scripts/WhatsApp Video 2026-11-23 at 7.11.541 PM.mp4",
                       "input/scripts/WhatsApp Video 2026-11-23 at 7.11.5411 PM.mp4"]):
    cut(f, 0, 20, f"script_rec_{k}.mp4", "scale=478:850")
# note 5: the WHOLE Genjutsu reel (crop of his screen recording, as in v8)
cut("assets/v8/genjutsu_reel.mp4", 0, 16, "genjutsu_reel_full.mp4")
# note 10: lip sync — blue room BEFORE = the still photo; AFTER = the lip-synced clip (crop the white bars)
Image.open("../2026-11-20 avatar avatarTest/input/avatar_photo_blue_room.png").convert("RGB").save(O / "blueroom_photo.jpg")
ff("-i", H10 + "blueroom_after_v10.mp4", "-vf", "crop=1080:608:0:656,scale=1280:-2", "-c:v", "libx264", "-crf", "18", "-an", str(O / "blueroom_after.mp4"))
ff("-i", H10 + "realroom_src_v10.mp4", "-vf", "scale=1280:-2", "-c:v", "libx264", "-crf", "18", "-an", str(O / "realroom_before.mp4"))
ff("-i", H10 + "realroom_after_v10.mp4", "-vf", "scale=1280:-2", "-c:v", "libx264", "-crf", "18", "-an", str(O / "realroom_after.mp4"))
# note 6: three real demos from our own clip 026
src = CL + "clip_026_C02b.mp4"
ff("-i", src, "-t", "4", "-vf", "fps=5,fps=25,scale=640:-2", "-an", "-c:v", "libx264", "-crf", "20", str(O / "frames_choppy.mp4"))
ff("-i", src, "-t", "4", "-vf", "fps=5,minterpolate=fps=25:mi_mode=mci:mc_mode=aobmc:vsbmc=1,scale=640:-2", "-an", "-c:v", "libx264", "-crf", "20", str(O / "frames_smooth.mp4"))
ff("-ss", "2", "-i", src, "-frames:v", "1", str(O / "_f.png"))
fr = Image.open(O / "_f.png").convert("RGB"); W, H = fr.size
low = fr.resize((W // 10, H // 10), Image.BILINEAR).resize((W, H), Image.NEAREST); low.save(O / "upscale_before.jpg"); fr.save(O / "upscale_after.jpg")
# «تطويل»: a film strip of the clip (5 real frames) + 5 new frames after it (the same shot going on), the new part outlined in gold
fs = []
for k in range(10):
    ff("-ss", str(0.2 + k * 0.48), "-i", src, "-frames:v", "1", "-vf", "scale=240:-2", str(O / f"_s{k}.png")); fs.append(Image.open(O / f"_s{k}.png").convert("RGB"))
sw, sh = fs[0].size; strip = Image.new("RGB", (sw * 10 + 22 * 9 + 40, sh + 80), (12, 14, 30)); d = ImageDraw.Draw(strip)
for k, im in enumerate(fs):
    x = 20 + k * (sw + 22); strip.paste(im, (x, 40))
    if k >= 5: d.rectangle((x - 4, 36, x + sw + 4, 40 + sh + 4), outline=(233, 185, 73), width=5)
strip.save(O / "extend_strip.jpg"); [os.remove(O / f"_s{k}.png") for k in range(10)]; os.remove(O / "_f.png")
print("media ready:", sorted(p.name for p in O.iterdir() if p.is_file()))

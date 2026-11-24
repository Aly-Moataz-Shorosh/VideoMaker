"""More v10 media: styles strip (note 35/39), versions strip of the real rough cuts (39), transparent motion over a checkerboard (46),
Whisper / faster-whisper card (20), Suno version list (53). Usage (project folder): python -X utf8 work/scripts/prep_media_v10b.py"""
import json, subprocess, glob, os
from pathlib import Path
from PIL import Image, ImageDraw
O = Path("assets/v10")
def ff(*a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
# styles strip: the real covers of the numbered styles
covers = sorted(glob.glob("../../styles/*/cover.jpg"))[:20]
th = [Image.open(c).convert("RGB").resize((320, 180)) for c in covers]
st = Image.new("RGB", (5 * 330 + 10, 4 * 190 + 10), (12, 14, 30))
for i, im in enumerate(th): st.paste(im, (10 + (i % 5) * 330, 10 + (i // 5) * 190))
st = st.resize((1440, int(st.height * 1440 / st.width))); st.save("../../styles/styles_strip_v10.jpg", quality=88)
# versions strip: one frame of every real rough cut v1..v9 (+ v10 label)
vs = []
for k in range(1, 10):
    f = f"output/rough_cut_v{k}.mp4"
    if not os.path.exists(f): f = "D:/Temp/v9_first_render/rough_cut_v9.mp4" if k == 9 else None
    if not f or not os.path.exists(f): continue
    ff("-ss", "95", "-i", f, "-frames:v", "1", "-vf", "scale=320:180", str(O / f"_v{k}.png")); vs.append((k, Image.open(O / f"_v{k}.png").convert("RGB")))
cols = 5; W = cols * 340 + 20; H = ((len(vs) + 1 + cols - 1) // cols) * 230 + 20
vt = Image.new("RGB", (W, H), (12, 14, 30)); d = ImageDraw.Draw(vt)
for i, (k, im) in enumerate(vs + [(10, None)]):
    x, y = 20 + (i % cols) * 340, 20 + (i // cols) * 230
    if im: vt.paste(im, (x, y))
    else: d.rectangle((x, y, x + 320, y + 180), outline=(233, 185, 73), width=6)
    d.rectangle((x, y + 184, x + 110, y + 220), fill=(233, 185, 73)); d.text((x + 10, y + 190), f"v{k}", fill=(10, 10, 10))
vt.save(O / "versions_strip.jpg", quality=88); [os.remove(O / f"_v{k}.png") for k, _ in vs]
# transparent motion over a checkerboard (a REAL alpha layer of this project)
lay = "output/layers_alpha_v1/card_C00.webm"
ff("-f", "lavfi", "-i", "color=c=0xd8d8d8:s=640x360:d=6", "-f", "lavfi", "-i", "color=c=0xa8a8a8:s=640x360:d=6",
   "-c:v", "libvpx-vp9", "-i", lay, "-filter_complex",
   "[0][1]blend=all_expr='if(eq(mod(floor(X/40)+floor(Y/40),2),0),A,B)'[ck];[2]scale=640:360[l];[ck][l]overlay=0:0:shortest=1",
   "-t", "6", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", str(O / "checker_motion.mp4"))
# Whisper card = the real faster-whisper repo header (the tool we run on the PC)
im = Image.open(O / "web/faster_whisper.png").convert("RGB"); w, h = im.size
im.crop((int(w * 0.12), int(h * 0.12), int(w * 0.72), int(h * 0.42))).resize((800, 400)).save(O / "web/faster_whisper_card.png")
# Suno: the real takes (1 call = 2 songs = 10 credits; 40 credits = 8 takes) — docs/33 2026-11-20
json.dump([{"label": "نسخة A"}, {"label": "نسخة B"}, {"label": "مكس: B بالاد ← A تراب (1)"}, {"label": "مكس (2)"},
           {"label": "تصحيح النطق (1)"}, {"label": "تصحيح النطق (2)"}, {"label": "8 نسخ = 40 كريدت"}, {"label": "النهائية", "final": True}],
          open("work/song_versions_v10.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ok", len(covers), "covers,", len(vs), "versions")

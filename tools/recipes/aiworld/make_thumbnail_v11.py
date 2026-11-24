"""Thumbnail of «عالم الـ AI كله» (Aly 2026-11-24: «اعمل ال thumbnail»). His REAL face (the studio twin frame from the v11 batch, RVM cut-out:
tools/matte.py --png) — no image model redraws him. HTML page -> headless Chrome screenshot (Arabic shaping + SVG logos) -> 1280x720 JPG.
Two versions = the first two titles in output/rough_cut_v11.txt. Usage (project folder): python -X utf8 work/scripts/make_thumbnail_v11.py"""
import random, subprocess, pathlib
PRJ = pathlib.Path.cwd(); VM = PRJ.parents[1]
CHROME = VM / "motion-library/node_modules/.remotion/chrome-headless-shell/win64/chrome-headless-shell-win64/chrome-headless-shell.exe"
LOG = VM / "brand/logos-tools"; FONT = (VM / "motion-library/public/fonts/Cairo.ttf").as_uri(); MONT = (VM / "motion-library/public/fonts/Montserrat.ttf").as_uri()
ALY = pathlib.Path("D:/Temp/thumb/aly_cut.png").as_uri()
LOGOS = ["claude.svg", "chatgpt.png", "heygen.ico", "elevenlabs.png", "higgsfield.png", "suno.png", "gemini.png", "kling.png", "blender.svg", "remotion.png", "cursor.png"]
# logos on an arc around his head (right half), big enough to read at thumbnail size
import math   # an oval around his head (centre 965,330), clear of the text block (x <= 600) and inside the frame
ARC = [(round(945 + 268 * math.cos(math.radians(a))), round(330 + 252 * math.sin(math.radians(a)))) for a in (200, 228, 256, 284, 312, 340, 8)]
LOGOS = LOGOS[:7]   # the 8th sat behind his shoulder
random.seed(7)
stars = "".join(f'<div class="st" style="left:{random.randint(0, 1270)}px;top:{random.randint(0, 710)}px;opacity:{random.uniform(.15, .45):.2f};font-size:{random.randint(14, 26)}px">✱</div>' for _ in range(70))
def page(l1, l2, badge):
    logos = "".join(f'<div class="lg" style="left:{x - 44}px;top:{y - 44}px"><img src="{(LOG / f).as_uri()}"></div>' for f, (x, y) in zip(LOGOS, ARC))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Cairo;src:url('{FONT}');font-weight:200 1000}}
@font-face{{font-family:Mont;src:url('{MONT}');font-weight:100 900}}
html,body{{margin:0;width:1280px;height:720px;overflow:hidden}}
body{{background:radial-gradient(circle at 74% 45%,#2a3b7a 0%,#14204a 38%,#070c1f 80%);position:relative;font-family:Cairo}}
.st{{position:absolute;color:#e8b54a}}
.glow{{position:absolute;left:640px;top:40px;width:640px;height:640px;border-radius:50%;background:radial-gradient(circle,rgba(232,181,74,.55),rgba(232,181,74,0) 65%)}}
.ring{{position:absolute;left:705px;top:65px;width:520px;height:520px;border-radius:50%;border:6px solid rgba(232,181,74,.85);box-shadow:0 0 40px rgba(232,181,74,.6)}}
.lg{{position:absolute;width:88px;height:88px;border-radius:22px;background:#fbf7ee;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(0,0,0,.55);border:3px solid #fff}}
.lg img{{width:64%;height:64%;object-fit:contain}}
.aly{{position:absolute;left:560px;top:118px;height:640px}}
.t{{position:absolute;left:24px;top:18px;width:560px;text-align:right;direction:rtl}}
.l1{{font-weight:1000;font-size:118px;line-height:1.05;color:#ffd23f;-webkit-text-stroke:6px #0b1020;paint-order:stroke fill;text-shadow:0 10px 0 #0b1020,0 14px 30px rgba(0,0,0,.6)}}
.l2{{font-weight:900;font-size:64px;line-height:1.15;color:#fff;-webkit-text-stroke:5px #0b1020;paint-order:stroke fill;text-shadow:0 8px 0 #0b1020;margin-top:6px}}
.badge{{position:absolute;left:40px;bottom:46px;transform:rotate(-3deg);background:#e0312e;color:#fff;font-weight:900;font-size:36px;padding:4px 22px 10px;white-space:nowrap;border-radius:14px;
        border:5px solid #fff;box-shadow:0 10px 24px rgba(0,0,0,.6);direction:rtl}}
</style></head><body>{stars}<div class="glow"></div><div class="ring"></div>{logos}<img class="aly" src="{ALY}">
<div class="t"><div class="l1">{l1}</div><div class="l2">{l2}</div></div><div class="badge">{badge}</div></body></html>"""
OUT = PRJ / "output"
for name, (l1, l2, badge) in {"A": ("عالم الـ AI", "كله في فيديو واحد", "والفيديو نفسه معمول بالـ AI"),
                              "B": ("مفيش كاميرا!", "الفيديو ده كله AI", "عالم الـ AI كله في 27 دقيقة")}.items():
    h = pathlib.Path(f"D:/Temp/thumb/thumb_{name}.html"); h.write_text(page(l1, l2, badge), encoding="utf-8")
    png = pathlib.Path(f"D:/Temp/thumb/thumb_{name}.png")
    subprocess.run([str(CHROME), "--headless", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files", "--force-device-scale-factor=1",
                    f"--screenshot={png}", "--window-size=1280,720", h.as_uri()], check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(png), "-q:v", "2", str(OUT / f"thumbnail_v11_{name}.jpg")], check=True)
    print("ok", name)

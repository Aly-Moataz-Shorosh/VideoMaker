"""Behind-the-scenes cards from REAL project files (editor look) -> work/bts/*.png, + a sheet of the 20 style covers.
No secrets: .mcp.json has only public server URLs. Usage (project folder): python -X utf8 work/scripts/make_bts_cards.py"""
import json, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

O = Path("work/bts"); O.mkdir(parents=True, exist_ok=True)
VM = Path("../..").resolve()
MONO = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 30)
AR = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 30)   # has the Arabic presentation forms (Cairo lacks some)
try:
    from arabic_reshaper import reshape; from bidi.algorithm import get_display
    fix = lambda s: get_display(reshape(s))
except Exception:
    fix = lambda s: s

def card(name, title, lines, arabic=False):
    W, H = 1600, 900
    im = Image.new("RGB", (W, H), (14, 18, 32)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 56), fill=(26, 32, 54))
    for i, c in enumerate([(255, 90, 110), (245, 196, 81), (76, 211, 122)]): d.ellipse((24 + i * 30, 20, 40 + i * 30, 36), fill=c)
    d.text((140, 12), title, fill=(200, 205, 220), font=MONO)
    y = 80
    for ln in lines[:22]:
        if arabic and re.search(r"[\u0600-\u06FF]", ln):
            t = fix(ln); w = d.textlength(t, font=AR); d.text((W - 40 - w, y), t, fill=(243, 238, 223), font=AR)
        else:
            d.text((40, y), ln[:86], fill=(180, 220, 255) if ln.strip().startswith(("#", "|", "{", '"')) else (230, 232, 240), font=MONO)
        y += 37
    im.save(O / f"{name}.png"); return str(O / f"{name}.png")

srt = open("work/captions_v2.srt", encoding="utf-8").read().split("\n")[:22]
card("srt", "captions_v2.srt  (Whisper: every word timed)", srt, arabic=True)
song = [l for l in open("song_v4.md", encoding="utf-8").read().split("\n") if l.strip() and not l.startswith(">")][16:38]
card("song", "song_v4.md  (lyrics written with Claude)", song, arabic=True)
err = [l for l in open("errors_log.md", encoding="utf-8").read().split("\n") if l.startswith("|")][2:14]
card("errors", "errors_log.md  (every mistake, how it was fixed)", [e[:120] for e in err], arabic=True)
dec = [l for l in open("decisions_log.md", encoding="utf-8").read().split("\n") if l.startswith("|")][-12:]
card("decisions", "decisions_log.md  (review notes -> decisions)", [e[:120] for e in dec], arabic=True)
card("skills", ".claude/skills  (expertise notebooks)", ["  aly-content-assistant/   SKILL.md  -> writes the script in the channel's voice",
     "  reels-publisher/         SKILL.md  -> schedules reels on 4 platforms", "  instagram-comment-dm/    SKILL.md  -> comment keyword -> DM link",
     "  aly-video-motion/        SKILL.md  -> the approved motion style + review lessons", "", "  # a skill = a folder: SKILL.md + scripts",
     "  # the AI reads it only when the task needs it"])
mcp = open(VM / ".mcp.json", encoding="utf-8").read().split("\n")[:20]
card("mcp_json", ".mcp.json  (Claude <-> HeyGen / ElevenLabs / Higgsfield / Suno)", mcp)
idx = [l for l in open(VM / "brand/logos-tools/index.md", encoding="utf-8").read().split("\n") if l.startswith("| ")][1:20]
card("logos_index", "brand/logos-tools/index.md  (official source of every logo)", [l[:110] for l in idx])
kp = json.load(open("work/keyframes_v1.json", encoding="utf-8"))
kp = kp if isinstance(kp, list) else kp.get("items", list(kp.values()))
pl = [f"#{k.get('n', k.get('shot', '?'))}: {str(k.get('prompt', ''))[:76]}" for k in kp[:18] if isinstance(k, dict)]
card("prompts", "work/keyframes_v1.json  (every prompt saved in a file)", pl)
cost = [l for l in open("cost_plan_v2.md", encoding="utf-8").read().split("\n") if l.startswith("|")][-8:]
card("cost", "cost_plan_v2.md  (credits, before every generation)", cost, arabic=True)
covers = sorted((VM / "styles").glob("*/cover.jpg"))[:20]
S = Image.new("RGB", (5 * 320 + 40, 4 * 180 + 30), (11, 20, 48))
for i, c in enumerate(covers):
    S.paste(Image.open(c).convert("RGB").resize((310, 174)), (10 + (i % 5) * 320, 10 + (i // 5) * 180))
S.save(O / "styles_20.png")
print("ok", len(list(O.glob("*.png"))))

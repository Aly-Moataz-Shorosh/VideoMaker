"""Times of every v9-note check, read from props_v10.json (item entry + 1.4 s). Usage (project folder): python -X utf8 work/scripts/still_list_v10.py"""
import json
P = json.load(open("work/props_v10.json", encoding="utf-8")); FPS = P["fps"]
KEYS = [("1 OPEN tree", "sep:OPEN"), ("3 hold في النص", "txt:في النص"), ("4 v2v", "txt:Video to Video"), ("5 Genjutsu reel", "txt:253"),
 ("6 demos", "txt:فريمات"), ("8/9 looks", "txt:Look"), ("10 lipsync", "txt:Lip"), ("11 gsplat", "txt:Gaussian"), ("12 prompt", "txt:البرومبت"),
 ("13 Magnific", "src:magnific"), ("14 video agent", "txt:Video Agent"), ("16 Luma", "src:luma"), ("17 LLM sep", "sep:LLM"),
 ("18 cowork", "src:cowork"), ("19 audiobook", "txt:كتاب صوتي"), ("20 whisper", "src:whisper"), ("21 chrome", "src:claude_chrome"),
 ("22 codex", "txt:تطبيق Desktop"), ("23 alt tools", "txt:Antigravity"), ("24 hyperframes", "txt:HyperFrames"), ("25 cc example", "txt:فولدر فاضي"),
 ("26 photoshop", "txt:Photoshop"), ("27 program/site", "txt:برنامج أو موقع"), ("28 MCP flow", "txt:الموقع بيرجّعله النتيجة"), ("29 davinci mcp", "src:davinci_mcp"),
 ("29b blender mcp", "src:blender_mcp_build"), ("31 puppet", "k:puppet"), ("32 skills sep", "sep:Skills"), ("33 SKILL.md", "txt:SKILL.md"),
 ("35 rules", "txt:قانون"), ("36 scripts", "src:script_rec"), ("37 content skill", "src:skill_content"), ("40 pdf wall", "src:pdf13"),
 ("43 reason", "txt:3 سنين"), ("44 step6", "txt:MCP"), ("45 step11", "txt:الريل"), ("46 layer", "src:checker_motion"), ("47 char sheet", "txt:character sheet"),
 ("48 davinci", "txt:DaVinci"), ("49 bill", "title:فاتورة"), ("50 meta", "txt:Meta"), ("53 song versions", "txt:نسخ الأغنية"), ("54 watermark", "k:LYR"),
 ("39 ending", "title:الـ AI مش ساحر"), ("56 cta", "txt:إنسان")]
def hit(sc, d, key):
    k, v = key.split(":", 1)
    if k == "txt": return any(v in str(d.get(f, "")) for f in ("label", "text", "t", "head", "name", "sub"))
    if k == "src": return v in str(d.get("src", ""))
    if k == "k": return d.get("k") == v
    if k == "sep": return d.get("k") == "sep" and v in str(d.get("name", ""))
out = []
for name, key in KEYS:
    t = None
    for sc in sorted(P["scenes"], key=lambda x: x["start"]):
        if key.startswith("title:"):
            if key[6:] in str(sc.get("title") or ""): t = sc["start"] + 2.5; break
            continue
        if key == "k:LYR":
            if sc["k"] == "LYR": t = sc["start"] + 20; break
            continue
        d = next((d for d in sc.get("items", []) if hit(sc, d, key)), None)
        if d: t = sc["start"] + d.get("at", 0) / FPS + (0.6 if key.startswith("sep") else 1.4); break
    out.append([name, round(t, 2) if t else None])
json.dump(out, open("work/still_checks_v10.json", "w", encoding="utf-8"), ensure_ascii=False)
for x in out: print(x)

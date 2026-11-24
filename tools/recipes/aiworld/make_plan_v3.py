"""plan_v3_data.P -> work/plan_v3.json (times) + output/plan_v3.md (Aly's table).
Start = sentence start (or the avatar clip window); end = next scene start. Logos = names found in the scene's words.
Checks: unknown sentence ids, scenes inside an avatar window, scenes > 9 s (need inner changes on words).
Usage (project folder): python -X utf8 work/scripts/make_plan_v3.py"""
import json, re, sys
sys.path.insert(0, "work/scripts")
from plan_v3_data import P

S = json.load(open("work/sentences_v3.json", encoding="utf-8"))
SID = {s["id"]: s for s in S}
M = json.load(open("work/rough_v2_map.json", encoding="utf-8"))
AV = {x["n"]: (x["start"], x["start"] + x["dur"]) for x in M["shots"] if x["type"] == "B"}
song0, total = M["song_start"], M["total"]
song1 = song0 + 189.68
LOGO = ["Seedance", "Kling", "Veo", "Wan", "MiniMax", "Higgsfield", "HeyGen", "ElevenLabs", "Suno", "Claude Code", "Claude in Chrome",
        "Claude", "Codex", "OpenAI", "Antigravity", "Gemini", "Nano Banana", "GPT Image", "Seedream", "Soul ID", "LoRA", "Genjutsu",
        "Blender", "three.js", "Gaussian", "Whisper", "OCR", "HyperFrames", "Remotion", "ffmpeg", "ComfyUI", "Comfy Cloud", "LTX",
        "Flux", "Qwen", "Kimi", "DeepSeek", "GLM", "ByteDance", "Ollama", "LM Studio", "Firefly", "Runway", "Luma", "CapCut",
        "After Effects", "Premiere", "Photoshop", "DaVinci", "Scribe", "Warner", "BMG", "Believe", "YouTube", "يوتيوب", "Meta",
        "تيك توك", "إنستجرام", "فيسبوك", "SynthID", "C2PA", "PowerShell", "MCP", "Cinema Studio", "Supercomputer", "LiveAvatar"]

def start_of(p):
    if "av" in p: return AV[p["av"]][0]
    if p.get("song"): return song0
    sid = p["at"]
    if sid not in SID:
        base = re.sub(r"[a-z]$", "", sid)
        if base in SID: return SID[base]["a"] + 1.2   # 'b' = a second scene inside the same sentence
        raise SystemExit(f"unknown sentence id {sid}")
    return SID[sid]["a"]

rows = []
for p in P:
    rows.append({**p, "start": round(start_of(p), 2)})
rows.sort(key=lambda r: r["start"])
for i, r in enumerate(rows):
    # a sentence scene that starts inside an avatar window starts when the window ends
    for (a, b) in AV.values():
        if "av" not in r and a - 0.05 < r["start"] < b - 0.05:
            r["start"] = round(b, 2); r["pushed"] = True
rows.sort(key=lambda r: r["start"])
for i, r in enumerate(rows):
    # an avatar clip is only as long as its window: the next scene starts when it ends
    if "av" in r and i + 1 < len(rows) and rows[i + 1]["start"] > AV[r["av"]][1]:
        rows[i + 1]["start"] = round(AV[r["av"]][1], 2)
for i, r in enumerate(rows):
    r["end"] = rows[i + 1]["start"] if i + 1 < len(rows) else total
    if r.get("song"): r["end"] = round(song1, 2)
    r["dur"] = round(r["end"] - r["start"], 2)
    words = " ".join(s["t"] for s in S if s["a"] < r["end"] - 0.05 and s["b"] > r["start"] + 0.05)
    r["text"] = words
    r["logos"] = [l for l in LOGO if l.lower() in words.lower()]
    for l in ("Claude Code", "Claude in Chrome"):
        if l in r["logos"] and "Claude" in r["logos"] and words.count("Claude") == words.count(l): r["logos"].remove("Claude")
warn = [f"{r['start']:.1f} {r['k']} {r['dur']}s" for r in rows if r["dur"] > 9 and r["k"] not in ("LYR",)]
neg = [r for r in rows if r["dur"] <= 0.3]
json.dump(rows, open("work/plan_v3.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

KIND = {"AV": "علي بيتكلم + موشن جنبه", "CLIP": "فيديو متولّد", "MAP6": "خريطة الطيارة", "LOGOS": "لوجوهات", "KT": "كلام متحرك",
        "WEB": "صفحة حقيقية", "NUM": "رقم/عداد", "VID": "فيديو القناة + QR", "ICON": "أيقونات", "FLOW": "سلسلة ←", "SPLIT": "قبل/بعد",
        "BTS": "من ورا الكواليس", "LYR": "الأغنية", "STEP": "خطوة"}
mm = lambda x: f"{int(x) // 60}:{int(x) % 60:02d}"
L = ["# خطة rough cut v3 — كل جملة والي بيظهر عليها", "",
     f"{len(rows)} مشهد · {sum(1 for r in rows if r['k']=='AV')} لعلي بيتكلم (من الـ 34 لقطة الموجودة) · مفيش ولا كارت · مفيش كابشن (الفيديو طويل) · "
     "كل لوجو بيطلع على اسمه · الكليبات المتولّدة على الجمل اللي بتتكلم عنها بس.", "",
     "| من | لـ | النوع | اللي على الشاشة | اللوجوهات | الكلام |", "|---|---|---|---|---|---|"]
ch = None
for r in rows:
    t = r["text"]; t = (t[:110] + "…") if len(t) > 110 else t
    clip = f" (كليب {', '.join(map(str, r['clip']))})" if r.get("clip") else ""
    L.append(f"| {mm(r['start'])} | {mm(r['end'])} | {KIND[r['k']]} | {r['d']}{clip} | {' · '.join(r['logos'])} | {t} |")
open("output/plan_v3.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
used = sorted({c for r in rows for c in r.get("clip", [])})
print(len(rows), "scenes; long>9s:", len(warn), warn[:30]); print("too short:", [(r['start'], r['k']) for r in neg])
print("clips used", len(used), used)
print("logos needed:", sorted({l for r in rows for l in r["logos"]}))

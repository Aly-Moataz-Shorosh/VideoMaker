"""Props for 'ai-world-v5' (v4 builder + v5_specs explaining scenes). Was: props for 'ai-world-v4' (Aly's v3 notes 1-16): every element = an enta board item (the «انت بتشتغل ايه» kit) placed by meaning,
ENTERING on its word and LEAVING smoothly; captions = the script on its word times; times = timeline v4 (make_timeline_v4.py).
Usage (project folder): python -X utf8 work/scripts/make_props_v5.py [--till SECONDS]"""
import json, os, re, shutil, sys, unicodedata
from pathlib import Path

P = Path(__file__).resolve().parents[2]; os.chdir(P)
VM = P.parents[1]; PUB = VM / "motion-library" / "public" / "projects" / "aiworld" / "v5"; PUB.mkdir(parents=True, exist_ok=True)
LOG = VM / "brand" / "logos-tools"; FL = VM / "motion-library" / "public" / "fluent"
sys.path.insert(0, "work/scripts")
from plan_v3_content import C
from plan_v4_content import C4
C = {**C, **C4}
plan = json.load(open("work/plan_v3.json", encoding="utf-8"))
T4 = json.load(open("work/timeline_v5.json", encoding="utf-8")); ED = T4["edits"]
W = json.load(open("work/words_v5.json", encoding="utf-8"))
m2 = json.load(open("work/rough_v2_map.json", encoding="utf-8"))
S0v4, TOTAL = T4["song_start_v4"], T4["total"]
FPS = 25

def v4(t):
    d = 0.0
    for e in ED:
        if t >= e["v2_b"] - 1e-6: d += e["delta"]
        elif e["file"] is None and t > e["v2_a"]: return round(e["v2_a"] + d, 3)
    return round(t + d, 3)

MISSING = []
def link(src, sub):
    src = Path(src)
    name = src.name if sub in ("clips", "logos", "channel", "avatar_gen", "avatar_real", "avatar_orig") else f"{src.parent.name}__{src.name}"
    dst = PUB / sub / name; dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists(): MISSING.append(str(src))
    elif not dst.exists():
        try: os.link(src, dst)
        except OSError: shutil.copy2(src, dst)
    return f"projects/aiworld/v5/{sub}/{name}"

LOGOS = {"Seedance": "seedance.ico", "Kling": "kling.png", "Veo": "veo.ico", "Wan": "wan.ico", "MiniMax": "minimax.ico", "Higgsfield": "higgsfield.png",
    "HeyGen": "heygen.ico", "ElevenLabs": "elevenlabs.png", "Suno": "suno.png", "Claude": "claude.svg", "Codex": "openai-codex.png", "OpenAI": "openai.png",
    "Antigravity": "antigravity.png", "Gemini": "gemini.png", "Nano Banana": "gemini.png", "GPT Image": "openai.png", "Seedream": "seedance.ico",
    "Genjutsu": "higgsfield.png", "Soul ID": "higgsfield.png", "Blender": "blender.svg", "three.js": "threejs.ico", "Whisper": "whisper.png",
    "HyperFrames": "hyperframes.ico", "Remotion": "remotion.png", "ffmpeg": "ffmpeg.ico", "ComfyUI": "comfyui.png", "LTX": "ltx.png", "Flux": "flux.png",
    "Qwen": "qwen.png", "Kimi": "kimi.ico", "DeepSeek": "deepseek.ico", "GLM": "glm.png", "ByteDance": "bytedance.png", "Ollama": "ollama.png",
    "LM Studio": "lmstudio.ico", "Firefly": "firefly.png", "Runway": "runway.png", "Luma": "luma.ico", "CapCut": "capcut.ico", "After Effects": "adobe.png",
    "Premiere": "premiere-pro-official.png", "Photoshop": "adobe.png", "DaVinci": "davinci-resolve.png", "Warner": "warner.png", "BMG": "bmg.ico",
    "Believe": "believe.png", "يوتيوب": "youtube.png", "YouTube": "youtube.png", "Meta": "meta.png", "تيك توك": "tiktok.png", "إنستجرام": "instagram.ico",
    "فيسبوك": "facebook.png", "SynthID": "synthid.ico", "C2PA": "c2pa.svg", "Scribe": "elevenlabs.png", "Python": "python.ico"}
EMO_FIX = {"❓": "red_question_mark", "🧩": "puzzle_piece", "🔀": "shuffle_tracks_button", "🖼": "framed_picture", "✂": "scissors", "↔": "left-right_arrow",
    "🧬": "dna", "🔎": "magnifying_glass_tilted_right", "🟦": "blue_square", "🟧": "orange_square", "➡": "right_arrow", "🔄": "counterclockwise_arrows_button",
    "⬆": "up_arrow", "⏩": "play_button", "✅": "check_mark_button", "🌍": "globe_showing_europe-africa", "🗣": "speaking_head", "🔊": "speaker_high_volume",
    "💥": "collision", "🔇": "muted_speaker", "🤖": "robot", "🧊": "ice", "🔤": "input_latin_letters", "👕": "dress", "💡": "light_bulb", "🏃": "person_running",
    "💻": "laptop", "▶": "play_button", "🚫": "prohibited", "🖱": "computer_mouse", "♻": "recycling_symbol", "🔁": "repeat_button", "🙅": "prohibited",
    "➕": "plus", "🧑": "person", "🔉": "speaker_low_volume"}
def fluent(e):
    c = e.replace("️", "")
    n = EMO_FIX.get(c) or unicodedata.name(c, "?").lower().replace(" ", "_")
    return n if (FL / f"{n}.png").exists() else None

def words_in(a, b): return [w for w in W if a - 0.02 <= w["a"] < b - 0.02]
def anchor(word, a, b):
    if not word: return None
    key = word.split()[0].lower()
    for w in words_in(a - 0.3, b + 0.3):
        if key in w["w"].lower(): return w["a"]
    return None
fix_kadr = lambda s: s.replace("الكادر", "الكدر").replace("كادر", "كدر") if isinstance(s, str) else s
fr = lambda t, a: max(0, int(round((t - a) * FPS)))

HF = json.load(open("assets/ai/higgsfield/clips_v1/clips_v1.json", encoding="utf-8"))
AVC = {x["n"]: x for x in json.load(open("assets/ai/heygen/avatar_clips_v1/avatar_clips_v1.json", encoding="utf-8"))}
METH = {int(k): v for k, v in json.load(open("work/avatar_methods_v3.json", encoding="utf-8"))["methods"].items()}
AVW = {x["n"]: (x["start"], x["start"] + x["dur"]) for x in m2["shots"] if x["type"] == "B"}
def clip_file(n): f = HF[str(n)]["file"]; return link(Path("assets/ai/higgsfield/clips_v1") / f, "clips"), HF[str(n)]["dur"]
def avatar_src(n, m):
    f = AVC[n]["file"]
    if m == "real": return link(Path("assets/ai/heygen/avatar_clips_v3_real") / f, "avatar_real")
    return link(Path("assets/ai/heygen/avatar_clips_v2_gen") / f, "avatar_gen")

def to_items(raw, a, b, kind):
    """content items -> enta items with layout + at/out frames (scene-relative)."""
    dur = b - a; end = int(dur * FPS) - 12
    rows = []
    for anc, it in raw:
        it = dict(it); t = it.pop("_t", None)
        if t is None: t = anchor(anc, a, b)
        rows.append([t, anc, it])
    n = len(rows); known = [r[0] for r in rows if r[0] is not None]
    for i, r in enumerate(rows):   # items whose word is not in this scene: spread, in order
        if r[0] is None: r[0] = a + 0.4 + i * max(0.7, (dur - 1.2) / max(1, n))
    rows.sort(key=lambda r: r[0])
    out = []
    big = kind in ("BOARD", "VIDCARD")
    pics = [r for r in rows if "img" in r[2]]
    lay = [r for r in rows if "pos" not in r[2] and "page" not in r[2]]   # only these share the board row
    groups, g = [], []   # a pause > 2.5 s between items = a NEW group: the old group leaves, the new one is laid out on its own (note 6)
    for r in lay:
        if g and r[0] - g[-1][0] > 2.5: groups.append(g); g = []
        g.append(r)
    if g: groups.append(g)
    gof = {id(r[2]): (gi, grp) for gi, grp in enumerate(groups) for r in grp}
    for i, (t, anc, it) in enumerate(rows):
        at = fr(t, a); o = end
        gi, grp = gof.get(id(it), (0, [[t, anc, it]]))
        if gi + 1 < len(groups) and "out_at" not in it: o = min(o, fr(groups[gi + 1][0][0], a) - 6)
        if "out_at" in it:
            ot = anchor(it["out_at"], a, b)
            if ot is not None: o = max(at + 25, fr(ot, a) - 4)
        o = max(o, at + int(1.5 * FPS)) if at + int(1.5 * FPS) < end + 12 else end
        lab = fix_kadr(it.get("label"))
        if "pos" in it: x, y = it["pos"]
        elif kind == "BOARD":
            li = next((q for q, r in enumerate(grp) if r[2] is it), 0); m = len(grp); row2 = m > 3; per = (m + 1) // 2 if row2 else m
            j = li % per if row2 else li; r_ = li // per if row2 else 0
            gap = 1200 / max(1, per); x = 960 + (per - 1) * gap / 2 - j * gap; y = (430 + r_ * 300) if row2 else 560
        else:   # over a video: beside him / beside the picture, alternating right / left, never in the centre
            li = next((q for q, r in enumerate(grp) if r[2] is it), 0); side = li % 2; slot = (li // 2) % 3
            x = 1500 if side == 0 else 420; y = 340 + slot * 210
        if "img" in it:
            w = it.get("w") or (560 if (kind == "BOARD" and len(pics) <= 2) else 430 if kind == "BOARD" else 400)
            if kind == "BOARD" and "pos" not in it: w = min(w, (1200 / max(1, per) if 'per' in dir() else 1200) / 0.8 - 40)
            if it["img"].startswith("work/pdf_pages"): w = min(w, 300)
            out.append({"k": "pic", "src": link(it["img"], "imgs"), "x": x, "y": y, "w": w, "ar": 16 / 9 if not it["img"].startswith("work/pdf_pages") else 0.74,
                        "fit": "cover" if not it["img"].startswith("work/pdf_pages") else "contain", "cap": lab, "capSize": 30, "at": at, "out": o, "rot": (-2 if i % 2 else 2)})
        elif "logo" in it:
            s = 170 if kind == "BOARD" else 120
            out.append({"k": "logo", "src": link(LOG / LOGOS[it["logo"]], "logos"), "x": x, "y": y - (30 if kind == "BOARD" else 0), "s": s, "at": at, "out": o})
            if lab: out.append({"k": "text", "text": lab, "x": x, "y": y + s * 0.5 + 26 - (30 if kind == "BOARD" else 0), "size": 36 if kind == "BOARD" else 30, "at": at + 3, "out": o})
        elif "num" in it:
            v = re.sub(r"[^\d.]", "", it["num"])
            if v and re.fullmatch(r"\d+(\.\d+)?", v) and "–" not in it["num"]:
                pre = "$" if it["num"].startswith("$") else ("-" if it["num"].startswith("-") else ""); suf = "K" if it["num"].endswith("K") else ""
                out.append({"k": "num", "from": 0, "to": float(v), "prefix": pre, "suffix": suf, "x": x, "y": y - 40, "size": 150 if kind == "BOARD" else 110, "dur": 20, "at": at, "out": o})
            else:
                out.append({"k": "text", "text": it["num"], "x": x, "y": y - 40, "size": 110, "color": "mustard", "at": at, "out": o})
            if lab: out.append({"k": "text", "text": lab, "x": x, "y": y + 70, "size": 40, "paper": True, "at": at + 4, "out": o})
        elif "text" in it:
            out.append({"k": "text", "text": fix_kadr(it["text"]), "x": x, "y": y, "size": 46, "paper": True, "hi": "orange", "at": at, "out": o})
        elif "page" in it:
            out.append({"k": "page", "src": link(it["page"], "pages"), "url": it.get("url"), "at": at, "out": o})
        elif lab or it.get("emoji"):
            emo = fluent(it["emoji"]) if it.get("emoji") else None
            out.append({"k": "chip", "text": lab or "", "emo": emo, "x": x, "y": y, "size": 40 if kind == "BOARD" else 34, "bg": ["blue", "orange", "olive", "mustard"][i % 4], "at": at, "out": o})
    return out

def anchor_wide(word, a, b):   # the FIRST time the word is said from this scene on (plan rows are shot windows, sentences run over them)
    if not word: return None
    key = word.split()[0].lower()
    for w in words_in(a - 0.3, b + 5):
        if key in w["w"].lower(): return w["a"]
    return None
push_to = 0.0; pull_to = None
CUTS = [v4(e["v2_a"]) for e in ED if e["file"] is None]
pending = []   # items whose word is said in a LATER scene -> shown there, on their word (note 6)
till = float(sys.argv[sys.argv.index("--till") + 1]) if "--till" in sys.argv else 1e9
scenes, hud = [], []
fam_done = False
for r in plan:
    a, b = v4(r["start"]), v4(r["end"])
    k = r["k"]; key = r.get("at") or (f"av{r['av']}" if "av" in r else None); c = C.get(key, {})
    if pull_to is not None: a = min(a, pull_to); pull_to = None
    a = max(a, push_to); b += c.get("extend", 0); push_to = b   # 'extend' = hold this scene into the next sentence (the next one starts later)
    cut = next((x for x in CUTS if a + 0.3 < x < b), None)
    if k in ("AV", "VID") and cut is not None: b = cut; pull_to = cut; push_to = cut   # a removed sentence inside an avatar shot: the shot ends there (no lips on deleted words)
    if b - a < 0.2 or a >= till: continue
    b = min(b, till)
    raw = list(c.get("items", []))
    if not raw and k in ("LOGOS", "AV"):   # names said in this scene -> their logos, on their words
        for nm in LOGOS:
            if any(nm.split()[0].lower() in w["w"].lower() for w in words_in(a, b)) and nm not in [x[0] for x in raw]:
                raw.append((nm, dict(logo=nm, label=nm)))
    if k not in ("SPLIT", "LYR", "MAP6") and c.get("fx") != "diffusion":
        keep = []
        for anc, it in raw:
            t = anchor_wide(anc, a, b) if not it.get("qr") else None
            if t is not None and t >= b - 0.3 and "page" not in it: pending.append((anc, {**it, "_t": t}))
            else: keep.append((anc, it))
        take = [x for x in pending if x[1]["_t"] < b - 0.3]
        pending = [x for x in pending if x[1]["_t"] >= b - 0.3]
        raw = [(anc, {**it, "_t": max(it["_t"], a + 0.1)}) for anc, it in take] + keep
    sc = {"k": k, "start": a, "dur": round(b - a, 3), "title": fix_kadr(c.get("title")), "clips": [], "items": [], "words": [], "glitch": [], "fam": [], "fx": c.get("fx")}
    if k == "AV" or (k == "VID" and "av" in r):
        n = r["av"]; wa, wb = v4(AVW[n][0]), v4(AVW[n][1])
        if n == 1:   # opening 0 -> 2 -> 1 with the SHOW's glitch (note 2)
            fs = {"orig": link("assets/ai/heygen/avatar_clips_v1/avatar_001_C00.mp4", "avatar_orig"), "real1": link("assets/ai/heygen/look_S4g/ex_real.mp4", "avatar_real"),
                  "gen1": link("assets/ai/heygen/look_S4g/ex_generated.mp4", "avatar_gen")}
            sc["clips"] = [{"src": fs[s], "from": round(a + x, 3), "dur": round(y - x, 3), "skip": x} for s, x, y in [("orig", 0, 1.6), ("real1", 1.6, 3.2), ("gen1", 3.2, b - a)]]
            sc["glitch"] = [a + 1.6, a + 3.2]
        else:
            sc["clips"] = [{"src": avatar_src(n, METH.get(n, "gen")), "from": a, "dur": round(b - a, 3), "skip": round(a - wa, 3)}]
        if k == "VID":
            vids = r["vid"] if isinstance(r["vid"], list) else [r["vid"]]
            raw = [(None, dict(img=f"assets/channel/thumb_{v}.jpg", qr=v)) for v in vids]
        sc["k"] = "AV"; kind = "AV"
    elif k == "CLIP":
        ids = [x[0] for x in c.get("clips", [])] or r.get("clip", [])
        ancs = [x[1] for x in c.get("clips", [])] or [None] * len(ids)
        t = a
        for i, n in enumerate(ids):
            src, cd = clip_file(n); even = a + (b - a) * (i + 1) / len(ids) if i + 1 < len(ids) else b
            nxt = (anchor(ancs[i + 1], a, b) if i + 1 < len(ids) and ancs[i + 1] else None) or even
            if nxt <= t + 0.5: nxt = max(even, t + 0.5)
            dd = min(cd - 0.15, nxt - t)
            sc["clips"].append({"src": src, "from": round(t, 3), "dur": round(dd, 3), "skip": 0.05}); t += dd
        kind = "CLIP"
        if t < b - 0.3:   # clips shorter than the sentence: the rest is a board (no freeze, no slow motion)
            cut = t
            scA = {**sc, "dur": round(cut - a, 3)}; scA["items"] = to_items([x for x in raw if (anchor(x[0], a, cut) or a) < cut], a, cut, "CLIP")
            scenes.append(scA)
            rest = [x for x in raw if (anchor(x[0], cut, b) or 0) >= cut]
            sc = {"k": "BOARD", "start": round(cut, 3), "dur": round(b - cut, 3), "title": None, "clips": [], "items": to_items(rest, cut, b, "BOARD"), "words": [], "glitch": [], "fam": []}
            scenes.append(sc); continue
    elif k == "MAP6":
        hi = re.search(r"قطعة (\d)", r["d"])
        if not fam_done and not hi:
            for fw in ["التوليد", "LLMs", "السكريبتات", "MCP", "skills", "الإنسان"]:
                t = anchor(fw, a, b); sc["fam"].append(fr(t if t is not None else a + 1, a))
            fam_done = True
        else:
            sc["hud"] = int(hi[1]) - 1 if hi else 5
        kind = "BOARD"
    elif k == "LYR":
        lines = json.load(open("work/song_C1_lines.json", encoding="utf-8"))
        POOL = [183, 207, 210, 204, 216, 171, 201, 213, 192, 189, 195, 198, 6, 26, 99, 115, 162]
        LMAP = [("الجدار", 186), ("فحمة", 186), ("تور", 186), ("حبر", 189), ("دماغي", 192), ("mouse", 195), ("Photoshop", 195), ("rendering", 198), ("frame", 198),
                ("جملة", 201), ("صوت", 204), ("agents", 213), ("MCP", 213), ("الآلة", 201), ("بتجري", 204), ("بترسم", 192), ("غيّر", 183), ("بس اللي", 207),
                ("الفحمة", 210), ("الإيد", 186), ("الفيديو", 216), ("الحلم", 171), ("أنا", 186), ("اتغيرت", 189), ("وعيني", 192), ("قالوا", 201), ("قلت", 168)]
        if r.get("song"):
            marks = [(S0v4 + ln["a"], ln) for ln in lines]; prev, pi = None, 0
            for i, (la, ln) in enumerate(marks):
                lb = marks[i + 1][0] if i + 1 < len(marks) else b
                t = a if i == 0 else t; n = next((n for key_, n in LMAP if key_ in ln["t"]), POOL[pi % len(POOL)])
                while t < min(lb, b) - 0.45:   # a rest < 0.45 s goes to the next line's clip (it starts that much early): no flashes
                    if n == prev: pi += 1; n = POOL[pi % len(POOL)]
                    src, cd = clip_file(n); dd = min(cd - 0.15, min(lb, b) - t)
                    rest = min(lb, b) - (t + dd)
                    if 0 < rest < 0.45 and dd + rest <= cd - 0.03: dd += rest   # never a 0.2 s flash of another clip
                    sc["clips"].append({"src": src, "from": round(t, 3), "dur": round(dd, 3), "skip": 0.05}); t += dd; prev = n; pi += 1; n = POOL[pi % len(POOL)]
                endl = (marks[i + 1][0] if i + 1 < len(marks) else S0v4 + 189.68)
                sc["items"].append({"k": "line", "t": round(S0v4 + ln["a"], 3), "end": round(endl, 3)})
                ws = ln["t"].split(); dd2 = ln["b"] - ln["a"]
                sc["words"] += [{"t": round(S0v4 + ln["a"] + j * dd2 / max(1, len(ws)), 3), "w": w} for j, w in enumerate(ws)]
            if t < b - 0.05:
                src, cd = clip_file(216); sc["clips"].append({"src": src, "from": round(t, 3), "dur": round(min(cd - 0.15, b - t), 3), "skip": 0.05})
        else:   # the short teaser in C02e
            src, cd = clip_file(186); sc["clips"] = [{"src": src, "from": a, "dur": round(min(cd - 0.15, b - a), 3), "skip": 0.05}]
            if cd - 0.15 < b - a:
                src2, _ = clip_file(189); sc["clips"].append({"src": src2, "from": round(a + cd - 0.15, 3), "dur": round(b - a - cd + 0.15, 3), "skip": 0.05})
            ln = lines[1]; ws = ln["t"].split()
            sc["items"] = [{"k": "line", "t": a + 0.3, "end": b}]
            sc["words"] = [{"t": round(a + 0.3 + j * 0.35, 3), "w": w} for j, w in enumerate(ws)]
        scenes.append(sc); continue
    elif k == "VID":
        vids = r["vid"] if isinstance(r["vid"], list) else [r["vid"]]
        raw = [(None, dict(img=f"assets/channel/thumb_{v}.jpg", qr=v)) for v in vids]; kind = "BOARD"; sc["k"] = "BOARD"
    else:
        kind = "BOARD"
        if k == "WEB": pass
        elif k == "SPLIT": pass
        sc["k"] = {"WEB": "WEB", "SPLIT": "SPLIT"}.get(k, "BOARD")
    # special item kinds
    items = []
    if k == "SPLIT":
        spare = list(r.get("clip") or [])   # a side with no picture = the plan's clip (before / after); none = a paper card with its words
        for anc, it in raw:
            if not it.get("img") and spare: it = {**it, "img": None, "_clip": spare.pop(0)}
            km = re.search(r"kf_(\d+)_", it.get("img") or "")
            if km and "فيديو" in (it.get("label") or "") and str(int(km[1])) in HF: it = {**it, "_clip": int(km[1])}   # «بقت فيديو» = the real clip
            t = anchor(anc, a, b) or a
            items.append({"k": "split", "src": clip_file(it["_clip"])[0] if it.get("_clip") else link(it["img"], "imgs") if it.get("img") else None, "before": link(it["before"], "imgs") if it.get("before") else None,
                          "prompt": it.get("prompt"), "cap": fix_kadr(it.get("label")), "at": fr(t, a)})
        if not raw and r.get("clip"):
            for n in r["clip"][:2]:
                src, cd = clip_file(n); sc["clips"].append({"src": src, "from": a, "dur": round(min(cd - 0.15, b - a), 3), "skip": 0.05}); break
            sc["k"] = "CLIP"
        raw = []
    if c.get("fx") == "diffusion":
        anc, it = raw[0]; items.append({"k": "diff", "src": link(it["img"], "imgs"), "at": fr(anchor(anc, a, b) or a, a)})
        raw = [(anc, {"label": it.get("label")})]
    if k == "WEB" and raw and not any("page" in x[1] for x in raw):   # v3 pages (evidence) -> real page in the browser
        raw = [(anc, ({"page": it["img"], "url": c.get("url")} if "img" in it and "evidence" in it["img"] else it)) for anc, it in raw]
    vidqr = [(x[1].get("qr")) for x in raw]
    its = to_items([(anc, {kk: vv for kk, vv in it.items() if kk != "qr"}) for anc, it in raw], a, b, kind)
    for d, q in zip([x for x in its if x["k"] == "pic"], [q for q in vidqr if q]):   # YouTube QR always beside its thumbnail
        its.append({"k": "pic", "src": link(f"assets/channel/qr_{q}.png", "channel"), "x": d["x"], "y": d["y"] + d.get("w", 430) * 0.8 / 1.78 / 2 + 110, "w": 150, "ar": 1, "fit": "contain",
                    "tape": False, "at": d["at"] + 6, "out": d["out"], "qr": True})   # QR right UNDER its own thumbnail (v5: beside it hit the next one)
    sc["items"] = items + its
    if sc["k"] == "BOARD" and not items and not sc["fam"] and sc.get("hud") is None and not any(d["k"] in ("pic",) and d.get("w", 0) >= 500 for d in its):
        sc["_raw"] = [(anc, {kk: vv for kk, vv in it.items() if kk != "qr"}) for anc, it in raw]
    scenes.append(sc)
    hi = re.search(r"قطعة (\d)", r["d"])
    if hi: hud.append({"a": a, "i": int(hi[1]) - 1})

# merge runs of short BOARD sentences into ONE board (note 16: items stay; each still enters on its own word), <= 9 s and <= 6 items
merged, i = [], 0
while i < len(scenes):
    sc = scenes[i]
    if "_raw" in sc:
        j, raw = i, list(sc["_raw"])
        while j + 1 < len(scenes) and "_raw" in scenes[j + 1] and scenes[j + 1]["start"] + scenes[j + 1]["dur"] - sc["start"] <= 9 and len(raw) + len(scenes[j + 1]["_raw"]) <= 6                 and (sc["dur"] < 3.5 or scenes[j + 1]["dur"] < 3.5):
            j += 1; raw += scenes[j]["_raw"]
        if j > i:
            a, b = sc["start"], scenes[j]["start"] + scenes[j]["dur"]
            subs = [x for x in scenes[i:j + 1] if x.get("title")]   # each sentence's title shows on ITS sentence, at the top
            tits = [{"k": "text", "text": x["title"], "x": 960, "y": 105, "size": 50, "paper": True, "hi": "orange", "at": fr(x["start"], a),
                     "out": (fr(subs[q + 1]["start"], a) - 2 if q + 1 < len(subs) else int((b - a) * FPS) - 12)} for q, x in enumerate(subs)]
            sc = {**sc, "title": None, "dur": round(b - a, 3), "items": tits + to_items(raw, a, b, "BOARD")}
        merged.append(sc); i = j + 1
    else:
        merged.append(sc); i += 1
scenes = merged
for x in scenes: x.pop("_raw", None)
scenes = [x for x in scenes if not (x["dur"] < 0.5 and not x["items"] and not x["clips"] and not x.get("title"))]   # an empty 0.4 s board = a flash
for x, y in zip(scenes, scenes[1:]): x["dur"] = round(y["start"] - x["start"], 3)   # no gaps (a gap = black)
scenes[-1]["dur"] = round(TOTAL - scenes[-1]["start"], 3)
for x in scenes:   # a video scene stretched by the gap fill: its last clip plays on (never a black hole)
    if x["clips"] and x["k"] in ("AV", "CLIP", "LYR"):
        c_ = x["clips"][-1]; gap_ = x["start"] + x["dur"] - (c_["from"] + c_["dur"])
        if 0 < gap_ < 0.8: c_["dur"] = round(c_["dur"] + gap_, 3)
# items in a short sentence over video: shown at least 1.5 s -> appear a bit before their word rather than flash
for x in scenes:
    end = int(x["dur"] * FPS) - 12
    for d in x["items"]:
        if "out" in d and d["out"] - d["at"] < 37 and d["k"] not in ("line",):
            d["at"] = max(0, min(d["at"], d["out"] - 37))

# ---- v5: explaining scenes replace their ranges (Aly's v4 notes) ----
import v5_specs, v5_apply
scenes = v5_apply.apply(scenes, v5_specs.SPECS, link)
for x, y in zip(scenes, scenes[1:]):   # no gaps, no overlaps after the inserts
    x["dur"] = round(y["start"] - x["start"], 3)
scenes = v5_apply.fix_short(scenes)
for x, y in zip(scenes, scenes[1:]): x["dur"] = round(y["start"] - x["start"], 3)
for x in scenes:   # the v4 kit items: 20% smaller (note 24) unless they already carry a scale
    for d in x["items"]:
        if d["k"] in ("pic", "logo", "text", "chip", "num", "emo", "sticker") and "scale" not in d: d["scale"] = 0.8
UNRES = v5_apply.resolve(scenes)   # «خلي بالك من ال overlap»: move whole groups apart / into the safe area (after the 0.8 scale)
print("overlaps left after the resolver:", UNRES)
SUBS = []
for word, after, fam, name in v5_specs.SUBS:
    t = v5_specs.T(word, after); SUBS.append({"a": t, "fam": fam, "name": name})
SUBS = [{**x, "b": (SUBS[i + 1]["a"] if i + 1 < len(SUBS) else S0v4)} for i, x in enumerate(SUBS)]
SFX = [("glitch", g) for sc in scenes for g in sc.get("glitch", [])] + [("whoosh_2", x["a"]) for x in SUBS]
for sp in v5_specs.SPECS: SFX += [(n, t) for n, t in sp["sfx"]]

# captions: the script on its word times (not over the song), <= 7 words, a sentence never split in a strange place
caps, cur = [], []
for w in W:
    if S0v4 - 0.2 <= w["a"] < S0v4 + 189.9: continue
    if cur and w["a"] - cur[-1]["b"] > 1.2:   # a long pause (or the song) closes the caption
        caps.append({"a": cur[0]["a"], "b": cur[-1]["b"] + 0.25, "t": fix_kadr(" ".join(x["w"] for x in cur))}); cur = []
    cur.append(w)
    if len(cur) >= 7 or re.search(r"[.!؟?:،,]$", w["w"]) and len(cur) >= 3:
        caps.append({"a": cur[0]["a"], "b": cur[-1]["b"] + 0.25, "t": fix_kadr(" ".join(x["w"] for x in cur))}); cur = []
if cur: caps.append({"a": cur[0]["a"], "b": cur[-1]["b"] + 0.25, "t": fix_kadr(" ".join(x["w"] for x in cur))})
mc = []
for c_ in caps:   # a tiny caption (one word cut off by a pause) joins its neighbour
    if mc and (c_["b"] - c_["a"] < 0.7 or mc[-1]["b"] - mc[-1]["a"] < 0.7) and c_["a"] - mc[-1]["b"] < 1.5 and len((mc[-1]["t"] + " " + c_["t"]).split()) <= 9:
        mc[-1] = {"a": mc[-1]["a"], "b": c_["b"], "t": mc[-1]["t"] + " " + c_["t"]}
    else: mc.append(c_)
caps = mc
for x, y in zip(caps, caps[1:]): x["b"] = min(x["b"], y["a"])
hud_r = [{"a": h["a"], "b": (hud[i + 1]["a"] if i + 1 < len(hud) else S0v4), "i": h["i"]} for i, h in enumerate(hud)]
dur = min(TOTAL, till)
for c_ in caps:   # «3D» in English (note 5 / 28)
    c_["t"] = c_["t"].replace("الثري دي", "الـ 3D").replace("وثري دي", "و3D").replace("ثري دي", "3D")
    c_["t"] = re.sub(r"(?<![\w\u0600-\u06FF])و(?=[A-Za-z0-9])", "و ", c_["t"])   # «وCreator» read as «Creatorg»: a space after و
props = {"fps": FPS, "duration": round(dur, 3), "outW": 1280, "scenes": scenes, "hud": hud_r, "subs": SUBS, "caps": [c_ for c_ in caps if c_["a"] < dur]}
json.dump(sorted(SFX, key=lambda x: x[1]), open("work/sfx_v5.json", "w"), indent=0)
out = "work/props_v5.json" if till > 1e8 else f"work/props_v5_till{int(till)}.json"
json.dump(props, open(out, "w", encoding="utf-8"), ensure_ascii=False)
print(out, len(scenes), "scenes", len(caps), "caps, total", TOTAL, "| missing", len(set(MISSING)), sorted(set(MISSING))[:5])

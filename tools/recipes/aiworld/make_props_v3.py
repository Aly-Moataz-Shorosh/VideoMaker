"""plan_v3.json (v2 times) -> Remotion props for 'ai-world-v3' (v3 times) + work/timeline_v3_shift.json.
v3 time = v2 time + shift of the 2 re-voiced sentences (S007.2, S009.2 «كلام مكتوب»).
Everything a scene shows is anchored on WORD times (logos on their names, families on their words, song words on the beat).
Media are hard-linked into motion-library/public/projects/aiworld/v3/.  Usage: python -X utf8 work/scripts/make_props_v3.py [--till SECONDS]"""
import json, os, re, sys, shutil
from pathlib import Path

P = Path(__file__).resolve().parents[2]
VM = P.parents[1]
PUB = VM / "motion-library" / "public" / "projects" / "aiworld" / "v3"; PUB.mkdir(parents=True, exist_ok=True)
LOG = VM / "brand" / "logos-tools"
os.chdir(P)
plan = json.load(open("work/plan_v3.json", encoding="utf-8"))
tl = json.load(open("work/timeline_v2.json", encoding="utf-8"))
m2 = json.load(open("work/rough_v2_map.json", encoding="utf-8"))
S = {s["id"]: s for s in json.load(open("work/sentences_v3.json", encoding="utf-8"))}
S0, EX = m2["song_start"], m2["extra"]
rm2 = lambda t: t if t <= S0 + 180 else t + EX

# ---- v3 shift: the two «كلام مكتوب» sentences (new HeyGen audio, trimmed to its words + 0.05 s) ----
FIX = {"S007.2": ("assets/ai/heygen/voice_fix_v1/S007.2_kalam_maktoob.wav", 0.299 - 0.05, 3.243 + 0.05,
                  [["كلام", 0.299, 0.597], ["مكتوب", 0.64, 1.024], ["يبقى", 1.237, 1.493], ["صورة،", 1.536, 1.835], ["وصورة", 2.048, 2.645], ["تبقى", 2.688, 2.944], ["صورة.", 2.987, 3.243]]),
       "S009.2": ("assets/ai/heygen/voice_fix_v1/S009.2_kalam_maktoob.wav", 0.256 - 0.05, 3.584 + 0.05,
                  [["كلام", 0.256, 0.597], ["مكتوب", 0.64, 0.896], ["يبقى", 0.939, 1.152], ["فيديو،", 1.195, 1.451], ["وصورة", 1.664, 2.091], ["تبقى", 2.133, 2.304], ["فيديو،", 2.347, 2.56], ["وأقوى", 2.773, 3.285], ["حاجة:", 3.328, 3.584]])}
shifts = []   # (v2 time after which, delta)
for sid, (f, a, b, _) in FIX.items():
    old = S[sid]; shifts.append((old["b"], (b - a) - (old["b"] - old["a"]), old["a"], sid, f, a, b))
shifts.sort()
def v3(t):
    d = 0.0
    for after, delta, *_ in shifts:
        if t >= after - 1e-6: d += delta
    return round(t + d, 3)
json.dump([{"sid": s[3], "v2_start": s[2], "v2_end": s[0], "delta": round(s[1], 3), "file": s[4], "trim": [s[5], s[6]]} for s in shifts],
          open("work/timeline_v3_shift.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
TOTAL = v3(m2["total"])

# ---- all words with v3 times ----
W = []
for c in tl["chapters"]:
    for seg in c["segments"]:
        for w, a, b in seg.get("word_times") or []:
            W.append({"w": w, "a": v3(rm2(a)), "b": v3(rm2(b))})
for sid, (f, a, b, words) in FIX.items():
    st = v3(S[sid]["a"]); en = v3(S[sid]["a"]) + (b - a)
    W = [w for w in W if not (st - 0.01 <= w["a"] < en - 0.01)]
    W += [{"w": w, "a": round(st + (x - a), 3), "b": round(st + (y - a), 3)} for w, x, y in words]
W.sort(key=lambda w: w["a"])

MISSING = []
def link(src, sub=""):
    src = Path(src)
    name = src.name if sub in ("clips", "logos", "channel", "evidence", "avatar_gen", "avatar_real", "avatar_orig") else f"{src.parent.name}__{src.name}"
    dst = PUB / sub / name; dst.parent.mkdir(parents=True, exist_ok=True)   # same file name in two folders = two different pictures
    if not src.exists():
        MISSING.append(str(src)); return f"projects/aiworld/v3/{sub + '/' if sub else ''}{name}"
    if not dst.exists():
        try: os.link(src, dst)
        except OSError: shutil.copy2(src, dst)
    return f"projects/aiworld/v3/{sub + '/' if sub else ''}{name}"

LOGOS = {  # spoken name -> logo file (official, brand/logos-tools)
    "Seedance": "seedance.ico", "Kling": "kling.png", "Veo": "veo.ico", "Wan": "wan.ico", "MiniMax": "minimax.ico", "Higgsfield": "higgsfield.png",
    "HeyGen": "heygen.ico", "ElevenLabs": "elevenlabs.png", "Suno": "suno.png", "Claude": "claude.svg", "Codex": "openai-codex.png",
    "OpenAI": "openai.png", "Antigravity": "antigravity.png", "Gemini": "gemini.png", "Nano Banana": "gemini.png", "GPT Image": "openai.png",
    "Seedream": "seedance.ico", "Genjutsu": "higgsfield.png", "Soul ID": "higgsfield.png", "Blender": "blender.svg", "three.js": "threejs.ico",
    "Whisper": "whisper.png", "HyperFrames": "hyperframes.ico", "Remotion": "remotion.png", "ffmpeg": "ffmpeg.ico", "ComfyUI": "comfyui.png",
    "LTX": "ltx.png", "Flux": "flux.png", "Qwen": "qwen.png", "Kimi": "kimi.ico", "DeepSeek": "deepseek.ico", "GLM": "glm.png",
    "ByteDance": "bytedance.png", "Ollama": "ollama.png", "LM Studio": "lmstudio.ico", "Firefly": "firefly.png", "Runway": "runway.png",
    "Luma": "luma.ico", "CapCut": "capcut.ico", "After Effects": "adobe.png", "Premiere": "premiere-pro-official.png", "Photoshop": "adobe.png",
    "DaVinci": "davinci-resolve.png", "Warner": "warner.png", "BMG": "bmg.ico", "Believe": "believe.png", "يوتيوب": "youtube.png",
    "YouTube": "youtube.png", "Meta": "meta.png", "تيك توك": "tiktok.png", "إنستجرام": "instagram.ico", "فيسبوك": "facebook.png",
    "SynthID": "synthid.ico", "C2PA": "c2pa.svg", "Scribe": "elevenlabs.png", "Python": "python.ico", "PowerShell": None, "MCP": None}
EMO = [("صورة", "🖼️"), ("صور", "🖼️"), ("فيديو", "🎬"), ("صوت", "🎙️"), ("مزيكا", "🎵"), ("ثري دي", "🧊"), ("3D", "🧊"), ("كود", "💻"),
       ("مفتاح", "🔑"), ("قفل", "🔒"), ("موافقة", "✍️"), ("فلوس", "💰"), ("دولار", "💵"), ("$", "💵"), ("كريدت", "🪙"), ("ساعة", "⏰"),
       ("نايم", "🌙"), ("متصفح", "🌐"), ("ماوس", "🖱️"), ("كيبورد", "⌨️"), ("ملف", "📄"), ("كتاب", "📘"), ("كراسة", "📒"), ("فكرة", "💡"),
       ("ذوق", "🎨"), ("مراجعة", "🔍"), ("مصادر", "📚"), ("مسؤولية", "🛡️"), ("عين", "👁️"), ("ودن", "👂"), ("لافتة", "🪧"), ("تكبير", "🔎"),
       ("خلفية", "✂️"), ("لوجو", "🔷"), ("ثمبنيل", "🖼️"), ("قص", "✂️"), ("شابترز", "📑"), ("فيشة", "🔌"), ("سلك", "🔌"), ("كاميرا", "🎥"),
       ("عدسة", "🔭"), ("إضاءة", "💡"), ("حركة", "🏃"), ("تطويل", "⏩"), ("4K", "📺"), ("fps", "🎞️"), ("مؤثرات", "💥"), ("دوشة", "🔇"),
       ("الإنسان", "🧑"), ("إيد", "✋"), ("✓", "✅"), ("LoRA", "🧬"), ("مرجع", "📌"), ("OCR", "🔤"), ("وصف", "📝"), ("تحليل", "📊")]
def emoji(s):
    for k, e in EMO:
        if k in s: return e
    return "✦"

EVID = {p.stem: p for p in Path("research/evidence_shots_v1").glob("*.png")}
CH = {c: f"assets/channel/thumb_{c}.jpg" for c in ["H5oOZypINf0", "PJTcdeSiDUI", "10UXB0cT4Ss", "8d4jkySoXe4", "ZXQLSxYmLsw", "Ps7A-UXx-5g"]}
VT = {"H5oOZypINf0": "عايز تبدأ تعمل فيديوهات AI؟ شوف ده الأول", "PJTcdeSiDUI": "الفيلم القصير اللي اتعمل بالـ AI",
      "10UXB0cT4Ss": "إزاي تعمل فيديو AI زي المحترفين وتعرف هيكلفك كام؟", "8d4jkySoXe4": "Genjutsu", "ZXQLSxYmLsw": "شيل الصمت بضغطة",
      "Ps7A-UXx-5g": "الـ AI جوه فوتوشوب"}
HF = json.load(open("assets/ai/higgsfield/clips_v1/clips_v1.json", encoding="utf-8"))
AVC = {x["n"]: x for x in json.load(open("assets/ai/heygen/avatar_clips_v1/avatar_clips_v1.json", encoding="utf-8"))}
METH = {int(k): v for k, v in json.load(open("work/avatar_methods_v3.json", encoding="utf-8"))["methods"].items()}
AVW = {x["n"]: (x["start"], x["start"] + x["dur"]) for x in m2["shots"] if x["type"] == "B"}
FAM_WORDS = ["التوليد", "LLMs", "السكريبتات", "MCP", "skills", "الإنسان"]

def words_in(a, b): return [w for w in W if a - 0.02 <= w["a"] < b - 0.02]
def logos_in(a, b):
    out, seen = [], set()
    ws = words_in(a, b)
    for name, f in LOGOS.items():
        if not f or name in seen: continue
        for w in ws:
            if name.split()[0].lower() in w["w"].lower():
                if name == "Claude" and any(x in w["w"] for x in ("Code",)): pass
                out.append({"t": w["a"], "logo": link(LOG / f, "logos"), "label": name}); seen.add(name); break
    return sorted(out, key=lambda x: x["t"])
def parts(d):
    d = d.split(":", 1)[1] if ":" in d and d.index(":") < 40 else d
    return [x.strip(" .«»") for x in re.split(r"\s/\s|،\s(?=\S+\s?=)", d) if x.strip()]
def spread(n, a, b, lead=0.4):
    if n <= 0: return []
    step = max(0.6, (b - a - lead - 0.8) / max(1, n))
    return [round(a + lead + i * step, 2) for i in range(n)]
def quoted(d):
    q = re.findall(r"«([^»]+)»", d); return q[0] if q else None
def clip_file(n):
    f = HF[str(n)]["file"]; return link(Path("assets/ai/higgsfield/clips_v1") / f, "clips"), HF[str(n)]["dur"]
def avatar_src(n, method):
    f = AVC[n]["file"]
    if method == "real": return link(Path("assets/ai/heygen/avatar_clips_v3_real") / f, "avatar_real")
    if method == "orig": return link(Path("assets/ai/heygen/avatar_clips_v1") / f, "avatar_orig")
    return link(Path("assets/ai/heygen/avatar_clips_v2_gen") / f, "avatar_gen")

sys.path.insert(0, "work/scripts")
from plan_v3_content import C as CONTENT
def anchor_t(word, a, b, used):
    for w in words_in(a - 0.3, b):
        if word and word in w["w"] and (word, w["a"]) not in used:
            used.add((word, w["a"])); return w["a"]
    return None
def apply_content(sc, key, a, b):
    c = CONTENT.get(key)
    if c is None: return sc
    for f in ("title", "url", "fx"):
        if f in c: sc[f] = c[f]
    if "items" in c:
        its, used, n = [], set(), len(c["items"])
        fall = spread(n, a, b)
        for i, (anc, it) in enumerate(c["items"]):
            t = anchor_t(anc, a, b, set()) if anc else None
            it = dict(it); it["t"] = round(t if t is not None else fall[i], 3)
            if "logo" in it: it["logo"] = link(LOG / LOGOS[it["logo"]], "logos")
            if "img" in it: it["img"] = link(it["img"], "imgs")
            if "before" in it: it["before"] = link(it["before"], "imgs")
            its.append(it)
        sc["items"] = sorted(its, key=lambda x: x["t"])
    if "clips" in c:
        ts = []
        for i, (n, anc) in enumerate(c["clips"]):
            t = anchor_t(anc, a, b, set()) if anc else None
            ts.append(a if i == 0 else (t if t is not None else a + (b - a) * i / len(c["clips"])))
        sc["clips"] = []
        for i, (n, _) in enumerate(c["clips"]):
            src, cd = clip_file(n); end = ts[i + 1] if i + 1 < len(ts) else b
            sc["clips"].append({"src": src, "from": round(ts[i], 3), "dur": round(min(end - ts[i], cd - 0.1), 3), "skip": 0.05})
        if sc["clips"]:   # a clip shorter than its slot: the next one starts right away (no freeze)
            for i in range(len(sc["clips"]) - 1):
                sc["clips"][i + 1]["from"] = round(sc["clips"][i]["from"] + sc["clips"][i]["dur"], 3)
    return sc

till = float(sys.argv[sys.argv.index("--till") + 1]) if "--till" in sys.argv else 1e9
scenes, hud, fam_seen = [], [], False
for r in plan:
    a, b = v3(r["start"]), v3(r["end"])
    if a >= till: break
    b = min(b, till)
    k, d = r["k"], r["d"]
    sc = {"k": k, "start": a, "dur": round(b - a, 3), "items": [], "clips": [], "imgs": []}
    lg = logos_in(a, b)
    if k == "AV":
        n = r["av"]; wa, wb = AVW[n]; wa, wb = v3(wa), v3(wb)
        if n == 1:   # opening: 0 real room -> glitch -> 2 real face -> glitch -> 1 generated (Aly 2026-11-21)
            segs = [("orig", 0.0, 1.6), ("real1", 1.6, 3.2), ("gen1", 3.2, sc["dur"])]
            files = {"orig": link("assets/ai/heygen/avatar_clips_v1/avatar_001_C00.mp4", "avatar_orig"),
                     "real1": link("assets/ai/heygen/look_S4g/ex_real.mp4", "avatar_real"), "gen1": link("assets/ai/heygen/look_S4g/ex_generated.mp4", "avatar_gen")}
            sc["clips"] = [{"src": files[s], "from": round(a + x, 3), "dur": round(y - x, 3), "skip": x} for s, x, y in segs]
            sc["items"] = [{"t": w["a"], "label": l, "emoji": e} for w in words_in(a, b + 3)
                           for key, l, e in (("الوش", "الوش", "🙂"), ("والصوت", "الصوت", "🎙️"), ("والمكان", "المكان", "🏛️")) if w["w"].startswith(key)]
        else:
            sc["clips"] = [{"src": avatar_src(n, METH.get(n, "gen")), "from": a, "dur": sc["dur"], "skip": round(a - wa, 3)}]
            sc["items"] = lg or [{"t": round(a + 0.6, 2), "label": p, "emoji": emoji(p)} for p in parts(d)[:3]]
    elif k == "CLIP":
        ids = r.get("clip", []); t = a; i = 0
        while t < b - 0.3 and i < len(ids) * 2:
            src, cd = clip_file(ids[i % len(ids)])
            if i >= len(ids): break           # never repeat a clip (no jump back)
            slot = (b - a) / len(ids) if len(ids) > 1 else (b - a)
            dd = min(cd - 0.1, slot, b - t)
            sc["clips"].append({"src": src, "from": round(t, 3), "dur": round(dd, 3), "skip": 0.05, "label": quoted(d) if i == 0 else None})
            t += dd; i += 1
        sc["items"] = lg
        if t < b - 0.3:   # clip shorter than the sentence: the rest becomes a KT beat (no freeze, no slow-motion)
            scenes.append({**sc, "dur": round(t - a, 3)})
            sc = {"k": "KT", "start": round(t, 3), "dur": round(b - t, 3), "title": quoted(d) or d.split("=")[0].strip(" «»"),
                  "items": logos_in(t, b) or [], "clips": [], "imgs": []}
    elif k == "MAP6":
        hi = re.search(r"قطعة (\d)", d)
        if not fam_seen and not hi:
            ws = words_in(a, b)
            for fw in FAM_WORDS:
                w = next((w for w in ws if fw in w["w"]), None)
                sc["items"].append({"t": w["a"] if w else a + 1})
            fam_seen = True
        else:
            sc["hud"] = int(hi[1]) - 1 if hi else 5
            sc["title"] = quoted(d)
        if r.get("clip"):
            src, cd = clip_file(r["clip"][0]); sc["clips"] = []
    elif k in ("LOGOS",):
        sc["items"] = [{**x, "sub": None} for x in lg] or [{"t": tt, "label": p, "emoji": emoji(p)} for p, tt in zip(parts(d), spread(len(parts(d)), a, b))]
        sc["title"] = quoted(d)
    elif k in ("KT", "ICON", "NUM"):
        ps = parts(d)
        its = []
        for p_, tt in zip(ps, spread(len(ps), a, b)):
            num = re.search(r"(\$?\d[\d.,]*\s?(K|%|LUFS|ث)?|\+\d+)", p_)
            it = {"t": tt, "label": re.sub(r"\(.*?\)", "", p_).strip()[:40]}
            if k == "NUM" and num: it["num"] = num[1].strip(); it["label"] = it["label"].replace(num[1].strip(), "").strip(" =")
            else: it["emoji"] = emoji(p_)
            its.append(it)
        sc["items"] = sorted(its + lg, key=lambda x: x["t"])[:7]
        sc["title"] = None      # titles only from plan_v3_content (auto titles showed plan prose)
        if k == "KT" and len(ps) == 1: sc["items"] = lg
    elif k in ("WEB", "STEP"):
        names = [n for n in re.findall(r"[a-z0-9_]+", d) if n in EVID]
        for nm, tt in zip(names, spread(len(names), a, b, 0.0)):
            sc["items"].append({"t": tt, "img": link(EVID[nm], "evidence"), "label": None})
        sc["items"] += lg
        sc["url"] = (lg[0]["label"].lower().replace(" ", "") + ".com") if lg else ""
        sc["title"] = quoted(d)
        if k == "STEP":
            st = re.search(r"خطوة (\d+)", d); sc["step"] = st[1] if st else ""
            sc["title"] = re.sub(r"\(.*?\)", "", d.split(":", 1)[1] if ":" in d else d).strip()[:60]
    elif k == "VID":
        vids = r.get("vid") if isinstance(r.get("vid"), list) else [r.get("vid")]
        ts = spread(len(vids), a, b, 0.6)
        sc["items"] = [{"t": tt, "img": link(CH[v], "channel"), "qr": link(f"assets/channel/qr_{v}.png", "channel"), "label": VT[v]} for v, tt in zip(vids, ts)]
        if "av" in r:
            n = r["av"]; wa, _ = AVW[n]
            sc["clips"] = [{"src": avatar_src(n, METH.get(n, "gen")), "from": a, "dur": sc["dur"], "skip": round(a - v3(wa), 3)}]
    elif k == "FLOW":
        ps = [x.strip(" .") for x in re.split(r"←", re.sub(r"\(.*?\)", "", d.split(":", 1)[-1])) if x.strip()]
        sc["items"] = [{"t": tt, "label": p_[:28], "emoji": emoji(p_)} for p_, tt in zip(ps, spread(len(ps), a, b))]
    elif k == "SPLIT":
        ps = [x.strip(" .") for x in re.split(r"←| vs ", re.sub(r"\(.*?\)", "", d.split(":", 1)[-1])) if x.strip()][:2]
        sc["items"] = [{"t": a, "label": p_[:30]} for p_ in ps]
        for n in r.get("clip", [])[:2]:
            src, cd = clip_file(n); sc["clips"].append({"src": src, "from": a, "dur": sc["dur"], "skip": 0.05})
        sc["title"] = quoted(d)
    elif k == "BTS":
        ps = parts(d)
        imgs = []
        if "وش" in d: imgs = ["output/keyframes_v2_test_compare.jpg", "output/keyframes_v4_test_compare.jpg", "output/keyframes_v6_test.jpg"]
        elif "diffusion" in d or "دوشة" in d: imgs = ["assets/ai/higgsfield/keyframes_final/kf_006_C01.png"]
        elif "looks" in d: imgs = ["output/keyframes_final_sheet.jpg"]
        elif "ستوديو" in d or "الستوديو" in d: imgs = ["output/studio_look_v6_S4.jpg", "output/studio_look_v9_mashrabiya.jpg"]
        elif "تجارب" in d: imgs = ["output/avatar_clips_v1_sheet.jpg"]
        elif "blockout" in d: imgs = ["output/clips_v1_sheet.jpg"]
        imgs = [x for x in imgs if Path(x).exists()]
        sc["items"] = [{"t": tt, "img": link(x, "bts"), "label": (ps[i] if i < len(ps) else "")[:50]} for i, (x, tt) in enumerate(zip(imgs, spread(len(imgs), a, b, 0.2)))]
        if not imgs:
            sc["items"] = [{"t": tt, "label": p_[:40], "emoji": emoji(p_)} for p_, tt in zip(ps, spread(len(ps), a, b))]
        sc["items"] += lg
        for n in r.get("clip", [])[:1]:
            src, cd = clip_file(n); sc["clips"].append({"src": src, "from": a, "dur": min(cd - 0.1, sc["dur"]), "skip": 0.05})
    elif k == "LYR":
        lines = json.load(open("work/song_C1_lines.json", encoding="utf-8"))
        s0 = v3(S0)
        LMAP = [("الجدار", 186), ("فحمة", 186), ("تور", 186), ("حبر", 189), ("دماغي", 192), ("mouse", 195), ("Photoshop", 195), ("rendering", 198),
                ("frame", 198), ("جملة", 201), ("صوت", 204), ("agents", 213), ("MCP", 213), ("الآلة", 201), ("بتجري", 204), ("هي بترسم", 192),
                ("بترسم", 192), ("غيّر", 183), ("بس اللي", 207), ("الفحمة", 210), ("الإيد", 186), ("الفيديو", 216), ("الحلم", 171), ("أنا", 186),
                ("اتغيرت", 189), ("وعيني", 192), ("قالوا", 201), ("قلت", 168)]
        POOL = [183, 207, 210, 204, 216, 171, 201, 213, 192, 189, 195, 198, 6, 26, 99, 115, 162]
        if not r.get("song"):     # the short teaser in C02e: its clip + the first song line, whole scene
            src, cd = clip_file((r.get("clip") or [186])[0])
            sc["clips"] = [{"src": src, "from": a, "dur": round(min(cd - 0.1, b - a), 3), "skip": 0.05}]
            if cd - 0.1 < b - a:
                src2, _ = clip_file(189); sc["clips"].append({"src": src2, "from": round(a + cd - 0.1, 3), "dur": round(b - a - cd + 0.1, 3), "skip": 0.05})
            ws = lines[1]["t"].split(); sc["items"] = [{"t": a + 0.3, "sub": str(b)}]
            sc["words"] = [{"t": round(a + 0.3 + j * 0.35, 3), "w": w} for j, w in enumerate(ws)]
        else:
            # every moment of the song is covered: each line gets its clip from the line start; when a clip runs out the
            # next clip of the pool continues (no freeze, no slow-motion, no clip twice in a row)
            marks = [(s0 + ln["a"], ln) for ln in lines]
            t, prev, pi = a, None, 0
            for i, (la, ln) in enumerate(marks):
                lb = marks[i + 1][0] if i + 1 < len(marks) else b
                if i == 0: la = a
                n = next((n for key, n in LMAP if key in ln["t"]), POOL[pi % len(POOL)])
                t = la
                while t < min(lb, b) - 0.05:
                    if n == prev: pi += 1; n = POOL[pi % len(POOL)]
                    src, cd = clip_file(n); dd = min(cd - 0.15, min(lb, b) - t)
                    sc["clips"].append({"src": src, "from": round(t, 3), "dur": round(dd, 3), "skip": 0.05})
                    t += dd; prev = n; pi += 1; n = POOL[pi % len(POOL)]
                lb_txt = (marks[i + 1][0] if i + 1 < len(marks) else s0 + 189.68)
                sc["items"].append({"t": round(s0 + ln["a"], 3), "sub": str(round(lb_txt, 3))})
                ws = ln["t"].split(); dur = ln["b"] - ln["a"]
                for j, w in enumerate(ws):
                    sc.setdefault("words", []).append({"t": round(s0 + ln["a"] + j * dur / max(1, len(ws)), 3), "w": w})
            if t < b - 0.05:       # after the last line until the scene end
                src, cd = clip_file(216); sc["clips"].append({"src": src, "from": round(t, 3), "dur": round(min(cd - 0.15, b - t), 3), "skip": 0.05})
    if k != "LYR":
        sc["words"] = []
    key = r.get("at") or (f"av{r['av']}" if "av" in r else None)
    if sc["start"] == a:
        sc = apply_content(sc, key, a, b)
    elif scenes and scenes[-1]["start"] == a:     # CLIP split into CLIP + KT: content goes on the CLIP part
        scenes[-1] = apply_content(scenes[-1], key, a, b)
    end_clips = max([c["from"] + c["dur"] for c in sc["clips"]] or [0])
    if sc["k"] == "CLIP" and end_clips < sc["start"] + sc["dur"] - 0.3:   # clips end early -> KT on the rest
        rest_a = round(end_clips, 3)
        scenes.append({**sc, "dur": round(rest_a - sc["start"], 3)})
        sc = {"k": "KT", "start": rest_a, "dur": round(sc["start"] + sc["dur"] - rest_a, 3), "title": None,
              "items": [x for x in sc["items"] if x["t"] >= rest_a - 0.2] or sc["items"][-1:], "clips": [], "imgs": [], "words": []}
    scenes.append(sc)
    # HUD: from the first MAP6 on, the current family stays lit top-right (note 6)
    hi = re.search(r"قطعة (\d)", d)
    if hi: hud.append({"a": a, "i": int(hi[1]) - 1})
hud_r = [{"a": h["a"], "b": (hud[i + 1]["a"] if i + 1 < len(hud) else v3(S0)), "i": h["i"]} for i, h in enumerate(hud)]
dur = min(TOTAL, till)
props = {"fps": 25, "duration": round(dur, 3), "outW": 1280, "scenes": scenes, "hud": hud_r}
out = "work/props_v3.json" if till > 1e8 else f"work/props_v3_till{int(till)}.json"
json.dump(props, open(out, "w", encoding="utf-8"), ensure_ascii=False)
json.dump(W, open("work/words_v3.json", "w", encoding="utf-8"), ensure_ascii=False)
print(out, len(scenes), "scenes, total", TOTAL, "shift", [round(s[1], 2) for s in shifts], "| missing media:", len(set(MISSING)), sorted(set(MISSING))[:6])

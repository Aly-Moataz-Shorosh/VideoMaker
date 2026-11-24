"""Props for 'ai-world-v9' = v8 + Aly's v8 notes (v9_new.py, kids on the separators, the 1:02 board waits for the face shot). Was: Props for 'ai-world-v8' = v6 builder + Aly's v6 notes (faces back between the boards, held boards, MAP6 merged, song shot per line,
whole logos + our subscribe_press). Was: props for 'ai-world-v5' (v4 builder + v5_specs explaining scenes). Was: props for 'ai-world-v4' (Aly's v3 notes 1-16): every element = an enta board item (the «انت بتشتغل ايه» kit) placed by meaning,
ENTERING on its word and LEAVING smoothly; captions = the script on its word times; times = timeline v4 (make_timeline_v4.py).
Usage (project folder): python -X utf8 work/scripts/make_props_v8.py [--till SECONDS]"""
import json, subprocess, os, re, shutil, sys, unicodedata
from pathlib import Path

P = Path(__file__).resolve().parents[2]; os.chdir(P)
VM = P.parents[1]; PUB = VM / "motion-library" / "public" / "projects" / "aiworld" / "v6"; PUB.mkdir(parents=True, exist_ok=True)
LOG = VM / "brand" / "logos-tools"; FL = VM / "motion-library" / "public" / "fluent"
sys.path.insert(0, "work/scripts")
from plan_v3_content import C
from plan_v4_content import C4
C = {**C, **C4}
plan = json.load(open("work/plan_v3.json", encoding="utf-8"))
T4 = json.load(open("work/timeline_v9.json", encoding="utf-8")); PIECES = T4["pieces"]; ED = []
W = json.load(open("work/words_v9.json", encoding="utf-8"))
m2 = json.load(open("work/rough_v2_map.json", encoding="utf-8"))
S0v4, TOTAL = T4["song_start_v6"], T4["total"]
FPS = 25

def v4(t):
    """v2 (source) time -> v6 time (pieces in the new order). Re-voiced sentences map linearly onto their file piece.
    A time that was dropped maps to the end of the nearest earlier kept piece (only used for anchors)."""
    for p in PIECES:
        if p["kind"] == "v2" and p["a"] - 1e-6 <= t <= p["b"] + 1e-6: return round(p["t"] + t - p["a"], 3)
        if p["kind"] == "file" and p.get("rep") and p["rep"][0] - 1e-6 <= t <= p["rep"][1] + 1e-6:
            r0, r1 = p["rep"]; return round(p["t"] + (t - r0) / max(0.01, r1 - r0) * (p["b"] - p["a"]), 3)
    return None
def split_row(r0, r1):
    """one plan row (v2 [r0, r1]) -> its parts in v6: [(a6, b6, t2a)] — a row can be split by the new order"""
    out = []
    for p in PIECES:
        if p["kind"] == "v2":
            lo, hi = max(r0, p["a"]), min(r1, p["b"])
            if hi - lo > 0.15: out.append((round(p["t"] + lo - p["a"], 3), round(p["t"] + hi - p["a"], 3), lo))
        elif p["kind"] == "file" and p.get("rep"):
            q0, q1 = p["rep"]; lo, hi = max(r0, q0), min(r1, q1)
            if hi - lo > 0.15:
                f = (p["b"] - p["a"]) / max(0.01, q1 - q0)
                out.append((round(p["t"] + (lo - q0) * f, 3), round(p["t"] + (hi - q0) * f, 3), lo))
    return out

MISSING = []
def link(src, sub):
    src = Path(src)
    name = src.name if sub in ("clips", "logos", "channel", "avatar_gen", "avatar_real", "avatar_orig") else f"{src.parent.name}__{src.name}"
    dst = PUB / sub / name; dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists(): MISSING.append(str(src))
    elif not dst.exists():
        try: os.link(src, dst)
        except OSError: shutil.copy2(src, dst)
    return f"projects/aiworld/v6/{sub}/{name}"

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
push_to = 0.0; pull_to = None; SUBP = None
CUTS = []
pending = []   # items whose word is said in a LATER scene -> shown there, on their word (note 6)
till = float(sys.argv[sys.argv.index("--till") + 1]) if "--till" in sys.argv else 1e9
scenes, hud = [], []
fam_done = False
ROWS6 = sorted([(a6, b6, t2a, r) for r in plan for a6, b6, t2a in split_row(r["start"], r["end"])], key=lambda x: x[0])
for a, b, t2a, r in ROWS6:
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
        n = r["av"]; wa = AVW[n][0]   # v2 time: the clip frame = the voice second it was made from (lip sync kept in any order)
        if n == 1:   # opening 0 -> 2 -> 1 with the SHOW's glitch (note 2)
            fs = {"orig": link("assets/ai/heygen/avatar_clips_v1/avatar_001_C00.mp4", "avatar_orig"), "real1": link("assets/ai/heygen/look_S4g/ex_real.mp4", "avatar_real"),
                  "gen1": link("assets/ai/heygen/look_S4g/ex_generated.mp4", "avatar_gen")}
            sc["clips"] = [{"src": fs[s], "from": round(a + x, 3), "dur": round(y - x, 3), "skip": x} for s, x, y in [("orig", 0, 1.6), ("real1", 1.6, 3.2), ("gen1", 3.2, b - a)]]
            sc["glitch"] = [a + 1.6, a + 3.2]
        else:
            sc["clips"] = [{"src": avatar_src(n, METH.get(n, "gen")), "from": a, "dur": round(b - a, 3), "skip": round(t2a - wa, 3)}]
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
        # notes 48-50: NO clip twice in the song; the new generated shots on their words; his logo; subscribe on the last line
        V6C = "assets/ai/higgsfield/clips_v6/"
        EXTRA = {"charcoal": V6C + "song_charcoal.mp4", "bull": V6C + "song_stoneage_bull.mp4", "mouse": V6C + "song_layers_mouse.mp4",
                 "render": V6C + "song_rendering_night.mp4", "market": V6C + "t2v_cairo_market.mp4", "jet3d": V6C + "jet_from_image_turntable.mp4"}
        def any_clip(n):
            if n in EXTRA:
                f_ = Path(EXTRA[n]); return link(f_, "clips"), float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f_)], capture_output=True, text=True).stdout)
            return clip_file(n)
        ORDER = [186, "charcoal", "bull", 189, 192, 195, 22, 28, 19, 115, 117, 210, "mouse", 25, 198, "render", 31, "market", 26, 29, 32, 53, 56, 207, 99, 102, 105,
                 112, 6, 9, 201, 204, 213, 171, 216, 183, "jet3d", 162, 165, 168, 901, 902, 903]
        LMAP = [("الجدار", 186), ("فحمة", "charcoal"), ("تور", "bull"), ("حبر", 189), ("دماغي", 192), ("mouse", "mouse"), ("Photoshop", 25), ("rendering", "render"),
                ("frame", 31), ("جملة", "market"), ("صوت", 183), ("agents", 99), ("MCP", 112), ("قالوا", 105), ("الآلة إيد", 102), ("بتجري", 204), ("بترسم", 22),
                ("الفيديو", 216), ("الحلم", 171)]
        used = set()
        RES = {n_ for _, n_ in LMAP}   # a line's own shot is kept for that line
        def take(pref):
            if pref is not None and pref not in used: used.add(pref); return pref
            for n_ in ORDER:
                if n_ not in used and n_ not in RES: used.add(n_); return n_
            for n_ in ORDER:
                if n_ not in used: used.add(n_); return n_
            return None
        if r.get("song"):
            # v7 note 19: a shot chosen for EACH line by what the line says (song time, s from the song start); every shot used once
            SONGPLAN = [(0, 213), (3.1, 115), (7.5, 186), (11.7, 28), (14.7, 192), (18.5, 117), (22.2, "charcoal"), (27.4, "bull"), (33.2, 189), (38.9, 195),
                        (44.1, 198), (49.5, 26), (55.0, 53), (60.2, 22), (63.6, 210), (67.0, "mouse"), (71.9, 25), (77.9, "render"), (83.1, 31), (86.4, 207),
                        (89.6, "market"), (92.5, 183), (95.3, 99), (98.1, 112), (101.9, 902), (106.7, 201), (112.8, "jet3d"), (118.0, 6), (121.3, 9), (124.5, 105),
                        (130.0, 102), (132.8, 32), (135.7, 204), (141.3, 19), (147.0, 162), (152.4, 29), (157.8, 56), (162.9, 168), (167.2, 903), (171.4, 216),
                        (176.3, 171), (181.8, 901)]
            assert len({n for _, n in SONGPLAN}) == len(SONGPLAN), "a shot twice in the song"
            for i, (st, n) in enumerate(SONGPLAN):
                t0 = a if i == 0 else S0v4 + st
                t1 = (S0v4 + SONGPLAN[i + 1][0]) if i + 1 < len(SONGPLAN) else b
                src, cd = any_clip(n); avail = cd - 0.15; L = t1 - t0
                rate = 1.0 if L <= avail else round(avail / L, 3)   # a line longer than its shot: the shot plays a bit slower (never a freeze, never a repeat)
                sc["clips"].append({"src": src, "from": round(t0, 3), "dur": round(L, 3), "skip": 0.05, "rate": rate})
            for i, ln in enumerate(lines):
                endl = (S0v4 + lines[i + 1]["a"]) if i + 1 < len(lines) else S0v4 + 189.68
                sc["items"].append({"k": "line", "t": round(S0v4 + ln["a"], 3), "end": round(endl, 3)})
                ws = ln["t"].split(); dd2 = ln["b"] - ln["a"]
                sc["words"] += [{"t": round(S0v4 + ln["a"] + j * dd2 / max(1, len(ws)), 3), "w": w} for j, w in enumerate(ws)]
            used = {n for _, n in SONGPLAN}; reuse = 0
            sc["items"].append({"k": "brand", "face": link(Path("assets/v7/logo_face_full.png"), "imgs"), "name": "brand/signature-calligraphy.png",
                                "handles": [{"logo": link(Path("../../brand/logos-tools/" + l_), "logos"), "t": t_} for l_, t_ in
                                            [("youtube.png", "@AlyShorosh"), ("tiktok.png", "@alyshorosh"), ("instagram.ico", "@alyshorosh"), ("facebook.png", "aly.shorosh")]]})   # v8 notes 51, 52
            tl = next(S0v4 + ln["a"] for ln in lines if "بني آدم" in ln["t"])
            sc["items"].append({"k": "subscribe", "at": int(round((tl - a) * FPS)), "yt": link(Path("../../brand/logos-tools/youtube.png"), "logos"),
                                "logos": [link(Path("../../brand/logos-tools/" + f_), "logos") for f_ in ["youtube.png", "tiktok.png", "instagram.ico", "facebook.png"]],
                                "handles": ["@AlyShorosh", "@alyshorosh", "@alyshorosh", "aly.shorosh"]})   # note 20: the channel names; the press = our subscribe_press
            SUBP = {"from": round(tl, 3), "dur": round(min(6.0, b - tl), 3)}
            print("song clips:", len(sc["clips"]), "unique", len(used), "reused", reuse)
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
        raw = [(anc, {"label": it.get("label"), "pos": (960, 905)})]
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

for p in PIECES:
    if p["kind"] == "gap":
        scenes.append({"k": "SEP", "start": p["t"], "dur": p["dur"], "title": None, "clips": [], "items": [{"k": "sep", "fam": p["sep"][0], "name": p["sep"][1]}],
                       "words": [], "glitch": [], "fam": [], "fx": None})
    elif p.get("new"):
        scenes.append({"k": "BOARD", "start": p["t"], "dur": round(p["b"] - p["a"], 3), "title": None, "clips": [], "items": [], "words": [], "glitch": [], "fam": [], "fx": None})
scenes.sort(key=lambda x: x["start"])
mm = []
for x in scenes:
    if mm and x["k"] == "SPLIT" and mm[-1]["k"] == "SPLIT" and x["start"] - (mm[-1]["start"] + mm[-1]["dur"]) < 0.8 \
            and [d.get("cap") for d in x["items"]] == [d.get("cap") for d in mm[-1]["items"]]:
        mm[-1]["dur"] = round(x["start"] + x["dur"] - mm[-1]["start"], 3); continue
    if mm and x["k"] == "MAP6" and mm[-1]["k"] == "MAP6" and x["start"] - (mm[-1]["start"] + mm[-1]["dur"]) < 0.8:
        mm[-1]["dur"] = round(x["start"] + x["dur"] - mm[-1]["start"], 3); continue
    mm.append(x)
scenes = mm
for x in scenes:
    if x["k"] == "MAP6" and x["start"] < 120:
        nums = ["واحد", "اتنين", "تلاتة", "أربعة", "خمسة", "وستة"]; aft = x["start"]; fam = []
        for nw in nums:
            t_ = next((w["a"] for w in W if w["a"] >= aft - 0.1 and w["a"] < x["start"] + x["dur"] + 3 and w["w"].startswith(nw)), None)
            if t_ is None: t_ = aft + 3
            fam.append(fr(t_, x["start"])); aft = t_ + 0.3
        x["fam"] = fam; x["hud"] = None
    elif x["k"] == "MAP6" and x["start"] > 1300:
        x["me"] = link("assets/v6/face_gen.jpg", "imgs")   # note 21: HIS picture, not the plane
        for n_, (wa_, wb_) in AVW.items():   # v8 note 54: him TALKING there (clip second = voice second)
            for p_ in PIECES:
                if p_["kind"] != "v2": continue
                t2_ = p_["a"] + (x["start"] - p_["t"])
                if p_["t"] <= x["start"] <= p_["t"] + p_["b"] - p_["a"] and wa_ <= t2_ <= wb_ - 1.0:
                    x["me"] = avatar_src(n_, METH.get(n_, "gen")); x["meSkip"] = round(t2_ - wa_, 3)
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
import v9_new as v5_specs, v5_apply
v5_apply.ENV = json.load(open("work/voice_env_v9.json"))
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
import v9_resolve   # GENERAL rule (Aly 2026-11-23): every card, hand-placed or not, never overlaps what is on screen with it
LEFT9 = v9_resolve.resolve_all(scenes)
print("v9 general overlap rule: could not place", len(LEFT9), LEFT9[:8])
VIS = lambda d: d["k"] not in ("titleAt", "line", "brand", "subscribe")
for x, y in zip(scenes, scenes[1:]):
    if y["k"] not in ("BOARD",) or x["k"] not in ("BOARD", "WEB", "SPLIT") or not y["items"]: continue
    first = min((d["at"] for d in y["items"] if VIS(d) and "at" in d), default=0)
    if first < 15: continue
    df = first - 4; dt = round(df / FPS, 3)
    old_end = int(x["dur"] * FPS) - 12
    x["dur"] = round(x["dur"] + dt, 3); new_end = int(x["dur"] * FPS) - 12
    for d in x["items"]:
        if d.get("out") is not None and d["out"] >= old_end - 15: d["out"] = new_end
    y["start"] = round(y["start"] + dt, 3); y["dur"] = round(y["dur"] - dt, 3)
    v5_apply.shift_items(y, -df)
    for d in y["items"]:
        if d["k"] == "titleAt": d["at"] = max(0, d["at"])
# v6 review: never a blank board in the middle — when a group leaves before the next one arrives, it stays until the next one comes
NOCOUNT = ("titleAt", "line", "brand", "subscribe", "circle")
for x in scenes:
    if x["k"] not in ("BOARD",): continue
    end = int(x["dur"] * FPS) - 12
    its = [d for d in x["items"] if "at" in d and d["k"] not in NOCOUNT]
    if len(its) < 2: continue
    for _ in range(3):
        cov = sorted((d["at"], (d["out"] if d.get("out") is not None else end) + 10, id(d)) for d in its)
        reach = cov[0][1]; changed = False
        for a_, b_, _ in cov[1:]:
            if a_ > reach + 12:   # blank from reach to a_: the items that just left stay until a_
                for d in its:
                    o_ = d["out"] if d.get("out") is not None else end
                    if reach - 12 <= o_ + 10 <= reach + 1: d["out"] = a_ - 2; changed = True
            reach = max(reach, b_)
        if not changed: break
FACES = []
import v5_boxes as VB
SPOTS = [(960, 250), (250, 260), (1670, 260), (250, 820), (1670, 820), (960, 820)]
def _busy(a7, d7, spot, r=105):
    sx, sy = spot; me_ = (sx - r - 20, sy - r - 20, sx + r + 20, sy + r + 20)
    for x in scenes:
        if not (x["start"] < a7 + d7 and x["start"] + x["dur"] > a7): continue
        end = int(x["dur"] * FPS)
        for d in x["items"]:
            if "at" not in d: continue
            t0 = x["start"] + d["at"] / FPS; t1 = x["start"] + (d.get("out", end) + 10) / FPS
            if t1 < a7 or t0 > a7 + d7: continue
            if d["k"] == "titleAt" and x.get("title"):
                if VB.inter(me_, (960 - 400, 128, 960 + 400, 200)) > 0: return True
                continue
            for bx in VB.boxes(d, end):
                if VB.inter(me_, bx) > 0: return True
    return False
for n, (wa, wb) in sorted(AVW.items(), key=lambda kv: kv[1][0]):
    cand = None
    for p in PIECES:
        if p["kind"] != "v2": continue
        lo, hi = max(wa + 0.15, p["a"]), min(wb - 0.1, p["b"])
        if hi - lo >= 2.0: cand = (round(p["t"] + lo - p["a"], 3), round(p["t"] + hi - p["a"], 3), lo); break
    if not cand: continue
    a7, b7, lo = cand; d7 = round(min(4.0, b7 - a7), 3)
    cover = [x for x in scenes if x["start"] < a7 + d7 and x["start"] + x["dur"] > a7]
    if any(x["k"] in ("AV", "LYR", "SEP") or any(d["k"] == "circle" for d in x["items"]) or x.get("me") for x in cover): continue
    if any(f_["from"] < a7 + d7 and f_["from"] + f_["dur"] > a7 for f_ in FACES): continue
    plain = all(x["k"] == "CLIP" for x in cover) or n == 12   # note 4 (v6): HIS face full frame at 1:03, then back to the motion
    f_ = {"src": avatar_src(n, METH.get(n, "gen")), "from": a7, "dur": d7, "skip": round(lo - wa, 3), "n": n}
    if not plain:
        spot = next((sp for sp in SPOTS if not _busy(a7, d7, sp)), None)
        if spot is None: continue
        f_["circle"] = {"x": spot[0], "y": spot[1], "r": 95}
    else:
        for x in cover:   # a full-frame face over a plain clip: its chips (and the title) come right after it
            e7 = int(round((a7 + d7 - x["start"]) * FPS)); s7 = int(round((a7 - 0.1 - x["start"]) * FPS)); k_ = 0
            for d in sorted([d for d in x["items"] if "at" in d], key=lambda d: d["at"]):
                if s7 <= d["at"] < e7:
                    d["at"] = e7 + 3 * k_; k_ += 1
                    if d.get("out") is not None and d["out"] < d["at"] + 37: d["out"] = min(int(x["dur"] * FPS) - 2, d["at"] + 37)
    FACES.append(f_)
for f_ in FACES:
    if "circle" in f_: continue
    fe = f_["from"] + f_["dur"]
    for i_, x in enumerate(scenes):
        if x["k"] != "BOARD" or not (f_["from"] - 1.6 <= x["start"] < f_["from"]) or i_ == 0: continue
        pv = scenes[i_ - 1]; d_ = round(f_["from"] - x["start"], 3)
        pv["dur"] = round(pv["dur"] + d_, 3)
        if pv["clips"]: pv["clips"][-1]["dur"] = round(pv["clips"][-1]["dur"] + d_, 3)
        x["start"] = round(x["start"] + d_, 3); x["dur"] = round(x["dur"] - d_, 3); df_ = int(round(d_ * FPS))
        v5_apply.shift_items(x, -df_)
        e7 = int(round((fe - x["start"]) * FPS))
        for d in x["items"]:
            if "at" in d and d["at"] < e7:
                if d.get("out") is not None and d["out"] < e7 + 37: d["out"] = e7 + 37
                d["at"] = e7
        if x.get("title") and not any(d["k"] == "titleAt" for d in x["items"]): x["items"].append({"k": "titleAt", "at": e7})
        print("note 3: board at", x["start"], "waits for the face until", round(fe, 2))
print("faces:", len(FACES), round(sum(f_["dur"] for f_ in FACES), 1), "s + AV scenes", round(sum(x["dur"] for x in scenes if x["k"] == "AV"), 1), "s")
gaps = [p for p in PIECES if p["kind"] == "gap" and p["sep"][1] != "OPEN"]
SUBS = [{"a": p["t"], "fam": p["sep"][0], "name": p["sep"][1], "b": (gaps[i + 1]["t"] if i + 1 < len(gaps) else TOTAL)} for i, p in enumerate(gaps)]
for x in SUBS:
    if x["name"] in ("ElevenLabs", "Higgsfield", "Suno", "على جهازك ببلاش"): x["parent"] = "مواقع التوليد"
SFX = [("glitch", g) for sc in scenes for g in sc.get("glitch", [])] + [("whoosh_2", x["a"] + 0.1) for i, x in enumerate(SUBS)]
KIDS = json.load(open("assets/ai/elevenlabs/kids_v9/kids_index.json", encoding="utf-8"))["names"]   # v8 note 4: the kids shout the name we enter
SFX += [(f"kids9_{KIDS.index(p['sep'][1]):02d}", p["t"] + 0.35) for p in PIECES if p["kind"] == "gap"]
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
hud_r = [{"a": SUBS[0]["a"], "b": S0v4, "i": 0}] if SUBS else []
dur = min(TOTAL, till)
for c_ in caps:   # «3D» in English (note 5 / 28)
    c_["t"] = c_["t"].replace("الثري دي", "الـ 3D").replace("وثري دي", "و3D").replace("ثري دي", "3D")
    c_["t"] = re.sub(r"(?<![\w\u0600-\u06FF])و(?=[A-Za-z0-9])", "و ", c_["t"])   # «وCreator» read as «Creatorg»: a space after و
props = {"fps": FPS, "duration": round(dur, 3), "outW": 1920, "handles": "--handles" in sys.argv, "scenes": scenes, "hud": hud_r, "subs": SUBS, "caps": [c_ for c_ in caps if c_["a"] < dur],
         "faces": [{k: v for k, v in f_.items() if k != "n"} for f_ in FACES if f_["from"] < dur]}
if SUBP: props["sub"] = SUBP
json.dump(sorted(SFX, key=lambda x: x[1]), open("work/sfx_v9.json", "w"), indent=0)
out = "work/props_v9.json" if till > 1e8 else f"work/props_v9_till{int(till)}.json"
json.dump(props, open(out, "w", encoding="utf-8"), ensure_ascii=False)
print(out, len(scenes), "scenes", len(caps), "caps, total", TOTAL, "| missing", len(set(MISSING)), sorted(set(MISSING))[:5])

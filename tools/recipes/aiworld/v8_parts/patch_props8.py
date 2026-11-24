p = "work/scripts/make_props_v8.py"; s = open(p, encoding="utf-8").read()
def R(a, b, n=1):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b, n)
# song: handles bottom-left (note 52)
R('''            sc["items"].append({"k": "brand", "face": link(Path("assets/v7/logo_face_full.png"), "imgs"), "name": "brand/signature-calligraphy.png"})   # notes 17, 18''',
  '''            sc["items"].append({"k": "brand", "face": link(Path("assets/v7/logo_face_full.png"), "imgs"), "name": "brand/signature-calligraphy.png",
                                "handles": [{"logo": link(Path("../../brand/logos-tools/" + l_), "logos"), "t": t_} for l_, t_ in
                                            [("youtube.png", "@AlyShorosh"), ("tiktok.png", "@alyshorosh"), ("instagram.ico", "@alyshorosh"), ("facebook.png", "aly.shorosh")]]})   # v8 notes 51, 52''')
# note 5: consecutive SPLIT scenes showing the same pair = ONE scene (no second fade in/out)
R('''mm = []
for x in scenes:''', '''mm = []
for x in scenes:
    if mm and x["k"] == "SPLIT" and mm[-1]["k"] == "SPLIT" and x["start"] - (mm[-1]["start"] + mm[-1]["dur"]) < 0.8 \\
            and [d.get("cap") for d in x["items"]] == [d.get("cap") for d in mm[-1]["items"]]:
        mm[-1]["dur"] = round(x["start"] + x["dur"] - mm[-1]["start"], 3); continue''')
# note 54: the last map = him TALKING (the avatar clip of that second)
R('''        x["me"] = link("assets/v6/face_gen.jpg", "imgs")   # note 21: HIS picture, not the plane''',
  '''        x["me"] = link("assets/v6/face_gen.jpg", "imgs")   # note 21: HIS picture, not the plane
        for n_, (wa_, wb_) in AVW.items():   # v8 note 54: him TALKING there (clip second = voice second)
            for p_ in PIECES:
                if p_["kind"] != "v2": continue
                t2_ = p_["a"] + (x["start"] - p_["t"])
                if p_["t"] <= x["start"] <= p_["t"] + p_["b"] - p_["a"] and wa_ <= t2_ <= wb_ - 1.0:
                    x["me"] = avatar_src(n_, METH.get(n_, "gen")); x["meSkip"] = round(t2_ - wa_, 3)''')
# notes 17, 27, 35 + 2: face shots = a CIRCLE in a free spot of the board (full frame only over a plain clip); nothing held back under a circle
i0 = s.index("FACES = []")
i1 = s.index('print("faces:"', i0)
s = s[:i0] + '''FACES = []
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
    plain = all(x["k"] == "CLIP" for x in cover)
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
''' + s[i1:]
# tree: children of «مواقع التوليد» (note 26); separators: no sting/claps any more (note 3c) -> a soft whoosh until the kids voices exist (paid, pending)
R('''SUBS = [{"a": p["t"], "fam": p["sep"][0], "name": p["sep"][1], "b": (gaps[i + 1]["t"] if i + 1 < len(gaps) else TOTAL)} for i, p in enumerate(gaps)]''',
  '''SUBS = [{"a": p["t"], "fam": p["sep"][0], "name": p["sep"][1], "b": (gaps[i + 1]["t"] if i + 1 < len(gaps) else TOTAL)} for i, p in enumerate(gaps)]
for x in SUBS:
    if x["name"] in ("ElevenLabs", "Higgsfield", "Suno", "على جهازك ببلاش"): x["parent"] = "مواقع التوليد"''')
R('''[("aly_show_sting" if i == 0 else "aly_transition_a", x["a"] + (0.0 if i == 0 else 0.15)) for i, x in enumerate(SUBS)]''',
  '''[("whoosh_2", x["a"] + 0.1) for i, x in enumerate(SUBS)]''')
R('''props = {"fps": FPS, "duration": round(dur, 3), "outW": 1280,''', '''props = {"fps": FPS, "duration": round(dur, 3), "outW": 1920, "handles": "--handles" in sys.argv,''')
open(p, "w", encoding="utf-8").write(s); print("ok")

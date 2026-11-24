"""Apply the v5 explaining scenes (v5_specs.SPECS) onto the scene list from make_props_v5: cut the replaced range out of the scenes
(trimming the edges, clips keep their sync), insert one diagram board per spec, turn absolute times into frames, link the files."""
import json, re
from pathlib import Path
FPS = 25
ENV = json.load(open("work/voice_env_v5.json"))

def trim(sc, a, b):
    """keep only the part of scene sc OUTSIDE [a, b]; returns 0, 1 or 2 pieces"""
    s0, s1 = sc["start"], sc["start"] + sc["dur"]
    out = []
    for lo, hi in ((s0, min(s1, a)), (max(s0, b), s1)):
        if hi - lo < 0.04: continue
        x = json.loads(json.dumps(sc)); sh = lo - s0
        x["start"], x["dur"] = round(lo, 3), round(hi - lo, 3)
        cl = []
        for c in x["clips"]:
            c0, c1 = max(c["from"], lo), min(c["from"] + c["dur"], hi)
            if c1 - c0 > 0.04: cl.append({**c, "skip": round(c.get("skip", 0) + (c0 - c["from"]), 3), "from": round(c0, 3), "dur": round(c1 - c0, 3)})
        x["clips"] = cl
        df = int(round(sh * FPS)); end = int(x["dur"] * FPS)
        its = []
        for d in x["items"]:
            if "at" in d:
                d = {**d, "at": d["at"] - df}
                if "out" in d: d["out"] = d["out"] - df
                if d.get("out", end) < 0 or d["at"] > end: continue
                d["at"] = max(0, d["at"])
            its.append(d)
        x["items"] = its
        x["glitch"] = [g for g in x.get("glitch", []) if lo <= g < hi]
        if sh > 0 and x.get("title"): x["title"] = None   # the second half of a cut scene keeps no title (it was said before)
        out.append(x)
    return out

def convert(it, a, b, link):
    fr = lambda t: max(0, int(round((t - a) * FPS)))
    d = {k: v for k, v in it.items() if k not in ("t", "out_t", "act_t", "dim_t", "clean_t", "grow_t")}
    if it.get("grow_t") is not None: d["grow"] = fr(it["grow_t"])   # v7: full frame -> circle
    if it.get("hide"): d["hide"] = [[fr(x), fr(y)] for x, y in it["hide"]]   # v8: circle hidden while the looks / lip sync play
    d["at"] = fr(it["t"])
    if it.get("out_t") is not None: d["out"] = fr(it["out_t"])
    if it.get("act_t"): d["act"] = [fr(it["act_t"][0]), fr(it["act_t"][1])]
    if it.get("dim_t") is not None: d["dimAfter"] = fr(it["dim_t"])
    if it.get("clean_t") is not None: d["cleanAt"] = fr(it["clean_t"])
    if d.get("src"): d["src"] = link(d["src"], "v5")
    if d.get("logo"): d["logo"] = link(d["logo"], "logos")
    if d["k"] == "wave": d["env"] = ENV[int(a * FPS): int(b * FPS) + 2]
    if d["k"] == "num":   # enta counter + its paper label
        big = d.pop("big", False); lab = d.pop("label", None); to = d.pop("to"); suf = d.pop("suffix", "")
        o_ = d.get("out", int((b - a) * FPS) - 12)
        return [{"k": "num", "from": 0, "to": float(to), "x": d["x"], "y": d["y"] - 30, "size": 190 if big else 130, "dur": 20, "at": d["at"], "out": o_, "suffix": suf},
                {"k": "text", "text": lab, "x": d["x"], "y": d["y"] + (110 if big else 80), "size": 36, "paper": True, "at": d["at"] + 4, "out": o_}]
    return [d]

def apply(scenes, specs, link):
    specs = sorted(specs, key=lambda x: x["a"])
    for i in range(len(specs) - 1):   # overlapping specs: the earlier one ends where the next begins
        specs[i]["b"] = min(specs[i]["b"], specs[i + 1]["a"])
    for sp in specs:
        a, b = sp["a"], sp["b"]
        new = []
        for sc in scenes:
            if sc["start"] + sc["dur"] <= a or sc["start"] >= b: new.append(sc)
            else: new += trim(sc, a, b)
        items = []
        for it in sp["items"]: items += convert(it, a, b, link)
        if sp["title"]: items.append({"k": "titleAt", "at": max(0, int(round(((sp["title_t"] or a) - a) * FPS)))})
        new.append({"k": "BOARD", "start": a, "dur": round(b - a, 3), "title": sp["title"], "clips": [], "items": items, "words": [], "glitch": [], "fam": [], "fx": None})
        scenes = sorted(new, key=lambda x: x["start"])
    return scenes

def shift_items(sc, df):
    for d in sc["items"]:
        if "at" in d: d["at"] = max(0, d["at"] + df)
        if "out" in d: d["out"] = d["out"] + df
        for k in ("act",):
            if k in d: d[k] = [d[k][0] + df, d[k][1] + df]
        for k in ("dimAfter", "cleanAt"):
            if k in d: d[k] = d[k] + df

def fix_short(scenes, min_board=3.2):
    """note 20: nothing on screen for less than ~3 s. (1) crumbs < 1.2 s left by the inserts join the next board (or the previous scene);
    (2) a short board takes time from the avatar/clip scene after it (the avatar just starts later, lip sync kept by skip)."""
    out = []
    for i, sc in enumerate(scenes):
        nxt = scenes[i + 1] if i + 1 < len(scenes) else None
        if sc["dur"] < 1.2 and (sc["k"] != "AV" or sc["dur"] < 0.5):
            if nxt is not None and nxt["k"] == "BOARD":
                df = int(round(sc["dur"] * FPS)); nxt["start"] = sc["start"]; nxt["dur"] = round(nxt["dur"] + sc["dur"], 3); shift_items(nxt, df)
            elif out:
                out[-1]["dur"] = round(out[-1]["dur"] + sc["dur"], 3)
                if out[-1]["clips"]: out[-1]["clips"][-1]["dur"] = round(out[-1]["clips"][-1]["dur"] + sc["dur"], 3)
            continue
        out.append(sc)
    for i, sc in enumerate(out[:-1]):
        nxt = out[i + 1]
        if sc["k"] in ("BOARD", "WEB", "SPLIT") and sc["dur"] < min_board and nxt["k"] in ("AV", "CLIP") and nxt["dur"] > 2 + (min_board - sc["dur"]):
            d = round(min_board - sc["dur"], 3); old_end = int(sc["dur"] * FPS) - 12
            sc["dur"] = round(sc["dur"] + d, 3); new_end = int(sc["dur"] * FPS) - 12
            for it in sc["items"]:
                if it.get("out") == old_end: it["out"] = new_end
            nxt["start"] = round(nxt["start"] + d, 3); nxt["dur"] = round(nxt["dur"] - d, 3)
            cl = []
            for c in nxt["clips"]:
                c0 = max(c["from"], nxt["start"]); c1 = c["from"] + c["dur"]
                if c1 - c0 > 0.04: cl.append({**c, "skip": round(c.get("skip", 0) + (c0 - c["from"]), 3), "from": round(c0, 3), "dur": round(c1 - c0, 3)})
            nxt["clips"] = cl; shift_items(nxt, -int(round(d * FPS)))
    return out

from v5_boxes import boxes, inter
SAFE = (96, 110, 1824, 925)
MOVABLE = ("pic", "logo", "text", "chip", "num", "emo", "sticker")
def _groups(items):
    gs = []
    for d in items:
        if d.get("x") is None or d["k"] not in MOVABLE: continue
        prev = gs[-1][-1] if gs else None
        if d.get("qr"):   # a QR goes with ITS thumbnail (same x, 6 frames later)
            own = next((g for g in gs if g[0]["k"] == "pic" and abs(g[0]["x"] - d["x"]) < 1 and g[0]["at"] == d["at"] - 6), None)
            (own if own is not None else gs[-1] if gs else gs).append(d) if (own is not None or gs) else gs.append([d])
        elif prev is not None and d["k"] == "text" and prev["k"] in ("logo", "num") and abs(d["x"] - prev["x"]) < 1:
            gs[-1].append(d)
        else: gs.append([d])
    return gs
def _box(g, end):
    bx = [b for d in g for b in boxes(d, end)]
    return (min(b[0] for b in bx), min(b[1] for b in bx), max(b[2] for b in bx), max(b[3] for b in bx)) if bx else None
def _win(g, end): return (min(d["at"] for d in g), max(min(d.get("out", end) + 10, end) for d in g))
def resolve(scenes):
    """per scene: every group of kit items is kept inside the safe area and away from the groups shown at the same time
    (the hand-placed diagram nodes of v5 count as fixed obstacles). Tries small vertical / horizontal moves first."""
    left = []
    for s in scenes:
        end = int(s["dur"] * FPS)
        fixed = [(b, (d.get("at", 0), min(d.get("out", end) + 10, end))) for d in s["items"] if d["k"] in ("node", "bar", "typed", "wave", "scan") for b in boxes(d, end)]
        if s.get("title"):
            fixed.append(((560, 120, 1360, 205), (0, end)))
        placed = []
        for g in sorted(_groups(s["items"]), key=lambda g: g[0]["at"]):
            bx = _box(g, end)
            if not bx: continue
            win = _win(g, end)
            def ok(b):
                if b[0] < SAFE[0] or b[1] < SAFE[1] or b[2] > SAFE[2] or b[3] > SAFE[3]: return False
                for ob, ow in fixed + placed:
                    if ow[0] < win[1] and win[0] < ow[1] and inter(b, ob) > 0: return False
                return True
            # clamp into the safe area first
            cx = max(SAFE[0] - bx[0], 0) - max(bx[2] - SAFE[2], 0); cy = max(SAFE[1] - bx[1], 0) - max(bx[3] - SAFE[3], 0)
            best = None
            for dy in [0, 60, -60, 120, -120, 180, -180, 240, -240, 320, -320, 400, -400]:
                for dx in [0, 140, -140, 280, -280, 420, -420]:
                    b = (bx[0] + cx + dx, bx[1] + cy + dy, bx[2] + cx + dx, bx[3] + cy + dy)
                    if ok(b): best = (cx + dx, cy + dy, b); break
                if best: break
            if best is None:   # shrink a little and keep it in the safe area
                for d in g: d["scale"] = round(d.get("scale", 1) * 0.8, 3)
                bx2 = _box(g, end); best = (cx, cy, (bx2[0] + cx, bx2[1] + cy, bx2[2] + cx, bx2[3] + cy))
                left.append((round(s["start"], 1), g[0]["k"], str(g[0].get("text") or g[0].get("cap") or "")[:20]))
            for d in g: d["x"] = round(d["x"] + best[0]); d["y"] = round(d["y"] + best[1])
            placed.append((best[2], win))
    return left

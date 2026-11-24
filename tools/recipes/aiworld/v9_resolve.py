"""GENERAL overlap rule (Aly 2026-11-23: «take care from overlaps, make sure it is a general rule»).
After every other placement step: every item with a box (nodes too — the hand-placed diagram cards were never checked before)
must not overlap anything shown at the same time, and must sit inside the safe area. The item that ENTERS LATER moves
(its arrows' ends move with it) to the nearest free spot; if no spot is free it shrinks a little and tries again.
A hand-over (one leaves as the other comes, < 8 frames together) is not an overlap. Returns what could not be fixed."""
from v5_boxes import boxes, inter
SAFE = (96, 110, 1824, 925)
SKIP = ("titleAt", "line", "brand", "subscribe", "circle", "edge", "sep", "split", "diff", "page")
STEPS = [(0, 0)] + [(dx, dy) for r in (40, 80, 120, 170, 230, 300, 380) for dx, dy in
                    ((0, r), (0, -r), (r, 0), (-r, 0), (r, r), (-r, r), (r, -r), (-r, -r))]

def _bx(d, end):
    b = boxes(d, end)
    return (min(x[0] for x in b), min(x[1] for x in b), max(x[2] for x in b), max(x[3] for x in b)) if b else None

def _hit(a, b):
    ov = inter(a, b); sm = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
    return sm > 0 and ov / sm > 0.005

def _move(d, dx, dy, edges, box, end=10 ** 6):
    d["x"] = round(d["x"] + dx); d["y"] = round(d["y"] + dy)
    a0, o0 = d.get("at", 0), min(d.get("out", end), end)
    for e in edges:   # arrow ends that touch this card follow it — only arrows on screen WITH this card
        if not (a0 - 8 <= e.get("at", 0) <= o0): continue
        p = e["pts"]
        for i in (0, 2):
            if box[0] - 60 <= p[i] <= box[2] + 60 and box[1] - 60 <= p[i + 1] <= box[3] + 60: p[i] += dx; p[i + 1] += dy

def resolve_all(scenes, title_box=(560, 120, 1360, 205)):
    left = []
    for s in scenes:
        end = int(s["dur"] * 25)
        edges = [d for d in s["items"] if d["k"] == "edge" and d.get("pts")]
        its = sorted([d for d in s["items"] if d["k"] not in SKIP and d.get("x") is not None and "at" in d], key=lambda d: d["at"])
        placed = []   # (box, at, out)
        if s.get("title"): placed.append((title_box, 0, end))
        for d in its:
            box = _bx(d, end)
            if not box: continue
            at, out = d["at"], min(d.get("out", end), end)
            def ok(b):
                if b[0] < SAFE[0] or b[1] < SAFE[1] or b[2] > SAFE[2] or b[3] > SAFE[3]: return False
                return not any(min(out, o2) - max(at, a2) >= 8 and _hit(b, ob) for ob, a2, o2 in placed)
            if ok(box) or "y" not in d: placed.append((box, at, out)); continue   # bars (no y) stay where they are: the others move around them
            done = False
            for shrink in (1.0, 0.85, 0.72):
                if shrink < 1.0:
                    if d.get("w"): d["w"] = round(d["w"] * 0.85)
                    else: d["scale"] = round(d.get("scale", 1) * 0.85, 3)
                    box = _bx(d, end)
                # clamp into the safe area first, then search around
                cx = max(SAFE[0] - box[0], 0) - max(box[2] - SAFE[2], 0); cy = max(SAFE[1] - box[1], 0) - max(box[3] - SAFE[3], 0)
                for dx, dy in STEPS:
                    b = (box[0] + cx + dx, box[1] + cy + dy, box[2] + cx + dx, box[3] + cy + dy)
                    if ok(b):
                        _move(d, cx + dx, cy + dy, edges, box, end); placed.append((b, at, out)); done = True; break
                if done: break
            if not done:
                placed.append((_bx(d, end), at, out))
                left.append((round(s["start"] + at / 25, 1), d["k"], str(d.get("label") or d.get("text") or d.get("cap") or d.get("src") or "")[:30]))
    return left

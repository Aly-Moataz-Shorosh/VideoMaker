"""Aly (2026-11-22): «خلي بالك من ال overlap». Approximate boxes of everything shown at the same moment in props_v5.json:
reports pairs that overlap and anything outside the safe area (x 96..1824, y 100..930). Usage: python -X utf8 work/scripts/check_overlap_v9.py <props>"""
import json, sys
sys.path.insert(0, "work/scripts")

P = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "work/props_v5.json", encoding="utf-8"))
from v5_boxes import tw, boxes, inter
fm = lambda t: "%d:%04.1f" % (t // 60, t % 60)
issues = []
for s in P["scenes"]:
    end = int(s["dur"] * 25)
    its = [d for d in s["items"] if d.get("x") is not None and d["k"] != "edge"]
    if s.get("title"):
        ta = next((d["at"] for d in s["items"] if d["k"] == "titleAt"), 3); w = tw(s["title"], 42)
        its.append({"k": "title", "at": ta, "_b": [(960 - w / 2, 128, 960 + w / 2, 196)]})
    for f in range(0, end, 12):
        vis = [d for d in its if d["at"] <= f < min(d.get("out", end) + 10, end)]
        bx = [(d, b) for d in vis for b in (d.get("_b") or boxes(d, end))]
        for i in range(len(bx)):
            for j in range(i + 1, len(bx)):
                if bx[i][0] is bx[j][0]: continue
                di, dj = bx[i][0], bx[j][0]
                oi, oj = min(di.get("out", end), end), min(dj.get("out", end), end)
                if min(oi, oj) - max(di["at"], dj["at"]) < 8: continue   # a hand-over (one leaves as the other comes) is not an overlap
                a, b = bx[i][1], bx[j][1]
                ov = inter(a, b); sm = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
                if sm > 0 and ov / sm > 0.08:
                    key = (fm(s["start"]), bx[i][0]["k"], str(bx[i][0].get("label") or bx[i][0].get("text") or bx[i][0].get("cap") or "")[:22],
                           bx[j][0]["k"], str(bx[j][0].get("label") or bx[j][0].get("text") or bx[j][0].get("cap") or "")[:22])
                    if key not in issues: issues.append(key)
        for d, b in bx:
            if d["k"] != "title" and (b[0] < 96 or b[2] > 1824 or b[1] < 100 or b[3] > 930):
                key = (fm(s["start"]), "OUT", d["k"], str(d.get("label") or d.get("text") or d.get("cap") or d.get("src", ""))[-26:], [round(v) for v in b])
                if key not in issues: issues.append(key)
print(len(issues), "issues")
for x in issues: print(x)

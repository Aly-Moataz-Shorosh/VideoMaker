"""Smart v11 render plan (Aly 2026-11-24: «متعيدش الموشن من الاول غير للحاجات اللي محتاجنها»).
Before the first timeline change (the new N1b lines) v10 and v11 share the same seconds, so a v11 scene that is IDENTICAL to the v10 scene
at the same time (scene JSON + the captions / faces / breadcrumb / hud inside its window) is cut from the v10 picture (D:/Temp/aiw10_chunks).
Everything else is rendered. After the first change everything is rendered (the star background runs on video time: reused footage would jump).
Writes work/redo_v11.json = [{"src": "v10"|"new", "a": frame, "b": frame (exclusive)}...]. Usage (project folder): python -X utf8 work/scripts/redo_v11.py"""
import json, re
FPS = 25
P10 = json.load(open("work/props_v10.json", encoding="utf-8")); P11 = json.load(open("work/props_v11.json", encoding="utf-8"))
T10 = json.load(open("work/timeline_v10.json", encoding="utf-8"))["pieces"]; T11 = json.load(open("work/timeline_v11.json", encoding="utf-8"))["pieces"]
# first second where the two timelines differ
SAME_UNTIL = 0.0
for p, q in zip(T10, T11):
    if p.get("kind") != q.get("kind") or p.get("sids") != q.get("sids") or abs(p["t"] - q["t"]) > 1e-3 or abs(p.get("dur", 0) - q.get("dur", 0)) > 1e-3: break
    SAME_UNTIL = q["t"] + (q["dur"] if q["kind"] in ("gap", "hold") else q["b"] - q["a"])
SAME_UNTIL -= 0.5   # safety: the last shared piece's board may run into the change
def window(P, a, b):
    """everything drawn in [a, b): the scene(s) + global layers, made RELATIVE to a"""
    r = lambda t: round(t - a, 3)
    sc = [{**{k: v for k, v in s.items() if k != "start"}, "rs": r(s["start"]),
           "clips": [{**c, "from": r(c["from"])} for c in s.get("clips", [])]} for s in P["scenes"] if s["start"] < b and s["start"] + s["dur"] > a]
    caps = [{**c, "a": r(c["a"]), "b": r(c["b"])} for c in P["caps"] if c["a"] < b and c["b"] > a]
    faces = [{**f, "from": r(f["from"])} for f in P["faces"] if f["from"] < b and f["from"] + f["dur"] > a]
    L = round(b - a, 3); cl = lambda v: min(r(v), L + 1.0)   # an end far after the window does not change what is drawn inside it
    subs = [{**s, "a": r(s["a"]), "b": cl(s["b"])} for s in P.get("subs", []) if s["a"] < b and s["b"] > a]
    hud = [{**h, "a": r(h["a"]), **({"b": cl(h["b"])} if "b" in h else {})} for h in P.get("hud", []) if isinstance(h, dict) and h.get("a", -1) < b and h.get("b", 1e9) > a]
    return json.dumps([sc, caps, faces, subs, hud], sort_keys=True, ensure_ascii=False)
segs = []
for s in sorted(P11["scenes"], key=lambda s: s["start"]):
    a, b = s["start"], s["start"] + s["dur"]
    fa, fb = round(a * FPS), round(b * FPS)
    en_only = any(isinstance(d.get(k_), str) and re.search(r"[A-Za-z]", d[k_]) and not re.search(r"[؀-ۿ]", d[k_])
                  for d in s.get("items", []) if d.get("k") == "node" for k_ in ("label", "sub"))   # V11 draws these left-to-right now -> render
    same = b <= SAME_UNTIL and not en_only and window(P10, a, b) == window(P11, a, b)
    src = "v10" if same else "new"
    if segs and segs[-1]["src"] == src and segs[-1]["b"] == fa: segs[-1]["b"] = fb
    else: segs.append({"src": src, "a": fa, "b": fb})
N = round(P11["duration"] * FPS); segs[-1]["b"] = N
assert segs[0]["a"] == 0 and all(x["b"] == y["a"] for x, y in zip(segs, segs[1:])), "gaps in the plan"
json.dump(segs, open("work/redo_v11.json", "w"), indent=0)
new = sum(x["b"] - x["a"] for x in segs if x["src"] == "new"); reuse = N - new
print(f"timeline identical until {SAME_UNTIL:.1f} s | {len(segs)} segments | reused from v10: {reuse / FPS:.0f} s | rendered: {new / FPS:.0f} s of {N / FPS:.0f} s")
for x in segs: print(f"  {x['src']:4} {x['a'] / FPS:8.2f} -> {x['b'] / FPS:8.2f}")
